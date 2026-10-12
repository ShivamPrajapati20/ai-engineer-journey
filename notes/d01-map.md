# Day 01 — Book Map: *AI Engineering* (Chip Huyen)

Source: https://github.com/chiphuyen/aie-book/blob/main/ToC.md

## Topic → Chapter

| Topic               | Main chapter | Also touched in |
|---------------------|:------------:|-----------------|
| Evaluation          | **3, 4**     | 6 (Agent Failure Modes and Evaluation), 1 (Use Case Evaluation) |
| Prompt engineering  | **5**        | 2 (Structured Outputs) |
| RAG                 | **6**        | 7 (Finetuning and RAG), 10 (Step 1: Enhance Context) |
| Agents              | **6**        | 10 (Step 5: Add Agent Patterns) |
| Finetuning          | **7**        | 2 (Post-Training: SFT, Preference Finetuning) |
| Dataset engineering | **8**        | — |
| Inference cost      | **9**        | 4 (Cost and Latency, Build vs Buy), 7 (Quantization), 10 (Router/Gateway, Caches) |
| Architecture        | **10**       | 2 (Model Architecture = transformer internals, not system architecture), 1 (The AI Engineering Stack) |

## Chapters and sub-headings

1. **Introduction to Building AI Applications with Foundation Models** (p.1)
   - The Rise of AI Engineering — LMs → LLMs → foundation models → AI engineering
   - Foundation Model Use Cases — coding, image/video, writing, education, bots, info aggregation, data organization, workflow automation
   - Planning AI Applications — use case evaluation, expectations, milestones, maintenance
   - The AI Engineering Stack — three layers; AI eng vs ML eng; AI eng vs full-stack eng
2. **Understanding Foundation Models** (p.49)
   - Training Data — multilingual, domain-specific models
   - Modeling — model architecture, model size
   - Post-Training — supervised finetuning, preference finetuning
   - Sampling — fundamentals, strategies, test-time compute, structured outputs, probabilistic nature of AI
3. **Evaluation Methodology** (p.113)
   - Challenges of evaluating foundation models
   - Language modeling metrics — entropy, cross entropy, BPC/BPB, perplexity
   - Exact Evaluation — functional correctness, similarity to reference data, intro to embeddings
   - AI as a Judge — why, how, limitations, which models can judge
   - Ranking Models with Comparative Evaluation — challenges, future
4. **Evaluate AI Systems** (p.159)
   - Evaluation Criteria — domain-specific, generation, instruction-following, cost & latency
   - Model Selection — workflow, build vs buy, public benchmarks
   - Design Your Evaluation Pipeline — evaluate all components, guidelines, methods & data
5. **Prompt Engineering** (p.211)
   - Introduction to Prompting — zero/few-shot ICL, system vs user prompt, context length
   - Best Practices — clear instructions, context, subtasks, time to think, iterate, tools, versioning
   - Defensive Prompt Engineering — reverse prompt engineering, jailbreaks & prompt injection, info extraction, defenses
6. **RAG and Agents** (p.253)
   - RAG — architecture, retrieval algorithms, retrieval optimization, RAG beyond texts
   - Agents — overview, tools, planning, failure modes & evaluation
   - Memory
7. **Finetuning** (p.307)
   - Finetuning Overview
   - When to Finetune — reasons to / not to, finetuning vs RAG
   - Memory Bottlenecks — backprop & trainable params, memory math, numerical representations, quantization
   - Finetuning Techniques — PEFT, model merging & multi-task, tactics
8. **Dataset Engineering** (p.363)
   - Data Curation — quality, coverage, quantity, acquisition & annotation
   - Data Augmentation and Synthesis — why, traditional, AI-powered, model distillation
   - Data Processing — inspect, deduplicate, clean/filter, format
9. **Inference Optimization** (p.405)
   - Understanding Inference Optimization — overview, performance metrics, AI accelerators
   - Inference Optimization — model optimization, inference service optimization
10. **AI Engineering Architecture and User Feedback** (p.449)
    - AI Engineering Architecture — enhance context, guardrails, router & gateway, caches, agent patterns, monitoring & observability, pipeline orchestration
    - User Feedback — extracting conversational feedback, feedback design, limitations
