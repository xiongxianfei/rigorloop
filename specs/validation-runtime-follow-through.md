# Validation Runtime Follow-Through

## Status

approved

## Related proposal

- Proposal: [Preflight-First Validation Runtime Optimization](../docs/proposals/2026-06-26-preflight-first-validation-runtime-optimization.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r1.md)
- Proposal review R2: [proposal-review-r2](../docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/proposal-review-r2.md)
- Prior accepted proposal: [Preflight-First and Measured Script Execution Optimization](../docs/proposals/2026-06-24-preflight-first-measured-script-execution-optimization.md)
- Prior spec: [Validation Execution Performance and Preflight](validation-execution-performance-and-preflight.md)
- Prior plan: [Preflight-First and Measured Script Execution Optimization Plan](../docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md)
- Prior timing evidence: [script-performance-baseline.yaml](../docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/script-performance-baseline.yaml)

## Goal and context

The June 24 validation execution work introduced preflight-first validation, phase metadata, selected-check timing, `cache_status: not-applicable`, preflight diagnostics, boundary phase metadata, and an immutable preflight context. Its verification evidence showed that selected validation can still exceed the default selected-CI timeout because `selector.regression` dominates focused selected-check runtime.

This spec defines the follow-through contract for using that evidence safely:

- collect and publish a durable baseline from the shipped timing surfaces;
- profile and, when safe, reduce `selector.regression` runtime without reducing selector proof;
- make missing selector routing a deterministic selected-validation blocker;
- classify broad-smoke child checks before any broad-smoke parallelism is proposed;
- keep cache, broad validator composition, and broad-smoke parallel execution outside this first implementation slice.

This spec does not replace the prior validation execution performance and preflight spec. The prior spec remains the source of truth for the general phase model, preflight gate, timing summary, final committed-state verification, cache boundary, and parallelism boundary.

## Glossary

- `June 24 validation foundation`: the accepted June 24 proposal, approved spec, plan, and implementation evidence for preflight-first measured validation execution.
- `baseline evidence`: change-local or plan-linked timing evidence produced from existing phase and selected-check timing output.
- `selector.regression`: the selected validation regression check that exercises validation selector behavior.
- `selected-check identity`: the set of selected check IDs, relevant reasons, and path triggers that define what selected validation proves.
- `failure sensitivity`: evidence that negative or malformed routing fixtures still fail after an optimization.
- `missing selector route`: a changed path or evidence class that should be classified by selected validation but lacks deterministic routing.
- `diagnostic broad-smoke`: broad-smoke execution requested for additional diagnostics after a blocker, without converting the blocked selected-validation result into a pass.
- `broad-smoke child classification`: a read-only inventory of broad-smoke child checks and their safety properties before parallelism.

## Examples first

Example E1: baseline identifies selected-validation bottleneck
Given the June 24 phase/timing instrumentation exists
When the follow-through baseline is recorded
Then it reports selected-validation, broad-smoke, and final-verify scenarios separately
And it identifies whether `selector.regression`, broad-smoke children, Git inspection, subprocess startup, or parsing dominates each scenario.

Example E2: selector optimization preserves proof
Given `selector.regression` has baseline selected-check identity and failure fixtures
When the suite is optimized
Then the same selected-check identity remains covered
And the same failure fixtures still fail
And the result records a before/after profile or explains why no safe reduction was possible.

Example E3: missing selector route blocks selected validation
Given a changed path belongs to an artifact class that requires deterministic selected routing
When selected validation cannot classify that path
Then selected validation reports a missing-route blocker
And diagnostic broad-smoke, if explicitly requested, does not erase the blocker.

Example E4: broad-smoke classification does not change execution
Given broad-smoke child checks have not been classified
When this first slice runs
Then broad-smoke remains sequential
And the output is a classification artifact, not enabled parallel execution.

Example E5: cache status remains boundary metadata
Given selected validation reports `cache_status`
When the first slice records evidence
Then `cache_status` remains informational
And no cache hit is used as final closeout proof.

## Requirements

R1. The follow-through work MUST treat the June 24 validation foundation as the upstream baseline and MUST NOT supersede or restate the prior phase model as a replacement contract.

R2. The baseline evidence MUST cite durable artifacts for the upstream foundation, including the accepted June 24 proposal, prior spec, prior plan, prior change ID, and relevant timing evidence.

R3. The baseline evidence MUST distinguish developer inner-loop selected validation, boundary or broad-smoke validation, and final verify scenarios.

R4. The baseline evidence MUST identify the dominant measured contributor for each recorded scenario when the existing timing output makes that determination possible.

