"""Actual archive membership, byte parity and archive integrity."""

from __future__ import annotations

import sys
from pathlib import Path
import hashlib
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging import adapter_distribution as adapter_distribution_module
from lib.packaging.adapter_distribution import ADAPTERS, POST_CUTOVER_ADAPTER_SKILLS, RETIRED_PROGRESSION_SKILLS, SUPPORTED_ADAPTERS, adapter_archive_name, build_adapter_archives, validate_adapter_archives, validate_adapter_output, validate_clean_install_smoke
from adapter_fixture_helpers import (configure_adapter_case)


class AdapterArchiveTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        configure_adapter_case(self.addCleanup)

    def test_distribution_archives_have_independent_complete_resource_inventory(self) -> None:
        # Independent filesystem oracle: do not use the producer's inventory helper.
        canonical = {path.relative_to(ROOT / "skills").as_posix(): path.read_bytes()
                     for path in (ROOT / "skills").rglob("*") if path.is_file()}
        with tempfile.TemporaryDirectory() as tmp:
            archives = build_adapter_archives("v1.0.0", Path(tmp))
            self.assertEqual(validate_adapter_archives("v1.0.0", Path(tmp)), [])
            # One actual candidate/install operation covers the formerly separate
            # discovery and requirement happy paths; assertions inspect installed resources.
            self.assertEqual(validate_clean_install_smoke(
                "v1.0.0", Path(tmp), skill_names=("explore", "research", "requirement-analysis", "requirement-review")), [])
            self.assertEqual(len(archives), 2)
            for target, archive_path in zip(("codex", "claude"), archives):
                prefix = {"codex": ".agents/skills/", "claude": ".claude/skills/"}[target]
                with zipfile.ZipFile(archive_path) as archive:
                    actual = {name[len(prefix):]: archive.read(name) for name in archive.namelist() if name.startswith(prefix)}
                self.assertEqual(set(actual), set(canonical), target)
                # Full emitted entrypoints include transformed Claude frontmatter;
                # canonical guidance checks and body parity alone cannot guard it.
                for skill_name in ("explore", "research"):
                    for forbidden in (b"skills/explore/SKILL.md", b"skills/research/SKILL.md",
                                      b"templates/shared", b"dist/adapters"):
                        self.assertNotIn(forbidden, actual[f"{skill_name}/SKILL.md"])
                for name, expected in canonical.items():
                    if target == "codex" or not name.endswith("/SKILL.md"):
                        self.assertEqual(actual[name], expected, f"{target}/{name}")
                    else:
                        # Only declared frontmatter transformations are permitted;
                        # structural metadata checks run when building the archive.
                        self.assertEqual(actual[name].split(b"---", 2)[2], expected.split(b"---", 2)[2], name)


if __name__ == "__main__":
    unittest.main()
