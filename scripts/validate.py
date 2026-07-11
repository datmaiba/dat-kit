#!/usr/bin/env python3
"""dat-kit repo validation — run locally (python3 scripts/validate.py) and in CI.

Checks: manifest JSON validity + version sync, skill/agent frontmatter,
description limits, body-length budgets, hooks.json shape, personal-info gate.
Exit 0 = all green; exit 1 = findings printed.
"""
import json, re, sys, glob, pathlib

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

# 3. Agents
for f in sorted(glob.glob(str(ROOT / "agents/*.md"))):
    if ".gitkeep" in f:
        continue
    fm, _ = frontmatter(f)
    if not fm:
        continue
    for key in ("name", "description", "tools"):
        check(key in fm, f"{f}: frontmatter missing '{key}'")

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

if findings:
    print(f"❌ {len(findings)} finding(s):")
    for x in findings:
        print(" -", x)
    sys.exit(1)
print("✓ all checks green")
