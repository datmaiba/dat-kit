---
name: build-loop
description: The self-questioning build loop for spec-driven projects. Invoke on any request like "build phase N", "run the build loop", "continue the project", "preflight", "autopilot", or any feature work in a repo that has a spec/ directory. Enforces context load → self-questioning against the spec → plan → approval gate → build → verified checks → independent review → lessons harvest. Autopilot mode runs one up-front PREFLIGHT questionnaire (recorded in spec/08-decisions.md), then executes all phases without stopping except for high-severity questions. Delegated-build mode ("delegated build") makes the main session an orchestrator dispatching fresh builder subagents per task with two-stage review. Use this skill whenever the user wants to build features from a written spec, resume an interrupted build (reads the newest handoffs/ file first), or run a multi-phase project hands-off.
---

# build-loop — the self-questioning build loop

You are building a production project from a spec. Think like the senior engineer who wrote that spec: **generate the questions, answer them from the spec, and escalate only the genuinely unanswerable ones to the user.**

## Prerequisites

On every runtime, read root `AGENTS.md` first. It is the generated project's
canonical contract and routes to `docs/agent-workflow.md` and
`docs/agent-working-rules.md`. `CLAUDE.md`, `.claude/CLAUDE.md`, and
`.cursorrules` are compatibility pointers only; never treat runtime settings or
hooks as a second policy source.

