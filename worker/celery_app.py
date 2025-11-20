import logging
import os
from typing import Any, Dict, Optional

import requests
from celery import Celery

logger = logging.getLogger(__name__)


BROKER_URL = os.getenv("CELERY_BROKER_URL", "kafka://kafka:9092")
TASK_TOPIC = os.getenv("CELERY_TASK_TOPIC", "celery")
DEFAULT_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10"))

app = Celery("kafka_worker", broker=BROKER_URL)
app.conf.update(
    task_default_queue=TASK_TOPIC,
    task_serializer="json",
    accept_content=["json"],
    result_backend=None,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)


@app.task(name="worker.perform_http_request")
def perform_http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    timeout: Optional[float] = None,
) -> Dict[str, Any]:
    """Execute an HTTP request and return a summary of the response.

    The task is designed to be triggered by events received through Kafka. It
    supports basic customization of HTTP method, headers and body. Exceptions
    are captured and returned so they can be logged by the worker rather than
    causing a crash.
    """

    request_timeout = timeout or DEFAULT_TIMEOUT

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data if isinstance(data, (dict, list)) else None,
            data=None if isinstance(data, (dict, list)) else data,
            timeout=request_timeout,
        )

        return {
            "url": url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
            "elapsed": response.elapsed.total_seconds(),
        }
    except requests.RequestException as exc:  # pragma: no cover - network errors are runtime dependent
        logger.exception("HTTP request failed")
        return {"url": url, "error": str(exc)}
