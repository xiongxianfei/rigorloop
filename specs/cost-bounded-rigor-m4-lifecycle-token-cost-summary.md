# Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary

## Status

approved

## Related proposal

- [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md)

## Goal and context

This spec defines the fourth cost-bounded-rigor implementation slice after PR #54 completed M1, PR #55 completed M2, and PR #56 completed M3.

M1 added scope-budget guidance and the full bounded-evidence rule in `docs/workflows.md`. M2 added selected skill reminders without changing validation behavior. M3 added validation-budget owner-surface guidance without changing selector behavior.

M4 defines conditional lifecycle token-cost summaries: lightweight diagnostic artifacts that record why a workflow or release change was worth measuring, which lifecycle stages were covered, which observable cost drivers appeared, and what follow-up is useful.

This slice is intentionally not a hard token gate, a dynamic benchmark expansion, release packaging work, adapter packaging work, or progressive-loading restructuring.

## Glossary

- lifecycle token-cost summary: a compact report for one change that records lifecycle-stage cost signals, observed cost drivers, the largest observed cost event, and result/rationale.
- trigger: a reason that makes a lifecycle token-cost summary required for a change.
- large workflow-governance change: a change that the accepted plan, test spec, review-resolution, or reviewer classifies as materially changing workflow policy, validation policy, lifecycle artifact rules, or stage behavior across multiple lifecycle surfaces.
- release change: a change that the accepted plan, release metadata, release validation mode, or reviewer classifies as release preparation, release evidence, release automation, or release policy work.
- dynamic benchmark warning: a warning result in accepted token-cost benchmark, analyzer, or release token-friendliness evidence.
- broad-search incident: an observed broad search, broad read, or large command output event that was relevant to the current change and not already justified as the smallest sufficient evidence.
- observed cost driver: an evidence-backed workflow-cost signal such as broad searches, large command outputs, full-skill reads, repeated file reads, generated-output reads, review rounds, or validation runs.
- largest observed event: the single largest available cost event by lines, estimated tokens, or another explicitly named basis.
- advisory numeric comparison: optional token totals, exact model usage, run-to-run variance, or before/after dynamic benchmark data used only when available or separately required.
- hard token gate: a blocking threshold based on token totals or token-cost regression. M4 does not introduce hard token gates.

## Examples first

### Example E1: ordinary small docs change does not create a summary

Given a change only corrects one small documentation typo
And no maintainer requests lifecycle token-cost evidence
And no broad-search incident, dynamic benchmark warning, release change, or large workflow-governance trigger applies
When the change is planned and verified
Then no lifecycle token-cost summary is required.

### Example E2: large workflow-governance change records a summary

Given a change updates workflow policy across multiple lifecycle surfaces
When the accepted plan or test spec classifies it as a large workflow-governance change
Then implementation records a lifecycle token-cost summary under `docs/reports/token-cost/lifecycle/`
And the summary records required field groups without adding a hard token gate.

### Example E3: broad-search incident triggers a summary

Given an implementation or review observes a broad search that produces large output before targeted evidence was tried
When the incident is relevant to the current change
Then a lifecycle token-cost summary records the broad search as an observed cost driver
And the largest event section cites the command, output size, and bounded follow-up.

### Example E4: release token-cost evidence is linked, not duplicated

Given a release change already has token-friendliness evidence under `docs/reports/token-cost/releases/`
When a lifecycle token-cost summary is required
Then the lifecycle summary links to the release report as source evidence
And does not duplicate the full release benchmark metadata.

### Example E5: dynamic benchmark warning does not require a new benchmark

Given an existing dynamic benchmark report contains warning status
When that warning triggers a lifecycle token-cost summary
Then the summary records the warning and its source artifact
And M4 does not require a fresh before/after dynamic benchmark unless the plan, test spec, or release process separately requires it.

### Example E6: no exact token telemetry is available

Given a triggered change has review rounds, validation runs, and command-output observations
But no exact model-usage or dynamic benchmark telemetry
When the lifecycle token-cost summary is written
Then required fields are still completed from observable evidence
And unavailable advisory fields are omitted or marked not measured with rationale.

