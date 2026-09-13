# M3 validation execution evidence

This records bounded adoption observations for the current initiative, not a maintained test inventory or a performance target. The owning change record controls stage state. Final review, Verify and PR readiness are separate.

## Delivered behavior and protection

The authored catalog consolidates identical full commands with identical inputs and no preparation dependencies. There are 54 executable/group entries after consolidation, compared with 83 before; all 12 broad-smoke and 27 main memberships remain. Main v0.1.5 and broad v0.1.3 archive builds/validators stay distinct and retain build-success dependencies. The selected adapter subset and complete adapter suite remain different scopes. Historical records retain their original IDs and bytes.

Composition retains canonical IDs in selection order, combines selecting reasons, rejects conflicting argv/resource/preparation definitions before launch, then applies the focused gate to remaining boundary work. Explicit diagnostic work preserves failed focused results. Reports contain actual work once and identify unsuccessful boundary scope even when its checks were all covered by focused work. No cache or runtime equivalence inference is introduced.

Three permanent full-production-suite comparison cases were removed: `test_real_selector_cases_match_direct_sequential_and_reverse_parallel`, `test_real_lifecycle_cases_match_direct_sequential_and_reverse_parallel`, and `test_real_metadata_cases_match_direct_sequential_and_reverse_parallel`. Their repeated complete normal/single/reversed executions are replaced by this bounded adoption observation. Recurring mechanism proof retains a two-case normal/isolated fixture with real setup/cleanup and observed overlap, actual metadata wrapper integration, normal custom filtering and dynamic discovery, and negative zero/duplicate/loader/skip/missing/unknown/disagreeing-receipt cases. Dependency, fail-fast, timeout, signal, descendant cleanup, nested budget and separate output protection remain. Four composition cases add actual once-only execution, failure-gate/diagnostic behavior, preparation preservation, distinct observations, conflicting definitions and fresh invocation proof. The executor population changes from 38 to 40 cases; no other M3 population is deleted.

All four M3 suites use per-case processes and owned temporary directories. Process-global environment and monkeypatches stay within each process. Git fixtures use owned repositories; immutable canonical inputs are read only. Nested scheduler tests consume their allocated budget; the exclusive-resource scenarios test the scheduler's barrier inside an otherwise independent case. The executor's 40 retained cases are promoted only after complete normal, individual and reversed-parallel observations.

## Corrections found by proof

The new composition tests first failed against duplicate execution and absent conflict rejection, then passed after composition was corrected. A real wrapper test found the old mode-membership guard incorrectly rejecting shared canonical IDs; unresolved placeholders still require composition scope. A serial-barrier fixture now uses an actually unassessed command instead of the read-only skill validator that already had a direct-mode parallel assessment. The retirement ledger test previously subtracted all direct-mode IDs from a live catalog to reconstruct historical scope; it now uses the exact original inventory captured from pre-consolidation commit `8984f099`. Historical ledger bytes and judgments are unchanged. This is a current caller correction, not renewed historical cleanup.

A discovery command using `-k broad_smoke` on the adapter suite selected zero tests; it is not passing evidence. The exact consumer case was then run successfully. The first executor/full-selector runs exposed the above guards and fixture assumptions and are recorded as failed observations, not adoption evidence.

## Commands and limits

The commands run include `python scripts/test-validation-execution.py`, `python scripts/test-select-validation.py`, the exact adapter consumer case, all 17 retirement-ledger cases, and the required explicit CI invocation. The normal observations below call each original entrypoint through the existing outer-runner observer, preserving its normal loader and test bodies. Isolated observations use existing internal functions, with fresh process receipts for every discovered case. Jobs=1 and reversed jobs=2 are separate fresh executions. Timings describe these local invocations while other validation was running; they establish neither a universal speed improvement nor a CI duration target.

The final composition and unknown/conflicting-constraint case checks were refreshed after adding the explicit all-overlap failed-gate summary and strict bool/int distinction. These additions change neither discovery nor fixture isolation; unchanged full-population observations retain their stated bounds.

## Reproduction procedure

Run from the repository root. This temporary harness is adoption evidence, not a new public runner. It uses the existing internal executor and stores invocation-owned receipts/logs outside authored roots.

```python
import sys,os,json,time,shlex
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
from validation_execution import discover_cases,case_plans,_case_command,CheckPlan,run_scheduled_checks
out=Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
for name in sys.argv[2:]:
 root=out/Path(name).stem;root.mkdir(exist_ok=True)
 args=[sys.executable,str(Path(name).resolve())]
 ids=discover_cases(args,root/'collection',jobs=2,timeout=600)
 data={'entrypoint':name,'ids':ids,'observations':[]}; print('DISCOVERED',name,len(ids),flush=True)
 for mode in ('normal','single','reverse'):
  start=time.monotonic();scratch=root/mode
  if mode=='normal':
   receipt=scratch/'normal.json'; command=_case_command('observe',receipt,args)
   plans=[CheckPlan('normal',shlex.join(args),command,None,'focused',False)]
   jobs=1
  else:
   parent=CheckPlan('suite',shlex.join(args),args,None,'focused',True)
   plans=case_plans(parent,ids if mode=='single' else list(reversed(ids)),scratch/'cases');jobs=1 if mode=='single' else 2
  results=run_scheduled_checks(plans,jobs=jobs,timeout_seconds=600,fail_fast=False,scratch=scratch/'run')
  failed=[{'id':r.plan.check_id,'code':r.exit_code,'reason':r.exit_reason,'stdout':str(r.stdout_path),'stderr':str(r.stderr_path)} for r in results if r.exit_code]
  if mode=='normal':
   rec=json.loads(receipt.read_text()) if receipt.exists() else {}
   assert rec.get('discovered')==ids and rec.get('started')==ids and rec.get('completed')==ids,rec
  else:
   assert sorted(r.plan.case_id for r in results)==sorted(ids)
  data['observations'].append({'mode':mode,'jobs':jobs,'elapsed':round(time.monotonic()-start,3),'count':len(ids),'failed':failed})
  (root/'result.json').write_text(json.dumps(data,indent=2)+'\n')
  print(name,mode,data['observations'][-1],flush=True)
  if failed: raise SystemExit(1)
```

