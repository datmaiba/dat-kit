# Session order — Phase 5 RC bundle (step 8) — scope PROPOSED; owner confirms at start

**Run this session on `opus` or `fable`, not `sonnet`.** Per
`docs/model-selection.md`, an RC bundle is the "final go/no-go on a phase" —
a judge/verify role. The reviewer subagents are pinned to `opus`; the
controller session should not sit below the workers it dispatches. If the
session starts on a lower tier, say so and ask the owner to raise it with
`/model` before doing substantive work.

Context: dat-kit repo, branch `feature/open-platform-v2`. HEAD must be
`222cac6` ("docs(5-ext): external-gate evidence — Gate 1 push+Actions PASS
…"); history `222cac6 ba77045 c7d25e7 a6a1be6 e751d5f b14d648 8d5fb70
024882b 291dd78`. Phases 0A→4 CLOSED. Phase 5 slices 5a/5b/5c CLOSED, and
the D-5c-C external gates are now VERIFIED (evidence
`docs/spikes/phase-5/evidence.md` § External gates) — which is exactly the
condition D-5c-C set for opening RC1. This session opens the RC bundle.

## Step 1 — minimal bootstrap (read nothing else)

Read `AGENTS.md` (root) + `handoffs/CONTEXT-2026-07-18-plan-v7-execution.md`
(the "5c deferrals/flags" AND "5-ext deferrals/flags → RC bundle" blocks
BIND this session) + `plans/PLAN-v7-platform.md` ONLY §6 Phase 5 (step 8 +
Exit) + §9.3 (evidence bundle shape) + §13.1 (the v2.0.0 Definition of Done
checklist — this is the RC's actual acceptance criteria) + §16 +
`docs/spikes/phase-5/evidence.md` § External gates and §5c only.

Verify: `git log --oneline -9` matches; tree clean; gates green:
`python3 -m pytest scripts/tests -q` (expect **275 passed 3 skipped**),
`python3 scripts/validate.py`, `python3 scripts/render.py --check`.

Machine quirks (Windows Cowork sandbox, confirmed 5a→5-ext — do NOT
rediscover):

- Mounted-FS pytest exceeds the 45s bash cap AND each bash call is a fresh
  sandbox. Protocol: `rsync -a --delete <mnt>/dat-kit/ <local-tmp>/kit/`
  then run the suite in the copy (~3s). Edits + git stay in the mounted
  repo. `pip install pytest --break-system-packages` may be needed once.
- `git config core.filemode false` once per session.
- Stale `.git/HEAD.lock`/`index.lock` → request Cowork file-delete
  permission, `rm -f`, retry; transient "unable to unlink tmp_obj" warnings
  are harmless.
- CRLF warnings on commit are normal; `.gitattributes` normalizes.
- `shellcheck` is not preinstalled: `pip install shellcheck-py
  --break-system-packages`, then `export PATH="$HOME/.local/bin:$PATH"`.
- Sandbox rsync copies do NOT reproduce checkout normalization. To verify
  anything line-ending/`.gitattributes`-related, use
  `git clone -c core.autocrlf=true <repo> <tmp>` — this is how the Windows
  CI failure was reproduced locally (lesson candidate 2, 5-ext).

## Facts that bind (established 5a→5-ext — never re-litigate silently)

- **Format freeze is BINDING** (registry.md R9 + `scripts/tests/
  test_format_freeze.py`): any change to `format_revision`, canonical
  revision `dat-kit 2.0`, or the green/migratable lists before the v2.0.0
  tag reopens the release train and must amend the R9 statement AND the pin
  test in the SAME commit. **RC1 must not touch these.**
- `release_version` is `"2.0.0"` everywhere (platform.json + 3 mirrored
  targets). D-5b-A: straight `2.0.0`, no rc suffix — because Phase 5 Exit
  requires "RC artifact equals tagged artifact". RC1/RC2 are **evidence
  bundles, not version strings**. Do not invent an `-rc1` version.
- D-5a-1: canonical snapshot = only scaffold source / only live-verified;
  historical snapshots immutable. `registry/snapshots/
  project-contract-1.16.json` IMMUTABLE (sha256 `be98855c…`).
- `_marker_scan_text` strictly SUBTRACTIVE; `UNSAFE_FIELD_CHARS` literal
  pinned; pinned eval phrases ("run the build loop" / "write a researched
  report") asserted by `benchmarks/skill-evals.jsonl`.
- `.gitattributes` now pins `skills/**/SKILL.md text eol=lf` (`ba77045`).
  Any NEW generated projection destination needs its own `eol=lf` pin —
  `* text=auto` does not protect byte-compared files on Windows checkout.
- The `docs/codex.md` redirect stub is LOAD-BEARING: current scripts AND
  rolled-back v1.17.1 tooling print "see docs/codex.md". Never delete it
  while v1.17.1 is the rollback target.

## External-gate status (input to the RC bundle — do not re-run)

Verified 2026-07-20 on the owner's machine, recorded in evidence
§ External gates:

- **Gate 1** — real Actions run `29744500620` on `ba77045`: `validate` PASS
  + `windows-python` PASS. Surfaced 2 CI-only defects (CRLF/eol pin,
  SC2015), fixed in `ba77045`, code-reviewer APPROVE 0 blocking,
  red-before-green proven via `git clone -c core.autocrlf=true`.
- **Gate 2** — Windows Git Bash clean-install smoke PASS (17 created, exit
  0, `dat-kit 2.0` marker, idempotent rerun 0/17).
- **Gate 3** — one real v1.16 project migrated (owner's blog project, via
  an isolated clone): plan applied → `contract_check` exit 0;
  `docs/agent-working-rules.md` sha256-identical before/after; the real
  working tree never touched.
- **Gate 4** — Claude Code AND Codex fresh-session smokes both PASS (pack
  read outside `skills/` confirmed; Codex verified from its own session
  JSONL transcript, plugin cache `…/dat-kit/2.0.0`).
- **KNOWN GAP** — Cursor manual evidence checklist NOT gathered (owner does
  not have Cursor installed). Gemini CLI correctly out of scope
  (`repo_only`, separate four-gate activation track).

## Step 2 — proposed RC scope (plan §6 step 8; CONFIRM before executing)

OPEN DECISIONS for the owner, present as ONE batch:

- **D-RC-A — the Cursor gap.** (1) Open RC1 now with Cursor recorded as an
  explicit, named known limitation in the bundle, to be closed before the
  `v2.0.0` tag (recommended — every other gate is green, and §13.1 does not
  require Cursor live evidence; `adapters/cursor/ADAPTER.md` itself says no
  scriptable headless Cursor exists, so this is a manual checklist, not an
  automated gate). (2) Block RC1 until the owner installs Cursor and runs
  the checklist. Consequence: (1) keeps the train moving with an honest
  documented gap; (2) is stricter but stalls on software the owner may not
  want to install.
- **D-RC-B — §13.1 verification depth.** The RC bundle's real job is
  proving the 14-item v2.0.0 Definition of Done. (1) Verify EVERY item
  against a named artifact/test/evidence section, recording the receipt per
  item, and mark any that cannot be closed (recommended — this is what makes
  the bundle an artifact rather than a claim). (2) Verify only the items
  Phase 5 touched and trust earlier phase evidence for the rest.
  Consequence: (1) costs budget but is the actual Exit criterion; (2) risks
  a Phase-4-era item having silently regressed.
- **D-RC-C — the three 5-ext lesson candidates** (gitattributes/projection
  coverage; sandbox-vs-real-checkout verification gap; Codex smoke-prompt
  scope) plus the **5c candidate** (lifecycle-label vs artifact-list
  contradiction). Approve for append to `lessons-learned/`, or defer?
  Recommended: approve all four and append FIRST (own commit), as with the
  5a candidates at 5b — they are exactly the kind of paid-for lesson the
  next release train must not re-learn.
- **D-RC-D — the Gemini registry quirk** (rolled INFO from 5c review:
  `repo_only` lifecycle coexists with a declared `GEMINI.md`
  `project_artifact`, contradicting the codex ADAPTER's definition of
  `repo_only`). (1) Leave as a documented known limitation in the RC
  bundle, fix after the tag (recommended — the fix touches registry data,
  which is FROZEN; amending requires the R9 + pin-test procedure and
  reopens the release train). (2) Fix now under the freeze-amendment
  procedure, accepting a re-review round.

Deliverables (after decisions):

1. **RC1 evidence bundle** — the §9.3 shape (commit + registry revisions;
   commands + exit codes; fixture names/results; projection check result;
   fact-check sources + dates; known limitations; reviewer and decision
   references; rollback notes), aggregating Phases 0A→5 evidence into ONE
   RC document. Location: `docs/spikes/phase-5/rc1-bundle.md` (new file;
   the per-slice `evidence.md` sections stay as the underlying receipts —
   the bundle CITES them, never restates them as fresh claims).
2. **§13.1 Definition-of-Done matrix** per D-RC-B: one row per checklist
   item → status → the exact artifact/test/evidence citation that proves
   it. Any unprovable item is a STOP, not a soft note.
3. **Known limitations section**: Cursor gap (per D-RC-A), Gemini quirk
   (per D-RC-D), freeze-coupling INFO (docs→test only), plus anything the
   §13.1 pass surfaces.
4. Lessons appended per D-RC-C (first commit if approved).
5. Gates re-run + full sequential review per §16.

OUT OF SCOPE RC1: migration guide + release notes + tag (step 11 — separate
session after RC1 is APPROVED); any registry/template/scripts code change
(freeze binding — a needed change means STOP and reopen the train per R9);
re-running external gates (already verified above); Cursor/Gemini
activation.

Reviews per §16: sequential, diff-scoped, ≤30-line reports. code-reviewer
always. security-reviewer: fires only if registry/migration/path surfaces
are touched — an evidence-document-only RC bundle does NOT fire it; state
the skip and reason explicitly. If the §13.1 pass forces any code change,
that changes the answer — re-evaluate, don't inherit this note.

Commit order by semantic owner: lessons (if approved) → RC1 bundle →
evidence/handoff/scorecard.

Discipline: budget ~50–80k tokens, checkpoint at 70%; grep before Read;
STOP on scope overflow. A §13.1 item that cannot be proven from existing
artifacts is a STOP-and-report, never a "probably fine". When RC1 is done,
STOP, report, wait for the owner's go/no-go before step 11.

## After RC1 (next session, not this one)

Step 11: migration guide + release notes + tag `v2.0.0` from the APPROVED
RC commit. Phase 5 Exit also requires `release/1.x` gates still passing on
its own branch — verify before tagging.
