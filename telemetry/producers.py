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
_STABLE_REF = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/#@-]{0,511}\Z")
_PRODUCER_REVISION = "build-loop-harvest/1"
_UNKNOWN_REVISION = {"value": None, "unavailable_reason": "not_emitted"}
_POLICY = runtime.ProducerPolicy(
    source_classes=("runtime",),
    verdict_sources=(),
    metadata_rules={
        "producer.revision": (_PRODUCER_REVISION,),
        "payload.workflow": ("build-loop",),
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


def validate_producer_registry(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"schema_version", "producers"}:
        raise ValueError("producer registry must use the closed versioned shape")
    if value["schema_version"] != 1 or isinstance(value["schema_version"], bool):
        raise ValueError("producer registry schema_version must be 1")
    entries = value["producers"]
    if not isinstance(entries, dict) or set(entries) != set(PRODUCER_IDS):
        raise ValueError("producer registry must contain exactly the five required producers")
    for producer_id, entry in entries.items():
        if not isinstance(entry, dict) or set(entry) != {"status", "event_id"}:
            raise ValueError(f"producer {producer_id} must use the closed status shape")
        if entry["status"] not in {"planned", "active"}:
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
    return value


def load_producer_registry(path: Path | str | None = None) -> dict[str, Any]:
    target = Path(path) if path is not None else Path(__file__).with_name("producers.json")
    try:
        value = json.loads(
            target.read_text(encoding="utf-8"),
            object_pairs_hook=_duplicate_object_pairs,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("producer registry is not valid UTF-8 JSON") from error
    return validate_producer_registry(value)


def _require_evidence_ref(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or _STABLE_REF.fullmatch(value) is None
        or not value.startswith("evidence:")
    ):
        raise ValueError(f"{name} must be a producer-owned evidence:* stable reference")
    return value


def _coverage(*missing: str, reason: str) -> dict[str, Any]:
    return {
        "status": "partial",
        "missing_event_types": sorted(missing),
        "missing_requirement_refs": [],
        "reason": reason,
    }


def _event(task_id: str, event_type: str, payload: Mapping[str, Any], coverage):
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
            "parent_task_id": None,
            "delegation_id": None,
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
    root_cause_locus: str,
    root_cause_ref: str,
    candidate_ref: str,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Emit one HARVEST lifecycle without claiming gate/review coverage."""

    environment = os.environ if environ is None else environ
    if environment.get("DAT_KIT_TELEMETRY") == "off":
        return {"status": "disabled", "event_count": 0}
    if root_cause_locus not in ROOT_CAUSE_LOCI:
        raise ValueError("root_cause_locus must use the closed locus enum")
    root_cause_ref = _require_evidence_ref(root_cause_ref, "root_cause_ref")
    candidate_ref = _require_evidence_ref(candidate_ref, "candidate_ref")

    task_id = str(uuid.uuid4())
    in_progress = _coverage(
        "gate_result",
        "review_result",
        "task_finished",
        reason="in_progress",
    )
    events = (
        _event(task_id, "task_started", {"workflow": "build-loop"}, in_progress),
        _event(
            task_id,
            "lesson_candidate_recorded",
            {
                "kit_facing": root_cause_locus in _KIT_FACING_LOCI,
                "root_cause_ref": root_cause_ref,
                "candidate_ref": candidate_ref,
            },
            in_progress,
        ),
        _event(
            task_id,
            "task_finished",
            {"outcome": "completed", "scorecard_ref": "benchmarks/scorecard.jsonl"},
            _coverage("gate_result", "review_result", reason="producer_failure"),
        ),
    )

    try:
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
