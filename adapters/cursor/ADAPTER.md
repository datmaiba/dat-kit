# Host Adapter — Cursor

Registry descriptor: `registry/adapters.json#adapter_id=cursor`. Lifecycle:
`scaffold_active` (carries the pre-existing 1.16 `.cursorrules` pointer).
Contract: `docs/contracts/host-adapter.md`.

## Pointer semantics

Cursor reads root `AGENTS.md` natively; the emitted `.cursorrules` is a
legacy-compatible thin pointer (template `templates/common/.cursorrules`)
kept byte-identical to dat-kit 1.16 scaffolding. It selects policy only.

## `.cursorrules` retirement path (Phase 3, not here)

Official docs mark `.cursorrules` deprecated-but-supported. Phase 3 gives it
typed `RETIRE_LEGACY` semantics: recognized, inventoried, and replaced by a
`.cursor/rules/*.mdc` pointer **only inside an approved migration plan**.
Per the Phase 0B fact-check correction (`docs/spikes/phase-0b/host-facts.md`),
retirement is based on documented deprecation — dat-kit does not claim Agent
mode ignores the file. No `.mdc` artifact ships in Phase 2.

## Official facts (dated; re-verify before the affected RC)

See descriptor `official_facts` (verified 2026-07-18, docs.cursor.com): CLI
reads root `AGENTS.md` and `CLAUDE.md`; project rules live in
`.cursor/rules`; `.cursorrules` legacy/deprecated.

## Conformance

- Fixture `ADAPTER-CURSOR-LEGACY-01` + `test_adapter_conformance.py`: pointer
  targets `AGENTS.md`, template is policy-free, rollback owns only
  `.cursorrules` (project side) and its template (repo side).
- Host smoke: no scriptable headless Cursor available — manual evidence
  checklist: Cursor version, project open with scaffolded tree, confirmation
  AGENTS.md is loaded as context, `.cursorrules` produces no conflicting
  instruction.

## Rollback

Remove `.cursorrules` after exact-hash check; `AGENTS.md` untouched.
