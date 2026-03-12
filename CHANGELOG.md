# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [0.2.0] - 2026-03-12
### Changed
- `POST /ask` — parses real `provider`, `quality`, `saved`, `tried_providers` from langgraph-proxy response (was hardcoded "unknown")
- Improved error handling: `httpx.RequestError` → 502, `HTTPStatusError` → 502, `KeyError` → 502
### Added
- `tests/test_ask.py` — 5 tests covering happy path, provider recording, cascade, 502 on proxy down, 422 on short question
- `AGENTS.md` — project rules for OpenCode agents

## [0.1.0] - 2026-03-11
### Added
- Initial project structure (src layout, pyproject.toml, tests)
- `models.py` — Pydantic models for services and requests
- `db.py` — SQLite async storage for request history
- `monitor.py` — async health checks for proxy/LM Studio/stack-rag
- `api.py` — FastAPI REST endpoints
- `cli.py` — Typer CLI interface