The temporary script above was saved as `/tmp/rigorloop-python-adoption.py` and invoked with:

```bash
python /tmp/rigorloop-python-adoption.py /tmp/m3-adoption-fixed scripts/test-validation-execution.py scripts/test-artifact-lifecycle-validator.py scripts/test-change-metadata-validator.py
python /tmp/rigorloop-python-adoption.py /tmp/m3-selector-adoption scripts/test-select-validation.py
```

## Authored catalog dispositions

| Previous ID | Canonical ID |
| --- | --- |
| `main.boundary_first.validate` | `boundary_first.validate` |
| `broad_smoke.skills.validate` | `skills.validate` |
| `main.skills.validate` | `skills.validate` |
| `broad_smoke.skills.regression` | `skills.regression` |
| `main.skills.regression` | `skills.regression` |
| `broad_smoke.review_artifacts.regression` | `review_artifacts.regression` |
| `main.review_artifacts.regression` | `review_artifacts.regression` |
| `broad_smoke.artifact_lifecycle.regression` | `artifact_lifecycle.regression` |
| `main.artifact_lifecycle.regression` | `artifact_lifecycle.regression` |
| `broad_smoke.change_metadata.regression` | `change_metadata.regression` |
| `main.change_metadata.regression` | `change_metadata.regression` |
| `main.change_record_query.regression` | `change_record_query.regression` |
| `main.workflow_automation.code_state_regression` | `workflow_automation.code_state_regression` |
| `main.workflow_automation.engine_regression` | `workflow_automation.engine_regression` |
| `main.workflow_automation.policy_regression` | `workflow_automation.policy_regression` |
| `main.workflow_automation.state_regression` | `workflow_automation.state_regression` |
| `main.workflow_automation.validator_regression` | `workflow_automation.validator_regression` |
| `main.release_transaction.regression` | `release_transaction.regression` |
| `main.readme.validate` | `readme.validate` |
| `main.readme.vision_markers` | `readme.vision_markers` |
| `main.markdown_readability.regression` | `markdown_readability.regression` |
| `main.guide_system.regression` | `guide_system.regression` |
| `main.guide_system.validate` | `guide_system.validate` |
| `broad_smoke.selector.regression` | `selector.regression` |
| `main.requirement_fidelity.spec_reads` | `requirement_fidelity.spec_reads` |
| `main.rigorloop_cli.test` | `rigorloop_cli.test` |
| `main.governed_lifecycle_cli_wrapper.test` | `governed_lifecycle_cli_wrapper.test` |
| `broad_smoke.validation_execution.regression` | `validation_execution.regression` |
| `main.adapters.regression` | `adapters.full_regression` |
| `broad_smoke.adapters.regression` | `adapters.full_regression` |

## Completed observations

Environment: Linux-6.18.33.2-microsoft-standard-WSL2-x86_64-with-glibc2.39, Python 3.12.3. Timings are seconds; no isolated machine or unlike-scope baseline claim.

### scripts/test-artifact-lifecycle-validator.py

