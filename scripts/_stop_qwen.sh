#!/bin/bash
pkill -9 -f qwen_tts_api.py 2>/dev/null
pkill -9 -f cosyvoice_api.py 2>/dev/null
echo stopped
