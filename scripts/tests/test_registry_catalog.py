import copy
import json
from pathlib import Path
import shutil
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from registry import Catalog, Diagnostic, canonical_relative_path


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_file(source: Path, root: Path) -> None:
    relative = source.relative_to(ROOT)
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def registry_fixture(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "registry", tmp_path / "registry")
    platform = json.loads((ROOT / "registry/platform.json").read_text(encoding="utf-8"))
    adapters = json.loads((ROOT / "registry/adapters.json").read_text(encoding="utf-8"))
    snapshot = json.loads(
        (ROOT / "registry/snapshots/project-contract-1.16.json").read_text(encoding="utf-8")
    )
    paths = {item["path"] for item in platform["version_targets"]}
    for adapter in adapters["adapters"]:
        paths.update(adapter["repository_artifact_paths"])
        paths.update(item["source_template"] for item in adapter["project_artifacts"])
    paths.update(item["source_template"] for item in snapshot["files"])
    for relative in sorted(paths):
        copy_file(ROOT / relative, tmp_path)
    # Active Domain Packs: Catalog.load fails closed (DOMAIN_SLOT_MISSING)
    # unless every declared slot exists under pack_location, so the fixture
    # must carry each active pack's slot tree alongside the registry. The
    # location is validated before touching the filesystem — raw registry
    # data must never drive a copy outside ROOT/tmp_path, even in tests.
    domains = json.loads((ROOT / "registry/domains.json").read_text(encoding="utf-8"))
    for descriptor in domains["domains"]:
        if descriptor["lifecycle"] == "active":
            location = canonical_relative_path(descriptor["pack_location"])
            shutil.copytree(ROOT / location, tmp_path / location)
    return tmp_path


def load_ok(root: Path) -> Catalog:
    loaded = Catalog.load(root)
    assert isinstance(loaded, Catalog), loaded
    return loaded


def codes(result: object) -> list[str]:
    assert isinstance(result, tuple)
    return [item.code for item in result]


def test_current_catalog_is_atomic_and_cutover_state_matches_plan():
    catalog = load_ok(ROOT)
    assert [item["domain_id"] for item in catalog.domains()] == ["knowledge-work", "software-dev"]
    # Phase 4 cutover state: software-dev cut over in slice 4c;
    # knowledge-work cut over in slice 4d.
    assert {item["domain_id"]: item["lifecycle"] for item in catalog.domains()} == {
        "knowledge-work": "active",
        "software-dev": "active",
    }
    assert catalog.release_version == "1.17.1"
    assert [item.path for item in catalog.version_targets()] == [
        ".claude-plugin/marketplace.json",
        ".claude-plugin/plugin.json",
        ".codex-plugin/plugin.json",
    ]
    assert [item.target_relative_path for item in catalog.scaffold_file_plan("greenfield").entries] == [
        ".claude/CLAUDE.md",
        ".cursorrules",
        "AGENTS.md",
        "CLAUDE.md",
        "docs/agent-workflow.md",
    ]


def test_future_bootstrap_fails_before_missing_child_is_read(tmp_path):
    root = registry_fixture(tmp_path)
    platform_path = root / "registry/platform.json"
    platform = json.loads(platform_path.read_text(encoding="utf-8"))
    platform["format_revision"] = 2
    platform["children"][0]["path"] = "registry/does-not-exist.json"
    write_json(platform_path, platform)
    result = Catalog.load(root)
    assert codes(result) == ["REGISTRY_FORMAT_UNSUPPORTED"]


def test_unknown_descriptor_field_has_json_path(tmp_path):
    root = registry_fixture(tmp_path)
    path = root / "registry/domains.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["domains"][0]["surprise"] = True
    write_json(path, value)
    result = Catalog.load(root)
    assert "REGISTRY_UNKNOWN_FIELD" in codes(result)
    diagnostic = next(item for item in result if item.code == "REGISTRY_UNKNOWN_FIELD")
    assert diagnostic.path == "registry/domains.json#/domains/0/surprise"


def test_mixed_code_and_child_format_fails_atomically(tmp_path):
    root = registry_fixture(tmp_path)
    path = root / "registry/adapters.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["format_revision"] = 2
    write_json(path, value)
    result = Catalog.load(root)
    assert "REGISTRY_ATOMIC_UPGRADE_REQUIRED" in codes(result)
    assert not isinstance(result, Catalog)


def test_new_governed_product_path_without_component_is_orphaned(tmp_path):
    root = registry_fixture(tmp_path)
    product = root / "docs/new-area/product.bin"
    product.parent.mkdir(parents=True)
    product.write_bytes(b"product")
    # Load must still succeed: a stray file must not brick every Catalog
    # consumer. The governed-inventory sweep is a validation-time concern.
    catalog = load_ok(root)
    result = catalog.validate_governed_inventory()
    assert "EVOLUTION_ORPHAN_PATH" in codes(result)
    assert any(item.path == "docs/new-area/product.bin" for item in result)


def test_catalog_results_are_defensive_copies():
    catalog = load_ok(ROOT)
    domains = catalog.domains()
    domains[0]["trigger"]["name"] = "mutated"
    assert catalog.domains()[0]["trigger"]["name"] == "knowledge-work"

