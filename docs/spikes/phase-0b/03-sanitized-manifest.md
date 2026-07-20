# Spike 03: sanitized Bash scaffold manifest

The approved row format is:

```text
source_rel<TAB>target_rel<TAB>ownership<TAB>action<TAB>introduced_revision<TAB>lifecycle
```

`parse_manifest.sh` uses Bash `read` with tab IFS, no `eval`, a restricted
relative-path grammar, explicit enums, and plans only `scaffold_active` rows.
It stages plan output privately and publishes it only after every row validates.
The probe accepted one active row, ignored one `repo_only` row, and rejected
injection, traversal, unknown-action, and valid-then-invalid-tail fixtures. Each
rejection asserted empty stdout, so a consumer cannot act on a partial plan.

Observed on Windows Git Bash 5.2.37 and Linux Bash 5.2.37:

```text
MANIFEST_PROBE_OK shell=5.2.37(1)-release valid=1 rejected=4 atomic-reject=1 no-eval=1
```

Decision: keep TSV as a committed projection, never an authority. Reject tabs,
newlines, absolute paths, drive prefixes, `..`, shell metacharacters, unknown
ownership/action/lifecycle values, and malformed revisions before publishing
any materialization plan.
The production action enum will be versioned by the normative registry
contract; adding an action requires validator and red-fixture changes, not an
ad hoc shell branch.
