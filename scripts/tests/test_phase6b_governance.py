"""Class C evidence checks for Phase 6B B0 governance admission."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
PROPOSAL = ROOT / "docs/decisions/evolution-proposal-27d40cbf7ff8c9cebe93.proposal.json"
DECISIONS = ROOT / "docs/decisions/evolution-manual.decisions.jsonl"
BASELINE_COMMIT = "8c8b4e08c9768fe5f78363c77a74a0a11625987c"
sys.path.insert(0, str(SCRIPTS))

from registry import canonical_file_hash, canonical_json


def github_heading_slugs(text: str) -> set[str]:
    slugs = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        slug = "".join(char for char in heading if char.isalnum() or char in " -_")
        slugs.add(slug.replace(" ", "-"))
    return slugs


def baseline_hash(path: str) -> str:
    if path != "registry/evolution.json":
        return canonical_file_hash(ROOT / path)
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{BASELINE_COMMIT}:{path}"],
        capture_output=True,
        check=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def test_b0_proposal_identity_inputs_policy_and_references_are_frozen() -> None:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evolution = json.loads((ROOT / "registry/evolution.json").read_text(encoding="utf-8"))
    policy = next(
        item for item in evolution["policies"]
        if item["policy_id"] == "platform-contract-policy"
    )
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
        assert item["sha256"] == baseline_hash(item["path"])

    payload = copy.deepcopy(proposal)
    payload.pop("proposal_id")
    expected_id = "proposal-" + hashlib.sha256(canonical_json(payload)).hexdigest()[:20]
    assert proposal["proposal_id"] == expected_id
    assert proposal["affected_paths"] == proposal["patch_scope"] == [
        "registry/evolution.json"
    ]
    assert proposal["required_gates"] == policy["required_gates"]
    assert proposal["required_reviewers"] == policy["required_reviewers"]
    assert proposal["closer_authority_ref"] == policy["closer_authority_ref"]

    for reference in proposal["evidence_refs"]:
        relative, separator, anchor = reference.partition("#")
        target = ROOT / relative
        assert separator and anchor and target.is_file()
        assert anchor in github_heading_slugs(target.read_text(encoding="utf-8"))


def test_b0_owner_decision_is_valid_when_recorded() -> None:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evolution = json.loads((ROOT / "registry/evolution.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in DECISIONS.read_text(encoding="utf-8").splitlines()]
    decisions = [record for record in records if record["proposal_id"] == proposal["proposal_id"]]
    assert len(decisions) <= 1
    if not decisions:
        return

    decision = decisions[0]
    assert set(decision) == {
        "format_revision", "decision_id", "proposal_id", "decision", "decided_at",
        "policy_revision", "policy_hash", "closer_identity", "closer_role",
        "approval_reference", "gate_evidence_refs", "effective_from_run",
        "observation_status", "correction_of",
    }
    assert decision["decision_id"] == "decision-27d40cbf7ff8c9cebe93-0001"
    assert decision["decision"] == "approved"
    assert decision["observation_status"] == "observing"
    assert decision["correction_of"] is None
    assert decision["policy_revision"] == proposal["policy_revision"]
    assert decision["policy_hash"] == proposal["policy_hash"]
    assert decision["effective_from_run"].startswith("run-2026-07-22-phase6b-b0-")

    authority = next(
        item for item in evolution["authorities"]
        if item["authority_id"] == proposal["closer_authority_ref"]
    )
    appointment = next(
        item for item in authority["appointments"]
        if item["appointment_id"] == "appointment/platform-owner-1"
    )
    assert decision["closer_identity"] == appointment["identity"] == "Dat Mai Ba"
    assert decision["closer_identity"] != proposal["proposer_identity"]
    assert decision["closer_role"] == appointment["role"] == "platform-owner"
    assert appointment["effective_from"] <= decision["decided_at"]
    assert appointment["revoked_at"] is None
    assert decision["approval_reference"] == (
        f"{appointment['appointment_id']}#{proposal['proposal_id']}"
    )
    assert len(decision["gate_evidence_refs"]) == 2
    assert decision["gate_evidence_refs"][0].startswith(
        "gate/full-cross-component-regression-"
    )
    assert decision["gate_evidence_refs"][1].startswith("gate/rollback-rehearsal-")
