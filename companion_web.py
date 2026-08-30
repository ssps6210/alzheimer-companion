#!/usr/bin/env python3
"""
爺爺語音陪伴系統 - 網頁版
平板 Chrome 開啟 http://<PC-IP>:8080
"""
import os, sys
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["PYTHONUTF8"] = "1"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load .env file if present (won't override existing env vars)
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    for _line in open(_env_path, encoding="utf-8"):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            if _k.strip() not in os.environ:
                os.environ[_k.strip()] = _v.strip()

import socket
import io
import json
import time
import re
import uuid
import asyncio
import urllib.parse
import numpy as np
import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from faster_whisper import WhisperModel
import uvicorn

# Fallback TTS when CosyVoice errors or WSL2 is unreachable — keeps the system
# audible (silence ≈ "broken" for 爺爺). Degrades gracefully if not installed.
try:
    import edge_tts
except ImportError:
    edge_tts = None

# App「自動尋找電腦」用：在區網廣播 mDNS，讓 Android NsdManager 找得到，免打 IP。
# 裝不了就靜靜跳過——App 會自動退回手動輸入網址，不影響其他功能。
try:
    from zeroconf import ServiceInfo, Zeroconf
except ImportError:
    Zeroconf = None

# /setup 頁的 QR code（App 掃碼連線用）。裝不了就這支端點回 501，頁面上退回純文字網址+複製按鈕。
try:
    import qrcode
    import qrcode.image.svg
except ImportError:
    qrcode = None

WEEKDAYS_ZH  = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PHRASES_DIR  = os.path.join(SCRIPT_DIR, "phrases")  # 固定句音檔 + phrases.json
PHOTOS_DIR   = os.path.join(SCRIPT_DIR, "photos")   # 爺爺老照片：閒置懷舊輪播（放 jpg/png 進去就會播）
UI_STATE_FILE= os.path.join(SCRIPT_DIR, "ui_state.json")  # 家人在 Setup 台設的預設（目前：說話模式）

def _load_talk_mode():
    try:
        m = json.load(open(UI_STATE_FILE, encoding="utf-8")).get("talk_mode", "hold")
        return m if m in ("hold", "auto") else "hold"   # validate: value is injected into JS
    except Exception:
        return "hold"

DEFAULT_TALK_MODE = _load_talk_mode()   # 'hold'=按住說話 / 'auto'=自動連續對話（爺爺畫面預設；本機可覆蓋）
TTS_CACHE_MAX = 64

# ── 聲音同意閘門（防冒用）：設定克隆音色前，錄音本人須先唸出同意聲明 ─────────
# 這句會被 whisper 轉出來、比對關鍵詞；由於同意句就在同一段錄音裡，說話者＝同意者，
# 把「同意」牢牢綁在「這個聲音」上。CONSENT_REQUIRED=0 可關（進階／本機用）。
CONSENT_REQUIRED = os.environ.get("CONSENT_REQUIRED", "1") != "0"
CONSENT_PHRASE   = "我同意用我的聲音陪伴家人"
CONSENT_KEYS     = ("同意", "陪伴")   # 兩個夠獨特的詞都出現才算通過（容忍 ASR 誤差、繁簡差異）

PORT = int(os.environ.get("COMPANION_PORT", 8080))

# ── Config (borrow Open-LLM-VTuber's config-driven pluggable pattern) ─────────
# All knobs live in conf.yaml; secrets (API key) stay in env vars. Falls back to
# these DEFAULTS if conf.yaml or pyyaml is missing — behaviour is unchanged.
try:
    import yaml
except ImportError:
    yaml = None

DEFAULTS = {
    "asr":   {"model": "medium", "device": "cuda", "compute_type": "float16", "language": "zh"},
    "llm":   {"base_url": "https://token-plan-ams.xiaomimimo.com/v1", "model": "mimo-v2.5",
              "api_key_env": "MIMO_API_KEY", "temperature": 0.7, "max_tokens": 150,
              "timeout": 25, "disable_thinking": True},
    "tts":   {"cosyvoice_url": "http://localhost:50000/tts",
              "cosyvoice_health": "http://localhost:50000/health",
              "cosyvoice_timeout": 15, "edge_voice": "zh-TW-YunJheNeural"},
    "memory": {"max_history": 10, "persist": True, "summary_trigger": 24},
    "notify": {"telegram_token_env": "TELEGRAM_BOT_TOKEN",
               "telegram_chat_env": "TELEGRAM_CHAT_ID",
               "daily_summary_hour": 20},   # 每天幾點寄摘要給家人；-1 = 關閉
    "active_character": "grandson",
    "characters": {"grandson": {"cosyvoice_spk": "family", "persona": (
        "你是爺爺最親近的家人，用親暱的口吻陪伴患有記憶力困難的爺爺。\n"
        "{date_line}\n\n"
        "你的原則：\n"
        "1. 每次只說1到3句話，語言簡單易懂，語氣自然親暱，像家人跟爺爺說話\n"
        "2. 不要用敬語或客套話，說話像家人不像服務員\n"
        "3. 爺爺重複問問題，永遠耐心重新回答，絕不說「我剛才說過了」\n"
        "4. 聽不懂時，溫柔說：「爺爺，可以再說一次嗎？」\n"
        "5. 多說溫暖鼓勵的話，讓爺爺感到被愛\n"
        "6. 稱對方為「爺爺」；說到自己一律用「我」，不要自稱孫子或任何特定身分\n"
        "7. 以台灣國語、台灣慣用語回答（避免大陸用詞）\n"
        "8. 不催促、不糾正、不讓爺爺感到難堪\n"
        "9. 被問到吃藥吃飯喝水，溫柔提醒\n"
        "10. 不主動提起爺爺的私事或家人細節（身邊可能有外人），只溫柔回應他當下說的\n"
        "11. 爺爺找已過世或不在身邊的親人時，不要說對方走了、也不糾正，溫柔讓他安心，再自然把話題帶開\n"
        "12. 遇到不確定的人名或私事，不要編造，溫柔帶過就好\n"
        "13. 回答要像說話一樣自然，不要有列表或特殊符號")}},
}

def _deep_merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        out[k] = _deep_merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out

def load_config():
    path = os.path.join(SCRIPT_DIR, "conf.yaml")
    if yaml and os.path.exists(path):
        try:
            cfg = _deep_merge(DEFAULTS, yaml.safe_load(open(path, encoding="utf-8")) or {})
            print(f"設定檔載入：{path}")
            return cfg
        except Exception as e:
            print(f"conf.yaml 讀取失敗，改用內建預設：{e}")
    return DEFAULTS

CFG = load_config()

# Derive the original module-level names from CFG so downstream code is untouched.
WHISPER_SIZE   = CFG["asr"]["model"]
WHISPER_DEVICE = CFG["asr"]["device"]
WHISPER_CTYPE  = CFG["asr"]["compute_type"]
ASR_LANG       = CFG["asr"]["language"]
MIMO_BASE_URL  = CFG["llm"]["base_url"]
MIMO_MODEL     = CFG["llm"]["model"]
MIMO_API_KEY   = os.environ.get(CFG["llm"]["api_key_env"], "")
LLM_TEMP       = CFG["llm"]["temperature"]
LLM_MAXTOK     = CFG["llm"]["max_tokens"]
LLM_TIMEOUT    = CFG["llm"]["timeout"]
LLM_NOTHINK    = CFG["llm"]["disable_thinking"]
COSY_URL       = CFG["tts"]["cosyvoice_url"]
COSY_HEALTH    = CFG["tts"]["cosyvoice_health"]
COSY_TIMEOUT   = CFG["tts"]["cosyvoice_timeout"]
EDGE_VOICE     = CFG["tts"]["edge_voice"]
MAX_HISTORY    = CFG["memory"]["max_history"]
MEM_PERSIST    = CFG["memory"].get("persist", True)
MEM_SUMMARY_TRIGGER = CFG["memory"].get("summary_trigger", 24)
MEMORY_FILE    = os.path.join(SCRIPT_DIR, "memory.json")

_notify_cfg    = CFG.get("notify", {})
TELEGRAM_TOKEN = os.environ.get(_notify_cfg.get("telegram_token_env", "TELEGRAM_BOT_TOKEN"), "")
TELEGRAM_CHAT  = os.environ.get(_notify_cfg.get("telegram_chat_env", "TELEGRAM_CHAT_ID"), "")
DAILY_SUMMARY_HOUR = _notify_cfg.get("daily_summary_hour", 20)

# #4 guard: a typo'd active_character must not crash startup.
_chars  = CFG["characters"]
_active = CFG["active_character"]
if _active not in _chars:
    print(f"⚠ active_character '{_active}' 不在 characters 裡，改用預設角色")
    _active = next(iter(_chars)) if _chars else "grandson"
CHARACTER = _chars.get(_active) or DEFAULTS["characters"]["grandson"]

# #1: frontend abort must exceed backend worst case (MiMo + CosyVoice + whisper
# margin), else the client cancels a request the server is still completing.
CLIENT_TIMEOUT_MS = (LLM_TIMEOUT + COSY_TIMEOUT + 15) * 1000

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
    allow_headers=["*"], expose_headers=["X-User-Text", "X-Reply-Text"]
)

whisper = None
history = []
session_summary = ""   # 滾動長期記憶筆記（背景由 LLM 濃縮）
_summarizing = False   # 防止重疊的摘要任務
_bg_tasks = set()      # 強引用背景任務，避免被 GC 中途回收
PHRASES = []     # [{triggers:[...], audio:bytes, media:str, text:str}]
tts_cache = {}   # reply_text -> (audio_bytes, media)  小型 LRU


_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "←-⇿⬀-⯿️]")

