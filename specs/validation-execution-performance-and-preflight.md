# Validation Execution Performance and Preflight

## Status

approved

## Related proposal

- [Preflight-First and Measured Script Execution Optimization](../docs/proposals/2026-06-24-preflight-first-measured-script-execution-optimization.md)
- Proposal review: [proposal-review-r1](../docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/proposal-review-r1.md)

## Goal and context

RigorLoop validation should preserve rigorous proof while reducing avoidable repeated work. Recent verification cost came from broad validation running before cheap branch-state blockers, repeated process startup and repository inspection, stale evidence after commit-state changes, and self-referential commit hash evidence.

This spec defines the observable contract for phase-aware validation execution, cheap preflight gating, timing evidence, selection explanation, final committed-state verification, and first-slice duplicate-work reduction. It does not authorize skipping required checks, final closeout proof, or cache/parallel behavior before their separate contracts exist.

## Glossary

- `preflight`: cheap deterministic checks that decide whether focused or boundary validation may proceed.
- `focused validation`: validation selected from changed paths, governing artifacts, validator implementation changes, declared dependencies, and explicit triggers.
- `boundary validation`: broad validation such as full suites, broad smoke, clean-install smoke, release validation, or final branch verification.
- `final verify`: the closeout proof that branch readiness is evaluated against committed tracked state.
- `selection explanation`: reviewable output identifying changed paths, selected checks, reasons, omitted checks, and boundary triggers.
- `timing summary`: bounded per-phase and per-check measurement evidence.
- `same-commit evidence`: evidence recorded in the same commit that contains the evidence artifact.

## Examples first

Example E1: cheap tracked-state blocker stops boundary validation
Given a validation run has untracked authoritative artifacts
When preflight runs
Then the run reports the blocker, affected paths, and the cheapest corrective action or rerun command
And boundary validation does not start unless the user explicitly requests diagnostic execution.

Example E2: focused failure prevents unnecessary broad validation
Given preflight passes and focused validation is selected
When a focused validator fails
Then boundary validation is skipped unless an explicit diagnostic override is requested
And the failure preserves the focused validator exit semantics and diagnostics.

Example E3: authoritative boundary trigger still runs broad validation
Given preflight and focused validation pass
When a validator implementation, selector implementation, release boundary, package boundary, or broad-smoke trigger changes
Then boundary validation runs and records the trigger reason.

Example E4: final verify proves committed branch state
Given implementation and pre-commit validation are complete
When final verify claims branch readiness
Then it evaluates current committed `HEAD` and clean tracked state
And same-commit evidence avoids embedding the commit's literal final hash in files being amended into that commit.

Example E5: optimized run remains explainable
Given a run selects a smaller validation set
When the run completes
Then evidence names selected checks, selection reasons, non-selected checks, boundary triggers, timings, and any explicitly unavailable timing details.

## Requirements

R1. Validation orchestration MUST evaluate preflight before focused validation and boundary validation.

R2. Preflight MUST check cheap blockers that can make final readiness impossible, including resolvable repository state, unmerged paths, tracked and untracked authoritative artifact state, required artifact presence, review closeout blockers when applicable, plan/change metadata consistency when applicable, generated-output dirtiness when applicable, and selection input validity.

R3. When preflight finds a blocker, the run MUST NOT start boundary validation unless the user explicitly requests diagnostic execution.

R4. A preflight blocker report MUST name the specific blocker, affected paths when applicable, and the cheapest corrective action or rerun command known to the tool.

R5. Focused validation MUST run only after preflight passes or an explicit diagnostic override is recorded.

R6. A focused validation failure MUST prevent boundary validation from starting unless an explicit diagnostic override is recorded.

R7. Boundary validation MUST still run when an authoritative trigger applies, including validator or selector implementation changes, release/package boundary changes, final closeout, clean-install smoke triggers, or when focused validation cannot prove sufficient coverage.

R8. Optimized validation MUST preserve required check coverage, failure detection, exit-code meaning, diagnostic IDs, machine-readable output contracts, and rerun guidance.

R9. Each selected check MUST record phase, command or check identifier, result, and duration.

R10. Timing evidence MUST include a bounded summary of preflight, focused, boundary, and total duration when those phases run.

R11. Timing evidence SHOULD distinguish cold and warm measurements when measuring representative performance baselines.

R12. Selection explanation MUST identify changed paths, selected checks, selection reasons, checks not selected, and boundary triggers.

R13. Related validators SHOULD share immutable repository-state context within one orchestration invocation when doing so reduces duplicate Git inspection, filesystem scans, or parsing without changing standalone validator contracts.

R14. Standalone validator CLI entry points MUST remain available and compatible for existing contributor and CI use.

R15. The first slice MUST NOT enable result caching for final closeout proof.

R16. Any future cache use MUST treat missing, malformed, incomplete, or changed identity as a cache miss.

R17. Final branch-readiness verification MUST run against committed tracked state when it claims branch readiness.

R18. Same-commit evidence MUST NOT require embedding the commit's literal final hash into files being amended into that same commit.

