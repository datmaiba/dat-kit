# External Verification Receipt Gate v1

**Status:** DRAFT FOR MAINTAINER APPROVAL — plan only, no execution authority

**Date:** 2026-07-22

**Scope:** move repeatable QA, static code checks, and baseline security checks
out of Codex reviewer sessions; let Codex validate a candidate-bound receipt
and inspect only exceptions. This is a separate review-infrastructure workstream.
It does not resume B2, start B3, or supersede the current review chain.

## 1. Decision requested

Approve, revise, or reject this staged approach:

1. Build a non-authoritative external verification pipeline in shadow mode.
2. Make it produce a tamper-evident, candidate-bound `review-receipt.json`.
3. Compare it with the current QA/code/security chain on three substantive
   tasks.
4. Only after the evidence passes the thresholds below, submit a separate
   Class C proposal to change review authority.
5. After that proposal is approved, Codex uses the receipt as its normal green
   path and reads source/findings only on yellow or red paths.

Approval of this plan authorizes planning and shadow-mode implementation only.
It does not authorize skipping or replacing any current reviewer.

## 2. Current baseline

The repository already has:

- GitHub Actions on Windows and Ubuntu in `.github/workflows/ci.yml`;
- Python 3.12, `scripts/validate.py`, pytest, and ShellCheck gates;
- `requirements-dev.txt` with PyYAML and pytest;
- a canonical QA → code review → conditional security review → final
  regression QA sequence.

It does not currently have an operative Ruff, mypy, CodeQL, Semgrep,
Hypothesis, dependency-audit, or candidate-bound receipt gate.

B2 demonstrates both sides of the problem:

- mechanical QA was green but required repeated reviewer invocations because
  the reviewer environment could not reliably locate executables;
- the security reviewer found lifecycle-race, malformed-payload, and dangling-
  link issues that generic pass/fail QA did not cover.

Therefore the target is not “replace all judgment with scanners.” The target is
to externalize deterministic work, encode every valid finding as a durable
test/rule, and reserve semantic review for explicitly risky deltas.

## 3. Goals and non-goals

### Goals

1. One reproducible external run owns mechanical execution and evidence.
2. Every result binds to exact base commit, candidate commit, tree, changed
   paths, commands, tool versions, and artifact hashes.
3. A green low-risk candidate needs no QA, code-review, or security-review
   agent invocation after authority promotion.
4. Codex validates the receipt first and opens only failed findings or
   explicitly high-risk changed blocks.
5. Every accepted human/AI finding becomes a regression test, property, or
   static rule when mechanically expressible.
6. Tool versions and action revisions are pinned so local PATH differences and
   silent upgrades cannot change results.

### Non-goals

- no B2 product or test edit;
- no B3 work;
- no broad verdict cache or semantic-epoch framework;
- no claim of token savings before measured evidence exists;
- no replacement of an AI reviewer with another unbounded AI reviewer;
- no weakening of current review authority during shadow mode;
- no claim that static scanners can prove concurrency or architecture correct.

## 4. Target architecture

```text
frozen candidate manifest
        |
        v
GitHub Actions / self-hosted runner
  - current repo gates
  - lint and type checks
  - tests and properties
  - security scans
        |
        v
JUnit + SARIF + JSON + logs
        |
        v
review-receipt.json + SHA-256 digests
        |
        v
receipt verifier
        |
        +--> GREEN: Codex verifies receipt only
        +--> YELLOW: external semantic/security verdict required
        +--> RED: Codex reads only failed evidence and relevant diff
```

The CI artifact is the source of evidence. The repository stores only the
schema, producer/verifier, configuration, and tests—not per-run reports.

## 5. Tools to set up

### 5.1 Required for the first shadow-mode slice

| Purpose | Tool | Setup decision |
|---|---|---|
| Existing canonical gates | GitHub Actions + `scripts/validate.py` + pytest + ShellCheck | Reuse; do not replace |
| Test evidence | pytest built-in JUnit XML | Enable `--junitxml`; no plugin required |
| Fast Python defects | Ruff | Exact version pin; start with correctness/security-relevant stable rules and changed-file enforcement |
| Type defects | mypy | Exact version pin; report-only baseline, then ratchet changed typed surfaces |
| Stateful lifecycle tests | Hypothesis | Exact version pin; use rule-based state machines for lifecycle invariants |
| Deterministic race tests | pytest barriers/process harness | Custom tests; do not depend on timing sleeps |
| Security scanning | CodeQL for Python and GitHub Actions | GitHub advanced/default setup, subject to repository licensing/availability |
| Pattern security rules | Semgrep OSS CLI | Pinned container digest, local rules, metrics disabled; output SARIF |
| Dependency audit | pip-audit | Exact version pin; JSON report; blocking only after baseline triage |
| Evidence retention | `actions/upload-artifact` | Pin action revision; store JUnit, SARIF, JSON, logs, manifest, and receipt |
| Receipt | repository-owned producer/verifier | JSON Schema + SHA-256 checks; fail closed |
| Merge enforcement | GitHub required status check + CODEOWNERS/required review | Configure only in EV4, after the authority proposal closes |
| Codex result intake | GitHub Actions check/artifact reader (`gh` or connected GitHub tooling) | Read receipt and failed artifacts; do not replay green jobs inside Codex |

