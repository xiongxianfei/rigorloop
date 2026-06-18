# RigorLoop Guide System Optimization and Source-of-Truth Alignment Review Resolution

## Scope

This record tracks material review finding closeout for the guide system optimization and source-of-truth alignment change.

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1

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

Review closeout: open

#### GUIDE-CR1

Finding ID: GUIDE-CR1
Disposition: needs-decision
Status: open
Owner: implementation author
Owning stage: review-resolution
Required outcome: Guide-system validation must not own an incomplete duplicate workflow-map registry contract. It must either compose/call the existing workflow-map validator for registry/table consistency or limit its own checks to guide-system ownership boundaries while ensuring the workflow-map validator remains selected where registry/table consistency is required.
Suggested resolution: Refactor `GUIDE-008` so it delegates registry/table consistency to `skill_validation.validate_workflow_artifact_map_contract` or removes partial registry-entry validation and adds selector/test coverage that runs the workflow-map validator when `docs/workflows.md` registry/table consistency is in scope. Add a regression proving a registry/table mismatch is caught by the owning workflow-map validator.
Needs-decision rationale: The implementation author must choose the allowed fix shape before code changes: compose the existing workflow-map validator from the guide-system validator, or keep the guide validator limited to guide ownership and select/run the workflow-map validator for workflow-map registry/table consistency.
Decision owner: implementation author
Decision needed: Choose whether `GUIDE-008` composes the existing workflow-map validator or whether guide-system validation stays limited to guide ownership while selector routing runs the workflow-map validator for registry/table consistency.
Stop state: M2 remains resolution-needed until the decision is made, the accepted fix is implemented, validation passes, and code-review reruns cleanly.
Validation target: Rerun guide-system validator tests, selector tests, workflow-map/skill-validator tests, guide-system validation, change metadata validation, artifact lifecycle validation for touched artifacts, and selected CI for the M2 surfaces.
Validation evidence: pending
