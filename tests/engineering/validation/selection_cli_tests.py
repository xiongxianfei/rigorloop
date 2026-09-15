"""Selection cli observations; loaded by the supported aggregate TestCase."""
from __future__ import annotations

from selection_test_helpers import (
    ADAPTER_REGRESSION_COMMAND,
    CHANGE_METADATA_FAILING_TEST,
    CHANGE_METADATA_PASSING_TEST,
    CI,
    Path,
    ROOT,
    allocated_workers,
    json,
    os,
    parse_stdout,
    run_change_metadata_test,
    run_ci,
    run_selector,
    selected_ids,
    shutil,
    signal,
    subprocess,
    sys,
    tempfile,
)


class SelectionCliChecks:
    def test_cli_outputs_json_for_classified_skill_path(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "skills/code-review/SKILL.md")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["mode"], "explicit")
        self.assertEqual(payload["status"], "ok")
        for field in (
            "changed_paths",
            "classified_paths",
            "unclassified_paths",
            "selected_checks",
            "affected_roots",
            "broad_smoke_required",
            "blocking_results",
            "preflight_results",
            "rationale",
        ):
            self.assertIn(field, payload)
        self.assertIn(
            {"path": "skills/code-review/SKILL.md", "category": "skills"},
            payload["classified_paths"],
        )
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue(
            {
                "skills.validate",
                "skills.regression",
                "adapters.regression",
            }.issubset(selected_ids(payload))
        )
        self.assertIn("adapters.drift", selected_ids(payload))
        for check in payload["selected_checks"]:
            self.assertIn(check["phase"], {"focused", "boundary"})
            self.assertEqual(check["cache_status"], "not-applicable")


    def test_boundary_sibling_failures_each_block_selected_execution(self) -> None:
        cases = (
            (
                "boundary_first.validate",
                "python scripts/validate-boundary-first.py --check",
                "scripts/validate-boundary-first.py",
                ("--mode", "explicit", "--path", "scripts/lib/validation/boundary_first_validation.py"),
            ),
            (
                "current_records.validate",
                "python scripts/validate-governed-lifecycle-cli.py",
                "scripts/validate-governed-lifecycle-cli.py",
                ("--mode", "explicit", "--path", "docs/changes/example/change.yaml"),
            ),
            (
                "skills.validate",
                "python scripts/validate-skills.py",
                "scripts/validate-skills.py",
                ("--mode", "explicit", "--path", "skills/design/SKILL.md"),
            ),
            (
                "adapters.regression",
                ADAPTER_REGRESSION_COMMAND,
                "tests/engineering/packaging/test-adapter-distribution.py",
                ("--mode", "explicit", "--path", "dist/adapters/manifest.yaml"),
            ),
            (
                "rigorloop_cli.test",
                "npm test --prefix packages/rigorloop",
                "<fake-npm>",
                ("--mode", "explicit", "--path", "packages/rigorloop/package.json"),
            ),
            (
                "npm_package_publication.test",
                "python tests/engineering/packaging/test-npm-package-publication.py",
                "tests/engineering/packaging/test-npm-package-publication.py",
                ("--mode", "explicit", "--path", "packages/rigorloop/package.json"),
            ),
            (
                "release.validate",
                "python scripts/validate-release.py --recorded-source-auto --version v0.4.0",
                "scripts/validate-release.py",
                ("--mode", "release", "--release-version", "v0.4.0"),
            ),
            (
                "selector.regression",
                "python tests/engineering/validation/test-select-validation.py",
                "tests/engineering/validation/test-select-validation.py",
                ("--mode", "explicit", "--path", ".github/workflows/ci.yml"),
            ),
        )
        for check_id, command, script_path, args in cases:
            with self.subTest(check_id=check_id):
                workspace = self.make_ci_workspace()
                run_env = None
                if check_id == "rigorloop_cli.test":
                    fake_bin = workspace / "fake-bin"
                    fake_bin.mkdir()
                    fake_npm = fake_bin / "npm"
                    fake_npm.write_text(
                        "#!/bin/sh\necho 'injected sibling failure'\nexit 7\n",
                        encoding="utf-8",
                    )
                    fake_npm.chmod(0o755)
                    run_env = {"PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"}
                else:
                    self.write_fake_script(
                        workspace,
                        script_path,
                        "import sys\nprint('injected sibling failure')\nraise SystemExit(7)\n",
                    )
                fixture = self.write_selector_fixture(
                    self.minimal_selector_payload(
                        mode="release" if args[1] == "release" else "explicit",
                        selected_checks=[
                            self.selected_check(
                                check_id,
                                command,
                                **(
                                    {"paths": ["docs/changes/example/change.yaml"]}
                                    if check_id == "current_records.validate"
                                    else {"versions": ["v0.4.0"]}
                                    if check_id == "release.validate"
                                    else {}
                                ),
                            )
                        ],
                    )
                )

                result = self.run_workspace_ci(workspace, fixture, *args, env=run_env)
                output = str(result.stdout) + str(result.stderr)

                self.assertNotEqual(result.returncode, 0, msg=output)
                self.assertIn(f"Run selected check: {check_id}", output)
                self.assertIn(f"Selected check {check_id} failed", output)


    def test_cli_accepts_changed_file_alias_for_plan_validation_commands(self) -> None:
        result = run_selector("--mode", "explicit", "--changed-file", "README.md", "--changed-file", "VISION.md")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["README.md", "VISION.md"])
        self.assertIn("documentation_prose.enforce", selected_ids(payload))


    def test_missing_mode_specific_inputs_return_json_error(self) -> None:
        result = run_selector("--mode", "pr", "--base", "HEAD~1")
        self.assertEqual(result.returncode, 4)
        payload = parse_stdout(result)
        self.assertEqual(payload["status"], "error")
        self.assertIn("invalid-invocation", {item["code"] for item in payload["blocking_results"]})


    def test_unclassified_path_blocks_without_fail_open(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "experimental/runtime/example.txt")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotEqual(payload["status"], "ok")


    def test_mixed_classified_and_unclassified_paths_block_partial_execution(self) -> None:
        result = run_selector(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--path",
            "experimental/runtime/example.txt",
        )
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])


    def test_malformed_release_profile_paths_require_release_version(self) -> None:
        for path in (
            "docs/releases/profiles/not-a-version.yaml",
            "docs/releases/profiles/v0.4.0.yml",
            "docs/releases/profiles/v.yaml",
        ):
            with self.subTest(path=path):
                result = run_selector("--mode", "explicit", "--path", path)
                payload = parse_stdout(result)

                self.assertEqual(result.returncode, 2)
                self.assertEqual(payload["status"], "blocked")
                self.assertIn(
                    "release-version-required",
                    {item["code"] for item in payload["blocking_results"]},
                )
                self.assertNotIn("release.validate", selected_ids(payload))


    def test_release_evidence_markdown_path_selects_lifecycle_checklist_validation(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "docs/releases/v1.2.3.md")
        payload = parse_stdout(result)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "docs/releases/v1.2.3.md", "category": "release"}, payload["classified_paths"])
        self.assertNotIn(
            "manual-routing-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertNotIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertIn("release_evidence.validate", selected_ids(payload))
        lifecycle_check = next(
            check for check in payload["selected_checks"] if check["id"] == "release_evidence.validate"
        )
        self.assertEqual(
            lifecycle_check["command"],
            "python scripts/release_evidence.py docs/releases/v1.2.3.md",
        )


    def test_release_guidance_paths_do_not_require_release_version(self) -> None:
        result = run_selector(
            "--mode",
            "explicit",
            "--path",
            "docs/releases/README.md",
            "--path",
            "docs/releases/index.md",
        )
        payload = parse_stdout(result)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "ok")
        self.assertIn(
            {"path": "docs/releases/README.md", "category": "workflow-guidance"},
            payload["classified_paths"],
        )
        self.assertIn(
            {"path": "docs/releases/index.md", "category": "workflow-guidance"},
            payload["classified_paths"],
        )
        self.assertNotIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )


    def test_release_path_without_version_directory_blocks(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "docs/releases/release-notes.md")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn({"path": "docs/releases/release-notes.md", "category": "release"}, payload["classified_paths"])
        self.assertIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertNotIn("release.validate", selected_ids(payload))


    def test_project_map_paths_are_living_reference_not_lifecycle(self) -> None:
        cli_result = run_selector("--mode", "explicit", "--path", "docs/project-map.md")
        self.assertEqual(cli_result.returncode, 0, cli_result.stdout + cli_result.stderr)
        cli_payload = parse_stdout(cli_result)
        self.assertIn(
            {"path": "docs/project-map.md", "category": "living-reference/project-map"},
            cli_payload["classified_paths"],
        )
        self.assertEqual(cli_payload["unclassified_paths"], [])
        self.assertEqual(cli_payload["blocking_results"], [])

        paths = ["docs/project-map.md", "docs/project-map/release.md"]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn(
                    {"path": path, "category": "living-reference/project-map"},
                    payload["classified_paths"],
                )

        self.assertNotIn("current_records.validate", selected_ids(payload))
        self.assertEqual({"guide_system.validate"}, selected_ids(payload))


    def test_release_mode_selects_release_validation_and_broad_smoke(self) -> None:
        result = run_selector("--mode", "release", "--release-version", "v0.1.1")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn("release.validate", selected_ids(payload))
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "release"}, payload["broad_smoke"]["sources"])
        self.assertIn(
            {"type": "release_metadata", "path": "docs/releases/v0.1.1/release.yaml"},
            payload["broad_smoke"]["sources"],
        )


    def test_ci_wrapper_executes_selector_selected_path_and_root_checks(self) -> None:
        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md",
            "--path",
            "docs/changes/2026-08-31-retire-standalone-test-spec-stage/change.yaml",
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selector mode: explicit", output)
        self.assertIn("Preflight results:", output)
        self.assertIn("Run selected check: record_retirement.regression", output)
        self.assertIn("Phase: focused", output)
        self.assertIn("Selected CI phase timing summary:", output)
        self.assertNotIn("Run selected check: current_records.validate", output)
        self.assertIn("node --test packages/rigorloop/test/record-retirement.test.js", output)


    def test_ci_wrapper_fails_on_blocked_selector_without_partial_execution(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                status="blocked",
                selected_checks=[
                    {
                        "id": "current_records.validate",
                        "command": "python scripts/validate-governed-lifecycle-cli.py docs/changes/example/",
                        "reason": "must not run when selector is blocked",
                        "affected_roots": ["docs/changes/example/"],
                    }
                ],
                blocking_results=[
                    {
                        "code": "unclassified-path",
                        "path": "experimental/runtime/example.txt",
                        "message": "changed path is not classified by the v1 selector",
                    }
                ],
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "2"},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Selector status: blocked", output)
        self.assertIn("unclassified-path", output)
        self.assertNotIn("Run selected check: current_records.validate", output)


    def test_ci_wrapper_rejects_fallback_and_malformed_selector_output(self) -> None:
        fallback_fixture = self.write_selector_fixture(self.minimal_selector_payload(status="fallback"))
        fallback = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fallback_fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "3"},
        )
        fallback_output = fallback.stdout + fallback.stderr

        self.assertNotEqual(fallback.returncode, 0)
        self.assertIn("Selector status: fallback", fallback_output)
        self.assertIn("fallback execution is not supported in v1", fallback_output)

        malformed_fixture = self.write_selector_fixture("not json")
        malformed = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture)},
        )
        malformed_output = malformed.stdout + malformed.stderr

        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("Malformed selector JSON", malformed_output)


    def test_ci_wrapper_rejects_selector_command_mismatch(self) -> None:
        marker_root = Path(tempfile.mkdtemp(prefix="validation-selection-command-mismatch-"))
        self.addCleanupTree(marker_root)
        marker = marker_root / "executed"
        tampered_command = (
            f"{sys.executable} -c "
            f"\"from pathlib import Path; Path({str(marker)!r}).write_text('ran')\""
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "skills.validate",
                        "command": tampered_command,
                        "reason": "tampered selector command must not be trusted",
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("command does not match catalog", output)
        self.assertNotIn("Run selected check: skills.validate", output)
        self.assertFalse(marker.exists())


    def test_ci_wrapper_preserves_selected_command_failure(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release.py --recorded-source-auto --version missing-version",
                        "reason": "fixture release version should fail validation",
                        "versions": ["missing-version"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "missing-version",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("Selected check release.validate failed", output)


    def test_ci_wrapper_jobs_one_uses_stable_summary_and_hides_success_output(self) -> None:
        workspace = self.make_ci_workspace()
        order_file = workspace / "order.txt"
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-start\\n")
print("SKILLS_STDOUT")
print("SKILLS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-end\\n")
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-start\\n")
print("ADAPTERS_STDOUT")
print("ADAPTERS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-end\\n")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
            env={"ORDER_FILE": str(order_file)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(
            order_file.read_text(encoding="utf-8").splitlines(),
            ["skills-start", "skills-end", "adapters-start", "adapters-end"],
        )
        self.assertIn("Selected CI check summary:", output)
        self.assertIn("skills.regression | passed | ok |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(
            output.index("skills.regression | passed | ok |"),
            output.index("adapters.regression | passed | ok |"),
        )
        self.assertNotIn("SKILLS_STDOUT", output)
        self.assertNotIn("ADAPTERS_STDERR", output)
        self.assertIn("Selected CI checks passed.", output)


    def test_ci_wrapper_parallel_safe_checks_run_concurrently_with_cap(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "tests/skill/test-skill-validator.py", "skills")
        self.write_active_counter_script(workspace, "tests/engineering/packaging/test-adapter-distribution.py", "adapters")
        self.write_active_counter_script(
            workspace,
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
            "artifact-lifecycle",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "governed_lifecycle_cli_wrapper.test",
                        "python tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
                    ),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "2",
            env={"ACTIVE_DIR": str(active_dir), "EXPECTED_ACTIVE_OVERLAP": str(allocated_workers(2))},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), allocated_workers(2), msg=(active_dir / "events.txt").read_text(encoding="utf-8"))
        self.assertLess(
            output.index("skills.regression | passed | ok |"),
            output.index("adapters.regression | passed | ok |"),
        )
        self.assertLess(
            output.index("adapters.regression | passed | ok |"),
            output.index("governed_lifecycle_cli_wrapper.test | passed | ok |"),
        )


    def test_ci_wrapper_default_budget_is_capped_and_parent_allocation_bounds_override(self):
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        for extra, parent, expected in (([], None, 4), (["--jobs", "8"], "2", 2)):
            env = {"RIGORLOOP_SELECTOR_FIXTURE": str(fixture), "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "8"}
            if parent:
                env["RIGORLOOP_VALIDATION_WORKERS"] = str(allocated_workers(int(parent)))
            result = run_ci("--mode", "explicit", "--path", "README.md", *extra, env=env)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertIn(f"Worker budget: {allocated_workers(expected)}", result.stdout)


    def test_ci_wrapper_default_jobs_uses_cpu_minus_one_fixture(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "tests/skill/test-skill-validator.py", "skills")
        self.write_active_counter_script(workspace, "tests/engineering/packaging/test-adapter-distribution.py", "adapters")
        self.write_active_counter_script(
            workspace,
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
            "artifact-lifecycle",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "governed_lifecycle_cli_wrapper.test",
                        "python tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
                    ),
                ]
            )
        )

        one_cpu = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            env={
                "ACTIVE_DIR": str(active_dir),
                "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "1",
            },
        )
        assert isinstance(one_cpu.stdout, str)
        self.assertEqual(one_cpu.returncode, 0, msg=one_cpu.stdout + one_cpu.stderr)
        self.assertEqual(self.read_max_active(active_dir), 1)

        shutil.rmtree(active_dir, ignore_errors=True)
        three_cpu = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            env={
                "ACTIVE_DIR": str(active_dir),
                "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "3",
                "EXPECTED_ACTIVE_OVERLAP": str(allocated_workers(2)),
            },
        )
        assert isinstance(three_cpu.stdout, str)
        self.assertEqual(three_cpu.returncode, 0, msg=three_cpu.stdout + three_cpu.stderr)
        self.assertEqual(self.read_max_active(active_dir), allocated_workers(2))


    def test_ci_wrapper_non_allowlisted_checks_run_alone(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "tests/skill/test-skill-validator.py", "skills-regression")
        self.write_active_counter_script(workspace, "scripts/validate-boundary-first.py", "boundary-validate")
        self.write_active_counter_script(workspace, "tests/engineering/packaging/test-adapter-distribution.py", "adapters-regression")
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("boundary_first.validate", "python scripts/validate-boundary-first.py --check"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "4",
            env={"ACTIVE_DIR": str(active_dir)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), 1)
        self.assertIn("boundary_first.validate | passed | ok |", output)


    def test_ci_wrapper_parallel_default_waits_for_started_check_after_failure(self) -> None:
        workspace = self.make_ci_workspace()
        marker_dir = workspace / "markers"
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "skills-started").write_text("started", encoding="utf-8")
deadline = time.monotonic() + 2
while int(os.environ["EXPECTED_PEER_WORKERS"]) > 1 and not (marker_dir / "adapters-started").exists():
    if time.monotonic() > deadline:
        raise SystemExit(9)
    time.sleep(0.02)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "adapters-started").write_text("started", encoding="utf-8")
