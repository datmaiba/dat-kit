# Phase 4 semantic ownership draft

This is the pre-move tripwire. Each current line range has one semantic owner.
Blank lines travel with the adjacent block. Root reviewer-agent files may remain
as host projections, but their semantics have only the Domain Pack owner shown
here. Phase 4 must refine this map after before-evals and before moving lines.

## `skills/build-loop/`

| Current lines | Sole destination owner | Intended destination |
|---|---|---|
| `SKILL.md:1-4` | domain-pack | Generated thin trigger for `software-dev`. |
| `SKILL.md:6-9` | domain-pack | `domains/software-dev/workflow.md` introduction. |
| `SKILL.md:10-16` | project-contract | Canonical `AGENTS.md` and adapter-pointer rule. |
| `SKILL.md:18-24` | domain-pack | Software workflow required inputs and missing-spec behavior. |
| `SKILL.md:25-36` | domain-pack | `domains/software-dev/reviewers.md`. |
| `SKILL.md:38-60` | domain-pack | Software workflow PREFLIGHT and decision artifact. |
| `SKILL.md:62-68` | engine | Cross-domain authority/severity routing. |
| `SKILL.md:70-72` | engine | Cross-domain LOAD lifecycle and phase ordering only. |
| `SKILL.md:73-78` | domain-pack | Software source list: spec, project contract, lessons, glossary, and previous code. |
| `SKILL.md:79-100` | domain-pack | Software ground-truth/question lenses and spec Q&A. |
| `SKILL.md:101-108` | domain-pack | Software plan and dependency-first build workflow. |
| `SKILL.md:109-120` | domain-pack | Software gate execution, red proof, demo walk. |
| `SKILL.md:122-129` | domain-pack | Software code/security reviewer routing. |
| `SKILL.md:131-139` | engine | Cross-domain HARVEST ordering and report contract; scorecard remains a utility skill. |
| `SKILL.md:140-143` | engine | Autopilot activation and cross-domain mode switch. |
| `SKILL.md:144-146` | domain-pack | Software preflight, spec decision log, plan deviation, and named security-review routing. |
| `SKILL.md:147-148` | engine | Retry/stop and wakeup-success mechanics. |
| `SKILL.md:149`, clause `commit` | domain-pack | Software repository commit convention. |
| `SKILL.md:149`, remainder | engine | Cross-domain HARVEST and phase-report mechanics. |
| `SKILL.md:150-151` | engine | Mode precedence and context-ceiling/handoff mechanics. |
| `SKILL.md:153-160` | engine | Delegated execution orchestration, cold briefs, and spec-compliance-first mechanics. |
| `SKILL.md:161` | maintainer-policy | Current host/model-tier routing; it is not engine behavior. |
| `SKILL.md:162`, through code-quality stage | engine | Generic two-stage ordering: compliance before quality. |
| `SKILL.md:162`, named reviewer and retry routing | domain-pack | Software `code-reviewer` route and retry gate. |
| `SKILL.md:163` | maintainer-policy | Host-tier consult routing and current escalation producer; keep out of the 2.0 engine pending the 2.1 telemetry cutover. |
| `SKILL.md:164`, gate/reviewer clauses | domain-pack | Software per-task gates and phase-level `qa-agent` route. |
| `SKILL.md:164`, composition clause | engine | Cross-domain requirement to verify composed tasks. |
| `SKILL.md:165` | engine | Delegated question escalation mechanics; the pack supplies its severity policy. |
| `SKILL.md:167-169` | engine | Cross-domain interrupted-run detection and recovery entry. |
| `SKILL.md:171`, handoff clause | engine | Read the newest compact handoff first. |
| `SKILL.md:171`, Git-verification clause; `SKILL.md:172-176` | domain-pack | Git/spec-specific interrupted software recovery. |
| `SKILL.md:178-182` | domain-pack | Software completion and spec-authority hard rules. |
| `loop-profile.md:1-25` | domain-pack | `domains/software-dev/loop-profile.md`; descriptor mirrors `loop_ceiling`. |

