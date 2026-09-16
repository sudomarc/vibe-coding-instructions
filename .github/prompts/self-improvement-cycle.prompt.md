# Controlled Self-Improvement Cycle Prompt

You are running the repository's controlled self-improvement cycle.

Read these first:

1. `AGENTS.md`
2. `.ai/self-improvement/SKILL.md`
3. `.ai/self-improvement/rules.md`
4. `.ai/self-improvement/feedback-loop.md`
5. `.ai/self-improvement/daily-cycle.md`
6. `.ai/self-improvement/metrics.md`
7. `cycle-report.json`
8. `cycle-report.md`

## Objective

Use the collected evidence to identify justified improvements to this instruction framework. Do not invent incidents or treat the collector's hypotheses as facts.

## Required reasoning model

For each candidate:

`OBSERVE → COLLECT → ANALYZE → CLASSIFY → ROOT CAUSE → PROPOSE → VALIDATE`

Classify the signal as `ONE_OFF_FAILURE`, `RECURRING_FAILURE`, or `SYSTEMIC_FAILURE` only when the evidence supports the classification.

Separate:

- `FACT` — directly established evidence;
- `HYPOTHESIS` — tentative explanation;
- `INTERPRETATION` — your conclusion from the evidence.

Consider alternative explanations before selecting a root-cause hypothesis.

## Change hierarchy

Prefer:

`LOCAL FIX → SKILL / REFERENCE / TEMPLATE FIX → WORKFLOW FIX → CORE GOVERNANCE REVIEW`

Do not change `.ai/core/` or any governance-critical behavior in this unattended run. Governance-critical candidates must be documented as a proposal and left for explicit human approval.

Governance-critical includes:

- `.ai/core/`;
- security or safety boundaries;
- verification authority or verification requirements;
- instruction precedence;
- provider trust boundaries;
- permissions or destructive-operation policy;
- privacy/data retention;
- increases in autonomous authority.

Confidence is not authorization.

## Implementation rules

- Inspect the existing implementation before editing.
- Preserve unrelated work.
- Make the smallest coherent change.
- Do not add dependencies unless justified.
- Do not modify application code; this repository is the framework itself.
- Do not commit, push, merge, or create a PR. The surrounding workflow handles Git integration.
- If no change is justified, leave the working tree unchanged and report why.

## Validation

When a change is made:

1. run `python3 scripts/validate_instructions.py`;
2. run any relevant focused checks;
3. run `python3 scripts/self_improvement_cycle.py --mode manual --days 7` when appropriate;
4. inspect `git diff --check` and the full diff;
5. check changed references and paths;
6. confirm the original problem is actually addressed;
7. inspect for contradictions or rule drift.

Never claim an improvement is confirmed merely because the edit looks correct.

## Durable memory

For a justified change, add or update the appropriate record under `.ai/self-improvement/records/`:

- observation record;
- proposal record;
- outcome record when post-change measurement is available.

Do not store secrets or unnecessary personal information.

## Final response for the workflow

Report:

- observations and evidence;
- classification;
- root-cause hypothesis and alternatives;
- proposed/applied change;
- risks;
- validation actually run;
- approval requirement;
- files changed;
- remaining uncertainty;
- measurement needed after merge.