time.sleep(0.3)
(marker_dir / "adapters-finished").write_text("finished", encoding="utf-8")
print("adapters finished")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "2",
            env={"MARKER_DIR": str(marker_dir), "EXPECTED_PEER_WORKERS": str(allocated_workers(2))},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((marker_dir / "adapters-finished").exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)


    def test_ci_wrapper_fail_fast_reports_queued_checks_not_started(self) -> None:
        workspace = self.make_ci_workspace()
        marker_dir = workspace / "markers"
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "skills-started").write_text("started", encoding="utf-8")
deadline = time.monotonic() + 2
while int(os.environ["EXPECTED_PEER_WORKERS"]) > 1 and not (marker_dir / "adapters-started").exists():
    if time.monotonic() > deadline:
        raise SystemExit(9)
    time.sleep(0.02)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "adapters-started").write_text("started", encoding="utf-8")
time.sleep(0.3)
(marker_dir / "adapters-finished").write_text("finished", encoding="utf-8")
print("adapters finished")
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
            """
import os
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "artifact-started").write_text("started", encoding="utf-8")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "governed_lifecycle_cli_wrapper.test",
                        "python tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
                    ),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "2",
            "--fail-fast",
            env={"MARKER_DIR": str(marker_dir), "EXPECTED_PEER_WORKERS": str(allocated_workers(2))},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((marker_dir / "adapters-finished").exists(), allocated_workers(2)>1, msg=output)
        self.assertFalse((marker_dir / "artifact-started").exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | " + ("passed | ok |" if allocated_workers(2)>1 else "not started | fail-fast cancelled remaining queue |"), output)
        self.assertIn(
            "governed_lifecycle_cli_wrapper.test | not started | fail-fast cancelled remaining queue | 0.00s",
            output,
        )


    def test_ci_wrapper_run_to_completion_reports_failed_output_after_summary(self) -> None:
        workspace = self.make_ci_workspace()
        marker = workspace / "second-ran.txt"
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import sys

print("FIRST_STDOUT")
print("FIRST_STDERR", file=sys.stderr)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            """
import os
from pathlib import Path

