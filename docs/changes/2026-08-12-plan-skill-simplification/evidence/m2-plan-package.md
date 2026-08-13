# M2 Plan Package Evidence

Date: 2026-08-13
Milestone: M2

## Outcome

The canonical `plan` package now has a shorter self-contained portable contract, one mapped governed-authoring reference, the unchanged boundary-first reference, and exactly three structural assets. New milestone copies contain stable execution intent and no mutable milestone state.

## Ownership proof

- `skills/plan/SKILL.md` owns portable planning quality, classification, universal safety, claims, handoff, and exact resource triggers.
- `skills/plan/references/governed-plan-authoring.md` owns only `create-primary-plan`, `revise-primary-plan`, and `initialize-approved-plan` procedure.
- `skills/plan/references/boundary-first-method-v1.md` retains detailed boundary procedure under its existing trigger.
- The three assets own structure only; `assets/milestone.md` no longer emits `Milestone state` or execution progress.
- `skills/plan-review/SKILL.md` records clean judgment before initialization and settles only after the matching initialization retry.
- `skills/workflow/SKILL.md` coordinates retry and owns later lifecycle transitions without enlarging plan's write authority.

## Preservation evidence

The rule-disposition ledger accounts for 15 behavior clusters with one destination each. The literal-compatibility inventory classifies 13 exact dependencies separately from semantic rules. Fourteen static scenarios cover valid profiles, operations, missing resources, state ownership, and unknown ledger values. Unknown dispositions and classifications fail closed in focused tests.

## Preliminary profile evidence

Measurements use canonical LF-normalized content and count each unique procedural resource once.

| Profile or package | Baseline words | Current words | Baseline bytes | Current bytes | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `PL0` | 2555 | 1988 | 18680 | 14888 | reduced |
| `PL1` | 2555 | 2442 | 18680 | 18398 | reduced |
| Total package | 3775 | 3661 | 27886 | 27619 | reduced |

The governed profile improvement is deliberately smaller because universal safety and planning quality remain inline. Final M3 evidence will record every profile, file identity, and package-chain result.

## Validation

- `python scripts/validate-skills.py skills/plan/SKILL.md` — passed; one canonical skill validated.
- `python scripts/test-skill-validator.py` — passed; 317 tests, 16 skipped.
- `python scripts/test-build-skills.py` — passed; 7 tests.
- `python scripts/build-skills.py --check` — passed.

No target-agent runtime, tokenizer dependency, or permanent simplicity validator was introduced.