### Example E7: hard token gate proposal is rejected

Given a lifecycle token-cost summary recommends blocking future changes on token totals
When M4 is reviewed
Then review requests removal or deferral of the hard-gate recommendation
And routes threshold policy to a later proposal after multiple comparable summaries exist.

## Requirements

R1. M4 MUST define lifecycle token-cost summaries as conditional diagnostic evidence, not as a default artifact for every change.

R2. M4 MUST require a lifecycle token-cost summary only when at least one trigger applies:

- large workflow-governance change;
- release change;
- dynamic benchmark warning;
- broad-search incident;
- explicit maintainer request.

R3. M4 MUST allow ordinary feature, documentation, proposal, and small skill edits to omit lifecycle token-cost summaries when no trigger applies.

R4. M4 MUST keep trigger applicability as workflow artifact or reviewer judgment in the first implementation slice. Validators MUST NOT fail a change solely because they infer that a trigger should have applied.

R5. A lifecycle token-cost summary MUST use the path `docs/reports/token-cost/lifecycle/<change-id>.md`, where `<change-id>` matches the active change root or accepted plan slug when a change root does not exist yet.

R6. A lifecycle token-cost summary MUST contain these required field groups: identity, trigger, scope, source artifacts, observed cost drivers, largest observed event, and result/rationale.

R7. The identity field group MUST identify the change ID, title, report date, and source artifacts used by the summary.

R8. The trigger field group MUST identify the trigger reason, the requester or owning artifact, and the date the trigger was identified.

R9. The scope field group MUST record stages covered, stages excluded, and the basis for the summary.

R10. The source-artifacts field group MUST link to the proposal, spec, plan, test spec, change metadata, review records, release report, benchmark report, or other durable artifacts used as evidence when those artifacts exist.

R11. The observed-cost-drivers field group MUST record whether broad searches, large command outputs, full-skill reads, repeated file reads, generated-output reads, review rounds, and validation runs were observed.

R12. The largest-observed-event field group MUST record event type, source, estimated tokens or lines when available, and evidence or rationale.

R13. The result/rationale field group MUST record informational status, largest driver, recommended follow-up, and any no-follow-up rationale.

R14. Required field groups MAY record `not observed`, `not measured`, or `not applicable` with rationale when exact data is unavailable.

R15. Detailed numeric comparisons, exact model usage, cached input tokens, reasoning output tokens, run-to-run variance, threshold regression results, hard-gate recommendations, and before/after dynamic benchmark comparisons MUST remain advisory unless a benchmark actually ran or a later accepted plan or test spec requires them.

R16. M4 MUST NOT introduce hard token thresholds, hard release gates, or CI blockers based on lifecycle token-cost totals.

R17. M4 MUST NOT require before/after dynamic benchmark comparison for changes that only add or revise lifecycle summary guidance, templates, or validation shape.

R18. Release token-friendliness reports under `docs/reports/token-cost/releases/` MUST remain separate release evidence. Lifecycle summaries MAY link to them but MUST NOT replace them.

R19. M4 MUST preserve the single-authored-skill-source boundary. Lifecycle summaries MUST NOT treat generated adapter skill bodies as authored skill truth.

R20. M4 MUST preserve the PR #53 follow-up routing model. Recommended follow-up from a lifecycle token-cost summary MUST route to the active plan, review-resolution, learn, proposal, or follow-up ownership surface according to the existing routing rule.

R21. If M4 adds a template or validator support, it MUST check required field or section presence and stable path placement only. It MUST NOT infer semantic trigger applicability or enforce token thresholds.

R22. If M4 changes validation selector behavior for lifecycle token-cost summary paths, the test spec MUST require selector regression coverage for that path classification and selected checks.

R23. If M4 implementation does not change selector behavior, it MUST record no-change rationale for selector behavior.

R24. Lifecycle summaries MUST use bounded evidence. They MUST summarize large command output, logs, and benchmark output instead of copying unnecessary raw output.

R25. Lifecycle summaries MUST NOT include secrets, credentials, private local paths beyond repo-relative paths, or raw JSONL content unless an existing token-cost report policy explicitly allows the tracked evidence.

