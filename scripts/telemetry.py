#!/usr/bin/env python3
"""Telemetry v3 schema validation and local single-writer storage primitives."""

from __future__ import annotations

import copy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import threading
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence
import uuid


EVENT_TYPES = (
    "task_started",
    "task_finished",
    "handoff_created",
    "task_resumed",
    "delegation_started",
    "gate_result",
    "review_result",
    "defect_recorded",
    "rework_recorded",
    "lesson_candidate_recorded",
    "fact_check_recorded",
    "scorecard_imported",
    "benchmark_exported",
)
EVENT_PATH = Path("telemetry/events.jsonl")
MAX_RECORD_BYTES = 65_536

STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
STABLE_REF = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/#@-]{0,511}\Z")
LOWER_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
UTC_TIMESTAMP = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?Z\Z"
)
WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "event_id",
    "task_id",
    "event_type",
    "occurred_at",
    "producer",
    "revisions",
    "lineage",
    "source_class",
    "privacy_class",
    "coverage",
    "tokens",
    "elapsed",
    "payload",
}
REVISION_FIELDS = {"domain", "engine", "adapter", "canonical_contract", "profile"}
LINEAGE_FIELDS = {
    "parent_task_id",
    "delegation_id",
    "correction_of",
    "correction_evidence_ref",
}

_WRITE_LOCK = threading.Lock()


class TelemetryError(ValueError):
    """A fail-closed Telemetry v3 diagnostic without rejected-value leakage."""

    def __init__(
        self,
        code: str,
        detail: str,
        *,
        path: str | None = None,
        event_id: str | None = None,
        line: int | None = None,
    ) -> None:
        self.code = code
        self.detail = detail
        self.path = path
        self.event_id = event_id
        self.line = line
        locations = []
        if path is not None:
            locations.append(f"path={path}")
        if event_id is not None:
            locations.append(f"event_id={event_id}")
        if line is not None:
            locations.append(f"line={line}")
        suffix = f" ({', '.join(locations)})" if locations else ""
        super().__init__(f"{code}: {detail}{suffix}")


CorrectionResolver = Callable[[str, Mapping[str, str]], bool]


class ProducerPolicy:
    """Immutable channel policy for provenance and producer-owned metadata."""

    __slots__ = (
        "correction_resolver",
        "source_classes",
        "verdict_sources",
        "metadata_rules",
        "_frozen",
    )

    def __init__(
        self,
        *,
        correction_resolver: CorrectionResolver | None = None,
        source_classes: Sequence[str],
        verdict_sources: Sequence[str],
        metadata_rules: Mapping[str, Sequence[str]],
    ) -> None:
        if correction_resolver is not None and not callable(correction_resolver):
            raise TypeError("correction_resolver must be callable or null")
        sources = frozenset(source_classes)
        verdicts = frozenset(verdict_sources)
        if not sources or not sources <= {"runtime", "repository", "human", "legacy_import", "derived"}:
            raise ValueError("source_classes must be a non-empty closed subset")
        if not verdicts <= {"human", "agent", "automation"}:
            raise ValueError("verdict_sources must use the closed verdict-source enum")
        copied_rules: dict[str, tuple[str, ...]] = {}
        for field, rules in metadata_rules.items():
            if not isinstance(field, str) or not field or not isinstance(rules, Sequence) or isinstance(rules, (str, bytes)):
                raise TypeError("metadata rules must map field names to sequences")
            normalized = tuple(rules)
            if not normalized or any(not isinstance(rule, str) or not rule or rule == "*" for rule in normalized):
                raise ValueError("metadata rules must use exact values or bounded prefixes")
            copied_rules[field] = normalized
        object.__setattr__(self, "correction_resolver", correction_resolver)
        object.__setattr__(self, "source_classes", sources)
        object.__setattr__(self, "verdict_sources", verdicts)
        object.__setattr__(self, "metadata_rules", MappingProxyType(copied_rules))
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError("ProducerPolicy is immutable")
        object.__setattr__(self, name, value)

    def authorizes(self, field: str, value: str) -> bool:
        for rule in self.metadata_rules.get(field, ()):
            if rule.endswith("*") and value.startswith(rule[:-1]):
                return True
            if value == rule:
                return True
        return False


class _ProducerChannel:
    """Internal producer identity resolved from an immutable store registry."""

    __slots__ = ("producer_id", "policy")

    def __init__(
        self,
        producer_id: str,
        policy: ProducerPolicy,
    ) -> None:
        _require_stable_id(producer_id, "producer channel id")
        object.__setattr__(self, "producer_id", producer_id)
        object.__setattr__(self, "policy", policy)


