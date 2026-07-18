# PORTABLE HANDOFF — token discipline for plan-v7 execution (2026-07-18)

**How to use:** give this ONE file to the Claude/Codex session on any machine
(paste it, or drop it into `handoffs/`). It is self-contained: the session
follows §A immediately and applies §B to the repo working tree — no git
pull/cherry-pick needed, safe on a dirty tree. All §B patches are idempotent:
if the marker text already exists in the target file, SKIP that patch.

**Why:** two machines (Claude Fable 5 Pro, Codex 5.6) exhausted token budgets
executing plan v7. Measured worst offender: ONE parallel 3-agent review round
≈ 284k tokens (code 122k, security 94k, QA 68k) — each agent re-read nearly
the whole repo and read-only reviewers ran PoCs. These are execution-
discipline gaps, not plan flaws. Maintainer (Dat) approved this as a Class B
amendment, recorded as plan-v7 §16 (rev v7.1).

---

## §A — Rules in effect IMMEDIATELY (follow even before patching files)

1. **Sequential reviewers only.** Review order qa → code-reviewer →
   (conditional) security-reviewer → regression qa is a strict SEQUENCE.
   Never dispatch reviewers in parallel.
2. **Diff-scoped reviewers.** A reviewer reads ONLY the phase diff, the files
   it touches, and directly referenced contract/spec sections — never the
   whole repo. Every dispatch prompt MUST name the changed-file list and
   paste gate outputs so the reviewer verifies claims instead of
   re-discovering them.
3. **Findings-scoped re-reviews.** Review round 2+ verifies previous findings
   against the new diff only — never a fresh full review.
4. **No PoC outside qa-agent.** code-reviewer and security-reviewer are
   static-analysis only. Reviewer reports capped at ~30 findings lines.
5. **Session context protocol.** Executing phase N of plan v7: load
   `AGENTS.md` + linked docs, newest `handoffs/` file, plan §6 for phase N
   ONLY, §9, and this document. Do NOT read the whole plan or completed-phase
   sections.
6. **Main-thread economy.** Grep before Read; Read targeted line ranges of
   large files; never re-read a just-edited file; resume from handoffs, not
   tree re-discovery.
7. **Model tiering unchanged.** Reviewer `model:` pins stay as-is until v2.1
   per-reviewer evidence (Class C per plan §8/§11). Do not "optimize" pins now.
