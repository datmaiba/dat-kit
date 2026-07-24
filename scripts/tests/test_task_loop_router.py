"""task-loop router projection (PLAN v8 Phase B).

The router is a SECOND projection type: one generated trigger that lists every
non-software `lifecycle=active` Domain Pack and routes the chosen one through the
work-loop engine and its six slots. Exclusion of software-dev is declared in the
registry (`domains.json#/task_loop/excluded_domain_ids`), never hardcoded in the
trigger, so a new non-software pack appears in the router with no code edit
(DP6 extension-proof). These fixtures were authored red-before-green.
"""
import json
from pathlib import Path
import sys


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from registry import Catalog  # noqa: E402
from render import check_outputs, expected_outputs, render_task_loop_router, write_outputs  # noqa: E402,F401
from test_registry_catalog import codes, load_ok, registry_fixture, write_json  # noqa: E402
from test_domain_builder_pack import add_ledger_close_pack, make_descriptor  # noqa: E402

ROUTER = "skills/task-loop/SKILL.md"


def _router_body(root: Path) -> str:
    return expected_outputs(load_ok(root))[ROUTER].decode("utf-8")


# 1. Auto-inclusion: a synthetic non-software active pack appears with NO
#    render.py / registry.py edit — the whole point of a registry-driven router.
def test_new_non_software_pack_appears_without_code_edit(tmp_path):
    root = registry_fixture(tmp_path)
    add_ledger_close_pack(root)
    body = _router_body(root)
    assert "ledger-close" in body
    assert "GENERATED FROM REGISTRY" in body
    assert "source_revision=domains/1" in body


# 2. Exclusion: software-dev is declared excluded, so neither its domain id nor
#    its trigger name (code-loop) leak into the router menu.
def test_software_dev_excluded_from_router(tmp_path):
    root = registry_fixture(tmp_path)
    body = _router_body(root)
    assert "knowledge-work" in body
    assert "software-dev" not in body
    assert "code-loop" not in body


# 3. Byte-exact: a hand edit to the generated router trips --check and is never
#    silently repaired.
def test_hand_edit_router_fails_byte_exact_check(tmp_path):
    root = registry_fixture(tmp_path)
    outputs = expected_outputs(load_ok(root))
    write_outputs(root, outputs)
    path = root / ROUTER
    before = path.read_bytes() + b"# hand edit\n"
    path.write_bytes(before)
    diagnostics = check_outputs(root, outputs)
    assert any(d.code == "PROJECTION_BYTE_MISMATCH" and d.path == ROUTER for d in diagnostics)
    assert path.read_bytes() == before  # check never repairs


# 4. Real slots: a listed pack resolves its six real slot files under its
#    pack_location, not just a name in text.
def test_listed_pack_resolves_its_real_six_slots(tmp_path):
    root = registry_fixture(tmp_path)
    catalog = load_ok(root)
    knowledge = next(d for d in catalog.domains() if d["domain_id"] == "knowledge-work")
    pack = root / knowledge["pack_location"]
    for slot in ("workflow.md", "ground-truth.md", "gates.md", "reviewers.md", "loop-profile.md"):
        assert (pack / slot).is_file(), slot
    deliverables = pack / "deliverables"
    assert deliverables.is_dir() and any(deliverables.iterdir())
    assert knowledge["pack_location"] in _router_body(root)


# 5. Destination collision: a domain whose trigger name is "task-loop" collides
#    with the router destination and fails closed at Catalog.load.
def test_domain_named_task_loop_collides_with_router(tmp_path):
    root = registry_fixture(tmp_path)
    descriptor = make_descriptor()
    descriptor["domain_id"] = "task-loop-dom"
    descriptor["pack_location"] = "domains/task-loop-dom"
    descriptor["trigger"]["name"] = "task-loop"
    descriptor["trigger"]["aliases"] = ["collide-alias"]
    add_ledger_close_pack(root, descriptor=descriptor)
    assert "PROJECTION_DESTINATION_COLLISION" in codes(Catalog.load(root))


# 6. Alias collision: a router alias colliding with an existing domain alias
#    fails closed rather than rendering silently.
def test_router_alias_colliding_with_domain_alias(tmp_path):
    root = registry_fixture(tmp_path)
    domains_path = root / "registry/domains.json"
    domains = json.loads(domains_path.read_text(encoding="utf-8"))
    domains["task_loop"]["trigger"]["aliases"] = ["fact check"]  # knowledge-work alias
    write_json(domains_path, domains)
    assert "REGISTRY_TRIGGER_ALIAS_COLLISION" in codes(Catalog.load(root))


# 7. Envelope absent: no task_loop envelope means no router projection at all,
#    and no stale-output diagnostic.
def test_router_absent_when_envelope_absent(tmp_path):
    root = registry_fixture(tmp_path)
    domains_path = root / "registry/domains.json"
    domains = json.loads(domains_path.read_text(encoding="utf-8"))
    del domains["task_loop"]
    write_json(domains_path, domains)
    catalog = load_ok(root)  # optional key — load still succeeds
    outputs = expected_outputs(catalog)
    assert ROUTER not in outputs
    assert not any(d.code == "PROJECTION_STALE_OUTPUT" for d in check_outputs(root, outputs))


# 8. Empty menu: envelope present but no eligible pack renders explicit
#    empty-state guidance, never an empty body.
def test_empty_menu_renders_guidance(tmp_path):
    root = registry_fixture(tmp_path)
    domains_path = root / "registry/domains.json"
    domains = json.loads(domains_path.read_text(encoding="utf-8"))
    domains["task_loop"]["excluded_domain_ids"] = ["knowledge-work", "software-dev"]
    write_json(domains_path, domains)
    body = _router_body(root)
    assert "domain-builder" in body
    assert "knowledge-work" not in body
