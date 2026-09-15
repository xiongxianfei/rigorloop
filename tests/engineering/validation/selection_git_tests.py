"""Selection git observations; loaded by the supported aggregate TestCase."""
from __future__ import annotations

from selection_test_helpers import (
    Path,
    ROOT,
    SelectionRequest,
    json,
    parse_stdout,
    run_selector,
    select_validation,
    selected_ids,
    shlex,
    shutil,
    subprocess,
    tempfile,
)


class SelectionGitChecks:
    def test_v3_registered_paths_select_owner_and_unknown_value_versions_fail_closed(self):
        repo = self.make_git_repo()
        source = ROOT / "docs/design/cli/examples/records/v3-complete-store"
        target = repo / "docs/changes/example-change"
        for file in source.rglob("*.json"):
            destination = target / file.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(file.read_bytes())
        path = "docs/changes/example-change/reviews/final-code-review.json"
        selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertEqual(selected.status, "ok", selected.blocking_results)
        checks = {c["id"] for c in selected.selected_checks}
        self.assertIn("change_metadata.validate", checks)
        self.assertNotIn("current_records.validate", checks)
        manifest = target / "change.json"
        value = json.loads(manifest.read_text())
        value["schema_version"] = 2
        manifest.write_text(json.dumps(value) + "\n")
        selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertTrue(any(x["code"] == "unsupported-change-contract" for x in selected.blocking_results))


    def test_manifest_discriminator_unknown_value_types_fail_closed(self):
        repo = self.make_git_repo()
        path = "docs/changes/example/change.json"
        manifest = repo / path
        manifest.parent.mkdir(parents=True)
        for field in ("schema_version", "contract"):
            for invalid in ([], {}, None, True, "unknown_value"):
                with self.subTest(field=field, invalid=invalid):
                    value = {"schema_version": 3, "contract": "rigorloop-records-v3"}
                    value[field] = invalid
                    manifest.write_text(json.dumps(value) + "\n")
                    selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
                    self.assertEqual(selected.status, "blocked")
                    self.assertTrue(any(x["code"] == "unsupported-change-contract" for x in selected.blocking_results))


    def test_v3_registered_json_paths_select_contract_owned_validator(self):
        repo, _ = self.recording_repo()
        shutil.rmtree(repo / "docs/changes/example")
        (repo / "docs/changes").mkdir(parents=True, exist_ok=True)
        fixture = json.loads((ROOT / "tests/fixtures/rigorloop-records-v3/records.json").read_text())
        # Supported synthetic fixture.
        for write in fixture["request"]["writes"]:
            destination = repo / write["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(write["content"])
        for write in fixture["request"]["writes"]:
            selected = select_validation(SelectionRequest(mode="explicit", paths=(write["path"],), repo_root=repo))
            self.assertEqual(selected.status, "ok", selected.blocking_results)
            checks = {c["id"]: c for c in selected.selected_checks}
            self.assertIn("docs/changes/example/change.json", checks["change_metadata.validate"]["command"])
            self.assertNotIn("current_records.validate", checks)

        (repo / "docs/plan.md").write_text("# Plan index\n")
        (repo / "docs/plan-archive.md").write_text("# Plan archive\n")
        subprocess.run(["git", "add", "docs"], cwd=repo, check=True, capture_output=True)
        paths = ("docs/plan.md", *(write["path"] for write in fixture["request"]["writes"]))
        selected = select_validation(SelectionRequest(mode="explicit", paths=paths, repo_root=repo))
        self.assertEqual(selected.status, "ok", selected.blocking_results)
        checks = {c["id"]: c for c in selected.selected_checks}
        self.assertIn("docs/changes/example/change.json", checks["change_metadata.validate"]["command"])
        self.assertEqual(checks["current_records.validate"]["command"], "python scripts/validate-governed-lifecycle-cli.py")
        self.assertNotIn("docs/changes/example/change.yaml", checks["current_records.validate"]["command"])


    def test_supporting_subject_selection_preserves_records_for_changed_and_deleted_files(self):
        repo, path, _ = self.supporting_subject_repo()
        records = {p: p.read_bytes() for p in (repo / "docs/changes/example").glob("*.json")}
        for deleted in (False, True):
            if deleted:
                (repo / path).unlink()
            result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
            self.assertEqual(result.status, "ok", result.blocking_results)
            self.assertIn("change_metadata.validate", selected_ids(result.to_json_dict()))
            if deleted:
                self.assertNotIn("documentation_prose.enforce", selected_ids(result.to_json_dict()))
            else:
                self.assertIn("documentation_prose.enforce", selected_ids(result.to_json_dict()))
            self.assertEqual(records, {p: p.read_bytes() for p in records})


    def test_supporting_subject_selection_rejects_mixed_unknown_and_reinspects_each_invocation(self):
        repo, path, evidence = self.supporting_subject_repo()
        unknown = "docs/changes/example/unknown_value.md"
        result = select_validation(SelectionRequest(mode="explicit", paths=(path, unknown), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(b["path"] == unknown for b in result.blocking_results))
        value = json.loads(evidence.read_text())
        value["checks"][0]["subjects"] = [s for s in value["checks"][0]["subjects"] if s["path"] != path]
        evidence.write_text(json.dumps(value) + "\n")
        result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(b["code"] == "unregistered-recording-path" for b in result.blocking_results))


    def test_supporting_subject_selection_rejects_malformed_registered_store(self):
        repo, path, evidence = self.supporting_subject_repo()
        value = json.loads(evidence.read_text())
        value["schema_version"] = "unknown_value"
        evidence.write_text(json.dumps(value) + "\n")
        result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(b["code"] == "invalid-supporting-subject-store" for b in result.blocking_results))


    def test_supporting_subject_selection_rejects_dangling_registered_entry_reference(self):
        repo, path, _ = self.supporting_subject_repo()
        decisions = repo / "docs/changes/example/material-decisions.json"
        value = json.loads(decisions.read_text())
        value["decisions"][0]["source_refs"] = [{"path": "docs/changes/example/evidence.json", "id": "unknown-check"}]
        decisions.write_text(json.dumps(value) + "\n")
        result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(b["code"] == "invalid-supporting-subject-store" for b in result.blocking_results))


    def test_supporting_subject_validator_rejects_unknown_value_and_mixed_options(self):
        repo, path, _ = self.supporting_subject_repo()
        command = ["node", str(ROOT / "scripts/validate-record-store.mjs"), str(repo / "docs/changes/example/change.json")]
        normal = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(normal.returncode, 0, normal.stderr)
        subjects = subprocess.run(command + ["--subjects"], capture_output=True, text=True)
        self.assertEqual(subjects.returncode, 0, subjects.stderr)
        self.assertIn(path, json.loads(subjects.stdout)["subject_paths"])
        for options in (["--unknown-value"], ["--subjects", "--revision", "HEAD"]):
            result = subprocess.run(command + options, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


    def test_supporting_subject_selection_cannot_promote_unregistered_reserved_record(self):
        repo, path, _ = self.supporting_subject_repo("docs/changes/example/reviews/unregistered.json")
        result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(b["code"] == "unregistered-recording-path" for b in result.blocking_results))


    def test_supporting_subject_selection_rejects_escaping_symlink(self):
        repo, path, _ = self.supporting_subject_repo()
        (repo / path).unlink()
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "notes.md"
            target.write_text("outside\n")
            (repo / path).symlink_to(target)
            result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
            self.assertEqual(result.status, "blocked")
            self.assertTrue(any(b["code"] == "outside-repository-path" for b in result.blocking_results))


    def test_er_m5_001_real_recording_paths_select_complete_set_validation(self):
        repo, paths = self.recording_repo()
        for path in paths:
            with self.subTest(path=path):
                result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
                self.assertEqual(result.status, "ok", result.blocking_results)
                checks = {check["id"]: check for check in result.selected_checks}
                self.assertIn("change_metadata.validate", checks)
                self.assertIn("docs/changes/example/change.json", checks["change_metadata.validate"]["command"])
                self.assertNotIn("current_records.validate", checks)


    def test_er_m5_001_local_selection_ignores_private_recorder_state_only(self):
        repo, paths = self.recording_repo()
        result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        self.assertFalse(any(path.startswith(".rigorloop/record-store/") for path in result.changed_paths))
        self.assertTrue(set(paths) <= set(result.changed_paths))
        self.assertEqual(result.status, "ok", result.blocking_results)
        private = ".rigorloop/unknown_value/state"
        (repo / private).parent.mkdir(parents=True)
        (repo / private).write_text("not excluded\n")
        result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        self.assertIn(private, result.unclassified_paths)


    def test_er_m5_001_unknown_value_contract_and_unregistered_paths_fail_closed(self):
        repo, _ = self.recording_repo()
        unknown = "docs/changes/example/unknown_value.md"
        result = select_validation(SelectionRequest(mode="explicit", paths=(unknown,), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        manifest = repo / "docs/changes/example/change.json"
        value = json.loads(manifest.read_text())
        value["contract"] = "unknown_value"
        manifest.write_text(json.dumps(value) + "\n")
        result = select_validation(SelectionRequest(mode="explicit", paths=("docs/changes/example/evidence.json",), repo_root=repo))
        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(block["code"] == "unsupported-change-contract" for block in result.blocking_results))


    def test_moved_design_selection_does_not_hide_present_or_symlink_source(self):
        old = "docs/design/skill/design.md"
        for kind in ("file", "symlink", "dangling"):
            with self.subTest(kind=kind):
                repo = self.make_git_repo()
                source = repo / old
                source.parent.mkdir(parents=True)
                if kind == "file":
                    source.write_text("# Invalid old model\n")
                else:
                    target = repo / "target.md"
                    if kind == "symlink":
                        target.write_text("# Target\n")
                    source.symlink_to(target)
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                selected = select_validation(SelectionRequest(mode="explicit", paths=(old,), repo_root=repo))
                if kind != "file":
                    self.assertEqual(selected.status, "blocked", selected.to_json_dict())
                    continue
                command = shlex.split(next(c["command"] for c in selected.selected_checks if c["id"] == "model.validate"))
                self.assertIn(old, command)


    def test_model_selection_validates_present_historical_flat_input(self):
        repo = self.make_git_repo()
        for owner in ("docs/design/skill/workflow.md", "docs/design/cli/cli.md", "docs/design/cli/records.md"):
            (repo / owner).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / owner, repo / owner)
        flat = "docs/design/workflow.md"
        (repo / flat).write_text("# Invalid historical model\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        selected = select_validation(SelectionRequest(mode="explicit", paths=(flat,), repo_root=repo))
        command = shlex.split(next(c["command"] for c in selected.selected_checks if c["id"] == "model.validate"))
        self.assertIn(flat, command)
        # Execute the selected paths through the real validator at the fixture root.
        command[1] = str(ROOT / command[1])
        checked = subprocess.run(command, cwd=repo, capture_output=True, text=True)
        self.assertNotEqual(checked.returncode, 0, checked.stdout)
        self.assertIn(flat, checked.stdout + checked.stderr)


    def test_model_selection_rejects_historical_flat_symlink(self):
        for dangling in (False, True):
            with self.subTest(dangling=dangling):
                repo = self.make_git_repo()
                flat = repo / "docs/design/workflow.md"
                flat.parent.mkdir(parents=True)
                target = repo / "target.md"
                if not dangling:
                    target.write_text("# Target\n")
                flat.symlink_to(target)
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                result = select_validation(SelectionRequest(mode="explicit", paths=(str(flat),), repo_root=repo))
                self.assertEqual(result.status, "blocked", result.to_json_dict())


    def test_deleted_isolated_prose_keeps_proof_without_reading_deleted_file(self):
        path = "docs/reviews/explicit-recording-m3-code-review.md"
        for committed in (False, True):
            with self.subTest(committed=committed):
                repo = self.make_git_repo()
                file = repo / path
                file.parent.mkdir(parents=True)
                file.write_text("# Historical review\n")
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "historical review"], cwd=repo, check=True, capture_output=True)
                file.unlink()
                if committed:
                    subprocess.run(["git", "commit", "-am", "remove unsupported review location"], cwd=repo, check=True, capture_output=True)
                selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
                checks = {c["id"]: c for c in selected.selected_checks}
                self.assertNotIn("documentation_prose.audit", checks)
                self.assertTrue({"model.validate", "rigorloop_cli.test"} <= checks.keys())


    def test_proven_lifecycle_deletion_keeps_regression_without_reading_absent_file(self):
        for path in ("specs/rigorloop-cli-lockfile.md", "docs/adr/ADR-20260516-rigorloop-cli-lockfile.md"):
            for committed in (False, True):
                with self.subTest(path=path, committed=committed):
                    repo = self.make_git_repo()
                    file = repo / path
                    file.parent.mkdir(parents=True)
                    file.write_text("# Retired contract\n")
                    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                    subprocess.run(["git", "commit", "-m", "old contract"], cwd=repo, check=True, capture_output=True)
                    file.unlink()
                    if committed:
                        subprocess.run(["git", "commit", "-am", "remove contract"], cwd=repo, check=True, capture_output=True)
                    result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
                    checks = {c["id"]: c for c in result.selected_checks}
                    self.assertIn("current_records.validate", checks)
                    self.assertNotIn(path, shlex.split(checks["current_records.validate"]["command"]))
                    self.assertIn("governed_lifecycle_cli_wrapper.test", checks)


    def test_plan_index_does_not_reintroduce_proven_deleted_lifecycle_inputs(self):
        repo = self.make_git_repo()
        path = "specs/rigorloop-cli-lockfile.md"
        file = repo / path
        file.parent.mkdir(parents=True)
        file.write_text("# Retired contract\n")
        for index in ("docs/plan.md", "docs/plan-archive.md"):
            target = repo / index
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Plan navigation\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "old contract and navigation"], cwd=repo, check=True, capture_output=True)
        file.unlink()
        result = select_validation(SelectionRequest(mode="explicit", paths=(path, "docs/plan.md"), repo_root=repo))
        checks = {c["id"]: c for c in result.selected_checks}
        self.assertIn("governed_lifecycle_cli_wrapper.test", checks)
        args = shlex.split(checks["current_records.validate"]["command"])
        self.assertNotIn(path, args)
        self.assertIn("guide_system.validate", checks)


    def test_unproven_missing_or_present_lifecycle_input_is_not_suppressed(self):
        path = "specs/rigorloop-cli-lockfile.md"
        for kind in ("missing", "present", "dangling-symlink"):
            with self.subTest(kind=kind):
                repo = self.make_git_repo()
                file = repo / path
                file.parent.mkdir(parents=True)
                if kind == "present":
                    file.write_text("# Current input\n")
                elif kind == "dangling-symlink":
                    file.symlink_to(repo / "absent-target")
                if kind != "missing":
                    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
                checks = {c["id"]: c for c in result.selected_checks}
                self.assertTrue(result.status == "blocked" or
                                any(path in shlex.split(check["command"]) for check in checks.values()))


    def test_retired_author_deletion_keeps_package_proof_without_auditing_absent_source(self):
        repo = self.make_git_repo()
        path = "skills/spec/SKILL.md"
        file = repo / path
        file.parent.mkdir(parents=True)
        file.write_text("# Historical author\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "old author"], cwd=repo, check=True, capture_output=True)
        file.unlink()
        selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
        checks = {c["id"] for c in selected.selected_checks}
        self.assertNotIn("documentation_prose.audit", checks)
        self.assertTrue({"skills.validate", "skills.regression", "adapters.drift"} <= checks)


    def test_missing_unproven_or_present_isolated_prose_retains_audit(self):
        path = "docs/reviews/explicit-recording-m3-code-review.md"
        repo = self.make_git_repo()
        for present in (False, True):
            if present:
                (repo / path).parent.mkdir(parents=True)
                (repo / path).write_text("# Explicit review input\n")
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
            selected = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
            check = next(c for c in selected.selected_checks if c["id"] == "documentation_prose.audit")
            self.assertIn(path, shlex.split(check["command"]))


    def test_model_selection_retains_authoritative_tracking_preflight(self):
        repo = self.make_git_repo()
        path = repo / "docs/design/skill/workflow.md"
        path.parent.mkdir(parents=True)
        path.write_text("# Model fixture\n")
        result = select_validation(SelectionRequest(mode="explicit", paths=("docs/design/skill/workflow.md",), repo_root=repo))
        self.assertIn("untracked-authoritative-artifacts", {item.get("code") for item in result.blocking_results})


    def test_isolated_recording_evidence_selects_proof_without_formal_settlement(self):
        repo = self.make_git_repo()
        for path in ("docs/implementation/explicit-recording-m4.md", "docs/reviews/explicit-recording-m3-code-review.md"):
            (repo / path).parent.mkdir(parents=True, exist_ok=True)
            (repo / path).write_text("# Present historical evidence fixture\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
            result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=repo))
            self.assertNotIn(path, result.unclassified_paths)
            checks = {check["id"] for check in result.selected_checks}
            self.assertTrue({"documentation_prose.audit", "model.validate", "rigorloop_cli.test"} <= checks)
            self.assertNotIn("current_records.validate", checks)
        unknown = "docs/reviews/unknown_value.md"
        result = select_validation(SelectionRequest(mode="explicit", paths=(unknown,), repo_root=ROOT,
                                                   preflight_context=self.root_preflight_context))
        self.assertIn(unknown, result.unclassified_paths)


    def test_mixed_skill_and_spec_scope_each_check_to_its_owner(self) -> None:
        skill_path = "skills/design/SKILL.md"
        spec_path = "specs/customer-feature.md"
        # Portable explicitly selected customer contracts remain supported;
        # this proof must not read a retired repository contract.
        repo = self.make_git_repo()
        for path in (skill_path, spec_path):
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Explicit customer input\n")
        self.git_output(repo, "add", ".")
        payload = select_validation(SelectionRequest(mode="explicit", paths=(skill_path, spec_path), repo_root=repo)).to_json_dict()

        self.assertEqual(payload["status"], "ok")
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertIn("current_records.validate", selected_ids(payload))
        lifecycle = next(
            check
            for check in payload["selected_checks"]
            if check["id"] == "current_records.validate"
        )
        self.assertEqual(lifecycle["command"], "python scripts/validate-governed-lifecycle-cli.py")
        boundary = next(
            check
            for check in payload["selected_checks"]
            if check["id"] == "boundary_first.validate"
        )
        self.assertEqual(boundary["paths"], [skill_path, spec_path])


    def test_preflight_blocks_untracked_authoritative_artifact_with_action(self) -> None:
        repo = self.make_git_repo()
        proposal = repo / "docs" / "proposals" / "new-proposal.md"
        proposal.parent.mkdir(parents=True)
        proposal.write_text("# New proposal\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/proposals/new-proposal.md",),
                repo_root=repo,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(payload["status"], "blocked")
        blockers = payload["blocking_results"]
        self.assertTrue(
            any(
                blocker.get("code") == "untracked-authoritative-artifacts"
                and blocker.get("corrective_action") == "git add -- docs/proposals/new-proposal.md"
                for blocker in blockers
            ),
            blockers,
        )
        self.assertTrue(
            any(
                result.get("check") == "tracked_authoritative_artifacts"
                and result.get("result") == "blocked"
                for result in payload["preflight_results"]
            ),
            payload["preflight_results"],
        )


    def test_preflight_passes_tracked_authoritative_artifact(self) -> None:
        repo = self.make_git_repo()
        proposal = repo / "docs" / "proposals" / "tracked-proposal.md"
        proposal.parent.mkdir(parents=True)
        proposal.write_text("# Tracked proposal\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/proposals/tracked-proposal.md",),
                repo_root=repo,
            )
        )
        payload = result.to_json_dict()

        self.assertNotIn(
            "untracked-authoritative-artifacts",
            {blocker.get("code") for blocker in payload["blocking_results"]},
        )
        self.assertTrue(
            any(
                item.get("check") == "tracked_authoritative_artifacts"
                and item.get("result") == "pass"
                for item in payload["preflight_results"]
            ),
            payload["preflight_results"],
        )


    def test_preflight_passes_directory_when_its_authoritative_contents_are_tracked(self) -> None:
        repo = self.make_git_repo()
        fixture = repo / "scripts" / "fixtures" / "boundary-first" / "activation"
        fixture.mkdir(parents=True)
        (fixture / "unknown-state.yaml").write_text("state: unknown\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("scripts/fixtures/boundary-first/activation",),
                repo_root=repo,
            )
        )

        self.assertNotIn(
            "untracked-authoritative-artifacts",
            {blocker.get("code") for blocker in result.to_json_dict()["blocking_results"]},
        )

        (fixture / "untracked.yaml").write_text("state: untracked\n", encoding="utf-8")
        mixed = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("scripts/fixtures/boundary-first/activation",),
                repo_root=repo,
            )
        )
        self.assertIn(
            "untracked-authoritative-artifacts",
            {blocker.get("code") for blocker in mixed.to_json_dict()["blocking_results"]},
        )


    def test_preflight_blocks_empty_only_untracked_and_symlink_directories(self) -> None:
        for case in ("empty", "only-untracked", "symlink"):
            with self.subTest(case=case):
                repo = self.make_git_repo()
                fixture = repo / "scripts" / "fixtures" / "boundary-first" / "activation"
                if case == "symlink":
                    target = repo / "fixture-target"
                    target.mkdir()
                    (target / "tracked.yaml").write_text("state: tracked\n", encoding="utf-8")
                    fixture.parent.mkdir(parents=True)
                    fixture.symlink_to(target, target_is_directory=True)
                    subprocess.run(["git", "add", "."], cwd=repo, check=True)
                else:
                    fixture.mkdir(parents=True)
                    if case == "only-untracked":
                        (fixture / "untracked.yaml").write_text("state: unknown\n", encoding="utf-8")
                result = select_validation(
                    SelectionRequest(
                        mode="explicit",
                        paths=("scripts/fixtures/boundary-first/activation",),
                        repo_root=repo,
                    )
                )
                expected = (
                    {"unclassified-path", "untracked-authoritative-artifacts"}
                    if case == "symlink"
                    else {"untracked-authoritative-artifacts"}
                )
                self.assertTrue(
                    expected
                    & {blocker.get("code") for blocker in result.to_json_dict()["blocking_results"]}
                )


    def test_preflight_blocks_tracked_file_replaced_by_untracked_directory(self) -> None:
        repo = self.make_git_repo()
        fixture = repo / "specs" / "tracked.md"
        fixture.parent.mkdir()
        fixture.write_text("# tracked\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "track artifact"], cwd=repo, check=True)
        fixture.unlink()
        fixture.mkdir()
        (fixture / "payload.md").write_text("untracked\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("specs/tracked.md",),
                repo_root=repo,
            )
        )

        self.assertIn(
            "untracked-authoritative-artifacts",
            {blocker.get("code") for blocker in result.to_json_dict()["blocking_results"]},
        )


    def test_selector_selected_readability_command_fails_changed_readme_hard_wrap(self) -> None:
        repo = self.make_git_repo()
        (repo / "scripts").mkdir()
        shutil.copy2(
            ROOT / "scripts" / "validate-markdown-readability.py",
            repo / "scripts" / "validate-markdown-readability.py",
        )
        (repo / "README.md").write_text(
            "# Example\n\nRigorLoop preserves proposal to spec handoffs.\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add semantic readme"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text(
            "# Example\n\nRigorLoop preserves proposal to\nspec handoffs.\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "hard wrap readme"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        selector_result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(selector_result.returncode, 0, msg=selector_result.stderr)
        payload = parse_stdout(selector_result)
        readability_check = next(
            check for check in payload["selected_checks"] if check["id"] == "markdown_readability.validate"
        )

        self.assertEqual(readability_check["changed_sections"], ["README.md:3:4"])
        command_result = subprocess.run(
            shlex.split(readability_check["command"]),
            cwd=repo,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(command_result.returncode, 0)
        self.assertIn("ERROR MDREAD-001", command_result.stdout)


    def test_valid_pr_and_main_modes_use_git_range(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "change skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        pr_result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(pr_result.returncode, 0, msg=pr_result.stderr)
        pr_payload = parse_stdout(pr_result)
        self.assertEqual(pr_payload["mode"], "pr")
        self.assertEqual(pr_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(pr_payload))
        self.assertFalse(pr_payload["broad_smoke_required"])

        main_result = run_selector("--mode", "main", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(main_result.returncode, 0, msg=main_result.stderr)
        main_payload = parse_stdout(main_result)
        self.assertEqual(main_payload["mode"], "main")
        self.assertEqual(main_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(main_payload))
        self.assertIn("broad_smoke.repo", selected_ids(main_payload))
        self.assertTrue(main_payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "main"}, main_payload["broad_smoke"]["sources"])


    def test_pr_mode_routes_adapter_distribution_test_script_to_adapter_checks(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        adapter_test = repo / "tests" / "engineering" / "packaging" / "test-adapter-distribution.py"
        adapter_test.parent.mkdir(parents=True)
        adapter_test.write_text("print('adapter tests')\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add adapter test"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["tests/engineering/packaging/test-adapter-distribution.py"])
        self.assertIn(
            {"path": "tests/engineering/packaging/test-adapter-distribution.py", "category": "adapters"},
            payload["classified_paths"],
        )
        self.assertTrue(
            {"adapters.regression", "adapters.drift", "adapters.validate"}.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["blocking_results"])


    def test_pr_mode_routes_adapter_fixture_to_adapter_checks(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        fixture = repo / "tests" / "fixtures" / "adapters" / "example" / "SKILL.md"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("# Adapter fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add adapter fixture"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["tests/fixtures/adapters/example/SKILL.md"])
        self.assertIn(
            {"path": "tests/fixtures/adapters/example/SKILL.md", "category": "adapters"},
            payload["classified_paths"],
        )
        self.assertTrue(
            {"adapters.regression", "adapters.drift", "adapters.validate"}.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["blocking_results"])


    def test_git_discovery_includes_deleted_and_both_renamed_paths(self):
        # TG-08: actual Git status/ranges, including a renamed unknown source.
        # Neither an unknown deletion nor its known destination may disappear.
        for unknown in (False, True):
            with self.subTest(unknown=unknown):
                repo = self.make_git_repo()
                deleted = 'specs/retired.md'
                before = 'unknown-input.xyz' if unknown else 'tests/fixtures/adapters/old/SKILL.md'
                after = 'tests/fixtures/adapters/new/SKILL.md'
                unknown_deleted = 'unknown-deleted.xyz'
                original = (deleted, before, unknown_deleted) if unknown else (deleted, before)
                for path in original:
                    target = repo / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text('# Stable historical content\n' * 10)
                self.git_output(repo, 'add', '.')
                self.git_output(repo, 'commit', '-m', 'original inputs')
                base = self.git_output(repo, 'rev-parse', 'HEAD')
                (repo / deleted).unlink()
                if unknown:
                    (repo / unknown_deleted).unlink()
                (repo / after).parent.mkdir(parents=True, exist_ok=True)
                (repo / before).rename(repo / after)
                for stage in ('unstaged', 'staged', 'committed'):
                    with self.subTest(stage=stage):
                        if stage == 'staged':
                            self.git_output(repo, 'add', '-A')
                        elif stage == 'committed':
                            self.git_output(repo, 'commit', '-m', 'retire and rename')
                        args = ('--mode', 'pr', '--base', base, '--head', 'HEAD') if stage == 'committed' else ('--mode', 'local')
                        result = run_selector(*args, cwd=repo)
                        payload = parse_stdout(result)
                        self.assertEqual(set(payload['changed_paths']), set(original) | {after})
                        self.assertEqual(payload['status'], 'blocked' if unknown else 'ok', payload)
                        self.assertEqual(set(payload['unclassified_paths']), {before, unknown_deleted} if unknown else set())
                        if unknown:
                            self.assertNotEqual(result.returncode, 0)
                        else:
                            self.assertIn('governed_lifecycle_cli_wrapper.test', selected_ids(payload))


    def test_pr_mode_routes_spec_read_retirement_deletions(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        script = repo / "scripts" / "test-fidelity-gate-spec-reads.py"
        script.parent.mkdir(parents=True)
        script.write_text("print('spec read proof')\n", encoding="utf-8")
        fixture = (
            repo
            / "tests"
            / "fixtures"
            / "requirement-fidelity-gate"
            / "representative-reviews"
            / "r26-matrix-pilot"
            / "spec-read-log.json"
        )
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add requirement fidelity spec-read proof"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        base = self.git_output(repo, "rev-parse", "HEAD")
        script.unlink()
        fixture.unlink()
        subprocess.run(["git", "add", "-u"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "retire fixed read log"], cwd=repo, check=True, capture_output=True)
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(
            payload["changed_paths"],
            [
                "scripts/test-fidelity-gate-spec-reads.py",
                "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
            ],
        )
        self.assertIn(
            {"path": "scripts/test-fidelity-gate-spec-reads.py", "category": "retired-spec-read"},
            payload["classified_paths"],
        )
        self.assertIn(
            {
                "path": "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
                "category": "retired-spec-read",
            },
            payload["classified_paths"],
        )
        self.assertNotIn("requirement_fidelity.spec_reads", selected_ids(payload))
        self.assertTrue({"selector.regression", "skills.regression", "skills.regression"}.issubset(selected_ids(payload)))
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertFalse(payload["blocking_results"])


    def test_spec_read_retirement_local_unstaged_and_staged_deletions(self) -> None:
        paths = ["scripts/test-fidelity-gate-spec-reads.py",
                 "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json"]
        repo = self.make_git_repo()
        for path in paths:
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("retired fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "baseline instrumentation"], cwd=repo, check=True, capture_output=True)
        for path in paths:
            (repo / path).unlink()
        for staged in (False, True):
            with self.subTest(staged=staged):
                if staged:
                    subprocess.run(["git", "add", "-u"], cwd=repo, check=True, capture_output=True)
                payload = parse_stdout(run_selector("--mode", "local", cwd=repo))
                self.assertEqual(payload["status"], "ok")
                self.assertEqual(set(payload["changed_paths"]), set(paths))
                self.assertTrue({"selector.regression", "skills.regression", "skills.regression"}.issubset(selected_ids(payload)))
                self.assertNotIn("requirement_fidelity.spec_reads", selected_ids(payload))


    def test_spec_read_retirement_recreated_file_and_symlink_block(self) -> None:
        paths = ["scripts/test-fidelity-gate-spec-reads.py",
                 "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json"]
        for path in paths:
            for kind in ("file", "symlink"):
                with self.subTest(path=path, kind=kind):
                    repo = self.make_git_repo()
                    target = repo / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if kind == "file":
                        target.write_text("recreated obsolete input\n", encoding="utf-8")
                    else:
                        target.symlink_to(repo / "missing-target")
                    result = run_selector("--mode", "explicit", "--path", path, cwd=repo)
                    payload = parse_stdout(result)
                    self.assertEqual(payload["status"], "blocked")
                    self.assertTrue(payload["blocking_results"])
                    self.assertNotIn("requirement_fidelity.spec_reads", selected_ids(payload))
                    self.assertTrue(target.exists() or target.is_symlink())


    def test_spec_read_retirement_unknown_sibling_and_mixed_paths_block(self) -> None:
        repo = self.make_git_repo()
        unknown = "tests/fixtures/requirement-fidelity-gate/representative-reviews/new-review/spec-read-log.json"
        for paths in ([unknown], ["scripts/test-fidelity-gate-spec-reads.py", unknown]):
            args = [value for path in paths for value in ("--path", path)]
            payload = parse_stdout(run_selector("--mode", "explicit", *args, cwd=repo))
            self.assertEqual(payload["status"], "blocked")
            self.assertIn(unknown, payload["unclassified_paths"])
            self.assertNotIn("requirement_fidelity.spec_reads", selected_ids(payload))


    def test_pr_mode_routes_readme_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text("# Example\n\nVision ownership wording.\n", encoding="utf-8")
        (repo / "skills" / "vision").mkdir(parents=True)
        (repo / "skills" / "vision" / "SKILL.md").write_text("# Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add readme and vision skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])


    def test_pr_mode_routes_root_vision_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        (repo / "VISION.md").write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add root vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "VISION.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])


    def test_pr_mode_blocks_reintroduced_retired_vision_as_unclassified(self) -> None:
        repo = self.make_git_repo()
        (repo / "VISION.md").write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add canonical vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "reintroduce legacy vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 2, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertNotIn({"path": "vision.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], ["vision.md"])
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})


    def test_pr_always_retains_lifecycle_scope_for_docs_and_code(self) -> None:
        for path in ("README.md", "packages/rigorloop/dist/lib/example.js"):
            with self.subTest(path=path):
                repo = self.make_git_repo()
                base = self.git_output(repo, "rev-parse", "HEAD")
                target = repo / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("changed\n")
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "bounded change"], cwd=repo, check=True, capture_output=True)
                head = self.git_output(repo, "rev-parse", "HEAD")
                result = select_validation(SelectionRequest(mode="pr", base=base, head=head, repo_root=repo))
                self.assertEqual(result.status, "ok", result.blocking_results)
                checks = {check["id"]: check for check in result.selected_checks}
                self.assertIn("current_records.snapshot", checks)
                self.assertEqual(shlex.split(checks["current_records.snapshot"]["command"])[-2:],
                                 ["--revision", head])
                if path == "README.md":
                    self.assertNotIn("adapters.regression", checks)
                    self.assertNotIn("rigorloop_cli.test", checks)
                else:
                    self.assertIn("rigorloop_cli.test", checks)


    def test_local_mode_discovers_tracked_and_untracked_git_paths(self) -> None:
        repo = self.make_git_repo()
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        (repo / "docs" / "changes" / "2026-04-25-local").mkdir(parents=True)
        (repo / "docs" / "changes" / "2026-04-25-local" / "change.yaml").write_text(
            "change_id: 2026-04-25-local\n",
            encoding="utf-8",
        )

        result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("skills/workflow/SKILL.md", payload["changed_paths"])
        self.assertIn("docs/changes/2026-04-25-local/change.yaml", payload["changed_paths"])
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertIn("record_retirement.regression", selected_ids(payload))


    def test_boundary_first_surfaces_select_boundary_validation(self) -> None:
        repo = self.make_git_repo()
        paths = (
            "specs/boundary-first-activation.yaml",
            "specs/boundary-first-resources.yaml",
            "scripts/resources/boundary-first/boundary-first-resources.yaml",
            "templates/shared/boundary-first-method-v1.md",
            "templates/shared/boundary-first-feature-authoring-v1.md",
            "templates/shared/boundary-first-proof-v1.md",
            "specs/feature.md",
            "specs/feature.test.md",
            "skills/design/references/boundary-first-method-v1.md",
            "dist/adapters/manifest.yaml",
            "scripts/lib/validation/boundary_first_reference.py",
            "scripts/project-boundary-first-reference.py",
            "tests/engineering/validation/test-boundary-first-reference.py",
            "scripts/lib/validation/boundary_first_validation.py",
            "scripts/fixtures/boundary-first/feature-records/minimal.md",
        )
        for path in paths:
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("fixture\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "."],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "boundary fixtures"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        for path in paths:
            result = select_validation(
                SelectionRequest(mode="explicit", paths=(path,), repo_root=repo)
            )
            with self.subTest(path=path):
                self.assertEqual(result.status, "ok", result.to_json_dict())
                self.assertIn(
                    "boundary_first.validate",
                    selected_ids(result.to_json_dict()),
                )
                if path in {
                    "specs/boundary-first-resources.yaml",
                    "scripts/resources/boundary-first/boundary-first-resources.yaml",
                    "templates/shared/boundary-first-method-v1.md",
                    "templates/shared/boundary-first-feature-authoring-v1.md",
                    "templates/shared/boundary-first-proof-v1.md",
                    "skills/design/references/boundary-first-method-v1.md",
                    "scripts/lib/validation/boundary_first_reference.py",
                    "scripts/project-boundary-first-reference.py",
                    "tests/engineering/validation/test-boundary-first-reference.py",
                }:
                    self.assertIn(
                        "boundary_first.reference_regression",
                        selected_ids(result.to_json_dict()),
                    )
                if path in {
                    "scripts/lib/validation/boundary_first_validation.py",
                    "scripts/fixtures/boundary-first/feature-records/minimal.md",
                }:
                    self.assertIn(
                        "boundary_first.regression",
                        selected_ids(result.to_json_dict()),
                    )
                command = next(
                    check["command"]
                    for check in result.to_json_dict()["selected_checks"]
                    if check["id"] == "boundary_first.validate"
                )
                if path in {"specs/feature.md", "specs/feature.test.md"}:
                    self.assertIn(f"--path {path}", command)
                else:
                    self.assertNotIn("--path", command)