8. **No state re-audit.** Phase status = `git log --oneline -15` on the working
   branch + the newest `handoffs/` file, spot-checked — NEVER a full-repo audit
   to rediscover where execution stands (a full re-audit costs ~30k tokens and
   produces nothing the handoff doesn't already say).
9. **Scope-overflow protocol.** A reviewer that genuinely needs files beyond
   the diff + touched files STOPS and returns `SCOPE OVERFLOW: <files + why>`;
   the orchestrator grants or denies. Reading on silently is a charter
   violation.

**Reviewer dispatch template (use verbatim, fill the brackets):**

```text
Review scope — HARD LIMIT:
- Changed files: [paste `git diff --name-only <range>`]
- Diff: [range or attached]
- Gate outputs: [paste verbatim — verify claims, do not re-run except to confirm a suspected lie]
- Referenced contracts: [only the sections the changed files cite]
Read NOTHING outside this list. If you need more, return SCOPE OVERFLOW.
[Round 2+: Previous findings: [list]. Verify ONLY these against the new diff.]
Report: checklist + findings ≤30 lines + verdict.
```

**Host note:** on hosts without subagent charters (Codex), reviews are
fresh-eyes passes — §A applies to those passes identically; the canonical
source is `AGENTS.md` → `docs/agent-working-rules.md` (§B5), which both hosts
load.

---

## §B — Idempotent repo patches (apply once, on the working tree)

Apply with Edit/append. Skip any patch whose marker already exists. After all
patches: run `python scripts/validate.py` — must stay green (these are
markdown-only changes; no gate logic touched).

### B1. `agents/code-reviewer.md` — marker: `## Scope discipline`
Insert after the opening paragraph ("You are the code reviewer. ... no charity."):

```markdown
## Scope discipline (token budget — hard rules)

- Read ONLY: the phase diff, the files that diff touches, and the spec/contract sections those files directly reference. Never read the whole repository — the diff defines your scope.
- Static analysis only: never run PoCs, attack scripts, or the feature itself. Runtime verification belongs to qa-agent alone.
- On a re-review round, verify ONLY the previous findings against the new diff — no fresh full review.
- Report cap: findings ≤ ~30 lines. Fewer, denser findings beat exhaustive prose.
- Tripwire: if a correct review genuinely requires reading beyond the diff + touched files (e.g. a cross-cutting invariant), STOP and return `SCOPE OVERFLOW: <files needed + why>` instead of reading on — the orchestrator decides.
```

### B2. `agents/security-reviewer.md` — marker: `## Scope discipline`
Insert after the opening paragraph ("You are the security reviewer. ... no assumptions of good intent."):

```markdown
## Scope discipline (token budget — hard rules)

- Read ONLY: the phase diff, the files that diff touches, and the security-relevant contract/spec sections they directly reference. Never read the whole repository.
- Static analysis only: never run PoCs or live attacks — write the one-line exploit scenario instead. Runtime verification belongs to qa-agent alone.
- On a re-review round, verify ONLY the previous findings against the new diff — no fresh full review.
- Report cap: findings ≤ ~30 lines.
- Tripwire: if a correct review genuinely requires reading beyond the diff + touched files (e.g. tracing a taint path), STOP and return `SCOPE OVERFLOW: <files needed + why>` instead of reading on — the orchestrator decides.
```

### B3. `agents/qa-agent.md` — marker: `## Scope discipline`
Insert after the opening paragraph ("You are the QA agent. ... prove it wrong."):

```markdown
## Scope discipline (token budget — hard rules)

- Read ONLY: the phase diff, the files it touches, and the spec sections defining this phase's behavior — never the whole repository.
- After builder fixes, re-runs are findings-scoped: re-run the failed gates and failed attacks only; restart the full attack list only when the new diff touches new surfaces.
- Report cap: ATTACKS ≤ ~30 lines.
- Tripwire: if a correct attack genuinely requires reading beyond the diff + touched files, STOP and return `SCOPE OVERFLOW: <files needed + why>` instead of reading on — the orchestrator decides.
```

### B4. `skills/build-loop/SKILL.md` — marker: `**Review-cost rules (hard):**`
Insert directly after the "Inner loop per phase: ..." paragraph in "The review team":

```markdown
**Review-cost rules (hard):** reviewers run SEQUENTIALLY in the loop order — never in parallel (a parallel security review of a diff that code review then changes is wasted work). Every delegation prompt names the phase's diff scope (changed-file list) and pastes the gate outputs — the reviewer verifies claims instead of re-discovering them. Re-review rounds after fixes are findings-scoped, never fresh full reviews. Reviewers obey the scope-discipline block in their charters (diff-only reading, no PoC outside qa-agent, capped reports).
```

### B5. `docs/agent-working-rules.md` — marker: `## Token discipline`
Insert before the `## Traps` section:

```markdown
## Token discipline

- Grep before Read; Read targeted line ranges of large files, never whole files
  by default.
- Never re-read a file just edited or already summarized in this session.
- Resume from the newest `handoffs/` file instead of re-deriving state from the
  tree.
- Reviewer subagents run sequentially (never in parallel), read only the diff
  plus touched files, cap their reports, and re-review findings-scoped — per
  the scope-discipline blocks in `agents/*.md`.
- A session executing a plan phase loads only that phase's section plus the
  standing-discipline section — not the whole plan.
```

### B6. Plan v7 file (wherever it lives on this machine, e.g. `plans/PLAN-v7-platform.md`) — marker: `## 16. Amendment v7.1`
Append at end of file, and update the header line
`**Plan revision:** v7 (2026-07-17) ...` → `**Plan revision:** v7 (2026-07-17), amended v7.1 (2026-07-18 — §16 token discipline) ...`:

```markdown
## 16. Amendment v7.1 (2026-07-18) — Token discipline

Motivation: executing phases 0A–1B on two machines (Claude Fable 5 Pro,
Codex 5.6) exhausted token budgets prematurely. Measured worst offender: one
3-agent parallel review round ≈ 284k tokens — roughly 60-70% of a session.
Root causes were execution-discipline gaps, not plan-architecture flaws.

Standing rules (extend §9.1; Class B change, maintainer-approved 2026-07-18):

1. **Sequential reviewers only.** The §9.1 review order is a strict sequence.
   Running reviewers in parallel is forbidden — a parallel security review of
   a diff that code review then changes is wasted work.
2. **Diff-scoped reviewers.** A reviewer reads the phase diff, the files it
   touches, and directly referenced contract/spec sections — never the whole
   repository. The dispatching prompt MUST name the changed-file list and
   paste the gate outputs so the reviewer verifies claims instead of
   re-discovering them.
3. **Findings-scoped re-reviews.** Round 2+ verifies the previous findings
   against the new diff only — never a fresh full review.
4. **Charter enforcement.** code-reviewer and security-reviewer are
   static-analysis-only (no PoC, no runtime attacks — those are qa-agent's
   alone). Reviewer reports are capped: findings ≤ ~30 lines.
5. **Session context protocol.** A session executing phase N of this plan
   loads: `AGENTS.md` + its linked docs, the newest `handoffs/` file, §6 for
   phase N only, §9, and this amendment. It does NOT read the whole plan or
   sections for phases already completed.
6. **Main-thread economy.** Grep before Read; Read targeted line ranges of
   large files; never re-read a just-edited file; resume from handoffs, not
   tree re-discovery.
7. **Model tiering stays deferred** per §11: reviewer `model:` pins change
   only on v2.1 per-reviewer evidence (Class C). This amendment does not
   change any pin.

Phase 4 must carry rules 1–4 into the software-dev and knowledge-work
`reviewers.md` slots via the ownership map, so the discipline survives the
cutover.
```

### B7. `lessons-learned/lessons-learned.md` — marker: `2026-07-18 — One review round burned 284k`
Insert as the newest entry (right after the first `---`):

```markdown
### 2026-07-18 — One review round burned 284k tokens (~65% of a session) by ignoring three existing rules

- **What happened**: during plan-v7 execution, three reviewer subagents (code 122k, security 94k, QA 68k) ran in PARALLEL, each re-read nearly the whole repo (registry.py ~900 lines, all contracts, tests), and the read-only reviewers ran their own PoCs. Token exhaustion hit two machines/accounts (Claude Fable 5 Pro, Codex 5.6) before phases could finish.
- **Root cause**: charters said "scope the diff" descriptively but did not forbid whole-repo reads; the sequential review order was stated but parallel execution was not explicitly banned; "read-only analysis" was not enforced as "no PoC". A rule a subagent can profitably ignore is a description, not a rule.
- **Rule**: reviewers run sequentially, read only the diff + touched files, cap reports at ~30 findings lines, re-review findings-scoped, and never run PoCs outside qa-agent. Dispatching prompts must name the diff scope and paste gate outputs. See PLAN-v7 §16 and the scope-discipline blocks in `agents/*.md`.

---
```

---

## §C — After patching

1. `python scripts/validate.py` → must be green (markdown-only changes).
2. Commit on the CURRENT branch with the rest of the WIP when convenient:
   `feat(v7.1): token-discipline amendment — sequential diff-scoped reviewers, session context protocol`.
   (Both machines applying this file independently converge on the same
   content; whichever pushes first wins, the other's git merge is trivial.)
3. **Cache trap:** if reviewer agents run from an INSTALLED dat-kit plugin
   (not this repo checkout), the charters are cached — reinstall/update the
   plugin + fresh session before the new rules take effect.
4. Continue plan-v7 execution under §A. Expected effect: review round
   ~284k → ~80–100k; session bootstrap no longer reads the ~1000-line plan;
   re-review rounds ↓ ~70%.
