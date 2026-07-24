# HANDOFF 2026-07-24 — B5 (telemetry-v3 release closure), the last unit of the B-line

## Goal

Execute **B5 — release closure** of the telemetry-v3 B-line (PLAN-v8 Phase E →
resume v7 Phase 6 DoD). Subsets #1–#5 and B4 (durable export) are **done and
committed**; B5 is the final acceptance/closure unit before Phase F (evolution).
B5 is **not** a code-feature unit — it is a release-gate/acceptance unit whose
"deliverables" are receipts (real tasks, downgrade/disable verification, schema
freeze, full regression, rollback evidence, an approved RC, and a tag on the exact
approved artifact). Governing text: `docs/contracts/telemetry-v3.md` **T3.13**
(release boundary, ~L648–666) and **PLAN-v7-platform.md §13.2** (DoD for Phase 6).

## Runtime

`cowork / claude-opus-4-8` for the session that produced this handoff. The next
session may be any runtime; record yours in the B5 scorecard line.

## Workflow

dat-kit `build-loop`, **plan-gated**, attended. Gate tier per **PLAN-v8 §6**.
The user (Dat) works plan-gated (draft plan → `dat-kit:plan-reviewer` → STOP for
explicit approval before any edit), replies in Vietnamese with English technical
terms, and commits only when he asks. B5 is high-stakes closure → expect the full
reviewer chain and a security/QA pass on any enforcement-touching change.

## Canonical contract

**dat-kit 1.16.0** (root `AGENTS.md`).

## Git state

- Branch **`feature/telemetry-v3-b3`**, HEAD **`d1e223d`**
  (`feat(telemetry): general event export to benchmarks/telemetry-v3.jsonl (B4…)`),
  **worktree clean**. Ancestors: `368c230` (subset #5 report views) → `a083f4c`
  (Fork B handoff) → `0a222b3` (Fork B resume CLI) → `f43aceb` → `2ceae62`.
- **NOT PUSHED** — the sandbox has no GitHub credentials (`could not read Username`).
  Push host-side: `git push origin feature/telemetry-v3-b3`.
- **Sandbox `.git` quirk (persists):** it can create but not `unlink` under `.git`,
  leaving a stale `.git/index.lock`. Commits still succeed; clear host-side with
  `del D:\project\dat-kit\.git\index.lock` if a git op complains.
- **Two-branch divergence (unchanged):** the v8 rename work (`code-loop`/`task-loop`,
  Phases A–C) lives on a SEPARATE branch `feature/v8-rename-code-loop` (`a4ab63c`,
  merge-base `2ceae62`), NOT an ancestor of this branch. Per branch-strategy A (Dat,
  2026-07-24) telemetry stays on `feature/telemetry-v3-b3`; the `domain_id` event
  field and branch reconciliation are deferred until after the B-line.

## State

- DONE (committed): subset #1/#2/#3; subset #4 Fork A (`f43aceb`) + Fork B
  (`0a222b3`); **subset #5 report views (`368c230`)**; **B4 general export
  (`d1e223d`)**.
- IN PROGRESS: none.
- NOT STARTED: **B5 release closure** (this handoff) → then **Phase F** (evolution
  `kit-evolve`), which requires an active telemetry producer first.

## Decisions in effect

- **Branch-strategy A** (Dat 2026-07-24): telemetry continues on
  `feature/telemetry-v3-b3`; v8 rename on its own branch; `domain_id` + branch
  reconciliation deferred until after the B-line.
- **Subset #5 D-1 / ADR `docs/decisions/0003-report-view-host-and-window.md`**:
  reports-view host = `revisions.adapter.value`; window = whole corpus (time-slice
  deferred to a later unit); no envelope field added.
- **Subset #5 D-2 / D-3**: reports views are pure functions (no CLI); aborted tasks
  count in the coverage-rate denominator (terminal-observed).
- **B4 D-1 / D-2 / D-3** (`docs/spikes/phase-6b/b4-general-export-observation.md`):
  export is corpus-wide, receipt task-attributed; **separate function + separate
  receipt per target** — the "ALSO"-clause (T3.10.2 L510) is **ratified by the owner
  as the separate-operation reading** (one `export` command writes one target; a
  general export does NOT cascade into `defects.jsonl`); the existing `export` CLI
  was extended (`--target` choices + dispatch branch), not replaced.
- **All five producers remain `planned`** (`telemetry/producers.json`): a generic
  CLI is not a trusted LOAD/HARVEST activation context (T3.12 ~L616). B5 must NOT
  flip a producer via any generic seam.

## Files touched

This session shipped subset #5 (`368c230`) and B4 (`d1e223d`); both committed, no
uncommitted work remains. B5 has touched nothing yet. Expected B5 surfaces (confirm
against §13.2 during planning): `telemetry/producers.json` (only if a real trusted
producer receipt legitimately activates one — likely still deferred), a release
evidence bundle (mirror the v2.0 RC bundle pattern under `docs/` or `handoffs/`),
`benchmarks/scorecard.jsonl` (closure line), an annotated tag (created **after** the
closure commit — see Traps).

## Verified gates

On `d1e223d` (Linux sandbox — `validate.py` false-reds on Windows on the `✓` print):
- `python3 scripts/validate.py` → `✓ all checks green` (RC 0)
- `python3 -m pytest scripts/tests -q` → `471 passed, 3 skipped`
- `ruff check .` → `All checks passed`; `git diff --check` clean
- `git check-attr text eol -- benchmarks/telemetry-v3.jsonl` → `text: set`, `eol: lf`
- No `*.sh` in the recent diffs → `bash -n`/`shellcheck` N/A. `mypy` report-only,
  not installed in-sandbox (non-blocking per R1).
- Sandbox deps: `pip install pytest pyyaml ruff --break-system-packages`; add
  `~/.local/bin` to `PATH`.

## Third-party tool risks

none reported (no external installer ran this session).

## Next steps

1. **Confirm clean start**: `cd D:\project\dat-kit && git status` on
   `feature/telemetry-v3-b3` at `d1e223d`; run the four gates above and confirm
   `471 passed, 3 skipped` before touching anything.
2. **Read the closure spec** before planning: `docs/contracts/telemetry-v3.md`
   T3.13 (~L648–666) — it enumerates the release-closure obligations verbatim: one
   real software-dev task AND one real knowledge-work task with human/agent/automation
   verdict sources distinguished; downgrade/disable verification; durable export
   (B4, done); schema freeze; full regression; rollback evidence; an approved RC;
   and a tag on the exact approved artifact. Cross-read `PLAN-v7-platform.md §13.2`
   (DoD Phase 6) and `PLAN-v8-refocus.md` §4 Phase E + §6 (gate tiers) + §9 (model).
3. **Study the precedent**: the v2.0 release closure is the pattern to mirror —
   `handoffs/SESSION-ORDER-2026-07-21-rc-bundle.md` and
   `handoffs/SESSION-ORDER-2026-07-22-step11-tag.md`, plus the two 2026-07-21
   lessons-learned entries about RC closure (DoD item closed on a non-existent
   receipt; tag cannot be cited from inside the tree it tags).
4. **Draft the B5 plan** (scratchpad, not a repo commit yet): decompose the T3.13
   obligations into ordered, receipt-bearing steps; classify the gate tier
   (schema-freeze / enforcement bits are Tier D → full reviewer chain). Decide
   whether the "one real software-dev + one real knowledge-work task with three
   verdict sources" can be satisfied without activating a producer (they likely can
   be observation/import receipts, since producers stay `planned` — confirm against
   T3.12/T3.13).
