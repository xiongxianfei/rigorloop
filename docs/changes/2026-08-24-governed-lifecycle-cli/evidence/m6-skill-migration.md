# M6 Governed Skill Migration Evidence

Milestone: M6
Validation result: passed
Subject: commit `aaa298a9`

The five governed authoring references now obtain CLI context, preserve stage-owned semantic work, write exact artifact/evidence identities, and invoke `record-artifact-revision`. The five matching review references now invoke `record-review` and, as a separate authority-bounded step, `settle-artifact`. They no longer teach field-level lifecycle mutation.

Semantic criteria, artifact ownership, stop behavior, evidence-first recovery, portable mode, workflow routing ownership, and the plan's existing narrow one-time planned-work initialization exception remain explicit.

Validation:

- `python3 scripts/test-skill-validator.py`: passed, 446 tests with 16 documented skips.
- `python3 scripts/validate-skills.py`: passed for all 24 canonical skill files.
- `python3 scripts/test-build-skills.py`: passed, 7 tests.
- `python3 scripts/build-skills.py --check`: passed using temporary generated output.
