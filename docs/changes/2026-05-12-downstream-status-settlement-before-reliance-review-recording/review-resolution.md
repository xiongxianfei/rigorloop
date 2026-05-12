# Downstream Status Settlement Before Reliance Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the downstream status settlement before reliance change.

Closeout status: closed

## Resolution Entries

### spec-review-r1

Review closeout: spec-review-r1

#### SR-001

Finding ID: SR-001
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: spec
Chosen action: Clarified the settlement output contract so blocked settlement reports a deterministic target status when known, or `not-applicable` when no deterministic target status can be selected. Added requirements for `New status` semantics and blocked-settlement blocker detail.
Rationale: The current spec requires a `New status` field for every reported settlement block, but blocked settlement can occur exactly because no deterministic new status exists.
Validation target: Update `specs/downstream-status-settlement-before-reliance.md` and rerun spec-review.
Validation evidence: `specs/downstream-status-settlement-before-reliance.md` now defines `R17a`, `R23a`-`R23d`, and `R24a`; examples and edge cases cover known-target and unknown-target blocked settlement.

### spec-review-r2

No material findings.

### code-review-r1

Review closeout: code-review-r1

#### CR-001

Finding ID: CR-001
Disposition: accepted
Status: resolved
Owner: implementer
Owning stage: implement
Chosen action: Updated the first-slice upstream status settlement guidance in `skills/spec/SKILL.md`, `skills/architecture/SKILL.md`, and `skills/plan/SKILL.md` to explicitly cover the no-edit-question rule, unknown artifact/lifecycle/target blockers, known-target blocked `New status`, unknown-target `New status: not-applicable`, and blocker distinction. Tightened `scripts/test-skill-validator.py` to assert those semantics for all first-slice skills.
Rationale: The finding identifies missing direct static proof and missing skill guidance for approved blocked-settlement and edit-permission semantics in M1.
Validation target: Update first-slice skill guidance and `scripts/test-skill-validator.py`, then rerun M1 validation and code-review.
Validation evidence: `python scripts/test-skill-validator.py` and `python scripts/validate-skills.py` passed after the fix.
