# Code Review M2 R1: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `0fc24f7`
Reviewed artifact: M2 implementation commit `0fc24f7`
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: CR-M2-R1-F1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: CR-M2-R1-F1
- Immediate next stage: review-resolution for M2

## Scope

Reviewed the M2 implementation commit for manifest and lockfile schema v2 behavior.

Review inputs:

- Commit `0fc24f7`
- `specs/multi-adapter-init-and-proxy-aware-download.md`
- `specs/multi-adapter-init-and-proxy-aware-download.test.md`
- `docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `docs/architecture/system/architecture.md`
- `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md`
- `packages/rigorloop/dist/lib/lockfile.js`
- `packages/rigorloop/dist/bin/rigorloop.js`
- `packages/rigorloop/test/cli.test.js`
- Validation evidence recorded in the active plan and change metadata

This review is isolated. It records the M2 first-pass result but does not apply review-driven fixes.

## Diff Summary

- Added schema v2 lockfile parsing and serialization for Codex, Claude, and opencode entries.
- Added single-root and multi-root lockfile validation with sorted adapter serialization.
- Added manifest merge behavior for preserving unrelated adapter entries.
- Added duplicate selected manifest entry blocking.
- Added schema v1 Codex upgrade and drift-blocking tests.
- Added local archive basename assertions for durable manifest and lockfile state.
- Added M2 lifecycle handoff updates and recorded the prior M1 code-review receipt.

## Findings

### CR-M2-R1-F1 - Skills-only opencode still records and creates commands root

Finding ID: CR-M2-R1-F1
Severity: major
Location: `packages/rigorloop/dist/bin/rigorloop.js:144`

Evidence: `manifestAdapterBlock()` builds root lines from `descriptor.installRoots`, so the opencode descriptor always writes both `skills` and `commands` roots. `buildInitPlan()` computes `plan.manifest` before archive metadata is loaded, and `planDirectoryActions()` uses the descriptor directory plan before metadata determines required roots. That means an older opencode archive with only `install_root: ".opencode/skills"` would still plan/create `.opencode/commands` and record `install_roots.commands` in `rigorloop.yaml`.

Required outcome: Skills-only older opencode installs must omit `.opencode/commands` from planned directories and `rigorloop.yaml`, and must record only installed roots actually declared by trusted metadata.

Safe resolution path: Recompute the selected manifest and directory plan from trusted artifact roots after metadata validation, or defer root-specific manifest/directory actions until trusted metadata is available. Add a fixture-backed skills-only opencode test for `TMAI-017`/`TMAI-020` proving `install_roots.commands` and `.opencode/commands` are omitted when metadata lacks `command_aliases.opencode`.

Spec references: `MAI-R14a`, `MAI-R46b`, `MAI-R46c`, `MAI-R51c`, `MAI-R51e`, `MAI-R64a`, `MAI-R64b`.

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | `CR-M2-R1-F1` violates the older opencode skills-only manifest/root requirements. |
| Test coverage | block | Tests cover opencode with commands, but do not cover older opencode skills-only manifest or directory omission required by `TMAI-017`/`TMAI-020`. |
| Edge cases | block | The named older opencode archive edge case remains unproved and currently fails by code inspection. |
| Error handling | pass | Existing malformed lockfile, unsupported lockfile, duplicate manifest, and drift-blocking paths are covered by tests. |
| Architecture boundaries | pass | Lockfile schema logic remains package-local and descriptor-driven; no new dependency or generated adapter source edit was introduced. |
| Compatibility | concern | Schema v1 Codex compatibility is covered, but older opencode compatibility has the root-recording gap above. |
| Security/privacy | pass | Local archive basename recording is covered; no new proxy or credential logging was added in M2. |
| Derived artifact currency | pass | No generated public adapter package output was hand-edited. |
| Unrelated changes | pass | The reviewed implementation diff is scoped to M2 code, tests, lifecycle handoff, and required review recording. |
| Validation evidence | pass | Plan records package tests and selected CI passing after M2 implementation, but passing tests do not cover `CR-M2-R1-F1`. |

## No-Finding Rationale

Not applicable. This review has one material finding.

## Residual Risks

M2 remains open pending review-resolution for `CR-M2-R1-F1`. M3 through M5 remain unimplemented.

## Handoff

- Reviewed milestone: M2. Manifest and lockfile schema v2
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR-M2-R1-F1`
- Remaining in-scope implementation milestones: M2, M3, M4, M5
- Immediate next stage: review-resolution for M2