```json
{
  "entrypoint": "scripts/test-artifact-lifecycle-validator.py",
  "ids": [
    "ArtifactLifecycleValidatorFixtureTests.test_active_test_spec_may_delegate_live_state_to_current_handoff_summary",
    "ArtifactLifecycleValidatorFixtureTests.test_active_test_spec_stale_implementation_readiness_fails",
    "ArtifactLifecycleValidatorFixtureTests.test_architecture_contract_matches_canonical_arc42_skeleton",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_activation_requires_gate_ready_and_persistence",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_architecture_assessment_routes_or_pauses",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_default_off_and_isolated_reviews_do_not_autoprogress",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_resume_and_cancellation_state_transitions",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_resume_is_idempotent_and_stops_on_ambiguity",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_state_gates_fail_closed",
    "ArtifactLifecycleValidatorFixtureTests.test_authoring_profile_stops_on_nonclean_review_decision_and_budget",
    "ArtifactLifecycleValidatorFixtureTests.test_automation_active_plan_context_rejects_ambiguous_current_milestone",
    "ArtifactLifecycleValidatorFixtureTests.test_automation_active_plan_context_reuses_canonical_handoff",
    "ArtifactLifecycleValidatorFixtureTests.test_cli_requires_explicit_paths",
    "ArtifactLifecycleValidatorFixtureTests.test_cli_requires_pr_ci_and_push_ci_inputs",
    "ArtifactLifecycleValidatorFixtureTests.test_current_v3_validation_does_not_decode_archival_baseline",
    "ArtifactLifecycleValidatorFixtureTests.test_direct_review_unchanged_by_requirement_fidelity_gate",
    "ArtifactLifecycleValidatorFixtureTests.test_dist_adapters_generated_output_path_is_rejected",
    "ArtifactLifecycleValidatorFixtureTests.test_duplicate_spec_identifier_fails",
    "ArtifactLifecycleValidatorFixtureTests.test_er_m5_001_recording_lifecycle_unknown_value_and_malformed_fail_closed",
    "ArtifactLifecycleValidatorFixtureTests.test_er_m5_001_recording_lifecycle_uses_complete_set_without_legacy_reviews",
    "ArtifactLifecycleValidatorFixtureTests.test_er_m5_002_recording_tracked_revision_never_uses_live_bytes",
    "ArtifactLifecycleValidatorFixtureTests.test_er_pr_002_snapshot_accepts_complete_set_above_request_limit",
    "ArtifactLifecycleValidatorFixtureTests.test_explicit_paths_ignore_unrelated_invalid_fixture_files",
    "ArtifactLifecycleValidatorFixtureTests.test_generated_output_path_is_rejected",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_allows_approved_generated_outputs_outside_finding_union",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_allows_approved_projections_and_evidence_outside_finding_union",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_declared_safe_required_fields_are_enumerated",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_enforce_ci_scope_and_audit",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_enforce_path_scope_and_commands",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_enforce_round_cap_and_shrinking_sets",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_mechanical_pauses_on_empty_deterministic_authority",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_mechanical_pauses_without_deterministic_authority",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_mechanical_required_fields_are_enumerated",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_pause_on_unclassified_or_invalid_findings",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_pauses_when_changed_outside_reviewer_union",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_pauses_when_finding_has_no_affected_paths",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_pauses_when_top_level_disagrees_with_findings",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_resolved_finding_does_not_contribute_to_allowed_paths",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_correction_guardrails_unknown_auto_fix_class_pauses",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_profile_activation_requires_clean_planning_and_phase",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_profile_ignores_retired_test_spec_inputs",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_profile_milestones_run_in_order_and_resume_idempotently",
    "ArtifactLifecycleValidatorFixtureTests.test_implementation_profile_phase_boundaries_refuse_closeout_until_promoted",
    "ArtifactLifecycleValidatorFixtureTests.test_invalid_fixtures_fail",
    "ArtifactLifecycleValidatorFixtureTests.test_legacy_proposal_without_status_still_fails",
    "ArtifactLifecycleValidatorFixtureTests.test_local_mode_blocks_duplicate_identifier_when_any_participant_is_related",
    "ArtifactLifecycleValidatorFixtureTests.test_local_mode_blocks_related_and_warns_unrelated_baseline",
    "ArtifactLifecycleValidatorFixtureTests.test_merge_dependent_lifecycle_language_warns_without_blocking",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_archive_contract_accepts_terminal_once_across_recent_and_archive",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_archive_contract_rejects_archive_only_nonterminal_plan",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_archive_contract_rejects_duplicate_terminal_entry",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_archive_contract_rejects_missing_terminal_entry",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_archive_contract_rejects_recent_done_over_cap",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_body_terminal_marker_alone_requires_done_location",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_context_blocks_invalid_referenced_workflow_authority",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_index_change_validates_linked_plan_body",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_index_context_expands_to_workflow_authority_artifacts",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_lifecycle_marker_does_not_infer_terminal_state_from_prose",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_lifecycle_marker_rejects_contradictory_and_unknown_values",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_scope_uses_current_context_refs_but_ignores_future_milestone_targets",
    "ArtifactLifecycleValidatorFixtureTests.test_plan_supersession_context_requires_structural_fields",
    "ArtifactLifecycleValidatorFixtureTests.test_pr_ci_mode_ignores_generated_outputs_in_diff",
    "ArtifactLifecycleValidatorFixtureTests.test_pr_ci_mode_ignores_untracked_baseline_artifacts",
    "ArtifactLifecycleValidatorFixtureTests.test_pr_ci_mode_uses_explicit_diff_range",
    "ArtifactLifecycleValidatorFixtureTests.test_prepared_ci_rejects_wrong_revision_or_invalid_proof",
    "ArtifactLifecycleValidatorFixtureTests.test_push_main_ci_mode_ignores_untracked_baseline_artifacts",
    "ArtifactLifecycleValidatorFixtureTests.test_push_main_ci_mode_uses_explicit_diff_range",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_all_states_reject_missing_duplicate_and_unknown_value_rows",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_allows_complete_emergency_deferral",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_blocks_emergency_deferral_without_owner",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_blocks_missing_routine_gate_item",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_blocks_nondeferrable_registry_verification",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_blocks_secret_bearing_content",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_emergency_deferral_must_match_exactly_one_result",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_emergency_deferral_rejects_not_applicable_required_values",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_emergency_deferral_rejects_unknown_value_status",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_fixture_passes_lightweight_checklist",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_rejects_unknown_value_status",
    "ArtifactLifecycleValidatorFixtureTests.test_release_evidence_result_vocabulary_is_state_and_applicability_aware",
    "ArtifactLifecycleValidatorFixtureTests.test_repeated_explicit_validation_observes_current_failure_and_preserves_cache",
    "ArtifactLifecycleValidatorFixtureTests.test_requirement_fidelity_gate_blocks_clean_handoff_when_applicable_receipt_missing",
    "ArtifactLifecycleValidatorFixtureTests.test_requirement_fidelity_gate_unknown_values_fail_before_clean_continuation",
    "ArtifactLifecycleValidatorFixtureTests.test_retired_cache_options_and_unknown_value_mode_reject_without_writes",
    "ArtifactLifecycleValidatorFixtureTests.test_review_fix_autoprogression_activation_requires_authorization_and_clean_current_gate",
    "ArtifactLifecycleValidatorFixtureTests.test_review_fix_autoprogression_architecture_assessment_routes_or_stops",
    "ArtifactLifecycleValidatorFixtureTests.test_review_fix_autoprogression_rejects_unknown_targets_and_direct_reviews",
    "ArtifactLifecycleValidatorFixtureTests.test_review_fix_autoprogression_resume_and_terminal_state_transitions",
    "ArtifactLifecycleValidatorFixtureTests.test_review_fix_autoprogression_routes_through_target_bounds",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_authority_kind_invalid_parser_order",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_blocked_and_inconclusive_pause_without_resolution_routing",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_changes_requested_routes_only_when_profile_and_evidence_permit",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_clean_status_derivation_covers_every_clean_advance_gate",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_critical_authority_gates_clean_handoff",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_normalized_clean_outcomes_advance_only_with_valid_evidence",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_outcome_derives_from_native_status_and_gate_state",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_sampling_floors_affect_clean_handoff",
    "ArtifactLifecycleValidatorFixtureTests.test_review_gate_second_review_disagreement_prevents_automatic_continuation",
    "ArtifactLifecycleValidatorFixtureTests.test_simplified_proposal_rejects_malformed_current_structure",
    "ArtifactLifecycleValidatorFixtureTests.test_simplified_proposal_variants_pass",
    "ArtifactLifecycleValidatorFixtureTests.test_specs_docs_are_not_classified_as_behavior_specs",
    "ArtifactLifecycleValidatorFixtureTests.test_title_case_proposal_headings_pass",
    "ArtifactLifecycleValidatorFixtureTests.test_v3_recording_complete_set_and_unknown_value_fail_closed",
    "ArtifactLifecycleValidatorFixtureTests.test_v3_recording_tracked_snapshot_ignores_valid_live_replacement",
    "ArtifactLifecycleValidatorFixtureTests.test_valid_canonical_arc42_architecture_passes",
    "ArtifactLifecycleValidatorFixtureTests.test_valid_fixtures_pass",
    "ArtifactLifecycleValidatorFixtureTests.test_verified_ci_candidate_allows_only_its_pending_preflight",
    "CurrentRecordBoundaryTests.test_explicit_retired_root_rejects_without_parsing_archive",
    "CurrentRecordBoundaryTests.test_reserved_residue_without_manifest_is_validated_not_skipped"
  ],
  "observations": [
    {
      "mode": "normal",
      "jobs": 1,
      "elapsed": 65.814,
      "count": 108,
      "failed": []
    },
    {
      "mode": "single",
      "jobs": 1,
      "elapsed": 138.506,
      "count": 108,
      "failed": []
    },
    {
      "mode": "reverse",
      "jobs": 2,
      "elapsed": 105.211,
      "count": 108,
      "failed": []
    }
  ]
}
```

