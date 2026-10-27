# Project 1 — LLM Chat Service (in progress, due Day 10)

FastAPI service that calls **Claude** (`claude-haiku-5-5`) behind a typed, validated API contract.

## Endpoints
| Method | Path | What it does |
|---|---|---|
| `POST` | `/chat` | Takes a `ChatRequest`, returns a `ChatResponse` with the model's answer, real token counts and latency |
| `POST` | `/chat/stream` | Same input; streams the answer as Server-Sent Events (`event: token` pieces, then `event: done` with usage) |
| `GET` | `/health` | `{"status": "ok", "version": "0.2.0"}` |

Bad input (empty prompt, prompt > 8,000 chars, `max_tokens` outside 1–4,096, `temperature` outside 0–2) is rejected with **422** before any model call.
`temperature` is validated but not sent: current Claude models reject sampling parameters.

## Structure
```
app/
├── main.py         # creates the app, includes routers, /health
├── schemas.py      # ChatRequest / ChatResponse (Pydantic)
├── api/chat.py     # POST /chat, POST /chat/stream (APIRouter)
└── core/config.py  # settings from .env (pydantic-settings)
prompts/system_v1.txt   # system prompt (versioned, never inline)
.env.example            # copy to .env and add your key
```

## Run
```
python -m pip install "fastapi[standard]" anthropic pydantic-settings
copy .env.example .env      # then put your real ANTHROPIC_API_KEY in .env (never commit it)
python -m fastapi dev app/main.py
```
Open http://127.0.0.1:8000/docs

Stream from the terminal (PowerShell):
```
curl.exe -N -X POST http://127.0.0.1:8000/chat/stream -H "Content-Type: application/json" -d '{\"prompt\": \"Explain RAG in 5 sentences.\"}'
```
