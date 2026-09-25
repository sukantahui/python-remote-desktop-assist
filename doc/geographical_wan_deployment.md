# Geographical & WAN Deployment Guide — Global AnyDesk P2P Connectivity

> **Scope**: Connecting machines across different cities, countries, and NAT/Firewall environments using 9-Digit Desk IDs.

---

## 1. How Global Connection (WAN / NAT Traversal) Works

When two machines are in **different geographical locations** (e.g., Host in London behind Home Wi-Fi, Client in Tokyo on 5G), neither machine has a public static IP. The system resolves this using the **WebRTC ICE / STUN / TURN & Rendezvous Protocol**:

```mermaid
sequenceDiagram
    autonumber
    participant Host as Host Machine (London - Desk ID: 982 411 723)
    participant STUN as Public STUN Server (Google / Coturn)
    participant Rendezvous as Global Rendezvous Server (Cloud VPS)
    participant Client as Controller Client (Tokyo - Remote Viewer)

    Note over Host,Rendezvous: 1. Host Registration
    Host->>STUN: Discover Public WAN IP & NAT Port Mapping
    STUN-->>Host: Public Reflexive IP:Port (e.g. 195.12.4.88:51240)
    Host->>Rendezvous: Register Desk ID `982 411 723` + Session Public Key
    Rendezvous-->>Host: Heartbeat Active (Keep-Alive)

    Note over Client,Rendezvous: 2. Connection Handshake Across the World
    Client->>Rendezvous: Connect Request -> Target: `982 411 723`
    Rendezvous->>Host: Signal Incoming Connection from Tokyo Client
    Host-->>Client: Exchange SDP Offer/Answer via Rendezvous WebSocket

    Note over Host,Client: 3. Direct P2P NAT Hole Punching (90% of connections)
    Host->>Client: UDP Hole Punch (Direct DTLS-SRTP P2P Stream)
    Client==>>Host: Direct 60 FPS Video Stream (< 80ms Latency)

    alt Strict / Symmetric Corporate Firewall (10% fallback)
        Host->>Rendezvous: Direct P2P Blocked -> Switch to Encrypted TURN Relay
        Rendezvous==>>Client: Encrypted Relay Tunneling
    end
```

---

## 2. Three Easy Deployment Methods for Worldwide Access

### Method 1: Zero-Config Cloud Rendezvous (Standard AnyDesk Way)
- **How it works**: Deploy the lightweight Python Rendezvous Server on any cloud VPS (AWS, DigitalOcean, Hetzner, Oracle Cloud Free Tier, or Render/Railway).
- **Setup**:
  1. Run `python -m src.server.rendezvous --port 8000` on your cloud server (e.g., `rendezvous.yourdomain.com`).
  2. In your local and remote machine `.env`, set:
     ```env
     RENDEZVOUS_SERVER_URL=wss://rendezvous.yourdomain.com/ws/rendezvous
     STUN_SERVER=stun:stun.l.google.com:19302
     ```
  3. Enter the 9-digit Desk ID from anywhere in the world to connect immediately!

---

### Method 2: Instant Secure Mesh via Tailscale / ZeroTier (Zero Cloud Cost)
- **How it works**: Uses WireGuard mesh to link any number of machines across the globe into a private encrypted network.
- **Setup**:
  1. Install [Tailscale](https://tailscale.com) (Free for up to 100 devices) on both machines.
  2. Each machine gets a global mesh IP (e.g., `100.x.y.z`).
  3. Start the host, and connect directly from any continent with zero port-forwarding.

---

### Method 3: Cloudflare Tunnels or Ngrok (Instant Public URL)
- **How it works**: Exposes your local Python daemon to a secure HTTPS/WSS endpoint anywhere on the internet without touching router settings.
- **Setup**:
  ```powershell
  # Using cloudflared (free):
  cloudflared tunnel --url http://localhost:8000

  # Or using ngrok:
  ngrok http 8000
  ```
  Share the generated secure public URL to connect from any browser on phone, tablet, or PC worldwide!

---

## 3. Security & Global Latency Benchmarks

| Route | Typical Direct P2P Latency | Video Quality | Encryption |
| :--- | :--- | :--- | :--- |
| **Same Country (US East -> US West)** | $35 - 55\text{ ms}$ | 1080p @ 60 FPS | DTLS 1.3 / AES-128-GCM |
| **Intercontinental (US -> Europe)** | $80 - 110\text{ ms}$ | 1080p @ 30-60 FPS | DTLS 1.3 / AES-128-GCM |
| **Transpacific (US -> Asia)** | $120 - 170\text{ ms}$ | 1080p @ 30 FPS | DTLS 1.3 / AES-128-GCM |
