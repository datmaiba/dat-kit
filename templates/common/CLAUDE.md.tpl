# CLAUDE.md — {{PROJECT_NAME}}

This file governs Claude Code in this repository. It is an instance of dat-kit (github.com/datmaiba/dat-kit), filled in for this project.

## What this repo is

**{{PROJECT_NAME}}** — {{PROJECT_DESC}}

## Mandatory reading, in order

1. This file.
2. `spec/` — the product brain: vision, features, architecture, build phases. **The spec answers most questions — check it before asking the user.**
3. The `build-loop` skill (from dat-kit) — the loop to follow for every phase.
4. `.claude/rules/working.rules.md` — working discipline (effort, plan gate, reporting).
5. `lessons-learned/lessons-learned.md` — known mistakes; never reintroduce.

Rules use RFC 2119 keywords. MUST / MUST NOT violations are blocking defects.

## Architecture rules (stack profile: {{PROFILE_NAME}})

{{PROFILE_ARCHITECTURE}}

## Quality gates (MUST)

{{PROFILE_GATES}}

## Silent-failure traps (inherited from the profile — extend per project)

{{PROFILE_TRAPS}}

## Scope control

Declare files you will touch before editing. Each phase (see `spec/04-build-phases.md`) has a defined scope — ask before crossing into another phase's territory or editing root configs or `spec/` (spec changes are proposals, not silent edits). **Exception**: appending to `spec/08-decisions.md` is always allowed — it's the decision log, not a spec change.

## The build loop (MUST)

For every "build phase N" request, run the dat-kit `build-loop` skill: load context → self-question → plan → **STOP for approval** → build → verify via the gates above → self-review → propose lessons-learned. Never bundle plan + code in one turn. Autopilot mode (PREFLIGHT + no-stop execution) is defined in the skill.

## Rule verification

On **"verify rules"**: list loaded files (CLAUDE.md, spec files, rules, lessons-learned) and recite: the architecture rules above, the gates, the plan gate, and the preflight/decisions rule (`spec/08-decisions.md` + severity rubric). No code.
