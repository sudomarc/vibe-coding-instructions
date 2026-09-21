#!/usr/bin/env python3
"""Validate structural integrity of the instruction framework.

The validator is deliberately conservative: it checks existence, links,
critical governance wording, and the GitHub custom-agent/workflow contracts.
It does not decide whether an instruction is substantively correct.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

REQUIRED_PATHS = [
    "AGENTS.md",
    "MASTER-PROMPT.md",
    "README.md",
    ".ai/core",
    ".ai/skills",
    ".ai/skills/token-economics/SKILL.md",
    ".ai/templates/agent-cost-report.md",
    ".ai/skills/legal-compliance/SKILL.md",
    ".ai/agents/legal-compliance-reviewer.agent.md",
    ".ai/templates/legal-audit.md",
    ".ai/self-improvement/SKILL.md",
    ".ai/self-improvement/rules.md",
    ".ai/self-improvement/feedback-loop.md",
    ".github/agents/self-improvement.agent.md",
    ".github/copilot-instructions.md",
]

GOVERNANCE_MARKERS = (
    "explicit human approval",
    "confidence is",
    "not authorization",
)

def fail(message: str) -> None:
    print(f"FAIL: {message}")

def validate_required_paths(failures: list[str]) -> None:
    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"missing required path: {rel}")

def validate_governance_markers(failures: list[str]) -> None:
    governance_files = [
        ".ai/self-improvement/SKILL.md",
        ".ai/self-improvement/rules.md",
        ".ai/self-improvement/feedback-loop.md",
        ".github/agents/self-improvement.agent.md",
    ]
    for rel in governance_files:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        missing = [marker for marker in GOVERNANCE_MARKERS if marker not in text]
        if missing:
            failures.append(f"{rel} is missing governance marker(s): {', '.join(missing)}")

def validate_links(failures: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for target in MARKDOWN_LINK_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not candidate.exists():
                failures.append(f"broken link in {rel}: {target}")

def validate_custom_agent(failures: list[str]) -> None:
    agent = ROOT / ".github/agents/self-improvement.agent.md"
    if not agent.exists():
        return
    text = agent.read_text(encoding="utf-8", errors="ignore")
    parts = text.split("---", 2)
    if len(parts) < 3 or not parts[0].strip() == "":
        failures.append("custom agent frontmatter is missing required YAML delimiters")
    elif "description:" not in parts[1]:
        failures.append("custom agent frontmatter is missing required description")
    if "OBSERVE → RECORD → CLASSIFY" not in text:
        failures.append("custom agent is missing the controlled improvement loop")

def validate_workflows(failures: list[str]) -> None:
    workflow_dir = ROOT / ".github/workflows"
    if not workflow_dir.exists():
        return
    for workflow in workflow_dir.glob("*.y*ml"):
        text = workflow.read_text(encoding="utf-8", errors="ignore")
        if "workflow_dispatch" not in text:
            failures.append(f"automation workflow lacks workflow_dispatch: {workflow.relative_to(ROOT)}")
        if "permissions:" not in text:
            failures.append(f"automation workflow lacks explicit permissions: {workflow.relative_to(ROOT)}")

def main() -> int:
    failures: list[str] = []
    validate_required_paths(failures)
    validate_governance_markers(failures)
    validate_links(failures)
    validate_custom_agent(failures)
    validate_workflows(failures)

    if failures:
        for failure in failures:
            fail(failure)
        return 1

    print("PASS: instruction framework structure and critical contracts are valid")
    return 0

if __name__ == "__main__":
    sys.exit(main())
