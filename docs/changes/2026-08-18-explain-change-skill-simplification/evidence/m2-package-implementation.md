# M2 package implementation

Milestone: M2

## Implemented contract

- Replaced the flat package with a compact universal skill, one governed-workflow reference, and one structural skeleton.
- Kept actual-diff grounding, evidence truthfulness, tri-state signal classification, independent output actions, resource failures, whole-file atomic replacement, claims, stops, and universal compatibility text inline.
- Moved governed eligibility, closeout, reviewed-subject basis, the closed one-commit evidence tail, staleness, and neutral workflow handback into the conditional reference.
- Required durable create and refresh to compose the complete current skeleton; no section parser or mixed-ownership refresh was introduced.
- Extended workflow verification evidence with reviewed-subject revision, explanation basis, and validation-evidence cutoff.
- Restricted post-review Git state to the reviewed subject or exactly one direct-child lifecycle-evidence commit; multiple evidence commits now fail closed.

## Loaded profiles

| Profile | Words | UTF-8 bytes | Baseline words | Baseline bytes |
| --- | ---: | ---: | ---: | ---: |
| EC0 portable inline | 555 | 4,472 | 1,175 | 8,224 |
| EC1 portable durable | 719 | 5,526 | 1,175 | 8,224 |
| EC2 governed inline | 852 | 7,031 | 1,175 | 8,224 |
| EC3 governed durable | 1,016 | 8,085 | 1,175 | 8,224 |

All four real loaded profiles strictly decrease in words and bytes. M3 retains the independent measurement and package-parity gate.

## Validation

- `python scripts/validate-skills.py skills/explain-change/SKILL.md` — passed.
- `python scripts/test-skill-validator.py ExplainChangeSkillSimplificationTests` — passed, 10 tests.
- `python scripts/test-workflow-code-state.py` — passed, 14 tests.
- `python scripts/test-workflow-automation-state.py` — passed, 65 tests.
- `python scripts/test-workflow-automation.py` — passed, 76 tests.
- `python scripts/test-skill-validator.py` — passed, 418 tests with 16 expected skips.
- `python scripts/test-build-skills.py` — passed, 7 tests.
- `python scripts/build-skills.py --check` — passed.

The EXCSIM-CR1 correction reran the focused repository-backed readiness test, all 14 Git code-state tests, all 76 workflow-automation tests, all 418 skill-validator tests, all 7 build tests, and check-mode generation; all passed.

No target-agent runtime, prose grader, new parser, new lifecycle state, or new persistence owner was introduced.
