# software-dev — reviewers

You are the **builder**. Independent reviewers keep you honest. dat-kit ships
four reviewer subagents; their operative charters live at the dat-kit root in
`agents/*.md` (projected to hosts by the adapters). **This file is the binding
surface**: it declares the team, the sequence, and the review-cost rules the
orchestrating session must enforce. If a named subagent is unavailable in
this environment, substitute a fresh subagent with the same charter, or as a
last resort a separate fresh-eyes pass — and say which substitution you made.

## The team

| Agent | Role | When |
|---|---|---|
| `plan-reviewer` | audits plans against spec (read-only) | PLAN, before the approval gate |
| `qa-agent` | runs gates + attacks with edge cases | VERIFY, loops until PHASE DONE |
| `code-reviewer` | audits the diff against the rules | REVIEW, loops until APPROVE |
| `security-reviewer` | attacker's-eye audit of the diff (read-only) | conditional — see trigger surfaces below |

Inner loop per phase: **build → qa-agent → fix → qa-agent → code-reviewer →
fix → (regression qa) → done**. Applies in BOTH normal and autopilot modes.

## security-reviewer trigger surfaces (conditional reviewer)

Trigger when the phase's diff touches ANY of: auth/session logic ·
user-supplied content (forms, markdown, comments) · file uploads or path
handling · new public endpoints · permission changes · payment/money.
security-reviewer runs after code-reviewer approves; verdict
`RETURN TO BUILDER` (any CRITICAL/HIGH finding) → fix → re-run qa-agent
(regression) + security-reviewer. Phases touching none of those surfaces skip
it — per the engine, the skip and its reason go in the report, never
silently.

## Review-cost rules (hard — carried from plan §16)

- **R1 — sequential only:** qa-agent → code-reviewer → security-reviewer is a
  strict sequence; never parallel.
- **R2 — diff-scoped + pasted gates:** Reviewer reads the phase diff, touched
  files, directly referenced contract/spec sections only; dispatch prompt
  names the changed-file list and pastes gate outputs.
- **R3 — findings-scoped re-reviews:** Round 2+ verifies previous findings
  against the new diff only.
- **R4 — charter: static-only + capped reports:** code/security reviewers:
  static analysis, no PoC — runtime belongs to qa-agent alone. Findings
  ≤ ~30 lines.

## Independence and conflicts

A proposer cannot close its own proposal — the builder-vs-grader rule itself
is engine REVIEW policy; this pack binds it to the team above. Reviewer
verdict schemas (`PHASE DONE`, `APPROVE`, `RETURN TO BUILDER`) and retry
behavior are declared in each charter; the escalation path for repeated
failure is the engine's retry bound, then STOP and report.
