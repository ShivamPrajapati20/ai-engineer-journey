# Day 03 — Scale Concepts for LLM Endpoints

Source: https://github.com/donnemartin/system-design-primer#performance-vs-scalability

## 1. Performance vs Scalability
**Definition:** A system is *scalable* if adding resources increases performance proportionally. A *performance* problem means it's slow for one user. A *scalability* problem means it's fast for one user but slow under heavy load.

**LLM example:** One chat request that takes 8 s because of a long prompt is a performance problem, which you fix with a smaller model, shorter context or prompt caching. If a single request takes 1 s but 500 concurrent users push it to 20 s, that's a scalability problem, which you fix with more GPU replicas, continuous batching and autoscaling.

## 2. Latency vs Throughput
**Definition:** *Latency* is the time to produce one result. *Throughput* is the number of results per unit of time. The goal is maximum throughput with acceptable latency.

**LLM example:** A streaming chat endpoint is latency-sensitive, so you tune for time-to-first-token and per-token speed with small batches. A batch embedding job over 1M documents is throughput-sensitive, so you tune for documents per second with large batches, and slow individual requests don't matter.

## 3. CAP Theorem
**Definition:** A distributed system can guarantee only two of Consistency (every read gets the latest write or an error), Availability (every request gets a response, possibly stale) and Partition tolerance. Networks fail, so partition tolerance is required, and the real choice is between CP and AP.

**LLM example:** A RAG chatbot whose vector index is replicated across regions is usually AP: during a partition it still answers from a slightly stale index, and new documents show up once replication catches up. A per-user token quota or billing counter should be CP: it's better to return an error than to let a user go over their paid limit because of inconsistent counts.

---

Source: https://github.com/donnemartin/system-design-primer#cache

## 4. Cache Strategy for LLM Responses → **Cache-aside**
**Definition:** In *cache-aside* (lazy loading), the app checks the cache first. On a miss it computes or loads the result, stores it in the cache and returns it. In *write-through*, every write goes to the cache and is written synchronously to the data store.

**Decision:** Use cache-aside, keyed on a hash of (model + model version + system prompt + user prompt + params such as temperature) and stored in Redis with a TTL.

**Why:**
- LLM responses are generated on read, not written ahead of time, so there is no write step for write-through to hook into. Write-through would also cache every response, and most of them are never asked again.
- Only repeated prompts (FAQ-style questions, the same RAG query) earn a cache slot, so memory goes to hot entries and LRU evicts the rest.
- A cache hit skips a 1–10 s generation and its token cost. A miss costs only a few milliseconds more than calling the model directly.
- Staleness is controlled by the TTL and by putting the model/prompt version in the key, so upgrading the model or the prompt invalidates old answers automatically.
- Caveats: only cache deterministic or low-temperature requests, and never share cached answers across users when the prompt contains private context.

## 5. Asynchronism & Message Queues — Jobs to Push to a Queue
**Definition:** The app publishes a slow job to a queue and immediately returns a status. A worker picks the job up and processes it in the background. Back pressure caps the queue size and returns 503 so clients retry with backoff.

**Queued jobs (none of these should block a user request):**
1. **Embedding new or updated documents:** on upload, return "processing", then a worker chunks and embeds the documents in large batches. This is throughput-sensitive work.
2. **Re-indexing the vector store:** when the embedding model or chunking strategy changes, a background job rebuilds the index and then swaps it in, so live search isn't touched until the new index is ready.
3. **Eval runs:** after a prompt or model change, or on a nightly schedule, a worker runs the eval set, using LLM-as-judge where needed, and stores the scores. These are long and expensive jobs that nobody waits on.

Tools: Celery or RQ on Redis/RabbitMQ (Python/FastAPI), or SQS. Make jobs idempotent, because SQS can deliver a message twice.
