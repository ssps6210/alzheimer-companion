# 阿茲海默陪伴者 · 無顯卡 CPU 版一鍵安裝（純 Windows，不需要 WSL / NVIDIA 顯卡）
# 家人的聲音仍是克隆的、完全本機；代價是合成較慢。
# 用法：在專案資料夾按右鍵「用 PowerShell 執行」，或：
#   powershell -ExecutionPolicy Bypass -File install_cpu.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host ''
Write-Host '==========================================' -ForegroundColor Cyan
Write-Host '  阿茲海默陪伴者 · 無顯卡 CPU 版 安裝' -ForegroundColor Cyan
Write-Host '==========================================' -ForegroundColor Cyan
Write-Host '  不需要顯卡、不需要 WSL。家人的聲音仍是克隆的，但合成較慢。' -ForegroundColor DarkGray
Write-Host '  卡住？先讀 docs\安裝指南.md' -ForegroundColor DarkGray
Write-Host ''

# --- 0) 前置檢查 ---
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host '✗ 缺少 python' -ForegroundColor Red
    Write-Host '   → 到 python.org 裝 Python 3.10+，安裝時勾「Add python.exe to PATH」，裝完重開視窗' -ForegroundColor Yellow
    exit 1
}
$pyver = (python -c "import sys;print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null)
if ($pyver -and ([version]$pyver -lt [version]'3.10')) {
    Write-Host "⚠ 你的 Python 是 $pyver，建議 3.10 以上" -ForegroundColor Yellow
}

# --- 1) Windows venv + 依賴（含 CPU 版語音克隆，會下載約 2GB）---
Write-Host '[1/2] 建立 venv + 裝依賴（torch CPU + coqui-tts，會下載約 2GB，請耐心）...' -ForegroundColor Yellow
if (-not (Test-Path venv)) { python -m venv venv }
.\venv\Scripts\python.exe -m pip install --upgrade pip -q
.\venv\Scripts\pip.exe install -q -r requirements-cpu.txt
Write-Host '  ✓ 依賴完成' -ForegroundColor Green

# --- 2) 設定檔（用 CPU 範本）---
Write-Host '[2/2] 設定檔...' -ForegroundColor Yellow
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host '  已建立 .env' -ForegroundColor Cyan }
if (-not (Test-Path conf.yaml)) { Copy-Item conf.cpu.example.yaml conf.yaml; Write-Host '  已建立 conf.yaml（CPU 版）' -ForegroundColor Cyan }
else { Write-Host '  conf.yaml 已存在，未覆蓋（要用 CPU 版可手動 copy conf.cpu.example.yaml conf.yaml）' -ForegroundColor DarkGray }

Write-Host ''
Write-Host '✅ 安裝完成！接下來兩步：' -ForegroundColor Green
Write-Host '   1) 打開 .env 填入你的 NVIDIA_API_KEY（到 https://build.nvidia.com 免費申請）' -ForegroundColor White
Write-Host '   2) 雙擊「一鍵啟動_CPU版.bat」' -ForegroundColor White
Write-Host ''
Write-Host '  首次啟動會下載 XTTS 語音模型（約 1.8GB），請耐心。' -ForegroundColor DarkGray
Write-Host ''
Read-Host '按 Enter 關閉'
