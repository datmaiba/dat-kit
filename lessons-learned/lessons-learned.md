# Lessons Learned — dat-kit

AI agents read this file before EVERY task in this repo. New entries go on top, written the same day. Format: date — title, then what happened · root cause · rule. If lesson-miner is installed it appends drafts at the bottom — promote them up when finalized.

---

### 2026-07-23 — A pinned reviewer with no executor refused rather than fabricating a verdict

- **What happened**: the pinned `qa-agent` dispatch for B2's final regression QA (candidate `bd4e844`) had only Read/Grep/Glob available — no bash/executor in that subagent context. It explicitly reported the tooling gap and refused to certify `PHASE DONE`, rather than inventing gate counts. A substitute general-purpose agent with real `mcp__workspace__bash` access was dispatched with the same charter and actually ran all five gates plus the edge-case attack.
- **Root cause**: the reviewer charter assumes an executor is always available inside the subagent's runtime; that assumption does not hold in every harness/session configuration.
- **Rule**: when a pinned reviewer reports "no executor available," treat that as a correct refusal, not a defect to route around silently — do not pressure it into a verdict. Dispatch a substitute agent with the same charter and real execution tools, and log both the interrupted dispatch and the substitute dispatch as separate rows in the invocation ledger (never delete the failed one).

---

### 2026-07-23 — A dispatch packet's byte budget should scale with finding count, not sit at a fixed constant

- **What happened**: the B2 findings-scoped security re-review packet for S1–S3 came in at 3,401 bytes, exceeding the ≤2.5 KB target pre-registered in the B2 observation ledger.
- **Root cause**: each finding (S1/S2/S3) needed enough fix-and-test-pin context for the reviewer to verify it independently without re-reading the whole diff; three findings bundled into one packet compounded past the flat threshold.
- **Rule**: budget a findings-scoped packet as roughly (finding count × ~800 bytes), not a single fixed constant. If the real packet still exceeds budget, declare the overage in the invocation ledger (as done here) rather than trimming context to the point where the reviewer verifies shallowly.

---

### 2026-07-23 — `git checkout -f` on a Cowork mount needs file-delete permission granted first, then a post-checkout stray-file check

- **What happened**: `git checkout feature/telemetry-v3` failed partway through with a wall of `unable to unlink ... Operation not permitted` errors, because the Cowork sandbox mount blocks unlink by default. Recovery required calling `allow_cowork_file_delete`, re-running `checkout -f`, then manually removing 9 leftover files that were tracked on `master` but not on the target branch.
- **Root cause**: the Cowork mount denies unlink by default; `git checkout` is not atomic when blocked partway through, so the working tree ends up with a mix of both branches' files.
- **Rule**: before any `git checkout`/`clean` on a Cowork mount, call `allow_cowork_file_delete` first. After the checkout, always run `git status --short --branch` and diff it against `git ls-tree <target> -r --name-only` to confirm no stray files from the previous branch remain.

---

### 2026-07-21 — A Definition-of-Done item was marked CLOSED four commits before its receipt existed

- **What happened**: step 11 marked §13.1 item 13 ("full release train … and tag complete") **CLOSED** in commit `e0f52f4`, citing "the `v2.0.0` annotated tag" as its receipt. The tag was not created until `a7aa0ad`, four commits later. The same commit also left two unfilled placeholders in `evidence.md` ("see below … once complete", "commit recorded once cut"), and the first handoff — committed *into the tree the tag was then placed on* — asserted that the tag "has not been cut yet". An owner-requested audit caught all of it before the tag was pushed.
- **Root cause**: the closing document and the closing act were put in the same commit, so the receipt could only be written as a forward promise. A tag cannot be cited from inside the tree it tags — the citation is structurally impossible, not merely inconvenient — and writing it anyway converts "closed on evidence" into "closed on assumption", which D-RC-B explicitly forbids. The placeholders are the same failure in miniature: text written to be filled by a step that had not happened yet, and then never revisited.
- **Rule**: an acceptance item whose receipt is the *final irreversible act* (a tag, a deploy, a publish) closes in a commit made **after** that act, never in the tree the act applies to. The pre-act commit states "every prerequisite receipted; closes at <act>"; the post-act commit records the real hashes. Never write a placeholder whose filling depends on a later step — either the fact exists now and you write it, or the section belongs in a later commit. → this is the load-bearing case of the self-referential-pointer lesson below; that entry warned about review verdicts, this one shows the same defect closing a program's Definition of Done.