def _sanitize_reply(s):
    # 爺爺 hears this via TTS — strip emoji / markdown so nothing weird is read
    # aloud (LLM occasionally adds 🌞 or markdown despite the persona rule).
    s = _EMOJI_RE.sub("", s)
    s = re.sub(r"[*#`_>~]", "", s)
    s = re.sub(r"[ \t]{2,}", " ", s)
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return s


def get_system_prompt():
    # Persona comes from the active character (conf.yaml); we only inject the
    # live date/time into its {date_line} slot. Output is identical to before.
    now = datetime.now()
    hour = now.hour
    # 0-4 點要講「凌晨」不是「下午」（失智長者半夜常問時間，不能餵錯給 LLM）
    tod = ("凌晨" if hour < 5 else "早上" if hour < 12 else
           "中午" if hour == 12 else "下午" if hour < 18 else "晚上")
    h12 = hour % 12 or 12   # 24h → 12h：說「晚上8點」不說「晚上20點」
    date_line = (f"今天是{now.year}年{now.month}月{now.day}日"
                 f"{WEEKDAYS_ZH[now.weekday()]}，現在是{tod}{h12}點。")
    prompt = CHARACTER["persona"].replace("{date_line}", date_line)
    if session_summary:
        prompt += ("\n\n（以下是你對爺爺的長期記憶，自然地融入關心即可；"
                   "不要主動提起他說過的話、也不要考他記不記得）：\n" + session_summary)
    return prompt


async def edge_tts_synth(text):
    """Fallback TTS → MP3 bytes (browsers decode MP3 via decodeAudioData)."""
    if edge_tts is None:
        raise RuntimeError("edge-tts not installed (pip install edge-tts)")
    comm = edge_tts.Communicate(text, EDGE_VOICE)
    buf = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            buf.extend(chunk["data"])
    if not buf:
        raise RuntimeError("edge-tts returned no audio")
    return bytes(buf)


def _audio_response(content, media_type, text, reply):
    # URL-encode headers: HTTP headers must be ASCII
    return Response(
        content=content, media_type=media_type,
        headers={
            "X-User-Text": urllib.parse.quote(text),
            "X-Reply-Text": urllib.parse.quote(reply),
        },
    )


def load_phrases():
    """Preload fixed-phrase audio into memory for instant, LLM/TTS-free replies."""
    PHRASES.clear()
    cfg = os.path.join(PHRASES_DIR, "phrases.json")
    if not os.path.exists(cfg):
        print(f"（無固定句設定 {cfg}，跳過快取層）")
        return
    try:
        rules = json.load(open(cfg, encoding="utf-8"))
    except Exception as e:
        print(f"phrases.json 讀取失敗，跳過：{e}")
        return
    for rule in rules:
        f = os.path.join(PHRASES_DIR, rule.get("file", ""))
        if not rule.get("triggers") or not os.path.exists(f):
            print(f"⚠ 固定句略過（缺 triggers 或音檔不存在）：{rule.get('file')}")
            continue
        with open(f, "rb") as fh:
            PHRASES.append({
                "triggers": rule["triggers"],
                "audio": fh.read(),
                "media": "audio/mpeg" if f.lower().endswith(".mp3") else "audio/wav",
                "text": rule.get("text", ""),
                "alert": rule.get("alert", False),   # True → 命中時通知家人
            })
    print(f"固定句快取：載入 {len(PHRASES)} 條")


_NEGATION = ("不", "沒", "別", "未", "甭")

def match_phrase(text):
    """First rule with a trigger that appears AND is not immediately negated wins.
    Substring match, but a hit is skipped if the char just before it is a negation
    (不痛 / 沒事 / 別怕…) to avoid the obvious false positives. If every occurrence
    of a trigger is negated, that rule is skipped."""
    for p in PHRASES:
        for t in p["triggers"]:
            if not t:
                continue
            i = text.find(t)
            while i != -1:
                if i == 0 or text[i - 1] not in _NEGATION:
                    return p
                i = text.find(t, i + 1)
    return None


def _tts_cache_put(key, audio, media):
    if len(tts_cache) >= TTS_CACHE_MAX:
        tts_cache.pop(next(iter(tts_cache)))  # drop oldest
    tts_cache[key] = (audio, media)


def load_memory():
    """Restore recent turns + long-term summary so a restart doesn't wipe context."""
    global history, session_summary
    if not MEM_PERSIST or not os.path.exists(MEMORY_FILE):
        return
    try:
        d = json.load(open(MEMORY_FILE, encoding="utf-8"))
        history = d.get("history", []) or []
        session_summary = d.get("summary", "") or ""
        print(f"記憶載入：近期 {len(history)} 則、摘要 {len(session_summary)} 字")
    except Exception as e:
        print(f"記憶載入失敗（忽略）：{e}")


def save_memory():
    if not MEM_PERSIST:
        return
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history, "summary": session_summary}, f, ensure_ascii=False)
    except Exception as e:
        print(f"記憶儲存失敗（忽略）：{e}")


def _remember(user_text, reply_text):
    """Append a turn, persist it, and fold older turns into the summary when long."""
    history.append({"role": "user", "content": user_text})
    if reply_text:
        history.append({"role": "assistant", "content": reply_text})
    save_memory()
    if MEM_SUMMARY_TRIGGER and len(history) > MEM_SUMMARY_TRIGGER and not _summarizing:
        fold = list(history[:-MAX_HISTORY])   # older turns beyond the recent window
        del history[:-MAX_HISTORY]            # keep only the recent window in context
        save_memory()
        try:
            task = asyncio.create_task(_fold_and_summarize(fold, session_summary))
            _bg_tasks.add(task)                       # strong ref so it isn't GC'd
            task.add_done_callback(_bg_tasks.discard)
        except RuntimeError:
            pass  # no running loop (shouldn't happen from the async handler)


async def _fold_and_summarize(fold_msgs, prev_summary):
    """Compress older turns into a compact long-term note. Background, best-effort —
    never on 爺爺's reply path, and any failure is swallowed."""
    global session_summary, _summarizing
    _summarizing = True
    try:
        convo = "\n".join(f"{'爺爺' if m['role'] == 'user' else '我'}：{m['content']}"
                          for m in fold_msgs)
        prompt = ("把對話濃縮成一段給陪伴AI的長期記憶筆記（150字內）："
                  "記住關於爺爺的穩定事實、他關心的事、提到的人，用簡短短句，不要流水帳。\n\n"
                  f"目前筆記：{prev_summary or '（無）'}\n\n新對話：\n{convo}\n\n更新後的筆記：")
        body = {"model": MIMO_MODEL, "messages": [{"role": "user", "content": prompt}],
                "stream": False, "temperature": 0.3, "max_tokens": 220}
        if LLM_NOTHINK:
            body["chat_template_kwargs"] = {"enable_thinking": False}
        r = await run_in_threadpool(lambda: requests.post(
            f"{MIMO_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {MIMO_API_KEY}"},
            json=body, timeout=LLM_TIMEOUT))
        r.raise_for_status()
        new_summary = (r.json()["choices"][0]["message"].get("content") or "").strip()
        if new_summary:
            session_summary = new_summary[:600]
            save_memory()
            print(f"［長期記憶更新］{session_summary[:40]}…")
    except Exception as e:
        print(f"記憶摘要失敗（忽略）：{e}")
    finally:
        _summarizing = False


async def notify_family(text):
    """Push a message to family via Telegram. Best-effort; no-op if unconfigured."""
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT):
        return
    try:
        await run_in_threadpool(lambda: requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": text}, timeout=10))
        print(f"［已通知家人］{text[:40]}")
    except Exception as e:
        print(f"通知家人失敗（忽略）：{e}")


def _fire_bg(coro):
    """Run a fire-and-forget coroutine while keeping a strong ref (no GC)."""
    try:
        t = asyncio.create_task(coro)
        _bg_tasks.add(t); t.add_done_callback(_bg_tasks.discard)
    except RuntimeError:
        pass


async def _daily_summary_text():
    """Ask MiMo for a short, warm daily update for family from today's memory."""
    if not history and not session_summary:
        return ""
    convo = "\n".join(f"{'爺爺' if m['role']=='user' else '陪伴'}：{m['content']}"
                      for m in history[-20:])
    prompt = ("根據以下今天的對話與長期記憶，寫一段給家人的簡短關懷摘要（100字內）："
              "爺爺今天聊了什麼、心情如何、有沒有需要注意的（不適/情緒/重複擔心的事）。"
              "用平實中文，不要客套。\n\n"
              f"長期記憶：{session_summary or '（無）'}\n\n今天對話：\n{convo}\n\n摘要：")
    body = {"model": MIMO_MODEL, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "temperature": 0.4, "max_tokens": 200}
    if LLM_NOTHINK:
        body["chat_template_kwargs"] = {"enable_thinking": False}
    r = await run_in_threadpool(lambda: requests.post(
        f"{MIMO_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {MIMO_API_KEY}"}, json=body, timeout=LLM_TIMEOUT))
    r.raise_for_status()
    return (r.json()["choices"][0]["message"].get("content") or "").strip()


async def daily_summary_loop():
    """Once a day at DAILY_SUMMARY_HOUR, send a conversation summary to family."""
    if DAILY_SUMMARY_HOUR is None or DAILY_SUMMARY_HOUR < 0:
        return
    while True:
        now = datetime.now()
        target = now.replace(hour=DAILY_SUMMARY_HOUR, minute=0, second=0, microsecond=0)
        if target <= now:
            target += timedelta(days=1)
        await asyncio.sleep((target - now).total_seconds())
        try:
            s = await _daily_summary_text()
            if s:
                await notify_family(f"📋 爺爺今日摘要（{datetime.now():%m/%d}）\n{s}")
        except Exception as e:
            print(f"每日摘要失敗（忽略）：{e}")


