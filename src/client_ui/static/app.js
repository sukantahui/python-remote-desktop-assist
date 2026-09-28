// Antigravity Desk AI — Multi-Machine Client Application Logic

let ws = null;
let currentWsUrl = null;
let isConnected = false;
let canvas, ctx, canvasContainer;
let lastFrameTime = performance.now();
let fpsCount = 0;
let currentDeskId = "982 411 723";
let keyboardForwarding = true;
let localNetworkInfo = null;

document.addEventListener("DOMContentLoaded", () => {
    canvas = document.getElementById("screen-canvas");
    ctx = canvas.getContext("2d");
    canvasContainer = document.getElementById("canvas-container");

    fetchNetworkInfo();
    setupEventListeners();
    initWebSocket();
});

async function fetchNetworkInfo() {
    try {
        const res = await fetch("/api/v1/network_info");
        if (res.ok) {
            localNetworkInfo = await res.json();
            document.getElementById("local-desk-id").innerText = localNetworkInfo.desk_id;
            document.getElementById("lan-url-display").innerText = localNetworkInfo.lan_url;
            document.getElementById("telemetry-host").innerText = localNetworkInfo.hostname || "Local PC";
            const recentInfo = document.getElementById("recent-local-info");
            if (recentInfo) {
                recentInfo.innerText = `ID: ${localNetworkInfo.desk_id} • ${localNetworkInfo.local_ip}`;
            }
        }
    } catch (e) {
        console.warn("Could not fetch network info:", e);
    }
}

function setupEventListeners() {
    // Navigation & Connection
    document.getElementById("btn-connect").addEventListener("click", () => {
        const target = document.getElementById("remote-id-input").value.trim();
        if (target) connectToDesk(target);
    });

    document.getElementById("btn-disconnect").addEventListener("click", disconnectSession);

    // Copy ID & Copy LAN Link
    document.getElementById("btn-copy-id").addEventListener("click", () => {
        const id = document.getElementById("local-desk-id").innerText;
        navigator.clipboard.writeText(id);
        showNotification("📋 Desk ID copied: " + id);
    });

    document.getElementById("btn-copy-lan").addEventListener("click", () => {
        const url = document.getElementById("lan-url-display").innerText;
        navigator.clipboard.writeText(url);
        showNotification("🔗 LAN Link copied! Open this on other devices on your Wi-Fi: " + url);
    });

    // Killswitch
    document.getElementById("btn-killswitch").addEventListener("click", triggerKillSwitch);

    // AI Execution
    document.getElementById("btn-run-ai").addEventListener("click", () => {
        const goal = document.getElementById("ai-task-input").value;
        if (goal.trim()) executeAIGoal(goal);
    });

    document.getElementById("btn-dashboard-ai").addEventListener("click", () => {
        const goal = document.getElementById("dashboard-ai-goal").value;
        if (goal.trim()) {
            connectToDesk(currentDeskId);
            document.getElementById("ai-task-input").value = goal;
            setTimeout(() => executeAIGoal(goal), 600);
        }
    });

    // In-Session Canvas Input Injection
    canvas.addEventListener("click", handleCanvasClick);
    canvas.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        handleCanvasClick(e, "right");
    });
    canvas.addEventListener("wheel", (e) => {
        e.preventDefault();
        handleCanvasScroll(e);
    });

    // Keyboard capture on canvas container
    canvasContainer.addEventListener("keydown", handleCanvasKey);

    // Monitor Selector
    const monitorSelect = document.getElementById("monitor-select");
    if (monitorSelect) {
        monitorSelect.addEventListener("change", (e) => {
            const idx = parseInt(e.target.value, 10);
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: "select_monitor", index: idx }));
                addTraceLog("Monitor", `Switched to display ${idx}`);
            }
        });
    }

    // Toggle keyboard forwarding
    const kbBtn = document.getElementById("tool-keyboard");
    if (kbBtn) {
        kbBtn.addEventListener("click", () => {
            keyboardForwarding = !keyboardForwarding;
            kbBtn.innerText = `⌨️ Keyboard: ${keyboardForwarding ? "ON" : "OFF"}`;
        });
    }

    // AI Sidebar Toggle
    document.getElementById("btn-toggle-ai-sidebar").addEventListener("click", () => {
        const sidebar = document.getElementById("ai-sidebar");
        sidebar.classList.toggle("hidden");
    });

    // Clear trace
    document.getElementById("btn-clear-trace").addEventListener("click", () => {
        document.getElementById("trace-logs").innerHTML = "";
    });
}

