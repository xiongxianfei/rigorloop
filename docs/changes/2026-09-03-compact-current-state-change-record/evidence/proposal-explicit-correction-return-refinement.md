# Proposal refinement: explicit correction return

Artifact path: docs/proposals/2026-09-03-compact-current-state-change-record.md
Artifact identity: sha256:a624830dce34f96427044039c33c32dc9f37da26268c89603e35b75df5e0708f
Authoring result: complete

## Result

The proposal now distinguishes the ordinary adjacent review loop from an explicit non-adjacent correction. Explicit return means that exact corrected content is ready for its required review; it does not approve or close the correction.

Review settlement keeps findings in correction authoring, retains blocked or inconclusive review state, or closes an approved correction. The CLI derives the earliest downstream gate that must be re-established and exposes that path through projection rather than storing a caller-maintained invalidation list.

## Handoff

The exact revised proposal requires fresh Proposal Review. This evidence does not claim acceptance or downstream readiness.
