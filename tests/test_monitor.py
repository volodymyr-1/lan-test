"""tests/test_monitor.py"""
import pytest
from unittest.mock import AsyncMock, patch
from lan_test.models import ServiceStatus
from lan_test.monitor import check_service, check_all


@pytest.mark.asyncio
async def test_check_service_ok():
    mock_resp = AsyncMock()
    mock_resp.status_code = 200

    with patch("lan_test.monitor.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_resp)
        result = await check_service({"name": "test", "url": "http://localhost:1236", "path": "/health"})

    assert result.status == ServiceStatus.OK
    assert result.name == "test"


@pytest.mark.asyncio
async def test_check_service_down():
    with patch("lan_test.monitor.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("refused"))
        result = await check_service({"name": "test", "url": "http://localhost:9999", "path": "/health"})

    assert result.status == ServiceStatus.DOWN
    assert result.error is not None


@pytest.mark.asyncio
async def test_check_all_returns_system_health():
    with patch("lan_test.monitor.check_service", new_callable=AsyncMock) as mock_check:
        from lan_test.models import ServiceHealth
        mock_check.return_value = ServiceHealth(
            name="x", url="http://x", status=ServiceStatus.OK, latency_ms=10
        )
        result = await check_all()

    assert result.status == ServiceStatus.OK
    assert len(result.services) == 3
