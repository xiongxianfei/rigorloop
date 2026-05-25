# Review Resolution: Installed-Skill Artifact Placement Contract

## Scope

This record tracks material review finding closeout for the installed-skill artifact placement contract change.

Closeout status: open

Review closeout: code-review-m1-r1

- Reviews covered: `code-review-m1-r1`
- Findings resolved: 0
- Unresolved findings: 1
- Final result: `code-review-m1-r1` requested changes for `SAP-M1-CR1`. M1 remains in `resolution-needed` until the finding is resolved and code-review reruns.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SAP-M1-CR1 | accepted | unresolved | The M1 helper/tests must reject wrong stage-owned record-type wording before M1 can close. |

## Finding Details

### code-review-m1-r1

Review closeout: open

#### SAP-M1-CR1

Finding ID: SAP-M1-CR1
Disposition: accepted
Owner: implementation author
Owning stage: implement M1 fix
Chosen action: Update the installed-skill placement helper and tests so first-slice review skills prove the stage-owned record type as well as the default path. Correct the compliant `spec-review` fixture text and add a negative assertion for wrong stage-owned wording.
Rationale: The approved spec requires each placement block to state the artifact or record type owned by the skill. The current M1 compliant fixture accidentally proves that the helper accepts `spec-review` text that still says `proposal-review records`, so the validator scaffolding is incomplete.
Validation target: Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, lifecycle validation for touched artifacts, and `git diff --check -- ...` after the targeted M1 fix.
Validation evidence: pending
Status: unresolved
