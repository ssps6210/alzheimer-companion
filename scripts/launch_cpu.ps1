$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
try { $Host.UI.RawUI.WindowTitle = '爺爺陪伴系統 · 啟動（CPU 版）' } catch {}
$root = Split-Path -Parent $PSScriptRoot   # 專案根目錄（scripts 的上一層）；放哪都能跑
$py   = Join-Path $root 'venv\Scripts\python.exe'

Write-Host ''
Write-Host '========================================' -ForegroundColor Cyan
Write-Host '   爺爺陪伴系統 · 一鍵啟動（無顯卡 CPU 版）' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''

# 1) companion（前端 + setup，:8080）—— 用 CommandLine 判斷，避免 Whisper 載入中被誤判沒跑
$compUp = (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) -or
          (Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
             Where-Object { $_.CommandLine -like '*companion_web.py*' })
if ($compUp) {
    Write-Host '[1/3] companion 已在執行 (:8080)' -ForegroundColor DarkGray
} else {
    Write-Host '[1/3] 啟動 companion（前端 + setup）...' -ForegroundColor Yellow
    Start-Process -FilePath $py -ArgumentList 'companion_web.py' -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput "$root\server.out.log" -RedirectStandardError "$root\server.err.log"
}

# 2) 等語音辨識載完（CPU 版首次載 small 模型約 20-40 秒）
Write-Host '[2/3] 等待語音辨識載入...' -ForegroundColor Yellow
$h = $null
for ($i = 0; $i -lt 60; $i++) {
    try { $h = Invoke-RestMethod 'http://localhost:8080/health' -TimeoutSec 5 } catch {}
    if ($h -and $h.whisper.loaded) { break }
    Start-Sleep -Seconds 2
}

# 3) 啟動 家人的聲音（XTTS-CPU，Windows :50000）—— 不需要 WSL
$ttsUp = (Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
             Where-Object { $_.CommandLine -like '*xtts_cpu_api.py*' })
if ($ttsUp) {
    Write-Host '[3/3] 家人的聲音（XTTS-CPU）已在執行 (:50000)' -ForegroundColor DarkGray
} else {
    Write-Host '[3/3] 啟動 家人的聲音（XTTS-CPU；首次會下載約 1.8GB 模型）...' -ForegroundColor Yellow
    Start-Process -FilePath $py -ArgumentList 'xtts_cpu_api.py' -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput "$root\tts.out.log" -RedirectStandardError "$root\tts.err.log"
}
# 等 XTTS 就緒（首次下載模型可能要幾分鐘，這裡最多等 ~2 分鐘，之後畫面自己會更新）
for ($i = 0; $i -lt 60; $i++) {
    try { if ((Invoke-RestMethod 'http://localhost:50000/health' -TimeoutSec 3).ref_loaded) { break } } catch {}
    Start-Sleep -Seconds 2
}
try { $h = Invoke-RestMethod 'http://localhost:8080/health' -TimeoutSec 5 } catch {}

Write-Host ''
if ($h -and $h.whisper.loaded) {
    $brain = if ($h.llm.ok) { '就緒' } else { '未連線(檢查網路/金鑰)' }
    $voice = if ($h.cosyvoice.ok) { '就緒' } else { '載入中(先用備援聲)' }
    Write-Host '  系統就緒！' -ForegroundColor Green
    Write-Host "    語音辨識：就緒     大腦：$brain     家人的聲音：$voice" -ForegroundColor White
    Write-Host ''
    Start-Process 'http://localhost:8080/'
    Start-Process 'http://localhost:8080/setup'
    Write-Host '  已為你開啟兩個分頁：' -ForegroundColor Cyan
    Write-Host '    前端（爺爺用）        http://localhost:8080/' -ForegroundColor White
    Write-Host '    家人管理台 setup      http://localhost:8080/setup' -ForegroundColor White
} else {
    Write-Host '  逾時：companion 沒起來。請看 server.err.log' -ForegroundColor Red
}

Write-Host ''
Write-Host '  提示：CPU 版語音合成較慢（一句話數秒~十幾秒），常用話走固定句會秒回。' -ForegroundColor DarkGray
Write-Host '        關掉這個視窗，服務仍在背景執行；要停止請雙擊「一鍵停止」。' -ForegroundColor DarkGray
Write-Host ''
Read-Host '  按 Enter 關閉此視窗'
