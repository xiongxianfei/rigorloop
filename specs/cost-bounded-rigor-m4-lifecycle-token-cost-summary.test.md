# Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary Test Spec

## Status

active

## Related spec and plan

- Spec: [Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary](cost-bounded-rigor-m4-lifecycle-token-cost-summary.md), approved.
- Plan: [Cost-Bounded Rigor M4 Lifecycle Token-Cost Summary Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md), active after clean plan-review.
- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Spec review: [spec-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/spec-review-r1.md), approved with no material findings.
- Plan review: [plan-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/reviews/plan-review-r1.md), approved with no material findings.
- Change metadata: [change.yaml](../docs/changes/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary/change.yaml).
- Architecture: not required. The approved spec, spec-review, and plan-review scope this slice to reporting guidance, template shape, focused static proof, and one diagnostic lifecycle summary.
- Project map: [docs/project-map.md](../docs/project-map.md) exists as a living orientation reference. This test spec relies on the approved spec, reviewed plan, and touched files for implementation proof.

## Approval

Maintainer-approved on 2026-05-14 by direct user request. Status remains `active` because this test spec is the relied-on proof-planning surface for M4 implementation.

## Testing strategy

M4 is verified through contract, static, selected-integration, lifecycle, security/privacy, and manual review checks. It does not require runtime end-to-end tests, release validation, adapter packaging validation, dynamic benchmark comparison, hard token gates, progressive-loading restructuring, release token-cost report schema validation, or semantic trigger inference by validators.

- Use proof-first static checks before adding the lifecycle summary template or M4 summary when feasible.
- Use static checks in `scripts/test-token-cost-report-validation.py` for stable section or field-group presence, stable path placement, and forbidden hard-gate behavior.
- Use manual contract review for semantic trigger applicability, concise workflow wording, release-report separation, no-change rationale, bounded evidence quality, and follow-up routing.
- Use selector regression proof only if implementation changes selector behavior. The current reviewed plan expects selector behavior to remain unchanged.
- Use selected explicit validation for changed paths. If implementation updates `change.yaml`, the active plan, or other lifecycle artifacts, include those paths so change-metadata and lifecycle checks remain selected.
- Run broad smoke only if an authoritative trigger appears in selector mode, explicit flags, active plan state, this test spec, review-resolution, release metadata, or explicit maintainer request.

## Requirement coverage map

