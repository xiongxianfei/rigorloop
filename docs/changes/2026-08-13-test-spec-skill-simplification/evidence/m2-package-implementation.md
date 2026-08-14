# M2 Package Implementation Evidence

## Result

Milestone M2 implemented the compact universal `test-spec` contract, one conditionally loaded governed-authoring reference, and structural-only asset composition. The two existing boundary references remain initially loaded and byte-identical to baseline.

## Test-first proof

Before the package implementation, `python scripts/test-skill-validator.py TestSpecSkillSimplificationTests` failed because `references/governed-test-spec-authoring.md` did not exist. The focused assertions were then satisfied by the canonical package change.

## Ownership result

- `SKILL.md` owns universal proof policy, profiles, candidate classification, command and milestone proof, optional manual verification, stops, claims, resource triggers, and the compact boundary bridge.
- `references/governed-test-spec-authoring.md` owns exact creation, revision, stale-restart, retry, and authoring-state procedure.
- The existing boundary references retain detailed boundary and proof semantics.
- The skeleton owns document structure; the four row/body assets own their repeated structures.
- `TS-RULE-018` was corrected from `removed-duplicate` to `retained-inline` after implementation inspection confirmed that the contract requires the compact boundary bridge inline. This changes only its destination classification, not the frozen rule inventory.

## Loaded-profile evidence

Measurement uses LF-normalized canonical files, UTF-8 bytes, Unicode whitespace-separated words, documented load order, and each resource once.

| Profile | Baseline bytes | Final bytes | Delta | Baseline words | Final words | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `TSA0-portable` | 25,419 | 20,730 | -4,689 (-18.4%) | 3,640 | 2,817 | -823 (-22.6%) |
| `TSA1-governed` | 25,419 | 25,023 | -396 (-1.6%) | 3,640 | 3,380 | -260 (-7.1%) |

Both required procedural profiles are smaller in both primary metrics. Assets are excluded from procedural loaded-profile totals and will be accounted for separately in M3.

## Validation

- `python scripts/validate-skills.py`: passed; 24 canonical skills validated.
- `python scripts/test-skill-validator.py TestSpecSkillSimplificationTests`: passed; 6 tests.
- `python scripts/test-skill-validator.py`: passed; 330 tests with 16 skips.
- `python scripts/test-build-skills.py`: passed; 7 tests.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/validate-boundary-first.py --check --path specs/test-spec-skill-simplification.md`: passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-13-test-spec-skill-simplification/change.yaml`: passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-13-test-spec-skill-simplification`: passed.
- `git diff --check`: passed.

No target-agent runtime, transcript grading, network publication, or permanent simplicity/tokenizer validator was used.
