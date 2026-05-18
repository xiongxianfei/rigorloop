# Code Review M3 R2: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: commit `dd018b4`
Reviewed artifact: M3 review-resolution commit `dd018b4`
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR-M3-R2-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: CR-M3-R2-F1
- Immediate next stage: review-resolution for M3

## Scope

Reviewed the M3 review-resolution commit for `CR-M3-R1-F1`, focused on whether opencode command-root and skills-only compatibility behavior now matches the approved trusted-metadata contract.

Review inputs:

- Commit `dd018b4`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- Validation evidence recorded after `CR-M3-R1-F1` resolution

This review is isolated. It records the M3 rerun result but does not apply review-driven fixes.

## Diff Summary

- Added `releaseListedForSkillsOnlyCompatibility()` and enforced a trusted metadata `skills_only_compatibility.releases` marker for opencode skills-only metadata.
- Marked positive older skills-only opencode fixtures as compatible.
- Added a negative fixture-backed test that blocks unmarked skills-only opencode metadata before mutation.
- Closed `CR-M3-R1-F1` in review-resolution and moved M3 back to review-requested.

## Findings

### CR-M3-R2-F1 - Opencode commands root can be installed without command alias metadata

Finding ID: CR-M3-R2-F1
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:540`

Evidence: `validateMetadata()` validates multi-root metadata generically when `artifact.install_roots` and `artifact.root_hashes` are present, then only validates opencode alias metadata inside `if (artifact.command_aliases?.opencode)`. The new `CR-M3-R1-F1` guard only runs when `!rootsForArtifact(descriptor, artifact).commands`, so an opencode artifact with `install_roots.commands` but no `command_aliases.opencode` is accepted. That path installs `.opencode/commands` without declared command aliases, emits no `opencode-command-aliases-not-declared` warning, and skips declared-alias existence checks. The positive multi-root test at `packages/rigorloop/test/cli.test.js:2036` includes `commandAliases`, and there is no negative test for opencode `install_roots.commands` without `command_aliases.opencode`.

Spec requirement `MAI-R21e` says absence of `command_aliases.opencode` is the signal that the selected official opencode archive is an older skills-only archive. Requirements `MAI-R44`, `MAI-R46a`, `MAI-R46b`, and `MAI-R46c` require that older skills-only installs omit `.opencode/commands`, emit the stable warning, and record only `skills`. Therefore metadata that declares `.opencode/commands` without `command_aliases.opencode` must not be treated as a valid commands install.

Required outcome: Opencode metadata that includes or requires `.opencode/commands` must also include valid `command_aliases.opencode` metadata. If `command_aliases.opencode` is absent, the CLI must treat the selected opencode metadata as the older skills-only shape: it may proceed only when explicitly marked compatible, must omit `.opencode/commands`, must emit `opencode-command-aliases-not-declared`, and must record only the installed `skills` root. A multi-root opencode artifact with commands root and no alias metadata should block before extraction, manifest writes, or lockfile writes.

Safe resolution path: Add an opencode-specific metadata validation branch after root validation: when `descriptor.name === "opencode"` and `artifact.install_roots?.commands` exists, require valid `artifact.command_aliases?.opencode`; otherwise return a stable metadata blocker or error before archive inspection. Add a fixture-backed negative test with `installRoots.skills` plus `installRoots.commands` and no `commandAliases`, proving the command exits before mutation. Keep the existing marked single-root skills-only tests as the allowed old-archive path.

Spec references: `MAI-R21d`, `MAI-R21e`, `MAI-R41` through `MAI-R46c`, `TMAI-014`, `TMAI-015`, `TMAI-016`, `TMAI-017`, `TMAI-020`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR-M3-R2-F1` allows opencode commands-root metadata without `command_aliases.opencode`, conflicting with `MAI-R21e` and the older skills-only rules. |
| Test coverage | block | Existing tests cover declared aliases and single-root skills-only metadata, but not commands-root metadata missing alias metadata. |
| Edge cases | block | The missing-alias-metadata edge case can silently install `.opencode/commands` without declared alias verification. |
| Error handling | concern | Invalid opencode multi-root metadata is accepted instead of blocking before extraction. |
| Architecture boundaries | concern | The trust boundary is still metadata-driven, but the metadata contract is under-validated for opencode command roots. |
| Compatibility | pass | Codex, Claude, and marked skills-only opencode paths are not affected by the finding. |
| Security/privacy | pass | No proxy diagnostics, credentials, or private values are introduced by this resolution. |
| Derived artifact currency | pass | Adapter build and validation evidence is recorded after the resolution. |
| Unrelated changes | pass | The reviewed commit is scoped to M3 resolution code, tests, and lifecycle artifacts. |
| Validation evidence | concern | Package tests and selected CI pass, but they do not exercise the commands-root-without-alias-metadata case. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M3 remains open pending review-resolution for `CR-M3-R2-F1`. M4 and M5 remain unimplemented.

## Handoff

- Reviewed milestone: M3. Multi-root archive extraction and local archive fallback
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR-M3-R2-F1`
- Remaining in-scope implementation milestones: M3, M4, M5
- Immediate next stage: review-resolution for M3
