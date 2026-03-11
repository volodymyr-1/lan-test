# Task: Интеграция с langgraph-proxy через /ask
Version: 0.2.0
Branch: feature/ask-endpoint
Priority: high

## Context
api.py уже имеет заглушку /ask которая вызывает proxy напрямую через httpx.
Нужно доработать её: записывать реальный provider и tried_providers из ответа графа,
добавить endpoint /stats для агрегированной статистики из БД.
db.py и models.py уже готовы — используй их как есть.

## What to build
1. Улучшить POST /ask:
   - proxy возвращает JSON с полями answer, provider, quality, saved, tried_providers
   - записывать provider и tried_providers корректно (сейчас hardcoded "unknown")
   - возвращать tried_providers в AskResponse

2. GET /stats — уже есть в api.py, убедиться что работает корректно

3. GET /history — уже есть, убедиться что возвращает список RequestRecord

## Files
MODIFY:
  src/lan_test/api.py  — исправить /ask, проверить /stats и /history

CREATE:
  tests/test_ask.py    — тесты для /ask endpoint

DO NOT TOUCH:
  models.py
  db.py
  monitor.py
  cli.py

## Acceptance criteria
- [ ] POST /ask корректно парсит ответ от proxy (answer, provider, quality, tried_providers)
- [ ] RequestRecord сохраняется с реальным provider (не "unknown")
- [ ] если proxy недоступен — возвращает 502 с понятным сообщением
- [ ] тесты мокают httpx.AsyncClient — без реальных сетевых вызовов
- [ ] GET /stats возвращает total, saved, avg_quality, by_provider

## Definition of Done
- [ ] pytest проходит (все тесты включая существующие 5)
- [ ] коммит в feature/ask-endpoint
- [ ] CHANGELOG.md обновлён (секция [0.2.0])
- [ ] ARCHITECTURE.md и CONVENTIONS.md соблюдены
