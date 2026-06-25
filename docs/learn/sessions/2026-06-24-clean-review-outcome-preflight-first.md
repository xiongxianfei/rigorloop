# Learn Session: Clean Review Outcome for Preflight-First Validation

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the preflight-first workflow produced no material findings.
- Trigger type: explicit maintainer request / workflow retrospective.
- Scope:
  - `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/review-log.md`
  - review records under `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/`
  - `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/explain-change.md`
  - `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/verify-report.md`
  - `docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md`
  - `specs/validation-execution-performance-and-preflight.md`
  - `specs/validation-execution-performance-and-preflight.test.md`
- Evidence in scope:
  - 8 formal review records.
  - 0 material findings in `review-log.md`.
  - 5 clean code-review receipts for implementation milestones M1 through M5.
  - Final verify report with one selected-CI default-timeout note rerun successfully with the documented timeout override.
  - Artifact validators that caught and resolved lifecycle bookkeeping issues before final verify.
- Explicit exclusions:
  - no claim about hosted CI;
  - no PR readiness claim;
  - no workflow, spec, skill, validator, topic, or plan-template update from this learn session;
  - no durable topic update without reusable evidence and contributor-confirmed routing.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
  - `docs/learn/sessions/2026-05-12-clean-review-settlement-vs-chat-evidence.md`
  - `docs/learn/topics/review-artifact-recording.md`
- Session record path: `docs/learn/sessions/2026-06-24-clean-review-outcome-preflight-first.md`

## Observe

### O1 - The reviews were clean because the implementation was narrow and reviewed in bounded slices

Evidence:

- The plan split the work into five milestones: timing/selection explanation, cheap preflight, boundary trigger preservation, shared immutable context, and final-verify boundaries.
- Code-review M1 through M5 each recorded `Material findings: none`.
- The code-review notes show scoped judgments rather than broad approval by assumption: M1 checked additive timing output, M2 checked untracked governing artifact blocking, M3 checked boundary trigger visibility, M4 checked the shared context stayed small, and M5 checked cache/concurrency remained out of scope.

Observation:

No material finding existed because each review target was small enough to compare directly against the accepted spec, test spec, and plan milestone. The reviewers did not need to settle broad architecture or policy questions during code review.

### O2 - Upstream artifacts had already absorbed the contentious decisions

Evidence:

- Proposal-review R1, spec-review R1, and plan-review R1 were approved with no material findings.
- The accepted proposal and approved spec explicitly deferred first-slice caching and new concurrency, required preflight diagnostics, preserved boundary validation, and avoided self-referential commit-hash evidence.
- The test spec mapped those requirements to selector/CI tests and manual final-verify checks before implementation.

Observation:

The likely disagreement points were resolved upstream before code was written. By the time implementation review ran, the question was mostly whether the diff matched the settled contract, not whether the direction was correct.

### O3 - Mechanical workflow mistakes were found by validators, not formal review findings

Evidence:

- During finalization, validation caught missing structured review header fields, stale plan-index stage text, stale test-spec readiness wording, and final-closeout reason-code formatting.
- Those were corrected before final verify passed.
- `validate-review-artifacts`, `validate-change-metadata`, `validate-artifact-lifecycle`, whitespace validation, and selected CI all passed after correction.

Observation:

The workflow was not error-free. The difference is that the errors were mechanical artifact-state issues detected by validation before they became unresolved review findings. That is exactly the useful boundary between validation failures and material review findings.

### O4 - The selected-CI timeout was a verify note, not a material review finding

Evidence:

- The verify report records that default selected CI timed out on `selector.regression` after 60 seconds.
- The same selected-CI scope passed with documented `--timeout 180`.
- The final post-commit selected-CI scope also passed with preflight results and focused phase summaries.

Observation:

The timeout was real evidence about local runtime behavior, but it did not prove a correctness bug in the implementation or a broken validation contract. It was recorded as residual risk and reproducible validation context, not as a material finding.

### O5 - The clean outcome is not proof that clean reviews should be expected by default

Evidence:

- Prior learn session `2026-05-09-review-finding-volume-root-cause.md` shows a workflow-governance change with many material findings when route vocabulary, generated surfaces, and plan state were unstable.
- This change reused lessons from that pattern: scope was narrower, follow-up boundaries were explicit, generated/public-skill surfaces were not changed, and validation caught lifecycle bookkeeping drift.

Observation:

Zero material findings here is best explained by preparation and scope control, not by weaker review standards. The useful signal is that the workflow kept unresolved correctness and contract issues out of formal review by settling them earlier or catching them with validators.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Review records and active plan evidence | The bounded milestone shape explains the clean code reviews for this change. |
| O2 | observation | observation | None | Proposal/spec/test-spec/plan review evidence | The contentious choices were already settled upstream. |
| O3 | observation | observation | None | Validator failures and final passing validation evidence | Mechanical mistakes occurred, but validation caught them before they became review findings. |
| O4 | observation | observation | None | Verify report evidence | The timeout was a recorded runtime caveat with a successful documented rerun, not a material correctness finding. |
| O5 | no-durable-lesson | no-durable-lesson | None | Prior learn evidence and current review log | A single clean workflow is not enough reusable evidence for new durable guidance. Existing learn records already cover review-finding root causes and clean review settlement. |

Contributor confirmation status: not confirmed for routing. This session records the explanation only.

## Route

- Observation routing: kept in this session record.
- Durable lesson routing: not created.
- Artifact update routing: not created.
- Decision routing: not created.
- Direction routing: not created.
- Process follow-up routing: not created.

## Direct Answer

No material finding exists in this workflow because the review gates did not find an unresolved correctness, contract, scope, or evidence defect at the moment they reviewed their targets.

The work avoided material findings for four practical reasons:

1. Directional choices were settled before implementation: proposal, spec, test spec, and plan had already defined the boundaries.
2. Implementation was sliced narrowly: each code review examined one bounded milestone instead of a broad mixed change.
3. Risky follow-ups stayed out of scope: caching, new concurrency, hard performance budgets, and persistent workers were deferred rather than half-implemented.
4. Mechanical mistakes were caught by validators and fixed before final verify, so they remained validation failures, not formal material review findings.

This does not mean the workflow had no issues. It had at least one important verify caveat: selected CI needed a higher timeout for the selector regression suite. The caveat was recorded and rerun successfully, so it did not become a material review finding.

## No-Durable-Lesson Rationale

No topic entry was created. The session explains one clean workflow outcome, but the evidence does not show a new recurring pattern or systemic gap. Existing learn artifacts already cover the contrasting case where unstable scope and vocabulary produced many findings, and existing governance already defines how clean reviews and validation evidence are recorded.

## Follow-Ups

- None scheduled.
- If future selector-regression runs repeatedly exceed the selected-CI default timeout, that should be handled as a separate performance or CI-maintenance follow-up rather than as a review-finding lesson.
