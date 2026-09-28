"""FastAPI & WebSocket Server with Multi-Machine LAN/WAN Rendezvous for AI Remote Desktop."""

import asyncio
import json
import socket
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.common.config import config
from src.common.logger import logger
from src.host_engine.screen_capture import screen_capturer
from src.host_engine.input_controller import input_controller
from src.ai_brain.orchestrator import ai_orchestrator

app = FastAPI(title="Antigravity Desk AI Server", version="1.1.0")

# Enable CORS for cross-machine browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "client_ui" / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

active_websockets: Set[WebSocket] = set()

# Built-in Rendezvous & Desk ID Registry (maps 9-digit Desk ID -> {ip, port, hostname, last_seen})
desk_registry: Dict[str, Dict] = {
    config.desk_id.replace(" ", ""): {
        "desk_id": config.desk_id,
        "ip": config.local_ip,
        "port": config.port,
        "hostname": config.hostname,
        "lan_url": config.lan_url,
        "last_seen": time.time(),
    }
}

DISCOVERY_PORT = 9002

def start_lan_discovery():
    """Broadcasts this machine's presence on LAN and listens for other Antigravity Desk instances."""
    def _listener():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", DISCOVERY_PORT))
            while True:
                try:
                    data, addr = sock.recvfrom(2048)
                    payload = json.loads(data.decode("utf-8"))
                    if payload.get("service") == "antigravity_desk":
                        peer_id = payload.get("desk_id", "")
                        clean_id = peer_id.replace(" ", "")
                        peer_ip = payload.get("ip") or addr[0]
                        peer_port = payload.get("port", 8000)
                        peer_host = payload.get("hostname", "")
                        self_clean = config.desk_id.replace(" ", "")
                        if clean_id and clean_id != self_clean:
                            desk_registry[clean_id] = {
                                "desk_id": peer_id,
                                "ip": peer_ip,
                                "port": peer_port,
                                "hostname": peer_host,
                                "lan_url": f"http://{peer_ip}:{peer_port}",
                                "last_seen": time.time(),
                            }
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"LAN discovery listener stopped: {e}")

    def _broadcaster():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while True:
                try:
                    msg = json.dumps({
                        "service": "antigravity_desk",
                        "desk_id": config.desk_id,
                        "ip": config.local_ip,
                        "port": config.port,
                        "hostname": config.hostname,
                    }).encode("utf-8")
                    sock.sendto(msg, ("255.255.255.255", DISCOVERY_PORT))
                except Exception:
                    pass
                time.sleep(3.0)
        except Exception as e:
            logger.debug(f"LAN discovery broadcaster stopped: {e}")

    threading.Thread(target=_listener, daemon=True).start()
    threading.Thread(target=_broadcaster, daemon=True).start()

# Launch discovery in background
try:
    start_lan_discovery()
except Exception:
    pass


class DeskRegistration(BaseModel):
    desk_id: str
    ip: str
    port: int = 8000
    hostname: str = ""


class AuthPayload(BaseModel):
    password: str


class MonitorSelectPayload(BaseModel):
    monitor_index: int


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
@app.head("/api/v1/status")
async def get_status():
    return {
        "status": "online",
        "desk_id": config.desk_id,
        "hostname": config.hostname,
        "local_ip": config.local_ip,
        "port": config.port,
        "lan_url": config.lan_url,
        "mode": "host_and_client",
        "ai_provider": config.default_vlm_provider,
        "safety_mode": config.safety_mode,
        "requires_password": bool(config.unattended_password),
    }


@app.get("/api/v1/network_info")
async def get_network_info():
    """Returns local network access URLs for connecting from other machines."""
    return {
        "desk_id": config.desk_id,
        "hostname": config.hostname,
        "local_ip": config.local_ip,
        "port": config.port,
        "local_url": f"http://localhost:{config.port}",
        "lan_url": config.lan_url,
        "active_connections": len(active_websockets),
    }


@app.get("/api/v1/monitors")
async def get_monitors():
    """Returns connected monitors available for remote viewing."""
    return {"monitors": screen_capturer.list_monitors(), "active_index": screen_capturer.monitor_index}


