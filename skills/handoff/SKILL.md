---
name: handoff
description: Compact the current working session into a handoff document saved in the repo, so a fresh session (or a delegated builder subagent) can continue the work with zero re-discovery. Invoke when the user says "handoff", "write a handoff", "hand this off", when a code-loop session approaches the context ceiling mid-phase, or before deliberately stopping work that another session must resume. The document is written to handoffs/ in the project and is what code-loop's interrupted-session recovery reads first. Unlike /compact, the handoff survives across sessions, machines, and agents because it lives in the repo.
---

# handoff — compact a session into a resumable document

You are ending (or pausing) a working session. Produce a document that lets a
**cold reader** — a fresh session, another machine, or a delegated builder
subagent — continue the work without re-reading the whole history. The test:
could someone with only this file + the repo pick up in under 5 minutes?

## When to write one

- The user asks for a handoff.
- A code-loop phase is running long and the context ceiling is near: finish
  the current commit-sized chunk, write the handoff, tell the user to restart.
- Work is deliberately paused mid-phase (end of day, blocked on the user).

Do NOT write one for completed phases — the 5-part wrap-up + git history
already cover those.

## Where

`handoffs/HANDOFF-<YYYY-MM-DD>-<slug>.md` in the project root (create the
directory if missing). Never overwrite an earlier handoff — newest file wins;
older ones are history.

## Format (also the builder-brief format for delegated builds)

Every section is mandatory; write "none" rather than omitting one.

```markdown
# HANDOFF <date> — <one-line goal>

## Goal
What this work item is, and the phase/spec section it belongs to.

## Runtime
Agent runtime and model, if known (for example: `codex / GPT-5`).

## Workflow
Working discipline used (for example: `code-loop`, `standalone`, or the Domain Pack name).

## Canonical contract
Exact revision from root `AGENTS.md` (or `none` when the project has no dat-kit contract).

## Git state
Current branch, HEAD commit, and whether the worktree is clean or has uncommitted files.

## State
- DONE: numbered, with commit hashes where committed.
- IN PROGRESS: what is half-built, which files, what state it's in.
- NOT STARTED: remaining scope, in dependency order.

## Decisions in effect
Rows from spec/08-decisions.md that constrain this work (IDs only + one line
each) + any session-local decisions not yet recorded there (record them NOW,
then reference).

## Files touched
Path → one line on what changed / what remains. Uncommitted work flagged.

## Verified gates
Last known result per gate, verbatim ("pest 24/24 ✓, tsc ✗ 3 errors in X").
State `unverified` when no result exists; never write "mostly passing".

## Third-party tool risks
Installer-reported security risk levels, affected tool/skill, and the user's
decision. Write `none reported` when no external installer ran; never omit a
reported risk because it is inconvenient.

## Next steps
Numbered, dependency order, each starting with the exact file or command.
Step 1 must be executable immediately by the cold reader.

## Traps
Lessons-learned entries and gotchas that bit (or nearly bit) this session.

## Glossary
CONTEXT.md terms the reader must know for this work (term names only).
```

## Rules

- Facts only — no narration of the session's back-and-forth. State, not story.
- Everything verifiable: runtime, canonical-contract revision, commit hashes,
  exact gate output, third-party installer risk reports, and exact paths.
- Session-local decisions MUST be flushed to `spec/08-decisions.md` before the
  handoff is written — a handoff that hoards decisions defeats the decisions file.
- After writing: print the file path and the single command/instruction the
  user should give the next session (e.g. `continue from handoffs/HANDOFF-….md`
  or "autopilot from phase N, read the latest handoff first").
