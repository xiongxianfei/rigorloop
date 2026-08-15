# M2 Package Implementation

- Change: `2026-08-15-spec-skill-simplification`
- Milestone: M2
- Implementation profile: `IP2-planned-armed`
- Result: implementation complete; code review required

## Outcome

The canonical `spec` package now keeps portable contract judgment and safety in `SKILL.md`, loads both existing boundary references initially, and conditionally loads one governed-authoring reference only for `single-governed-candidate`. The existing skeleton has one formal-boundary insertion marker. No target-agent runtime, new validator family, lifecycle state, policy asset, or generated authored source was added.

## Tests first

`SpecSkillSimplificationTests` was added before the package rewrite. Its first run failed all five focused cases because the old package had no governed reference, closed profile and signal contract, restart procedure, insertion marker, or required-resource boundary. The canonical edits then made those assertions pass.

## Changed surfaces

| Surface | Result |
| --- | --- |
| `skills/spec/SKILL.md` | Shortened universal dispatcher with tri-state governed signals, portable operations, universal contract quality, boundary composition, stops, claims, and exact resource triggers. |
| `skills/spec/references/governed-spec-authoring.md` | Added authority validation, create/revise transactions, identical retry, explicit stale restart, byte preservation, bounded writes, and handoff. |
| `skills/spec/assets/spec-skeleton.md` | Added one conditional formal-boundary insertion marker between the two approved anchors. |
| `scripts/test-skill-validator.py` | Added focused contract checks and migrated directly coupled lifecycle and initial-resource consumers. |
| `scripts/skill_validation.py` | Registered the governed reference in the existing packaged-resource allowlist. |

The two existing boundary references were not edited because their initial-loading behavior and procedure ownership remain unchanged. Adapter generation, schemas, lifecycle vocabulary, workflow routing, and historical specs were unaffected because existing owners already cover the selected package shape.

## Preliminary profile evidence

Counts use canonical LF-normalized authored resources, Unicode whitespace-separated words, UTF-8 bytes, and one count per loaded procedure.

| Profile | Baseline words | Current words | Baseline bytes | Current bytes | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `SA0-portable` | 3020 | 2453 | 21523 | 18312 | decreased |
| `SA1-governed` | 3020 | 2862 | 21523 | 21515 | decreased |

The complete authored package is 3080 words and 23140 bytes versus the 3229-word and 23087-byte baseline. The 53-byte package increase is the visible cost of adding one explicit governed resource while both real procedural profiles decrease. M3 owns final identity, parity, and measurement proof.

## Validation

- `python scripts/validate-skills.py skills/spec/SKILL.md`: passed.
- `python scripts/test-skill-validator.py SpecSkillSimplificationTests`: passed five tests.
- `python scripts/test-skill-validator.py`: passed 347 tests with 16 skips.
- `python scripts/test-build-skills.py`: passed seven tests.
- `python scripts/build-skills.py --check`: passed.
- `python scripts/validate-boundary-first.py --check --path specs/spec-skill-simplification.md`: passed.
- `git diff --check`: passed.

## Handoff

M2 is implementation-complete evidence only. It routes to formal milestone code review and does not claim milestone closure, final package parity, verification, branch readiness, or PR readiness.
