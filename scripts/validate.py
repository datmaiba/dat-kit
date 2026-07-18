#!/usr/bin/env python3
"""dat-kit repo validation — run locally (python3 scripts/validate.py) and in CI.

Checks: manifest JSON validity + version sync, canonical agent-contract
templates, skill/agent frontmatter, JSONL, hooks.json shape, personal-info gate.
Exit 0 = all green; exit 1 = findings printed.
"""
import json, re, sys, glob, pathlib
from contract_check import check_repo, validate_scorecard
from registry import Catalog
from render import check_outputs, expected_outputs

try:
    import yaml
except ModuleNotFoundError:
    print("PyYAML is required: python3 -m pip install -r requirements-dev.txt")
    sys.exit(1)

# Windows consoles default to a legacy codepage (cp1252) that cannot encode the
# ✓/❌ status symbols — the script would crash on its final print with a false-red
# exit code even when every check passed. CI (Linux, UTF-8) never sees this.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parent.parent
findings = []


def check(cond, msg):
    if not cond:
        findings.append(msg)


def frontmatter(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    parts = text.split("---")
    check(len(parts) >= 3, f"{path}: missing frontmatter")
    if len(parts) < 3:
        return None, text
    try:
        return yaml.safe_load(parts[1]), text
    except Exception as e:
        findings.append(f"{path}: frontmatter YAML error: {e}")
        return None, text


def exact_path(relative):
    """Return a repo path only when every segment has the expected casing."""
    current = ROOT
    for part in pathlib.PurePosixPath(relative).parts:
        if not current.is_dir():
            findings.append(f"{relative}: parent directory is missing")
            return current / part
        names = {child.name for child in current.iterdir()}
        if part not in names:
            findings.append(f"{relative}: missing or wrong-cased path segment '{part}'")
            return current / part
        current = current / part
    return current


# 1. Registry Catalog and the only two committed projections.
catalog_result = Catalog.load(ROOT)
catalog = catalog_result if isinstance(catalog_result, Catalog) else None
if catalog is None:
    for diagnostic in catalog_result:
        findings.append(f"{diagnostic.code}: {diagnostic.path}: {diagnostic.message}")
else:
    # Governed-inventory sweep runs at validation time, not inside
    # Catalog.load (a stray untracked file must not brick every consumer).
    for diagnostic in catalog.validate_governed_inventory():
        findings.append(f"{diagnostic.code}: {diagnostic.path}: {diagnostic.message}")
    for diagnostic in check_outputs(ROOT, expected_outputs(catalog)):
        findings.append(f"{diagnostic.code}: {diagnostic.path}: {diagnostic.message}")

# 1b. Engine revision entry — every registered domain's `required_engine_revision`
# must resolve to a committed engine manifest whose declared revision matches, and
# the engine policy file the manifest names must exist. A mismatch is the
# composition stop (DOMAIN_ENGINE_REVISION_MISMATCH) enforced at validation time.
if catalog is not None:
    for domain in catalog.domains():
        required = domain.get("required_engine_revision", "")
        if not re.fullmatch(r"[a-z][a-z0-9-]*/[0-9]+", required or ""):
            findings.append(f"{domain.get('domain_id')}: malformed required_engine_revision {required!r}")
            continue
        engine_id = required.split("/")[0]
        manifest_path = ROOT / "engine" / engine_id / "engine.json"
        check(manifest_path.is_file(),
              f"{domain.get('domain_id')}: requires engine {required!r} but engine/{engine_id}/engine.json is missing")
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            findings.append(f"engine/{engine_id}/engine.json: invalid JSON: {e}")
            continue
        if not isinstance(manifest, dict):
            findings.append(f"engine/{engine_id}/engine.json: manifest must be a JSON object")
            continue
        check(manifest.get("engine_revision") == required,
              f"DOMAIN_ENGINE_REVISION_MISMATCH: {domain.get('domain_id')} requires {required!r} "
              f"but engine/{engine_id}/engine.json declares {manifest.get('engine_revision')!r}")
        # The policy path comes from data: require a repo-relative path with no
        # parent escapes (ROOT / "/abs" discards ROOT; ".." walks out of it).
        policy = manifest.get("policy", "")
        policy_parts = pathlib.PurePosixPath(policy).parts if isinstance(policy, str) and policy else ()
        policy_ok = bool(policy_parts) and not pathlib.PurePosixPath(policy).is_absolute() and ".." not in policy_parts
        check(policy_ok, f"engine/{engine_id}/engine.json: policy must be a repo-relative path, got {policy!r}")
        check(not policy_ok or (ROOT / policy).is_file(),
              f"engine/{engine_id}/engine.json: declared policy file missing: {policy!r}")

# 2. Skills
skill_files = sorted(path for path in (ROOT / "skills").rglob("SKILL.md") if path.is_file())
for f in skill_files:
    fm, text = frontmatter(f)
    if not fm:
        continue
    check("name" in fm and "description" in fm, f"{f}: frontmatter needs name + description")
    check(len(fm.get("description", "")) < 1024, f"{f}: description {len(fm.get('description',''))} chars (limit 1024)")
    check(text.count("\n") < 500, f"{f}: body {text.count(chr(10))} lines (keep under 500)")

# 2b. Pack-contract completeness — a Domain Pack's SKILL.md declares its slot
# files in the five-slot table and states "Contract files live beside this one."
# (that sentence is the pack-instance marker; domain-builder's SKILL.md carries
# the same table as a *definition* and must not be checked). Every declared slot
# file must exist beside the SKILL.md, and deliverables/ must hold >=1 template.
# Guards against a pack shipping (or being authored) with dangling slot refs.
SLOT_ROW = re.compile(r"^\|[^|]+\|\s*`([a-z0-9_.-]+\.md)`")
for f in skill_files:
    text = pathlib.Path(f).read_text(encoding="utf-8")
    # quoted mentions (e.g. domain-builder instructing pack authors to include
    # the marker) do not count — only the bare sentence marks a pack instance
    if not re.search(r'(?<!")Contract files live beside this one', text):
        continue
    skill_dir = pathlib.Path(f).parent
    for line in text.splitlines():
        m = SLOT_ROW.match(line)
        if m:
            check((skill_dir / m.group(1)).exists(),
                  f"{f}: declares slot `{m.group(1)}` but the file is not beside SKILL.md")
    if re.search(r"^\|[^|]+\|\s*`deliverables/`", text, re.M):
        deliv = skill_dir / "deliverables"
        check(deliv.is_dir() and any(deliv.iterdir()),
              f"{f}: declares `deliverables/` but the directory is missing or empty")

# 3. Agents
for f in sorted(glob.glob(str(ROOT / "agents/*.md"))):
    if ".gitkeep" in f:
        continue
    fm, _ = frontmatter(f)
    if not fm:
        continue
    for key in ("name", "description", "tools"):
        check(key in fm, f"{f}: frontmatter missing '{key}'")

# 3b. Registered legacy triggers may own reviewer-agent projection tables.
if catalog is not None:
    for domain in catalog.domains():
        trigger_path = ROOT / "skills" / domain["trigger"]["name"] / "SKILL.md"
        check(trigger_path.is_file(), f"registered domain trigger is missing: {trigger_path.relative_to(ROOT)}")
        if not trigger_path.is_file():
            continue
        for line in trigger_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("| `"):
                match = re.search(r"`([^`]+)`", line)
                if match:
                    name = match.group(1)
                    check((ROOT / f"agents/{name}.md").exists(),
                          f"{trigger_path}: references missing agents/{name}.md")

# 4. Hooks
hooks = json.load(open(ROOT / "hooks.json"))
check("SessionStart" in hooks.get("hooks", {}), "hooks.json: SessionStart missing")
boot = ROOT / "templates/session-bootstrap.txt"
check(boot.exists(), "templates/session-bootstrap.txt missing")
check(len(boot.read_text().split()) < 150, "session-bootstrap.txt too long (injected into every session — keep under 150 words)")
agents_template = ROOT / "templates/common/AGENTS.md"
check(agents_template.exists(), "templates/common/AGENTS.md missing")
if agents_template.exists():
    agent_text = agents_template.read_text(encoding="utf-8")
    check("single canonical instruction entrypoint" in agent_text,
          "AGENTS.md template must declare itself the canonical contract")
    check("`docs/agent-workflow.md`" in agent_text and "`docs/agent-working-rules.md`" in agent_text,
          "AGENTS.md template must link the shared workflow and working-rules docs")

# 4b. Shared contract checker — also used by brownfield preflight and CI.
for code, message in check_repo().items:
    findings.append(f"{code}: {message}")

handoff_skill = ROOT / "skills/handoff/SKILL.md"
if handoff_skill.is_file():
    handoff_text = handoff_skill.read_text(encoding="utf-8")
    for heading in ("## Runtime", "## Workflow", "## Canonical contract", "## Git state", "## Decisions in effect", "## Verified gates", "## Third-party tool risks"):
        check(heading in handoff_text,
              f"skills/handoff/SKILL.md: missing required handoff section '{heading}'")

# 5. Personal-info gate (this repo is public and portfolio-linked)
BANNED = re.compile(r"datmba3|freighttracker|meoanca|30kft|yuranga|job.hunt", re.I)
for f in glob.glob(str(ROOT / "**/*"), recursive=True):
    p = pathlib.Path(f)
    if p.is_dir() or ".git/" in f or p.suffix not in {".md", ".json", ".sh", ".txt", ".tpl", ".py", ".yml", ".yaml", ".mdc", ".toml", ".tsv"}:
        continue
    if p.name == "validate.py":  # the gate itself names the patterns
        continue
    for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if BANNED.search(line):
            findings.append(f"PERSONAL INFO LEAK {f}:{i}: {line.strip()[:80]}")

# 6. Skill-eval cases — static guard against trigger regressions (Tier 1).
# Each positive case names a `match` trigger phrase that MUST (a) still appear in
# its expect_skill's description and (b) appear in no other skill's description.
# Catches the common failure of editing a description and silently breaking a
# skill's triggering, or two skills fighting over the same trigger.
skill_desc = {}
for f in skill_files:
    fm, _ = frontmatter(f)
    if fm and fm.get("name"):
        skill_desc[fm["name"]] = fm.get("description", "") or ""

evals_path = ROOT / "benchmarks/skill-evals.jsonl"
check(evals_path.exists(), "benchmarks/skill-evals.jsonl missing")
if evals_path.exists():
    for i, raw in enumerate(evals_path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            case = json.loads(raw)
        except Exception as e:
            findings.append(f"skill-evals.jsonl:{i}: invalid JSON: {e}")
            continue
        exp = case.get("expect_skill")
        if exp is None:
            continue  # negative case — verifiable only behaviourally (Tier 2), skip here
        cid = case.get("id", f"line {i}")
        if exp not in skill_desc:
            findings.append(f"skill-evals [{cid}]: expect_skill '{exp}' has no skills/{exp}/SKILL.md")
            continue
        m = (case.get("match") or "").lower()
        check(bool(m), f"skill-evals [{cid}]: positive case needs a 'match' trigger phrase")
        if m:
            check(m in skill_desc[exp].lower(),
                  f"skill-evals [{cid}]: trigger '{case.get('match')}' no longer in {exp} description (trigger regressed?)")
            clash = [n for n, d in skill_desc.items() if n != exp and m in d.lower()]
            check(not clash,
                  f"skill-evals [{cid}]: trigger '{case.get('match')}' also in {clash} — trigger collision")

# 7. JSONL is append-only evidence. Scorecard v1 remains valid before the v2
# boundary; v2 records are strict and v1 may never follow the first v2 line.
for jsonl in sorted((ROOT / "benchmarks").glob("*.jsonl")):
    parsed_entries = []
    for i, raw in enumerate(jsonl.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except Exception as e:
            findings.append(f"{jsonl.name}:{i}: invalid JSON: {e}")
            continue
        parsed_entries.append(entry)
    if jsonl.name == "scorecard.jsonl":
        for code, detail in validate_scorecard(parsed_entries):
            findings.append(f"scorecard.jsonl: {code}: {detail}")

if findings:
    print(f"❌ {len(findings)} finding(s):")
    for x in findings:
        print(" -", x)
    sys.exit(1)
print("✓ all checks green")
