"""Day 05 - LLMClient with a custom error, retries, and type hints.

The model call is a stub (fake) for now. A real API call replaces it later.
Run:         python client.py
Type-check:  mypy labs/d05-python
"""

import random
import time
from typing import Literal

# Only these model names are allowed. A typo like "claud" is caught by mypy.
ModelName = Literal["fake-model", "claude", "gpt"]


class LLMError(Exception):
    """Raised when the model call fails and we have given up."""


class LLMClient:
    def __init__(
        self,
        model: ModelName = "fake-model",
        max_retries: int = 3,
        fail_rate: float = 0.5,
    ) -> None:
        self.model = model              # which model to call
        self.max_retries = max_retries  # how many tries before giving up
        self.fail_rate = fail_rate      # stub only: 0 = never fails, 1 = always fails

    def complete(self, prompt: str) -> str:
        """Send a prompt, retrying on temporary errors. Returns the answer text."""
        for attempt in range(1, self.max_retries + 1):
            try:
                return self._call_model(prompt)                 # success -> done
            except TimeoutError as e:                           # temporary -> retry
                print(f"attempt {attempt}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(0.1 * 2 ** attempt)              # wait longer each time
        raise LLMError(f"gave up after {self.max_retries} attempts")

    def _call_model(self, prompt: str) -> str:
        """STUB: pretends to be a model API that sometimes times out."""
        if random.random() < self.fail_rate:
            raise TimeoutError("model timed out")
        return f"[{self.model}] answer to: {prompt}"


if __name__ == "__main__":
    # 1) Never fails -> answer on the first try
    print(LLMClient(fail_rate=0).complete("What is RAG?"))

    # 2) Always fails -> 3 attempts, then LLMError  (this is the "done when" proof)
    try:
        LLMClient(fail_rate=1).complete("What is RAG?")
    except LLMError as e:
        print("LLMError:", e)
