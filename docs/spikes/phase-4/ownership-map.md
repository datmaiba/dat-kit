# Phase 4a — line-level ownership map (read-only; NO lines move in this slice)

**Scope:** every substantive line of the files below → exactly ONE destination:
`engine` | `domain-pack` | `project-contract` | `maintainer-policy` | `retired-with-reason`.
This map is the pre-move tripwire input for slices 4b–4f. Written against HEAD `7fff212`.

## Conventions

1. **Line ranges** refer to the file at HEAD `7fff212`. Blank lines and pure headings
   ride with the block that follows them.
2. **`engine` assignments map semantics, not vocabulary.** Where a line's *mechanism*
   is domain-neutral but its *wording* carries software tokens, the map assigns `engine`
   only if the note lists the mandatory neutral rewording for 4b. A line whose semantics
   (not just words) need software knowledge must NOT be `engine` — that is the tripwire.
3. **`domain-pack` assignments name the target slot** (workflow · ground-truth · gates ·
   reviewers · deliverables · loop-profile) and the pack (sw = software-dev, kw = knowledge-work).
4. **Sanctioned duplication (the only one):** plan §16 mandates rules 1–4 land in BOTH
   packs' `reviewers.md`. Category is still single (`domain-pack`); see §Map-§16 below.
5. Engine phase naming: 4b writes `engine/work-loop/ENGINE.md` as **LOAD → SELF-QUESTION →
   PLAN → EXECUTE → VERIFY → REVIEW → REPORT → HARVEST**. knowledge-work's A→G names
   (clarify…harvest) are that same sequence; 4d's workflow.md keeps A→G labels but must
   declare the phase correspondence so the engine deletion test (4f) can key on it.

---

