# 看門狗：每 30 秒檢查 companion (:8080) 與語音克隆服務 (:50000)，掛了就自動重啟，
# 持續離線就通知家人。用法：
#   powershell -ExecutionPolicy Bypass -File <專案路徑>\watchdog.ps1
# （這支自己會把 companion 拉起來，所以直接跑這支即可；不需另外手動開 companion）
#
# 為什麼要通知家人：這套系統是給失智長輩用的，它若默默啞掉，長輩不會抱怨、
# 也不知道要找誰——只有家人收到通知才可能去處理。但通知只在「狀態轉換」時發，
# 不會每 30 秒洗一次頻，否則家人乾脆關掉通知，比不通知還糟。
$ErrorActionPreference = "SilentlyContinue"
$dir    = Split-Path -Parent $MyInvocation.MyCommand.Path   # 專案根目錄；放哪都能跑
$venvPy = Join-Path $dir 'venv\Scripts\python.exe'
$log    = Join-Path $dir 'watchdog.log'
$wslRoot = "/mnt/" + $dir.Substring(0,1).ToLower() + ($dir.Substring(2) -replace '\\','/')

$FAIL_BEFORE_NOTIFY = 3      # 連續失敗幾次才通知（3 × 30 秒 ≈ 90 秒，避開短暫抖動）

function Log($m) { "$(Get-Date -Format 'MM-dd HH:mm:ss')  $m" | Tee-Object -FilePath $log -Append }

# Telegram 由看門狗自己發：companion 掛掉時不能靠它轉發通知。
function Get-EnvValue($name) {
    $envFile = Join-Path $dir '.env'
    if (-not (Test-Path $envFile)) { return $null }
    foreach ($line in Get-Content $envFile -Encoding UTF8) {
        $t = $line.Trim()
        if ($t -and -not $t.StartsWith('#') -and $t.Contains('=')) {
            $k, $v = $t.Split('=', 2)
            if ($k.Trim() -eq $name) { return $v.Trim() }
        }
    }
    return $null
}

function Notify-Family($text) {
    $token = Get-EnvValue 'TELEGRAM_BOT_TOKEN'
    $chat  = Get-EnvValue 'TELEGRAM_CHAT_ID'
    if (-not $token -or -not $chat) { return }   # 沒設定就靜默略過
    try {
        Invoke-RestMethod -Method Post -Uri "https://api.telegram.org/bot$token/sendMessage" `
            -Body @{ chat_id = $chat; text = $text } -TimeoutSec 10 | Out-Null
        Log "已通知家人：$($text -replace "`n", ' ')"
    } catch { Log "通知家人失敗（忽略）：$_" }
}

function Start-Companion {
  Start-Process -FilePath $venvPy -ArgumentList "companion_web.py" -WorkingDirectory $dir `
    -RedirectStandardOutput "$dir\server.out.log" -RedirectStandardError "$dir\server.err.log" `
    -WindowStyle Hidden
}

function Start-Qwen {
  # 用自我定位的啟動腳本，不硬編路徑
  Start-Process wsl -ArgumentList '-d','Ubuntu-22.04','-u','root','--','bash',"$wslRoot/scripts/_start_qwen.sh" `
    -WindowStyle Hidden
}

Log "看門狗啟動：每 30 秒檢查 companion :8080 與 語音克隆 :50000（專案：$dir）"

$compFails = 0; $compNotified = $false
$ttsFails  = 0; $ttsNotified  = $false

while ($true) {
  # ── companion（核心：沒有它長輩完全無法對話）────────────────────
  $ok = $false
  try { $r = Invoke-RestMethod -Uri "http://localhost:8080/health" -TimeoutSec 8; if ($r.whisper.loaded) { $ok = $true } } catch {}

  if (-not $ok) {
    $compFails++
    Log "companion 無回應（連續 $compFails 次）→ 重啟"
    Get-NetTCPConnection -LocalPort 8080 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
    # 還在載入 Whisper（尚未聽 :8080）的 companion 也要先收掉，避免起出第二支搶 VRAM
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
      Where-Object { $_.CommandLine -like '*companion_web.py*' } |
      ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 2
    Start-Companion
    if ($compFails -ge $FAIL_BEFORE_NOTIFY -and -not $compNotified) {
      Notify-Family "🔴 陪伴系統離線`n主程式重啟多次仍未恢復，長輩目前無法對話，請盡快查看電腦。"
      $compNotified = $true
    }
    Log "已重啟 companion，等 Whisper 載入(90s)"
    Start-Sleep -Seconds 90    # 避免 Whisper 還在載就被判死、連環重啟
    continue                   # 這輪不判斷 TTS（companion 剛起來，資訊不可靠）
  }

  if ($compNotified) { Notify-Family "🟢 陪伴系統已恢復正常，長輩可以正常對話了。" }
  $compFails = 0; $compNotified = $false

  # ── 語音克隆 TTS（掉了還有 edge 通用聲可用，不算全斷，但聲音不再像家人）──
  $tts = $false
  try { $h = Invoke-RestMethod -Uri "http://localhost:50000/health" -TimeoutSec 4; if ($h.ref_loaded) { $tts = $true } } catch {}

  if (-not $tts) {
    $ttsFails++
    Log "語音克隆(:50000) 未就緒（連續 $ttsFails 次）→ 嘗試重啟（期間走 edge 通用聲，對話不中斷）"
    Start-Qwen
    if ($ttsFails -ge $FAIL_BEFORE_NOTIFY -and -not $ttsNotified) {
      Notify-Family "🟡 家人聲音暫時無法使用`n語音克隆服務重啟多次仍未恢復，長輩現在聽到的是通用聲音（對話仍正常）。方便時請查看電腦。"
      $ttsNotified = $true
    }
    Start-Sleep -Seconds 60     # 模型載入要時間，別連環重啟搶 VRAM
    continue
  }

  if ($ttsNotified) { Notify-Family "🟢 家人的聲音已恢復。" }
  $ttsFails = 0; $ttsNotified = $false

  Start-Sleep -Seconds 30
}
