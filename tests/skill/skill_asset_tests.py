"""Asset metadata, required structure and canonical/generated resource presence.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
import tempfile
import textwrap
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
from lib.validation import skill_validation
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    assert_validation_fails,
    assert_validation_passes,
    asset_text,
    proposal_family_asset_text,
    review_family_asset_text,
    write_asset_fixture,
)


class SkillAssetContractTests(unittest.TestCase):
    maxDiff = None













    def test_current_generated_asset_presence_passes_for_complete_output(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/valid"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="proposal",
            canonical_skill_dir=fixture / "canonical/proposal",
            generated_skill_dir=fixture / "generated/proposal",
            surface_label="generated skill mirror",
        )

        self.assertEqual(errors, [])

    def test_current_generated_asset_presence_fails_for_missing_generated_asset(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/missing-asset"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="proposal",
            canonical_skill_dir=fixture / "canonical/proposal",
            generated_skill_dir=fixture / "generated/proposal",
            surface_label="generated skill mirror",
        )

        self.assertEqual(
            errors,
            [
                "Generated output for skill 'proposal' is missing mapped asset "
                "'assets/proposal-skeleton.md' in generated skill mirror"
            ],
        )

    def test_current_generated_asset_presence_names_adapter_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_skill_dir = write_asset_fixture(
                root / "canonical",
                "code-review",
                {
                    "assets/review-result-skeleton.md": asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="## Result\n\n- Review status: <review status>\n",
                    ),
                    "assets/material-finding.md": asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body="## Finding <finding id>\n\n- Finding ID: <finding id>\n- Severity: <severity>\n",
                    ),
                },
            )
            generated_skill_dir = root / "generated-adapter" / "code-review"
            generated_asset = generated_skill_dir / "assets/review-result-skeleton.md"
            generated_asset.parent.mkdir(parents=True, exist_ok=True)
            generated_asset.write_text("generated result skeleton", encoding="utf-8")

            errors = skill_validation.validate_generated_asset_presence(
                skill_name="code-review",
                canonical_skill_dir=canonical_skill_dir,
                generated_skill_dir=generated_skill_dir,
                surface_label="generated adapter output",
            )

            self.assertEqual(
                errors,
                [
                    "Generated output for skill 'code-review' is missing mapped asset "
                    "'assets/material-finding.md' in generated adapter output"
                ],
            )
