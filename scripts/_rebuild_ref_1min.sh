#!/bin/bash
SRC=/mnt/d/elder-companion/recordings/Father_Voice/Father_1min_long.m4a
REF=/mnt/d/elder-companion/father_reference.wav
cd /root/seed-vc || exit 1
PY=/root/rvc_env/bin/python
EDGE=/root/rvc_env/bin/edge-tts

echo "=== 1. 用 1 分鐘連續長音重建參考音（去噪+正規化+去頭靜音，取前 30s） ==="
ffmpeg -nostdin -y -i "$SRC" \
  -af "highpass=f=70,afftdn=nf=-25,loudnorm=I=-20:TP=-2,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.1" \
  -ac 1 -ar 16000 -t 30 "$REF" 2>/dev/null
echo "新 father_reference 時長: $(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$REF")s"

echo "=== 2. edge-tts 來源（放慢 -15%） ==="
"$EDGE" --voice zh-TW-YunJheNeural --rate=-15% --text "阿公，今天天氣真好，有沒有想出去走走？我等一下回去看你。" --write-media /tmp/src.mp3 2>&1 | tail -1
ffmpeg -nostdin -y -i /tmp/src.mp3 -ar 22050 -ac 1 /tmp/src.wav 2>/dev/null

echo "=== 3. seed-vc(v1, 快) 換成爸爸聲 ==="
"$PY" inference.py --source /tmp/src.wav --target "$REF" --output /tmp/vc_new \
  --diffusion-steps 30 --inference-cfg-rate 0.7 --fp16 True 2>&1 | tail -6

out=$(ls /tmp/vc_new/*.wav 2>/dev/null | head -1)
if [ -n "$out" ]; then
  cp "$out" /mnt/c/Users/admin/Desktop/seedvc_father_NEW.wav
  echo "✅ 完成 → 桌面 seedvc_father_NEW.wav"
else
  echo "⚠ 沒輸出，看上面錯誤"
fi
