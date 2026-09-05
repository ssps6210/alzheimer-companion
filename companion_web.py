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
import threading
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

# ── 聲音同意閘門：設定克隆音色前，錄音本人須先唸出同意聲明 ──────────────────
# 這句會被 whisper 轉出來、比對關鍵詞；由於同意句就在同一段錄音裡，說話者＝同意者，
# 把「同意」牢牢綁在「這個聲音」上。CONSENT_REQUIRED=0 可關（進階／本機用）。
CONSENT_REQUIRED = os.environ.get("CONSENT_REQUIRED", "1") != "0"
CONSENT_PHRASE   = "我同意用我的聲音陪伴家人"
CONSENT_KEYS     = ("同意", "陪伴")   # 兩個夠獨特的詞都出現才算通過（容忍 ASR 誤差、繁簡差異）

# ── 多語支援 ───────────────────────────────────────────────────────────────
# 繁體中文是原始語言（直接寫在這支程式裡）。lang/<code>.yaml 覆蓋三件事：
# 引擎語言代碼、安全關鍵詞、人設，外加一份介面對照表。
# 沒翻到的字串會留著中文——半套翻譯照樣能跑，不會變空白畫面。
LANG_DIR = os.path.join(SCRIPT_DIR, "lang")


def load_language(code):
    """讀語言包。找不到或沒裝 pyyaml 就回空 dict（＝維持繁體）。"""
    if not code or code in ("zh-TW", "zh-Hant", "zh"):
        return {}
    path = os.path.join(LANG_DIR, f"{code}.yaml")
    if not yaml or not os.path.exists(path):
        print(f"⚠ 找不到語言包 {code}（{path}），改用繁體中文")
        return {}
    try:
        d = yaml.safe_load(open(path, encoding="utf-8")) or {}
        print(f"語言包載入：{code}（{d.get('name', code)}）")
        return d
    except Exception as e:
        print(f"語言包 {code} 讀取失敗，改用繁體中文：{e}")
        return {}

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
    # 預設用「本機模型」：不需要任何金鑰，對話文字也不會離開這台電腦。
    # 連不上本機模型時，才退到雲端備援（要填自己的免費金鑰）。
    "llm":   {"base_url": "http://localhost:11434/v1", "model": "qwen2.5:3b",
              "api_key_env": "", "temperature": 0.7, "max_tokens": 150,
              "timeout": 25, "disable_thinking": True,
              "fallback_base_url": "https://integrate.api.nvidia.com/v1",
              "fallback_model": "nvidia/nemotron-3-super-120b-a12b",
              "fallback_api_key_env": "NVIDIA_API_KEY"},
    "tts":   {"cosyvoice_url": "http://localhost:50000/tts",
              "cosyvoice_health": "http://localhost:50000/health",
              "cosyvoice_timeout": 15, "edge_voice": "zh-TW-YunJheNeural"},
    "memory": {"max_history": 10, "persist": True, "summary_trigger": 24},
    "notify": {"telegram_token_env": "TELEGRAM_BOT_TOKEN",
               "telegram_chat_env": "TELEGRAM_CHAT_ID",
               "daily_summary_hour": 20},   # 每天幾點寄摘要給家人；-1 = 關閉
    "language": "zh-TW",   # 介面／語音／護欄的語言；見 lang/ 目錄（en、zh-CN）
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
        "12. 絕對不可以編造事實。被問到「某人有沒有來過」「某件事發生了沒」這類你無法確定的事，"
        "不可以回答有或沒有，更不可以描述任何細節（誰來了、帶了什麼、說了什麼、待多久，一律不准講）。"
        "改成溫柔地把話帶回當下，例如：「大家都很惦記你喔」「我先陪你好不好？」\n"
        "13. 回答要像說話一樣自然，不要有列表或特殊符號\n"
        "14. 你只是一個聲音，做不到任何實際的事。絕不答應開門、帶他出去、幫他拿東西、"
        "打電話給誰這類你做不到的事——承諾了做不到，他會更焦躁。尤其他說要自己出門時，"
        "不要順著答應（有走失風險），改成溫柔把注意力帶到當下（喝口水、坐著陪他聊聊），"
        "需要人幫忙就說「我請家人過來陪你」")}},
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
LANG = load_language(CFG.get("language", "zh-TW"))
UI_MAP = LANG.get("ui") or {}
# 長字串先換：短字串若是長字串的一部分，先換短的會把長的切壞
UI_KEYS = sorted(UI_MAP, key=len, reverse=True)


def _t(s):
    """把介面字串換成目前語言。沒有對照就原樣留著（＝退回中文，不會空白）。"""
    for k in UI_KEYS:
        if k in s:
            s = s.replace(k, UI_MAP[k])
    return s


