# Release Process Contract Review Resolution

## Scope

This record tracks formal lifecycle review findings for the release process contract change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1
Review closeout: code-review-m4-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### proposal-review-r2

No material findings.

### spec-review-r1

#### REL-SR1

Finding ID: REL-SR1
Disposition: accepted
Status: resolved after spec revision
Owner: spec author
Owning stage: spec
Required outcome: Resolve the normative conflict between the hard full-gate-before-publish rule and the emergency-release deferred-gate path.
Resolution: Clarified the relationship between the default full release gate and emergency release deferrals.
Chosen action: REL-R14 now states that routine releases must pass the full release gate before publish, and that the only exception is an emergency release with owner-approved gate deferrals recorded under REL-R14a and REL-R63. Added an emergency-deferral contract requiring owner approval, rationale, deferred gate item, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage. The spec now states that release evidence creation, secret suppression, source/version/dist-tag recording, publish path recording, recovery/follow-up recording, and post-publish registry verification are non-deferrable. Updated REL-R63, emergency edge cases, and AC-REL-005 so they cite the same exception contract.
Rationale: The default gate remains hard for routine releases, while emergency release behavior is now a narrow, testable exception instead of a contradictory implied bypass.
Validation target: Rerun spec-review after spec revision and validate review artifacts.
Validation evidence: Focused validation passed after spec revision: review artifact structure, change metadata, explicit-path artifact lifecycle, and `git diff --check`.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

#### CR-M2-1

Finding ID: CR-M2-1
Disposition: accepted
Status: resolved after implementation
Owner: implementer
Owning stage: implement
Required outcome: Changing `docs/releases/v<version>.md` must select the release-evidence checklist validation path that can reject missing or unsafe evidence.
Chosen action: Updated selector routing so flat release evidence files such as `docs/releases/v1.2.3.md` select `artifact_lifecycle.validate`, the lifecycle-owned release evidence checklist route. Preserved existing release-directory routing for `docs/releases/<version>/release.yaml` and related directory artifacts. Updated selector tests so the flat release evidence case asserts `artifact_lifecycle.validate` directly.
Suggested resolution: Add selector handling for flat `docs/releases/v<version>.md` evidence files that selects `artifact_lifecycle.validate` for the evidence path, while preserving existing release-directory routing for `docs/releases/<version>/release.yaml`, release notes, and npm publication evidence. Update selector regression tests to assert the checklist route.
Rationale: M2 implemented the checklist in artifact lifecycle validation, but the selector path for release evidence selects only `release.validate`, so a changed standing evidence file bypasses the new checklist.
Validation target: Rerun `python scripts/test-select-validation.py`, `python scripts/test-artifact-lifecycle-validator.py`, targeted artifact lifecycle validation, change metadata validation, and `git diff --check`.
Validation evidence: Focused selector proof and regression validation passed after the routing fix, including `python scripts/select-validation.py --mode explicit --path docs/releases/v1.2.3.md`, `python scripts/select-validation.py --mode explicit --path docs/releases/README.md --path docs/releases/index.md`, `python scripts/select-validation.py --mode explicit --path docs/releases/v0.1.5/release.yaml`, `python scripts/test-select-validation.py`, and `python scripts/test-artifact-lifecycle-validator.py`.

### code-review-m2-r2

No material findings.

### code-review-m3-r1

No material findings.

### code-review-m4-r1

No material findings.