def _advertise_mdns():
    """在區網廣播這台電腦，讓 App 的「自動尋找電腦」不用手打 IP。
    純加分項：裝不了 zeroconf、找不到區網 IP，都只印一行提示、不影響其他任何功能。"""
    if Zeroconf is None:
        print("mDNS 廣播未啟用（缺 zeroconf，App 自動尋找功能會找不到；pip install zeroconf 可補上）")
        return None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))   # 不會真的送出封包，只是借系統路由表問「我對外的 IP 是哪個」
        ip = s.getsockname()[0]
        s.close()
        info = ServiceInfo(
            "_eldercompanion._tcp.local.",
            "陪伴系統._eldercompanion._tcp.local.",
            addresses=[socket.inet_aton(ip)], port=PORT,
            properties={"path": "/"},
        )
        zc = Zeroconf()
        zc.register_service(info)
        print(f"mDNS 廣播中：App「自動尋找電腦」找得到這台（{ip}:{PORT}）")
        return zc
    except Exception as e:
        print(f"mDNS 廣播失敗（不影響其他功能）：{e}")
        return None


@app.on_event("startup")
async def startup():
    global whisper
    _advertise_mdns()
    if not MIMO_API_KEY:
        print(f"⚠ 未設定 {CFG['llm']['api_key_env']} 環境變數，LLM 會無法回應！")
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT):
        print("（未設定 Telegram，家人通知/每日摘要停用）")
    load_phrases()
    load_memory()
    _fire_bg(daily_summary_loop())
    print("載入 Whisper...")
    whisper = WhisperModel(WHISPER_SIZE, device=WHISPER_DEVICE, compute_type=WHISPER_CTYPE)
    print("Whisper 就緒")


@app.get("/")
async def index():
    return HTMLResponse(HTML
                        .replace("__CLIENT_TIMEOUT_MS__", str(CLIENT_TIMEOUT_MS))
                        .replace("__DEFAULT_MODE__", DEFAULT_TALK_MODE))


@app.get("/health")
async def health():
    """Diagnostic: reports each link (Whisper / MiMo / CosyVoice) so you can see
    exactly what's broken during bring-up. Runs live reachability checks."""
    wh = {"loaded": whisper is not None, "size": WHISPER_SIZE}

    def _check_mimo():
        if not MIMO_API_KEY:
            return {"ok": False, "error": "MIMO_API_KEY 未設定"}
        try:
            t = time.time()
            hbody = {"model": MIMO_MODEL,
                     "messages": [{"role": "user", "content": "嗨"}],
                     "max_tokens": 1, "stream": False}
            if LLM_NOTHINK:  # mirror the real request path
                hbody["chat_template_kwargs"] = {"enable_thinking": False}
            r = requests.post(
                f"{MIMO_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {MIMO_API_KEY}"},
                json=hbody, timeout=8)
            r.raise_for_status()
            return {"ok": True, "model": MIMO_MODEL, "latency_ms": int((time.time() - t) * 1000)}
        except Exception as e:
            return {"ok": False, "model": MIMO_MODEL, "error": str(e)}

    def _check_cosy():
        try:
            r = requests.get(COSY_HEALTH, timeout=3)
            r.raise_for_status()
            d = r.json()
            return {"ok": True, "ref_loaded": d.get("ref_loaded"),
                    "watermark": d.get("watermark"),
                    "sample_rate": d.get("sample_rate")}
        except Exception as e:
            return {"ok": False, "error": f"{e}（WSL2 的 cosyvoice_api 未啟動？Phase 0 屬正常）"}

    mimo = await run_in_threadpool(_check_mimo)
    cosy = await run_in_threadpool(_check_cosy)
    edge = {"available": edge_tts is not None}

    if not wh["loaded"] or not mimo["ok"]:
        status = "error"          # 核心鏈斷，無法回應
    elif not cosy["ok"]:
        status = "degraded"       # 可用，但無克隆聲音，靠 edge-tts（Phase 0 預期狀態）
    else:
        status = "ok"

    return {"status": status, "whisper": wh, "mimo": mimo,
            "cosyvoice": cosy, "edge_tts": edge, "phrases": len(PHRASES),
            "llm_key_set": bool(MIMO_API_KEY),      # 大腦金鑰有沒有填（不限 NVIDIA）
            "llm_key_env": CFG["llm"]["api_key_env"]}   # 該填哪個環境變數名


@app.post("/reload-phrases")
async def reload_phrases():
    """Re-read phrases.json without a full restart (Whisper stays loaded).
    Use after adding/removing/replacing recordings in phrases/."""
    load_phrases()
    return {"phrases": len(PHRASES)}


# ── 爺爺老照片（閒置懷舊輪播）：把照片丟進 photos/ 就會播，沒有就顯示暖色占位 ──
@app.get("/photos")
async def list_photos():
    try:
        files = sorted(f for f in os.listdir(PHOTOS_DIR)
                       if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    except Exception:
        files = []
    return [f"/photos/{urllib.parse.quote(f)}" for f in files]


@app.get("/photos/{fname}")
async def get_photo(fname: str):
    p = os.path.join(PHOTOS_DIR, os.path.basename(fname))   # basename: no path traversal
    if not os.path.isfile(p):   # isfile: ".." resolves to a directory → 404, not a 500
        raise HTTPException(status_code=404, detail="not found")
    ext = os.path.splitext(p)[1].lower().lstrip(".")
    media = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
             "png": "image/png", "webp": "image/webp"}.get(ext, "application/octet-stream")
    with open(p, "rb") as f:
        return Response(content=f.read(), media_type=media)


PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".webp")
PHOTO_MAX_BYTES = 20 * 1024 * 1024   # 20MB 上限，避免傳錯檔把硬碟塞爆


@app.post("/setup/upload-photo")
async def setup_upload_photo(photo: UploadFile = File(...)):
    """家人上傳爺爺的老照片（懷舊輪播用）。/setup 網頁跟 App 原生選圖都打這支，
    後端邏輯共用一份。檔名前綴時間戳記，讓輪播順序約略照上傳先後（list_photos 會排序）。"""
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    ext = (os.path.splitext(photo.filename or "")[1] or "").lower()
    if ext not in PHOTO_EXTS:
        raise HTTPException(status_code=400, detail="只支援 jpg / png / webp 圖片")
    data = await photo.read()
    if len(data) < 100:
        raise HTTPException(status_code=400, detail="圖片是空的")
    if len(data) > PHOTO_MAX_BYTES:
        raise HTTPException(status_code=400, detail="圖片太大（上限 20MB）")
    fname = f"{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    with open(os.path.join(PHOTOS_DIR, fname), "wb") as f:
        f.write(data)
    return {"ok": True, "file": fname, "bytes": len(data)}


@app.post("/setup/delete-photo")
async def setup_delete_photo(fname: str = Form(...)):
    """刪掉一張已上傳的老照片（傳錯張時，家人不用自己去翻資料夾）。"""
    p = os.path.join(PHOTOS_DIR, os.path.basename(fname))
    if os.path.isfile(p):
        os.remove(p)
    return {"ok": True}


# ── 預設說話模式（家人在 Setup 台設；爺爺畫面本機可覆蓋） ──
@app.get("/setup/talk-mode")
async def get_talk_mode():
    return {"talk_mode": DEFAULT_TALK_MODE}


@app.get("/setup/qr")
async def setup_qr(request: Request):
    """這台電腦連線網址的 QR code——App 的「📷 掃碼連線」對著螢幕掃這個就好，不用打字。
    用 request.base_url，家人在哪個網址開 /setup，QR 就編碼那個網址（同區網用 IP，通道用通道網址）。"""
    if qrcode is None:
        raise HTTPException(status_code=501, detail="QR 功能未啟用（伺服器缺 qrcode 套件，可 pip install qrcode）")
    img = qrcode.make(str(request.base_url), image_factory=qrcode.image.svg.SvgImage, box_size=8)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/svg+xml")


@app.post("/setup/talk-mode")
async def set_talk_mode(mode: str = Form(...)):
    global DEFAULT_TALK_MODE
    DEFAULT_TALK_MODE = mode if mode in ("hold", "auto") else "hold"
    try:
        json.dump({"talk_mode": DEFAULT_TALK_MODE}, open(UI_STATE_FILE, "w", encoding="utf-8"))
    except Exception:
        pass
    return {"ok": True, "talk_mode": DEFAULT_TALK_MODE}


# ── Setup / admin (separate from 爺爺's companion UI; for family/caregiver) ────
@app.get("/setup")
async def setup_page():
    return HTMLResponse(SETUP_HTML)


@app.get("/setup/phrases")
async def setup_list_phrases():
    cfg = os.path.join(PHRASES_DIR, "phrases.json")
    try:
        rules = json.load(open(cfg, encoding="utf-8")) if os.path.exists(cfg) else []
    except Exception:
        rules = []
    for r in rules:
        r["has_audio"] = os.path.exists(os.path.join(PHRASES_DIR, r.get("file", "")))
    return rules


@app.post("/setup/upload-phrase")
async def setup_upload_phrase(file: str = Form(...), audio: UploadFile = File(...)):
    """Save a recording for a fixed phrase, then hot-reload (no restart)."""
    dest = os.path.join(PHRASES_DIR, os.path.basename(file))   # basename: no path traversal
    data = await audio.read()
    with open(dest, "wb") as f:
        f.write(data)
    load_phrases()
    return {"ok": True, "file": os.path.basename(file), "bytes": len(data), "phrases": len(PHRASES)}