| Requirement IDs | Covered by | Notes |
|---|---|---|
| `R1` | `T1`, `T2`, `T10` | Summaries remain conditional diagnostic evidence. |
| `R2` | `T1`, `T2`, `T9` | Only the five approved triggers require summaries. |
| `R3` | `T1`, `T9`, `T10` | Ordinary small changes may omit summaries when no trigger applies. |
| `R4` | `T1`, `T7`, `T10` | Trigger applicability remains artifact or reviewer judgment; validators do not infer it. |
| `R5` | `T3`, `T7`, `T10` | Summary path is `docs/reports/token-cost/lifecycle/<change-id>.md`. |
| `R6` | `T3`, `T8`, `T10` | Required field groups are present. |
| `R7` | `T3`, `T8` | Identity field group is present and complete. |
| `R8` | `T3`, `T8` | Trigger field group is present and complete. |
| `R9` | `T3`, `T8` | Scope field group is present and complete. |
| `R10` | `T3`, `T8` | Source-artifacts field group links durable evidence when available. |
| `R11` | `T3`, `T4`, `T8` | Observed-cost-drivers field group records the required driver categories. |
| `R12` | `T3`, `T4`, `T8` | Largest-observed-event field group records type, source, estimate, and evidence or rationale. |
| `R13` | `T3`, `T8` | Result/rationale field group records informational status, largest driver, follow-up, or no-follow-up rationale. |
| `R14` | `T3`, `T4` | Unavailable exact data uses `not observed`, `not measured`, or `not applicable` with rationale. |
| `R15` | `T5`, `T9` | Numeric comparisons and dynamic benchmark comparisons remain advisory unless separately required. |
| `R16` | `T5`, `T8`, `T10` | No hard token thresholds, hard release gates, or CI blockers are introduced. |
| `R17` | `T5`, `T9` | Guidance/template/validation-shape changes do not require before/after dynamic benchmarks. |
| `R18` | `T6`, `T9` | Release Token-Friendliness reports remain separate evidence and may be linked. |
| `R19` | `T6`, `T10` | Generated adapter skill bodies are not treated as authored skill truth. |
| `R20` | `T6`, `T9` | Follow-up recommendations route through the existing follow-up ownership model. |
| `R21` | `T5`, `T7`, `T8` | Template or validator support checks presence and path only; no trigger inference or thresholds. |
| `R22` | `T7`, `T10` | Selector behavior changes require selector regression coverage. |
| `R23` | `T7`, `T9` | Unchanged selector behavior requires no-change rationale. |
| `R24` | `T4`, `T8`, `T9` | Summaries use bounded evidence and summarize large output. |
| `R25` | `T4`, `T8`, `T9` | Summaries avoid secrets, credentials, private paths, and raw JSONL outside existing policy. |
| `R26` | `T5`, `T9` | Trigger expansion or blocking thresholds require a later proposal or spec after 3-5 summaries. |
| `R27` | `T6`, `T10` | Progressive-loading follow-through is out of scope. |
| `R28` | `T6`, `T10` | Release packaging, adapter packaging, generated-output tracking, benchmark suite scope, and release report schema remain unchanged. |
| `R29` | `T9`, `T10` | Final verify checks required summary existence, field groups, and trigger match. |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` ordinary small docs change does not create a summary | `T1`, `T10` |
| `E2` large workflow-governance change records a summary | `T1`, `T3`, `T9` |
| `E3` broad-search incident triggers a summary | `T1`, `T4`, `T9` |
| `E4` release token-cost evidence is linked, not duplicated | `T6`, `T9` |
| `E5` dynamic benchmark warning does not require a new benchmark | `T5`, `T9` |
| `E6` no exact token telemetry is available | `T3`, `T4`, `T9` |
| `E7` hard token gate proposal is rejected | `T5`, `T8`, `T9` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` small docs-only change has no trigger | `T1`, `T10` |
| `EC2` change touches workflow policy, lifecycle skill, and selector behavior | `T1`, `T7`, `T9` |
| `EC3` explicit maintainer request requires a summary | `T1`, `T9` |
| `EC4` release change already has release token-cost report | `T6`, `T9` |
| `EC5` dynamic benchmark warning exists in release evidence | `T5`, `T6`, `T9` |
| `EC6` broad search returns thousands of lines | `T4`, `T9` |
| `EC7` full-skill read is justified because whole skill is target | `T4`, `T9` |
| `EC8` report has no exact token telemetry | `T3`, `T4`, `T9` |
| `EC9` validator fails ordinary docs changes for lacking a summary | `T1`, `T5`, `T7`, `T10` |
| `EC10` report recommends hard CI token thresholds after one example | `T5`, `T8`, `T9` |

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
|---|---|
| Lifecycle token-cost summaries are conditional and diagnostic | `T1`, `T2` |
| Required triggers are the five approved trigger types | `T1`, `T2` |
| Ordinary small feature, docs, proposal, and skill edits may omit summaries when no trigger applies | `T1`, `T10` |
| The report path is `docs/reports/token-cost/lifecycle/<change-id>.md` | `T3`, `T7` |
| Required field groups are identity, trigger, scope, source artifacts, observed cost drivers, largest observed event, and result/rationale | `T3`, `T8` |
| Advisory numeric comparison fields remain optional unless separately required | `T5`, `T9` |
| No hard token thresholds, hard gates, release packaging changes, adapter packaging changes, benchmark-suite expansion, or progressive-loading restructuring are introduced | `T5`, `T6`, `T10` |
| Release token-friendliness reports remain separate and may be linked rather than duplicated | `T6`, `T9` |
| Follow-up recommendations route through the existing follow-up ownership model | `T6`, `T9` |
| M4 records no-change rationale for selector, release, benchmark, adapter, and progressive-loading surfaces that remain unchanged | `T6`, `T7`, `T9`, `T10` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Lifecycle summary guidance, template, static proof, and first summary` | `T1`-`T10` |

## Test cases

### T1. Trigger rules stay conditional and artifact-owned

- Covers: `R1`-`R4`, `R26`, `E1`, `E2`, `E3`, `EC1`-`EC3`, `EC9`
- Level: contract, static, manual
- Fixture/setup:
  - approved M4 spec
  - active M4 plan
  - `docs/workflows.md`
  - final implementation diff
  - M4 lifecycle summary, if trigger applies
- Steps:
  - Confirm `docs/workflows.md`, the template, and the active plan describe lifecycle summaries as conditional diagnostic evidence.
  - Confirm the only required triggers named by implementation are large workflow-governance change, release change, dynamic benchmark warning, broad-search incident, and explicit maintainer request.
  - Confirm ordinary small feature, docs, proposal, and skill edits are allowed to omit summaries when no trigger applies.
  - Confirm trigger applicability is decided by the active plan, test spec, review-resolution, release metadata, explicit maintainer request, or reviewer judgment.
  - Confirm validators do not fail ordinary changes solely because they infer that a lifecycle-summary trigger should have applied.
- Expected result: M4 introduces conditional lifecycle summaries without routine reporting or semantic trigger inference.
- Failure proves: M4 turned diagnostic summaries into routine artifacts or validator-inferred policy.
- Automation location: manual contract review, `docs/workflows.md` static cues, selected CI output.

### T2. Workflow guidance names triggers, path, and warning-only boundary

- Covers: `R1`, `R2`
- Level: static, manual
- Fixture/setup:
  - `docs/workflows.md`
  - optional static proof in `scripts/test-token-cost-report-validation.py`
- Steps:
  - Confirm workflow guidance names the conditional trigger set.
  - Confirm workflow guidance names `docs/reports/token-cost/lifecycle/<change-id>.md` as the lifecycle-summary path.
  - Confirm workflow guidance says lifecycle summaries are diagnostic or warning-only and not a hard token gate.
  - If static proof is added, assert stable cues rather than a single exact paragraph.
- Expected result: contributor-facing guidance is concise and complete enough to route triggered summaries.
- Failure proves: contributors cannot tell when or where to record M4 lifecycle summaries, or guidance implies a hard gate.
- Automation location: `scripts/test-token-cost-report-validation.py` stable wording/section checks plus manual wording review.

### T3. Template and M4 summary contain required field groups

- Covers: `R5`-`R14`, `E2`, `E6`, `EC8`
- Level: unit, static, manual
- Fixture/setup:
  - `templates/lifecycle-token-cost-summary.md`
  - `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md`
  - `scripts/test-token-cost-report-validation.py`
- Steps:
  - Add a proof-first static test for required lifecycle-summary field groups before adding the template when feasible.
  - Confirm the template and first M4 summary contain identity, trigger, scope, source artifacts, observed cost drivers, largest observed event, and result/rationale sections or field groups.
  - Confirm identity includes change ID, title, report date, and source artifacts.
  - Confirm trigger includes trigger reason, requester or owning artifact, and date identified.
  - Confirm scope includes stages covered, stages excluded, and summary basis.
  - Confirm source artifacts link durable evidence when available.
  - Confirm observed cost drivers include broad searches, large command outputs, full-skill reads, repeated file reads, generated-output reads, review rounds, and validation runs.
  - Confirm largest observed event includes type, source, estimate when available, and evidence or rationale.
  - Confirm result/rationale includes informational status, largest driver, recommended follow-up, and no-follow-up rationale when applicable.
  - Confirm unavailable exact data may use `not observed`, `not measured`, or `not applicable` with rationale.
- Expected result: template and first summary prove the required shape without requiring unavailable exact telemetry.
- Failure proves: M4 added a report surface that cannot reliably satisfy required summary fields.
- Automation location: `python scripts/test-token-cost-report-validation.py TokenCostReportValidatorTests.test_lifecycle_summary_template_has_required_field_groups_and_warning_only_boundary`, full `python scripts/test-token-cost-report-validation.py`, manual summary review.

### T4. Lifecycle summaries use bounded and privacy-safe evidence

- Covers: `R11`, `R12`, `R14`, `R24`, `R25`, `E3`, `E6`, `EC6`-`EC8`
- Level: contract, security/privacy, manual
- Fixture/setup:
  - first M4 lifecycle summary
  - validation command outputs and review records used as evidence
  - final implementation diff
- Steps:
  - Confirm large command output, benchmark output, and logs are summarized instead of copied wholesale.
  - Confirm evidence uses repo-relative paths, stable IDs, counts, links, or concise rationale.
  - Confirm no secrets, credentials, private local paths, or raw JSONL content are copied into the lifecycle summary outside existing token-cost report policy.
  - Confirm broad searches, large command outputs, full-skill reads, repeated file reads, generated-output reads, review rounds, and validation runs are recorded as observed, not observed, not measured, or not applicable with rationale.
  - Confirm justified full-file or whole-skill reads can be recorded as justified observations rather than failures.
- Expected result: the first M4 summary captures useful cost drivers without becoming a raw log dump or privacy risk.
- Failure proves: lifecycle reporting added token waste or unsafe evidence handling.
- Automation location: manual security/privacy review, code-review checklist, verify checklist.

### T5. Advisory numeric data and hard-gate boundaries are preserved

- Covers: `R15`-`R17`, `R21`, `R26`, `E5`, `E7`, `EC5`, `EC9`, `EC10`
- Level: static, contract, manual
- Fixture/setup:
  - `docs/workflows.md`
  - lifecycle summary template
  - first M4 lifecycle summary
  - `scripts/test-token-cost-report-validation.py`
  - final implementation diff
- Steps:
  - Confirm detailed numeric comparisons, exact model usage, cached input tokens, reasoning output tokens, run-to-run variance, threshold regression results, hard-gate recommendations, and before/after dynamic benchmark comparisons are advisory unless a benchmark actually ran or a later accepted artifact requires them.
  - Confirm M4 does not introduce hard token thresholds, hard release gates, or CI blockers based on lifecycle token totals.
  - Confirm guidance/template/validation-shape changes do not require before/after dynamic benchmark comparison.
  - Confirm static proof checks required field or section presence and forbidden hard-gate behavior only.
  - Confirm trigger expansion or blocking thresholds are routed to a later proposal or spec after 3-5 completed summaries.
- Expected result: M4 creates warning-only measurement evidence without hard gates or default dynamic benchmarks.
- Failure proves: M4 changed from diagnostic reporting into release or CI policy.
- Automation location: `scripts/test-token-cost-report-validation.py` forbidden-hard-gate/static-boundary checks plus manual diff review.

### T6. Release, adapter, generated-output, follow-up, and progressive-loading boundaries remain intact

- Covers: `R18`-`R20`, `R27`, `R28`, `E4`, `E7`, `EC4`
- Level: contract, manual
- Fixture/setup:
  - final implementation diff
  - release and adapter support surfaces if touched
  - first M4 lifecycle summary
  - active plan/change metadata/explain-change evidence
- Steps:
  - Confirm release Token-Friendliness reports under `docs/reports/token-cost/releases/` remain separate and are linked rather than replaced or duplicated.
  - Confirm release token-cost report schema, release packaging, adapter packaging, generated adapter output tracking, and benchmark suite scope are unchanged unless a later accepted artifact explicitly broadens scope.
  - Confirm generated adapter skill bodies are not treated as authored skill truth and are not added back to tracked source.
  - Confirm no progressive-loading work for `workflow`, `implement`, or `code-review` is included.
  - Confirm recommended follow-up routes to the active plan, review-resolution, learn, proposal, or follow-up ownership surface according to existing rules.
- Expected result: M4 stays a lifecycle-summary slice and does not reopen completed cleanup, release, adapter, benchmark, or progressive-loading tracks.
- Failure proves: implementation absorbed deferred or out-of-scope work.
- Automation location: manual final diff review, `git diff --name-only`, selected validation output, release/adapter checks only if a later accepted scope requires them.

### T7. Selector behavior is unchanged or directly proved if changed

- Covers: `R4`, `R5`, `R21`-`R23`, `EC2`, `EC9`
- Level: integration, conditional
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/select-validation.py`
  - `scripts/test-select-validation.py`
  - selector output for `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md`
  - active plan/change metadata no-change rationale
