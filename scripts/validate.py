#!/usr/bin/env python3
"""dat-kit repo validation — run locally (python3 scripts/validate.py) and in CI.

Checks: manifest JSON validity + version sync, skill/agent frontmatter,
description limits, body-length budgets, hooks.json shape, personal-info gate.
Exit 0 = all green; exit 1 = findings printed.
"""
import json, re, sys, glob, pathlib

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
        import yaml
        return yaml.safe_load(parts[1]), text
    except Exception as e:
        findings.append(f"{path}: frontmatter YAML error: {e}")
        return None, text


# 1. Manifests
plugin = json.load(open(ROOT / ".claude-plugin/plugin.json"))
market = json.load(open(ROOT / ".claude-plugin/marketplace.json"))
check(plugin["name"] == "dat-kit", "plugin.json: unexpected name")
check(re.match(r"^\d+\.\d+\.\d+", plugin.get("version", "")), "plugin.json: version must be semver")
check(plugin["version"] == market["plugins"][0]["version"],
      f"version mismatch: plugin.json {plugin['version']} vs marketplace.json {market['plugins'][0]['version']}")
check(market["plugins"][0]["source"] == "./", "marketplace.json: source must be './'")
check(plugin.get("hooks") == "./hooks.json", "plugin.json: hooks must be declared explicitly (auto-discovery unreliable in dev mode)")

# 2. Skills
for f in sorted(glob.glob(str(ROOT / "skills/*/SKILL.md"))):
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
for f in sorted(glob.glob(str(ROOT / "skills/*/SKILL.md"))):
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

# 3b. Agent-existence gate — the review team table in build-loop is the single source of truth
build_loop = ROOT / "skills/build-loop/SKILL.md"
for line in build_loop.read_text(encoding="utf-8").splitlines():
    if line.startswith("| `"):
        m = re.search(r"`([^`]+)`", line)
        if m:
            name = m.group(1)
            check((ROOT / f"agents/{name}.md").exists(),
                  f"build-loop references agent '{name}' but agents/{name}.md does not exist")

# 4. Hooks
hooks = json.load(open(ROOT / "hooks.json"))
check("SessionStart" in hooks.get("hooks", {}), "hooks.json: SessionStart missing")
boot = ROOT / "templates/session-bootstrap.txt"
check(boot.exists(), "templates/session-bootstrap.txt missing")
check(len(boot.read_text().split()) < 150, "session-bootstrap.txt too long (injected into every session — keep under 150 words)")

# 5. Personal-info gate (this repo is public and portfolio-linked)
BANNED = re.compile(r"datmba3|freighttracker|meoanca|30kft|yuranga|job.hunt", re.I)
for f in glob.glob(str(ROOT / "**/*"), recursive=True):
    p = pathlib.Path(f)
    if p.is_dir() or ".git/" in f or p.suffix not in {".md", ".json", ".sh", ".txt", ".tpl", ".py", ".yml", ".yaml"}:
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
for f in sorted(glob.glob(str(ROOT / "skills/*/SKILL.md"))):
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

if findings:
    print(f"❌ {len(findings)} finding(s):")
    for x in findings:
        print(" -", x)
    sys.exit(1)
print("✓ all checks green")
