#!/usr/bin/env python3
"""Reproducible, stdlib-only probes for Phase 0B decisions."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unicodedata
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


SUPPORTED_REGISTRY_FORMAT = 1


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def render_trigger(descriptor: dict[str, Any]) -> bytes:
    aliases = sorted(set(descriptor["trigger"]["aliases"]))
    lines = [
        "---",
        f'name: {descriptor["trigger"]["name"]}',
        f'description: {descriptor["trigger"]["description"]}',
        "---",
        "",
        f'Load domain pack `{descriptor["pack_location"]}`.',
        f'Aliases: {", ".join(aliases)}',
        f'Required engine revision: {descriptor["required_engine_revision"]}',
        "",
    ]
    return "\n".join(lines).encode("utf-8")


def probe_trigger() -> dict[str, Any]:
    first = {
        "id": "software-dev",
        "pack_location": "domains/software-dev",
        "required_engine_revision": "work-loop/1",
        "trigger": {
            "name": "build-loop",
            "description": "Execute an approved software plan.",
            "aliases": ["run build loop", "build phase"],
        },
    }
    second = json.loads(json.dumps(first))
    second["trigger"]["aliases"].reverse()
    rendered_first = render_trigger(first)
    rendered_second = render_trigger(second)
    assert rendered_first == rendered_second
    assert rendered_first.endswith(b"\n") and b"\r\n" not in rendered_first
    return {
        "decision": "sort aliases, fixed field order, UTF-8, LF, terminal newline",
        "sha256": _sha256(rendered_first),
        "byte_exact_across_input_order": True,
    }


def load_registry_bootstrap(path: Path) -> str:
    if not path.exists():
        return "REGISTRY_BOOTSTRAP_MISSING"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return "REGISTRY_BOOTSTRAP_MALFORMED"
    actual = data.get("format_revision") if isinstance(data, dict) else None
    if type(actual) is not int or actual != SUPPORTED_REGISTRY_FORMAT:
        return f"REGISTRY_FORMAT_UNSUPPORTED actual={actual!r} supported={SUPPORTED_REGISTRY_FORMAT}"
    return "OK"


def probe_registry_bootstrap(root: Path) -> dict[str, Any]:
    malformed = root / "malformed.json"
    malformed.write_text("{", encoding="utf-8")
    future = root / "future.json"
    future.write_text(
        json.dumps({"format_revision": 2, "children": ["must-not-be-loaded.json"]}),
        encoding="utf-8",
    )
    diagnostics = {
        "missing": load_registry_bootstrap(root / "missing.json"),
        "malformed": load_registry_bootstrap(malformed),
        "future_with_missing_child": load_registry_bootstrap(future),
    }
    assert diagnostics == {
        "missing": "REGISTRY_BOOTSTRAP_MISSING",
        "malformed": "REGISTRY_BOOTSTRAP_MALFORMED",
        "future_with_missing_child": "REGISTRY_FORMAT_UNSUPPORTED actual=2 supported=1",
    }
    return {
        "diagnostics": diagnostics,
        "bootstrap_precedes_child_loading": True,
        "validator": "Python standard library only",
    }


def snapshot_state(project: Path, descriptor: dict[str, str]) -> dict[str, str]:
    state: dict[str, str] = {}
    for relative, expected_hash in sorted(descriptor.items()):
        target = project / PurePosixPath(relative)
        if not target.exists():
            state[relative] = "missing"
        elif _sha256(target.read_bytes()) == expected_hash:
            state[relative] = "exact"
        else:
            state[relative] = "customized"
    return state


def probe_snapshot(root: Path) -> dict[str, Any]:
    project = root / "project-without-git"
    project.mkdir()
    agent = project / "AGENTS.md"
    workflow = project / "docs" / "agent-workflow.md"
    workflow.parent.mkdir()
    agent.write_text("canonical contract\n", encoding="utf-8")
    workflow.write_text("workflow v1\n", encoding="utf-8")
    descriptor = {
        "AGENTS.md": _sha256(agent.read_bytes()),
        "docs/agent-workflow.md": _sha256(workflow.read_bytes()),
        "docs/agent-working-rules.md": _sha256(b"rules v1\n"),
    }
    before = snapshot_state(project, descriptor)
    workflow.write_text("user customization\n", encoding="utf-8")
    after = snapshot_state(project, descriptor)
    assert not (project / ".git").exists()
    assert before == {
        "AGENTS.md": "exact",
        "docs/agent-workflow.md": "exact",
        "docs/agent-working-rules.md": "missing",
    }
    assert after["docs/agent-workflow.md"] == "customized"
    return {
        "without_git_history": True,
        "initial": before,
        "after_user_edit": after,
        "decision": "ship immutable content hashes per recognized revision",
    }


def normalize_relative_path(raw: str) -> str:
    if any(unicodedata.category(character) == "Cc" for character in raw):
        raise ValueError(f"unsafe proposal input path: {raw!r}")
    candidate = raw.replace("\\", "/")
    path = PurePosixPath(candidate)
    windows_path = PureWindowsPath(raw)
    normalized = path.as_posix()
    if (
        not raw
        or normalized == "."
        or path.is_absolute()
        or bool(windows_path.drive)
        or windows_path.is_absolute()
        or ".." in path.parts
    ):
        raise ValueError(f"unsafe proposal input path: {raw}")
    return normalized


def proposal_id(
    records: list[dict[str, Any]],
    evidence_window: str,
    policy_revision: str,
    governed_owner: str,
) -> str:
    normalized = []
    for record in records:
        copy = dict(record)
        copy["path"] = normalize_relative_path(str(copy["path"]))
        normalized.append(copy)
    payload = {
        "evidence_window": evidence_window,
        "governed_owner": governed_owner,
        "policy_revision": policy_revision,
        "records": sorted(normalized, key=lambda item: _canonical_json(item)),
    }
    return "proposal-" + _sha256(_canonical_json(payload))[:20]


def probe_proposal_ids() -> dict[str, Any]:
    posix = [
        {"path": "lessons-learned/lessons-learned.md", "hash": "aaa"},
        {"path": "benchmarks/defects.jsonl", "hash": "bbb"},
    ]
    windows_reordered = [
        {"path": "benchmarks\\defects.jsonl", "hash": "bbb"},
        {"path": "lessons-learned\\lessons-learned.md", "hash": "aaa"},
    ]
    first = proposal_id(posix, "2026-07-01/2026-07-17", "evolution/1", "software-dev")
    second = proposal_id(
        windows_reordered,
        "2026-07-01/2026-07-17",
        "evolution/1",
        "software-dev",
    )
    changed_window = proposal_id(
        posix,
        "2026-07-02/2026-07-17",
        "evolution/1",
        "software-dev",
    )
    changed_policy = proposal_id(
        posix,
        "2026-07-01/2026-07-17",
        "evolution/2",
        "software-dev",
    )
    changed_owner = proposal_id(
        posix,
        "2026-07-01/2026-07-17",
        "evolution/1",
        "knowledge-work",
    )
    assert first == second
    assert first != changed_window
    assert first != changed_policy
    assert first != changed_owner
    unsafe_paths = (
        "",
        ".",
        "./",
        "/etc/passwd",
        "C:\\secrets\\x",
        "\\\\server\\share\\x",
        "../escape",
        "foo\x00bar",
        "foo\u0085bar",
    )
    for unsafe in unsafe_paths:
        try:
            normalize_relative_path(unsafe)
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe proposal path was accepted: {unsafe!r}")
    return {
        "posix_id": first,
        "windows_reordered_id": second,
        "changed_window_id": changed_window,
        "changed_policy_id": changed_policy,
        "changed_owner_id": changed_owner,
        "separator_and_record_order_independent": True,
        "evidence_window_is_identity": True,
        "policy_revision_is_identity": True,
        "governed_owner_is_identity": True,
        "unsafe_paths_rejected": len(unsafe_paths),
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="dat-kit-phase0b-") as raw_root:
        root = Path(raw_root)
        results = {
            "domain_trigger": probe_trigger(),
            "registry_bootstrap": probe_registry_bootstrap(root),
            "project_snapshot": probe_snapshot(root),
            "proposal_ids": probe_proposal_ids(),
        }
    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
