---
name: session-workflow
description: Session start and end protocol — read TODO.md, continue from checkpoint, update and commit
version: "4.0"
author: software-engineer
audience: all-agents
workflow: session-management
---

# Session Workflow

Every session starts by reading state. Every session ends by writing state. This makes any agent able to continue from where the last session stopped.

## Agent Responsibilities: Feature File Moves

**The PO is the sole owner of all `.feature` file moves.** Software-engineer and reviewer never move, rename, or create feature files.

| Trigger | Action | Who |
|---|---|---|
| Feature selected for development | Move `backlog/<name>.feature` → `in-progress/<name>.feature` | PO only |
| Step 4 APPROVED | Move `in-progress/<name>.feature` → `completed/<name>.feature` | PO only |

**Escalation**: if software-engineer or reviewer find no file in `docs/features/in-progress/`, they **stop immediately** and output:

> No feature is currently in progress. Escalating to @product-owner — please move a BASELINED feature from `docs/features/backlog/` to `docs/features/in-progress/` to begin development.

## Session Start

1. Read `TODO.md` — find current feature, current step, and the "Next" line.
   - If `TODO.md` does not exist, create a basic one:
     ```markdown
     # Current Work

     No feature in progress.
     Next: Run @product-owner — load skill feature-selection and pick the next BASELINED feature from backlog.
     ```
2. If a feature is active, read:
   - `docs/features/in-progress/<name>.feature` — feature spec (feature description + Rules + Examples)
   - `docs/discovery.md` — project-level discovery changelog (for context)
3. Run `git status` — understand what is committed vs. what is not
4. Confirm scope: you are working on exactly one step of one feature

If TODO.md says "No feature in progress" and you are the PO: load `skill feature-selection` — it guides the PO through scoring and selecting the next BASELINED backlog feature. The PO must verify the feature has `Status: BASELINED` in its feature description before moving it to `in-progress/` — if not baselined, complete Step 1 first.

If TODO.md says "No feature in progress" and you are software-engineer or reviewer: stop and escalate to PO (see Escalation above).

## Session End

1. Update TODO.md manually:
   - Mark completed criteria `[x]`
   - Mark in-progress criteria `[~]`
   - Add `[ ]` rows for any new `@id` criteria introduced since the last session
   - Update the "Next" line with one concrete action
   - When starting a fresh feature (cycle reset): drop all `[x]` rows from the previous feature
2. Commit any uncommitted work (even WIP):
   ```bash
   git add -A
   git commit -m "WIP(<feature-name>): <what was done>"
   ```
3. If a step is fully complete, use the proper commit message instead of WIP.

## Step Completion Protocol

When a step completes within a session:

1. Update TODO.md to reflect the completed step before doing any other work.
2. Commit the TODO.md update:
   ```bash
   git add TODO.md
   git commit -m "chore: complete step <N> for <feature-name>"
   ```
3. Only then begin the next step (in a new session where possible — see Rule 4).

## TODO.md Format

```markdown
# Current Work

Feature: <name>
Step: <1-5> (<step name>)
Source: docs/features/in-progress/<name>.feature

## Progress
- [x] `@id:<hex>`: <description>
- [~] `@id:<hex>`: <description>  ← IN PROGRESS
- [ ] `@id:<hex>`: <description>

## Next
Run @<agent-name> — <one concrete action>
```

**"Next" line format**: Always prefix with `Run @<agent-name>` so the human knows exactly which agent to invoke. Examples:
- `Run @software-engineer — implement @id:a1b2c3d4 (Step 3 RED)`
- `Run @reviewer — verify feature display-version at Step 4`
- `Run @product-owner — pick next BASELINED feature from backlog`
- `Run @product-owner — accept feature display-version at Step 5`

**Source path by step:**
- Step 1: `Source: docs/features/backlog/<name>.feature`
- Steps 2–4: `Source: docs/features/in-progress/<name>.feature`
- Step 5: `Source: docs/features/completed/<name>.feature`

Status markers:
- `[ ]` — not started
- `[~]` — in progress
- `[x]` — complete
- `[-]` — cancelled/skipped

When no feature is active:
```markdown
# Current Work

No feature in progress.
Next: Run @product-owner — load skill feature-selection and pick the next BASELINED feature from backlog.
```

## Step 3 (TDD Loop) Cycle-Aware TODO Format

During Step 3 (TDD Loop), TODO.md **must** include a `## Cycle State` block to track Red-Green-Refactor progress.

```markdown
# Current Work

Feature: <name>
Step: 3 (TDD Loop)
Source: docs/features/in-progress/<name>.feature

## Cycle State
Test: `@id:<hex>` — <description>
Phase: RED | GREEN | REFACTOR

## Progress
- [x] `@id:<hex>`: <description>
- [~] `@id:<hex>`: <description>          ← in progress (see Cycle State)
- [ ] `@id:<hex>`: <description>          ← next

## Next
<One actionable sentence>
```

### Phase Transitions

- Move from `RED` → `GREEN` when the test fails with a real assertion
- Move from `GREEN` → `REFACTOR` when the test passes
- Move from `REFACTOR` → mark `@id` complete in `## Progress` when test-fast passes

## Recovery: gen-todo Script

If `TODO.md` gets out of sync after a branch merge, manual reset, or corrupted state, run the recovery script directly to rebuild the `## Progress` block from the in-progress `.feature` file:

```bash
python .opencode/skills/session-workflow/scripts/gen_todo.py
python .opencode/skills/session-workflow/scripts/gen_todo.py --check   # dry run
```

This is a recovery tool only — do not run it as part of the normal session workflow.

## Rules

1. Never skip reading TODO.md at session start
2. Never end a session without updating TODO.md
3. Never leave uncommitted changes — commit as WIP if needed
4. One step per session where possible; do not start Step N+1 in the same session as Step N
5. The "Next" line must be actionable enough that a fresh AI can execute it without asking questions
6. During Step 3, always update `## Cycle State` when transitioning between RED/GREEN/REFACTOR phases
7. When a step completes, update TODO.md and commit **before** any further work
8. During Step 3, produce the Self-Declaration as conversation output before handing off to Step 4 — every claim must have AGREE/DISAGREE with `file:line` evidence (see implementation/SKILL.md for the full checklist)
9. Software-engineer and reviewer never move, rename, or create `.feature` files — escalate to PO
