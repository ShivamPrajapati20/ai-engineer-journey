import json
import logging

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

DEFAULT_RETRY_AFTER_SECONDS = "10"

def error_response(status_code: int, code: str, message:str, headers:dict[str, str] | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error":{"code":code,"message":message}},
        headers=headers
    )

def provider_error_to_status(exc: anthropic.APIError) -> tuple[int, str, str]:
    """Map a Claude SDK error to (our HTTP status, error code, safe message)."""
    if isinstance(exc, anthropic.APITimeoutError):
        return 504, "provider_timeout", "The model provider took too long to respond. Please try again."
    if isinstance(exc, anthropic.RateLimitError):
        return 429, "rate_limited", "Too many requests to the model provider. Please retry later."
    if isinstance(exc, anthropic.APIConnectionError):
        return 502, "provider_unreachable", "Could not reach the model provider."
    return 502, "provider_error", "The model provider returned an error. Please try again."


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(anthropic.APIError)
    async def handle_provider_error(request: Request, exc: anthropic.APIError) -> JSONResponse:
        status_code, code, message = provider_error_to_status(exc)
        logger.warning(json.dumps({"event": "provider_error", "path": request.url.path, "code": code,
                                   "provider_status": getattr(exc, "status_code", None)}))
        headers = None
        if isinstance(exc, anthropic.RateLimitError):
            retry_after = exc.response.headers.get("retry-after", DEFAULT_RETRY_AFTER_SECONDS)
            headers = {"Retry-After": retry_after}
        return error_response(status_code, code, message, headers)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0]
        field = ".".join(str(part) for part in first["loc"] if part != "body")
        return error_response(422, "invalid_request", f"{field}: {first['msg']}")

    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, exc: HTTPException) -> JSONResponse:
        code = {401: "unauthorized", 404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
        return error_response(exc.status_code, code, str(exc.detail), getattr(exc, "headers", None))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unexpected error on %s", request.url.path)     # full traceback -> server log only
        return error_response(500, "internal_error", "Something went wrong on our side.")