#!/usr/bin/env python3
"""Shared dat-kit contract checker and brownfield preflight (stdlib only)."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_REVISION = "dat-kit 1.16.0"
POINTERS = {
    "claude-code": ("CLAUDE.md", ".claude/CLAUDE.md"),
    "cursor": (".cursorrules",),
    "codex": (),
}
RUNTIMES = tuple(POINTERS) + ("other",)
POINTER_TEMPLATES = {
    "CLAUDE.md": "templates/common/CLAUDE.md",
    ".claude/CLAUDE.md": "templates/common/.claude/CLAUDE.md",
    ".cursorrules": "templates/common/.cursorrules",
}
CANONICAL_STATIC = {
    **POINTER_TEMPLATES,
    "docs/agent-workflow.md": "templates/common/docs/agent-workflow.md",
}
LOCAL_CONFIGS = (".codex/config.toml", ".codex/hooks.json")
LEGACY = ("CLAUDE.md.tpl", "rules/working.rules.md")
POLICY_TERMS = re.compile(
    r"(^##|\bMUST\b|quality gates?|build-loop|architecture rules?|plan gate)", re.I | re.M
)


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str]] = []

    def add(self, code: str, message: str) -> None:
        self.items.append((code, message))

    def emit(self) -> int:
        for code, message in self.items:
            print(f"{code}: {message}")
        return 1 if self.items else 0


def normalized(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def exact_path(root: Path, relative: str, report: Report) -> Path | None:
    current = root
    for part in PurePosixPath(relative).parts:
        if not current.is_dir():
            report.add("CONTRACT_MISSING", f"{relative}: parent is missing")
            return None
        names = {child.name for child in current.iterdir()}
        if part not in names:
            folded = [name for name in names if name.casefold() == part.casefold()]
            code = "CONTRACT_WRONG_CASE" if folded else "CONTRACT_MISSING"
            report.add(code, f"{relative}: expected segment {part!r}")
            return None
        current = current / part
    return current


def wrong_case_if_present(root: Path, relative: str, report: Report) -> None:
    current = root
    for part in PurePosixPath(relative).parts:
        if not current.is_dir():
            return
        names = {child.name for child in current.iterdir()}
        if part in names:
            current /= part
            continue
        if any(name.casefold() == part.casefold() for name in names):
            report.add("CONTRACT_WRONG_CASE", f"{relative}: expected segment {part!r}")
        return


def is_tracked(path: str) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return result.returncode == 0


def check_pointer(path: Path, template: Path, label: str, report: Report) -> None:
    text = normalized(path)
    if text != normalized(template):
        report.add("POINTER_MISMATCH", f"{label}: differs from {template.relative_to(ROOT)}")
    if "AGENTS.md" not in text or POLICY_TERMS.search(text):
        report.add("POINTER_POLICY", f"{label}: must be a policy-free AGENTS.md pointer")


def manifest_versions(report: Report) -> None:
    sources = (
        (".claude-plugin/plugin.json", lambda d: d.get("version")),
        (".codex-plugin/plugin.json", lambda d: d.get("version")),
        (".claude-plugin/marketplace.json", lambda d: d.get("plugins", [{}])[0].get("version")),
    )
    expected = CONTRACT_REVISION.rsplit(" ", 1)[-1]
    for rel, getter in sources:
        try:
            value = getter(json.loads((ROOT / rel).read_text(encoding="utf-8")))
        except (OSError, ValueError, IndexError) as exc:
            report.add("MANIFEST_INVALID", f"{rel}: {exc}")
            continue
        if value != expected:
            report.add("CONTRACT_REVISION_MISMATCH", f"{rel}: {value!r}, expected {expected!r}")


def check_repo(root: Path = ROOT) -> Report:
    report = Report()
    required = (
        "AGENTS.md", "docs/agent-workflow.md", "docs/agent-working-rules.md",
        "templates/common/AGENTS.md", "templates/common/docs/agent-workflow.md",
        "templates/common/docs/agent-working-rules.md.tpl",
    )
    for rel in required:
        exact_path(root, rel, report)
    for pointer, template in POINTER_TEMPLATES.items():
        source = exact_path(root, template, report)
        if source:
            check_pointer(source, source, template, report)
    for legacy in ("templates/common/CLAUDE.md.tpl", "templates/common/rules/working.rules.md"):
        if (root / legacy).exists():
            report.add("LEGACY_CONTRACT", f"{legacy}: migrate manually; see docs/codex.md")
    for local in LOCAL_CONFIGS:
        if (root / local).exists() and is_tracked(local):
            report.add("TRACKED_RUNTIME_CONFIG", f"{local}: machine-local runtime config must not be tracked")
    bootstrap = root / "templates/session-bootstrap.txt"
    if not bootstrap.exists():
        report.add("ADAPTER_MISSING", "templates/session-bootstrap.txt is missing")
    else:
        text = normalized(bootstrap)
        if "AGENTS.md" not in text or POLICY_TERMS.search(text) or len(text.splitlines()) > 3:
            report.add("ADAPTER_POLICY", "session bootstrap must only locate AGENTS.md and provide the adoption fallback")
    try:
        hook_text = normalized(root / "hooks.json")
        hook = json.loads(hook_text)
        if any(term in hook_text for term in ("ANTHROPIC_BASE_URL", "build-loop", "quality gate")):
            report.add("ADAPTER_POLICY", "hooks.json contains shared policy or machine-local routing")
        if "SessionStart" not in hook.get("hooks", {}):
            report.add("ADAPTER_INVALID", "hooks.json has no SessionStart adapter")
    except (OSError, ValueError) as exc:
        report.add("ADAPTER_INVALID", f"hooks.json: {exc}")
    agents = root / "templates/common/AGENTS.md"
    if agents.exists() and CONTRACT_REVISION not in normalized(agents):
        report.add("CONTRACT_REVISION_MISMATCH", "templates/common/AGENTS.md revision is stale")
    manifest_versions(report)
    return report


def contained(root: Path, path: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def check_target(target: Path) -> Report:
    report = Report()
    try:
        root = target.resolve(strict=True)
    except OSError as exc:
        report.add("TARGET_INVALID", str(exc))
        return report
    if not root.is_dir():
        report.add("TARGET_INVALID", f"{root} is not a directory")
        return report

    inventory = {"AGENTS.md", "docs/agent-workflow.md", "docs/agent-working-rules.md"}
    inventory.update(POINTER_TEMPLATES)
    inventory.update(LOCAL_CONFIGS)
    inventory.update(LEGACY)
    for source in (ROOT / "templates/common").rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT / "templates/common").as_posix()
        if relative == "docs/agent-working-rules.md.tpl":
            relative = "docs/agent-working-rules.md"
        inventory.add(relative)
    for rel in sorted(inventory):
        wrong_case_if_present(root, rel, report)
        path = root / PurePosixPath(rel)
        if path.is_symlink():
            report.add("UNSAFE_SYMLINK", f"{rel}: symlinks are not accepted during brownfield adoption")
        if not contained(root, path):
            report.add("TARGET_ESCAPE", f"{rel}: resolves outside target")

    for legacy in LEGACY:
        if (root / legacy).exists():
            report.add("LEGACY_CONTRACT", f"{legacy}: migrate manually; see docs/codex.md")

    agents = root / "AGENTS.md"
    if agents.exists():
        text = normalized(agents)
        if "single canonical instruction entrypoint" not in text or CONTRACT_REVISION not in text:
            report.add("COMPETING_AGENTS", "AGENTS.md is not the current dat-kit canonical contract")

    for rel, template_rel in CANONICAL_STATIC.items():
        path = root / PurePosixPath(rel)
        if not path.exists():
            continue
        template = ROOT / template_rel
        if rel in POINTER_TEMPLATES:
            check_pointer(path, template, rel, report)
        elif normalized(path) != normalized(template):
            report.add("PARTIAL_INSTALL_MISMATCH", f"{rel}: existing canonical file differs from current template")

    rules = root / "docs/agent-working-rules.md"
    if rules.exists() and "This document is part of the canonical `AGENTS.md` contract." not in normalized(rules):
        report.add("PARTIAL_INSTALL_MISMATCH", "docs/agent-working-rules.md is not a dat-kit canonical file")

    for local in LOCAL_CONFIGS:
        path = root / PurePosixPath(local)
        if path.exists():
            report.add("RUNTIME_ADAPTER_CONFLICT", f"{local}: inspect and remove policy or machine-local activation manually")
    return report


def registry_json() -> dict[str, object]:
    return {
        "contract_revision": CONTRACT_REVISION,
        "pointers": {name: list(paths) for name, paths in POINTERS.items()},
        "runtimes": list(RUNTIMES),
        "templates": POINTER_TEMPLATES,
    }


def validate_scorecard(entries: Iterable[dict[str, object]]) -> list[tuple[str, str]]:
    """Validate the append-only v1/v2 boundary and strict v2 evidence shape."""
    result: list[tuple[str, str]] = []
    seen_v2 = False
    for index, entry in enumerate(entries, 1):
        if "schema_version" not in entry:
            if seen_v2:
                result.append(("SCORECARD_V1_AFTER_V2", f"line {index}"))
            continue
        seen_v2 = True
        if not isinstance(entry.get("schema_version"), int) or entry.get("schema_version", 0) < 2:
            result.append(("SCORECARD_SCHEMA_VERSION", f"line {index}"))
        if entry.get("agent_runtime") not in RUNTIMES:
            result.append(("SCORECARD_AGENT_RUNTIME", f"line {index}"))
        for field in ("workflow", "canonical_contract_revision"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                result.append((f"SCORECARD_{field.upper()}", f"line {index}"))
        state = entry.get("git_state")
        if not isinstance(state, dict):
            result.append(("SCORECARD_GIT_STATE", f"line {index}"))
            continue
        for field in ("branch", "head"):
            if state.get(field) is not None and not isinstance(state.get(field), str):
                result.append((f"SCORECARD_GIT_{field.upper()}", f"line {index}"))
        if state.get("dirty") is not None and not isinstance(state.get("dirty"), bool):
            result.append(("SCORECARD_GIT_DIRTY", f"line {index}"))
    return result


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, help="read-only brownfield preflight")
    parser.add_argument("--registry-json", action="store_true")
    args = parser.parse_args(argv)
    if args.registry_json:
        print(json.dumps(registry_json(), sort_keys=True))
        return 0
    return (check_target(args.target) if args.target else check_repo()).emit()


if __name__ == "__main__":
    sys.exit(main())
