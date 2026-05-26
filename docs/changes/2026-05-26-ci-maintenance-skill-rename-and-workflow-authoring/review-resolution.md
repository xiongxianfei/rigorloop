# Review Resolution: CI-Maintenance Skill Rename and Workflow Authoring

## Scope

This record tracks material review finding closeout for the CI-maintenance skill rename and workflow authoring proposal.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m2-r1
Review closeout: code-review-m3-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `spec-review-r1`, `spec-review-r2`, `plan-review-r1`, `code-review-m1-r1`, `code-review-m2-r1`, `code-review-m3-r1`
- Findings resolved: 6
- Unresolved findings: 0
- Final result: `proposal-review-r1` requested changes for `CIM-PR1`, `CIM-PR2`, and `CIM-PR3`; the proposal was revised to resolve those findings. `proposal-review-r2` approved the proposal with non-blocking observations for spec. `spec-review-r1` requested changes for `CIM-SR1`, `CIM-SR2`, and `CIM-SR3`; the spec was revised to resolve those findings. `spec-review-r2` approved the revised spec with no material findings. `plan-review-r1` approved the execution plan with no material findings. `code-review-m1-r1` approved M1 with no material findings. `code-review-m2-r1` approved M2 with no material findings. `code-review-m3-r1` approved M3 with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| CIM-PR1 | accepted | resolved | Added an explicit compatibility alias decision forbidding duplicate active installed `ci` and `ci-maintenance` skill bodies. |
| CIM-PR2 | accepted | resolved | Added the command ownership boundary and test criteria for blocking when validation commands are missing. |
| CIM-PR3 | accepted | resolved | Split the risk map into portable core guidance and project-specific extensions. |
| CIM-SR1 | accepted | resolved | Added frontmatter metadata requirements and acceptance criteria for `version` and `schema-version`. |
| CIM-SR2 | accepted | resolved | Updated `Next artifacts` to route through architecture assessment, plan, and plan-review before test-spec. |
| CIM-SR3 | accepted | resolved | Replaced contradictory permissions wording with least-privilege default plus justified job-specific elevation. |

## Resolution Entries

### proposal-review-r1

#### CIM-PR1 - Compatibility alias policy must be resolved before spec

Finding ID: CIM-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Compatibility alias decision`, making `ci-maintenance` the canonical installed skill, forbidding duplicate active `ci/` and `ci-maintenance/` skill directories, allowing `ci` only as a non-duplicating alias when a safe alias mechanism exists, and requiring hard-rename release-note migration guidance otherwise.
Rationale: Skill names are routing identifiers. The proposal needed a testable no-duplicate policy before spec could encode generated adapter behavior.
Validation target: Proposal text includes the compatibility alias decision and acceptance criteria `AC-CIM-013` through `AC-CIM-015`.
Validation evidence: `proposal-review-r2` approved the revised proposal with no material findings; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md` passed after revision.

#### CIM-PR2 - Command ownership boundary must be explicit

Finding ID: CIM-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Command ownership boundary`, listing allowed validation command sources and stating that missing command sources produce a blocker instead of invented commands. Added acceptance criteria `AC-CIM-016` through `AC-CIM-018`.
Rationale: `ci-maintenance` authors or reviews CI infrastructure; it should not design tests, invent validation commands, execute validation, or claim readiness.
Validation target: Proposal text states the boundary and adds tests for missing command-source blockers.
Validation evidence: `proposal-review-r2` approved the revised proposal with no material findings; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md` passed after revision.

#### CIM-PR3 - Risk-to-check map needs a portable/public boundary

Finding ID: CIM-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Added `Risk-map portability boundary`, split the risk-to-check map into `Portable core` and `Project-specific extensions`, and labeled RigorLoop-specific rows as examples. Added acceptance criteria `AC-CIM-019` through `AC-CIM-021`.
Rationale: The public `ci-maintenance` skill should work in non-RigorLoop repositories and should not present RigorLoop-specific surfaces as universal requirements.
Validation target: Proposal text separates portable and project-specific rows and includes portability acceptance criteria.
Validation evidence: `proposal-review-r2` approved the revised proposal with no material findings; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring.md` passed after revision.

### proposal-review-r2

No material findings.

### proposal-review-r3

No material findings.

### spec-review-r1

Review closeout: closed

#### CIM-SR1 - Normalized frontmatter metadata is missing

Finding ID: CIM-SR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Added `CIM-R3a` requiring `name: ci-maintenance`, `version`, and `schema-version` frontmatter metadata, with first-slice expected schema version `skill-readability-v1` unless the published-skill contract names a newer reviewed schema before implementation. Added `AC-CIM-FM-001` through `AC-CIM-FM-004`.
Rationale: The renamed published skill needs the normalized frontmatter metadata required by the skill contract.
Validation target: Rerun artifact lifecycle validation, change metadata validation, review artifact structure validation, whitespace checks, and spec-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring`, and no-index whitespace checks passed after the spec revision. Rerun spec-review remains required before downstream reliance.

### spec-review-r2

Review closeout: closed

No material findings. Clean rerun approval is recorded in `reviews/spec-review-r2.md`.

### plan-review-r1

Review closeout: closed

No material findings. Clean plan-review approval is recorded in `reviews/plan-review-r1.md`.

### code-review-m1-r1

Review closeout: closed

No material findings. Clean M1 code-review approval is recorded in `reviews/code-review-m1-r1.md`. M1 is closed and the next implementation stage is M2 - Validator and Fixture Coverage.

### code-review-m2-r1

Review closeout: closed

No material findings. Clean M2 code-review approval is recorded in `reviews/code-review-m2-r1.md`. M2 is closed and the next implementation stage is M3 - Generated Adapter Proof and Migration Evidence.

### code-review-m3-r1

Review closeout: closed

No material findings. Clean M3 code-review approval is recorded in `reviews/code-review-m3-r1.md`. M3 is closed and all in-scope implementation milestones are complete. The next stage is final closeout; no review-resolution is required.

#### CIM-SR2 - Downstream artifact sequence skips plan before test-spec

Finding ID: CIM-SR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Updated `Next artifacts` so the sequence is `spec-review`, `architecture` and `architecture-review` if required, `plan`, `plan-review`, `test-spec`, `implementation`, `code-review`, `review-resolution` when triggered, `explain-change`, `verify`, and `pr`. Added architecture-skip rationale guidance and `AC-CIM-SEQ-001` through `AC-CIM-SEQ-004`.
Rationale: The spec's next-artifact sequence must match the repository workflow contract before downstream stages rely on it.
Validation target: Rerun artifact lifecycle validation, change metadata validation, review artifact structure validation, whitespace checks, and spec-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring`, and no-index whitespace checks passed after the spec revision. Rerun spec-review remains required before downstream reliance.

#### CIM-SR3 - Permissions elevation wording is contradictory

Finding ID: CIM-SR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec revision
Chosen action: Rewrote `CIM-R37` to require least-privilege permissions, `permissions: contents: read` for generic read-only CI, and named rationale for additional or broader job-specific permissions. Added `CIM-R37a`, `CIM-R37b`, and `AC-CIM-PERM-001` through `AC-CIM-PERM-004`.
Rationale: The permissions requirement must avoid contradictory language before tests and implementation encode it.
Validation target: Rerun artifact lifecycle validation, change metadata validation, review artifact structure validation, whitespace checks, and spec-review.
Validation evidence: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`, `python scripts/validate-change-metadata.py docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring/change.yaml`, `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-26-ci-maintenance-skill-rename-and-workflow-authoring`, and no-index whitespace checks passed after the spec revision. Rerun spec-review remains required before downstream reliance.
