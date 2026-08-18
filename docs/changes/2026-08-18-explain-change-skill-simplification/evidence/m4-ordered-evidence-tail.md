# M4 Ordered Final-Review Evidence Tail

Stage: implement
Milestone: M4
Status: review-requested

## Implemented contract

- Canonical code-state resolution derives the reviewed subject `S`, final-review recording revision `R`, explanation recording revision `E`, and handoff revision without placing `R` or `E` in the reviewed product-code identity.
- The pre-verify tail accepts exact linear non-merge `S -> R -> E`; exact `S -> R` remains the only recoverable partial state.
- `R` and `E` use separate exact path manifests and semantic `change.yaml` field allowlists. Unknown or sibling-owned fields fail closed.
- Verification readiness requires a complete ordered tail. Later explicitly bounded verify-owned evidence leaves the reviewed product identity and handoff revision unchanged.
- Published explain-change guidance and deterministic scenarios now describe the ordered tail and its ownership boundaries.

## Test-first evidence

The focused code-state tests were changed before production code. Their initial run failed on the former one-commit behavior, including the complete ordered tail, review-only recovery state, field ownership, and reversed-order cases. Production changes were then added to make those cases pass.

## Validation

- `python scripts/test-workflow-code-state.py` — passed, 17 tests.
- `python scripts/test-workflow-automation.py` — passed, 76 tests.
- Focused `ExplainChangeSkillSimplificationTests` loaded from `scripts/test-skill-validator.py` — passed, 10 tests.
- `python scripts/test-skill-validator.py` — passed, 418 tests with 16 documented skips.
- `python scripts/test-adapter-distribution.py` — passed.
- `python scripts/validate-skills.py skills/explain-change/SKILL.md` — passed.
- `python scripts/build-skills.py --check` — passed.
- `python scripts/validate-boundary-first.py --check --path specs/explain-change-skill-simplification.md` — passed.

## Real Git journey

`scripts/test-workflow-code-state.py` creates a temporary Git repository and proves `S -> R -> E -> verify`: exact review and explanation commits are derived, the public verify-facing ordered-tail predicate accepts them, `E` remains the handoff revision after the verify-owned commit, and the reviewed product identity remains stable. The same predicate rejects exact `S -> R` as incomplete for verify while code-state recovery preserves it for the unchanged explanation retry. The suite also rejects product code after review, reversed stage order, unknown shared-metadata fields, dirty worktrees, target drift, mutable reviewed-revision expressions, and untrusted provider substitution.

## Measurement

The largest loaded assembly remains below the frozen flat baseline:

| Assembly | Words | UTF-8 bytes | Frozen baseline words | Frozen baseline bytes |
| --- | ---: | ---: | ---: | ---: |
| `EC3` | 1,038 | 8,212 | 1,175 | 8,224 |

No new persistence surface, lifecycle state, runtime service, or write owner was introduced.
