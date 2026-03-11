"""models.py - Pydantic models for lan-test."""
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    OK      = "ok"
    DEGRADED = "degraded"
    DOWN    = "down"


class ServiceHealth(BaseModel):
    name:         str
    url:          str
    status:       ServiceStatus
    latency_ms:   float | None = None
    checked_at:   datetime = Field(default_factory=datetime.utcnow)
    error:        str | None = None


class SystemHealth(BaseModel):
    status:   ServiceStatus
    services: list[ServiceHealth]
    version:  str = "0.1.0"


class RequestRecord(BaseModel):
    id:          int | None = None
    question:    str
    provider:    str
    quality:     float
    saved:       bool
    latency_ms:  float
    created_at:  datetime = Field(default_factory=datetime.utcnow)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


class AskResponse(BaseModel):
    answer:          str
    provider:        str
    quality:         float
    saved:           bool
    tried_providers: list[str]
    latency_ms:      float