function resolveWsUrl(target) {
    let clean = target.replace("http://", "").replace("https://", "").replace("ws://", "").replace("wss://", "").trim();
    if (clean.includes(":") || clean.split(".").length === 4) {
        // Direct IP / Host address (e.g. 192.168.1.50:8000)
        const host = clean.includes(":") ? clean : `${clean}:8000`;
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        return `${protocol}//${host}/ws/stream`;
    }
    // Default local stream
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${window.location.host}/ws/stream`;
}

function initWebSocket(customUrl = null) {
    if (ws) {
        try {
            ws.close();
        } catch (e) {}
    }

    const wsUrl = customUrl || resolveWsUrl(window.location.host);
    currentWsUrl = wsUrl;

    const dot = document.getElementById("telemetry-dot");
    const statusText = document.getElementById("telemetry-status");
    statusText.innerText = "Connecting...";
    dot.className = "dot pulse-yellow";

    ws = new WebSocket(wsUrl);
    ws.binaryType = "blob";

    ws.onopen = () => {
        isConnected = true;
        console.log(`[WS] Connected to Remote Machine at ${wsUrl}`);
        statusText.innerText = "Online (Connected)";
        dot.className = "dot pulse-green";
        const overlay = document.getElementById("connection-overlay");
        if (overlay) overlay.classList.add("hidden");
    };

    ws.onmessage = async (event) => {
        if (event.data instanceof Blob) {
            // Screen Frame Received (JPEG Binary)
            const imgBitmap = await createImageBitmap(event.data);
            if (canvas.width !== imgBitmap.width) {
                canvas.width = imgBitmap.width;
                canvas.height = imgBitmap.height;
            }
            ctx.drawImage(imgBitmap, 0, 0);

            // FPS calculation
            fpsCount++;
            const now = performance.now();
            if (now - lastFrameTime >= 1000) {
                document.getElementById("telemetry-fps").innerText = fpsCount;
                fpsCount = 0;
                lastFrameTime = now;
            }
        } else {
            // JSON Telemetry / AI Trace
            try {
                const data = JSON.parse(event.data);
                handleTelemetryEvent(data);
            } catch (e) {
                console.error("Error parsing WS message:", e);
            }
        }
    };

    ws.onclose = () => {
        isConnected = false;
        statusText.innerText = "Disconnected";
        dot.className = "dot pulse-red";
    };

    ws.onerror = () => {
        statusText.innerText = "Connection Error";
        dot.className = "dot pulse-red";
    };
}

async function connectToDesk(targetDesk) {
    currentDeskId = targetDesk;
    document.getElementById("active-session-label").innerText = `Connected: ${targetDesk}`;
    document.getElementById("view-dashboard").classList.add("hidden");
    document.getElementById("view-session").classList.remove("hidden");
    
    const overlay = document.getElementById("connection-overlay");
    if (overlay) overlay.classList.remove("hidden");

    canvasContainer.focus();
    addTraceLog("System", `Initiating session with Remote Machine [${targetDesk}]...`);

    // Check if connecting to remote IP or Desk ID lookup
    let cleanTarget = targetDesk.replace(" ", "");
    if (!cleanTarget.includes(":") && cleanTarget.split(".").length !== 4) {
        // Try looking up Desk ID via rendezvous API
        try {
            const lookupRes = await fetch(`/api/v1/rendezvous/lookup/${cleanTarget}`);
            if (lookupRes.ok) {
                const data = await lookupRes.json();
                if (data.found && data.desk && data.desk.ip) {
                    const remoteHost = `${data.desk.ip}:${data.desk.port || 8000}`;
                    addTraceLog("Discovery", `Found Desk ID on LAN at ${remoteHost}`);
                    initWebSocket(resolveWsUrl(remoteHost));
                    return;
                }
            }
        } catch (e) {
            console.log("Rendezvous lookup skipped, using direct connection.");
        }
    }

    const wsUrl = resolveWsUrl(targetDesk);
    initWebSocket(wsUrl);
}

function disconnectSession() {
    document.getElementById("view-session").classList.add("hidden");
    document.getElementById("view-dashboard").classList.remove("hidden");
    addTraceLog("System", "Session disconnected.");
}

function handleCanvasClick(e, button = "left") {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const canvasX = (e.clientX - rect.left) * scaleX;
    const canvasY = (e.clientY - rect.top) * scaleY;

    const normX = canvasX / canvas.width;
    const normY = canvasY / canvas.height;

    ws.send(JSON.stringify({
        type: "input_click",
        x: normX,
        y: normY,
        button: button
    }));
}

function handleCanvasScroll(e) {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    const clicks = e.deltaY > 0 ? -3 : 3;
    ws.send(JSON.stringify({
        type: "input_scroll",
        clicks: clicks
    }));
}

function handleCanvasKey(e) {
    if (!keyboardForwarding || !ws || ws.readyState !== WebSocket.OPEN) return;

    // Forward special keys
    const specialKeys = ["Enter", "Backspace", "Tab", "Escape", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Delete"];
    if (specialKeys.includes(e.key)) {
        e.preventDefault();
        ws.send(JSON.stringify({
            type: "input_key",
            key: e.key
        }));
    } else if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        ws.send(JSON.stringify({
            type: "input_text",
            text: e.key
        }));
    }
}

function executeAIGoal(goal) {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    addTraceLog("Goal", `Started: "${goal}"`);
    ws.send(JSON.stringify({
        type: "ai_goal",
        goal: goal
    }));
}

function triggerKillSwitch() {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ws.send(JSON.stringify({ type: "emergency_stop" }));
    addTraceLog("EMERGENCY", "🛑 Kill Switch Triggered! All remote actions halted.");
}

function handleTelemetryEvent(data) {
    if (data.type === "handshake") {
        addTraceLog("Handshake", `Connected to ${data.hostname || "Remote Machine"}. ID: ${data.desk_id}`);
        if (data.monitors && data.monitors.length) {
            updateMonitorDropdown(data.monitors);
        }
        if (data.requires_password) {
            showPasswordModal();
        }
    } else if (data.type === "step_started") {
        addTraceLog(`Step ${data.payload.step}`, data.payload.status);
    } else if (data.type === "action_proposed") {
        addTraceLog(`AI Thought [Step ${data.payload.step}]`, data.payload.thought);
        if (data.payload.parameters && data.payload.parameters.point) {
            updateGazePointer(data.payload.parameters.point);
        }
    } else if (data.type === "task_completed") {
        addTraceLog("Complete", `✅ ${data.payload.message}`);
        hideGazePointer();
    } else if (data.type === "hitl_approval_required") {
        showHITLCard(data.payload);
    }
}

function updateMonitorDropdown(monitors) {
    const select = document.getElementById("monitor-select");
    if (!select) return;
    select.innerHTML = "";
    monitors.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m.index;
        opt.innerText = `🖥️ ${m.label}`;
        select.appendChild(opt);
    });
}

function updateGazePointer(point) {
    const reticle = document.getElementById("ai-gaze-pointer");
    const rect = canvas.getBoundingClientRect();

    const clientX = rect.left + point[0] * rect.width;
    const clientY = rect.top + point[1] * rect.height;

    reticle.style.left = `${clientX}px`;
    reticle.style.top = `${clientY}px`;
    reticle.classList.remove("hidden");
}

function hideGazePointer() {
    const reticle = document.getElementById("ai-gaze-pointer");
    if (reticle) reticle.classList.add("hidden");
}

function showHITLCard(payload) {
    const card = document.getElementById("hitl-card");
    document.getElementById("hitl-text").innerText = `AI Action: ${payload.action.thought}`;
    card.classList.remove("hidden");

    document.getElementById("btn-hitl-approve").onclick = () => {
        card.classList.add("hidden");
        ws.send(JSON.stringify({ type: "hitl_response", approved: true }));
    };
    document.getElementById("btn-hitl-reject").onclick = () => {
        card.classList.add("hidden");
        ws.send(JSON.stringify({ type: "hitl_response", approved: false }));
    };
}

function showPasswordModal() {
    const modal = document.getElementById("auth-modal");
    if (!modal) return;
    modal.classList.remove("hidden");

    document.getElementById("btn-auth-submit").onclick = async () => {
        const pwd = document.getElementById("auth-password-input").value;
        try {
            const res = await fetch("/api/v1/auth/verify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password: pwd })
            });
            if (res.ok) {
                modal.classList.add("hidden");
                showNotification("Session unlocked!");
            } else {
                alert("Incorrect passcode.");
            }
        } catch (e) {
            alert("Auth failed.");
        }
    };

    document.getElementById("btn-auth-cancel").onclick = () => {
        modal.classList.add("hidden");
        disconnectSession();
    };
}

function showNotification(msg) {
    alert(msg);
}

function addTraceLog(timeLabel, text) {
    const logs = document.getElementById("trace-logs");
    if (!logs) return;
    const item = document.createElement("div");
    item.className = "trace-item";
    item.innerHTML = `<span class="trace-time">${timeLabel}</span><p>${text}</p>`;
    logs.appendChild(item);
    logs.scrollTop = logs.scrollHeight;
}
