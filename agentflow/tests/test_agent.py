import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_run_agent_returns_expected_fields():
    mock_result = {
        "answer": "Cloud Run is a serverless platform.",
        "session_id": "test-session-123",
        "trace_id": "trace-abc",
        "steps": 3,
    }
    with patch("app.agents.orchestrator.run_agent",
               new=AsyncMock(return_value=mock_result)):
        from app.agents.orchestrator import run_agent
        result = await run_agent("What is Cloud Run?")
        assert "answer" in result
        assert "session_id" in result
        assert "trace_id" in result
        assert "steps" in result


@pytest.mark.asyncio
async def test_health_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app
    with patch("app.agents.orchestrator.get_graph"):
        with patch("app.config.get_settings") as mock_settings:
            mock_settings.return_value = MagicMock(log_level="INFO")
            client = TestClient(app)
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"
