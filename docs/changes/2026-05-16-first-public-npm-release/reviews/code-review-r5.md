# Code Review R5 - M4 Release Workflow Gates

Review ID: code-review-r5
Stage: code-review
Round: 5
Reviewer: Codex code-review
Target: M4 release workflow and publication mode gates implementation
Reviewed artifact: .github/workflows/release.yml; scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; docs/plans/2026-05-16-rigorloop-npm-publication.md; docs/changes/2026-05-16-first-public-npm-release/change.yaml
Review date: 2026-05-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR5-F1
- Blocking findings: CR5-F1
- Reviewed milestone: M4. Release Workflow And Publication Mode Gates
- Milestone closeout: blocked pending review-resolution and implementation fix
- Remaining implementation milestones: M4, M5
- Required review-resolution: yes
- Next stage: review-resolution for CR5-F1, then implement the M4 fix and rerun code-review

## Review inputs

- Diff/review surface: current workspace diff for `.github/workflows/release.yml`, `scripts/adapter_distribution.py`, `scripts/test-adapter-distribution.py`, the active plan, and change metadata.
- Governing artifacts: `specs/rigorloop-npm-publication.md`, `specs/rigorloop-npm-publication.test.md`, `docs/adr/ADR-20260516-rigorloop-npm-publication.md`, `docs/architecture/system/architecture.md`, and `docs/plans/2026-05-16-rigorloop-npm-publication.md`.
- Test-spec focus: TNP-009, TNP-010, TNP-011, and TNP-012.
- Validation evidence: M4 validation notes in the active plan and `docs/changes/2026-05-16-first-public-npm-release/change.yaml`.

## Diff summary

M4 adds a `publish-npm-trusted` job to `.github/workflows/release.yml`, gated after the release job and skipped for the selected `v0.1.4` bootstrap path. The job uses npm public registry setup, stable tag and package-version checks, OIDC permissions, and `npm publish --provenance --access public ./packages/rigorloop`. The release evidence validator now requires a 64-hex tarball SHA-256 for published bootstrap evidence, and tests cover workflow gating plus missing published bootstrap identity fields.

## Findings

### CR5-F1 - Bootstrap tarball SHA mismatch is not validated

Finding ID: CR5-F1
Severity: blocker

Location:
- `scripts/adapter_distribution.py:2463`
- `scripts/test-adapter-distribution.py:3393`
- `specs/rigorloop-npm-publication.md:346`
- `specs/rigorloop-npm-publication.test.md:281`

Evidence:
The approved spec requires bootstrap publication to block if "the tarball SHA-256 differs from recorded evidence" (`R61c`). The test spec also names "Negative fixture: mismatched tarball SHA fails validation" under TNP-011. The current validator checks only that `tarball.sha256` is shaped like 64 lowercase hex characters:

```text
tarball_sha256 = str(tarball.get("sha256", ""))
if not re.fullmatch(r"[0-9a-f]{64}", tarball_sha256):
    errors.append(...)
```

The new negative test only covers a missing or placeholder SHA, plus missing maintainer and publish command. There is no fixture where a real tarball exists with hash B while evidence records hash A, and no implementation path compares recorded evidence to packed tarball bytes.

Required outcome:
Bootstrap evidence validation must reject a mismatched tarball SHA-256, not only missing or malformed SHA text, before M4 can close.

Safe resolution path:
Add a deterministic test fixture that creates or points to a packed tarball file and records a different `tarball.sha256` in `npm-publication.md`. Then update validation so, when a bootstrap tarball is available to the release/evidence validator, it computes the SHA-256 over the exact tarball named by evidence and fails when it differs. Keep the pending-publication scaffold behavior intact; the mismatch check can apply to published bootstrap evidence or to pre-publication bootstrap identity evidence when the tarball file is present.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R61c requires blocking on mismatched bootstrap tarball SHA-256, but the implementation checks only hash shape. |
| Test coverage | block | TNP-011 requires a mismatched tarball SHA negative fixture; current tests cover missing/placeholder SHA and complete happy path only. |
| Edge cases | block | The exact bootstrap artifact identity mismatch edge case remains unproven and unenforced. |
| Error handling | concern | Published bootstrap evidence with a well-formed but wrong SHA can pass the current validator, allowing evidence to claim the wrong tarball identity. |
| Architecture boundaries | pass | The workflow keeps one release workflow and uses trusted-publishing OIDC only in the publish job. |
| Compatibility | pass | Existing GitHub release archive behavior remains in the `release` job and npm tarballs are not uploaded as adapter archives. |
| Security/privacy | block | Bootstrap publication is a supply-chain boundary; accepting an unchecked tarball SHA weakens the exact-artifact publish contract. |
| Derived artifact currency | pass | No generated public adapter skill bodies were edited for M4. |
| Unrelated changes | pass | The M4 changes are scoped to release workflow, release evidence validation/tests, and lifecycle state. |
| Validation evidence | concern | Recorded M4 validation is relevant, but it does not include the required mismatched-SHA negative proof. |

## No-finding rationale

Not applicable. This review has a material finding.

## Residual risks

- M5 remains planned and must not start until M4 returns to clean code-review or the plan is revised.
- Public npm publication, post-publication `npm view`/`npx` smoke, and real non-dry-run Codex adapter install proof remain future M6b work and are not claimed by this review.
