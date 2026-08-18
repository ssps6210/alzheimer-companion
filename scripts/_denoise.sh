#!/bin/bash
cd /mnt/c/Users/admin/Downloads || exit 1
IN=$(ls *.aac | head -n1)
echo "輸入檔: $IN"
echo "--- 音訊資訊 ---"
ffprobe -v error -show_entries format=duration:stream=sample_rate,channels,codec_name -of default=noprint_wrappers=1 "$IN"
echo "--- 產生3版 ---"
ffmpeg -y -i "$IN" -ac 1 -ar 16000 dad_raw.wav 2>/dev/null && echo "ok dad_raw.wav"
ffmpeg -y -i "$IN" -af "highpass=f=80,afftdn=nf=-25,lowpass=f=7500" -ac 1 -ar 16000 dad_clean.wav 2>/dev/null && echo "ok dad_clean.wav"
ffmpeg -y -i "$IN" -af "highpass=f=90,afftdn=nf=-20,lowpass=f=7000" -ac 1 -ar 16000 dad_strong.wav 2>/dev/null && echo "ok dad_strong.wav"
echo "--- 輸出 ---"
ls -la dad_raw.wav dad_clean.wav dad_strong.wav
