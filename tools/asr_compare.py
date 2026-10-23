#!/usr/bin/env python3
"""拿長輩的真實錄音比較幾個語音辨識模型，看哪個最聽得懂他。

為什麼要自己比：模型卡上的錯字率是用標準錄音量的。長輩說話慢、含糊、
台語華語混著講，實際表現可能差很多——換模型之前，用他本人的聲音量一次。

準備：一個資料夾，放 20–30 段阿公平常說話的錄音（wav / mp3 / m4a 都行），
每段旁邊放一個同檔名的 .txt，寫下他「說的意思」（用華語漢字寫，
因為 Breeze-ASR-26 會把台語寫成華語）：
    samples/asr/001.wav   samples/asr/001.txt  →  「我要吃飯了」
（samples/ 已被 .gitignore，錄音不會被提交。）

用法：
    venv\\Scripts\\python.exe tools\\asr_compare.py samples\\asr
    venv\\Scripts\\python.exe tools\\asr_compare.py samples\\asr --models medium large-v3 paulpengtw/faster-whisper-Breeze-ASR-26
    venv\\Scripts\\python.exe tools\\asr_compare.py samples\\asr --device cpu --compute-type int8

輸出每個模型的平均錯字率（CER，越低越好）、每段花的時間，以及錯最多的幾段。
"""
import argparse
import glob
import os
import re
import sys
import time

DEFAULT_MODELS = ["medium", "large-v3", "paulpengtw/faster-whisper-Breeze-ASR-26"]
AUDIO_EXTS = (".wav", ".mp3", ".m4a", ".flac", ".ogg")


def _clean(s):
    """只比字：去掉標點、空白，英文轉小寫。"""
    return re.sub(r"[\s\W_]+", "", (s or "").lower())


def cer(ref, hyp):
    """字元錯誤率 = 編輯距離 / 參考字數。"""
    r, h = _clean(ref), _clean(hyp)
    if not r:
        return 0.0 if not h else 1.0
    prev = list(range(len(h) + 1))
    for i, rc in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hc in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rc != hc))
        prev = cur
    return prev[-1] / len(r)


def load_samples(folder):
    out = []
    for p in sorted(glob.glob(os.path.join(folder, "*"))):
        if not p.lower().endswith(AUDIO_EXTS):
            continue
        txt = os.path.splitext(p)[0] + ".txt"
        if not os.path.exists(txt):
            print(f"  （略過 {os.path.basename(p)}：沒有同名的 .txt 參考文字）")
            continue
        with open(txt, encoding="utf-8") as f:
            out.append((p, f.read().strip()))
    return out


def main():
    ap = argparse.ArgumentParser(description="用長輩的真實錄音比較語音辨識模型")
    ap.add_argument("folder")
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--compute-type", default="int8_float16")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--min-silence-ms", type=int, default=1000)
    ap.add_argument("--hotwords", default="", help="以空白分隔，例如：阿明 阿嬤 鹿港")
    args = ap.parse_args()

    samples = load_samples(args.folder)
    if not samples:
        print(f"✗ {args.folder} 裡找不到「錄音＋同名 .txt」的配對")
        return 2
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio

    audio = [(p, ref, decode_audio(p, sampling_rate=16000)) for p, ref in samples]
    print(f"{len(audio)} 段錄音，比較 {len(args.models)} 個模型\n")

    results = []
    for name in args.models:
        print(f"── {name}")
        try:
            t0 = time.time()
            model = WhisperModel(name, device=args.device, compute_type=args.compute_type)
            print(f"   載入 {time.time() - t0:.0f} 秒")
        except Exception as e:
            print(f"   ✗ 載入失敗：{e}\n")
            continue
        scores, worst, spent = [], [], 0.0
        for p, ref, wav in audio:
            kw = {"hotwords": args.hotwords} if args.hotwords else {}
            t0 = time.time()
            segs, _ = model.transcribe(
                wav, beam_size=5, language=args.language, vad_filter=True,
                vad_parameters={"min_silence_duration_ms": args.min_silence_ms},
                condition_on_previous_text=False, **kw)
            hyp = "".join(s.text for s in segs).strip()
            spent += time.time() - t0
            c = cer(ref, hyp)
            scores.append(c)
            worst.append((c, os.path.basename(p), ref, hyp))
        avg = sum(scores) / len(scores)
        results.append((avg, name, spent / len(audio)))
        print(f"   平均錯字率 {avg:.1%}，每段 {spent / len(audio):.1f} 秒")
        for c, f, ref, hyp in sorted(worst, reverse=True)[:3]:
            print(f"   錯最多 {c:.0%}  {f}\n      應為：{ref}\n      聽成：{hyp}")
        print()
        del model

    if results:
        print("=" * 60)
        for avg, name, sec in sorted(results):
            print(f"{avg:7.1%}  {sec:5.1f} 秒/段  {name}")
        print("\n錯字率最低的，把它填進 conf.yaml 的 asr.model。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
