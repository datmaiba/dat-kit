"""Plan §6 Phase 3 fixtures: project-contract revision state machine.

Six mandated states: clean v1.16 (nonzero + deterministic preview),
customized v1.16 (preserved + conflict), clean v2 (green), partial (named
diagnostic), unknown revision (unsupported, no mutation), missing marker with
recognizable files (ambiguous, no mutation). All paths are read-only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import contract_check as cc
from test_contract_check import scaffold_contract


def tree_hash(target: Path) -> dict[str, str]:
    # lstat-based: a file swapped for a symlink to identical content must
    # register as a change (no-follow discipline, security review item 6).
    result: dict[str, str] = {}
    for path in sorted(target.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            result[str(path.relative_to(target))] = "symlink:" + str(path.readlink())
        elif stat.S_ISREG(mode):
            result[str(path.relative_to(target))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def run_cli(target: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "contract_check.py"), "--target", str(target), *extra],
        capture_output=True,
        text=True,
    )


def codes(report) -> set[str]:
    return {item.code for item in report.diagnostics}


def scaffold_v2(target: Path) -> None:
    (target / "AGENTS.md").write_text(
        "# Agent contract — demo\n\n"
        "**Canonical contract revision:** dat-kit 2.0\n\n"
        "This file is the single canonical instruction entrypoint.\n",
        encoding="utf-8",
    )
    (target / "CLAUDE.md").write_text(
        (ROOT / "templates/common/CLAUDE.md").read_text(encoding="utf-8"), encoding="utf-8"
    )


# 1. clean v1.16 → nonzero, deterministic preview ---------------------------

def test_clean_v116_nonzero_with_deterministic_preview(tmp_path):
    scaffold_contract(tmp_path)
    before = tree_hash(tmp_path)
    result = run_cli(tmp_path)
    assert result.returncode == 1
    assert "CONTRACT_MIGRATION_REQUIRED" in result.stdout
    first = run_cli(tmp_path, "--migration-plan", "--format", "json")
    second = run_cli(tmp_path, "--migration-plan", "--format", "json")
    assert first.returncode == 1 and first.stdout == second.stdout
    plan = json.loads(first.stdout)["migration_plan"]
    instructions = {step["instruction"] for step in plan["steps"]}
    assert "REMOVE_LEGACY_POINTER" in instructions  # typed RETIRE_LEGACY
    assert "ADD_RULES_POINTER" in instructions      # .cursor/rules only in plan
    assert tree_hash(tmp_path) == before            # read-only


# 2. customized v1.16 → nonzero, preserved, conflict reported ---------------

def test_customized_v116_reports_conflict_and_preserves(tmp_path):
    scaffold_contract(tmp_path)
    custom = tmp_path / ".claude/CLAUDE.md"
    custom.write_text(custom.read_text(encoding="utf-8") + "\nMy local note.\n", encoding="utf-8")
    before = tree_hash(tmp_path)
    report = cc.check_target(tmp_path)
    assert "CONTRACT_MIGRATION_REQUIRED" in codes(report)
    conflicts = [i for i in report.diagnostics if i.code == "CONTRACT_MIGRATION_CONFLICT"]
    assert [i.path for i in conflicts] == [".claude/CLAUDE.md"]
    assert all(i.action == "MERGE_REQUIRED" for i in conflicts)  # never overwrite
    assert tree_hash(tmp_path) == before


# 3. clean v2 → green --------------------------------------------------------

def test_clean_v2_is_green(tmp_path):
    scaffold_v2(tmp_path)
    report = cc.check_target(tmp_path)
    assert report.revision_state == "green"
    assert not report.diagnostics, [i.code for i in report.diagnostics]
    assert run_cli(tmp_path).returncode == 0


# 4. partially migrated → named diagnostic ----------------------------------

def test_partial_migration_is_named(tmp_path):
    scaffold_v2(tmp_path)
    (tmp_path / "CLAUDE.md").unlink()  # green marker, incomplete pointer set
    report = cc.check_target(tmp_path)
    assert report.revision_state == "partial"
    assert "CONTRACT_PARTIAL_MIGRATION" in codes(report)


def test_mixed_markers_are_partial(tmp_path):
    scaffold_v2(tmp_path)
    agents = tmp_path / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8") + "\nMigrated from dat-kit 1.16.0.\n",
        encoding="utf-8",
    )
    report = cc.check_target(tmp_path)
    assert report.revision_state == "partial"
    assert "CONTRACT_PARTIAL_MIGRATION" in codes(report)


# 5. unknown revision → unsupported, no mutation -----------------------------

def test_unknown_revision_is_unsupported_without_mutation(tmp_path):
    (tmp_path / "AGENTS.md").write_text(
        "# dat-kit guidance\n**Canonical contract revision:** dat-kit 3.7.9\n",
        encoding="utf-8",
    )
    before = tree_hash(tmp_path)
    report = cc.check_target(tmp_path)
    assert report.revision_state == "unsupported"
    assert "CONTRACT_UNSUPPORTED_REVISION" in codes(report)
    assert tree_hash(tmp_path) == before


def test_pre_marker_generation_is_unsupported_with_guidance(tmp_path):
    (tmp_path / "CLAUDE.md.tpl").write_text("legacy template\n", encoding="utf-8")
    report = cc.check_target(tmp_path)
    assert report.revision_state == "unsupported"
    assert "CONTRACT_UNSUPPORTED_REVISION" in codes(report)


# 6. missing marker + recognizable files → ambiguous, no mutation ------------

def test_missing_marker_with_recognizable_files_is_ambiguous(tmp_path):
    (tmp_path / "AGENTS.md").write_text(
        "# dat-kit guidance\nThis is the canonical, agent-neutral contract.\n",
        encoding="utf-8",
    )
    before = tree_hash(tmp_path)
    report = cc.check_target(tmp_path)
    assert report.revision_state == "partial"
    ambiguous = [i for i in report.diagnostics if i.classification == "ambiguous-no-marker"]
    assert ambiguous and ambiguous[0].code == "CONTRACT_PARTIAL_MIGRATION"
    assert tree_hash(tmp_path) == before


# plain brownfield without dat-kit traces stays out of the state machine ----

def test_non_dat_kit_tree_is_unclassified(tmp_path):
    (tmp_path / "README.md").write_text("hello\n", encoding="utf-8")
    report = cc.check_target(tmp_path)
    assert report.revision_state == "unclassified"
    assert not {c for c in codes(report) if c.startswith("CONTRACT_")}
