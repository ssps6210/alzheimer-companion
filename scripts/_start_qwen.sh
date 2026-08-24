#!/bin/bash
# 由 launch.ps1 啟動；自動定位專案根（本檔在 scripts/，上一層即根），放哪都能跑
ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
pkill -9 -f qwen_tts_api.py 2>/dev/null
pkill -9 -f cosyvoice_api.py 2>/dev/null
sleep 1
exec /root/rvc_env/bin/python "$ROOT/qwen_tts_api.py" > /root/qwen.log 2>&1
