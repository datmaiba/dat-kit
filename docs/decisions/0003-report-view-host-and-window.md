# Decision 0003: reports-producer view host and window mapping

- Status: accepted
- Date: 2026-07-24
- Owner and approving authority: Dat Mai Ba (platform owner)
- Scope: Phase 6B B3 subset #5 — the two reports-producer derivation views in
  `scripts/telemetry.py` (`build_per_reviewer_view`, `build_event_coverage_rate_view`).
- Source: `docs/contracts/telemetry-v3.md` T3.12 (per-reviewer view + event-coverage-rate
  view, "for each host and observation window").

## Context

T3.12 defines the event-coverage-rate view "for each host and observation window",
but the v3 event envelope (`TOP_LEVEL_FIELDS`, `scripts/telemetry.py`) carries no
`host` field and no `window` field. The view must therefore choose how "host" and
"window" are read from the existing schema without adding a field — a schema change
would be Class C and is out of scope for this subset.

## Decision

1. **Host = `revisions.adapter.value`.** The host adapter is the envelope's existing
   identifier of the emitting host; the contract's own "host" language elsewhere
   (`unsupported_host_start`, "Host Adapter trust contract") denotes the Host Adapter.
   Tasks are grouped by their terminal event's `revisions.adapter.value`. A `null`
   adapter value (adapter revision unavailable) is a valid grouping key of its own.

2. **Window = the whole corpus (single window) for this subset.** The view treats the
   entire passed event stream as one observation window. Arbitrary time-range windowing
   is deferred to B4 (durable export/aggregation), where a window filter is the natural
   layer. The functions take the event stream as their only input so a future window
   filter can be applied upstream without changing the view contract.

3. **No envelope change.** Neither a `host` nor a `window` field is added. This decision
   binds only the read-side derivation; the immutable event schema is untouched.

## Consequences

- The `reports` producer stays `planned`; these are read-only derivations, not emissions.
- B4 owns time-window slicing and any durable projection of these views; it may revisit
  this decision if a window field is later justified through a governed schema proposal.
- Recorded here (kit decision log) rather than in `templates/common/spec/08-decisions.md`,
  which is a downstream generated-project template, not dat-kit's own decision record.
