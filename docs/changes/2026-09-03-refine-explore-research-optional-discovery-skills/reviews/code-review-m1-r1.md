# Code Review M1 R1: Canonical optional discovery packages

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: commit e56aa50f
Reviewed artifact: M1 implementation commit e56aa50f
Reviewed milestone: M1
Review date: 2026-09-03
Status: changes-requested
Review status: changes-requested
Material findings: ER-M1-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-m1-r1.md`, `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-log.md`, and `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-resolution.md`
- Open blockers: ER-M1-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: ER-M1-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-log.md`
- Review resolution: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3
- Required review-resolution: yes
- Finding IDs: ER-M1-CR1
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `e56aa50f` against its first parent, bounded to M1 implementation files after separating the accompanying Proposal, Design, Delivery, and lifecycle evidence.
- Approved Design package: `design-review-r2`, exact architecture and specification members current with granted authority.
- Approved Delivery package: `delivery-review-r1`, exact primary plan current with granted authority.
- Current milestone: M1 in `review-requested`; M2 and M3 remain planned.
- Implementation evidence: `docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/evidence/m1-canonical-discovery-packages.md`.
- Validation evidence: six focused tests, 358 full skill-validator tests, canonical validation, temporary generated-skill validation, and whitespace validation.

## Actual-diff summary

M1 replaces the old fixed-quota Explore and inline-capable Research instructions with normalized optional support contracts, adds standalone artifact assets and conditional methods, admits and copies one shared discovery-support policy, and extends canonical validation with drift and unknown-consumer checks. Route and broad workflow documentation remain intentionally deferred to M2; adapter distribution remains M3.

## Finding ER-M1-CR1

Finding ID: ER-M1-CR1
Severity: minor
Location: `skills/explore/assets/exploration-skeleton.md:4`; `skills/research/assets/research-skeleton.md:4`
Evidence: Both packaged assets contain `Maintained alongside: skills/<skill>/SKILL.md`. These comments ship inside installed public skill packages and expose the repository-maintainer canonical source path. ER-R34 and the approved architecture require shipped skill text to omit canonical source paths and maintainer-only shared-copy or adapter mechanics. Existing generic self-containment validation scans normalized `SKILL.md` bodies but does not scan these two new assets, so all reported M1 validation passed despite the violation.
Required outcome: Remove the maintainer-only canonical source comments from both packaged discovery assets and add direct regression proof that all files shipped by Explore and Research exclude the prohibited maintainer-path and packaging-mechanics patterns.
Safe resolution path: Accept ER-M1-CR1 in Review Resolution, route the same M1 milestone to Implementation, add a package-wide public-text hygiene test first, remove only the two comments, rerun every M1 command, update implementation evidence, and return M1 for a new Code Review round.
needs-decision rationale: none; the approved specification and architecture already require public-text hygiene.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | ER-M1-CR1 violates ER-R34; the remaining M1 contract matches ER-R1-ER-R22, ER-R27-ER-R33, and ER-R37-ER-R38. |
| Test coverage | concern | Contract, shared-copy drift, unknown consumer, package presence, proportional Explore, and standalone Research are covered; package-wide public-text scanning is missing. |
| Edge cases | pass | The skills directly cover absent and exact-revision targets, collision, ambiguity, escape, resource failure, unavailable evidence, contradiction, scope expansion, and owner judgment. |
| Error handling | pass | Failed support operations grant no completion or downstream authority and preserve unrelated artifacts. |
| Architecture boundaries | pass | The common policy, self-contained packages, local resources, progressive loading, and owner handoff match the approved architecture. |
| Compatibility | pass | Public skill names and historical artifacts remain unchanged; current behavior moves to proportional and standalone contracts. |
| Security/privacy | pass | The contracts forbid secrets, credentials, unnecessary private raw input, and machine-local absolute paths. |
| Derived artifact currency | pass | `build-skills.py --check` proves the local generated candidate; public adapters remain allocated to M3. |
| Unrelated changes | pass | M1 implementation files stay within the approved canonical package and validator slice. |
| Validation evidence | concern | All named M1 commands pass, but they miss the exact ER-R34 asset leakage identified above. |

## No automatic downstream handoff

M1 remains open. ER-M1-CR1 must be dispositioned and corrected before rereview; M2 must not start until the same milestone receives a clean Code Review and route-owned closeout.
