# Lessons Learned — dat-kit

AI agents read this file before EVERY task in this repo. New entries go on top, written the same day. Format: date — title, then what happened · root cause · rule. If lesson-miner is installed it appends drafts at the bottom — promote them up when finalized.

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
