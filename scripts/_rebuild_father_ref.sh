#!/bin/bash
SRC=/mnt/d/Downloads/Father_Voice
OUT=/mnt/d/elder-companion/father_reference.wav
tmp=$(mktemp -d); list="$tmp/list.txt"; : > "$list"
# 0.35s 自然停頓（不硬切，避免接縫讓生成失穩）
ffmpeg -nostdin -y -f lavfi -i anullsrc=r=16000:cl=mono -t 0.35 "$tmp/sil.wav" 2>/dev/null
i=0
for f in "Morning.wav.m4a" "Walk.wav.m4a" "Goodnight.wav.m4a"; do
  o="$tmp/c$i.wav"
  # 降噪 + 響度正規化，保留自然停頓（不做 silenceremove）
  ffmpeg -nostdin -y -i "$SRC/$f" -af "highpass=f=70,afftdn=nf=-25,loudnorm=I=-20:TP=-2,aresample=16000" -ac 1 "$o" 2>/dev/null
  echo "file '$o'" >> "$list"
  [ $i -lt 2 ] && echo "file '$tmp/sil.wav'" >> "$list"
  i=$((i+1))
done
ffmpeg -nostdin -y -f concat -safe 0 -i "$list" -ac 1 -ar 16000 "$OUT" 2>/dev/null
echo -n "新 father_reference 時長(秒): "
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT"
