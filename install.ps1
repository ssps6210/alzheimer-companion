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

# --- 0) 前置檢查 ---
function Need($cmd, $hint) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "✗ 缺少 $cmd —— $hint" -ForegroundColor Red; exit 1
    }
}
Need python 'https://www.python.org 裝 Python 3.10+（安裝時勾 Add to PATH）'
Need wsl '系統管理員 PowerShell 跑：wsl --install -d Ubuntu-22.04，重開機後再來'

$gpu = (wsl -d Ubuntu-22.04 -u root -- bash -lc "nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null")
if ($gpu) { Write-Host "✓ GPU：$gpu" -ForegroundColor Green }
else { Write-Host '⚠ WSL 內看不到 NVIDIA GPU —— 請更新顯卡驅動（支援 WSL 的版本）。沒有 GPU 仍可裝，但語音會很慢。' -ForegroundColor Yellow }

# --- 1) Windows 端 ---
Write-Host '[1/3] Windows：建立 venv + 裝依賴...' -ForegroundColor Yellow
if (-not (Test-Path venv)) { python -m venv venv }
.\venv\Scripts\python.exe -m pip install --upgrade pip -q
.\venv\Scripts\pip.exe install -q -r requirements.txt
Write-Host '  ✓ Windows 依賴完成' -ForegroundColor Green

# --- 2) WSL 端（Qwen 語音克隆，會下載數 GB） ---
Write-Host '[2/3] WSL：安裝語音克隆環境（torch + qwen-tts + flash-attn，會下載數 GB，請耐心）...' -ForegroundColor Yellow
$drive = $root.Substring(0,1).ToLower()
$wslPath = "/mnt/$drive" + ($root.Substring(2) -replace '\\','/')
wsl -d Ubuntu-22.04 -u root -- bash "$wslPath/scripts/_install_wsl.sh"
Write-Host '  ✓ WSL 環境完成' -ForegroundColor Green

# --- 3) 設定檔 ---
Write-Host '[3/3] 設定檔...' -ForegroundColor Yellow
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host '  已建立 .env' -ForegroundColor Cyan }
if (-not (Test-Path conf.yaml)) { Copy-Item conf.example.yaml conf.yaml; Write-Host '  已建立 conf.yaml' -ForegroundColor Cyan }

Write-Host ''
Write-Host '✅ 安裝完成！接下來兩步：' -ForegroundColor Green
Write-Host '   1) 打開 .env 填入你的 NVIDIA_API_KEY（到 https://build.nvidia.com 免費申請）' -ForegroundColor White
Write-Host '   2) 雙擊「一鍵啟動.bat」' -ForegroundColor White
Write-Host ''
Read-Host '按 Enter 關閉'