5. **Run the plan past `dat-kit:plan-reviewer`, fold findings, then STOP** for Dat's
   explicit approval. Do not edit release artifacts, freeze schema, or create a tag
   before approval.
6. After approval: execute per tier, append a `benchmarks/scorecard.jsonl` closure
   line and **re-run `validate.py` after the append**, then let Dat commit/push and
   cut the tag host-side.

## Traps

- **A tag/RC receipt closes in a commit made AFTER the irreversible act, never in
  the tree it applies to** (lessons-learned 2026-07-21, twice): a tag cannot be cited
  from inside the tree it tags; a DoD item whose receipt is the final act closes in a
  post-act commit. No placeholder whose filling depends on a later step.
- **`plan-reviewer` runs before every approval gate**, including a pre-written session
  order; a skip is declared to the owner, never silent (lessons 2026-07-21).
- **Scorecard append must re-run `validate.py`** after writing; `agent_runtime` is
  `"other"` for Cowork, never `"cowork"` (lessons 2026-07-21).
- **`validate.py` false-reds on Windows** via `UnicodeEncodeError` on `✓`/`❌` —
  run gates in the Linux sandbox; verify both pass AND fail print paths if that code
  is touched (lessons 2026-07-14).
- **A workflow file existing ≠ CI working; a local/rsync green ≠ a checkout green** —
  anything line-ending / `.gitattributes` / CI-related must be verified through a real
  `git clone -c core.autocrlf=true` and a real green Actions run before release
  (lessons 2026-07-13 & 07-20).
- **Reviewers stay sequential, diff-scoped, opus-pinned** (Class C — do NOT change
  `agents/*.md` model pins). `docs/spikes/**` is append-only; never edit a past
  observation file.
- **Producer activation needs a trusted context**, not a generic CLI (T3.12) — B5
  must not flip a producer from a generic seam.
- **No push creds in sandbox**; **`.git/index.lock`** may need host-side `del`.

## Glossary

telemetry-v3 T3.13 (release boundary) · DoD v7 §13.2 · lifecycle corpus
(`telemetry/events.jsonl`) · durable export (`benchmarks/telemetry-v3.jsonl`,
`benchmarks/defects.jsonl`) · producer (`planned`/`active`; trusted LOAD/HARVEST
context) · schema freeze · RC bundle · `benchmark_exported` receipt · Tier A–D gate
model (PLAN-v8 §6) · branch-strategy A · reports views (subset #5) · ALSO-clause
(D-2, separate-operation reading).
