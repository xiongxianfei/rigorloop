# M2 Package Refactor Evidence

Milestone: M2
Date: 2026-08-11
Status: implementation-complete; review pending

## Implemented package boundary

- `skills/test-spec-review/SKILL.md` remains self-sufficient for advisory proof review, lifecycle and handoff classification, boundary applicability, recording triggers, universal proof quality, statuses, routing, staleness, findings, stops, claims, isolation, and compact output.
- `references/test-spec-review-recording-and-settlement.md` now owns shared durable-recording mechanics and a visibly separate `## Formal-only settlement` procedure.
- Both governed boundary references and both structural assets remain byte-identical to the M1 baseline.
- `scripts/skill_validation.py` recognizes the new packaged reference and validates installed artifact placement from the complete mapped package rather than requiring duplicated procedure in `SKILL.md`.
- `scripts/test-skill-validator.py` adds focused T1-T5/T9-T10/T15-T16 contract assertions and migrates stage-owned settlement checks to the packaged reference for `test-spec-review`.

## Test-first receipt

The new `TestSpecReviewSkillSimplificationContractTests` suite was added before package text changed. Its first execution failed because the recording reference, closed classifications, exact assemblies, fail-safe wording, and split ownership did not yet exist. After implementation and compatibility migration, all six focused tests pass.

## Contract proof

- Exactly three lifecycle/handoff pairs are valid; `advisory + workflow-managed` stops.
- `durable_recording_context` and `boundary_first_context` select the four named base assemblies without changing authority.
- Late recording changes only recording obligations and cannot execute formal-only settlement in advisory mode.
- Missing triggered resources block dependent recording or proof judgment without memory reconstruction; untriggered resources do not load.
- Universal traceability, negative/failure coverage, command ownership, deterministic fixtures, manual-proof requirements, statuses, staleness, claims, and boundary-first compact scan remain inline.
- Formal settlement reads current governed identity, records first, mutates only the matching test-spec entry, preserves workflow state, and stops or returns control according to handoff mode.
- Assets remain unchanged layout owners and contain no activation, settlement, or workflow policy.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/validate-skills.py skills/test-spec-review/SKILL.md` | pass; one canonical skill validated |
| `python scripts/test-skill-validator.py` | pass; 308 tests, 16 skipped |
| `python scripts/test-build-skills.py` | pass; 7 tests |
| `python scripts/build-skills.py --check` | pass; generated skill parity validated in temporary output |
| `python scripts/validate-change-metadata.py docs/changes/2026-08-11-test-spec-review-skill-simplification/change.yaml` | pass |
| `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-11-test-spec-review-skill-simplification` | pass; 9 reviews, 5 findings, 9 log entries, 5 resolution entries |
| `git diff --check` | pass |

No command executed or graded Codex, Claude Code, opencode, or another target-agent runtime. M2 does not claim final package parity or semantic closeout; those remain M3 obligations.
