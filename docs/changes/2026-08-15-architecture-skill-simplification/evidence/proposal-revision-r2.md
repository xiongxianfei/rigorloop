# Proposal Revision Evidence R2: Architecture Skill Simplification

Stage: proposal
Date: 2026-08-15
Artifact ID: `proposal`
Artifact: `docs/proposals/2026-08-15-architecture-skill-simplification.md`
Revision authority: accepted findings `ARSIM-PR4`, `ARSIM-PR5`, and `ARSIM-PR6` from `proposal-review-r2`
Completion status: complete
Review request: `proposal-review-r3`

## Resolution summary

| Finding | Revision |
| --- | --- |
| `ARSIM-PR4` | Bound workflow-managed authoring to one current required assessment, exact spec identity, and approving spec-review identity, with explicit staleness and portable applicability rules. |
| `ARSIM-PR5` | Required the complete manifest and intended file identities to be durably prepared on the existing authoring-evidence surface before the first target write. |
| `ARSIM-PR6` | Added dependency edges, commit groups, intermediate-validity checks, canonical-package commit order, and deterministic ADR supersession order. |

## Architecture condition

The expected result remains `architecture-not-required` only if the existing authoring-evidence model supports prepared manifests, per-target progress, dependency edges, and commit groups without a new schema, persistent authority, or write owner. Otherwise the downstream assessment must return `architecture-required`.

## Validation

- `python scripts/validate-change-metadata.py docs/changes/2026-08-15-architecture-skill-simplification/change.yaml`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-08-15-architecture-skill-simplification`
- `python scripts/validate-documentation-prose.py --mode enforce --path docs/proposals/2026-08-15-architecture-skill-simplification.md --path docs/changes/2026-08-15-architecture-skill-simplification/evidence/proposal-revision-r2.md`
- `git diff --check`

The revised proposal is ready for independent same-stage rereview and claims no specification or downstream readiness.