### scripts/test-validation-execution.py

```json
{
  "entrypoint": "scripts/test-validation-execution.py",
  "ids": [
    "CaseAdapterTests.test_actual_worker_rejects_skipped_missing_and_disagreeing_receipts",
    "CaseAdapterTests.test_case_expansion_preserves_declared_serial_resource_constraint",
    "CaseAdapterTests.test_expansion_keeps_all_case_dependencies_and_failed_case_blocks_consumer",
    "CaseAdapterTests.test_missing_or_unknown_value_receipt_cannot_reuse_a_previous_pass",
    "CaseAdapterTests.test_normal_and_isolated_fixture_preserve_hooks_population_and_parallelism",
    "CaseAdapterTests.test_normal_custom_patterns_and_dynamic_fixture_discovery_are_preserved",
    "CaseAdapterTests.test_real_discovery_duplicate_zero_and_loader_error_reject_before_cases",
    "CaseAdapterTests.test_real_wrapper_expands_selected_metadata_into_actual_cases",
    "CaseAdapterTests.test_unknown_adapter_mode_rejects_before_script_execution",
    "CatalogTests.test_case_unit_rejects_contradictory_command_before_launch",
    "CatalogTests.test_catalog_is_valid_and_unassessed_commands_are_serial",
    "CatalogTests.test_unknown_value_units_modes_fields_and_stale_basis_reject",
    "CompositionTests.test_boundary_only_and_new_invocation_execute_again",
    "CompositionTests.test_canonical_overlap_runs_once_with_reasons_and_failure_gate",
    "CompositionTests.test_catalog_composes_broad_and_main_with_distinct_preserved_package_versions",
    "CompositionTests.test_conflicting_same_id_arguments_or_constraints_reject_before_launch",
    "CompositionTests.test_overlap_preserves_preparation_and_distinct_observations",
    "CompositionTests.test_retired_classification_override_rejects_before_work",
    "CompositionTests.test_unknown_value_composed_mode_rejects",
    "ExecutionTests.test_budget_and_timeout_overrides_reject_invalid_values",
    "ExecutionTests.test_complete_graph_rejects_before_any_launch",
    "ExecutionTests.test_fail_fast_awaits_started_failure_and_marks_every_queued_task",
    "ExecutionTests.test_failed_parent_stops_queue_during_descendant_cleanup",
    "ExecutionTests.test_fast_orphan_with_replaced_environment_is_reaped_without_touching_unrelated_child",
    "ExecutionTests.test_independent_failure_continues_and_dependency_failure_prevents_launch",
    "ExecutionTests.test_interrupt_reaps_started_processes_and_retains_unfinished_results",
    "ExecutionTests.test_invalid_success_output_cannot_hide_decoding_failure",
    "ExecutionTests.test_malformed_empty_selection_and_unknown_value_labels_reject",
    "ExecutionTests.test_missing_capture_is_runner_failure",
    "ExecutionTests.test_nested_budget_caps_actual_children_and_unknown_value_rejects_before_launch",
    "ExecutionTests.test_observed_outcome_survives_cleanup_past_execution_timeout",
    "ExecutionTests.test_parallel_tasks_actually_overlap_with_bounded_workers",
    "ExecutionTests.test_reverse_completion_keeps_order_and_separate_streams",
    "ExecutionTests.test_selector_cannot_relabel_boundary_phase",
    "ExecutionTests.test_serial_barrier_and_queue_time_excluded",
    "ExecutionTests.test_signal_and_unavailable_command_are_distinct",
    "ExecutionTests.test_timeout_reaps_descendant_in_new_session",
    "ExecutionTests.test_timeout_terminates_descendant_that_ignores_term_and_retry_is_fresh",
    "ExecutionTests.test_unknown_value_phase_and_resource_constraints_reject",
    "ExecutionTests.test_unsupported_platform_rejects_before_launch"
  ],
  "observations": [
    {
      "mode": "normal",
      "jobs": 1,
      "elapsed": 52.449,
      "count": 40,
      "failed": []
    },
    {
      "mode": "single",
      "jobs": 1,
      "elapsed": 58.613,
      "count": 40,
      "failed": []
    },
    {
      "mode": "reverse",
      "jobs": 2,
      "elapsed": 28.242,
      "count": 40,
      "failed": []
    }
  ]
}
```