- Steps:
  - Confirm implementation records selector behavior as unchanged with rationale if no selector files change.
  - Run selector inspection for the lifecycle summary path and confirm it is classified without unclassified-path blocking.
  - Confirm no validator infers semantic trigger applicability.
  - If selector behavior changes, stop unless the active plan/test spec is revised to scope the change.
  - If selector behavior changes after approved scope revision, add selector regression coverage for lifecycle-summary path classification and selected checks, then run `python scripts/test-select-validation.py`.
- Expected result: M4 either leaves selector behavior unchanged with proof or directly tests any approved selector change.
- Failure proves: selector behavior changed silently or semantic trigger inference leaked into validation.
- Automation location: `python scripts/select-validation.py --mode explicit --path docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md`, optional `python scripts/test-select-validation.py`.

### T8. Static proof stays stable and shape-focused

- Covers: `R6`-`R13`, `R16`, `R21`, `R24`, `R25`, `E7`, `EC10`
- Level: unit, static, manual
- Fixture/setup:
  - `scripts/test-token-cost-report-validation.py`
  - lifecycle summary template
  - first M4 lifecycle summary
  - final implementation diff
- Steps:
  - Confirm added tests check stable headings, field-group labels, path placement, driver-category labels, warning-only cues, and forbidden hard-gate text.
  - Confirm tests do not require a single exact full-sentence assertion when equivalent wording satisfies the contract.
  - Confirm tests do not perform broad natural-language scoring, semantic trigger inference, or token-threshold enforcement.
  - Confirm tests do not require release YAML schema changes for lifecycle summaries.