---

### 2026-07-21 — The plan-gate reviewer was skipped because the session order looked authoritative enough

- **What happened**: step 11 ran the full build-loop otherwise faithfully (self-questioning, approval gate, gates, code review, harvest) but never dispatched `plan-reviewer` before the approval gate. The omission was not declared to the owner; it surfaced only in a later self-audit. No damage resulted — but the two defects the audit *did* find (a Definition-of-Done item closed on a non-existent receipt, and a doc-placement conflict with a frozen registry glob) are precisely the class a plan review is meant to catch before any commit exists.
- **Root cause**: the session order was unusually detailed — binding facts, pre-decided scope, named decisions — and that thoroughness was silently treated as a substitute for independent plan review. A well-written plan is exactly the case where review feels redundant and is not: it is still the *builder's own* reading of that plan that goes unchecked.
- **Rule**: `plan-reviewer` runs before every approval gate, including when the plan arrives pre-written as a session order or dictated scope. If it is deliberately skipped, the skip and its reason go in the report to the owner at the gate — never silently, exactly as the security-reviewer skip must be stated.

---

### 2026-07-21 — A scorecard line can pass the run it describes and still fail the gate that reads it back

- **What happened**: the RC1 scorecard append (`5154f3f`, `benchmarks/scorecard.jsonl` line 23) recorded `"agent_runtime": "cowork"`, a value `validate_scorecard()`'s `RUNTIMES` tuple (`tuple(POINTERS) + ("other",)`, `scripts/contract_check.py:50`) does not accept. Every prior Cowork session on this branch had correctly used `"other"`. `validate.py` was green on the commit that was reviewed (`dc3fe81`, 22 lines) and only went red one commit later when the RC1 handoff commit appended line 23 — so the RC bundle's "gates green" claim was true of the tree it cited and false of HEAD by the time step 11 started.
- **Root cause**: the scorecard skill's HARVEST step writes the append and reports success from the write succeeding, not from re-running `validate.py` afterward — so a malformed enum value can land, get committed, and sit undetected until the next session's independent gate run.
- **Rule**: any HARVEST step that appends to a file `validate.py` checks must re-run `validate.py` (or the specific check) after the append, in the same phase, before declaring the phase's gates green — a write succeeding is not the same claim as the write being valid. This is the append-only sibling of "a green gate proves nothing until you've seen it fail": here the miss was a green gate not re-run after its own precondition changed.

---

### 2026-07-21 — An evidence bundle that lists planned and completed files under one heading breaks its own citation contract

- **What happened**: RC1 code review found the evidence bundle's diff-scope statement mixed files it had already touched with files it only planned to touch, under a single undifferentiated list — a reader could not tell proof from intent by looking at the list alone.
- **Root cause**: the diff-scope statement was drafted from the session order's plan and never regenerated from the actual `git diff` at commit time, so "planned" and "done" silently merged.
- **Rule**: an evidence artifact's diff-scope statement must be generated from the real diff at commit time, never copied from the plan that preceded it. If a planned-but-not-done item needs mentioning, label it explicitly as such in its own line.

---

### 2026-07-21 — A self-referential review pointer inside a document cannot cite the commit that reviewed it

- **What happened**: RC1 code review found §10 of the bundle pointing to "see §10" for its own review record — scaffolding that survived into a release artifact, and structurally incapable of citing the RC commit hash since the document can't contain its own future hash.
- **Root cause**: the review-record placeholder was drafted before the commit existed and never replaced with a real pointer once it did.
- **Rule**: a review verdict belongs in a commit message or a follow-up appendix that can cite the reviewed commit's hash — never a self-reference inside the document being reviewed. Replace draft placeholders with real pointers in the same commit that closes the review round.

---

### 2026-07-20 — `* text=auto` let a Windows checkout rewrite a byte-compared generated file

