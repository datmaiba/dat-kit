import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import contract_check as cc


def scaffold_contract(target: Path) -> None:
    shutil.copytree(ROOT / "templates/common", target, dirs_exist_ok=True)
    (target / "AGENTS.md").write_text(
        (target / "AGENTS.md").read_text(encoding="utf-8").replace("{{PROJECT_NAME}}", "demo"),
        encoding="utf-8",
    )
    rules = target / "docs/agent-working-rules.md"
    rules.write_text("This document is part of the canonical `AGENTS.md` contract.\n", encoding="utf-8")


def codes(report):
    return {code for code, _ in report.items}


def test_empty_brownfield_is_compatible(tmp_path):
    assert not cc.check_target(tmp_path).items


def test_canonical_brownfield_is_compatible(tmp_path):
    scaffold_contract(tmp_path)
    assert not cc.check_target(tmp_path).items


@pytest.mark.parametrize(
    ("relative", "content", "diagnostic"),
    [
        ("AGENTS.md", "# competing policy\n", "COMPETING_AGENTS"),
        ("CLAUDE.md", "# Build rules\n## Quality gates\n", "POINTER_MISMATCH"),
        ("CLAUDE.md.tpl", "legacy", "LEGACY_CONTRACT"),
        (".codex/config.toml", "model_provider='local'", "RUNTIME_ADAPTER_CONFLICT"),
    ],
)
def test_conflicts_are_named(tmp_path, relative, content, diagnostic):
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    assert diagnostic in codes(cc.check_target(tmp_path))


def test_wrong_case_is_rejected(tmp_path):
    scaffold_contract(tmp_path)
    (tmp_path / "CLAUDE.md").rename(tmp_path / "claude.md")
    # A missing pointer is acceptable for partial adoption; a wrong-cased one is
    # found by the full inventory during mutation tests, so assert exact helper.
    report = cc.Report()
    assert cc.exact_path(tmp_path, "CLAUDE.md", report) is None
    assert "CONTRACT_WRONG_CASE" in codes(report)


def test_symlink_is_rejected(tmp_path):
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.write_text("x", encoding="utf-8")
    try:
        (tmp_path / "CLAUDE.md").symlink_to(outside)
    except OSError:
        pytest.skip("symlinks unavailable")
    assert "UNSAFE_SYMLINK" in codes(cc.check_target(tmp_path))


def test_registry_is_the_pointer_inventory():
    flattened = {path for paths in cc.POINTERS.values() for path in paths}
    assert flattened == set(cc.POINTER_TEMPLATES)
    assert set(cc.POINTERS) <= set(cc.RUNTIMES)
    assert "cursor" in cc.RUNTIMES


def test_registry_extension_needs_only_entry_and_template(monkeypatch, tmp_path):
    template = tmp_path / "NEW_AGENT.md"
    template.write_text("Read AGENTS.md. Do not add policy here.\n", encoding="utf-8")
    pointers = {**cc.POINTERS, "synthetic": ("NEW_AGENT.md",)}
    templates = {**cc.POINTER_TEMPLATES, "NEW_AGENT.md": str(template)}
    flattened = {path for paths in pointers.values() for path in paths}
    assert flattened == set(templates)


def test_cli_registry_json():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "contract_check.py"), "--registry-json"],
        text=True, capture_output=True, check=True,
    )
    data = json.loads(result.stdout)
    assert data["runtimes"] == list(cc.RUNTIMES)


def test_init_pointer_copy_list_matches_registry():
    script = (SCRIPTS / "init.sh").read_text(encoding="utf-8")
    for pointer in {path for paths in cc.POINTERS.values() for path in paths}:
        assert f'TARGET/{pointer}' in script
