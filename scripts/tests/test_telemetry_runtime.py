import copy
import json
import os
from pathlib import Path
import sys
import uuid

import pytest


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import telemetry as telemetry_runtime


REVISION = {"value": "test/1", "unavailable_reason": None}


def event(event_type: str = "task_started", payload: dict | None = None) -> dict:
    payloads = {
        "task_started": {"workflow": "build-loop"},
        "task_finished": {"outcome": "completed", "scorecard_ref": None},
        "handoff_created": {
            "handoff_ref": "handoffs/task.md",
            "reason": "deliberate_pause",
        },
        "task_resumed": {
            "handoff_ref": "handoffs/task.md",
            "resumed_from_handoff": True,
            "resumed_from_event_id": str(uuid.uuid4()),
        },
        "delegation_started": {
            "delegation_id": str(uuid.uuid4()),
            "child_task_id": str(uuid.uuid4()),
            "delegated_role": "builder",
            "brief_ref": "handoffs/brief.md",
        },
        "gate_result": {
            "gate_id": "pytest",
            "outcome": "pass",
            "first_pass": True,
            "verdict_source": "automation",
            "evidence_ref": "run:pytest:1",
        },
        "review_result": {
            "reviewer_id": "code-reviewer",
            "reviewer_class": "software-dev",
            "round": 1,
            "verdict": "approve",
            "verdict_source": "agent",
            "finding_count": 0,
            "evidence_ref": "review:1",
        },
        "defect_recorded": {
            "defect_id": "defect-1",
            "introduced_task": None,
            "approving_reviewers": ["code-reviewer"],
            "gate_that_should_have_caught_it": "pytest",
            "evidence_ref": "defect:1",
        },
        "rework_recorded": {
            "cause_event_id": str(uuid.uuid4()),
            "round": 1,
            "reason": "review_finding",
            "evidence_ref": None,
        },
        "lesson_candidate_recorded": {
            "kit_facing": True,
            "root_cause_ref": "root:1",
            "candidate_ref": "candidate:1",
        },
        "fact_check_recorded": {
            "gate_id": "fact-check",
            "verdict": "sourced",
            "verdict_source": "human",
            "finding_count": 0,
            "failure_classes": [],
            "evidence_ref": "fact-check:1",
        },
        "scorecard_imported": {
            "source_path": "benchmarks/scorecard.jsonl",
            "source_record_ordinal": 1,
            "source_record_hash": "a" * 64,
            "source_record_ref": "scorecard:1",
        },
        "benchmark_exported": {
            "export_batch_id": str(uuid.uuid4()),
            "target_path": "benchmarks/telemetry-v3.jsonl",
            "prior_hash": None,
            "exported_event_ids": [str(uuid.uuid4())],
        },
    }
    return {
        "schema_version": 3,
        "event_id": str(uuid.uuid4()),
        "task_id": str(uuid.uuid4()),
        "event_type": event_type,
        "occurred_at": "2026-07-22T05:54:42Z",
        "producer": {"revision": "test/1"},
        "revisions": {
            "domain": copy.deepcopy(REVISION),
            "engine": copy.deepcopy(REVISION),
            "adapter": copy.deepcopy(REVISION),
            "canonical_contract": copy.deepcopy(REVISION),
            "profile": copy.deepcopy(REVISION),
        },
        "lineage": {
            "parent_task_id": None,
            "delegation_id": None,
            "correction_of": None,
            "correction_evidence_ref": None,
        },
        "source_class": "runtime",
        "privacy_class": "project",
        "coverage": {
            "status": "partial",
            "missing_event_types": ["task_finished"],
            "missing_requirement_refs": [],
            "reason": "in_progress",
        },
        "tokens": {
            "total": None,
            "attribution_status": "unknown",
            "reason": "unsupported_provider",
        },
        "elapsed": {
            "milliseconds": None,
            "clock_source": "unknown",
            "reason": "not_reported",
        },
        "payload": copy.deepcopy(payloads[event_type] if payload is None else payload),
    }


def channel(resolver=None):
    return telemetry_runtime.ProducerChannel("test-producer", resolver)


def stored(value: dict) -> dict:
    result = copy.deepcopy(value)
    result["producer"]["id"] = "test-producer"
    return result