R5. The system MUST NOT set a fixed percentage runtime-reduction target for this follow-through slice until baseline evidence has been reviewed in a downstream plan or test spec.

R6. `selector.regression` MUST be profiled before any runtime optimization is accepted.

R7. `selector.regression` preservation proof MUST record baseline selected-check identity and post-change selected-check identity.

R8. `selector.regression` preservation proof MUST show that routing and failure fixtures that are expected to fail still fail after optimization.

R9. `selector.regression` preservation proof MUST show that routing fixtures that are expected to pass still pass after optimization.

R10. A `selector.regression` runtime change MUST NOT be accepted solely because elapsed time is lower; it also needs preserved selected-check identity, preserved failure sensitivity, and preserved diagnostics.

R11. If no safe `selector.regression` runtime reduction is found, the result MUST record the profile, the reason no safe reduction was available, and either a timeout recommendation or a follow-up decision.

R12. Selected validation MUST report a deterministic missing-route blocker when a changed path belongs to a known class that requires selector routing but no routing rule applies.

R13. A missing-route blocker report MUST include the unclassified path, blocker ID, affected artifact or path class when known, and corrective guidance to add or update selector routing.

R14. Diagnostic broad-smoke MAY run after a missing-route blocker only when explicitly requested, but it MUST NOT convert the blocked selected-validation result into a clean selected-validation pass.

R15. New lifecycle evidence classes, validator fixture classes, guide artifact classes, generated output classes, and release evidence classes MUST have selector-routing registration or an explicit out-of-scope rationale before selected validation can pass for those paths.

R16. The first broad-smoke follow-through slice MUST produce broad-smoke child classification before proposing any broad-smoke parallel execution.

R17. Broad-smoke child classification MUST record check ID, command, read/write behavior, temporary roots, shared outputs, network use if any, CPU/I/O expectations, nested parallelism risk, output-order risk, failure-output dependency, parallel-safe candidate status, and classification confidence.

R18. Broad-smoke child classification MUST be read-only in this slice and MUST NOT change broad-smoke execution order or concurrency.

R19. Broad-smoke parallel execution MUST remain disabled unless a later approved artifact consumes the classification and authorizes bounded parallel execution.

R20. `cache_status` MAY remain in selected validation output as boundary metadata, but this slice MUST NOT enable cache reuse or treat cache hits as final proof.

R21. Broad multi-validator in-process composition MUST remain out of scope for this slice.

R22. A downstream plan MAY include validator composition readiness assessment only when baseline evidence shows repeated startup, import, Git inspection, or parsing remains material.

R23. If a validator composition proof of concept is later allowed, it MUST start with one validator or wrapper and MUST preserve standalone CLI behavior, exit codes, failure diagnostics, and rerun guidance.

R24. Final verify MUST remain actual-run evidence against stable committed tracked state; selected-validation speedups MUST NOT claim branch readiness, PR readiness, or hosted CI success.

R25. Follow-through evidence MUST preserve selected-check coverage, broad-smoke coverage, failure detection, exit behavior, diagnostic IDs, and reviewable rerun guidance.

## Inputs and outputs

Inputs include changed paths, selector results, selected-check timing output, prior June 24 timing evidence, selected validation command output, broad-smoke child commands, final verify evidence, routing fixture results, failure fixture results, and explicit diagnostic broad-smoke requests.

Outputs include baseline evidence, selector-regression profile evidence, selected-check identity comparison, failure-sensitivity proof, missing-route blocker diagnostics, broad-smoke child classification, follow-up recommendations, validation exit status, and updated change-local metadata.

## State and invariants

- Validation must become faster only through measurement, sequencing, safe optimization, or duplicate-work reduction, not by removing proof.
- The June 24 validation execution performance and preflight spec remains active for the general preflight and phase model.
- Selected-validation proof and broad-smoke proof remain distinct.
- Missing selector routing is a blocker even when diagnostic broad-smoke also runs.
- Broad-smoke classification is evidence for a later decision, not permission to parallelize.
- Cache metadata is not cache permission.
- Final verify remains separate from inner-loop selected validation.

## Error and boundary behavior

- If baseline evidence cannot distinguish selected validation, broad-smoke, and final verify, the result is blocked until the evidence is split or the limitation is recorded.
- If selected-check identity cannot be compared before and after a selector optimization, the optimization is blocked from acceptance.
- If expected failure fixtures stop failing, the optimization is blocked even if runtime improves.
- If a path class is ambiguous, selected validation reports a missing-route or ambiguous-route blocker rather than silently falling through to broad-smoke.
- If broad-smoke child classification confidence is low, the child is not a parallel-safe candidate.
- If a diagnostic broad-smoke run passes after a missing-route blocker, selected validation remains blocked until routing is fixed or an explicit out-of-scope rationale is accepted.

