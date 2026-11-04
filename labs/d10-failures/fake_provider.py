"""A fake model provider that fails ON PURPOSE, so you can test your error handling.

Run:   python -m uvicorn fake_provider:app --port 9000
Pick the failure with FAIL_MODE: timeout | 429 | 500 | ok
"""

import os
import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
MODE = os.environ.get("FAIL_MODE", "500")

@app.post("/v1/messages")
def messages() -> JSONResponse:
    if MODE == "timeout":
        time.sleep(30)                                   # longer than our timeout -> we should return 504
    if MODE == "429":
        return JSONResponse(status_code=429, headers={"retry-after": "20"},
                            content={"type": "error", "error": {"type": "rate_limit_error", "message": "slow down"}})
    if MODE == "500":
        return JSONResponse(status_code=500,
                            content={"type": "error", "error": {"type": "api_error", "message": "internal boom"}})
    return JSONResponse(content={
        "id": "msg_fake", "type": "message", "role": "assistant", "model": "claude-haiku-5-5",
        "content": [{"type": "text", "text": "fake answer"}], "stop_reason": "end_turn",
        "stop_sequence": None, "usage": {"input_tokens": 10, "output_tokens": 2},
    })