"""Tests for scripts/review_summary.py — R1 slice of the receipt-gate plan.

Covers the negative/edge cases a producer-only script must get right: missing
inputs marked not_run (not silently dropped), malformed XML detected instead
of crashing, correct pass/fail counting, and the required-gate-set exit code.
Written observed-red-before-green per docs/agent-working-rules.md: run these
against review_summary.py with a deliberately broken junit parser first to
confirm they fail, then restore.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review_summary as rs  # noqa: E402


JUNIT_PASS = """<?xml version="1.0"?>
<testsuite name="pytest" tests="10" failures="0" errors="0" skipped="1"></testsuite>
"""

JUNIT_FAIL = """<?xml version="1.0"?>
<testsuite name="pytest" tests="10" failures="2" errors="0" skipped="0"></testsuite>
"""

JUNIT_MALFORMED = "<testsuite this is not valid xml"


def test_junit_counts_missing_file_is_not_run(tmp_path):
    result = rs._junit_counts(str(tmp_path / "nope.xml"))
    assert result["outcome"] == "not_run"
    assert result["collected"] is None


def test_junit_counts_pass(tmp_path):
    p = tmp_path / "junit.xml"
    p.write_text(JUNIT_PASS, encoding="utf-8")
    result = rs._junit_counts(str(p))
    assert result == {"outcome": "pass", "collected": 10, "passed": 9, "failed": 0, "skipped": 1}


def test_junit_counts_fail(tmp_path):
    p = tmp_path / "junit.xml"
    p.write_text(JUNIT_FAIL, encoding="utf-8")
    result = rs._junit_counts(str(p))
    assert result["outcome"] == "fail"
    assert result["failed"] == 2
    assert result["passed"] == 8


def test_junit_counts_malformed_does_not_raise(tmp_path):
    p = tmp_path / "junit.xml"
    p.write_text(JUNIT_MALFORMED, encoding="utf-8")
    result = rs._junit_counts(str(p))
    assert result["outcome"] == "malformed"


def test_ruff_findings_counts_list_length(tmp_path):
    p = tmp_path / "ruff.json"
    p.write_text(json.dumps([{"code": "F401"}, {"code": "S101"}]), encoding="utf-8")
    result = rs._ruff_findings(str(p), exit_code=1)
    assert result["finding_count"] == 2
    assert result["outcome"] == "fail"
    assert result["required"] is True


def test_ruff_findings_missing_report_still_records_exit_code(tmp_path):
    result = rs._ruff_findings(str(tmp_path / "missing.json"), exit_code=0)
    assert result["outcome"] == "pass"
    assert result["finding_count"] is None


def test_mypy_is_never_required():
    # No log path AND no exit code == the job genuinely didn't run.
    result = rs._mypy_findings(None, exit_code=None)
    assert result["required"] is False
    assert result["outcome"] == "not_run"


def test_mypy_ran_but_report_missing_is_still_report_only():
    # exit_code present (mypy executed) but no log file -> report_only with
    # an unknown finding_count, distinct from "didn't run at all".
    result = rs._mypy_findings(None, exit_code=1)
    assert result["outcome"] == "report_only"
    assert result["finding_count"] is None
    assert result["required"] is False


def test_mypy_report_only_outcome(tmp_path):
    p = tmp_path / "mypy.log"
    p.write_text("scripts/foo.py:1: error: bad type\n", encoding="utf-8")
    result = rs._mypy_findings(str(p), exit_code=1)
    assert result["outcome"] == "report_only"
    assert result["finding_count"] == 1
    assert result["required"] is False


def test_build_summary_required_gates_pass_returns_exit_0(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    junit = tmp_path / "junit.xml"
    junit.write_text(JUNIT_PASS, encoding="utf-8")
    import argparse

    args = argparse.Namespace(
        junit=str(junit), ruff_json=None, ruff_exit_code=0,
        mypy_log=None, mypy_exit_code=None,
        validate_exit_code=0, shellcheck_exit_code=0,
        os="ubuntu-latest", out=str(tmp_path / "summary.json"),
    )
    summary = rs.build_summary(args)
    assert summary["gates"]["validate"]["outcome"] == "pass"
    assert summary["gates"]["pytest"]["outcome"] == "pass"
    assert summary["required_gate_set"] == ["validate", "pytest", "ruff", "shellcheck"]


def test_build_summary_required_gate_failure_is_visible(tmp_path):
    import argparse

    args = argparse.Namespace(
        junit=None, ruff_json=None, ruff_exit_code=1,  # ruff failed
        mypy_log=None, mypy_exit_code=None,
        validate_exit_code=0, shellcheck_exit_code=0,
        os="ubuntu-latest", out=str(tmp_path / "summary.json"),
    )
    summary = rs.build_summary(args)
    assert summary["gates"]["ruff"]["outcome"] == "fail"


def test_main_writes_file_and_exit_code_reflects_required_gates(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    junit = tmp_path / "junit.xml"
    junit.write_text(JUNIT_PASS, encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_summary.py",
            "--junit", str(junit),
            "--ruff-exit-code", "0",
            "--validate-exit-code", "0",
            "--shellcheck-exit-code", "0",
            "--out", str(tmp_path / "reports" / "summary.json"),
        ],
    )
    exit_code = rs.main()
    assert exit_code == 0
    assert (tmp_path / "reports" / "summary.json").exists()


def test_main_nonzero_exit_when_required_gate_failed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_summary.py",
            "--ruff-exit-code", "1",  # required gate failed
            "--validate-exit-code", "0",
            "--shellcheck-exit-code", "0",
            "--out", str(tmp_path / "reports" / "summary.json"),
        ],
    )
    exit_code = rs.main()
    assert exit_code == 1
