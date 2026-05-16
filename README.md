# Query Intelligence API

FastAPI backend service that accepts natural language research queries, extracts structured intelligence with Anthropic Claude, stores the processed result in SQLite, and supports later retrieval by ID.

Example query:

```text
Find battery technology startups in Southeast Asia
```

Example extracted data:

```json
{
  "industry": "battery technology",
  "region": "Southeast Asia",
  "company_type": "startup",
  "keywords": [
      "battery technology",
      "startups",
      "southeast asia",
      "energy storage"
    ],
   "confidence_score": 0.95
}

```

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Anthropic Python SDK
- SQLite with SQLAlchemy ORM
- Jinja2 prompt templates
- python-dotenv

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Set your Anthropic API key in `.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Run

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive docs:

```text
http://127.0.0.1:8000/docs
```

## Environment Variables

| Variable                      | Default                               | Description                                |
| ----------------------------- | ------------------------------------- | ------------------------------------------ |
| `ANTHROPIC_API_KEY`         | empty                                 | Anthropic API key used by the official SDK |
| `ANTHROPIC_MODEL`           | `claude-haiku-4-5-20251001`         | Claude model used for extraction           |
| `ANTHROPIC_TIMEOUT_SECONDS` | `10`                                | Per-request timeout for Claude calls       |
| `ANTHROPIC_MAX_RETRIES`     | `2`                                 | SDK retry count                            |
| `DATABASE_URL`              | `sqlite:///./query_intelligence.db` | SQLAlchemy database URL                    |

## API Examples

### Create Query

```bash
curl -X POST http://127.0.0.1:8000/queries ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Find battery startups in Southeast Asia\"}"
```

Response:

```json
{
  "status": "success",
  "id": 1,
  "query": "Find battery startups in Southeast Asia",
  "normalized_query": "find battery startups in southeast asia",
  "structured_data": {
    "industry": "battery",
    "region": "Southeast Asia",
    "company_type": "startup",
    "keywords": ["battery", "startup", "southeast", "asia"],
    "confidence_score": 0.91
  },
  "metadata": {
    "model": "claude-haiku-4-5-20251001",
    "prompt_version": "v1",
    "processing_latency_ms": 842,
    "extraction_source": "llm"
  },
  "validation": {
    "schema_valid": true
  },
  "created_at": "2026-05-16T12:00:00Z"
}
```

### Get Query

```bash
curl http://127.0.0.1:8000/queries/1
```

Missing IDs return:

```json
{
  "detail": "Query not found"
}
```

## Running Sample Queries

The `app/test` folder includes complex sample queries and a small runner script:

```bash
python app/test/run_queries.py
```

By default it sends requests to `http://127.0.0.1:8000` and writes responses to:

```text
app/test/output/<run_id>/
```

The runner sends each query once using `POST /queries` and writes the API response body directly to one output file per query. To use another API URL:

```bash
python app/test/run_queries.py --base-url http://127.0.0.1:8000
```

## Architecture

```text
app/
  main.py                 FastAPI app, startup, middleware
  config.py               Environment-based settings
  database.py             SQLAlchemy engine/session setup
  models/                 ORM models
  schemas/                Pydantic request/response contracts
  routes/                 Thin HTTP route handlers
  services/               Business logic and Claude integration
  repositories/           Persistence layer
  prompts/                Jinja2 prompt templates
  utils/                  Parsing, heuristics, logging, rate limiting
```

Route handlers validate HTTP input and delegate to services. The query service normalizes text by trimming whitespace, collapsing repeated spaces, and lowercasing before calling Claude. It validates the structured response with Pydantic, falls back to safe parsing and heuristics when necessary, then persists through the repository.

## What I Would Improve With More Time

- Add a frontend dashboard to submit queries and view extracted intelligence in a cleaner UI.
- Add authentication and user-specific query history.
- Add proper integration tests with a mocked Anthropic client.
- Add Alembic migrations for better database version management.
- Improve extraction accuracy with better prompts and additional validation rules.
- Add retry handling and better error messages for failed LLM responses.
- Add caching for repeated queries to reduce API costs and improve response time.
- Add stricter and configurable rate limiting for production-grade API protection.
- Add analytics such as query counts, extraction success rate, and average processing latency.
