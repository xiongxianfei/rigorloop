# Proposal refinement: derived compact state

Artifact path: docs/proposals/2026-09-03-compact-current-state-change-record.md
Artifact identity: sha256:755823b25a7aa820f57b9da2f4b7a72949e27b54929d705c8f542580cf8ba1a6
Authoring result: complete

## Result

The proposal now requires the CLI to construct lifecycle coordination from semantic input, derive allowed operations, check explicit subject identities without Git or PR data, and apply compact v1 only to newly created changes.

## Validation

- The five-surface current-state direction is unchanged.
- Caller authentication and caller-constructed coordinator state remain excluded.
- In-flight legacy changes finish under their existing contract; compact v1 has no migration writer.

## Handoff

The materially refined proposal requires fresh Proposal Review. This evidence does not claim acceptance.
