# M2 PR package implementation

## Result

- Milestone: M2
- Status: implementation-complete; review required
- PR package: compact universal skill, one governed-readiness reference, and one structural body asset
- Coupled producer: normalized verification basis added to `verify`
- Validator compatibility: `validate-skills.py` accepts one or more explicit targets

## Test-first evidence

`PRSkillSimplificationTests` was added before the new reference and asset existed. Its first run executed 11 tests and failed all 11 with missing-resource errors. After implementation, all 11 pass.

## Implemented contract

The universal skill now owns the tri-state governed signal, independent intent/refresh/state-transition authorities, directional branch and PR states, hosted-CI truthfulness, exact base/head consumption, evidence-tail rule, ordered rereads, retry, read-back, stops, claims, and results. The conditional reference performs read-only governed evidence aggregation. The asset owns only repeated body structure. `verify` emits the seven-field normalized basis through its current result/report surfaces.

The first version preserves existing PR body bytes unless an explicit whole-body replacement is authorized; it has no Markdown section parser or managed markers. `prepare-only` performs no external writes.

## Validation

Observed on 2026-08-16:

- `python scripts/validate-skills.py skills/pr/SKILL.md skills/verify/SKILL.md` — passed for both explicit targets.
- `python scripts/test-skill-validator.py PRSkillSimplificationTests` — 11 passed.
- `python scripts/test-skill-validator.py` — 384 passed, 16 skipped.
- `python scripts/test-build-skills.py` — seven passed.
- `python scripts/build-skills.py --check` — passed using temporary generated output.

These are local deterministic checks. No live PR, remote mutation, hosted-CI claim, or target-agent runtime was used.