### scripts/test-change-metadata-validator.py

```json
{
  "entrypoint": "scripts/test-change-metadata-validator.py",
  "ids": [
    "ChangeMetadataValidatorFixtureTests.test_retired_measurement_input_rejects_without_reading_or_writing",
    "ExplicitRecordingMetadataTests.test_explicit_recording_metadata_accepts_structure_without_stage_eligibility",
    "ExplicitRecordingMetadataTests.test_explicit_recording_metadata_rejects_duplicate_keys_encoding_and_symlink",
    "ExplicitRecordingMetadataTests.test_explicit_recording_metadata_validates_registered_set_not_subject_freshness",
    "ExplicitRecordingMetadataTests.test_explicit_recording_unknown_value_and_mixed_contract_fail_closed",
    "ExplicitRecordingMetadataTests.test_recording_v3_full_set_and_unknown_value_version_fail_closed",
    "ExplicitRecordingMetadataTests.test_recording_v3_manifest_dispatch_preserves_contract_and_unknown_value_rejects"
  ],
  "observations": [
    {
      "mode": "normal",
      "jobs": 1,
      "elapsed": 12.551,
      "count": 7,
      "failed": []
    },
    {
      "mode": "single",
      "jobs": 1,
      "elapsed": 9.137,
      "count": 7,
      "failed": []
    },
    {
      "mode": "reverse",
      "jobs": 2,
      "elapsed": 5.001,
      "count": 7,
      "failed": []
    }
  ]
}
```

### scripts/test-select-validation.py

