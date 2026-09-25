# 🚀 AI-Powered Remote Desktop Assistant (AnyDesk Paradigm)

> A next-generation, high-performance **Python-based Remote Desktop application** featuring an integrated **Multimodal Generative AI Copilot ("Computer Use")**, AnyDesk-style 9-digit Device ID pairing, low-latency screen streaming, and human-in-the-loop safety guardrails.

---

## 📖 Authoritative Documentation & User Manuals

All project documentation, user manuals, and technical specifications are organized in the [`doc/`](file:///e:/python%20remote%20desktop%20assitant/doc) folder:

| Document | Description |
| :--- | :--- |
| 📖 [**`doc/user_manual.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/user_manual.md) | **End-User Manual**: Step-by-step instructions for installation, dashboard navigation, in-session controls, voice push-to-talk, and troubleshooting. |
| 📚 [**`doc/project_documentation.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/project_documentation.md) | **Master Project Documentation**: High-level synthesis of architecture, core subsystems, module layout, and security principles. |
| 🏗️ [**`doc/system_architecture.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/system_architecture.md) | **Architecture Blueprint**: AnyDesk topology, Rendezvous P2P/Relay server, WebRTC channels, AI OODA loop, and security architecture. |
| 📋 [**`doc/feature_specifications.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/feature_specifications.md) | **Feature Matrix & Specs**: 9-digit Device ID, split-pane file transfer, multimodal AI autonomous agent, voice assistant, and acceptance criteria. |
| ⚙️ [**`doc/tech_stack_and_engine.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/tech_stack_and_engine.md) | **Pure Python Tech Stack**: Library manifest (`FastAPI`, `aiortc`, `bettercam`, `google-genai`, `pywin32`, `pydantic`), and hardware acceleration specs. |
| 🎨 [**`doc/ui_ux_design.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/ui_ux_design.md) | **Design System & Wireframes**: Cyber-Glassmorphism dark theme tokens, AnyDesk Home Dashboard, and in-session floating toolbar. |
| 🧪 [**`doc/testing_and_verification.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/testing_and_verification.md) | **Testing Strategy**: Verification pyramid, unit tests, synthetic headless OS mock harness, and VLM visual grounding benchmark suites. |
| 🌐 [**`doc/geographical_wan_deployment.md`**](file:///e:/python%20remote%20desktop%20assitant/doc/geographical_wan_deployment.md) | **Worldwide WAN Guide**: Connecting across different countries/NATs via STUN/TURN, Cloudflare Tunnels, Tailscale, and Rendezvous servers. |
| 🤖 [**`AGENTS.md`**](file:///e:/python%20remote%20desktop%20assitant/AGENTS.md) | **AI Agent Operating Rules**: Coding conventions, directory structure, coordinate normalization math, and Definition of Done. |

---

## 🌟 Key Highlights

- **AnyDesk-Style P2P Connectivity**: 9-digit Device ID (e.g. `982 411 723`), zero-configuration NAT traversal via WebRTC STUN/TURN, and instant unattended access.
- **Hardware-Accelerated Screen Streaming**: DXGI Desktop Duplication (`bettercam`/`mss`) delivering up to 60 FPS 1080p with sub-100ms latency.
- **Multimodal AI Desktop Copilot ("Computer Use")**: Powered by Google Gemini 2.5/1.5 Pro/Flash, Claude 3.5 Sonnet, and Local Vision Models. Translates natural language goals into precise OS GUI actions (clicks, typing, shortcuts).
- **Split-Pane File Transfer**: AnyDesk-style dual-pane remote file manager with drag-and-drop and AI-powered document summarization.
- **In-Session Toolbar**: Remote display switcher, view scaling (1:1 / fit), native OS controls (`Ctrl+Alt+Del`, Lock), and emergency kill-switch (`Esc + Esc`).
- **Safety First & Privacy Shield**: Automatic blurring of sensitive fields (passwords/banking), three-tier risk action approval (Human-in-the-Loop), and signed audit logs.

---

## 🛠️ Quick Start

### 1. Prerequisites
- Python 3.10 or 3.11+
- Windows 10/11, Linux, or macOS

### 2. Installation
```powershell
# Clone and enter repository
cd "python remote desktop assitant"

# Create and activate virtual environment
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```powershell
python src/main.py
```
*The default browser will automatically open to `http://localhost:8000`.*
