"""monitor.py - async health checks for all local AI services."""
import httpx
import asyncio
import os
from datetime import datetime
from .models import ServiceHealth, ServiceStatus, SystemHealth

SERVICES = [
    {"name": "langgraph-proxy", "url": os.getenv("PROXY_URL",    "http://localhost:1236"), "path": "/health"},
    {"name": "lm-studio",       "url": os.getenv("LM_STUDIO_URL","http://localhost:1234"), "path": "/v1/models"},
    {"name": "stack-rag",       "url": os.getenv("STACK_RAG_URL","http://localhost:8000"), "path": "/health"},
]


async def check_service(svc: dict) -> ServiceHealth:
    url = svc["url"] + svc["path"]
    t0  = asyncio.get_event_loop().time()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
        latency = round((asyncio.get_event_loop().time() - t0) * 1000, 1)
        status  = ServiceStatus.OK if resp.status_code < 400 else ServiceStatus.DEGRADED
        return ServiceHealth(name=svc["name"], url=svc["url"],
                             status=status, latency_ms=latency)
    except Exception as e:
        latency = round((asyncio.get_event_loop().time() - t0) * 1000, 1)
        return ServiceHealth(name=svc["name"], url=svc["url"],
                             status=ServiceStatus.DOWN,
                             latency_ms=latency, error=str(e)[:100])


async def check_all() -> SystemHealth:
    results = await asyncio.gather(*[check_service(s) for s in SERVICES])
    overall = (
        ServiceStatus.OK       if all(s.status == ServiceStatus.OK for s in results) else
        ServiceStatus.DOWN     if all(s.status == ServiceStatus.DOWN for s in results) else
        ServiceStatus.DEGRADED
    )
    return SystemHealth(status=overall, services=list(results))
