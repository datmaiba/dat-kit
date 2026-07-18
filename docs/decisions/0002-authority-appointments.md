# Decision 0002: Initial governance-authority appointments

- Status: accepted
- Date: 2026-07-18
- Owner and approving authority: Dat Mai Ba (platform owner)
- Source of authority: `PLAN-v7-platform.md` §14 approval record (12/12
  approve, 2026-07-17) and `docs/contracts/evolution.md` authority rules.

This document is the appointment evidence referenced by
`registry/evolution.json#/authorities/*/appointments`. Its canonical SHA-256
(CRLF-normalized, as computed by `scripts/registry.py canonical_file_hash`) is
recorded as each appointment's `evidence_hash`; changing this file without
re-recording the hash fails registry validation review.

## Appointments

### software-dev-reviewer-1 {#software-dev-reviewer-1}

The `software-dev-reviewer` authority's initial closer seat is appointed as an
owner-appointed independent reviewer, exercised in practice through the
repository's independent review agents (`agents/code-reviewer.md`,
`agents/qa-agent.md`) and any human reviewer the owner designates. Effective
2026-01-01. Successor rule: the platform owner appoints; the proposer of a
change may never be its closer.

### independent-fact-checker-1 {#independent-fact-checker-1}

The `knowledge-work-reviewer` authority's initial closer seat is appointed as
an owner-appointed independent fact-checker per the knowledge-work pack's
reviewer contract. Effective 2026-01-01. Same succession and
proposer-is-never-closer rule.

### platform-owner-1 {#platform-owner-1}

The `platform-owner` authority is held by the maintainer, Dat Mai Ba, the
named Class C closer for contract, authority, and enforcement changes. The
maintainer's name is intentionally public here: a Class C authority must be an
identifiable person, and the same identity already signs the plan approval
record. Succession: a recorded successor in a future appointment entry of this
document, approved as Class C.
