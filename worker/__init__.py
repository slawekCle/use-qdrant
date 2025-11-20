"""Celery worker package configured to consume tasks from Kafka."""

from .celery_app import app  # noqa: F401
