# Architecture — lan-test

> This file is written by the Architect (Claude).
> OpenCode must read this before writing any code.
> Do NOT modify without explicit architect approval.

---

## Purpose

Monitoring service and test bed for the langgraph-lab pipeline.
Tracks health of local AI services, logs request history, exposes REST API.

## Stack (frozen)

| Layer      | Choice              | Reason                          |
|------------|---------------------|---------------------------------|
| Web        | FastAPI             | async, Pydantic v2 native       |
| DB         | SQLite + aiosqlite  | zero-dependency, local only     |
| Validation | Pydantic v2         | strict types, no v1 compat      |
| CLI        | Typer + Rich        | consistent UX                   |
| Tests      | pytest + asyncio    | async-first                     |
| Build      | hatchling, src/     | modern Python packaging         |
| Python     | 3.11                | match langgraph-lab venv        |

## Layout (src layout — mandatory)

```
src/lan_test/
  __init__.py     # __version__ only
  models.py       # Pydantic models — no logic
  db.py           # DB access — no business logic
  monitor.py      # health checks — pure async functions
  api.py          # FastAPI app — thin handlers only
  cli.py          # Typer CLI — calls api or monitor
tests/
  test_*.py       # mirrors src structure
TASKS/
  current.md      # active task for OpenCode
  done/           # completed tasks archive
```

## Rules (mandatory for OpenCode)

1. **Async everywhere** — no `requests`, no blocking I/O
2. **No logic in api.py** — handlers call functions from other modules
3. **Models in models.py only** — never define Pydantic models inline
4. **Tests mandatory** — every new module gets test_*.py
5. **All existing tests must pass** after any change
6. **CHANGELOG.md must be updated** in every commit
7. **One branch per task** — branch name from TASKS/current.md

## Services (external, read-only from this project)

```
langgraph-proxy  http://localhost:1236   /v1/chat/completions, /health
lm-studio        http://localhost:1234   /v1/models
stack-rag        http://localhost:8000   /health
```

## Versioning

- `MAJOR.MINOR.PATCH` — semantic versioning
- PATCH: bugfix, refactor
- MINOR: new feature, new endpoint
- MAJOR: breaking change

## Current version: 0.1.0

## OpenCode workflow (mandatory)

After completing a task:
1. Run `pytest` — fix until all tests pass
2. Update `CHANGELOG.md` under correct version section
3. Write result to `TASKS/current.md` at the bottom:
   ```
   ## Result
   Status: DONE
   Tests: X passed
   Commit: <hash>
   Notes: <any issues>
   ```
4. Git commit with format: `type: description`
5. Do NOT push — architect reviews first

## Branch strategy (Variant B)

```
stable   ← последняя известно рабочая версия
           обновляется ВРУЧНУЮ после проверки main
           ОТКАТ: git checkout stable

main     ← стабильные релизы (только merge из develop)
           тегируется: git tag v0.x.0

develop  ← текущая разработка
           OpenCode работает здесь

feature/ ← одна задача = одна ветка
           создаётся от develop
           merge обратно в develop через PR
```

## Rollback procedure

Если что-то сломалось:
```powershell
# Быстрый откат к stable
cd D:\!Projects\lan-test
git fetch origin
git checkout stable

# Откат main к предыдущему тегу
git checkout v0.1.0
```

## When to update stable

stable обновляется только когда:
1. Все тесты в main зелёные
2. Архитектор (Claude) явно подтверждает
3. Команда: git checkout stable && git merge main && git push
