# Code Review M3 R3: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m3-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review skill
Target: commit `2af1bc6`
Reviewed artifact: M3 review-resolution commit `2af1bc6`
Review date: 2026-05-18
Recording status: recorded
Status: clean-with-notes

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m3-r3.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: none
- Immediate next stage: implement M4

## Scope

Reviewed the M3 review-resolution commit for `CR-M3-R2-F1`, focused on whether opencode metadata that declares `.opencode/commands` without `command_aliases.opencode` now blocks before mutation in both dry-run and non-dry-run paths.

Review inputs:

- Commit `2af1bc6`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- Validation evidence recorded in the active plan and change metadata

This review is isolated. It records the M3 rerun result and updates milestone state, but it does not automatically implement M4.

## Diff Summary

- Added an opencode-specific trusted metadata blocker when `artifact.install_roots.commands` is present and `command_aliases.opencode` is absent.
- Preserved existing local-archive dry-run behavior for unrelated metadata validation while allowing opencode metadata-shape blockers to surface in dry-run.
- Added non-dry-run fixture coverage for commands-root metadata without alias metadata.
- Added dry-run fixture coverage for the same invalid metadata shape without filesystem mutation.
- Closed `CR-M3-R2-F1` in review-resolution and returned M3 to code-review rerun.

## Findings

No material findings.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | The diff enforces `MAI-R21d`, `MAI-R21e`, and `MAI-R40` through `MAI-R46c` by requiring alias metadata for opencode commands-root metadata and preserving the marked skills-only path. |
| Test coverage | pass | `TMAI-014 opencode commands root without alias metadata blocks before mutation` and `TMAI-020 dry-run opencode commands root without alias metadata blocks without mutation` directly cover the reviewed edge case. |
| Edge cases | pass | The reviewed diff covers both dry-run and non-dry-run local archive behavior for the invalid commands-root-without-alias metadata state. |
| Error handling | pass | Invalid metadata returns blocked status and exit class `blocked` before `.opencode`, `rigorloop.yaml`, or `rigorloop.lock` is written. |
| Architecture boundaries | pass | The change stays inside descriptor/trusted-metadata validation and does not add user-supplied metadata, generated source edits, or new dependencies. |
| Compatibility | pass | Existing marked older skills-only opencode tests and multi-root opencode alias tests remain in the package suite, and dry-run planning for unrelated local archive cases remains covered. |
| Security/privacy | pass | No proxy diagnostics, credential handling, raw environment values, or private URLs are introduced by M3. |
| Derived artifact currency | pass | M3 validation evidence records adapter build and validation commands passing after the resolution. |
| Unrelated changes | pass | The reviewed commit is scoped to `validateMetadata()`, dry-run metadata blocker routing, targeted tests, and required lifecycle state updates. |
| Validation evidence | pass | Change metadata records `npm test --prefix packages/rigorloop`, adapter build/validation, review artifact validation, lifecycle validation, diff check, and selected `scripts/ci.sh` passing after the fix. |

## No-Finding Rationale

The reviewed fix closes the remaining M3 opencode metadata gap by making the command root require explicit alias metadata, while keeping the approved marked skills-only path intact. The tests now cover the relevant opencode metadata truth table rows for declared aliases, missing declared alias files, marked skills-only metadata, unmarked skills-only metadata, commands-root-without-alias metadata, and dry-run behavior for the malformed commands-root case.

## Residual Risks

M4 and M5 remain unimplemented. This clean review closes only M3 and does not prove proxy-safe download diagnostics, output-envelope diagnostics, package documentation alignment, or final lifecycle closeout.

## Handoff

- Reviewed milestone: M3. Multi-root archive extraction and local archive fallback
- Review status: clean-with-notes
- Milestone closeout: M3 closed
- Remaining in-scope implementation milestones: M4, M5
- Required review-resolution: none
- Immediate next stage: implement M4
