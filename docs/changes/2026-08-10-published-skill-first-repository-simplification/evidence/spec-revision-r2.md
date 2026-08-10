# Published-Skill-First Repository Simplification Spec Revision R2

Evidence ID: published-skill-first-spec-revision-r2
Artifact ID: spec
Stage: spec
Artifact: `specs/published-skill-first-repository-simplification.md`
Owning change record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`
Completion status: complete
Resulting review-request path: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/spec-review-r2.md`

## Trigger

Test-spec structural validation found that requirement ranges such as `R1-R29` are not valid serialized ID lists under `boundary-first-v1` and that E2, E4, and E5 cited boundaries not owned by every cited requirement.

## Correction

- Expanded requirement ranges into exact comma-separated stable IDs.
- Added R3 to semantic authority ownership.
- Narrowed E2 to R4, E4 to R6, and E5 to R9 with only the boundaries that directly govern those illustration outcomes.
- Made the same model-scope and proof-owner serialization correction in the draft proof map.

No requirement text, observable outcome, target, gate, compatibility disposition, architecture decision, plan milestone, or implementation authority changed.
