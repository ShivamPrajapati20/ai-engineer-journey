# AI Engineer Journey — 90 Days

A build-first, 90-day plan to go from Full Stack Engineer (Java/Spring Boot, Python/FastAPI, Next.js) to AI Engineer, from an SE-foundation refresh to a deployed production AI system. Every day's work lands in this repo.

## 90-Day Goal

By **Day 90**, ship **7 projects** that each pass their acceptance bar with real, dated numbers in their README. The last one is a **deployed, production-grade AI system**. Then pass AI Engineer interviews and land an **AI Engineer** role.

## Capstone Domain

**SMB finance & accounting automation.** The capstone is an assistant for a small retail business that answers questions over its invoices and ledger exports, reconciles them, flags mismatches and duplicates, and drafts entries for human approval. All money math is done in SQL, the LLM only explains and suggests, and every action is audit-logged.

Full scope (user, question, corpus, quality bar): [`docs/capstone-brief.md`](docs/capstone-brief.md) *(Day 4 task — to write)*

## The 7 Projects

| # | Project | Day | Folder |
|---|---------|----:|--------|
| 1 | LLM Chat Service | 10 | `projects/p1-chat-api` |
| 2 | Chat With Your Documents | 44 | `projects/p2-doc-chat` |
| 3 | Enterprise Knowledge Assistant | 46 | `projects/p3-knowledge-assistant` |
| 4 | Research Agent | 57 | `projects/p4-research-agent` |
| 5 | Multi-Agent Research & Report | 63 | `projects/p5-multi-agent` |
| 6 | Document Intelligence Platform | 74 | `projects/p6-doc-intelligence` |
| 7 | **Production AI System (Capstone)** | 90 | `projects/p7-capstone` |

A project is done when it passes its "Done when" bar, not when it merely runs.

## Repo Layout

```
notes/               dNN-topic.md — daily write-ups
labs/                dNN-topic/ — throwaway code for a day's exercise
projects/            p1-chat-api … p7-capstone — the 7 builds, each with its own README
evals/               rag_testset.jsonl, test_llm.py, baselines.md, injection_tests.md
prompts/             versioned prompts (system_v1.txt, …) — never inline a prompt in code
docs/                stack.md, eval-policy.md, ship-checklist.md, security.md, cost-report.md, capstone-brief.md
docs/architecture/   Mermaid diagrams: current-state, target-state, p5-graph, serving, mcp
```

## Log

- **Day 01:** Mapped the book's 10 chapters to topics → [`notes/d01-map.md`](notes/d01-map.md)
- **Day 03:** Scale concepts for LLM endpoints (performance vs scalability, latency vs throughput, CAP, caching, queues) → [`notes/d03-scale.md`](notes/d03-scale.md)
- **Day 04:** Created this repo
- **Day 05:** `LLMClient` with custom error, retries, type hints (mypy --strict clean) and structured JSON logging → [`labs/d05-python/client.py`](labs/d05-python/client.py)
- **Day 07:** Pandas EDA on Telco churn — cleaned `TotalCharges`, churn by segment, hypothesis → [`notes/d07-eda.md`](notes/d07-eda.md)
