"""Private adapter inputs and explicit generation/install fixture operations."""

from __future__ import annotations

import sys
from pathlib import Path
import importlib.util
import hashlib
import os
import shutil
import subprocess
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging import adapter_distribution as adapter_distribution_module
from lib.packaging.adapter_distribution import ADAPTERS, sync_adapter_output


FIXTURES = ROOT / "tests/fixtures/adapters"
VALIDATE_RELEASE = ROOT / "scripts/validate-release.py"


def configure_adapter_case(add_cleanup) -> None:
    """Own the diagnostics of real installed CLI children for this case."""
    temporary = tempfile.TemporaryDirectory(prefix="adapter-case-")
    add_cleanup(temporary.cleanup)
    environment = patch.dict(os.environ, {
        "RIGORLOOP_LOG_DIR": str(Path(temporary.name) / "logs"),
    })
    environment.start()
    add_cleanup(environment.stop)


def load_validate_release_module():
    spec = importlib.util.spec_from_file_location("validate_release_test", VALIDATE_RELEASE)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def fixture_path(name: str) -> Path:
    return FIXTURES / name

def copy_fixture_skills(target: Path, names: tuple[str, ...]) -> Path:
    skills_root = target / "skills"
    skills_root.mkdir()
    for name in names:
        shutil.copytree(fixture_path(name), skills_root / name)
    return skills_root

def generate_fixture_adapters(
    root: Path,
    names: tuple[str, ...] = ("portable-basic", "transformable-frontmatter"),
    version: str = "0.1.0-rc.1",
) -> tuple[Path, Path]:
    skills_root = copy_fixture_skills(root, names)
    output_root = root / "dist" / "adapters"
    sync_adapter_output(version, skills_root=skills_root, output_root=output_root)
    return skills_root, output_root

def write_adapter_artifact_metadata(
    root: Path,
    release_output_dir: Path,
    *,
    version: str = "v0.1.2",
    source_commit: str = "0123456789abcdef0123456789abcdef01234567",
    artifact_overrides: dict[str, dict[str, str]] | None = None,
    combined_required: bool = False,
    validation_result: str = "pass",
    historical: bool = False,
) -> Path:
    metadata_root = root / "docs" / "reports" / "adapter-artifacts" / "releases"
    metadata_root.mkdir(parents=True, exist_ok=True)
    artifact_overrides = artifact_overrides or {}
    lines = [
        "schema_version: 1",
        "",
        "release:",
        f"  version: {version}",
        f"  source_commit: {source_commit}",
        '  date: "2026-05-13"',
        "",
        "generator:",
        f'  command: "python scripts/build-adapters.py --version {version} --output-dir <release-output-dir>"',
        '  source_skills: "skills/"',
        '  manifest: "dist/adapters/manifest.yaml"',
        "",
        "artifacts:",
    ]
    adapters = adapter_distribution_module.HISTORICAL_ADAPTERS if historical else ADAPTERS
    for adapter in adapters:
        archive = f"rigorloop-adapter-{adapter}-{version}.zip"
        archive_path = release_output_dir / archive
        sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        row = {
            "adapter": adapter,
            "archive": archive,
            "sha256": sha256,
            "install_root": adapters[adapter].skill_root.as_posix().rstrip("/") + "/",
            "result": "pass",
        }
        row.update(artifact_overrides.get(adapter, {}))
        lines.extend(
            [
                f"  - adapter: {row['adapter']}",
                f"    archive: {row['archive']}",
                f"    sha256: {row['sha256']}",
                f"    install_root: {row['install_root']}",
                f"    result: {row['result']}",
            ]
        )
    lines.extend(
        [
            "",
            "combined_artifact:",
            f"  required: {'true' if combined_required else 'false'}",
            f"  archive: rigorloop-adapters-{version}.tar.gz",
            '  sha256: ""',
            "  included_adapters:",
            *[f"    - {name}" for name in adapters],
            "",
            "validation:",
            f'  command: "python scripts/validate-adapters.py --root <release-output-dir> --version {version}"',
            f"  result: {validation_result}",
            '  validated_at: "2026-05-13"',
            "",
        ]
    )
    metadata_path = metadata_root / f"{version}.yaml"
    metadata_path.write_text("\n".join(lines), encoding="utf-8")
    return metadata_path

def clean_install_runner_with_resource_mutation(
    *,
    target: str,
    skill_name: str,
    relative_resource_path: str,
    mutation,
    real_runner=subprocess.run,
):
    def runner(command, **kwargs):
        result = real_runner(command, **kwargs)
        installed_target = command[command.index("init") + 1]
        if result.returncode != 0 or installed_target != target:
            return result

        project_root = Path(kwargs["cwd"])
        skill_root = project_root / Path(ADAPTERS[target].skill_root.as_posix()) / skill_name
        assert skill_root.is_dir(), skill_root
        assert (skill_root / "SKILL.md").is_file(), skill_root

        resource_path = skill_root / relative_resource_path
        assert resource_path.is_file(), resource_path
        mutation(resource_path)
        return result

    return runner