# 語言包可覆蓋安全關鍵詞——中文的關鍵詞列表在英文部署裡完全無效，
# 不覆蓋的話護欄會「靜默失效」，這是最危險的一種壞法。
_SAFETY = LANG.get("safety") or {}
# 合成語言：一併傳給 TTS 服務，否則英文部署會用中文腔念英文
# 兩種格式都送：Qwen 吃 "English"／"Chinese"，XTTS 吃 "en"／"zh-cn"。
# companion 不知道對面跑的是哪一個，各自取自己看得懂的欄位。
TTS_LANG = LANG.get("tts_language") or ""
TTS_LANG_CODE = LANG.get("tts_language_xtts") or ""
if _SAFETY.get("consent_phrase"):
    CONSENT_PHRASE = _SAFETY["consent_phrase"]
if _SAFETY.get("consent_keys"):
    CONSENT_KEYS = tuple(_SAFETY["consent_keys"])

# Derive the original module-level names from CFG so downstream code is untouched.
WHISPER_SIZE   = CFG["asr"]["model"]
WHISPER_DEVICE = CFG["asr"]["device"]
WHISPER_CTYPE  = CFG["asr"]["compute_type"]
ASR_LANG       = LANG.get("asr_language") or CFG["asr"]["language"]
def _resolve_llm(cfg):
    """決定這次用哪個大腦。回 (base_url, model, api_key, 是否本機)。

    本機優先的理由不只是省一把金鑰：本機模型跑起來，**對話文字完全不出門**，
    這套系統就真的是 100% 離線的。雲端只是備援，而且要使用者自己填金鑰。
    """
    base, model = cfg["base_url"], cfg["model"]
    key = os.environ.get(cfg.get("api_key_env") or "", "") if cfg.get("api_key_env") else ""
    is_local = "localhost" in base or "127.0.0.1" in base

    if is_local:
        try:                      # 本機模型有在跑嗎？（Ollama 等 OpenAI 相容端點）
            requests.get(base.rstrip("/").rsplit("/v1", 1)[0] + "/api/tags", timeout=2)
            print(f"大腦：本機模型 {model}（對話文字不出這台電腦）")
            return base, model, key, True
        except Exception:
            fb = cfg.get("fallback_base_url")
            fb_key = os.environ.get(cfg.get("fallback_api_key_env") or "", "")
            if fb and fb_key:
                print(f"大腦：本機模型連不上 → 改用雲端備援 {cfg.get('fallback_model')}"
                      f"（對話文字會送到雲端）")
                return fb, cfg.get("fallback_model"), fb_key, False
            print(f"⚠ 大腦連不上：本機模型（{base}）沒在跑，也沒設定雲端備援金鑰。\n"
                  f"  兩條路擇一：① 裝 Ollama 並 `ollama pull {model}`（本機、免金鑰、最私密）\n"
                  f"            ② 在 .env 填 {cfg.get('fallback_api_key_env')}（雲端、較聰明）")
    if not is_local:
        print(f"大腦：雲端 {model}（對話文字會送到 {base.split('//')[-1].split('/')[0]}）")
    return base, model, key, is_local


LLM_BASE_URL, LLM_MODEL, LLM_API_KEY, LLM_IS_LOCAL = _resolve_llm(CFG["llm"])
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
# 語言包的人設優先（英文部署不能用中文人設——模型會用中文回覆英文使用者）
_chars  = dict(CFG["characters"])
for _n, _txt in (LANG.get("persona") or {}).items():
    _chars.setdefault(_n, {})
    _chars[_n] = dict(_chars[_n], persona=_txt)
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


# ── /setup 的密碼保護 ──────────────────────────────────────────────────────
# 家人管理台能上傳聲音、改設定，還能讀長輩的完整對話記錄——那是這整套系統裡
# 最私密的東西。只要有人拿到網址就能看，比聲音外流嚴重得多，所以它一定要有鎖。
#
# 預設就安全、又不增加負擔的做法：沒設密碼就自動產生一組寫進 .env，啟動時印出來。
# 長輩畫面（/）刻意不加鎖——長輩不可能輸入密碼，而那個畫面本來就沒有私密內容。
def _ensure_setup_password():
    pw = os.environ.get("SETUP_PASSWORD", "").strip()
    if pw:
        return pw
    import secrets
    pw = secrets.token_urlsafe(9)
    try:
        with open(_env_path, "a", encoding="utf-8") as f:
            f.write(f"\n# 家人管理台 /setup 的密碼（首次啟動自動產生，可自行改成好記的）\n"
                    f"SETUP_PASSWORD={pw}\n")
        print(f"\n{'='*54}\n  已為家人管理台產生密碼（也寫進 .env 了）：\n"
              f"    帳號：family    密碼：{pw}\n"
              f"  第一次開 /setup 時輸入，瀏覽器會記住。\n{'='*54}\n")
    except Exception as e:
        print(f"⚠ 無法寫入 .env（{e}）。本次密碼：family / {pw}")
    os.environ["SETUP_PASSWORD"] = pw
    return pw


