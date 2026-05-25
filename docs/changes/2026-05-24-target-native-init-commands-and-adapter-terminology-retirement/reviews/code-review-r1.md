# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: working tree M1 implementation slice
Reviewed artifact: packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/lib/lockfile.js; packages/rigorloop/test/cli.test.js; packages/rigorloop/README.md; docs/plans/2026-05-24-target-native-init-commands.md
Review date: 2026-05-24
Status: changes-requested
Recording status: recorded

## Outcome

- Review status: changes-requested
- Material findings: TNI-CR1-F1
- Blocking findings: none
- Reviewed milestone: M1. CLI Command And State Schema Contract
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Next stage: review-resolution

## Review inputs

- Diff/review surface: working tree diff for M1 package CLI/parser/state schema changes.
- Tracked governing branch state: governing target-native init artifacts are local workflow artifacts in the current working tree; branch readiness is not claimed.
- Governing artifacts: `specs/target-native-init.md`, `specs/target-native-init.test.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/adr/ADR-20260524-target-native-init-state-boundary.md`.
- Validation evidence: M1 validation notes in `docs/plans/2026-05-24-target-native-init-commands.md` and `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/change.yaml`.

## Diff summary

M1 updates the package CLI to accept positional `init <target>` syntax, reject `--adapter`, add `--write-state`, skip manifest and lockfile planning for default init, and write target-oriented schema v2/v3 state when managed state is requested. The lockfile parser/serializer now accepts schema v3 `generated.targets`, package README/help examples teach target-native init, and package CLI tests were migrated to the new command shape.

## Findings

### TNI-CR1-F1 - Missing required parser-edge tests for aliases and mixed removed syntax

Finding ID: TNI-CR1-F1
Severity: major
Location: `packages/rigorloop/test/cli.test.js`; `specs/target-native-init.test.md` TTNI-CLI-002 and TTNI-CLI-003; `docs/plans/2026-05-24-target-native-init-commands.md` M1 tests.
Evidence: The active test spec requires `TTNI-CLI-002` to run `rigorloop init claude-code`, `rigorloop init open-code`, `rigorloop init openai`, and `rigorloop init codex-cli`, and requires `TTNI-CLI-003` to run `rigorloop init --adapter codex claude` and `rigorloop init codex --adapter claude`. The active M1 plan also names parser tests for aliases and mixed forms. The implemented package tests cover an unknown target (`cursor`) at `packages/rigorloop/test/cli.test.js:1100` and one removed syntax form (`init --adapter codex`) at `packages/rigorloop/test/cli.test.js:1112`, but they do not exercise the named alias targets or mixed removed/positional forms.
Required outcome: Add durable package CLI tests for the named alias targets and mixed `--adapter` forms, proving each fails before mutation and reports the required target-native migration or allowed-target guidance.
Safe resolution path: Extend the existing parser tests in `packages/rigorloop/test/cli.test.js` with table-driven cases for `claude-code`, `open-code`, `openai`, `codex-cli`, `init --adapter codex claude`, and `init codex --adapter claude`. Assert exit class/status, diagnostic code where stable, allowed-target or migration guidance, and unchanged temporary project contents. Rerun `npm test --prefix packages/rigorloop` plus the M1 metadata/lifecycle/diff checks.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The implementation changes align with M1 command/state goals, but direct proof is missing for TNI-R5 and TNI-R11 parser edge cases required by the test spec. |
| Test coverage | block | `TTNI-CLI-002` and `TTNI-CLI-003` require alias and mixed-form parser tests that are not present in `packages/rigorloop/test/cli.test.js`. |
| Edge cases | block | Named parser edge cases for ambiguous aliases and mixed removed syntax are not covered by durable tests. |
| Error handling | concern | Code shape appears to reject `--adapter` before mutation, but mixed-form diagnostics and pre-mutation behavior lack targeted test proof. |
| Architecture boundaries | pass | The diff keeps internal adapter descriptors and archive naming as implementation details while changing public command/state surfaces. |
| Compatibility | pass | Legacy lockfile parsing remains available and schema v3 serialization is added without renaming deferred archive metadata surfaces. |
| Security/privacy | pass | Reviewed M1 state writers keep archive filenames relative and do not add secret, proxy, environment, or local absolute path fields. |
| Derived artifact currency | concern | Package README/help are updated, but M3 remains responsible for broader public docs and release validation surfaces. |
| Unrelated changes | pass | The reviewed package CLI/test/README changes are in the M1 scope; unrelated dirty metadata files were not part of this review conclusion. |
| Validation evidence | concern | `npm test --prefix packages/rigorloop` passed, but the passing suite does not include all M1 parser-edge cases required by the approved test spec. |

## No-finding rationale

Not applicable; one material finding requires resolution before M1 can close.

## Residual risks

- M2 still owns deeper default existing-state safety parsing and verified install behavior.
- M3 still owns broader public docs, release metadata, packed-package smoke, and post-publish smoke validation.

## Milestone handoff

- Reviewed milestone: M1. CLI Command And State Schema Contract
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1, M2, M3, M4
- Next stage: review-resolution for TNI-CR1-F1
- Final closeout readiness: not ready; M1 has an open code-review finding and M2 through M4 remain open.
