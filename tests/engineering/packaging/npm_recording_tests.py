"""Ordered recording transactions through a real packed binary in both installed targets."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from npm_fixture_helpers import (
    ROOT, PACKAGE_ROOT, RELEASE_TAG,
    TARGET_SKILL_ROOTS, run_command, pack_package, configure_npm_case,
)


class PackedRecordingTests(unittest.TestCase):
    def setUp(self):
        configure_npm_case(self.addCleanup)

    def test_installed_target_supports_explicit_and_primary_recording(self):
        with tempfile.TemporaryDirectory(prefix="rigorloop-npm-pack-") as pack_temp, tempfile.TemporaryDirectory(
            prefix="rigorloop-npm-install-"
        ) as install_temp, tempfile.TemporaryDirectory(prefix="rigorloop-npm-project-") as project_temp, tempfile.TemporaryDirectory(
            prefix="rigorloop-npm-release-output-"
        ) as release_temp:
            tarball = pack_package(Path(pack_temp))
            release_output = Path(release_temp)
            build_result = run_command(
                ["python", "scripts/build-adapters.py", "--version", RELEASE_TAG, "--output-dir", str(release_output)]
            )
            self.assertEqual(build_result.returncode, 0, build_result.stderr)

            install_root = Path(install_temp)
            install = run_command(["npm", "install", "--prefix", str(install_root), str(tarball)])
            self.assertEqual(install.returncode, 0, install.stderr)

            bin_path = install_root / "node_modules" / ".bin" / "rigorloop"
            self.assertTrue(bin_path.exists())
            self.assertNotEqual(bin_path.resolve(), (PACKAGE_ROOT / "dist" / "bin" / "rigorloop.js").resolve())


            binary = bin_path
            for target in ("codex", "claude"):
                with self.subTest(target=target):
                    project = Path(project_temp) / target
                    project.mkdir()
                    archive = release_output / f"rigorloop-adapter-{target}-{RELEASE_TAG}.zip"
                    installed = run_command(
                        [str(binary), "init", target, "--from-archive", str(archive), "--json"], cwd=project,
                    )
                    self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
                    self.assertTrue((project / TARGET_SKILL_ROOTS[target]).is_dir())
                    package = binary.resolve().parents[2]
                    templates = json.loads((package / "dist/templates/rigorloop-records-v3/records.json").read_text())
                    self.assertEqual((package / "dist/templates/rigorloop-records-v3/records.json").read_bytes(),
                                     (ROOT / "templates/rigorloop-records-v3/records.json").read_bytes())
                    self.assertTrue((package / "dist/schemas/rigorloop-records-v3.schema.json").is_file())
                    (project / "docs/changes").mkdir(parents=True)
                    manifest = project / "docs/changes/example/change.json"
                    change = templates["change"]
                    change["schema_version"] = 3
                    change["change_id"] = "example"
                    change["records"] = []
                    change["applicability"] = []
                    change["contract"] = "rigorloop-records-v3"
                    change["activity"]["reason"] = "Explicit installed-package test decision"
                    content = json.dumps(change) + "\n"
                    request = {"schema_version": 2, "contract": "rigorloop-records-v3", "change_id": "example",
                               "expected_revision": None, "writes": [{"path": "docs/changes/example/change.json",
                               "expected_identity": None, "content": content}], "reads": []}

                    def invoke(operation: str, request_data=None, *, change_id="example", extra=(), expected=0):
                        args = [str(binary), "record-store", operation, "--root", str(project), "--change", change_id, "--format", "json", *extra]
                        if request_data is not None:
                            args.extend(["--input", "-"])
                        result = subprocess.run(args, cwd=project, input=None if request_data is None else json.dumps(request_data) + "\n",
                                                capture_output=True, text=True, check=False)
                        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                        payload = json.loads(result.stdout)
                        self.assertEqual(payload["claim"], "storage-only")
                        return payload

                    self.assertEqual(invoke("inspect")["revision"], None)
                    for extra in (("--no-file-log",), ("--console-log-level", "unknown_value")):
                        rejected = invoke("record", request, extra=extra, expected=2)
                        self.assertEqual(rejected["status"], "rejected")
                        self.assertEqual(rejected["errors"][0]["code"], "invalid-input")
                        self.assertEqual(rejected["files"], [])
                        self.assertIsNone(rejected["snapshot"])
                        self.assertFalse(manifest.exists())
                    self.assertEqual(invoke("check", request)["status"], "valid")
                    self.assertFalse(manifest.exists())
                    self.assertEqual(invoke("record", request)["status"], "saved")
                    self.assertEqual(manifest.read_text(), content)
                    self.assertEqual(invoke("record", request, expected=3)["status"], "conflict")
                    before = invoke("inspect")
                    self.assertEqual(before["snapshot"]["records"][0]["content"], content)
                    text_result = run_command([str(binary), "record-store", "inspect", "--root", str(project),
                                               "--change", "example", "--format", "text"], cwd=project)
                    self.assertEqual(text_result.returncode, 0, text_result.stdout + text_result.stderr)
                    self.assertIn(f'Revision: {before["revision"]}\n', text_result.stdout)
                    for record_file in before["files"]:
                        self.assertIn(f'{record_file["path"]}: {record_file["identity"]}\n', text_result.stdout)
                    request["expected_revision"] = before["revision"]
                    request["writes"][0]["expected_identity"] = before["files"][0]["identity"]
                    change["activity"].update(stage="design", status="in-progress", reason="Explicitly reopen")
                    request["writes"][0]["content"] = json.dumps(change) + "\n"

                    # Inject interruption into the packed dispatcher; recovery and competing
                    # writers still enter through the real installed public binary.
                    launcher = project / "interrupt.mjs"
                    launcher.write_text(
                        'import {main} from ' + json.dumps(binary.resolve().as_uri()) + ';\n'
                        'import {spawnSync} from "node:child_process";\n'
                        'const args=JSON.parse(process.env.TEST_ARGS), input=process.env.TEST_INPUT;\n'
                        'await main(args,{recordStoreOptions:{fault:point=>{\n'
                        'if(point==="after-preparation"){const c=spawnSync(process.env.TEST_BIN,args,{input,encoding:"utf8"});'
                        'if(c.status!==4)throw Error("competing writer did not report busy");}\n'
                        'if(point==="after-replace:0")process.exit(99);}}});\n'
                    )
                    args = ["record-store", "record", "--root", str(project), "--change", "example", "--format", "json", "--input", "-"]
                    for action in ("restore", "complete"):
                        env = {**os.environ, "TEST_BIN": str(binary), "TEST_ARGS": json.dumps(args), "TEST_INPUT": json.dumps(request) + "\n"}
                        interrupted = subprocess.run(["node", str(launcher)], cwd=project, input=json.dumps(request) + "\n", env=env,
                                                     capture_output=True, text=True, check=False)
                        self.assertEqual(interrupted.returncode, 99, interrupted.stdout + interrupted.stderr)
                        blocked = invoke("inspect", expected=5)
                        self.assertIsNone(blocked["snapshot"])
                        tx = blocked["transaction"]
                        self.assertEqual(invoke("recover", extra=("--transaction", tx["id"], "--expected-recovery", tx["recovery_identity"], "--action", action))["status"], "recovered")
                        self.assertEqual(manifest.read_text(), content if action == "restore" else request["writes"][0]["content"])

                    # A write-stop keeps this reader available and preserves every byte.
                    preserved = manifest.read_bytes()
                    invoke("inspect")
                    self.assertEqual(manifest.read_bytes(), preserved)
                    for contract in ("stage-owned-change-local-v3", "compact-current-state-v1", "unknown_value"):
                        old = project / "docs/changes/historical"
                        old.mkdir(exist_ok=True)
                        old_record = old / "change.yaml"
                        raw = json.dumps({"lifecycle_contract": contract}) + "\n"
                        old_record.write_text(raw)
                        invoke("inspect", change_id="historical", expected=2)
                        bad = {**request, "change_id": "historical", "expected_revision": None,
                               "writes": [{"path": "docs/changes/historical/change.json", "expected_identity": None, "content": content}]}
                        invoke("record", bad, change_id="historical", expected=2)
                        self.assertEqual(old_record.read_text(), raw)
                    for contract in ("unknown_value", "compact-current-state-v1"):
                        bad = {**request, "contract": contract}
                        invoke("record", bad, expected=2)
                        self.assertEqual(manifest.read_bytes(), preserved)
                    self.assertFalse((project / ".git").exists())
                    package = binary.resolve().parents[2]
                    for relative, canonical in (
                        ("dist/templates/rigorloop-records-v3/records.json", "templates/rigorloop-records-v3/records.json"),
                        ("dist/schemas/rigorloop-records-v3.schema.json", "schemas/rigorloop-records-v3.schema.json"),
                        ("dist/schemas/targeted-recording-v1.schema.json", "schemas/targeted-recording-v1.schema.json"),
                    ):
                        self.assertEqual((package / relative).read_bytes(), (ROOT / canonical).read_bytes())
                    def invoke(words, data=None, expected=0, change="primary"):
                        args = [str(binary), *words, "--root", str(project), "--change", change, "--format", "json"]
                        if data is not None:
                            args.extend(["--input", "-"])
                        r = subprocess.run(args, cwd=project, input=None if data is None else json.dumps(data) + "\n",
                                           capture_output=True, text=True)
                        self.assertEqual(r.returncode, expected, r.stdout + r.stderr)
                        result = json.loads(r.stdout)
                        self.assertEqual(result["claim"], "storage-only")
                        return result
                    basis = project / "primary-basis.md"
                    basis.write_text("Installed-package decision basis.\n")
                    subject = {"path": basis.name, "identity": "sha256:" + hashlib.sha256(basis.read_bytes()).hexdigest()}
                    inspected = subprocess.run([str(binary), "subject", "inspect", "--root", str(project),
                                                "--path", basis.name, "--content", "full", "--format", "json"],
                                               cwd=project, capture_output=True, text=True)
                    self.assertEqual(inspected.returncode, 0, inspected.stdout + inspected.stderr)
                    self.assertEqual(json.loads(inspected.stdout)["data"]["subjects"], [subject])
                    actor = {"id": "tester", "role": "implement"}
                    operation = {"op": "change.create", "target": {}, "values": {
                        "proposal": subject, "models": [], "plan": None, "work": [], "blockers": [],
                        "activity": {"stage": "implement", "status": "in-progress", "owner": actor, "reason": "Explicit package fixture."}}}
                    request = {"schema_version": 1, "interface": "targeted-recording-v1", "contract": "rigorloop-records-v3",
                               "change_id": "primary", "expected_revision": None, "reads": [subject], "operation": operation}
                    self.assertEqual(invoke(["change", "create"], request)["status"], "saved")
                    context = invoke(["context"], {"schema_version": 1, "select": [{"kind": "activity", "where": {}}]})
                    self.assertEqual(context["record_contract"], "rigorloop-records-v3")
                    request["expected_revision"] = context["revision"]
                    request["operation"] = {"op": "verify.record", "target": {}, "values": {
                        "verifier": {"id": "verifier", "role": "verify"}, "subjects": [], "evidence_refs": [], "review_refs": [],
                        "outcome": "success", "summary": "Explicit installed-package explanation.\n", "assessment_scope": "Package fixture", "rationale": ["Supplied fixture evidence"], "limitations": [], "changes": ["Named fields available"]},
                        "applicability": {"value": "current", "actor": actor, "reason": "Explicit fixture declaration."}}
                    self.assertEqual(invoke(["verify", "record"], request)["status"], "saved")
                    self.assertEqual(invoke(["verify", "show"])["data"]["items"][0]["fields"]["summary"],
                                     "Explicit installed-package explanation.\n")
                    self.assertTrue((project / "docs/changes/primary/change.json").is_file())
                    self.assertFalse((project / "docs/changes/primary/change.yaml").exists())
                    for unsupported in ("explicit-recording-v1", "unknown_value"):
                        bad = {**request, "contract": unsupported, "change_id": "absent", "expected_revision": None,
                               "operation": operation}
                        invoke(["change", "create"], bad, expected=2, change="absent")
                        self.assertFalse((project / "docs/changes/absent").exists())
                    projected = invoke(["verify", "show", "--fields", "summary,limitations"])
                    self.assertEqual(projected["schema_version"], 3)
                    self.assertEqual(sorted(projected["data"]["items"][0]["fields"]), ["limitations", "summary"])
                    self.assertTrue(projected["scope"]["omitted_fields"])
                    request["expected_revision"] = projected["revision"]
                    request["operation"] = {"op": "verify.set", "target": {}, "values": {"limitations": ["Packaged caller scope"]}}
                    self.assertEqual(invoke(["verify", "set"], request)["status"], "saved")
                    # The primary reader reports the installed-package v3 store.
                    self.assertEqual(invoke(["status"], change="example")["record_contract"], "rigorloop-records-v3")
