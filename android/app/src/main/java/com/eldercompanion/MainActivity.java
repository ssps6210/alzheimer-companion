package com.eldercompanion;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;

/**
 * 爺爺的小助手 · 極簡 WebView 外殼。
 * 把後端 companion 的畫面包成一個 App：一點就開、全螢幕、麥克風原生授權（http 也能錄音）。
 * AI 仍跑在你的 PC 上，這個 App 只是連過去的客戶端。
 *
 * 伺服器網址「不寫死」：首次開啟會請你輸入（記在手機裡），所以同一個 APK 每個家庭都能用。
 * 連不上時（打錯 / 電腦沒開）會自動再跳出來讓你重填。
 */
public class MainActivity extends Activity {

    private static final String PREFS = "companion";
    private static final String KEY_URL = "server_url";

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

        web.setWebViewClient(new WebViewClient() {       // 連結留在 App 內，不跳瀏覽器
            // 主頁連不上（網址打錯 / 電腦沒開機）→ 自動跳出來讓家人重新輸入
            @Override
            public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError err) {
                if (req.isForMainFrame()) {
                    runOnUiThread(new Runnable() {
                        @Override public void run() { showUrlDialog(savedUrl()); }
                    });
                }
            }
        });
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

        String url = savedUrl();
        if (url.isEmpty()) showUrlDialog("");   // 首次開啟：請家人輸入電腦網址
        else web.loadUrl(url);
    }

    private SharedPreferences prefs() { return getSharedPreferences(PREFS, MODE_PRIVATE); }

    private String savedUrl() { return prefs().getString(KEY_URL, ""); }

    /** 跳出暖色對話窗，讓家人填/改「架設 companion 那台電腦」的網址，存起來並載入。 */
    private void showUrlDialog(String current) {
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_server, null);
        final EditText in = view.findViewById(R.id.urlInput);
        in.setText(current.isEmpty() ? "http://" : current);
        in.setSelection(in.getText().length());

        final AlertDialog dialog = new AlertDialog.Builder(this)
                .setView(view)
                .setCancelable(false)
                .create();
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        }

        view.findViewById(R.id.connectBtn).setOnClickListener(b -> {
            String u = in.getText().toString().trim();
            if (u.isEmpty() || u.equals("http://") || u.equals("https://")) return;  // 沒填就先別關
            if (!u.startsWith("http://") && !u.startsWith("https://")) u = "http://" + u;
            prefs().edit().putString(KEY_URL, u).apply();
            dialog.dismiss();
            web.loadUrl(u);
        });

        dialog.show();
        if (dialog.getWindow() != null) {   // 卡片寬度給舒服一點，不要頂滿螢幕
            int w = (int) (getResources().getDisplayMetrics().widthPixels * 0.86);
            dialog.getWindow().setLayout(w, WindowManager.LayoutParams.WRAP_CONTENT);
        }
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