@app.post("/setup/upload-voice")
async def setup_upload_voice(name: str = Form("family"), audio: UploadFile = File(...)):
    """Save a family voice source (used later to build the cloned voice)."""
    vdir = os.path.join(SCRIPT_DIR, "voices")
    os.makedirs(vdir, exist_ok=True)
    ext = (os.path.splitext(audio.filename or "")[1] or ".wav").lower()
    dest = os.path.join(vdir, os.path.basename(name) + ext)
    data = await audio.read()
    with open(dest, "wb") as f:
        f.write(data)
    return {"ok": True, "saved": dest, "bytes": len(data)}


@app.post("/setup/set-voice")
async def setup_set_voice(audio: UploadFile = File(...), ref_text: str = Form(""),
                          consent: str = Form("")):
    """使用者上傳一段參考音 → 設為 Qwen 的克隆音色。
    存 voices/active_reference.wav (+ 逐字稿 .txt)，再叫 Qwen 熱重載，不用重啟。
    這是開源版讓「每個人塞自己想要的音色」的入口。

    防冒用（同意閘門）：CONSENT_REQUIRED 時，錄音本人須在錄音裡先唸同意聲明，
    且需勾選確認；同意證明存 voices/active_reference.consent.json。"""
    if CONSENT_REQUIRED and not consent.strip():
        raise HTTPException(status_code=400,
            detail="請先勾選下方的同意聲明（確認你是本人或已取得本人同意），才能設定聲音。")
    vdir = os.path.join(SCRIPT_DIR, "voices")
    os.makedirs(vdir, exist_ok=True)
    raw = await audio.read()
    if len(raw) < 2000:
        raise HTTPException(status_code=400, detail="音檔太短或空的")
    ext = (os.path.splitext(audio.filename or "")[1] or ".wav").lower()
    up = os.path.join(vdir, "active_reference_upload" + ext)
    with open(up, "wb") as f:
        f.write(raw)
    # 解碼（faster-whisper 的 decode_audio 走 PyAV，支援 wav / mp3 / m4a）
    from faster_whisper.audio import decode_audio
    try:
        wav24 = await run_in_threadpool(lambda: decode_audio(up, sampling_rate=24000))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"讀不了這個音檔：{e}")
    # 寫成 24k PCM16 wav（用 stdlib wave，不依賴 soundfile）
    ref_wav = os.path.join(vdir, "active_reference.wav")
    import wave as _wave
    pcm = (np.clip(wav24, -1.0, 1.0) * 32767.0).astype("<i2").tobytes()
    with _wave.open(ref_wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    # 逐字稿：使用者填了就用；否則用 companion 自己的 whisper 轉（避免 WSL 端再下載模型）
    rt = (ref_text or "").strip()
    if not rt and whisper is not None:
        wav16 = await run_in_threadpool(lambda: decode_audio(up, sampling_rate=16000))

        def _tx():
            segs, _ = whisper.transcribe(wav16, language=ASR_LANG, vad_filter=True)
            return "".join(s.text for s in segs).strip()

        rt = await run_in_threadpool(_tx)
    with open(os.path.splitext(ref_wav)[0] + ".txt", "w", encoding="utf-8") as f:
        f.write(rt)
    # ── 同意閘門：錄音裡必須包含口說的同意聲明 ────────────────────────────
    # 同意句就在同一段錄音裡 → 說話者＝同意者，把「同意」綁死在「這把聲音」上。
    if CONSENT_REQUIRED:
        said = (rt or "") + " " + (ref_text or "")
        if not all(k in said for k in CONSENT_KEYS):
            for p in (ref_wav, os.path.splitext(ref_wav)[0] + ".txt", up):
                try: os.remove(p)
                except Exception: pass
            raise HTTPException(status_code=400,
                detail=f"為了防止聲音被冒用：請在錄音的最開頭先清楚唸這句同意聲明，再自然說話——"
                       f"「{CONSENT_PHRASE}」。沒聽到這句，聲音不會被設定。")
        import hashlib, time
        try:
            digest = hashlib.sha256(open(ref_wav, "rb").read()).hexdigest()
            rec = {"phrase": CONSENT_PHRASE, "spoken_in_voice": True,
                   "affirmed": consent.strip(), "transcript": rt,
                   "ref_sha256": digest, "ts": int(time.time())}
            with open(os.path.join(vdir, "active_reference.consent.json"), "w", encoding="utf-8") as f:
                json.dump(rec, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    # 叫 Qwen 熱重載新音色（不用重啟）
    reloaded = False
    try:
        rr = await run_in_threadpool(lambda: requests.post(
            COSY_URL.replace("/tts", "/reload-ref"), timeout=30))
        reloaded = (rr.status_code == 200 and bool(rr.json().get("ref_set")))
    except Exception:
        pass
    # 重載後清掉這個回覆的 TTS 舊快取（否則會續播舊音色）
    tts_cache.clear()
    return {"ok": True, "ref_text": rt, "reloaded": reloaded}


@app.get("/setup/phrase-audio/{fname}")
async def setup_phrase_audio(fname: str):
    p = os.path.join(PHRASES_DIR, os.path.basename(fname))
    if not os.path.exists(p):
        raise HTTPException(status_code=404, detail="not found")
    media = "audio/mpeg" if p.lower().endswith(".mp3") else "audio/wav"
    with open(p, "rb") as f:
        return Response(content=f.read(), media_type=media)


@app.post("/setup/tts-preview")
async def setup_tts_preview(text: str = Form(...)):
    """Let family type any text and hear it in the current voice (TTS → edge fallback)."""
    reply = text.strip()
    if not reply:
        raise HTTPException(status_code=400, detail="empty")
    try:
        tts_r = await run_in_threadpool(lambda: requests.post(
            COSY_URL, json={"text": reply, "speed": 1.0}, timeout=COSY_TIMEOUT))
        if tts_r.status_code == 200 and tts_r.content:
            return Response(content=tts_r.content, media_type="audio/wav")
    except Exception:
        pass
    try:
        mp3 = await edge_tts_synth(reply)
        return Response(content=mp3, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/setup/history")
async def setup_history():
    """Recent conversation + long-term summary, for family to see how 爺爺 is."""
    return {"summary": session_summary, "recent": history[-30:]}


@app.post("/interact")
async def interact(request: Request):
    global history
    if whisper is None:
        return JSONResponse({"type": "error", "reply": "我還在準備中，請等我一下下再說。"},
                            status_code=503)

    pcm_bytes = await request.body()
    if len(pcm_bytes) < 6400:  # < 0.2s at 16kHz int16
        return Response(status_code=204)
    if len(pcm_bytes) % 2:     # 奇數位元組會讓 frombuffer 直接拋錯 → 500，截掉半個樣本即可
        pcm_bytes = pcm_bytes[:-1]

    audio = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    # Whisper is blocking/CPU-GPU heavy; run off the event loop so /health and
    # other requests stay responsive while transcribing.
    def _transcribe():
        segments, _ = whisper.transcribe(
            audio, beam_size=5, language=ASR_LANG,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 400}
        )
        return "".join(seg.text for seg in segments).strip()

    text = await run_in_threadpool(_transcribe)

    if not text:
        return JSONResponse({"type": "no_speech"})

    print(f"爺爺：{text}")

    # #3: Fixed-phrase cache FIRST — checked before the length filter so single-char
    # distress words ("痛"/"餓") can still hit a canned reply. Instant, skips LLM+TTS.
    hit = match_phrase(text)
    if hit:
        print(f"［固定句命中］→ {hit['text']}")
        if hit.get("alert"):   # 不適等關鍵字 → 推播通知家人
            _fire_bg(notify_family(f"⚠️ 爺爺剛說了：「{text}」（{datetime.now():%H:%M}），請留意。"))
        _remember(text, hit["text"])
        return _audio_response(hit["audio"], hit["media"], text, hit["text"])

    # Open-ended LLM path: ignore too-short noise that matched no phrase.
    if len(text) < 2:
        return JSONResponse({"type": "no_speech"})

    msgs = [{"role": "system", "content": get_system_prompt()}]
    msgs.extend(history[-MAX_HISTORY:])
    msgs.append({"role": "user", "content": text})

    body = {"model": MIMO_MODEL, "messages": msgs, "stream": False,
            "temperature": LLM_TEMP, "max_tokens": LLM_MAXTOK}
    if LLM_NOTHINK:
        # Disable reasoning. Nemotron-3 accepts this too (verified: reasoning→0,
        # clean content). Critical: with reasoning ON, its 200-1000-char think
        # doesn't fit max_tokens=80 → the truncated think LEAKS into content and
        # 爺爺 hears the model's inner monologue (incl. "as a granddaughter…").
        body["chat_template_kwargs"] = {"enable_thinking": False}
    try:
        r = await run_in_threadpool(lambda: requests.post(
            f"{MIMO_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {MIMO_API_KEY}"},
            json=body, timeout=LLM_TIMEOUT))
        r.raise_for_status()
        reply = (r.json()["choices"][0]["message"].get("content") or "").strip()
        reply = _sanitize_reply(reply)
        if not reply:
            raise ValueError("empty content from LLM")
    except Exception as e:
        print(f"MiMo 錯誤：{e}")
        return JSONResponse({"type": "error", "reply": "不好意思，我現在有點問題，請稍後再說。"})
    print(f"回應：{reply}")

    # #6: if 爺爺 gave up / closed the tab mid-request, don't record a turn he
    # never heard — it would pollute the next reply's context.
    if await request.is_disconnected():
        print("client 已斷線，丟棄本輪（不寫入記憶）")
        return Response(status_code=204)

    _remember(text, reply)

    # Reply-level TTS cache: repeated identical replies (common with 爺爺) skip synthesis.
    cached = tts_cache.get(reply)
    if cached:
        return _audio_response(cached[0], cached[1], text, reply)

    # Primary: CosyVoice (cloned voice). On any failure, fall back to edge-tts so
    # 爺爺 still hears a reply rather than silence.
    try:
        tts_r = await run_in_threadpool(lambda: requests.post(
            COSY_URL,
            json={"text": reply, "speed": 1.0, "spk_id": CHARACTER.get("cosyvoice_spk", "")},
            timeout=COSY_TIMEOUT))
        if tts_r.status_code == 200 and tts_r.content:
            _tts_cache_put(reply, tts_r.content, "audio/wav")
            return _audio_response(tts_r.content, "audio/wav", text, reply)
        print(f"CosyVoice 回應 {tts_r.status_code}，改用 edge-tts")
    except Exception as e:
        print(f"CosyVoice 連線失敗，改用 edge-tts：{e}")

    try:
        mp3 = await edge_tts_synth(reply)
        # Don't cache the fallback: once CosyVoice recovers we want it to re-synthesize
        # in 爸爸's cloned voice, not keep serving this generic edge-tts audio.
        return _audio_response(mp3, "audio/mpeg", text, reply)
    except Exception as e:
        print(f"edge-tts 也失敗，回傳文字：{e}")

    return JSONResponse({"type": "text_only", "user": text, "reply": reply})


# ── HTML ─────────────────────────────────────────────────────────────────────
HTML = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>爺爺的小幫手</title>
<style>
/* 日系優雅簡約溫暖：原研哉／無印 — 和紙留白、墨色、柿色暖調；日/夜自動切換 */
:root{
  --bg1:#F3ECDD; --bg2:#EAE0CC;
  --ink:#3B342A; --ink-soft:#8C8069;
  --accent:#C0673B; --accent-deep:#A44A2B;
  --surface:rgba(255,255,255,.42); --surface-reply:rgba(192,103,59,.12);
  --line:rgba(59,52,42,.10); --btn-fg:#FBF6EC; --dot:rgba(59,52,42,.16);
}
body.night{
  --bg1:#221E19; --bg2:#171410;
  --ink:#ECE2D0; --ink-soft:#9C9078;
  --accent:#D89A5B; --accent-deep:#C97B44;
  --surface:rgba(255,255,255,.06); --surface-reply:rgba(216,154,91,.14);
  --line:rgba(236,226,208,.10); --btn-fg:#241F18; --dot:rgba(236,226,208,.16);
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%}
body{
  background:linear-gradient(180deg,var(--bg1),var(--bg2));color:var(--ink);
  font-family:"Noto Serif TC","Songti TC","Source Han Serif TC","Yu Mincho","Hiragino Mincho ProN",serif;
  height:100dvh;display:flex;flex-direction:column;overflow:hidden;
  user-select:none;-webkit-tap-highlight-color:transparent;transition:color .8s ease;position:relative;
}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/></svg>");
  mix-blend-mode:multiply;}
