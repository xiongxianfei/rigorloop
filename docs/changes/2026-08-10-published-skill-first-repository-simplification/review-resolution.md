# Review Resolution: Published-Skill-First Repository Simplification

## Summary

Closeout status: open

Review closeout: code-review-m1-r1

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: architecture-review-r1
Review closeout: architecture-review-r2
Review closeout: plan-review-r1
Review closeout: spec-review-r2
Review closeout: test-spec-review-r1
Review closeout: test-spec-review-r2
Review closeout: test-spec-review-r3

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `architecture-review-r1`, `architecture-review-r2`, `plan-review-r1`, `spec-review-r2`, `test-spec-review-r1`, `test-spec-review-r2`, `test-spec-review-r3`, `code-review-m1-r1`
- Findings resolved: 5
- Unresolved findings: 2
- Current result: M1 code-review R1 requested two fail-closed corrections before milestone closeout.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| PSR-PR1-001 | rejected | resolved | R2 accepted deterministic repository acceptance and review-owned semantic quality instead of target-runtime behavior evaluation. |
| PSR-AR1-001 | accepted | resolved | The canonical Deployment View now records the approved package, materialization, release, and target-runtime execution boundaries. |
| PSR-TSR1-001 | accepted | resolved | Feature-spec identity now cites current approving review R2. |
| PSR-TSR1-002 | accepted | resolved | MP1 now provides the complete auditable manual-proof contract. |
| PSR-TSR2-001 | accepted | resolved | CMD18 now validates active R2 test-spec revision evidence. |
| PSR-CR-M1-R1-001 | accepted | open | Structured completed proof must replace nonempty prose as removal authority. |
| PSR-CR-M1-R1-002 | accepted | open | R26 disposition values must fail closed, not only their key set. |

## Finding Details

### code-review-m1-r1

Review ID: code-review-m1-r1

#### PSR-CR-M1-R1-001 - Placeholder evidence can authorize removal

Finding ID: PSR-CR-M1-R1-001
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: review-resolution
Chosen action: Add structured old/replacement commands and results, comparison outcome, removal decision, rollback point, and evidence paths; require completed values before removable or retired.
Rationale: R17-R20 make completed dual proof and recovery evidence authoritative; nonempty pending prose cannot satisfy those properties.
Safe resolution path: Apply the declared-safe recipe recorded in code-review-m1-r1 without touching CI, selector, package, release, or skill bodies.
Validation target: code-review-m1-r2
Validation evidence: pending
needs-decision rationale: none

#### PSR-CR-M1-R1-002 - R26 values do not fail closed

Finding ID: PSR-CR-M1-R1-002
Disposition: accepted
Status: open
Owner: implementation author
Owning stage: review-resolution
Chosen action: Validate the exact `superseded-prospectively` value for every R26 key and add an unknown-value regression test.
Rationale: The exact prospective disposition and repository closed-vocabulary rule already determine the correction.
Safe resolution path: Apply the mechanical constant-and-test correction without changing the approved clause set or retained deterministic parity.
Validation target: code-review-m1-r2
Validation evidence: pending
needs-decision rationale: none

### proposal-review-r1

#### PSR-PR1-001 - Published skill effectiveness lacks a proof surface

Finding ID: PSR-PR1-001
Disposition: rejected
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Restrict repository acceptance to deterministic skill integrity, generated-package parity, release integrity, optional installer filesystem behavior, and lifecycle governance; keep semantic skill quality in human or agent review.
Rationale: Running an LLM to validate an LLM instruction file is nondeterministic, expensive, and would recreate the validation subsystem this change is intended to remove. The repository owns the instruction files and packages, not target-model interpretation. Review remains responsible for clarity, ownership, stop conditions, claims, outputs, and handoffs.
Safe resolution path: Preserve the R1 finding and owner rationale, revise the proposal to three deterministic product gates plus one governance validator, remove all target-runtime acceptance, and require proposal-review R2 to decide whether that boundary is acceptable before specification.
Validation target: proposal-review-r2
Validation evidence: `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/proposal-revision-r2.md`; `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/proposal-review-r2.md` approves the alternate resolution with no material findings
needs-decision rationale: none

