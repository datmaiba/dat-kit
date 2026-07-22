#!/usr/bin/env python3
"""Compose reports/summary.json from already-produced tool reports.

R1 slice of the External Verification Receipt Gate plan (v2). This script is
a PRODUCER ONLY: it does not execute pytest/ruff/mypy/shellcheck/validate.py
and does not reinterpret their findings — it reads the report files each tool
already wrote and gate exit codes passed in as arguments, and writes one small
JSON summary alongside them. Deliberately no JSON Schema, no cryptographic
hashing, no receipt-verifier logic yet (that is R3, and only if R0's measured
GREEN rate ever justifies building it — see R0-feasibility-report.md).

Usage (CI):
    python3 scripts/review_summary.py \
        --junit reports/pytest-junit.xml \
        --ruff-json reports/ruff.json --ruff-exit-code 0 \
        --mypy-log reports/mypy.log --mypy-exit-code 1 \
        --validate-exit-code 0 --shellcheck-exit-code 0 \
        --os ubuntu-latest \
        --out reports/summary.json

Any input that is missing/not supplied is recorded as gate outcome
"not_run" rather than silently omitted, so a human or Codex reading the
summary can tell "skipped" apart from "forgot to wire this up".
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "summary-lite/1"


def _tool_version(cmd: list[str]) -> str:
    # S603 suppression owner: R1 producer script (review_summary.py).
    # Reason: cmd is always one of this file's own hardcoded literal lists
    # (["ruff", "--version"], ["mypy", "--version"], ["pytest", "--version"]);
    # no shell=True, no argument built from CI input or diff content. Not
    # untrusted-input execution. Review condition: re-check if a future
    # revision ever derives `cmd` from anything outside this module.
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)  # noqa: S603
        return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else "unknown"
    except Exception:
        return "unknown"


def _junit_counts(path: str | None) -> dict:
    if not path or not Path(path).exists():
        return {"outcome": "not_run", "collected": None, "passed": None, "failed": None, "skipped": None}
    try:
        # S314 suppression owner: R1 producer script (review_summary.py).
        # Reason: `path` is always this repo's own pytest --junitxml output,
        # produced by the same CI job in the same run — not a file supplied
        # by an external/untrusted party. Review condition: reconsider (use
        # defusedxml) if this script is ever pointed at a junit file that did
        # not come from this repo's own pipeline.
        root = ET.parse(path).getroot()  # noqa: S314
        # pytest emits either <testsuite> at root or <testsuites><testsuite>
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        if suite is None:
            return {"outcome": "malformed", "collected": None, "passed": None, "failed": None, "skipped": None}
        total = int(suite.get("tests", 0))
        failed = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
        skipped = int(suite.get("skipped", 0))
        passed = total - failed - skipped
        return {
            "outcome": "pass" if failed == 0 else "fail",
            "collected": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
        }
    except ET.ParseError:
        return {"outcome": "malformed", "collected": None, "passed": None, "failed": None, "skipped": None}


def _ruff_findings(path: str | None, exit_code: int | None) -> dict:
    count = None
    if path and Path(path).exists():
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            count = len(data) if isinstance(data, list) else None
        except (json.JSONDecodeError, OSError):
            count = None
    return {
        "outcome": "not_run" if exit_code is None else ("pass" if exit_code == 0 else "fail"),
        "exit_code": exit_code,
        "finding_count": count,
        "required": True,
    }


def _mypy_findings(path: str | None, exit_code: int | None) -> dict:
    count = None
    if path and Path(path).exists():
        text = Path(path).read_text(encoding="utf-8", errors="replace")
        count = sum(1 for line in text.splitlines() if ": error:" in line)
    return {
        "outcome": "not_run" if exit_code is None else "report_only",
        "exit_code": exit_code,
        "finding_count": count,
        "required": False,  # R1: mypy never fails the build (see mypy.ini header)
    }


def _simple_gate(exit_code: int | None) -> dict:
    return {"outcome": "not_run" if exit_code is None else ("pass" if exit_code == 0 else "fail"), "exit_code": exit_code}


def build_summary(args: argparse.Namespace) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "candidate_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "os": args.os or os.environ.get("RUNNER_OS", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commands": {
            "validate": "python scripts/validate.py",
            "pytest": "pytest scripts/tests --junitxml=reports/pytest-junit.xml",
            "ruff": "ruff check --output-format=json --output-file=reports/ruff.json .",
            "mypy": "mypy scripts --config-file mypy.ini",
            "shellcheck": "shellcheck scripts/init.sh",
        },
        "tool_versions": {
            "python": sys.version.split()[0],
            "ruff": _tool_version(["ruff", "--version"]),
            "mypy": _tool_version(["mypy", "--version"]),
            "pytest": _tool_version(["pytest", "--version"]),
        },
        "gates": {
            "validate": _simple_gate(args.validate_exit_code),
            "pytest": _junit_counts(args.junit),
            "ruff": _ruff_findings(args.ruff_json, args.ruff_exit_code),
            "mypy": _mypy_findings(args.mypy_log, args.mypy_exit_code),
            "shellcheck": _simple_gate(args.shellcheck_exit_code),
        },
        "required_gate_set": ["validate", "pytest", "ruff", "shellcheck"],
        "artifact_paths": [p for p in [args.junit, args.ruff_json, args.mypy_log] if p and Path(p).exists()],
        "completed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--junit")
    parser.add_argument("--ruff-json")
    parser.add_argument("--ruff-exit-code", type=int)
    parser.add_argument("--mypy-log")
    parser.add_argument("--mypy-exit-code", type=int)
    parser.add_argument("--validate-exit-code", type=int)
    parser.add_argument("--shellcheck-exit-code", type=int)
    parser.add_argument("--os")
    parser.add_argument("--out", default="reports/summary.json")
    args = parser.parse_args()

    summary = build_summary(args)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    required_ok = all(
        summary["gates"][g]["outcome"] == "pass" for g in summary["required_gate_set"]
    )
    print(f"summary written to {out_path} — required gates {'PASS' if required_ok else 'FAIL'}")
    return 0 if required_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