### 5.2 Optional developer convenience

| Purpose | Tool | Policy |
|---|---|---|
| Local fast-fail | pre-commit | Optional mirror of Ruff and lightweight validation; CI remains authoritative |
| Local reproduction | dedicated PowerShell/Bash wrapper | Same commands and config as CI; not a second policy source |

Do not add Bandit initially: Ruff security rules, Semgrep, and CodeQL already
cover the baseline static-analysis role, and another overlapping scanner would
increase triage noise before its marginal value is measured.

### 5.3 Version and installation policy

- Keep project runtime dependencies separate from review-tool dependencies.
- Resolve exact versions during the compatibility spike and store them in a
  dedicated review-tool lock/input; do not use floating `latest` in gates.
- Pin third-party GitHub Actions by immutable revision for the authoritative
  pipeline.
- Run Semgrep in an isolated pinned container to avoid Python dependency
  conflicts with the repository test environment.
- Record every resolved tool version in the receipt.

## 6. Receipt contract

`review-receipt.json` must contain at least:

```text
schema_revision
run_id
base_commit
candidate_commit
candidate_tree
changed_paths_with_status
risk_profile
tool_versions
commands
gate_id / outcome / exit_code / duration
test collected / passed / failed / skipped
finding counts by severity
unresolved finding IDs
artifact paths and SHA-256 digests
required-gate set
completed timestamp
```

The verifier rejects:

1. stale commit or tree;
2. changed-path mismatch, rename/deletion omission, or dirty input;
3. missing required gate;
4. unknown, skipped-without-policy, or malformed outcome;
5. non-zero unresolved critical/high findings;
6. mismatched artifact hash;
7. unpinned or unexpected tool/action version;
8. a receipt generated before the final candidate;
9. self-declared external semantic approval without a separately bound verdict.

An external human/security reviewer, when required, produces a small separate
verdict record bound to the same commit and tree. Codex validates that record;
it does not need the review conversation.

## 7. Risk routing

### GREEN — receipt-only path

Eligible only when all required mechanical gates pass and the diff does not
touch a yellow trigger. After authority promotion:

- no QA agent;
- no general code-review agent;
- no security-review agent;
- Codex checks identity, completeness, hashes, severities, and freshness.

### YELLOW — external semantic path

Triggered by any of:

- concurrency, locks, append/atomicity, recovery, or lifecycle transitions;
- public or untrusted input, path/link handling, subprocesses, permissions,
  authentication, cryptography, uploads, payments, or secrets;
- contract, policy, gate, schema, migration, or reviewer-authority changes;
- new architecture boundary or materially changed public behavior;
- a scanner suppression or risk-classification override.

Machines still run first. Then one focused external reviewer—human, security
owner, or separately governed review service—reviews only the risky diff and
open evidence. Its commit-bound verdict joins the receipt. If no such reviewer
is configured, current Codex review remains the fail-closed fallback.

### RED — failure path

Codex receives only:

- failed gate/finding IDs;
- the relevant report excerpts;
- directly affected changed blocks;
- the candidate identity.

Other green reports and unrelated repository context are not dispatched.

## 8. Execution plan

### EV0 — governance and isolation

1. Keep B2 stopped at its current REPLAN handoff and do not start B3.
2. Execute this work in a separate worktree/branch, proposed name
   `codex/external-verification-receipt-gate`.
3. Register shadow mode as non-authoritative under the current policy.
4. Record that promotion of the receipt to acceptance authority is a separate
   Class C decision; the new checker cannot approve itself.

**Exit:** written routing decision, isolated clean tree, unchanged current
reviewer authority.

### EV1 — reproducible toolchain spike

1. Add pinned Ruff, mypy, Hypothesis, and pip-audit tooling.
2. Add pinned/isolated Semgrep and CodeQL jobs.
3. Make every current and new job emit a machine-readable report.
4. Preserve Windows and Ubuntu coverage.
5. Deliberately introduce one temporary failure per new gate, observe the red
   result, revert it, and then trust green.
6. Keep new tools report-only until their existing finding baselines are
   classified.

**Exit:** identical commands are reproducible; every gate has observed-red and
green evidence; no untriaged baseline blocks development.

### EV2 — receipt producer and verifier

1. Define JSON Schema for candidate manifest and review receipt.
2. Build a small producer that consumes reports; it does not execute or
   reinterpret tools.