SETUP_USER = os.environ.get("SETUP_USER", "family")
SETUP_PASSWORD = _ensure_setup_password()


@app.middleware("http")
async def _guard_setup(request: Request, call_next):
    """用 middleware 而不是逐一加裝飾器：以後新增 /setup/xxx 端點會自動受保護，
    不必仰賴有人記得加——漏掉一個就等於整個鎖形同虛設。"""
    if request.url.path.startswith("/setup"):
        import base64
        import hmac
        ok = False
        auth = request.headers.get("authorization", "")
        if auth.startswith("Basic "):
            try:
                user, _, pw = base64.b64decode(auth[6:]).decode("utf-8").partition(":")
                # compare_digest：避免用字串比較洩漏長度/內容的時間差
                ok = (hmac.compare_digest(user, SETUP_USER)
                      and hmac.compare_digest(pw, SETUP_PASSWORD))
            except Exception:
                ok = False
        if not ok:
            return Response(status_code=401, content="家人管理台需要密碼",
                            headers={"WWW-Authenticate": 'Basic realm="Family console"'})
    return await call_next(request)

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


# 絕對不能讓長輩聽到的字眼：揭穿親人的死訊。
# 為什麼需要這一層——persona 已經有規則叫模型別說，但實測顯示「靠 prompt 指令」
# 是機率性的（同一條規則會這次遵守、下次不遵守）。對失智長輩來說，一次失誤就是
# 重新經歷一次喪親之痛，所以這裡再加一道「確定性」的防線：真的出現就整句換掉。
_NEVER_SAY = tuple(_SAFETY.get("never_say") or
                   ("過世", "去世", "往生", "不在了", "已經死", "過身", "died", "passed away"))
# 「走了」單獨看不準——中文裡多半是「離開」而不是「過世」（「爸爸上班走了，晚上就回來」
# 正是我們想要的溫柔轉移，不能攔）。所以只在它跟明確的死亡語境同時出現時才算。
_DEATH_PAIRS = tuple(tuple(p) for p in (_SAFETY.get("death_pairs") or
                     [("走了", "不會回來"), ("走了", "好幾年"), ("走了", "很久"),
                      ("走了", "再也"), ("離開我們", "了")]))
# 不帶稱呼——每個家庭的叫法不同（爺爺／阿公／爸），寫死會在攔截時露出破綻
_SAFE_FALLBACK = _SAFETY.get("safe_fallback") or "大家都很惦記你喔。我先陪著你好不好？"


def guard_reply(s):
    """最後一道輸出防線。回 (安全的回覆, 是否被攔下)。"""
    if not s:
        return s, False
    low = s.lower()
    if any(w.lower() in low for w in _NEVER_SAY):
        return _SAFE_FALLBACK, True
    if any(all(w.lower() in low for w in pair) for pair in _DEATH_PAIRS):
        return _SAFE_FALLBACK, True
    return s, False


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


def _alert_level(v):
    """把 phrases.json 的 alert 欄位正規化成 'urgent' / 'notice' / None。
    舊格式 true 視為 'notice'，這樣既有設定檔不會壞。"""
    if v is True:
        return "notice"
    if isinstance(v, str) and v.lower() in ("urgent", "notice"):
        return v.lower()
    return None


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
                # 分級："urgent"（出聲）/ "notice"（靜音推播）/ None。
                # 舊格式相容：alert: true → "notice"
                "alert": _alert_level(rule.get("alert")),
            })
    print(f"固定句快取：載入 {len(PHRASES)} 條")


_NEGATION = tuple(_SAFETY.get("negation") or ("不", "沒", "別", "未", "甭"))
# 中文的否定詞緊貼關鍵詞（「沒跌倒」），英文隔得遠（"didn't fall"）→ 回看視窗可調
_NEG_WINDOW = int(_SAFETY.get("negation_window", 2))

def _mentions(text, words):
    """text 是否提到 words 之一（且不是被否定的）。跟 match_phrase 用同一套否定判斷。

    往前看兩個字，不是一個：「沒有跌倒」「沒有不舒服」的否定詞隔了一個「有」，
    只看前一字會把它當成真的跌倒／不舒服，害家人收到假警報。
    """
    low = text.lower()   # 英文關鍵詞是小寫，句首大寫的「Help me」也要抓到
    for t in words:
        tl = t.lower()
        i = low.find(tl)
        while i != -1:
            before = low[max(0, i - _NEG_WINDOW):i]
            if not any(nw.lower() in before for nw in _NEGATION):
                return t
            i = low.find(tl, i + 1)
    return None


def match_phrase(text):
    """First rule with a trigger that appears AND is not immediately negated wins.
    Substring match, but a hit is skipped if the char just before it is a negation
    (不痛 / 沒事 / 別怕…) to avoid the obvious false positives. If every occurrence
    of a trigger is negated, that rule is skipped."""
    for p in PHRASES:
        if _mentions(text, p["triggers"]):
            return p
    return None


