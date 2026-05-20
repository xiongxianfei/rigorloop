# Explain Change: Spec and Test-Spec Structural Hygiene

## Summary

This change makes the skill-contract spec and matching test spec easier to navigate by grouping existing contract surfaces by slice. It adds a proposal, a growth-strategy rule, a spec navigation index, slice headers in the spec Requirements and Acceptance criteria sections, and matching slice headers in the test-spec coverage maps and Test cases section.

The change is navigation-only. It preserves existing R-clause IDs, R-clause text, acceptance-criterion text, test-case IDs, test-case bodies, coverage rows, validator behavior, skills, adapters, and build scripts.

## Problem

`specs/skill-contract.md` and `specs/skill-contract.test.md` had grown large enough that a reader landing on a clause, criterion, or test case had to infer its slice from surrounding context and parent proposals. The accepted proposal identifies this as a navigability problem rather than a correctness problem.

The intended behavior after this change is that a reader can locate the Foundational, Baseline normalization first slice, Published-skill design pilot, and Assets-first plan pilot surfaces directly from headings while downstream references continue to rely on unchanged stable IDs.

## Decision Trail

| Stage | Decision or artifact | Effect on this change |
|---|---|---|
| Proposal | `docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md` | Chose proposal-first structural hygiene and paired spec/test-spec restructuring in one change. |
| Proposal-review | `proposal-review-r1` | Approved the direction with no material findings. |
| Spec | `specs/skill-contract.md` | Added the structural-hygiene contract, growth strategy, navigation index, and slice grouping rules. |
| Spec-review | `spec-review-r1` | Approved the draft spec amendment with no material findings. |
| Architecture | Not created | The change is documentation structure only; no runtime behavior, data flow, persistence, deployment, or security boundary changed. |
| Plan | `docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md` | Scoped one implementation milestone for the remaining test-spec grouping work. |
| Plan-review | `plan-review-r1` | Approved the execution plan with no material findings. |
| Test-spec | `specs/skill-contract.test.md` | Mirrored the spec grouping in proof surfaces without adding executable tests. |
| Implement | M1 | Grouped the test-spec coverage maps and test cases by slice and updated lifecycle state. |
| Code-review | `code-review-m1-r1`, `code-review-m1-r2` | Found and closed `CR-M1-001`; M1 then passed clean re-review. |

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Evidence |
|---|---|---|---|---|
| `docs/proposals/2026-05-19-spec-and-test-spec-structural-hygiene.md` | Recorded the navigation-only proposal, options, risks, rollout, and non-goals. | The repository workflow requires proposal-stage direction before amending the contract. | Proposal workflow; accepted proposal. | `proposal-review-r1` approved with no material findings. |
| `specs/skill-contract.md` | Added the related proposal link, structural hygiene context, `Spec growth strategy`, and `Spec navigation`. | Future amendments need an explicit navigation and growth rule, not an implicit convention. | Accepted proposal goals and recommended direction. | Spec-review approved with no material findings. |
| `specs/skill-contract.md` | Added slice headers to Requirements for R1-R7, R8-R26, R27-R36, and R37-R45. | Readers can locate each R-clause band by slice without scanning the full flat section. | Spec navigation table and Slice terminology bands. | R-clause preservation check passed. |
| `specs/skill-contract.md` | Added slice headers to Acceptance criteria and corrected three baseline criteria into the baseline group. | The spec and test spec must describe the same structural grouping. | `CR-M1-001`; accepted review resolution. | Acceptance-criterion text preservation passed after resolution. |
| `specs/skill-contract.test.md` | Grouped Requirement coverage map, Acceptance criteria coverage map, and Test cases under the four slice headers. | The test spec needed to mirror the approved spec grouping while preserving proof content. | Active plan M1 and amended test spec. | Coverage-row, heading, and body preservation checks passed. |
| `docs/plans/2026-05-19-spec-and-test-spec-structural-hygiene.md` and `docs/plan.md` | Tracked stage state from planning through M1 closeout and now hand off to `verify`. | Planned initiatives keep current milestone, review status, and next stage in the active plan and plan index. | AGENTS.md planning rules and active plan policy. | Lifecycle validation passed through M1 and review-resolution. |
| `docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/` | Added change metadata, review log, review records, review resolution, and this explanation. | The workflow requires durable evidence for formal reviews and material finding closeout. | Change-local artifact pack policy. | Change metadata and review artifact validators passed before this explain-change stage. |

