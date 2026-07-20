"""Contract-only checks for the Phase 6A Telemetry v3 boundary."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
CONTRACT = ROOT / "docs/contracts/telemetry-v3.md"
PROPOSAL = ROOT / "docs/decisions/evolution-proposal-7658d0c11f5cd343a855.proposal.json"
sys.path.insert(0, str(SCRIPTS))

from registry import Catalog, Diagnostic, canonical_file_hash, canonical_json


def contract_text() -> str:
    return CONTRACT.read_text(encoding="utf-8")


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


def test_proposal_identity_and_policy_binding_are_deterministic() -> None:
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
        "plans/PLAN-v7-platform.md#phase-6-telemetry-v3-and-dat-kit-2.1.0",
    ]
    for reference in proposal["evidence_refs"]:
        path, separator, anchor = reference.partition("#")
        assert separator and anchor and (ROOT / path).is_file()


def test_envelope_fields_types_and_closed_enums_are_normative() -> None:
    text = contract_text()
    for field in (
        "`schema_version`", "`event_id`", "`task_id`", "`event_type`",
        "`occurred_at`", "`producer`", "`revisions`", "`lineage`",
        "`source_class`", "`privacy_class`", "`coverage`", "`tokens`",
        "`elapsed`", "`payload`",
    ):
        assert field in text
    assert "`runtime | repository | human | legacy_import | derived`" in text
    assert "`public | project | local_private`" in text
    assert "`full | partial`" in text
    assert "Unknown fields are invalid" in text


def test_lifecycle_lineage_and_event_payloads_are_closed() -> None:
    text = contract_text()
    for event_type in (
        "task_started", "task_finished", "handoff_created", "task_resumed",
        "delegation_started", "gate_result", "review_result", "defect_recorded",
        "rework_recorded", "lesson_candidate_recorded", "fact_check_recorded",
        "scorecard_imported", "benchmark_exported",
    ):
        assert f"`{event_type}`" in text
    for requirement in (
        "`resumed_from_handoff`", "`first_pass`", "`verdict_source`",
        "`introduced_task`", "`approving_reviewers`",
        "`gate_that_should_have_caught_it`", "`kit_facing`",
    ):
        assert requirement in text
    assert "minted at LOAD" in text
    assert "same `event_type`" in text
    assert "forward, self, missing, or cyclic correction" in text
    assert "Exactly one original `task_started`" in text
    assert "Exactly one original `task_finished`" in text
    assert "finish-before-start" in text
    assert "one immutable `(parent_task_id, delegation_id)` pair" in text
    assert "exactly one parent-child task pair" in text


def test_attribution_coverage_storage_and_recovery_are_bounded() -> None:
    text = contract_text()
    for requirement in (
        "`exact | unknown`", "`human | agent | automation`",
        "`completion_only | unsupported_host_start | telemetry_disabled | legacy_import | producer_failure`",
        "single writer", "`O_APPEND`", "exact positive write count",
        "interrupted final record", "Multi-writer locking is deferred",
        "Duplicate `event_id` values are invalid",
        "full coverage requires both `task_started` and `task_finished`",
    ):
        assert requirement in text


def test_privacy_retention_import_export_disable_and_compatibility_are_explicit() -> None:
    text = contract_text()
    for path in (
        "`telemetry/events.jsonl`", "`benchmarks/telemetry-v3.jsonl`",
        "`benchmarks/defects.jsonl`", "`benchmarks/scorecard.jsonl`",
    ):
        assert path in text
    for requirement in (
        "Raw prompts", "tool request or response bodies", "environment values",
        "credentials", "secrets", "No automatic TTL", "verified export",
        "never rewrites existing benchmark bytes", "must not block the work loop",
        "1.x", "schema freeze", "No telemetry field accepts free-form text",
        "`[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`",
        "`source_record_ordinal`", "path + ordinal + hash + event type",
        "`benchmark_exported` events are never export-eligible",
    ):
        assert requirement in text


def test_five_named_producers_and_required_views_are_mapped() -> None:
    text = contract_text()
    for requirement in (
        "build-loop HARVEST", "diagnosing-bugs", "knowledge-work fact-check",
        "resumed_from_handoff", "per-reviewer view", "event-coverage-rate view",
        "`planned`", "`active`", "`reviewer_id`",
    ):
        assert requirement in text