- **What happened**: the first real push of `feature/open-platform-v2` failed the Windows Actions job with `PROJECTION_BYTE_MISMATCH` on `skills/build-loop/SKILL.md` and `skills/knowledge-work/SKILL.md`. `.gitattributes` pinned `registry/**`, `templates/**`, `*.py` and `*.sh` to `eol=lf` but not the generated skill projections, so a `core.autocrlf=true` checkout (the GitHub-hosted Windows default) normalized their committed LF bytes to CRLF while `render.py` always emits LF — `validate.py`'s byte-compare failed on Windows only. Fixed in `ba77045` by adding `skills/**/SKILL.md text eol=lf`.
- **Root cause**: byte-exactness was enforced at compare time but never protected at checkout time; `* text=auto` is a heuristic that actively rewrites line endings, so it is the opposite of a guarantee for a file whose bytes are the contract.
- **Rule**: every destination in `render.py`'s `expected_outputs()` needs its own explicit `.gitattributes` `eol=lf` pin — adding a new projection means adding its pin in the same commit. A repo check asserting that every `expected_outputs()` path is covered by such a pin is the mechanical form of this rule and should be added before the next projection lands.

---

### 2026-07-20 — Sandbox rsync-copy verification is structurally blind to checkout-normalization bugs

- **What happened**: every gate run for slices 5a→5c was green, but they all ran against an `rsync`'d copy of the working tree — never a real `git clone`. The `.gitattributes` defect above was therefore undiscoverable locally and surfaced only after a push, in CI. It was reproduced locally only afterwards, with `git clone -c core.autocrlf=true --quiet . /tmp/before`, which produced the identical two diagnostics.
- **Root cause**: the local verification loop copied files rather than materializing them through git, so the entire class of "what does checkout do to these bytes" bugs was outside what any local green could ever prove. The copy protocol was adopted for speed and its blind spot was never stated.
- **Rule**: a green gate on a file copy proves nothing about checkout behavior. Anything line-ending-, `.gitattributes`- or filter-related must be verified through a real `git clone -c core.autocrlf=true <repo> <tmp>` before push — not discovered post-push via Actions. State the blind spot wherever the copy protocol is documented, so the next session doesn't mistake copy-green for checkout-green. → strengthens the 2026-07-13 entry below ("a workflow file existing ≠ CI working"): a local green ≠ a CI green, for reasons that are structural, not flaky.

---

### 2026-07-20 — An unscoped smoke prompt authorized a host agent to execute the whole plan

- **What happened**: the Gate 4 Codex host smoke ran `codex exec "run the build loop"` under the default `sandbox: workspace-write` + `approval: never`. Codex treated the prompt as full authorization: it re-ran parts of Gates 1–2 itself, tried to shell out to Claude Code, and **wrote** `handoffs/HANDOFF-2026-07-20-phase5-external-gates.md` plus a `benchmarks/scorecard.jsonl` append recording a "Claude pack-read FAIL" conclusion that was true only of its own sandboxed attempt. Both artifacts were uncommitted and were reverted — but a stale handoff is exactly what build-loop reads first on resume.
- **Root cause**: the smoke test's intent (does the host read the pack?) and the prompt's literal meaning (execute the build loop) were not the same thing, and nothing in the invocation constrained the gap. A trigger phrase chosen to prove trigger-matching doubles as a real work order.
- **Rule**: a host-conformance smoke must restrict scope in the prompt itself ("read-only: report three facts, do not modify files or execute the plan") or run under a read-only sandbox flag. Never smoke-test a trigger phrase with write permissions granted — and treat any artifact a smoke run leaves in `handoffs/` or `benchmarks/` as contaminated evidence until proven otherwise.

---

### 2026-07-20 — A lifecycle label and a declared artifact list contradicted each other across descriptors

