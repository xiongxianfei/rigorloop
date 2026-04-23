# Code Review Branch Reality And Traceability Explain Change

## Summary

This initiative implements the approved first slice for branch reality and traceability in repository workflow guidance, then closes the overlap drift that review exposed afterward. The main implementation aligned the durable workflow rule, the short workflow summary, and the directly affected workflow-facing skills around stage-owned claims, tracked governing branch authority, qualified readiness terms, and direct-proof expectations. Two 2026-04-23 follow-ups then removed the last conflicting live guidance: the mixed-evidence status rule in the older `code-review` independence surfaces, and the stale broad `PR readiness` wording in two overlap specs that should have been using `branch-ready`.

## Problem

The repository had already tightened `code-review` independence, but a real project incident showed a remaining gap. Implementation-stage language could still sound like completed review, local-only artifacts could still be over-credited as branch authority, and named edge-case coverage could still be inferred from code shape instead of explicit proof. After the first implementation landed, isolated review also showed that older approved overlap surfaces could still contradict the new mixed-evidence rule or the newer `branch-ready` ownership split if they were left untouched.

## Decision trail

- Proposal: `docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md`
- Spec: `specs/code-review-branch-reality-and-traceability.md`
- Test spec: `specs/code-review-branch-reality-and-traceability.test.md`
- Architecture: none. The approved spec and plan both kept this slice below the architecture threshold.
- Plan: `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`
- Milestone:
  - `M1`: implement branch-reality and traceability alignment
- Review-resolution follow-ups:
  - align the mixed-evidence status rule across the canonical `code-review` skill and the earlier approved `code-review` independence spec/test surfaces
  - replace the last live broad `PR readiness` wording in `specs/plan-index-lifecycle-ownership.md` and `specs/rigorloop-workflow.md` with `branch-ready`

## Diff rationale by area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `specs/rigorloop-workflow.md` | adds the enduring invariant, then narrows the remaining lifecycle-state overlap from broad `PR readiness` to `branch-ready` | the workflow-wide rule must not live only in the focused feature spec, and later overlap cleanup must not leave the durable spec semantically behind | focused spec `R1`-`R4e` and plan `M1` | focused test spec `T4`, targeted terminology scan, isolated clean local code-review and verify rerun |
| `docs/workflows.md` | adds short-form execution-lane guidance for claim ownership, tracked authority, and direct proof | the contributor summary must stay truthful once the durable workflow rule changes | focused spec `R1`, `R2`, `R3` | focused test spec `T1`-`T5` |
| `skills/implement/SKILL.md` | narrows implementation closeout language so it cannot imply review findings or `branch-ready` | `implement` may report completion and readiness for `code-review`, but it does not own review conclusions | focused spec `R1a`-`R1c` | focused test spec `T1` |
| `skills/code-review/SKILL.md` | teaches review surface versus tracked governing branch state, then receives the mixed-evidence wording fix | `code-review` must separate inspectable diff context from tracked authority and must not force `inconclusive` when the review surface independently supports a finding | focused spec `R2d`-`R2k`; earlier independence compatibility rule | focused test spec `T3`, overlap rerun on `5a15a5c^..5a15a5c` |
| `skills/verify/SKILL.md` | makes `branch-ready` ownership explicit and blocks local-only authoritative support or unresolved direct-proof gaps | `verify` owns branch-scoped readiness, not a broad unqualified PR-ready claim | focused spec `R1d`-`R1f`, `R2l`-`R2n`, `R3e` | focused test spec `T4`, `T5` |
| `skills/workflow/SKILL.md` | aligns orchestrator guidance with the new execution-stage ownership split | the full-feature lane should route and describe these claims consistently | focused spec `R1`-`R4` | focused test spec `T1`, `T4`, `T7` |
| `skills/pr/SKILL.md` and `skills/explain-change/SKILL.md` | removes live unqualified `PR-ready` wording in favor of explicit PR-stage handoff language | remaining unqualified uses should survive only as negative guidance or quoted definitions | focused spec `R1e`, `R1f`, `R2m`, `R2n` | focused test spec `T4` |
| `specs/code-review-independence-under-autoprogression.md` and `.test.md` | aligns the older approved overlap contract with the mixed-evidence rule | the repository cannot keep two authoritative `code-review` status contracts that disagree | focused spec compatibility rule `R4b` | isolated clean rerun on `5a15a5c^..5a15a5c` |
| `specs/plan-index-lifecycle-ownership.md` | replaces the remaining live verify-owned `PR readiness` wording with `branch-ready` | the lifecycle-ownership overlap spec must use the same qualified readiness term as the new durable workflow invariant | focused spec `R1d`, `R1f`, `R2l`-`R2n`, `R4c` | local spec-overlap review/verify rerun |
| `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md` and `change.yaml` | records the mixed-evidence follow-up, the later spec-overlap fix, and the isolated validation evidence | the initiative artifacts must stay truthful as local review-resolution work continues | workflow contract and plan bookkeeping rules | targeted lifecycle and metadata validation |
| `.codex/skills/` | regenerated from canonical `skills/` during the main implementation | generated compatibility output must stay synchronized with the authored guidance | plan `M1` | `build-skills` and `build-skills --check` |

