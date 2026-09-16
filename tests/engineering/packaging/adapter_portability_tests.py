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
            "$Proposal",
            "$PROPOSAL",
            "$Route",
            "$ROUTE",
            "$plan",
            "$PLAN",
            "$proposal-review",
        ):
            with self.subTest(token=token), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "codex-dollar-skill"
                shutil.copytree(source, target)
                (target / "SKILL.md").write_text(
                    source_text.replace("$proposal", token),
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
                        "Invoke this workflow as `$proposal` before continuing.",
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

    def test_route_explicit_adapter_invocation_equivalents_remain_portable(
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

    def test_route_slash_commands_end_at_phrase_terminators(self) -> None:
        additions = (
            "Run /route\nThen continue.",
            "Run /route\r\nThen continue.",
            "Run `/route` before continuing.",
            "Run /route, then continue.",
            "Run /route. Then continue.",
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

                self.assertEqual(report.included_adapters, ("codex",))
                self.assertIn("Codex-specific $skill invocation", report.reason)

    def test_route_invocation_equivalence_uses_narrow_static_scope(
        self,
    ) -> None:
        mutations = {
            "codex_skill": lambda text: text.replace(
                "$route auto: <argument>",
                "$broken auto: <argument>",
                1,
            ),
            "claude_skill": lambda text: text.replace(
                "/route auto: <argument>",
                "/broken auto: <argument>",
                1,
            ),
            "shared_argument": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.",
                "Here `<argument>` is `<stage>`, `status`, or `off`.",
                1,
            ),
            "bare_codex": lambda text: text + "\nUse `$route`.\n",
            "non_auto_codex": lambda text: text + "\nUse `$route manual`.\n",
            "case_codex": lambda text: text + "\nUse `$Route auto: <argument>`.\n",
            "wrong_claude_argument": lambda text: text
            + "\nUse `/route auto: <wrong>`.\n",
            "case_claude": lambda text: text
            + "\nUse `/Route auto: <argument>`.\n",
            "wrong_opencode_argument": lambda text: text
            + "\nOpenCode invokes installed `route` with `auto: <wrong>`.\n",
            "case_opencode": lambda text: text
            + "\nOpenCode invokes installed `Route` with `auto: <argument>`.\n",
            "plain_codex": lambda text: text
            + "\nUse $route manual to continue.\n",
            "html_codex": lambda text: text
            + "\nUse <code>$route manual</code> to continue.\n",
            "plain_claude": lambda text: text
            + "\nClaude users run /route manual to continue.\n",
            "whitespace_claude": lambda text: text
            + "\nClaude users run ` /route auto: <wrong>`.\n",
            "plain_opencode": lambda text: text
            + "\nOpenCode invokes route with auto: wrong.\n",
            "composed_opencode": lambda text: text
            + "\nOpenCode invokes installed `broken` skill with "
            + "`manual: <argument>`.\n",
            "codex_labeled_composed": lambda text: text
            + "\nCodex users run broken manual to continue.\n",
            "codex_labeled_html": lambda text: text
            + "\nCodex uses <code>broken manual</code>.\n",
            "codex_entity": lambda text: text
            + "\nCodex uses &#36;route manual.\n",
            "claude_call": lambda text: text
            + "\nFor Claude, call /broken auto: wrong.\n",
            "opencode_execute": lambda text: text
            + "\nOpenCode executes route with auto: wrong.\n",
            "opencode_command": lambda text: text
            + "\nOpenCode command: route auto: wrong.\n",
            "html_split_codex": lambda text: text
            + "\nCo<em>dex</em> executes broken manual.\n",
            "html_split_claude": lambda text: text
            + "\nCla<strong>ude</strong> starts broken manual.\n",
            "html_split_opencode": lambda text: text
            + "\nOpen<span>Code</span> command: broken manual.\n",
            "html_comment_codex": lambda text: text
            + "\nCo<!-- hidden -->dex executes broken manual.\n",
            "html_attribute_opencode": lambda text: text
            + '\nOpen<span title=">">Code</span> command: broken manual.\n',
            "html_unknown_tag_claude": lambda text: text
            + "\nCla<custom>ude</custom> starts broken manual.\n",
            "markdown_emphasis_codex": lambda text: text
            + "\nCo**dex** executes broken manual.\n",
            "markdown_emphasis_claude": lambda text: text
            + "\nCla**_ude_** starts broken manual.\n",
            "markdown_link_opencode": lambda text: text
            + "\nOpen[Code](https://example.invalid) command: broken manual.\n",
            "markdown_triple_emphasis_codex": lambda text: text
            + "\nCo***dex*** executes broken manual.\n",
            "markdown_mixed_emphasis_opencode": lambda text: text
            + "\nOpen**_Code_** command: broken manual.\n",
            "markdown_nested_strike_opencode": lambda text: text
            + "\nOpen~~**Code**~~ command: broken manual.\n",
            "markdown_nested_link_opencode": lambda text: text
            + "\nOpen[***Code***](https://example.invalid) command: broken manual.\n",
            "markdown_code_opencode": lambda text: text
            + "\nOpen`Code` command: broken manual.\n",
            "markdown_full_reference_codex": lambda text: text
            + "\nCo[dex][vendor] executes broken manual.\n"
            + "[vendor]: https://example.invalid\n",
            "markdown_collapsed_reference_claude": lambda text: text
            + "\nCla[ude][] starts broken manual.\n"
            + "[ude]: https://example.invalid\n",
            "markdown_shortcut_reference_opencode": lambda text: text
            + "\nOpen[Code] command: broken manual.\n"
            + "[Code]: https://example.invalid\n",
            "placeholder_tag_opencode": lambda text: text
            + "\nOpen<argument>Code</argument> command: broken manual.\n",
            "target_placeholder_tag_opencode": lambda text: text
            + "\nOpen<target-stage>Code</target-stage> command: broken manual.\n",
            "private_use_split_opencode": lambda text: text
            + "\nOpen\uf000\uf001Code command: broken manual.\n",
            "encoded_zero_width_split_opencode": lambda text: text
            + "\nOpen&#x200B;Code command: broken manual.\n",
            "combining_joiner_split_opencode": lambda text: text
            + "\nOpen\u034fCode command: broken manual.\n",
            "variation_selector_split_opencode": lambda text: text
            + "\nOpen\ufe0fCode command: broken manual.\n",
            "encoded_combining_joiner_split_opencode": lambda text: text
            + "\nOpen&#x034F;Code command: broken manual.\n",
            "encoded_variation_selector_split_opencode": lambda text: text
            + "\nOpen&#xFE0F;Code command: broken manual.\n",
            "null_control_split_opencode": lambda text: text
            + "\nOpen\u0000Code command: broken manual.\n",
            "backspace_control_split_opencode": lambda text: text
            + "\nOpen\u0008Code command: broken manual.\n",
            "unit_separator_split_opencode": lambda text: text
            + "\nOpen\u001fCode command: broken manual.\n",
            "hangul_filler_split_opencode": lambda text: text
            + "\nOpen\u115fCode command: broken manual.\n",
            "halfwidth_hangul_filler_split_opencode": lambda text: text
            + "\nOpen\uffa0Code command: broken manual.\n",
            "encoded_hangul_filler_split_opencode": lambda text: text
            + "\nOpen&#x115F;Code command: broken manual.\n",
            "mongolian_variation_split_opencode": lambda text: text
            + "\nOpen\u180bCode command: broken manual.\n",
            "encoded_mongolian_variation_split_opencode": lambda text: text
            + "\nOpen&#x180B;Code command: broken manual.\n",
            "khmer_inherent_vowel_split_opencode": lambda text: text
            + "\nOpen\u17b4Code command: broken manual.\n",
            "literal_argument_sentinel": lambda text: text.replace(
                "Claude uses `/route auto: <argument>`",
                "Claude uses `/route auto: \uf000argument\uf001`",
                1,
            ),
            "encoded_argument_sentinel": lambda text: text.replace(
                "Claude uses `/route auto: <argument>`",
                "Claude uses `/route auto: &#xF000;argument&#xF001;`",
                1,
            ),
            "literal_target_sentinel": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`",
                "Here `<argument>` is `\uf000target-stage\uf001`",
                1,
            ),
            "claude_zero_width_identity": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/rou\u200bte auto: <argument>`",
                1,
            ),
            "claude_private_use_identity": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/rou\uf000te auto: <argument>`",
                1,
            ),
            "claude_uppercase_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <ARGUMENT>`",
                1,
            ),
            "claude_spaced_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <argument >`",
                1,
            ),
            "claude_self_closing_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <argument/>`",
                1,
            ),
            "claude_encoded_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: &lt;argument&gt;`",
                1,
            ),
            "uppercase_target_placeholder": lambda text: text.replace(
                "`<target-stage>`",
                "`<TARGET-STAGE>`",
                1,
            ),
            "nested_claude_placeholder": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route auto: <custom><argument></custom>`",
                1,
            ),
            "claude_nbsp_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\u00a0auto: <argument>`",
                1,
            ),
            "claude_em_space_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\u2003auto: <argument>`",
                1,
            ),
            "claude_tab_separator": lambda text: text.replace(
                "`/route auto: <argument>`",
                "`/route\tauto: <argument>`",
                1,
            ),
            "slash_unit_separator": lambda text: text
            + "\nUse /work\u001fflow manual.\n",
            "slash_file_separator": lambda text: text
            + "\nUse /work\u001cflow manual.\n",
            "slash_next_line_control": lambda text: text
            + "\nUse /work\u0085flow manual.\n",
            "slash_mongolian_variation": lambda text: text
            + "\nUse /work\u180bflow manual.\n",
            "codex_status_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status-now`",
                1,
            ),
            "codex_status_trailing_argument": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status extra`",
                1,
            ),
            "codex_off_prefix": lambda text: text.replace(
                "`$route auto: off`",
                "`$route auto: office`",
                1,
            ),
            "codex_target_suffix": lambda text: text.replace(
                "`$route auto: <target-stage>`",
                "`$route auto: <target-stage>-extra`",
                1,
            ),
            "codex_command_prefix": lambda text: text.replace(
                "`$route auto: status`",
                "`x$route auto: status`",
                1,
            ),
            "codex_status_html_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status<em>-now</em>`",
                1,
            ),
            "codex_status_adjacent_suffix": lambda text: text.replace(
                "`$route auto: status`",
                "`$route auto: status`-now",
                1,
            ),
            "codex_off_adjacent_suffix": lambda text: text.replace(
                "`$route auto: off`",
                "`$route auto: off`-now",
                1,
            ),
            "codex_target_adjacent_suffix": lambda text: text.replace(
                "`$route auto: <target-stage>`",
                "`$route auto: <target-stage>`-extra",
                1,
            ),
            "codex_status_adjacent_argument": lambda text: text.replace(
                "`$route auto: status` is read-only",
                "`$route auto: status` extra is read-only",
                1,
            ),
            "equivalence_block_suffix": lambda text: text.replace(
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.",
                "Here `<argument>` is `<target-stage>`, `status`, or `off`.extra",
                1,
            ),
        }
        nonportable = {
            "codex_skill",
            "claude_skill",
            "shared_argument",
            "bare_codex",
            "non_auto_codex",
            "case_codex",
            "wrong_claude_argument",
            "case_claude",
            "plain_codex",
            "html_codex",
            "plain_claude",
            "whitespace_claude",
            "literal_argument_sentinel",
            "encoded_argument_sentinel",
            "literal_target_sentinel",
            "claude_zero_width_identity",
            "claude_private_use_identity",
            "claude_uppercase_placeholder",
            "claude_spaced_placeholder",
            "claude_self_closing_placeholder",
            "claude_encoded_placeholder",
            "uppercase_target_placeholder",
            "nested_claude_placeholder",
            "claude_nbsp_separator",
            "claude_em_space_separator",
            "claude_tab_separator",
            "codex_status_suffix",
            "codex_status_trailing_argument",
            "codex_off_prefix",
            "codex_target_suffix",
            "codex_command_prefix",
            "codex_status_html_suffix",
            "codex_status_adjacent_suffix",
            "codex_off_adjacent_suffix",
            "codex_target_adjacent_suffix",
            "codex_status_adjacent_argument",
            "equivalence_block_suffix",
        }
        source = ROOT / "skills" / "route" / "SKILL.md"
        source_text = source.read_text(encoding="utf-8")
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "route"
                shutil.copytree(source.parent, target)
                skill_file = target / "SKILL.md"
                mutated = mutate(source_text)
                self.assertNotEqual(mutated, source_text, "mutation must exercise the current contract")
                skill_file.write_text(mutated, encoding="utf-8")

                report = evaluate_skill(target)

                if name in nonportable:
                    self.assertEqual(report.included_adapters, ("codex",))
                    self.assertIn(
                        "Codex-specific $skill invocation",
                        report.reason,
                    )
                else:
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
