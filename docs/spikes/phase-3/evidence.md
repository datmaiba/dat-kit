# Phase 3 evidence bundle — contract revision state machine + adapter activation

Date: 2026-07-18 · Branch: `feature/open-platform-v2`
Commits: `92699ce` (implementation) → review-fix commit (this one).
Environment: Linux sandbox, Python 3.10.12. Review mode: plan §16 (v7.1) —
sequential, diff-scoped, gate outputs pasted, reports capped.

## Gates (at close)

| Command | Result |
|---|---|
| `python3 -m pytest scripts/tests/ -q` | 133 passed, 3 skipped |
| `python3 scripts/validate.py` | ✓ all checks green |
| `python3 scripts/render.py --check` | exit 0, byte-exact |
| greenfield smoke | `.cursorrules` emitted; `.cursor/` NEVER emitted |

## Scope delivered

Registry-driven revision state machine in `contract_check.py` via
`Catalog.revision_model()` (R4 amended first): five states — green /
migration-source / partial / unsupported / unclassified; hardcoded 1.16
constants deleted; recognition never green. Typed `RETIRE_LEGACY` for
pristine `.cursorrules` with `REMOVE_LEGACY_POINTER → ADD_RULES_POINTER`
plan steps; `.cursor/rules/dat-kit.mdc` template + cursor artifact at
`migration_ready` (descriptor mirrors artifact minimum). Marker-rule files
treated as rendered (hash divergence ≠ customization). `init.sh` rerun on a
1.16 scaffold = read-only migration gate. 9 state fixtures with no-mutation
tree hashes (plan §6 Phase 3 fixture list complete).

## Reviews (sequential, v7.1)

1. **qa-agent (sonnet, runtime)** — APPROVE. All 7 exit criteria reproduced
   live; adversarial AGENTS.md (both markers, fence-quoted marker, empty,
   directory) never crashed, never false-negative. Soft finding: substring
   marker matching → fence-quoted v2 marker + byte-exact pointer = false
   green (edge).
2. **code-reviewer (sonnet, static)** — APPROVE. Minors: local hashlib
   import (fixed); `.cursorrules` hardcoded vs future `migration_edges`
   derivation (follow-up); substring idiom pre-existing (follow-up with QA
   finding); cp1252 gap pre-existing file-wide (follow-up).
3. **security-reviewer (sonnet, static)** — APPROVE. Confirmed: reads
   confined to inventory dict, TOCTOU/no-follow held; no target mutation
   exists in the checker; no JSON/diagnostic injection (regex charset +
   json.dumps escaping). LOWs: unbounded `_read_target` size (fixed —
   `MAX_TARGET_READ_BYTES` 10 MiB, `BLOCKED_UNSAFE`); fixture `tree_hash`
   followed symlinks (fixed — lstat-based, symlinks recorded distinctly).

Regression (findings-scoped then full once): 133 passed, validate green,
render byte-exact.

## Tracked follow-ups (not Phase 3 blockers)

- FU-1 Marker parsing hardening: fence/anchor-aware marker matching (QA soft
  finding + code review; pre-existing idiom, dedicated pass).
- FU-2 Derive typed-retire pointers from `migration_edges` instead of the
  `.cursorrules` literal when the edge schema grows a pointer field.
- FU-3 `contract_check.py` stdout UTF-8 reconfigure (file-wide, pre-existing).

## Exit criteria vs plan §6 Phase 3

v1.16 never green: PROVEN (fixtures + real scaffold). Brownfield default
inspect-only: PROVEN (checker has no mutation path at all). Greenfield
registry-driven: held (Phase 1B manifest; `.mdc` structurally excluded).
Artifacts activate individually: cursor `.mdc` at `migration_ready`, gemini
stays `repo_only`, `scaffold_active` set unchanged. Rollback fixture-tested:
rollback of this phase = revert two commits; no public output changed
(smoke identical). `scaffold_active` promotion for `.mdc` deliberately
deferred until clean + customized migration fixtures run against a REAL
v1.16 project (Phase 5 step 7 external evidence).

## Rollback

Revert `92699ce` + the review-fix commit. Registry data changes (cursor
artifact) revert with them; no other component depends on revision_model yet
besides contract_check.