body.night::before{mix-blend-mode:screen;opacity:.35}
#clock{text-align:center;padding:4vh 0 0;line-height:1;z-index:1;
  font-family:"Noto Sans TC","PingFang TC",-apple-system,sans-serif;
  font-size:15vw;font-weight:200;letter-spacing:.02em;color:var(--ink);font-variant-numeric:tabular-nums;}
#greet{text-align:center;font-size:5.4vw;color:var(--accent);letter-spacing:.28em;padding:1.4vh 0 .4vh;z-index:1;font-weight:500}
#date{text-align:center;font-size:4.4vw;color:var(--ink-soft);letter-spacing:.16em;z-index:1}
#mid{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;
     align-items:center;gap:1.6vh;padding:0 8vw;overflow:hidden;z-index:1}
#wave{display:flex;align-items:center;justify-content:center;gap:10px;height:46px}
.bar{width:6px;height:8px;background:var(--dot);border-radius:3px;transition:height .09s ease}
.bar.on{background:var(--accent)}
#status{text-align:center;font-size:5.2vw;color:var(--ink-soft);min-height:1.5em;line-height:1.6;letter-spacing:.06em}
#user-box{display:none;max-width:100%;background:var(--surface);border:1px solid var(--line);border-radius:20px;
  padding:1.6vh 5.5vw;font-size:4.4vw;color:var(--ink-soft);line-height:1.6;letter-spacing:.04em}
#reply-box{display:none;max-width:100%;background:var(--surface-reply);border-radius:22px;
  padding:2.2vh 5.5vw;font-size:5.4vw;color:var(--ink);line-height:1.65;letter-spacing:.04em;box-shadow:0 2px 20px rgba(0,0,0,.04)}
#modeSw{display:flex;align-self:center;flex-shrink:0;margin:0 0 1.6vh;z-index:1;
  background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:5px}
#modeSw .ms{border:none;background:transparent;color:var(--ink-soft);font-family:inherit;
  font-size:3.7vw;letter-spacing:.1em;padding:1vh 6.5vw;border-radius:999px;cursor:pointer;
  transition:background .25s,color .25s;-webkit-tap-highlight-color:transparent}
#modeSw .ms.active{background:var(--accent);color:var(--btn-fg);font-weight:600}
#btn{
  margin:0 6vw 3.5vh;height:13vh;min-height:112px;flex-shrink:0;z-index:1;
  border:none;border-radius:30px;cursor:pointer;font-family:inherit;
  font-size:7.4vw;font-weight:600;letter-spacing:.5em;text-indent:.5em;color:var(--btn-fg);background:var(--accent);
  box-shadow:0 10px 30px rgba(160,74,43,.22),inset 0 1px 0 rgba(255,255,255,.18);
  transition:transform .12s ease,background .3s ease,box-shadow .3s ease;
}
#btn:active{transform:scale(.985)}
#btn.listening{background:var(--accent-deep);letter-spacing:.35em;box-shadow:0 0 0 8px rgba(164,74,43,.14),0 10px 30px rgba(164,74,43,.28)}
#btn.processing{background:var(--ink-soft);color:var(--btn-fg);pointer-events:none;box-shadow:none;opacity:.85}
#idle{position:fixed;inset:0;z-index:5;opacity:0;pointer-events:none;transition:opacity 1.6s ease;background:var(--bg2)}
#idle.show{opacity:1;pointer-events:auto}
.photo{position:absolute;inset:0;opacity:0;transition:opacity 2.4s ease;background-size:cover;background-position:center;
  animation:kenburns 26s ease-in-out infinite alternate}
.photo.on{opacity:1}
@keyframes kenburns{from{transform:scale(1.04) translate(0,0)}to{transform:scale(1.14) translate(-2%,-2%)}}
#idle::after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.30) 100%)}
#idle .hint{position:absolute;left:0;right:0;bottom:6vh;text-align:center;color:rgba(255,255,255,.82);
  font-size:4.2vw;letter-spacing:.2em;z-index:2;text-shadow:0 2px 12px rgba(0,0,0,.5)}
</style>
</head>
<body>
<div id="idle">
  <div class="photo" style="background:linear-gradient(135deg,#caa87e,#9c7b52)"></div>
  <div class="photo" style="background:linear-gradient(135deg,#b98c6a,#7d5a44)"></div>
  <div class="photo" style="background:linear-gradient(135deg,#a89e86,#6f6a56)"></div>
  <div class="hint">〈 爺爺的老照片 · 碰一下就回來 〉</div>
</div>
<div id="clock">--:--</div>
<div id="greet"></div>
<div id="date"></div>
<div id="mid">
  <div id="wave"><div class="bar"></div><div class="bar"></div><div class="bar"></div>
    <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>
  <div id="status">我在這裡陪你</div>
  <div id="user-box"></div>
  <div id="reply-box"></div>
</div>
<div id="modeSw">
  <button class="ms" data-mode="hold">按住說話</button>
  <button class="ms" data-mode="auto">自動說話</button>
</div>
<button id="btn">按住說話</button>

<script>
/* ── 時鐘 + 早午晚安 + 自動日夜（18:00–06:00 暖夜） ── */
const DAYS=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
function tick(){
  const n=new Date(),h=n.getHours(),m=n.getMinutes();
  document.getElementById('clock').textContent=String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');
  document.getElementById('date').textContent=
    n.getFullYear()+'年'+(n.getMonth()+1)+'月'+n.getDate()+'日　'+DAYS[n.getDay()];
  document.getElementById('greet').textContent=
    h<5?'夜深了':h<11?'早安　爺爺':h<14?'午安　爺爺':h<18?'午後好':'晚安　爺爺';
  document.body.classList.toggle('night', h>=18||h<6);
}
setInterval(tick,1000);tick();

/* ── 元件 + 模式（按住說話 / 自動連續對話） ── */
const btn=document.getElementById('btn'),statusEl=document.getElementById('status');
const userBox=document.getElementById('user-box'),replyBox=document.getElementById('reply-box');
const bars=document.querySelectorAll('.bar');
let mode=localStorage.getItem('talkMode')||'__DEFAULT_MODE__';  // 家人於 Setup 台設預設；本機切換覆蓋
let autoOn=false;                                               // 自動連續對話 session
let noSpeech=0;                                                 // auto：連續「沒聽到話」次數（防雜訊無限迴圈）
const VAD_ON=0.02, SILENCE_MS=1400, NOSPEECH_MS=8000, NOSPEECH_MAX=4;  // 靜音偵測：停頓自動送 / 無語自動結束
let vad={speech:false,lastVoice:0,start:0};
let ctx,stream,proc,src,recording=false,chunks=[];
let pressed=false;   // hold：實體按著中（getUserMedia await 期間放開，也要被 startRec 看到）
let micBusy=false;   // 麥克風初始化/喚醒 await 中：擋重入（否則第二次呼叫會在 proc 建好前用到它）

function btnLabel(s){
  if(mode==='auto')return s==='listening'?'我在聽…':s==='processing'?'請稍候…':autoOn?'點一下　結束':'開始說話';
  return s==='listening'?'放開　送出':s==='processing'?'請稍候…':'按住說話';
}
function setUI(state,msg){statusEl.textContent=msg;btn.className=state;btn.textContent=btnLabel(state);}

