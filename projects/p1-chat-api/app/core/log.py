import json
import logging

from app.core.config import settings

def setup_logging() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

def log_llm_call(logger: logging.Logger, **fields: object) -> None:
    logger.info(json.dumps({"event":"llm_call",**fields}))