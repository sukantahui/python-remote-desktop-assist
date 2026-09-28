"""Unit tests for AI Brain Agent Orchestrator."""

import pytest
from src.ai_brain.orchestrator import AgentOrchestrator
from src.common.types import ActionType, AIAction


@pytest.mark.asyncio
async def test_orchestrator_execution():
    orchestrator = AgentOrchestrator()
    telemetry_events = []

    def on_telemetry(data):
        telemetry_events.append(data)

    orchestrator.set_telemetry_callback(on_telemetry)
    await orchestrator.execute_goal("Open Notepad and write 'Hello World'", max_steps=3)

    assert len(telemetry_events) > 0
    event_types = [e["type"] for e in telemetry_events]
    assert "task_started" in event_types
    assert "step_started" in event_types
    assert "action_proposed" in event_types
    assert "task_completed" in event_types
