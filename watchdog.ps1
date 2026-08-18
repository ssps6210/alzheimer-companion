# 看門狗：每 30 秒檢查 companion (:8080)，掛了就自動重啟。
# 用法：powershell -ExecutionPolicy Bypass -File D:\elder-companion\watchdog.ps1
# （這支自己會把 companion 拉起來，所以直接跑這支即可；不需另外手動開 companion）
$ErrorActionPreference = "SilentlyContinue"
$venvPy = "D:\elder-companion\venv\Scripts\python.exe"
$dir    = "D:\elder-companion"
$log    = "D:\elder-companion\watchdog.log"

function Log($m) { "$(Get-Date -Format 'MM-dd HH:mm:ss')  $m" | Tee-Object -FilePath $log -Append }

function Start-Companion {
  Start-Process -FilePath $venvPy -ArgumentList "companion_web.py" -WorkingDirectory $dir `
    -RedirectStandardOutput "$dir\server.out.log" -RedirectStandardError "$dir\server.err.log" `
    -WindowStyle Hidden
}

Log "看門狗啟動：每 30 秒檢查 companion :8080"
while ($true) {
  $ok = $false
  try { $r = Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 8; if ($r.whisper.loaded) { $ok = $true } } catch {}

  if (-not $ok) {
    Log "companion 無回應 → 重啟"
    Get-NetTCPConnection -LocalPort 8080 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
    # 還在載入 Whisper（尚未聽 :8080）的 companion 也要先收掉，避免起出第二支搶 VRAM
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
      Where-Object { $_.CommandLine -like '*companion_web.py*' } |
      ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 2
    Start-Companion
    Log "已重啟 companion，等 Whisper 載入(90s)"
    Start-Sleep -Seconds 90    # 避免 Whisper 還在載就被判死、連環重啟
  }
  else {
    # 順帶記錄 TTS 服務(:50000)狀態（不自動重啟 WSL，只提醒）
    $tts = $false
    try { $h = Invoke-RestMethod -Uri "http://localhost:50000/health" -TimeoutSec 4; if ($h.ref_loaded) { $tts = $true } } catch {}
    if (-not $tts) { Log "提醒：TTS(:50000) 未就緒，開放對話走 edge-tts(companion 正常)" }
  }
  Start-Sleep -Seconds 30
}
