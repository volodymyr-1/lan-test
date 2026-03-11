"""tests/test_api.py"""
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from lan_test.api import app
from lan_test.models import ServiceStatus, ServiceHealth, SystemHealth


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json()["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health():
    mock_health = SystemHealth(
        status=ServiceStatus.OK,
        services=[ServiceHealth(name="x", url="http://x", status=ServiceStatus.OK, latency_ms=5)],
    )
    with patch("lan_test.api.check_all", new_callable=AsyncMock, return_value=mock_health):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
