#!/bin/bash
PY=/root/rvc_env/bin/python
PIP=/root/rvc_env/bin/pip
echo "=== torch 資訊 ==="
$PY -c 'import torch,sys; print("torch",torch.__version__,"| abi",torch._C._GLIBCXX_USE_CXX11_ABI,"| py",sys.version.split()[0],"| cuda",torch.version.cuda)'

BASE=https://github.com/Dao-AILab/flash-attention/releases/download
# torch2.3 / cp310 / linux / cu12x，abi False 與 True 都試（只裝 wheel，不編譯）
CANDS=(
  "v2.6.3/flash_attn-2.6.3+cu123torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl"
  "v2.6.3/flash_attn-2.6.3+cu123torch2.3cxx11abiTRUE-cp310-cp310-linux_x86_64.whl"
  "v2.5.9.post1/flash_attn-2.5.9.post1+cu122torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl"
  "v2.5.8/flash_attn-2.5.8+cu122torch2.3cxx11abiFALSE-cp310-cp310-linux_x86_64.whl"
)
for c in "${CANDS[@]}"; do
  echo "=== 試 $c ==="
  $PIP install --no-deps "$BASE/$c" 2>&1 | tail -3
  if $PY -c 'import flash_attn' 2>/dev/null; then
    $PY -c 'import flash_attn; print("✅ flash_attn", flash_attn.__version__, "裝成功")'
    echo FLASH_OK
    break
  fi
done
$PY -c 'import flash_attn; print("最終:", flash_attn.__version__)' 2>&1 | tail -1
echo FLASH_SETUP_DONE
