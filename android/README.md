# 爺爺的小助手 · Android App（WebView 外殼）

把 companion 的長輩畫面包成一個 Android App：**一點就開、全螢幕、麥克風原生授權**（解決瀏覽器在 http 下不給錄音的坑）、可鎖成單一畫面給長輩用。

> ⚠️ 這只是「客戶端」—— AI 仍跑在你的 PC（companion + Qwen）。平板要連得到那台 PC：同一 WiFi 用區網 IP，或用 https 通道連遠端。

## 需要
- **Android Studio**（免費）
- 一台 Android 平板／手機（Android 7 以上）

## A. 用 Android Studio（推薦）
1. **改網址**：打開 `app/src/main/java/com/eldercompanion/MainActivity.java`，把最上面的 `COMPANION_URL` 改成你電腦上 companion 的網址：
   - 同一 WiFi：`http://<你電腦IP>:8080/`（IP 在「一鍵啟動」視窗會顯示）
   - 遠端：`https://<你的通道網址>/`
2. Android Studio →「**Open**」→ 選這個 `android` 資料夾 → 等 Gradle 同步（第一次會下載，請耐心）。
3. 接上平板（開發者模式 + USB 偵錯）按 **Run ▶**；或 **Build → Build APK(s)**，把產生的 `app-debug.apk` 傳到平板安裝。
4. 平板首次開啟會問麥克風權限 → **允許**。

> Gradle 同步若報版本問題，讓 Android Studio 自動升級 AGP / Gradle 即可（或用下面 B 方案）。

## B. 怕版本問題就用這個（最保險）
1. Android Studio →「New Project」→「**Empty Views Activity**」（Language 選 **Java**，package 填 `com.eldercompanion`）。
2. 用本資料夾的 `MainActivity.java`、`AndroidManifest.xml` 覆蓋新專案對應的檔。
3. 改 `COMPANION_URL` → **Build APK**。

## 給長輩用（可選：鎖成單一 App / Kiosk）
- Android 內建「**螢幕固定／App 固定**」（設定 → 安全性）可把平板鎖在這個 App，長輩退不出去、只看得到爺爺畫面。
- 桌面其他圖示都拿掉，只留這一個。

## 排錯
- **白畫面／連不到**：確認 PC 的 companion 有在跑、平板和 PC **同一 WiFi**、`COMPANION_URL` 的 IP 對。
- **按按鈕不錄音**：到「設定 → 應用程式 → 爺爺的小助手 → 權限」確認麥克風已允許。
- **想退出 App**：預設返回鍵不會退（防長輩誤退）；用「最近工作」或 Home 鍵離開，或刪掉 `MainActivity` 的 `onBackPressed`。
