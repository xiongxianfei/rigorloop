# Code Review M2 R2: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: commit `7858e9b`
Reviewed artifact: M2 review-resolution commit `7858e9b`
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR-M2-R2-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: CR-M2-R2-F1
- Immediate next stage: review-resolution for M2

## Scope

Reviewed the M2 review-resolution commit for `CR-M2-R1-F1`, focused on whether older skills-only opencode archives omit `.opencode/commands` from planned roots, manifest output, and lockfile output in all M2-covered planning paths.

Review inputs:

- Commit `7858e9b`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- Validation evidence recorded after `CR-M2-R1-F1` resolution

This review is isolated. It records the M2 rerun result but does not apply review-driven fixes.

## Diff Summary

- Updated manifest and directory planning to accept trusted artifact roots.
- Rebuilt the init plan after non-dry-run metadata validation provides the selected artifact.
- Added a fixture-backed non-dry-run older opencode skills-only test.
- Closed `CR-M2-R1-F1` in review-resolution and moved M2 back to review-requested.

## Findings

### CR-M2-R2-F1 - Dry-run skills-only opencode still plans commands root

Finding ID: CR-M2-R2-F1
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:1415`

Evidence: `archiveWorkForInit()` returns `{}` immediately for `flags.dryRun`, before loading or validating bundled trusted metadata. `handleInit()` builds the initial plan without an artifact, and only rebuilds the plan when `archiveWork.artifact` exists. In dry-run mode no artifact is available, so `rootsForArtifact()` falls back to `descriptor.installRoots`, which gives opencode both `.opencode/skills` and `.opencode/commands`. The new regression test for `CR-M2-R1-F1` covers only the non-dry-run local archive path, while `TMAI-020` requires older opencode skills-only dry-run planned roots and planned lockfile content to match metadata.

Required outcome: `rigorloop init --adapter opencode --dry-run --json` for a trusted older skills-only opencode archive must omit `.opencode/commands` from planned directory actions, planned manifest content, and planned lockfile content while still making no filesystem mutations.

Safe resolution path: Load and validate the selected bundled metadata artifact during dry-run root planning, then rebuild the plan from trusted artifact roots without downloading, extracting, or writing archive bytes. Add fixture-backed dry-run coverage for older opencode skills-only metadata proving actions, manifest, and planned lockfile omit `commands`.

Spec references: `MAI-R14a`, `MAI-R21e`, `MAI-R51e`, `MAI-R56`, `MAI-R88`, `TMAI-020`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR-M2-R2-F1` violates metadata-determined opencode roots for dry-run planning. |
| Test coverage | block | The added skills-only opencode test is non-dry-run only; `TMAI-020` dry-run skills-only coverage remains missing. |
| Edge cases | block | Older opencode skills-only dry-run still reports the newer command root by code inspection. |
| Error handling | pass | Existing invalid adapter, archive path, lockfile, manifest, and drift paths are unchanged by the reviewed fix. |
| Architecture boundaries | pass | The fix remains descriptor/metadata-driven and does not introduce generated adapter source edits or new dependencies. |
| Compatibility | concern | Real installs now handle skills-only opencode, but dry-run compatibility output remains misleading. |
| Security/privacy | pass | No new proxy or credential reporting was introduced in M2. |
| Derived artifact currency | pass | No generated public adapter package output was hand-edited. |
| Unrelated changes | pass | The reviewed commit is scoped to M2 resolution files and lifecycle handoff. |
| Validation evidence | concern | Package tests pass, but they do not exercise the failing dry-run path required by the test spec. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M2 remains open pending review-resolution for `CR-M2-R2-F1`. M3 through M5 remain unimplemented.

## Handoff

- Reviewed milestone: M2. Manifest and lockfile schema v2
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR-M2-R2-F1`
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Immediate next stage: review-resolution for M2
