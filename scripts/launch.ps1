$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
try { $Host.UI.RawUI.WindowTitle = '爺爺陪伴系統 · 啟動' } catch {}
$root = Split-Path -Parent $PSScriptRoot   # 專案根目錄（scripts 的上一層）；放哪都能跑
$py   = Join-Path $root 'venv\Scripts\python.exe'
$wslRoot = "/mnt/" + $root.Substring(0,1).ToLower() + ($root.Substring(2) -replace '\\','/')

Write-Host ''
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host '   爺爺陪伴系統 · 一鍵啟動' -ForegroundColor Cyan
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host ''

# 1) companion（前端 + setup，:8080）
# 注意：載入 Whisper 的 30-60 秒內還沒聽 :8080，只看 port 會誤判沒在跑 → 起第二支搶 VRAM 撞掛，
#       所以同時用 CommandLine 找還在載入中的 companion 行程。
$compUp = (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) -or
          (Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
             Where-Object { $_.CommandLine -like '*companion_web.py*' })
if ($compUp) {
    Write-Host '[1/3] companion 已在執行 (:8080)' -ForegroundColor DarkGray
} else {
    Write-Host '[1/3] 啟動 companion（前端 + setup）...' -ForegroundColor Yellow
    Start-Process -FilePath $py -ArgumentList 'companion_web.py' -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput "$root\server.out.log" -RedirectStandardError "$root\server.err.log"
}

# 2) 先等語音辨識載完，再起 Qwen —— 兩個模型同時載會搶爆 8GB VRAM 撞掛（錯開 GPU 尖峰）
Write-Host '[2/3] 等待語音辨識載入（首次約 30-60 秒）...' -ForegroundColor Yellow
$h = $null
for ($i = 0; $i -lt 60; $i++) {
    try { $h = Invoke-RestMethod 'http://localhost:8080/health' -TimeoutSec 5 } catch {}
    if ($h -and $h.whisper.loaded) { break }
    Start-Sleep -Seconds 2
}

# 3) 語音辨識就緒後，才起 爸爸的聲音（Qwen TTS，WSL :50000）
Write-Host '[3/3] 啟動 爸爸的聲音（Qwen TTS）...' -ForegroundColor Yellow
Start-Process wsl -ArgumentList '-d','Ubuntu-22.04','-u','root','--','bash',"$wslRoot/scripts/_start_qwen.sh" -WindowStyle Hidden
# 等 Qwen 就緒（最多 ~60 秒），好在畫面顯示正確狀態
for ($i = 0; $i -lt 30; $i++) {
    try { if ((Invoke-RestMethod 'http://localhost:50000/health' -TimeoutSec 3).ref_loaded) { break } } catch {}
    Start-Sleep -Seconds 2
}
try { $h = Invoke-RestMethod 'http://localhost:8080/health' -TimeoutSec 5 } catch {}

Write-Host ''
if ($h -and $h.whisper.loaded) {
    $brain = if ($h.llm.ok) { '就緒' } else { '未連線(檢查網路/金鑰)' }
    $voice = if ($h.cosyvoice.ok) { '就緒' } else { '載入中(先用備援聲)' }
    Write-Host '  系統就緒！' -ForegroundColor Green
    Write-Host "    語音辨識：就緒     大腦：$brain     爸爸的聲音：$voice" -ForegroundColor White
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
Write-Host '  提示：關掉這個視窗，服務仍在背景執行。' -ForegroundColor DarkGray
Write-Host '        要完全停止，請雙擊「一鍵停止」。' -ForegroundColor DarkGray
Write-Host ''
Read-Host '  按 Enter 關閉此視窗'
