$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
try { $Host.UI.RawUI.WindowTitle = '阿公陪伴系統 · 停止' } catch {}

Write-Host ''
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host '   阿公陪伴系統 · 停止' -ForegroundColor Cyan
Write-Host '=====================================' -ForegroundColor Cyan
Write-Host ''

# companion :8080（前端 + setup）
$c = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($c) {
    $c.OwningProcess | Select-Object -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
    Write-Host '  已停止 companion（前端 + setup）' -ForegroundColor Yellow
} else {
    Write-Host '  companion 原本就沒在跑' -ForegroundColor DarkGray
}
# 還在載入 Whisper、尚未聽 :8080 的 companion 也要停（不然按了停止，它稍後又自己活過來）
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like '*companion_web.py*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

# ngrok 通道（若有）
$n = Get-Process ngrok -ErrorAction SilentlyContinue
if ($n) { $n | Stop-Process -Force -ErrorAction SilentlyContinue; Write-Host '  已停止 ngrok 通道' -ForegroundColor Yellow }

# 爸爸的聲音 Qwen TTS（WSL）— pkill 放獨立腳本，避免殺到自己那條 bash
Start-Process wsl -ArgumentList '-d','Ubuntu-22.04','-u','root','--','bash','/mnt/d/elder-companion/scripts/_stop_qwen.sh' -WindowStyle Hidden -Wait
Write-Host '  已停止 爸爸的聲音（Qwen TTS）' -ForegroundColor Yellow

Write-Host ''
Write-Host '  全部停止完成。' -ForegroundColor Green
Write-Host ''
Read-Host '  按 Enter 關閉此視窗'
