#!/bin/bash
# WSL2 (Ubuntu) 安裝：Qwen3-TTS 語音克隆環境 → /root/rvc_env
# 由 install.ps1 自動呼叫；也可手動：bash /mnt/<碟>/elder-companion/scripts/_install_wsl.sh
set -e
echo "== 語音克隆環境安裝（WSL）=="

echo "-- 系統套件（python venv / ffmpeg）--"
apt-get update -qq >/dev/null 2>&1 || true
apt-get install -y -qq python3.10-venv python3-pip ffmpeg >/dev/null 2>&1 || true

echo "-- 建立 venv /root/rvc_env --"
[ -d /root/rvc_env ] || python3 -m venv /root/rvc_env
PIP=/root/rvc_env/bin/pip
$PIP install --upgrade pip -q

echo "-- PyTorch (CUDA 12.1)：約 2.5GB，請耐心 --"
$PIP install -q torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121

echo "-- Qwen3-TTS + 依賴 --"
$PIP install -q qwen-tts soundfile fastapi uvicorn "numpy==1.26.4" transformers accelerate einops

echo "-- flash-attn（可選，加速；裝不起來會自動退回 sdpa，不影響運作）--"
$PIP install -q "https://github.com/Dao-AILab/flash-attention/releases/download/v2.6.3/flash_attn-2.6.3+cu123torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl" \
  || echo "  flash-attn 跳過（非必需，模型會用 sdpa/eager）"

echo "-- audioseal（AI 語音浮水印，防冒用；裝不起來會自動略過，克隆聲仍可用但不標記）--"
$PIP install -q audioseal || echo "  audioseal 跳過 → 克隆語音不會打浮水印（可事後 pip install audioseal 補上）"

echo "== 完成，驗證 --"
/root/rvc_env/bin/python -c "import torch; print('torch', torch.__version__, '| CUDA 可用:', torch.cuda.is_available())"
echo "== WSL 環境就緒 =="
