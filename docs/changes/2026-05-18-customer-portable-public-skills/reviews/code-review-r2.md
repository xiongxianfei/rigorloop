# Code Review R2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M2. Public skill wording and static validation
Reviewed artifact: docs/plans/2026-05-18-customer-portable-public-skills.md
Review date: 2026-05-18
Recording status: recorded
Status: clean-with-notes

## Review Inputs

- Diff/review surface:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `skills/project-map/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`
  - `docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `docs/changes/2026-05-18-customer-portable-public-skills/explain-change.md`
  - `docs/plans/2026-05-18-customer-portable-public-skills.md`
- Governing spec: `specs/customer-portable-public-skill-evidence.md`
- Test spec: `specs/customer-portable-public-skill-evidence.test.md`
- Plan milestone: `docs/plans/2026-05-18-customer-portable-public-skills.md`, M2
- Validation evidence:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `git diff -- skills/code-review/SKILL.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check -- skills scripts docs/changes/2026-05-18-customer-portable-public-skills docs/plans/2026-05-18-customer-portable-public-skills.md docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`

## Diff Summary

M2 adds concise `Project-local evidence` sections to the audited risky public skills `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `verify`, and `pr`. It adds a light `Customer-project orientation` caveat to `project-map`, adds static validator coverage for the new wording and required RigorLoop-internal dependency examples, records per-skill safety-preservation notes, updates change-local evidence, and moves the active plan from M2 implementation to M2 review handoff.

`code-review` remains unchanged.

## Findings

No blocking or required-change findings.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | The touched skills now state customer-project mode by default, project-local evidence use, no required RigorLoop repository-internal docs, portable defaults, and ambiguity blocking, satisfying R1-R10 and R17-R25. |
| Test coverage | pass | `scripts/test-skill-validator.py` adds checks for M2 `Project-local evidence` sections, the `project-map` optional-local-input caveat, and forbidden/allowed required-internal-dependency examples, satisfying T4 and T6. |
| Edge cases | pass | The new tests cover absent project-map orientation inputs, legitimate guarded local docs/spec references, and forbidden required RigorLoop-internal wording. `git diff -- skills/code-review/SKILL.md` proves the EC10 no-edit path for `code-review`. |
| Error handling | pass | The skill wording preserves portable-default behavior and explicit ambiguity blocking. `verify` and `pr` additionally preserve no-false-claim boundaries for validation and readiness evidence. |
| Architecture boundaries | pass | No runtime architecture, CLI, workflow YAML, generated workflow docs, or release benchmark behavior is introduced. The change stays in public skill text, validator tests, reports, and lifecycle evidence. |
| Compatibility | pass | Existing project-local specs, docs, governance files, plans, architecture records, and workflow guides remain allowed when present and relevant. RigorLoop repository mode is not removed. |
| Security/privacy | pass | The skill wording does not require customer secrets, tokens, private keys, unrelated local paths, generated adapter internals, or repository-maintainer-only implementation details. |
| Derived artifact currency | pass | `python scripts/build-skills.py --check` passed using temporary generated output from canonical `skills/`. Public adapter temp-output validation remains correctly scheduled for M3. |
| Unrelated changes | pass | The reviewed M2 diff is limited to audited risky skills, focused validator checks, migration/report evidence, and change-local/plan handoff updates. |
| Validation evidence | pass | The M2 validation commands recorded in the active plan and change metadata passed, including `test-skill-validator`, `validate-skills`, `build-skills --check`, metadata, review artifact, lifecycle, and diff checks. |

## No-Finding Rationale

The implementation satisfies the approved M2 slice without broad skill rewrites. The wording additions are concise and project-local, and the existing skill sections that carry claim boundaries, stop conditions, output shape, formal review behavior, validation behavior, and readiness boundaries remain in place. Static validation is narrow and phrase/path based: it catches obvious required RigorLoop-internal dependency wording while allowing guarded project-local or conditional references.

The M2 evidence also records why each touched skill rewrite is safe and where each essential rule remains preserved. `code-review` is protected by the audit decision and has no diff.

## Residual Risks

- M3 still needs after-change static token measurement, targeted customer-fixture dynamic benchmark evidence, and generated public adapter output validation.
- This review does not claim branch readiness, PR readiness, CI status, final verification, or M3 completion.

## Recommended Next Stage

Clean non-final milestone review. Close M2 and hand off to `implement` for M3.
