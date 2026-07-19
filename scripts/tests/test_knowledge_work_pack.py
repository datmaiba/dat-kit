"""knowledge-work Domain Pack cutover checks (Phase 4d).

Before/after behavioral pins for the two knowledge-work paths (report,
fact-check): the policy that lived in the pre-cutover skills/knowledge-work/*
files must survive on the composed surface — engine/work-loop/ENGINE.md for
loop mechanics, domains/knowledge-work/* for research-and-writing policy —
and the rendered thin trigger must actually resolve the files it names. Also
pins plan §16 rules 1–4 in reviewers.md (the ownership map's exact kw
phrasing), the Goal human-run ceiling in loop-profile + descriptor, the A→G ↔
engine-phase correspondence (including the PLAN approval stop landing at B),
pack purity both ways, and the 4d marker decision (§2b vacuous, mechanism
intact until 4f).
"""
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from registry import Catalog  # noqa: E402

PACK = ROOT / "domains" / "knowledge-work"
ENGINE = (ROOT / "engine/work-loop/ENGINE.md").read_text(encoding="utf-8")
TRIGGER = (ROOT / "skills/knowledge-work/SKILL.md").read_text(encoding="utf-8")


def slot(name: str) -> str:
    return (PACK / name).read_text(encoding="utf-8")


def flat(text: str) -> str:
    """Whitespace-normalized view: prose is hard-wrapped, policy is not."""
    return " ".join(text.split())


# --- composition: descriptor, trigger, slots -------------------------------

def test_descriptor_is_active_and_points_at_the_pack():
    catalog = Catalog.load(ROOT)
    assert isinstance(catalog, Catalog)
    descriptor = next(d for d in catalog.domains() if d["domain_id"] == "knowledge-work")
    assert descriptor["lifecycle"] == "active"
    assert descriptor["pack_location"] == "domains/knowledge-work"
    assert descriptor["required_engine_revision"] == "work-loop/1"
    assert descriptor["loop_ceiling"] == "Goal"
    # skill-eval trg-knowwork-01 keys on this phrase in the trigger description
    assert "write a researched report" in descriptor["trigger"]["description"]


def test_trigger_is_generated_and_resolves_every_named_file():
    assert "GENERATED FROM REGISTRY" in TRIGGER
    named = re.findall(r"`(domains/knowledge-work/[^`]+)`", TRIGGER)
    assert len(named) == 6, "thin trigger must name exactly the six slots"
    for relative in named:
        path = ROOT / relative
        assert path.is_dir() if relative.endswith("/") else path.is_file(), relative
    assert "work-loop/1" in TRIGGER
    # thin means thin: no policy vocabulary from the old operative body
    for token in ("SOURCED", "fact-checker", "Primary over summary",
                  "verification step", "[UNSOURCED]"):
        assert token not in TRIGGER, f"trigger carries policy token {token!r}"


def test_old_pack_location_holds_only_the_rendered_trigger():
    remaining = sorted(p.name for p in (ROOT / "skills/knowledge-work").iterdir())
    assert remaining == ["SKILL.md"], "legacy slot files must not survive the cutover"


# --- A→G correspondence (engine deletion test, ENGINE.md requirement) -------

def test_workflow_declares_the_engine_phase_correspondence():
    workflow = slot("workflow.md")
    for engine_phase, pack_phase in [
        ("LOAD", "A Clarify (brief intake) + C Ground truth (source intake)"),
        ("SELF-QUESTION", "A Clarify (assumptions and open questions)"),
        ("PLAN", "B Decompose"),
        ("EXECUTE", "D Execute"),
        ("VERIFY", "E Verify (gate runs)"),
        ("REVIEW", "E Verify (independent review)"),
        ("REPORT", "F Report"),
        ("HARVEST", "G Harvest"),
    ]:
        assert f"| {engine_phase} | {pack_phase} |" in workflow, engine_phase


def test_plan_approval_stop_is_addressed_explicitly():
    # 4b flag: engine PLAN's attended approval stop has no historical kw
    # phase-B counterpart — the correspondence must bind it, not skip it.
    workflow = flat(slot("workflow.md"))
    assert "The engine's PLAN approval stop lands at B" in workflow
    assert "no plan reviewer" in workflow
    assert "never bundled with the draft" in workflow


# --- the two behavioral paths ----------------------------------------------

def test_report_path_policy_survives():
    workflow, ground_truth = flat(slot("workflow.md")), flat(slot("ground-truth.md"))
    # engine owns the loop mechanics
    assert "stop for explicit approval" in flat(ENGINE)
    assert "Never grade your own work" in flat(ENGINE)
    # pack owns the research-and-writing instantiation
    assert "audience, purpose, scope, length, required sources or jurisdiction, deadline" in workflow
    assert "verification step" in workflow
    assert "Attach a source to every non-trivial factual claim" in workflow
    assert "you do not grade your own claims" in workflow
    assert "Primary over summary, current over remembered" in workflow
    assert "Primary over summary." in ground_truth and "Current over remembered." in ground_truth
    assert "flag it inline, do not launder it into confident prose" in ground_truth
    report = (PACK / "deliverables/report.template.md").read_text(encoding="utf-8")
    assert "[UNSOURCED]" in report and "Verification record" in report