## `skills/knowledge-work/`

| Current lines/files | Sole destination owner | Intended destination |
|---|---|---|
| `SKILL.md:1-15` | domain-pack | Generated thin `knowledge-work` trigger. |
| `SKILL.md:17-19` | domain-pack | Workflow introduction. |
| `SKILL.md:21-29` | retired-with-reason | Five-slot inventory is replaced by the normative six-slot descriptor/projection. |
| `SKILL.md:31-45` | domain-pack | `domains/knowledge-work/workflow.md` phases A-G. |
| `SKILL.md:47-49` | domain-pack | Move reasoning to `loop-profile.md`; trigger retains only generated summary. |
| `ground-truth.md:1-24` | domain-pack | `ground_truth` slot, semantic move. |
| `gates.md:1-51` | domain-pack | `gates` slot, semantic move. |
| `reviewers.md:1-20` | domain-pack | `reviewers` slot, semantic move. |
| `deliverables/report.template.md:1-26` | domain-pack | `deliverables` slot. |
| `deliverables/fact-check.template.md:1-22` | domain-pack | `deliverables` slot. |
| `loop-profile.md:1-18` | domain-pack | `loop_profile` slot; descriptor mirrors Goal ceiling. |

## Capability ladder, authoring, and reviewers

| Current lines/files | Sole destination owner | Intended destination |
|---|---|---|
| `docs/loops.md:1-42` | engine | Loop model and capability ladder; remain hand-maintained documentation checked for consistency, not a Projection Module output. |
| `docs/loops.md:44-46` | maintainer-policy | Practitioner scope boundary. |
| `skills/domain-builder/SKILL.md:1-15` | maintainer-policy | Utility-skill trigger, rendered from its maintained source. |
| `skills/domain-builder/SKILL.md:17-23` | maintainer-policy | Practitioner-authority boundary. |
| `skills/domain-builder/SKILL.md:25-37` | retired-with-reason | Five-slot and sentence-marker detection replaced by six-slot registry conformance. |
| `skills/domain-builder/SKILL.md:39-80` | maintainer-policy | Interview, gate validation, ceiling, write, and handoff authoring workflow, rewritten for descriptor + six slots. |
| `skills/domain-builder/SKILL.md:82-87` | maintainer-policy | Pack-authoring hard rules. |
| `agents/plan-reviewer.md:1-22` | domain-pack | Software reviewer semantics; root agent becomes a thin host projection. |
| `agents/qa-agent.md:1-36` | domain-pack | Software QA/gate semantics; root agent becomes a thin host projection. |
| `agents/code-reviewer.md:1-29` | domain-pack | Software review semantics; root agent becomes a thin host projection. |
| `agents/security-reviewer.md:1-29` | domain-pack | Software security-review semantics; root agent becomes a thin host projection. |

## Project and maintainer policy

| Current lines/files | Sole destination owner | Intended destination |
|---|---|---|
| `templates/common/AGENTS.md:1-19` | project-contract | Canonical generated-project contract. |
| `templates/common/CLAUDE.md:1-5` | project-contract | Generated thin Host Adapter pointer; no policy body. |
| `templates/common/docs/agent-workflow.md:1-47` | project-contract | Generated-project workflow owner. |
| `templates/common/docs/agent-working-rules.md.tpl:1-66` | project-contract | Generated-project architecture, gates, scope, and reporting. |
| `docs/agent-workflow.md:1-32` | maintainer-policy | dat-kit maintainer execution/review/migration/handoff. |
| `docs/agent-working-rules.md:1-44` | maintainer-policy | dat-kit maintainer architecture, gates, evidence, and traps. |

No line above is assigned to both engine and a Domain Pack. A future split of a
mixed line must first rewrite it into separate clauses and update this map; it
may not copy the same instruction into two owners.
