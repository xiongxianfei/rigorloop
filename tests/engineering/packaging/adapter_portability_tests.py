"""Named portability partitions and invocation syntax transformations."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import SUPPORTED_ADAPTERS, evaluate_skill
from adapter_fixture_helpers import (fixture_path)


class AdapterPortabilityTests(unittest.TestCase):
    maxDiff = None

    def test_portable_skill_includes_all_adapters(self) -> None:
        report = evaluate_skill(fixture_path("portable-basic"))

        self.assertTrue(report.portable)
        self.assertEqual(report.name, "portable-basic")
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertEqual(report.reason, "")

    def test_invalid_name_description_and_body_fail_all_adapters(self) -> None:
        invalid_name = evaluate_skill(fixture_path("invalid-name"))
        invalid_description = evaluate_skill(fixture_path("invalid-description"))
        invalid_body = evaluate_skill(fixture_path("invalid-body"))

        self.assertFalse(invalid_name.portable)
        self.assertEqual(invalid_name.included_adapters, ())
        self.assertIn("portable skill name", invalid_name.reason)

        self.assertFalse(invalid_description.portable)
        self.assertEqual(invalid_description.included_adapters, ())
        self.assertIn("description", invalid_description.reason)

        self.assertFalse(invalid_body.portable)
        self.assertEqual(invalid_body.included_adapters, ())
        self.assertIn("top-level # title", invalid_body.reason)
        self.assertIn("Expected output", invalid_body.reason)

    def test_argument_hint_is_explicit_transform_not_exclusion(self) -> None:
        report = evaluate_skill(fixture_path("transformable-frontmatter"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        expected_transforms = (
            "drop frontmatter: argument-hint",
            "drop frontmatter: schema-version",
            "drop frontmatter: version",
        )
        self.assertEqual(report.adapter_decision("claude").transforms, expected_transforms)

    def test_codex_only_assumptions_exclude_non_codex_adapters(self) -> None:
        cases = {
            "unsupported-frontmatter": "unsupported frontmatter",
            "codex-invocation": "Codex-only invocation syntax",
            "agents-openai": "agents/openai.yaml",
            "codex-install-only": ".codex/skills",
            "codex-tool-assumption": "Codex-only tool, UI, approval, or runtime assumption",
            "codex-dollar-skill": "Codex-specific $skill invocation",
        }

        for fixture, expected_reason in cases.items():
            with self.subTest(fixture=fixture):
                report = evaluate_skill(fixture_path(fixture))
                self.assertFalse(report.portable)
                self.assertEqual(report.included_adapters, ("codex",))
                self.assertTrue(report.adapter_decision("codex").included)
                self.assertFalse(report.adapter_decision("claude").included)
                self.assertIn(expected_reason, report.reason)

    def test_case_variant_governed_dollar_invocations_are_codex_only(self) -> None:
        source = fixture_path("codex-dollar-skill")
        source_text = (source / "SKILL.md").read_text(encoding="utf-8")

        for token in (
            "$Requirement-Analysis",
            "$REQUIREMENT-ANALYSIS",
            "$Route",
            "$ROUTE",
            "$plan",
            "$PLAN",
            "$requirement-review",
        ):
            with self.subTest(token=token), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "codex-dollar-skill"
                shutil.copytree(source, target)
                (target / "SKILL.md").write_text(
                    source_text.replace("$requirement-analysis", token),
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_real_dollar_invocation_is_not_hidden_by_later_dollar(self) -> None:
        source = fixture_path("codex-dollar-skill")
        source_text = (source / "SKILL.md").read_text(encoding="utf-8")
        lines = (
            "Invoke `$plan`; let `$x$` denote the input.",
            "Invoke `$plan`; then read `$HOME`.",
            "Invoke `$plan`; the fallback costs $5.",
            r"Invoke `$plan`; document \$value.",
            "Invoke `$route auto: status`; let `$plan + 1$` denote input.",
            "Invoke `$plan` -> then read `$HOME`.",
            "Invoke `$plan` - then read `$HOME`.",
            "Invoke `$plan` -> budget $5.",
            r"Invoke `$plan` -> document \$value.",
            "Invoke `$plan` --verbose then inspect `$HOME`.",
            "Invoke `$plan` + compare with `$PATH`.",
            "Invoke `$plan` < input then inspect `$HOME`.",
            "Invoke $plan -> inspect ${HOME}.",
            "Invoke $plan -> run $(pwd).",
            r"Invoke $plan + 5\$.",
            r"Invoke \\$plan.",
        )

        for line in lines:
            with self.subTest(line=line), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "codex-dollar-skill"
                shutil.copytree(source, target)
                (target / "SKILL.md").write_text(
                    source_text.replace(
                        "Invoke this workflow as `$requirement-analysis` before continuing.",
                        line,
                    ),
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_generic_artifact_paths_remain_portable(self) -> None:
        report = evaluate_skill(fixture_path("generic-artifact-paths"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))

    def test_codex_skills_reference_with_adapter_alternatives_remains_portable(self) -> None:
        report = evaluate_skill(fixture_path("codex-install-with-alternatives"))

        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertEqual(report.reason, "")

    def test_current_route_guidance_is_portable_without_adapter_grammar(
        self,
    ) -> None:
        report = evaluate_skill(ROOT / "skills" / "route")

        self.assertTrue(report.portable, report.reason)
        self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_route_invocation_checks_preserve_variables_and_paths(self) -> None:
        additions = (
            "Read the shell variable `$project`.",
            "Let `$x$` denote the input.",
            "Read the shell variable `$workflow_status`.",
            "Read the path from `$plan_path`.",
            "Let `$spec₂` denote the input.",
            "Let `$plan$` denote the input.",
            "Let `$plan + 1$` denote the input.",
            "Let `$plan^2$` denote the input.",
            "Let `$plan + 1 - 2$` denote the input.",
            "Let `$plan + (1)$` denote the input.",
            "Let `$plan + π$` denote the input.",
            "Let `$plan ** 2$` denote the input.",
            "Let `$plan >= 1$` denote the input.",
            "Let `$plan + -1$` denote the input.",
            r"Let `$plan + \$5$` denote the input.",
            r"Document \$plan as a literal.",
            r"Document \\\$plan as a literal.",
            "Read the variable `$plan\u0301_value`.",
            "Read the variable `$workflow\ufe0f`.",
            "Read the variable `$plan\u200c_value`.",
            "Read the variable `$plan\u200d_value`.",
            "Do not treat `$ſpec` as a published name.",
            "Do not treat `$ımplement` as a published name.",
            "Do not treat `$worKflow` as a published name.",
            "Document `/workflow-guide`.",
            "Document `/workflow.md`.",
            "Document `/workflow/status`.",
            "Document `docs-/workflow`.",
            "Do not treat `/worKflow` as a published command.",
        )
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")

        for addition in additions:
            with self.subTest(addition=addition), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                (target / "SKILL.md").write_text(
                    source_text + f"\n{addition}\n",
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_route_benign_visible_boundaries_remain_portable(self) -> None:
        additions = (
            "Encode XML before parsing.",
            "Encode X509 certificates consistently.",
            "Keep open code samples in the fixture.",
            "Review open-code licensing separately.",
            "The cod_ex identifier is illustrative.",
            "The Co_dex_ key is illustrative.",
            "The Open_Code_ key is illustrative.",
            "The Co`dex token is illustrative.",
            "The Open[Code token is illustrative.",
            "The Cla]ude token is illustrative.",
            "The Open[Code] token is illustrative.",
            "The Open[Code][missing] token is illustrative.",
            "The Open[Code][] token is illustrative.",
            "The Open&#42;Code&#42; token is illustrative.",
            "The Open&#42;&#42;Code&#42;&#42; token is illustrative.",
            "The Open&#91;Code&#93; token is illustrative.",
            "The Open&#96;Code&#96; token is illustrative.",
            "An unrelated /workéflow token is illustrative.",
            "An unrelated /work☃flow token is illustrative.",
        )
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")
        for addition in additions:
            with self.subTest(addition=addition), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                (target / "SKILL.md").write_text(
                    source_text + f"\n{addition}\n",
                    encoding="utf-8",
                )

                report = evaluate_skill(target)

                self.assertEqual(report.included_adapters, SUPPORTED_ADAPTERS)

    def test_unrelated_equivalence_prose_does_not_portabilize_dollar_skill(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "codex-dollar-skill"
            shutil.copytree(fixture_path("codex-dollar-skill"), target)
            skill_file = target / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8")
                + "\nAdapter invocation equivalents: Codex uses, Claude uses, "
                + "and opencode invokes.\n",
                encoding="utf-8",
            )

            report = evaluate_skill(target)

        self.assertEqual(report.included_adapters, ("codex",))
        self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_retired_target_exclusion_does_not_reduce_current_portability(self) -> None:
        report = evaluate_skill(fixture_path("partial-portability"))
        self.assertTrue(report.portable)
        self.assertEqual(report.included_adapters, ("codex", "claude"))
        self.assertTrue(report.adapter_decision("codex").included)
        self.assertTrue(report.adapter_decision("claude").included)