@app.post("/api/v1/monitors/select")
async def select_monitor(payload: MonitorSelectPayload):
    screen_capturer.select_monitor(payload.monitor_index)
    return {"success": True, "active_index": screen_capturer.monitor_index}


@app.post("/api/v1/auth/verify")
async def verify_auth(payload: AuthPayload):
    """Verifies unattended access passcode for cross-machine connections."""
    if not config.unattended_password:
        return {"authenticated": True, "message": "No password required."}
    if payload.password == config.unattended_password:
        return {"authenticated": True, "message": "Access granted."}
    raise HTTPException(status_code=401, detail="Invalid session passcode.")


@app.post("/api/v1/rendezvous/register")
async def register_desk(payload: DeskRegistration):
    """Registers a remote machine's 9-digit Desk ID and IP address."""
    clean_id = payload.desk_id.replace(" ", "")
    desk_registry[clean_id] = {
        "desk_id": payload.desk_id,
        "ip": payload.ip,
        "port": payload.port,
        "hostname": payload.hostname,
        "lan_url": f"http://{payload.ip}:{payload.port}",
        "last_seen": time.time(),
    }
    return {"success": True, "registered": desk_registry[clean_id]}


@app.get("/api/v1/rendezvous/lookup/{desk_id}")
async def lookup_desk(desk_id: str):
    """Resolves a 9-digit Desk ID to its IP and connect URL."""
    clean_id = desk_id.replace(" ", "")
    if clean_id in desk_registry:
        entry = desk_registry[clean_id]
        return {"found": True, "desk": entry}
    # Check if querying self
    self_clean = config.desk_id.replace(" ", "")
    if clean_id == self_clean:
        return {
            "found": True,
            "desk": {
                "desk_id": config.desk_id,
                "ip": config.local_ip,
                "port": config.port,
                "hostname": config.hostname,
                "lan_url": config.lan_url,
            }
        }
    raise HTTPException(status_code=404, detail=f"Desk ID '{desk_id}' not found in registry.")


@app.get("/api/v1/rendezvous/discovered")
async def get_discovered_desks():
    """Returns all active remote machines discovered on the local network."""
    now = time.time()
    self_clean = config.desk_id.replace(" ", "")
    active_peers = []
    for clean_id, entry in list(desk_registry.items()):
        if clean_id != self_clean:
            if now - entry.get("last_seen", 0) < 30:
                active_peers.append(entry)
    return {"discovered": active_peers}


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
async def websocket_stream_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    await websocket.accept()
    client_host = websocket.client.host if websocket.client else "unknown"
    active_websockets.add(websocket)
    logger.info(f"[+] Remote Machine Connected from IP: {client_host}")

    # Send initial handshake welcome
    await websocket.send_text(json.dumps({
        "type": "handshake",
        "desk_id": config.desk_id,
        "hostname": config.hostname,
        "requires_password": bool(config.unattended_password),
        "monitors": screen_capturer.list_monitors(),
    }))

    async def frame_streamer():
        """Pushes desktop screen snapshots to connected client at target FPS."""
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

            elif event_type == "input_text":
                text = data.get("text", "")
                if text:
                    input_controller.type_text(text)

            elif event_type == "input_key":
                key_name = data.get("key", "")
                if key_name:
                    input_controller.press_key(key_name)

            elif event_type == "input_scroll":
                clicks = data.get("clicks", -3)
                input_controller.mouse_scroll(clicks)

            elif event_type == "select_monitor":
                mon_idx = data.get("index", 1)
                screen_capturer.select_monitor(mon_idx)

            elif event_type == "ai_goal":
                goal = data.get("goal", "")
                if goal:
                    asyncio.create_task(ai_orchestrator.execute_goal(goal))

            elif event_type == "hitl_response":
                approved = data.get("approved", False)
                ai_orchestrator.resolve_hitl(approved)

            elif event_type == "emergency_stop":
                input_controller.trigger_emergency_stop()
                ai_orchestrator.stop()

            elif event_type == "reset_emergency_stop":
                input_controller.reset_emergency_stop()

    except WebSocketDisconnect:
        logger.info(f"[-] Remote Machine Disconnected: {client_host}")
    except Exception as e:
        logger.error(f"WebSocket error from {client_host}: {e}")
    finally:
        active_websockets.discard(websocket)
        stream_task.cancel()
