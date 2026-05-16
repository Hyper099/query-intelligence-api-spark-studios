"""Run complex sample queries against the Query Intelligence API.

Usage:
    python app/test/run_queries.py
    python app/test/run_queries.py --base-url http://127.0.0.1:8000
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
QUERY_FILE = HERE / "complex_queries.json"
OUTPUT_DIR = HERE / "output"


def main() -> None:
    args = parse_args()
    queries = load_queries(args.query_file)
    OUTPUT_DIR.mkdir(exist_ok=True)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / run_id
    run_dir.mkdir()

    results = []
    for index, item in enumerate(queries, start=1):
        print(f"[{index}/{len(queries)}] {item['name']}")
        result = run_query(args.base_url, item)
        results.append(result)

        output_path = run_dir / f"{index:02d}_{item['name']}.json"
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    summary = {
        "base_url": args.base_url,
        "run_id": run_id,
        "total_queries": len(results),
        "successful_queries": sum(1 for result in results if result.get("status") == "success"),
        "results": results,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote outputs to: {run_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run complex sample queries against the API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="API base URL")
    parser.add_argument("--query-file", type=Path, default=QUERY_FILE, help="JSON file of queries")
    return parser.parse_args()


def load_queries(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Query file must contain a JSON list")
    return data


def run_query(base_url: str, item: dict[str, str]) -> dict[str, Any]:
    response = post_json(f"{base_url.rstrip('/')}/queries", {"query": item["query"]})
    return response.get("json") or response.get("error")


def post_json(url: str, payload: dict[str, str]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return send_request(request)


def send_request(request: urllib.request.Request) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return {
                "status": response.status,
                "json": json.loads(response.read().decode("utf-8")),
            }
    except urllib.error.HTTPError as exc:
        return {
            "status": exc.code,
            "error": read_error_body(exc),
        }
    except urllib.error.URLError as exc:
        return {
            "status": None,
            "error": str(exc.reason),
        }


def read_error_body(exc: urllib.error.HTTPError) -> Any:
    raw_body = exc.read().decode("utf-8")
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body


if __name__ == "__main__":
    main()