# 緊急關鍵字：刻意「不」綁在固定句上——固定句需要家人錄好的音檔才會生效，
# 但「跌倒」「救命」不能因為家人還沒錄音就不通報。這條路獨立判斷、永遠有效。
# 注意詞要夠具體：單放「心臟」會把「我心臟不好，吃很多年藥了」這種慢性陳述判成緊急，
# 假警報多了，家人就會開始忽略緊急通知——那才是真正危險的事。
URGENT_WORDS = tuple(_SAFETY.get("urgent_words") or
                     ("跌倒", "摔倒", "摔跤", "救命", "喘不過氣", "喘不過來",
                      "心絞痛", "流血", "起不來", "站不起來", "叫救護車", "很喘"))
# 部位＋症狀分開比對：中間插了程度詞也抓得到（「胸口好悶」「心臟很痛」），
# 又不會像單放「心臟」那樣把「我心臟不好，吃很多年藥了」誤判成緊急。
URGENT_PAIRS = tuple(tuple(p) for p in (_SAFETY.get("urgent_pairs") or
                     [("胸口", "悶"), ("胸口", "痛"), ("心臟", "痛"),
                      ("心臟", "不舒服"), ("喘", "不過")]))


def urgency_of(text, phrase_hit):
    """回傳 'urgent' / 'notice' / None。緊急詞優先，其次才看命中的固定句分級。"""
    if _mentions(text, URGENT_WORDS):
        return "urgent"
    for pair in URGENT_PAIRS:
        if all(_mentions(text, (w,)) for w in pair):
            return "urgent"
    if phrase_hit:
        return phrase_hit.get("alert") or None
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


# ── 「最近常說的話」：幫家人看見長輩在意什麼 ──────────────────────────
# 刻意的界線：這是陪伴觀察，不是醫療判讀，也不是行為監控。呈現方式一律是
# 「他最近常提到什麼」，不做退化程度評分、不下任何健康結論——那是醫師的事。
# 為什麼要另外存一份：history 只留最近 10 則、其餘會被摺疊進摘要，算不出趨勢。
PATTERNS_FILE = os.path.join(SCRIPT_DIR, "patterns.json")
PATTERN_KEEP_DAYS = 14      # 只留兩週，看得出近況又不會無限累積
PATTERN_MAX_GROUPS = 200    # 上限，避免檔案無限長大
_SIMILAR_ENOUGH = 0.65      # 「我要回家」「我想回家了」要能歸成同一件事（實測 0.667）
patterns = []               # [{"key":str, "times":[unix_ts,...]}]


def _norm(s):
    """去掉標點與空白，讓「現在幾點？」和「現在幾點」算同一句。"""
    return re.sub(r"[\s，。？！、,.?!~…；;：:「」『』（）()]", "", s or "")


def load_patterns():
    global patterns
    try:
        if os.path.exists(PATTERNS_FILE):
            patterns = json.load(open(PATTERNS_FILE, encoding="utf-8")).get("groups", [])
    except Exception as e:
        print(f"常說的話載入失敗（忽略）：{e}")
        patterns = []


def save_patterns():
    try:
        with open(PATTERNS_FILE, "w", encoding="utf-8") as f:
            json.dump({"groups": patterns}, f, ensure_ascii=False)
    except Exception as e:
        print(f"常說的話儲存失敗（忽略）：{e}")


