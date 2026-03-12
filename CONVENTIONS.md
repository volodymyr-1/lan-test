# Conventions — lan-test

> OpenCode must follow these conventions exactly.

---

## Naming

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Pydantic models: noun describing the data (`ServiceHealth`, `RequestRecord`)

## Code style

```python
# Imports order: stdlib → third-party → local
import os
import asyncio

import httpx
from pydantic import BaseModel

from .models import ServiceHealth
```

- Type hints on all function signatures
- Docstrings only on public functions (one line is enough)
- No commented-out code in commits
- Max line length: 100

## Tests

```python
# File: tests/test_<module>.py
# Function: test_<function>_<scenario>

async def test_check_service_ok(): ...
async def test_check_service_down(): ...
async def test_check_service_degraded(): ...
```

- Cover: happy path + error/down case
- Use `unittest.mock` — no real network calls in tests
- No `time.sleep` in tests

## Git commits

Format: `type: short description`

Types: `feat` / `fix` / `refactor` / `test` / `docs` / `chore`

Examples:
```
feat: add SQLite request history
fix: handle timeout in monitor
test: add coverage for db.save_request
docs: update CHANGELOG for 0.2.0
```

## CHANGELOG format

```markdown
## [0.2.0] - YYYY-MM-DD
### Added
- ...
### Fixed
- ...
### Changed
- ...
```
