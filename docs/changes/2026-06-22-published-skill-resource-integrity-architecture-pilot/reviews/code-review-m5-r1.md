# Code Review M5 R1

Review ID: code-review-m5-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `f146eff7`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m5-r1.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M5-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m5-r1.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M5. Reusable Packed Clean-Install Regression Gate
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M5 resolution, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M5-CR1
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `f146eff7` (`M5: add reusable clean-install resource gate`).
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 through M4 reviews, active plan M5 review-requested state, and M5 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R50-R50b and R52-R52c; `specs/skill-contract.test.md` T46; active plan M5.
- Validation evidence: focused M5 clean-install tests, full `python scripts/test-adapter-distribution.py`, selector-selected adapter regression command, packed archive build, archive validation, clean-install smoke, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --` recorded in the active plan and change metadata.
- Implementation files reviewed: `scripts/adapter_distribution.py`, `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/clean-install-proof.md`, active plan state, and change metadata.

## Diff summary

M5 adds a reusable clean-install smoke path to `validate-adapters.py`.

The new `validate_clean_install_smoke()` helper validates locally packed adapter archives, prepares temporary local CLI metadata for those archives, installs Codex, Claude, and opencode archives into empty temporary projects through `rigorloop init --from-archive`, and compares installed mapped resources by skill-root relative path and raw-byte SHA-256.

The test suite adds coverage for successful real clean install from local archives, no-op command output rejected as proof, stale installed mapped-resource bytes, and rejecting `--clean-install-smoke` without a packed archive `--root`.

## Findings

## Finding SRI-M5-CR1

Finding ID: SRI-M5-CR1
Severity: major
Location: `scripts/test-adapter-distribution.py:1102`; `scripts/test-adapter-distribution.py:1125`; `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md:333`
Evidence: The M5 plan explicitly requires tests proving the reusable gate detects "missing and stale installed mapped resources." The added tests prove stale installed bytes with `test_clean_install_smoke_rejects_stale_installed_mapped_resource`, and they prove a non-mutating command cannot pass because the whole skill root is missing. They do not prove the named missing-resource case where the installed skill root exists but one mapped resource file is absent. Code shape alone is not enough direct proof for this named edge case under the code-review contract.
Required outcome: Add direct M5 regression coverage for a clean-install smoke result where the target installed skill root exists but a mapped resource file is missing, and assert the diagnostic names the target, skill, and resource path.
Safe resolution path: Add a focused test alongside the existing clean-install smoke tests. Use a command runner that extracts the archive into the temporary target project, removes one mapped resource such as `assets/template.md` from one target's installed skill root, and assert `validate_clean_install_smoke(...)` reports `clean-install mapped resource missing: <target>/<skill>: assets/template.md`. Rerun `python scripts/test-adapter-distribution.py`, selector-selected validation for `scripts/adapter_distribution.py`, `scripts/validate-adapters.py`, and `scripts/test-adapter-distribution.py`, packed archive build/validation, clean-install smoke, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --`.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | R52-R52b require locally packed release candidates installed into empty target projects with skill-root-relative path checks. `validate_clean_install_smoke()` builds empty target projects and uses `rigorloop init --from-archive` for Codex, Claude, and opencode before inspecting installed skill roots. |
| Test coverage | concern | Tests cover real local archive install, no-op output rejection, stale installed bytes, and `--root` enforcement, but they do not directly cover missing installed mapped resources with an existing skill root. |
| Edge cases | concern | The named missing-resource edge case in the M5 plan lacks direct proof. |
| Error handling | pass | Missing archives, installer command failures, missing skill roots, missing mapped files, and stale hashes return validation errors instead of passing. |
| Architecture boundaries | pass | The change stays in adapter distribution validation, CLI validation, tests, and M5 proof artifacts. It does not alter architecture skill behavior or M5/M1 boundary ownership. |
| Compatibility | pass | Existing `validate-adapters.py --root` behavior remains available. The new smoke mode requires `--root`, preserving the locally packed release-candidate boundary. |
| Security/privacy | pass | The smoke uses temporary directories, local archives, and no live registry, credentials, or remote resource loading. |
| Derived artifact currency | pass | The reviewed change builds and validates release archives without hand-editing generated adapter output or installed target trees as durable source. |
| Unrelated changes | pass | The diff is scoped to M5 clean-install smoke implementation, tests, proof artifact, and lifecycle bookkeeping. |
| Validation evidence | concern | Recorded commands are relevant and passed, but the focused M5 tests omit one named failure-path proof. |

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M5. Reusable Packed Clean-Install Regression Gate
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Remaining implementation milestones: M5 resolution, M6, M7
Next stage: review-resolution for SRI-M5-CR1
Final closeout readiness: not ready; M5 remains open and later implementation milestones remain.

This direct `code-review` invocation is isolated; no automatic downstream handoff is performed here.
