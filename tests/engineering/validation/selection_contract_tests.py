"""Selection contract observations; loaded by the supported aggregate TestCase."""
from __future__ import annotations

from selection_test_helpers import (
    CHECK_CATALOG,
    CI,
    EXPECTED_CATALOG,
    MODE_CHECK_IDS,
    Path,
    README_VALIDATOR,
    ROOT,
    SelectionRequest,
    catalog_command,
    normalize_path,
    select_validation,
    selected_ids,
    shlex,
    subprocess,
    sys,
    tempfile,
)


class SelectionContractChecks:
    def test_retired_skill_archive_paths_select_current_protection_without_reading_sources(self):
        from lib.validation.validation_selection import SKILL_SOURCE_ARCHIVE_PATHS
        for path in SKILL_SOURCE_ARCHIVE_PATHS:
            result = select_validation(SelectionRequest(mode="explicit", paths=(path,), repo_root=ROOT, preflight_context=self.root_preflight_context))
            self.assertEqual(result.status, "ok", result.blocking_results)
            checks = {check["id"] for check in result.selected_checks}
            self.assertIn("skills.regression", checks)
            self.assertNotIn("current_records.validate", checks)
            self.assertNotIn("documentation_prose.enforce", checks)
        unknown = "docs/archive/skill-model/2026-09-08/unknown_value.md"
        result = select_validation(SelectionRequest(mode="explicit", paths=(unknown,), repo_root=ROOT, preflight_context=self.root_preflight_context))
        self.assertEqual(result.status, "blocked")
        self.assertIn(unknown, result.unclassified_paths)


    def test_explicit_recording_adoption_surfaces_select_real_proof(self):
        paths = (
            "docs/design/cli/cli.md", "docs/design/skill/workflow.md",
            "schemas/explicit-recording-v1.schema.json",
            "schemas/targeted-recording-v1.schema.json",
            "scripts/build-record-store-schema.mjs",
            "scripts/validate-record-store.mjs",
            "tests/fixtures/explicit-recording-v1/records.json",
            "templates/explicit-recording/records.json",
            "schemas/rigorloop-records-v3.schema.json",
            "templates/rigorloop-records-v3/records.json",
            "tests/fixtures/rigorloop-records-v3/records.json",
        )
        for path in paths:
            with self.subTest(path=path):
                result = select_validation(SelectionRequest(
                    mode="explicit", paths=(path,), repo_root=ROOT,
                    preflight_context=self.root_preflight_context,
                ))
                checks = {check["id"] for check in result.selected_checks}
                self.assertTrue({"rigorloop_cli.test", "record_store.schema", "model.validate"} <= checks, checks)
                self.assertNotIn(path, result.unclassified_paths)
                self.assertFalse(any(item.get("code") == "manual-routing-required" for item in result.blocking_results))


    def test_explicit_recording_package_paths_retain_publication_proof(self):
        for path in ("packages/rigorloop/dist/lib/record-store.js",
                     "packages/rigorloop/dist/lib/recording-query-cli.js",
                     "packages/rigorloop/dist/schemas/targeted-recording-v1.schema.json",
                     "packages/rigorloop/test/helpers/recording-query-launcher.mjs",
                     "packages/rigorloop/dist/lib/record-json.js",
                     "packages/rigorloop/dist/schemas/rigorloop-records-v3.schema.json",
                     "packages/rigorloop/dist/templates/rigorloop-records-v3/records.json",
                     "packages/rigorloop/dist/templates/explicit-recording/records.json",
                     "packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json",
                     "packages/rigorloop/test/record-store-cli.test.js",
                     "packages/rigorloop/test/helpers/record-store-launcher.mjs"):
            with self.subTest(path=path):
                result = select_validation(SelectionRequest(
                    mode="explicit", paths=(path,), repo_root=ROOT,
                    preflight_context=self.root_preflight_context,
                ))
                self.assertEqual({check["id"] for check in result.selected_checks}, {
                    "rigorloop_cli.test", "npm_package_publication.test", "record_store.schema",
                    "model.validate", "boundary_first.regression", "change_metadata.regression",
                })


    def test_package_initializers_select_all_descendant_consumers(self):
        # Initializers have no legacy predecessor: all descendant readers apply.
        descendants = {'validation': ['scripts/lib/validation/boundary_first_reference.py', 'scripts/lib/validation/boundary_first_validation.py', 'scripts/lib/validation/model_layout.py', 'scripts/lib/validation/record_store_classification.py', 'scripts/lib/validation/skill_validation.py', 'scripts/lib/validation/validation_execution.py', 'scripts/lib/validation/validation_selection.py', 'scripts/lib/validation/validation_node_adapter.mjs', 'scripts/lib/validation/record_snapshot_git.mjs'], 'packaging': ['scripts/lib/packaging/adapter_distribution.py', 'scripts/lib/packaging/npm_package_validation.py'], 'release': ['scripts/lib/release/release_candidate.py', 'scripts/lib/release/release_coordination.py', 'scripts/lib/release/release_evidence.py', 'scripts/lib/release/release_execution.py', 'scripts/lib/release/release_provider.py', 'scripts/lib/release/release_transaction.py']}
        all_required = set()
        for group, paths in descendants.items():
            with self.subTest(group=group):
                required = {c['id'] for c in self.select(paths).selected_checks}
                all_required.update(required)
                selected = self.select(['scripts/lib/' + group + '/__init__.py'])
                self.assertEqual(selected.status, 'ok')
                self.assertTrue(required <= {c['id'] for c in selected.selected_checks}, required)
        root = self.select(['scripts/lib/__init__.py'])
        self.assertEqual(root.status, 'ok')
        self.assertTrue(all_required <= {c['id'] for c in root.selected_checks})
        self.assertEqual(self.select(['scripts/lib/unknown/__init__.py']).status, 'blocked')


    def test_tooling_module_and_resource_moves_preserve_required_selection(self):
        # ENG-SR-16: both sides retain check scope, including retired parser deletion paths.
        destinations = {'scripts/boundary_first_reference.py': 'scripts/lib/validation/boundary_first_reference.py',
         'scripts/boundary_first_validation.py': 'scripts/lib/validation/boundary_first_validation.py',
         'scripts/model_layout.py': 'scripts/lib/validation/model_layout.py',
         'scripts/project_yaml.py': 'scripts/lib/validation/project_yaml.py',
         'scripts/record_store_classification.py': 'scripts/lib/validation/record_store_classification.py',
         'scripts/skill_validation.py': 'scripts/lib/validation/skill_validation.py',
         'scripts/validation_execution.py': 'scripts/lib/validation/validation_execution.py',
         'scripts/validation_selection.py': 'scripts/lib/validation/validation_selection.py',
         'scripts/validation_node_adapter.mjs': 'scripts/lib/validation/validation_node_adapter.mjs',
         'scripts/record_snapshot_git.mjs': 'scripts/lib/validation/record_snapshot_git.mjs',
         'scripts/adapter_distribution.py': 'scripts/lib/packaging/adapter_distribution.py',
         'scripts/npm_package_validation.py': 'scripts/lib/packaging/npm_package_validation.py',
         'scripts/release_candidate.py': 'scripts/lib/release/release_candidate.py',
         'scripts/release_coordination.py': 'scripts/lib/release/release_coordination.py',
         'scripts/release_evidence.py': 'scripts/lib/release/release_evidence.py',
         'scripts/release_execution.py': 'scripts/lib/release/release_execution.py',
         'scripts/release_provider.py': 'scripts/lib/release/release_provider.py',
         'scripts/release_transaction.py': 'scripts/lib/release/release_transaction.py',
         'scripts/boundary-first-resources.yaml': 'scripts/resources/boundary-first/boundary-first-resources.yaml',
         'scripts/adapter_templates/claude/CLAUDE.md': 'scripts/resources/adapter-templates/claude/CLAUDE.md',
         'scripts/adapter_templates/codex/AGENTS.md': 'scripts/resources/adapter-templates/codex/AGENTS.md'}
        for old_path, new_path in destinations.items():
            with self.subTest(path=new_path):
                old = self.select([old_path])
                new = self.select([new_path])
                self.assertFalse(new.to_json_dict()['unclassified_paths'])
                self.assertEqual({c['id'] for c in old.selected_checks},
                                 {c['id'] for c in new.selected_checks})
        self.assertEqual(self.select(['scripts/lib/validation/unknown.py']).status, 'blocked')


    def test_moved_validation_suites_preserve_selection_and_current_commands(self):
        # TEST-SR-10/17: both sides of relocation retain the same real checks.
        names = (
            "test-boundary-first-reference.py", "test-boundary-first-validation.py",
            "test-change-metadata-validator.py", "test-documentation-prose-validator.py",
            "test-governed-lifecycle-cli-validator.py", "test-guide-system-validator.py",
            "test-markdown-readability-validator.py",
            "test-select-validation.py", "test-validation-execution.py",
        )
        for name in names:
            with self.subTest(name=name):
                old = self.select(["scripts/" + name])
                new = self.select(["tests/engineering/validation/" + name])
                self.assertFalse(new.to_json_dict()["unclassified_paths"])
                self.assertEqual({c["id"] for c in old.selected_checks},
                                 {c["id"] for c in new.selected_checks})
                for check in new.selected_checks:
                    self.assertNotIn("scripts/" + name, check["command"])
        for name in (
            "boundary_structural_tests.py", "boundary_path_tests.py",
            "boundary_handoff_tests.py", "boundary_model_tests.py",
            "boundary_command_tests.py", "boundary_fixture_helpers.py",
        ):
            with self.subTest(module=name):
                payload = self.select(["tests/engineering/validation/" + name]).to_json_dict()
                self.assertEqual(payload["unclassified_paths"], [])
                checks = {check["id"]: check for check in payload["selected_checks"]}
                self.assertEqual(set(checks), {"boundary_first.validate", "boundary_first.regression"})
                self.assertEqual(checks["boundary_first.regression"]["command"],
                                 "python tests/engineering/validation/test-boundary-first-validation.py")
                self.assertEqual(len(checks), len(payload["selected_checks"]))
        unknown = self.select(["tests/engineering/validation/test-unknown.py"])
        self.assertTrue(unknown.to_json_dict()["unclassified_paths"])


    def test_split_selection_modules_preserve_selector_and_executor_consumers(self):
        for name in ("selection_contract_tests.py", "selection_git_tests.py",
                     "selection_cli_tests.py", "selection_test_helpers.py"):
            with self.subTest(module=name):
                payload = self.select(["tests/engineering/validation/" + name]).to_json_dict()
                self.assertEqual(payload["unclassified_paths"], [])
                ids = [check["id"] for check in payload["selected_checks"]]
                self.assertEqual(set(ids), {"selector.regression", "validation_execution.regression"})
                self.assertEqual(len(ids), len(set(ids)))


    def test_release_fixture_helper_preserves_release_selection(self):
        payload = self.select(["tests/engineering/release/release_fixture_helpers.py"]).to_json_dict()
        self.assertEqual(payload["unclassified_paths"], [])
        checks = {check["id"]: check for check in payload["selected_checks"]}
        self.assertIn("release_transaction.regression", checks)
        self.assertEqual(checks["release_transaction.regression"]["command"],
                         "python tests/engineering/release/test-release-transaction.py")
        self.assertEqual(len(checks), len(payload["selected_checks"]))


    def test_split_skill_modules_select_required_consumers(self):
        # Independently named consumers: a helper move must not hide Skill proof.
        for name in (
            "skill_contract_tests.py", "skill_cli_tests.py", "skill_guidance_tests.py",
            "skill_metadata_tests.py",
            "skill_resource_tests.py",
            "skill_asset_tests.py",
            "skill_ci_contract_tests.py",
            "skill_canonical_tests.py",
            "skill_portability_tests.py",
            "skill_project_map_tests.py",
            "skill_placement_tests.py",
            "skill_fixture_helpers.py",
            "skill_guidance_helpers.py",
            "skill_readability_guidance_tests.py",
            "skill_authority_tests.py",
            "skill_route_guidance_tests.py",
            "skill_verify_guidance_tests.py",
            "skill_pr_guidance_tests.py",
            "skill_plan_guidance_tests.py",
            "skill_proposal_guidance_tests.py",
            "skill_design_resource_tests.py",
            "skill_vision_guidance_tests.py",
            "skill_learn_guidance_tests.py",
            "skill_project_map_guidance_tests.py",
            "skill_ci_guidance_tests.py",
            "skill_bugfix_guidance_tests.py",
            "skill_shared_policy_tests.py",
            "skill_discovery_guidance_tests.py",
        ):
            with self.subTest(module=name):
                payload = self.select(["tests/skill/" + name]).to_json_dict()
                self.assertEqual(payload["unclassified_paths"], [])
                checks = {check["id"]: check for check in payload["selected_checks"]}
                self.assertEqual(set(checks), {"skills.regression", "adapters.regression"})
                self.assertEqual(checks["skills.regression"]["command"],
                                 "python tests/skill/test-skill-validator.py")
                self.assertEqual(len(checks), len(payload["selected_checks"]))


    def test_moved_skill_packaging_and_release_suites_preserve_selection(self):
        # TEST-SR-17: imported helpers retain their owning suite's selection too.
        destinations = {
            "test-skill-validator.py": "tests/skill/",
            "review_independence_skill_phrases.py": "tests/skill/",
            "test-adapter-distribution.py": "tests/engineering/packaging/",
            "test-npm-package-publication.py": "tests/engineering/packaging/",
            "test-release-transaction.py": "tests/engineering/release/",
            "release_candidate_tests.py": "tests/engineering/release/",
            "release_coordination_tests.py": "tests/engineering/release/",
            "release_execution_tests.py": "tests/engineering/release/",
            "release_evidence_tests.py": "tests/engineering/release/",
        }
        for name, directory in destinations.items():
            with self.subTest(name=name):
                old = self.select(["scripts/" + name])
                new = self.select([directory + name])
                self.assertFalse(new.to_json_dict()["unclassified_paths"])
                self.assertEqual({c["id"] for c in old.selected_checks},
                                 {c["id"] for c in new.selected_checks})
                for check in new.selected_checks:
                    self.assertNotIn("scripts/" + name, check["command"])
        self.assertTrue(self.select(["tests/skill/test-unknown.py"]).to_json_dict()["unclassified_paths"])
        workflow = self.select([".github/workflows/publish-github-packages.yml"])
        self.assertFalse(workflow.to_json_dict()["unclassified_paths"])
        self.assertIn("npm_package_publication.test", {c["id"] for c in workflow.selected_checks})


    def test_model_layout_change_selects_all_actual_readers(self):
        result = self.select(["scripts/lib/validation/model_layout.py"])
        checks = {c["id"] for c in result.selected_checks}
        self.assertTrue({"boundary_first.regression", "selector.regression", "guide_system.validate", "guide_system.regression"} <= checks, checks)
        self.assertFalse(result.to_json_dict()["unclassified_paths"])


    def test_model_example_selection_uses_owner_not_example_as_model(self):
        import shlex
        for path in ("docs/design/cli/examples/records/v3-complete-store/change.json",
                     "docs/design/cli/examples/v3-review-limitations-update/request.json",
                     "docs/design/cli/examples/observation-freshness/scan-b.json",
                     "docs/design/skill/examples/workflow/correction-cycle.mmd"):
            result = select_validation(SelectionRequest(
                mode="explicit", paths=(path,), repo_root=ROOT,
                preflight_context=self.root_preflight_context))
            self.assertIn("rigorloop_cli.test", {c["id"] for c in result.selected_checks})
            check = next(c for c in result.selected_checks if c["id"] == "model.validate")
            command = shlex.split(check["command"])
            self.assertNotIn(path, command)
            owner = ("docs/design/cli/records.md" if "/examples/records/" in path else
                     "docs/design/skill/workflow.md" if path.startswith("docs/design/skill/") else
                     "docs/design/cli/cli.md")
            self.assertIn(owner, command)


    def test_model_selection_deleted_layout_paths_and_examples_select_current_owner(self):
        for old, current in (
            ("docs/design/system/system.md", "docs/design/system.md"),
            ("docs/design/skill/design.md", "docs/design/skill/authoring/design.md"),
            ("docs/design/workflow/workflow.md", "docs/design/skill/workflow.md"),
            ("docs/design/record-format/examples/v3-complete-store/change.json", "docs/design/cli/records.md"),
            ("docs/design/workflow/examples/correction-cycle.mmd", "docs/design/skill/workflow.md"),
        ):
            with self.subTest(old=old):
                result = self.select([old])
                command = shlex.split(next(c["command"] for c in result.selected_checks if c["id"] == "model.validate"))
                self.assertIn(current, command)
                self.assertNotIn(old, command)


    def test_model_selection_deleted_flat_input_selects_current_owner(self):
        result = self.select(["docs/design/workflow.md"])
        command = shlex.split(next(c["command"] for c in result.selected_checks if c["id"] == "model.validate"))
        self.assertNotIn("docs/design/workflow.md", command)
        self.assertIn("docs/design/skill/workflow.md", command)


    def test_compact_contract_surfaces_select_cross_runtime_and_metadata_proof(self) -> None:
        for path in (
            "schemas/compact-current-state-v1.schema.json",
            "tests/fixtures/compact-current-state-v1/schema-records.json",
            "scripts/test-compact-current-state-canonical-contract.py",
            "scripts/test-retirement-ledger.py",
            "scripts/retirement_ledger.py",
        ):
            with self.subTest(path=path):
                result = self.select([path])
                self.assertEqual(
                    selected_ids(result.to_json_dict()),
                    {"record_retirement.regression", "change_metadata.regression"},
                )


    def test_deleted_historical_ledger_selects_current_rejection_proof(self) -> None:
        result = self.select(["docs/changes/2026-08-10-published-skill-first-repository-simplification/retirement-ledger.json"])
        self.assertEqual(result.status, "ok", result.blocking_results)
        self.assertEqual(selected_ids(result.to_json_dict()), {"record_retirement.regression"})


    def test_shared_preflight_context_requires_matching_repository_identity(self) -> None:
        other_root = Path(tempfile.mkdtemp(prefix="validation-selection-preflight-mismatch-"))
        self.addCleanupTree(other_root)

        with self.assertRaisesRegex(ValueError, "preflight context does not match repository root"):
            select_validation(
                SelectionRequest(
                    mode="explicit",
                    paths=("docs/workflows.md",),
                    repo_root=other_root,
                    preflight_context=self.root_preflight_context,
                )
            )


    def test_selector_preservation_surface_keeps_selected_check_identity(self) -> None:
        paths = [
            "scripts/lib/validation/validation_selection.py",
            "tests/engineering/validation/test-select-validation.py",
            "docs/changes/2026-04-25-example/selector-preservation.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertEqual(
            {"record_retirement.regression", "selector.regression", "validation_execution.regression"},
            selected_ids(payload),
        )
        selector_check = next(check for check in payload["selected_checks"] if check["id"] == "selector.regression")
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "record_retirement.regression")
        self.assertEqual(selector_check["phase"], "focused")
        self.assertEqual(selector_check["cache_status"], "not-applicable")
        self.assertIn("Changed selector code requires selector regression fixtures.", selector_check["reason"])


    def test_selector_registry_changes_select_selector_regression(self) -> None:
        result = self.select(
            [
                "scripts/lib/validation/validation_selection.py",
                "scripts/lib/validation/validation_node_adapter.mjs",
                "tests/engineering/validation/test-select-validation.py",
                "scripts/validate-broad-smoke-classification.py",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertIn("selector.regression", selected_ids(payload))


    def test_catalog_matches_v1_contract(self) -> None:
        self.assertNotIn("main.retirement_ledger.regression", CHECK_CATALOG)
        with self.assertRaisesRegex(ValueError, "unknown check ID"):
            catalog_command("main.retirement_ledger.regression")
        self.assertEqual(set(CHECK_CATALOG), set(EXPECTED_CATALOG) | {key for ids in MODE_CHECK_IDS.values() for key in ids})
        for check_id, command in EXPECTED_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertEqual(CHECK_CATALOG[check_id].command_template, command)
                self.assertTrue(CHECK_CATALOG[check_id].category)


    def test_documentation_prose_tier_a_routes_to_enforcement_without_displacing_existing_checks(self) -> None:
        result = self.select(["README.md", "VISION.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertIn({"path": "VISION.md", "category": "vision"}, payload["classified_paths"])
        self.assertTrue(
            {
                "documentation_prose.enforce",
                "readme.validate",
                "readme.vision_markers",
                "guide_system.validate",
            }.issubset(selected_ids(payload))
        )
        prose_check = next(
            check for check in payload["selected_checks"] if check["id"] == "documentation_prose.enforce"
        )
        self.assertEqual(
            prose_check["command"],
            "python scripts/validate-documentation-prose.py --mode enforce --path README.md --path VISION.md",
        )
        self.assertEqual(prose_check["paths"], ["README.md", "VISION.md"])


    def test_documentation_prose_tier_b_routes_to_audit_without_repository_failure(self) -> None:
        result = self.select(
            [
                "skills/code-review/SKILL.md",
                "docs/changes/2026-04-25-example/explain-change.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("documentation_prose.audit", selected_ids(payload))
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertIn("record_retirement.regression", selected_ids(payload))
        audit_check = next(
            check for check in payload["selected_checks"] if check["id"] == "documentation_prose.audit"
        )
        self.assertEqual(
            audit_check["command"],
            "python scripts/validate-documentation-prose.py --mode audit --path skills/code-review/SKILL.md",
        )
        self.assertEqual(
            audit_check["paths"],
            ["skills/code-review/SKILL.md"],
        )


    def test_documentation_prose_tier_c_paths_do_not_select_first_slice_prose_validation(self) -> None:
        result = self.select(
            [
                "specs/documentation-source-formatting.md",
                "docs/plans/2026-06-24-semantic-source-line-contract.md",
                "docs/changes/2026-04-25-example/reviews/code-review-r1.md",
                "docs/learn/topics/documentation-prose.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertNotIn("documentation_prose.enforce", selected_ids(payload))
        self.assertNotIn("documentation_prose.audit", selected_ids(payload))
        self.assertIn("current_records.validate", selected_ids(payload))
        self.assertIn("record_retirement.regression", selected_ids(payload))
        self.assertIn("guide_system.validate", selected_ids(payload))


    def test_documentation_prose_validator_surfaces_route_without_manual_blocks(self) -> None:
        result = self.select(
            [
                ".markdownlint.json",
                ".prettierrc.json",
                "scripts/validate-documentation-prose.py",
                "tests/engineering/validation/test-documentation-prose-validator.py",
                "tests/fixtures/documentation-prose/pass/semantic-lines.md",
                "tests/fixtures/documentation-prose/fail/mechanical-wrap.md",
                "tests/fixtures/documentation-prose/warn/ambiguous-clause.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        expected_categories = {
            ".markdownlint.json": "validator-documentation-prose",
            ".prettierrc.json": "validator-documentation-prose",
            "scripts/validate-documentation-prose.py": "validator-documentation-prose",
            "tests/engineering/validation/test-documentation-prose-validator.py": "validator-documentation-prose",
            "tests/fixtures/documentation-prose/pass/semantic-lines.md": "validator-documentation-prose",
            "tests/fixtures/documentation-prose/fail/mechanical-wrap.md": "validator-documentation-prose",
            "tests/fixtures/documentation-prose/warn/ambiguous-clause.md": "validator-documentation-prose",
        }
        for path, category in expected_categories.items():
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": category}, payload["classified_paths"])
        self.assertIn("documentation_prose.regression", selected_ids(payload))


    def test_contributing_guidance_routes_without_manual_block(self) -> None:
        result = self.select(["CONTRIBUTING.md", ".github/pull_request_template.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        for path in ("CONTRIBUTING.md", ".github/pull_request_template.md"):
            self.assertIn({"path": path, "category": "contributor-guidance"}, payload["classified_paths"])
        self.assertTrue(
            {
                "selector.regression",
                "guide_system.validate",
                "current_records.validate",
            }.issubset(selected_ids(payload))
        )


    def test_catalog_records_audited_commands_and_initial_case_population(self) -> None:
        from lib.validation.validation_selection import is_parallel_safe_check

        expected_parallel_safe = {key for ids in MODE_CHECK_IDS.values() for key in ids if key.endswith(("skills.validate", "skills.regression", "adapters.build_archives", "adapters.validate_archives"))}

        expected_cases = {
            'skills.regression',
            'governed_lifecycle_cli_wrapper.test',
            'adapters.regression',
            'adapters.drift',
            'adapters.validate',
            'adapters.full_regression',
            'release_transaction.regression',
            'npm_package_publication.test',
            'boundary_first.reference_regression',
            'boundary_first.regression',
            'documentation_prose.regression',
            'markdown_readability.regression',
            'guide_system.regression',
            'governed_lifecycle_cli_wrapper.test','change_metadata.regression','selector.regression','validation_execution.regression',
        }
        self.assertEqual({key for key,entry in CHECK_CATALOG.items()
                          if entry.constraints and entry.constraints.unit=='python-unittest'},expected_cases)
        expected_node = {"rigorloop_cli.test", "record_retirement.regression"}
        self.assertEqual({key for key,entry in CHECK_CATALOG.items()
                          if entry.constraints and entry.constraints.unit=="node-test"}, expected_node)
        expected_parallel_safe |= expected_cases | expected_node

        self.assertEqual(
            {check_id for check_id in CHECK_CATALOG if is_parallel_safe_check(check_id)},
            expected_parallel_safe,
        )
        for check_id, entry in CHECK_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertIsInstance(entry.parallel_safe, bool)
                self.assertEqual(entry.parallel_safe, check_id in expected_parallel_safe)


    def test_canonical_skill_only_uses_purpose_built_checks_without_lifecycle(self) -> None:
        path = "skills/design/SKILL.md"
        payload = self.select([path]).to_json_dict()

        self.assertEqual(payload["status"], "ok")
        self.assertNotIn("current_records.validate", selected_ids(payload))
        self.assertTrue(
            {
                "boundary_first.validate",
                "skills.validate",
                "skills.regression",
                "adapters.regression",
                "adapters.drift",
                "documentation_prose.audit",
            }.issubset(selected_ids(payload))
        )
        self.assertIn("skills/design", payload["affected_roots"])


    def test_generated_skill_only_uses_derivation_checks_without_lifecycle(self) -> None:
        path = ".codex/skills/design/SKILL.md"
        payload = self.select([path]).to_json_dict()

        self.assertEqual(payload["status"], "ok")
        self.assertNotIn("current_records.validate", selected_ids(payload))
        self.assertEqual(
            {"adapters.regression"},
            selected_ids(payload),
        )


    def test_lifecycle_artifact_classes_retain_owned_lifecycle_paths(self) -> None:
        paths = [
            "docs/proposals/2026-07-29-example.md",
            "specs/example.md",
            "specs/example.test.md",
            "docs/architecture/system/example.md",
            "docs/adr/ADR-20260729-example.md",
            "docs/plans/2026-07-29-example.md",
            "docs/changes/2026-07-29-example/review-resolution.md",
            "docs/changes/2026-07-29-example/change.yaml",
        ]
        payload = self.select(paths).to_json_dict()

        self.assertEqual(payload["status"], "ok")
        lifecycle = next(
            check
            for check in payload["selected_checks"]
            if check["id"] == "current_records.validate"
        )
        self.assertEqual(shlex.split(lifecycle["command"]),
                         ["python", "scripts/validate-governed-lifecycle-cli.py"])
        self.assertIn("record_retirement.regression", selected_ids(payload))




    def test_selector_marks_broad_smoke_as_boundary_phase(self) -> None:
        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                broad_smoke=True,
                repo_root=ROOT,
            )
        )
        payload = result.to_json_dict()
        phases = {check["id"]: check["phase"] for check in payload["selected_checks"]}
        self.assertEqual(phases["broad_smoke.repo"], "boundary")
        self.assertEqual(phases["skills.validate"], "focused")


    def test_boundary_checked_revision_surface_retains_sibling_validation_owners(self) -> None:
        result = self.select(
            [
                "scripts/lib/validation/boundary_first_validation.py",
                "docs/changes/2026-08-05-example/review-log.md",
                "skills/design/SKILL.md",
                "dist/adapters/manifest.yaml",
                "packages/rigorloop/package.json",
                "docs/releases/v0.3.6/release.yaml",
                ".github/workflows/ci.yml",
            ]
        )
        checks = selected_ids(result.to_json_dict())

        self.assertIn("boundary_first.validate", checks)
        self.assertIn("record_retirement.regression", checks)
        self.assertIn("skills.validate", checks)
        self.assertIn("adapters.regression", checks)
        self.assertIn("rigorloop_cli.test", checks)
        self.assertIn("npm_package_publication.test", checks)
        self.assertIn("release.validate", checks)
        self.assertIn("selector.regression", checks)


    def test_retired_boundary_activation_publication_surface_is_not_cataloged(self) -> None:
        result = self.select(
            ["scripts/lib/validation/boundary_first_validation.py"]
        )

        self.assertNotIn("boundary_activation_release.regression", CHECK_CATALOG)
        self.assertNotIn(
            "boundary_activation_release.regression",
            selected_ids(result.to_json_dict()),
        )
        self.assertIn("boundary_first.validate", selected_ids(result.to_json_dict()))
        self.assertIn("boundary_first.regression", selected_ids(result.to_json_dict()))


    def test_review_lifecycle_and_release_paths_select_scoped_validators(self) -> None:
        result = self.select(
            [
                "docs/changes/2026-04-25-example/review-resolution.md",
                "specs/rigorloop-workflow.test.md",
                "docs/releases/v0.1.1/release.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("record_retirement.regression", selected_ids(payload))
        self.assertIn("current_records.validate", selected_ids(payload))
        self.assertIn("release.validate", selected_ids(payload))
        self.assertNotIn("docs/changes/2026-04-25-example/", payload["affected_roots"])
        release_check = next(check for check in payload["selected_checks"] if check["id"] == "release.validate")
        self.assertEqual(
            release_check["command"],
            "python scripts/validate-release.py --recorded-source-auto --version v0.1.1",
        )


    def test_multiple_release_paths_share_one_release_validation_check(self) -> None:
        result = self.select(
            [
                "docs/releases/v0.1.1/release.yaml",
                "docs/releases/v0.1.2/release.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("release.validate", selected_ids(payload))
        release_check = next(check for check in payload["selected_checks"] if check["id"] == "release.validate")
        self.assertEqual(
            release_check["command"],
            "python scripts/validate-release.py --recorded-source-auto --version v0.1.1 v0.1.2",
        )


    def test_release_profile_path_uses_profile_filename_as_version(self) -> None:
        result = self.select(["docs/releases/profiles/v0.4.0.yaml"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        release_check = next(
            check for check in payload["selected_checks"] if check["id"] == "release.validate"
        )
        self.assertEqual(
            release_check["command"],
            "python scripts/validate-release.py --recorded-source-auto --version v0.4.0",
        )


    def test_release_transaction_scripts_and_fixtures_select_focused_regression(self) -> None:
        result = self.select(
            [
                "scripts/lib/release/release_transaction.py",
                "scripts/lib/release/release_candidate.py",
                "scripts/lib/release/release_execution.py",
                "scripts/lib/release/release_provider.py",
                "scripts/lib/release/release_coordination.py",
                "scripts/release-coordinator.py",
                "tests/engineering/release/test-release-transaction.py",
                "scripts/prepare-release.py",
                "scripts/release-preflight.py",
                "scripts/close-release-publication.py",
                "tests/fixtures/release-transaction/profiles/valid-routine-v0.3.5.yaml",
                "tests/fixtures/release-transaction/literal-audit/valid-baseline.yaml",
                "tests/fixtures/release-transaction/surface-inventory/valid-inventory.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertNotIn(
            "manual-routing-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertIn("release_transaction.regression", selected_ids(payload))
        check = next(
            check for check in payload["selected_checks"] if check["id"] == "release_transaction.regression"
        )
        self.assertEqual(check["command"], "python tests/engineering/release/test-release-transaction.py")


    def test_markdown_readability_validator_scripts_select_focused_regression(self) -> None:
        result = self.select(
            [
                "scripts/validate-markdown-readability.py",
                "tests/engineering/validation/test-markdown-readability-validator.py",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertNotIn(
            "manual-routing-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertIn("markdown_readability.regression", selected_ids(payload))
        check = next(
            check for check in payload["selected_checks"] if check["id"] == "markdown_readability.regression"
        )
        self.assertEqual(check["command"], "python tests/engineering/validation/test-markdown-readability-validator.py")


    def test_first_slice_representative_categories_route_or_block_safely(self) -> None:
        cases = [
            {
                "path": "dist/adapters/opencode/AGENTS.md",
                "category": "generated-adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": ".codex/skills/code-review/SKILL.md",
                "category": "generated-skills",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "docs/workflows.md",
                "category": "workflow-guidance",
                "status": "ok",
                "checks": {"selector.regression", "guide_system.validate"},
            },
            {
                "path": ".gitignore",
                "category": "ignore-policy",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "CONSTITUTION.md",
                "category": "governance",
                "status": "ok",
                "checks": {"selector.regression", "guide_system.validate"},
            },
            {
                "path": "schemas/change.schema.json",
                "category": "schemas",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "templates/example.md",
                "category": "templates",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "scripts/build-adapters.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "tests/engineering/packaging/test-adapter-distribution.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "scripts/validation_cache.py",
                "category": "validation-retirement",
                "status": "ok",
                "checks": {"governed_lifecycle_cli_wrapper.test", "change_metadata.regression"},
            },
            {
                "path": "scripts/test-validation-cache.py",
                "category": "validation-retirement",
                "status": "ok",
                "checks": {"governed_lifecycle_cli_wrapper.test", "change_metadata.regression"},
            },
            {
                "path": "scripts/validate-skills.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "adapters.regression"},
            },
            {
                "path": "tests/skill/review_independence_skill_phrases.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "adapters.regression"},
            },
            {
                "path": "scripts/validate-guide-system.py",
                "category": "guide-system-validator",
                "status": "ok",
                "checks": {"guide_system.regression", "guide_system.validate"},
            },
            {
                "path": "tests/engineering/validation/test-guide-system-validator.py",
                "category": "guide-system-validator",
                "status": "ok",
                "checks": {"guide_system.regression", "guide_system.validate"},
            },
            {
                "path": "scripts/lifecycle_state_sync.py",
                "category": "validator-artifact-lifecycle",
                "status": "ok",
                "checks": {"governed_lifecycle_cli_wrapper.test"},
            },
            {
                "path": "scripts/change_metadata_semantics.py",
                "category": "validator-change-metadata",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "scripts/query-change-record.py",
                "category": "change-record-query",
                "status": "ok",
                "checks": {"record_retirement.regression", "change_metadata.regression", "selector.regression"},
            },
            {
                "path": "scripts/workflow_automation.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/workflow_code_state.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/test-workflow-code-state.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/workflow_automation_policy.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/workflow_automation_state.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/validate_workflow_automation.py",
                "category": "workflow-automation",
                "status": "ok",
                "checks": {
                    "rigorloop_cli.test",
                },
            },
            {
                "path": "scripts/build-skills.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "adapters.regression"},
            },
            {
                "path": "tests/fixtures/skills/skill-readability/valid-pilot/SKILL.md",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "adapters.regression"},
            },
            {
                "path": "tests/fixtures/skills",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "adapters.regression"},
            },
            {
                "path": "scripts/validate-release.py",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "scripts/validate-release-ci.py",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": ".github/workflows/release.yml",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "scripts/ci.sh",
                "category": "ci-wrapper",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": ".github/workflows/ci.yml",
                "category": "ci-workflow",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "docs/plan.md",
                "category": "plan-index",
                "status": "ok",
                "checks": {"current_records.validate", "guide_system.validate"},
            },
            {
                "path": "docs/plan-archive.md",
                "category": "plan-index",
                "status": "ok",
                "checks": {"current_records.validate", "guide_system.validate"},
            },
            {
                "path": "docs/architecture/system/diagrams/context.mmd",
                "category": "architecture-diagram",
                "status": "ok",
                "checks": {"current_records.validate"},
            },
            {
                "path": "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
                "category": "artifact-lifecycle-fixtures",
                "status": "ok",
                "checks": {"governed_lifecycle_cli_wrapper.test"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"skills.regression"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-requirement-compression-calibration/reviews/code-review-r1.md",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"skills.regression"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"skills.regression", "change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/change-metadata/compact-valid/change.yaml",
                "category": "change-metadata-fixtures",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/change-metadata",
                "category": "change-metadata-fixtures",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
                "category": "retired-spec-read",
                "status": "ok",
                "checks": {"selector.regression", "skills.regression", "skills.regression"},
            },
            {
                "path": "scripts/test-fidelity-gate-spec-reads.py",
                "category": "retired-spec-read",
                "status": "ok",
                "checks": {"selector.regression", "skills.regression", "skills.regression"},
            },
            {
                "path": "scripts/measure-skill-tokens.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "scripts/analyze-codex-jsonl.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "scripts/test-token-cost-measurement.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "scripts/run-token-cost-benchmarks.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": 'scripts/measure-cli-result-bytes.py',
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": 'scripts/test-cli-result-measurement.py',
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "scripts/validate-token-cost-report.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "scripts/test-token-cost-report-validation.py",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "benchmarks/token-cost/manifest.yaml",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "benchmarks/token-cost/prompts/proposal-short.md",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "benchmarks/token-cost/fixtures/minimal-public-project/AGENTS.md",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "docs/reports/token-cost/2026-05-10-baseline.md",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "docs/reports/token-cost/releases/v0.1.1.yaml",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "docs/reports/adapter-artifacts/releases/v0.1.2.yaml",
                "category": "adapter-artifact-metadata",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.analysis.yaml",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "packages/rigorloop/package.json",
                "category": "rigorloop-cli",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "npm_package_publication.test"},
            },
            {
                "path": "tests/engineering/packaging/test-npm-package-publication.py",
                "category": "rigorloop-cli",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "npm_package_publication.test"},
            },
            {
                "path": "scripts/validate-governed-lifecycle-cli.py",
                "category": "governed-lifecycle-cli-wrapper",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "governed_lifecycle_cli_wrapper.test"},
            },
            {
                "path": "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
                "category": "governed-lifecycle-cli-wrapper",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "governed_lifecycle_cli_wrapper.test"},
            },
            {
                "path": "tests/fixtures/token-cost/sample-codex-session.jsonl",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
            {
                "path": "tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml",
                "category": "retired-token-cost",
                "status": "ok",
                "checks": {"selector.regression", "adapters.regression", "release_transaction.regression"},
            },
        ]

        for case in cases:
            with self.subTest(path=case["path"]):
                result = self.select([case["path"]])
                payload = result.to_json_dict()

                self.assertEqual(result.status, case["status"])
                self.assertIn({"path": case["path"], "category": case["category"]}, payload["classified_paths"])
                if case.get("checks"):
                    self.assertTrue(case["checks"].issubset(selected_ids(payload)))
                if case.get("blocking_code"):
                    self.assertIn(
                        case["blocking_code"],
                        {item["code"] for item in payload["blocking_results"]},
                    )


    def test_learn_artifact_paths_are_known_lightweight_paths(self) -> None:
        paths = [
            "docs/learn/README.md",
            "docs/learn/sessions/2026-05-04-example.md",
            "docs/learn/topics/verification.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": "learn-artifact"}, payload["classified_paths"])

        self.assertNotIn("current_records.validate", selected_ids(payload))
        self.assertEqual({"guide_system.validate"}, selected_ids(payload))


    def test_research_artifact_path_selects_document_checks_without_unclassified_block(self) -> None:
        path = "docs/research/2026-08-05-boundary-first-v1-activation-release.md"

        result = self.select([path])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": path, "category": "research-artifact"}, payload["classified_paths"])
        self.assertEqual(
            {"documentation_prose.audit", "markdown_readability.validate"},
            selected_ids(payload),
        )


    def test_retired_docs_examples_path_is_known_during_deletion_compatibility(self) -> None:
        paths = ["docs/examples/README.md"]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn(
                    {"path": path, "category": "retired-examples"},
                    payload["classified_paths"],
                )

        self.assertNotIn("current_records.validate", selected_ids(payload))
        self.assertEqual(payload["selected_checks"], [])


    def test_follow_up_register_path_selects_static_validation(self) -> None:
        path = "docs/follow-ups.md"

        result = self.select([path])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": path, "category": "follow-up-register"}, payload["classified_paths"])
        self.assertEqual({"skills.regression"}, selected_ids(payload))


    def test_plan_index_surfaces_select_lifecycle_validation_with_both_surfaces(self) -> None:
        result = self.select(["docs/plan-archive.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": "docs/plan-archive.md", "category": "plan-index"}, payload["classified_paths"])
        self.assertIn("current_records.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "current_records.validate")
        self.assertEqual(lifecycle_check["command"], "python scripts/validate-governed-lifecycle-cli.py")
        self.assertIn("guide_system.validate", selected_ids(payload))


    def test_selector_and_validation_script_paths_select_regressions(self) -> None:
        result = self.select(["scripts/select-validation.py", "scripts/validate-governed-lifecycle-cli.py"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("governed_lifecycle_cli_wrapper.test", selected_ids(payload))
        self.assertIn("rigorloop_cli.test", selected_ids(payload))


    def test_governance_paths_select_deterministic_proof_instead_of_empty_ok(self) -> None:
        result = self.select(["AGENTS.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "AGENTS.md", "category": "governance"}, payload["classified_paths"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])


    def test_pr_contained_lifecycle_surfaces_exclude_published_skill_path(self) -> None:
        paths = [
            "AGENTS.md",
            "CONSTITUTION.md",
            "docs/workflows.md",
            "skills/workflow/SKILL.md",
            "docs/changes/2026-05-05-example/change.yaml",
            "docs/changes/2026-05-05-example/review-resolution.md",
        ]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertIn("current_records.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "current_records.validate")
        self.assertEqual(shlex.split(lifecycle_check["command"]),
                         ["python", "scripts/validate-governed-lifecycle-cli.py"])
        self.assertIn("record_retirement.regression", selected_ids(payload))


    def test_readme_path_selects_lightweight_readme_validation(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-no-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text("# Example\n\nNo generated vision marker block.\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("readme.validate", selected_ids(payload))
        self.assertIn("markdown_readability.validate", selected_ids(payload))
        self.assertIn("guide_system.validate", selected_ids(payload))
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        readability_check = next(
            check for check in payload["selected_checks"] if check["id"] == "markdown_readability.validate"
        )
        self.assertEqual(readability_check["changed_sections"], ["README.md:1:3"])
        self.assertIn("--changed-section README.md:1:3", readability_check["command"])
        self.assertFalse(payload["blocking_results"])


    def test_workflow_guidance_selects_composed_guide_system_validator(self) -> None:
        result = self.select(["docs/workflows.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "docs/workflows.md", "category": "workflow-guidance"}, payload["classified_paths"])
        self.assertIn("guide_system.validate", selected_ids(payload))
        guide_check = next(check for check in payload["selected_checks"] if check["id"] == "guide_system.validate")
        self.assertEqual(guide_check["command"], "python scripts/validate-guide-system.py")
        self.assertIn("cross-guide validation", guide_check["reason"])


    def test_readme_marker_validation_is_selected_for_marker_block_or_vision_scope(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )

        marker_result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        marker_payload = marker_result.to_json_dict()

        self.assertEqual(marker_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(marker_payload)))

        scoped_result = self.select(["README.md", "skills/vision/SKILL.md"])
        scoped_payload = scoped_result.to_json_dict()

        self.assertEqual(scoped_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(scoped_payload)))
        self.assertFalse(scoped_payload["unclassified_paths"])
        self.assertFalse(scoped_payload["blocking_results"])


    def test_root_vision_path_selects_marker_validation_without_unclassified_block(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-root-vision-"))
        self.addCleanupTree(temp_root)
        (temp_root / "VISION.md").write_text("# Project Vision\n\nExample vision.\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("VISION.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "VISION.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("markdown_readability.validate", selected_ids(payload))
        self.assertIn("readme.vision_markers", selected_ids(payload))
        readability_check = next(
            check for check in payload["selected_checks"] if check["id"] == "markdown_readability.validate"
        )
        self.assertEqual(readability_check["changed_sections"], ["VISION.md:1:3"])
        self.assertIn("--changed-section VISION.md:1:3", readability_check["command"])
        self.assertFalse(payload["blocking_results"])


    def test_vision_rationale_path_selects_lifecycle_validation_without_unclassified_block(self) -> None:
        result = self.select(["docs/vision/strategic-positioning.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn(
            {"path": "docs/vision/strategic-positioning.md", "category": "lifecycle"},
            payload["classified_paths"],
        )
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("current_records.validate", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])


    def test_retired_lowercase_root_vision_path_blocks_as_unclassified(self) -> None:
        result = self.select(["vision.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertNotIn({"path": "vision.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], ["vision.md"])
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})


    def test_retired_lowercase_root_vision_presence_does_not_create_global_conflict(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-retired-vision-presence-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        (temp_root / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        (temp_root / "VISION.md").write_text("# Canonical Vision\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])


    def test_pr_handoff_surfaces_select_deterministic_checks(self) -> None:
        result = self.select(
            [
                ".github/workflows/ci.yml",
                "docs/workflows.md",
                "docs/plan.md",
                "docs/changes/2026-04-25-example/explain-change.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("current_records.validate", selected_ids(payload))


    def test_architecture_support_paths_route_without_manual_blocks(self) -> None:
        result = self.select(
            [
                "docs/architecture/system/diagrams/context.mmd",
                "docs/architecture/system/diagrams/container.mmd",
                "docs/changes/2026-04-25-example/architecture.md",
                "docs/changes/2026-04-25-example/diagrams/context.mmd",
                "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("current_records.validate", selected_ids(payload))
        self.assertIn("governed_lifecycle_cli_wrapper.test", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "current_records.validate")
        self.assertEqual(lifecycle_check["command"], "python scripts/validate-governed-lifecycle-cli.py")


    def test_workflow_refactor_surface_set_selects_expected_checks(self) -> None:
        paths = [
            "CONSTITUTION.md",
            "AGENTS.md",
            "README.md",
            "docs/workflows.md",
            "docs/plan.md",
            "docs/plan-archive.md",
            "docs/plans/2026-05-03-workflow-refactor.md",
            "docs/vision/strategic-positioning.md",
            "docs/proposals/2026-05-01-workflow-refactor.md",
            "specs/rigorloop-workflow.md",
            "specs/rigorloop-workflow.test.md",
            "skills/workflow/SKILL.md",
            ".codex/skills/workflow/SKILL.md",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md",
            "tests/engineering/validation/test-select-validation.py",
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
            "scripts/build-skills.py",
            "scripts/test-build-skills.py",
            "tests/skill/test-skill-validator.py",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md",
            "docs/changes/2026-05-03-workflow-refactor/verify-report.md",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        expected_categories = {
            "CONSTITUTION.md": "governance",
            "AGENTS.md": "governance",
            "README.md": "readme",
            "docs/workflows.md": "workflow-guidance",
            "docs/plan.md": "plan-index",
            "docs/plan-archive.md": "plan-index",
            "docs/plans/2026-05-03-workflow-refactor.md": "lifecycle",
            "docs/vision/strategic-positioning.md": "lifecycle",
            "docs/proposals/2026-05-01-workflow-refactor.md": "lifecycle",
            "specs/rigorloop-workflow.md": "lifecycle",
            "specs/rigorloop-workflow.test.md": "lifecycle",
            "skills/workflow/SKILL.md": "skills",
            ".codex/skills/workflow/SKILL.md": "generated-skills",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md": "generated-adapters",
            "tests/engineering/validation/test-select-validation.py": "selector",
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py": "governed-lifecycle-cli-wrapper",
            "scripts/build-skills.py": "validator-skills",
            "scripts/test-build-skills.py": "validator-skills",
            "tests/skill/test-skill-validator.py": "validator-skills",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml": "change-records",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md": "change-records",
            "docs/changes/2026-05-03-workflow-refactor/verify-report.md": "change-records",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md": "change-records",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md": "change-records",
        }
        for path, category in expected_categories.items():
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": category}, payload["classified_paths"])

        self.assertTrue(
            {
                "skills.validate",
                "skills.regression",
                "adapters.regression",
                "adapters.drift",
                "adapters.validate",
                "record_retirement.regression",
                "governed_lifecycle_cli_wrapper.test",
                "current_records.validate",
                "guide_system.validate",
                "readme.validate",
                "readme.vision_markers",
                "selector.regression",
            }.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["broad_smoke_required"])
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "current_records.validate")
        self.assertEqual(lifecycle_check["command"], "python scripts/validate-governed-lifecycle-cli.py")


    def test_broad_smoke_sources_are_attributed(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        plan_path = temp_root / "docs" / "plans" / "active.md"
        plan_path.parent.mkdir(parents=True)
        plan_path.write_text("broad_smoke_required: true\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                broad_smoke=True,
                trigger_context_paths=(str(plan_path),),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "explicit_flag", "value": "--broad-smoke"}, sources)
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)


    def test_broad_smoke_sources_include_test_spec_and_review_resolution_context(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        context_files = {
            "docs/plans/active.md": "broad_smoke_required: true\n",
            "specs/example.test.md": "- broad smoke required before final verify\n",
            "docs/changes/example/review-resolution.md": "- broad smoke required by review closeout\n",
        }
        for relative_path, content in context_files.items():
            target = temp_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                trigger_context_paths=tuple(context_files),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)
        self.assertIn({"type": "test_spec", "path": "specs/example.test.md"}, sources)
        self.assertIn(
            {"type": "review_resolution", "path": "docs/changes/example/review-resolution.md"},
            sources,
        )


    def test_spec_read_retirement_removes_catalog_and_mode_entry(self) -> None:
        self.assertNotIn("requirement_fidelity.spec_reads", CHECK_CATALOG)
        for ids in MODE_CHECK_IDS.values():
            self.assertNotIn("requirement_fidelity.spec_reads", ids)


    def test_readme_validator_accepts_absent_or_valid_standalone_marker_block(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-validator-"))
        self.addCleanupTree(temp_root)
        readme = temp_root / "README.md"
        readme.write_text(
            "# Example\n\nInline `<!-- vision:start -->` text is not a generated marker block.\n",
            encoding="utf-8",
        )

        absent = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(absent.returncode, 0, msg=absent.stdout + absent.stderr)

        readme.write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        valid = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, msg=valid.stdout + valid.stderr)

        readme.write_text("# Example\n\n<!-- vision:start -->\nMissing end.\n", encoding="utf-8")
        malformed = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(malformed.returncode, 0)


    def test_ci_wrapper_duration_reporting_does_not_use_bash_seconds(self) -> None:
        ci_text = CI.read_text(encoding="utf-8")

        self.assertNotIn("$SECONDS", ci_text)
        self.assertIn("time.monotonic()", (ROOT / "scripts/lib/validation/validation_execution.py").read_text())
        self.assertNotIn("run_check()", ci_text)


    def test_pr_lifecycle_catalog_preserves_revision_scope(self) -> None:
        command = catalog_command("current_records.snapshot", mode="pr",
                                  base="base-sha", head="head-sha",
                                  paths=("docs/plans/example.md",))
        self.assertEqual(shlex.split(command),
                         ["python", "scripts/validate-governed-lifecycle-cli.py", "--revision", "head-sha"])
        with self.assertRaises(ValueError):
            catalog_command("current_records.snapshot", mode="pr", paths=("README.md",))


    def test_catalog_rejects_unknown_value_for_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported catalog mode"):
            catalog_command("current_records.validate", mode="unknown_value", paths=("README.md",))


    def test_workflow_guidance_aligns_with_validation_layering_contract(self) -> None:
        expectations = {
            "skills/implement/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "project's validation selector",
                "selected checks",
                "skills.validate",
            ],
            "skills/code-review/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "selected checks",
                "direct proof",
            ],
            "skills/verify/SKILL.md": [
                "registered evidence",
                "manual by design",
                "manual proof",
                "release metadata",
                "not-run",
                "project's broad validation command",
                "broad_smoke_required",
            ],
            "skills/route/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "broad_smoke.sources",
                "workflow-context",
            ],
        }

        for path, required_terms in expectations.items():
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, content)


    def test_hosted_ci_remains_thin_and_matrix_free(self) -> None:
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

        self.assertIn("bash scripts/ci.sh --mode pr", workflow)
        self.assertIn("bash scripts/ci.sh --mode main", workflow)
        forbidden_terms = [
            "matrix:",
            "check-id:",
            "fromJson",
            "scripts/select-validation.py",
            "actions/cache",
            "distributed",
            "sandbox",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, workflow)


    def test_hosted_ci_installs_locked_public_package_dependencies_before_validation(self) -> None:
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        install_command = "npm ci --prefix packages/rigorloop"
        validation_command = "bash scripts/ci.sh --mode pr"

        self.assertIn(install_command, workflow)
        self.assertLess(workflow.index(install_command), workflow.index(validation_command))


    def test_normalize_path_rejects_outside_repository_paths(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-paths-"))
        self.addCleanupTree(temp_root)
        outside = temp_root.parent / "outside.txt"

        normalized = normalize_path(str(outside), repo_root=temp_root)
        self.assertFalse(normalized.ok)
        self.assertEqual(normalized.blocking_code, "outside-repository-path")
