#!/usr/bin/env python3
"""Validate Phase 1A examples against explicit normative contract clauses.

This is review evidence, not a runtime registry schema. The Markdown contracts
remain authoritative; Phase 1B must implement them independently.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from datetime import date, datetime
from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "docs" / "contracts" / "examples"
HEX64 = re.compile(r"[0-9a-f]{64}")
SEMVER = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
RFC3339_UTC_SHAPE = re.compile(
    r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    r"[Tt](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.(?P<fraction>[0-9]+))?(?P<offset>[Zz]|[+-][0-9]{2}:[0-9]{2})"
)
MATERIALIZATION_ACTIONS = {"copy", "render-pointer", "preserve", "RETIRE_LEGACY"}
PRECONDITIONS = {
    "target-absent",
    "target-exact-expected-hash",
    "target-user-owned-preserve",
    "approved-backup-and-exact-hash",
}
ACTION_PRECONDITIONS = {
    "copy": {"target-absent", "target-exact-expected-hash"},
    "render-pointer": {"target-absent", "target-exact-expected-hash"},
    "preserve": {"target-user-owned-preserve"},
    "RETIRE_LEGACY": {"approved-backup-and-exact-hash"},
}
WINDOWS_RESERVED_BASENAMES = {
    "con", "prn", "aux", "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
SHELL_EXECUTABLES = {
    "sh", "bash", "dash", "zsh", "ksh", "fish",
    "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe",
}
COMMAND_STRING_FLAGS = {"-c", "/c", "-command", "--command", "-encodedcommand"}
INDIRECT_EXECUTORS = {"env", "env.exe", "command", "xargs", "start", "start.exe"}


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(name: str) -> dict[str, Any]:
    value = json.loads(
        (EXAMPLES / name).read_text(encoding="utf-8"),
        object_pairs_hook=_object_without_duplicate_keys,
    )
    if not isinstance(value, dict):
        raise AssertionError(f"{name}: root must be an object")
    return value


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    assert actual == expected, f"{label}: fields missing={expected - actual} unknown={actual - expected}"


def canonical_relative_path(raw: str) -> str:
    assert isinstance(raw, str) and raw and "\\" not in raw
    assert raw == unicodedata.normalize("NFC", raw)
    assert not any(unicodedata.category(char) == "Cc" for char in raw)
    assert not any(char in raw for char in '<>:"|?*')
    parts = raw.split("/")
    assert all(part not in {"", ".", ".."} for part in parts)
    for part in parts:
        assert not part.endswith((" ", "."))
        assert part.split(".", 1)[0].casefold() not in WINDOWS_RESERVED_BASENAMES
    windows = PureWindowsPath(raw)
    posix = PurePosixPath(raw)
    normalized = posix.as_posix()
    assert normalized != "." and not posix.is_absolute() and not windows.drive
    assert not windows.is_absolute() and ".." not in posix.parts
    assert normalized == raw
    return normalized


def portable_path_key(raw: str) -> str:
    """Identity used for duplicate checks on supported case-insensitive filesystems."""
    return "/".join(part.casefold() for part in canonical_relative_path(raw).split("/"))


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def is_rfc3339_utc(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    match = RFC3339_UTC_SHAPE.fullmatch(value)
    if match is None or match.group("offset") not in {"Z", "z", "+00:00"}:
        return False
    year, month, day, hour, minute, second = (
        int(match.group(name)) for name in ("year", "month", "day", "hour", "minute", "second")
    )
    if second > 60:
        return False
    if second == 60 and not (hour == 23 and minute == 59 and (month, day) in {(6, 30), (12, 31)}):
        return False
    try:
        datetime(year, month, day, hour, minute, min(second, 59))
    except ValueError:
        return False
    return True


def canonical_z_instant(value: Any) -> datetime:
    assert isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value)
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


def rfc3339_utc_key(value: Any) -> tuple[int, int, int, int, int, int, str]:
    assert is_rfc3339_utc(value)
    match = RFC3339_UTC_SHAPE.fullmatch(value)
    assert match is not None
    numbers = tuple(int(match.group(name)) for name in ("year", "month", "day", "hour", "minute", "second"))
    fraction = (match.group("fraction") or "").rstrip("0")
    return (*numbers, fraction)


def normalized_proposal_path(raw: str) -> str:
    assert isinstance(raw, str)
    return canonical_relative_path(raw.replace("\\", "/"))


def deterministic_proposal_id(proposal: dict[str, Any]) -> str:
    payload = {key: copy.deepcopy(value) for key, value in proposal.items() if key != "proposal_id"}
    payload["input_hashes"] = [
        {"path": normalized_proposal_path(record["path"]), "sha256": record["sha256"]}
        for record in proposal["input_hashes"]
    ]
    payload["input_hashes"] = sorted(payload["input_hashes"], key=canonical_json)
    for field in ("affected_paths", "patch_scope"):
        payload[field] = sorted(normalized_proposal_path(path) for path in proposal[field])
    for field in ("baseline_refs", "evidence_refs", "required_gates", "required_reviewers"):
        payload[field] = sorted(proposal[field])
    return "proposal-" + hashlib.sha256(canonical_json(payload)).hexdigest()[:20]


def policy_content_hash(policy: dict[str, Any], evolution: dict[str, Any]) -> str:
    authorities = {item["authority_id"]: item for item in evolution["authorities"]}
    signals = {item["signal_id"]: item for item in evolution["signals"]}
    payload = {
        "policy": policy,
        "closer_authority": authorities[policy["closer_authority_ref"]],
        "required_signals": [signals[signal_id] for signal_id in sorted(policy["required_signals"])],
    }
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def decode_json_pointer_token(raw: str) -> str:
    assert not re.search(r"~(?![01])", raw)
    return raw.replace("~1", "/").replace("~0", "~")


def resolve_json_pointer(document: Any, pointer: str) -> Any:
    assert isinstance(pointer, str) and pointer.startswith("/")
    current = document
    for raw_part in pointer.split("/")[1:]:
        part = decode_json_pointer_token(raw_part)
        if isinstance(current, list):
            assert re.fullmatch(r"0|[1-9][0-9]*", part)
            index = int(part)
            assert index < len(current)
            current = current[index]
        else:
            assert isinstance(current, dict) and part in current
            current = current[part]
    return current


def validate_direct_argv(argv: Any) -> None:
    assert isinstance(argv, list) and argv
    assert all(isinstance(argument, str) and argument for argument in argv)
    executable = PureWindowsPath(argv[0]).name.casefold()
    assert executable not in SHELL_EXECUTABLES | INDIRECT_EXECUTORS
    assert not any(PureWindowsPath(argument).name.casefold() in SHELL_EXECUTABLES for argument in argv[1:])
    assert not any(argument.casefold() in COMMAND_STRING_FLAGS for argument in argv[1:])


def validate_mutation_guard(preview: dict[str, Any], immediate: dict[str, Any]) -> None:
    keys = {"root_identity", "parent_identities", "target_identity", "target_hash", "link_components"}
    exact_keys(preview, keys, "preview mutation identity")
    exact_keys(immediate, keys, "immediate mutation identity")
    assert preview == immediate
    assert not immediate["link_components"]


def expect_assertion(action: Any) -> None:
    try:
        action()
    except (AssertionError, IndexError, ValueError):
        return
    raise AssertionError("expected validation failure")


def validate_glob(pattern: str) -> None:
    assert pattern and "\\" not in pattern and not pattern.startswith("/")
    assert not any(unicodedata.category(char) == "Cc" for char in pattern)
    parts = pattern.split("/")
    assert all(part not in {"", ".", ".."} for part in parts)
    for index, part in enumerate(parts):
        if part == "**":
            assert index == len(parts) - 1
        else:
            assert "**" not in part and not any(char in part for char in "?[]{}")
            assert re.fullmatch(r"[A-Za-z0-9._*-]+", part)


def glob_matches(pattern: str, path: str) -> bool:
    validate_glob(pattern)
    pattern_parts = pattern.split("/")
    path_parts = canonical_relative_path(path).split("/")
    if pattern_parts[-1] == "**":
        prefix = pattern_parts[:-1]
        return len(path_parts) >= len(prefix) and all(
            fnmatchcase(path_part, pattern_part) for path_part, pattern_part in zip(path_parts, prefix)
        )
    return len(path_parts) == len(pattern_parts) and all(
        fnmatchcase(path_part, pattern_part)
        for path_part, pattern_part in zip(path_parts, pattern_parts)
    )


def resolve_governed_component(evolution: dict[str, Any], path: str) -> dict[str, Any]:
    canonical = canonical_relative_path(path)
    assert not any(
        canonical == exclusion["path"] or canonical.startswith(exclusion["path"] + "/")
        for exclusion in evolution["explicit_exclusions"]
    )
    roots = [
        root
        for root in evolution["governed_roots"]
        if canonical == root["path"] or canonical.startswith(root["path"] + "/")
    ]
    assert len(roots) == 1
    components = [
        component
        for component in evolution["component_classes"]
        if any(glob_matches(pattern, canonical) for pattern in component["path_globs"])
    ]
    assert len(components) == 1
    return components[0]


def validate_platform(platform: dict[str, Any]) -> None:
    exact_keys(
        platform,
        {
            "format_revision",
            "registry_revision",
            "release_version",
            "version_targets",
            "children",
            "canonical_revision",
            "green_revisions",
            "migratable_source_revisions",
            "unsupported_revisions",
            "revision_descriptors",
            "migration_edges",
        },
        "platform",
    )
    assert platform["format_revision"] == 1
    assert SEMVER.fullmatch(platform["release_version"])
    version_paths = []
    for target in platform["version_targets"]:
        exact_keys(target, {"path", "kind", "locator"}, f"version target {target}")
        version_paths.append(canonical_relative_path(target["path"]))
        assert target["kind"] == "json-pointer"
        assert target["locator"].startswith("/")
        for raw_part in target["locator"].split("/")[1:]:
            decode_json_pointer_token(raw_part)
    assert version_paths == sorted(version_paths)
    assert len(version_paths) == len({portable_path_key(path) for path in version_paths})
    assert platform["canonical_revision"] == "dat-kit 2.0"
    assert platform["green_revisions"] == ["dat-kit 2.0"]
    assert platform["migratable_source_revisions"] == ["dat-kit 1.16.0"]
    assert len(platform["children"]) == 3
    assert {child["kind"] for child in platform["children"]} == {
        "domains",
        "adapters",
        "evolution",
    }
    for child in platform["children"]:
        exact_keys(child, {"kind", "path", "revision"}, f"child {child}")
        canonical_relative_path(child["path"])
    descriptor_keys = {
        "revision",
        "marker_rules",
        "required_pointer_paths",
        "static_template_hashes",
        "snapshot_provenance",
        "support_removal_not_before",
    }
    revisions = set()
    for descriptor in platform["revision_descriptors"]:
        exact_keys(descriptor, descriptor_keys, f"revision {descriptor}")
        revisions.add(descriptor["revision"])
        for marker in descriptor["marker_rules"]:
            exact_keys(marker, {"path", "required_text"}, f"marker {marker}")
            canonical_relative_path(marker["path"])
        for path in descriptor["required_pointer_paths"]:
            canonical_relative_path(path)
    assert len(platform["revision_descriptors"]) == len(revisions)
    assert revisions == {"dat-kit 2.0", "dat-kit 1.16.0"}
    migration_ids: set[str] = set()
    for edge in platform["migration_edges"]:
        exact_keys(
            edge,
            {"migration_id", "source_revision", "target_revision", "status"},
            f"migration edge {edge}",
        )
        assert edge["source_revision"] in revisions and edge["target_revision"] in revisions
        assert edge["status"] in {"planned", "available", "retired"}
        assert edge["migration_id"] not in migration_ids
        migration_ids.add(edge["migration_id"])

    mirror_fixture = load("version-mirrors.example.json")
    exact_keys(mirror_fixture, {"documents"}, "version mirror fixture")
    assert set(mirror_fixture["documents"]) == set(version_paths)

    for target in platform["version_targets"]:
        actual = resolve_json_pointer(mirror_fixture["documents"][target["path"]], target["locator"])
        assert isinstance(actual, str) and actual == platform["release_version"]

    scaffold_header = (
        "# GENERATED FROM REGISTRY — DO NOT EDIT; "
        f"source_revision={platform['registry_revision']}"
    )
    assert scaffold_header.endswith("source_revision=platform/1")


def validate_domains(domains: dict[str, Any]) -> None:
    exact_keys(domains, {"format_revision", "registry_revision", "contract_revision", "domains"}, "domains")
    assert domains["format_revision"] == 1
    descriptor_keys = {
        "domain_id",
        "contract_revision",
        "lifecycle",
        "pack_location",
        "trigger",
        "required_engine_revision",
        "gate_authority_ref",
        "loop_ceiling",
        "evolution_profile_ref",
    }
    trigger_namespace: set[str] = set()
    ids: set[str] = set()
    for descriptor in domains["domains"]:
        exact_keys(descriptor, descriptor_keys, f"domain {descriptor}")
        exact_keys(descriptor["trigger"], {"name", "description", "aliases"}, "trigger")
        assert descriptor["domain_id"] not in ids
        ids.add(descriptor["domain_id"])
        # re-derived at the Phase 4 cutover (4f): both example rows mirror the
        # post-cutover registry state — active six-slot packs under domains/
        assert descriptor["lifecycle"] == "active"
        assert descriptor["pack_location"] == f"domains/{descriptor['domain_id']}"
        assert descriptor["loop_ceiling"] in {"Turn", "Goal", "Time", "Proactive"}
        canonical_relative_path(descriptor["pack_location"])
        canonical_relative_path(f"skills/{descriptor['trigger']['name']}/SKILL.md")
        trigger_name = descriptor["trigger"]["name"].strip().casefold()
        assert trigger_name and trigger_name not in trigger_namespace
        trigger_namespace.add(trigger_name)
        for alias in descriptor["trigger"]["aliases"]:
            normalized = alias.strip().casefold()
            assert normalized and normalized not in trigger_namespace
            trigger_namespace.add(normalized)
    assert ids == {"software-dev", "knowledge-work"}
    destinations = [f"skills/{item['trigger']['name']}/SKILL.md" for item in domains["domains"]]
    assert len(destinations) == len(set(destinations))


def validate_adapters(adapters: dict[str, Any]) -> None:
    exact_keys(adapters, {"format_revision", "registry_revision", "contract_revision", "adapters"}, "adapters")
    assert adapters["format_revision"] == 1
    descriptor_keys = {
        "adapter_id",
        "aliases",
        "contract_revision",
        "host",
        "lifecycle",
        "official_facts",
        "plugin_root_rules",
        "repository_artifact_paths",
        "project_artifacts",
        "pointer_semantics",
        "policy_prohibition",
        "capability_assumptions",
        "conformance_fixtures",
        "smoke_command",
        "migration_fixture_refs",
        "rollback",
    }
    artifact_keys = {
        "source_template",
        "target_relative_path",
        "ownership_class",
        "materialization_action",
        "artifact_lifecycle",
        "project_contract_revision",
        "expected_content_hash",
        "precondition",
    }
    fact_keys = {"fact_id", "verified_on", "source_url", "claim", "scope", "reverify_before"}
    aliases: set[str] = set()
    adapter_ids: set[str] = set()
    for descriptor in adapters["adapters"]:
        exact_keys(descriptor, descriptor_keys, f"adapter {descriptor}")
        assert descriptor["lifecycle"] == "repo_only"
        assert descriptor["adapter_id"] not in adapter_ids
        adapter_ids.add(descriptor["adapter_id"])
        for alias in descriptor["aliases"]:
            normalized = alias.strip().casefold()
            assert normalized and normalized not in aliases
            aliases.add(normalized)
        exact_keys(
            descriptor["plugin_root_rules"],
            {"manifest_paths", "skill_roots", "containment_root", "fresh_session_required"},
            "plugin_root_rules",
        )
        assert descriptor["plugin_root_rules"]["containment_root"] in {"plugin-root", "extension-root"}
        assert descriptor["plugin_root_rules"]["fresh_session_required"] is True
        for path in descriptor["plugin_root_rules"]["manifest_paths"] + descriptor["plugin_root_rules"]["skill_roots"]:
            canonical_relative_path(path)
        for path in descriptor["repository_artifact_paths"]:
            canonical_relative_path(path)
        for fact in descriptor["official_facts"]:
            exact_keys(fact, fact_keys, f"host fact {fact}")
            assert fact["source_url"].startswith("https://")
            assert all(isinstance(fact[field], str) and fact[field].strip() for field in fact_keys)
            assert len(fact["verified_on"]) == 10 and date.fromisoformat(fact["verified_on"]).isoformat() == fact["verified_on"]
        for artifact in descriptor["project_artifacts"]:
            exact_keys(artifact, artifact_keys, f"artifact {artifact}")
            canonical_relative_path(artifact["source_template"])
            canonical_relative_path(artifact["target_relative_path"])
            assert artifact["artifact_lifecycle"] == "repo_only"
            assert artifact["materialization_action"] in MATERIALIZATION_ACTIONS
            assert artifact["precondition"] in PRECONDITIONS
            assert artifact["precondition"] in ACTION_PRECONDITIONS[artifact["materialization_action"]]
            if artifact["source_template"].startswith(f"adapters/{descriptor['adapter_id']}/"):
                assert artifact["source_template"] in descriptor["repository_artifact_paths"]
        exact_keys(
            descriptor["pointer_semantics"],
            {"canonical_target", "mechanism", "missing_target_behavior"},
            "pointer_semantics",
        )
        assert descriptor["pointer_semantics"]["canonical_target"] == "AGENTS.md"
        assert descriptor["pointer_semantics"]["missing_target_behavior"] in {
            "clear-failure",
            "documented-degradation",
        }
        exact_keys(
            descriptor["policy_prohibition"],
            {"canonical_owner", "forbidden_categories"},
            "policy_prohibition",
        )
        assert descriptor["policy_prohibition"]["canonical_owner"] == "AGENTS.md"
        assert set(descriptor["policy_prohibition"]["forbidden_categories"]) == {
            "canonical-policy",
            "engine-policy",
            "domain-policy",
            "governance-authority",
        }
        fact_id_list = [fact["fact_id"] for fact in descriptor["official_facts"]]
        assert len(fact_id_list) == len(set(fact_id_list))
        fact_ids = set(fact_id_list)
        for assumption in descriptor["capability_assumptions"]:
            exact_keys(assumption, {"assumption_id", "claim", "fact_ref", "required_for"}, "capability")
            assert assumption["fact_ref"] in fact_ids
        validate_direct_argv(descriptor["smoke_command"])
        for argument in descriptor["smoke_command"]:
            placeholders = re.findall(r"\{[^{}]+\}", argument)
            assert set(placeholders) <= {"{plugin_root}", "{project_root}"}
        exact_keys(
            descriptor["rollback"],
            {"owned_repository_paths", "owned_project_paths", "removal_precondition", "verification_commands"},
            "rollback",
        )
        assert descriptor["rollback"]["removal_precondition"] == "exact-adapter-owned-hash"
        for path in descriptor["rollback"]["owned_repository_paths"] + descriptor["rollback"]["owned_project_paths"]:
            canonical_relative_path(path)
        assert set(descriptor["repository_artifact_paths"]) <= set(
            descriptor["rollback"]["owned_repository_paths"]
        )
        assert descriptor["rollback"]["verification_commands"]
        assert isinstance(descriptor["rollback"]["verification_commands"], list)
        for command in descriptor["rollback"]["verification_commands"]:
            validate_direct_argv(command)


def validate_file_plan() -> None:
    plan = load("file-plan.example.json")
    exact_keys(plan, {"mode", "entries"}, "file plan")
    assert plan["mode"] in {"greenfield", "add-missing", "inspect-brownfield", "migrate-approved"}
    entry_keys = {
        "source_template", "target_relative_path", "ownership_class", "materialization_action",
        "artifact_lifecycle", "project_contract_revision", "expected_content_hash", "precondition",
    }
    targets: list[str] = []
    manifest_rows = []
    materialized_rows = []
    for entry in plan["entries"]:
        exact_keys(entry, entry_keys, f"file plan entry {entry}")
        canonical_relative_path(entry["source_template"])
        targets.append(canonical_relative_path(entry["target_relative_path"]))
        assert entry["ownership_class"] in {"dat-kit", "adapter", "user"}
        assert entry["materialization_action"] in MATERIALIZATION_ACTIONS
        assert entry["precondition"] in PRECONDITIONS
        assert entry["precondition"] in ACTION_PRECONDITIONS[entry["materialization_action"]]
        assert entry["artifact_lifecycle"] in {"repo_only", "migration_ready", "scaffold_active", "retired"}
        if entry["expected_content_hash"] is not None:
            assert HEX64.fullmatch(entry["expected_content_hash"])
        if entry["materialization_action"] in {"copy", "RETIRE_LEGACY"}:
            assert HEX64.fullmatch(entry["expected_content_hash"])
        if entry["materialization_action"] == "RETIRE_LEGACY":
            assert entry["artifact_lifecycle"] == "retired"
        if entry["materialization_action"] == "preserve":
            assert entry["ownership_class"] == "user"
        if entry["precondition"] == "target-exact-expected-hash":
            assert HEX64.fullmatch(entry["expected_content_hash"])
        if entry["precondition"] == "target-absent":
            manifest_rows.append(
                (
                    entry["source_template"],
                    entry["target_relative_path"],
                    entry["ownership_class"],
                    entry["materialization_action"],
                    entry["project_contract_revision"],
                    entry["artifact_lifecycle"],
                )
            )
            if entry["artifact_lifecycle"] == "scaffold_active":
                materialized_rows.append(entry["target_relative_path"])
    assert targets == sorted(targets)
    assert len(targets) == len({portable_path_key(target) for target in targets})
    assert manifest_rows == [
        (
            "templates/common/AGENTS.md", "AGENTS.md", "dat-kit", "copy", "dat-kit 2.0", "scaffold_active"
        ),
        (
            "adapters/gemini-cli/GEMINI.md.tpl", "GEMINI.md", "adapter", "render-pointer", "dat-kit 2.0", "repo_only"
        ),
    ]
    assert materialized_rows == ["AGENTS.md"]


def validate_evolution(evolution: dict[str, Any], domains: dict[str, Any]) -> None:
    exact_keys(
        evolution,
        {
            "format_revision",
            "registry_revision",
            "contract_revision",
            "governed_roots",
            "explicit_exclusions",
            "component_classes",
            "signals",
            "authorities",
            "policies",
        },
        "evolution",
    )
    assert evolution["format_revision"] == 1
    for root in evolution["governed_roots"]:
        exact_keys(root, {"path", "owner"}, f"governed root {root}")
        canonical_relative_path(root["path"])
    assert len({portable_path_key(root["path"]) for root in evolution["governed_roots"]}) == len(
        evolution["governed_roots"]
    )
    for exclusion in evolution["explicit_exclusions"]:
        exact_keys(exclusion, {"path", "reason", "owner"}, f"exclusion {exclusion}")
        canonical_relative_path(exclusion["path"])
    assert len({portable_path_key(item["path"]) for item in evolution["explicit_exclusions"]}) == len(
        evolution["explicit_exclusions"]
    )
    component_keys = {"component_id", "path_globs", "owner", "governance_class", "policy_ref"}
    component_ids: list[str] = []
    for component in evolution["component_classes"]:
        exact_keys(component, component_keys, f"component {component}")
        component_ids.append(component["component_id"])
        assert component["governance_class"] in {"A", "B", "C"}
        for pattern in component["path_globs"]:
            validate_glob(pattern)
    assert len(component_ids) == len(set(component_ids))
    signal_keys = {
        "signal_id",
        "status",
        "producer",
        "artifact_or_schema_revision",
        "quality_limitations",
        "retention",
    }
    signal_ids: list[str] = []
    for signal in evolution["signals"]:
        exact_keys(signal, signal_keys, f"signal {signal}")
        signal_ids.append(signal["signal_id"])
        assert signal["status"] in {"active", "proxy", "planned"}
    assert len(signal_ids) == len(set(signal_ids))
    authority_keys = {
        "authority_id",
        "role_type",
        "allowed_decision_classes",
        "allowed_closer",
        "appointments",
        "succession_rule",
        "approval_evidence_contract",
        "revocation_rule",
    }
    authority_ids_list = [authority["authority_id"] for authority in evolution["authorities"]]
    assert len(authority_ids_list) == len(set(authority_ids_list))
    authorities = {authority["authority_id"]: authority for authority in evolution["authorities"]}
    appointment_ids: set[str] = set()
    for authority in authorities.values():
        exact_keys(authority, authority_keys, f"authority {authority}")
        assert authority["appointments"]
        for appointment in authority["appointments"]:
            exact_keys(
                appointment,
                {
                    "appointment_id", "identity", "role", "effective_from", "revoked_at",
                    "successor_of", "evidence_ref", "evidence_hash",
                },
                f"appointment {appointment}",
            )
            assert appointment["appointment_id"] not in appointment_ids
            appointment_ids.add(appointment["appointment_id"])
            assert appointment["role"] == authority["authority_id"]
            for field in ("appointment_id", "identity", "role", "evidence_ref"):
                assert isinstance(appointment[field], str) and appointment[field].strip()
            effective = canonical_z_instant(appointment["effective_from"])
            if appointment["revoked_at"] is not None:
                assert canonical_z_instant(appointment["revoked_at"]) > effective
            assert appointment["successor_of"] is None or isinstance(appointment["successor_of"], str)
            assert HEX64.fullmatch(appointment["evidence_hash"])
    for authority in authorities.values():
        authority_appointments = {
            appointment["appointment_id"]: appointment for appointment in authority["appointments"]
        }
        predecessor_ids: list[str] = []
        for appointment in authority["appointments"]:
            if appointment["successor_of"] is not None:
                assert appointment["successor_of"] in authority_appointments
                predecessor = authority_appointments[appointment["successor_of"]]
                assert canonical_z_instant(appointment["effective_from"]) > canonical_z_instant(
                    predecessor["effective_from"]
                )
                predecessor_ids.append(appointment["successor_of"])
        assert len(predecessor_ids) == len(set(predecessor_ids))
    policy_keys = {
        "policy_id",
        "revision",
        "owner",
        "allowed_classes",
        "required_signals",
        "required_gates",
        "required_reviewers",
        "closer_authority_ref",
        "rollback_evidence",
    }
    signals = {signal["signal_id"]: signal for signal in evolution["signals"]}
    policy_ids_list = [policy["policy_id"] for policy in evolution["policies"]]
    assert len(policy_ids_list) == len(set(policy_ids_list))
    policies = {policy["policy_id"]: policy for policy in evolution["policies"]}
    for policy in policies.values():
        exact_keys(policy, policy_keys, f"policy {policy}")
        assert policy["closer_authority_ref"] in authorities
        assert set(policy["required_signals"]) <= set(signals)
        assert all(signals[signal_id]["status"] in {"active", "proxy"} for signal_id in policy["required_signals"])
        assert set(policy["allowed_classes"]) <= set(
            authorities[policy["closer_authority_ref"]]["allowed_decision_classes"]
        )
    for component in evolution["component_classes"]:
        assert component["policy_ref"] in policies
        assert policies[component["policy_ref"]]["owner"] == component["owner"]
    for domain in domains["domains"]:
        assert domain["gate_authority_ref"] in authorities
        assert domain["evolution_profile_ref"] in policies
    roots = evolution["governed_roots"]
    exclusions = evolution["explicit_exclusions"]
    for index, root in enumerate(roots):
        for other in roots[index + 1 :]:
            assert not root["path"].startswith(other["path"] + "/")
            assert not other["path"].startswith(root["path"] + "/")
    for exclusion in exclusions:
        matching_roots = [
            root
            for root in roots
            if exclusion["path"] == root["path"] or exclusion["path"].startswith(root["path"] + "/")
        ]
        assert len(matching_roots) <= 1
        if matching_roots:
            assert exclusion["owner"] == matching_roots[0]["owner"]
    for index, exclusion in enumerate(exclusions):
        for other in exclusions[index + 1 :]:
            assert not exclusion["path"].startswith(other["path"] + "/")
            assert not other["path"].startswith(exclusion["path"] + "/")

    def explain(path: str) -> str:
        canonical = canonical_relative_path(path)
        matched_exclusions = [
            exclusion
            for exclusion in exclusions
            if canonical == exclusion["path"] or canonical.startswith(exclusion["path"] + "/")
        ]
        if matched_exclusions:
            assert len(matched_exclusions) == 1
            return "excluded"
        matched_roots = [
            root for root in roots if canonical == root["path"] or canonical.startswith(root["path"] + "/")
        ]
        if not matched_roots:
            return "orphan"
        assert len(matched_roots) == 1
        matched_components = [
            component
            for component in evolution["component_classes"]
            if any(glob_matches(pattern, canonical) for pattern in component["path_globs"])
        ]
        if not matched_components:
            return "orphan"
        assert len(matched_components) == 1
        return matched_components[0]["component_id"]

    assert explain("domains/software-dev/gates.md") == "software-dev"
    assert explain("scripts/registry.py") == "maintainer-scripts"
    assert explain("scripts/tests/test_registry.py") == "maintainer-scripts"
    assert explain("scripts/spikes/phase1a/probe.py") == "excluded"
    assert explain("scripts/other/file.txt") == "orphan"
    assert explain("README.md") == "excluded"
    assert explain("brand-new/file.md") == "orphan"

    declared_product_paths: set[str] = set()
    platform = load("platform.example.json")
    adapters = load("adapters.example.json")
    file_plan = load("file-plan.example.json")
    declared_product_paths.update(target["path"] for target in platform["version_targets"])
    for domain in domains["domains"]:
        declared_product_paths.add(domain["pack_location"])
        declared_product_paths.add(f"skills/{domain['trigger']['name']}/SKILL.md")
    for adapter in adapters["adapters"]:
        declared_product_paths.update(adapter["repository_artifact_paths"])
        declared_product_paths.update(adapter["rollback"]["owned_repository_paths"])
        declared_product_paths.update(artifact["source_template"] for artifact in adapter["project_artifacts"])
    declared_product_paths.update(entry["source_template"] for entry in file_plan["entries"])
    declared_product_paths.update(
        {
            "docs/contracts/registry.md",
            "docs/decisions/evolution-proposal-example.proposal.json",
        }
    )
    for path in sorted(declared_product_paths):
        assert explain(path) not in {"orphan", "excluded"}, f"declared product path is ungoverned: {path}"


def validate_proposal_record(proposal: dict[str, Any], evolution: dict[str, Any]) -> None:
    proposal_keys = {
        "format_revision", "proposal_id", "created_at", "proposer_identity", "policy_revision",
        "policy_hash", "governed_owner", "governance_class", "evidence_window", "input_hashes",
        "affected_paths", "baseline_refs", "evidence_refs", "hypothesis", "patch_scope",
        "required_gates", "required_reviewers", "closer_authority_ref", "observation_window",
        "rollback_condition",
    }
    exact_keys(proposal, proposal_keys, "proposal")
    assert proposal["format_revision"] == 1 and is_rfc3339_utc(proposal["created_at"])
    assert proposal["governance_class"] in {"A", "B", "C"} and HEX64.fullmatch(proposal["policy_hash"])
    for field in (
        "proposer_identity", "governed_owner", "hypothesis", "closer_authority_ref", "rollback_condition"
    ):
        assert isinstance(proposal[field], str) and proposal[field].strip()
    for window_name in ("evidence_window", "observation_window"):
        exact_keys(proposal[window_name], {"start", "end"}, window_name)
        assert is_rfc3339_utc(proposal[window_name]["start"])
        assert is_rfc3339_utc(proposal[window_name]["end"])
        assert rfc3339_utc_key(proposal[window_name]["start"]) < rfc3339_utc_key(
            proposal[window_name]["end"]
        )
    for record in proposal["input_hashes"]:
        exact_keys(record, {"path", "sha256"}, f"input hash {record}")
        canonical_relative_path(record["path"])
        assert HEX64.fullmatch(record["sha256"])
    assert proposal["input_hashes"] == sorted(proposal["input_hashes"], key=canonical_json)
    assert len({portable_path_key(record["path"]) for record in proposal["input_hashes"]}) == len(
        proposal["input_hashes"]
    )
    for field in ("affected_paths", "patch_scope"):
        assert proposal[field]
        assert proposal[field] == sorted(set(proposal[field]))
        for path in proposal[field]:
            canonical_relative_path(path)
        assert len(proposal[field]) == len({portable_path_key(path) for path in proposal[field]})
    assert set(proposal["patch_scope"]) <= set(proposal["affected_paths"])
    for field in ("baseline_refs", "evidence_refs", "required_gates", "required_reviewers"):
        assert proposal[field]
        assert proposal[field] == sorted(set(proposal[field]))
    expected_id = deterministic_proposal_id(proposal)
    assert proposal["proposal_id"] == expected_id
    windows_reordered = dict(proposal)
    windows_reordered["input_hashes"] = [
        {"path": item["path"].replace("/", "\\"), "sha256": item["sha256"]}
        for item in reversed(proposal["input_hashes"])
    ]
    assert deterministic_proposal_id(windows_reordered) == expected_id
    changed = dict(proposal)
    changed["policy_hash"] = "d" * 64
    assert deterministic_proposal_id(changed) != expected_id

    components = [
        resolve_governed_component(evolution, path)
        for path in sorted(set(proposal["affected_paths"] + proposal["patch_scope"]))
    ]
    assert len({component["policy_ref"] for component in components}) == 1
    assert len({component["owner"] for component in components}) == 1
    policy_ref = components[0]["policy_ref"]
    policies = {policy["policy_id"]: policy for policy in evolution["policies"]}
    authorities = {authority["authority_id"]: authority for authority in evolution["authorities"]}
    policy = policies[policy_ref]
    class_rank = {"A": 1, "B": 2, "C": 3}
    required_class = max((component["governance_class"] for component in components), key=class_rank.__getitem__)
    assert proposal["governed_owner"] == components[0]["owner"] == policy["owner"]
    assert proposal["governance_class"] == required_class
    assert required_class in policy["allowed_classes"]
    assert proposal["policy_revision"] == policy["revision"]
    assert proposal["policy_hash"] == policy_content_hash(policy, evolution)
    assert proposal["required_gates"] == sorted(policy["required_gates"])
    assert proposal["required_reviewers"] == sorted(policy["required_reviewers"])
    assert proposal["closer_authority_ref"] == policy["closer_authority_ref"]
    authority = authorities[proposal["closer_authority_ref"]]
    assert required_class in authority["allowed_decision_classes"]


def resolve_authorized_appointment(
    decision: dict[str, Any], proposal: dict[str, Any], evolution: dict[str, Any]
) -> dict[str, Any]:
    authority = next(
        item for item in evolution["authorities"] if item["authority_id"] == proposal["closer_authority_ref"]
    )
    matches = [
        appointment
        for appointment in authority["appointments"]
        if decision["approval_reference"] == f"{appointment['appointment_id']}#{proposal['proposal_id']}"
        and decision["closer_identity"] == appointment["identity"]
        and decision["closer_role"] == appointment["role"]
    ]
    assert len(matches) == 1
    appointment = matches[0]
    decided_at = canonical_z_instant(decision["decided_at"])
    assert decided_at >= canonical_z_instant(appointment["effective_from"])
    assert appointment["revoked_at"] is None or decided_at < canonical_z_instant(appointment["revoked_at"])
    assert not any(
        candidate["successor_of"] == appointment["appointment_id"]
        and canonical_z_instant(candidate["effective_from"]) <= decided_at
        for candidate in authority["appointments"]
    )
    return appointment


def validate_decision_record(
    decision: dict[str, Any], proposal: dict[str, Any], evolution: dict[str, Any]
) -> None:
    decision_keys = {
        "format_revision", "decision_id", "proposal_id", "decision", "decided_at",
        "policy_revision", "policy_hash", "closer_identity", "closer_role", "approval_reference",
        "gate_evidence_refs", "effective_from_run", "observation_status", "correction_of",
    }
    exact_keys(decision, decision_keys, "decision")
    assert decision["proposal_id"] == proposal["proposal_id"]
    assert decision["decision_id"] == f"decision-{proposal['proposal_id'].removeprefix('proposal-')}-0001"
    assert decision["decision"] == "approved" and decision["observation_status"] == "observing"
    assert decision["effective_from_run"] and decision["correction_of"] is None
    assert decision["policy_revision"] == proposal["policy_revision"]
    assert decision["policy_hash"] == proposal["policy_hash"]
    assert is_rfc3339_utc(decision["decided_at"])
    assert decision["closer_identity"] != proposal["proposer_identity"]
    assert decision["closer_role"] == proposal["closer_authority_ref"]
    authority = next(
        item for item in evolution["authorities"] if item["authority_id"] == decision["closer_role"]
    )
    assert proposal["governance_class"] in authority["allowed_decision_classes"]
    resolve_authorized_appointment(decision, proposal, evolution)
    assert decision["gate_evidence_refs"] == sorted(set(decision["gate_evidence_refs"]))
    assert len(decision["gate_evidence_refs"]) == len(proposal["required_gates"])
    assert all(
        evidence_ref.startswith(f"gate/{gate_id}-")
        for gate_id, evidence_ref in zip(proposal["required_gates"], decision["gate_evidence_refs"])
    )


def validate_proposal_and_decision(evolution: dict[str, Any]) -> None:
    proposal = load("proposal.example.json")
    decision = load("decision-record.example.json")
    validate_proposal_record(proposal, evolution)
    validate_decision_record(decision, proposal, evolution)

    def mutated_proposal(**changes: Any) -> dict[str, Any]:
        result = copy.deepcopy(proposal)
        result.update(changes)
        result["proposal_id"] = deterministic_proposal_id(result)
        return result

    expect_assertion(
        lambda: validate_proposal_record(
            mutated_proposal(
                affected_paths=["docs/contracts/registry.md"],
                patch_scope=["docs/contracts/registry.md"],
            ),
            evolution,
        )
    )
    expect_assertion(lambda: validate_proposal_record(mutated_proposal(governance_class="A"), evolution))
    expect_assertion(lambda: validate_proposal_record(mutated_proposal(required_gates=["bogus-gate"]), evolution))
    expect_assertion(lambda: validate_proposal_record(mutated_proposal(policy_hash="d" * 64), evolution))
    reversed_evidence = copy.deepcopy(proposal["evidence_window"])
    reversed_evidence["start"], reversed_evidence["end"] = reversed_evidence["end"], reversed_evidence["start"]
    expect_assertion(
        lambda: validate_proposal_record(mutated_proposal(evidence_window=reversed_evidence), evolution)
    )
    reversed_observation = copy.deepcopy(proposal["observation_window"])
    reversed_observation["start"], reversed_observation["end"] = (
        reversed_observation["end"], reversed_observation["start"]
    )
    expect_assertion(
        lambda: validate_proposal_record(mutated_proposal(observation_window=reversed_observation), evolution)
    )
    colliding_hashes = copy.deepcopy(proposal["input_hashes"])
    colliding_hashes.append({"path": "Benchmarks/defects.jsonl", "sha256": "e" * 64})
    colliding_hashes.sort(key=canonical_json)
    expect_assertion(
        lambda: validate_proposal_record(mutated_proposal(input_hashes=colliding_hashes), evolution)
    )
    changed_appointment_evolution = copy.deepcopy(evolution)
    changed_appointment_evolution["authorities"][0]["appointments"][0]["evidence_hash"] = "f" * 64
    policy = next(item for item in evolution["policies"] if item["policy_id"] == "software-dev-policy")
    changed_policy = next(
        item for item in changed_appointment_evolution["policies"] if item["policy_id"] == "software-dev-policy"
    )
    assert policy_content_hash(policy, evolution) != policy_content_hash(
        changed_policy, changed_appointment_evolution
    )
    expect_assertion(lambda: validate_proposal_record(proposal, changed_appointment_evolution))
    self_closed = copy.deepcopy(decision)
    self_closed["closer_identity"] = proposal["proposer_identity"]
    expect_assertion(lambda: validate_decision_record(self_closed, proposal, evolution))
    unauthorized = copy.deepcopy(decision)
    unauthorized["closer_identity"] = "totally-unauthorized"
    unauthorized["approval_reference"] = f"appointment/fabricated#{proposal['proposal_id']}"
    expect_assertion(lambda: validate_decision_record(unauthorized, proposal, evolution))
    blank_reference = copy.deepcopy(decision)
    blank_reference["approval_reference"] = ""
    expect_assertion(lambda: validate_decision_record(blank_reference, proposal, evolution))

    revoked_evolution = copy.deepcopy(evolution)
    revoked = revoked_evolution["authorities"][0]["appointments"][0]
    revoked["revoked_at"] = decision["decided_at"]
    expect_assertion(lambda: resolve_authorized_appointment(decision, proposal, revoked_evolution))
    future_evolution = copy.deepcopy(evolution)
    future_evolution["authorities"][0]["appointments"][0]["effective_from"] = "2026-07-19T00:00:00Z"
    expect_assertion(lambda: resolve_authorized_appointment(decision, proposal, future_evolution))

    successor_evolution = copy.deepcopy(evolution)
    old_appointment = successor_evolution["authorities"][0]["appointments"][0]
    old_appointment["revoked_at"] = decision["decided_at"]
    successor = {
        "appointment_id": "appointment/software-dev-reviewer-2",
        "identity": "independent-reviewer-2",
        "role": "software-dev-reviewer",
        "effective_from": decision["decided_at"],
        "revoked_at": None,
        "successor_of": old_appointment["appointment_id"],
        "evidence_ref": "authority/software-dev-reviewer-appointment-2",
        "evidence_hash": "4" * 64,
    }
    successor_evolution["authorities"][0]["appointments"].append(successor)
    expect_assertion(lambda: resolve_authorized_appointment(decision, proposal, successor_evolution))
    successor_decision = copy.deepcopy(decision)
    successor_decision["closer_identity"] = successor["identity"]
    successor_decision["approval_reference"] = f"{successor['appointment_id']}#{proposal['proposal_id']}"
    resolve_authorized_appointment(successor_decision, proposal, successor_evolution)
    unrevoked_predecessor = copy.deepcopy(successor_evolution)
    unrevoked_predecessor["authorities"][0]["appointments"][0]["revoked_at"] = None
    expect_assertion(lambda: resolve_authorized_appointment(decision, proposal, unrevoked_predecessor))


def validate_cross_file_revisions(
    platform: dict[str, Any], domains: dict[str, Any], adapters: dict[str, Any], evolution: dict[str, Any]
) -> None:
    children = {child["kind"]: child["revision"] for child in platform["children"]}
    assert children == {
        "domains": domains["registry_revision"],
        "adapters": adapters["registry_revision"],
        "evolution": evolution["registry_revision"],
    }


def validate_normative_prose() -> None:
    requirements = {
        "registry.md": ["## R1.", "## R10.", "REGISTRY_FORMAT_UNSUPPORTED", "CONTRACT_MIGRATION_REQUIRED"],
        "domain-pack.md": ["## DP1.", "## DP9.", "workflow", "loop_profile", "DOMAIN_SLOT_MISSING"],
        "host-adapter.md": ["## HA1.", "## HA10.", "repo_only → migration_ready → scaffold_active → retired"],
        "evolution.md": ["## EV1.", "## EV10.", "EVOLUTION_ORPHAN_PATH", "Class C"],
    }
    for name, markers in requirements.items():
        text = (ROOT / "docs" / "contracts" / name).read_text(encoding="utf-8")
        for marker in markers:
            assert marker in text, f"{name}: missing normative marker {marker!r}"


def main() -> int:
    assert is_rfc3339_utc("2026-07-18T00:00:00.123Z")
    assert is_rfc3339_utc("2026-07-18t12:00:00z")
    assert is_rfc3339_utc("2026-07-18T12:00:00+00:00")
    assert is_rfc3339_utc("2026-06-30T23:59:60Z")
    assert not is_rfc3339_utc("2026-99-99T99:99:99Z")
    assert not is_rfc3339_utc("2026-07-18T12:00Z")
    assert not is_rfc3339_utc("2026-W29-6T12:00:00Z")
    assert not is_rfc3339_utc("2026-07-18T12:00:00-00:00")
    assert not is_rfc3339_utc("2026-07-18T12:00:00+01:00")
    assert SEMVER.fullmatch("1.0.0-alpha.1+build.5")
    assert not SEMVER.fullmatch("1.0.0-01")
    assert not SEMVER.fullmatch("1.0.0-..")
    for unsafe_path in (
        "docs//contracts", "./docs", "AGENTS.md:payload", "CON", "nul.txt",
        "docs/trailing.", "docs/trailing ", "docs\\contracts", "docs/../registry",
    ):
        expect_assertion(lambda path=unsafe_path: canonical_relative_path(path))
    assert portable_path_key("Docs/Contracts.md") == portable_path_key("docs/contracts.md")
    pointer_document = {"plugins": [{"version": "2.0.0-dev"}], "a/b": {"~key": "ok"}}
    assert resolve_json_pointer(pointer_document, "/plugins/0/version") == "2.0.0-dev"
    assert resolve_json_pointer(pointer_document, "/a~1b/~0key") == "ok"
    for invalid_pointer in ("plugins/0", "/plugins/00/version", "/plugins/٠/version", "/plugins/2", "/plugins/0~2"):
        expect_assertion(lambda pointer=invalid_pointer: resolve_json_pointer(pointer_document, pointer))
    expect_assertion(lambda: resolve_json_pointer(pointer_document, "/plugins/0/version/more"))
    expect_assertion(lambda: validate_direct_argv(["sh", "-c", "printf injected"]))
    expect_assertion(lambda: validate_direct_argv(["powershell.exe", "-Command", "Write-Output injected"]))
    expect_assertion(lambda: validate_direct_argv(["env", "bash", "script.sh"]))
    preview_identity = {
        "root_identity": "root-file-id-1",
        "parent_identities": ["parent-file-id-1"],
        "target_identity": "target-file-id-1",
        "target_hash": "a" * 64,
        "link_components": [],
    }
    validate_mutation_guard(preview_identity, copy.deepcopy(preview_identity))
    link_swap = copy.deepcopy(preview_identity)
    link_swap["link_components"] = ["reparse:target"]
    expect_assertion(lambda: validate_mutation_guard(preview_identity, link_swap))
    parent_swap = copy.deepcopy(preview_identity)
    parent_swap["parent_identities"] = ["parent-file-id-2"]
    expect_assertion(lambda: validate_mutation_guard(preview_identity, parent_swap))
    platform = load("platform.example.json")
    domains = load("domains.example.json")
    adapters = load("adapters.example.json")
    evolution = load("evolution.example.json")
    validate_platform(platform)
    validate_domains(domains)
    validate_adapters(adapters)
    validate_file_plan()
    validate_evolution(evolution, domains)
    validate_proposal_and_decision(evolution)
    validate_cross_file_revisions(platform, domains, adapters, evolution)
    validate_normative_prose()
    print("PHASE1A_CONTRACT_EXAMPLES_OK files=8 format_revision=1 domains=2 adapters=2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
