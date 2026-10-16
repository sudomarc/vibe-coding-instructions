# Long-Horizon Engineering Task State & Handoff Template

**Task ID**: `TASK-YYYYMMDD-XXX`
**Current State**: `[ INIT | RESEARCHING | PLANNING | EXECUTING | VERIFYING | SUSPENDED | COMPLETED | FAILED ]`
**Cumulative Sessions**: `1`
**Total Tokens Consumed**: `0`
**Estimated Spent Budget (%)**: `0%`

---

## 1. Task Objective & Bounded Scope

- **Primary Goal**:
- **In-Scope Surfaces**:
- **Explicit Non-Goals**:
- **Success Criteria**:

---

## 2. Current Engineering Phase & Status

- **Active Phase**:
- **Current Progress Summary**:
- **Last Active Session ID / Trace ID**:

---

## 3. Architecture & Key Decisions Made

| Decision ID | Decision Title | Chosen Option | Rationale | Rejected Alternatives | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ADR-001` | | | | | `VERIFIED` |

---

## 4. Work Completed & Modified Surfaces

### 4.1 Completed Subtasks / Batches
- [x]

### 4.2 Changed Files & Deliverables
- `file/path/one.ts` —
- `file/path/two.py` —

---

## 5. Verification Evidence Observed

| Verification Step | Command / Probe | Observed Result | Pass/Fail | Evidence Reference |
| :--- | :--- | :--- | :--- | :--- |
| Unit Tests | `pytest tests/unit` | `24 passed` | `PASS` | `test-log-01` |

---

## 6. Durable Failure Log & Discarded Paths

> **INVARIANT**: Never delete a material failed attempt during compaction or handoff.

| Attempt # | Strategy / Code Approach | Observed Outcome | Failure Root Cause | Reconsideration Conditions |
| :--- | :--- | :--- | :--- | :--- |
| `1` | | | | |

---

## 7. Open Questions, Risks & Blockers

- **Known Risks**:
- **Uncertainties / Assumptions**:
- **Human Checkpoint Required?**: `[ YES | NO ]` —

---

## 8. Resumption Protocol & Immediate Next Actions

### 8.1 Re-Inspection Checklist for Next Session
1. Run `git status` and `git diff` to verify repository evidence matches section 4.2.
2. Run baseline verification command to confirm working tree state.
3. Verify budget and token limit before executing next batch.

### 8.2 Immediate Next Actions
1. [ ]
2. [ ]
