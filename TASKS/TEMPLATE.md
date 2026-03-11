# TASK TEMPLATE
# Copy this to current.md and fill in before giving to OpenCode
---

# Task: [название]
Version: 0.x.x
Branch: feature/[name]
Priority: high | medium | low

## Context
<!-- Почему эта задача нужна, какой модуль затрагивает -->

## What to build
<!-- Что именно реализовать. Конкретно, без лишних слов -->

## Files
CREATE:
  src/lan_test/xxx.py
  tests/test_xxx.py

MODIFY:
  src/lan_test/api.py  — добавить endpoint

DO NOT TOUCH:
  models.py

## Acceptance criteria
- [ ] ...
- [ ] ...

## Definition of Done
- [ ] pytest проходит (все тесты включая старые)
- [ ] коммит в ветку feature/xxx
- [ ] CHANGELOG.md обновлён
- [ ] ARCHITECTURE.md и CONVENTIONS.md соблюдены
