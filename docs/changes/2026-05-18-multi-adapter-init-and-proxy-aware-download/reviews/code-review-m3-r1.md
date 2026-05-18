# Code Review M3 R1: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `a04b16b`
Reviewed artifact: M3 implementation commit `a04b16b`
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR-M3-R1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: CR-M3-R1-F1
- Immediate next stage: review-resolution for M3

## Scope

Reviewed the M3 implementation commit for multi-root archive extraction, local archive fallback, opencode command alias validation, older opencode skills-only warnings, and generated adapter validation evidence.

Review inputs:

- Commit `a04b16b`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- M3 validation evidence recorded in the active plan and change metadata

This review is isolated. It records the M3 first-pass result but does not apply review-driven fixes.

## Diff Summary

- Added validation for declared `command_aliases.opencode` metadata, including count/path checks and required commands root.
- Switched archive unsafe-path allowlisting from descriptor possible roots to trusted artifact roots.
- Added archive inspection that fails when a declared opencode command alias file is missing.
- Added warning output for older opencode metadata that lacks declared command aliases and installs only skills.
- Added fixture-backed tests for Claude install roots, opencode skills plus commands, missing declared aliases, older skills-only warnings, and skills-only archive extraction boundaries.
- Recorded M3 validation evidence, including package tests and generated adapter build/validation commands.

## Findings

### CR-M3-R1-F1 - Skills-only opencode compatibility is inferred without explicit metadata range

Finding ID: CR-M3-R1-F1
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:522`

Evidence: `validateMetadata()` accepts an opencode artifact without `command_aliases.opencode` when the artifact otherwise has valid single-root metadata, but it does not require any bundled trusted-metadata field or compatible release-range marker for skills-only opencode installation. `initWarnings()` then emits `opencode-command-aliases-not-declared` based only on adapter name, absent command aliases, and absent commands root. The positive skills-only tests at `packages/rigorloop/test/cli.test.js:2126` and `packages/rigorloop/test/cli.test.js:2161` use fixtures with only `adapter: "opencode"` and `installRoot: ".opencode/skills"`, so the current test suite proves that unmarked skills-only metadata is accepted.

Spec requirement `MAI-R21f` says skills-only older opencode archive behavior is allowed only for release ranges explicitly listed in bundled trusted metadata as compatible with skills-only opencode installation. The current implementation treats absence of command aliases as sufficient and does not enforce the explicit compatibility boundary.

Required outcome: Older skills-only opencode installation must be allowed only when bundled trusted metadata explicitly marks the selected release or artifact as compatible with skills-only opencode installation. Unmarked opencode metadata lacking `command_aliases.opencode` must block before extraction, manifest writes, or lockfile writes. Tests must include both an allowed marked skills-only archive and a rejected unmarked skills-only archive.

Safe resolution path: Add a minimal trusted-metadata compatibility marker or release-range field for older skills-only opencode artifacts, validate it in `validateMetadata()` before returning the artifact, and update fixture metadata helpers so positive skills-only tests include the marker. Add a negative fixture-backed test proving unmarked skills-only opencode metadata fails with a stable metadata or compatibility blocker before mutation. If the owner wants a different marker shape than the smallest implementation-local field, update the spec/test-spec first; the existing spec already requires an explicit trusted-metadata boundary.

Spec references: `MAI-R21e`, `MAI-R21f`, `MAI-R39` through `MAI-R46c`, `TMAI-016`, `TMAI-017`, `TMAI-020`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR-M3-R1-F1` violates `MAI-R21f` by allowing skills-only opencode without an explicit trusted-metadata compatibility boundary. |
| Test coverage | block | Positive skills-only tests pass without any compatibility marker, and no negative test rejects unmarked skills-only metadata. |
| Edge cases | block | The older-archive compatibility edge case is accepted by inference rather than by the approved release-range contract. |
| Error handling | concern | Invalid unmarked skills-only metadata is not blocked before extraction; it becomes a warning install. |
| Architecture boundaries | concern | Metadata remains trusted, but the compatibility decision is inferred from missing fields instead of an explicit trusted metadata contract. |
| Compatibility | concern | Older archive support exists, but the release-range guard for compatibility is missing. |
| Security/privacy | pass | No new proxy logging, credential handling, or private URL exposure is introduced by M3. |
| Derived artifact currency | pass | Generated adapter build and validation commands are recorded as passing for M3. |
| Unrelated changes | pass | The reviewed implementation is scoped to CLI archive/root behavior, tests, and lifecycle handoff. |
| Validation evidence | concern | Recorded tests pass, but they prove the incorrect unmarked skills-only acceptance path. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M3 remains open pending review-resolution for `CR-M3-R1-F1`. M4 and M5 remain unimplemented.

## Handoff

- Reviewed milestone: M3. Multi-root archive extraction and local archive fallback
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR-M3-R1-F1`
- Remaining in-scope implementation milestones: M3, M4, M5
- Immediate next stage: review-resolution for M3
