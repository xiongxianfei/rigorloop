# Code Review R1

Review ID: code-review-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: M1. Lockfile schema, parser, serializer, and write-plan contract
Status: changes-requested

## Review inputs

- Diff/review surface: unstaged changes to `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/lockfile.js`, and `packages/rigorloop/test/cli.test.js`
- Plan: `docs/plans/2026-05-16-rigorloop-cli-lockfile.md`
- Spec: `specs/rigorloop-cli-lockfile.md`
- Test spec: `specs/rigorloop-cli-lockfile.test.md`
- Validation evidence from implementation handoff:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`

## Diff summary

M1 adds a package-local lockfile helper with strict schema parsing, deterministic serialization, and normalized manifest hashing. `rigorloop init` now includes `rigorloop.lock` in the write plan, classifies supported existing lockfiles as unchanged, blocks unsupported shapes, and errors on invalid shapes before adapter mutation. Tests add lockfile fixtures and coverage for complete shape parsing, dry-run planning, malformed lockfiles, unsupported shapes, and normalization.

## Findings

### CR1-F1 - Unknown nested mapping fields are silently accepted

Finding ID: CR1-F1
Severity: major
Location: `packages/rigorloop/dist/lib/lockfile.js`

Evidence:

- Spec requirements R23d and R23e require blocking before mutation when `rigorloop.lock` contains an unknown field inside a known section or inside a `generated.adapters[]` entry.
- The parser only recognizes nested section fields when a line matches `^  key: value` and adapter fields when a line matches `^      key: value`. Unknown mapping keys without scalar values, such as `future:`, do not match either pattern and are ignored.
- Direct proof from the reviewed implementation:

```text
rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.3"
  future:
    value: true
```

and:

```text
generated:
  adapters:
    - adapter: codex
      ...
      file_count: 23
      future:
        value: true
```

both return `ok: true` from `parseLockfile(...)`.

Required outcome:

The parser must classify unknown nested mapping fields in known sections and adapter entries as `unsupported-lockfile-shape`, returning `status: blocked` and exit code `2` through the CLI before mutation.

Safe resolution path:

Update the strict parser to detect any indented field key in known sections and adapter entries, including keys without scalar values. Add unit coverage for unknown mapping keys inside `rigorloop` and `generated.adapters[]`, and add or extend an integration test proving the CLI blocks before generated output mutation.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | CR1-F1 violates R23d/R23e unknown-field blocking. |
| Test coverage | concern | Current tests cover unknown scalar fields, but not unknown mapping keys with no scalar value. |
| Edge cases | block | Named unknown-field edge cases are incomplete for nested YAML mappings. |
| Error handling | concern | Invalid/unsupported shape routing exists, but this unsupported shape is not detected. |
| Architecture boundaries | pass | The implementation keeps lockfile authority package-local and does not enable durable writes in M1. |
| Compatibility | concern | Accepting unknown nested mappings can let an older CLI treat future lockfile sections as supported. |
| Security/privacy | pass | No secret, token, hostname, timestamp, or absolute-path recording was found in the reviewed M1 diff. |
| Derived artifact currency | pass | No generated artifact regeneration is in scope for M1. |
| Unrelated changes | pass | Package diff is scoped to lockfile planning, helper logic, and tests. |
| Validation evidence | pass | Implementation handoff records package tests and selected CI passing; the finding is a coverage/behavior gap not exposed by current tests. |

## Review result

Review status: changes-requested

M1 is not closed. `CR1-F1` requires review-resolution and an implementation fix before M1 can return to code-review.

## Handoff

- Reviewed milestone: M1. Lockfile schema, parser, serializer, and write-plan contract
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `CR1-F1`
- Remaining implementation milestones: M1 resolution needed, M2, M3
- Next stage: review-resolution for `CR1-F1`, then implement the accepted M1 fix
- Final closeout readiness: not ready; M1 is unresolved and M2/M3 have not started
