# Downstream Status Settlement Before Reliance Explain Change

## Summary

This change implements the first downstream status settlement slice for `spec`, `architecture`, and `plan`.

It teaches those downstream skills to check upstream lifecycle/status metadata before relying on upstream artifacts, settle only deterministic lifecycle/status metadata, and block when review evidence, open findings, lifecycle vocabulary, or status mappings are not clear.

The change does not add review-side artifact-status sync, does not update later-slice skills, and does not add lifecycle-validator stale-status enforcement.

## Problem

The approved proposal identified a stale-status failure mode: review evidence can approve an upstream artifact while the artifact itself still says an older lifecycle status, such as a proposal that remains `Status: draft` after proposal-review approves it.

The chosen responsibility split is:

```text
Review records evidence.
Downstream settles status before reliance.
Artifacts remain the source of truth.
```

That means review skills stay focused on review evidence and material-finding recording, while downstream skills perform narrow status settlement immediately before they rely on an upstream artifact.

## Decision Trail

- Proposal accepted the downstream-settlement model while keeping review skills independent.
- Spec approved a first slice limited to `spec`, `architecture`, and `plan`.
- Spec-review `SR-001` was accepted and resolved by defining blocked `New status` semantics, including `not-applicable` when no deterministic target exists.
- Plan-review approved the two-milestone execution plan with no material findings.
- Code-review `CR-001` was accepted and resolved by tightening skill guidance and static validator assertions for edit permission and blocked-settlement semantics.
- M2 refreshed generated local Codex skill mirrors and public adapter output from the canonical skill changes.

## Diff Rationale

| Area | Files | Why it changed |
| --- | --- | --- |
| Proposal, spec, test spec | `docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md`, `specs/downstream-status-settlement-before-reliance.md`, `specs/downstream-status-settlement-before-reliance.test.md` | Establish the approved contract, first-slice scope, deterministic mappings, blocked-settlement semantics, and requirement-to-test coverage. |
| Active plan and plan index | `docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md`, `docs/plan.md` | Track the approved two-milestone execution, validation evidence, review outcomes, generated-output refresh, and current handoff state. |
| Canonical downstream skills | `skills/spec/SKILL.md`, `skills/architecture/SKILL.md`, `skills/plan/SKILL.md` | Add concise operational guidance for upstream status settlement before reliance in the first-slice downstream skills. |
| Static validator | `scripts/test-skill-validator.py` | Prove first-slice skills contain required settlement guidance, output vocabulary, edit-permission semantics, and blocked unknown-target semantics, while later-slice enforcement remains deferred. |
| Generated skill output | `.codex/skills/{spec,architecture,plan}/SKILL.md`, `dist/adapters/**/skills/{spec,architecture,plan}/SKILL.md` | Keep generated local Codex mirrors and public adapters synchronized with canonical skill text. |
| Review evidence | `docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/**` | Preserve material review findings, dispositions, validation evidence, and this rationale under the change-local evidence root. |

## Implementation Notes

The skill guidance is intentionally concise. It tells `spec`, `architecture`, and `plan` to:

- run upstream status settlement only during workflow-managed downstream execution;
- treat downstream execution as permission for minimal lifecycle/status settlement;
- edit only lifecycle/status/readiness/follow-on/closeout metadata;
- block when review evidence is missing, contradictory, unresolved, or not mapped;
- use `New status: not-applicable` when no deterministic target exists;
- report settlement only when stale status was detected, a status was updated, or settlement was blocked.

Later-slice skills remain out of operational scope. The static validator checks that `test-spec`, `implement`, `explain-change`, `verify`, and `pr` do not receive first-slice operational settlement requirements.

## Tests And Validation

The change added static validator coverage in `scripts/test-skill-validator.py` instead of runtime lifecycle validation. That matches the approved first slice: skill guidance and static proof now, lifecycle-validator stale-status detection later.

Validation already run before this explain-change handoff:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-change-metadata.py docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-12-downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.md --path specs/downstream-status-settlement-before-reliance.test.md --path docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md --path docs/plan.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/change.yaml --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-log.md --path docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording/review-resolution.md
git diff --check -- .codex/skills dist/adapters docs/changes/2026-05-12-downstream-status-settlement-before-reliance-review-recording docs/plans/2026-05-12-downstream-status-settlement-before-reliance.md docs/plan.md
```

The lifecycle validation passed with the existing unrelated `docs/plan.md` lifecycle-language warning.

## Review Resolution Summary

`review-resolution.md` is closed.

Material findings resolved:

- `SR-001`: accepted and resolved in the spec by defining blocked `New status` semantics.
- `CR-001`: accepted and resolved in skill guidance and validator assertions.

The latest code-review for M2 was `clean-with-notes` with no material findings, so no detailed clean review record was required.

## Alternatives Rejected

- Review-side artifact-status sync was rejected because it blurs review and authoring responsibilities.
- Implementing settlement in `test-spec`, `implement`, `explain-change`, `verify`, or `pr` was deferred because the first slice is limited to the clearest dependency chain.
- Lifecycle-validator stale-status enforcement was deferred until the settlement behavior and mappings stabilize.
- Substantive upstream artifact rewrites were excluded; settlement is limited to lifecycle/status metadata.

## Remaining Risk

The main residual risk is behavioral coverage depth. Static validator checks prove the first-slice skills carry the required contract, but they do not execute an end-to-end settlement scenario. The approved plan accepts that for this slice and leaves lifecycle-validator stale-status detection for a later proposal or milestone.

## Handoff

Next stage: `verify`.

This explain-change artifact documents the implemented diff and rationale, but it is not final verification or release handoff approval.
