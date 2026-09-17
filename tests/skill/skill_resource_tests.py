"""Resource-map classes, containment and instruction-reference boundaries.

Model scenarios own the baseline, mutation and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    FIXTURES,
    assert_validation_fails,
    assert_validation_passes,
    resource_skill,
)


def guidance_skill(body_extra: str, *, skill_name: str = "resource-integrity-fixture"):
    """A valid mapped reference isolates the instruction supplied by each case."""
    return resource_skill(
        resource_entries="- READ `references/guidance.md` when reviewing guidance.",
        resources={"references/guidance.md": "# Guidance\n"},
        body_extra=body_extra,
        skill_name=skill_name,
    )


def mapped_skill(*, reference: str = "guidance.md"):
    """Fresh complete COPY/READ/RUN package for resource-contract scenarios."""
    return resource_skill(
        resource_entries=f"""\
            - COPY `assets/skeleton.md` when creating output.
              Fill all fields and do not emit unfilled placeholders.
            - READ `references/{reference}` when reviewing guidance.
            - RUN `scripts/check.py` when deterministic checking is needed.
              Input: repository root path.
              Output: zero exit code or diagnostic output.
              Failure: nonzero exit code blocks the check.
            """,
        resources={
            "assets/skeleton.md": "# Skeleton\n",
            f"references/{reference}": "# Guidance\n",
            "scripts/check.py": "print('ok')\n",
        },
    )


class SkillResourceMapTests(unittest.TestCase):
    maxDiff = None

    def test_resource_verbs_require_their_declared_directories(self):
        # SKL-RC-001: each wrong pairing starts from an accepted package.
        for verb, old, new, directory in (
            ("copy", "READ `references/guidance.md`", "COPY `references/guidance.md`", "assets/"),
            ("read", "COPY `assets/skeleton.md`", "READ `assets/skeleton.md`", "references/"),
            ("run", "COPY `assets/skeleton.md`", "RUN `assets/skeleton.md`", "scripts/"),
        ):
            with self.subTest(verb=verb), mapped_skill() as root:
                assert_validation_passes(self, run_validator(root))
                skill = root / "SKILL.md"
                body = skill.read_text()
                self.assertEqual(body.count(old), 1)
                skill.write_text(body.replace(old, new))
                pairing = new.replace("`", "")
                assert_validation_fails(self, run_validator(root),
                    f"Resource map entry '{pairing}' must point to {directory}")

    def test_resource_inventory_agrees_with_map_in_both_directions(self):
        # SKL-RC-002: map, declaration and content are separate omissions.
        for omission, diagnostic in (
            ("map", "packaged resources require a '## Resource map' section"),
            ("entry", "Resource map must name packaged resource 'references/detail.md'"),
            ("content", "mapped resource 'assets/skeleton.md' does not exist in canonical skill source"),
        ):
            with self.subTest(omission=omission), mapped_skill(reference="detail.md") as root:
                assert_validation_passes(self, run_validator(root))
                skill = root / "SKILL.md"
                body = skill.read_text()
                if omission == "map":
                    start, end = body.index("## Resource map"), body.index("## Expected output")
                    skill.write_text(body[:start] + body[end:])
                elif omission == "entry":
                    entry = "- READ `references/detail.md` when reviewing guidance."
                    self.assertEqual(body.count(entry), 1)
                    skill.write_text(body.replace(entry, ""))
                else:
                    (root / "assets/skeleton.md").unlink()
                assert_validation_fails(self, run_validator(root), diagnostic)
                if omission == "content":
                    self.assertFalse((root / "assets/skeleton.md").exists())

    def test_run_resource_requires_failure_action(self):
        # SKL-RC-003: retain script, input and output; omit only failure action.
        with mapped_skill() as root:
            assert_validation_passes(self, run_validator(root))
            skill = root / "SKILL.md"
            body = skill.read_text()
            failure = "Failure: nonzero exit code blocks the check."
            self.assertEqual(body.count(failure), 1)
            skill.write_text(body.replace(failure, ""))
            assert_validation_fails(self, run_validator(root),
                "packaged script 'scripts/check.py' map entry must describe failure behavior")

    def test_mapped_paths_must_stay_inside_skill_root(self):
        # SKL-RC-004: a missing-file error cannot satisfy containment.
        for variant, old, outside in (
            ("parent", "references/guidance.md", "../references/escape.md"),
            ("absolute", "scripts/check.py", "/tmp/check.py"),
        ):
            with self.subTest(path=variant), mapped_skill() as root:
                assert_validation_passes(self, run_validator(root))
                skill = root / "SKILL.md"
                body = skill.read_text()
                self.assertEqual(body.count(f"`{old}`"), 1)
                skill.write_text(body.replace(f"`{old}`", f"`{outside}`"))
                assert_validation_fails(self, run_validator(root),
                    f"mapped resource path '{outside}' must be relative to the skill root and stay inside it")

    def test_published_design_repository_root_script_dependency_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/required-root-script")
        assert_validation_fails(self, result, "required repository-root dependency")

    def test_published_design_repository_root_script_command_dependency_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/required-root-script-command")
        assert_validation_fails(self, result, "required repository-root dependency by command wording: scripts/validate-internal.py")

    def test_published_skill_legacy_template_loading_instruction_fails(self) -> None:
        cases = [
            ("Use templates/architecture.md when relevant.", "templates/architecture.md"),
            ("Use templates/architecture.md when available.", "templates/architecture.md"),
            ("Read references/diagram-conventions.md when needed.", "references/diagram-conventions.md"),
            ("Copy assets/architecture-skeleton.md if present.", "assets/architecture-skeleton.md"),
            ("Run scripts/render-diagram.py when relevant.", "scripts/render-diagram.py"),
        ]
        for instruction, resource_path in cases:
            with self.subTest(instruction=instruction), guidance_skill(instruction) as skill_dir:
                result = run_validator(skill_dir)
                assert_validation_fails(self, result, f"unmapped skill-local resource reference `{resource_path}`; "
                    "declare it in `## Resource map`, migrate it to an approved "
                    "resource class, or remove the instruction")

    def test_published_skill_legacy_lint_avoids_examples_and_docs_paths(self) -> None:
        cases = [
            "Use the project-provided templates/architecture.md when relevant.",
            "Use templates/custom.md provided by the project.",
            "Read the repository-root templates/architecture.md when available.",
            "Read references/policy.md supplied by the repository.",
            "Use the user-provided references/diagram-conventions.md.",
            "Example path: templates/architecture.md",
            "Illustrative resource: references/diagram.md",
            "The generated artifact may contain the string templates/architecture.md.",
            "Inspect docs/templates/architecture.md when that artifact is the review target.",
            """\
            ```text
            Use templates/architecture.md in a customer artifact example.
            ```
            """,
            "Customer projects may contain `assets/example.png` as normal data.",
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction):
                with guidance_skill(
                    body_extra=f"""\
                        Artifact examples may mention `docs/changes/example/review-log.md`.

                        {instruction}
                        """,
                ) as skill_dir:
                    result = run_validator(skill_dir)
                    assert_validation_passes(self, result)

    def test_published_skill_legacy_lint_checks_each_reference_on_mixed_line(self) -> None:
        cases = [
            (
                "When the project provides the helper, read references/external.md and run scripts/query-change-record.py.",
                "scripts/query-change-record.py",
                "references/external.md",
            ),
            (
                "Use the user-provided references/external.md and templates/architecture.md.",
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                Use the user-provided references/external.md and
                templates/architecture.md when relevant.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                Use templates/architecture.md when relevant and the user-provided
                references/external.md.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                - Use the user-provided references/external.md and
                  templates/architecture.md when relevant.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                - Use templates/architecture.md when relevant and
                  the user-provided references/external.md.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                "Use the user-provided references/a.md and references/b.md.",
                "references/b.md",
                "references/a.md",
            ),
            (
                "Example path: references/example.md; use templates/architecture.md.",
                "templates/architecture.md",
                "references/example.md",
            ),
        ]
        for instruction, reported_path, suppressed_path in cases:
            with self.subTest(instruction=instruction), guidance_skill(instruction) as skill_dir:
                result = run_validator(skill_dir)
                combined_output = f"{result.stdout}\n{result.stderr}"
                self.assertNotEqual(
                    result.returncode,
                    0,
                    msg=f"expected mixed reference fixture to fail\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn(
                    f"unmapped skill-local resource reference `{reported_path}`",
                    combined_output,
                )
                self.assertNotIn(
                    f"unmapped skill-local resource reference `{suppressed_path}`",
                    combined_output,
                )

    def test_published_skill_legacy_lint_keeps_instruction_boundaries(self) -> None:
        cases = [
            """\
            - Use the user-provided references/external.md.
            - The generated artifact may contain the string templates/architecture.md.
            """,
            """\
            1. Use the user-provided references/external.md.
            2. The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            ## Output example

            The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            ```md
            Use templates/architecture.md.
            ```
            """,
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction), guidance_skill(instruction) as skill_dir:
                result = run_validator(skill_dir)
                assert_validation_passes(self, result)

    def test_published_skill_legacy_lint_ignores_resource_map_entries(self) -> None:
        with resource_skill(
            resource_entries='- COPY `assets/architecture-skeleton.md` when authoring architecture.',
            resources={"assets/architecture-skeleton.md": "# Architecture\n"},
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_passes(self, result)

    def test_published_skill_legacy_lint_allows_individually_qualified_references(self) -> None:
        cases = [
            "Use the user-provided references/external.md and the project-provided templates/custom.md.",
            "Use the user-provided references/external.md and templates/custom.md provided by the project.",
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction), guidance_skill(instruction) as skill_dir:
                result = run_validator(skill_dir)
                assert_validation_passes(self, result)

    def test_published_skill_architecture_legacy_references_fail_after_m3(self) -> None:
        with guidance_skill(
            body_extra="Use `templates/architecture.md` for the full 12-section arc42 structure. "
            "Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. "
            "Use `templates/adr.md` for ADR structure.",
            skill_name="architecture",
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/architecture.md`")

        with guidance_skill(
            body_extra="Use templates/architecture.md when relevant.",
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "resource-integrity-fixture: unmapped skill-local resource reference `templates/architecture.md`")

        with guidance_skill(
            body_extra="Use templates/unapproved.md when relevant.",
            skill_name="architecture",
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/unapproved.md`")

        with guidance_skill(
            body_extra="Use the user-provided references/external.md and templates/architecture.md when relevant.",
            skill_name="architecture",
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/architecture.md`")

        with guidance_skill(
            body_extra="""\
            Use `templates/architecture.md` for the full 12-section arc42 structure. Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. Use `templates/adr.md` for ADR structure.
            - Use templates/unapproved.md when relevant.
            """,
            skill_name="architecture",
        ) as skill_dir:
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/unapproved.md`")

    def test_current_design_resource_map_uses_packaged_assets(self) -> None:
        root = ROOT / "skills/design"
        body = (root / "SKILL.md").read_text()
        for name in ("design-skeleton.md", "diagram-styles.mmd"):
            self.assertIn(f"COPY `assets/{name}`", body)
            self.assertTrue((root / "assets" / name).is_file())
        for private in ("templates/architecture.md", "templates/adr.md", "templates/diagram-styles.mmd"):
            self.assertNotIn(private, body)
        self.assertEqual(run_validator(root).returncode, 0)
