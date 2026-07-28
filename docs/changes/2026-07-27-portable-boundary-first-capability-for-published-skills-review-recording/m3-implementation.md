# M3 implementation evidence

## Result

- Milestone: PBF-M3
- Status: review-requested
- Scope: structural boundary records and the two-state release manifest
- Next stage: code-review M3

## Implementation

The structural validator continues to check the closed boundary record and
proof-map grammar without claiming semantic completeness.

Activation validation now implements the approved lightweight contract:

- state is exactly `pending` or `active`;
- pending release and baseline fields use `-`;
- active state binds existing immutable activating and immediately preceding
  rollback release tags;
- the ten governed skills and canonical/projection byte identities remain
  closed;
- the baseline is the exact full parent identity of the repository's single
  pending-to-active manifest transition on first-parent integration history;
- the activating tag resolves to that transition commit and current release
  fields remain identical to the transition snapshot;
- grandfathered paths are derived from that exact commit, contain only
  accepted, approved, or active unmarked top-level feature specs, exclude the
  bootstrap spec, README, test specs, marked specs, nonterminal specs, and
  child-introduced paths, and use unique raw-UTF-8 order;
- baseline inventory reads NUL-delimited Git tree entries, accepts only regular
  blobs, and reads blobs by object identity.

The previous `rolled-back` state, activation timestamp, historical file
hashes, inventory digest, rollback receipt path, and receipt identity are
removed. Source control owns historical bytes and immutable release-tag
ordering. The adapter support manifest is no longer an M3 release-order
authority. There is no activation writer, rollback writer, transaction, or
attestation store.

Changed unmarked grandfathered specs continue to route to `spec-review`.
Marked feature/test pairs continue to receive structural validation.

## Test-first evidence

The focused activation suite now builds a minimal temporary Git history with a
parent and activating worktree. Direct regressions prove:

- accepted, approved, and active parent specs are included;
- draft, marked, excluded, and child-introduced specs are omitted;
- an older but valid release tag cannot serve as rollback release;
- nonexistent and equal activating/rollback tags fail;
- integer, child, and grandparent baselines fail;
- Unicode parent paths remain present through raw Git tree enumeration;
- baseline symlink modes fail before blob interpretation;
- merge integration uses the target branch's first parent and inventories
  target-only historical specs;
- a tag moved to a pending commit and an active-to-active release rewrite
  fail;
- duplicate and incorrectly ordered inventories fail;
- unknown states, fields, contract versions, and governed skills fail closed;
- canonical projection divergence and authoritative symlinks fail.

Obsolete receipt, rolled-back-state, historical-hash, and transaction tests
were removed rather than preserved as compatibility behavior.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-boundary-first-validation.py` | pass; 51 tests |
| `python scripts/validate-boundary-first.py --check` | pass; pending two-state manifest |
| `python scripts/test-select-validation.py` | pass; 134 tests |
| `python -m py_compile scripts/boundary_first_validation.py scripts/validate-boundary-first.py scripts/test-boundary-first-validation.py` | pass |
| `git diff --check` | pass |

## Aligned-surface audit

- Feature spec, architecture, ADR, plan, and approved test spec already own the
  lightweight release-manifest contract.
- M1 reference projection and M2 governed skill instructions are unaffected;
  their byte and semantic tests remain in place.
- Existing adapter-distribution parsers and fixtures continue to own release
  metadata shape. M4 owns the narrow current-metadata selection integration,
  archive/package parity, and installed cold-read proof; M3 adds no parallel
  package parser or script.

## Handoff

M3 is ready for independent code-review against the approved R5 proof map.
M4 remains blocked until M3 review closes.
