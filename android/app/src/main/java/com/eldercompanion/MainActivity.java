package com.eldercompanion;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/**
 * 爺爺的小助手 · 極簡 WebView 外殼。
 * 把後端 companion 的畫面包成一個 App：一點就開、全螢幕、麥克風原生授權（http 也能錄音）。
 * AI 仍跑在你的 PC 上，這個 App 只是連過去的客戶端。
 */
public class MainActivity extends Activity {

    // ⚠️⚠️ 改成你電腦上 companion 的網址 ⚠️⚠️
    //  · 同一個 WiFi：用電腦的區網 IP，例如 http://192.168.1.104:8080/
    //  · 遠端（爺爺不在你旁邊）：用 https 通道網址，例如 https://xxx.trycloudflare.com/
    private static final String COMPANION_URL = "http://192.168.1.104:8080/";

    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 螢幕常亮（長輩用不會自己黑掉）
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        hideSystemBars();

        // 先要麥克風權限（Android 6+ 執行期權限）
        if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, 1);
        }

        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);   // 允許自動播放回覆語音

        web.setWebViewClient(new WebViewClient());       // 連結留在 App 內，不跳瀏覽器
        web.setWebChromeClient(new WebChromeClient() {
            // 關鍵：把麥克風授權給網頁的 getUserMedia —— 這樣即使是 http 也能錄音
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                runOnUiThread(new Runnable() {
                    @Override public void run() { request.grant(request.getResources()); }
                });
            }
        });

        setContentView(web);
        web.loadUrl(COMPANION_URL);
    }

    private void hideSystemBars() {
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
              | View.SYSTEM_UI_FLAG_FULLSCREEN
              | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
              | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
              | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
              | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideSystemBars();
    }

    // 返回鍵：網頁能上一頁就上一頁，否則留在 App（避免長輩誤退）。
    // 要允許退出就把整個方法刪掉。
    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack();
    }
}
