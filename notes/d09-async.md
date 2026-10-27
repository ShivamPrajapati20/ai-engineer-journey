# Day 09 — Async, JSON & calling an LLM API

## Task 1 — `asyncio.gather` vs sequential (10 calls to httpbin.org/delay/1)
| Run | Sequential | Concurrent | Speedup |
|---|---:|---:|---:|
| My first run (new client per call in the sequential loop) | 19.35 s | 2.96 s | 6.5× |
| Reference (fixed code: one shared client, local 1-second server) | 10.16 s | 1.05 s | 9.7× |

Total time for concurrent ≈ the slowest single call, not the sum. The first sequential run was inflated because it opened a new HTTPS connection for every call.

## Task 2 — `async def` vs `def` in FastAPI
**Rule**
- `async def` → only when every slow call inside is **awaited** (`await asyncio.sleep`, `httpx.AsyncClient`, `AsyncAnthropic`).
- plain `def` → when calling **blocking** code (`time.sleep`, `requests`, sync SDK clients like `Anthropic()`). FastAPI runs it in a threadpool, so the event loop stays free.

**What happens if you block inside `async def`:** the event loop is a single thread; a blocking call freezes it, so **every request to every endpoint waits** — including `/health`.

| Endpoint (5 requests at once, each waits 1 s) | Time |
|---|---:|
| `async def` + `await asyncio.sleep(1)` | 1.04 s |
| `def` + `time.sleep(1)` (threadpool) | 1.04 s |
| `async def` + `time.sleep(1)` (blocking) | **5.01 s** |
| `/health` while the blocking endpoint runs | **4.91 s** |

When in doubt, use plain `def` — never catastrophic; blocking inside `async def` is.

## Task 3 — First real model call
- `POST /chat` now calls Claude (`claude-haiku-5-5`) with the blocking `Anthropic()` client in a plain `def` endpoint.
- API key in `.env` (git-ignored), loaded by `pydantic-settings`; `.env.example` committed.
- System prompt in `prompts/system_v1.txt`, written with "Be clear and direct": role, answer first, < 150 words, say when unsure.
- Real `input_tokens` / `output_tokens` from `message.usage`; real `latency_ms`.
- Current Claude models reject `temperature` (400), so it stays in `ChatRequest` but is not sent.

## Task 4 — Streaming
- `POST /chat/stream` returns Server-Sent Events: `event: token` for each text piece, then `event: done` with model, token usage and latency.
- `curl.exe -N` shows the tokens arriving progressively, not in one block.
- Streaming doesn't make the model faster — it cuts **time to first token**, which is what users feel.
