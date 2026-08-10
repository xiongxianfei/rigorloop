# Published-Skill-First Repository Simplification Test-Spec Authoring

Evidence ID: published-skill-first-test-spec-authoring
Artifact ID: test-spec
Stage: test-spec
Artifact: `specs/published-skill-first-repository-simplification.test.md`
Owning change record: `docs/changes/2026-08-10-published-skill-first-repository-simplification/change.yaml`
Completion status: complete
Resulting review-request path: `docs/changes/2026-08-10-published-skill-first-repository-simplification/reviews/test-spec-review-r1.md`

## Inputs

- Approved feature spec and `spec-review-r1`.
- Approved canonical architecture, accepted ADR, and `architecture-review-r2`.
- Approved execution plan and `plan-review-r1`.
- `boundary-first-v1` compact core and proof guidance.
- Existing skill, adapter, release, lifecycle, change-metadata, review, selector, and npm package test conventions.

## Authoring result

The test spec maps all 29 requirements, 12 acceptance criteria, eight examples, eight edge cases, eight approved boundaries, and five selected interactions to 16 stable test cases and 13 proof obligations.
All six implementation milestones have separate test, command, evidence, review, and recovery obligations.
M6 requires each ledger-eligible deletion to close as a separately recorded sub-slice before aggregate cutover closeout.

The command ledger distinguishes existing commands from planned M1 and M3 commands, assigns first-required milestones, defines zero-test behavior, and bounds all execution to repository-local or temporary artifacts.
MP1 owns semantic skill review.
No runtime, prompt, transcript, model selection, network publication, or LLM-output evidence is admitted.
No uncovered proof gap remains.

## Authoring checks

- The normative test-spec and repeated-row assets were used.
- Every boundary and interaction ID is copied unchanged from the approved feature spec.
- Existing scripts and fixtures were inspected for feasible command ownership; implementation validation commands were not executed during authoring.
- The proof map preserves exact upstream stop conditions and does not invent new behavior.
