#!/bin/bash
SRC="/mnt/d/Downloads/Father_Voice"
DST="/mnt/d/elder-companion/phrases"
mkdir -p "$DST"
# 溫和降噪（這些是直接播給阿公聽，寧可少清一點、保留自然人聲）
AF="highpass=f=80,afftdn=nf=-25,lowpass=f=9000"
map="
Bored.wav.m4a|bored.wav
Bye.wav.m4a|bye.wav
Discomfort.wav.m4a|discomfort.wav
Go home.wav.m4a|gohome.wav
Goodnight.wav.m4a|goodnight.wav
Hello.wav.m4a|hello.wav
Meal.wav.m4a|meal.wav
Medicine.wav.m4a|medicine.wav
Miss family.wav.m4a|miss_family.wav
Morning.wav.m4a|morning.wav
Sad.wav.m4a|sad.wav
Scared.wav.m4a|scared.wav
Thanks.wav.m4a|thanks.wav
Toilet.wav.m4a|toilet.wav
Walk.wav.m4a|walk.wav
Water.wav.m4a|water.wav
Where.wav.m4a|where.wav
Who.wav.m4a|who.wav
"
ok=0; fail=0
while IFS='|' read -r s d; do
  [ -z "$s" ] && continue
  if [ -f "$SRC/$s" ]; then
    if ffmpeg -nostdin -y -i "$SRC/$s" -af "$AF" -ac 1 "$DST/$d" 2>/dev/null; then
      echo "ok   $d"; ok=$((ok+1))
    else
      echo "FAIL $d"; fail=$((fail+1))
    fi
  else
    echo "MISSING $s"; fail=$((fail+1))
  fi
done <<< "$map"
echo "---- 完成：$ok 成功 / $fail 失敗 ----"
echo "phrases 目錄現有 wav：$(ls "$DST"/*.wav 2>/dev/null | wc -l)"
