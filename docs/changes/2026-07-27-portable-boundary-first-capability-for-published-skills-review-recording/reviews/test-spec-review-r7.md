# Boundary-First Test Spec Review R7

Review ID: test-spec-review-r7
Stage: test-spec-review
Round: 7
Reviewer: independent Codex test-spec reviewer
Target: `specs/boundary-first-proof-model.test.md`
Reviewed artifact: commit c631da01
Review date: 2026-07-28
Recording status: recorded
Status: blocked
Review status: blocked
Material findings: PBF-TSR7-1
Immediate next stage: plan revision
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: blocked
- Material findings: PBF-TSR7-1
- Recording status: recorded
- Open blockers: pinned M4 plan contradicts the corrected proof population
- Immediate next stage: plan revision

## Packet integrity and independence

The reviewer used the exact R7 packet and excluded both the later invocation
commit and uncommitted M4 implementation. All pinned identities matched.

## Finding

### PBF-TSR7-1

Finding ID: PBF-TSR7-1
Severity: high
Location: `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md`, M4 deliverables
Evidence: The corrected test spec covers every adapter-included governed
target/skill combination, but the M4 plan still requires all ten governed
skills on every target even though the existing adapter portability decision
publishes `workflow` only for Codex.
Required outcome: Use the adapter-applicable proof population in the M4 plan
and name existing adapter portability evaluation as the exclusion owner.
Safe resolution path: Require archive and clean-install proof for every
governed skill included by each adapter, inspect all three target trees, and
retain CMD9 ownership of inclusion/exclusion validity.
needs-decision rationale: none

## Test-spec assessment

The amended test spec itself preserves PBF-R046 through PBF-R048: all ten
canonical projections remain required, while package and installed parity
applies to surfaces selected by the independently owned adapter-support
decision.
