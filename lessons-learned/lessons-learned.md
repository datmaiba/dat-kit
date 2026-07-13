# Lessons Learned — dat-kit

AI agents read this file before EVERY task in this repo. New entries go on top, written the same day. Format: date — title, then what happened · root cause · rule. If lesson-miner is installed it appends drafts at the bottom — promote them up when finalized.

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
