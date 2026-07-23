# HANDOFF 2026-07-23 — B3 subset #1 execution context (scorecard/HARVEST producer)

## Goal

Execute Phase 6B **B3 subset #1 only**: build the build-loop HARVEST producer
(`lesson_candidate_recorded` + task lifecycle emission wired into the
scorecard HARVEST step), its status registry, tests, and observation
pre-registration. **The producer ends this subset in status `planned`, NOT
`active`** — activation requires a real live-instrumented HARVEST receipt
from a later task and is out of scope here. Subsets #2–#5 (diagnosing-bugs,
knowledge-work footer, task/handoff linkage, reports) must not start without
separate approval.

## Approval provenance

- Plan drafted 2026-07-23 under Fable-5 discipline; independent
  `plan-reviewer` returned **REPLAN** with 3 blockers + 3 warnings; all six
  were incorporated (see Decisions below).
- Maintainer (Dat) **approved the revised plan and all recommended decisions**
  on 2026-07-23 ("duyệt theo đề xuất"). This satisfies the plan-approval gate
  for this subset. No further approval stop is needed before build — the next
  mandatory stops are the reviewer verdicts and the end-of-subset report.

## Runtime / model

- Builder: **Codex** (maintainer's call). Safe because this subset is
  producer-side wiring only — see the hard scope fence below.
- Reviewers: unchanged current pins (per RE-v3 binding rule: no reviewer
  model change until Telemetry v3 evidence).
- **Hard scope fence (makes Codex safe here): this subset MUST NOT modify
  `_WRITE_LOCK`, `_append_local_event`, `ProducerWriter._append`, or any
  locked/strict-tail/corpus-check internals in `scripts/telemetry.py`.** The
  producer calls the existing public B1/B2 surfaces
  (`TelemetryStore`/`ProducerWriter.append`, or the CLI) only. If the work
  seems to require touching those internals, STOP and REPLAN — that would be
  Fable-5-tier concurrency work not authorized for this subset.

## Workflow

`dat-kit:build-loop` with the software-development Domain Pack, red-before-
green, per-slice review chain (QA → code review → security review — security
triggers because the diff touches producer authority surfaces), one full-gate
run at freeze, `dat-kit:handoff` at any mandatory stop. Resume protocol: this
file is the newest handoff; verify its claims against git before trusting.

## Canonical contract

`dat-kit 1.16.0` (root `AGENTS.md` → `docs/agent-workflow.md`,
`docs/agent-working-rules.md`, `lessons-learned/lessons-learned.md` — READ the
2026-07-23 entries; two of them are load-bearing for this subset).

## Git state

- `master` @ `d8058ec` — PR #4 merged; B0–B2 complete on master
  (B2 candidate `bd4e844`, closure `a6d76e6`, reconcile `3b1914e`,
  Stage-A evidence `3ade01e` all in master history).
- `feature/telemetry-v3` @ `3ade01e` — fully merged into master; do not build
  on it. **Create a fresh branch off `master` (`d8058ec`), suggested name
  `feature/telemetry-v3-b3`.**
- Preserve, never stage/modify/delete, the user-owned untracked provenance
  files under `handoffs/` and `plans/` (currently 8 such files).
- CI note: `.github/workflows/ci.yml` on master already has `fetch-depth: 0`
  on all three jobs and the bounded Windows test-node IDs — do not revert.

## Spec sources (load these, not the whole history)

1. `docs/contracts/telemetry-v3.md` — T3.12 (producers + status
   truthfulness), T3.5.1 (coverage/terminal reasons), T3.6 (task identity),
   T3.9 (no secret echo), T3.11 (disable/degraded semantics), event payload
   table (`lesson_candidate_recorded`). T3.10.1 (`scorecard_imported` legacy
   import) is **B4 scope — do not implement it**.
2. `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md` — B3
   section: five producers, dependency order, receipt matrix, per-slice
   review protocol.
3. `docs/spikes/phase-6b/b2-observation.md` — the observation-doc pattern to
   replicate for `b3-observation.md`.
4. B2 producer surfaces in `scripts/telemetry.py`: `_cli_policy`,
   `_cli_writer`, `_new_event`, `validate_lifecycle_events`,
   `_append_lifecycle_event` (call sites only — see the scope fence).

## Decisions in effect (all maintainer-approved 2026-07-23)

| ID | Decision |
|---|---|
| D-B3-1 | Producer status registry lives in **`telemetry/producers.json`** (new file under the already-owned `telemetry/**` glob, governance Class B). NOT in `registry/evolution.json` (that is Class C — rejected). Shape: five producers, each `planned|active`, `active` requires the activating receipt `event_id`. This subset writes all five as `planned`. |
| D-B3-2 | Subset #1 = **live HARVEST emission** during a real scorecard HARVEST step. Legacy import (`scorecard_imported`, T3.10.1) is B4 — out of scope. |
| D-B3-3 | Line budget: **~500 combined product+test added lines**; STOP + REPLAN when approaching it, or if the work needs new architecture / schema change / append-internals change / another subset's wiring. |
| D-B3-4 | Producer code lives in **`telemetry/producers.py`** (new module under `telemetry/**`, Class B). NOT `scripts/telemetry_producers.py` (orphan path — `EVOLUTION_ORPHAN_PATH`, rejected). NOT appended into `scripts/telemetry.py`. |
| D-B3-5 | **Producer stays `planned` at the end of this subset.** Activation happens only when a later real build-loop HARVEST runs live through this wiring and produces a validated `lesson_candidate_recorded` receipt (T3.12: prose/fixtures/synthetic events cannot activate). Do NOT backfill events from existing `lessons-learned.md` prose — that is a synthetic receipt (violates T3.6 task-minted-at-LOAD and T3.1 no-retroactive-history). |

## Files to create/modify (exact scope)

1. `telemetry/producers.py` (NEW) — producer-side helper: given a repository
   root, drive a task lifecycle (start → `lesson_candidate_recorded` →
   finish) through the existing B1/B2 public surfaces. `kit_facing` handling:
   caller supplies the root-cause locus; the helper enforces `kit_facing=true`
   ONLY for the closed set {dat-kit skill, template, gate} (T3.12) — agents,
   reviewer charters, CI, git, host behavior are all `kit_facing=false`.
   `root_cause_ref` / `candidate_ref` are stable-refs (T3.3.1 grammar,
   `evidence:*`), never prose titles.
2. `telemetry/producers.json` (NEW) — status registry per D-B3-1; all five
   producers `planned`.
3. `scripts/scorecard.py` (MODIFY) — after a successful scorecard append,
   invoke the helper. Honors `DAT_KIT_TELEMETRY=off` (emit nothing, exit
   clean); any telemetry failure is non-blocking degraded — the HARVEST/
   scorecard flow must NEVER break because telemetry failed. **After the
   telemetry append, re-run the consuming validator** (the 2026-07-21
   scorecard lesson: a write succeeding is not the write being valid).
4. `scripts/tests/test_telemetry_producers.py` (NEW) — **red-before-green**,
   capture the red receipt before implementing:
   - lifecycle correctness: start → lesson_candidate_recorded → finish, one
     task ID, coverage `partial` (build-loop requires gate_result +
     review_result which HARVEST alone does not emit — expect partial, never
     claim full);
   - `kit_facing` gate: true for skill/template/gate loci; **false** for
     agent-charter, CI, and git loci (negative cases);
   - stable-ref validation: prose in root_cause_ref/candidate_ref rejected;
   - disable path: `DAT_KIT_TELEMETRY=off` → no file created, scorecard append
     still succeeds;
   - degraded path: telemetry target unavailable → scorecard append still
     succeeds, structured degraded result;
   - status registry: `producers.json` validates, all five `planned`, and a
     guard test that `active` without a receipt event_id is rejected.
5. `docs/spikes/phase-6b/b3-observation.md` (NEW) — pre-register the B3
   observation BEFORE the first product edit (mirror b2-observation.md:
   observation task ID minted via UUIDv4, immutable scope, threat model rows
   for the new surface, acceptance criteria, ledger schema). One observation
   ID covers all of B3; subsets are internal candidates.
6. If `validate.py` needs to learn the new `telemetry/producers.json`
   invariants, extend its checks — and prove red-before-green by breaking the
   file once (a green gate proves nothing until you've seen it fail).

## Canonical order

Pre-register observation → red tests → implement (one batched round) →
full gates ONCE at freeze → adversarial self-check → QA (PHASE DONE) →
code review (APPROVE) → security review (APPROVE — producer authority
surface) → observation ledger append → scorecard skill append + re-run
validator → 5-part report → STOP (no subset #2).

## Gates (from repo root; 120s timeouts, no short probes)

```text
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
git diff --check
```

Name your executable paths in the QA packet up front (B2 QA burned four
invocations on executable discovery).

## Token-economy / stop controls

- Reviewer packets ≤ ~2.5 KB per finding-set (budget scales with finding
  count, ~800 bytes/finding — 2026-07-23 lesson); dispatch sequentially,
  never parallel.
- Tokens `unknown` unless the runtime exposes attribution; never estimate.
- Mandatory checkpoint at 70% remaining context; if the ceiling arrives
  mid-build, finish the commit-sized chunk, run `dat-kit:handoff`, resume
  from that file.

## Traps

- **The scope fence is the trap that matters**: no edits to locked-append
  internals. Wire through public surfaces only.
- Do not activate the producer from this subset's own test events — tests are
  synthetic by definition (D-B3-5).
- The 2026-07-23 "pinned reviewer" lesson looks like a kit_facing=true case
  but is NOT (root cause = agent charter, outside the T3.12 closed set). Use
  loci, not vibes, to classify.
- Coverage for a HARVEST-only lifecycle is `partial` — asserting `full`
  anywhere is a spec violation, not a nicety.
- `telemetry/.gitignore` currently ignores runtime artifacts under
  `telemetry/` — check it does not accidentally ignore `producers.py` /
  `producers.json`; adjust narrowly if so (never widen).
- Windows/Ubuntu CI both run the suite: keep parametrize IDs short
  (PYTEST_CURRENT_TEST 32,767-char env-var cap on Windows — 2026-07-23
  lesson), and pin any new text files' line endings if byte-compared.
- Do not put future review verdicts inside the reviewed artifact; append
  scorecard only after all verdicts and re-run its validator.

## Glossary

- **subset #1** — scorecard/HARVEST producer slice of B3; one committed,
  independently reviewed candidate.
- **producer status registry** — `telemetry/producers.json`; truthful
  `planned|active` per T3.12.
- **activation receipt** — a validated `lesson_candidate_recorded` emitted by
  a real, live HARVEST task through this wiring; the only thing that may flip
  `planned → active` (in a later, separately approved change).
- **scope fence** — the prohibition on touching locked-append internals in
  `scripts/telemetry.py` during this subset.
