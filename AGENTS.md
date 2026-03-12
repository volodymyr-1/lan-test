# lan-test — Agent Rules

## Project Overview
FastAPI monitoring service that acts as a **test bed for the langgraph-lab pipeline**.
It proxies questions to `langgraph-proxy` (port 1236), records results to SQLite, and exposes health/stats endpoints.

- **Version**: 0.1.0 (current), 0.2.0 (in progress on `feature/ask-endpoint`)
- **Python**: 3.11+, async throughout (asyncio, aiosqlite, httpx)
- **Framework**: FastAPI + Pydantic v2 + Uvicorn

---

## Project Structure

```
src/lan_test/
  api.py       — FastAPI app, all HTTP endpoints (MAIN FILE)
  models.py    — Pydantic models only (DO NOT MODIFY without explicit instruction)
  db.py        — aiosqlite CRUD (DO NOT MODIFY without explicit instruction)
  monitor.py   — async health checks (DO NOT MODIFY without explicit instruction)
  cli.py       — Typer CLI (DO NOT MODIFY without explicit instruction)
tests/
  test_health.py   — existing 5 passing tests
  test_ask.py      — to be created
TASKS/
  current.md       — active task description (read before every session)
CHANGELOG.md
```

---

## External Dependencies (local services)

| Service         | Default URL               | Purpose                        |
|-----------------|---------------------------|--------------------------------|
| langgraph-proxy | http://localhost:1236      | AI pipeline, proxies LLM calls |
| lm-studio       | http://localhost:1234      | Local LLM fallback             |
| stack-rag       | http://localhost:8000      | Vector search (RAG)            |

The proxy accepts `POST /v1/chat/completions` (OpenAI-compatible) and returns:
```json
{
  "choices": [{"message": {"content": "..."}}],
  "provider": "gemini",
  "quality": 0.85,
  "saved": true,
  "tried_providers": ["gemini"]
}
```

---

## Code Conventions

### General
- **Always async** — all DB calls, HTTP calls, endpoint handlers use `async/await`
- **Pydantic v2** — use `model_validate`, not `.dict()`, not `.parse_obj()`
- **No print()** — use proper FastAPI error handling (`HTTPException`)
- **Absolute imports** — always `from .models import X`, never relative `..`
- **Type hints everywhere** — return types on all functions

### Endpoints pattern
```python
@app.post("/endpoint", response_model=ResponseModel)
async def endpoint_name(req: RequestModel) -> ResponseModel:
    try:
        # business logic
        return ResponseModel(...)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Proxy error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Tests pattern (pytest-asyncio)
```python
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

@pytest.fixture
def app_client():
    from lan_test.api import app
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.mark.asyncio
async def test_something(app_client):
    async with app_client as client:
        resp = await client.post("/ask", json={"question": "test?"})
    assert resp.status_code == 200
```

**Always mock httpx.AsyncClient** for proxy calls — no real network in tests.
Mock target: `lan_test.api.httpx.AsyncClient`

---

## Workflow Rules

1. **Before starting** — always read `TASKS/current.md` for current task
2. **Before committing** — run `pytest` and ensure ALL tests pass (including existing 5)
3. **Commit format**: `feat: <description>` / `fix: <description>` / `test: <description>`
4. **Branch**: commit to the branch specified in `TASKS/current.md` (currently `feature/ask-endpoint`)
5. **After implementation** — update `CHANGELOG.md` with the version from the task

---

## Environment
```
PROXY_URL=http://localhost:1236       # langgraph-proxy
LM_STUDIO_URL=http://localhost:1234   # LM Studio
STACK_RAG_URL=http://localhost:8000   # stack-rag
DB_PATH=lan_test.db                   # SQLite file
API_PORT=8080                         # uvicorn port
```

Run tests: `pytest`
Run server: `uvicorn lan_test.api:app --reload --port 8080`
Or via CLI: `lan-test serve`
