"""XTTS-CPU 聲音克隆服務（無顯卡也能跑，可在 Windows 直接跑，不需要 WSL/CUDA）。

跟 qwen_tts_api.py 講「同一套」HTTP 介面，所以是 Qwen 的 drop-in 替代：
  POST /tts {text} → audio/wav（用目前設定的音色克隆）
  GET  /health              /  POST /reload-ref
companion 完全不用改，只要這支或 Qwen 其中一個跑在同一個 port（預設 50000）即可。

取捨（相對 Qwen GPU 版）：
  ✓ 沒有 NVIDIA 顯卡也能用，且「保住家人的聲音」（一樣是克隆）
  ✓ 完全本機、不出網（聲音絕不離開這台電腦）
  ✗ 慢：CPU 上一句話約數秒~十幾秒（常用話走 phrases 秒回墊著，只有開放對話才吃這段）

音色來源：voices/active_reference.wav（使用者在 /setup 上傳，同一套流程、同一道同意閘門）。
浮水印：與 Qwen 版共用 wm.py（AudioSeal，CPU），所有克隆語音一樣標記為 AI 合成。

模型：Coqui XTTS-v2（多語、零樣本克隆）。授權為 CPML（**僅供非商業用途**；家庭/個人照護 OK）。
首次會下載模型（約 1.8GB）。COQUI_TOS_AGREED=1 讓下載不卡在互動同意提示。

啟動：venv\\Scripts\\python.exe xtts_cpu_api.py   （或由 launch_cpu.ps1 帶起）
"""
import os, io, re
os.environ.setdefault("COQUI_TOS_AGREED", "1")   # 非互動下載 XTTS（CPML 非商業授權，見檔頭）
import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import wm   # 共用的 AI 浮水印（AudioSeal，CPU）

_HERE = os.path.dirname(os.path.abspath(__file__))   # 專案根目錄；放哪都能跑
VOICES_DIR = os.environ.get("QWEN_VOICES", os.path.join(_HERE, "voices"))
ACTIVE_REF = os.path.join(VOICES_DIR, "active_reference.wav")
LEGACY_REF = os.environ.get("QWEN_REF", os.path.join(_HERE, "father_reference.wav"))
MODEL_ID = os.environ.get("XTTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
LANG = os.environ.get("XTTS_LANG", "zh-cn")          # XTTS 中文用 zh-cn
PORT = int(os.environ.get("QWEN_PORT", 50000))       # 與 Qwen 同 port → companion 免改
MAX_LEN = int(os.environ.get("XTTS_MAX_LEN", 120))   # XTTS 單塊字數上限（過長會被截/報錯）

app = FastAPI(title="XTTS-CPU voice clone")
model = None
REF_AUDIO = None   # 目前生效的參考音路徑（None → /tts 回 503 → companion 用 edge 通用聲）


def _resolve_ref():
    for a in (ACTIVE_REF, LEGACY_REF):
        if a and os.path.exists(a):
            return a
    return None


def _apply_ref():
    global REF_AUDIO
    REF_AUDIO = _resolve_ref()
    if REF_AUDIO:
        print(f"音色參考: {REF_AUDIO}")
    else:
        print("尚未設定音色（到 /setup 上傳一段參考音）→ /tts 暫回 503，companion 用通用聲")
    return REF_AUDIO


def _split(text):
    # XTTS 自己會斷句，但過長會出問題；先切句再貪婪合併到 ~MAX_LEN 字。
    if len(text) <= MAX_LEN:
        return [text]
    units = [s.strip() for s in re.split(r'(?<=[。！？!?\n])', text) if s.strip()]
    flat = []
    for u in units:
        while len(u) > MAX_LEN:
            flat.append(u[:MAX_LEN]); u = u[MAX_LEN:]
        if u:
            flat.append(u)
    out = []
    for u in flat:
        if out and len(out[-1]) + len(u) <= MAX_LEN:
            out[-1] += u
        else:
            out.append(u)
    return out or [text]


@app.on_event("startup")
def load():
    global model
    from TTS.api import TTS
    print(f"載入 {MODEL_ID}（CPU；首次會下載約 1.8GB，請耐心）…")
    model = TTS(model_name=MODEL_ID, progress_bar=False)
    model.to("cpu")
    print("XTTS-CPU 就緒（無顯卡克隆；慢但完全本機）")
    _apply_ref()
    wm.load()   # 浮水印（CPU）


@app.get("/health")
def health():
    return {"status": "ok",
            "ref_loaded": model is not None and REF_AUDIO is not None,
            "model_loaded": model is not None,
            "ref_set": REF_AUDIO is not None,
            "ref_path": REF_AUDIO or "",
            "backend": "xtts-cpu",
            "watermark": wm.ok(),
            "sample_rate": wm.WM_SR if wm.ok() else 24000, "model": MODEL_ID}


@app.post("/reload-ref")
def reload_ref():
    a = _apply_ref()
    return {"ok": True, "ref_set": a is not None, "ref_path": a or ""}


class TTSReq(BaseModel):
    text: str
    speed: float = 1.0
    spk_id: str = ""
    language: str = ""        # Qwen 格式（"English"）；本服務不用
    language_code: str = ""   # XTTS 格式（"en"／"zh-cn"）；空字串＝用服務端預設


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
        for piece in _split(text):
            wav = model.tts(text=piece, speaker_wav=REF_AUDIO, language=(req.language_code or LANG))
            chunks.append(np.asarray(wav, dtype=np.float32))
    except Exception as e:
        raise HTTPException(500, str(e))
    audio = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
    audio, out_sr = wm.apply(audio, 24000)   # XTTS 輸出 24k → 打浮水印（未就緒則原樣）
    buf = io.BytesIO()
    sf.write(buf, audio, out_sr, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return Response(content=buf.read(), media_type="audio/wav")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")
