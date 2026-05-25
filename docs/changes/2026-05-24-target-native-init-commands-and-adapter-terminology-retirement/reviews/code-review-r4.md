# Code Review R4

Review ID: code-review-r4
Stage: code-review
Round: 4
Reviewer: Codex code-review
Target: working tree M2 implementation slice after TNI-CR3-F1 resolution
Reviewed artifact: packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/lockfile.js; packages/rigorloop/test/cli.test.js; scripts/test-npm-package-publication.py; docs/plans/2026-05-24-target-native-init-commands.md
Review date: 2026-05-24
Status: approved
Recording status: recorded

## Outcome

- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Reviewed milestone: M2. Verified Install, Existing State Safety, And Target Roots
- Milestone closeout: closed
- Remaining implementation milestones: M3, M4
- Required review-resolution: none
- Next stage: implement M3

## Review inputs

- Diff/review surface: working tree diff for M2 package CLI install/state-safety changes, package CLI tests, npm package publication smoke alignment, and `TNI-CR3-F1` direct-proof test additions.
- Tracked governing branch state: not claimed; governing target-native init artifacts are local workflow artifacts in the current working tree.
- Governing artifacts: `specs/target-native-init.md`, `specs/target-native-init.test.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/adr/ADR-20260524-target-native-init-state-boundary.md`.
- Validation evidence: M2 and `TNI-CR3-F1` validation notes in the active plan and `change.yaml`, including `npm test --prefix packages/rigorloop` passing with 117 tests, `python scripts/test-npm-package-publication.py`, `python scripts/test-adapter-distribution.py`, lifecycle validation, review-artifact closeout validation, and patch hygiene.

## Diff summary

M2 adds default install-only safety reads before target-root mutation, preserves existing state files by default, blocks malformed, drifted, or conflicting implicated state before mutation, keeps `--write-state` responsible for state rewrites, and preserves opencode multi-root install behavior. The `TNI-CR3-F1` resolution adds direct package CLI tests for default opencode skills/commands installation without state files, selected-target drift blocking, overlapping-root conflict blocking, and legacy adapter state byte preservation. No production runtime changes were needed for the `TNI-CR3-F1` resolution.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `existingStateSafetyBlocker` in `packages/rigorloop/dist/bin/rigorloop.js` enforces TNI-R19 through TNI-R24; default init skips state writes per TNI-R14 through TNI-R17; opencode roots and state compatibility remain covered by M2 tests. |
| Test coverage | pass | `packages/rigorloop/test/cli.test.js` includes direct tests for default codex/claude no-state install, default opencode no-state multi-root install, unrelated state preservation, selected-target drift blocking, overlapping-root conflict blocking, malformed state blocking, and legacy adapter state preservation. |
| Edge cases | pass | The named `TNI-CR3-F1` cases are directly covered by `TTNI-INST-002`, `TTNI-STATE-005`, and `TTNI-MIG-001`; the focused selector `npm test --prefix packages/rigorloop -- --test-name-pattern "TTNI-INST-002|TTNI-STATE-005|TTNI-MIG-001"` passed. |
| Error handling | pass | Blocked drift/conflict tests assert stable blocker codes, byte-preserved state files, and unchanged target roots before mutation. Existing malformed-state tests continue to prove blocking before mutation. |
| Architecture boundaries | pass | The implementation keeps deferred internal adapter names, archive filenames, and package-bundled metadata fields intact while changing public command/state behavior. |
| Compatibility | pass | Legacy schema v1/v2 lockfile and legacy manifest compatibility remain parseable input; `TTNI-MIG-001` proves default init preserves legacy `adapter` / `adapters` state byte-for-byte. |
| Security/privacy | pass | The reviewed diff adds no secret logging, auth behavior, raw proxy values, absolute local path state output, or request-header exposure. |
| Derived artifact currency | pass | No generated public adapter package output is hand-edited; package publication smoke was aligned with target-native CLI behavior. |
| Unrelated changes | pass | The reviewed changes are scoped to M2 runtime/tests, package publication smoke, and lifecycle/review evidence. M3 release/docs work remains separate. |
| Validation evidence | pass | Recorded validation includes package CLI tests, npm publication smoke, adapter distribution tests, change metadata validation, lifecycle validation, review-artifact validation, and patch hygiene. |

## No-finding rationale

The R3 direct-proof gap is closed by package CLI tests that exercise the exact missing default-init paths. The broader M2 runtime path now has direct evidence for no-state default installs, multi-root opencode handling, safe preservation of unrelated and legacy state, and blocking of malformed, drifted, or conflicting state before mutation. Passing validation supports closing M2 and moving to the planned M3 release/docs validation milestone.

## Residual risks

- M3 still must update broader public docs, package version/release metadata, packed-package smoke, and post-publish smoke validation.
- M4 still must perform lifecycle closeout, durable explanation, final verification, and PR handoff.

## Milestone handoff

- Reviewed milestone: M2. Verified Install, Existing State Safety, And Target Roots
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M3, M4
- Next stage: implement M3
- Final closeout readiness: not ready; M3, M4, final explain-change, verify, and PR handoff remain open.