## 1. skills/build-loop/SKILL.md (184 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–4 | frontmatter: name + trigger description | domain-pack (sw · descriptor) | Regenerated as rendered thin trigger from `registry/domains.json` descriptor in 4c; prose not moved verbatim. |
| 6–8 | title + "think like the senior engineer… escalate only unanswerable" | domain-pack (sw · workflow) | Software persona framing. Engine states the abstract escalate-only-unanswerable principle in its SELF-QUESTION phase (4b, fresh text). |
| 10–16 | Prerequisites: read root AGENTS.md; CLAUDE.md/.cursorrules are pointers | engine | LOAD phase: "read the project's canonical contract; runtime files are compatibility adapters, never a second policy source." Host- and domain-neutral as written. |
| 18–23 | requires spec/ dir, project-init numbering, partial-spec handling | domain-pack (sw · ground-truth) | spec/00–08 structure is software-dev's ground truth. "Say what's missing and proceed" generalizes — engine may restate abstractly (4b, fresh). |
| 25–27 | review team intro: never grade your own work; subagent substitution | domain-pack (sw · reviewers) | The principle "never grade your own work when an independent grader exists" is engine REVIEW-phase text (4b, fresh); the three named subagents + substitution protocol are sw reviewer policy. |
| 29–34 | reviewer table (plan-reviewer / qa-agent / code-reviewer / security-reviewer) | domain-pack (sw · reviewers) | The sw review team, roles, and step bindings. |
| 36 | inner loop order build→qa→fix→qa→code-reviewer→…; security add-on | domain-pack (sw · reviewers) | Sequential order is also §16 R1 — see §Map-§16. |
| 38 | Review-cost rules (sequential, diff-scoped, findings-scoped, charters) | domain-pack (BOTH packs · reviewers) | §16 rules 1–4; the sanctioned duplication. See §Map-§16. |
| 40–62 | PREFLIGHT: trigger, incremental preflight, contract_check.py inventory, question batch, spec/08-decisions.md format, taste choices | domain-pack (sw · workflow) | Deeply bound to spec/08-decisions.md and dat-kit contract_check. Engine carries only the abstract "single up-front approval stop" mode concept (4b, fresh). |
| 64–70 | severity rubric (ASK vs AUTO-DECIDE lists, logging) | domain-pack (sw · workflow) | Trigger list carries software items (public API contract, deploy) and the spec/08-decisions.md binding. Engine 4b writes a domain-neutral escalation rubric (severity classes, ask/auto-decide/log-and-report); each pack supplies its concrete trigger list and log target. |
| 72 | "The loop (run in full for every phase or feature)" | engine | The invariant loop header; engine owns the phase sequence. |
| 74 | "### 1. LOAD" heading | engine | Phase name. |
| 75–79 | LOAD read-list: AGENTS.md, docs, spec/, lessons-learned, CONTEXT.md, previous code | domain-pack (sw · ground-truth) | The sw read-list. Engine LOAD says "read the pack's ground-truth sources + canonical contract + lessons + glossary" (4b, reworded per convention 2). |
| 81–82 | SELF-QUESTION: generate across lenses, answer from spec w/ citation, only unanswerable escalate | engine | Mandatory rewording (4b): "from the spec" → "from the pack's ground-truth sources". Mechanism is domain-neutral. |
| 84–94 | lens table (Data/Contracts/UX/invariants/Security/Edge/Reuse/Traps/Scope) | domain-pack (sw · workflow) | The sw question lenses. Engine requires "the pack declares its lenses" (4b, fresh). |
| 96–100 | SELF-Q&A / OPEN QUESTIONS output format | engine | Reword "answered from spec" → "answered from ground truth". Generic escalation format. |
| 101 | check spec/08-decisions.md first; record answers there | domain-pack (sw · workflow) | Decision-memory binding to spec/08-decisions.md. Engine states abstract "never re-ask a logged decision; record new ones" (4b, fresh). |
| 103–104 | PLAN → independent plan review → STOP for approval; never bundle plan + code | engine | Reword: "plan-reviewer" → "the pack's plan reviewer, when it declares one"; "code" → "execution". sw reviewers.md binds plan-reviewer; kw phase B outline has no plan reviewer — engine makes the reviewer binding pack-optional. |
| 106–109 | BUILD: architecture rules, dependencies-first, conventional commits | domain-pack (sw · workflow) | Git/commit conventions and stack-profile order are sw policy (plan §6 names them explicitly). |
| 111–122 | VERIFY: qa-agent delegation, gates exactly as contract writes them, red-green gate proof, max 3 rounds, demo walk | domain-pack (sw · workflow) | qa-agent, docker-only example, type-check anecdote, demo walk = sw. Engine VERIFY carries abstract "gates run exactly as the contract declares; a changed gate must be seen red before its green is trusted; bounded retry then stop" (4b, reworded fresh). |
| 124–128 | REVIEW: code-reviewer delegation, regression re-run, APPROVE loop | domain-pack (sw · workflow) | Charter lives in sw reviewers.md. Engine REVIEW: "independent reviewer per pack charter; loop until approve; re-reviews findings-scoped" (4b). |
| 130–131 | 6b security-reviewer trigger surface list; explicit-skip rule | domain-pack (sw · reviewers) | Surface list is software. The "state the skip and reason explicitly, never silently" clause is engine REPORT material (4b, fresh). |
| 133–140 | HARVEST: mechanical-first ordering, scorecard, lessons (mode-dependent approval), glossary, lesson-miner, 5-part wrap-up | engine | Domain-neutral harvest/report protocol. Mandatory rewording (4b): "phase" → "task"; drop the software example "(pest 24/24 ✓, tsc ✓)" → neutral example; scorecard skill is domain-neutral. |
| 142–144 | AUTOPILOT activation keyword + mode concept | engine | Mode activation and semantics are loop-level. |
| 146–148 | autopilot: preflight-first, plan-gate relaxation vs spec/08-decisions, phase-transition requirements (gates+demo+security APPROVE) | domain-pack (sw · workflow) | All three lines bind spec/08-decisions.md / demo / security-reviewer. Engine states abstract "hands-off mode still stops on high-severity questions; transitions require the pack's gates green" (4b, fresh). |
| 149 | fail-fix ≤3 attempts then STOP; never continue on red | engine | Neutral as written. |
| 150 | verify wakeup/scheduling calls succeeded before yielding | engine | Host-neutral long-run rule. |
| 151 | end-of-phase commit + full HARVEST | domain-pack (sw · workflow) | "Commit" is sw; the HARVEST-always-runs rule is already engine via 133–140. |
| 152 | precedence: skill over project plan-gate during autopilot | engine | Composition/contradiction rule for 4b. Mandatory rewording: "this skill wins over any plan-gate rule" → "in hands-off mode the engine's single-up-front-approval rule overrides any per-step plan-approval gate declared by the project contract; in attended mode the project's gate applies unchanged" (the plan gate is a project-contract concept — templates/common/docs/agent-working-rules.md.tpl L33–38 — not software semantics). |
| 153 | context hygiene: finish phase, restart session; mid-phase ceiling → handoff skill | engine | Session/context policy. Mandatory rewording: "phase" → "task"; "commit-sized chunk" → "the smallest self-contained unit of work the pack defines" (sw instantiates it as a commit-sized chunk in workflow.md). |
| 155–157 | DELEGATED-BUILD activation + auto-activation thresholds | domain-pack (sw · workflow) | Delegation mode is shipped as sw policy; engine abstraction of delegation is explicitly OUT of Phase 4 scope (no map line assigns it). |
| 159–167 | orchestrator writes no code; builder briefs; model tiering; two-stage review (compliance→quality); consult-before-final-retry; per-task gates + phase-level qa; severity bubble-up | domain-pack (sw · workflow) | Two-stage review order and consult escalation reference docs/model-selection.md, code-reviewer, benchmarks/escalations.jsonl — all sw. Brief format reuses handoff skill (engine-adjacent but pack-bound here). |
| 169–171, 173 | recovery: determine already-started; read newest handoff first; verify its claims against reality | engine | Resume-from-handoff protocol is domain-neutral (reword "phase" → "task", "against git" → "against the working tree/record"). |
| 174–178 | git log/status checks, disk-vs-spec compare, RESUME STATE vocabulary, never rebuild what passes, keep-conforming-halfwork, skip re-reading summarized files | domain-pack (sw · workflow) | Git mechanics + build-phases spec. Line 178 (context economy) is engine (4b, fresh restatement). RESUME STATE vocabulary may be restated neutrally by engine; sw keeps the git instantiation. |
| 180–183 | Hard rules: spec is law / amendments not silent deviation; user approves plans + spec changes only | engine | Reword "spec" → "the governing spec/brief". Authority rules are loop-level. |
| 184 | phase not done without green gates + working demo | domain-pack (sw · gates) | "Working demo" is sw's done-criterion. Engine states "a task is not done until the pack's gates pass" (4b, fresh). |

