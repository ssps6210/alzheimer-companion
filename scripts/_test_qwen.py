import torch, gc, soundfile as sf
REF = "/mnt/d/elder-companion/father_reference.wav"
TXT = "爺爺，今天天氣真好，有沒有想出去走走？我等一下回去看你。"

# 1. 轉逐字稿當 ref_text
from transformers import pipeline
print("=== 轉逐字稿 ===", flush=True)
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small",
               device=0, torch_dtype=torch.float16)
ref_text = asr(REF, generate_kwargs={"language": "zh", "task": "transcribe"})["text"].strip()
print("REF_TEXT:", ref_text, flush=True)
del asr; gc.collect(); torch.cuda.empty_cache()

# 2. Qwen3-TTS 零樣本克隆
print("=== 載入 Qwen3-TTS 1.7B（首次下載~4.5GB）===", flush=True)
from qwen_tts import Qwen3TTSModel
try:
    model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                                          device_map="cuda:0", dtype=torch.bfloat16,
                                          attn_implementation="sdpa")
except Exception as e:
    print("sdpa 失敗，改 eager:", e, flush=True)
    model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                                          device_map="cuda:0", dtype=torch.bfloat16,
                                          attn_implementation="eager")
print("=== 克隆合成 ===", flush=True)
wavs, sr = model.generate_voice_clone(text=TXT, language="Chinese",
                                      ref_audio=REF, ref_text=ref_text)
sf.write("/tmp/qwen_father.wav", wavs[0], sr)
print("SAVED sr=", sr, flush=True)
