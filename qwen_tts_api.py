"""
Qwen3-TTS 聲音克隆服務（跑在 WSL2，被 Windows 的 companion 呼叫）。
介面：POST /tts {text} → audio/wav（用目前設定的音色克隆）。

音色來源優先序（開源友善：clone 下來沒有任何人的聲音，由使用者自己上傳）：
  1. voices/active_reference.wav  ← 使用者在 /setup 前端上傳（+ 同名 .txt 逐字稿）
  2. QWEN_REF（本地舊預設，例如 father_reference.wav；已被 .gitignore，clone 不會有）
  3. 都沒有 → /tts 回 503 → companion 自動改用通用聲（edge-tts），不會壞。
換音色不用重啟：companion 上傳後打 POST /reload-ref 熱重載。

啟動：由 scripts/_start_qwen.sh 啟動（自動定位專案路徑，無需硬編）
"""
import os, io, re
import numpy as np
import soundfile as sf
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import wm   # 共用的 AI 浮水印（AudioSeal，CPU）；Qwen 與 XTTS-CPU 兩個服務共用

_HERE = os.path.dirname(os.path.abspath(__file__))   # 專案根目錄（本檔所在）；放哪都能跑
VOICES_DIR = os.environ.get("QWEN_VOICES", os.path.join(_HERE, "voices"))
ACTIVE_REF = os.path.join(VOICES_DIR, "active_reference.wav")   # 使用者上傳的音色（優先）
LEGACY_REF = os.environ.get("QWEN_REF", os.path.join(_HERE, "father_reference.wav"))  # 本地舊預設
MODEL_ID = os.environ.get("QWEN_MODEL", "Qwen/Qwen3-TTS-12Hz-1.7B-Base")
LANG = os.environ.get("QWEN_LANG", "Chinese")
PORT = int(os.environ.get("QWEN_PORT", 50000))
MAX_LEN = int(os.environ.get("QWEN_MAX_LEN", 58))   # ~16s 上限；每塊貪婪合併到 10-16s 甜蜜區（太短不像、>18s 會飄）

app = FastAPI(title="Qwen3-TTS voice clone")
model = None
REF_AUDIO = None   # 目前生效的參考音路徑（None = 尚未設定 → /tts 回 503）
ref_text = ""


def _transcribe(path):
    # 最後手段：沒有逐字稿檔時用 whisper 轉（會下載 whisper-small）。
    # 正常情況 companion 上傳音色時就已用它自己的 whisper 寫好 .txt，走不到這裡。
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-small",
                   device=0, torch_dtype=torch.float16)
    t = asr(path, generate_kwargs={"language": "zh", "task": "transcribe"})["text"].strip()
    import gc; del asr; gc.collect(); torch.cuda.empty_cache()
    return t


def _resolve_ref():
    """回 (audio_path or None, ref_text)。優先使用者音色 > 本地舊預設 > 無。"""
    for a in (ACTIVE_REF, LEGACY_REF):
        if a and os.path.exists(a):
            txt = os.path.splitext(a)[0] + ".txt"
            if os.path.exists(txt):
                rt = open(txt, encoding="utf-8").read().strip()
            else:
                rt = _transcribe(a)
                try:
                    open(txt, "w", encoding="utf-8").write(rt)
                except Exception:
                    pass
            return a, rt
    return None, ""


def _apply_ref():
    global REF_AUDIO, ref_text
    REF_AUDIO, ref_text = _resolve_ref()
    if REF_AUDIO:
        print(f"音色參考: {REF_AUDIO}｜逐字稿({len(ref_text)}字): {ref_text[:30]}…")
    else:
        print("尚未設定音色（到 /setup 上傳一段參考音）→ /tts 暫回 503，companion 用通用聲")
    return REF_AUDIO


def _split(text):
    # 目標：每塊落在 Qwen 音色最像的甜蜜區（~10-16s）。先切句，再貪婪合併到 ~MAX_LEN 字：
    # 太短(<~8s)音色還沒鎖定就不像；太長(>~18s)後半會飄。合併讓短句不落單。
    if len(text) <= MAX_LEN:
        return [text]
    units = [s.strip() for s in re.split(r'(?<=[。！？!?\n])', text) if s.strip()]
    flat = []
    for u in units:
        while len(u) > MAX_LEN:               # 單句仍過長 → 硬切
            flat.append(u[:MAX_LEN]); u = u[MAX_LEN:]
        if u:
            flat.append(u)
    out = []
    for u in flat:                            # 貪婪合併到 MAX_LEN
        if out and len(out[-1]) + len(u) <= MAX_LEN:
            out[-1] += u
        else:
            out.append(u)
    return out or [text]


@app.on_event("startup")
def load():
    global model
    from qwen_tts import Qwen3TTSModel
    print(f"載入 {MODEL_ID} …")
    # flash_attention_2 快 2-3 倍且更省顯存；沒裝就自動退回 sdpa/eager（開源友善）
    for impl in ("flash_attention_2", "sdpa", "eager"):
        try:
            model = Qwen3TTSModel.from_pretrained(MODEL_ID, device_map="cuda:0",
                                                  dtype=torch.bfloat16, attn_implementation=impl)
            print(f"Qwen3-TTS 就緒（attn={impl}）")
            break
        except Exception as e:
            print(f"attn={impl} 不可用：{e}")
    _apply_ref()   # 模型好了再解析音色（若要 whisper 轉稿，此時 GPU 已就緒）
    wm.load()      # 載入浮水印（CPU，不影響 GPU 顯存）


@app.get("/health")
def health():
    return {"status": "ok",
            "ref_loaded": model is not None and REF_AUDIO is not None,  # 有模型且有音色才算就緒
            "model_loaded": model is not None,
            "ref_set": REF_AUDIO is not None,
            "ref_path": REF_AUDIO or "",
            "watermark": wm.ok(),   # 克隆語音是否打上 AI 浮水印（可事後驗證為合成）
            "sample_rate": wm.WM_SR if wm.ok() else 24000, "model": MODEL_ID}


@app.post("/reload-ref")
def reload_ref():
    """companion 上傳新音色後呼叫：重新解析 voices/active_reference.wav，不用重啟。"""
    a = _apply_ref()
    return {"ok": True, "ref_set": a is not None, "ref_path": a or "", "ref_text_len": len(ref_text)}


class TTSReq(BaseModel):
    text: str
    speed: float = 1.0
    spk_id: str = ""
    language: str = ""        # Qwen 格式（"English"／"Chinese"）；空字串＝用服務端預設
    language_code: str = ""   # XTTS 格式；本服務不用，宣告出來才不會被當成非法欄位


@app.post("/tts")
def tts(req: TTSReq):
    if model is None:
        raise HTTPException(503, "model not loaded")
    if REF_AUDIO is None:
        raise HTTPException(503, "no reference voice set")   # → companion 改用 edge-tts 通用聲
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "empty text")
    chunks = []
    try:
        for piece in _split(text):          # 逐句合成，短句穩、不飄
            wavs, sr = model.generate_voice_clone(text=piece, language=(req.language or LANG),
                                                  ref_audio=REF_AUDIO, ref_text=ref_text)
            chunks.append(np.asarray(wavs[0], dtype=np.float32))
    except Exception as e:
        raise HTTPException(500, str(e))
    audio = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
    audio, out_sr = wm.apply(audio, 24000)   # 打上 AI 浮水印（可事後驗證）；未就緒則原樣輸出
    buf = io.BytesIO()
    sf.write(buf, audio, out_sr, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return Response(content=buf.read(), media_type="audio/wav")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
