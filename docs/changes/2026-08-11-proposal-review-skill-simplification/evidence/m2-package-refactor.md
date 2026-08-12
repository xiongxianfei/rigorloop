# M2 Proposal-Review Package Refactor

Milestone: M2
Date: 2026-08-12
Status: implementation-complete; review pending

The canonical package now has a compact self-sufficient `SKILL.md`, `references/proposal-review-recording-and-settlement.md`, `references/conditional-proposal-gates.md`, and the two existing structural assets.

Implementation summary:

- Added a focused failing package-contract test before creating the references.
- Kept universal role, evidence, proposal judgment, materiality, statuses, modes, durable and specialized trigger classification, isolation, stops, claims, resource selection, and output applicability inline.
- Moved location resolution, recording, formal settlement, retries, automation packets, correction, and workflow-managed return procedure to the recording reference without granting authority by loading it.
- Moved only detailed vision-exception, standing-artifact, and broad scope-budget procedure to the gates reference; predicate truth remains proposal-review judgment.
- Reworked the result skeleton into one core group plus specialized-gate, durable-recording, formal-settlement, and automated-review groups. Inapplicable groups are omitted by procedure; assets contain labels and placeholders only.
- Preserved `material-finding.md` unchanged.
- Extended the existing package allowlist and structural-label validation rather than creating a new validator family.
- Migrated exact-string tests to inspect the complete mapped package or the reference that now owns the procedure. Universal shared-block and customer-portability checks remain inline.

Validation:

- `python scripts/validate-skills.py skills/proposal-review/SKILL.md` — passed.
- `python scripts/test-skill-validator.py` — 311 tests passed, 16 skipped.
- `python scripts/test-build-skills.py` — 7 tests passed.
- `python scripts/build-skills.py --check` — passed using temporary generated output.
- `git diff --check` — passed.

Unaffected with rationale:

- `skills/proposal-review/assets/material-finding.md`: its complete repeated finding structure already has one owner.
- Formal-review-recording schemas and lifecycle code: this milestone changes skill composition, not record schemas or runtime lifecycle behavior.
- Adapter distribution tooling: existing resource discovery already packages mapped references; direct all-target proof belongs to M3.

M2 does not claim package-chain completion, semantic final acceptance, milestone closeout, or verify readiness. It is ready for independent code review.
