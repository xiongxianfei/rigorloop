# Review Finding Resolution Contract Review Resolution

## Scope

This record resolves material findings from formal lifecycle reviews for the review finding resolution contract change.

Closeout status: closed

## Resolution Entries

### architecture-review-r1

#### AR1

Finding ID: AR1
Disposition: accepted
Owner: implementer
Owning stage: architecture
Chosen action: Revise `docs/architecture/2026-04-24-review-finding-resolution-contract.md` before planning so `review-resolution.md` closeout fields are parseable and phase-specific.
Rationale: The approved spec requires disposition records to carry rationale, final action or stop state, required evidence, decision-owner fields for `needs-decision`, and sub-decisions for `partially-accepted`; the architecture currently defines only `Finding ID:` and `Disposition:` labels.
Validation target: Rerun architecture-review after revision and run artifact lifecycle validation on the proposal, spec, architecture, and change metadata.
Validation evidence: Architecture revision completed in `docs/architecture/2026-04-24-review-finding-resolution-contract.md`. `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `git diff --check -- specs/review-finding-resolution-contract.md docs/architecture/2026-04-24-review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract`, and ASCII/trailing-whitespace checks passed. `architecture-review-r2` approved the closeout.

#### AR2

Finding ID: AR2
Disposition: accepted
Owner: implementer
Owning stage: architecture
Chosen action: Revise `docs/architecture/2026-04-24-review-finding-resolution-contract.md` before planning so `review-log.md` has a precise parseable Review ID reference convention.
Rationale: The approved spec requires every detailed Review ID to appear exactly once in `review-log.md`, but the architecture does not yet say which log structure the validator counts.
Validation target: Rerun architecture-review after revision and run artifact lifecycle validation on the proposal, spec, architecture, and change metadata.
Validation evidence: Architecture revision completed in `docs/architecture/2026-04-24-review-finding-resolution-contract.md`. `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `git diff --check -- specs/review-finding-resolution-contract.md docs/architecture/2026-04-24-review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract`, and ASCII/trailing-whitespace checks passed. `architecture-review-r2` approved the closeout.

### architecture-review-r2

No material findings.

### spec-review-r1

#### SR1

Finding ID: SR1
Disposition: accepted
Owner: implementer
Owning stage: spec
Chosen action: Define top-level `review-resolution.md` closeout status values as exactly `open` or `closed`, and define disposition-specific conditions for a finding to count toward `closed`.
Rationale: The spec-review finding is correct. Without exact closeout states and disposition-specific closure rules, `verify`, `explain-change`, `pr`, and tests would have to infer finality.
Validation target: Rerun spec-review after spec revision and run artifact lifecycle validation on the proposal, spec, architecture, and change metadata.
Validation evidence: Spec revision completed. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, and `git diff --check -- specs/review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract` passed. `spec-review-r2` approved the closeout.

#### SR2

Finding ID: SR2
Disposition: accepted
Owner: implementer
Owning stage: spec
Chosen action: Define late repair as allowed only through a reconstructed review record labeled `Record mode: reconstructed`, with original review source, original evidence or durable link, after-fix timing disclosure, stable Finding IDs, and known loss of fidelity.
Rationale: The spec-review finding is correct. The preferred rule is record before fixes; late repair must not allow silent retroactive cleanup without durable review evidence.
Validation target: Rerun spec-review after spec revision and run artifact lifecycle validation on the proposal, spec, architecture, and change metadata.
Validation evidence: Spec revision completed. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, and `git diff --check -- specs/review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract` passed. `spec-review-r2` approved the closeout.

#### SR3

