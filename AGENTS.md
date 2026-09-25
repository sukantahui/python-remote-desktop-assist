# AGENTS.md — AI Agent Operating Guidelines

> **Target Audience**: Any AI Agent, LLM, or pair-programming assistant working on this repository.  
> **Repository Purpose**: Python-Based Autonomous & Generative AI Remote Desktop Software (AnyDesk-Style Architecture).

---

## 1. Core Mission & Philosophy

This repository implements a **Python-Based, AnyDesk-Style Remote Desktop Application** with an integrated **Multimodal Generative AI Copilot ("Computer Use")**. 

It provides:
1. **AnyDesk Experience**: 9-digit Device ID (e.g. `982 411 723`), Rendezvous/P2P NAT traversal, low-latency 60 FPS screen streaming (`bettercam` / `mss` / `aiortc`), direct mouse/keyboard input forwarding, split-pane file transfer, and in-session OS control toolbars.
2. **Generative AI Copilot**: Direct multimodal vision perception (Gemini 2.5/1.5 Pro/Flash, Claude 3.5 Sonnet, Local VLMs), OCR / Visual Grounding (OmniParser/RapidOCR), natural language and voice dialog (Whisper STT + Edge-TTS), and step-by-step GUI automation with human-in-the-loop (HITL) safety verification.
3. **100% Python Engine**: All server components, host daemons, capture engines, AI orchestration, and desktop GUI shells are built in Python (Python 3.11+).

---

## 2. Authoritative Documentation Index (`doc/`)

Before writing or modifying any code, all agents MUST consult the following authoritative documents located in the `doc/` directory:

| Document | Purpose |
| :--- | :--- |
| [`doc/system_architecture.md`](file:///e:/python%20remote%20desktop%20assitant/doc/system_architecture.md) | AnyDesk topology, Rendezvous P2P/Relay, AI OODA loop, WebRTC channels, security model |
| [`doc/feature_specifications.md`](file:///e:/python%20remote%20desktop%20assitant/doc/feature_specifications.md) | Epics, 9-digit ID, split-pane file manager, voice HUD, HITL approval, acceptance criteria |
| [`doc/tech_stack_and_engine.md`](file:///e:/python%20remote%20desktop%20assitant/doc/tech_stack_and_engine.md) | Python libraries (`aiortc`, `FastAPI`, `bettercam`, `google-genai`, `pywin32`, `pydantic`) |
| [`doc/ui_ux_design.md`](file:///e:/python%20remote%20desktop%20assitant/doc/ui_ux_design.md) | Home Dashboard (This Desk / Remote Desk), in-session floating toolbar, glassmorphism tokens |
| [`doc/testing_and_verification.md`](file:///e:/python%20remote%20desktop%20assitant/doc/testing_and_verification.md) | Unit tests, Mock OS Screen harness, benchmark grounding suites, CI/CD pipeline |

---

## 3. Directory Layout & Code Organization

All code additions must strictly follow this structure:

```
├── doc/                            # Authoritative specification documents
│   ├── system_architecture.md
│   ├── feature_specifications.md
│   ├── tech_stack_and_engine.md
│   ├── ui_ux_design.md
│   └── testing_and_verification.md
├── config/                         # Configuration schemas and default YAMLs
│   ├── settings.example.yaml
│   └── safety_policies.yaml
├── src/
│   ├── __init__.py
│   ├── main.py                     # Entry point (CLI, Daemon, and App Launcher)
│   ├── common/                     # Shared utilities, logging, schemas, errors
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── types.py
│   ├── server/                     # Rendezvous signaling, WebSockets, WebRTC & REST API
│   │   ├── app.py
│   │   ├── rendezvous.py           # 9-digit Device ID allocator & session registry
│   │   ├── auth.py
│   │   ├── routes/
│   │   └── streaming/              # WebRTC aiortc & frame streamers
│   ├── host_engine/                # OS-level capture & automation (Host Machine)
│   │   ├── screen_capture.py       # DXGI BetterCam / MSS / Native capture
│   │   ├── input_controller.py     # Mouse & keyboard injection (ctypes / SendInput)
│   │   ├── window_manager.py       # Win32 / OS window enumeration & metadata
│   │   ├── file_manager.py         # Remote split-pane file system agent
│   │   ├── audio_engine.py         # WASAPI loopback & audio streaming
│   │   └── platform/               # OS-specific adapters (windows/, macos/, linux/)
│   ├── ai_brain/                   # Multimodal Reasoning & Agent Execution Loop
│   │   ├── orchestrator.py         # Main Plan -> Observe -> Act -> Verify loop
│   │   ├── providers/              # VLM Providers (Gemini, Claude, OpenAI, Local)
│   │   ├── visual_grounding.py     # UI element detection, Set-of-Marks, OCR
│   │   ├── prompt_templates.py     # System instructions and few-shot examples
│   │   ├── action_parser.py        # Converts model output into structured OS actions
│   │   ├── voice_assistant.py      # STT (Whisper) & TTS (Edge-TTS)
│   │   └── safety_guardrails.py    # Sensitive region masking, forbidden action filters
│   └── client_ui/                  # Python Desktop / Web Viewer Interface
│       ├── app.py                  # PySide6 / Webview App Launcher
│       ├── static/                 # Cyber-glassmorphic Web & Canvas assets
│       └── components/             # Reusable UI components
├── tests/                          # Automated tests & test mocks
│   ├── unit/
│   ├── integration/
│   ├── mocks/
│   └── e2e/
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Project packaging & tool configs
└── README.md                       # High-level overview & quickstart
```

---

## 4. Coding Standards & Conventions

1. **Pure Python & Type Annotations**: Use Python 3.11+ syntax with complete type hints (`mypy` compatible) and Pydantic v2 data validation schemas.
2. **Asynchronous Architecture**: Network operations, frame streaming, and AI API calls must use `asyncio` and `async/await`. Offload CPU-intensive frame processing to `asyncio.to_thread` or worker pools.
3. **Coordinate Normalization**: AI coordinates are normalized $[0.0, 1.0]$. The host controller converts these to exact native integer pixels $(X_{native}, Y_{native})$ considering monitor offsets and DPI scaling factors.
4. **Safety & HITL**: Destructive actions (terminal execution, file deletion) must evaluate against `safety_policies.yaml` and prompt for human approval before execution.
5. **No Placeholders**: Write complete, robust, error-handled implementations.