- Expected result: static proof protects the M4 contract without freezing prose or creating brittle workflow cost.
- Failure proves: test implementation conflicts with cost-bounded rigor by overfitting wording or expanding scope.
- Automation location: `python scripts/test-token-cost-report-validation.py`, manual review of changed assertions.

### T9. Final verify checks required summary and no-change rationale against triggers

- Covers: `R2`, `R15`, `R17`, `R18`, `R20`, `R23`-`R26`, `R29`, `E2`-`E7`, `EC2`-`EC8`, `EC10`
- Level: manual, lifecycle, verification
- Fixture/setup:
  - accepted plan
  - active and approved test spec
  - first M4 lifecycle summary
  - change metadata
  - review records or review-resolution if triggered
  - release metadata if touched
  - explain-change evidence
- Steps:
  - Confirm the accepted plan requires a lifecycle summary for M4 as a large workflow-governance change.
  - Confirm the required summary exists at the expected path and contains required field groups.
  - Confirm trigger reason, source artifacts, stages covered/excluded, observed drivers, largest event, result, and follow-up rationale match the accepted plan, test spec, review artifacts, and release metadata if any.
  - Confirm no-change rationale exists for selector, release, benchmark, adapter, and progressive-loading surfaces that remain unchanged.
  - Confirm explain-change records why no before/after dynamic benchmark comparison was required unless implementation actually ran one or a later accepted artifact required one.
  - Confirm verify blocks if the required summary is missing, incomplete, unsafe, oversized, or inconsistent with the trigger evidence.
