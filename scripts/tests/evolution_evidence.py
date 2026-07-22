"""Shared immutable-evidence assertions for evolution proposal tests."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Mapping

from registry import canonical_json


DECISION_KEYS = {
    "format_revision", "decision_id", "proposal_id", "decision", "decided_at",
    "policy_revision", "policy_hash", "closer_identity", "closer_role",
    "approval_reference", "gate_evidence_refs", "effective_from_run",
    "observation_status", "correction_of",
}


def git_blob(root: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        capture_output=True,
        check=True,
    )
    return result.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_file_hash(root: Path, commit: str, path: str) -> str:
    return hashlib.sha256(git_blob(root, commit, path)).hexdigest()


def git_json(root: Path, commit: str, path: str) -> object:
    return json.loads(git_blob(root, commit, path).decode("utf-8"))


def github_heading_slugs(text: str) -> set[str]:
    slugs = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        slug = "".join(char for char in heading if char.isalnum() or char in " -_")
        slugs.add(slug.replace(" ", "-"))
    return slugs


def policy_graph(evolution: dict[str, object], policy_id: str) -> dict[str, object]:
    policies = evolution["policies"]
    authorities = evolution["authorities"]
    signal_rows = evolution["signals"]
    assert isinstance(policies, list)
    assert isinstance(authorities, list)
    assert isinstance(signal_rows, list)
    policy = next(item for item in policies if item["policy_id"] == policy_id)
    authority = next(
        item for item in authorities
        if item["authority_id"] == policy["closer_authority_ref"]
    )
    signals = {item["signal_id"]: item for item in signal_rows}
    return {
        "policy": policy,
        "closer_authority": authority,
        "required_signals": [signals[item] for item in sorted(policy["required_signals"])],
    }


def assert_frozen_proposal(
    root: Path,
    proposal: dict[str, object],
    evolution: dict[str, object],
    default_commit: str,
    *,
    input_commits: Mapping[str, str] | None = None,
    evidence_commits: Mapping[str, str] | None = None,
) -> None:
    graph = policy_graph(evolution, str(proposal["policy_revision"]).rsplit("/", 1)[0])
    assert proposal["policy_hash"] == hashlib.sha256(canonical_json(graph)).hexdigest()
    input_hashes = proposal["input_hashes"]
    assert isinstance(input_hashes, list)
    assert input_hashes == sorted(input_hashes, key=canonical_json)
    for item in input_hashes:
        path = item["path"]
        commit = (input_commits or {}).get(path, default_commit)
        assert item["sha256"] == git_file_hash(root, commit, path)

    payload = copy.deepcopy(proposal)
    payload.pop("proposal_id")
    expected_id = "proposal-" + hashlib.sha256(canonical_json(payload)).hexdigest()[:20]
    assert proposal["proposal_id"] == expected_id

    evidence_refs = proposal["evidence_refs"]
    assert isinstance(evidence_refs, list)
    for reference in evidence_refs:
        relative, separator, anchor = reference.partition("#")
        commit = (evidence_commits or {}).get(relative, default_commit)
        text = git_blob(root, commit, relative).decode("utf-8")
        assert separator and anchor and anchor in github_heading_slugs(text)


def assert_approved_decision_common(
    decision: dict[str, object],
    proposal: dict[str, object],
    evolution: dict[str, object],
    expected_decision_id: str,
) -> dict[str, object]:
    assert set(decision) == DECISION_KEYS
    assert decision["format_revision"] == 1
    assert decision["decision_id"] == expected_decision_id
    assert decision["decision"] == "approved"
    assert decision["observation_status"] == "observing"
    assert decision["correction_of"] is None
    assert decision["policy_revision"] == proposal["policy_revision"]
    assert decision["policy_hash"] == proposal["policy_hash"]

    graph = policy_graph(evolution, str(proposal["policy_revision"]).rsplit("/", 1)[0])
    authority = graph["closer_authority"]
    assert isinstance(authority, dict)
    appointment = next(
        item for item in authority["appointments"]
        if item["appointment_id"] == "appointment/platform-owner-1"
    )
    assert decision["closer_identity"] == appointment["identity"] == "Dat Mai Ba"
    assert decision["closer_identity"] != proposal["proposer_identity"]
    assert decision["closer_role"] == appointment["role"] == "platform-owner"
    assert proposal["governance_class"] in authority["allowed_decision_classes"]
    assert appointment["effective_from"] <= decision["decided_at"]
    assert appointment["revoked_at"] is None
    assert decision["approval_reference"] == (
        f"{appointment['appointment_id']}#{proposal['proposal_id']}"
    )
    return appointment

