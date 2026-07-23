"""Producer-side Telemetry v3 integrations."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping
import uuid

from scripts import telemetry as runtime


PRODUCER_IDS = (
    "build-loop-harvest",
    "diagnosing-bugs",
    "knowledge-work-fact-check",
    "task-handoff",
    "reports",
)
ROOT_CAUSE_LOCI = (
    "skill",
    "template",
    "gate",
    "agent-charter",
    "ci",
    "git",
    "host",
)
_KIT_FACING_LOCI = {"skill", "template", "gate"}
_EVIDENCE_REFS = {
    "root_cause_ref": re.compile(
        r"evidence:(?:root-cause:[0-9a-f]{64}|scorecard:[0-9a-f]{64}:root-cause)\Z"
    ),
    "candidate_ref": re.compile(
        r"evidence:(?:lesson-candidate:[0-9a-f]{64}|scorecard:[0-9a-f]{64}:lesson-candidate)\Z"
    ),
}
_PRODUCER_REVISION = "build-loop-harvest/1"
_RECEIPT_EVENTS = {
    "build-loop-harvest": ("lesson_candidate_recorded", _PRODUCER_REVISION),
}
_UNKNOWN_REVISION = {"value": None, "unavailable_reason": "not_emitted"}
_POLICY = runtime.ProducerPolicy(
    source_classes=("runtime",),
    verdict_sources=(),
    metadata_rules={
        "producer.revision": (_PRODUCER_REVISION,),
        "payload.root_cause_ref": ("evidence:*",),
        "payload.candidate_ref": ("evidence:*",),
    },
)


def _duplicate_object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("producer registry contains a duplicate key")
        result[key] = value
    return result


def validate_producer_registry(
    value: Any,
    repository_root: Path | str | None = None,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"schema_version", "producers"}:
        raise ValueError("producer registry must use the closed versioned shape")
    if value["schema_version"] != 1 or isinstance(value["schema_version"], bool):
        raise ValueError("producer registry schema_version must be 1")
    entries = value["producers"]
    if not isinstance(entries, dict) or set(entries) != set(PRODUCER_IDS):
        raise ValueError("producer registry must contain exactly the five required producers")
    validated_events = None
    for producer_id, entry in entries.items():
        if not isinstance(entry, dict) or set(entry) != {"status", "event_id"}:
            raise ValueError(f"producer {producer_id} must use the closed status shape")
        if not isinstance(entry["status"], str) or entry["status"] not in {"planned", "active"}:
            raise ValueError(f"producer {producer_id} status must be planned or active")
        event_id = entry["event_id"]
        if entry["status"] == "planned" and event_id is not None:
            raise ValueError(f"planned producer {producer_id} event_id must be null")
        if entry["status"] == "active":
            try:
                parsed = uuid.UUID(event_id)
            except (AttributeError, TypeError, ValueError):
                raise ValueError(f"active producer {producer_id} requires a UUIDv4 event_id") from None
            if parsed.version != 4 or str(parsed) != event_id:
                raise ValueError(f"active producer {producer_id} requires a UUIDv4 event_id")
            if repository_root is None or producer_id not in _RECEIPT_EVENTS:
                raise ValueError(f"active producer {producer_id} requires a validated receipt event_id")
            if validated_events is None:
                validated_events = runtime.validate_lifecycle_events(repository_root)
            event_type, revision = _RECEIPT_EVENTS[producer_id]
            if not any(
                event["event_id"] == event_id
                and event["event_type"] == event_type
                and event["producer"] == {"id": producer_id, "revision": revision}
                for event in validated_events
            ):
                raise ValueError(f"active producer {producer_id} event_id is not its validated receipt")
    return value


def load_producer_registry(
    path: Path | str | None = None,
    repository_root: Path | str | None = None,
) -> dict[str, Any]:
    target = Path(path) if path is not None else Path(__file__).with_name("producers.json")
    try:
        value = json.loads(
            target.read_text(encoding="utf-8"),
            object_pairs_hook=_duplicate_object_pairs,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("producer registry is not valid UTF-8 JSON") from error
    return validate_producer_registry(value, repository_root)


def _require_evidence_ref(value: Any, name: str) -> str:
    if not isinstance(value, str) or _EVIDENCE_REFS[name].fullmatch(value) is None:
        raise ValueError(f"{name} must be a producer-owned evidence:* stable reference")
    return value


def _require_task_id(value: Any) -> str:
    try:
        parsed = uuid.UUID(value)
    except (AttributeError, TypeError, ValueError):
        raise ValueError("task_id must be a canonical UUIDv4") from None
    if parsed.version != 4 or str(parsed) != value:
        raise ValueError("task_id must be a canonical UUIDv4")
    return value


def _coverage(*missing: str, reason: str) -> dict[str, Any]:
    return {
        "status": "partial",
        "missing_event_types": sorted(missing),
        "missing_requirement_refs": [],
        "reason": reason,
    }


def _event(
    task_id: str,
    event_type: str,
    payload: Mapping[str, Any],
    coverage,
    *,
    parent_task_id=None,
    delegation_id=None,
):
    return {
        "schema_version": 3,
        "event_id": str(uuid.uuid4()),
        "task_id": task_id,
        "event_type": event_type,
        "occurred_at": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
        "producer": {"revision": _PRODUCER_REVISION},
        "revisions": {
            name: dict(_UNKNOWN_REVISION)
            for name in runtime.REVISION_FIELDS
        },
        "lineage": {
            "parent_task_id": parent_task_id,
            "delegation_id": delegation_id,
            "correction_of": None,
            "correction_evidence_ref": None,
        },
        "source_class": "runtime",
        "privacy_class": "project",
        "coverage": coverage,
        "tokens": {
            "total": None,
            "attribution_status": "unknown",
            "reason": "not_reported",
        },
        "elapsed": {
            "milliseconds": None,
            "clock_source": "unknown",
            "reason": "not_reported",
        },
        "payload": dict(payload),
    }


def emit_build_loop_harvest(
    repository_root: Path | str,
    *,
    task_id: str,
    root_cause_locus: str,
    root_cause_ref: str,
    candidate_ref: str,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Append HARVEST evidence to one existing LOAD-minted task."""

    environment = os.environ if environ is None else environ
    if environment.get("DAT_KIT_TELEMETRY") == "off":
        return {"status": "disabled", "event_count": 0}
    if root_cause_locus not in ROOT_CAUSE_LOCI:
        raise ValueError("root_cause_locus must use the closed locus enum")
    task_id = _require_task_id(task_id)
    root_cause_ref = _require_evidence_ref(root_cause_ref, "root_cause_ref")
    candidate_ref = _require_evidence_ref(candidate_ref, "candidate_ref")

    try:
        existing = runtime.validate_lifecycle_events(repository_root)
        task_events = [
            event
            for event in existing
            if event["task_id"] == task_id
            and event["lineage"]["correction_of"] is None
        ]
        starts = [event for event in task_events if event["event_type"] == "task_started"]
        if (
            len(starts) != 1
            or starts[0]["payload"]["workflow"] != "build-loop"
            or any(event["event_type"] == "task_finished" for event in task_events)
            or task_events[-1]["coverage"]["missing_requirement_refs"]
        ):
            raise ValueError("task_id must name one unfinished build-loop lifecycle")
        observed = {event["event_type"] for event in task_events}
        lineage = starts[0]["lineage"]
        in_progress = _coverage(
            *({"gate_result", "review_result", "task_finished"} - observed),
            reason="in_progress",
        )
        terminal_missing = {"gate_result", "review_result"} - observed
        terminal = (
            _coverage(*terminal_missing, reason="producer_failure")
            if terminal_missing
            else {
                "status": "full",
                "missing_event_types": [],
                "missing_requirement_refs": [],
                "reason": None,
            }
        )
        events = (
            _event(
            task_id,
            "lesson_candidate_recorded",
            {
                "kit_facing": root_cause_locus in _KIT_FACING_LOCI,
                "root_cause_ref": root_cause_ref,
                "candidate_ref": candidate_ref,
            },
            in_progress,
                parent_task_id=lineage["parent_task_id"],
                delegation_id=lineage["delegation_id"],
            ),
            _event(
                task_id,
                "task_finished",
                {"outcome": "completed", "scorecard_ref": "benchmarks/scorecard.jsonl"},
                terminal,
                parent_task_id=lineage["parent_task_id"],
                delegation_id=lineage["delegation_id"],
            ),
        )
        writer = runtime.TelemetryStore(
            repository_root,
            {"build-loop-harvest": _POLICY},
        ).bind("build-loop-harvest")
        for event in events:
            writer.append(event)
        runtime.validate_lifecycle_events(repository_root)
    except Exception as error:
        return {
            "status": "degraded",
            "reason": "producer_failure",
            "code": getattr(error, "code", "TELEMETRY_OPERATIONAL_FAILURE"),
        }
    return {
        "status": "ok",
        "task_id": task_id,
        "event_ids": [event["event_id"] for event in events],
        "event_count": len(events),
        "coverage": events[-1]["coverage"],
    }