- Expected result: final verification can prove M4 met the reporting contract without broadening validation scope.
- Failure proves: lifecycle summary evidence is absent, stale, unsafe, or disconnected from the accepted workflow state.
- Automation location: verify checklist, artifact lifecycle validation, change metadata validation, selected CI, manual evidence comparison.

### T10. Selected validation covers changed paths without broad smoke

- Covers: `R1`, `R3`, `R4`, `R5`, `R16`, `R19`, `R22`, `R27`-`R29`, `E1`, `EC1`, `EC9`
- Level: integration, smoke
- Fixture/setup:
  - final changed implementation paths
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - active plan, test spec, and change metadata
- Steps:
  - Run `python scripts/select-validation.py --mode explicit` with final changed implementation paths and lifecycle artifacts.
  - Confirm all changed paths are classified and no unexpected unclassified paths appear.
  - Confirm selected checks cover token-cost static tests, lifecycle artifacts, change metadata, and any selector regression if selector behavior changes.
  - Confirm `broad_smoke_required` remains false unless a later authoritative trigger appears.
  - Run `bash scripts/ci.sh --mode explicit` with the same final path set.
  - Run `git diff --check --`.
- Expected result: selected validation is sufficient for the scoped M4 implementation and broad smoke remains trigger-driven.
- Failure proves: implementation cannot be validated through the planned targeted proof set or accidentally triggered broad validation.
- Automation location: selector CLI, selected CI wrapper, `git diff --check --`.

