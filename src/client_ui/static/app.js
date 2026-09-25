// Antigravity Desk AI — Client Application Logic

let ws = null;
let isConnected = false;
let canvas, ctx;
let lastFrameTime = performance.now();
let fpsCount = 0;
let currentDeskId = "982 411 723";

document.addEventListener("DOMContentLoaded", () => {
    canvas = document.getElementById("screen-canvas");
    ctx = canvas.getContext("2d");

    setupEventListeners();
    initWebSocket();
});

function setupEventListeners() {
    // Navigation & Connection
    document.getElementById("btn-connect").addEventListener("click", () => {
        const deskId = document.getElementById("remote-id-input").value;
        connectToDesk(deskId);
    });

    document.getElementById("btn-disconnect").addEventListener("click", disconnectSession);

    // Copy ID
    document.getElementById("btn-copy-id").addEventListener("click", () => {
        const id = document.getElementById("local-desk-id").innerText;
        navigator.clipboard.writeText(id);
        alert("Desk ID copied to clipboard: " + id);
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
            connectToDesk("982 411 723");
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

    // AI Sidebar Toggle
    document.getElementById("btn-toggle-ai-sidebar").addEventListener("click", () => {
        const sidebar = document.getElementById("ai-sidebar");
        sidebar.classList.toggle("hidden");
    });
}

function initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/stream`;

    ws = new WebSocket(wsUrl);
    ws.binaryType = "blob";

    ws.onopen = () => {
        console.log("[WS] Connected to Host Daemon");
        document.getElementById("telemetry-status").innerText = "Online (Connected)";
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
        document.getElementById("telemetry-status").innerText = "Disconnected";
        setTimeout(initWebSocket, 2000);
    };
}

function connectToDesk(deskId) {
    currentDeskId = deskId;
    document.getElementById("active-session-label").innerText = `Desk: ${deskId}`;
    document.getElementById("view-dashboard").classList.add("hidden");
    document.getElementById("view-session").classList.remove("hidden");
    addTraceLog("System", `Session established with Desk ${deskId}. Direct input & AI Copilot active.`);
}

function disconnectSession() {
    document.getElementById("view-session").classList.add("hidden");
    document.getElementById("view-dashboard").classList.remove("hidden");
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
    addTraceLog("EMERGENCY", "🛑 Kill Switch Triggered. All AI input injection halted.");
}

function handleTelemetryEvent(data) {
    if (data.type === "step_started") {
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

function updateGazePointer(point) {
    const reticle = document.getElementById("ai-gaze-pointer");
    const container = document.getElementById("canvas-container");
    const rect = canvas.getBoundingClientRect();

    const clientX = rect.left + point[0] * rect.width;
    const clientY = rect.top + point[1] * rect.height;

    reticle.style.left = `${clientX}px`;
    reticle.style.top = `${clientY}px`;
    reticle.classList.remove("hidden");
}

function hideGazePointer() {
    document.getElementById("ai-gaze-pointer").classList.add("hidden");
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

function addTraceLog(timeLabel, text) {
    const logs = document.getElementById("trace-logs");
    const item = document.createElement("div");
    item.className = "trace-item";
    item.innerHTML = `<span class="trace-time">${timeLabel}</span><p>${text}</p>`;
    logs.appendChild(item);
    logs.scrollTop = logs.scrollHeight;
}