class TelemetryStore:
    """Trusted composition root for one repository and immutable producer registry."""

    __slots__ = ("_repository_root", "_registry", "_writer_seal", "_frozen")

    def __init__(
        self,
        repository_root: Path | str,
        producer_registry: Mapping[str, ProducerPolicy],
    ) -> None:
        if not isinstance(producer_registry, Mapping):
            raise TypeError("producer_registry must be a mapping")
        copied: dict[str, ProducerPolicy] = {}
        for producer_id, policy in producer_registry.items():
            _require_stable_id(producer_id, "registered producer id")
            if type(policy) is not ProducerPolicy:
                raise TypeError("registered producer entries must be ProducerPolicy instances")
            copied[producer_id] = policy
        object.__setattr__(self, "_repository_root", _canonical_root(repository_root))
        object.__setattr__(self, "_registry", MappingProxyType(copied))
        object.__setattr__(self, "_writer_seal", object())
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError("TelemetryStore is immutable")
        object.__setattr__(self, name, value)

    def bind(self, producer_id: str) -> "ProducerWriter":
        if not isinstance(producer_id, str) or producer_id not in self._registry:
            _error("producer is not registered", code="TELEMETRY_CORRECTION_UNAUTHORIZED", path=str(EVENT_PATH))
        return ProducerWriter(self, producer_id, self._writer_seal)


class ProducerWriter:
    """Bound append surface; event callers cannot supply identity or authority."""

    __slots__ = ("_store", "_producer_id", "_frozen")

    def __init__(self, store: TelemetryStore, producer_id: str, seal: object | None = None) -> None:
        if type(store) is not TelemetryStore or seal is not store._writer_seal:
            raise TypeError("ProducerWriter instances are created only by TelemetryStore.bind")
        object.__setattr__(self, "_store", store)
        object.__setattr__(self, "_producer_id", producer_id)
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError("ProducerWriter is immutable")
        object.__setattr__(self, name, value)

    def append(self, event: Mapping[str, Any]) -> dict[str, Any]:
        channel = _ProducerChannel(
            self._producer_id,
            self._store._registry[self._producer_id],
        )
        return _append_local_event(self._store._repository_root, event, channel)


def _error(
    detail: str,
    *,
    code: str = "TELEMETRY_EVENT_INVALID",
    path: str | None = None,
    event_id: str | None = None,
    line: int | None = None,
) -> None:
    raise TelemetryError(code, detail, path=path, event_id=event_id, line=line)