## Fixtures and data

- Lifecycle summary template path: `templates/lifecycle-token-cost-summary.md`.
- Required first summary path: `docs/reports/token-cost/lifecycle/2026-05-14-cost-bounded-rigor-m4-lifecycle-token-cost-summary.md`.
- Existing release token-cost reports under `docs/reports/token-cost/releases/` are source evidence only when linked; they are not migrated or duplicated.
- Existing run evidence under `docs/reports/token-cost/runs/` and benchmark fixtures under `benchmarks/token-cost/` remain unchanged unless a later accepted artifact broadens scope.
- No raw JSONL fixture is required for M4.

## Mocking/stubbing policy

No external service mocking is required. Static tests should read repository files directly. If a test needs missing-report behavior, use temporary files or missing-path assertions inside the existing Python test framework rather than adding broad fixtures.

## Migration or compatibility tests

- Existing M1, M2, and M3 cost-bounded-rigor changes do not require retroactive lifecycle token-cost summaries.
- Existing release Token-Friendliness reports and YAML metadata remain valid and are not migrated into lifecycle summaries.
- Existing selector behavior remains valid unless implementation intentionally changes selector behavior after plan/test-spec revision.
- Compatibility is verified by `T6`, `T7`, `T9`, and selected CI.

## Observability verification

- Required lifecycle summaries are observable under `docs/reports/token-cost/lifecycle/`.
- Trigger decisions are observable in the active plan, this test spec, review-resolution if any, release metadata if any, or explicit maintainer request.
- Source artifacts, observed cost drivers, largest observed event, result/rationale, and follow-up routing are observable in the summary.
- `explain-change` must record why dynamic benchmark comparison was or was not required.
- `verify` must check required summary existence, field groups, and trigger match.

## Security/privacy verification

Use `T4` to verify the lifecycle summary avoids secrets, credentials, private machine paths, personal data, and raw JSONL outside existing token-cost policy. Prefer repo-relative paths, counts, stable IDs, links, and concise rationale.

## Performance checks

No runtime performance or dynamic token benchmark is required for M4. Static token-cost report tests and selected validation are sufficient unless implementation explicitly changes benchmark, analyzer, or release-token-cost behavior under a later accepted artifact.

## Manual QA checklist

- Confirm the implementation stays within `docs/workflows.md`, the lifecycle summary template, the first M4 summary, focused static tests, plan/change metadata, and required lifecycle updates unless a review-approved scope change occurs.
- Confirm lifecycle summary triggers remain conditional and limited to the five approved trigger types.
- Confirm the first M4 summary exists because this plan classifies M4 as a large workflow-governance change.
- Confirm the first M4 summary uses bounded evidence and does not paste large raw output.
- Confirm no hard token gates, release gates, dynamic benchmark requirements, release schema changes, adapter packaging changes, generated adapter body tracking, or progressive-loading work were added.
- Confirm selector behavior is recorded as unchanged unless direct regression proof covers an approved change.
- Confirm follow-up recommendations route through existing follow-up ownership rules.
- Confirm final validation commands match the active plan and this test spec.

## What not to test

- Do not run before/after dynamic benchmark comparison for M4 unless a later accepted plan, test spec, release process, or maintainer request requires it.
- Do not validate lifecycle summaries with the release Token-Friendliness YAML schema.
- Do not run release validation, adapter validation, generated adapter archive validation, or broad smoke unless an authoritative trigger appears.
- Do not add tests that infer whether ordinary changes should have had a lifecycle summary.
- Do not freeze one exact workflow/template sentence when stable headings, field groups, or forbidden-boundary checks are sufficient.
- Do not retest progressive-loading behavior, high-cost skill restructuring, or generated public adapter output tracking.

## Uncovered gaps

None. Every M4 `MUST` requirement has automated, selected-integration, lifecycle, or manual proof coverage.

## Next artifacts

```text
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

This test spec is active and maintainer-approved. Implementation may start under the active M4 plan.
