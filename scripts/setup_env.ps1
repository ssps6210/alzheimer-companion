$ErrorActionPreference = "Continue"
$log = "D:\elder-companion\setup_log.txt"

function Log($msg) {
    $ts = Get-Date -Format "HH:mm:ss"
    "$ts  $msg" | Tee-Object -FilePath $log -Append
}

Log "=== 開始安裝環境 ==="

# 建立 venv（Python 3.12）
Log "[1/5] 建立虛擬環境..."
py -3.12 -m venv D:\elder-companion\venv
Log "完成"

$pip = "D:\elder-companion\venv\Scripts\pip.exe"
$py  = "D:\elder-companion\venv\Scripts\python.exe"

# 升級 pip + setuptools
Log "[2/5] 升級 pip / setuptools..."
& $py -m pip install --upgrade pip setuptools wheel 2>&1 | Tee-Object -FilePath $log -Append

# 先裝 torch（CUDA 12.1）
Log "[3/5] 安裝 PyTorch CUDA..."
& $pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121 2>&1 | Tee-Object -FilePath $log -Append

# CosyVoice 依賴（排除 torch，已裝）
Log "[4/5] 安裝 CosyVoice 依賴..."
& $pip install -r D:\CosyVoice\requirements_win.txt --ignore-installed torch torchaudio 2>&1 | Tee-Object -FilePath $log -Append

# 陪伴系統依賴
Log "[4.5/5] 安裝陪伴系統依賴..."
& $pip install faster-whisper sounddevice edge-tts pygame pillow gradio-client huggingface_hub 2>&1 | Tee-Object -FilePath $log -Append

# 下載 CosyVoice3 模型
Log "[5/5] 下載 CosyVoice3 模型（約 1-2GB）..."
& $py D:\elder-companion\download_cosyvoice.py 2>&1 | Tee-Object -FilePath $log -Append

Log "=== 安裝完成 ==="
Log "啟動 venv：D:\elder-companion\venv\Scripts\Activate.ps1"