```json
{
  "entrypoint": "scripts/test-select-validation.py",
  "ids": [
    "ScriptOutputContractTests.test_output_contract_conflicting_output_flags_fail_before_tests_run",
    "ScriptOutputContractTests.test_output_contract_default_failure_expands_failures_only",
    "ScriptOutputContractTests.test_output_contract_default_success_is_single_summary_line",
    "ScriptOutputContractTests.test_output_contract_json_support_is_not_added_in_first_slice",
    "ScriptOutputContractTests.test_output_contract_quiet_failure_remains_actionable",
    "ScriptOutputContractTests.test_output_contract_quiet_success_is_silent",
    "ScriptOutputContractTests.test_output_contract_reliable_failure_includes_scoped_rerun",
    "ScriptOutputContractTests.test_output_contract_unreliable_failure_omits_misleading_scoped_rerun",
    "ScriptOutputContractTests.test_output_contract_verbose_success_preserves_full_pass_detail",
    "ScriptOutputContractTests.test_output_contract_zero_executed_tests_fail_with_summary",
    "ValidationSelectionTests.test_architecture_support_paths_route_without_manual_blocks",
    "ValidationSelectionTests.test_blocked_selection_diagnostic_broad_smoke_cannot_clear_original_blocker",
    "ValidationSelectionTests.test_boundary_checked_revision_surface_retains_sibling_validation_owners",
    "ValidationSelectionTests.test_boundary_first_surfaces_select_boundary_validation",
    "ValidationSelectionTests.test_boundary_sibling_failures_each_block_selected_execution",
    "ValidationSelectionTests.test_broad_smoke_default_success_captures_child_output_and_prints_aggregate",
    "ValidationSelectionTests.test_broad_smoke_explicit_jobs_parallelizes_eligible_children",
    "ValidationSelectionTests.test_broad_smoke_failed_build_prevents_archive_validation",
    "ValidationSelectionTests.test_broad_smoke_failure_prints_command_exit_duration_and_captured_output",
    "ValidationSelectionTests.test_broad_smoke_jobs_one_keeps_sequential_compatibility",
    "ValidationSelectionTests.test_broad_smoke_omitted_jobs_uses_assessed_default_concurrency",
    "ValidationSelectionTests.test_broad_smoke_parallel_multiple_failures_report_all_in_canonical_order",
    "ValidationSelectionTests.test_broad_smoke_parallel_result_evidence_records_child_phases",
    "ValidationSelectionTests.test_broad_smoke_parallel_runs_without_historical_classification",
    "ValidationSelectionTests.test_broad_smoke_parallel_verbose_groups_successful_child_output_in_order",
    "ValidationSelectionTests.test_broad_smoke_parallel_worker_crash_reports_scheduler_error",
    "ValidationSelectionTests.test_broad_smoke_reserved_missing_manifest_is_not_skipped",
    "ValidationSelectionTests.test_broad_smoke_routes_changed_records_to_current_v3_validator",
    "ValidationSelectionTests.test_broad_smoke_skips_unrelated_historical_descendants",
    "ValidationSelectionTests.test_broad_smoke_sources_are_attributed",
    "ValidationSelectionTests.test_broad_smoke_sources_include_test_spec_and_review_resolution_context",
    "ValidationSelectionTests.test_broad_smoke_verbose_prints_successful_child_output_in_order",
    "ValidationSelectionTests.test_canonical_skill_only_uses_purpose_built_checks_without_lifecycle",
    "ValidationSelectionTests.test_catalog_matches_v1_contract",
    "ValidationSelectionTests.test_catalog_records_audited_commands_and_initial_case_population",
    "ValidationSelectionTests.test_catalog_rejects_unknown_value_for_mode",
    "ValidationSelectionTests.test_change_metadata_validator_default_failure_is_actionable",
    "ValidationSelectionTests.test_change_metadata_validator_default_success_is_compact",
    "ValidationSelectionTests.test_change_metadata_validator_quiet_compatibility_is_preserved",
    "ValidationSelectionTests.test_change_metadata_validator_verbose_preserves_full_detail",
    "ValidationSelectionTests.test_change_metadata_validator_zero_selected_tests_fail",
    "ValidationSelectionTests.test_ci_wrapper_accepts_execution_flags_without_forwarding_to_selector",
    "ValidationSelectionTests.test_ci_wrapper_default_budget_is_capped_and_parent_allocation_bounds_override",
    "ValidationSelectionTests.test_ci_wrapper_default_jobs_uses_cpu_minus_one_fixture",
    "ValidationSelectionTests.test_ci_wrapper_delegates_broad_smoke_non_recursively",
    "ValidationSelectionTests.test_ci_wrapper_duration_reporting_does_not_use_bash_seconds",
    "ValidationSelectionTests.test_ci_wrapper_executes_selector_selected_path_and_root_checks",
    "ValidationSelectionTests.test_ci_wrapper_fail_fast_reports_queued_checks_not_started",
    "ValidationSelectionTests.test_ci_wrapper_fails_on_blocked_selector_without_partial_execution",
    "ValidationSelectionTests.test_ci_wrapper_forwards_mode_arguments_to_selector",
    "ValidationSelectionTests.test_ci_wrapper_jobs_one_uses_stable_summary_and_hides_success_output",
    "ValidationSelectionTests.test_ci_wrapper_keeps_large_output_isolated_per_check",
    "ValidationSelectionTests.test_ci_wrapper_non_allowlisted_checks_run_alone",
    "ValidationSelectionTests.test_ci_wrapper_parallel_default_waits_for_started_check_after_failure",
    "ValidationSelectionTests.test_ci_wrapper_parallel_safe_checks_run_concurrently_with_cap",
    "ValidationSelectionTests.test_ci_wrapper_preserves_selected_command_failure",
    "ValidationSelectionTests.test_ci_wrapper_rejects_fallback_and_malformed_selector_output",
    "ValidationSelectionTests.test_ci_wrapper_rejects_invalid_execution_flags_before_selector",
    "ValidationSelectionTests.test_ci_wrapper_rejects_selector_command_mismatch",
    "ValidationSelectionTests.test_ci_wrapper_reports_decode_failures_without_emitting_invalid_bytes",
    "ValidationSelectionTests.test_ci_wrapper_reports_unavailable_selected_command",
    "ValidationSelectionTests.test_ci_wrapper_run_to_completion_reports_failed_output_after_summary",
    "ValidationSelectionTests.test_ci_wrapper_timeout_and_signal_failures_have_distinct_statuses",
    "ValidationSelectionTests.test_ci_wrapper_verbose_prints_successful_output_in_stable_order",
    "ValidationSelectionTests.test_cli_accepts_changed_file_alias_for_plan_validation_commands",
    "ValidationSelectionTests.test_cli_outputs_json_for_classified_skill_path",
    "ValidationSelectionTests.test_compact_contract_surfaces_select_cross_runtime_and_metadata_proof",
    "ValidationSelectionTests.test_contributing_guidance_routes_without_manual_block",
    "ValidationSelectionTests.test_deleted_isolated_prose_keeps_proof_without_reading_deleted_file",
    "ValidationSelectionTests.test_documentation_prose_tier_a_routes_to_enforcement_without_displacing_existing_checks",
    "ValidationSelectionTests.test_documentation_prose_tier_b_routes_to_audit_without_repository_failure",
    "ValidationSelectionTests.test_documentation_prose_tier_c_paths_do_not_select_first_slice_prose_validation",
    "ValidationSelectionTests.test_documentation_prose_validator_surfaces_route_without_manual_blocks",
    "ValidationSelectionTests.test_er_m5_001_local_selection_ignores_private_recorder_state_only",
    "ValidationSelectionTests.test_er_m5_001_real_recording_paths_select_complete_set_validation",
    "ValidationSelectionTests.test_er_m5_001_unknown_value_contract_and_unregistered_paths_fail_closed",
    "ValidationSelectionTests.test_explicit_recording_adoption_surfaces_select_real_proof",
    "ValidationSelectionTests.test_explicit_recording_package_paths_retain_publication_proof",
    "ValidationSelectionTests.test_first_slice_representative_categories_route_or_block_safely",
    "ValidationSelectionTests.test_follow_up_register_path_selects_static_validation",
    "ValidationSelectionTests.test_generated_skill_only_uses_derivation_checks_without_lifecycle",
    "ValidationSelectionTests.test_governance_paths_select_deterministic_proof_instead_of_empty_ok",
    "ValidationSelectionTests.test_hosted_ci_installs_locked_public_package_dependencies_before_validation",
    "ValidationSelectionTests.test_hosted_ci_remains_thin_and_matrix_free",
    "ValidationSelectionTests.test_isolated_recording_evidence_selects_proof_without_formal_settlement",
    "ValidationSelectionTests.test_learn_artifact_paths_are_known_lightweight_paths",
    "ValidationSelectionTests.test_lifecycle_artifact_classes_retain_owned_lifecycle_paths",
    "ValidationSelectionTests.test_lifecycle_words_do_not_change_skill_path_classification",
    "ValidationSelectionTests.test_local_mode_discovers_tracked_and_untracked_git_paths",
    "ValidationSelectionTests.test_main_mode_uses_direct_lifecycle_scope",
    "ValidationSelectionTests.test_malformed_release_profile_paths_require_release_version",
    "ValidationSelectionTests.test_manifest_discriminator_unknown_value_types_fail_closed",
    "ValidationSelectionTests.test_markdown_readability_validator_scripts_select_focused_regression",
    "ValidationSelectionTests.test_missing_mode_specific_inputs_return_json_error",
    "ValidationSelectionTests.test_missing_unproven_or_present_isolated_prose_retains_audit",
    "ValidationSelectionTests.test_mixed_classified_and_unclassified_paths_block_partial_execution",
    "ValidationSelectionTests.test_mixed_skill_and_spec_scope_each_check_to_its_owner",
    "ValidationSelectionTests.test_model_example_selection_uses_owner_not_example_as_model",
    "ValidationSelectionTests.test_model_layout_change_selects_all_actual_readers",
    "ValidationSelectionTests.test_model_selection_deleted_flat_input_selects_current_owner",
    "ValidationSelectionTests.test_model_selection_deleted_layout_paths_and_examples_select_current_owner",
    "ValidationSelectionTests.test_model_selection_rejects_historical_flat_symlink",
    "ValidationSelectionTests.test_model_selection_retains_authoritative_tracking_preflight",
    "ValidationSelectionTests.test_model_selection_validates_present_historical_flat_input",
    "ValidationSelectionTests.test_multiple_release_paths_share_one_release_validation_check",
    "ValidationSelectionTests.test_normalize_path_rejects_outside_repository_paths",
    "ValidationSelectionTests.test_output_contract_red_tests_are_unmasked_and_separate",
    "ValidationSelectionTests.test_plan_index_does_not_reintroduce_proven_deleted_lifecycle_inputs",
    "ValidationSelectionTests.test_plan_index_surfaces_select_lifecycle_validation_with_both_surfaces",
    "ValidationSelectionTests.test_pr_always_retains_lifecycle_scope_for_docs_and_code",
    "ValidationSelectionTests.test_pr_contained_lifecycle_surfaces_exclude_published_skill_path",
    "ValidationSelectionTests.test_pr_handoff_surfaces_select_deterministic_checks",
    "ValidationSelectionTests.test_pr_lifecycle_catalog_preserves_revision_scope",
    "ValidationSelectionTests.test_pr_mode_blocks_reintroduced_retired_vision_as_unclassified",
    "ValidationSelectionTests.test_pr_mode_routes_adapter_distribution_test_script_to_adapter_checks",
    "ValidationSelectionTests.test_pr_mode_routes_adapter_fixture_to_adapter_checks",
    "ValidationSelectionTests.test_pr_mode_routes_readme_without_unclassified_block",
    "ValidationSelectionTests.test_pr_mode_routes_requirement_fidelity_spec_read_proof_paths",
    "ValidationSelectionTests.test_pr_mode_routes_root_vision_without_unclassified_block",
    "ValidationSelectionTests.test_pr_mode_runs_selected_checks_instead_of_full_product_graph",
    "ValidationSelectionTests.test_pr_wrapper_executes_exact_lifecycle_range_and_preserves_failure",
    "ValidationSelectionTests.test_pr_wrapper_rejects_selector_mode_substitution",
    "ValidationSelectionTests.test_preflight_blocks_empty_only_untracked_and_symlink_directories",
    "ValidationSelectionTests.test_preflight_blocks_tracked_file_replaced_by_untracked_directory",
    "ValidationSelectionTests.test_preflight_blocks_untracked_authoritative_artifact_with_action",
    "ValidationSelectionTests.test_preflight_passes_directory_when_its_authoritative_contents_are_tracked",
    "ValidationSelectionTests.test_preflight_passes_tracked_authoritative_artifact",
    "ValidationSelectionTests.test_project_map_paths_are_living_reference_not_lifecycle",
    "ValidationSelectionTests.test_proven_lifecycle_deletion_keeps_regression_without_reading_absent_file",
    "ValidationSelectionTests.test_readme_marker_validation_is_selected_for_marker_block_or_vision_scope",
    "ValidationSelectionTests.test_readme_path_selects_lightweight_readme_validation",
    "ValidationSelectionTests.test_readme_validator_accepts_absent_or_valid_standalone_marker_block",
    "ValidationSelectionTests.test_release_evidence_markdown_path_selects_lifecycle_checklist_validation",
    "ValidationSelectionTests.test_release_guidance_paths_do_not_require_release_version",
    "ValidationSelectionTests.test_release_mode_selects_release_validation_and_broad_smoke",
    "ValidationSelectionTests.test_release_path_without_version_directory_blocks",
    "ValidationSelectionTests.test_release_profile_path_uses_profile_filename_as_version",
    "ValidationSelectionTests.test_release_transaction_scripts_and_fixtures_select_focused_regression",
    "ValidationSelectionTests.test_research_artifact_path_selects_document_checks_without_unclassified_block",
    "ValidationSelectionTests.test_retired_author_deletion_keeps_package_proof_without_auditing_absent_source",
    "ValidationSelectionTests.test_retired_boundary_activation_publication_surface_is_not_cataloged",
    "ValidationSelectionTests.test_retired_docs_examples_path_is_known_during_deletion_compatibility",
    "ValidationSelectionTests.test_retired_lowercase_root_vision_path_blocks_as_unclassified",
    "ValidationSelectionTests.test_retired_lowercase_root_vision_presence_does_not_create_global_conflict",
    "ValidationSelectionTests.test_review_lifecycle_and_release_paths_select_scoped_validators",
    "ValidationSelectionTests.test_root_vision_path_selects_marker_validation_without_unclassified_block",
    "ValidationSelectionTests.test_selected_broad_smoke_is_one_invocation_and_diagnostic_failure_remains",
    "ValidationSelectionTests.test_selector_and_validation_script_paths_select_regressions",
    "ValidationSelectionTests.test_selector_marks_broad_smoke_as_boundary_phase",
    "ValidationSelectionTests.test_selector_preservation_surface_keeps_selected_check_identity",
    "ValidationSelectionTests.test_selector_registry_changes_select_selector_regression",
    "ValidationSelectionTests.test_selector_selected_readability_command_fails_changed_readme_hard_wrap",
    "ValidationSelectionTests.test_shared_preflight_context_requires_matching_repository_identity",
    "ValidationSelectionTests.test_skill_source_archive_selects_integrity_without_current_lifecycle",
    "ValidationSelectionTests.test_unclassified_path_blocks_without_fail_open",
    "ValidationSelectionTests.test_unproven_missing_or_present_lifecycle_input_is_not_suppressed",
    "ValidationSelectionTests.test_v3_registered_json_paths_select_contract_owned_validator",
    "ValidationSelectionTests.test_v3_registered_paths_select_owner_and_unknown_value_versions_fail_closed",
    "ValidationSelectionTests.test_valid_pr_and_main_modes_use_git_range",
    "ValidationSelectionTests.test_vision_rationale_path_selects_lifecycle_validation_without_unclassified_block",
    "ValidationSelectionTests.test_workflow_guidance_aligns_with_validation_layering_contract",
    "ValidationSelectionTests.test_workflow_guidance_selects_composed_guide_system_validator",
    "ValidationSelectionTests.test_workflow_refactor_surface_set_selects_expected_checks"
  ],
  "observations": [
    {
      "mode": "normal",
      "jobs": 1,
      "elapsed": 124.631,
      "count": 163,
      "failed": []
    },
    {
      "mode": "single",
      "jobs": 1,
      "elapsed": 404.413,
      "count": 163,
      "failed": []
    },
    {
      "mode": "reverse",
      "jobs": 2,
      "elapsed": 214.468,
      "count": 163,
      "failed": []
    }
  ]
}
```

