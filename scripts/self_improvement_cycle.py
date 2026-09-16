#!/usr/bin/env python3
"""Collect repository evidence for a controlled self-improvement cycle.

This script is intentionally deterministic: it collects evidence and computes
mechanical metrics. It does not modify governance or decide that a rule must
change. An AI agent may use the report to perform semantic analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PATH_RE = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.github|\.ai|docs|scripts)/[^\s`\)>,]+)")


def run(command: list[str]) -> tuple[int, str]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip()


def git_files() -> list[str]:
    code, out = run(["git", "ls-files"])
    if code != 0:
        raise RuntimeError("git ls-files failed")
    return [line for line in out.splitlines() if line]


def collect_broken_links(files: list[str]) -> list[dict[str, str]]:
    known = {Path(p).as_posix() for p in files}
    broken: list[dict[str, str]] = []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for target in MARKDOWN_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or re.match(r"^(?:https?:|mailto:|#)", target):
                continue
            candidate = (Path(rel).parent / target).as_posix()
            candidate = Path(candidate).as_posix()
            if candidate not in known and not (ROOT / candidate).exists():
                broken.append({"source": rel, "target": target})
    return broken


def collect_referenced_missing_paths(files: list[str]) -> list[dict[str, str]]:
    existing = {Path(p).as_posix() for p in files}
    missing: list[dict[str, str]] = []
    for rel in files:
        if not rel.endswith(".md"):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        for match in PATH_RE.findall(text):
            candidate = match.rstrip(".,:;`\")'")
            if candidate not in existing and not (ROOT / candidate).exists():
                missing.append({"source": rel, "reference": candidate})
    unique = {(item["source"], item["reference"]): item for item in missing}
    return list(unique.values())


def github_get(path: str) -> object | None:
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not repo or not token:
        return None
    request = Request(
        f"https://api.github.com/repos/{repo}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "vibe-self-improvement-cycle",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def collect_github_signals(days: int) -> dict[str, object]:
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    runs = github_get(f"/actions/runs?per_page=100&created=>={since}")
    issues = github_get(f"/issues?state=all&per_page=100&since={since}")

    workflow_failures: Counter[str] = Counter()
    workflow_total = 0
    if isinstance(runs, dict):
        for run_data in runs.get("workflow_runs", []):
            workflow_total += 1
            if run_data.get("conclusion") in {"failure", "timed_out", "cancelled"}:
                workflow_failures[run_data.get("name", "unknown")] += 1

    issue_signals: list[dict[str, str]] = []
    if isinstance(issues, list):
        for item in issues:
            title = str(item.get("title", ""))
            body = str(item.get("body") or "")
            haystack = f"{title}\n{body}".lower()
            if any(token in haystack for token in ("bug", "broken", "regression", "failed", "failure", "contradiction", "friction")):
                issue_signals.append({
                    "title": title,
                    "kind": "pull_request" if "pull_request" in item else "issue",
                    "url": str(item.get("html_url", "")),
                })

    return {
        "window_days": days,
        "workflow_run_count": workflow_total,
        "workflow_failures": dict(workflow_failures),
        "issue_signal_count": len(issue_signals),
        "issue_signals": issue_signals[:25],
        "api_available": isinstance(runs, dict) or isinstance(issues, list),
    }


def load_record_counts() -> dict[str, int]:
    base = ROOT / ".ai" / "self-improvement" / "records"
    observations = list((base / "observations").glob("*.md")) if (base / "observations").exists() else []
    proposals = list((base / "proposals").glob("*.md")) if (base / "proposals").exists() else []
    outcomes = list((base / "outcomes").glob("*.md")) if (base / "outcomes").exists() else []
    return {
        "observation_count": len(observations),
        "proposal_count": len(proposals),
        "outcome_count": len(outcomes),
    }


def build_report(mode: str, days: int) -> dict[str, object]:
    files = git_files()
    broken_links = collect_broken_links(files)
    missing_refs = collect_referenced_missing_paths(files)
    github = collect_github_signals(days)
    records = load_record_counts()

    recurring = []
    for name, count in github["workflow_failures"].items():
        if count >= 2:
            recurring.append({
                "type": "recurring_ci_failure",
                "name": name,
                "count": count,
                "classification": "RECURRING_FAILURE",
                "facts": [f"Workflow {name} failed/cancelled {count} times in the collection window."],
                "hypothesis": "Repeated workflow failure may indicate a workflow, environment, or validation problem; root cause is not established by this collector.",
            })

    if broken_links:
        recurring.append({
            "type": "broken_markdown_links",
            "count": len(broken_links),
            "classification": "SYSTEMIC_FAILURE" if len(broken_links) >= 3 else "RECURRING_FAILURE",
            "facts": [f"Collector found {len(broken_links)} broken Markdown links."],
            "hypothesis": "Link integrity may lack an enforceable validation gate; root cause requires inspection.",
        })

    if missing_refs:
        recurring.append({
            "type": "missing_referenced_paths",
            "count": len(missing_refs),
            "classification": "RECURRING_FAILURE" if len(missing_refs) >= 2 else "ONE_OFF_FAILURE",
            "facts": [f"Collector found {len(missing_refs)} missing repository-path references."],
            "hypothesis": "Documentation/path references may be drifting without a complete validator.",
        })

    return {
        "schema_version": "1.0",
        "cycle_id": datetime.now(timezone.utc).strftime("cycle-%Y%m%dT%H%M%SZ"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
        "commit": os.environ.get("GITHUB_SHA"),
        "facts": {
            "tracked_file_count": len(files),
            "broken_links": broken_links,
            "missing_referenced_paths": missing_refs,
            "github": github,
            "records": records,
        },
        "candidate_signals": recurring,
        "metrics": {
            "observation_count": records["observation_count"],
            "proposal_count": records["proposal_count"],
            "accepted_count": 0,
            "rejected_count": 0,
            "reverted_count": 0,
            "regression_count": 0,
            "confirmed_improvements": 0,
        },
        "interpretation_policy": {
            "fact": "Directly collected evidence.",
            "hypothesis": "Tentative explanation that requires validation.",
            "interpretation": "Agent-generated conclusion; never treat it as a fact without evidence.",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("daily", "weekly", "manual"), default="manual")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--output", default="cycle-report.json")
    args = parser.parse_args()
    if args.days < 1 or args.days > 90:
        parser.error("--days must be between 1 and 90")

    report = build_report(args.mode, args.days)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = ROOT / "cycle-report.md"
    candidates = report["candidate_signals"]
    lines = [
        f"# Self-improvement cycle `{report['cycle_id']}`",
        "",
        f"Mode: `{report['mode']}`",
        f"Generated: `{report['generated_at']}`",
        f"Repository: `{report['repository']}`",
        f"Commit: `{report['commit'] or 'UNKNOWN'}`",
        "",
        "## Deterministic facts",
        f"- Tracked files: {report['facts']['tracked_file_count']}",
        f"- Broken Markdown links: {len(report['facts']['broken_links'])}",
        f"- Missing referenced paths: {len(report['facts']['missing_referenced_paths'])}",
        f"- Workflow runs observed: {report['facts']['github']['workflow_run_count']}",
        f"- Issue/PR signals observed: {report['facts']['github']['issue_signal_count']}",
        "",
        "## Candidate signals",
    ]
    if candidates:
        for item in candidates:
            lines.append(f"- `{item['classification']}` — {item['type']} ({item['count']})")
            lines.append(f"  - FACT: {item['facts'][0]}")
            lines.append(f"  - HYPOTHESIS: {item['hypothesis']}")
    else:
        lines.append("- None produced by deterministic collection.")
    lines += [
        "",
        "## Agent policy",
        "Do not treat candidate signals as proof of a systemic rule failure. Distinguish ONE-OFF, RECURRING, and SYSTEMIC findings using repository evidence.",
        "",
        "Generated by `scripts/self_improvement_cycle.py`.",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(summary.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
