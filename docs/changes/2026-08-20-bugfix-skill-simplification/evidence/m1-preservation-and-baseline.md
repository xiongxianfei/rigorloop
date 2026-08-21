# M1 Preservation and Baseline Evidence

Milestone: M1
Status: implementation-complete; review required

## Tests-first evidence

`python scripts/test-skill-validator.py BugfixSkillSimplificationTests` initially failed four tests because the required rule ledger, literal ledger, scenario inventory, and baseline did not exist. The failure established the M1 proof before the evidence surfaces were authored.

## Completed scope

- Recorded one disposition and owner for every meaningful legacy bugfix rule.
- Recorded R1-R27 exactly once and preserved all unlisted behavior.
- Recorded closed vocabulary and handoff literals plus unknown-value-first policy.
- Serialized T1-T15 and the named architecture triggers.
- Bound the current one-file package to identity `ea55e7f477dbc03e11e59798999ce3705125ce24b444766f50da95689c83d2ae`, 586 words, and 3761 bytes.

## Unchanged surfaces

- `skills/bugfix/SKILL.md`: unaffected by design in M1; canonical mutation begins only after clean M1 review.
- Specs, plan, and test spec: unchanged because implementation consumes them read-only.
- Package projections: unchanged because no canonical package source changed.

## Architecture trigger check

Persistent bug transactions, repair engines, external issue integration, cross-stage state owners, and a separate diagnosis skill remain absent. The recorded `architecture-not-required` assessment remains current.

## Validation

- `python scripts/test-skill-validator.py BugfixSkillSimplificationTests`
- `python scripts/validate-change-metadata.py docs/changes/2026-08-20-bugfix-skill-simplification/change.yaml`

This evidence establishes implementation completion for code review only. It does not close M1 or claim downstream readiness.
