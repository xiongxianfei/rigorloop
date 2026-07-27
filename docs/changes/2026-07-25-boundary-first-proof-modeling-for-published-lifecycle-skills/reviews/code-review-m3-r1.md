# Code Review M3 R1

Review ID: code-review-m3-r1

Stage: code-review

Round: 1

Reviewer: Codex code-review skill

Target: M3 implementation at `c5f63f83`

Reviewed artifact: implementation diff `1440c246..c5f63f83`

Reviewed milestone: M3

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M3-1

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m3-implementation

Reviewer context ID: boundary-m3-review-r1-reset

Context separation mechanism: blind-first diff and generated-evidence
inspection before reading the validation summary

Risk tier: elevated

Risk-tier triggers: generated evidence, behavior-preservation claims, public
skill behavior, and downstream capability aggregation

Risk-tier classifier: generated-evidence, requirement-fidelity, and
public-skill triggers

Governing artifacts: `specs/skill-contract.md` R56f-R56l;
`specs/skill-contract.test.md` T52, T53, T59;
`specs/rigorloop-workflow.md` R28f-R28j, R28y;
`docs/plans/2026-07-25-boundary-first-proof-modeling.md` M3

Formal criteria: stage-owned downstream responsibilities, exact current
identity and origin proof, 40-key completeness, no upstream reinvocation,
semantic-preservation claim boundary, and fail-closed contrasts

Initial packet inventory: specs/skill-contract.md@c5f63f83#sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc; specs/skill-contract.test.md@c5f63f83#sha256:586e77d3b9587dcc016c447eb499eff5b0855ed0e77381b2368a4c62ca92da5d; specs/rigorloop-workflow.md@c5f63f83#sha256:7b035049f01e8e197809e79dbfb7f8481a2c61f63fc3bf992116544a4250c819; docs/plans/2026-07-25-boundary-first-proof-modeling.md@c5f63f83#sha256:3994e64f856b4aebabed5ce78e6208603cbddd5b6471959710110b7817db70a5; scripts/boundary_proof_behavior.py@c5f63f83#sha256:57847dd436323d9a2db2cbd6b425ff38e4cc64f1fb3fcbc412fb8386e9f4c7ba; scripts/test-boundary-proof.py@c5f63f83#sha256:5f3c058acba282f4270fc54bed898c544c939b25795548dc8a060978e2e0a053; docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/evidence/preservation/manifest.json@c5f63f83#sha256:9472ae42c47b7bc0862503c42b594b89d0fb78e9a84130f5e042bad1c1cff433

Prompt template version: code-review-template-v1

Initial packet hash: sha256:4720bb89bb0b532b21ce943d82a8fb3d2f963750192df4a4c8d56ce24bb5bfc2

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

## Independent risk map

Affected behavior: downstream boundary guidance, packaged reference mapping,
historical materialization, current identity validation, and preservation
claims.

Highest-impact failure modes: structural evidence presented as semantic
preservation, missing category behavior hidden by duplicated snapshots, stale
or cross-skill evidence, or public skill authority expansion.

Changed boundaries: structural identity versus semantic behavior;
implementation-owned evidence versus reviewer-owned judgment; historical
origin versus current materialization.

Evidence expected: exact 40-key manifest, origin/current identity checks,
unknown/missing/duplicate/stale/cross-skill contrasts, stage-specific skill
proof, and an explicit semantic-review boundary.

Areas requiring direct inspection: `generate_preservation`,
`validate_preservation`, M3 negative tests, all four downstream skill edits,
and the generated after records.

Areas intentionally out of scope: M4, final holistic review, final verify,
release activation, PR, and deployment.

Risk classes considered: authorization=applicable; generated
evidence=applicable; validation=applicable; requirement fidelity=applicable;
release=not-applicable

Falsifiable review questions: Can the harness report category preservation
`pass` even when it never evaluates category semantics?

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, review log, review resolution, change metadata, and plan handoff
- Open blockers: BFP-CR-M3-1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M3-1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: open
- Finding IDs: BFP-CR-M3-1
- Verify readiness: not-claimed

## Review findings

Finding ID: BFP-CR-M3-1

Severity: major

Location: `scripts/boundary_proof_behavior.py` preservation result assembly and
validation; generated `evidence/preservation/*/after/` records

Evidence: Every after record is emitted with `result: pass` from only the pair
key, historical identity, current skill/resource identity, and a constant
`semantic_review_required: true`. The validator compares that same
self-authored shape but never evaluates behavior, claim boundary, review
recording, isolation, or handoff. The five before files per skill are identical
whole-skill snapshots, so the 40 labels do not constitute 40 semantic results.

Required outcome: Keep machine-owned origin, identity, completeness, and
no-reinvocation proof distinct from reviewer-owned semantic preservation.
Generated pair results must not claim unqualified preservation pass before
semantic review. Add direct proof that all four downstream skills contain their
stage-owned R56 responsibilities and that missing responsibilities fail.
The approving rereview must record the semantic five-category matrix for all
eight skills.

Safe resolution path: Change generated results and the command verdict to an
explicit structural status, add a closed downstream responsibility projection
with positive and missing-phrase tests, regenerate the current evidence, and
use code-review R2 to record the 8-by-5 semantic preservation decision.

## Validation evidence

The submitted validation commands pass, but they prove only the structural
and identity scope described above. Green tests do not resolve the semantic
claim mismatch.

## Handoff

M3 remains open in resolution-needed state. Record and implement
BFP-CR-M3-1 before rereview. M4 and final closeout remain blocked.
