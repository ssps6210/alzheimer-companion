import torch, soundfile as sf, os, time
from qwen_tts import Qwen3TTSModel

REF = "/mnt/d/elder-companion/father_reference.wav"
ref_text = open("/mnt/d/elder-companion/father_reference.txt", encoding="utf-8").read().strip()

print("載入 Qwen3-TTS 1.7B ...", flush=True)
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                                      device_map="cuda:0", dtype=torch.bfloat16,
                                      attn_implementation="sdpa")

texts = {
 "05s": "阿公，今天天氣真好，出去走走好嗎？",
 "10s": "阿公，今天天氣真好，太陽暖暖的。要不要等一下我們一起去公園走走，曬曬太陽呢？",
 "20s": "阿公，今天天氣真好，太陽暖暖的，風也很輕。要不要等一下我們一起去公園走走，看看花、曬曬太陽？走累了就找張長椅坐下來，慢慢聊天，不用著急。",
 "30s": "阿公，今天天氣真好，太陽暖暖的，風也很輕。要不要等一下我們一起去公園走走，看看花、曬曬太陽？走累了就找張長椅坐下來，慢慢聊天，不用著急。你開開心心，我就開心，我會一直陪著你。記得按時吃藥、多喝水，天氣涼了多穿件衣服喔。",
}
for name, txt in texts.items():
    t = time.time()
    wavs, sr = model.generate_voice_clone(text=txt, language="Chinese",
                                          ref_audio=REF, ref_text=ref_text)
    out = f"/tmp/qwen_len_{name}.wav"
    sf.write(out, wavs[0], sr)
    dur = len(wavs[0]) / sr
    os.system(f"cp '{out}' /mnt/c/Users/admin/Desktop/qwen_len_{name}.wav")
    print(f"{name}: 音長 {dur:.1f}s，合成耗時 {time.time()-t:.1f}s -> 桌面 qwen_len_{name}.wav", flush=True)
print("DONE", flush=True)
