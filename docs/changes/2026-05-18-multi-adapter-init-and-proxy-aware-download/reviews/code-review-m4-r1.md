# Code Review M4 R1: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m4-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `2c4c18f`
Reviewed artifact: M4 implementation commit `2c4c18f`
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR-M4-R1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m4-r1.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: CR-M4-R1-F1
- Immediate next stage: review-resolution for M4

## Scope

Reviewed the M4 implementation commit for proxy-safe network download diagnostics and the JSON/human output envelope.

Review inputs:

- Commit `2c4c18f`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- Validation evidence recorded in the active plan and change metadata

This review is isolated. It records the M4 first-pass result but does not apply review-driven fixes.

## Diff Summary

- Added bounded download failure helpers for proxy environment variable name detection, Node env-proxy status, fetch failure classification, and release-download fallback guidance.
- Changed network archive fetch failures from the generic `release-unavailable` blocker to `release-download-failed` with bounded diagnostics.
- Added fixture-backed network success coverage for Codex, Claude, and opencode.
- Added JSON and human network-failure tests for proxy-safe diagnostics and redaction.
- Added a regression test proving proxy diagnostics do not mask archive checksum verification failures.
- Updated the active plan, plan index, and change metadata for M4 handoff.

## Findings

### CR-M4-R1-F1 - `--use-env-proxy` runtime flag is not detected

Finding ID: CR-M4-R1-F1
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:465`

Evidence: `nodeEnvProxyStatus()` checks only `process.env.NODE_OPTIONS` and `process.env.NODE_USE_ENV_PROXY` before reporting `enabled`; it does not inspect `process.execArgv`. When a supported Node runtime is launched with the official `--use-env-proxy` flag, that flag is exposed through `process.execArgv`, not necessarily through `NODE_OPTIONS`. With proxy environment variables present, the current function falls through to `disabled` even though env-proxy support was explicitly enabled. The new tests at `packages/rigorloop/test/cli.test.js:1415` and `packages/rigorloop/test/cli.test.js:1453` assert only that `node_env_proxy_status` is one of the allowed enum values, so this supported activation path has no direct proof.

Spec requirement `MAI-R77` says first-slice proxy support uses Node built-in env-proxy behavior when the runtime supports and enables it. `MAI-R80` requires actionable diagnostics, `MAI-R82` through `MAI-R82b` require a bounded and truthful `node_env_proxy_status`, and the proposal explicitly identifies `NODE_USE_ENV_PROXY` and `--use-env-proxy` as the supported Node env-proxy activation mechanisms. Reporting `disabled` when `--use-env-proxy` is active makes the diagnostic misleading for the exact enterprise-networking path this milestone is meant to clarify.

Required outcome: `node_env_proxy_status` must report `enabled` when env-proxy support is enabled through `NODE_USE_ENV_PROXY`, `NODE_OPTIONS=--use-env-proxy`, or the actual Node runtime flag in `process.execArgv`. The test suite must include direct proof for the `--use-env-proxy` activation path, or use `unknown` when the runtime cannot expose or support that flag without guessing.

Safe resolution path: Update `nodeEnvProxyStatus()` to accept or read runtime exec arguments and include `process.execArgv.includes("--use-env-proxy")` in the enabled check. Add a fixture-backed CLI test that launches the package fixture with `node --use-env-proxy <cli> init --adapter codex --json` when the current Node runtime supports the flag, and asserts `diagnostics.node_env_proxy_status === "enabled"` on a mocked fetch failure. If a supported-runtime check is needed for hermeticity across Node versions, make the test skip or assert `unknown` only when the flag is unavailable.

Spec references: `MAI-R77`, `MAI-R80`, `MAI-R82`, `MAI-R82a`, `MAI-R82b`, `TMAI-029`, `TMAI-030`, `AC14`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR-M4-R1-F1` misses the explicit `--use-env-proxy` activation path for `node_env_proxy_status`, conflicting with `MAI-R77` and `MAI-R82`. |
| Test coverage | block | M4 tests assert the enum shape and env-var allowlist, but no test proves `--use-env-proxy` reports `enabled`. |
| Edge cases | block | The official Node runtime flag path is a named enterprise proxy edge case and can be misreported as `disabled`. |
| Error handling | pass | Fetch failures still return blocked status and exit code `2`, while checksum failures remain validation errors. |
| Architecture boundaries | pass | The diff stays diagnostics-first and does not add Undici dispatcher support or a new dependency. |
| Compatibility | pass | Existing JSON envelope fields are preserved and the new diagnostics are additive. |
| Security/privacy | pass | Tests cover redaction of raw proxy URLs, credentials, hostnames, tokens, and unrelated env vars. |
| Derived artifact currency | pass | No generated adapter output is changed in M4. |
| Unrelated changes | pass | The reviewed commit is scoped to M4 CLI diagnostics, tests, and lifecycle handoff artifacts. |
| Validation evidence | concern | `npm test --prefix packages/rigorloop` and selected CI are recorded as passing, but they do not exercise the missing `--use-env-proxy` path. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M4 remains open pending review-resolution for `CR-M4-R1-F1`. M5 remains unimplemented. This review does not assess package documentation alignment or final lifecycle closeout.

## Handoff

- Reviewed milestone: M4. Network download diagnostics and output envelope
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR-M4-R1-F1`
- Remaining in-scope implementation milestones: M4, M5
- Immediate next stage: review-resolution for M4
