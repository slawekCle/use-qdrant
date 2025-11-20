"""Example utility to publish a task to the Kafka-backed Celery worker."""

import os

from worker.celery_app import app

BROKER_URL = os.getenv("CELERY_BROKER_URL", "kafka://localhost:9092")
TASK_NAME = "worker.perform_http_request"


def main() -> None:
    async_result = app.send_task(
        TASK_NAME,
        args=["https://example.org"],
        kwargs={"method": "GET"},
    )
    print(f"Enqueued task {async_result.id} to {BROKER_URL}")


if __name__ == "__main__":
    main()
