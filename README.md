# AI Engineer Journey — 90 Days

A public log of my move from Full Stack Engineer (Java/Spring Boot, Python/FastAPI, Next.js) to AI Engineer, following Chip Huyen's *AI Engineering* and the System Design Primer.

## 90-Day Goal

By **Day 90**, ship **7 evaluated AI projects** (including a production-grade capstone) and land an **AI Engineer** role. Every project must have:
- a measurable eval (accuracy, recall@k, judge score) with before/after numbers,
- latency and cost per request reported,
- an architecture note in `docs/architecture/`.

## Capstone Domain

**SMB finance & accounting automation.** The capstone is an AI assistant for a small retail business that reconciles invoices against ledger exports, flags mismatches and duplicates, and drafts accounting entries for human approval. All money math is done in SQL, the LLM only explains and suggests, and every action is audit-logged.

## Projects

| # | Project | Book chapters | Target day |
|---|---------|---------------|-----------:|
| 1 | Prompt lab + eval harness | Ch 3–5 | 7 |
| 2 | RAG with an eval set: recall@k, hybrid search + reranking | Ch 6 | 18 |
| 3 | Tool-using agent with failure-mode tests | Ch 6 | 30 |
| 4 | Eval pipeline: LLM-as-judge running in CI | Ch 3–4 | 42 |
| 5 | LoRA finetune + dataset engineering | Ch 7–8 | 55 |
| 6 | Inference: serving, caching, queues, cost dashboard | Ch 9 | 68 |
| 7 | **Capstone:** production system with guardrails, model router, monitoring | Ch 10 | 90 |

## Repo Layout

```
notes/               daily reading notes (dNN-topic.md)
labs/                small throwaway experiments
projects/            the 7 projects, one folder each
evals/               eval sets, judge prompts, results
docs/architecture/   architecture diagrams and decision records
```

## Log

- **Day 01:** Mapped the book's 10 chapters to topics → [`notes/d01-map.md`](notes/d01-map.md)
- **Day 03:** Scale concepts for LLM endpoints (performance vs scalability, latency vs throughput, CAP, caching, queues) → [`notes/d03-scale.md`](notes/d03-scale.md)
