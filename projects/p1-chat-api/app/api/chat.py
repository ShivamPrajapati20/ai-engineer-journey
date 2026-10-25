import time

from fastapi import APIRouter

from app.core.config import settings
from app.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    start = time.perf_counter()
    answer = f"(hardcoded) You said: {request.prompt}"   # stub - real model on Day 10
    return ChatResponse(
        answer=answer,
        model=settings.model_name,
        input_tokens=len(request.prompt.split()),
        output_tokens=len(answer.split()),
        latency_ms=int((time.perf_counter() - start) * 1000),
    )