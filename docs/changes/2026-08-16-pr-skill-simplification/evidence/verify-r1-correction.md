# Verify R1 correction: PR review-summary compatibility

## Reproduction

Expected behavior: the universal PR contract summarizes review resolution as
counts by disposition, links `review-resolution.md`, blocks `needs-decision`,
and does not duplicate every detailed finding.

Actual behavior: final PR-mode CI failed
`test_review_stage_skills_align_with_review_resolution_contract` because the
simplified `skills/pr/SKILL.md` omitted `counts by disposition`. The same test
would subsequently have found the omitted `do not duplicate every detailed
finding` phrase.

## Root cause

This was a compatibility-preservation regression. M1's literal inventory did
not classify the two shared review-summary phrases, and the focused PR
simplification suite did not assert them. Semantic compression therefore
removed a universal output constraint even though the repository-wide review
artifact suite still owned it.

## Test-first proof

`test_review_resolution_summary_contract_is_preserved` was added to
`PRSkillSimplificationTests` before the canonical skill changed. Its first run
executed 13 focused tests and failed on the missing `counts by disposition`
phrase.

## Minimal correction

- Rewrote only the existing universal `Review closeout` paragraph to restore
  both phrases while retaining closeout, non-approval, and no-material rules.
- Added PRL-026 through PRL-030 to the literal ledger as normative
  compatibility contracts after the broader suite exposed three adjacent
  shared closeout phrases.
- Kept the rule inline rather than moving it to the governed reference or
  structural asset because it applies to portable and governed PR output.

## Validation

- `python scripts/test-skill-validator.py PRSkillSimplificationTests` — 13 passed.
- `python scripts/test-review-artifact-validator.py` — 103 passed.
- `python docs/changes/2026-08-16-pr-skill-simplification/fixtures/validate-pr-simplification.py` — passed with 24 rules, 30 literals, seven basis fields, 18 scenarios, and two final profiles.

The corrected PR0 profile is 1,373 words and 10,389 bytes. PR1 is 1,494 words
and 11,303 bytes. Both remain below the 1,678-word and 11,375-byte baseline.
