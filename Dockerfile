FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

RUN pip install --no-cache-dir uv

COPY pyproject.toml .

RUN uv sync --no-dev

COPY worker ./worker

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info"]
