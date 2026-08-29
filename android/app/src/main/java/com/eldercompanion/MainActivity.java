package com.eldercompanion;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.webkit.MimeTypeMap;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * 爺爺的小助手 · WebView 外殼 + 一點原生功能。
 * 長輩看到的畫面（按鈕、麥克風、對話）都是 companion 網頁，跑在 WebView 裡。
 * 但「家人專用」的事——例如上傳老照片——原生處理更順手：系統原生選圖、直接
 * 呼叫後端同一支 API，不用經過網頁那層。入口是螢幕角落一顆不顯眼的⚙。
 *
 * 伺服器網址「不寫死」：首次開啟會請你輸入（記在手機裡），所以同一個 APK 每個家庭都能用。
 * 連不上時（打錯 / 電腦沒開）會自動再跳出來讓你重填。
 */
public class MainActivity extends Activity {

    private static final String PREFS = "companion";
    private static final String KEY_URL = "server_url";
    private static final int REQ_PICK_PHOTOS = 1001;

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

        // 用 FrameLayout 疊一顆不顯眼的「家人專用」入口在角落，長輩不太會注意到
        FrameLayout root = new FrameLayout(this);
        root.addView(web, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));

        float density = getResources().getDisplayMetrics().density;
        TextView familyBtn = new TextView(this);
        familyBtn.setText("⚙");
        familyBtn.setTextSize(15);
        familyBtn.setTextColor(0x66FFFFFF);
        familyBtn.setGravity(Gravity.CENTER);
        familyBtn.setBackgroundResource(R.drawable.corner_btn_bg);
        int sizePx = (int) (34 * density), marginPx = (int) (10 * density);
        FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(sizePx, sizePx);
        lp.gravity = Gravity.TOP | Gravity.END;
        lp.setMargins(0, marginPx, marginPx, 0);
        familyBtn.setLayoutParams(lp);
        familyBtn.setOnClickListener(v -> showFamilyMenu());
        root.addView(familyBtn);

        setContentView(root);

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

    /** 「家人專用」選單：上傳老照片 / 改連線網址。從角落⚙進來。 */
    private void showFamilyMenu() {
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_family, null);
        final AlertDialog dialog = new AlertDialog.Builder(this).setView(view).create();
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        }

        view.findViewById(R.id.btnUploadPhotos).setOnClickListener(b -> { dialog.dismiss(); pickPhotos(); });
        view.findViewById(R.id.btnChangeUrl).setOnClickListener(b -> { dialog.dismiss(); showUrlDialog(savedUrl()); });
        view.findViewById(R.id.btnCloseFamily).setOnClickListener(b -> dialog.dismiss());

        dialog.show();
        if (dialog.getWindow() != null) {
            int w = (int) (getResources().getDisplayMetrics().widthPixels * 0.86);
            dialog.getWindow().setLayout(w, WindowManager.LayoutParams.WRAP_CONTENT);
        }
    }

    /** 系統原生選圖（可多選），不需要額外的儲存權限（SAF 授權範圍僅限選中的檔案）。 */
    private void pickPhotos() {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("image/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        try {
            startActivityForResult(intent, REQ_PICK_PHOTOS);
        } catch (Exception e) {
            Toast.makeText(this, "找不到選圖程式", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode != REQ_PICK_PHOTOS || resultCode != RESULT_OK || data == null) return;
        List<Uri> uris = new ArrayList<>();
        if (data.getClipData() != null) {
            int n = data.getClipData().getItemCount();
            for (int i = 0; i < n; i++) uris.add(data.getClipData().getItemAt(i).getUri());
        } else if (data.getData() != null) {
            uris.add(data.getData());
        }
        if (!uris.isEmpty()) uploadPhotosNative(uris);
    }

    /** 逐張讀檔 → 直接 multipart POST 給後端 /setup/upload-photo（跟網頁版共用同一支）。 */
    private void uploadPhotosNative(List<Uri> uris) {
        View pv = LayoutInflater.from(this).inflate(R.layout.dialog_progress, null);
        TextView progressText = pv.findViewById(R.id.progressText);
        AlertDialog progress = new AlertDialog.Builder(this).setView(pv).setCancelable(false).create();
        if (progress.getWindow() != null) {
            progress.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        }
        progress.show();
        if (progress.getWindow() != null) {
            int w = (int) (getResources().getDisplayMetrics().widthPixels * 0.7);
            progress.getWindow().setLayout(w, WindowManager.LayoutParams.WRAP_CONTENT);
        }

        final int total = uris.size();
        final String endpoint = uploadUrl();
        new Thread(() -> {
            int ok = 0, fail = 0;
            for (int i = 0; i < total; i++) {
                final int idx = i + 1;
                runOnUiThread(() -> progressText.setText("上傳中…（" + idx + "/" + total + "）"));
                Uri u = uris.get(i);
                try {
                    byte[] data = readAll(u);
                    String name = resolveFileName(u);
                    String mime = getContentResolver().getType(u);
                    if (mime == null) mime = "image/jpeg";
                    if (postPhoto(endpoint, name, mime, data)) ok++; else fail++;
                } catch (Exception e) {
                    fail++;
                }
            }
            final int okF = ok, failF = fail;
            runOnUiThread(() -> {
                progress.dismiss();
                String msg = failF > 0
                        ? ("完成：" + okF + " 張成功、" + failF + " 張失敗（請確認電腦網址正確、companion 有在跑）")
                        : ("✅ " + okF + " 張照片已上傳，爺爺畫面待機時就會輪播");
                new AlertDialog.Builder(this).setMessage(msg).setPositiveButton("好", null).show();
            });
        }).start();
    }

    private String uploadUrl() {
        String base = savedUrl();
        if (!base.endsWith("/")) base += "/";
        return base + "setup/upload-photo";
    }

    private byte[] readAll(Uri uri) throws Exception {
        InputStream in = getContentResolver().openInputStream(uri);
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int n;
        if (in != null) {
            while ((n = in.read(buf)) > 0) bos.write(buf, 0, n);
            in.close();
        }
        return bos.toByteArray();
    }

    private String resolveFileName(Uri uri) {
        String name = null;
        try (Cursor c = getContentResolver().query(uri, null, null, null, null)) {
            if (c != null && c.moveToFirst()) {
                int idx = c.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (idx >= 0) name = c.getString(idx);
            }
        } catch (Exception ignored) { }
        if (name == null || !hasImageExt(name)) {
            String mime = getContentResolver().getType(uri);
            String ext = mime != null ? MimeTypeMap.getSingleton().getExtensionFromMimeType(mime) : null;
            name = "photo_" + System.currentTimeMillis() + "." + (ext != null ? ext : "jpg");
        }
        return name;
    }

    private boolean hasImageExt(String name) {
        String n = name.toLowerCase();
        return n.endsWith(".jpg") || n.endsWith(".jpeg") || n.endsWith(".png") || n.endsWith(".webp");
    }

    /** 手刻 multipart/form-data POST——不加任何 HTTP 依賴，跟專案「純用 Android framework」一致。 */
    private boolean postPhoto(String urlStr, String filename, String mime, byte[] data) {
        HttpURLConnection conn = null;
        try {
            String boundary = "----EC" + System.currentTimeMillis();
            conn = (HttpURLConnection) new URL(urlStr).openConnection();
            conn.setDoOutput(true);
            conn.setRequestMethod("POST");
            conn.setConnectTimeout(15000);
            conn.setReadTimeout(30000);
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

            OutputStream os = conn.getOutputStream();
            os.write(("--" + boundary + "\r\n").getBytes("UTF-8"));
            os.write(("Content-Disposition: form-data; name=\"photo\"; filename=\"" + filename + "\"\r\n")
                    .getBytes("UTF-8"));
            os.write(("Content-Type: " + mime + "\r\n\r\n").getBytes("UTF-8"));
            os.write(data);
            os.write(("\r\n--" + boundary + "--\r\n").getBytes("UTF-8"));
            os.flush();
            os.close();

            return conn.getResponseCode() == 200;
        } catch (Exception e) {
            return false;
        } finally {
            if (conn != null) conn.disconnect();
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
