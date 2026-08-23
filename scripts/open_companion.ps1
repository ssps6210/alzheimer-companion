# Open the local companion (爺爺/阿公 frontend). Starts services if needed, then opens the browser.
$ErrorActionPreference = 'SilentlyContinue'
$py   = 'D:\elder-companion\venv\Scripts\python.exe'
$root = 'D:\elder-companion'
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
    Start-Process wsl -ArgumentList '-d','Ubuntu-22.04','-u','root','--','bash','/mnt/d/elder-companion/scripts/_start_qwen.sh' -WindowStyle Hidden
}

Start-Process $url
