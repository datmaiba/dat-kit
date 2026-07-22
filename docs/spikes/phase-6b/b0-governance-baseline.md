# Phase 6B B0 governance-admission baseline

- Captured at: `2026-07-22T02:57:58Z`
- Baseline commit: `8c8b4e08c9768fe5f78363c77a74a0a11625987c`
- Scope: ownership admission only; no Telemetry v3 runtime or event data exists.

## Planned paths and pre-admission explanations

`scripts/registry.py explain-evolution` was run on every exact storage surface
from Telemetry v3 T3.2 plus the proposed schema, CLI, and test paths.

| Path | Baseline result |
|---|---|
| `telemetry` | `EVOLUTION_ORPHAN_PATH`: matched 0 governed roots |
| `telemetry/schema-v3.json` | `EVOLUTION_ORPHAN_PATH`: matched 0 governed roots |
| `telemetry/events.jsonl` | `EVOLUTION_ORPHAN_PATH`: matched 0 governed roots |
| `scripts/telemetry.py` | `EVOLUTION_ORPHAN_PATH`: matched 0 component classes |
| `scripts/tests/test_telemetry.py` | governed by `maintainer-scripts`, class B, `maintainer-policy/1` |
| `benchmarks/telemetry-v3.jsonl` | governed by `maintainer-evidence`, class B, `maintainer-policy/1` |
| `benchmarks/defects.jsonl` | governed by `maintainer-evidence`, class B, `maintainer-policy/1` |
| `benchmarks/scorecard.jsonl` | governed by `maintainer-evidence`, class B, `maintainer-policy/1` |

Only the first four paths need admission. The narrow ownership design is one
new `telemetry` governed root plus one component whose globs are exactly
`telemetry/**` and `scripts/telemetry.py`. Both resolve to owner `maintainers`,
class B, under `maintainer-policy/1`. Existing benchmark and test ownership is
unchanged.

## Boundary and fail-closed cases

The admission tests require:

- `telemetry-v3/events.jsonl` to stay outside the new root;
- `scripts/telemetry.py.bak` to stay orphaned rather than being hidden by a
  broad `scripts/**` glob;
- removing the new component to yield `EVOLUTION_ORPHAN_PATH`; and
- adding an overlapping component to yield
  `EVOLUTION_OWNERSHIP_AMBIGUOUS`.

Red-before-green receipt on the baseline registry:

```text
pytest scripts/tests/test_registry_catalog.py -k phase6b_telemetry -q
2 failed, 1 passed, 10 deselected; exit 1
```

The two failures were the intended missing-admission failures: the `telemetry`
root had no governed root and the `telemetry-v3-runtime` component did not yet
exist. The boundary-orphan test already passed.

## Frozen input hashes

| Path | SHA-256 |
|---|---|
| `registry/evolution.json` | `52ac2dc5d027c1cd4449b39c04a923cd2e804633ee3a081f1e536503db471975` |
| `docs/contracts/evolution.md` | `45e188e19ff7d2398640e4aafbe3c54ed61f7a259be4fb669c1fbbf4c6c7a83a` |
| `docs/contracts/telemetry-v3.md` | `c9fa5e6bcfc8760cd9a6e78597a8db1ae3a305b870e137335f185a7966b70dde` |
| `handoffs/HANDOFF-2026-07-22-phase6b-token-economy-plan-v3.md` | `63a0e97a598d7198c94afc3196dbf767acf6b03123706169f0e1abe7b3b1e6f5` |
| `scripts/tests/test_registry_catalog.py` | `39cec24f4fd6af7034c3add3fe34852889e6f5f0fda1e83e18f7024ceb196e24` |
