# Plan Review R1 - Independent Adversarial Review Gates

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Target: docs/plans/2026-06-25-independent-adversarial-review-gates.md
Reviewed artifact: docs/plans/2026-06-25-independent-adversarial-review-gates.md
Review date: 2026-06-25
Reviewer: Codex plan-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: PR1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/plan-review-r1.md
- Review log: ../review-log.md
- Review resolution: ../review-resolution.md
- Open blockers: PR1-F1
- Immediate next stage: plan revision

## Scope

Reviewed the active execution plan against the accepted proposal, approved spec, approved architecture package, ADR, architecture-review evidence, repository governance, and existing validation/generation boundaries.

## Reviewed Inputs

- Plan: `docs/plans/2026-06-25-independent-adversarial-review-gates.md`
- Plan index: `docs/plan.md`
- Accepted proposal: `docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md`
- Approved spec: `specs/review-independence-and-criticality.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260625-independent-adversarial-review-gates.md`
- Architecture-review: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/architecture-review-r1.md`
- Change metadata: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
- Review ledger: `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/review-log.md`

## Dimension Review

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan identifies source artifacts, current handoff, touched surfaces, non-goals, risks, dependencies, and validation ownership. |
| Source alignment | concern | The milestones trace the approved spec and architecture, but generated adapter proof is named as in scope without repository-supported adapter archive commands. See PR1-F1. |
| Milestone size | pass | M1-M5 split evidence schema, routing semantics, skill pilot guidance, calibration, and final generated/doc proof into reviewable slices. |
| Sequencing | pass | Evidence model precedes routing, routing precedes skill guidance, calibration follows record semantics, and test-spec is required before implementation. |
| Scope discipline | pass | The plan keeps hosted services, databases, external control planes, ordinary heterogeneous-model requirements, and full review-family migration out of the first slice. |
| Validation quality | concern | Core validators, lifecycle checks, skill checks, selector checks, and CI commands are named, but adapter release-archive validation is omitted despite planned canonical skill changes. See PR1-F1. |
| TDD readiness | pass | Each milestone names concrete tests and blocks implementation on the matching test spec. |
| Risk coverage | concern | The plan covers attestation-only gates, correction-loop regression, skill-publication leakage, fixture overfit, and selector routing debt; it needs adapter proof coverage to close generated guidance risk. See PR1-F1. |
| Architecture alignment | concern | The architecture says generated adapter validation is required when canonical stage-skill text changes; the plan's M3/M5 command set does not yet operationalize that requirement. See PR1-F1. |
| Operational readiness | concern | The plan is operationally clear for review, lifecycle, skill, selector, and CI checks, but not for generated public adapter archive proof. See PR1-F1. |
| Plan maintainability | pass | Status, handoff, progress, decisions, surprises, validation notes, and rollback paths are present and updateable. |

## Findings

### PR1-F1 - Generated adapter proof is in scope but lacks runnable validation commands

Finding ID: PR1-F1
Severity: major
Dimension: Validation quality

Location:

- `docs/plans/2026-06-25-independent-adversarial-review-gates.md:175`
- `docs/plans/2026-06-25-independent-adversarial-review-gates.md:200`
- `docs/plans/2026-06-25-independent-adversarial-review-gates.md:261`
- `docs/plans/2026-06-25-independent-adversarial-review-gates.md:285`
- `docs/architecture/system/architecture.md:315`
- `docs/architecture/system/architecture.md:316`
- `docs/architecture/system/architecture.md:913`
- `AGENTS.md:34`
- `AGENTS.md:36`

Evidence:

- M3 changes canonical review and workflow skills under `skills/`, including `code-review`, `workflow`, `implement`, `review-resolution`, `spec-review`, and `plan-review`, but its validation commands are limited to skill validation, skill tests, local skill build tests, and `build-skills.py --check`.
- M5 names "generated skill/adapters checks", lists `generated adapter validation surfaces`, and says implementation should "Refresh generated skill/adapters evidence using repository-owned scripts", but its validation commands again omit adapter archive generation and adapter validation.
- Repository governance states that for `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`, and generated public adapter package output must not be hand-edited.
- The canonical architecture identifies `scripts/build-adapters.py` as the generator for public adapter output and `scripts/validate-adapters.py` as the validator for generated temporary or release-output adapter packages. It also states that generated adapter validation is required whenever canonical stage-skill text changes.
- The local command interfaces support the required proof path: `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>` and `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`.

Problem:

The plan correctly treats public generated adapter compatibility as part of the final proof, but it does not name the runnable repository-supported adapter archive commands. An implementer could complete M3/M5 with valid canonical skill checks while never proving that Codex, Claude, and opencode adapter archives still build and validate from the changed skill guidance.

Required outcome:

Revise the plan so canonical skill changes that affect public skill guidance include generated public adapter archive proof through repository-owned commands.

Safe resolution path:

Add explicit adapter archive proof to M5 and the overall validation plan. A sufficient revision is:

- Build temporary public adapter archives with `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"`.
- Validate the temporary archives with `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`.
- Record that this is the supported proof path for `v0.1.3` and later, instead of relying on tracked generated adapter package bodies.
- If the test spec chooses a different current version token, use the version selected by `dist/adapters/manifest.yaml` or the approved release guidance, but keep both generation and validation commands explicit.

## Missing Milestones Or Dependencies

No implementation milestone is missing. The plan needs a validation-command addition inside the existing generated guidance/final proof slice before it is ready for test-spec.

## Suggested Edits

- In M5 `Validation commands`, add temporary adapter archive generation and validation commands for the current adapter manifest version.
- In the top-level `Validation plan`, include the same generated adapter proof when canonical `skills/` files are touched.
- In M3 or M5 notes, state that `build-skills.py --check` proves local/generated skill output, while `build-adapters.py --output-dir` plus `validate-adapters.py --root` proves public adapter archive output.

## Immediate Next Stage

Plan revision. Do not proceed to test-spec until PR1-F1 is resolved and plan-review reruns cleanly.

## Isolation

This was an isolated formal plan-review request. There is no automatic downstream handoff.
