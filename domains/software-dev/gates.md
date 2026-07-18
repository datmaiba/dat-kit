# software-dev — gates

Done-criteria for a software-dev phase. Each gate carries worked cases and
the way it can be gamed (per the gate-validity rule in `docs/loops.md`). A
phase without ALL of these green is NOT done — no exceptions, in any mode.

## SW-G1 — Project gates green · *automatable* · closer: qa-agent

Every quality-gate command the project's canonical `AGENTS.md` contract
declares exits green, run **exactly as written there** (if the project says
docker-only, never fall back to host binaries).

- **Pass:** `docker compose exec app pest` → 24/24 ✓, run verbatim from the
  contract.
- **Fail:** substituting `php artisan test` on the host because docker "was
  slow" — a different command proves nothing about the declared gate.
- **Gamed by:** a no-op gate command that exits green regardless — a
  type-check once stayed green for six phases while dozens of real errors
  accumulated. Countermeasure: the engine's red-green proof (VERIFY) applied
  to every added or changed gate command. **Evidence:** the red run's output
  captured alongside the green.
- **Evidence contract:** verbatim per-gate results in the phase report
  ("pest 24/24 ✓, tsc ✓") — never "everything works".

## SW-G2 — Working demo · **human-run** · closer: builder walks, user verifies

The phase's demo step from the build-phases spec is actually walked, not
described.

- **Pass:** each demo step executed with its observed result stated;
  browser-only steps the user must perform are listed and deferred
  explicitly.
- **Fail:** "the endpoint should now return the new field" — prediction, not
  demonstration.
- **Gamed by:** narrating the expected behavior instead of exercising it.
  Countermeasure: the report names what was actually run and seen, step by
  step.

## SW-G3 — Independent review chain · **human-run** · load-bearing · closer: reviewers per `reviewers.md`

`qa-agent` reports PHASE DONE, `code-reviewer` reports APPROVE, and
`security-reviewer` reports APPROVE whenever its trigger surfaces were
touched (see `reviewers.md`).

- **Pass:** verdicts on record for the phase's actual diff, in sequence.
- **Fail:** self-review, or a verdict on a stale diff.
- **Gamed by:** shrinking the dispatch scope so the reviewer never sees the
  risky files, or re-running a full review until one round misses the
  finding. Countermeasure: the dispatch prompt names the complete
  changed-file list; re-reviews are findings-scoped against the new diff.
- **Ceiling:** "APPROVE" is reviewer judgement, not a mechanical signal —
  **this gate caps the domain at Goal** (see `loop-profile.md`).
