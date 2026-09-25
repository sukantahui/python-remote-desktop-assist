# 📖 User Manual — Antigravity AI Remote Desktop Assistant

> **Software Version**: 1.0.0 (AnyDesk-Style Python Engine)  
> **Audience**: End Users, System Administrators, and Remote Operators

---

## 1. Introduction

**Antigravity AI Remote Desktop Assistant** is a high-performance, Python-based remote desktop application inspired by **AnyDesk** and **TeamViewer**, augmented with an integrated **Multimodal Generative AI Copilot ("Computer Use")**.

With this software, you can:
- View and interact with any remote desktop with sub-100ms latency and 60 FPS video streaming.
- Pair computers across the world using a simple **9-digit Device ID** (e.g., `982 411 723`).
- Delegate complex OS workflows (browsing, file manipulation, data extraction, forms) to an autonomous AI Copilot.
- Speak directly to your remote computer using **Voice Push-to-Talk** and receive spoken progress updates.
- Maintain full security with **Emergency Stop**, sensitive screen masking, and Human-in-the-Loop approvals.

---

## 2. Installation & Quick Start

### 2.1. System Requirements
- **Host Machine (Controlled PC)**: Windows 10/11 (64-bit), Linux (X11/Wayland), or macOS 12+.
- **Client Machine (Controller)**: Any modern web browser (Chrome, Edge, Firefox, Safari) or Python client.
- **Python**: Python 3.10 or 3.11+.

### 2.2. Installation Steps
1. Open PowerShell or Terminal in the project folder:
   ```powershell
   # Create and activate virtual environment
   py -3.10 -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Install dependencies
   pip install -r requirements.txt
   ```

2. *(Optional)* Set up your AI API Key:
   - Copy `.env.example` to `.env`.
   - Add your `GEMINI_API_KEY` (or `ANTHROPIC_API_KEY`).

3. Start the application:
   ```powershell
   python src/main.py
   ```
   *Your default browser will automatically open to `http://localhost:8000`.*

---

## 3. Navigating the Home Dashboard

```
+----------------------------------------------------------------------------------------------------+
|  ⚡ ANTIGRAVITY DESK AI                                       [Online] [FPS: 30] [🛑 STOP]         |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   +---------------------------------------+       +---------------------------------------+        |
|   |  THIS DESK (Your Machine)             |       |  REMOTE DESK (Connect to PC)          |        |
|   |---------------------------------------|       |---------------------------------------|        |
|   |  Your Address:                        |       |  Enter Remote ID or Alias:            |        |
|   |  [ 982  411  723 ]   [ Copy ]         |       |  [ 123  456  789                 ]    |        |
|   |                                       |       |                                       |        |
|   |  [x] Allow Mouse & Keyboard           |       |  [  ⚡ CONNECT DESK  ]                |        |
|   |  [x] Allow Multimodal AI Copilot      |       |                                       |        |
|   |  [x] Enforce Human-in-the-Loop        |       |  [🤖 Delegate AI Goal Directly ]      |        |
|   +---------------------------------------+       +---------------------------------------+        |
+----------------------------------------------------------------------------------------------------+
```

### 3.1. Sharing Your Screen ("This Desk")
- Locate your **9-Digit Device ID** in the green box (e.g., `982 411 723`).
- Click **"📋 Copy"** to share your address with a remote operator or your other devices.
- Toggle permissions on or off (Mouse/Keyboard control, AI Copilot, or Human Approval enforcement).

### 3.2. Connecting to a Remote Computer ("Remote Desk")
- Enter the target computer's **9-Digit ID** in the input field.
- Click **"⚡ Connect Desk"** to immediately open the live remote desktop session.

---

## 4. In-Session Remote Desktop & Floating Toolbar

Once connected, you will see the remote desktop streaming in real-time.

```
+----------------------------------------------------------------------------------------------------+
|  [🖥️ Monitor 1 ▾]  [🔍 100% Fit]  [📁 File Manager]  [⚡ Actions ▾]  [🤖 AI Copilot]  [❌ Disconnect]|
+--------------------------------------------------------------------+-------------------------------+
|                                                                    |  [ AI COPILOT COMMAND CENTER] |
|                                                                    |-------------------------------|
|                                                                    |  PROMPT GOAL:                 |
|                                                                    |  [ "Download latest invoice   |
|                     REMOTE DESKTOP CANVAS                          |    and save to Documents"   ] |
|                                                                    |  [ ▶️ Execute ]  [ 🎙️ Voice ]  |
|              (Low-latency WebRTC Video Stream)                     |-------------------------------|
|                                                                    |  REASONING TRACE:             |
|              +------------------------------+                      |  > [Step 1] Inspecting screen |
|              | AI Gaze Target (X: 520, Y:310)|                     |  > [Step 2] Found download btn|
|              +------------------------------+                      |  > [Step 3] Clicking button...|
+--------------------------------------------------------------------+-------------------------------+
```

