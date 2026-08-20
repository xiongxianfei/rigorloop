# M2 Contract Implementation Evidence

## Scope

Milestone M2 rewrote the single authored `bugfix` skill and added focused contract tests. No reference, asset, script, runtime, or persistent bug state was added.

## Tests-first evidence

Before editing `skills/bugfix/SKILL.md`, the focused suite reported seven failures for the absent closed operation, authority, proof-phase, action, cause/result, governed-signal, and handoff contracts. The four M1 preservation tests remained green.

## Implemented contract

- Operation, command authority, and write authority are independently classified and bound to one repository and concrete defect.
- Governed signals use a fail-closed three-state classifier with no portable fallback.
- Proof-authoring is a bounded writable phase before production correction.
- Production correction requires a failing automated test or complete deterministic alternative under recorded infeasibility.
- Cause, action, and terminal-result vocabularies are closed; completed and failed corrections precede broad eligibility.
- Upstream, lifecycle, verification, PR, and release surfaces remain read-only; changed implementation hands off only to `code-review`.

## Review correction

`code-review-m2-r1` found that the first compact draft omitted three approved causes, `complete-diagnosis`, the exact `post-fix-validation` phase, the unexpected-mutation stop, and required result fields. `BUGSIM-CR1` was accepted. The canonical skill and focused assertions now contain the complete approved vocabularies and behavior while retaining strict word and byte reductions.

## Measurements

| Surface | Before | After | Change |
| --- | ---: | ---: | ---: |
| normalized words | 586 | 412 | -174 |
| LF-normalized UTF-8 bytes | 3761 | 3754 | -7 |
| packaged files | 1 | 1 | 0 |

The byte reduction is intentionally strict despite the newly explicit closed vocabularies. Final package-chain measurements belong to M3.

## Validation

All commands passed:

- `python scripts/test-skill-validator.py BugfixSkillSimplificationTests` — 11 tests.
- `python scripts/validate-skills.py skills/bugfix` — canonical skill valid.
- `python scripts/test-skill-validator.py` — 443 tests, 16 skipped.
- `python scripts/validate-boundary-first.py --check --path specs/bugfix-skill-simplification.md`.
- `python scripts/test-build-skills.py` — 7 tests.
- `python scripts/build-skills.py --check`.
- `python scripts/validate-documentation-prose.py --mode audit --path specs/bugfix-skill-simplification.md --path specs/bugfix-skill-simplification.test.md --path docs/plans/2026-08-20-bugfix-skill-simplification.md` — no errors or warnings.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`.

## Result

M2 implementation is complete and ready for independent milestone code review. Hosted CI and target-agent execution were not performed.