3. Build a separate verifier that reconciles receipt identity with Git.
4. Add negative tests for every rejection in section 6.
5. Upload reports and receipt as one immutable CI artifact bundle.

**Exit:** 100% rejection of stale, incomplete, malformed, or tampered fixtures;
one clean candidate produces a verifiable receipt on Windows and Ubuntu.

### EV3 — B2 finding replay and shadow observation

Encode the B2 security findings without modifying or resuming the B2 product
slice:

1. stale-snapshot finish/resume race → deterministic barrier/process test plus
   lifecycle state-machine invariant;
2. malformed/deep payload failures → Hypothesis strategies and structured-
   error assertions;
3. dangling telemetry parent → explicit link/path regression test and, if its
   false-positive rate is acceptable, a local Semgrep rule.

Then run the external pipeline beside the unchanged canonical reviewer chain
for three substantive tasks. Record:

- agreement per deterministic gate;
- findings detected only by humans/AI;
- false positives and suppressions;
- environment/tool-discovery retries;
- elapsed duration and reviewer invocation counts;
- receipt identity/tamper failures;
- tokens as `unknown` unless the runtime provides trustworthy attribution.

**Exit thresholds:**

- 100% agreement on deterministic QA results;
- zero stale, incomplete, or wrongly accepted receipts;
- all three known B2 security classes caught by durable tests/rules in replay;
- zero critical/high scanner finding left unresolved;
- every human-only finding classified as “encode next” or “semantic-only”;
- three completed tasks with final regression evidence.

Failure to meet a threshold keeps the pipeline in shadow mode.

### EV4 — separate authority-promotion proposal

Only after EV3 passes:

1. submit a Class C proposal under the current parent authority;
2. define which mechanical gates replace QA-agent execution;
3. define exact green/yellow/red routing and external-verdict authority;
4. retain semantic review for yellow triggers until evidence supports a
   narrower change;
5. require independent reviews, cross-component regression, rollback rehearsal,
   effective-from boundary, and append-only decision evidence;
6. make the single `external-verification` status check required by branch
   protection only after the proposal closes.

**Exit:** approved authority decision, required status check active, current
fallback chain still available.

### EV5 — receipt-first Codex operation

1. Green: Codex validates the final receipt and reports closure.
2. Yellow: Codex validates mechanical evidence plus the external focused
   verdict; it reads code only if the verdict is missing or conflicting.
3. Red: Codex diagnoses only the failure scope.
4. Every newly accepted finding becomes a candidate regression gate.
5. Review tool upgrades go through their own observed-red/green compatibility
   change, never silent auto-upgrade.

## 9. Proposed file surfaces

Exact names may be refined during EV0, but ownership should remain narrow:

```text
.github/workflows/ci.yml                  # existing gates + report production
.github/workflows/codeql.yml             # security scan, if separate workflow
requirements-review.*                    # isolated exact review-tool versions
ruff.toml or pyproject.toml               # Ruff configuration
mypy.ini or pyproject.toml                # mypy ratchet configuration
.semgrep.yml / semgrep-rules/             # local pinned security policy
schemas/review-candidate.schema.json
schemas/review-receipt.schema.json
scripts/review_receipt.py                 # report composition only
scripts/verify_review_receipt.py           # independent fail-closed verifier
scripts/tests/test_review_receipt.py
docs/decisions/...                        # only when governance requires it
```

Do not store generated JUnit, SARIF, logs, or per-run receipts in Git.

## 10. Acceptance and rollback

### Acceptance before authority promotion

- EV1–EV3 thresholds all pass;
- current review chain remains complete on all shadow tasks;
- no scanner suppression lacks owner, reason, and expiry/review condition;
- CodeQL availability/licensing is confirmed; if unavailable, the plan records
  the reduced coverage instead of claiming equivalence;
- external semantic reviewer ownership is named for yellow paths;
- the Class C proposal is separately approved.

### Rollback after promotion

1. append a corrective governance decision from an explicit effective
   boundary;
2. remove the receipt check's acceptance authority while retaining artifacts;
3. restore the ordinary full reviewer chain for later candidates;
4. invalidate open receipts after the rollback boundary;
5. run full cross-component regression and preserve the failed evidence.

## 11. Expected operational effect

Before EV4, token usage does not decrease materially because shadow mode keeps
the current reviewers. Its purpose is evidence and safety.

After EV4:

- green candidates use zero reviewer-agent invocations and one bounded Codex
  receipt check;
- yellow candidates use one focused external semantic verdict, not three broad
  agent reviews;
- red candidates dispatch only failed evidence for diagnosis;
- no numerical token-saving claim is made until measured after the effective
  boundary.

## 12. Approval boundary

Approving this document authorizes EV0–EV3 only. EV4 authority promotion needs
a separate maintained Class C plan and explicit approval. B2 remains stopped
at its security REPLAN threshold, and B3 remains prohibited without separate
approval.