def test_schema_artifact_is_closed_and_lists_every_event_type():
    schema = json.loads((ROOT / "telemetry/schema-v3.json").read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert set(schema["$defs"]["payloads"]) == set(telemetry_runtime.EVENT_TYPES)
    assert (ROOT / "telemetry/.gitignore").read_text(encoding="utf-8") == "events.jsonl\n"


@pytest.mark.parametrize("event_type", telemetry_runtime.EVENT_TYPES)
def test_closed_schema_accepts_every_payload_shape(event_type):
    telemetry_runtime.validate_event(stored(event(event_type)))


def test_closed_schema_rejects_unknown_fields_and_invalid_pairs():
    value = stored(event())
    value["unknown"] = True
    with pytest.raises(telemetry_runtime.TelemetryError, match="TELEMETRY_EVENT_INVALID"):
        telemetry_runtime.validate_event(value)

    value = stored(event())
    value["source_class"] = "prompt"
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.validate_event(value)
    assert caught.value.code == "TELEMETRY_PRIVACY_VIOLATION"

    value = stored(event())
    value["coverage"] = {
        "status": "full",
        "missing_event_types": ["task_finished"],
        "missing_requirement_refs": [],
        "reason": None,
    }
    with pytest.raises(telemetry_runtime.TelemetryError, match="TELEMETRY_EVENT_INVALID"):
        telemetry_runtime.validate_event(value)


def test_privacy_rejection_does_not_echo_forbidden_value():
    value = stored(event("gate_result"))
    secret = "https://host/path?access_token=secret-value"
    value["payload"]["evidence_ref"] = secret
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.validate_event(value)
    assert caught.value.code == "TELEMETRY_PRIVACY_VIOLATION"
    assert secret not in str(caught.value)


def test_append_is_single_line_duplicate_safe_and_preserves_prior_bytes(tmp_path):
    first = event()
    first_stored = telemetry_runtime.append_local_event(tmp_path, first, channel())
    path = tmp_path / "telemetry/events.jsonl"
    prior = path.read_bytes()
    assert prior.endswith(b"\n") and len(prior.splitlines()) == 1

    second = event("gate_result")
    telemetry_runtime.append_local_event(tmp_path, second, channel())
    assert path.read_bytes().startswith(prior)

    before_duplicate = path.read_bytes()
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, first, channel())
    assert caught.value.code == "TELEMETRY_DUPLICATE_EVENT_ID"
    assert path.read_bytes() == before_duplicate
    assert first_stored["producer"]["id"] == "test-producer"
    assert telemetry_runtime.validate_local_events(tmp_path) == [first_stored, stored(second)]


def test_validation_of_missing_stream_is_read_only(tmp_path):
    assert telemetry_runtime.validate_local_events(tmp_path) == []
    assert not (tmp_path / "telemetry").exists()


def test_storage_rejects_caller_authored_producer_id_and_names_fixed_path(tmp_path):
    value = event()
    value["producer"]["id"] = "caller-controlled"
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, value, channel())
    assert caught.value.path == "telemetry\\events.jsonl" or caught.value.path == "telemetry/events.jsonl"
    assert not (tmp_path / "telemetry/events.jsonl").exists()


def test_interrupted_final_record_is_recovered_but_complete_corruption_is_not(tmp_path):
    telemetry_runtime.append_local_event(tmp_path, event(), channel())
    path = tmp_path / "telemetry/events.jsonl"
    prior = path.read_bytes()
    with path.open("ab") as stream:
        stream.write(b'{"schema_version":3')

    telemetry_runtime.append_local_event(tmp_path, event("gate_result"), channel())
    recovered = path.read_bytes()
    assert recovered.startswith(prior)
    assert b'{"schema_version":3{' not in recovered
    assert len(recovered.splitlines()) == 2

    path.write_bytes(b"not-json\n" + recovered)
    corrupt = path.read_bytes()
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, event("review_result"), channel())
    assert caught.value.code == "TELEMETRY_HISTORY_CORRUPT"
    assert path.read_bytes() == corrupt