## 2. skills/build-loop/loop-profile.md (25 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–25 | entire file: advisory note, per-task loop table, Goal ceiling + reasoning | domain-pack (sw · loop-profile) | Migrates wholesale to `domains/software-dev/loop-profile.md` (4c). Ceiling `Goal` mirrored in descriptor `loop_ceiling` (already true in registry/domains.json). L23's validate.py/runners note stays as-is (deferred-work pointer, not policy). |

## 3. skills/knowledge-work/SKILL.md (49 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–15 | frontmatter: name + trigger description | domain-pack (kw · descriptor) | Regenerated as rendered thin trigger from descriptor in 4d. |
| 17, 19 | one physical paragraph (L19; L17 is the title, L18 blank) carrying three clauses — DECLARED clause-level split, one destination per clause: | — | — |
| 19a | "This is a dat-kit Domain Pack: it teaches the working loop what 'knowledge work' means." | domain-pack (kw · workflow) | Pack self-description; opens workflow.md (4d). L17 title rides with it. |
| 19b | invariant-loop sentence "clarify → decompose → ground-truth → execute → verify → report → harvest — this pack fills in what each phase means" | engine | The invariant-loop sentence IS the engine sequence; 4b owns it under LOAD→…→HARVEST names with the A→G correspondence declared (convention 5). |
| 19c | "Contract files live beside this one." (validate.py sentence-marker) | retired-with-reason | Sentence-marker pack detection is replaced by registry conformance in 4f (plan §6). Marker must SURVIVE 4a–4e and retire only at the 4f cutover commit. |
| 21–29 | five-slot contract table | retired-with-reason | Per-pack restatement of the pack contract. Canonical slot definition lives in the domain-pack contract + descriptor after 4b; restating it per pack is drift risk (Phase 3 FU-1 territory). |
| 31–45 | A→G playbook (Clarify, Decompose, Ground truth, Execute, Verify, Report, Harvest) | domain-pack (kw · workflow) | Plan 4d: "workflow.md absorbs the A→G playbook." Phase E's "you do not grade your own claims" mirrors engine REVIEW; stays kw-flavored here. |
| 47–49 | Loop ceiling: Goal (human-run), G2 reasoning, never Time/Proactive | domain-pack (kw · loop-profile) | Consolidate with existing loop-profile.md; descriptor `loop_ceiling: Goal` mirrors it (4d). |

## 4. skills/knowledge-work/gates.md (51 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–51 | entire file: G1–G6 with worked cases, gaming lines, ceilings; domain-ceiling summary | domain-pack (kw · gates) | Migrates wholesale (4d). L3 cross-ref "per domain-builder's validity rule" → update to the rewritten domain-builder/contract location. L5 practitioner-sign-off provenance note stays (it is the gates' validity evidence). |

## 5. skills/knowledge-work/ground-truth.md (24 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–24 | entire file: source priority, before-writing checklist, red flags | domain-pack (kw · ground-truth) | Migrates wholesale (4d). No engine leakage: "primary over summary, current over remembered" is quoted by domain-builder as an example but owned here. |

