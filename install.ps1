# 阿茲海默陪伴者 · 一鍵安裝（Windows + WSL2）
# 用法：在專案資料夾按右鍵「用 PowerShell 執行」，或：
#   powershell -ExecutionPolicy Bypass -File install.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host ''
Write-Host '======================================' -ForegroundColor Cyan
Write-Host '  阿茲海默陪伴者 · 安裝' -ForegroundColor Cyan
Write-Host '======================================' -ForegroundColor Cyan
Write-Host '  卡住？先讀 docs\安裝指南.md（手把手 + 常見問題）' -ForegroundColor DarkGray
Write-Host ''

# --- 0) 前置檢查（缺什麼就明確告訴你去裝哪個） ---
function Need($cmd, $hint) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "✗ 缺少 $cmd" -ForegroundColor Red
        Write-Host "   → $hint" -ForegroundColor Yellow
        Write-Host '   （逐步教學見 docs\安裝指南.md）' -ForegroundColor DarkGray
        exit 1
    }
}
Need python '到 python.org 裝 Python 3.10+，安裝時「勾 Add python.exe to PATH」，裝完重開這個視窗'
Need wsl '用「系統管理員」PowerShell 跑一次：wsl --install -d Ubuntu-22.04，重開機後再回來'
$pyver = (python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null)
if ($pyver -and ([version]$pyver -lt [version]'3.10')) {
    Write-Host "⚠ 你的 Python 是 $pyver，建議 3.10 以上（可能有相容問題）" -ForegroundColor Yellow
}

$gpu = (wsl -d Ubuntu-22.04 -u root -- bash -lc "nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null")
if ($gpu) { Write-Host "✓ GPU：$gpu" -ForegroundColor Green }
else { Write-Host '⚠ WSL 內看不到 NVIDIA GPU —— 請更新顯卡驅動（支援 WSL 的版本）。沒有 GPU 仍可裝，但語音會很慢。' -ForegroundColor Yellow }

# --- 1) Windows 端 ---
Write-Host '[1/4] Windows：建立 venv + 裝依賴...' -ForegroundColor Yellow
if (-not (Test-Path venv)) { python -m venv venv }
.\venv\Scripts\python.exe -m pip install --upgrade pip -q
.\venv\Scripts\pip.exe install -q -r requirements.txt
Write-Host '  ✓ Windows 依賴完成' -ForegroundColor Green

# --- 2) WSL 端（Qwen 語音克隆，會下載數 GB） ---
Write-Host '[2/4] WSL：安裝語音克隆環境（torch + qwen-tts + flash-attn，會下載數 GB，請耐心）...' -ForegroundColor Yellow
$drive = $root.Substring(0,1).ToLower()
$wslPath = "/mnt/$drive" + ($root.Substring(2) -replace '\\','/')
wsl -d Ubuntu-22.04 -u root -- bash "$wslPath/scripts/_install_wsl.sh"
Write-Host '  ✓ WSL 環境完成' -ForegroundColor Green

# --- 3) 設定檔 ---
Write-Host '[3/4] 設定檔...' -ForegroundColor Yellow
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host '  已建立 .env' -ForegroundColor Cyan }
if (-not (Test-Path conf.yaml)) { Copy-Item conf.example.yaml conf.yaml; Write-Host '  已建立 conf.yaml' -ForegroundColor Cyan }

# --- 4) 本機大腦（可選：沒裝 Ollama 就跳過，改用雲端備援） ---
Write-Host '[4/4] 本機大腦...' -ForegroundColor Yellow
$ollamaModel = 'qwen3:4b'
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    # 8GB 顯卡上，語音辨識＋聲音克隆已經吃掉大部分顯存。
    # 保留一點顯存給它們，Ollama 才會主動把大腦剩下的部分「溢出」到記憶體，
    # 而不是硬搶同一張卡把整個系統撐爆。只在使用者還沒自己設過時才動它。
    if (-not [Environment]::GetEnvironmentVariable('OLLAMA_GPU_OVERHEAD', 'User')) {
        [Environment]::SetEnvironmentVariable('OLLAMA_GPU_OVERHEAD', '2147483648', 'User')  # 2GB
        Write-Host '  ✓ 已保留 2GB 顯存給語音辨識／聲音克隆（下次啟動 Ollama 生效）' -ForegroundColor Green
        Write-Host '    要調整：改「使用者環境變數」OLLAMA_GPU_OVERHEAD（單位是位元組）' -ForegroundColor DarkGray
    }
    # KV cache 用 q8_0 量化：記憶體砍半、品質損失可忽略（需要 flash attention，
    # 支援的顯卡預設就有開）。同樣只在使用者沒自己設過時才動。
    if (-not [Environment]::GetEnvironmentVariable('OLLAMA_KV_CACHE_TYPE', 'User')) {
        [Environment]::SetEnvironmentVariable('OLLAMA_KV_CACHE_TYPE', 'q8_0', 'User')
        Write-Host '  ✓ KV cache 改用 q8_0 量化，省下的顯存讓三個服務更好相處' -ForegroundColor Green
    }
    Write-Host "  下載 $ollamaModel（幾 GB，跟語音模型一起跑，請耐心）..." -ForegroundColor Yellow
    ollama pull $ollamaModel
    Write-Host '  ✓ 本機大腦就緒——不需要任何金鑰，對話文字不會離開這台電腦' -ForegroundColor Green
} else {
    Write-Host '  未偵測到 Ollama，略過（不影響安裝）' -ForegroundColor DarkGray
    Write-Host '    想要「不用金鑰、對話文字不出門」：到 https://ollama.com 裝好後' -ForegroundColor DarkGray
    Write-Host "    重跑這支腳本，或自己跑一次：ollama pull $ollamaModel" -ForegroundColor DarkGray
    Write-Host '    暫時沒裝也能用：打開 .env 填 NVIDIA_API_KEY（build.nvidia.com 免費申請）當雲端備援' -ForegroundColor DarkGray
}

Write-Host ''
Write-Host '✅ 安裝完成！雙擊「一鍵啟動.bat」即可開始。' -ForegroundColor Green
Write-Host ''
Read-Host '按 Enter 關閉'
