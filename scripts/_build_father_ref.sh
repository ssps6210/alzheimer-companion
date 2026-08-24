#!/bin/bash
ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
SRC=/mnt/d/Downloads/Father_Voice
OUT=$ROOT/father_reference.wav
tmp=$(mktemp -d); list="$tmp/list.txt"; : > "$list"
# 挑較長、清楚的幾句，去靜音+降噪後接起來當參考音
i=0
for f in "Morning.wav.m4a" "Medicine.wav.m4a" "Meal.wav.m4a" "Walk.wav.m4a" "Goodnight.wav.m4a" "Hello.wav.m4a" "Sad.wav.m4a" "Thanks.wav.m4a"; do
  o="$tmp/c$i.wav"
  ffmpeg -nostdin -y -i "$SRC/$f" \
    -af "highpass=f=80,afftdn=nf=-25,lowpass=f=8000,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05:stop_periods=-1:stop_threshold=-40dB:stop_silence=0.25" \
    -ac 1 -ar 16000 "$o" 2>/dev/null && echo "file '$o'" >> "$list"
  i=$((i+1))
done
ffmpeg -nostdin -y -f concat -safe 0 -i "$list" -ac 1 -ar 16000 "$OUT" 2>/dev/null
echo -n "father_reference 時長(秒): "
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT"
ls -la "$OUT"
