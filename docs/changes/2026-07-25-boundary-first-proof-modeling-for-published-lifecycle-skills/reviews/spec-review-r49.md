# Boundary-First Proof Modeling Spec Review R49

Review ID: spec-review-r49
Stage: spec-review
Round: 49
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.md and specs/rigorloop-workflow.test.md
Reviewed artifact: focused three-category runtime-projection amendment at 4b601220
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR49-1, BFP-SR49-2, BFP-SR49-3
Immediate next stage: spec
Eventual test-spec readiness: not-ready
Architecture assessment: architecture-required
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `4b601220c897734eb1aebb60aaf91af42f960013`

Reviewed spec identity:
`sha256:e9343cceab549f158cdb7f272c9bb991ed0a14a5d7542058ce2273dc83f53c04`

## Result

Changes requested.

The eleven-field 3/4/89 projection and recomputed identity are directionally
correct, but three closed contracts remain incomplete:

- `BFP-SR49-1`: each projection collection must equal its corresponding
  feature-classification category, with count-preserving category swaps
  rejected before thread start;
- `BFP-SR49-2`: the recorded preflight failure used a diagnostic phase that
  the closed cause-to-phase table does not permit and must be retained only as
  nonconforming discovery evidence; and
- `BFP-SR49-3`: the proof map still claims readiness and identities from the
  superseded R48/R22/R17 inputs.

## Required outcome

Revise the spec and proof map to bind category equality, preserve the existing
closed diagnostic phase table, add direct contrast proof, and mark downstream
architecture, plan, and test-spec identities pending until their focused
rereviews approve the correction.

## Material findings

### BFP-SR49-1 — Projection collections are not bound to classification categories

Finding ID: BFP-SR49-1

Severity: major

Evidence:

Counts, uniqueness, disjointness, and exhaustiveness permit a count-preserving
member swap between two feature categories.

Required outcome:

Bind every projection collection by exact equality to its corresponding
feature-classification category and reject category disagreement before thread
start.

Safe resolution:

Add the three equality rules and direct pairwise swap contrasts.

### BFP-SR49-2 — Discovery receipt uses a forbidden diagnostic phase

Finding ID: BFP-SR49-2

Severity: major

Evidence:

The discovery receipt pairs `file-change-control-mismatch` with
`pre-thread-start`, while the closed observed causes map to `pre-turn-start`.

Required outcome:

Retain the receipt only as nonconforming historical discovery evidence and
prove corrected cause-to-phase behavior.

Safe resolution:

Add the exact receipt as a negative fixture and preserve the closed phase
table.

### BFP-SR49-3 — Proof-map identities and readiness are stale

Finding ID: BFP-SR49-3

Severity: major

Evidence:

The proof map still names R48/R22/R17 identities and claims no blocking gap
after those inputs changed.

Required outcome:

Mark affected identities and readiness pending through focused upstream
rereviews.

Safe resolution:

Synchronize exact identities only after spec, architecture, and plan approval,
then rerun test-spec review.

## Readiness

Not ready for architecture or implementation. The immediate next stage is a
focused spec revision followed by spec-review R50.
