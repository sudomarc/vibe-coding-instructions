# Handoff Protocol

## Header

```markdown
# Handoff
Date: <YYYY-MM-DD>
Task: <short name>
Repository: <name>
State: <clean|modified|blocked>
```

## Objective

State the requested outcome exactly.

## Completed

List only work that actually exists in the repository.

## Files changed

List each path and its purpose.

## Verification

Record exact commands, tools, outcomes, and failures.

## Decisions

Record decisions already made so the next session does not reopen settled questions.

## Open issues

List unresolved defects, missing information, conflicts, and approvals.

## Next action

Describe the smallest concrete next step.

## Safety notes

Record pending migrations, deployment steps, destructive operations, secrets requirements, or other high-impact concerns.

## Resume protocol

The next agent should:

1. read `AGENTS.md`;
2. read the five core files;
3. read this handoff;
4. inspect repository status and diff;
5. run the minimal verification needed to confirm the handoff state;
6. continue only from the documented next action.

Do not infer that a command passed merely because it appears in the handoff. Treat it as historical evidence and re-run checks when current state matters.