R26. After 3-5 completed lifecycle token-cost summaries exist, expanding trigger rules or converting token totals into blocking thresholds MUST require a later proposal or spec.

R27. M4 MUST NOT implement progressive-loading follow-through for `workflow`, `implement`, or `code-review`.

R28. M4 MUST NOT change release packaging, adapter packaging, generated adapter output tracking, benchmark suite scope, or release token-cost report schema unless a later accepted artifact explicitly broadens the scope.

R29. Final verify for an M4 implementation MUST check that any required lifecycle token-cost summary exists, contains the required field groups, and matches the accepted plan, test spec, review-resolution, release metadata, and maintainer-request triggers.

## Inputs and outputs

Inputs:

- accepted cost-bounded-rigor proposal;
- completed M1, M2, and M3 specs and plans;
- current `docs/reports/token-cost/` report conventions;
- current token-cost analyzer, benchmark, and report-validation behavior;
- current workflow guidance for bounded evidence, validation budgets, and follow-up routing;
- active plan, test spec, review-resolution, release metadata, or maintainer request that identifies a trigger.

Outputs:

- focused M4 spec;
- later M4 plan and test spec;
- lifecycle token-cost summary path and required field contract;
- optional template or validation support, if scoped by the plan;
- no-change rationale for selector, release, benchmark, adapter, and progressive-loading surfaces that remain unchanged;
- lifecycle summary artifacts only when a trigger applies.

## State and invariants

1. Lifecycle token-cost summaries remain conditional, diagnostic, and warning-only.
2. Required lifecycle summaries live under `docs/reports/token-cost/lifecycle/`.
3. Existing release token-friendliness reports remain release evidence under `docs/reports/token-cost/releases/`.
4. Existing dynamic benchmark reports remain benchmark evidence under `docs/reports/token-cost/runs/` and release report metadata.
5. The active plan, test spec, review-resolution, release metadata, and maintainer request surfaces may require a lifecycle summary.
6. Validators may check report shape when a report exists, but first-slice validators do not infer semantic trigger applicability.
7. Follow-up recommendations route through existing follow-up ownership rules.

## Error and boundary behavior

1. If a trigger applies and no lifecycle token-cost summary exists, implementation or verify must stop and record the missing artifact before claiming readiness.
2. If trigger applicability is ambiguous, the active plan or review must decide before implementation relies on omission.
3. If a lifecycle summary omits a required field group, review or validation must request completion.
4. If exact token data is unavailable, the summary must use observable evidence and record `not measured` rationale instead of fabricating numbers.
5. If a lifecycle summary tries to create a hard token gate, review must reject or defer that policy.
6. If a report would need raw sensitive data, the summary must link to sanitized evidence or record a privacy-preserving rationale.
7. If M4 work discovers that release report schema, benchmark suite scope, release packaging, adapter packaging, or progressive-loading behavior must change, implementation must stop and route that work to a later accepted artifact.

## Compatibility and migration

- Existing token-cost baseline reports remain valid historical evidence.
- Existing release token-friendliness reports and YAML metadata remain valid and are not migrated into lifecycle summaries.
- Existing M1, M2, and M3 cost-bounded-rigor changes do not require retroactive lifecycle token-cost summaries.
- Existing selector behavior remains valid unless the M4 plan identifies a focused lifecycle-summary path gap.
- Rollback for guidance-only M4 implementation is to remove the new lifecycle-summary guidance or template while preserving existing token-cost reports and validation behavior.

## Observability

M4 behavior is observable through:

- lifecycle token-cost summary files under `docs/reports/token-cost/lifecycle/` when triggered;
- source-artifact links inside those summaries;
- active plan and test-spec decisions about whether a summary is required;
- review findings for missing, oversized, unsafe, or hard-gate summary behavior;
- selected validation output if the implementation changes selector or token-cost report validation behavior;
- explain-change and verify evidence for why a dynamic benchmark comparison was or was not required.

## Security and privacy