## 6. skills/knowledge-work/loop-profile.md (18 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–18 | entire file: advisory header, per-task loop table, why-not-higher | domain-pack (kw · loop-profile) | Migrates wholesale (4d); absorbs SKILL.md 47–49. L18 runners/ deferral pointer stays. |

## 7. skills/knowledge-work/reviewers.md (20 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–20 | entire file: fact-checker charter, per-claim checks, SOURCED verdict, never-list | domain-pack (kw · reviewers) | Migrates wholesale (4d) AND gains §16 rules 1–4 (see §Map-§16). Existing text already covers R4-static ("Read-only") partially; R1–R3 and the report cap are additions. |

## 8. skills/knowledge-work/deliverables/ (2 files, 48 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| report.template.md 1–26 | report template + verification record | domain-pack (kw · deliverables) | Wholesale (4d). |
| fact-check.template.md 1–22 | fact-check template + verdict vocabulary | domain-pack (kw · deliverables) | Wholesale (4d). Phase 6 adds the machine-readable footer — out of Phase 4 scope. |

## 9. docs/loops.md (46 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–5 | intro, two axes, ADR 0001 pointer | engine | Loop model is engine documentation. |
| 7 | domain axis: five-slot list + "software-dev (the build-loop skill)" | engine | Mandatory rewrite (4b/4f): five slots → six-slot contract; pack locations → `domains/`; trigger names from registry. |
| 9–18 | loop axis: the four loop types table | engine | As-is. |
| 20–33 | capability ladder: gate validity, prerequisites table, human-run gates, high-risk notify-only cap | engine | As-is. The kw G2 example on L31 is illustrative, not kw policy — stays as an example. |
| 35–42 | how to choose a loop | engine | As-is. |
| 44–46 | scope boundary: practitioner-authored domains only; dat-kit runs nothing on a schedule | engine | Platform authoring constraint documented with the loop model; enforced operationally by the rewritten domain-builder (4e). |

## 10. skills/domain-builder/SKILL.md (87 lines)

| Lines | Content | Destination | Note |
|---|---|---|---|
| 1–15 | frontmatter: trigger description (five-slot contract, gate-validity, Turn/Goal cap) | engine | Rewritten in 4e: five-slot → descriptor + six slots + rendered trigger + inherited evolution profile. Semantics (practitioner rule, validity check, interview cap) survive. |
| 17–19 | what a Domain Pack is; scribe-not-expert stance | engine | 4e rewrite carries it. |
| 21–23 | hard rule: only encode practiced domains | engine | Canonical statement rides with docs/loops.md scope boundary (§9 L44–46); domain-builder references, not restates, after 4e — dedup noted. |
| 27–37 | five-slot contract table + "Contract files live beside this one" marker rule (L37) | retired-with-reason | Superseded by the six-slot contract + registry conformance (4e/4f). L37's marker mechanism retires with the 4f detection cutover; until then validate.py still keys on it. |
| 39–51 | process step 1: practitioner interview questions | engine | 4e rewrite keeps the interview; adds descriptor + evolution-profile questions. |
| 53–62 | step 2: gate-validity check (worked cases, gaming line, human-needed, sign-off) | engine | Core platform rule; unchanged semantics in 4e. |
| 64–72 | step 3: loop ceiling / capability ladder application | engine | Duplicates the ladder in docs/loops.md — after 4e domain-builder applies the ladder and cites docs/loops.md as canonical (dedup note). |
| 74–76 | step 4: write the pack (five files, marker sentence) | retired-with-reason | Instructions to write the FIVE-slot layout + marker are superseded by 4e's descriptor + six-slot + rendered-trigger authoring. Replacement is a rewrite, not a move. |
| 78–80 | step 5: confirm and hand over; ceiling-raise entry condition | engine | 4e rewrite keeps; adds registry registration step. |
| 82–87 | rules for every pack (checkable gates, why-over-rule, no automation from interview, no decorative packs) | engine | 4e rewrite keeps verbatim in spirit. |

## 11. Reviewer charters — agents/*.md (code-reviewer, qa-agent, security-reviewer, plan-reviewer)

Not in 4a's mandated move-map list; recorded for completeness, no line moves here:
the four charters are software-dev reviewer assets. Their ownership rides with
**domain-pack (sw · reviewers)** — 4c decides whether they relocate under the pack or stay
in `agents/` referenced by `domains/software-dev/reviewers.md` (either way, reviewers.md
is the binding surface). Their "Scope discipline" blocks already carry §16 rules 2–4;
§16 R1 (sequencing) is an orchestrator rule and lives in reviewers.md, not the charters.

## 12. Related templates (generated projects)

