# lan-test

Test bed for the **langgraph-lab** pipeline.

FastAPI monitoring service that tracks the health of all local AI services
and logs request history through the langgraph proxy.

## Services monitored

| Service       | URL                          |
|---------------|------------------------------|
| langgraph proxy | http://localhost:1236       |
| LM Studio     | http://localhost:1234        |
| stack-rag     | http://localhost:8000        |

## Install

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

```powershell
python -m lan_test.api       # API server on :8080
lan-test status              # CLI health check
lan-test history             # show request history
```

## Version

`0.1.0` — see [CHANGELOG](CHANGELOG.md)
