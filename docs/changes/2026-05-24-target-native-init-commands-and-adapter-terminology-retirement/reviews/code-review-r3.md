# Code Review R3

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: working tree M2 implementation slice
Reviewed artifact: packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/lockfile.js; packages/rigorloop/test/cli.test.js; scripts/test-npm-package-publication.py; docs/plans/2026-05-24-target-native-init-commands.md
Review date: 2026-05-24
Status: changes-requested
Recording status: recorded

## Outcome

- Review status: changes-requested
- Material findings: TNI-CR3-F1
- Blocking findings: none
- Reviewed milestone: M2. Verified Install, Existing State Safety, And Target Roots
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Next stage: review-resolution for TNI-CR3-F1

## Review inputs

- Diff/review surface: working tree diff for the M2 package CLI install/state-safety changes, package CLI tests, npm package publication smoke alignment, and active plan handoff updates.
- Tracked governing branch state: not claimed; governing target-native init artifacts are local workflow artifacts in the current working tree.
- Governing artifacts: `specs/target-native-init.md`, `specs/target-native-init.test.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/adr/ADR-20260524-target-native-init-state-boundary.md`.
- Validation evidence: M2 validation notes in the active plan and `change.yaml`, including `npm test --prefix packages/rigorloop`, `python scripts/test-npm-package-publication.py`, `python scripts/test-adapter-distribution.py`, lifecycle validation, review-artifact validation, and patch hygiene.

## Diff summary

M2 adds target/root state-safety helpers to the CLI, parses target-oriented and legacy manifest roots for default-init safety decisions, scopes global lockfile drift checks to `--write-state`, keeps default init install-only for state files, preserves unrelated valid state during default init, blocks malformed state before mutation, and updates package publication smoke expectations to target-native syntax. The tests add direct coverage for default single-root installs without state files, valid unrelated state byte preservation, and malformed existing state blocking.

## Findings

### TNI-CR3-F1

Finding ID: TNI-CR3-F1
Severity: major
Location: `packages/rigorloop/test/cli.test.js`; `specs/target-native-init.test.md`; `docs/plans/2026-05-24-target-native-init-commands.md`
Evidence: The approved M2 plan says tests must cover default non-dry-run install for `codex`, `claude`, and `opencode`, valid implicated state, drifted/conflicting state, and legacy state handling. The test spec maps M2 to `TTNI-INST-001` through `TTNI-INST-004`, `TTNI-STATE-003` through `TTNI-STATE-007`, and `TTNI-MIG-001` through `TTNI-MIG-004`. The actual M2 additions directly cover only default single-root `codex`/`claude` install without state files, unrelated valid state preservation, and malformed state blocking. Existing opencode install tests run with `--write-state`, and existing drift tests also exercise `--write-state`; there is no direct package CLI proof for default `init opencode` installing skills/commands without state files, default init blocking selected-target drift/conflicting implicated state before mutation, or default legacy adapter state preservation under the new safety path.
Required outcome: Add durable direct M2 package CLI tests for the named default-init install and state-safety cases before closing M2.
Safe resolution path: Extend `packages/rigorloop/test/cli.test.js` with focused default-init tests for opencode declared skills/commands that assert `.opencode/skills` and `.opencode/commands` install and `rigorloop.yaml` / `rigorloop.lock` are absent. Add default-init tests for selected-target or overlapping-root state drift/conflict that assert blocked status, bounded blocker code, unchanged state files, and no target-root mutation. Add at least one default legacy `adapter`/`adapters` state preservation test covering compatibility input and byte preservation. If these tests expose a parser or safety-ordering bug, fix the minimal runtime path and rerun the M2 validation set.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | Runtime changes generally align with TNI-R19 through TNI-R24 and TNI-R70 through TNI-R75, but direct proof is missing for several named M2 state-safety/default-init requirements. |
| Test coverage | block | `TTNI-INST-001` default install proof covers `codex` and `claude` only; opencode default no-state install, default implicated drift/conflict, and default legacy compatibility input are not directly tested. |
| Edge cases | block | Named M2 edge cases in `TTNI-STATE-004`, `TTNI-STATE-005`, and `TTNI-MIG-001` do not have direct default-init package CLI proof. |
| Error handling | concern | The new `existingStateSafetyBlocker` appears designed to block malformed and implicated unsafe state, but missing default-init drift/conflict tests prevent a clean conclusion for those failure paths. |
| Architecture boundaries | pass | The implementation keeps deferred internal adapter names, archive filenames, and metadata fields intact while changing public command/state behavior. |
| Compatibility | concern | Schema v1/v2 lockfile parsing and legacy manifest parsing remain present, but default legacy state preservation needs direct M2 proof. |
| Security/privacy | pass | The reviewed M2 diff does not add secret logging, auth behavior, raw proxy values, or local absolute path exposure in state output. |
| Derived artifact currency | pass | No generated public adapter package output is hand-edited; package publication smoke was aligned to the target-native CLI surface. |
| Unrelated changes | pass | The M2 changes are within package CLI runtime/tests, npm package publication smoke, and lifecycle handoff artifacts. |
| Validation evidence | concern | The recorded commands passed, but they do not compensate for missing direct proof of named M2 edge cases. |

## No-finding rationale

Not applicable; one material finding requires review-resolution before M2 can close.

## Residual risks

- The implementation may already satisfy the missing runtime cases. The blocker is durable direct proof for named M2 cases, not a confirmed runtime defect.

## Milestone handoff

- Reviewed milestone: M2. Verified Install, Existing State Safety, And Target Roots
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `TNI-CR3-F1`
- Remaining in-scope implementation milestones: M2, M3, M4
- Next stage: review-resolution for `TNI-CR3-F1`
- Final closeout readiness: not ready; M2 has an open material finding and M3, M4, final explain-change, verify, and PR handoff remain open.
