# Behavior Preservation Evidence

Change ID: 2026-06-23-workflow-state-projection-and-pre-transition-synchronization-gate
Status: implementation evidence for M5
Date: 2026-06-23

## Scope

This evidence records the M5 proof that workflow-state synchronization enforcement preserves the accepted Single Source of Workflow State ownership model while making active projections and derived evidence mechanically comparable.

The proof is bounded to the approved first implementation slice:

- active plan owner parsing;
- active and blocked `docs/plan.md` projection validation;
- current milestone-state projection validation;
- pointer-only `Readiness`;
- review evidence and change metadata consistency;
- parser-scoped stale-token behavior;
- binding workflow guidance and active/blocked audit behavior.

It does not claim branch readiness, PR readiness, hosted CI success, or final verification.

## Preservation Matrix

| Surface | Baseline | Revised proof | Result |
| --- | --- | --- | --- |
| Workflow stage order | Standard chain routes through proposal, spec, architecture when needed, plan, test-spec, implementation, code-review, review-resolution when triggered, explain-change, verify, and PR. | M1-M5 used the same chain; clean non-final review routed to the next implementation milestone, and M5 handoff routes to code-review rather than verify or PR. | preserved |
| Current state owner | Active plan `Current Handoff Summary` owns current milestone, milestone state, review status, remaining implementation milestones, next stage, final readiness, and final-readiness reason. | `scripts/lifecycle_state_sync.py` parses exact owner fields and compares only bounded projections and derived evidence against that owner. | preserved |
| Plan index | `docs/plan.md` is a bounded lifecycle index, not the body of a plan. | Active and blocked rows use the table projection; `State`, `Next stage`, and `Change ID` are checked against named owner fields. | strengthened |
| Review log | `review-log.md` records review events and open finding state as ledger evidence. | Review-log entries remain append-oriented; state-sync consumes review summaries through review-artifact parsing instead of making the log the live next-stage owner. | preserved |
| Review resolution | `review-resolution.md` owns finding dispositions and validation evidence. | `finding_closure_state()` requires positive evidence for closeout and is reused by review validation, change metadata counts, and lifecycle owner-state blocking. | preserved |
| Change metadata | `change.yaml` stores compact evidence, validation events, and artifact pointers. | `change.yaml.change_id` and review counts are derived consistency checks; metadata does not own live planned-initiative next stage. | strengthened |
| Verify | Verify owns branch-readiness decisions. | State-sync validation never infers branch readiness; M5 evidence stops at code-review handoff. | preserved |
| PR | PR owns PR-readiness and PR-body handoff decisions. | No plan state or metadata field claims PR readiness; PR handoff remains downstream of verify. | preserved |
| Historical plans and ledgers | Historical plans, review records, progress, and review-resolution history remain durable evidence. | Parser-scoped enforcement skips legacy plans without the structured marker and permits historical stage tokens in ledger/review evidence. | preserved |

## Transition Exercise Evidence

| Transition or gate | Direct proof | Preservation result |
| --- | --- | --- |
| Implementation to code review | `test_workflow_state_plan_index_projection_sources`, `test_workflow_state_owner_review_status_cases`, `test_workflow_state_current_milestone_projection_must_match_owner`, and the active plan M1-M5 handoffs prove synchronized `review-requested` owner and projection state. | synchronized transition passes |
| Incomplete projection before review | `test_workflow_state_index_only_catches_next_stage_drift`, `test_workflow_state_plan_index_projection_sources`, and the WSS-CR4 all-active audit regression prove stale or mispaired projection surfaces block before review handoff. | incomplete transition fails |
| Code review requests changes | `test_workflow_state_open_review_finding_blocks_review_requested_owner_state` proves open material findings block downstream `review-requested` owner state. | resolution route enforced |
| Resolution complete and re-review requested | `test_workflow_state_invalid_disposition_blocks_review_requested_owner_state`, `test_workflow_state_closed_status_missing_validation_blocks_review_requested_owner_state`, `test_full_closeout_summary_passes`, and `test_predicate_parity_with_closeout_mode` prove re-review is permitted only after positive finding-closeout evidence. | evidence-owned closeout preserved |
| Clean non-final milestone review | Code-review receipts M1 R2, M2 R1, M3 R3, and M4 R2 close their respective milestones and route to the next implementation milestone rather than final closeout. | non-final handoff preserved |
| Final closeout routing | `test_workflow_state_final_closeout_reason_cases` rejects inconsistent final readiness reason codes; the active plan keeps final closeout `not ready` while M5 is open and explain-change, verify, and PR remain pending. | final readiness not inferred early |
| Historical token retention | `test_workflow_state_readiness_live_surface_rejects_historical_token_drift`, `test_workflow_state_readiness_rejects_live_stage_restatements`, and `test_workflow_state_index_only_legacy_plan_is_skipped` distinguish bounded live surfaces from historical/legacy evidence. | history preserved |
| Active/blocked enforcement scope | `test_multi_active_plans_correct_change_ids_pass`, `test_multi_active_plan_misassigned_change_id_blocks`, `test_multi_active_plan_missing_change_id_blocks_only_that_plan`, `test_multi_active_plan_unmatched_change_yaml_blocks`, and `test_audit_pairs_by_key_not_order` cover multi-active association and active/blocked audit scope. | R81/T19 enforced |

## Derived-Fact Ownership Checks

| Derived fact | Shared computation or owner | M5 conclusion |
| --- | --- | --- |
| Workflow-state projection match | `lifecycle_state_sync.py` through `validate-artifact-lifecycle.py` | one parser/comparison path |
| Finding open or closed | `finding_closure_state()` in `review_artifact_validation.py` | one positive-evidence predicate |
| Change metadata review counts | `summarize_review_evidence()` | derived from review artifacts, not authored independently |
| Branch readiness | verify stage | not inferred by state-sync |
| PR readiness | PR stage | not inferred by state-sync |

## Absence-Equals-Pass Audit

The M3 and M4 review findings identified a repeated anti-pattern: treating missing evidence or narrow scope as a passing result. M5 confirms the implemented slice now rejects that pattern at the known risk points:

- owner fields fail closed when missing, duplicated, or malformed;
- plan-index rows fail on missing targets, duplicate projections, drifted `Next stage`, drifted `Change ID`, or wrong section;
- review findings stay open when disposition, closeout status, validation evidence, or later-review state is missing or ambiguous;
- active/blocked audits pair plan bodies and change metadata by key, not iteration order;
- unmatched in-scope change metadata blocks unless it points to a legacy plan explicitly outside the structured-marker enforcement boundary.

## Success Measurement Baseline

The post-rollout success metric is zero workflow-state drift findings across the next 10 formal reviews or 30 days, whichever yields more evidence. Any drift finding in that window should be treated as a coverage or binding defect unless it is explicitly outside the approved enforcement scope.

Current starting state for that measurement:

- Open workflow-state drift findings: none.
- Last closed workflow-state drift finding: WSS-CR4, confirmed by code-review-m4-r2.
- Required downstream stages not yet claimed: code-review M5, explain-change, verify, and PR.

## Validation Evidence

M5 validation is recorded in the active plan and `change.yaml`. The required validation set includes:

- `python scripts/test-artifact-lifecycle-validator.py`;
- `python scripts/test-review-artifact-validator.py`;
- `python scripts/test-change-metadata-validator.py`;
- explicit-path artifact lifecycle validation over plan, spec, test spec, architecture, change metadata, review log, and review resolution;
- review artifact validation;
- change metadata validation;
- diff cleanliness over touched workflow-state surfaces.
