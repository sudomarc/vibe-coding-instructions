# Long-Horizon Engineering Task State

**Task ID**: `LHT-YYYY-XXX`
**Title**: Short descriptive title of the long-running engineering task
**Status**: `IN_PROGRESS` | `PAUSED` | `COMPLETED` | `FAILED` | `BLOCKED` | `ROLLED_BACK`
**Current Phase**: `DISCOVERY_RESEARCH` | `ARCHITECTURAL_SPECIFICATION` | `BATCHED_IMPLEMENTATION` | `INTEGRATION_VERIFICATION` | `FINAL_DIFF_REVIEW`
**Created At**: `YYYY-MM-DDTHH:MM:SSZ`
**Updated At**: `YYYY-MM-DDTHH:MM:SSZ`
**Session Count**: `1`

---

## 1. Executive Objective & Non-Goals

### Objective
Clear, observable statement of what must be achieved across multiple execution sessions.

### Non-Goals
Specific items explicitly out of scope to prevent scope expansion across sessions.

---

## 2. Token Budget & Cost Management

- **Allocated Token Budget**: `5,000,000`
- **Consumed Token Count**: `0`
- **Max Cost Cap (USD)**: `$50.00`
- **Consumed Cost (USD)**: `$0.00`
- **Circuit Breaker Threshold**: `3 consecutive verification failures`

---

## 3. Active Checkpoints

| Checkpoint ID | Session ID | Phase | Timestamp (UTC) | Git SHA | Verified | Evidence / Log Ref |
|---|---|---|---|---|---|---|
| `CP-001` | `SESS-001` | `DISCOVERY_RESEARCH` | `YYYY-MM-DDTHH:MM:SSZ` | `a1b2c3d` | Yes | `logs/research.log` |

---

## 4. Active Artifacts & Research-to-Code Dossier

| Artifact ID | Artifact Type | Path / Storage | Checksum (SHA256) | Producer Agent |
|---|---|---|---|---|
| `ART-001` | `RESEARCH_DOSSIER` | `docs/dossier.md` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `researcher` |

### Verified Research Findings Summary (`FACT`/`OBSERVED`/`VERIFIED`)
1. `[VERIFIED]` Brief statement of verified code finding with source file path.
2. `[FACT]` Baseline system constraint or configuration detail.

---

## 5. Batched Implementation Roadmap

- [ ] **Batch 1**: First verifiable implementation chunk
  - **Goal**: ...
  - **Affected Files**: `src/foo.py`, `tests/test_foo.py`
  - **Verification Command**: `python3 -m unittest tests/test_foo.py`
  - **Status**: `NOT_STARTED`
- [ ] **Batch 2**: Second verifiable implementation chunk
  - **Goal**: ...
  - **Status**: `NOT_STARTED`

---

## 6. Recovery & Failure Log

| Timestamp (UTC) | Session ID | Failure Taxonomy | Observed Error / Root Cause | Remediation Action |
|---|---|---|---|---|
| `YYYY-MM-DD` | `SESS-000` | `NONE` | N/A | N/A |

---

## 7. Next Actions for Resumption
1. Step 1 to execute in the next session or following context compaction.
2. Step 2 to execute.
