# Review Resolution: Installed-Skill Artifact Placement Contract

## Scope

This record tracks material review finding closeout for the installed-skill artifact placement contract change.

Closeout status: open

Review closeout: code-review-m2-r1

- Reviews covered: `code-review-m1-r1`, `code-review-m2-r1`
- Findings resolved: 1
- Unresolved findings: 1
- Final result: `code-review-m1-r1` requested changes for `SAP-M1-CR1`; that finding is resolved. `code-review-m2-r1` requested changes for `SAP-M2-CR1`; that finding remains open pending review-resolution.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SAP-M1-CR1 | accepted | resolved | M1 helper/tests now reject wrong stage-owned record-type wording and accept correct proposal-review/spec-review fixtures. |
| SAP-M2-CR1 | accepted | open | M2 plan readiness footer still points to `implement M2` after M2 handoff and must be synchronized before rerun code-review. |

## Finding Details

### code-review-m1-r1

Review closeout: closed

#### SAP-M1-CR1

Finding ID: SAP-M1-CR1
Disposition: accepted
Owner: implementation author
Owning stage: implement M1 fix
Chosen action: Update the installed-skill placement helper and tests so first-slice review skills prove the stage-owned record type as well as the default path. Correct the compliant `spec-review` fixture text and add a negative assertion for wrong stage-owned wording.
Rationale: The approved spec requires each placement block to state the artifact or record type owned by the skill. The current M1 compliant fixture accidentally proves that the helper accepts `spec-review` text that still says `proposal-review records`, so the validator scaffolding is incomplete.
Validation target: Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, lifecycle validation for touched artifacts, and `git diff --check -- ...` after the targeted M1 fix.
Validation evidence: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md`, and `git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md docs/changes/2026-05-25-installed-skill-artifact-placement-contract` passed.
Status: resolved

### code-review-m2-r1

Review closeout: open

#### SAP-M2-CR1

Finding ID: SAP-M2-CR1
Disposition: accepted
Owner: implementation author
Owning stage: implement M2 fix
Chosen action: Synchronize the active plan readiness footer with the M2 review-resolution handoff so it no longer says `Ready for implement M2` after M2 implementation has already been committed and reviewed.
Rationale: The active plan's `Current Handoff Summary` and `docs/plan.md` identify `code-review M2` as next after the M2 handoff, while the plan footer still names `implement M2`. The plan's current handoff state and readiness surfaces must not disagree during milestone-based workflow.
Validation target: Rerun lifecycle validation for the plan, plan index, change metadata, review log, review-resolution, and `code-review-m2-r1` record, plus targeted whitespace checks after the fix.
Validation evidence: pending
Status: open
