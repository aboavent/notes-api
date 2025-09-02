# Notes API (FastAPI + SQLite)

Simple CRUD service to manage text notes. Great as a container demo and CI/CD target.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit: http://127.0.0.1:8000/healthz and http://127.0.0.1:8000/docs

## Environment

Copy `.env.example` to `.env` (optional). Default DB is SQLite at `./data/notes.db`.

## Docker

```bash
docker build -t notes-api:local .
docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data notes-api:local
```

## API quickstart

```bash
curl -X POST http://localhost:8000/notes -H 'Content-Type: application/json'       -d '{"title":"First note","content":"Hello!"}'

curl http://localhost:8000/notes
```
