# Governed test-spec authoring

Load after `SKILL.md` establishes `governed_test_spec_candidate_context`. The parent owns universal policy; this reference owns governed authoring transactions.

## Authority and writes

Read the complete current `change.yaml`. Require `lifecycle_contract: stage-owned-change-local-v1`; resolve one change ID, operation, stable artifact ID or intended ID, normalized canonical path, governing input identities, authoring-evidence path, and authority. Operations are `create-primary-test-spec`, `revise-primary-test-spec`, and `restart-stale-authoring`. Unknown operations or states fail first; invalid or caller-asserted evidence stops.

Write only the exact test-spec, its authoring evidence, and the same matching artifact entry and authoring transition. It must not mutate `workflow_state`, routing, automation, another entry, review evidence, implementation state, or downstream settlement. Workflow-managed execution does not enlarge this boundary.

## Create-primary-test-spec

Creation needs no existing file or entry. Prove one artifact ID, normalized path, evidence path, governing basis, and no collision, then:

1. Create the same entry at `authoring` with kind, role, path, and evidence path.
2. Write asset-composed content; compute its identity and basis.
3. Write complete bound authoring evidence and validate consistency.
4. Move only the same entry to `review-required`.

Creation must not write peer-review settlement, set `active`, mutate `workflow_state`, or authorize implementation; the skill must not authorize implementation.

Retry identity is change ID, artifact ID, normalized path, authoring-evidence path, and all governing input identities.

| State | Result |
| --- | --- |
| Matching entry only | Resume content. |
| Matching file; evidence incomplete | Validate the basis and complete evidence. |
| Complete basis at `authoring` | Validate and transition. |
| Complete basis at `review-required` | idempotent success; no write or occurrence. |
| Mismatch, collision, multiple candidate, or changed path | Stop. |
| Intended content or basis changed | `stale-authoring-attempt`; never rebind, revise, overwrite, or abandon implicitly. |

## Restart-stale-authoring

Restart applies only to one incomplete, unreviewed `authoring` entry with no downstream reliance. Preserve artifact ID, kind, role, same canonical path, and state; replace only its evidence path and bind current inputs. Record old/new bases and retry IDs, no-reliance proof, evidence paths, and required partial content. Never create another entry, terminal state, duplicate path, or review, workflow, or automation mutation. Invalid state or evidence stops; then rerun creation for the same entry.

## Revise-primary-test-spec

Revision requires one entry and file, prior content identity, current inputs, legal state, one authorizing finding or upstream-change identity, revision-authoring-evidence path, and no competing revision. Legal cases are `revision-required`, identical `authoring` retry, authorized pre-settlement correction, or reopened pre-reliance `active`; implementation reliance routes to governed reopen or migration.

Retry identity is change ID, artifact ID, normalized path, prior content identity, governing input identities, authorizing finding or upstream-change identity, and revision-authoring-evidence path. A changed component stops as another attempt.

1. Preserve prior authoring and review evidence.
2. Move only the matching entry to `authoring`, remove its current review mapping when required, and bind new evidence.
3. Write revised content without changing artifact ID or path; compute its new identity and basis.
4. Write and validate revision evidence.
5. Move only the matching entry to `review-required` for fresh independent `test-spec-review`.

An identical retry reconciles only that attempt. Unsupported state, stale authorizer, identity change, evidence loss, implementation reliance, or competing write stops.

## Result

Every success leaves the same entry at `review-required`. Only `test-spec-review` may settle it to `active`; workflow may route but cannot rewrite content or settlement. Return operation, identities, changes, validation, retry state, blockers, and handoff without downstream readiness claims.
