#!/usr/bin/env python3
"""Analyze provider-neutral agent usage records.

Input is JSON Lines. Each record should contain any known fields from the
agent-cost-report template. Missing fields remain unknown rather than being
invented.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

NUMERIC_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_tokens",
    "tool_calls",
    "tool_result_tokens",
    "retries",
    "compactions",
    "subagents",
    "estimated_cost",
)
REQUIRED_FIELDS = ("input_tokens", "output_tokens")


def number(value: Any) -> float:
    if isinstance(value, bool) or value is None:
        return 0.0
    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0
    return value if math.isfinite(value) else 0.0


def load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{path}:{line_no}: record must be a JSON object")
            records.append(item)
    return records


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {field: sum(number(r.get(field)) for r in records) for field in NUMERIC_FIELDS}
    cached = totals["cached_input_tokens"]
    inputs = totals["input_tokens"]
    verified = sum(1 for r in records if r.get("verified_success") is True)

    return {
        "records": len(records),
        **totals,
        "cache_hit_ratio": (cached / inputs) if inputs else None,
        "retry_ratio": (totals["retries"] / len(records)) if records else None,
        "average_tool_calls": (totals["tool_calls"] / len(records)) if records else None,
        "average_compactions": (totals["compactions"] / len(records)) if records else None,
        "average_subagents": (totals["subagents"] / len(records)) if records else None,
        "verified_successes": verified,
        "cost_per_verified_success": (
            totals["estimated_cost"] / verified if verified else None
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path, help="JSONL usage records")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    try:
        records = load_records(args.jsonl)
        summary = aggregate(records)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    missing = [
        field
        for field in REQUIRED_FIELDS
        if records and all(field not in record for record in records)
    ]
    if missing:
        print(
            "WARN: no records contain required usage fields: " + ", ".join(missing),
            file=sys.stderr,
        )

    print(json.dumps(summary, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
