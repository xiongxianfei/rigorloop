"""Actual packed v2/v4 CLI, installed workflow and maintenance qualification."""
from __future__ import annotations
import json
import os
import tempfile
import unittest
from pathlib import Path
from npm_fixture_helpers import ROOT, RELEASE_TAG, TARGET_SKILL_ROOTS, run_command, pack_package, configure_npm_case

class PackedRecordingTests(unittest.TestCase):
    def setUp(self):
        configure_npm_case(self.addCleanup)

    def test_packed_successor_workflow_records_and_maintenance(self):
        with tempfile.TemporaryDirectory(prefix="rigorloop-packed-successor-") as temporary:
            root = Path(temporary)
            tarball = pack_package(root)
            installed = run_command(["npm", "install", "--prefix", str(root / "installed"), str(tarball)])
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            binary = root / "installed/node_modules/.bin/rigorloop"
            package = binary.resolve().parents[2]
            for relative in ("schemas/rigorloop-records-v4.schema.json", "schemas/targeted-recording-v2.schema.json", "schemas/store-maintenance-v1.schema.json", "templates/shared/rigorloop-workflow.json"):
                self.assertEqual((package / "dist" / relative).read_bytes(), (ROOT / relative).read_bytes())
            for target, skill_root in TARGET_SKILL_ROOTS.items():
                project = root / target
                project.mkdir()
                for name in ("proposal", "proposal-review", "design"):
                    old = project / skill_root / name
                    old.mkdir(parents=True)
                    (old / "custom.md").write_text("customized " + name)
                archive = root / "archives" / f"rigorloop-adapter-{target}-{RELEASE_TAG}.zip"
                base = [str(binary), "init", target, "--from-archive", str(archive), "--json", "--no-file-log"]
                refused = run_command(base + ["--force"], cwd=project)
                self.assertNotEqual(refused.returncode, 0)
                self.assertEqual(json.loads(refused.stdout)["blockers"][0]["code"], "workflow-replacement-required")
                adopted = run_command(base + ["--replace-workflow", "requirement-first-v1", "--force"], cwd=project)
                self.assertEqual(adopted.returncode, 0, adopted.stdout + adopted.stderr)
                result = json.loads(adopted.stdout)
                self.assertEqual(result["schema_version"], 2)
                retired = [row for row in result["unit_results"] if row["action"] == "retire"]
                self.assertEqual(len(retired), 3)
                for row in retired:
                    self.assertEqual(row["outcome"], "completed")
                    self.assertFalse((project / row["path"]).exists())
                    self.assertEqual((Path(row["retained_path"]) / "custom.md").read_text(), "customized " + Path(row["path"]).name)
                for name in ("requirement-analysis", "requirement-review", "system-design", "architecture-design", "code-review", "verify"):
                    self.assertTrue((project / skill_root / name / "SKILL.md").is_file())
                self.assertFalse((project / "rigorloop-workflow.json").exists())
                self.assertFalse((project / ".rigorloop/rigorloop.db").exists())
            checked = run_command(["node", "--test", "packages/rigorloop/test/operational-review.test.js", "packages/rigorloop/test/operational-maintenance.test.js"], env={**os.environ, "RIGORLOOP_TEST_PACKAGED_BIN": str(binary)})
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
