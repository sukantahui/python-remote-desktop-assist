"""Global Rendezvous & 9-Digit Desk ID Signaling Server."""

import asyncio
import json
import random
from typing import Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Antigravity Desk Global Rendezvous Server")

# Mapping: 9-Digit Desk ID -> WebSocket Connection
registered_hosts: Dict[str, WebSocket] = {}
registered_clients: Dict[str, WebSocket] = {}


def generate_unique_desk_id() -> str:
    """Generates a formatted 9-digit AnyDesk ID (e.g. 982 411 723)."""
    while True:
        part1 = random.randint(100, 999)
        part2 = random.randint(100, 999)
        part3 = random.randint(100, 999)
        candidate = f"{part1} {part2} {part3}"
        if candidate not in registered_hosts:
            return candidate


@app.get("/")
async def root():
    return {
        "service": "Antigravity Rendezvous Signaling Server",
        "active_hosts": len(registered_hosts),
        "status": "online",
    }


@app.websocket("/ws/rendezvous")
async def rendezvous_endpoint(websocket: WebSocket):
    await websocket.accept()
    assigned_id = None
    role = None

    try:
        while True:
            raw_msg = await websocket.receive_text()
            data = json.loads(raw_msg)
            msg_type = data.get("type")

            # 1. Host registers its 9-digit Desk ID
            if msg_type == "register_host":
                requested_id = data.get("desk_id")
                assigned_id = requested_id if requested_id else generate_unique_desk_id()
                role = "host"
                registered_hosts[assigned_id] = websocket
                await websocket.send_text(json.dumps({
                    "type": "registered",
                    "desk_id": assigned_id,
                    "message": "Host successfully registered on Global Rendezvous.",
                }))

            # 2. Client initiates connection to target Desk ID
            elif msg_type == "connect_target":
                target_id = data.get("target_id")
                if target_id in registered_hosts:
                    host_ws = registered_hosts[target_id]
                    # Forward connection request & SDP offer to Host
                    await host_ws.send_text(json.dumps({
                        "type": "incoming_connection",
                        "client_id": data.get("client_id", "anonymous_client"),
                        "sdp_offer": data.get("sdp_offer"),
                    }))
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "code": "DESK_NOT_FOUND",
                        "message": f"Desk ID {target_id} is currently offline.",
                    }))

            # 3. Host sends back SDP Answer to Client
            elif msg_type == "sdp_answer":
                client_ws = registered_clients.get(data.get("client_id"))
                if client_ws:
                    await client_ws.send_text(json.dumps({
                        "type": "sdp_answer",
                        "sdp_answer": data.get("sdp_answer"),
                    }))

    except WebSocketDisconnect:
        if role == "host" and assigned_id and assigned_id in registered_hosts:
            del registered_hosts[assigned_id]
    except Exception:
        pass


def start_rendezvous_server(host: str = "0.0.0.0", port: int = 9000):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_rendezvous_server()
