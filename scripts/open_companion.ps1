# Open the local companion (爺爺/阿公 frontend). Starts services if needed, then opens the browser.
$ErrorActionPreference = 'SilentlyContinue'
$root = Split-Path -Parent $PSScriptRoot   # 專案根目錄；放哪都能跑
$py   = Join-Path $root 'venv\Scripts\python.exe'
$wslRoot = "/mnt/" + $root.Substring(0,1).ToLower() + ($root.Substring(2) -replace '\\','/')
$url  = 'http://localhost:8080/'

$running = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if (-not $running) {
    # Not running -> start companion, wait for Whisper, then start Qwen (stagger to avoid VRAM clash)
    Start-Process -FilePath $py -ArgumentList 'companion_web.py' -WorkingDirectory $root -WindowStyle Hidden `
        -RedirectStandardOutput "$root\server.out.log" -RedirectStandardError "$root\server.err.log"
    $h = $null
    for ($i = 0; $i -lt 60; $i++) {
        try { $h = Invoke-RestMethod 'http://localhost:8080/health' -TimeoutSec 5 } catch {}
        if ($h -and $h.whisper.loaded) { break }
        Start-Sleep -Seconds 2
    }
    Start-Process wsl -ArgumentList '-d','Ubuntu-22.04','-u','root','--','bash',"$wslRoot/scripts/_start_qwen.sh" -WindowStyle Hidden
}

Start-Process $url
