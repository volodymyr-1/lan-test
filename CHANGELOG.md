# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/)

## [Unreleased]

## [0.1.0] - 2026-03-11
### Added
- Initial project structure (src layout, pyproject.toml, tests)
- `models.py` — Pydantic models for services and requests
- `db.py` — SQLite async storage for request history
- `monitor.py` — async health checks for proxy/LM Studio/stack-rag
- `api.py` — FastAPI REST endpoints
- `cli.py` — Typer CLI interface
