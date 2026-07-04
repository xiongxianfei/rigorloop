#!/usr/bin/env python3
"""Fixture-driven tests for Markdown readability validation."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-markdown-readability.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("markdown_readability_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load markdown readability validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")
    return path


class MarkdownReadabilityValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator_module()

    def test_changed_readme_hard_wrap_phrase_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-hard-wrap-") as temp:
            readme = write_text(
                Path(temp) / "README.md",
                """
                # Example

                RigorLoop makes AI
                agents reviewable in Git.
                """,
            )

            result = self.validator.validate_paths(
                [readme],
                changed_sections=[self.validator.ChangedSection(readme, 3, 5)],
            )

        self.assertTrue(result.has_errors)
        self.assertIn("MDREAD-001", {diagnostic.check_id for diagnostic in result.diagnostics})

    def test_long_complete_semantic_line_warns_without_failure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-long-line-") as temp:
            readme = write_text(
                Path(temp) / "README.md",
                """
                # Example

                This generated sentence is intentionally long because it is one complete semantic source line that should remain reviewable without a fixed width wrap rule.
                """,
            )

            result = self.validator.validate_paths(
                [readme],
                changed_sections=[self.validator.ChangedSection(readme, 3, 3)],
            )

        self.assertFalse(result.has_errors)
        self.assertIn("MDREAD-002", {diagnostic.check_id for diagnostic in result.diagnostics})
        self.assertTrue(all(diagnostic.severity != "error" for diagnostic in result.diagnostics))

    def test_prose_checks_exclude_code_tables_html_links_and_generated_regions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-exclude-") as temp:
            doc = write_text(
                Path(temp) / "README.md",
                """
                # Example

                ```text
                RigorLoop makes AI agents
                reviewable in Git.
                ```

                | Column |
                | --- |
                | AI agents
                reviewable in Git |

                <div>
                AI agents
                reviewable in Git.
                </div>

                [ai-agents]: https://example.test/AI
                [reviewable]: https://example.test/reviewable-in-Git

                <!-- rigorloop:generated:start surface=demo source=fixtures/demo.md generator=scripts/demo.py -->
                AI agents
                reviewable in Git.
                <!-- rigorloop:generated:end surface=demo -->
                """,
            )

            result = self.validator.validate_paths(
                [doc],
                changed_sections=[self.validator.ChangedSection(doc, 3, 25)],
            )

        self.assertFalse(result.has_errors)
        self.assertNotIn("MDREAD-001", {diagnostic.check_id for diagnostic in result.diagnostics})

    def test_generated_region_marker_pairing_and_source_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-marker-") as temp:
            valid = write_text(
                Path(temp) / "valid.md",
                """
                # Example

                <!-- rigorloop:generated:start surface=readme-vision source=VISION.md generator=scripts/sync.py -->
                Generated content.
                <!-- rigorloop:generated:end surface=readme-vision -->
                """,
            )
            invalid = write_text(
                Path(temp) / "invalid.md",
                """
                # Example

                <!-- rigorloop:generated:start surface=readme-vision source=VISION.md -->
                Generated content.
                <!-- rigorloop:generated:end surface=other-surface -->
                """,
            )
            missing_source = write_text(
                Path(temp) / "missing-source.md",
                """
                # Example

                <!-- rigorloop:generated:start surface=readme-vision -->
                Generated content.
                <!-- rigorloop:generated:end surface=readme-vision -->
                """,
            )

            valid_result = self.validator.validate_paths([valid])
            invalid_result = self.validator.validate_paths([invalid])
            source_result = self.validator.validate_paths([missing_source])

        self.assertFalse(valid_result.has_errors)
        self.assertTrue(invalid_result.has_errors)
        self.assertIn("MDREAD-004", {diagnostic.check_id for diagnostic in invalid_result.diagnostics})
        self.assertTrue(source_result.has_errors)
        self.assertIn("MDREAD-004", {diagnostic.check_id for diagnostic in source_result.diagnostics})

    def test_unchanged_historical_hard_wrap_is_audit_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-historical-") as temp:
            vision = write_text(
                Path(temp) / "VISION.md",
                """
                # Vision

                RigorLoop preserves proposal to
                spec traceability.
                """,
            )

            result = self.validator.validate_paths([vision])

        self.assertFalse(result.has_errors)
        self.assertIn("MDREAD-001", {diagnostic.check_id for diagnostic in result.diagnostics})
        self.assertTrue(all(diagnostic.severity != "error" for diagnostic in result.diagnostics))

    def test_generated_document_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-placeholder-") as temp:
            doc = write_text(
                Path(temp) / "generated.md",
                """
                # Generated

                ## Status

                <status>
                """,
            )

            result = self.validator.validate_paths([doc], generated_documents={doc})

        self.assertTrue(result.has_errors)
        self.assertIn("MDREAD-005", {diagnostic.check_id for diagnostic in result.diagnostics})

    def test_cli_changed_section_failure_and_help(self) -> None:
        with tempfile.TemporaryDirectory(prefix="mdread-cli-") as temp:
            readme = write_text(
                Path(temp) / "README.md",
                """
                # Example

                RigorLoop makes proposal to
                spec handoffs reviewable.
                """,
            )

            help_result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--help"],
                capture_output=True,
                text=True,
                cwd=ROOT,
                check=False,
            )
            fail_result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    str(readme),
                    "--changed-section",
                    f"{readme}:3:5",
                ],
                capture_output=True,
                text=True,
                cwd=ROOT,
                check=False,
            )

        self.assertEqual(help_result.returncode, 0, msg=help_result.stderr)
        self.assertIn("Validate Markdown readability", help_result.stdout)
        self.assertEqual(fail_result.returncode, 1)
        self.assertIn("MDREAD-001", fail_result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
