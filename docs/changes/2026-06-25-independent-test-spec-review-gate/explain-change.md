# Explain Change: Independent Test-Spec-Review Gate

## Summary

This change adds an independent `test-spec-review` gate between `test-spec` and `implement`. The gate reviews whether an active test spec is an adequate, executable, and traceable proof map before implementation relies on it.

The test-spec artifact state remains `active`; approval is recorded separately in formal review evidence. Downstream `code-review` and `verify` remain required backstops.

## Problem

The approved proposal identified an ownership gap: `plan-review` happens before the test spec exists, while `code-review` and `verify` happen after implementation has already relied on the test spec. A weak proof map could therefore shape code, tests, milestone closeout, and validation evidence before any independent adequacy review.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Add a dedicated `test-spec-review` gate and keep test specs `active`. |
| Spec | Requirements R1-R28 define workflow order, review enums, implementation handoff, staleness, review records, skill boundaries, and adapter inclusion. |
| Architecture/ADR | Use the existing review-family pattern; no new review engine, service, or ADR-level mechanism beyond the accepted stage and packaging changes. |
| Plan | M1 updated workflow and validator contracts; M2 added the canonical skill/assets and adjacent routing; M3 added lifecycle/generated package proof. |
| Test spec | T1-T15 map workflow order, result validation, review placement, proof adequacy, staleness, skill routing, generated adapters, and lifecycle validation. |

## Diff Rationale By Area

| Area | Files | Why changed | Source / evidence |
| --- | --- | --- | --- |
| Workflow contract | `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`, `docs/workflows.md`, `AGENTS.md` | Insert `test-spec-review` between `test-spec` and `implement`; preserve active test-spec status; define implementation eligibility and staleness expectations. | R1-R4, R19-R23; M1; `code-review-r1`. |
| Feature contract | `specs/test-spec-review-gate.md`, `specs/test-spec-review-gate.test.md` | Record the approved requirements, examples, edge cases, acceptance criteria, and proof plan for the new gate. | Proposal-review, spec-review, architecture-review, plan-review records. |
| Architecture records | `docs/architecture/...`, `docs/adr/...` | Document that the established review-family pattern is sufficient and that generated adapter/package surfaces are affected. | Architecture-review R1. |
| Canonical skill | `skills/test-spec-review/SKILL.md`, `skills/test-spec-review/assets/*` | Add the public skill, result skeleton, and material-finding asset for independent proof-map adequacy review. | R13-R24; M2; `code-review-r2`. |
| Adjacent skill routing | `skills/test-spec/SKILL.md`, `skills/implement/SKILL.md`, `skills/workflow/SKILL.md` | Route formal test-spec output to review, require approved current review before implementation, and expose the new stage in workflow guidance. | R25-R26; T10; skill-validator evidence. |
| Review validators | `scripts/review_artifact_validation.py`, `scripts/test-review-artifact-validator.py` | Recognize `test-spec-review`, enforce closed enums, status/handoff mapping, next-stage combinations, and formal record placement. | R5-R12, R22-R23, R27; T3-T6. |
| Skill validators | `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | Include review-family assets for the new skill and prove adjacent routing/claim boundaries. | R24-R26; T10. |
| Lifecycle sync | `scripts/lifecycle_state_sync.py`, `scripts/test-artifact-lifecycle-validator.py` | Accept `test-spec-review` as a formal review stage in workflow-state handoffs. | R1-R2, R21; T1-T2, T9. |
| Adapter packaging | `dist/adapters/manifest.yaml`, `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, `docs/releases/v0.1.5/release.yaml` | Package `test-spec-review` for supported adapters and keep v-prefixed adapter alias handling/release validation coherent. | R28; T11; full adapter distribution suite. |
| Change evidence | `docs/changes/...`, `docs/plans/...`, `docs/plan.md` | Record proposal/spec/architecture/plan reviews, implementation reviews, validation evidence, behavior preservation, and current handoff state. | Workflow recording contract; `code-review-r1` through `code-review-r3`. |

## Tests Added Or Changed

- `scripts/test-review-artifact-validator.py`: added `test-spec-review` result fixtures, unknown-value regression cases, and invalid status/handoff/next-stage combinations.
- `scripts/test-skill-validator.py`: added workflow baseline and canonical skill/asset/adjacent-routing checks for `test-spec-review`.
- `scripts/test-artifact-lifecycle-validator.py`: added a workflow-state fixture proving `stage=test-spec-review` is accepted in review-requested state.
- `scripts/test-adapter-distribution.py`: added a v-prefixed release regression proving `v0.1.5` manifests include OpenCode command aliases when the canonical alias skills are present.
- `specs/rigorloop-workflow.test.md` and `specs/test-spec-review-gate.test.md`: record the contract-level proof map for workflow order, status separation, staleness, review records, and generated adapter proof.

## Validation Evidence Before Final Verify

Recorded passing validation includes:

- `python scripts/test-review-artifact-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version v0.1.5 --check`
- `python scripts/validate-adapters.py --version v0.1.5`
- `python scripts/validate-release-ci.py --version v0.1.5`
- `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-test-spec-review-gate/change.yaml`
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-test-spec-review-gate`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- scoped `git diff --check` commands

No hosted CI status is claimed here.

## Review Summary

Formal review records:

- `proposal-review-r1`: approved, no material findings.
- `spec-review-r1`: approved, no material findings.
- `architecture-review-r1`: approved, no material findings.
- `plan-review-r1` and `plan-review-r2`: approved, no material findings.
- `code-review-r1`, `code-review-r2`, `code-review-r3`: clean-with-notes, no material findings.

No `review-resolution.md` was required because no material findings were recorded.

## Alternatives Rejected

- Put approval into the test-spec artifact state: rejected because it would confuse active proof-map state with independent review status.
- Fold the gate into `plan-review`: rejected because the test spec does not exist during plan review.
- Let `implement` self-approve the test spec: rejected because it would remove independent review ownership.
- Rely on `code-review` or `verify`: rejected because both occur after implementation has already consumed the proof map.
- Hand-edit generated adapter output: rejected by repository policy; generation and validation were used instead.

## Scope Control

The change does not implement historical test-spec migration, automated semantic scoring, a new review service, different-model enforcement, final validation inside `test-spec-review`, or code-review/verify redesign.

## Risks And Follow-Ups

- Stale-review detection remains first-slice, evidence-based behavior rather than content-hash fingerprinting. The proposal keeps fingerprinting as a possible follow-on if manual staleness checks prove insufficient.
- Review-model/vendor diversity remains a broader review-independence policy question, not part of this gate.
- Generated adapter directories under `dist/adapters/{codex,claude,opencode}` are local validation output and remain untracked.

## Readiness

All implementation milestones are closed with clean code-review records. The active plan routes next to `verify`; this explanation does not claim final verification, branch readiness, or PR readiness.
