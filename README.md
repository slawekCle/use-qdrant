# Kafka Celery Worker

Ten projekt zawiera prostego workera Celery, który pobiera zadania z brokera Kafka i wykonuje zapytania HTTP. Do uruchomienia środowiska deweloperskiego dołączono plik `docker-compose.yml` z usługami Zookeeper, Kafka oraz kontenerem workera.

## Wymagania

- Docker i Docker Compose
- Python 3.13 (opcjonalnie, jeżeli chcesz uruchomić skrypty lokalnie)
- [uv](https://github.com/astral-sh/uv) jako menedżer pakietów (instalacja: `pip install uv` lub skrypt z dokumentacji uv)

## Uruchamianie

1. Zbuduj i uruchom stack (obraz instaluje zależności poleceniem `uv sync --no-dev` na bazie `pyproject.toml`):
   ```bash
   docker compose up --build
   ```
2. Worker zostanie uruchomiony z konfiguracją brokera `kafka://kafka:9092` i będzie oczekiwał na wiadomości w temacie `celery`.

## Lokalne środowisko

Jeżeli chcesz testować kod poza Dockerem, utwórz środowisko wirtualne (np. `.venv`) i zainstaluj zależności przez uv:

```bash
python -m venv .venv
source .venv/bin/activate
uv sync --no-dev
```

## Wysyłanie zadań

Przykładowy skrypt `examples/send_task.py` publikuje zadanie wykonujące żądanie `GET` do `https://example.org`:

```bash
CELERY_BROKER_URL=kafka://localhost:9092 python examples/send_task.py
```

Zadanie `worker.perform_http_request` przyjmuje argumenty:
- `url` (str): adres docelowy,
- `method` (str): metoda HTTP (domyślnie `GET`),
- `headers` (dict): dodatkowe nagłówki,
- `data` (dowolne): treść żądania,
- `timeout` (float): limit czasu żądania w sekundach (domyślnie 10s).

Wynik zawiera status odpowiedzi, nagłówki, treść oraz czas wykonania. W przypadku błędu sieciowego w odpowiedzi pojawi się klucz `error`.