R19. Parallel validation execution MUST NOT be enabled until a separate approved contract proves independence, deterministic ordered output, and resource bounds.

R20. Performance budgets MUST start as recorded baselines and warnings for at least two rollout cycles before any threshold becomes a failing gate.

R21. Detailed timing sidecars MUST have a retention policy before rollout so high-volume measurement output does not become long-term repository bloat by default.

R22. Diagnostic output reduction MUST NOT be treated as runtime improvement unless timing evidence proves elapsed-time reduction.

## Inputs and outputs

Inputs include changed paths, repository state, selected explicit paths, governing artifacts, validator implementation files, release/package boundary signals, review and plan state when applicable, and explicit diagnostic override flags.

Outputs include preflight result, selected checks, phase results, timing summary, blocker diagnostics, validation exit status, and optional detailed timing sidecars.

## State and invariants

- Required validation proof remains required even when execution is optimized.
- Preflight is an execution gate, not a replacement for focused or boundary validation.
- Cache hits, when later introduced, are inner-loop evidence and are not final closeout proof.
- Final branch readiness belongs to final verify evidence, not pre-commit validation.
- The optimized path remains reviewable from tracked artifacts and command output.

## Error and boundary behavior

- Unknown changed-surface selection input produces a preflight failure.
- Missing cache identity, if caching exists later, produces a cache miss rather than a pass.
- Architecture ambiguity for a future persistent service, remote cache, shared worker, or cross-process protocol returns to architecture before planning or implementation.
- Explicit diagnostic override may run broad checks after a blocker, but the result cannot claim final readiness until the blocker is resolved.

## Compatibility and migration

Existing standalone validation scripts and CI wrapper calls remain supported. Initial rollout may add timing and selection explanation without changing selected check coverage. Contributors can continue running existing commands while orchestration begins to share immutable repository context.

## Observability

Validation evidence records per-check phase, result, duration, selected checks, blocker reasons, and boundary triggers. Detailed timing sidecars are optional and bounded by a retention policy.

## Security and privacy

Validation evidence must not record secrets, credentials, private keys, or host-specific debug paths except where already intentionally part of a reviewed example. Subprocess execution uses explicit arguments and failure checking rather than shell-dependent command strings where repository scripts control invocation.

## Accessibility and UX

No user-interface accessibility impact. Command output should remain concise and actionable, especially for preflight blockers.

## Performance expectations

The representative workflow should show measured wall-clock reduction or record why no safe reduction was available. Baselines include cold and warm timing, Git inspection count, subprocess launch count, and phase durations.

## Edge cases

EC1. Preflight blocks on untracked authoritative artifacts before boundary validation.

EC2. Focused validation fails and boundary validation is skipped without an override.

EC3. Validator implementation changes trigger boundary validation even when changed user artifacts are narrow.

EC4. Final verify runs after commit creation and avoids literal self-referential hash evidence.

EC5. Timing instrumentation is present but does not alter validator exit semantics.

EC6. Detailed timing output is too large for common evidence and is routed to a sidecar with retention policy.

EC7. A future cache record is malformed and is treated as a miss.

EC8. A future parallel run would interleave output and is rejected until deterministic ordering exists.

## Non-goals

- Skip required validation.
- Replace final broad validation when an authoritative trigger requires it.
- Enable first-slice local, remote, or shared caching.
- Enable first-slice parallel execution.
- Rewrite every validator or optimize individual functions before profiling.
- Redesign hosted CI.
- Treat quieter output as performance improvement.

## Acceptance criteria

AC1. Preflight runs before focused and boundary validation.

AC2. Known tracked-state blockers prevent unnecessary boundary validation.

AC3. Focused checks preserve approved selected-check coverage.

AC4. Authoritative boundary triggers still run broad validation.

AC5. Per-check and per-phase timings are reviewable.

AC6. Selection reasons are visible.

AC7. Repeated repository-state collection is reduced where shared immutable context is introduced.

AC8. Standalone script interfaces remain compatible.

AC9. Exit codes and failure diagnostics are preserved.

AC10. Final branch verification runs against committed state.

AC11. Evidence files do not embed their own mutable final commit hash.

AC12. Caching and parallelism remain disabled until separate approved contracts exist.

AC13. Preflight failures name blockers and corrective action.

AC14. Timing sidecar retention is defined before detailed timing rollout.

## Open questions

None for first-slice specification. Caching, parallelism, hosted-CI reuse, and persistent workers require follow-up proposals or specs before implementation.

## Next artifacts

- spec-review
- architecture assessment
- plan
- plan-review
- test-spec

## Follow-on artifacts

- Spec review: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/spec-review-r1.md`
- Architecture assessment: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/change.yaml`
- Plan: `docs/plans/2026-06-24-preflight-first-measured-script-execution-optimization.md`
- Plan review: `docs/changes/2026-06-24-preflight-first-measured-script-execution-optimization/reviews/plan-review-r1.md`

## Readiness

Approved for downstream planning after recorded clean spec-review and architecture assessment.
