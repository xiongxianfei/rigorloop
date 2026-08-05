# M3 selector-routing evidence

## Scope

Milestone M3 removes `artifact_lifecycle.validate` from canonical published skill paths. Generated skill paths already used only derivation checks. Actual lifecycle artifacts and change records retain lifecycle validation.

## Routing results

| Changed set | Result |
| --- | --- |
| `skills/spec/SKILL.md` | Selects boundary, skill, generation, drift, adapter, and prose checks; no lifecycle check |
| `.codex/skills/spec/SKILL.md` | Selects generation regression and drift; no lifecycle check |
| Lifecycle artifact matrix | Proposal, spec, test spec, architecture, ADR, plan, review-resolution, and change metadata remain lifecycle protected |
| Skill plus feature spec | Retains both families; lifecycle paths contain only the feature spec, while boundary paths contain both surfaces |
| Selector implementation and tests | Selects `selector.regression` |

Classification depends only on the path contract. Lifecycle-like words in published skill prose do not affect routing.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-select-validation.py` | pass, 141 tests |
| `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md` | pass, no lifecycle check |
| `python scripts/select-validation.py --mode explicit --path skills/spec/SKILL.md --path specs/progressive-boundary-first-skill-guidance.md` | pass, lifecycle path scoped to the feature spec |
| `python scripts/test-artifact-lifecycle-validator.py` | pass, 162 tests |
| `git diff --check` | pass |

## Recovery

The behavior change is one selector call removal under the canonical `skills` category. Reverting that call and the focused expectations restores the former extra lifecycle route without changing the lifecycle validator.
