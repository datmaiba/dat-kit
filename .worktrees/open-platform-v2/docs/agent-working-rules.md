# Agent working rules — dat-kit maintainers

This document is part of the root `AGENTS.md` contract. It contains no generated
project placeholders.

## Architecture

- `templates/common/AGENTS.md` is the canonical generated-project entrypoint.
- `templates/common/docs/agent-*.md` contain shared generated-project policy.
- Runtime compatibility pointers are derived from `scripts/contract_check.py`'s
  registry and contain no substantive policy.
- Skills define reusable workflows; `scripts/validate.py` and `scripts/tests/`
  enforce their packaging and evidence contracts.

## Quality gates

Run from the repository root:

```text
python scripts/validate.py
pytest scripts/tests
bash -n scripts/init.sh
shellcheck scripts/init.sh
git diff --check
```

When a gate itself changes, prove red-before-green with an isolated failing
fixture before trusting the final green run.

## Scope and evidence

- Preserve user changes and append-only benchmark history.
- Brownfield scaffolding must inspect before it mutates and fail closed on any
  competing instruction source, unsafe path, or incompatible partial install.
- New scorecard records use schema v2; historical v1 records are not rewritten.
- Whenever a skill description changes, add or update its positive trigger case
  in `benchmarks/skill-evals.jsonl`.

## Traps

- Git line endings differ across Windows and Linux; compare normalized text.
- A workflow file is not proof CI ran; verify a real run before release.
- Installed plugins and active sessions retain old metadata until reinstall or
  update and a fresh session.
