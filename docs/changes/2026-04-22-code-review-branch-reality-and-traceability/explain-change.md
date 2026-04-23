# Code Review Branch Reality And Traceability Explain Change

## Summary

This change implements the approved first slice for branch reality and traceability in repository workflow guidance. It updates the durable workflow rule, the short workflow summary, and the directly affected workflow-facing skills so review ownership, tracked branch authority, qualified readiness terms, and direct-proof expectations use the same contract.

## Problem

The repository had already tightened `code-review` independence, but a real project incident showed a remaining gap. Implementation-stage language could still sound like completed review, local-only artifacts could still be over-credited as branch authority, and named edge-case coverage could still be inferred from code shape instead of explicit proof.

## Decision trail

- Proposal: `docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md`
- Spec: `specs/code-review-branch-reality-and-traceability.md`
- Test spec: `specs/code-review-branch-reality-and-traceability.test.md`
- Plan: `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
- Milestone:
  - `M1`: implement branch-reality and traceability alignment

## Diff rationale by area

| File or area | Change | Reason |
| --- | --- | --- |
| `specs/rigorloop-workflow.md` | adds the enduring invariant for stage-owned language, tracked governing branch state, mixed-evidence review behavior, qualified readiness terms, and direct proof | the workflow-wide rule must not live only in the focused feature spec |
| `docs/workflows.md` | adds short-form execution-lane guidance for claim ownership, tracked authority, and direct proof | the contributor summary must stay truthful once the durable workflow rule changes |
| `skills/implement/SKILL.md` | narrows implementation closeout language so it cannot imply review findings or `branch-ready` | `implement` may report completion and readiness for `code-review`, but it does not own review conclusions |
| `skills/code-review/SKILL.md` | teaches review surface versus tracked governing branch state, mixed-evidence handling, and direct-proof expectations | `code-review` must separate inspectable diff context from the authority supporting clean branch-scoped conclusions |
| `skills/verify/SKILL.md` | makes `branch-ready` ownership explicit and blocks local-only authoritative support or unresolved direct-proof gaps | `verify` owns branch-scoped readiness, not a broad unqualified PR-ready claim |
| `skills/workflow/SKILL.md` | aligns orchestrator guidance with the new execution-stage ownership split | the full-feature lane should route and describe these claims consistently |
| `skills/pr/SKILL.md` and `skills/explain-change/SKILL.md` | removes live unqualified `PR-ready` wording in favor of explicit PR-stage handoff language | remaining unqualified uses should survive only as negative guidance or quoted definitions |
| `.codex/skills/` | regenerated from canonical `skills/` | generated compatibility output must stay synchronized with the authored guidance |

## Validation evidence

The implementation proof path passed with:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-artifact-lifecycle-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
- `rg -n 'review surface|tracked governing branch state|branch-ready|pr-body-ready|pr-open-ready|clean-with-notes|changes-requested|blocked|inconclusive|direct proof|PR-ready' skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md .codex/skills`
- `rg -n 'workflow|review|verify|pr-ready|branch-ready|pr-body-ready|pr-open-ready' AGENTS.md CONSTITUTION.md docs/workflows.md specs/rigorloop-workflow.md`
- `git diff --check -- specs/code-review-branch-reality-and-traceability.test.md specs/code-review-branch-reality-and-traceability.md specs/rigorloop-workflow.md skills/implement/SKILL.md skills/code-review/SKILL.md skills/verify/SKILL.md skills/workflow/SKILL.md skills/pr/SKILL.md skills/explain-change/SKILL.md docs/workflows.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability .codex/skills AGENTS.md CONSTITUTION.md docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/plan.md`
- `bash scripts/ci.sh`

The generated-skill proof needed one correction while the work was in progress: running `python scripts/build-skills.py` and `python scripts/build-skills.py --check` in parallel created a false drift failure, so the recorded passing evidence is the sequential rerun.

Residual unqualified `PR-ready` hits were manually classified. Surviving hits are negative guidance or quoted definitions in the workflow skill and spec surfaces, not live guidance in the touched execution-stage skills or workflow summary.

Additional review and verification evidence will be recorded here as the workflow-managed downstream stages complete.

## Scope control

- This slice stays wording-first. It does not add validator-backed enforcement for forbidden `implement` review language.
- It does not require committed-only review.
- It does not add a review router, readiness registry, or other orchestration subsystem.
- `AGENTS.md` and `CONSTITUTION.md` remain intentionally unchanged because M1 does not alter the concise repository summary or the governing principles enough to justify edits there.

## Risks and follow-ups

- Residual unqualified `PR-ready` hits must be manually classified so only negative guidance, historical context, or quoted definitions remain.
- The focused spec and `specs/rigorloop-workflow.md` must stay aligned so the enduring invariant is not duplicated inconsistently.
- A later follow-up may add validator-backed wording enforcement once the contract stabilizes, but that is out of scope for this v1 implementation.

## Readiness

This explain-change artifact is the durable reasoning surface for the implementation milestone.

Implementation is complete and the immediate next workflow-managed stage is `code-review`.
