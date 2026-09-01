# 參與這個專案 · Contributing

謝謝你願意投入。這個專案的使用者是**失智長輩**——他們無法回報 bug、無法抱怨、
也不會知道系統壞了。所以這裡的規矩比一般開源專案嚴一點，請先讀完這頁。

> _Thank you for helping. The users of this project are elders with dementia:
> they cannot report bugs, cannot complain, and will not know when something
> breaks. The rules here are stricter than a typical project — please read on._

---

## 三條不可退讓的底線

**1. 絕不提交任何個人資料**
聲音、照片、錄音、對話記錄、金鑰，一律不進版本庫。`.gitignore` 已經擋掉，
CI 的隱私掃描是第二道防線。送 PR 前請自己先跑一次：

```bash
python tools/privacy_scan.py
```

**2. 安全護欄不可以退讓**
「不糾正、不催促、找已故親人時溫柔安撫而不揭穿、不編造事實、不自稱特定身分」——
這些不是產品功能，是照護倫理。**任何改動 persona 的 PR，都必須跑安全測試並附上結果：**

```bash
venv\Scripts\python.exe tests\test_safety.py
```

這些測試會用真實 LLM 跑九個高風險情境（需要你自己的 API 金鑰，會有少量費用）。
測試曾經真的抓到模型憑空捏造一整段「某某昨天有來看你」的探視情節——這種回覆
會讓長輩拿去和現實對照，造成更深的混亂。**紅燈就不要合併。**

**3. 同意閘門與浮水印預設保持開啟**
聲音克隆是雙面刃。設定音色需要本人口說同意、生成語音會打上 AI 浮水印，
這兩者的**預設值必須是開啟**。可以提供關閉的選項（`CONSENT_REQUIRED=0`、
`WATERMARK=0`）給進階使用者，但不要改預設。

---

## 開發環境

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1      # 有 NVIDIA 顯卡
powershell -ExecutionPolicy Bypass -File install_cpu.ps1  # 沒有顯卡
```

架構、各服務的角色、踩過的坑，都寫在 [`PROJECT.md`](PROJECT.md)。

## 送 PR 之前

- [ ] `python tools/privacy_scan.py` 通過
- [ ] 改過 persona / 固定句 / LLM 設定 → `tests\test_safety.py` 全綠
- [ ] 改過 `companion_web.py` → `python -m py_compile companion_web.py` 通過
- [ ] 改過 Android → 讓 CI build 過（push 後看 Actions）
- [ ] 說明「為什麼」，不只是「改了什麼」

## 特別歡迎這些貢獻

- **在地化**：台語、客語的辨識與語音——這對台灣的失智照護場景很關鍵，
  目前卡在模型可用性，如果你懂這塊，非常需要你
- **安全護欄**：更多危險情境測試案例（`tests/safety_cases.yaml`）
- **人設**：不同失智階段、不同關係的陪伴語氣（見 [`docs/人設範例.md`](docs/人設範例.md)）
- **無障礙**：更大的字、更高的對比、更簡單的操作

## 語氣與文件

程式碼註解與文件用**繁體中文**，說明「為什麼這樣做」而不只是「做了什麼」。
面向長輩與家人的文字，請用正向的說法（講「要做什麼」，不要用「不要做什麼」的句型）。

## 授權

送出 PR 即表示你同意你的貢獻以 [MIT](LICENSE) 授權釋出。
