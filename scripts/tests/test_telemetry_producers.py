import importlib.util
import json
from pathlib import Path
import sys
import uuid

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import scorecard
import telemetry as telemetry_runtime


def _load_producers():
    path = ROOT / "telemetry" / "producers.py"
    spec = importlib.util.spec_from_file_location("dat_kit_producers_test", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


producers = _load_producers()
ROOT_CAUSE_REF = f"evidence:root-cause:{'a' * 64}"
CANDIDATE_REF = f"evidence:lesson-candidate:{'b' * 64}"


def _scorecard_record():
    return {
        "schema_version": 2,
        "ts": "2026-07-23T12:00:00+07:00",
        "date": "2026-07-23",
        "task": "B3 producer test",
        "complexity": 2,
        "notes": "test fixture",
        "est_manual_hours": 1,
        "actual_wall_minutes": 5,
        "gates": "pytest",
        "tokens": None,
        "model": "test",
        "agent_runtime": "codex",
        "workflow": "build-loop",
        "canonical_contract_revision": "dat-kit 1.16.0",
        "git_state": {"branch": "test", "head": "abc", "dirty": True},
    }


def _start(root, capsys):
    assert telemetry_runtime.main(
        ["--repository-root", str(root), "start", "--workflow", "build-loop"],
        environ={},
    ) == 0
    return json.loads(capsys.readouterr().out)["task_id"]


def _emit(root, capsys, *, locus="gate"):
    task_id = _start(root, capsys)
    return producers.emit_build_loop_harvest(
        root,
        task_id=task_id,
        root_cause_locus=locus,
        root_cause_ref=ROOT_CAUSE_REF,
        candidate_ref=CANDIDATE_REF,
    )


def test_harvest_reuses_one_load_minted_partial_build_loop_lifecycle(tmp_path, capsys):
    result = _emit(tmp_path, capsys)
    events = telemetry_runtime.validate_lifecycle_events(tmp_path)

    assert result["status"] == "ok"
    assert uuid.UUID(result["task_id"]).version == 4
    assert [event["event_type"] for event in events] == [
        "task_started",
        "lesson_candidate_recorded",
        "task_finished",
    ]
    assert {event["task_id"] for event in events} == {result["task_id"]}
    assert events[1]["payload"] == {
        "kit_facing": True,
        "root_cause_ref": ROOT_CAUSE_REF,
        "candidate_ref": CANDIDATE_REF,
    }
    assert events[-1]["coverage"] == {
        "status": "partial",
        "missing_event_types": ["gate_result", "review_result"],
        "missing_requirement_refs": [],
        "reason": "producer_failure",
    }


@pytest.mark.parametrize(
    ("locus", "expected"),
    [
        ("skill", True),
        ("template", True),
        ("gate", True),
        ("agent-charter", False),
        ("ci", False),
        ("git", False),
        ("host", False),
    ],
)
def test_kit_facing_is_derived_from_the_closed_locus(tmp_path, capsys, locus, expected):
    _emit(tmp_path, capsys, locus=locus)
    events = telemetry_runtime.validate_lifecycle_events(tmp_path)
    assert events[1]["payload"]["kit_facing"] is expected


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("root_cause_ref", "human readable root cause"),
        ("root_cause_ref", "prose-title"),
        ("root_cause_ref", "evidence:the-root-cause-was-a-race-condition"),
        ("candidate_ref", "candidate prose"),
        ("candidate_ref", "artifact:but-not-producer-evidence"),
        ("candidate_ref", "evidence:the-candidate-was-a-new-regression-test"),
    ],
)
def test_references_must_be_producer_owned_stable_evidence(tmp_path, capsys, field, value):
    task_id = _start(tmp_path, capsys)
    path = tmp_path / telemetry_runtime.EVENT_PATH
    before = path.read_bytes()
    arguments = {
        "task_id": task_id,
        "root_cause_locus": "gate",
        "root_cause_ref": ROOT_CAUSE_REF,
        "candidate_ref": CANDIDATE_REF,
    }
    arguments[field] = value

    with pytest.raises(ValueError, match=field):
        producers.emit_build_loop_harvest(tmp_path, **arguments)

    assert path.read_bytes() == before


