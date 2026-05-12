# Record Every Formal Review Explain Change

## Summary

This change makes every supported formal lifecycle review leave durable review evidence.

Clean formal reviews now use lightweight review receipts indexed in `review-log.md`. Reviews with material findings continue to use detailed review records and `review-resolution.md`. The change keeps review evidence separate from artifact lifecycle/status settlement.

## Problem

Clean formal reviews could previously be approved in chat or artifact-local text without a dedicated review evidence file. Later agents then had to infer whether a formal review happened, which artifact and round were reviewed, what scope was checked, and whether the result was clean.

The approved direction keeps clean reviews lightweight while making formal review evidence reconstructable.

## Decision Trail

- Proposal-review requested revisions to make the policy shift explicit, define the formal review boundary, and separate receipts from artifact status settlement.
- The proposal was accepted after those decisions were incorporated.
- Spec-review `SR-001` was accepted and resolved by defining the minimal clean receipt root shape.
- Architecture-review approved the architecture update with no material findings.
- Plan-review approved the five-milestone execution plan.
- Code-review M1 through M4 closed cleanly after resolving M2 findings `CR-M2-001` and `CR-M2-002`.

## Diff Rationale

| Area | Files | Why it changed |
| --- | --- | --- |
| Proposal, spec, test spec | `docs/proposals/2026-05-12-record-every-formal-review.md`, `specs/formal-review-recording.md`, `specs/formal-review-recording.test.md` | Define the record-every-formal-review contract, clean receipt root, recording status vocabulary, test mapping, and compatibility boundaries. |
| Review artifact validation | `scripts/review_artifact_validation.py`, `scripts/change_metadata_semantics.py`, validator tests, clean receipt fixtures | Parse clean receipt log tables, reject empty clean-review resolution files, and enforce minimal clean-root `change.yaml.review` metadata. |
| Canonical guidance | `templates/shared/review-isolation-and-recording.md`, formal review skills, `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md` | Align user-facing review skills and maintainer governance with receipt-or-blocked recording for formal lifecycle reviews. |
| Generated output | `.codex/skills/`, `dist/adapters/**/skills/` | Regenerate local Codex skill mirrors and tracked public adapters after canonical skill changes. |
| Change-local evidence | `docs/changes/2026-05-12-record-every-formal-review-review-recording/**` | Preserve review records, material finding dispositions, validation evidence, and this explanation under the change root. |

## Implementation Notes

The clean receipt model is intentionally small. A clean receipt records metadata, outcome, scope checked, and a no-finding statement. It is indexed in `review-log.md` and does not create an empty `review-resolution.md`.

The minimal clean receipt root requires `change.yaml`, `review-log.md`, and `reviews/<stage>-r<n>.md`. For clean roots, `change.yaml.review.status` must be `clean`, `review.reviewed_artifact` and `review.review_log` must be present, and `review.unresolved_items` must be `0`.

Review skills point to the shared recording contract instead of duplicating long templates. `not-required` is reserved for non-formal review-like requests outside the formal lifecycle review model.

## Tests And Validation

Validation recorded before this handoff includes:

```bash
python scripts/test-review-artifact-validator.py
python scripts/test-change-metadata-validator.py
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-record-every-formal-review-review-recording
python scripts/validate-change-metadata.py docs/changes/2026-05-12-record-every-formal-review-review-recording/change.yaml
bash scripts/ci.sh --mode explicit --path specs/formal-review-recording.md --path specs/formal-review-recording.test.md --path scripts/review_artifact_validation.py --path scripts/test-review-artifact-validator.py --path templates/shared/review-isolation-and-recording.md --path skills/spec-review/SKILL.md --path skills/code-review/SKILL.md --path dist/adapters/codex/.agents/skills/spec-review/SKILL.md --path dist/adapters/codex/.agents/skills/code-review/SKILL.md
git diff --check
```

## Review Resolution Summary

`review-resolution.md` is closed for all material findings currently recorded.

Material findings resolved:

- `SR-001`: accepted and resolved by adding the clean receipt root contract to the spec.
- `CR-M2-001`: accepted and resolved by enforcing required clean-root review metadata.
- `CR-M2-002`: accepted and resolved by requiring `review.status: clean` for clean receipt roots.

## Remaining Risk

The remaining workflow risk is process adoption: future agents must consistently create the lightweight receipt or report blocked recording for formal lifecycle reviews. The shared skill block, governance text, fixtures, and validators are updated to reduce that risk.

## Handoff

Next stage: `code-review M5`.

This explain-change artifact documents the implemented diff and rationale. It is not final verification or PR approval.
