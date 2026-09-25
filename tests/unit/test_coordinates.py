"""Unit tests for coordinate math and AI action parsing."""

from src.common.types import ActionType, AIAction, RiskTier


def test_action_serialization():
    action = AIAction(
        thought="Click on Spotify icon to open music player",
        action_type=ActionType.MOUSE_CLICK,
        parameters={"point": [0.45, 0.92], "button": "left"},
        risk_tier=RiskTier.TIER_1_SAFE,
    )
    assert action.action_type == ActionType.MOUSE_CLICK
    assert action.parameters["point"] == [0.45, 0.92]
    assert action.risk_tier == RiskTier.TIER_1_SAFE
