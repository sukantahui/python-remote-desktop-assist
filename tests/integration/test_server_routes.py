"""Integration tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from src.server.app import app

client = TestClient(app)


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Antigravity Desk AI" in response.text


def test_css_assets():
    response = client.get("/style.css")
    assert response.status_code == 200
    assert "css" in response.headers["content-type"]


def test_js_assets():
    response = client.get("/app.js")
    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_api_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "desk_id" in data
    assert "local_ip" in data
    assert "lan_url" in data


def test_network_info_endpoint():
    response = client.get("/api/v1/network_info")
    assert response.status_code == 200
    data = response.json()
    assert "desk_id" in data
    assert "local_ip" in data
    assert "lan_url" in data
    assert "local_url" in data


def test_monitors_endpoint():
    response = client.get("/api/v1/monitors")
    assert response.status_code == 200
    data = response.json()
    assert "monitors" in data
    assert len(data["monitors"]) >= 1

    # Test selecting monitor
    select_res = client.post("/api/v1/monitors/select", json={"monitor_index": 1})
    assert select_res.status_code == 200
    assert select_res.json()["success"] is True


def test_rendezvous_registration_and_lookup():
    reg_payload = {
        "desk_id": "111 222 333",
        "ip": "192.168.1.150",
        "port": 8000,
        "hostname": "test-workstation"
    }
    reg_res = client.post("/api/v1/rendezvous/register", json=reg_payload)
    assert reg_res.status_code == 200
    assert reg_res.json()["success"] is True

    # Lookup
    lookup_res = client.get("/api/v1/rendezvous/lookup/111 222 333")
    assert lookup_res.status_code == 200
    data = lookup_res.json()
    assert data["found"] is True
    assert data["desk"]["ip"] == "192.168.1.150"


def test_discovered_desks_endpoint():
    response = client.get("/api/v1/rendezvous/discovered")
    assert response.status_code == 200
    data = response.json()
    assert "discovered" in data
    assert isinstance(data["discovered"], list)

