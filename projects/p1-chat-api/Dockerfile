# ---- LLM Chat Service ----
FROM python:3.12-slim

# Don't write .pyc files; print logs immediately (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Dependencies first: this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Then the code (changes often, so it comes last)
COPY app/ app/
COPY prompts/ prompts/

# Run as a normal user, not root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Docker marks the container "unhealthy" if /health stops answering
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

# 0.0.0.0 = accept connections from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
