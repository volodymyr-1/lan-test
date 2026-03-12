# Task: COMPLETED - Интеграция с langgraph-proxy через /ask
Version: 0.2.0
Branch: feature/ask-endpoint → merged to develop
Status: DONE (2026-03-12)

## What was done
- api.py: POST /ask парсит provider/quality/saved/tried_providers из ответа прокси
- tests/test_ask.py: 5 тестов, 10/10 passed
- AGENTS.md: правила проекта для OpenCode
- CHANGELOG.md: секция [0.2.0] добавлена

---

# Next Task: Тег v0.2.0 + merge в main

## What to do
1. Создать git tag v0.2.0 на develop
2. Merge develop → main
3. Push tags и main

## Commands
  git tag v0.2.0
  git checkout main
  git merge develop --no-ff
  git push origin main --tags
