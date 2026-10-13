"""Day 05 - LLMClient with a custom error, retries, type hints, and structured logging.

The model call is a stub (fake) for now. A real API call replaces it later.
Run:         python client.py
Type-check:  mypy labs/d05-python
"""

import json
import logging
import random
import time
from typing import Literal

# One logger per file, named after the module. Never print().
logger = logging.getLogger(__name__)

# Only these model names are allowed. A typo like "claud" is caught by mypy.
ModelName = Literal["fake-model", "claude", "gpt"]
Outcome = Literal["success", "failed"]


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
        """Send a prompt, retrying on temporary errors. Returns the answer text.

        Writes exactly ONE structured log line per call (success or failed).
        """
        start = time.perf_counter()                             # start the timer
        for attempt in range(1, self.max_retries + 1):
            try:
                answer = self._call_model(prompt)
                self._log_call(prompt, start, "success", attempt)   # 1 line on success
                return answer
            except TimeoutError as e:                           # temporary -> retry
                # Per-attempt detail is DEBUG, so it is hidden at the normal INFO level.
                logger.debug("attempt %d/%d failed: %s", attempt, self.max_retries, e)
                if attempt < self.max_retries:
                    time.sleep(0.1 * 2 ** attempt)              # wait longer each time
        self._log_call(prompt, start, "failed", self.max_retries)  # 1 line on failure
        raise LLMError(f"gave up after {self.max_retries} attempts")

    def _log_call(self, prompt: str, start: float, outcome: Outcome, attempts: int) -> None:
        """Write one structured (JSON) log line for this call."""
        record = {
            "event": "llm_call",
            "model": self.model,
            "prompt_chars": len(prompt),
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "outcome": outcome,
            "attempts": attempts,
        }
        level = logging.INFO if outcome == "success" else logging.ERROR
        logger.log(level, json.dumps(record))

    def _call_model(self, prompt: str) -> str:
        """STUB: pretends to be a model API that sometimes times out."""
        if random.random() < self.fail_rate:
            raise TimeoutError("model timed out")
        return f"[{self.model}] answer to: {prompt}"


if __name__ == "__main__":
    # Configure logging ONCE, at the program's entry point (not inside the library code).
    logging.basicConfig(
        level=logging.INFO,  # set to logging.DEBUG to also see each failed attempt
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # 1) Never fails -> one "success" log line
    LLMClient(fail_rate=0).complete("What is RAG?")

    # 2) Always fails -> one "failed" log line, then LLMError
    try:
        LLMClient(fail_rate=1).complete("What is RAG?")
    except LLMError:
        pass  # already logged above; a real app would return an error response here
