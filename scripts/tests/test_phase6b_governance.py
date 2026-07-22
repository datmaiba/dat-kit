"""Class C evidence checks for Phase 6B B0 governance admission."""

from __future__ import annotations

import json
from pathlib import Path
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
TESTS = Path(__file__).resolve().parent
PROPOSAL = ROOT / "docs/decisions/evolution-proposal-27d40cbf7ff8c9cebe93.proposal.json"
DECISIONS = ROOT / "docs/decisions/evolution-manual.decisions.jsonl"
BASELINE_COMMIT = "8c8b4e08c9768fe5f78363c77a74a0a11625987c"
B0_FROZEN_INPUT_COMMIT = "d9bc068442891eef21fdb5ecc9d7d1702e80b29a"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(TESTS))

from evolution_evidence import (
    assert_approved_decision_common,
    assert_frozen_proposal,
    git_json,
)


def test_b0_proposal_identity_inputs_policy_and_references_are_frozen() -> None:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evolution = git_json(ROOT, BASELINE_COMMIT, "registry/evolution.json")
    assert isinstance(evolution, dict)
    policy = next(
        item for item in evolution["policies"]
        if item["policy_id"] == "platform-contract-policy"
    )
    assert_frozen_proposal(
        ROOT,
        proposal,
        evolution,
        BASELINE_COMMIT,
        input_commits={
            "docs/spikes/phase-6b/b0-governance-baseline.md": B0_FROZEN_INPUT_COMMIT,
            "scripts/tests/test_registry_catalog.py": B0_FROZEN_INPUT_COMMIT,
        },
        evidence_commits={
            "docs/spikes/phase-6b/b0-governance-baseline.md": B0_FROZEN_INPUT_COMMIT,
        },
    )
    assert proposal["affected_paths"] == proposal["patch_scope"] == [
        "registry/evolution.json"
    ]
    assert proposal["required_gates"] == policy["required_gates"]
    assert proposal["required_reviewers"] == policy["required_reviewers"]
    assert proposal["closer_authority_ref"] == policy["closer_authority_ref"]


def test_b0_owner_decision_is_valid_when_recorded() -> None:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evolution = git_json(ROOT, BASELINE_COMMIT, "registry/evolution.json")
    assert isinstance(evolution, dict)
    records = [json.loads(line) for line in DECISIONS.read_text(encoding="utf-8").splitlines()]
    decisions = [record for record in records if record["proposal_id"] == proposal["proposal_id"]]
    approvals = [record for record in decisions if record["decision"] == "approved"]
    assert len(approvals) <= 1
    if not approvals:
        return

    decision = approvals[0]
    assert_approved_decision_common(
        decision,
        proposal,
        evolution,
        "decision-27d40cbf7ff8c9cebe93-0001",
    )
    assert decision["effective_from_run"].startswith("run-2026-07-22-phase6b-b0-")
    assert len(decision["gate_evidence_refs"]) == 2
    assert decision["gate_evidence_refs"][0].startswith(
        "gate/full-cross-component-regression-"
    )
    assert decision["gate_evidence_refs"][1].startswith("gate/rollback-rehearsal-")