### proposal-review-r2

No new findings.
R2 confirms the owner-rejected disposition of `PSR-PR1-001` is final and the proposal is accepted for downstream workflow routing.

### spec-review-r1

No new findings.
The clean review approves the feature contract and records the matching boundary-first proof map as the downstream `test-spec` condition.

### architecture-review-r1

#### PSR-AR1-001 - Deployment View omits the new execution boundary

Finding ID: PSR-AR1-001
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Chosen action: Add the approved Gate B, Gate C, conditional materialization, target-runtime exclusion, and transition behavior to the canonical Deployment View.
Rationale: The architecture method requires section 7 to carry packaging, generated-output, adapter, release, and execution-boundary changes directly.
Safe resolution path: Revise only the Deployment View and authoring evidence, then obtain architecture-review R2.
Validation target: architecture-review-r2
Validation evidence: `docs/architecture/system/architecture.md` section 7 and `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/architecture-review-r2.md`
needs-decision rationale: none

### architecture-review-r2

No new findings.
R2 confirms PSR-AR1-001 is resolved and approves the canonical architecture package and ADR for planning reliance.

### plan-review-r1

No new findings.
R1 approves the plan for test-spec authoring and requires the proof map to bind final cutover removals to per-slice replacement proof and rollback evidence.

### spec-review-r2

No new findings.
R2 approves the closed-ID and illustration-ownership correction without changing the accepted product contract or downstream design.

### test-spec-review-r1

#### PSR-TSR1-001 - Test spec cites a superseded feature-spec review

Finding ID: PSR-TSR1-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Update the input artifact identity to `spec-review-r2`, confirm proof IDs remain aligned, and request test-spec-review R2.
Rationale: Implementation must rely on the current approved governing revision.
Safe resolution path: Make the link-only identity correction, update authoring evidence, and rerun formal test-spec review.
Validation target: test-spec-review-r2
Validation evidence: `specs/published-skill-first-repository-simplification.test.md` Input artifact identities; `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/test-spec-revision-r2.md`
needs-decision rationale: none

#### PSR-TSR1-002 - MP1 is not an auditable manual-proof contract

Finding ID: PSR-TSR1-002
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Add explicit automation rationale, owner, stage, environment, steps, evidence, pass, failure, and rerun fields for MP1 without converting semantic judgment into automation.
Rationale: M2 implementation and review must know exactly how semantic-review evidence is produced and when it passes or fails.
Safe resolution path: Revise MP1 and its T3/M2 links, then rerun formal test-spec review.
Validation target: test-spec-review-r2
Validation evidence: `specs/published-skill-first-repository-simplification.test.md` MP1; `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/test-spec-revision-r2.md`
needs-decision rationale: none

### test-spec-review-r2

#### PSR-TSR2-001 - CMD18 validates stale authoring evidence

Finding ID: PSR-TSR2-001
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec revision
Chosen action: Point CMD18 at the active R2 revision evidence and request test-spec-review R3.
Rationale: Preimplementation lifecycle proof must validate the exact authoring evidence used by the reviewed test-spec entry.
Safe resolution path: Change only the CMD18 evidence operand, update revision evidence, validate, and rerun formal test-spec review.
Validation target: test-spec-review-r3
Validation evidence: `specs/published-skill-first-repository-simplification.test.md` CMD18; `docs/changes/2026-08-10-published-skill-first-repository-simplification/evidence/test-spec-revision-r2.md`
needs-decision rationale: none

### test-spec-review-r3

No new findings.
R3 confirms PSR-TSR1-001, PSR-TSR1-002, and PSR-TSR2-001 are resolved, approves the current proof map, and allows implementation handoff to M1.