def test_scorecard_without_real_candidate_emits_nothing(tmp_path):
    path = tmp_path / "benchmarks" / "scorecard.jsonl"

    record, telemetry_result = scorecard.append_scorecard_with_harvest(
        path,
        _scorecard_record(),
        provider="codex",
    )

    assert record["task"] == "B3 producer test"
    assert telemetry_result == {"status": "not_applicable", "event_count": 0}
    assert not (tmp_path / telemetry_runtime.EVENT_PATH).exists()


def test_scorecard_seam_reuses_existing_task_and_real_receipts(tmp_path, capsys):
    task_id = _start(tmp_path, capsys)
    path = tmp_path / "benchmarks" / "scorecard.jsonl"

    _record, telemetry_result = scorecard.append_scorecard_with_harvest(
        path,
        _scorecard_record(),
        provider="codex",
        task_id=task_id,
        root_cause_locus="gate",
        root_cause_ref=ROOT_CAUSE_REF,
        candidate_ref=CANDIDATE_REF,
    )

    events = telemetry_runtime.validate_lifecycle_events(tmp_path)
    assert telemetry_result["task_id"] == task_id
    assert [event["event_type"] for event in events] == [
        "task_started",
        "lesson_candidate_recorded",
        "task_finished",
    ]


def test_scorecard_append_succeeds_without_event_file_when_disabled(tmp_path):
    path = tmp_path / "benchmarks" / "scorecard.jsonl"
    record, telemetry_result = scorecard.append_scorecard_with_harvest(
        path,
        _scorecard_record(),
        provider="codex",
        task_id=str(uuid.uuid4()),
        root_cause_locus="gate",
        root_cause_ref=ROOT_CAUSE_REF,
        candidate_ref=CANDIDATE_REF,
        environ={"DAT_KIT_TELEMETRY": "off"},
    )

    assert record["task"] == "B3 producer test"
    assert telemetry_result == {"status": "disabled", "event_count": 0}
    assert path.exists()
    assert not (tmp_path / telemetry_runtime.EVENT_PATH).exists()


def test_scorecard_append_survives_unavailable_telemetry_target(tmp_path):
    path = tmp_path / "benchmarks" / "scorecard.jsonl"
    (tmp_path / "telemetry").write_text("not a directory", encoding="utf-8")

    record, telemetry_result = scorecard.append_scorecard_with_harvest(
        path,
        _scorecard_record(),
        provider="codex",
        task_id=str(uuid.uuid4()),
        root_cause_locus="gate",
        root_cause_ref=ROOT_CAUSE_REF,
        candidate_ref=CANDIDATE_REF,
    )

    assert record["task"] == "B3 producer test"
    assert json.loads(path.read_text(encoding="utf-8"))["task"] == record["task"]
    assert telemetry_result["status"] == "degraded"
    assert telemetry_result["reason"] == "producer_failure"


def test_status_registry_is_closed_and_all_five_producers_are_planned():
    registry = producers.load_producer_registry()

    assert set(registry["producers"]) == set(producers.PRODUCER_IDS)
    assert len(registry["producers"]) == 5
    assert all(
        item == {"status": "planned", "event_id": None}
        for item in registry["producers"].values()
    )


def test_status_registry_rejects_active_without_receipt_event_id():
    registry = producers.load_producer_registry()
    registry["producers"]["build-loop-harvest"]["status"] = "active"

    with pytest.raises(ValueError, match="event_id"):
        producers.validate_producer_registry(registry)


def test_status_registry_rejects_uuid_not_bound_to_validated_producer_receipt(
    tmp_path,
    capsys,
):
    task_id = _start(tmp_path, capsys)
    start = telemetry_runtime.validate_lifecycle_events(tmp_path)[0]
    assert start["task_id"] == task_id
    registry = producers.load_producer_registry()
    registry["producers"]["build-loop-harvest"] = {
        "status": "active",
        "event_id": start["event_id"],
    }

    with pytest.raises(ValueError, match="validated receipt"):
        producers.validate_producer_registry(registry, tmp_path)
