# Code Review M2 R1: RigorLoop Published Skill Design Contract

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: commit `bea95ca` / M2 validator and fixture support
Status: changes-requested

Reviewed artifact: bea95ca
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: changes-requested
- Material findings: RLSDC-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/code-review-m2-r1.md
- Review log: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md
- Review resolution: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md#code-review-m2-r1
- Open blockers: RLSDC-M2-CR1
- Immediate next stage: review-resolution for M2
- No automatic downstream handoff: this isolated review does not start fixes.

## Scope

Reviewed implementation surface:

- commit `bea95ca` (`M2: validate published skill design contract checks`)
- `scripts/skill_validation.py`
- `scripts/test-skill-validator.py`
- `tests/fixtures/skills/published-design/`
- active plan and change metadata updates for M2

Governing artifacts checked:

- `specs/skill-contract.md`, R29, R32, R33, R35, R36
- `specs/skill-contract.test.md`, T17 through T20
- `docs/plans/2026-05-19-rigorloop-published-skill-design-contract.md`, M2

## Diff Summary

M2 adds deterministic published-skill validation checks for description length, `when_to_use` replacement, packaged resource maps, packaged script resource-map fields, and repository-root dependency wording. It also adds published-design fixtures and records M2 validation and handoff state.

## Findings

### RLSDC-M2-CR1 - Repository-root script dependency check misses ordinary `Run scripts/...` wording

Finding ID: RLSDC-M2-CR1
Severity: major

Location:

- `scripts/skill_validation.py:67`
- `scripts/skill_validation.py:371`
- `tests/fixtures/skills/published-design/required-root-script/SKILL.md:20`

Evidence:

The new self-containment check matches repository-root-like paths, including `scripts/`, but only evaluates a line as required when `READABILITY_REQUIRED_CONTEXT_PATTERN` matches. That pattern includes words such as `must`, `required`, `read`, `open`, and `before proceeding`, but not ordinary command verbs such as `run`, `execute`, or `invoke`. The M2 negative fixture only covers `Before proceeding, run \`scripts/validate-internal.py\`.`

Direct proof:

Changing the same negative fixture line to `Run \`scripts/validate-internal.py\` for validation.` makes `python scripts/validate-skills.py <temp-fixture>` pass, even though the line still requires a repository-root `scripts/` dependency.

Problem:

R33a requires published skills not to require unavailable repository-root `scripts/` dependencies as normal customer-project dependencies. T18 also requires self-containment validation to block repository-root internal paths while distinguishing packaged skill resources. A validator that only catches "before proceeding" style wording leaves a common required-script formulation unblocked.

Required outcome:

Static validation must reject required repository-root `scripts/` dependencies expressed with ordinary imperative command wording such as `Run`, while still allowing mapped packaged skill-local scripts.

Safe resolution path:

- Add a published-self-containment command-context pattern for `run`, `execute`, `invoke`, and equivalent deterministic command verbs when the matched path is repository-root-like.
- Add a fixture that fails for `Run \`scripts/validate-internal.py\` for validation.`
- Keep or add a passing fixture for an actual skill-local packaged script with a valid `Resource map`, so R32d/R33c remain covered.

## Checklist Coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R33a/R33c are only partially satisfied; repository-root `scripts/` requirements expressed with `Run` can pass. |
| Test coverage | concern | Fixture coverage catches `Before proceeding, run ...` but misses the more common `Run scripts/...` required-command wording. |
| Edge cases | concern | The packaged-script-vs-root-script edge case is under-tested for command verbs. |
| Error handling | pass | Validator returns stable error strings for the cases it detects. |
| Architecture boundaries | pass | No runtime architecture or adapter root behavior changed. |
| Compatibility | pass | Canonical skills still validate; M2 does not rewrite skill bodies. |
| Security/privacy | pass | No secret handling or sensitive runtime value exposure changed. |
| Derived artifact currency | pass | No generated skill or adapter output changed in M2. |
| Unrelated changes | pass | Diff is limited to M2 validator/tests/fixtures and lifecycle evidence, plus M1 review recording committed with the handoff. |
| Validation evidence | concern | `python scripts/test-skill-validator.py` and selected CI pass, but they do not cover the missed root-script command wording. |

## No-Finding Rationale

Not applicable. One material finding remains open.

## Handoff

M2 requires review-resolution for RLSDC-M2-CR1 before rerun code-review.

Next stage: `review-resolution` for M2.

Do not claim final verification, branch readiness, PR readiness, or final closeout from this review. M2 remains open and M3 remains unimplemented.