Path(os.environ["SECOND_MARKER"]).write_text("ran", encoding="utf-8")
print("SECOND_STDOUT")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
            env={"SECOND_MARKER": str(marker)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(marker.exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(output.index("Selected CI check summary:"), output.index("Failed selected check output:"))
        self.assertIn("==> skills.regression (exited)", output)
        self.assertIn("--- stdout ---", output)
        self.assertIn("FIRST_STDOUT", output)
        self.assertIn("--- stderr ---", output)
        self.assertIn("FIRST_STDERR", output)
        self.assertNotIn("SECOND_STDOUT", output)


    def test_ci_wrapper_verbose_prints_successful_output_in_stable_order(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            "import sys\nprint('SKILL_VERBOSE_STDOUT')\nprint('SKILL_VERBOSE_STDERR', file=sys.stderr)\n",
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            "print('ADAPTER_VERBOSE_STDOUT')\n",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
            "--verbose",
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selected check output:", output)
        self.assertLess(output.index("==> skills.regression (passed)"), output.index("==> adapters.regression (passed)"))
        self.assertIn("SKILL_VERBOSE_STDOUT", output)
        self.assertIn("SKILL_VERBOSE_STDERR", output)
        self.assertIn("ADAPTER_VERBOSE_STDOUT", output)


    def test_broad_smoke_routes_changed_records_to_current_v3_validator(self):
        workspace = self.make_broad_smoke_workspace(child_bodies={
            "scripts/validate-governed-lifecycle-cli.py": "raise SystemExit(0)\n",
            "scripts/validate-change-metadata.py":
                "import sys\nassert sys.argv[1:] == ['docs/changes/example/change.json'], sys.argv\n",
        })
        # Other children isolate wrapper dispatch; current-v3 validation itself
        # is exercised by record-store tests and the real repository smoke.
        result = run_ci("--mode", "broad-smoke", script=workspace / "scripts/ci.sh", cwd=workspace)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


    def test_broad_smoke_skips_unrelated_historical_descendants(self):
        workspace = self.make_broad_smoke_workspace(child_bodies={
            "scripts/validate-governed-lifecycle-cli.py": "raise SystemExit(0)\n",
            "scripts/validate-change-metadata.py": "raise SystemExit(9)\n",
        })
        current = workspace / "docs/changes/example/change.json"
        current.unlink()
        historical = workspace / "docs/changes/example/broad-smoke-child-classification.yaml"
        historical.write_text("historical: unchanged-schema\n")
        subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "historical operational input"], cwd=workspace, check=True, capture_output=True)
        historical.write_text("historical: changed-operational-input\n")
        result = run_ci("--mode", "broad-smoke", script=workspace / "scripts/ci.sh", cwd=workspace)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("9 checks passed", result.stdout)
        explicit = run_ci("--mode", "broad-smoke", env={"REVIEW_ARTIFACT_ROOTS": "docs/changes/example/"},
                          script=workspace / "scripts/ci.sh", cwd=workspace)
        self.assertEqual(explicit.returncode, 9, explicit.stdout + explicit.stderr)


    def test_broad_smoke_reserved_missing_manifest_is_not_skipped(self):
        workspace = self.make_broad_smoke_workspace(child_bodies={
            "scripts/validate-change-metadata.py": "raise SystemExit(9)\n",
        })
        (workspace / "docs/changes/example/change.json").unlink()
        residue = workspace / "docs/changes/example/evidence.json"
        residue.write_text("{}\n")
        subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "reserved residue"], cwd=workspace, check=True, capture_output=True)
        residue.write_text('{"broken":true}\n')
        result = run_ci("--mode", "broad-smoke", script=workspace / "scripts/ci.sh", cwd=workspace)
        self.assertEqual(result.returncode, 9, result.stdout + result.stderr)


    def test_broad_smoke_failed_build_prevents_archive_validation(self):
        workspace = self.make_broad_smoke_workspace(failing_child="scripts/build-adapters.py",
            child_bodies={"scripts/validate-adapters.py":"from pathlib import Path; Path('archive-ran').touch()"})
        result = run_ci("--mode","broad-smoke","--jobs","2",script=workspace/"scripts/ci.sh",cwd=workspace)
        self.assertEqual(result.returncode,7,result.stdout+result.stderr)
        self.assertFalse((workspace/"archive-ran").exists())
        self.assertIn("failed prerequisite: broad_smoke.adapters.build_archives",result.stdout)
        self.assertIn("validation_execution.regression | passed",result.stdout)


    def test_selected_broad_smoke_is_one_invocation_and_diagnostic_failure_remains(self):
        workspace = self.make_broad_smoke_workspace(failing_child="tests/skill/test-skill-validator.py",
            child_bodies={"scripts/validate-skills.py":"from pathlib import Path; Path('broad-ran').touch()"})
        wrapper = workspace/"scripts/ci.sh"
        wrapper.write_text(wrapper.read_text().replace('cd "$ROOT_DIR"','cd "$ROOT_DIR"\nprintf "called\\n" >> "$INVOCATIONS"'))
        marker = workspace/'broad-ran'
        invocations = workspace/'invocations'
        for diagnostic in (False,True):
            marker.unlink(missing_ok=True)
            invocations.unlink(missing_ok=True)
            payload = self.minimal_selector_payload(selected_checks=[
                self.selected_check('skills.regression','python tests/skill/test-skill-validator.py'),
                self.selected_check('broad_smoke.repo','bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped')])
            payload['broad_smoke']['sources'] = [{'type':'explicit_flag','value':'--broad-smoke'}] if diagnostic else []
            fixture = self.write_selector_fixture(payload)
            result = self.run_workspace_ci(workspace,fixture,'--mode','explicit','--path','README.md','--jobs','2',env={'INVOCATIONS':str(invocations)})
            self.assertEqual(result.returncode,7,result.stdout+result.stderr)
            self.assertEqual(marker.exists(),diagnostic,result.stdout+result.stderr)
            self.assertEqual(invocations.read_text().splitlines(),['called'])
            self.assertIn('skills.validate',result.stdout)


    def test_blocked_selection_diagnostic_broad_smoke_cannot_clear_original_blocker(self):
        workspace = self.make_broad_smoke_workspace(child_bodies={"scripts/validate-skills.py":"from pathlib import Path; Path('diagnostic-ran').touch()"})
        payload = self.minimal_selector_payload(status='blocked',blocking_results=[{'code':'manual-routing-required'}])
        payload['broad_smoke']['sources'] = [{'type':'explicit_flag','value':'--broad-smoke'}]
        fixture = self.write_selector_fixture(payload)
        result = self.run_workspace_ci(workspace,fixture,'--mode','explicit','--path','unknown.txt','--jobs','2')
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        self.assertTrue((workspace/'diagnostic-ran').exists(),result.stdout+result.stderr)
        self.assertIn('original selector blocker remains unsuccessful',result.stdout)


    def test_broad_smoke_default_success_captures_child_output_and_prints_aggregate(self) -> None:
        workspace = self.make_broad_smoke_workspace()

        result = run_ci(
            "--mode",
            "broad-smoke",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        nonempty_lines = [line for line in output.splitlines() if line.strip()]
        self.assertEqual(len(nonempty_lines), 1, msg=output)
        self.assertRegex(nonempty_lines[0], r"^\[PASS\] broad-smoke: 10 checks passed in \d+(?:\.\d+)?s$")
        self.assertNotIn("STDOUT marker", output)
        self.assertNotIn("STDERR marker", output)
        self.assertNotIn("==>", output)
        self.assertNotIn("--quiet", output)


    def test_broad_smoke_omitted_jobs_uses_assessed_default_concurrency(self) -> None:
        active_children = {
            "scripts/validate-skills.py",
            "tests/skill/test-skill-validator.py",
        }
        workspace = self.make_broad_smoke_workspace(active_counter_children=active_children)
        active_dir = workspace / "active"

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            env={"ACTIVE_DIR": str(active_dir), "EXPECTED_ACTIVE_OVERLAP": str(allocated_workers(2)), "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "8"},
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), allocated_workers(2), msg=output)


    def test_broad_smoke_jobs_one_keeps_sequential_compatibility(self) -> None:
        active_children = {
            "scripts/validate-skills.py",
            "tests/skill/test-skill-validator.py",
        }
        workspace = self.make_broad_smoke_workspace(active_counter_children=active_children)
        active_dir = workspace / "active"

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "1",
            env={"ACTIVE_DIR": str(active_dir)},
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), 1, msg=output)


    def test_broad_smoke_explicit_jobs_parallelizes_eligible_children(self) -> None:
        active_children = {
            "scripts/validate-skills.py",
            "tests/skill/test-skill-validator.py",
        }
        workspace = self.make_broad_smoke_workspace(active_counter_children=active_children)
        active_dir = workspace / "active"

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "2",
            env={"ACTIVE_DIR": str(active_dir), "EXPECTED_ACTIVE_OVERLAP": str(allocated_workers(2))},
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), allocated_workers(2), msg=output)
        self.assertRegex(output, r"^\[PASS\] broad-smoke: 9 checks passed in \d+(?:\.\d+)?s")


    def test_broad_smoke_failure_prints_command_exit_duration_and_captured_output(self) -> None:
        workspace = self.make_broad_smoke_workspace(failing_child="tests/skill/test-skill-validator.py")

        result = run_ci(
            "--mode",
            "broad-smoke",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 7, msg=output)
        self.assertRegex(output, r"\[FAIL\] skills.regression / Run skill validator fixtures: exit 7 in \d+(?:\.\d+)?s")
        self.assertIn("Command:\npython tests/skill/test-skill-validator.py", output)
        self.assertIn("Captured output:", output)
        stdout_index = output.index("test-skill-validator.py STDOUT marker")
        stderr_index = output.index("test-skill-validator.py STDERR marker")
        self.assertLess(stdout_index, stderr_index)


    def test_broad_smoke_parallel_multiple_failures_report_all_in_canonical_order(self) -> None:
        workspace = self.make_broad_smoke_workspace(
            failing_children={
                "tests/skill/test-skill-validator.py",
                "scripts/validate-governed-lifecycle-cli.py",
                "tests/engineering/packaging/test-adapter-distribution.py",
            }
        )

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "4",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 7, msg=output)
        first_failure = output.index("[FAIL] skills.regression")
        second_failure = output.index("[FAIL] adapters.full_regression")
        self.assertLess(first_failure, second_failure)
        self.assertIn("Execution phase:\n" + ("parallel" if allocated_workers(2)>1 else "sequential"), output)
        self.assertIn("Execution phase:\nsequential", output)
        self.assertIn("[FAIL] current_records.validate", output)
        self.assertIn("Check ID:\nskills.regression", output)
        self.assertIn("Check ID:\nadapters.full_regression", output)
        self.assertIn("Captured output:", output)
        self.assertIn("Re-run:\npython tests/skill/test-skill-validator.py", output)


    def test_broad_smoke_parallel_runs_without_historical_classification(self) -> None:
        workspace = self.make_broad_smoke_workspace()
        self.assertFalse((workspace / "docs/changes/2026-06-27-broad-smoke-safe-parallelism").exists())

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "2",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("[PASS] broad-smoke", output)
        self.assertNotIn("STDOUT marker", output)


    def test_broad_smoke_parallel_worker_crash_reports_scheduler_error(self) -> None:
        workspace = self.make_broad_smoke_workspace(
            child_bodies={
                "tests/skill/test-skill-validator.py": """
import os
import signal

os.kill(os.getppid(), signal.SIGKILL)
""".lstrip()
            }
        )

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "2",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 4, msg=output)
        self.assertIn("[FAIL] skills.regression / Run skill validator fixtures: exit 4", output)
        self.assertIn("runner error", output)
        self.assertIn("missing task outcome", output)
        self.assertNotIn("[PASS] broad-smoke", output)


    def test_broad_smoke_verbose_prints_successful_child_output_in_order(self) -> None:
        workspace = self.make_broad_smoke_workspace()

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--verbose",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertRegex(output, r"\[PASS\] broad-smoke: 10 checks passed in \d+(?:\.\d+)?s")
        self.assertLess(output.index("validate-skills.py STDOUT marker"), output.index("test-skill-validator.py STDOUT marker"))
        self.assertIn("validate-skills.py STDERR marker", output)
        self.assertIn("test-skill-validator.py STDERR marker", output)


    def test_broad_smoke_parallel_verbose_groups_successful_child_output_in_order(self) -> None:
        active_children = {
            "scripts/validate-skills.py",
            "tests/skill/test-skill-validator.py",
        }
        workspace = self.make_broad_smoke_workspace(active_counter_children=active_children)
        active_dir = workspace / "active"

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "4",
            "--verbose",
            env={"ACTIVE_DIR": str(active_dir), "EXPECTED_ACTIVE_OVERLAP": str(allocated_workers(2))},
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), allocated_workers(2), msg=output)
        self.assertLess(output.index("==> Validate canonical skills (passed)"), output.index("==> Run skill validator fixtures (passed)"))
        self.assertLess(output.index("validate-skills.py done"), output.index("test-skill-validator.py done"))
        self.assertNotRegex(output, r"validate-skills.py done.*==> Run skill validator fixtures", msg=output)


    def test_broad_smoke_parallel_result_evidence_records_child_phases(self) -> None:
        workspace = self.make_broad_smoke_workspace()
        result_path = workspace / "parallel-result.json"

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--skip-diff-scoped",
            "--jobs",
            "3",
            env={"RIGORLOOP_BROAD_SMOKE_RESULT_JSON": str(result_path)},
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        with result_path.open(encoding="utf-8") as handle:
            evidence = json.load(handle)
        self.assertEqual(evidence["scenario"], "broad-smoke-safe-parallelism")
        self.assertEqual(evidence["parallel"]["jobs"], allocated_workers(3))
        child_phases = {
            child["check_id"]: child["phase"]
            for child in evidence["parallel"]["child_durations"]
        }
        self.assertEqual(child_phases["skills.validate"], "parallel" if allocated_workers(3)>1 else "sequential")
        self.assertEqual(child_phases["adapters.full_regression"], "parallel" if allocated_workers(3)>1 else "sequential")
        self.assertIn("delta", evidence)


    def test_change_metadata_validator_default_success_is_compact(self) -> None:
        result = run_change_metadata_test(CHANGE_METADATA_PASSING_TEST)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(result.stderr, "")
        nonempty_lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(nonempty_lines), 1, msg=output)
        self.assertRegex(
            nonempty_lines[0],
            r"^\[PASS\] test-change-metadata-validator: 1 passed in \d+(?:\.\d+)?s$",
        )
        self.assertNotIn("test_explicit_recording_metadata_accepts_structure_without_stage_eligibility", output)
        self.assertNotIn(" ... ok", output)


    def test_change_metadata_validator_default_failure_is_actionable(self) -> None:
        result = run_change_metadata_test(
            CHANGE_METADATA_FAILING_TEST,
            env={"RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE": "1"},
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, msg=output)
        self.assertIn("[FAIL] test-change-metadata-validator: 1 failed, 0 passed", output)
        self.assertIn("FAILED ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure", output)
        self.assertIn("AssertionError: intentional output-contract failure", output)
        self.assertIn("tests/engineering/validation/test-change-metadata-validator.py:", output)
        self.assertNotIn("test_explicit_recording_metadata_accepts_structure_without_stage_eligibility", output)


    def test_change_metadata_validator_verbose_preserves_full_detail(self) -> None:
        for flag in ("--verbose", "-v"):
            with self.subTest(flag=flag):
                result = run_change_metadata_test(flag, CHANGE_METADATA_PASSING_TEST)
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                self.assertIn("test_explicit_recording_metadata_accepts_structure_without_stage_eligibility", output)
                self.assertIn(" ... ok", output)
                self.assertIn("Ran 1 test", output)
                self.assertIn("OK", output)


    def test_change_metadata_validator_quiet_compatibility_is_preserved(self) -> None:
        for flag in ("--quiet", "-q"):
            with self.subTest(flag=flag):
                result = run_change_metadata_test(flag, CHANGE_METADATA_PASSING_TEST)

                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertIn("Ran 1 test", result.stderr)
                self.assertIn("OK", result.stderr)
                self.assertNotIn("[PASS] test-change-metadata-validator", result.stderr)


    def test_change_metadata_validator_zero_selected_tests_fail(self) -> None:
        result = run_change_metadata_test("-k", "no_such_test_name")
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, msg=output)
        self.assertIn(
            "[FAIL] test-change-metadata-validator: 0 tests run; expected at least 1 selected test",
            output,
        )


    def test_ci_wrapper_reports_decode_failures_without_emitting_invalid_bytes(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import sys

sys.stdout.buffer.write(b"valid-before-stdout\\n")
sys.stdout.buffer.write(b"bad-stdout-\\xff\\n")
sys.stderr.buffer.write(b"bad-stderr-\\xfe\\n")
raise SystemExit(1)
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
            text=False,
        )
        assert isinstance(result.stdout, bytes)
        combined = result.stdout + result.stderr
        output = combined.decode("utf-8")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skills.regression | exited | exit code 1; stdout decode error; stderr decode error |", output)
        self.assertIn("--- stdout (decode error; replacement text) ---", output)
        self.assertIn("bad-stdout-", output)
        self.assertIn("--- stderr (decode error; replacement text) ---", output)
        self.assertIn("bad-stderr-", output)


    def test_ci_wrapper_keeps_large_output_isolated_per_check(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            """
import sys

sys.stdout.write("SKILLS_STDOUT_BEGIN\\n")
sys.stdout.write("skills-stdout-line\\n" * 5000)
sys.stderr.write("skills-stderr-line\\n" * 5000)
sys.stdout.write("SKILLS_STDOUT_END\\n")
raise SystemExit(2)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "tests/engineering/packaging/test-adapter-distribution.py",
            """
import sys

sys.stdout.write("ADAPTERS_STDOUT_BEGIN\\n")
sys.stdout.write("adapters-stdout-line\\n" * 5000)
sys.stderr.write("adapters-stderr-line\\n" * 5000)
sys.stdout.write("ADAPTERS_STDOUT_END\\n")
raise SystemExit(3)
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        skills_start = output.index("==> skills.regression (exited)")
        adapters_start = output.index("==> adapters.regression (exited)")
        skills_section = output[skills_start:adapters_start]
        adapters_section = output[adapters_start:]

        self.assertIn("skills.regression | exited | exit code 2 |", output)
        self.assertIn("adapters.regression | exited | exit code 3 |", output)
        self.assertIn("SKILLS_STDOUT_BEGIN", skills_section)
        self.assertIn("skills-stderr-line", skills_section)
        self.assertNotIn("ADAPTERS_STDOUT_BEGIN", skills_section)
        self.assertIn("ADAPTERS_STDOUT_BEGIN", adapters_section)
        self.assertIn("adapters-stderr-line", adapters_section)
        self.assertNotIn("SKILLS_STDOUT_BEGIN", adapters_section)


    def test_ci_wrapper_timeout_and_signal_failures_have_distinct_statuses(self) -> None:
        workspace = self.make_ci_workspace()
        self.assertRegex(
            (workspace / "scripts" / "ci.sh").read_text(encoding="utf-8"),
            r"(?m)^DEFAULT_TIMEOUT_SECONDS=300$",
        )
        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            "import time\nprint('before-timeout', flush=True)\ntime.sleep(5)\n",
        )
        timeout_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                ]
            )
        )

        timed_out = self.run_workspace_ci(
            workspace,
            timeout_fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
            "--timeout",
            "1",
        )
        assert isinstance(timed_out.stdout, str)
        timeout_output = timed_out.stdout + timed_out.stderr

        self.assertNotEqual(timed_out.returncode, 0)
        self.assertIn("skills.regression | timed out | timeout after 1s |", timeout_output)
        self.assertIn("before-timeout", timeout_output)

        self.write_fake_script(
            workspace,
            "tests/skill/test-skill-validator.py",
            f"import os, signal\nos.kill(os.getpid(), {signal.SIGTERM})\n",
        )
        signal_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python tests/skill/test-skill-validator.py"),
                ]
            )
        )

        killed = self.run_workspace_ci(
            workspace,
            signal_fixture,
            "--mode",
            "explicit",
            "--path",
            "tests/skill/test-skill-validator.py",
            "--jobs",
            "1",
        )
        assert isinstance(killed.stdout, str)
        signal_output = killed.stdout + killed.stderr

        self.assertNotEqual(killed.returncode, 0)
        self.assertIn("skills.regression | killed | signal SIGTERM (15) |", signal_output)


    def test_ci_wrapper_reports_unavailable_selected_command(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-ci-missing-"))
        self.addCleanupTree(temp_root)
        (temp_root / "scripts").mkdir()
        shutil.copy2(CI, temp_root / "scripts" / "ci.sh")
        shutil.copytree(ROOT / "scripts/lib", temp_root / "scripts/lib", ignore=shutil.ignore_patterns("__pycache__"))
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release.py --recorded-source-auto --version v0.1.1",
                        "reason": "fixture command should be unavailable in the temporary workspace",
                        "versions": ["v0.1.1"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "v0.1.1",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
            script=temp_root / "scripts" / "ci.sh",
            cwd=temp_root,
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("release.validate | unavailable | command unavailable: scripts/validate-release.py |", output)


    def test_ci_wrapper_forwards_mode_arguments_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-trace-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                ["--mode", "release", "--release-version", "v0.1.1"],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
            (
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)


    def test_pr_mode_runs_selected_checks_instead_of_full_product_graph(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload(mode="pr"))
        trace = Path(tempfile.mkdtemp(prefix="validation-selected-pr-")) / "selector-argv.txt"
        self.addCleanupTree(trace.parent)
        result = run_ci("--mode", "pr", "--base", "base-sha", "--head", "head-sha",
                        env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                             "RIGORLOOP_CI_DIRECT_DRY_RUN": "1",
                             "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace)})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(trace.exists(), "PR must consult the selector")
        self.assertEqual(trace.read_text().splitlines()[-6:],
                         ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"])
        self.assertIn("Selector mode: pr", result.stdout)
        self.assertNotIn("Gate B: adapter parity regressions", result.stdout)


    def test_pr_wrapper_executes_exact_lifecycle_range_and_preserves_failure(self) -> None:
        workspace = self.make_ci_workspace()
        marker = workspace / "argv.json"
        self.write_fake_script(workspace, "scripts/validate-governed-lifecycle-cli.py",
                               "import json, os, sys\nfrom pathlib import Path\n"
                               "Path(os.environ['ARGV_MARKER']).write_text(json.dumps(sys.argv[1:]))\n"
                               "sys.exit(int(os.environ['CHECK_EXIT']))\n")
        for exit_code in (0, 7):
            with self.subTest(exit_code=exit_code):
                payload = self.minimal_selector_payload(mode="pr", selected_checks=[{
                    "id": "current_records.snapshot", "paths": ["docs/plans/example.md"],
                    "command": "python scripts/validate-governed-lifecycle-cli.py --revision head-sha",
                }])
                fixture = self.write_selector_fixture(payload)
                result = run_ci("--mode", "pr", "--base", "base-sha", "--head", "head-sha",
                                env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                                     "ARGV_MARKER": str(marker), "CHECK_EXIT": str(exit_code)},
                                script=workspace / "scripts/ci.sh", cwd=workspace)
                self.assertEqual(result.returncode, exit_code, result.stdout + result.stderr)
                self.assertEqual(json.loads(marker.read_text()),
                                 ["--revision", "head-sha"])
        marker.unlink()
        payload["selected_checks"][0]["command"] = payload["selected_checks"][0]["command"].replace("head-sha", "other-sha")
        fixture = self.write_selector_fixture(payload)
        result = run_ci("--mode", "pr", "--base", "base-sha", "--head", "head-sha",
                        env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture), "ARGV_MARKER": str(marker), "CHECK_EXIT": "0"},
                        script=workspace / "scripts/ci.sh", cwd=workspace)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("command does not match catalog", result.stderr)
        self.assertFalse(marker.exists())


    def test_pr_wrapper_rejects_selector_mode_substitution(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload(mode="explicit"))
        result = run_ci("--mode", "pr", "--base", "base-sha", "--head", "head-sha",
                        env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)})
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("Selector mode does not match", result.stderr)


    def test_main_mode_uses_direct_lifecycle_scope(self) -> None:
        result = run_ci(
            "--mode",
            "main",
            "--base",
            "before-sha",
            "--head",
            "after-sha",
            env={"RIGORLOOP_CI_DIRECT_DRY_RUN": "1"},
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, output)
        self.assertIn(
            "python scripts/validate-governed-lifecycle-cli.py --revision after-sha",
            output,
        )
        self.assertNotIn("scripts/select-validation.py", output)


    def test_ci_wrapper_accepts_execution_flags_without_forwarding_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                [
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    "--jobs",
                    "2",
                    "--timeout",
                    "60",
                    "--fail-fast",
                    "--verbose",
                ],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md"],
            ),
            (
                [
                    "--mode",
                    "release",
                    "--release-version",
                    "v0.1.1",
                    "--fail-fast",
                    "--jobs",
                    "3",
                ],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)

        broad_smoke = run_ci(
            "--mode",
            "broad-smoke",
            "--jobs",
            "1",
            "--timeout",
            "60",
            "--fail-fast",
            "--verbose",
            env={"RIGORLOOP_CI_BROAD_SMOKE_STUB": "1"},
        )
        self.assertEqual(broad_smoke.returncode, 0, msg=broad_smoke.stdout + broad_smoke.stderr)
        self.assertIn("Broad smoke stub", broad_smoke.stdout + broad_smoke.stderr)


    def test_ci_wrapper_rejects_invalid_execution_flags_before_selector(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
                        "reason": "must not run when wrapper arguments are invalid",
                    }
                ]
            )
        )
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-invalid-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            ("--jobs", "0"),
            ("--jobs", "-1"),
            ("--jobs", "abc"),
            ("--jobs", ""),
            ("--jobs", "unlimited"),
            ("--timeout", "0"),
            ("--timeout", "-1"),
            ("--timeout", "abc"),
            ("--timeout", ""),
        ]

        for flag, value in cases:
            with self.subTest(flag=flag, value=value):
                if trace.exists():
                    trace.unlink()
                result = run_ci(
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    flag,
                    value,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                        "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
                    },
                )
                output = result.stdout + result.stderr

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"Invalid {flag}", output)
                self.assertFalse(trace.exists(), msg=output)
                self.assertNotIn("Selector mode:", output)
                self.assertNotIn("Run selected check:", output)


    def test_ci_wrapper_delegates_broad_smoke_non_recursively(self) -> None:
        malformed_fixture = self.write_selector_fixture("not json")
        direct = run_ci(
            "--mode",
            "broad-smoke",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        direct_output = direct.stdout + direct.stderr

        self.assertEqual(direct.returncode, 0, msg=direct_output)
        self.assertIn("Broad smoke stub", direct_output)
        self.assertNotIn("Malformed selector JSON", direct_output)

        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
                        "reason": "Broad smoke is required by an authoritative source.",
                    }
                ]
            )
        )
        selected = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--verbose",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        selected_output = selected.stdout + selected.stderr

        self.assertEqual(selected.returncode, 0, msg=selected_output)
        self.assertIn("Run selected check: broad_smoke.repo", selected_output)
        self.assertIn("Broad smoke stub", selected_output)


    def test_output_contract_red_tests_are_unmasked_and_separate(self) -> None:
        source = (ROOT / "tests/engineering/validation/test-select-validation.py").read_text(encoding="utf-8")
        contract_section = source.split("class ScriptOutputContractTests", 1)[1].split(
            "class ValidationSelectionTests",
            1,
        )[0]

        self.assertNotIn("@unittest.expectedFailure", contract_section)
        self.assertIn("class ScriptOutputContractTests", source)
