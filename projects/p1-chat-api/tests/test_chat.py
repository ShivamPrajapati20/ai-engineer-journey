"""Tests for POST /chat. The model provider is mocked: no network, no cost."""

import anthropic
import httpx
from fastapi.testclient import TestClient

from tests.conftest import FakeMessages

FAKE_REQUEST = httpx.Request("POST", "https://api.anthropic.com/v1/messages")


# ---------- 1. Happy path ----------

def test_chat_happy_path(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    response = client.post("/chat", json={"prompt": "  What is RAG?  "}, headers=auth)

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "RAG retrieves relevant documents first."
    assert body["input_tokens"] == 95
    assert body["output_tokens"] == 7
    assert body["latency_ms"] >= 0

    assert len(fake_llm.calls) == 1                                       # called exactly once
    assert fake_llm.calls[0]["messages"] == [{"role": "user", "content": "What is RAG?"}]   # prompt was stripped
    assert "temperature" not in fake_llm.calls[0]                          # Claude rejects it


# ---------- 2. Missing / wrong key ----------

def test_missing_api_key_returns_401(client: TestClient, fake_llm: FakeMessages) -> None:
    response = client.post("/chat", json={"prompt": "hi"})

    assert response.status_code == 401
    assert response.json() == {"error": {"code": "unauthorized", "message": "Invalid or missing API key"}}
    assert fake_llm.calls == []                                            # model never called


def test_wrong_api_key_returns_401(client: TestClient, fake_llm: FakeMessages) -> None:
    response = client.post("/chat", json={"prompt": "hi"}, headers={"X-API-Key": "wrong"})

    assert response.status_code == 401
    assert fake_llm.calls == []


# ---------- 3. Oversized prompt ----------

def test_oversized_prompt_returns_422(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    response = client.post("/chat", json={"prompt": "x" * 9000}, headers=auth)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    assert "8000" in response.json()["error"]["message"]
    assert fake_llm.calls == []


# ---------- 4. Bad temperature ----------

def test_bad_temperature_returns_422(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    response = client.post("/chat", json={"prompt": "hi", "temperature": 3}, headers=auth)

    assert response.status_code == 422
    assert "temperature" in response.json()["error"]["message"]
    assert fake_llm.calls == []


# ---------- 5-7. Provider failures (Task 3) ----------

def test_provider_timeout_returns_504(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    fake_llm.error = anthropic.APITimeoutError(request=FAKE_REQUEST)

    response = client.post("/chat", json={"prompt": "hi"}, headers=auth)

    assert response.status_code == 504
    assert response.json()["error"]["code"] == "provider_timeout"


def test_rate_limit_returns_429_with_retry_after(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    provider_response = httpx.Response(429, request=FAKE_REQUEST, headers={"retry-after": "20"})
    fake_llm.error = anthropic.RateLimitError("slow down", response=provider_response, body=None)

    response = client.post("/chat", json={"prompt": "hi"}, headers=auth)

    assert response.status_code == 429
    assert response.headers["retry-after"] == "20"
    assert response.json()["error"]["code"] == "rate_limited"


def test_provider_5xx_returns_502_without_stack_trace(client: TestClient, auth: dict[str, str], fake_llm: FakeMessages) -> None:
    provider_response = httpx.Response(500, request=FAKE_REQUEST)
    fake_llm.error = anthropic.InternalServerError("boom", response=provider_response, body=None)

    response = client.post("/chat", json={"prompt": "hi"}, headers=auth)

    assert response.status_code == 502
    assert response.json() == {"error": {"code": "provider_error",
                                         "message": "The model provider returned an error. Please try again."}}
    assert "Traceback" not in response.text


def test_health_is_open(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"