# Code Review R2

Review ID: code-review-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: M1. Lockfile schema, parser, serializer, and write-plan contract
Status: approved

## Review inputs

- Diff/review surface: unstaged M1 lockfile implementation changes, including `packages/rigorloop/dist/lib/lockfile.js`, `packages/rigorloop/dist/bin/rigorloop.js`, and `packages/rigorloop/test/cli.test.js`
- Prior review: `docs/changes/2026-05-15-rigorloop-cli-lockfile/reviews/code-review-r1.md`
- Review resolution: `docs/changes/2026-05-15-rigorloop-cli-lockfile/review-resolution.md`
- Plan: `docs/plans/2026-05-16-rigorloop-cli-lockfile.md`
- Spec: `specs/rigorloop-cli-lockfile.md`
- Test spec: `specs/rigorloop-cli-lockfile.test.md`
- Validation evidence:
  - `npm test --prefix packages/rigorloop -- --test-name-pattern 'TLF-005|TLF-006|TLF-007'`
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop --path docs/plans/2026-05-16-rigorloop-cli-lockfile.md --path docs/plan.md --path specs/rigorloop-cli-lockfile.md --path specs/rigorloop-cli-lockfile.test.md --path docs/changes/2026-05-15-rigorloop-cli-lockfile/change.yaml`

## Diff summary

The rerun-reviewed implementation adds strict lockfile schema handling for M1. The parser now recognizes allowed top-level, `rigorloop`, `manifest`, `generated`, and adapter-entry fields; rejects unsupported unknown fields as `unsupported-lockfile-shape`; rejects missing scalar values for known scalar fields as invalid lockfile config; and still serializes the supported shape deterministically. `init` includes `rigorloop.lock` in the write plan and blocks invalid or unsupported existing lockfiles before mutation, while deferring durable writes to M2. Tests cover valid shape parsing, deterministic serialization, missing fields, unknown scalar fields, unknown nested mapping fields, unsupported schema/source/adapter/tree-hash values, dry-run planning, and CLI no-mutation behavior.

## Findings

No material findings.

## Prior finding closeout

### CR1-F1

Status: resolved by implementation

Evidence:

- `packages/rigorloop/dist/lib/lockfile.js` now matches section and adapter keys with optional scalar values and validates every detected key against allowlists.
- Direct parser proof during review returned `unsupported-lockfile-shape` for unknown nested mapping keys in `rigorloop`, `manifest`, `generated`, and `generated.adapters[0]`.
- `packages/rigorloop/test/cli.test.js` includes unit coverage for all four unknown nested mapping locations and integration coverage proving unknown nested mapping lockfiles block before generated output mutation.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | pass | M1 behavior covers R1-R17h, R23c-R23k, R34-R35, R40-R45c, and R54-R61 without enabling durable writes before M2. |
| Test coverage | pass | TLF tests cover valid shape, missing fields, malformed lockfiles, unsupported schema/source/adapter/tree-hash, unknown scalar fields, unknown nested mapping fields, dry-run planning, and no mutation. |
| Edge cases | pass | CR1-F1 named edge cases for `rigorloop.future:`, `manifest.future:`, `generated.future:`, and adapter `future:` now have direct parser proof. |
| Error handling | pass | Unsupported shape routes to `unsupported-lockfile-shape` / blocked / exit 2; malformed or invalid required scalar shape routes to invalid lockfile / error / exit 4. |
| Architecture boundaries | pass | M1 remains parser/serializer/write-plan only; durable lockfile writes remain deferred to M2. |
| Compatibility | pass | Unknown future lockfile shape is blocked instead of silently accepted or rewritten. |
| Security/privacy | pass | Planned and serialized lockfile output excludes absolute paths, timestamps, usernames, hostnames, tokens, and secrets in covered tests. |
| Derived artifact currency | pass | No generated workflow or adapter artifacts are updated in M1. |
| Unrelated changes | pass | Package changes are scoped to lockfile helper, init planning, and tests; lifecycle artifacts record the M1 state. |
| Validation evidence | pass | Focused TLF regression tests, full package tests, and selected CI are recorded as passed. |

## No-finding rationale

The implementation satisfies the approved M1 contract: it defines and validates the complete supported lockfile shape, plans `rigorloop.lock` writes without performing durable writes, blocks invalid or unsupported existing lockfiles before mutation, and preserves current adapter install behavior. The CR1-F1 gap is covered by direct parser proof and tests.

## Residual risks

M2 still needs to implement durable lockfile creation/update after verified adapter installation, and M3 still needs drift/conflict protection. This clean review closes only M1.

## Handoff

- Reviewed milestone: M1. Lockfile schema, parser, serializer, and write-plan contract
- Milestone state after review: closed
- Required review-resolution: closed for M1
- Remaining implementation milestones: M2, M3
- Next stage: implement M2
- Final closeout readiness: not ready; M2 and M3 implementation, downstream code-review, explain-change, verify, and PR handoff remain open
