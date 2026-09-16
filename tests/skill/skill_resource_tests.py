"""Resource-map classes, containment and instruction-reference boundaries.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    FIXTURES,
    assert_validation_fails,
    assert_validation_passes,
    write_resource_integrity_skill,
)


class SkillResourceMapTests(unittest.TestCase):
    maxDiff = None

    def test_published_design_missing_resource_map_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/missing-resource-map")
        assert_validation_fails(self, result, "packaged resources require a '## Resource map' section")

    def test_published_design_resource_map_must_name_every_resource(self) -> None:
        result = run_validator(FIXTURES / "published-design/resource-map-missing-resource")
        assert_validation_fails(self, result, "Resource map must name packaged resource 'references/detail.md'")

    def test_published_design_packaged_script_with_map_passes(self) -> None:
        result = run_validator(FIXTURES / "published-design/packaged-script-valid")
        assert_validation_passes(self, result)

    def test_published_design_packaged_script_requires_failure_behavior(self) -> None:
        result = run_validator(FIXTURES / "published-design/packaged-script-missing-failure")
        assert_validation_fails(self, result, "packaged script 'scripts/check.py' map entry must describe failure behavior")

    def test_published_design_repository_root_script_dependency_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/required-root-script")
        assert_validation_fails(self, result, "required repository-root dependency")

    def test_published_design_repository_root_script_command_dependency_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/required-root-script-command")
        assert_validation_fails(self, result, "required repository-root dependency by command wording: scripts/validate-internal.py")

    def test_published_design_packaged_script_resource_map_passes(self) -> None:
        result = run_validator(FIXTURES / "published-design/packaged-script-resource-map")
        assert_validation_passes(self, result)

    def test_published_skill_resource_map_copy_read_run_classes_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `assets/skeleton.md` when creating the output structure.
                  Fill all fields and do not emit unfilled placeholders.
                - READ `references/guidance.md` when reviewing domain guidance.
                - RUN `scripts/check.py` when deterministic checking is needed.
                  Input: repository root path.
                  Output: zero exit code or diagnostic output.
                  Failure: nonzero exit code blocks the check.
                """,
                resources={
                    "assets/skeleton.md": "# Skeleton\n",
                    "references/guidance.md": "# Guidance\n",
                    "scripts/check.py": "print('ok')\n",
                },
            )
            result = run_validator(skill_dir)
            self.assertEqual(
                result.returncode,
                0,
                msg=f"expected mapped resources to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_published_skill_resource_map_copy_must_point_to_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `references/guidance.md` when creating output.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "Resource map entry 'COPY references/guidance.md' must point to assets/")

    def test_published_skill_resource_map_read_must_point_to_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `assets/skeleton.md` when reviewing guidance.
                """,
                resources={"assets/skeleton.md": "# Skeleton\n"},
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "Resource map entry 'READ assets/skeleton.md' must point to references/")

    def test_published_skill_resource_map_run_must_point_to_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - RUN `assets/check.md` when checking output.
                """,
                resources={"assets/check.md": "# Check\n"},
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "Resource map entry 'RUN assets/check.md' must point to scripts/")

    def test_published_skill_resource_map_rejects_templates_class(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `templates/architecture.md` when creating output.
                """,
                resources={"templates/architecture.md": "# Architecture\n"},
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "Resource map entry 'COPY templates/architecture.md' must point to assets/")

    def test_published_skill_resource_map_rejects_missing_mapped_resource(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `assets/missing.md` when creating output.
                """,
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "mapped resource 'assets/missing.md' does not exist in canonical skill source")

    def test_published_skill_resource_map_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `../references/escape.md` when reviewing guidance.
                """,
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "mapped resource path '../references/escape.md' must be relative to the skill root and stay inside it")

    def test_published_skill_resource_map_rejects_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - RUN `/tmp/check.py` when checking output.
                """,
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "mapped resource path '/tmp/check.py' must be relative to the skill root and stay inside it")

    def test_published_skill_legacy_template_loading_instruction_fails(self) -> None:
        cases = [
            ("Use templates/architecture.md when relevant.", "templates/architecture.md"),
            ("Use templates/architecture.md when available.", "templates/architecture.md"),
            ("Read references/diagram-conventions.md when needed.", "references/diagram-conventions.md"),
            ("Copy assets/architecture-skeleton.md if present.", "assets/architecture-skeleton.md"),
            ("Run scripts/render-diagram.py when relevant.", "scripts/render-diagram.py"),
        ]
        for instruction, resource_path in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
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
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=f"""\
                        Artifact examples may mention `docs/changes/example/review-log.md`.

                        {instruction}
                        """,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected non-resource example to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

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
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
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
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected independent instruction boundaries to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

    def test_published_skill_legacy_lint_ignores_resource_map_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `assets/architecture-skeleton.md` when authoring architecture.
                """,
                resources={"assets/architecture-skeleton.md": "# Architecture\n"},
            )
            result = run_validator(skill_dir)
            self.assertEqual(
                result.returncode,
                0,
                msg=f"expected Resource map entries to stay owned by mapped validation\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_published_skill_legacy_lint_allows_individually_qualified_references(self) -> None:
        cases = [
            "Use the user-provided references/external.md and the project-provided templates/custom.md.",
            "Use the user-provided references/external.md and templates/custom.md provided by the project.",
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected individually qualified references to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

    def test_published_skill_architecture_legacy_references_fail_after_m3(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `references/guidance.md` when reviewing guidance.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
                body_extra="Use `templates/architecture.md` for the full 12-section arc42 structure. "
                "Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. "
                "Use `templates/adr.md` for ADR structure.",
                skill_name="architecture",
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/architecture.md`")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `references/guidance.md` when reviewing guidance.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
                body_extra="Use templates/architecture.md when relevant.",
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "resource-integrity-fixture: unmapped skill-local resource reference `templates/architecture.md`")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `references/guidance.md` when reviewing guidance.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
                body_extra="Use templates/unapproved.md when relevant.",
                skill_name="architecture",
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/unapproved.md`")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `references/guidance.md` when reviewing guidance.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
                body_extra="Use the user-provided references/external.md and templates/architecture.md when relevant.",
                skill_name="architecture",
            )
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "architecture: unmapped skill-local resource reference `templates/architecture.md`")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - READ `references/guidance.md` when reviewing guidance.
                """,
                resources={"references/guidance.md": "# Guidance\n"},
                body_extra="""\
            Use `templates/architecture.md` for the full 12-section arc42 structure. Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. Use `templates/adr.md` for ADR structure.
            - Use templates/unapproved.md when relevant.
            """,
                skill_name="architecture",
            )
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