| Lines | Content | Destination | Note |
|---|---|---|---|
| templates/common/AGENTS.md 1–19 | generated canonical contract; "dat-kit 1.16.0" revision marker (L3); build-loop pointer (L18–19) | project-contract | Stays a template. 4f flips the revision marker → "dat-kit 2.0" and re-derives the trigger name from the registry. |
| templates/common/docs/agent-workflow.md 1–18 | runtime-adapter rules for generated projects | project-contract | As-is. |
| templates/common/docs/agent-workflow.md 20–25 | build workflow: run build-loop skill; loop phase list | project-contract | 4f re-derives the trigger name + phase list from registry/engine so the fallback text cannot drift (it intentionally duplicates engine phases — generated projects must be self-contained). |
| templates/common/docs/agent-workflow.md 27–37 | rule verification + handoffs | project-contract | As-is. |
| templates/common/docs/agent-workflow.md 39–47 | inline fallback loop when skills unavailable | project-contract | Same 4f re-derivation note as L20–25. |
| templates/common/docs/agent-working-rules.md.tpl 1–66 | project scope/architecture/gates template; build-loop autopilot plan-gate note (L37–38); effort ladder (L40–45) | project-contract | As-is; L37–38 and L43 mention the trigger by name → 4f re-derives names from registry. |
| templates/session-bootstrap.txt (1 line) | session bootstrap pointer | project-contract | As-is. |
| templates/adapters/*, templates/profiles/* | host adapters + stack profiles | project-contract | No loop/review policy found (grep: only profile traps reference reviews as advice). Out of Phase 4's cutover surface; unchanged. |

## Map-§16 — plan §16 rules 1–4 → BOTH packs' reviewers.md (mandated duplication)

Canonical source: `plans/PLAN-v7-platform.md` §16 (maintainer-policy — the plan stays
authoritative). Current operative carriers: build-loop SKILL.md L38 + agents/*.md scope
blocks. Phase 4 lands the rules in each pack's `reviewers.md` so the discipline survives
the cutover (plan §16 closing paragraph — this is the single sanctioned duplication):

| Rule | software-dev reviewers.md phrasing | knowledge-work reviewers.md phrasing |
|---|---|---|
| R1 sequential only | qa-agent → code-reviewer → security-reviewer is a strict sequence; never parallel. | One fact-checker today, so trivially sequential — but binding: if the pack ever adds reviewers, they run in sequence, never parallel. |
| R2 diff-scoped + pasted gates | Reviewer reads the phase diff, touched files, directly referenced contract/spec sections only; dispatch prompt names the changed-file list and pastes gate outputs. | Fact-checker reads the draft + each cited source's relevant passage + the brief only; dispatch prompt names the claim list and pastes the builder's gate results (G1/G4/G5/G6 self-check). |
| R3 findings-scoped re-reviews | Round 2+ verifies previous findings against the new diff only. | Re-submission checks previously failing claims only; full re-check only if new claims were added. |
| R4 charter: static-only + capped reports | code/security reviewers: static analysis, no PoC — runtime belongs to qa-agent alone. Findings ≤ ~30 lines. | Fact-checker is read-only (already chartered); never fetches beyond cited sources to build a case. Findings ≤ ~30 lines. |

## Coverage check

- Files fully covered, no unassigned substantive lines: build-loop SKILL.md (1–184),
  build-loop loop-profile.md (1–25), kw SKILL.md (1–49), kw gates.md (1–51),
  kw ground-truth.md (1–24), kw loop-profile.md (1–18), kw reviewers.md (1–20),
  kw deliverables (2 files), docs/loops.md (1–46), domain-builder SKILL.md (1–87),
  templates/common/AGENTS.md, templates/common/docs/* (2 files), session-bootstrap.txt.
- No line has two destinations, with one DECLARED clause-level split: kw SKILL.md
  physical L19 carries three clauses (19a/19b/19c above), each with exactly one
  destination — the 4d/4f movers split the sentence, not the map. The §16 R1–R4
  landing in both reviewers.md is a
  plan-mandated render into two pack surfaces, category `domain-pack`, canonical text
  remaining in plan §16 (maintainer-policy).
- `retired-with-reason` lines: kw SKILL.md L19, L21–29; domain-builder L27–37, L74–76 —
  each retires only at its named slice (4e/4f), with the reason recorded above.
- Destination tallies: engine ≈ 34% of build-loop mechanism + all of docs/loops.md +
  domain-builder process; domain-pack carries every software- or research-specific line;
  project-contract = templates only; maintainer-policy = plan §16 canonical text (no
  skill line maps there); nothing retired without a named successor.