def track_utterance(text, now=None):
    """記一次長輩說的話，歸到相近的group。失敗一律吞掉——這是附加功能，不能影響對話。"""
    try:
        import difflib
        key = _norm(text)
        if len(key) < 2:
            return
        ts = int(now or time.time())
        cutoff = ts - PATTERN_KEEP_DAYS * 86400

        best, best_ratio = None, 0.0
        for g in patterns:
            r = difflib.SequenceMatcher(None, key, g["key"]).ratio()
            if r > best_ratio:
                best, best_ratio = g, r
        if best is not None and best_ratio >= _SIMILAR_ENOUGH:
            best["times"].append(ts)
        else:
            patterns.append({"key": key, "times": [ts]})

        # 汰舊：丟掉兩週前的紀錄，整組都空了就移除
        for g in patterns:
            g["times"] = [t for t in g["times"] if t >= cutoff]
        patterns[:] = [g for g in patterns if g["times"]]
        if len(patterns) > PATTERN_MAX_GROUPS:      # 留最常出現的
            patterns.sort(key=lambda g: len(g["times"]), reverse=True)
            del patterns[PATTERN_MAX_GROUPS:]
        save_patterns()
    except Exception as e:
        print(f"常說的話記錄失敗（忽略）：{e}")


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
        body = {"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}],
                "stream": False, "temperature": 0.3, "max_tokens": 220}
        if LLM_NOTHINK:
            body["chat_template_kwargs"] = {"enable_thinking": False}
        r = await run_in_threadpool(lambda: requests.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=({"Authorization": f"Bearer {LLM_API_KEY}"} if LLM_API_KEY else {}),
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


async def notify_family(text, level="notice"):
    """Push a message to family via Telegram. Best-effort; no-op if unconfigured.

    分級的用意：如果每件小事都讓家人的手機響，家人最後會直接關掉通知——那時
    真正的緊急狀況也傳不到。所以只有 urgent（跌倒／胸口／救命）才出聲，
    其餘用 Telegram 的靜音推播，家人有空再看。
    """
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT):
        return
    urgent = (level == "urgent")
    body = {"chat_id": TELEGRAM_CHAT,
            "text": ("🚨【緊急】" if urgent else "⚠️【留意】") + text,
            "disable_notification": not urgent}   # notice → 靜音送達
    try:
        await run_in_threadpool(lambda: requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json=body, timeout=10))
        print(f"［已通知家人／{level}］{text[:40]}")
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
    body = {"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}],
            "stream": False, "temperature": 0.4, "max_tokens": 200}
    if LLM_NOTHINK:
        body["chat_template_kwargs"] = {"enable_thinking": False}
    r = await run_in_threadpool(lambda: requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers=({"Authorization": f"Bearer {LLM_API_KEY}"} if LLM_API_KEY else {}), json=body, timeout=LLM_TIMEOUT))
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
    # 背景執行緒跑，不 await：zeroconf 在複雜網路（VPN/虛擬網卡）下可能卡住甚至掛住，
    # 這是加分項，絕不能拖累核心服務（Whisper/大腦/克隆聲）的啟動——daemon=True 讓它卡死也不擋程式關閉。
    threading.Thread(target=_advertise_mdns, daemon=True).start()
    if not LLM_API_KEY and not LLM_IS_LOCAL:
        print("⚠ 雲端大腦需要金鑰，但沒設定 → LLM 會無法回應")
    if not (TELEGRAM_TOKEN and TELEGRAM_CHAT):
        print("（未設定 Telegram，家人通知/每日摘要停用）")
    load_phrases()
    load_memory()
    load_patterns()
    _fire_bg(daily_summary_loop())
    print("載入 Whisper...")
    whisper = WhisperModel(WHISPER_SIZE, device=WHISPER_DEVICE, compute_type=WHISPER_CTYPE)
    print("Whisper 就緒")


@app.get("/")
async def index():
    return HTMLResponse(_t(HTML)
                        .replace("__CLIENT_TIMEOUT_MS__", str(CLIENT_TIMEOUT_MS))
                        .replace("__DEFAULT_MODE__", DEFAULT_TALK_MODE))