def test_authorized_correction_preserves_target_and_binds_receipt(tmp_path):
    original = event("gate_result")
    telemetry_runtime.append_local_event(tmp_path, original, channel())
    path = tmp_path / "telemetry/events.jsonl"
    prior = path.read_bytes()
    bindings = []

    correction = copy.deepcopy(original)
    correction["event_id"] = str(uuid.uuid4())
    correction["producer"] = {"revision": "test/2"}
    correction["lineage"]["correction_of"] = original["event_id"]
    correction["lineage"]["correction_evidence_ref"] = "correction:receipt:1"
    correction["tokens"] = {
        "total": 123,
        "attribution_status": "exact",
        "reason": None,
    }
    correction["privacy_class"] = "local_private"

    def authorize(evidence_ref, binding):
        bindings.append((evidence_ref, binding))
        return True

    telemetry_runtime.append_local_event(tmp_path, correction, channel(authorize))
    assert path.read_bytes().startswith(prior)
    assert len(path.read_bytes().splitlines()) == 2
    assert bindings[0][0] == "correction:receipt:1"
    assert bindings[0][1]["root_event_id"] == original["event_id"]
    assert bindings[0][1]["target_event_id"] == original["event_id"]
    assert bindings[0][1]["correcting_event_id"] == correction["event_id"]
    assert len(bindings[0][1]["record_sha256"]) == 64


def test_correction_rejects_changed_payload_and_missing_authority_without_mutation(tmp_path):
    original = event("gate_result")
    telemetry_runtime.append_local_event(tmp_path, original, channel())
    path = tmp_path / "telemetry/events.jsonl"
    prior = path.read_bytes()

    correction = copy.deepcopy(original)
    correction["event_id"] = str(uuid.uuid4())
    correction["producer"] = {"revision": "test/2"}
    correction["lineage"]["correction_of"] = original["event_id"]
    correction["lineage"]["correction_evidence_ref"] = "correction:receipt:1"
    correction["payload"]["outcome"] = "fail"
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, correction, channel(lambda *_: True))
    assert caught.value.code == "TELEMETRY_CORRECTION_INVALID"
    assert path.read_bytes() == prior

    correction["payload"]["outcome"] = "pass"
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, correction, channel())
    assert caught.value.code == "TELEMETRY_CORRECTION_UNAUTHORIZED"
    assert path.read_bytes() == prior


def test_invalid_utf8_in_complete_history_fails_without_mutation(tmp_path):
    target = tmp_path / "telemetry/events.jsonl"
    target.parent.mkdir()
    target.write_bytes(b"\xff\n")
    before = target.read_bytes()
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, event(), channel())
    assert caught.value.code == "TELEMETRY_HISTORY_CORRUPT"
    assert target.read_bytes() == before


def test_reader_stops_after_65537_tail_bytes_without_mutation(tmp_path):
    target = tmp_path / "telemetry/events.jsonl"
    target.parent.mkdir()
    target.write_bytes(b"x" * 65537)
    before = target.read_bytes()
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, event(), channel())
    assert caught.value.code == "TELEMETRY_HISTORY_CORRUPT"
    assert target.read_bytes() == before


def test_hard_link_target_is_rejected_without_mutation(tmp_path):
    target = tmp_path / "telemetry/events.jsonl"
    target.parent.mkdir()
    target.write_bytes(b"")
    other = tmp_path / "linked.jsonl"
    os.link(target, other)
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, event(), channel())
    assert caught.value.code == "TELEMETRY_HISTORY_CORRUPT"
    assert target.read_bytes() == b""


def test_symlink_parent_is_rejected_when_supported(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (tmp_path / "telemetry").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    with pytest.raises(telemetry_runtime.TelemetryError) as caught:
        telemetry_runtime.append_local_event(tmp_path, event(), channel())
    assert caught.value.code == "TELEMETRY_HISTORY_CORRUPT"
    assert not (outside / "events.jsonl").exists()


def test_record_size_limit_is_enforced_before_write(tmp_path):
    value = event("gate_result")
    value["payload"]["evidence_ref"] = "a" * 70000
    with pytest.raises(telemetry_runtime.TelemetryError):
        telemetry_runtime.append_local_event(tmp_path, value, channel())
    assert not (tmp_path / "telemetry/events.jsonl").exists()
