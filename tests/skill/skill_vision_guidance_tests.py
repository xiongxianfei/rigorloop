"""Vision guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class VisionSkillProgressiveDisclosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "vision"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.strategic = (self.root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        self.readme = (self.root / "references" / "readme-vision-sync.md").read_text(encoding="utf-8")
        self.vision_asset = (self.root / "assets" / "vision-skeleton.md").read_text(encoding="utf-8")
        self.positioning_asset = (self.root / "assets" / "strategic-positioning-skeleton.md").read_text(encoding="utf-8")
        self.package = "\n".join((self.skill, self.strategic, self.readme))

    def test_package_inventory_resource_verbs_and_six_assemblies_are_exact(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["readme-vision-sync.md", "strategic-vision-authoring.md"])
        self.assertEqual(sorted(path.name for path in (self.root / "assets").iterdir()), ["strategic-positioning-skeleton.md", "vision-skeleton.md"])
        self.assertFalse(any(path.suffix == ".py" for path in self.root.rglob("*")))
        for mapping in ("READ `references/strategic-vision-authoring.md`", "READ `references/readme-vision-sync.md`", "COPY `assets/vision-skeleton.md`", "COPY `assets/strategic-positioning-skeleton.md`"):
            self.assertIn(mapping, self.skill)
        rows = [line for line in self.skill.splitlines() if line.startswith("| `VA")]
        for assembly in ("VA0-readme-sync", "VA0S-readme-skip", "VA1-editorial-sync", "VA1S-editorial-skip", "VA2-strategic-sync", "VA2S-strategic-skip"):
            self.assertEqual(sum(assembly in row for row in rows), 1)

    def test_universal_operations_actions_authority_and_claims_remain_inline(self) -> None:
        for value in ("establish-vision", "revise-vision", "sync-readme", "editorial", "substantive-nonmaterial", "material-repositioning", "synchronize-existing", "insert-and-synchronize", "full-rewrite", "partial-retry-required", "blocked-before-write"):
            self.assertIn(value, self.skill)
        for phrase in ("`CONSTITUTION.md` outranks `VISION.md`", "`VISION.md` is canonical", "only supported project-vision artifact", "loading a reference or copying an asset never grants", "privacy", "stop before", "do not claim", "does not hand off automatically"):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertNotIn("## Modes", self.skill)

    def test_references_have_distinct_procedure_and_no_authority_grant(self) -> None:
        for phrase in ("project category", "primary user", "primary pain", "primary promise", "core mechanism", "alternatives", "tradeoff", "compatibility surfaces", "refusals", "falsifiability", "MUST NOT exceed 900 words", "methodology-as-product"):
            self.assertIn(phrase.lower(), self.strategic.lower())
        for phrase in ("<!-- vision:start -->", "<!-- vision:end -->", "first H1 block", "preserve every byte outside", "derived", "idempot"):
            self.assertIn(phrase.lower(), self.readme.lower())
        for reference in (self.strategic, self.readme):
            self.assertIn("parent skill owns", reference.lower())
            self.assertNotIn("grants authority", reference.lower())

    def test_assets_are_structural_complete_and_policy_free(self) -> None:
        for heading in ("## Pitch", "## What makes this different", "## Who it is for", "## Who it is not for", "## What it commits to", "## What it refuses to be", "## What would prove this wrong"):
            self.assertIn(heading, self.vision_asset)
        for heading in ("## Project category", "## Primary user", "## Primary pain", "## Primary promise", "## Core mechanism", "## Alternatives", "## Tradeoff", "## Compatibility surfaces", "## Refusals", "## Falsifiability"):
            self.assertIn(heading, self.positioning_asset)
        self.assertIn("does not independently override it", self.positioning_asset)
        for asset in (self.vision_asset, self.positioning_asset):
            for forbidden in ("authority is", "lifecycle", "review status", "marker parsing", "word limit"):
                self.assertNotIn(forbidden, asset.lower())

    def test_skip_manifest_write_order_retry_and_resource_failures_are_closed(self) -> None:
        for phrase in ("not-evaluated-under-exact-skip", "equal prior and intended identities", "authorized change-local authoring evidence before its first target write", "otherwise stop and require Design before planning", "zero-write skip has no changed files", "claims neither synchronization nor marker validity", "write source-first", "immediately before README", "read-back of every required", "committed and pending targets", "portable cross-session recovery", "missing, unreadable, escaped, stale, contradictory, or mixed-version", "do not reconstruct"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for claim in ("review approval", "implementation", "validation", "verification", "branch readiness", "PR readiness", "release", "deployment"):
            self.assertIn(claim.lower(), self.skill.lower())