## Tests added or changed

- `specs/code-review-branch-reality-and-traceability.test.md` is the focused proof surface for stage-owned language, the glossary split, mixed-evidence outcomes, qualified readiness terms, direct-proof requirements, and compatibility with the earlier `code-review` independence contract.
- `specs/code-review-independence-under-autoprogression.test.md` was updated in the mixed-evidence follow-up so the older overlap proof surface now matches the newer rule: missing authoritative artifacts block `clean-with-notes`, but they do not erase a supported `changes-requested` or `blocked` finding.
- No runtime unit or end-to-end tests were added because this slice changes workflow contract and contributor-facing guidance rather than product runtime behavior.

## Validation evidence

The main implementation proof path passed with:

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

The mixed-evidence review-resolution follow-up then passed with:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-branch-reality-and-traceability.md --path specs/rigorloop-workflow.md --path specs/code-review-branch-reality-and-traceability.test.md --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/code-review-independence-under-autoprogression.md --path specs/code-review-independence-under-autoprogression.test.md`
- `git diff --check -- skills/code-review/SKILL.md .codex/skills/code-review/SKILL.md specs/code-review-independence-under-autoprogression.md specs/code-review-independence-under-autoprogression.test.md`
- `bash scripts/ci.sh`

The later local spec-overlap follow-up then passed with:

- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/plan-index-lifecycle-ownership.md --path specs/rigorloop-workflow.md`
- `rg -n '\bPR-ready\b|\bPR readiness\b|\bbranch-ready\b' specs/plan-index-lifecycle-ownership.md specs/rigorloop-workflow.md`
- `git diff --check -- specs/plan-index-lifecycle-ownership.md specs/rigorloop-workflow.md`
- `python scripts/validate-change-metadata.py docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md --path specs/plan-index-lifecycle-ownership.md --path specs/rigorloop-workflow.md`
- `rg -n '^## (Active|Blocked|Done|Superseded)$|2026-04-22-code-review-branch-reality-and-traceability' docs/plan.md`
- `git diff --check -- docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md docs/changes/2026-04-22-code-review-branch-reality-and-traceability/change.yaml specs/plan-index-lifecycle-ownership.md specs/rigorloop-workflow.md`

Review and verification outcomes across the initiative were:

- first-pass `code-review` on `297a010^..55255a8`: `clean-with-notes`
- mixed-evidence rerun `code-review` on `5a15a5c^..5a15a5c`: `clean-with-notes`
- isolated local `code-review` on `specs/plan-index-lifecycle-ownership.md` and `specs/rigorloop-workflow.md`: `clean-with-notes`
- mixed-evidence follow-up `verify`: `ready`
- local spec-overlap follow-up `verify`: `ready`

Residual unqualified `PR-ready` hits were manually classified. Surviving hits are negative guidance, historical context, or quoted definitions, not live guidance in the touched execution-stage skills or live overlap specs.

Hosted CI remains unobserved from this environment. `bash scripts/ci.sh` passed during the main implementation and mixed-evidence follow-up, but it was not rerun for the final narrow local spec-and-bookkeeping follow-up because that last step only changed two live specs plus lifecycle bookkeeping.

## Alternatives rejected

- Leaving the focused branch-reality spec as the only corrected authority. That would have left older approved overlap specs contradicting the live contract.
- Treating missing authoritative artifacts as an automatic `inconclusive` in all cases. The approved mixed-evidence rule keeps supported `changes-requested` and `blocked` findings intact.
- Rewriting every historical `PR-ready` reference in one pass. This slice updates live authoritative surfaces and allows archived or quoted historical usage to remain non-operative.
- Adding validator-backed enforcement for forbidden `implement` review language in v1. The approved plan explicitly defers that to a later initiative after the wording pattern stabilizes.

## Scope control

- This slice stays wording-first. It does not add validator-backed enforcement for forbidden `implement` review language.
- It does not require committed-only review.
- It does not add a review router, readiness registry, or other orchestration subsystem.
- `AGENTS.md` and `CONSTITUTION.md` remain intentionally unchanged because M1 does not alter the concise repository summary or the governing principles enough to justify edits there.
- The archived `specs/plan-index-lifecycle-ownership.test.md` surface was left untouched because it is historical, not a current authoritative proof surface.

## Risks and follow-ups

- The current follow-up is still local in this workspace and has not yet been carried through a fresh PR branch.
- Hosted CI is still unobserved for the final narrow local follow-up.
- Residual unqualified `PR-ready` hits must continue to be manually classified so only negative guidance, historical context, or quoted definitions remain.
- The focused spec and `specs/rigorloop-workflow.md` must stay aligned so the enduring invariant is not duplicated inconsistently.
- A later follow-up may add validator-backed wording enforcement once the contract stabilizes, but that is out of scope for this v1 implementation.

## Readiness

This explain-change artifact is the durable reasoning surface for the implementation milestone and the 2026-04-23 local review-resolution follow-ups.

The local spec-overlap follow-up passed isolated `code-review` and `verify`, and the active plan and active test spec now record that downstream state.

The tracked initiative is done on-branch and ready for `pr`.
