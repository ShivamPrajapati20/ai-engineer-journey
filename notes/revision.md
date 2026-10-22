# Revision Notes — AI Engineer Journey

One file to review everything learned so far. Updated after every task.
**How to use:** skim the Quick Review (5 min). If a line feels fuzzy, jump to that day's section.

---

## ⚡ Quick Review — one line per idea

| Day | Remember this |
|---|---|
| 01 | Evaluation = Ch 3–4, Prompting = Ch 5, RAG + Agents = Ch 6, Finetuning = Ch 7, Data = Ch 8, Inference cost = Ch 9, Architecture = Ch 10. |
| 03 | Performance = slow for **one** user. Scalability = fast for one, slow under **load**. |
| 03 | Aim for **max throughput at acceptable latency**. Streaming chat = latency-sensitive; batch embedding = throughput-sensitive. |
| 03 | CAP: networks fail, so choose **CP** (correct or error) or **AP** (always answer, maybe stale). |
| 03 | Cache LLM responses with **cache-aside** + TTL; key includes model + prompt version. |
| 03 | Slow work (embedding, re-indexing, evals) goes on a **queue**; make jobs safe to run twice. |
| 05 | A **class** bundles data + functions; `self` = Java's `this`. |
| 05 | `try/except` what you can handle; `raise` your own clear error when you can't. |
| 05 | Retry only **temporary** errors (timeouts), never bad prompts or bad keys. |
| 05 | Type hints are labels Python ignores and **mypy checks**. `name: type` only where you **define**, never where you **call**. |
| 05 | `print` is for you while coding; **`logging`** is for the running system. One structured line per call. |
| 06 | An embedding table is a 2D array: **rows = chunks, columns = dimensions**. |
| 06 | The axis you name **disappears**: `(1000, 384).mean(axis=1)` → `(1000,)`. |
| 06 | **Normalize** = same direction, length 1. **Broadcasting** = one instruction for every row; numbers must stand as a **column** (`keepdims=True`). |
| 06 | **Search = one matrix multiply**: `chunks @ question`. ~500× faster than a Python loop. |
| 07 | `isna()` only finds real `NaN`, not `" "` or `"N/A"`. A number column showing as **text** = hidden bad values. |
| 07 | Before fixing missing data, find out **why** it's missing. |
| 07 | `groupby` = split → summarize → combine (SQL `GROUP BY`). For a rate, average a 1/0 column and **always show the count**. |
| 07 | Commit **code and conclusions**, not data. |
| 08 | A **Pydantic model is an enforced contract**: bad input is rejected before it reaches your code or costs money. |
| 08 | `Field` limits for simple rules (`min_length`, `ge`, `le`); `@field_validator` for custom ones — and always **`return` the value**. |
| 08 | One `try` per test case; catch **`pydantic.ValidationError`**, and check imports your editor adds. |
| 08 | Model as parameter type → FastAPI validates **input** (bad = 422, client's fault). `response_model` → validates **output** (broken = 500, your fault). |
| 08 | Run tools with **`python -m ...`** (`python -m pip`, `python -m fastapi dev`) so they use the Python you actually have. |

---

## Day 01 — Book map (*AI Engineering*, Chip Huyen)

| Topic | Chapter |
|---|---|
| Evaluation | 3 (methodology), 4 (evaluating AI systems) |
| Prompt engineering | 5 |
| RAG | 6 |
| Agents | 6 |
| Finetuning | 7 |
| Dataset engineering | 8 |
| Inference cost | 9 (also cost in Ch 4, quantization in Ch 7, router/caches in Ch 10) |
| Architecture | 10 |

**Trap:** "Model Architecture" in Ch 2 = how the transformer is built. "AI Engineering Architecture" in Ch 10 = how the whole *application* is built.

📄 Details: [`d01-map.md`](d01-map.md)

---

## Day 03 — Scale concepts for LLM endpoints

**Performance vs scalability**
- Performance problem: one request is slow → smaller model, shorter prompt, caching.
- Scalability problem: fast alone, slow under heavy traffic → more GPU replicas, batching, autoscaling.

**Latency vs throughput**
- Latency = time for **one** result. Throughput = results **per second**.
- Streaming chat → tune for time-to-first-token (latency).
- Batch embedding of 1M docs → tune for docs/second with big batches (throughput).

**CAP theorem**
- Consistency, Availability, Partition tolerance — pick 2. Partitions always happen, so the real choice is **CP vs AP**.
- RAG index across regions → **AP** (answer from slightly stale index).
- Billing / token quota → **CP** (better an error than letting someone overspend).

**Cache strategy for LLM responses → cache-aside**
- Check cache → miss → call model → store with TTL → return.
- Key = hash(model + version + system prompt + user prompt + params).
- Why not write-through: responses are created on read; most are never asked again.
- Only cache low-temperature, non-private answers.

**Queues**
- Publish slow job → return "processing" → worker does it in background.
- Queue these: embedding new documents, re-indexing the vector store, eval runs.
- **Back pressure:** cap the queue; return 503 so clients retry with backoff.
- SQS can deliver twice → jobs must be **idempotent** (safe to run twice).

📄 Details: [`d03-scale.md`](d03-scale.md)

---

## Day 04 — Repo setup

- Repo: `ai-engineer-journey` → `notes/`, `labs/`, `projects/`, `evals/`, `prompts/`, `docs/architecture/`.
- `notes/` = `.md` write-ups only. Code goes in `labs/` or `projects/`.

---

## Day 05 — Python essentials for AI

### Classes and exceptions
```python
class LLMError(Exception):          # your own named error (Java: extends RuntimeException)
    pass

class LLMClient:
    def __init__(self, model: str, max_retries: int = 3) -> None:   # constructor
        self.model = model                                            # self = this
```
- `try:` risky code → `except TimeoutError:` handle it → `raise LLMError(...)` when you give up.
- **Retry loop:** `for attempt in range(1, max_retries + 1)`, wait longer each time (`0.1 * 2 ** attempt`).
- **Only retry temporary errors** (timeout, server busy). Bad prompt / bad key fails the same way every time.
- **Stub** = a fake function that pretends to be the model (sometimes fails on purpose) so you can test logic without paying.

### Type hints + mypy
| Hint | Meaning | Java-ish |
|---|---|---|
| `str`, `int`, `float`, `bool`, `list[str]`, `dict[str, float]` | basic types | same |
| `Optional[str]` / `str \| None` | may be `None` → mypy forces a check | nullable |
| `Literal["a", "b"]` | only these exact values | mini `enum` |
| `TypedDict` | dict with fixed keys + types | DTO |
| `Protocol` | "anything with these methods" | `interface` without `implements` |
| `-> None` | function returns nothing (`__init__` always) | `void` |

- Run: `mypy labs/d05-python` (add `--strict` to also flag missing hints).
- **Trap:** `self._call_model(prompt: str)` ❌ → `self._call_model(prompt)` ✅. Hints go in the **definition**, not the **call**.
- **Trap:** using `Literal` without `from typing import Literal` → `NameError`.

### Logging
```python
logger = logging.getLogger(__name__)                 # one per file, top of file
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")  # ONCE, in __main__
logger.info(json.dumps({"prompt_chars": 12, "latency_ms": 231, "outcome": "success"}))
```
- Levels: DEBUG (detail) < INFO (normal) < WARNING < ERROR.
- **Structured** = fixed fields as JSON, so tools can search/average them.
- **One line per call** (= one per user request). Per-attempt detail at DEBUG.
- `time.perf_counter()` = precise stopwatch: read before and after, subtract.
- Library code never calls `basicConfig`; the program that runs it does.

📄 Code: [`labs/d05-python/client.py`](../labs/d05-python/client.py)

---

## Day 06 — NumPy

### Fundamentals
| Code | Result | Meaning |
|---|---|---|
| `np.array([1, 2, 3])` | array | list → array, **one type** for all |
| `a.shape` | `(1000, 384)` | (rows, columns) — rows first |
| `a.dtype` | `float32` | type of every number |
| `a[1:4]` | items 1, 2, 3 | end not included |
| `b[1, 3]` | one value | row 1, column 3 |
| `b[:, 0]` | first column | `:` = all rows |
| `a.reshape(2000, 192)` | new grid | rows × cols must equal total |
| `a.mean(axis=1)` | `(1000,)` | one average **per row** |
| `rng = np.random.default_rng(42)` | generator | same seed → same numbers |

- **float32** = 4 bytes/number, half of float64. Embeddings use it. (1000 × 384 × 4 = ~1.5 MB.)
- **Trap:** `reshape` returns a **new** array; the original is unchanged → `d = c.reshape(2, 3)`.
- **Trap:** `reshape(4, 2)` on 6 numbers → error (4 × 2 ≠ 6).

### Broadcasting + normalizing
- **Normalize:** divide each row by its own length → every row has length 1, same direction.
  (3, 4) and (6, 8) both become (0.6, 0.8) — same meaning, different size.
- **Broadcasting rule:** compare shapes **from the right**; each pair must be **equal or 1**. A 1 gets stretched.
```python
x = x / np.linalg.norm(x, axis=1, keepdims=True)    # (1000, 384) / (1000, 1)
np.allclose(np.linalg.norm(x, axis=1), 1, atol=1e-6) # True
```
- **Trap:** without `keepdims=True` the lengths are shape `(1000,)` (a row) → shape error. `keepdims` makes it `(1000, 1)` (a column).
- float32 gives 0.9999999, not exactly 1 → always compare with a tolerance (`allclose`).
- Indexing: `x[[0, 5, 9]]` picks rows (top-k results); `x[x > 0.9]` keeps matching values (mask).

### Vectorization
- **Cosine similarity** = do two arrows point the same way? 1 = same, 0 = unrelated, −1 = opposite.
- For length-1 vectors, cosine = **dot product** = multiply matching numbers and add.
- `scores = x @ q` → `(1000, 384) @ (384,)` = `(1000,)`, one score per chunk. `scores.argmax()` = best match.
- Pure Python loop ≈ 0.1 s; `x @ q` ≈ 0.0002 s → **~500× faster**.
- **Trap:** a loop calling `np.dot(q, row)` is only ~6× slower — the inner math is still NumPy. The real cost is pure-Python loops.

### Embeddings
- **Embedding** = text → fixed list of numbers capturing meaning. Similar meaning → arrows point the same way.
- **384** = embedding size of the model (e.g. `all-MiniLM-L6-v2`). Each dimension is a *learned* feature, not a human label. Other models: 768, 1536, 3072.
- A **vector database** stores exactly this matrix (float32) + each row's text and metadata. Search = embed question → `matrix @ question` → top scores.

---

## Day 07 — Pandas

### First look at any dataset
| Code | Question it answers |
|---|---|
| `df = pd.read_csv("file.csv")` | load a table |
| `df.head()` | first 5 rows — always look first |
| `df.shape` | rows, columns → `(7043, 21)` |
| `df.dtypes` | type per column (`object`/`str` = text) |
| `df.describe()` | stats for **number** columns only |
| `df.isna().sum()` | real missing values per column |
| `df[df["age"] > 30]` | filter rows |
| `df["city"].value_counts()` | count each unique value |

- DataFrame = table with named columns (Excel in Python). Series = one column.
- A missing value turns an int column into **float64** (NaN is a float).

### Cleaning
```python
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
```
- `.astype(float)` is strict → crashes on `" "`.
- `pd.to_numeric(errors="coerce")` → bad values become NaN, so `isna()` can see them.
- `dropna()` deletes rows; `fillna(value)` fills them.
- **Telco case:** 11 blanks, all tenure = 0 (not billed yet) → true value is **0**. Fill 0 > drop > mean (mean would invent ~$2,283).

### Groupby
```python
df["churned"] = (df["Churn"] == "Yes").astype(int)            # Yes/No → 1/0
df.groupby("Contract")["churned"].agg(["mean", "count"]).sort_values("mean", ascending=False)
df["bucket"] = pd.cut(df["tenure"], bins=[-1, 12, 24, 48, 72], labels=["0-12", "13-24", "25-48", "49+"])
```
- Average of a 1/0 column **=** the rate.
- `pd.cut` bins include the **right** edge. First edge **−1**, not 0, or tenure-0 rows become NaN.
- `observed=True` in groupby → only buckets that have data (no warning).
- **Telco results:** baseline 26.5%; first 12 months **47.4%**; month-to-month 42.7%; fiber 41.9%; month-to-month + first year **51.4%**.
- Groupby shows **correlation, not causation**. A hypothesis must be testable.

### Git
- `.gitignore` keeps data and caches out: `labs/*/data/`, `__pycache__/`, `.mypy_cache/`, `.venv/`, `.env`.
- `git status` → check the CSV isn't listed → `git add <specific files>` → `git commit -m "..."` → `git push`.

📄 Note: [`d07-eda.md`](d07-eda.md) · Code: [`labs/d07-pandas/explore.py`](../labs/d07-pandas/explore.py)

---

## Day 08 — FastAPI + Pydantic

### Task 1 — Pydantic models as the API contract
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str                 # required (no default)
    max_tokens: int = 512       # optional (has default)
    temperature: float = 0.7

ChatRequest.model_json_schema()   # machine-readable contract → powers FastAPI /docs
request.model_dump()              # model → dict
request.model_dump_json()         # model → JSON string
```
- Pydantic = DTO + Jackson + Bean Validation in one. FastAPI is built on it.
- **Converts** sensible input (`"30"` → `30`, `1` → `1.0`); **rejects** bad input with `ValidationError` (FastAPI turns it into **422**).
- `max_tokens` caps cost (you pay per token). `temperature`: 0 = focused, higher = creative.
- `"required"` in the schema lists only fields **without defaults**.
- Put test code under `if __name__ == "__main__":` so it doesn't run when the file is **imported**.
- Style: **CapitalCase = classes**, **snake_case = variables** (`request`, not `CRequest`).
- Call schema on the **class**: `ChatRequest.model_json_schema()`.
- **Trap:** never name a file `pydantic.py` (or `numpy.py`, `json.py`) — it hides the real library.

### Task 2 — Validation that rejects bad input before it costs money
```python
from pydantic import BaseModel, Field, ValidationError, field_validator

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    max_tokens: int = Field(default=512, ge=1, le=4096)      # default goes INSIDE Field
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    @field_validator("prompt")
    @classmethod                       # required; first param is cls, not self
    def strip_and_check(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("prompt must not be empty or only spaces")
        return v                       # what you return is what gets stored
```
| Word | Meaning | For |
|---|---|---|
| `min_length` / `max_length` | shortest / longest text | strings |
| `ge` / `le` | ≥ / ≤ (greater/less than or equal) | numbers |
| `gt` / `lt` | > / < (strict) | numbers |

- Task 1 checks the **type**; Task 2 checks the **value** (bouncer with a checklist).
- Why it matters: long prompts, huge `max_tokens`, invalid `temperature`, blank prompts all **cost money** or fail at the model — reject them free, at the door.
- `"     "` passes `min_length=1` (5 chars) → only the **validator** (strip first) catches it. That's why you need both.
- Limits show up in the JSON schema as `minimum` / `maximum` / `maxLength` → visible in `/docs`.
- `ValidationError` in Python **=** HTTP **422** once the model is used in a FastAPI endpoint; your endpoint code never runs.
- `ChatRequest(**data)` unpacks a dict into named arguments (`**{"prompt": "hi"}` = `prompt="hi"`).
- `e.errors()` → list of `{"loc": ("prompt",), "msg": "..."}` — use it to print *which field* and *why*.
- Error messages should say exactly what to fix (not "not proper value").

### Task 3 — Wire it into a real endpoint (`POST /chat`)
```python
from fastapi import FastAPI
from schemas import ChatRequest, ChatResponse

app = FastAPI(title="LLM Chat Service")

@app.post("/chat", response_model=ChatResponse)     # = @PostMapping("/chat")
def chat(request: ChatRequest) -> ChatResponse:      # type hint = @RequestBody + @Valid
    answer = f"(hardcoded) You said: {request.prompt}"   # stub — real model on Day 10
    return ChatResponse(answer=answer, model="stub-model",
                        input_tokens=..., output_tokens=..., latency_ms=...)
```
```
Client ─JSON─▶ [check ChatRequest] ─▶ chat() ─▶ [check ChatResponse] ─JSON─▶ Client
                 ❌ bad input → 422                  ❌ your bug → 500
```
- Restaurant: `ChatRequest` = order form checked by the waiter; your function = kitchen (only sees valid orders); `ChatResponse` = plate standard checked before it leaves.
- Build the **pipe** first with a hardcoded answer (free), swap in the real model later — same idea as Day 5's stub.
- `/docs` (Swagger UI) is generated from your models: **Schemas** shows `ChatRequest`, `ChatResponse`, plus `HTTPValidationError` (the 422 format). "Try it out" → Execute to test.
- 422 error body: `{"detail": [{"loc": ["body", "prompt"], "msg": "String should have at most 8000 characters", ...}]}`.
- Returning a dict that misses fields with `response_model` set → **500**; FastAPI won't send a broken response.
- Run: `python -m fastapi dev main.py` → http://127.0.0.1:8000/docs. Auto-reloads on save; stop with Ctrl+C.
  Alternative: `python -m uvicorn main:app --reload` (`main:app` = file `main.py`, variable `app`).
- Call it from Python: `httpx.post("http://127.0.0.1:8000/chat", json={"prompt": "x" * 9000}).status_code` → 422.
- Import trap: `from schemas import ...` needs the file to be named exactly **`schemas.py`**.

**Fixing "Fatal error in launcher … C:\\Python310\\python.exe … cannot find the file"**
- `fastapi.exe` / `pip.exe` are small launchers tied to the Python that installed them. Old Python removed → launcher is dead.
- Fix: `python --version` → `python -m pip install "fastapi[standard]"` → `python -m fastapi dev main.py`.
- Lasting fix: a **venv** per repo: `python -m venv .venv` → `.venv\\Scripts\\activate` → install inside it. Prompt shows `(.venv)`. Activate in each new terminal.

---

## Traps to avoid (several I actually hit)

- Type hint inside a function **call**: `f(prompt: str)` → syntax error.
- Forgot `from typing import Literal` → `NameError`.
- Expected `c.reshape(...)` to change `c` → save the result.
- Divided by row lengths without `keepdims=True` → shape error.
- Trusted `isna() = 0` → `TotalCharges` had 11 hidden blanks.
- Printed only one schema when the task asked for both → read the "Done when" line twice.
- Practice code saved in `notes/` → code belongs in `labs/`.
- Editor auto-imported `from xml.dom import ValidationErr` → `except` never caught Pydantic's error. Use `from pydantic import ValidationError`.
- Put 4 tests in one `try` → first failure skipped the other 3. One `try` per test.
- `except ...: raise Exception` → threw away the useful message. Print `e.errors()` instead.
- Named the file `schema.py` but imported `schemas` → keep file names exactly as the task says.
- `fastapi dev` failed with "Fatal error in launcher" (old Python 3.10 launcher) → use `python -m fastapi dev main.py`.