const msBtns=document.querySelectorAll('#modeSw .ms');
function paintMode(){
  msBtns.forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
  if(!autoOn&&!recording&&btn.className!=='processing')
    setUI('', mode==='auto'?'點一下下面，就能開始聊天':'我在這裡陪你');
}
msBtns.forEach(b=>b.addEventListener('click',e=>{
  e.stopPropagation(); if(autoOn||recording)endAuto();   // recording：按住錄音中切模式也要收掉，否則 recording 卡死
  mode=b.dataset.mode; localStorage.setItem('talkMode',mode); paintMode();
}));

/* ── 閒置 → 爺爺老照片慢速輪播（懷舊療法）；photos/ 沒照片就用暖色占位 ── */
const IDLE_MS=75000;
let idleTimer,photoTimer,pi=0;
const idle=document.getElementById('idle');
let photos=idle.querySelectorAll('.photo');
fetch('/photos').then(r=>r.json()).then(a=>{
  if(Array.isArray(a)&&a.length){
    idle.querySelectorAll('.photo').forEach(p=>p.remove());
    const hint=idle.querySelector('.hint');
    a.forEach(u=>{const d=document.createElement('div');d.className='photo';d.style.backgroundImage='url('+u+')';idle.insertBefore(d,hint);});
    photos=idle.querySelectorAll('.photo');
  }
}).catch(()=>{});
function showIdle(){
  if(autoOn||btn.className){resetIdle();return;}   // 對話進行中不跳懷舊層
  idle.classList.add('show');
  photos.forEach((p,i)=>p.classList.toggle('on',i===0));pi=0;
  clearInterval(photoTimer);
  photoTimer=setInterval(()=>{photos[pi].classList.remove('on');pi=(pi+1)%photos.length;photos[pi].classList.add('on');},8000);
}
function hideIdle(){idle.classList.remove('show');clearInterval(photoTimer);}
function resetIdle(){hideIdle();clearTimeout(idleTimer);idleTimer=setTimeout(showIdle,IDLE_MS);}
['pointerdown','touchstart'].forEach(ev=>document.addEventListener(ev,resetIdle,{passive:true}));
idle.addEventListener('pointerdown',hideIdle);
resetIdle();

/* ── 錄音管線（真）：按住錄音，自動模式加 VAD 靜音偵測 ── */
async function startRec(){
  if(recording||micBusy||btn.classList.contains('processing'))return;
  micBusy=true;
  try{
    if(!ctx){
      ctx=new(window.AudioContext||window.webkitAudioContext)();
      stream=await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:true,noiseSuppression:true}});
      src=ctx.createMediaStreamSource(stream);
      proc=ctx.createScriptProcessor(4096,1,1);
      src.connect(proc);proc.connect(ctx.destination);
    }
    if(ctx.state==='suspended'){await ctx.resume();}
  }catch(err){
    console.error('mic init failed',err);
    try{stream&&stream.getTracks().forEach(t=>t.stop());}catch(_){}
    try{ctx&&ctx.close();}catch(_){}   // 不關會累積 AudioContext（瀏覽器有上限），拒絕幾次後就再也開不了
    ctx=null;stream=null;proc=null;src=null;recording=false;autoOn=false;micBusy=false;
    setUI('','請允許麥克風，再按一次');return;
  }
  micBusy=false;
  // await（權限框/喚醒）期間使用者已放開（hold）或已點結束（auto）→ 不能開錄，否則錄音收不掉
  if(mode==='auto'?!autoOn:!pressed){paintMode();return;}
  chunks=[];recording=true;
  vad={speech:false,lastVoice:performance.now(),start:performance.now()};
  setUI('listening', mode==='auto'?'我在聽…（再點一下就結束）':'錄音中...');
  proc.onaudioprocess=e=>{
    if(!recording)return;
    chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
    const last=chunks[chunks.length-1];
    const rms=Math.sqrt(last.reduce((s,x)=>s+x*x,0)/last.length);
    bars.forEach(b=>{b.style.height=Math.min(8+rms*500,44)+'px';b.classList.toggle('on',rms>.008);});
    if(mode==='auto'&&autoOn){                       // VAD：說完停頓自動送出，一直沒說話自動結束
      const now=performance.now();
      if(rms>VAD_ON){vad.speech=true;vad.lastVoice=now;}
      if(vad.speech&&now-vad.lastVoice>SILENCE_MS){stopRec();}
      else if(!vad.speech&&now-vad.start>NOSPEECH_MS){endAuto();}
    }
  };
}

async function stopRec(){
  if(!recording)return;
  recording=false;proc.onaudioprocess=null;
  bars.forEach(b=>{b.style.height='8px';b.classList.remove('on');});
  if(chunks.length<4){ if(mode==='auto'&&autoOn){autoNothing();}else setUI('','請再說一次'); return; }

  const total=chunks.reduce((n,c)=>n+c.length,0);
  const merged=new Float32Array(total);
  let off=0;chunks.forEach(c=>{merged.set(c,off);off+=c.length;});

  // Resample to 16kHz if device uses different rate (iOS=44100, Android=48000)
  const srcRate=ctx.sampleRate;let pcm=merged;
  if(srcRate!==16000){
    const ratio=srcRate/16000,outLen=Math.floor(merged.length/ratio);
    pcm=new Float32Array(outLen);
    for(let i=0;i<outLen;i++){
      const j=i*ratio,j0=Math.floor(j),j1=Math.min(j0+1,merged.length-1);
      pcm[i]=merged[j0]+(merged[j1]-merged[j0])*(j-j0);
    }
  }
  const i16=new Int16Array(pcm.length);
  for(let i=0;i<pcm.length;i++)i16[i]=Math.max(-32768,Math.min(32767,pcm[i]*32768));

  setUI('processing', mode==='auto'?'讓我想想…':'識別中...');
  userBox.style.display='none';replyBox.style.display='none';

  const ctrl=new AbortController();
  // Injected from config: > backend worst case so the client never aborts a request the server is still completing.
  const tid=setTimeout(()=>ctrl.abort(),__CLIENT_TIMEOUT_MS__);
  try{
    const res=await fetch('/interact',{method:'POST',signal:ctrl.signal,
      headers:{'Content-Type':'application/octet-stream'},body:i16.buffer});
    clearTimeout(tid);
    if(res.status===204){ if(mode==='auto'&&autoOn){autoNothing();}else setUI('','沒聽清楚，再說一次'); return; }
    const ct=res.headers.get('content-type')||'';
    if(ct.includes('audio')){
      noSpeech=0;
      const ut=decodeURIComponent(res.headers.get('X-User-Text')||'');
      const rt=decodeURIComponent(res.headers.get('X-Reply-Text')||'');
      if(ut){userBox.textContent='你：'+ut;userBox.style.display='block';}
      if(rt){replyBox.textContent=rt;replyBox.style.display='block';}
      setUI('','回應中...');
      const blob=await res.blob();
      const url=URL.createObjectURL(blob);
      const aud=new Audio(url);
      aud.onended=()=>{URL.revokeObjectURL(url);endTurn();};
      aud.onerror=()=>{URL.revokeObjectURL(url);endTurn();};
      aud.play().catch(()=>{ctx.resume().then(()=>aud.play())        // Android 有時要先 unlock
        .catch(()=>{URL.revokeObjectURL(url);endTurn();});});        // 再失敗也要收尾，別卡在「回應中」
    }else{
      const d=await res.json();
      if(d.type==='no_speech'){ if(mode==='auto'&&autoOn){autoNothing();}else setUI('','沒聽清楚，請靠近麥克風再說一次'); }
      else if(d.reply){replyBox.textContent=d.reply;replyBox.style.display='block';endTurn();}
    }
  }catch(e){
    clearTimeout(tid);console.error(e);
    if(mode==='auto')autoOn=false;
    setUI('',e.name==='AbortError'?'回應太慢，請重試':'連線錯誤，請重試');
  }
}

/* ── 自動連續對話控制 ── */
function endTurn(){ if(recording)return;   // 回覆還在播時爺爺已按著在講下一句 → 別把 listening 蓋掉
  if(mode==='auto'&&autoOn){autoRelisten();} else setUI('', mode==='auto'?'點一下下面，就能開始聊天':'請說話'); }
function autoRelisten(){ if(!autoOn)return; setTimeout(()=>{ if(autoOn&&!recording)startRec(); },300); }   // 回覆播完自動再聽
function autoNothing(){  // auto 送出但沒聽到話：連續太多次就休息，避免雜訊造成無限「錄→送→再錄」
  if(++noSpeech>=NOSPEECH_MAX){endAuto();setUI('','我先休息一下，想聊天再按一下');}
  else {setUI('','沒聽清楚，我再聽一次');autoRelisten();}   // 必須先清掉 processing class，否則 startRec 會被它擋住 → 卡死在「請稍候…」
}
function startAuto(){ autoOn=true; noSpeech=0; resetIdle(); userBox.style.display='none';replyBox.style.display='none'; startRec(); }
function endAuto(){ autoOn=false; if(recording){recording=false; if(proc)proc.onaudioprocess=null;}
  bars.forEach(b=>{b.style.height='8px';b.classList.remove('on');}); paintMode(); }

/* ── 按鈕依模式分派：hold=按住錄音；auto=點一下開始／結束 ── */
function onPress(){ pressed=true; if(mode==='auto'){ autoOn?endAuto():startAuto(); } else startRec(); }
function onRelease(){ pressed=false; if(mode!=='auto')stopRec(); }
btn.addEventListener('touchstart',e=>{e.preventDefault();onPress();},{passive:false});
btn.addEventListener('touchend',e=>{e.preventDefault();onRelease();},{passive:false});
btn.addEventListener('touchcancel',onRelease);      // 來電/通知欄中斷觸控只發 touchcancel，不收會一直錄音
btn.addEventListener('mousedown',onPress);
document.addEventListener('mouseup',onRelease);     // 滑鼠移出按鈕才放開，掛在 btn 上會漏接 → 一直錄音
btn.addEventListener('contextmenu',e=>e.preventDefault());

