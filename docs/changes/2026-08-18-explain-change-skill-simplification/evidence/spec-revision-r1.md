# Spec Revision R1 Evidence

- Stage: spec
- Operation: `revise-primary-spec`
- Artifact ID: `spec`
- Spec: `specs/explain-change-skill-simplification.md`
- Prior identity: `sha256:4bb07c3be46d22e97ef1ffb874d83421e5311c3ed8621149c36b6e58fa99b5f8`
- Revised identity: `sha256:826cbf5c07be5dab2c4e4f2e4631799ba2caac6f46a4570fc78b7b0c3f4f3e15`
- Revision authority: explicit user instruction accepting the recommended resolution for `EXCSIM-CR2`
- Governing proposal review: `proposal-review-r3`
- Authoring status: complete
- Review request: `spec-review-r2`

## Resolution

R24-R29 now define one non-circular ordered stage-evidence tail:

```text
S: reviewed subject
-> R: final-review recording and its closed workflow transition
-> E: explanation recording and its closed workflow handback
-> verify
```

The contract separates all four revision identities, derives commit identities from Git after commit, and requires direct linear ancestry. It uses path-and-field ownership for shared files: `R` may contain only exact final-review evidence and matching workflow transition fields, while `E` may contain only the exact explanation artifact and matching workflow handback fields. Product code, tests, specs, architecture, plans, generated output, merges, intervening revisions, reordered evidence, other lifecycle state, and unlisted shared-file fields invalidate final-review reuse.

The revision also closes identical recovery when only `S -> R` exists, keeps later verify evidence outside the pre-verify tail, updates the boundary and interaction records, and adds an interrupted-recording example. It introduces no self-referential commit field, lifecycle state, persistence service, or cross-stage authority transfer.

The prior plan, test specification, architecture assessment, and implementation are stale relative to this revised spec and cannot authorize further execution until independent `spec-review`, bounded architecture reassessment, and downstream artifact reconciliation complete.

The revised spec returns to `review-required` and claims no approving rereview, architecture result, plan readiness, test-spec readiness, implementation correctness, verification, branch readiness, or PR readiness.