Lifecycle summaries must minimize copied raw output and prefer repo-relative paths, counts, stable IDs, and links to durable sanitized evidence. They must not expose secrets, credentials, personal data, private machine paths, or raw JSONL content outside existing token-cost evidence policy.

## Accessibility and UX

No UI is involved.

## Performance expectations

Lifecycle summaries should reduce future workflow cost by making large cost drivers visible. They must not add routine reporting overhead to ordinary small changes. No runtime, latency, or token-count threshold is introduced by M4.

## Edge cases

1. A small docs-only change touches no workflow policy and has no broad-search incident. No lifecycle summary is required.
2. A change touches `docs/workflows.md`, a lifecycle skill, and validation selector behavior. The active plan should decide whether this is a large workflow-governance change and whether M4 requires a lifecycle summary.
3. A maintainer explicitly asks for a lifecycle token-cost summary on a small skill edit. The summary is required because explicit maintainer request is a trigger.
4. A release change already has `docs/reports/token-cost/releases/<version>.yaml`. A lifecycle summary may link to it and summarize lifecycle drivers, but must not duplicate the release report body.
5. A dynamic benchmark warning exists in release evidence. The lifecycle summary records the warning source; it does not automatically rerun the benchmark.
6. A broad search returns thousands of lines during implementation. The lifecycle summary records the command, largest observed event, and recommended follow-up without copying the full output.
7. A full-skill read is justified because the whole skill is the target. The summary may record it as observed and justified rather than treating it as a failure.
8. A report has no exact token telemetry. The report remains valid if it records observable drivers and `not measured` rationale.
9. A proposed validator fails ordinary docs changes for lacking a lifecycle summary. Review must reject it because first-slice validators must not infer trigger applicability.
10. A report recommends hard CI token thresholds after one example. Review must defer threshold policy until multiple comparable summaries exist and a later proposal or spec accepts it.

## Non-goals

- Do not add routine lifecycle token-cost summaries for every change.
- Do not add hard token gates.
- Do not require before/after dynamic benchmark comparison by default.
- Do not expand the dynamic benchmark suite.
- Do not change release packaging or adapter packaging.
- Do not replace release token-friendliness reports.
- Do not reintroduce tracked generated public adapter skill bodies.
- Do not implement progressive-loading follow-through.
- Do not rewrite high-cost public skills.
- Do not make validators infer semantic trigger applicability in the first implementation slice.

## Acceptance criteria

- Lifecycle token-cost summaries are conditional and diagnostic.
- Required triggers are large workflow-governance change, release change, dynamic benchmark warning, broad-search incident, and explicit maintainer request.
- Ordinary small feature, docs, proposal, and skill edits may omit summaries when no trigger applies.
- The report path is `docs/reports/token-cost/lifecycle/<change-id>.md`.
- Required field groups are identity, trigger, scope, source artifacts, observed cost drivers, largest observed event, and result/rationale.
- Advisory numeric comparison fields remain optional unless benchmark evidence exists or a later accepted plan or test spec requires them.
- No hard token thresholds, hard gates, release packaging changes, adapter packaging changes, benchmark-suite expansion, or progressive-loading restructuring are introduced.
- Release token-friendliness reports remain separate and may be linked rather than duplicated.
- Follow-up recommendations route through the existing follow-up ownership model.
- M4 records no-change rationale for selector, release, benchmark, adapter, and progressive-loading surfaces that remain unchanged.

## Open questions

None.

## Next artifacts

```text
spec-review
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

Architecture is not expected for this slice because the change defines reporting guidance and shape, not runtime architecture, data flow, persistence, APIs, deployment, or security boundaries. `spec-review` may still require architecture if it finds a hard-to-reverse validation or reporting design risk.

## Follow-on artifacts

- [Spec Review R1](../docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/spec-review-r1.md)
- [Execution Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md)
- [Plan Review R1](../docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/plan-review-r1.md)
- [Test Spec](cost-bounded-rigor-m4-lifecycle-token-cost-summary.test.md)

## Readiness

Approved after clean spec-review. The focused M4 execution plan has clean plan-review approval, and the M4 test spec is active and maintainer-approved for implementation.