def _closed_object(value: Any, fields: set[str], name: str) -> Mapping[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        _error(f"{name} must contain exactly its closed fields")
    return value


def _is_integer(value: Any, *, positive: bool = False) -> bool:
    if isinstance(value, bool) or not isinstance(value, int):
        return False
    return value > 0 if positive else value >= 0


def _require_stable_id(value: Any, name: str) -> None:
    if not isinstance(value, str) or STABLE_ID.fullmatch(value) is None:
        _error(f"{name} must be a stable ID")


def _require_stable_ref(value: Any, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or STABLE_REF.fullmatch(value) is None:
        _error(
            f"{name} is not allowlisted metadata",
            code="TELEMETRY_PRIVACY_VIOLATION",
        )
    windows = PureWindowsPath(value)
    if PurePosixPath(value).is_absolute() or windows.is_absolute() or windows.drive:
        _error(
            f"{name} must not contain an absolute path",
            code="TELEMETRY_PRIVACY_VIOLATION",
        )


def _require_uuid4(value: Any, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or value != value.lower():
        _error(f"{name} must be a canonical lowercase UUIDv4")
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        _error(f"{name} must be a canonical lowercase UUIDv4")
    if parsed.version != 4 or str(parsed) != value or parsed.int == 0:
        _error(f"{name} must be a canonical lowercase UUIDv4")


def _require_timestamp(value: Any) -> None:
    if not isinstance(value, str) or UTC_TIMESTAMP.fullmatch(value) is None:
        _error("occurred_at must be an RFC 3339 UTC timestamp")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        _error("occurred_at must be an RFC 3339 UTC timestamp")


def _require_sha256(value: Any, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or LOWER_SHA256.fullmatch(value) is None:
        _error(f"{name} must be a lowercase SHA-256")


def _require_path(value: Any, name: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not 1 <= len(value) <= 512:
        _error(f"{name} must be an allowlisted repository-relative path", code="TELEMETRY_PRIVACY_VIOLATION")
    if "\\" in value or any(ord(char) < 32 or ord(char) == 127 for char in value):
        _error(f"{name} must be an allowlisted repository-relative path", code="TELEMETRY_PRIVACY_VIOLATION")
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    parts = value.split("/")
    invalid_part = any(
        not part
        or part in {".", ".."}
        or part.endswith((" ", "."))
        or part.split(".", 1)[0].lower() in WINDOWS_RESERVED
        for part in parts
    )
    if posix.is_absolute() or windows.is_absolute() or windows.drive or invalid_part:
        _error(f"{name} must be an allowlisted repository-relative path", code="TELEMETRY_PRIVACY_VIOLATION")


def _require_enum(value: Any, choices: set[str], name: str) -> None:
    if not isinstance(value, str) or value not in choices:
        _error(f"{name} must use its closed enum")


def _require_sorted_unique(
    value: Any,
    name: str,
    validator: Callable[[Any, str], None],
    *,
    maximum: int,
) -> None:
    if not isinstance(value, list) or len(value) > maximum:
        _error(f"{name} must be a bounded sorted array")
    for item in value:
        validator(item, name)
    if value != sorted(value):
        _error(f"{name} must be a bounded sorted array")
    if len(value) != len(set(value)):
        _error(f"{name} must not contain duplicates")


def _validate_revision(value: Any, name: str) -> None:
    revision = _closed_object(value, {"value", "unavailable_reason"}, name)
    present = revision["value"] is not None
    missing = revision["unavailable_reason"] is not None
    if present == missing:
        _error(f"{name} must contain exactly one revision alternative")
    if present:
        _require_stable_ref(revision["value"], f"{name}.value")
    else:
        _require_enum(
            revision["unavailable_reason"],
            {"not_applicable", "not_emitted", "unsupported_host", "legacy_source", "ambiguous"},
            f"{name}.unavailable_reason",
        )


def _validate_coverage(value: Any) -> None:
    coverage = _closed_object(
        value,
        {"status", "missing_event_types", "missing_requirement_refs", "reason"},
        "coverage",
    )
    _require_enum(coverage["status"], {"full", "partial"}, "coverage.status")
    _require_sorted_unique(
        coverage["missing_event_types"],
        "coverage.missing_event_types",
        lambda item, name: _require_enum(item, set(EVENT_TYPES), name),
        maximum=13,
    )
    _require_sorted_unique(
        coverage["missing_requirement_refs"],
        "coverage.missing_requirement_refs",
        _require_stable_id,
        maximum=128,
    )
    if coverage["status"] == "full":
        if coverage["missing_event_types"] or coverage["missing_requirement_refs"] or coverage["reason"] is not None:
            _error("full coverage must have empty missing arrays and null reason")
    else:
        if not (coverage["missing_event_types"] or coverage["missing_requirement_refs"]):
            _error("partial coverage must name missing requirements")
        _require_enum(
            coverage["reason"],
            {
                "completion_only",
                "unsupported_host_start",
                "telemetry_disabled",
                "legacy_import",
                "producer_failure",
                "unresumed_handoff",
                "in_progress",
            },
            "coverage.reason",
        )


def _validate_tokens(value: Any) -> None:
    tokens = _closed_object(value, {"total", "attribution_status", "reason"}, "tokens")
    _require_enum(tokens["attribution_status"], {"exact", "unknown"}, "tokens.attribution_status")
    if tokens["attribution_status"] == "exact":
        if not _is_integer(tokens["total"]) or tokens["reason"] is not None:
            _error("exact tokens require a non-negative total and null reason")
    else:
        if tokens["total"] is not None:
            _error("unknown tokens require a null total")
        _require_enum(
            tokens["reason"],
            {
                "unsupported_provider",
                "missing_timestamp",
                "no_matching_session",
                "multiple_matching_sessions",
                "ambiguous_multi_task_session",
                "not_reported",
                "legacy_source",
                "telemetry_disabled",
            },
            "tokens.reason",
        )


def _validate_elapsed(value: Any) -> None:
    elapsed = _closed_object(value, {"milliseconds", "clock_source", "reason"}, "elapsed")
    if elapsed["milliseconds"] is None:
        if elapsed["clock_source"] != "unknown":
            _error("unknown elapsed time requires clock_source=unknown")
        _require_enum(
            elapsed["reason"],
            {"not_reported", "unsupported_host", "ambiguous", "legacy_source", "telemetry_disabled"},
            "elapsed.reason",
        )
    elif not _is_integer(elapsed["milliseconds"]) or elapsed["clock_source"] not in {"monotonic", "wall"} or elapsed["reason"] is not None:
        _error("measured elapsed time requires non-negative milliseconds, a measured clock, and null reason")


def _payload(value: Any, fields: set[str], event_type: str) -> Mapping[str, Any]:
    return _closed_object(value, fields, f"{event_type}.payload")


def _validate_payload(event_type: str, value: Any) -> None:
    if event_type == "task_started":
        item = _payload(value, {"workflow"}, event_type)
        _require_stable_id(item["workflow"], "workflow")
    elif event_type == "task_finished":
        item = _payload(value, {"outcome", "scorecard_ref"}, event_type)
        _require_enum(item["outcome"], {"completed", "aborted", "unknown"}, "outcome")
        _require_path(item["scorecard_ref"], "scorecard_ref", nullable=True)
    elif event_type == "handoff_created":
        item = _payload(value, {"handoff_ref", "reason"}, event_type)
        _require_path(item["handoff_ref"], "handoff_ref")
        _require_enum(item["reason"], {"context_ceiling", "deliberate_pause", "delegation_brief"}, "reason")
    elif event_type == "task_resumed":
        item = _payload(value, {"handoff_ref", "resumed_from_handoff", "resumed_from_event_id"}, event_type)
        _require_path(item["handoff_ref"], "handoff_ref")
        if item["resumed_from_handoff"] is not True:
            _error("resumed_from_handoff must be literal true")
        _require_uuid4(item["resumed_from_event_id"], "resumed_from_event_id")
    elif event_type == "delegation_started":
        item = _payload(value, {"delegation_id", "child_task_id", "delegated_role", "brief_ref"}, event_type)
        _require_uuid4(item["delegation_id"], "delegation_id")
        _require_uuid4(item["child_task_id"], "child_task_id")
        _require_stable_id(item["delegated_role"], "delegated_role")
        _require_path(item["brief_ref"], "brief_ref")
    elif event_type == "gate_result":
        item = _payload(value, {"gate_id", "outcome", "first_pass", "verdict_source", "evidence_ref"}, event_type)
        _require_stable_id(item["gate_id"], "gate_id")
        _require_enum(item["outcome"], {"pass", "fail", "skipped"}, "outcome")
        if not isinstance(item["first_pass"], bool):
            _error("first_pass must be boolean")
        _require_enum(item["verdict_source"], {"human", "agent", "automation"}, "verdict_source")
        _require_stable_ref(item["evidence_ref"], "evidence_ref", nullable=True)
    elif event_type == "review_result":
        item = _payload(value, {"reviewer_id", "reviewer_class", "round", "verdict", "verdict_source", "finding_count", "evidence_ref"}, event_type)
        _require_stable_id(item["reviewer_id"], "reviewer_id")
        _require_enum(item["reviewer_class"], {"plan", "qa", "software-dev", "knowledge-work", "security", "owner"}, "reviewer_class")
        if not _is_integer(item["round"], positive=True):
            _error("round must be a positive integer")
        _require_enum(item["verdict"], {"approve", "return_to_builder", "phase_done", "revise", "skipped"}, "verdict")
        _require_enum(item["verdict_source"], {"human", "agent", "automation"}, "verdict_source")
        if not _is_integer(item["finding_count"]):
            _error("finding_count must be a non-negative integer")
        _require_stable_ref(item["evidence_ref"], "evidence_ref", nullable=True)
    elif event_type == "defect_recorded":
        item = _payload(value, {"defect_id", "introduced_task", "approving_reviewers", "gate_that_should_have_caught_it", "evidence_ref"}, event_type)
        _require_stable_id(item["defect_id"], "defect_id")
        _require_uuid4(item["introduced_task"], "introduced_task", nullable=True)
        _require_sorted_unique(item["approving_reviewers"], "approving_reviewers", _require_stable_id, maximum=64)
        _require_stable_id(item["gate_that_should_have_caught_it"], "gate_that_should_have_caught_it")
        _require_stable_ref(item["evidence_ref"], "evidence_ref")
    elif event_type == "rework_recorded":
        item = _payload(value, {"cause_event_id", "round", "reason", "evidence_ref"}, event_type)
        _require_uuid4(item["cause_event_id"], "cause_event_id")
        if not _is_integer(item["round"], positive=True):
            _error("round must be a positive integer")
        _require_enum(item["reason"], {"gate_failure", "review_finding", "spec_correction", "other"}, "reason")
        _require_stable_ref(item["evidence_ref"], "evidence_ref", nullable=True)
    elif event_type == "lesson_candidate_recorded":
        item = _payload(value, {"kit_facing", "root_cause_ref", "candidate_ref"}, event_type)
        if not isinstance(item["kit_facing"], bool):
            _error("kit_facing must be boolean")
        _require_stable_ref(item["root_cause_ref"], "root_cause_ref")
        _require_stable_ref(item["candidate_ref"], "candidate_ref")
    elif event_type == "fact_check_recorded":
        item = _payload(value, {"gate_id", "verdict", "verdict_source", "finding_count", "failure_classes", "evidence_ref"}, event_type)
        _require_stable_id(item["gate_id"], "gate_id")
        _require_enum(item["verdict"], {"sourced", "return_to_builder"}, "verdict")
        _require_enum(item["verdict_source"], {"human", "agent", "automation"}, "verdict_source")
        if not _is_integer(item["finding_count"]):
            _error("finding_count must be a non-negative integer")
        failures = {
            "unsupported_claim", "weaker_than_claim", "contradiction", "unreliable_source",
            "stale_source", "inadequate_coverage", "prose_contradiction",
        }
        _require_sorted_unique(item["failure_classes"], "failure_classes", lambda entry, name: _require_enum(entry, failures, name), maximum=7)
        if item["verdict"] == "sourced" and (item["finding_count"] != 0 or item["failure_classes"]):
            _error("sourced fact checks must have no findings")
        if item["verdict"] == "return_to_builder" and (item["finding_count"] <= 0 or not item["failure_classes"]):
            _error("return_to_builder fact checks must name findings")
        _require_stable_ref(item["evidence_ref"], "evidence_ref")
    elif event_type == "scorecard_imported":
        item = _payload(value, {"source_path", "source_record_ordinal", "source_record_hash", "source_record_ref"}, event_type)
        if item["source_path"] != "benchmarks/scorecard.jsonl":
            _error("source_path must be the closed scorecard path")
        if not _is_integer(item["source_record_ordinal"], positive=True):
            _error("source_record_ordinal must be a positive integer")
        _require_sha256(item["source_record_hash"], "source_record_hash")
        _require_stable_ref(item["source_record_ref"], "source_record_ref")
    elif event_type == "benchmark_exported":
        item = _payload(value, {"export_batch_id", "target_path", "prior_hash", "exported_event_ids"}, event_type)
        _require_uuid4(item["export_batch_id"], "export_batch_id")
        _require_enum(item["target_path"], {"benchmarks/telemetry-v3.jsonl", "benchmarks/defects.jsonl"}, "target_path")
        _require_sha256(item["prior_hash"], "prior_hash", nullable=True)
        _require_sorted_unique(item["exported_event_ids"], "exported_event_ids", _require_uuid4, maximum=256)
    else:
        _error("event_type must use the closed Telemetry v3 enum")


def validate_event(value: Mapping[str, Any]) -> None:
    """Validate one already-persisted Telemetry v3 event."""

    event = _closed_object(value, TOP_LEVEL_FIELDS, "event")
    if event["schema_version"] != 3 or isinstance(event["schema_version"], bool):
        _error("schema_version must be integer literal 3", code="TELEMETRY_SCHEMA_UNSUPPORTED")
    _require_uuid4(event["event_id"], "event_id")
    _require_uuid4(event["task_id"], "task_id")
    _require_enum(event["event_type"], set(EVENT_TYPES), "event_type")
    _require_timestamp(event["occurred_at"])

    producer = _closed_object(event["producer"], {"id", "revision"}, "producer")
    _require_stable_id(producer["id"], "producer.id")
    _require_stable_ref(producer["revision"], "producer.revision")

    revisions = _closed_object(event["revisions"], REVISION_FIELDS, "revisions")
    for name in sorted(REVISION_FIELDS):
        _validate_revision(revisions[name], f"revisions.{name}")

    lineage = _closed_object(event["lineage"], LINEAGE_FIELDS, "lineage")
    _require_uuid4(lineage["parent_task_id"], "lineage.parent_task_id", nullable=True)
    _require_uuid4(lineage["delegation_id"], "lineage.delegation_id", nullable=True)
    if (lineage["parent_task_id"] is None) != (lineage["delegation_id"] is None):
        _error("parent_task_id and delegation_id must be present together")
    _require_uuid4(lineage["correction_of"], "lineage.correction_of", nullable=True)
    _require_stable_ref(lineage["correction_evidence_ref"], "lineage.correction_evidence_ref", nullable=True)
    if (lineage["correction_of"] is None) != (lineage["correction_evidence_ref"] is None):
        _error("correction lineage fields must be present together", code="TELEMETRY_CORRECTION_INVALID")

    if not isinstance(event["source_class"], str) or event["source_class"] not in {"runtime", "repository", "human", "legacy_import", "derived"}:
        _error("source_class is not allowlisted", code="TELEMETRY_PRIVACY_VIOLATION")
    if not isinstance(event["privacy_class"], str) or event["privacy_class"] not in {"public", "project", "local_private"}:
        _error("privacy_class is not allowlisted", code="TELEMETRY_PRIVACY_VIOLATION")
    _validate_coverage(event["coverage"])
    _validate_tokens(event["tokens"])
    _validate_elapsed(event["elapsed"])
    _validate_payload(event["event_type"], event["payload"])

    encoded = _encode_validated_event(event)
    if len(encoded) > MAX_RECORD_BYTES:
        _error("encoded event exceeds 65,536 bytes")


def _encode_validated_event(value: Mapping[str, Any]) -> bytes:
    try:
        return (
            json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            + "\n"
        ).encode("utf-8")
    except (TypeError, UnicodeError):
        _error("event is not encodable as one UTF-8 JSON object")


def encode_event(value: Mapping[str, Any]) -> bytes:
    validate_event(value)
    return _encode_validated_event(value)


def _prepare_event(value: Mapping[str, Any], channel: _ProducerChannel) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("event input must be an object")
    prepared = copy.deepcopy(value)
    producer = prepared.get("producer")
    if not isinstance(producer, dict) or set(producer) != {"revision"}:
        _error("event input accepts producer.revision only; producer.id is injected")
    _require_stable_ref(producer["revision"], "producer.revision")
    prepared["producer"] = {"id": channel.producer_id, "revision": producer["revision"]}
    validate_event(prepared)
    _enforce_producer_policy(prepared, channel.policy)
    return prepared


def _metadata_values(event: Mapping[str, Any]) -> list[tuple[str, str]]:
    values = [("producer.revision", event["producer"]["revision"])]
    for revision_name, revision in event["revisions"].items():
        if revision["value"] is not None:
            values.append((f"revisions.{revision_name}.value", revision["value"]))
    for requirement in event["coverage"]["missing_requirement_refs"]:
        values.append(("coverage.missing_requirement_refs", requirement))
    correction_ref = event["lineage"]["correction_evidence_ref"]
    if correction_ref is not None:
        values.append(("lineage.correction_evidence_ref", correction_ref))

    metadata_fields = {
        "workflow",
        "delegated_role",
        "gate_id",
        "evidence_ref",
        "reviewer_id",
        "defect_id",
        "approving_reviewers",
        "gate_that_should_have_caught_it",
        "root_cause_ref",
        "candidate_ref",
        "source_record_ref",
    }
    for field, value in event["payload"].items():
        if field not in metadata_fields or value is None:
            continue
        if isinstance(value, list):
            values.extend((f"payload.{field}", item) for item in value)
        else:
            values.append((f"payload.{field}", value))
    return values


def _enforce_producer_policy(event: Mapping[str, Any], policy: ProducerPolicy) -> None:
    if event["source_class"] not in policy.source_classes:
        _error("source_class is not authorized for this producer", code="TELEMETRY_PRIVACY_VIOLATION")
    verdict_source = event["payload"].get("verdict_source")
    if verdict_source is not None and verdict_source not in policy.verdict_sources:
        _error("verdict_source is not authorized for this producer", code="TELEMETRY_PRIVACY_VIOLATION")
    for field, value in _metadata_values(event):
        if not policy.authorizes(field, value):
            _error(f"{field} is outside the producer-owned metadata namespace", code="TELEMETRY_PRIVACY_VIOLATION")


def _duplicate_object_pairs(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate object key")
        result[key] = value
    return result


def _parse_line(raw: bytes, *, path: str, line: int) -> dict[str, Any]:
    if len(raw) > MAX_RECORD_BYTES or not raw.endswith(b"\n"):
        _error("history record boundary is invalid", code="TELEMETRY_HISTORY_CORRUPT", path=path, line=line)
    try:
        text = raw[:-1].decode("utf-8", errors="strict")
        value = json.loads(text, object_pairs_hook=_duplicate_object_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        _error("history record is not a complete UTF-8 JSON object", code="TELEMETRY_HISTORY_CORRUPT", path=path, line=line)
    if not isinstance(value, dict):
        _error("history record is not an object", code="TELEMETRY_HISTORY_CORRUPT", path=path, line=line)
    try:
        validate_event(value)
    except TelemetryError as diagnostic:
        candidate_event_id = value.get("event_id")
        safe_event_id = None
        try:
            _require_uuid4(candidate_event_id, "event_id")
            safe_event_id = candidate_event_id
        except TelemetryError:
            pass
        raise TelemetryError(
            "TELEMETRY_HISTORY_CORRUPT",
            f"stored event fails {diagnostic.code}",
            path=path,
            event_id=safe_event_id,
            line=line,
        ) from None
    return value


def _split_history(raw: bytes, *, path: str) -> tuple[list[dict[str, Any]], int]:
    last_boundary = raw.rfind(b"\n") + 1
    complete = raw[:last_boundary]
    events = [
        _parse_line(line, path=path, line=index)
        for index, line in enumerate(complete.splitlines(keepends=True), 1)
    ]
    _validate_existing_corpus(events, path=path)
    return events, last_boundary


def _privacy_rank(value: str) -> int:
    return {"public": 0, "project": 1, "local_private": 2}[value]


def _validate_correction_shape(correction: Mapping[str, Any], target: Mapping[str, Any]) -> None:
    immutable_paths = (
        ("schema_version",),
        ("task_id",),
        ("event_type",),
        ("source_class",),
        ("producer", "id"),
        ("lineage", "parent_task_id"),
        ("lineage", "delegation_id"),
        ("payload",),
    )
    for path in immutable_paths:
        left: Any = correction
        right: Any = target
        for part in path:
            left = left[part]
            right = right[part]
        if left != right:
            _error("correction changes an immutable field", code="TELEMETRY_CORRECTION_INVALID", event_id=correction["event_id"])
    if _privacy_rank(correction["privacy_class"]) < _privacy_rank(target["privacy_class"]):
        _error("correction loosens privacy", code="TELEMETRY_CORRECTION_INVALID", event_id=correction["event_id"])


def _validate_existing_corpus(events: Sequence[Mapping[str, Any]], *, path: str) -> None:
    by_id: dict[str, Mapping[str, Any]] = {}
    for line, event in enumerate(events, 1):
        event_id = event["event_id"]
        if event_id in by_id:
            raise TelemetryError("TELEMETRY_HISTORY_CORRUPT", "duplicate event ID in history", path=path, event_id=event_id, line=line)
        correction_of = event["lineage"]["correction_of"]
        if correction_of is not None:
            target = by_id.get(correction_of)
            if target is None or correction_of == event_id:
                raise TelemetryError("TELEMETRY_HISTORY_CORRUPT", "correction target is not an earlier event", path=path, event_id=event_id, line=line)
            try:
                _validate_correction_shape(event, target)
            except TelemetryError:
                raise TelemetryError("TELEMETRY_HISTORY_CORRUPT", "stored correction is invalid", path=path, event_id=event_id, line=line) from None
        by_id[event_id] = event


def _authorize_correction(
    event: Mapping[str, Any],
    encoded: bytes,
    existing: Sequence[Mapping[str, Any]],
    channel: _ProducerChannel,
) -> None:
    target_id = event["lineage"]["correction_of"]
    if target_id is None:
        return
    by_id = {item["event_id"]: item for item in existing}
    target = by_id.get(target_id)
    if target is None or target_id == event["event_id"]:
        _error("correction target must be an earlier event", code="TELEMETRY_CORRECTION_INVALID", event_id=event["event_id"])
    if target["producer"]["id"] != channel.producer_id:
        _error("correction arrived through a different producer channel", code="TELEMETRY_CORRECTION_UNAUTHORIZED", event_id=event["event_id"])
    _validate_correction_shape(event, target)
    if channel.policy.correction_resolver is None:
        _error("correction lacks channel authority", code="TELEMETRY_CORRECTION_UNAUTHORIZED", event_id=event["event_id"])

    root = target
    seen = {event["event_id"]}
    while root["lineage"]["correction_of"] is not None:
        current_id = root["event_id"]
        if current_id in seen:
            _error("correction chain is cyclic", code="TELEMETRY_CORRECTION_INVALID", event_id=event["event_id"])
        seen.add(current_id)
        parent = by_id.get(root["lineage"]["correction_of"])
        if parent is None:
            _error("correction chain is incomplete", code="TELEMETRY_CORRECTION_INVALID", event_id=event["event_id"])
        root = parent

    binding = {
        "root_event_id": root["event_id"],
        "target_event_id": target_id,
        "correcting_event_id": event["event_id"],
        "record_sha256": hashlib.sha256(encoded).hexdigest(),
    }
    try:
        authorized = channel.policy.correction_resolver(event["lineage"]["correction_evidence_ref"], binding)
    except Exception:
        authorized = False
    if authorized is not True:
        _error("correction evidence binding was rejected", code="TELEMETRY_CORRECTION_UNAUTHORIZED", event_id=event["event_id"])


def _is_linklike(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def _canonical_root(root: Path | str) -> Path:
    supplied = Path(root)
    if not supplied.is_absolute():
        _error("repository root must be absolute", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    try:
        info = supplied.lstat()
        resolved = supplied.resolve(strict=True)
    except OSError:
        _error("repository root is unavailable", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    if _is_linklike(info) or not stat.S_ISDIR(info.st_mode) or os.path.normcase(str(supplied)) != os.path.normcase(str(resolved)):
        _error("repository root is not canonical", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    return resolved


def _verify_parent(root: Path, parent: Path, *, create: bool) -> None:
    try:
        relative = parent.relative_to(root)
    except ValueError:
        _error("event path escapes the repository root", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    current = root
    for part in relative.parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if not create:
                _error("event parent path is missing", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
            try:
                current.mkdir(mode=0o700)
            except OSError:
                _error("event parent path cannot be created safely", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
            info = current.lstat()
        except OSError:
            _error("event parent path is unavailable", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        if _is_linklike(info) or not stat.S_ISDIR(info.st_mode):
            _error("event parent path is link-like or non-directory", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        try:
            if not current.resolve(strict=True).is_relative_to(root):
                _error("event parent path escapes the repository root", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        except OSError:
            _error("event parent containment is ambiguous", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))


def _verify_target_before_open(target: Path) -> None:
    try:
        info = target.lstat()
    except FileNotFoundError:
        return
    except OSError:
        _error("event target is unavailable", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    if _is_linklike(info) or not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        _error("event target must be one unlinked regular file", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))


def _handle_identity(fd: int, target: Path) -> tuple[int, int]:
    try:
        handle = os.fstat(fd)
        path_info = target.lstat()
    except OSError:
        _error("event target identity is unavailable", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    if (
        _is_linklike(path_info)
        or not stat.S_ISREG(handle.st_mode)
        or not stat.S_ISREG(path_info.st_mode)
        or handle.st_nlink != 1
        or path_info.st_nlink != 1
        or not os.path.samestat(handle, path_info)
    ):
        _error("event target identity changed", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    return handle.st_dev, handle.st_ino


def _read_fd(fd: int, *, path: str) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks = []
    pending = 0
    while True:
        chunk = os.read(fd, min(1024 * 1024, MAX_RECORD_BYTES + 1 - pending))
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        start = 0
        while True:
            boundary = chunk.find(b"\n", start)
            if boundary < 0:
                pending += len(chunk) - start
                if pending > MAX_RECORD_BYTES:
                    _error("history record exceeds 65,536 bytes", code="TELEMETRY_HISTORY_CORRUPT", path=path)
                break
            record_bytes = pending + boundary - start + 1
            if record_bytes > MAX_RECORD_BYTES:
                _error("history record exceeds 65,536 bytes", code="TELEMETRY_HISTORY_CORRUPT", path=path)
            pending = 0
            start = boundary + 1


def _append_local_event(
    repository_root: Path | str,
    event: Mapping[str, Any],
    channel: _ProducerChannel,
) -> dict[str, Any]:
    """Validate and append one event to the fixed local Telemetry v3 stream."""

    if type(channel) is not _ProducerChannel:
        _error("producer channel capability is invalid", code="TELEMETRY_CORRECTION_UNAUTHORIZED", path=str(EVENT_PATH))
    root = _canonical_root(repository_root)
    target = root / EVENT_PATH

    with _WRITE_LOCK:
        try:
            prepared = _prepare_event(event, channel)
        except TelemetryError as diagnostic:
            raise TelemetryError(diagnostic.code, diagnostic.detail, path=str(EVENT_PATH)) from None
        encoded = _encode_validated_event(prepared)
        _verify_parent(root, target.parent, create=True)
        _verify_target_before_open(target)
        flags = os.O_RDWR | os.O_APPEND | os.O_CREAT
        flags |= getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(target, flags, 0o600)
        except OSError:
            _error("event target cannot be opened safely", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        try:
            identity = _handle_identity(fd, target)
            raw = _read_fd(fd, path=str(EVENT_PATH))
            existing, complete_bytes = _split_history(raw, path=str(EVENT_PATH))
            if any(item["event_id"] == prepared["event_id"] for item in existing):
                _error("event ID already exists", code="TELEMETRY_DUPLICATE_EVENT_ID", path=str(EVENT_PATH), event_id=prepared["event_id"])
            _authorize_correction(prepared, encoded, existing, channel)

            _verify_parent(root, target.parent, create=False)
            if _handle_identity(fd, target) != identity:
                _error("event target identity changed before append", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH), event_id=prepared["event_id"])
            if complete_bytes != len(raw):
                os.ftruncate(fd, complete_bytes)
                os.lseek(fd, 0, os.SEEK_END)
            written = os.write(fd, encoded)
            _verify_parent(root, target.parent, create=False)
            if _handle_identity(fd, target) != identity:
                _error("event target identity changed after append", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH), event_id=prepared["event_id"])
            if written <= 0 or written != len(encoded):
                os.fsync(fd)
                _error("append did not write one complete record", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH), event_id=prepared["event_id"])
            os.fsync(fd)
            _verify_parent(root, target.parent, create=False)
            if _handle_identity(fd, target) != identity:
                _error("event target identity changed after append", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH), event_id=prepared["event_id"])
        finally:
            os.close(fd)
    return prepared


def validate_local_events(repository_root: Path | str) -> list[dict[str, Any]]:
    """Read and validate the complete local stream without mutating it."""

    root = _canonical_root(repository_root)
    target = root / EVENT_PATH
    if not target.parent.exists():
        return []
    _verify_parent(root, target.parent, create=False)
    _verify_target_before_open(target)
    if not target.exists():
        return []
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(target, flags)
    except OSError:
        _error("event target cannot be opened safely", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
    try:
        identity = _handle_identity(fd, target)
        raw = _read_fd(fd, path=str(EVENT_PATH))
        events, complete_bytes = _split_history(raw, path=str(EVENT_PATH))
        _verify_parent(root, target.parent, create=False)
        if _handle_identity(fd, target) != identity:
            _error("event target identity changed while validating", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        if complete_bytes != len(raw):
            _error("event stream ends with an interrupted record", code="TELEMETRY_HISTORY_CORRUPT", path=str(EVENT_PATH))
        return events
    finally:
        os.close(fd)
