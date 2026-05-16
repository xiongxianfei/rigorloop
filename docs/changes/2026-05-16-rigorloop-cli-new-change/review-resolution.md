# RigorLoop CLI New Change Review Resolution

## Scope

This record tracks material finding closeout for the RigorLoop CLI `new-change` scaffolding contract.

Closeout status: closed

Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: architecture-review-r1
Review closeout: plan-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1
Review closeout: code-review-m2-r2
Review closeout: code-review-m3-r1

- Reviews covered: `spec-review-r1`, `spec-review-r2`, `architecture-review-r1`, `plan-review-r1`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m3-r1`
- Findings resolved: 5
- Unresolved findings: 0
- Final result: `SR1-F1`, `SR1-F2`, `SR1-F3`, `CR1-F1`, and `CR2-F1` are resolved. `spec-review-r2` approved the revised spec with no material findings. `architecture-review-r1` approved the canonical architecture update with no material findings. `plan-review-r1` approved the execution plan with no material findings. `code-review-m1-r1` found `CR1-F1`; the M1 renderer and test coverage were updated, validation passed, and `code-review-m1-r2` closed M1. `code-review-m2-r1` found `CR2-F1`; the M2 tests were extended to directly prove the named write-plan edge cases, validation passed, and `code-review-m2-r2` closed M2 with no material findings. `code-review-m3-r1` closed M3 with no material findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
|---|---|---|---|
| SR1-F1 | accepted | resolved | The spec now defines first-slice value domains and invalid-value behavior for `--type` and `--risk`; spec-review-r2 approved the revision. |
| SR1-F2 | accepted | resolved | The spec now omits `explain-change.md` placeholders from the first slice and keeps `artifacts` empty; spec-review-r2 approved the revision. |
| SR1-F3 | accepted | resolved | The spec now defines observable partial-write failure behavior after mutation begins; spec-review-r2 approved the revision. |
| CR1-F1 | accepted | resolved | M1 renderer now emits `review.unresolved_items: 0`, and `TNC-006` asserts the field under `review`. |
| CR2-F1 | accepted | resolved | M2 tests now directly prove dry-run existing-directory planning and nested planned-directory symlink conflicts. |

## Common Resolution Metadata

- Owner: spec author
- Owning stage: spec
- Validation target: revise `specs/rigorloop-cli-new-change.md`, rerun `spec-review`, then run review artifact, change metadata, artifact lifecycle, and selected CI validation.
- Validation evidence: spec-review-r2 approved the revised spec and closed the material findings.

## Finding Details

### spec-review-r1

#### SR1-F1 - Public option value domains are underdefined

Finding ID: SR1-F1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Define `--type` as a lowercase classification token matching `[a-z][a-z0-9-]{0,63}` and `--risk` as exactly `low`, `medium`, or `high`; add field-specific invalid-value status, exit code, and error codes.
Rationale: Public command options persisted into `change.yaml` are compatibility-sensitive. Test-spec and implementation must not invent accepted values.
Validation target: Spec-review rerun confirms the option value domains and invalid-value behavior are explicit.
Validation evidence: `specs/rigorloop-cli-new-change.md` now defines `R5a` through `R5c` and `R7a` through `R7b`; spec-review-r2 approved the revision.

#### SR1-F2 - Standard-profile `explain-change.md` placeholder conflicts with durable reasoning semantics

Finding ID: SR1-F2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Simplify the first slice so both standard and minimal profiles create only `change.yaml`; do not create or map `explain-change.md` until a later template spec defines lifecycle semantics.
Rationale: `artifacts.explain_change` should not look like final durable rationale while the file content says the explain-change stage has not completed.
Validation target: Spec-review rerun confirms the placeholder or no-placeholder contract has one interpretation.
Validation evidence: `specs/rigorloop-cli-new-change.md` now forbids first-slice durable Markdown placeholders, omits `artifacts.explain_change`, and records that the absence of `explain-change.md` does not weaken workflow closeout requirements; spec-review-r2 approved the revision.

#### SR1-F3 - Partial mutation failure behavior is incomplete

Finding ID: SR1-F3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add observable partial-write failure behavior covering completed actions, failed actions, exit code, status, no success claim, and the first-slice no-atomic-rollback rule.
Rationale: `new-change` mutates multiple filesystem paths. Mutation safety requires users and agents to know what happened if a later write fails.
Validation target: Spec-review rerun confirms partial mutation failures are testable.
Validation evidence: `specs/rigorloop-cli-new-change.md` now defines `R56a` through `R56k`; spec-review-r2 approved the revision.

### spec-review-r2

No material findings; no resolution entry required. The same-stage spec-review rerun approved the revised spec and closed `SR1-F1`, `SR1-F2`, and `SR1-F3`.

### architecture-review-r1

No material findings; no resolution entry required. The architecture-review approved the canonical architecture update and found no required ADR, C4, arc42, boundary, runtime, deployment, security, or plan-readiness changes.

### plan-review-r1

No material findings; no resolution entry required. Plan-review approved the execution plan and cleared the path to test-spec.

### code-review-m1-r1

#### CR1-F1 - Generated change metadata omits required `review.unresolved_items`

Finding ID: CR1-F1
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: implement
Chosen action: Add `review.unresolved_items: 0` under the `review` section in `renderChangeMetadata`, and extend `TNC-006` to assert the deterministic `changed_files` to `review` order plus the numeric `unresolved_items: 0` field.
Rationale: `review.unresolved_items: 0` is part of the approved first-slice `change.yaml` shape. Omitting it made scaffolded metadata diverge from the public command contract.
Validation target: `npm test --prefix packages/rigorloop`, selected M1 CI, and diff check.
Validation evidence: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-006'` passed after first failing for the missing field; full validation evidence is recorded in the active plan after the fix.

### code-review-m1-r2

No material findings; no resolution entry required. The M1 code-review rerun found `CR1-F1` resolved and closed M1 with `clean-with-notes`.

### code-review-m2-r1

#### CR2-F1 - M2 tests do not directly prove all named write-plan edge cases

Finding ID: CR2-F1
Disposition: accepted
Status: resolved
Owner: implementation owner
Owning stage: implement
Chosen action: Extended `TNC-012` to run dry-run before actual scaffolding against an existing `docs/`, `docs/changes`, and change-root fixture, proving existing directories are reported as existing and unrelated files are preserved before mutation. Extended `TNC-014` into table-driven symlink coverage for `docs`, `docs/changes`, and `docs/changes/<change-id>`.
Rationale: The active test spec names these edge cases, and the code-review contract requires direct proof for named edge cases before a clean milestone review can close.
Validation target: `npm test --prefix packages/rigorloop`, selected M2 CI, and diff check after the tests are updated.
Validation evidence: `npm test --prefix packages/rigorloop -- --test-name-pattern 'TNC-012|TNC-014'` passed after the test updates. Full M2 validation evidence is recorded in the active plan.

### code-review-m2-r2

No material findings; no resolution entry required. The M2 code-review rerun found `CR2-F1` resolved and closed M2 with `clean-with-notes`.

### code-review-m3-r1

No material findings; no resolution entry required. The M3 code-review closed the final implementation milestone with `clean-with-notes`.

## Closeout Checklist

- [x] Every material finding has a final disposition.
- [x] Every accepted finding has action and rationale.
- [x] Validation evidence is recorded for each resolved finding.
- [x] `review-log.md` lists no open findings.
- [x] Closeout status is correct.
