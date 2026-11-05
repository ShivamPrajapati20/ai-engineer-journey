"""Shared test setup. Runs BEFORE the tests import the app."""

import os

# Fake keys for tests.
os.environ["ANTHROPIC_API_KEY"] = "test-anthropic-key"
os.environ["SERVICE_API_KEY"] = "test-service-key"
# Safety net: point the real client at a dead address. If any test accidentally makes a
# real call, it fails instead of reaching Claude (and costing money).
os.environ["PROVIDER_BASE_URL"] = "http://127.0.0.1:1"
os.environ["MAX_RETRIES"] = "0"

from types import SimpleNamespace          

import pytest                              
from fastapi.testclient import TestClient  

import app.api.chat as chat_module         
from app.main import app                   

API_KEY = "test-service-key"

class FakeMessages:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []
        self.error: Exception | None = None          # set this to make the "provider" fail

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text="RAG retrieves relevant documents first.")],
            model=kwargs["model"],
            usage=SimpleNamespace(input_tokens=95, output_tokens=7),
        )


@pytest.fixture
def fake_llm(monkeypatch: pytest.MonkeyPatch) -> FakeMessages:
    """Swap the real Claude client for a fake one, for one test only."""
    fake = FakeMessages()
    monkeypatch.setattr(chat_module, "client", SimpleNamespace(messages=fake))
    return fake


@pytest.fixture
def client() -> TestClient:
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def auth() -> dict[str, str]:
    return {"X-API-Key": API_KEY}