@app.get("/health")
async def health():
    """Diagnostic: reports each link (Whisper / MiMo / CosyVoice) so you can see
    exactly what's broken during bring-up. Runs live reachability checks."""
    wh = {"loaded": whisper is not None, "size": WHISPER_SIZE}

    def _check_llm():
        if not LLM_API_KEY and not LLM_IS_LOCAL:
            return {"ok": False, "error": "雲端大腦需要金鑰，但 .env 沒設定"}
        try:
            t = time.time()
            hbody = {"model": LLM_MODEL,
                     "messages": [{"role": "user", "content": "嗨"}],
                     "max_tokens": 1, "stream": False}
            if LLM_NOTHINK:  # mirror the real request path
                hbody["chat_template_kwargs"] = {"enable_thinking": False}
            r = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers=({"Authorization": f"Bearer {LLM_API_KEY}"} if LLM_API_KEY else {}),
                json=hbody, timeout=8)
            r.raise_for_status()
            return {"ok": True, "model": LLM_MODEL, "latency_ms": int((time.time() - t) * 1000)}
        except Exception as e:
            return {"ok": False, "model": LLM_MODEL, "error": str(e)}

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

    llm = await run_in_threadpool(_check_llm)
    cosy = await run_in_threadpool(_check_cosy)
    edge = {"available": edge_tts is not None}

    if not wh["loaded"] or not llm["ok"]:
        status = "error"          # 核心鏈斷，無法回應
    elif not cosy["ok"]:
        status = "degraded"       # 可用，但無克隆聲音，靠 edge-tts（Phase 0 預期狀態）
    else:
        status = "ok"

    return {"status": status, "whisper": wh, "llm": llm,
            "cosyvoice": cosy, "edge_tts": edge, "phrases": len(PHRASES),
            # 本機模型不需要金鑰，所以「就緒」＝本機在跑 或 有填雲端金鑰
            "llm_key_set": bool(LLM_API_KEY) or LLM_IS_LOCAL,
            "llm_is_local": LLM_IS_LOCAL,
            "llm_key_env": CFG["llm"].get("fallback_api_key_env") or ""}


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
AUDIO_EXTS = (".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".webm")
AUDIO_MAX_BYTES = 50 * 1024 * 1024   # 50MB：10-30 秒的參考音遠遠用不到這麼多


async def _read_upload(upload, max_bytes, allowed_exts, what="檔案"):
    """讀取上傳內容，同時擋掉「太大」與「型別不對」。

    邊讀邊算而不是 `await upload.read()` 一次吃完：後者對一個超大檔會先把整包
    塞進記憶體，才有機會判斷它太大——那時已經來不及了。
    """
    ext = (os.path.splitext(upload.filename or "")[1] or "").lower()
    if allowed_exts and ext not in allowed_exts:
        raise HTTPException(status_code=400,
                            detail=f"不支援這種{what}格式（可用：{'、'.join(allowed_exts)}）")
    buf, size = [], 0
    while True:
        chunk = await upload.read(1024 * 1024)
        if not chunk:
            break
        size += len(chunk)
        if size > max_bytes:
            raise HTTPException(status_code=400,
                                detail=f"{what}太大（上限 {max_bytes // 1048576}MB）")
        buf.append(chunk)
    return b"".join(buf), ext


@app.post("/setup/upload-photo")
async def setup_upload_photo(photo: UploadFile = File(...)):
    """家人上傳爺爺的老照片（懷舊輪播用）。/setup 網頁跟 App 原生選圖都打這支，
    後端邏輯共用一份。檔名前綴時間戳記，讓輪播順序約略照上傳先後（list_photos 會排序）。"""
    os.makedirs(PHOTOS_DIR, exist_ok=True)
    data, ext = await _read_upload(photo, PHOTO_MAX_BYTES, PHOTO_EXTS, "圖片")
    if len(data) < 100:
        raise HTTPException(status_code=400, detail="圖片是空的")
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
    return HTMLResponse(_t(SETUP_HTML))


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
    data, _ = await _read_upload(audio, AUDIO_MAX_BYTES, AUDIO_EXTS, "音檔")
    with open(dest, "wb") as f:
        f.write(data)
    load_phrases()
    return {"ok": True, "file": os.path.basename(file), "bytes": len(data), "phrases": len(PHRASES)}


@app.post("/setup/upload-voice")
async def setup_upload_voice(name: str = Form("family"), audio: UploadFile = File(...)):
    """Save a family voice source (used later to build the cloned voice)."""
    vdir = os.path.join(SCRIPT_DIR, "voices")
    os.makedirs(vdir, exist_ok=True)
    data, ext = await _read_upload(audio, AUDIO_MAX_BYTES, AUDIO_EXTS, "音檔")
    fname = os.path.basename(name) + (ext or ".wav")
    with open(os.path.join(vdir, fname), "wb") as f:
        f.write(data)
    # 只回檔名不回絕對路徑：回應內容沒必要洩漏這台機器的目錄結構
    return {"ok": True, "saved": fname, "bytes": len(data)}


def _voice_quality_problem(wav, sr=24000):
    """檢查參考音品質，有問題就回一句「照著做就能改善」的中文說明，沒問題回 None。

    為什麼要擋：家人常常錄了就上傳，直到長輩聽見奇怪的聲音才發現錄壞了。
    在這裡花 0.01 秒判斷，勝過讓長輩聽一整天不像家人的聲音。
    """
    n = len(wav)
    if n == 0:
        return "這個音檔沒有聲音，請換一個檔案。"
    dur = n / sr
    if dur < 8:
        return f"這段錄音只有 {dur:.0f} 秒，太短了，聲音會不像。請錄 10–30 秒再上傳。"
    if dur > 180:
        return f"這段錄音長達 {dur/60:.0f} 分鐘。請剪成 10–30 秒最自然的一段再上傳。"

    peak = float(np.abs(wav).max())
    rms = float(np.sqrt(np.mean(np.square(wav))))
    if peak < 0.05 or rms < 0.01:
        return "錄音太小聲了，聽起來會模糊。請靠近麥克風、或把錄音音量調大，重錄一次。"
    if float(np.mean(np.abs(wav) > 0.99)) > 0.01:
        return "錄音有破音（音量過大導致失真）。請離麥克風遠一點、或把音量調小，重錄一次。"

    # 靜音比例：切成 20ms 一格，看有多少格幾乎沒聲音
    win = int(sr * 0.02)
    frames = wav[:n - n % win].reshape(-1, win) if n >= win else wav.reshape(1, -1)
    frame_rms = np.sqrt(np.mean(np.square(frames), axis=1))
    quiet_ratio = float(np.mean(frame_rms < max(0.01, peak * 0.05)))
    if quiet_ratio > 0.6:
        return ("這段錄音有超過一半是空白或雜訊，可用的人聲太少。"
                "請在安靜的地方連續說 10–30 秒，中間不要有長時間停頓。")
    return None


@app.post("/setup/set-voice")
async def setup_set_voice(audio: UploadFile = File(...), ref_text: str = Form(""),
                          consent: str = Form("")):
    """使用者上傳一段參考音 → 設為 Qwen 的克隆音色。
    存 voices/active_reference.wav (+ 逐字稿 .txt)，再叫 Qwen 熱重載，不用重啟。
    這是開源版讓「每個人塞自己想要的音色」的入口。

    同意閘門：CONSENT_REQUIRED 時，錄音本人須在錄音裡先唸同意聲明，
    且需勾選確認；同意證明存 voices/active_reference.consent.json。"""
    if CONSENT_REQUIRED and not consent.strip():
        raise HTTPException(status_code=400,
            detail="請先勾選下方的同意聲明（確認你是本人或已取得本人同意），才能設定聲音。")
    vdir = os.path.join(SCRIPT_DIR, "voices")
    os.makedirs(vdir, exist_ok=True)
    raw, ext = await _read_upload(audio, AUDIO_MAX_BYTES, AUDIO_EXTS, "音檔")
    if len(raw) < 2000:
        raise HTTPException(status_code=400, detail="音檔太短或空的")
    up = os.path.join(vdir, "active_reference_upload" + (ext or ".wav"))
    with open(up, "wb") as f:
        f.write(raw)
    # 解碼（faster-whisper 的 decode_audio 走 PyAV，支援 wav / mp3 / m4a）
    from faster_whisper.audio import decode_audio
    try:
        wav24 = await run_in_threadpool(lambda: decode_audio(up, sampling_rate=24000))
    except Exception as e:
        # 不把原始例外回給呼叫端：decode_audio 的訊息會帶上本機檔案路徑
        print(f"音檔解碼失敗：{e}")
        raise HTTPException(status_code=400,
                            detail="讀不了這個音檔，請換成 wav / mp3 / m4a 再試一次")
    # 品質把關：在覆蓋既有音色「之前」擋下來，也在跑 whisper 之前（省下無謂的等待）。
    # 音訊已經解好在記憶體裡，這幾個判斷幾乎不花成本。
    problem = _voice_quality_problem(wav24)
    if problem:
        try:
            os.remove(up)
        except OSError:
            pass
        raise HTTPException(status_code=400, detail=problem)
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
        said = ((rt or "") + " " + (ref_text or "")).lower()
        if not all(k.lower() in said for k in CONSENT_KEYS):
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
            COSY_URL, json={"text": reply, "speed": 1.0, "language": TTS_LANG, "language_code": TTS_LANG_CODE}, timeout=COSY_TIMEOUT))
        if tts_r.status_code == 200 and tts_r.content:
            return Response(content=tts_r.content, media_type="audio/wav")
    except Exception:
        pass
    try:
        mp3 = await edge_tts_synth(reply)
        return Response(content=mp3, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/setup/patterns")
async def setup_patterns():
    """「最近常說的話」：家人看得到爺爺這陣子在意什麼、哪個時段最需要陪伴。

    刻意只回原始次數與時段，不做任何評分或健康判讀——那是醫師的專業，不是這個
    工具該下的結論。家人自己看到「他這兩天一直問要回家」，比任何分數都有用。
    """
    now = int(time.time())
    day, week = now - 86400, now - 7 * 86400
    items = []
    for g in patterns:
        today = sum(1 for t in g["times"] if t >= day)
        wk = sum(1 for t in g["times"] if t >= week)
        if wk:
            items.append({"text": g["key"], "today": today, "week": wk,
                          "last": max(g["times"])})
    items.sort(key=lambda x: (-x["week"], -x["last"]))

    # 一天當中哪個時段說得最多（0-23 → 分成四段），幫家人抓陪伴的時機
    buckets = {"清晨 (0-6)": 0, "上午 (6-12)": 0, "下午 (12-18)": 0, "晚上 (18-24)": 0}
    labels = list(buckets)
    for g in patterns:
        for t in g["times"]:
            if t >= week:
                buckets[labels[min(3, datetime.fromtimestamp(t).hour // 6)]] += 1
    return {"items": items[:12], "by_time": buckets,
            "total_week": sum(i["week"] for i in items)}


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
    track_utterance(text)   # 記進「最近常說的話」，給家人看趨勢（不影響回覆路徑）

    hit = match_phrase(text)

    # 通報判斷放在固定句「之外」：緊急詞不能因為家人還沒錄那句音檔就漏掉通報。
    level = urgency_of(text, hit)
    if level:
        _fire_bg(notify_family(
            f"爺爺剛說了：「{text}」（{datetime.now():%H:%M}），請留意。", level))

    if hit:
        print(f"［固定句命中］→ {hit['text']}")
        _remember(text, hit["text"])
        return _audio_response(hit["audio"], hit["media"], text, hit["text"])

    # Open-ended LLM path: ignore too-short noise that matched no phrase.
    if len(text) < 2:
        return JSONResponse({"type": "no_speech"})

    msgs = [{"role": "system", "content": get_system_prompt()}]
    msgs.extend(history[-MAX_HISTORY:])
    msgs.append({"role": "user", "content": text})

    body = {"model": LLM_MODEL, "messages": msgs, "stream": False,
            "temperature": LLM_TEMP, "max_tokens": LLM_MAXTOK}
    if LLM_NOTHINK:
        # Disable reasoning. Nemotron-3 accepts this too (verified: reasoning→0,
        # clean content). Critical: with reasoning ON, its 200-1000-char think
        # doesn't fit max_tokens=80 → the truncated think LEAKS into content and
        # 爺爺 hears the model's inner monologue (incl. "as a granddaughter…").
        body["chat_template_kwargs"] = {"enable_thinking": False}
    try:
        r = await run_in_threadpool(lambda: requests.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers=({"Authorization": f"Bearer {LLM_API_KEY}"} if LLM_API_KEY else {}),
            json=body, timeout=LLM_TIMEOUT))
        r.raise_for_status()
        reply = (r.json()["choices"][0]["message"].get("content") or "").strip()
        reply = _sanitize_reply(reply)
        reply, blocked = guard_reply(reply)
        if blocked:
            # 家人該知道模型差點說出死訊——這代表 persona 需要檢查
            print(f"⚠ 已攔截不該說出口的回覆（原內容含死訊字眼），改用安撫語")
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
            json={"text": reply, "speed": 1.0, "language": TTS_LANG, "language_code": TTS_LANG_CODE,
                  "spk_id": CHARACTER.get("cosyvoice_spk", "")},
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
    <span style="font-size:12px">同意句就在同一段錄音裡，代表「這個聲音的本人」確實同意。系統聽到才會設定。<br>另外，所有生成的語音都會打上聽不見的 AI 浮水印，事後可以驗證「這段是 AI 合成的，不是本人說的」。</span>
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
  <h2>📈 爺爺最近常說的話 <span class="muted" id="patCount"></span></h2>
  <p class="hint">看得出爺爺這陣子<b>在意什麼</b>、什麼時段最需要陪伴——例如一直問「要回家」，
  也許是傍晚特別不安。<b>這是陪伴觀察，不是醫療診斷</b>，任何健康上的疑問請諮詢醫師。</p>
  <div id="patterns">載入中…</div>
  <div style="margin-top:12px"><button class="ghost sm" onclick="loadPatterns()">🔄 重新整理</button></div>
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
      b(h.llm&&h.llm.ok,'大腦')+
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
        <div class="ph-text">${p.text||'(無文字)'}<div class="ph-trig">聽到「${(p.triggers||[]).join('、')}」就回這句 · ${p.file}${p.alert==='urgent'?' · 🚨緊急通報(出聲)':(p.alert?' · ⚠️留意通報(靜音)':'')}</div></div>
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
async function loadPatterns(){
  const box=document.getElementById('patterns');
  try{
    const d=await (await fetch('/setup/patterns')).json();
    const items=d.items||[];
    document.getElementById('patCount').textContent = d.total_week? '（近七天 '+d.total_week+' 次）' : '';
    if(!items.length){ box.innerHTML='<span class="muted">還沒有足夠的對話記錄。</span>'; return; }
    const max=Math.max(...items.map(i=>i.week));
    box.innerHTML = items.map(i=>`
      <div class="row">
        <div class="ph-text">${i.text}
          <div class="ph-trig">近七天 ${i.week} 次${i.today? ' · 今天 '+i.today+' 次':''}</div>
        </div>
        <div style="flex:0 0 120px;background:#eef1f8;border-radius:6px;height:10px;overflow:hidden">
          <div style="width:${Math.round(i.week/max*100)}%;height:100%;background:#26418f"></div>
        </div>
      </div>`).join('');
    const bt=d.by_time||{};
    const tmax=Math.max(1,...Object.values(bt));
    box.innerHTML += '<div style="margin-top:14px;font-size:13px;color:#7a8494">說話最多的時段（近七天）</div>'
      + Object.entries(bt).map(([k,v])=>`
        <div class="row" style="padding:6px 0">
          <div style="flex:0 0 110px;font-size:13px">${k}</div>
          <div style="flex:1;background:#eef1f8;border-radius:6px;height:10px;overflow:hidden">
            <div style="width:${Math.round(v/tmax*100)}%;height:100%;background:#b45309"></div>
          </div>
          <div class="muted" style="flex:0 0 40px;text-align:right">${v}</div>
        </div>`).join('');
  }catch(e){ box.innerHTML='<span class="muted">載入失敗</span>'; }
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
loadStatus(); loadPhrases(); loadHistory(); loadMode(); loadPhotoGrid(); loadPatterns();
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
