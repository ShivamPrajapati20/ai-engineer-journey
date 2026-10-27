import time, json
from pathlib import Path

from anthropic import Anthropic
from fastapi import APIRouter

from app.core.config import settings
from app.schemas import ChatRequest, ChatResponse

from collections.abc import Iterator
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["chat"])

client = Anthropic(api_key=settings.anthropic_api_key)
SYSTEM_PROMPT = Path(settings.system_prompt_path).read_text(encoding="utf-8")

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    start = time.perf_counter()

    message = client.messages.create(
        model=settings.model_name,
        max_tokens=request.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role":"user","content":request.prompt}]
    )

    answer = "".join(block.text for block in message.content if block.type == "text")
    
    return ChatResponse(
        answer=answer,
        model=message.model,
        input_tokens=message.usage.input_tokens,
        output_tokens=message.usage.output_tokens,
        latency_ms=int((time.perf_counter() - start) * 1000),
    )

def sse(event:str, data:dict[str,object]) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"

@router.post("/chat/stream")
def chat_stream(request: ChatRequest) -> StreamingResponse:
    def event_generator() -> Iterator[str]:                       # plain generator: FastAPI runs it in a threadpool
        start = time.perf_counter()
        with client.messages.stream(
            model=settings.model_name,
            max_tokens=request.max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": request.prompt}],
        ) as stream:
            for text in stream.text_stream:                       # each small piece of text as it is generated
                yield sse("token", {"text": text})
            final = stream.get_final_message()                    # full message, incl. real token usage

        yield sse("done", {
            "model": final.model,
            "input_tokens": final.usage.input_tokens,
            "output_tokens": final.usage.output_tokens,
            "latency_ms": int((time.perf_counter() - start) * 1000),
        })

    return StreamingResponse(event_generator(), media_type="text/event-stream")