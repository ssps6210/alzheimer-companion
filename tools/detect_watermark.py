#!/usr/bin/env python3
"""偵測一段音檔是否由本專案的克隆聲音生成（AudioSeal 浮水印）。

本專案產生的每一段克隆語音都會打上聽不見的 AI 浮水印。用這支工具可以驗證：

    python tools/detect_watermark.py 某段錄音.wav

輸出 0~1 的機率；> 0.5 代表偵測到本專案的浮水印（即：AI 合成、非真人）。
用途：向家人／機構證明「這確實是合成聲、不是本人親口說的」，降低被冒用詐騙的空間。

需要（在 WSL 的 rvc_env 內）：pip install audioseal soundfile torch torchaudio
"""
import sys


def detect(path):
    import numpy as np, soundfile as sf, torch, torchaudio
    from audioseal import AudioSeal

    audio, sr = sf.read(path, dtype="float32")
    if audio.ndim > 1:                       # 立體聲 → 取單聲道
        audio = audio.mean(axis=1)
    wav = torch.from_numpy(np.ascontiguousarray(audio)).float()
    if sr != 16000:                          # AudioSeal 在 16kHz 運作
        wav = torchaudio.functional.resample(wav, sr, 16000)

    detector = AudioSeal.load_detector("audioseal_detector_16bits")
    with torch.no_grad():
        result, _message = detector.detect_watermark(wav.view(1, 1, -1), sample_rate=16000)
    prob = float(result if not hasattr(result, "mean") else result.mean())
    return prob


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python tools/detect_watermark.py <音檔.wav>")
        sys.exit(1)
    try:
        p = detect(sys.argv[1])
    except Exception as e:
        print(f"偵測失敗：{e}\n（請確認已安裝 audioseal：pip install audioseal）")
        sys.exit(2)
    verdict = "AI 合成 —— 帶本專案浮水印 ✓" if p > 0.5 else "未偵測到本專案浮水印"
    print(f"浮水印機率：{p:.3f}　→　{verdict}")
