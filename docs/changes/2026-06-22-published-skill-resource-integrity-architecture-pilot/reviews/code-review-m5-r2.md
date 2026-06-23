# Code Review M5 R2

Review ID: code-review-m5-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `47eba3f4`
Status: clean-with-notes

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m5-r2.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: implement M6
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m5-r2.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: not-required
- Reviewed milestone: M5. Reusable Packed Clean-Install Regression Gate
- Milestone closeout: closed
- Remaining implementation milestones: M6, M7
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `47eba3f4` (`M5: resolve clean-install missing resource proof`), plus the existing M5 implementation commit `f146eff7`.
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 through M4 reviews, SRI-M5-CR1 detailed review, accepted review-resolution evidence, active plan M5 review-requested rerun state, and M5 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R50-R50b and R52-R52c; `specs/skill-contract.test.md` T46; active plan M5; SRI-M5-CR1 review-resolution entry.
- Validation evidence: focused missing-resource clean-install regression, focused M5 clean-install test bundle, selector-selected adapter regression command, packed archive build, archive validation, reusable clean-install smoke, full `python scripts/test-adapter-distribution.py`, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --` recorded in the active plan and change metadata.
- Implementation files reviewed: `scripts/test-adapter-distribution.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/clean-install-proof.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, active plan state, and change metadata.

## Diff summary

The SRI-M5-CR1 resolution adds direct regression coverage for an installed target skill root that exists while one mapped resource is missing.

The new test performs a local packed archive build and lets `validate_clean_install_smoke()` invoke the real install path. A shared post-install mutation helper waits until the target install succeeds, resolves the installed target skill root using `ADAPTERS[target].skill_root`, asserts the skill root exists, asserts `SKILL.md` exists, asserts `assets/template.md` exists, and then applies the test mutation.

The missing-resource test removes `assets/template.md` after the valid Codex install and asserts `validate_clean_install_smoke()` reports `clean-install mapped resource missing: codex/portable-with-assets: assets/template.md`, while also asserting the case is not misreported as a missing skill root.

The stale-resource test now reuses the same post-install mutation helper for its byte-corruption path. The proof artifact and review-resolution entry were updated with the missing-resource case and validation evidence.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R52-R52b and T46 require locally packed release candidates, empty target projects, real installed skill tree inspection, and skill-root-relative mapped resource validation. The reviewed test exercises `validate_clean_install_smoke()` after archive build and real target installation before deleting the mapped resource. |
| Test coverage | pass | `test_clean_install_smoke_rejects_missing_installed_mapped_resource` directly covers the SRI-M5-CR1 gap. The focused M5 bundle also retains valid install, non-mutating command rejection, stale bytes, and `--root` enforcement. |
| Edge cases | pass | The test proves the installed skill root exists, `SKILL.md` exists, the mapped resource exists before mutation, only `assets/template.md` is removed, the diagnostic names target/skill/path, and the case is not reported as a missing skill root. |
| Error handling | pass | The missing-file branch in `validate_clean_install_smoke()` is now directly exercised through a post-install filesystem mutation rather than a hand-built incomplete fixture. |
| Architecture boundaries | pass | The resolution changes only adapter distribution tests and M5 proof/lifecycle artifacts. It does not change architecture resources, installer behavior, archive identity, or target-root mappings. |
| Compatibility | pass | Existing clean-install success, stale-byte, no-op, and archive-root enforcement tests remain green; `validate-adapters.py --root` and `--clean-install-smoke` behavior is unchanged. |
| Security/privacy | pass | The test uses temporary projects and local archives, with no live registry, credentials, network loading, or secret-bearing evidence. |
| Derived artifact currency | pass | No generated adapter output or installed target tree is hand-edited as durable source. The mutation is confined to a temporary test install. |
| Unrelated changes | pass | The diff is scoped to SRI-M5-CR1 test/proof coverage and lifecycle bookkeeping. |
| Validation evidence | pass | The active plan and change metadata record the focused missing-resource test, focused M5 bundle, selector-selected adapter checks, packed archive build, archive validation, clean-install smoke, full adapter suite, lifecycle validation, metadata validation, review-artifact validation, and whitespace check as passing. |

## No-finding rationale

SRI-M5-CR1 required direct proof for a distinct installed state: installed skill root exists, installed `SKILL.md` exists, and one mapped resource file is missing. The reviewed test helper proves root and `SKILL.md` existence before mutating the resource path, and the test asserts the resulting diagnostic names `codex`, `portable-with-assets`, and `assets/template.md`.

The test uses the same locally packed archive and real clean-install smoke route as the valid install test. That closes the prior proof gap without changing production installer, archive, target-root, or raw-byte identity behavior.

## Residual risk

M6 repository-wide audit/enforcement and M7 final evidence closeout remain open and are not claimed by this review.

## Handoff

Reviewed milestone: M5. Reusable Packed Clean-Install Regression Gate
Review status: clean-with-notes
Milestone closeout: closed
Required review-resolution: no
Remaining implementation milestones: M6, M7
Next stage: implement M6
Final closeout readiness: not ready; later implementation milestones remain.

Do not claim final closeout, verify readiness, branch readiness, or PR readiness from this review.
