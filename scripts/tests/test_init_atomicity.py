from pathlib import Path
import os
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[2]
INIT = ROOT / "scripts/init.sh"


def bash_executable():
    candidates = [r"C:\Program Files\Git\bin\bash.exe", shutil.which("bash")]
    return next((value for value in candidates if value and Path(value).exists()), None)


def snapshot(root: Path):
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*") if path.is_file()
    }


def run_here(target: Path):
    bash = bash_executable()
    if not bash:
        pytest.skip("bash unavailable")
    env = os.environ.copy()
    env["PATH"] = str(Path(os.sys.executable).parent) + os.pathsep + env.get("PATH", "")
    return subprocess.run(
        [bash, INIT.as_posix(), "--here", "--profile", "react"], cwd=target,
        text=True, capture_output=True, env=env, check=False,
    )


def test_hostile_brownfield_is_byte_preserved(tmp_path):
    (tmp_path / "CLAUDE.md").write_bytes(b"# private policy\r\n## Quality gates\r\n")
    (tmp_path / "app.txt").write_bytes(b"user bytes\x00\xff")
    before = snapshot(tmp_path)
    result = run_here(tmp_path)
    assert result.returncode != 0
    assert "POINTER_MISMATCH" in result.stdout
    assert snapshot(tmp_path) == before


def test_canonical_rerun_is_idempotent(tmp_path):
    first = run_here(tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    before = snapshot(tmp_path)
    second = run_here(tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    assert snapshot(tmp_path) == before


def test_compatible_partial_gets_only_missing_files(tmp_path):
    workflow = tmp_path / "docs/agent-workflow.md"
    workflow.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "templates/common/docs/agent-workflow.md", workflow)
    preserved = workflow.read_bytes()
    result = run_here(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert workflow.read_bytes() == preserved
    assert (tmp_path / "AGENTS.md").is_file()
