# 爺爺的小助手 · Android App（WebView 外殼）

把 companion 的長輩畫面包成一個 Android App：**一點就開、全螢幕、麥克風原生授權**（解決瀏覽器在 http 下不給錄音的坑）、可鎖成單一畫面給長輩用。

> ⚠️ 這只是「客戶端」—— AI 仍跑在你的 PC（companion + 語音服務）。平板要連得到那台 PC：同一 WiFi 用區網 IP，或用 https 通道連遠端。
> **伺服器網址不寫死**：App 首次開啟會請你輸入（記在手機裡），所以同一個 APK 每個家庭都能用；連不上時會自動再跳出來讓你重填。

## 最簡單：直接下載 APK（不用 Android Studio）
1. 到 **[Releases](https://github.com/ssps6210/alzheimer-companion/releases)** 下載 `elder-companion.apk`。
2. 手機開「允許安裝未知來源／此來源」→ 安裝。
3. 開啟 → 首次會請你輸入電腦上 companion 的網址（「一鍵啟動」視窗 / 家人管理台會顯示）→ 完成。

> APK 由 GitHub Actions 在雲端自動 build（見 [`.github/workflows/android.yml`](../.github/workflows/android.yml)）。維護者只要 push 一個 `v*` 標籤（如 `v1.0`）就會自動出新版並發到 Releases。

## 想自己 build？用 Android Studio
1. Android Studio →「**Open**」→ 選這個 `android` 資料夾 → 等 Gradle 同步（第一次會下載，請耐心）。
2. 接上平板（開發者模式 + USB 偵錯）按 **Run ▶**；或 **Build → Build APK(s)**，把產生的 `app-debug.apk` 傳到平板安裝。
3. 平板首次開啟會問麥克風權限 → **允許**，並輸入伺服器網址。

> 不用改任何程式碼——**網址是開 App 後輸入的**，不再寫死在 `MainActivity.java`。
> Gradle 同步若報版本問題，讓 Android Studio 自動升級 AGP / Gradle 即可。

## 給長輩用（可選：鎖成單一 App / Kiosk）
- Android 內建「**螢幕固定／App 固定**」（設定 → 安全性）可把平板鎖在這個 App，長輩退不出去、只看得到爺爺畫面。
- 桌面其他圖示都拿掉，只留這一個。

## 排錯
- **白畫面／連不到**：會自動跳出來讓你重填網址。確認 PC 的 companion 有在跑、平板和 PC **同一 WiFi**、網址的 IP 對。
- **按按鈕不錄音**：到「設定 → 應用程式 → 爺爺的小助手 → 權限」確認麥克風已允許。
- **想換伺服器網址**：讓它連一次失敗（或清除 App 資料）就會再跳出輸入框。
- **想退出 App**：預設返回鍵不會退（防長輩誤退）；用「最近工作」或 Home 鍵離開，或刪掉 `MainActivity` 的 `onBackPressed`。
