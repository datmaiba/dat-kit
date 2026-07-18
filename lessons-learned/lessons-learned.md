# Lessons Learned — dat-kit

AI agents read this file before EVERY task in this repo. New entries go on top, written the same day. Format: date — title, then what happened · root cause · rule. If lesson-miner is installed it appends drafts at the bottom — promote them up when finalized.

---

### 2026-07-18 — One review round burned 284k tokens (~65% of a session) by ignoring three existing rules

- **What happened**: during plan-v7 execution, three reviewer subagents (code 122k, security 94k, QA 68k) ran in PARALLEL, each re-read nearly the whole repo (registry.py ~900 lines, all contracts, tests), and the read-only reviewers ran their own PoCs. Token exhaustion hit two machines/accounts (Claude Fable 5 Pro, Codex 5.6) before phases could finish.
- **Root cause**: charters said "scope the diff" descriptively but did not forbid whole-repo reads; the sequential review order was stated but parallel execution was not explicitly banned; "read-only analysis" was not enforced as "no PoC". A rule a subagent can profitably ignore is a description, not a rule.
- **Rule**: reviewers run sequentially, read only the diff + touched files, cap reports at ~30 findings lines, re-review findings-scoped, and never run PoCs outside qa-agent. Dispatching prompts must name the diff scope and paste gate outputs. See PLAN-v7 §16 and the scope-discipline blocks in `agents/*.md`.

---

### 2026-07-14 — validate.py green on CI, false-red on the maintainer's own Windows console

- **What happened**: `python scripts/validate.py` ran every check successfully on Windows but crashed with `UnicodeEncodeError` on the final `print("✓ all checks green")` — non-zero exit despite all checks passing. The fail path's `❌` print had the same latent crash. CI (ubuntu, UTF-8) was green the whole time, so the bug lived only on the exact machine the README maintenance workflow tells the maintainer to run the script on.
- **Root cause**: Windows consoles default to a legacy codepage (cp1252) that cannot encode the status symbols; the script assumed a UTF-8 stdout.
- **Rule**: any script that prints non-ASCII must reconfigure stdout to UTF-8 (`sys.stdout.reconfigure(encoding="utf-8", errors="replace")`) or stick to ASCII. A green CI run does not cover the maintainer's local console — verify both the pass AND fail print paths on the actual target console (the fail path needs a deliberately injected finding, mirroring "a green gate proves nothing until you've seen it fail").

---

### 2026-07-14 — Drafted five "missing" contract files that already existed in the repo

- **What happened**: an upgrade session saw only `SKILL.md` in an installed copy of the knowledge-work skill, concluded the five-slot contract files were missing, authored all five from scratch, ran a subagent review on the drafts, and shipped a git patch — which failed to apply because four of the files already exist in the repo, richer than the drafts. The repo was mounted in the session the whole time; the actual defect was an install flow that saved a lone SKILL.md without its sibling files.
- **Root cause**: a derived artifact (an install copy) was treated as ground truth for the source repo, and the failure signal (`git apply`: "already exists") was answered with a workaround script instead of a diagnosis.
- **Rule**: before declaring anything "missing," open the source of record — the repo, not a cache/install/summary of it. When a patch fails with "already exists," read the existing file before generating another byte. A copy lacking a file ≠ the source lacking it (sibling of "a workflow file existing ≠ CI working"). Never install a skill by copying its SKILL.md alone — copy the directory.

---

### 2026-07-13 — CI existed for 20 releases but had never run once

- **What happened**: `.github/workflows/ci.yml` shipped in v0.6.0 with a push trigger on `main`, but the repo's default branch is `master` — zero runs ever fired. The very first real run then failed on a smoke-test assertion (`1 created, 11 skipped`) that had gone stale when CONTEXT.md grew the template set in v1.3.0. A local pre-check gave a false pass because a failed `cmd | grep -q` pipeline did not abort the check script despite `set -e`.
- **Root cause**: a workflow file was treated as proof of working CI; nobody verified an actual green run after adding it, so both the dead trigger and the stale assertion accumulated silently.
- **Rule**: a workflow file existing ≠ CI working. When adding or changing a workflow, verify at least one real run is green on the Actions tab before declaring done — and when a template file is added/removed, grep ci.yml for count assertions. Trust the CI run over a hand-rolled local pipeline check.

---

<!-- Real project entries go above this line. Entry format:

### YYYY-MM-DD — Short title

- **What happened**: one or two sentences.
- **Root cause**: the actual cause, plainly named.
- **Rule**: the checkable rule that prevents recurrence.
-->
