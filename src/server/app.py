"""FastAPI & WebSocket Server for AI Remote Desktop."""

import asyncio
import json
from pathlib import Path
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.common.config import config
from src.common.logger import logger
from src.host_engine.screen_capture import screen_capturer
from src.host_engine.input_controller import input_controller
from src.ai_brain.orchestrator import ai_orchestrator

app = FastAPI(title="Antigravity Desk AI Server", version="1.0.0")

STATIC_DIR = Path(__file__).parent.parent / "client_ui" / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

active_websockets: Set[WebSocket] = set()


@app.get("/")
async def get_index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/style.css")
async def get_css():
    return FileResponse(STATIC_DIR / "style.css")


@app.get("/app.js")
async def get_js():
    return FileResponse(STATIC_DIR / "app.js")


@app.get("/api/v1/status")
async def get_status():
    return {
        "status": "online",
        "desk_id": config.desk_id,
        "mode": "host_and_client",
        "ai_provider": config.default_vlm_provider,
        "safety_mode": config.safety_mode,
    }


def broadcast_telemetry(data: dict):
    """Sends AI reasoning telemetry to all connected WebSocket clients."""
    msg = json.dumps(data)
    for ws in list(active_websockets):
        try:
            asyncio.create_task(ws.send_text(msg))
        except Exception:
            pass


ai_orchestrator.set_telemetry_callback(broadcast_telemetry)


@app.websocket("/ws/stream")
async def websocket_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    logger.info(f"[+] Client connected: {websocket.client}")

    async def frame_streamer():
        """Pushes desktop screen snapshots to client at ~30 FPS."""
        interval = 1.0 / max(10, min(60, config.fps))
        while websocket in active_websockets:
            try:
                frame_bytes = screen_capturer.capture_jpeg(quality=70)
                if frame_bytes:
                    await websocket.send_bytes(frame_bytes)
                await asyncio.sleep(interval)
            except Exception:
                break

    stream_task = asyncio.create_task(frame_streamer())

    try:
        while True:
            msg_text = await websocket.receive_text()
            data = json.loads(msg_text)
            event_type = data.get("type")

            if event_type == "input_click":
                norm_x = data.get("x", 0.5)
                norm_y = data.get("y", 0.5)
                btn = data.get("button", "left")
                input_controller.mouse_click(norm_x, norm_y, button=btn)

            elif event_type == "ai_goal":
                goal = data.get("goal", "")
                if goal:
                    asyncio.create_task(ai_orchestrator.execute_goal(goal))

            elif event_type == "emergency_stop":
                input_controller.trigger_emergency_stop()
                ai_orchestrator.stop()

    except WebSocketDisconnect:
        logger.info(f"[-] Client disconnected: {websocket.client}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_websockets.discard(websocket)
        stream_task.cancel()