Finding ID: SR3
Disposition: accepted
Owner: implementer
Owning stage: spec
Chosen action: Define the v1 `review-log.md` canonical parseable form as a simple line-based `### Review entry` block with exact field labels.
Rationale: The spec-review finding is correct. Exact-once Review ID validation needs a contributor-visible ledger shape that does not count incidental prose mentions.
Validation target: Rerun spec-review after spec revision and run artifact lifecycle validation on the proposal, spec, architecture, and change metadata.
Validation evidence: Spec revision completed. `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-24-review-finding-resolution-contract.md --path specs/review-finding-resolution-contract.md --path docs/architecture/2026-04-24-review-finding-resolution-contract.md --path docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, and `git diff --check -- specs/review-finding-resolution-contract.md docs/changes/2026-04-24-review-finding-resolution-contract` passed. `spec-review-r2` approved the closeout.

### spec-review-r2

No material findings.

### code-review-r1

Review closeout: code-review-r1

#### CR1-F1

Finding ID: CR1-F1
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Require same-stage non-blocking rerun evidence to have a strictly later round than the original blocking review.
Rationale: The code-review finding is correct. A same-stage, same-round non-blocking review is not a rerun and must not satisfy `R8f`.
Validation target: Add a regression test where `Round: 1` followed by approved `Round: 1` fails closeout, then run the review artifact validator tests and closeout validation.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed after the regression test failed red before the production fix. `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract` is the closeout proof target for the updated artifact state.

### code-review-r2

Review closeout: code-review-r2

#### CR2-F1

Finding ID: CR2-F1
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Update `specs/rigorloop-workflow.md` `R12ab` so material review findings MUST be recorded before review-driven fixes begin.
Rationale: The code-review finding is correct. The approved feature spec requires pre-fix recording with a reconstructed-record recovery path, and the general workflow contract must not weaken that requirement.
Validation target: Run focused review-artifact validation, change metadata validation, artifact lifecycle explicit-path validation, and diff whitespace checks after the wording fix and artifact closeout updates.
Validation evidence: `specs/rigorloop-workflow.md` `R12ab` now uses MUST for pre-fix material finding recording. `python scripts/test-review-artifact-validator.py`, `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-04-24-review-finding-resolution-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, and `git diff --check -- specs docs skills .codex/skills dist AGENTS.md CONSTITUTION.md scripts` passed after the fix.

### code-review-r3

Review closeout: code-review-r3

#### CR3-F1

Finding ID: CR3-F1
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Update closeout validation so a closed handoff fails when any review-log entry still lists open findings.
Rationale: The code-review finding is correct. A closed review-resolution state and a non-empty review-log open-finding set conflict, and downstream handoff must not proceed with that stale ledger state.
Validation target: Add focused validator coverage for stale open findings in closeout mode, then run review-artifact tests and closeout validation.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed after adding a regression where `Closeout status: closed` plus stale `Open findings:` fails closeout mode. `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract` passed for the updated artifact state.

#### CR3-F2

Finding ID: CR3-F2
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Validate review-log `Resolution:` fields as canonical `review-resolution.md#<Review ID>` references and check the referenced Review ID when `review-resolution.md` exists.
Rationale: The code-review finding is correct. The parser stored `Resolution:` without validating the symbolic link, which allowed stale or malformed ledger references.
Validation target: Add focused validator coverage for malformed resolution target, mismatched anchor, duplicate `Resolution:` fields, and missing review-resolution Review ID headings, then run review-artifact tests and closeout validation.
Validation evidence: `python scripts/test-review-artifact-validator.py` passed after adding regressions for malformed `Resolution:` target, mismatched anchor, duplicate `Resolution:` field, and missing review-resolution Review ID heading. `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-04-24-review-finding-resolution-contract` passed for the updated artifact state.

#### CR3-F3

Finding ID: CR3-F3
Disposition: rejected
Owner: maintainer
Owning stage: code-review
Stop state: no implementation change required
Rationale: The maintainer explicitly rejected the heavier CI changed-root integration test for v1 because the repository already has substantial review-artifact validator coverage and the additional test would add more weight than value for this patch.
Expected proof: The focused CR3-F1 and CR3-F2 regressions pass, while the existing CI coverage remains unchanged.