def test_gates_migrated_with_ids_and_gaming_lines():
    gates = slot("gates.md")
    for gate_id in ("G1", "G2", "G3", "G4", "G5", "G6"):
        assert f"## {gate_id} " in gates, f"gate {gate_id} lost in cutover"
    assert gates.count("**Gamed by:**") == 6
    assert "This gate sets the domain ceiling" in flat(gates)
    # cross-ref updated off the 4e-rewritten domain-builder onto the contract
    assert "docs/contracts/domain-pack.md` DP3.3" in gates
    assert "domain-builder" not in gates


def test_fact_check_path_policy_survives():
    reviewers = flat(slot("reviewers.md"))
    assert "attack the deliverable's claims, not defend them. Read-only." in reviewers
    assert "`SOURCED` only when every claim passes G2" in reviewers
    assert "pass a claim on citation *presence* alone" in reviewers
    template = (PACK / "deliverables/fact-check.template.md").read_text(encoding="utf-8")
    assert "Claim-by-claim" in template
    assert "`SOURCED`" in template


def test_reviewers_has_no_charter_table_rows():
    # validate.py §3b probes `| `-prefixed rows against agents/<name>.md;
    # fact-checker has no agents/ charter, so the prose format is load-bearing.
    for line in slot("reviewers.md").splitlines():
        assert not line.startswith("| `"), f"charter-table row would break §3b: {line!r}"


# --- plan §16 rules 1–4 (ownership map §Map-§16, exact kw phrasing) ---------

@pytest.mark.parametrize("phrase", [
    "if the pack ever adds reviewers, they run in sequence, never parallel",
    "dispatch prompt names the claim list and pastes the builder's gate results (G1/G4/G5/G6 self-check)",
    "Re-submission checks previously failing claims only; full re-check only if new claims were added",
    "never fetches beyond cited sources to build a case",
    "≤ ~30 lines",
])
def test_review_cost_rules_land_in_reviewers_slot(phrase):
    assert phrase in flat(slot("reviewers.md")), f"§16 phrasing missing: {phrase!r}"


# --- loop ceiling: Goal, human-run, mirrored -------------------------------

def test_goal_human_run_ceiling_pinned_in_profile_and_descriptor():
    profile = flat(slot("loop-profile.md"))
    assert "Domain ceiling: Goal (human-run)" in profile
    assert "mirrored in the descriptor's `loop_ceiling`" in profile
    assert "never unlocks Time or Proactive automation" in profile
    assert "not a limitation to route around" in profile  # absorbed SKILL.md L47–49
    catalog = Catalog.load(ROOT)
    descriptor = next(d for d in catalog.domains() if d["domain_id"] == "knowledge-work")
    assert descriptor["loop_ceiling"] == "Goal"


# --- purity: no engine mechanics restated in the pack -----------------------

ENGINE_ONLY = [
    "genuinely unanswerable ones to the user",  # SELF-QUESTION escalation rule
    "grade your own work",                      # REVIEW independence rule (kw keeps "claims" flavor)
    "until you have seen it fail",              # red-green proof mechanics
    "keep what conforms",                       # recovery keep-or-fix rule
    "Never bundle plan",                        # PLAN approval mechanics
    "wakeup",                                   # long-run scheduling rule
    "is law",                                   # hard rules
    "propose an amendment",
    "5-part wrap-up",                           # HARVEST protocol
]


@pytest.mark.parametrize("sentence", ENGINE_ONLY)
def test_pack_purity_no_engine_mechanics_restated(sentence):
    for name in ("workflow.md", "ground-truth.md", "gates.md", "reviewers.md", "loop-profile.md"):
        assert sentence not in slot(name), f"{name} restates engine mechanics: {sentence!r}"


def test_purity_no_kw_policy_left_outside_the_pack():
    for token in ("SOURCED", "fact-checker", "source–claim fidelity"):
        assert token not in ENGINE, f"engine carries kw policy token {token!r}"


# --- 4d marker decision: §2b vacuous, mechanism intact until 4f -------------

def test_no_bare_pack_marker_remains_but_the_mechanism_survives():
    bare = re.compile(r'(?<!")Contract files live beside this one')
    for skill_md in (ROOT / "skills").glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        assert not bare.search(text), f"{skill_md}: bare five-slot marker should be gone after 4d"
    # the detection mechanism retires only at 4f (registry conformance cutover).
    # 4e decision: the rewritten domain-builder keeps ONE quoted legacy note
    # (no bare marker, §2b stays vacuous) so the mechanism keeps its documented
    # authoring partner; 4f removes validate §2b + that note in a single fire.
    validate = (ROOT / "scripts/validate.py").read_text(encoding="utf-8")
    assert "Contract files live beside this one" in validate


def test_deliverables_slot_has_real_templates():
    templates = list((PACK / "deliverables").glob("*.md"))
    assert len(templates) == 2, "DP3.5: report + fact-check templates"
    for template in templates:
        text = template.read_text(encoding="utf-8")
        assert "Verification record" in text, "deliverable must name the evidence it owes"
