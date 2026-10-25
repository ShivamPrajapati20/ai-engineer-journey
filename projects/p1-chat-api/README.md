# Project 1 — LLM Chat Service (in progress, due Day 10)

FastAPI service with a typed API contract. The model call is a **stub** for now; a real model replaces it on Day 10.

## Endpoints
| Method | Path | What it does |
|---|---|---|
| `POST` | `/chat` | Takes a `ChatRequest`, returns a `ChatResponse` (hardcoded answer for now) |
| `GET` | `/health` | `{"status": "ok", "version": "0.1.0"}` |

Bad input (empty prompt, prompt > 8,000 chars, `max_tokens` outside 1–4,096, `temperature` outside 0–2) is rejected with **422** before any model call.

## Structure
```
app/
├── main.py         # creates the app, includes routers, /health
├── schemas.py      # ChatRequest / ChatResponse (Pydantic)
├── api/chat.py     # POST /chat (APIRouter)
└── core/config.py  # settings: name, version, model
```

## Run
```
pip install "fastapi[standard]"
python -m fastapi dev app/main.py
```
Open http://127.0.0.1:8000/docs
