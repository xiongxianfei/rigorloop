# RigorLoop Guide System Optimization and Source-of-Truth Alignment Review Resolution

## Scope

This record tracks material review finding closeout for the guide system optimization and source-of-truth alignment change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2

## Resolution Entries

### proposal-review-r1

No material findings remain open.

### spec-review-r1

No material findings.

### spec-review-r2

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

Review closeout: closed

#### GUIDE-CR1

Finding ID: GUIDE-CR1
Disposition: accepted
Status: resolved
Owner: implementation author
Owning stage: review-resolution
Required outcome: Guide-system validation must not own an incomplete duplicate workflow-map registry contract. It must either compose/call the existing workflow-map validator for registry/table consistency or limit its own checks to guide-system ownership boundaries while ensuring the workflow-map validator remains selected where registry/table consistency is required.
Chosen action: Refactored `scripts/validate-guide-system.py` so `GUIDE-008` composes `skill_validation.validate_workflow_artifact_map_contract` instead of carrying a partial guide-owned list of workflow-map registry entries. Added guide-system validator coverage proving a registry/table mismatch fails through a `workflow map contract failed` diagnostic and static coverage preventing a guide-owned required-entry list from returning. Added selector coverage documenting that `docs/workflows.md` changes select the composed guide-system validator.
Rationale: This preserves the approved ownership boundary. Guide-system validation still owns guide links, guide ownership, project-map scope, plan-index boundary, learn-session non-authority, stage-skill drift, and duplicate registry placement outside `docs/workflows.md`; workflow-map registry/table semantics remain owned by the existing workflow-map validator.
Validation target: Rerun guide-system validator tests, selector tests, workflow-map/skill-validator tests, guide-system validation, change metadata validation, artifact lifecycle validation for touched artifacts, and selected CI for the M2 surfaces.
Validation evidence: `python scripts/test-guide-system-validator.py`, `python scripts/validate-guide-system.py`, `python scripts/test-select-validation.py`, `python scripts/test-skill-validator.py -k workflow`, and `python scripts/test-skill-validator.py` passed after the fix. Final lifecycle and selected CI evidence is recorded in `change.yaml`.

### code-review-m2-r2

No material findings. `GUIDE-CR1` remains resolved and M2 is closed after clean rerun.
