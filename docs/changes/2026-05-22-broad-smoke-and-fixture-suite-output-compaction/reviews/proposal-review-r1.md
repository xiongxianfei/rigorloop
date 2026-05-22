# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Contributor proposal-review
Target: docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md
Status: changes-requested

## Review inputs

- Proposal: `docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`
- User-supplied proposal-review result in chat on 2026-05-22
- Governing boundaries: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`
- Related accepted proposal: `docs/proposals/2026-05-21-script-output-optimization.md`
- Related approved spec: `specs/script-output-optimization.md`

## Result

- Material findings: `BSO-PR1`, `BSO-PR2`, `BSO-PR3`, `BSO-PR4`
- Recording status: recorded after initial chat-only blocker was resolved
- Recording blocker: none
- Review record: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md`
- Review resolution: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`
- Open blockers: none after proposal revision
- Immediate next stage: proposal-review R2
- No automatic downstream handoff: this review does not start spec, test-spec, plan, or implementation work.

## Overall verdict

Good direction, changes requested before planning.

The proposal diagnoses the right problem: the first script-output slice optimized one producer and one wrapper path, while broad-smoke remains a separate orchestration path that streams child output, and some child producers still have noisy direct-run defaults. The producer/orchestrator distinction is the correct frame.

The proposal needs revision before planning because it leaves the proof route conditional, lacks explicit acceptance criteria, does not fully settle the first producer and verbosity contract, and does not yet require stable command/test identity proof.

## Findings

### BSO-PR1 - Proof route is too conditional for a new output layer

Finding ID: BSO-PR1
Severity: major
Location: `Architecture impact`, `Rollout and rollback`, `Next artifacts`
Evidence: The proposal extends the accepted script-output direction from selected-CI to broad-smoke `run_check` and a new direct-run producer, but leaves the route conditional.
Required outcome: State the proof route explicitly before planning.
Safe resolution: Add a `Proof route` section requiring focused test-spec amendment, naming when a spec amendment is required, and blocking implementation until the plan names an approved route.

### BSO-PR2 - Acceptance criteria are missing

Finding ID: BSO-PR2
Severity: major
Location: whole proposal
Evidence: The proposal has goals, testing expectations, risks, and open questions, but no dedicated acceptance-criteria section.
Required outcome: Add explicit acceptance criteria.
Safe resolution: Add `AC-BSO-*` criteria covering audit, broad-smoke capture, failure and verbose output, selected command preservation, first producer output, ordinary-validation coverage, selected-CI regression, and unchanged out-of-scope surfaces.

### BSO-PR3 - First producer and verbosity contract are still ambiguous

Finding ID: BSO-PR3
Severity: major
Location: `Goals`, `Recommended direction`, `Testing and verification strategy`, `Open questions`
Evidence: The proposal names `scripts/test-change-metadata-validator.py` as expected but allows the audit to select a different producer; it also suggests `--verbose` and `--quiet` while saying quiet applies where applicable.
Required outcome: Promote the first-producer and verbosity candidates into explicit decisions.
Safe resolution: Lock the default first producer to `scripts/test-change-metadata-validator.py` unless the audit records a justified approved replacement, and require the plan to explicitly include or exclude `--quiet`.

### BSO-PR4 - Behavior-preservation proof needs stable identity

Finding ID: BSO-PR4
Severity: major
Location: `Testing and verification strategy`, `Rollout and rollback`
Evidence: The proposal requires output-shape and exit-code evidence, but does not require stable ordered command/test identity proof.
Required outcome: Require deterministic command/test identity proof and ordinary-validation coverage.
Safe resolution: Add a behavior-preservation matrix with ordered command/test lists plus SHA-256 hashes, and add an ordinary-validation guard for output-contract tests.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The layering problem is clear and well framed. |
| User value | pass | Successful broad-smoke output becomes easier to scan without weakening failure evidence. |
| Option diversity | pass | The options cover do-nothing, producer-only, wrapper-only, and coordinated slice. |
| Decision rationale | pass | Option 4 follows from the producer/orchestrator model. |
| Scope control | concern | Producer target and proof route need firmer boundaries. |
| Architecture awareness | pass | Correctly separates repository-owned script output from UI transcript folding and generated artifacts. |
| Testability | concern | Needs acceptance criteria and stable selected-command/test identity proof. |
| Risk honesty | pass | Names failure hiding, stderr loss, producer churn, and wrapper divergence. |
| Rollout realism | concern | Milestone idea is good, but acceptance gates are not yet explicit. |
| Readiness for plan | changes-requested | Direction is good; fix the four findings first. |

## Scope-preservation result

Pass.

The proposal preserves the user intent to continue script-output optimization, address broad-smoke and direct producer noise, audit layers, preserve validation behavior and failure evidence, avoid UI transcript folding, and avoid blanket unittest rewrites.

## Recommended next stage

Revise the proposal to resolve `BSO-PR1`, `BSO-PR2`, `BSO-PR3`, and `BSO-PR4`, then rerun proposal-review before downstream plan reliance.