### 4.1. In-Session Toolbar Functions
- **🖥️ Monitor Switcher**: Switch between multi-monitor displays on the remote machine.
- **🔍 View Mode**: Toggle between *Original (1:1 pixel resolution)*, *Fit to Window*, and *Stretch*.
- **📁 File Manager**: Opens the split-pane file transfer explorer to upload or download files.
- **⚡ Actions Menu**: Send native OS signals (`Ctrl+Alt+Del`, `Lock Workstation`, `Elevate UAC`).
- **🤖 AI Copilot HUD**: Toggles the right-side AI reasoning panel.
- **❌ Disconnect**: Safely closes the remote session.

### 4.2. Direct Mouse & Keyboard Control
- **Click anywhere on the canvas** to send native mouse clicks to the remote computer.
- **Right-click** on the canvas to open remote context menus.
- Keystrokes typed while focusing the canvas are passed through directly.

---

## 5. Using the Generative AI Copilot ("Computer Use")

The AI Copilot can visually inspect the remote screen and autonomously perform multi-step computer tasks on your behalf.

### 5.1. Submitting a Natural Language Goal
1. Click the **"🤖 AI Copilot HUD"** button on the toolbar to open the sidebar.
2. In the text box, type your desired goal. Examples:
   - *"Open Chrome, search for the top 5 tech news headlines today, and copy them to Notepad."*
   - *"Open Excel, load sales_report.csv from Downloads, and calculate the average revenue in column D."*
   - *"Find the PDF named Invoice_October.pdf on the desktop and move it to the Archive folder."*
3. Click **"▶️ Execute"**.

### 5.2. Step-by-Step Reasoning Trace & Visual Gaze
- The AI will capture a frame snapshot, analyze interactive UI elements, and display its **Thought Process** in the trace window.
- A **Cyan Pulsing Reticle** will show on the screen exactly where the AI is focusing and clicking.

### 5.3. Voice Push-to-Talk Mode
- Click and hold **"🎙️ Voice"** (or hold `Space`).
- Speak your instruction naturally into your microphone.
- Release to send; the AI will transcribe your speech, begin execution, and speak progress updates back to you.

---

## 6. Safety & Human-in-the-Loop (HITL) Verification

### 6.1. Action Risk Tiers
- **Tier 1 (Safe)**: Clicks, navigation, scrolling, and reading screen contents execute automatically.
- **Tier 2 (Moderate)**: Form filling and typing text show a brief visual preview.
- **Tier 3 (High-Risk - Destructive Actions)**: File deletion, shell commands (`rm`, `del`, `format`), or financial checkouts **pause execution** and display an **Approval Modal**:
  ```
  +-------------------------------------------------------+
  |  ⚠️ ACTION APPROVAL REQUIRED                          |
  |  Action: Delete old backup file from C:\Backups       |
  |  [ Reject Action ]               [ Approve Action ]   |
  +-------------------------------------------------------+
  ```

### 6.2. Emergency Kill-Switch (Instant Stop)
If the AI behaves unexpectedly or you want to regain immediate total control:
- Press **`Esc + Esc`** or **`Ctrl + Shift + Alt + K`** on your keyboard, OR
- Click the glowing red **"🛑 EMERGENCY STOP"** button in the top navigation bar.
- *All AI inputs are terminated within $< 20\text{ ms}$.*

---

## 7. Connecting from Different Geographical Locations (WAN)

To connect two machines located in different cities or networks across the internet:

### Option A: Cloudflare Tunnels (Zero Setup)
On the Host PC, run:
```powershell
cloudflared tunnel --url http://localhost:8000
```
Open the provided secure HTTPS URL (`https://xyz.trycloudflare.com`) on your client machine anywhere in the world.

### Option B: Tailscale Mesh (Fastest & Free)
1. Install [Tailscale](https://tailscale.com) on both machines.
2. Start the host on Machine A.
3. On Machine B, open `http://<Machine-A-Tailscale-IP>:8000`.

---

## 8. Frequently Asked Questions (FAQ) & Troubleshooting

### Q1: The screen stream is black or not updating.
- **Fix**: Ensure your host machine display is awake. If running on Windows, verify that `bettercam` or `mss` is installed (`pip install mss pillow`).

### Q2: Mouse clicks are slightly off-target on high-DPI laptops.
- **Fix**: The system automatically accounts for Windows DPI scaling ($125\%, 150\%$). If misaligned, click the **"🔍 100% Fit"** button on the toolbar to reset scaling.

### Q3: How do I change the default 9-digit Desk ID?
- **Fix**: Set `DESK_ID=123456789` in your `.env` file or pass `--desk-id "123 456 789"` when running `python src/main.py`.

### Q4: Which AI model is best for GUI automation?
- **Fix**: Google **Gemini 2.5 Flash** (fastest response time for clicking and navigation) or **Gemini 2.5 Pro** (best for complex multi-app reasoning).