The project must have: an `AGENTS.md` canonical contract (including architecture
rules + quality-gate commands through its linked docs) and a `spec/` directory
(vision, features, architecture, build phases — the numbering convention from
dat-kit's `project-init`: `00-vision` … `08-decisions`). Missing both? Suggest
running `/dat-kit:project-init` first. A partial spec is workable — say what's
missing and proceed with what exists.

## The review team

You are the **builder**. Independent reviewers keep you honest — never grade your own work when an independent grader exists. dat-kit ships three subagents (`plan-reviewer`, `qa-agent`, `code-reviewer`); if they are unavailable in this environment, substitute a fresh subagent with the same charter, or as a last resort a separate fresh-eyes pass — and say which substitution you made.

| Agent | Role | When |
|---|---|---|
| `plan-reviewer` | audits plans against spec (read-only) | step 3, before the approval gate |
| `qa-agent` | runs gates + attacks with edge cases | step 5, loops until PHASE DONE |
| `code-reviewer` | audits the diff against the rules | step 6, loops until APPROVE |
| `security-reviewer` | attacker's-eye audit of the diff (read-only) | step 6b — only when the phase touches security-relevant surfaces |

Inner loop per phase: **build → qa-agent → fix → qa-agent → code-reviewer → fix → (regression qa) → done**. Applies in BOTH normal and autopilot modes. Phases touching security-relevant surfaces (see step 6b) add security-reviewer after code-reviewer.

## PREFLIGHT — one-time whole-project questionnaire (before phase 0)

Goal: the user answers ALL decisions ONCE, up front — no mid-build interruptions.

**Trigger**: the user asks for preflight, OR an autopilot run starts and `spec/08-decisions.md` is missing or still marked `PREFLIGHT NOT RUN` (then preflight runs automatically first).

**Incremental preflight**: if `spec/08-decisions.md` exists but its `covers phases` range doesn't include the phases about to run, run preflight ONLY for the uncovered phases — one batch of new questions, append answers, update the range. Never re-ask what's already logged.

1. **Scan everything**: `AGENTS.md`, its linked `docs/agent-*.md`, ALL `spec/`
   files, `lessons-learned/`, and existing code state (`git log`, tree). Resolve
   `DAT_KIT_ROOT` from this skill and run
   `python "$DAT_KIT_ROOT/scripts/contract_check.py" --target .` to inventory
   every registered instruction entrypoint and runtime adapter. Stop PREFLIGHT
   on any named diagnostic (duplicate policy, missing/wrong-cased pointer,
   legacy contract, unsafe link, or dependency on a runtime adapter).
2. **Run the step-2 question lenses across EVERY phase** in the build-phases spec — not just the next one. Answer everything answerable from spec (with citations); keep only the genuinely unanswerable.
3. **Present ALL open questions in ONE batch**, grouped by phase. Each question gets: a numbered ID (`D-001`…), 2–3 concrete options, a recommended default, and one line on the consequence of each option. Wait for answers — this is the ONLY approval stop of the whole run.
4. **Write `spec/08-decisions.md`**: one row per decision — `ID | question | decision | rationale | source (user/auto) | date` — and set the status line to `PREFLIGHT DONE <date>, covers phases <range>`. This file is spec: later steps consult it before ever asking the user.

Preflight MUST also cover **taste choices** the spec leaves open — library picks, UI patterns, tooling — since autopilot won't stop at plan gates, this is the user's only chance to steer them.

## Severity rubric for NEW questions mid-run

Score every question that surfaces after preflight before anything stops:

**ASK THE USER (stop)** if ANY of: secrets/credentials/auth policy · irreversible or destructive data operations · deviation from spec · external services, cost, or sign-ups · public API contract or URL structure · production/deploy impact.

**AUTO-DECIDE (never stop)** otherwise — internal naming, file layout, dev-only tooling, anything reversible in <15 minutes. Pick the safest spec-consistent default, append it to `spec/08-decisions.md` with `source: auto`, and list all auto-decisions in the end-of-phase report.

## The loop (run in full for every phase or feature)

### 1. LOAD
Read: `AGENTS.md`, its linked `docs/agent-*.md`, the relevant `spec/` files for
this phase, `lessons-learned/lessons-learned.md` (if present), `CONTEXT.md` (if
present — the project glossary; use its terms verbatim in code, commits, and
reports), and the previous phase's code. Surface lessons-learned hits relevant
to this phase explicitly.

### 2. SELF-QUESTION (the core of this skill)
Generate questions across ALL these lenses, then answer each one **from the spec** with a citation (file + section). Only questions the spec cannot answer go to the user.

| Lens | Example questions to generate |
|---|---|
| Data | Which tables/entities/invariants does this phase touch? What cascades? What's nullable? |
| Contracts | Which endpoints/interfaces? Request/response shapes? Pagination contract? Versioning? |
| UX states | For every screen/surface: loading, empty, error, success? What happens on double-submit? |
| Domain invariants | Project-specific rules that must always hold (i18n fallbacks, currency rounding, tenancy isolation…) |
| Security | Auth? Rate limits? Sanitization of user content? Mass-assignment? Injection surfaces? For every new public endpoint that WRITES data, ask two SEPARATE questions: does it have its own rate limit, AND does the data it accumulates need a retention policy? (A rate limiter caps request speed, not unbounded storage growth.) |
| Edge cases | Collisions? Time-based state whose moment passes? Deleting a parent with children? |
| Reuse | Before writing a new data access/helper, does an existing method with the same purpose already exist (grep by domain)? When reusing one written for another feature, read its actual contract — never trust the name (it may carry looser assumptions, e.g. no status filtering). |
| Traps | Which known silent-failure traps apply (from `lessons-learned/` and the stack profile's traps file)? |
| Scope | What is explicitly OUT of this phase? |

Output format:
```
SELF-Q&A (answered from spec): [numbered — question → answer → citation]
OPEN QUESTIONS (for you): [only what spec AND spec/08-decisions.md cannot answer — with my recommended default]
```
Before listing an open question, check `spec/08-decisions.md` — if decided there, use that answer silently. Remaining open questions: apply the severity rubric — low-severity → auto-decide + log (`source: auto`); high-severity → ask and STOP. When the user answers, **record it in `spec/08-decisions.md`** so it's never asked again.

### 3. PLAN → plan-reviewer → STOP
Draft the plan: files to create/modify (grouped by area), endpoints with shapes, components with paths, test list, risks, demo steps. **Delegate to `plan-reviewer`** for an independent audit against the spec. Fix BLOCKERs, then present the plan **including the reviewer's verdict** and **stop for explicit approval**. Never bundle plan + code.

### 4. BUILD
Follow the architecture rules linked by the project's `AGENTS.md` exactly. Work
dependencies-first (data layer → domain → interfaces → tests, or the order the
stack profile prescribes). Commit-sized chunks with conventional-commit messages.

### 5. VERIFY → qa-agent (the inner loop)
**Delegate to `qa-agent`**: it runs ALL quality gates defined by the project's
canonical `AGENTS.md` contract — using exactly the commands written there (if
the project says docker-only, never fall back to host binaries) — AND attacks
the feature with spec edge cases. **A green gate proves nothing until you've
seen it fail**: whenever a phase ADDS or CHANGES a gate command itself,
deliberately introduce one error, confirm the gate goes red, revert — only then
trust its green (a no-op type-check once stayed green for six phases while
dozens of real errors accumulated). Verdict `RETURN TO BUILDER` → fix the
failing list → send back. **Repeat until `PHASE DONE`** (max 3 rounds; still
failing → stop and report). Then walk the phase's demo step from the
build-phases spec yourself.

### 6. REVIEW → code-reviewer
**Delegate to `code-reviewer`**: independent diff audit against the canonical
`AGENTS.md` contract and the stack profile. Verdict `RETURN TO BUILDER` → fix
findings → re-run **both** qa-agent (regression) and code-reviewer. Repeat
until `APPROVE`. Its LESSON CANDIDATES feed step 7.

### 6b. SECURITY → security-reviewer (conditional)
Trigger when the phase's diff touches ANY of: auth/session logic · user-supplied content (forms, markdown, comments) · file uploads or path handling · new public endpoints · permission changes · payment/money. Delegate to `security-reviewer` after code-reviewer approves. Verdict `RETURN TO BUILDER` (any CRITICAL/HIGH finding) → fix → re-run qa-agent (regression) + security-reviewer. Its LESSON CANDIDATES feed step 7. Phases touching none of those surfaces skip 6b — state the skip and the reason explicitly in the report, never silently.

### 7. HARVEST
Run in this exact order — the mechanical step comes FIRST so no approval pause can cut it off:

1. **Scorecard**: run the **scorecard** skill for this phase and capture the appended JSON line. This requires no approval and must never be placed after a step that can pause.
2. **Lessons**: propose lessons-learned entries for anything the user corrected or you caught yourself. Normal mode: write to `lessons-learned/` only after the user approves. Autopilot mode: appending is auto-approved (append-only, trivially reversible — low severity per the rubric); list the appended entries in the report instead of stopping. When a new lesson strengthens or supersedes an earlier entry, also add a one-line forward reference to that earlier entry (e.g. '→ superseded by <date> entry above') — a reader landing on the old entry must not trust a stale rule.
3. **Glossary**: if `CONTEXT.md` exists, propose one-line entries for any domain concept this phase forced you to describe in a sentence more than once (normal mode: after approval; autopilot: auto-append like lessons and list in the report). No candidates → skip silently.
4. If the `lesson-miner` tool is installed, remind the user to run its scan after the session; if not, skip silently.
5. **Print the 5-part wrap-up** — BOTH modes; the phase is not reported until all five parts are present: (1) done/fixed, numbered · (2) left intentionally, with reason · (3) remaining for the user — exact commands, dependency order · (4) concrete verification results per gate ("pest 24/24 ✓, tsc ✓") + auto-decisions logged this phase — never "everything works" · (5) the scorecard JSON line from item 1. End by stating what the next phase needs from this one.

## AUTOPILOT MODE

Activated ONLY when the user's request contains the word **"autopilot"**. Changes to the loop:

- **Preflight first**: if `spec/08-decisions.md` doesn't exist, run PREFLIGHT (the single approval stop), then proceed through all phases without stopping.
- Step 3 relaxes: present the plan, then **proceed without waiting** — UNLESS there's a HIGH-severity open question not covered by `spec/08-decisions.md`, or the plan deviates from spec (still stop).
- Phase transition REQUIRES: all gates green + the phase's demo verified (describe how; browser-only steps the user must do are listed and deferred, never skipped silently) + security-reviewer APPROVE when step 6b was triggered (an open CRITICAL/HIGH finding blocks the transition).
- Any check failure: fix up to 3 attempts, then STOP and report — never continue on red.
- **Long-running commands**: verify any wakeup/scheduling call actually SUCCEEDED before yielding the turn; if it errored, retry or fall back to a foreground wait. A yielded turn with no wakeup set kills the run silently.
- End of each phase: commit + run step 7 (HARVEST) in full — the **5-part wrap-up** including the scorecard line. Lessons are auto-appended per step 7.
- **Precedence**: during autopilot this skill wins over any plan-gate rule in the project's rules files; in normal mode the plan-gate applies unchanged.
- Context hygiene: if the session grows long, finish the current phase, print the report, and tell the user to start a fresh session with "autopilot from phase N+1" — don't degrade quality to avoid a restart. If the ceiling arrives MID-phase: finish the current commit-sized chunk, run the **handoff** skill, and tell the user to resume from the handoff file.

## DELEGATED-BUILD MODE (orchestrator + fresh builder per task)

Activated when the user asks for it ("delegated build", "delegate the build"), or during **autopilot** when a phase's plan exceeds ~5 tasks or the session is past roughly half its context — delegation is what keeps long runs from hitting the ceiling.

Changes to the loop — steps 1–3 and 7 are unchanged; steps 4–6 become:

- **The main session is the orchestrator and writes NO code.** After plan approval it splits the phase into commit-sized tasks (≤ ~30 min each, exact file paths, dependency order) and dispatches a **fresh builder subagent per task**.
- **Each task gets a builder brief** in the handoff-skill format (Goal / State / Decisions in effect / Files / Gates / Next steps / Traps / Glossary). The brief is the builder's ONLY context — write it so a cold reader succeeds; a vague brief is the orchestrator's failure, not the builder's.
- **Model per dispatch** (see `docs/model-selection.md`): default to leaving `model` unset so the builder inherits the orchestrator's tier. Set `model: sonnet` for a task that's pure scaffolding/pattern-following from a clear brief, or `model: opus` for a task that needs real architectural judgment — never `haiku` for a builder (implementation, unlike scouting, isn't mechanical enough). The review agents already run `model: opus`, matching their judge/verify role.
- **Two-stage review per task, in this order**: (1) **spec compliance** — the orchestrator checks the diff against the brief: everything asked, nothing beyond scope; (2) **code quality** — `code-reviewer` on the diff. Compliance first: quality-polishing the wrong thing wastes a round. Either stage fails → return to a FRESH builder with the brief plus the findings (max 2 retries per task, then STOP and report).
- **Consult before the final retry** (`docs/model-selection.md` → Escalation): when a task's first retry also fails, dispatch ONE read-only consult raised per-invocation to `opus`, with the failure bundle (brief, diff, verbatim gate/review output, approaches tried). Verdict `PLAN` → final retry runs the normal builder tier with the plan added to the brief; `TAKE_OVER` → final retry runs at the consult's tier. The consult does not consume a retry. Severity-rubric STOPs still go to the user — no consult answers an authority question. Log one line per consult to `benchmarks/escalations.jsonl`.
- **Gates still run per task** (builder runs them, orchestrator spot-checks the claim) and **qa-agent still runs once at phase level** after all tasks land — per-task green does not prove the tasks compose.
- Builders inherit the severity rubric: a HIGH-severity question inside a task bubbles up to the orchestrator, which applies the normal rules (ask/stop or auto-decide + log).

## Interrupted-session recovery (on every phase start)

Before step 2, determine whether this phase was already started:

0. If `handoffs/` exists, read the **newest** handoff file first — it is the previous session's compacted state and answers most of the questions below. Verify its claims against git rather than trusting blindly.
1. `git log --oneline -10` and `git status` — look for this phase's commits and uncommitted work.
2. Compare what exists on disk against the phase's scope in the build-phases spec.
3. Report a RESUME STATE: `fresh | partially built (list what exists) | built but unverified`.
4. NEVER rebuild what already exists and passes checks — continue from the first missing/failing item. Uncommitted half-done work: review against the plan, keep what conforms, fix what doesn't.
5. If prior context exists in the transcript, skip re-reading files already summarized.

## Hard rules

- Spec is law; disagreement = propose an amendment, never silently deviate.
- The user approves plans and spec changes (normal mode) — nothing else needs their time.
- A phase without green gates and a working demo is NOT done — no exceptions, in any mode.