## Named command results

| Command | Actual result |
| --- | --- |
| `python scripts/test-validation-execution.py` | 40 passed, final direct run 45.027 s. |
| `python scripts/test-select-validation.py` | 163 passed, final direct run 116.23 s. |
| `python scripts/test-artifact-lifecycle-validator.py` | 108 passed, direct run 72.862 s. |
| `python scripts/test-change-metadata-validator.py` | 7 passed, direct run 6.95 s. |
| `python scripts/test-validation-execution.py CompositionTests` | 7 passed after final reporting/constraint refinements. |
| `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_ci_script_runs_adapter_checks_and_filters_generated_paths` | 1 passed; actual composition consumer and distinct archive preparation retained. |
| `python scripts/test-retirement-ledger.py` | 17 passed; original inventory and archive records preserved. |
| `bash scripts/ci.sh --mode explicit --path scripts/validation_execution.py --path scripts/validation_selection.py --jobs 2` | Passed all 203 canonical case results: selector 163 and executor 40. No repeated executor group. |
| `python scripts/validate-change-metadata.py docs/changes/2026-09-13-independent-parallel-tests/change.json` | Passed. |
| `git diff --check` and `git diff --cached --check` | Passed. |

The late boundary-summary text is covered by refreshed composition proof and the complete final executor and selector direct commands. The explicit invocation's selected IDs have no boundary group; its recorded implementation basis remains applicable.

## Unaffected surfaces

The wrapper shell, selector entrypoint, product implementation, package generation, schemas, model contracts and lifecycle permissions need no changes for M3. They consume the same trusted selection/result contract. Main/broad leaf membership is authored in the catalog; concrete preparation and version differences are preserved. Current consumers expecting retired IDs were updated; historical reports and ledger bytes were not rewritten. M4–M7 populations and final integration remain for their own milestones and reviews.
