<p align="center">
  <a href="安裝指南.md">繁體中文</a> · <b>English</b>
</p>

# Install Guide (step by step)

> Written for someone **comfortable with a computer but not an engineer**. Follow
> it in order; if you get stuck, the FAQ is at the bottom.
> Expect 30–60 minutes, most of it waiting for downloads.

---

## 0. Check your computer can run it

| | Minimum | Comfortable |
|---|---|---|
| **Graphics card** | NVIDIA **8GB VRAM** (RTX 3060 / 4060 / 2080…) | NVIDIA **12GB+** |
| **RAM** | 8 GB | 16 GB+ |
| **Free disk** | **30 GB** | **50 GB+ SSD** |
| **OS** | Windows 10 (2004+) / 11 | Windows 11 |

**No NVIDIA card?** There is a CPU build. The family voice is still cloned and
everything still stays on your machine — it is just slower, and you skip WSL
entirely. Use `install_cpu.ps1` wherever this guide says `install.ps1`, and
`一鍵啟動_CPU版.bat` instead of `一鍵啟動.bat`. You can also skip step 1.2.

---

## 1. Three things to set up first (once each)

### 1.1 Install Python
Download **Python 3.10 or newer** from <https://www.python.org/downloads/>. During
setup, **tick "Add python.exe to PATH"** at the bottom.

> Miss that tick and you will later see "python not found". Reinstall and tick it.

### 1.2 Install WSL — GPU build only
WSL is Linux running inside Windows; the voice cloning uses it. *CPU build users:
skip this.*

1. Search the Start menu for **PowerShell** → right-click → **Run as administrator**
2. Paste this and press Enter:
   ```
   wsl --install -d Ubuntu-22.04
   ```
3. It will ask you to **restart**. After restarting you may be asked to pick a
   Linux username and password — anything you'll remember is fine.

### 1.3 Get a free AI key
Go to <https://build.nvidia.com>, sign in, open any Nemotron model, click
**Get API Key** at the top right, and copy the `nvapi-…` string.

> Any OpenAI-compatible provider works — see `conf.yaml`. NVIDIA is just the
> default because the free tier is generous.

---

## 2. Install (once)

### 2.1 Download the project
On the GitHub page: green **Code** button → **Download ZIP** → unzip it wherever
you like (say `D:\alzheimer-companion`).

> If you use git, `git clone` is fine. Any folder works — the scripts locate
> themselves.

### 2.2 Open PowerShell in that folder
Open the unzipped folder, click the **address bar** in File Explorer, type
`powershell` and press Enter.

### 2.3 Run the installer
```
powershell -ExecutionPolicy Bypass -File install.ps1
```
It checks your environment, installs the Windows dependencies, sets up the WSL
voice environment (**several GB — expect 20–40 minutes**) and copies the config
files.

### 2.4 Add your key
Open `.env` in the folder with Notepad, replace the placeholder with the
`nvapi-…` string you copied, and **save**.

### 2.5 Start it
Double-click **`一鍵啟動.bat`**. First start loads the models, about 1–2 minutes,
then two browser tabs open.

> 🔑 The first start prints the **family console password** in that window (and
> writes it to `.env` as `SETUP_PASSWORD`). When `/setup` asks, the username is
> `family` and the password is that string. Your browser remembers it after once.
> The console can read the elder's conversation history, so it is always locked;
> the elder's own screen needs no password.

✅ Done. The elder's screen is <http://localhost:8080/>.

### 2.6 Optional — switch language
Open `conf.yaml` and set `language: en` (or `zh-CN`). This changes the interface,
speech recognition and synthesis, the care guardrails and the persona together.
Restart to apply.

---

## 3. Set the family voice (important)

**No one's voice ships with this project** — you provide it:

1. Open <http://localhost:8080/setup> (opened automatically at start)
2. Find **① Set the companion voice**
3. Upload a **clear, quiet, 10–30 second** recording (wav / mp3 / m4a)

The recording must start with the person saying the consent sentence aloud —
the console shows you the exact wording. This is deliberate: the person speaking
is the person consenting, and nothing is set up without it.

4. Press **Set as companion voice** — it takes effect immediately

---

## 4. Put it on the elder's tablet

**Easiest — install the app:**

1. On the tablet, open [Releases](https://github.com/ssps6210/alzheimer-companion/releases)
   and download `elder-companion.apk`
2. Allow installing from unknown sources, then install
3. Open it. On the same WiFi it finds your computer by itself; otherwise scan the
   QR code shown in the family console, or paste the address

The app handles the microphone permission natively, so there is nothing to
configure.

**Or use the browser** (no app): open `http://<your computer's IP>:8080` in
Chrome on the tablet — the IP is shown in the launcher window. For the microphone
to work over plain http you need a one-time setting: `chrome://flags` → search
"insecure" → **Insecure origins treated as secure** → add
`http://<your IP>:8080` → Enabled → Relaunch. Then use Chrome's "Add to Home
screen" so it opens like an app.

---

## 5. FAQ

**"python not found" when running install.ps1**
Python isn't installed, or "Add to PATH" wasn't ticked. Reinstall with that
ticked, **open a new PowerShell**, and try again.

**`wsl --install` fails or does nothing**
Make sure PowerShell is running **as administrator** and Windows is recent enough
(Win10 2004+ / Win11). **Restart after installing.** If it still fails: Control
Panel → Turn Windows features on or off → tick **Windows Subsystem for Linux**
and **Virtual Machine Platform**, then restart.

**install.ps1 says it cannot see the GPU**
Update your graphics driver from GeForce's site (a WSL-capable version). Or use
the CPU build — `install_cpu.ps1`.

**It works, but the voice is generic rather than the family member's**
Either the voice isn't set yet (do section 3), or the cloning service is still
loading — give it a minute or two.

**The tablet button does nothing / no microphone prompt**
Tablet and computer must be on the **same WiFi**. In a browser you need the
`chrome://flags` setting in section 4; the app doesn't. The permission prompt
appears when the button is **pressed**, not when the page opens.

**Downloads are taking forever**
Normal. PyTorch plus the models is several GB. Leave it running.

---

Still stuck? Open an **Issue** on this repository, or see the troubleshooting
section in [`PROJECT.md`](../PROJECT.md) (Traditional Chinese).
