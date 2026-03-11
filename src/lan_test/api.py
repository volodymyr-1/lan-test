"""api.py - FastAPI REST endpoints."""
import time
import os
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .models import AskRequest, AskResponse, SystemHealth
from .monitor import check_all
from .db import init_db, save_request, get_history, get_stats, RequestRecord
from . import __version__

PROXY_URL = os.getenv("PROXY_URL", "http://localhost:1236")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="lan-test",
    version=__version__,
    description="Monitoring + test bed for langgraph-lab pipeline",
    lifespan=lifespan,
)


@app.get("/health", response_model=SystemHealth)
async def health():
    return await check_all()


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    t0 = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{PROXY_URL}/v1/chat/completions",
                json={
                    "model":    "langgraph-proxy",
                    "messages": [{"role": "user", "content": req.question}],
                    "stream":   False,
                },
            )
        data       = resp.json()
        answer     = data["choices"][0]["message"]["content"]
        provider   = "unknown"
        quality    = 0.9 if len(answer) > 200 else 0.3
        saved      = quality >= 0.5
        latency_ms = round((time.monotonic() - t0) * 1000, 1)

        await save_request(RequestRecord(
            question=req.question, provider=provider,
            quality=quality, saved=saved, latency_ms=latency_ms,
        ))

        return AskResponse(
            answer=answer, provider=provider, quality=quality,
            saved=saved, tried_providers=[], latency_ms=latency_ms,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.get("/history")
async def history(limit: int = 20):
    return await get_history(limit)


@app.get("/stats")
async def stats():
    return await get_stats()


@app.get("/")
async def root():
    return {"service": "lan-test", "version": __version__, "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8080))
    uvicorn.run("lan_test.api:app", host="0.0.0.0", port=port, reload=True)
