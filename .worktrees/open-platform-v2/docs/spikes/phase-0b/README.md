# Phase 0B evidence index

Phase 0B ran on 2026-07-18 from branch `feature/open-platform-v2`. It changes no
released scaffolding behavior. Reproducible probes live under
`scripts/spikes/phase0b/`.

## Approved decisions in force

- Six-slot Domain Pack contract; descriptor is not a slot.
- Python standard-library registry validation; no JSON Schema claim.
- Bash-only greenfield materialization through generated sanitized TSV.
- `dat-kit 2.0` sole green revision; `dat-kit 1.16.0` migration source.
- Adapter lifecycle: `repo_only → migration_ready → scaffold_active → retired`.
- Release split: 2.0 platform, 2.1 telemetry v3, 2.2 governed evolution.
- Option A selected by live Claude and Codex evidence.

## Baseline

Windows worktree checkout initially exposed CRLF materialization of
`scripts/init.sh`. The repository now declares `*.sh text eol=lf`; after that
correction the baseline was:

```text
python scripts/validate.py                         PASS
python -m pytest scripts/tests                     86 passed, 5 skipped
bash -n scripts/init.sh                            PASS
shellcheck scripts/init.sh                         PASS
git diff --check                                   PASS
```

Linux container verification used Python 3.12.13, Git, Bash 5.2.37, and the
official ShellCheck image: `validate.py` passed, the repository suite reported
`88 passed, 3 skipped`, the spike harness passed, and all three shell scripts
passed syntax and ShellCheck. An initial minimal-container attempt lacked the
`git` executable and was discarded as an environment failure before the green
run.

## Reports

1. `01-host-materialization.md`
2. `02-domain-trigger-rendering.md`
3. `03-sanitized-manifest.md`
4. `04-registry-bootstrap.md`
5. `05-project-snapshots.md`
6. `06-append-recovery.md`
7. `07-proposal-ids.md`

Supporting controls are in `host-facts.md`, `revert-map.md`,
`fixture-inventory.md`, and `phase4-ownership-draft.md`.
