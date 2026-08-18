#!/bin/bash
pkill -9 -f qwen_tts_api.py 2>/dev/null
pkill -9 -f cosyvoice_api.py 2>/dev/null
sleep 1
exec /root/rvc_env/bin/python /mnt/d/elder-companion/qwen_tts_api.py > /root/qwen.log 2>&1
