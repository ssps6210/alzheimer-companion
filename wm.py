"""AI 語音浮水印（AudioSeal）—— 給 Qwen(GPU) 與 XTTS(CPU) 兩個 TTS 服務共用。

放 CPU，不佔顯存。裝不了就 no-op：合成「不會壞」，但會如實回報未標記。
用途：每段克隆語音打上聽不見的標記，讓人事後能驗證「這段是 AI 合成的」。
注意這是**可驗證性**，不是防護：重新編碼有機會洗掉，也可以用 WATERMARK=0 關掉。
對外別講成「防詐騙」——它擋不住有心人，講過頭反而會折損其他真實的說明。
驗證：python tools/detect_watermark.py <音檔>
"""
import os
import numpy as np

WATERMARK = os.environ.get("WATERMARK", "1") != "0"  # 預設開
WM_SR = 16000                                         # AudioSeal 在 16kHz 運作
_model = None
_ok = False


def load():
    """載入 AudioSeal 產生器（CPU）。回傳是否就緒。裝不了→大聲提醒並繼續。"""
    global _model, _ok
    if not WATERMARK:
        print("浮水印：已由 WATERMARK=0 關閉（克隆語音不會標記）")
        return False
    try:
        from audioseal import AudioSeal
        _model = AudioSeal.load_generator("audioseal_wm_16bits")
        _model.eval()
        _ok = True
        print("浮水印：AudioSeal 就緒 ✓（每段克隆語音都標記為 AI 合成，可用 tools/detect_watermark.py 驗）")
    except Exception as e:
        _ok = False
        print(f"⚠ 浮水印未啟用：audioseal 載入失敗（{e}）→ 克隆語音「不會」被標記。安裝：pip install audioseal")
    return _ok


def ok():
    return _ok


def apply(audio, sr_in=24000):
    """在 float32 音訊上加浮水印。回 (audio, sample_rate)。
    有浮水印 → 16k 已標記；沒有就緒 → 原樣返回（絕不讓合成失敗）。"""
    if not (_ok and _model is not None):
        return audio, sr_in
    try:
        import torch, torchaudio
        wav = torch.from_numpy(np.ascontiguousarray(audio)).float()
        if sr_in != WM_SR:
            wav = torchaudio.functional.resample(wav, sr_in, WM_SR)
        x = wav.view(1, 1, -1)
        with torch.no_grad():
            mark = _model.get_watermark(x, sample_rate=WM_SR)
            y = (x + mark).squeeze().clamp(-1.0, 1.0)
        return y.cpu().numpy().astype(np.float32), WM_SR
    except Exception as e:
        print(f"⚠ 這段浮水印套用失敗，改輸出未標記音訊：{e}")
        return audio, sr_in
