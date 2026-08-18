#!/bin/bash
cd /mnt/c/Users/admin/Downloads || exit 1
for f in dad_raw.wav dad_clean.wav dad_strong.wav; do
  echo "=== $f ==="
  echo -n "  整體   : "
  ffmpeg -i "$f" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume" | sed 's/.*] //' | tr '\n' '  '
  echo
  echo -n "  低頻<120Hz(哼聲帶): "
  ffmpeg -i "$f" -af "lowpass=f=120,volumedetect" -f null - 2>&1 | grep -E "mean_volume" | sed 's/.*] //' | tr '\n' '  '
  echo
done
