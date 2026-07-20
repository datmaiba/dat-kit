"""Structural contract-only checks for the Phase 6A Telemetry v3 boundary."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
CONTRACT = ROOT / "docs/contracts/telemetry-v3.md"
PROPOSAL = ROOT / "docs/decisions/evolution-proposal-f80fa03211e51c3f68c5.proposal.json"
sys.path.insert(0, str(SCRIPTS))

from registry import Catalog, Diagnostic, canonical_file_hash, canonical_json


def contract_text() -> str:
    return CONTRACT.read_text(encoding="utf-8")


def section(text: str, start: str, end: str) -> str:
    assert text.count(start) == 1, start
    assert text.count(end) == 1, end
    return text.split(start, 1)[1].split(end, 1)[0]


def prose(text: str) -> str:
    """Collapse Markdown line wrapping while preserving normative wording."""
    return " ".join(text.split())


def markdown_table(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 2 or cells[0].startswith("---") or cells[1] in {"Type and rule", "Exact payload fields"}:
            continue
        key = cells[0].strip("`")
        assert key not in rows, key
        rows[key] = cells[1]
    return rows


def github_heading_slugs(text: str) -> set[str]:
    slugs = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        slug = "".join(char for char in heading if char.isalnum() or char in " -_")
        slugs.add(slug.replace(" ", "-"))
    return slugs


def test_contract_is_routed_as_class_c_platform_contract() -> None:
    catalog = Catalog.load(ROOT)
    assert isinstance(catalog, Catalog), catalog
    explanation = catalog.explain_path("docs/contracts/telemetry-v3.md")
    assert not isinstance(explanation, Diagnostic), explanation
    assert explanation["component_id"] == "registry-contract"
    assert explanation["governance_class"] == "C"
    assert explanation["policy_revision"] == "platform-contract-policy/1"
    assert explanation["required_gates"] == [
        "full-cross-component-regression",
        "rollback-rehearsal",
    ]
    assert explanation["required_reviewers"] == [
        "knowledge-work-reviewer",
        "software-dev-reviewer",
    ]
    assert explanation["closer_authority_ref"] == "platform-owner"


def test_proposal_identity_policy_and_evidence_fragments_are_valid() -> None:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evolution = json.loads((ROOT / "registry/evolution.json").read_text(encoding="utf-8"))
    policy = next(item for item in evolution["policies"] if item["policy_id"] == "platform-contract-policy")
    authority = next(
        item for item in evolution["authorities"]
        if item["authority_id"] == policy["closer_authority_ref"]
    )
    signals = {item["signal_id"]: item for item in evolution["signals"]}
    policy_graph = {
        "policy": policy,
        "closer_authority": authority,
        "required_signals": [signals[item] for item in sorted(policy["required_signals"])],
    }
    assert proposal["policy_hash"] == hashlib.sha256(canonical_json(policy_graph)).hexdigest()
    assert proposal["input_hashes"] == sorted(proposal["input_hashes"], key=canonical_json)
    for item in proposal["input_hashes"]:
        assert item["sha256"] == canonical_file_hash(ROOT / item["path"])
    payload = copy.deepcopy(proposal)
    payload.pop("proposal_id")
    expected_id = "proposal-" + hashlib.sha256(canonical_json(payload)).hexdigest()[:20]
    assert proposal["proposal_id"] == expected_id
    assert proposal["evidence_refs"] == [
        "handoffs/HANDOFF-2026-07-21-phase6-telemetry-v3-entry.md#verified-gates",
        "plans/PLAN-v7-platform.md#phase-6--telemetry-v3-and-dat-kit-210",
    ]
    for reference in proposal["evidence_refs"]:
        relative, separator, anchor = reference.partition("#")
        target = ROOT / relative
        assert separator and anchor and target.is_file()
        assert anchor in github_heading_slugs(target.read_text(encoding="utf-8"))


def test_envelope_table_owns_every_required_field_and_type() -> None:
    text = contract_text()
    envelope = markdown_table(section(text, "## T3.3 Closed event envelope", "### T3.3.1 String grammars"))
    assert set(envelope) == {
        "schema_version", "event_id", "task_id", "event_type", "occurred_at",
        "producer", "revisions", "lineage", "source_class", "privacy_class",
        "coverage", "tokens", "elapsed", "payload",
    }
    assert envelope["schema_version"] == "integer literal `3`"
    assert "UUIDv4" in envelope["event_id"] and "unique" in envelope["event_id"]
    assert envelope["task_id"] == "canonical lowercase UUIDv4 string"
    assert "all revision references" in envelope["revisions"]
    assert "every key is present and nullable" in envelope["lineage"]
    assert envelope["source_class"] == "`runtime`, `repository`, `human`, `legacy_import`, or `derived`"
    assert envelope["privacy_class"] == "`public`, `project`, or `local_private`"
    assert "Unknown fields are invalid" in text


def test_payload_table_owns_closed_event_shapes() -> None:
    text = contract_text()
    payloads = markdown_table(section(text, "## T3.6 Lifecycle and closed event payloads", "## T3.7 Lineage and corrections"))
    assert set(payloads) == {
        "task_started", "task_finished", "handoff_created", "task_resumed",
        "delegation_started", "gate_result", "review_result", "defect_recorded",
        "rework_recorded", "lesson_candidate_recorded", "fact_check_recorded",
        "scorecard_imported", "benchmark_exported",
    }
    assert payloads["task_started"] == "`{workflow: stable-id}`"
    assert payloads["task_resumed"] == (
        "`{handoff_ref: path, resumed_from_handoff: true, resumed_from_event_id: UUIDv4}`"
    )
    assert "delegation_id: UUIDv4" in payloads["delegation_started"]
    assert "first_pass: bool" in payloads["gate_result"]
    assert "reviewer_id: stable-id" in payloads["review_result"]
    assert "introduced_task: UUIDv4 or null" in payloads["defect_recorded"]
    assert "kit_facing: bool" in payloads["lesson_candidate_recorded"]
    assert "source_record_ordinal: positive-integer" in payloads["scorecard_imported"]
    assert "verdict: sourced/return_to_builder" in payloads["fact_check_recorded"]
    assert "finding_count: non-negative-integer" in payloads["fact_check_recorded"]
    assert "failure_classes: sorted-unique-fact-check-failure-array" in payloads["fact_check_recorded"]


def test_lifecycle_coverage_lineage_and_corrections_are_satisfiable() -> None:
    text = contract_text()
    coverage = section(text, "### T3.5.1 Coverage", "### T3.5.2 Tokens")
    lifecycle = section(text, "## T3.6 Lifecycle and closed event payloads", "## T3.7 Lineage and corrections")
    lineage = section(text, "## T3.7 Lineage and corrections", "## T3.8 Append, validation, and recovery")
    assert (
        "`completion_only | unsupported_host_start | telemetry_disabled | legacy_import | "
        "producer_failure | in_progress`"
    ) in coverage
    assert "`in_progress` is valid only before the original `task_finished`" in coverage
    assert "full coverage requires both `task_started` and `task_finished`" in coverage
    assert "Exactly one original `task_started`" in lifecycle
    assert "Exactly one original `task_finished`" in lifecycle
    assert "finish-before-start" in lifecycle
    assert "does not emit another `task_started`" in lifecycle
    assert "same `task_id`" in lifecycle
    assert "earlier unmatched `handoff_created.event_id`" in lifecycle
    assert "one immutable `(parent_task_id, delegation_id)` pair" in lineage
    assert "parent event keeps the parent's own lineage pair" in lineage
    assert "exactly one parent-child task pair" in lineage
    assert "same `event_type`" in lineage
    assert "forward, self, missing, or cyclic correction" in lineage
    lineage_prose = prose(lineage)
    assert "Immutable target fields are `schema_version`, `task_id`, `event_type`" in lineage_prose
    assert "Replacement fields are `coverage`, `tokens`, `elapsed`, and `payload`" in lineage_prose
    assert "Correction-evidence fields are `event_id`, `occurred_at`, `producer`, and `revisions`" in lineage_prose


def test_partial_reason_precedence_import_set_and_defect_projection_are_closed() -> None:
    text = contract_text()
    coverage = section(text, "### T3.5.1 Coverage", "### T3.5.2 Tokens")
    transfer = section(text, "## T3.10 Import, export, retention, and durable history", "## T3.11 Disable, downgrade, and compatibility")
    assert (
        "`telemetry_disabled` > `legacy_import` > `producer_failure` > "
        "`unsupported_host_start` > `completion_only`"
    ) in coverage
    transfer_prose = prose(transfer)
    assert "exactly one `scorecard_imported` and one `task_finished`" in transfer_prose
    assert "mints one UUIDv4 task ID on the first import of the source-record identity" in transfer_prose
    assert "reuses that task ID after an interrupted import" in transfer_prose
    assert "source-record identity is path + ordinal + hash" in transfer_prose
    assert "linked event identity is that source-record identity + event type" in transfer_prose
    assert "terminal CRLF or CR to LF" in transfer_prose
    assert "include that LF" in transfer_prose
    projection = markdown_table(transfer)
    assert projection["Defect projection field"] == "Normative value"
    assert set(projection) == {
        "Defect projection field",
        "schema_version", "event_id", "task_id", "parent_task_id", "delegation_id",
        "correction_of", "occurred_at", "defect_id", "introduced_task",
        "approving_reviewers", "gate_that_should_have_caught_it", "evidence_ref",
    }


def test_attribution_privacy_storage_import_export_and_compatibility_are_bounded() -> None:
    text = contract_text()
    for requirement in (
        "`exact | unknown`", "`human | agent | automation`", "single writer",
        "`O_APPEND`", "exact positive write count", "interrupted final record",
        "Multi-writer locking is deferred", "Duplicate `event_id` values are invalid",
        "Raw prompts", "tool request or response bodies", "environment values",
        "credentials", "secrets", "No telemetry field accepts free-form text",
        "`[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`", "No automatic TTL",
            "verified export", "never rewrites existing benchmark bytes",
            "source-record identity is path + ordinal + hash", "`benchmark_exported` events are never export-eligible",
        "must not block the work loop", "1.x", "schema freeze",
    ):
        assert requirement in text
    for path in (
        "`telemetry/events.jsonl`", "`benchmarks/telemetry-v3.jsonl`",
        "`benchmarks/defects.jsonl`", "`benchmarks/scorecard.jsonl`",
    ):
        assert path in text


def test_five_producer_rows_and_report_keys_are_structurally_owned() -> None:
    text = contract_text()
    producer_section = section(text, "## T3.12 Required producers and status truthfulness", "## T3.13 Conformance and release boundary")
    for requirement in (
        "build-loop HARVEST", "diagnosing-bugs", "knowledge-work fact-check",
        "resumed_from_handoff", "per-reviewer view", "event-coverage-rate view",
        "Every producer begins `planned`", "becomes `active`", "`reviewer_id`",
    ):
        assert requirement in producer_section
