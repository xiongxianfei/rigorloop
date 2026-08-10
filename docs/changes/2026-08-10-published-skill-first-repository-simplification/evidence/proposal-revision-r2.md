# Proposal revision evidence after owner refinement

Stage: proposal
Date: 2026-08-10
Outcome: review-required
Source review: proposal-review-r1
Material finding reconsidered: PSR-PR1-001

## Inputs

- Owner-provided refined design summary establishing deterministic repository ownership as the acceptance boundary.
- `docs/proposals/2026-08-10-published-skill-first-repository-simplification.md` after the first revision.
- `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/proposal-review-r1.md`.
- `docs/changes/2026-08-10-published-skill-first-repository-simplification/review-resolution.md`.
- `CONSTITUTION.md`, `VISION.md`, and the existing canonical skill, adapter, package, release, and lifecycle-governance boundaries.

## Owner decision

Repository acceptance tests only deterministic surfaces RigorLoop owns.
Semantic skill quality remains human or agent review-owned.
Codex, Claude Code, and opencode runtimes are not executed to validate published instruction files.

The owner rejected the R1 remedy that added Codex journey suites, runtime behavior evidence, and invocation smoke.
This does not erase the finding; proposal-review R2 must determine whether the revised deterministic boundary is acceptable.

## Revision

- Replaced four product gates with Gate A canonical skill integrity, Gate B all-target generated package parity, and Gate C release integrity.
- Removed Codex prompts, journeys, transcripts, behavior grading, runtime matrices, and behavioral certification from repository acceptance.
- Gave Codex, Claude Code, and opencode equivalent deterministic package proof.
- Made installer materialization testing conditional on meaningful RigorLoop-owned filesystem logic and prohibited starting target runtimes during that test.
- Added the semantic skill-review checklist as the owner for description, ownership, inputs, procedure, resources, stop conditions, claims, output, and handoff quality.
- Kept one bounded lifecycle and change-record governance validator outside the product gates.
- Added explicit script-admission defaults and a safety-preserving retirement sequence.

## Result

The proposal is ready for proposal-review R2 under the refined deterministic-ownership direction.
No specification, architecture, planning, implementation, runtime execution, release, or publication was performed.