## Compatibility and migration

Existing standalone validation commands remain supported. The existing selected-CI timeout override remains available while `selector.regression` profiling and optimization are evaluated. Broad-smoke remains sequential in this slice, so existing broad-smoke output ordering and failure behavior remain compatible. Existing `cache_status: not-applicable` output remains valid as boundary metadata.

No migration of historical timing evidence is required. New evidence should cite durable June 24 artifacts rather than relying on PR-number shorthand.

## Observability

Follow-through evidence must be reviewable from tracked or change-local artifacts. Baseline evidence records scenario, command, selected checks, phase duration, dominant contributor when measurable, and known limitations. Selector-regression evidence records before/after profile shape and proof-preservation results. Missing-route blockers expose path, blocker ID, class, and corrective action. Broad-smoke classification records the fields in R17.

## Security and privacy

Evidence must not record secrets, credentials, tokens, private keys, or machine-local debug paths unless they are intentionally part of a reviewed fixture. Broad-smoke classification must identify network use when present so later parallel execution does not multiply external side effects silently.

## Accessibility and UX

No UI accessibility impact. Command-line diagnostics should remain concise and actionable. Missing-route blocker output should tell the contributor what path was unclassified and what routing or out-of-scope decision is needed.

## Performance expectations

This slice measures before setting numeric performance targets. It should reduce or explain the `selector.regression` selected-validation bottleneck. It should not claim success solely from lower elapsed time unless proof preservation also passes.

Broad-smoke performance is addressed by classification in this slice. Runtime reduction for broad-smoke belongs to a later approved slice after classification evidence exists.

## Edge cases

EC1. Baseline evidence shows `selector.regression` dominates selected validation but no safe runtime reduction is found.

EC2. A selector-regression optimization lowers runtime but removes a negative routing fixture.

EC3. A new generated output class changes but no selector route applies.

EC4. Diagnostic broad-smoke passes after selected validation reports a missing-route blocker.

EC5. A broad-smoke child writes generated output or shared temporary state and is therefore not a parallel-safe candidate.

EC6. A broad-smoke child has no writes but has output ordering assumptions that make concurrent aggregation unsafe.

EC7. Baseline evidence uses PR-number shorthand without durable artifact references.

EC8. A composition readiness assessment finds repeated parsing cost but no safe standalone CLI compatibility proof.

EC9. `cache_status` appears in output and is mistakenly treated as cache reuse evidence.

## Non-goals

- Do not supersede the June 24 proposal or the prior validation execution performance and preflight spec.
- Do not enable broad-smoke parallel execution in this slice.
- Do not enable local, remote, or shared result caching in this slice.
- Do not compose multiple validators into one in-process runner in this slice.
- Do not remove selector regression fixtures to improve runtime.
- Do not weaken selected routing, broad-smoke coverage, failure diagnostics, or final verify.
- Do not set a fixed percentage runtime target before reviewed baseline evidence exists.
- Do not claim branch readiness, PR readiness, hosted CI success, or final closeout from inner-loop speedups.

## Acceptance criteria

AC1. Baseline evidence cites durable June 24 artifacts and distinguishes selected validation, broad-smoke, and final verify scenarios.

AC2. `selector.regression` has profile evidence before any optimization is accepted.

AC3. Selector-regression optimization either preserves selected-check identity and failure sensitivity or records why no safe reduction was available.

AC4. Missing selector routing produces a deterministic blocker with path, blocker ID, class when known, and corrective guidance.

AC5. Diagnostic broad-smoke cannot erase a missing-route selected-validation blocker.

AC6. Broad-smoke child classification records the fields required by R17.

AC7. Broad-smoke execution remains sequential in this slice.

AC8. Cache reuse and broad validator composition remain disabled unless separate approved artifacts authorize them.

AC9. Final verify remains actual-run evidence against stable committed tracked state.

AC10. Existing standalone validator and CI wrapper behavior remains compatible.

## Open questions

None for this spec. Numeric runtime targets, broad-smoke parallel execution, cache identity, and broad validator composition are intentionally routed to downstream plans or separate follow-up artifacts.

## Next artifacts

- spec-review
- architecture assessment
- plan
- plan-review
- test-spec
- implementation
- code-review
- explain-change
- verify
- pr

## Follow-on artifacts

- Spec review: `docs/changes/2026-06-26-preflight-first-validation-runtime-optimization/reviews/spec-review-r1.md`
- Plan: `docs/plans/2026-06-26-preflight-first-validation-runtime-optimization.md`
- Test spec: `specs/validation-runtime-follow-through.test.md`

## Readiness

Approved for planning.