- **What happened**: 5c code review found that `adapters/codex/ADAPTER.md` defines the `repo_only` lifecycle as "no project artifact exists or is emitted", while the gemini-cli descriptor in `registry/adapters.json` sits at `repo_only` *and* declares a `GEMINI.md` `project_artifact`. Both are shipped truth; nothing detects the contradiction, and it survived to the RC because the definition lives in one adapter's prose rather than in the registry contract.
- **Root cause**: lifecycle semantics were documented per-adapter instead of being defined once and enforced mechanically, so a label became a comment — a descriptor can claim a state whose stated meaning its own data violates.
- **Rule**: every registry lifecycle state needs exactly one canonical definition in the registry contract plus a conformance check asserting each descriptor's data matches the state it claims (`repo_only` ⇒ empty `project_artifact`). Per-adapter prose describing a shared state is a documentation smell — the next descriptor will contradict it silently. Deferred past v2.0.0 only because the fix edits frozen registry surfaces (R9 amendment procedure required).

---

### 2026-07-20 — A snapshot doubling as recognition record AND live-template proof deadlocked the revision flip

- **What happened**: the 5a templates flip could not go green under pre-5a registry semantics — the immutable 1.16 snapshot and the new 2.0 snapshot listed the same target paths (`REGISTRY_PATH_COLLISION`) and both pointed at the same `templates/common/` files, of which only one revision's bytes can live-hash (`REGISTRY_SNAPSHOT_HASH_MISMATCH` ×2). No arrangement of hashes could avoid it; the builder had to stop for decision D-5a-1.
- **Root cause**: one shipped artifact carried two roles at once — historical recognition record and live scaffold source verified against current template bytes. Any second revision necessarily breaks whichever role is preserved.
- **Rule**: split the roles before any revision cutover (D-5a-1 / registry.md R6): only the CANONICAL revision's snapshot scaffolds and is live-verified; historical snapshots are immutable records checked for descriptor↔snapshot consistency only. A future flip authors a new canonical snapshot and demotes the old one — never edits a historical snapshot.

---

### 2026-07-20 — A pre-match sanitizer must be strictly subtractive, or it can forge the match it guards

- **What happened**: FU-1 made contract-marker matching fence/inline-code-aware by stripping fenced blocks and inline code spans before the scan (`_marker_scan_text`). Security review confirmed the helper can only HIDE a marker (failing safe toward non-green), never forge one — and flagged that replacing spans with `""` instead of a same-width neutral placeholder could FUSE adjacent fragments into a brand-new match.
- **Root cause**: the false-green guarantee rested on an unstated property of the normalizer — that it never emits new substrings — which nothing pinned; a plausible "simplification" would have silently destroyed it.
- **Rule**: a sanitizer that runs before recognition may only remove or neutralize text in place — it must never emit new substrings or join previously separated text. State the invariant next to the code and re-verify it in review whenever the normalizer changes.

---

### 2026-07-20 — Relaxing a redundant integrity check requires the trust-domain equivalence test — both halves

- **What happened**: D-5a-1 relaxed live hash-verification of historical snapshots. Security review approved only after showing (1) bypassing recognition requires editing `platform.json` — an equal-trust, independently gated artifact — and (2) historical snapshots have no data-flow into FilePlans or classification, so a tampered record cannot reach a privileged output.
- **Root cause**: "the check is redundant" is an argument about one path; without both properties proven, a relaxation can open an unexamined tamper path through the artifact that was demoted.
- **Rule**: before relaxing any redundant integrity check, prove BOTH: bypass requires editing an equal-or-higher-trust, independently gated artifact, AND the relaxed artifact has no data-flow into privileged outputs. Either half alone is insufficient.

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
- **Rule**: a workflow file existing ≠ CI working. When adding or changing a workflow, verify at least one real run is green on the Actions tab before declaring done — and when a template file is added/removed, grep ci.yml for count assertions. Trust the CI run over a hand-rolled local pipeline check. → strengthened by the 2026-07-20 entry above ("Sandbox rsync-copy verification is structurally blind to checkout-normalization bugs"): a local green can differ from a CI green for structural reasons, not just flakiness — verify through a real `git clone`, not a file copy.

---

<!-- Real project entries go above this line. Entry format:

### YYYY-MM-DD — Short title

- **What happened**: one or two sentences.
- **Root cause**: the actual cause, plainly named.
- **Rule**: the checkable rule that prevents recurrence.
-->
