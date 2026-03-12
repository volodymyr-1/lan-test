"""test_ask.py - Tests for /ask endpoint."""
import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport, Response


@pytest.fixture
async def client():
    from lan_test.api import app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c:
        yield c


def make_proxy_response(
    answer="Test answer from LLM",
    provider="gemini",
    quality=0.85,
    saved=True,
    tried_providers=None,
):
    """Helper: build a mock httpx.Response mimicking langgraph-proxy output."""
    if tried_providers is None:
        tried_providers = [provider]
    body = {
        "choices": [{"message": {"content": answer}}],
        "provider": provider,
        "quality": quality,
        "saved": saved,
        "tried_providers": tried_providers,
    }
    mock_resp = MagicMock(spec=Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = body
    mock_resp.raise_for_status = MagicMock()
    mock_resp.text = json.dumps(body)
    return mock_resp


def mock_http_client(mock_resp):
    """Build AsyncMock context manager that returns mock_resp on .post()"""
    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=False)
    mock_http.post = AsyncMock(return_value=mock_resp)
    return mock_http


@pytest.mark.asyncio
async def test_ask_returns_answer(client):
    """Happy path: proxy returns full response with real provider."""
    mock_resp = make_proxy_response(answer="Paris", provider="gemini", quality=0.9)

    with patch("lan_test.api.httpx.AsyncClient", return_value=mock_http_client(mock_resp)), \
         patch("lan_test.api.save_request", new_callable=AsyncMock):
        resp = await client.post("/ask", json={"question": "What is the capital of France?"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"] == "Paris"
    assert data["provider"] == "gemini"
    assert data["quality"] == 0.9
    assert data["saved"] is True
    assert "gemini" in data["tried_providers"]
    assert data["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_ask_records_provider_correctly(client):
    """Provider from proxy response is saved — not 'unknown'."""
    mock_resp = make_proxy_response(provider="groq", quality=0.7, saved=False)

    with patch("lan_test.api.httpx.AsyncClient", return_value=mock_http_client(mock_resp)), \
         patch("lan_test.api.save_request", new_callable=AsyncMock):
        resp = await client.post("/ask", json={"question": "Hello world?"})

    assert resp.status_code == 200
    assert resp.json()["provider"] == "groq"
    assert resp.json()["provider"] != "unknown"


@pytest.mark.asyncio
async def test_ask_tried_providers_cascade(client):
    """tried_providers reflects full cascade e.g. [gemini, groq]."""
    mock_resp = make_proxy_response(
        provider="groq",
        tried_providers=["gemini", "groq"],
        quality=0.6,
    )

    with patch("lan_test.api.httpx.AsyncClient", return_value=mock_http_client(mock_resp)), \
         patch("lan_test.api.save_request", new_callable=AsyncMock):
        resp = await client.post("/ask", json={"question": "Cascade test?"})

    assert resp.status_code == 200
    assert resp.json()["tried_providers"] == ["gemini", "groq"]


@pytest.mark.asyncio
async def test_ask_proxy_unreachable_returns_502(client):
    """If proxy is down, /ask returns 502 with clear message."""
    import httpx as real_httpx

    mock_http = mock_http_client(None)
    mock_http.post = AsyncMock(
        side_effect=real_httpx.ConnectError("Connection refused")
    )

    with patch("lan_test.api.httpx.AsyncClient", return_value=mock_http):
        resp = await client.post("/ask", json={"question": "Will this fail?"})

    assert resp.status_code == 502
    assert "unreachable" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_ask_question_too_short_returns_422(client):
    """Pydantic validation: question must be >= 3 chars."""
    resp = await client.post("/ask", json={"question": "Hi"})
    assert resp.status_code == 422
