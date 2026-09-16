"""Fresh Skill input builders and explicit validator assertion helpers.

Callers own temporary roots, defining mutations and validator invocations.
Assertions receive observed results and independent expected diagnostics."""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
from lib.validation import skill_validation


def write_asset_fixture(
    root: Path,
    skill_name: str,
    assets: dict[str, str],
    resource_entries: str | None = None,
) -> Path:
    skill_dir = root / skill_name
    skill_dir.mkdir(parents=True)
    if resource_entries is None:
        resource_entries = "\n".join(
            [
                f"- COPY `{relative_path}` when producing the related artifact structure.\n"
                f"  Fill: structural fields for {relative_path}.\n"
                "  Do not emit unfilled placeholders."
                for relative_path in sorted(assets)
            ]
        )
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {skill_name}",
                "description: Validate spec-family asset packaging.",
                "---",
                "",
                f"# {skill_name}",
                "",
                "## Resource map",
                "",
                resource_entries.rstrip(),
                "",
                "## Expected output",
                "",
                "Compact output summary.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for relative_path, content in assets.items():
        asset_path = skill_dir / relative_path
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        asset_path.write_text(textwrap.dedent(content), encoding="utf-8")
    return skill_dir


def asset_text(
    *,
    template: str,
    skill: str,
    status: str = "normative",
    body: str = "| <field> | <value> |\n",
    include_metadata: bool = True,
) -> str:
    metadata = ""
    if include_metadata:
        metadata = textwrap.dedent(
            f"""\
            <!-- Template: {template} -->
            <!-- Skill: {skill} -->
            <!-- Template status: {status} -->
            <!-- Maintained alongside: skills/{skill}/SKILL.md -->

            """
        )
    return metadata + textwrap.dedent(body)


def proposal_family_asset_text(
    *,
    template: str,
    skill: str,
    status: str = "normative",
    body: str = "| <field> | <value> |\n",
    include_metadata: bool = True,
) -> str:
    return asset_text(
        template=template,
        skill=skill,
        status=status,
        body=body,
        include_metadata=include_metadata,
    )


def review_family_asset_text(
    *,
    template: str,
    skill: str,
    status: str = "normative",
    body: str = "| <field> | <value> |\n",
    include_metadata: bool = True,
) -> str:
    return asset_text(
        template=template,
        skill=skill,
        status=status,
        body=body,
        include_metadata=include_metadata,
    )


def write_resource_integrity_skill(
    root: Path,
    *,
    resource_entries: str,
    resources: dict[str, str] | None = None,
    body_extra: str = "",
    skill_name: str = "resource-integrity-fixture",
) -> Path:
    skill_dir = root / skill_name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {skill_name}",
                "description: Validate mapped skill-local resource integrity.",
                "---",
                "",
                f"# {skill_name}",
                "",
                "## Resource map",
                "",
                textwrap.dedent(resource_entries).strip(),
                "",
                "## Expected output",
                "",
                "Compact output summary.",
                "",
                body_extra.strip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    for relative_path, content in (resources or {}).items():
        resource_path = skill_dir / relative_path
        resource_path.parent.mkdir(parents=True, exist_ok=True)
        resource_path.write_text(textwrap.dedent(content), encoding="utf-8")
    return skill_dir


def copy_ci_maintenance_fixture(root: Path) -> Path:
    source = ROOT / "skills" / "ci-maintenance"
    target = root / "ci-maintenance"
    shutil.copytree(source, target)
    return target


def project_map_contract_fixture_errors(skill_dir: Path) -> list[str]:
    skill_path = skill_dir / "SKILL.md"
    metadata, body = skill_validation.load_skill_file(skill_path)
    return skill_validation.validate_project_map_contract_fixture(
        skill_path,
        metadata,
        body,
    )


def assert_validation_passes(case, result) -> None:
    case.assertEqual(
        result.returncode, 0,
        msg=f"expected validator success\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )


def assert_validation_fails(case, result, expected_text: str) -> None:
    case.assertNotEqual(
        result.returncode, 0,
        msg=f"expected validator failure\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
    )
    case.assertIn(expected_text, f"{result.stdout}\n{result.stderr}")


def assert_contract_errors(case, errors: list[str], expected_text: str) -> None:
    case.assertTrue(errors, "expected contract validation errors")
    case.assertIn(expected_text, "\n".join(errors))
