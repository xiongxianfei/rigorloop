# Proposal Review R3: Implement Skill Simplification

Review ID: proposal-review-r3
Stage: proposal-review
Round: r3
Reviewer: external proposal-review supplied by the user
Target: docs/proposals/2026-08-11-implement-skill-simplification.md
Reviewed artifact: `docs/proposals/2026-08-11-implement-skill-simplification.md`
Status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: IMPSIM-PR3, IMPSIM-PR4, IMPSIM-PR5
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-11-implement-skill-simplification/reviews/proposal-review-r3.md
- Review log: docs/changes/2026-08-11-implement-skill-simplification/review-log.md
- Review resolution: docs/changes/2026-08-11-implement-skill-simplification/review-resolution.md
- Open blockers: profile lattice, result-group applicability, and semantic-versus-literal preservation are not closed
- Immediate next stage: proposal revision

## Material Findings

### Finding IMPSIM-PR3

Finding ID: IMPSIM-PR3
Severity: major
Location: Recommended Direction; invocation-profile table; reference triggers
Evidence: The proposal makes the automation reference independently triggered while `IP2-armed` always loads both references. It does not state whether armed automation requires a current planned milestone, which evidence establishes either predicate, or how missing, stale, mismatched, or ambiguous evidence behaves. The supplied review labeled this concern `IMPSIM-PR1`; this record assigns a unique durable ID because R1 already owns that identifier.
Required outcome: Define a closed invocation-profile lattice, make the planned-to-armed relationship explicit, identify authoritative trigger evidence, and specify stop behavior for invalid combinations.
Safe resolution path: Support `IP0-isolated`, `IP1-planned`, and `IP2-planned-armed`; make armed automation valid only within a current planned milestone; bind both predicates to durable matching change and milestone evidence; stop on an unplanned-armed combination or stale, missing, mismatched, or ambiguous authority.
needs-decision rationale: The proposal-owning stage must choose the valid profile combinations and authority boundary before specification.

### Finding IMPSIM-PR4

Finding ID: IMPSIM-PR4
Severity: major
Location: Recommended Direction; implementation-result asset ownership
Evidence: One result asset serves profiles with materially different evidence, but the proposal does not define core, planned-only, and automation-only groups. This risks empty placeholders, meaningless `not applicable` values, profile-specific structures outside the asset, or policy explanations inside the asset. The supplied review labeled this concern `IMPSIM-PR2`; this record assigns a unique durable ID.
Required outcome: Define one core result group and closed planned-milestone and armed-automation structural groups while keeping applicability and policy outside the asset.
Safe resolution path: Omit inapplicable groups, forbid unfilled placeholders, keep labels and layout in the asset, and keep status meaning, applicability, claim authority, and handoff policy in `SKILL.md` or the applicable reference.
needs-decision rationale: The proposal-owning stage must choose a structural model that lets one asset serve all valid profiles without becoming a policy owner.

### Finding IMPSIM-PR5

Finding ID: IMPSIM-PR5
Severity: major
Location: Recommended Direction; Testing and Verification Strategy; compatibility inventory
Evidence: The proposal combines behaviorally significant rule disposition with literal heading and phrase dependencies. Semantic rules require preservation, while test-only incidental literals should not freeze accidental wording. The proposal lacks separate ledgers and closed classifications for these evidence classes. The supplied review labeled this concern `IMPSIM-PR3`; this record uses the next available durable ID.
Required outcome: Separate semantic-rule preservation from literal compatibility classification and prevent incidental tests from becoming prose-policy owners.
Safe resolution path: Create change-local semantic-rule and literal-compatibility ledgers with closed dispositions and classifications; preserve contract literals, migrate parser/package contracts atomically, update incidental tests, and remove obsolete literals with evidence.
needs-decision rationale: The proposal-owning stage must settle which evidence proves behavior preservation and which evidence only supports dependency migration.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Common-path overload and duplicated ownership remain concrete. |
| User value | pass | The intended context reduction is valuable for isolated and planned use. |
| Option diversity | pass | The compared structures remain materially different. |
| Decision rationale | pass | Two references remain the strongest broad direction. |
| Scope control | pass | The change remains bounded to the `implement` package and its direct proof. |
| Architecture awareness | pass | Existing package architecture likely suffices after a bounded assessment. |
| Testability | concern | Profile evidence, result applicability, and literal classification need closed contracts. |
| Risk honesty | pass | The proposal names the major package and semantic risks. |
| Rollout realism | pass | Atomic canonical and generated package handling remains sound. |
| Readiness for spec | block | IMPSIM-PR3 through IMPSIM-PR5 require proposal-level decisions. |

## Scope Preservation Review

- Scope-preservation result: pass. The new concerns refine the selected package model without expanding implementation into other skills or runtime testing.

## Recommended Proposal Edits

- Recommended edits: define a three-profile lattice with invalid unplanned automation; define core, planned, and automation result groups; separate semantic and literal ledgers; make words and UTF-8 bytes primary profile metrics; and record the likely `architecture-not-required` outcome subject to bounded assessment.

## Recommendation

- Recommendation: revise the proposal to close IMPSIM-PR3 through IMPSIM-PR5, then run a fresh proposal review. No automatic downstream handoff follows this review.