## Tests Added Or Changed

No executable tests were added or changed. That is intentional because the change does not alter validator behavior, skill behavior, adapter output, or build logic.

The proof surface changed in `specs/skill-contract.test.md`: existing coverage maps and test-case sections were grouped by slice. Existing coverage rows, test-case IDs, and test-case body text were preserved.

## Validation Evidence Available Before Final Verify

The following evidence is available before the final `verify` gate:

- R-clause preservation check: passed.
- Spec acceptance-criterion preservation check: passed before and after `CR-M1-001` resolution.
- Example ID preservation check: passed.
- Test-spec Requirement coverage row preservation check: passed.
- Test-spec Acceptance criteria coverage row preservation check: passed.
- Test-case heading preservation check: passed.
- Test-case body preservation check: passed.
- `git diff --check`: passed during spec, test-spec, implementation, and review-resolution stages.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`: passed during spec, test-spec, implementation, and review-resolution stages.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/change.yaml`: passed during test-spec, implementation, and review-resolution stages.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene`: passed during test-spec, implementation, and review-resolution stages.
- `python scripts/validate-skills.py`: passed after the spec amendment.
- `python scripts/test-skill-validator.py`: passed after the spec amendment.

Hosted CI has not been claimed by this explain-change stage. Final local verification remains owned by `verify`.

## Review Resolution Summary

One material code-review finding was recorded: `CR-M1-001`.

Disposition: accepted. Status: resolved. The fix moved three baseline normalization acceptance criteria from the Foundational acceptance-criteria group to the Baseline normalization first slice group in `specs/skill-contract.md`, preserving exact criterion text. `code-review-m1-r2` then closed M1 with no material findings.

Durable closeout is recorded in `docs/changes/2026-05-19-spec-and-test-spec-structural-hygiene/review-resolution.md`.

## Alternatives Rejected

- Direct implementation without a proposal was rejected because it would bypass the amendment workflow for a contract-level change.
- Plan-only execution was rejected because planning should execute settled direction, not create it.
- Splitting the spec and test spec into multiple files was rejected as premature; the current ownership boundary remains clear.
- Content cleanup during structural hygiene was rejected because the proposal's invariant is navigation without content changes.
- Grouping the Examples section was rejected for this slice because some examples are cross-cutting; the navigation table lists relevant examples instead.
- Validator, skill, adapter, and build-script changes were rejected because no runtime behavior changed.

## Scope Control

The diff stays inside governance, spec, test-spec, plan, and change-local evidence files. It does not modify authored skills, generated adapter output, validator logic, build scripts, schemas, or release artifacts.

The preserved-content invariant remains: every R-clause keeps its number and text, every acceptance criterion keeps its text, every test case keeps its ID and body, and cross-references continue to resolve by stable IDs.

## Risks And Follow-Ups

Residual risk is future drift: a later amendment could add a slice without updating the navigation table or grouping headers. The new growth-strategy and structural-hygiene rules make that drift reviewable.

Follow-up candidates remain those named by the accepted proposal: move operational detail out of the spec where appropriate, apply structural-fingerprint discipline to specs, extend slice grouping to other large specs, split the skill contract only if ownership pain develops, and consider a closed-enum verb set for specs.

## Current Handoff

M1 is closed after clean code-review rerun. This explain-change records the rationale needed before final verification. The next workflow stage is `verify`; branch readiness, PR readiness, and hosted CI status are not claimed here.