paintMode();
</script>
</body>
</html>
"""

# ── Setup / admin page (family/caregiver; NOT 爺爺's interface) ────────────────
SETUP_HTML = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>陪伴系統 · 家人設定台</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#eef1f6;color:#1e2430;font-family:'Microsoft JhengHei','Noto Sans TC',system-ui,sans-serif;line-height:1.55}
header{background:#26418f;color:#fff;padding:18px 20px}
header .t{font-size:20px;font-weight:800}
header .s{font-size:13px;opacity:.85;margin-top:2px}
main{max-width:820px;margin:0 auto;padding:16px}
.card{background:#fff;border-radius:16px;padding:18px 20px;margin:14px 0;box-shadow:0 1px 3px rgba(20,30,60,.08)}
h2{margin:0 0 6px;font-size:16px;display:flex;align-items:center;gap:8px}
.hint{color:#7a8494;font-size:13px;margin:0 0 14px}
.muted{color:#7a8494;font-size:13px}
.badges{display:flex;flex-wrap:wrap;gap:8px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:20px;font-size:13px;font-weight:700}
.ok{background:#dcfce7;color:#166534}.bad{background:#fee2e2;color:#991b1b}.warn{background:#fef3c7;color:#92400e}
.row{display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid #eef0f4;flex-wrap:wrap}
.row:first-child{border-top:none}
.ph-text{flex:1;min-width:220px;font-size:15px}
.ph-trig{font-size:12px;color:#98a2b3;margin-top:2px}
input[type=file]{font-size:13px;max-width:180px}
input[type=text]{padding:9px 11px;border:1px solid #d3d9e3;border-radius:10px;font-size:14px;background:#fbfcfe}
input[type=text]:focus{outline:none;border-color:#26418f}
button{background:#26418f;color:#fff;border:none;border-radius:10px;padding:9px 16px;font-size:14px;font-weight:600;cursor:pointer;transition:.12s}
button:hover{background:#1c3272}button:active{transform:scale(.97)}
button.sm{padding:6px 11px;font-size:13px}
button.ghost{background:#eef1f8;color:#26418f}
button.ghost:hover{background:#dfe5f3}
button:disabled{background:#b6bdc9;cursor:default}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:0 0 auto}
.note{font-size:13px;color:#3a4658;background:#eef4ff;border-radius:10px;padding:11px 13px;margin-top:10px}
.field{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.turn{padding:7px 0;border-top:1px solid #f1f3f7;font-size:14px}
.turn:first-child{border-top:none}
.who{font-weight:700;margin-right:6px}
.who.u{color:#b45309}.who.a{color:#26418f}
.sumbox{background:#f7f9fc;border-radius:10px;padding:12px 14px;font-size:14px;white-space:pre-wrap}
a.link{color:#26418f;font-weight:600;text-decoration:none}
</style>
</head>
<body>
<header>
  <div class="t">🛠 家人設定台</div>
  <div class="s">給家人／照顧者使用 —— 這不是爺爺看的畫面</div>
</header>
<main>

<div class="card">
  <h2>📊 系統狀態</h2>
  <div class="badges" id="status">檢查中…</div>
  <div id="keyWarn"></div>
  <div style="margin-top:12px"><a class="link" href="/" target="_blank">→ 開啟爺爺的畫面（Companion）</a></div>
  <div class="field" style="margin-top:12px">
    <input type="text" id="thisUrl" readonly style="flex:1;min-width:200px;background:#f7f9fc" value="讀取中…">
    <button class="ghost sm" onclick="copyThisUrl()" id="copyUrlBtn">📋 複製網址</button>
  </div>
  <p class="hint" style="margin:6px 0 0">在平板的 App 開「輸入電腦網址」，按貼上、或用「📷 掃碼連線」掃下面這個 QR。</p>
  <div style="margin-top:10px;text-align:center">
    <img src="/setup/qr" alt="QR code" width="150" height="150"
         style="border-radius:10px;background:#fff;padding:6px;box-shadow:0 1px 3px rgba(20,30,60,.12)"
         onerror="this.style.display='none';document.getElementById('qrFallback').style.display='block'">
    <p id="qrFallback" class="muted" style="display:none">QR 功能未啟用（伺服器缺 qrcode 套件），用上面「複製網址」就好</p>
  </div>
</div>

<div class="card">
  <h2>① 🎙 設定陪伴聲音（音色）</h2>
  <p class="hint"><b>第一次使用先做這個。</b>上傳一段<b>清楚、安靜、連續 10–30 秒</b>的人聲，長輩之後就會聽到「這個聲音」回應他。語氣一致比錄很長更重要（系統只取最好的約 24 秒）。支援 wav / mp3 / m4a。<br>逐字稿可<b>留空</b>——系統會自動辨識；填了更準。</p>
  <div class="note" style="background:#fff7ed;color:#9a3412;margin-bottom:12px">
    🛡️ <b>防止聲音被冒用</b>：錄音的<b>最開頭</b>，請本人先清楚唸這一句同意聲明，接著再自然說話——<br>
    <b style="font-size:15px">「我同意用我的聲音陪伴家人」</b><br>
    <span style="font-size:12px">同意句就在同一段錄音裡，代表「這個聲音的本人」確實同意。系統聽到才會設定。<br>另外，所有生成的語音都會打上聽不見的 AI 浮水印，可被偵測為合成聲——降低被拿去詐騙的價值。</span>
  </div>
  <div class="field">
    <input type="file" id="voiceFile" accept="audio/*">
    <input type="text" id="voiceText" placeholder="（選填）這段錄音說了什麼" style="flex:1;min-width:200px">
    <button onclick="setVoice()" id="vbtn">設為陪伴聲音</button>
  </div>
  <label style="display:flex;gap:8px;align-items:flex-start;margin-top:10px;font-size:13px;color:#3a4658;cursor:pointer">
    <input type="checkbox" id="consentChk" style="margin-top:3px">
    <span>我確認我是這個聲音的<b>本人</b>，或已取得本人同意，僅用於陪伴長輩。</span>
  </label>
  <div id="voiceMsg" class="note" style="display:none"></div>
</div>

<div class="card">
  <h2>② 🗣 爺爺的說話方式</h2>
  <p class="hint">「按住說話」＝按著講、放開送出（最不會誤觸）。「自動說話」＝點一下就開始，講完自動送出、小幫手回覆後自動再聽，適合手腳不方便、不好一直按的長輩。這裡設的是爺爺畫面的<b>預設</b>；爺爺畫面上也有小切換可自己換。</p>
  <div class="field">
    <button id="modeHold" onclick="setMode('hold')">按住說話</button>
    <button id="modeAuto" onclick="setMode('auto')">自動說話（連續對話）</button>
    <span class="muted" id="modeNow"></span>
  </div>
</div>

<div class="card">
  <h2>③ 📷 爺爺的老照片 <span class="muted" id="photoCount"></span></h2>
  <p class="hint">爺爺畫面沒在說話時，會慢慢輪播這些照片（懷舊療法，安撫情緒）。可一次選多張，jpg / png / webp，單張上限 20MB。</p>
  <div class="field">
    <input type="file" id="photoFiles" accept="image/*" multiple>
    <button onclick="uploadPhotos()" id="photoBtn">上傳照片</button>
  </div>
  <div id="photoMsg" class="note" style="display:none"></div>
  <div id="photoGrid" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:14px"></div>
</div>

<div class="card">
  <h2>🔊 試聽現在的聲音</h2>
  <p class="hint">打一句話，聽聽爺爺會聽到什麼樣的聲音（開放對話用的克隆聲；克隆未啟用時是通用聲）。</p>
  <div class="field">
    <input type="text" id="prevText" placeholder="例如：爺爺，該吃藥囉。" value="爺爺，今天天氣真好，要記得多喝水喔。" style="flex:1;min-width:220px">
    <button onclick="preview()" id="pbtn">▶ 試聽</button>
  </div>
</div>

<div class="card">
  <h2>💬 固定句 <span class="muted" id="phCount"></span></h2>
  <p class="hint">爺爺常說的話 → 播放家人的真聲，秒回。每句可上傳一段家人錄音（wav / mp3），上傳後立即生效。綠點=已有錄音。</p>
  <div id="phrases">載入中…</div>
  <div style="margin-top:12px"><button class="ghost sm" onclick="loadPhrases()">🔄 重新整理</button></div>
</div>

<div class="card">
  <h2>📋 爺爺近況（對話記錄）</h2>
  <p class="hint">最近聊了什麼、AI 幫忙記住的重點。方便家人了解爺爺狀況。</p>
  <div id="summary" class="sumbox" style="display:none"></div>
  <div id="history" style="margin-top:10px">載入中…</div>
  <div style="margin-top:12px"><button class="ghost sm" onclick="loadHistory()">🔄 重新整理</button></div>
</div>

</main>
<script>
const player=new Audio();
let lastBlobUrl=null;
function play(url){
  if(lastBlobUrl){URL.revokeObjectURL(lastBlobUrl);lastBlobUrl=null;}   // 試聽的 blob URL 不回收會累積佔記憶體
  if(url.startsWith('blob:'))lastBlobUrl=url;
  player.src=url; player.play().catch(()=>{});
}

function copyThisUrl(){
  const el=document.getElementById('thisUrl'), btn=document.getElementById('copyUrlBtn');
  const done=()=>{ const old=btn.textContent; btn.textContent='✅ 已複製'; setTimeout(()=>btn.textContent=old,1500); };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(el.value).then(done).catch(()=>{ el.select(); document.execCommand('copy'); done(); });
  } else {   // 舊瀏覽器 / 非 https 沒有 clipboard API 時的退路
    el.select(); document.execCommand('copy'); done();
  }
}
document.getElementById('thisUrl').value = location.origin + '/';

async function loadStatus(){
  const el=document.getElementById('status');
  try{
    const h=await (await fetch('/health')).json();
    const b=(ok,t,warn)=>`<span class="badge ${ok?'ok':(warn?'warn':'bad')}">${ok?'✓':'✕'} ${t}</span>`;
    el.innerHTML =
      b(h.whisper&&h.whisper.loaded,'語音辨識')+
      b(h.mimo&&h.mimo.ok,'大腦')+
      b(h.cosyvoice&&h.cosyvoice.ok,'克隆聲音'+((h.cosyvoice&&h.cosyvoice.ok)?'':'（未啟用·用通用聲）'),true)+
      (h.cosyvoice&&h.cosyvoice.ok?b(h.cosyvoice.watermark,'AI浮水印'+(h.cosyvoice.watermark?'':'（未啟用）'),true):'')+
      b(h.phrases>0,'固定句 '+h.phrases+' 句',true);
    const kw=document.getElementById('keyWarn');
    if(kw){
      kw.innerHTML = (h.llm_key_set===false)
        ? '<div class="note" style="background:#fee2e2;color:#991b1b;margin-top:10px">⚠ <b>尚未設定大腦（LLM）金鑰</b>：請到專案資料夾的 <b>.env</b> 填入 <b>'+(h.llm_key_env||'你的 API key')+'</b>，大腦才會回應。<br><span style="font-size:12px">預設用 NVIDIA Nemotron（<b>build.nvidia.com</b> 免費申請）；也可改用任何 OpenAI 相容的 LLM——改 <b>conf.yaml</b> 的 <code>llm.base_url / model / api_key_env</code> 即可。</span></div>'
        : '';
    }
  }catch(e){ el.innerHTML='<span class="badge bad">✕ 無法連線到伺服器</span>'; }
}
async function preview(){
  const t=document.getElementById('prevText').value.trim(); const btn=document.getElementById('pbtn');
  if(!t)return; btn.disabled=true; btn.textContent='合成中…';
  try{
    const fd=new FormData(); fd.append('text',t);
    const res=await fetch('/setup/tts-preview',{method:'POST',body:fd});
    if(res.ok){ play(URL.createObjectURL(await res.blob())); } else { alert('合成失敗'); }
  }catch(e){ alert('失敗：'+e); }
  btn.disabled=false; btn.textContent='▶ 試聽';
}
async function setVoice(){
  const f=document.getElementById('voiceFile').files[0];
  const txt=document.getElementById('voiceText').value.trim();
  const consent=document.getElementById('consentChk').checked;
  const msg=document.getElementById('voiceMsg'); const btn=document.getElementById('vbtn');
  if(!f){ msg.style.display='block'; msg.textContent='請先選一個音檔'; return; }
  if(!consent){ msg.style.display='block'; msg.innerHTML='請先勾選同意聲明（確認你是本人或已取得本人同意）。'; return; }
  btn.disabled=true; btn.textContent='處理中…（辨識+套用，約 10-30 秒）';
  const fd=new FormData(); fd.append('audio',f); fd.append('ref_text',txt); fd.append('consent',consent?'1':'');
  try{
    const r=await (await fetch('/setup/set-voice',{method:'POST',body:fd})).json();
    msg.style.display='block';
    msg.innerHTML = r.ok
      ? '✅ 已設為陪伴聲音'+(r.reloaded?'（已即時套用）':'（Qwen 未在跑，下次啟動生效）')+'。<br>逐字稿：「'+((r.ref_text||'').slice(0,40)||'(空)')+'」<br>→ 到上面「試聽現在的聲音」聽聽看。'
      : ('⚠ '+(r.detail||'失敗'));
    loadStatus();
  }catch(e){ msg.style.display='block'; msg.textContent='失敗：'+e; }
  btn.disabled=false; btn.textContent='設為陪伴聲音';
}
async function loadPhrases(){
  const box=document.getElementById('phrases');
  try{
    const ps=await (await fetch('/setup/phrases')).json();
    document.getElementById('phCount').textContent='（'+ps.filter(p=>p.has_audio).length+'/'+ps.length+' 已錄）';
    box.innerHTML = ps.map(p=>`
      <div class="row">
        <span class="dot" style="background:${p.has_audio?'#16a34a':'#d1d5db'}"></span>
        <div class="ph-text">${p.text||'(無文字)'}<div class="ph-trig">聽到「${(p.triggers||[]).join('、')}」就回這句 · ${p.file}${p.alert?' · ⚠️通報家人':''}</div></div>
        ${p.has_audio?`<button class="ghost sm" onclick="play('/setup/phrase-audio/'+encodeURIComponent('${p.file}')+'?t='+Date.now())">▶ 播放</button>`:''}
        <input type="file" accept="audio/*" id="f_${p.file}">
        <button class="sm" onclick="upPhrase('${p.file}')">上傳</button>
      </div>`).join('');
  }catch(e){ box.textContent='載入失敗：'+e; }
}
async function upPhrase(file){
  const inp=document.getElementById('f_'+file); const f=inp.files[0];
  if(!f){ alert('請先選音檔'); return; }
  const fd=new FormData(); fd.append('file',file); fd.append('audio',f);
  try{ await fetch('/setup/upload-phrase',{method:'POST',body:fd}); await loadPhrases(); await loadStatus(); }
  catch(e){ alert('上傳失敗：'+e); }
}
async function loadHistory(){
  const sb=document.getElementById('summary'), hb=document.getElementById('history');
  try{
    const d=await (await fetch('/setup/history')).json();
    if(d.summary){ sb.style.display='block'; sb.textContent='🧠 記住的重點：\\n'+d.summary; } else { sb.style.display='none'; }
    const r=d.recent||[];
    hb.innerHTML = r.length? r.map(m=>`<div class="turn"><span class="who ${m.role==='user'?'u':'a'}">${m.role==='user'?'爺爺':'陪伴'}</span>${m.content}</div>`).join('') : '<div class="muted">還沒有對話記錄。</div>';
  }catch(e){ hb.textContent='載入失敗：'+e; }
}
async function loadMode(){ try{ const d=await (await fetch('/setup/talk-mode')).json(); paintModeBtns(d.talk_mode); }catch(e){} }
async function loadPhotoGrid(){
  const grid=document.getElementById('photoGrid');
  try{
    const urls=await (await fetch('/photos')).json();
    document.getElementById('photoCount').textContent = urls.length? `（${urls.length} 張）` : '';
    grid.innerHTML = urls.length ? urls.map(u=>`
      <div style="position:relative;width:96px;height:96px">
        <img src="${u}" style="width:100%;height:100%;object-fit:cover;border-radius:10px;border:1px solid #eef0f4">
        <button class="sm ghost" onclick="deletePhoto('${decodeURIComponent(u.split('/').pop())}')" style="position:absolute;top:4px;right:4px;padding:1px 7px;font-size:12px;box-shadow:0 1px 3px rgba(20,30,60,.25)">✕</button>
      </div>`).join('') : '<span class="muted">還沒有照片，爺爺畫面會顯示暖色占位。</span>';
  }catch(e){ grid.innerHTML='<span class="muted">載入失敗</span>'; }
}
async function uploadPhotos(){
  const files=document.getElementById('photoFiles').files;
  const msg=document.getElementById('photoMsg'), btn=document.getElementById('photoBtn');
  if(!files.length){ msg.style.display='block'; msg.textContent='請先選照片'; return; }
  btn.disabled=true;
  let ok=0, fail=0;
  for(let i=0;i<files.length;i++){
    btn.textContent = `上傳中…（${i+1}/${files.length}）`;
    const fd=new FormData(); fd.append('photo', files[i]);
    try{
      const r=await (await fetch('/setup/upload-photo',{method:'POST',body:fd})).json();
      if(r.ok) ok++; else fail++;
    }catch(e){ fail++; }
  }
  msg.style.display='block';
  msg.textContent = fail ? `完成：${ok} 張成功、${fail} 張失敗（格式需 jpg/png/webp，單張上限 20MB）` : `✅ ${ok} 張照片已上傳`;
  document.getElementById('photoFiles').value='';
  btn.disabled=false; btn.textContent='上傳照片';
  loadPhotoGrid();
}
async function deletePhoto(fname){
  if(!confirm('刪除這張照片？')) return;
  const fd=new FormData(); fd.append('fname', fname);
  try{ await fetch('/setup/delete-photo',{method:'POST',body:fd}); }catch(e){}
  loadPhotoGrid();
}
function paintModeBtns(m){
  document.getElementById('modeHold').className = m==='hold'?'':'ghost';
  document.getElementById('modeAuto').className = m==='auto'?'':'ghost';
  document.getElementById('modeNow').textContent = '目前預設：'+(m==='auto'?'自動說話':'按住說話');
}
async function setMode(m){
  try{ const fd=new FormData(); fd.append('mode',m);
    const d=await (await fetch('/setup/talk-mode',{method:'POST',body:fd})).json(); paintModeBtns(d.talk_mode);
  }catch(e){ alert('設定失敗：'+e); }
}
loadStatus(); loadPhrases(); loadHistory(); loadMode(); loadPhotoGrid();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    print("=" * 50)
    print("  爺爺語音陪伴系統 - 網頁版")
    print("=" * 50)
    print(f"  平板 Chrome 打開：http://{local_ip}:8080")
    print("  確保平板和電腦在同一 WiFi")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
