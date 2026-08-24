# M6 Blocker: Missing Governed Authoring Operation

## Conflict

The approved direction requires all governed lifecycle mutations to cross the CLI and requires migrated skills to stop directly mutating lifecycle fields. The closed first-release operation vocabulary nevertheless contains review/evidence registration, settlement, milestones, migration, and repair only. It has no operation that can register a newly authored or revised governed artifact and move its entry to `review-required`.

Affected contracts:

- Proposal section 6.1: all supported governed lifecycle mutations occur through the CLI.
- Spec R3: closed operation vocabulary has no authoring registration operation.
- Spec R28: governed skills must use the CLI instead of directly mutating lifecycle fields after enforcement.
- Current proposal/spec/architecture/plan/test-spec authoring skills: create or revise an artifact entry, invalidate prior review where applicable, record authoring evidence, and move the artifact to `review-required`.

## Impact

Review and settlement skills can be simplified now, but fully migrating authoring skills would require either:

1. retaining direct lifecycle mutation, contradicting the mandatory boundary; or
2. inventing an unapproved operation, contradicting the closed vocabulary and no-generic-setter requirement.

Mandatory enforcement therefore remains disabled and M6 cannot meet its completion criteria under the current specification.

## Recommended resolution

Add one narrow semantic operation, provisionally `record-artifact-revision`, which:

- accepts exact artifact ID, kind, role, repository-relative artifact and authoring-evidence paths, current lifecycle revision, stage authority, and prior artifact identity when revising;
- verifies the authored bytes and stage-owned evidence;
- creates or revises only the matching artifact entry;
- invalidates prior review/validation registrations for the replaced identity;
- derives `review-required` without accepting an arbitrary target state;
- never changes workflow routing or another artifact.

The spec, architecture, request fixtures, test specification, and M1 contract would require a bounded revision before implementation resumes.
