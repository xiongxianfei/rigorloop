# Review Skill Recording and Status Output Guardrail Change Explanation

## Summary

This change makes formal lifecycle review output explicit about three separate states:

- the review verdict;
- review-recording status;
- artifact-status sync status.

It applies to `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. The canonical skill changes are backed by static validator coverage and regenerated into the local Codex skill mirror and public adapter packages.

## Problem

The repository already required material review findings to be recorded, but the operating flow still allowed a review skill to report a material finding in chat without creating the durable review artifacts or reporting a concrete blocker. The motivating lapse was a `plan-review` finding that was not recorded until challenged, followed by a first correction that omitted the finding `Location`.

A related learn session showed the same shape of drift for clean approvals: a review could say `approved` while the reviewed lifecycle artifact still said `Status: draft`. The accepted direction was to make review output report both recording state and artifact-status sync state.

## Decision Trail

- Proposal: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` accepted the guardrail for all formal review skills, not only `plan-review`.
- Learn session: `docs/learn/sessions/2026-05-12-review-approval-status-sync.md` motivated artifact-status sync for clean or approving outcomes.
- Spec: `specs/formal-review-recording.md` requirements `R24`-`R33a` define review-status, recording-status, and status-sync output contracts.
- Test spec: `specs/formal-review-recording.test.md` tests `T21`-`T23` define static proof for recording status, status sync, and generated-output alignment.
- Plan: `docs/plans/2026-05-12-review-skill-recording-output-guardrail.md` split implementation into M1 recording status, M2 status sync, and M3 generated output/closeout.
- Architecture: no new architecture artifact was needed; `change.yaml` records `architecture.status: no-impact` because this is skill text, validation, generated-output, and lifecycle evidence work.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/formal-review-recording.md` | Added the formal output contract for review verdict, recording status, status sync, blockers, complete finding shape, change ID selection, and artifact-specific sync targets. | Make artifact recording and status-sync behavior normative rather than skill-only. | Accepted proposal, spec-review finding `SR1`, requirements `R24`-`R33a`. | Spec-review closeout in `review-resolution.md`; lifecycle validation through explicit CI. |
| `specs/formal-review-recording.test.md` | Added `T21`-`T23` coverage for recording-status fields, status-sync fields, and generated output alignment. | Every new `MUST` needed an operational proof path. | Spec `R24`-`R33a`; plan M1-M3. | `python scripts/test-skill-validator.py`; explicit CI selected checks. |
| `scripts/test-skill-validator.py` | Added static assertions for the five formal review skills covering recording-status terms, status-sync terms, required blockers, finding shape, change ID selection, and per-skill sync targets. | Prevent future drift in the public review-skill output contract. | Test spec `T21`, `T22`, `T23`. | `python scripts/test-skill-validator.py` passed with 64 tests. |
| `skills/proposal-review/SKILL.md` | Added recording-status and status-sync output guidance; proposal approvals target proposal `Status: accepted`. | Proposal review can have material findings and clean approvals that must settle durably. | Spec `R25`-`R32`; `R31` proposal target. | Skill validator and generated-output drift checks. |
| `skills/spec-review/SKILL.md` | Added recording-status and status-sync output guidance; spec approvals target spec `Status: approved`. | Spec review output must not leave recording or lifecycle state implicit. | Spec `R25`-`R32`; `R31` spec target. | Skill validator and generated-output drift checks. |
| `skills/architecture-review/SKILL.md` | Added recording-status and status-sync output guidance; architecture approvals target `Status: approved`, ADR approvals target `accepted` or `active` according to local lifecycle field. | Architecture and ADR lifecycle vocabulary differs and must not be guessed. | Spec `R31`, `R31a`, `R31b`. | Skill validator and generated-output drift checks. |
| `skills/plan-review/SKILL.md` | Added recording-status and status-sync output guidance; plan approvals target the plan readiness section and plan index only when it owns active-plan state. | Plan readiness is plan-owned and must not be replaced by chat approval. | Spec `R31`; plan-review approval-status sync rule. | Skill validator and generated-output drift checks. |
| `skills/code-review/SKILL.md` | Added recording-status and status-sync output guidance; clean code-review targets active plan milestone state and does not edit source files solely for review status. | Code-review clean status closes or advances review-owned workflow state, not product source. | Spec `R31`; milestone-aware review contract. | Skill validator and generated-output drift checks. |
| `skills/workflow/SKILL.md` | Restored explicit review-resolution disposition vocabulary including `partially-accepted`. | Final broad smoke found workflow guidance no longer named a validator-required disposition. | Review artifact validator contract; `CONSTITUTION.md` and `docs/workflows.md` already name the same vocabulary. | `python scripts/test-review-artifact-validator.py`; `bash scripts/ci.sh --mode broad-smoke`. |
| `.codex/skills/**` | Regenerated local Codex runtime mirror for the five changed formal review skills. | Canonical skill changes must be reflected in runtime skill surfaces. | Spec `R15a`, `R33a`; test spec `T12`, `T23`. | `python scripts/build-skills.py --check`. |
| `dist/adapters/**` | Regenerated Claude, Codex, and opencode adapter skill output for the five changed formal review skills. | Public adapter output must match canonical skill behavior. | Spec `R15a`, `R33a`; token-cost spec versioned adapter guidance. | `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| `docs/changes/2026-05-12-review-skill-recording-output-guardrail/**` | Added change metadata, detailed review records, review log, review resolution, and this explanation. | Material proposal/spec review findings required durable records; ordinary non-trivial work required change-local reasoning. | Formal review recording spec; docs-changes baseline pack. | `validate-change-metadata`; `validate-review-artifacts --mode closeout`. |
| `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` | Accepted proposal and later normalized `Recommended direction` heading spelling after lifecycle validation found the mismatch. | Lifecycle-managed proposal needed validator-compatible section naming before closeout. | Artifact lifecycle validator failure during M3 CI. | Corrected explicit CI passed after the heading fix. |
| `docs/plan.md` and active plan | Tracked milestone state through M1, M2, M3, and final closeout readiness. | The active plan owns current milestone and next-stage state. | Workflow plan policy and milestone-aware handoff. | Code-review status sync after each clean milestone review. |

## Tests Added Or Changed

- `T21`: proves formal review output reports `Recording status` separately from review verdict, includes blocker semantics, complete material-finding shape, and deterministic change ID selection.
- `T22`: proves formal review output reports `Status sync` separately from review verdict and recording status, includes no-edit/ambiguous-target blockers, and preserves artifact-specific sync targets.
- `T23`: proves canonical and generated formal review skills expose the same recording/status-sync guardrail.

The implementation chose static skill-validator checks because the approved spec keeps the first slice structural. It does not add semantic runtime parsing of review output.

## Validation Evidence Before Verify

The change metadata records the full command history. The key passing checks before final `verify` are:

- `python scripts/test-skill-validator.py` passed with 64 tests.
- `python scripts/validate-skills.py` passed for 23 skills.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version 0.1.1 --check` passed.
- `python scripts/validate-adapters.py --version 0.1.1` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-12-review-skill-recording-output-guardrail/change.yaml` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-12-review-skill-recording-output-guardrail` passed.
- `bash scripts/ci.sh --mode explicit --path ...` passed after correcting the explicit-path syntax and proposal heading.
- `bash scripts/ci.sh --mode broad-smoke` passed after restoring the workflow disposition vocabulary.
- `git diff --check --` passed.

Two validation failures were intentionally preserved in evidence:

- The first explicit CI command used paths without `--path`; the plan was corrected to the repository-supported syntax.
- The corrected explicit CI run found the proposal heading `Recommended Direction`; it was normalized to `Recommended direction`, then CI passed.
- The first broad-smoke run found `skills/workflow/SKILL.md` missing `partially-accepted`; workflow guidance was corrected and generated output was refreshed, then broad smoke passed.

## Review Resolution Summary

Material review findings are closed in `docs/changes/2026-05-12-review-skill-recording-output-guardrail/review-resolution.md`.

- `proposal-review-r1`: 6 findings, all accepted and closed.
- `proposal-review-r2`: 5 findings, all accepted and closed.
- `spec-review-r1`: 1 finding, accepted and closed.

There are 12 total material findings, no open findings in `review-log.md`, and `Closeout status: closed`.

Implementation code-reviews for M1, M2, and M3 returned `clean-with-notes` with no material findings, so no additional detailed review record was required for those clean reviews.

## Alternatives Rejected

- Updating only `plan-review`: rejected because the failure mode applies to all formal lifecycle review skills.
- Requiring detailed files for every clean review: rejected because clean no-material reviews should remain lightweight unless another detailed-record trigger applies.
- Leaving clean approval status updates manual-only: rejected because it leaves chat review status and tracked artifact lifecycle state out of sync.
- Adding semantic runtime output validation in this slice: rejected because the approved first slice is structural/static; recurrence can trigger a later automation proposal.
- Hand-editing generated `.codex/skills` or `dist/adapters`: rejected because generated output must come from repository generators.

## Scope Control

This change did not add a new review stage, did not add `pr-review`, did not change review-resolution disposition vocabulary, did not require empty `review-resolution.md` files for no-material detailed records, and did not make status sync permission for downstream workflow continuation.

The review skills may update only minimal lifecycle/status/readiness/closeout surfaces for status sync. Explicit no-edit instructions still block status sync and require `Status sync: blocked`.

## Risks And Follow-Ups

- The guardrail remains static guidance plus static validation. If a formal review again reports material findings without `Recording status: recorded` or `Recording status: blocked`, a follow-up proposal should add runtime/output validation.
- Generated output is current as of this change, but future canonical skill edits must rerun generated-output and adapter validation.
- Final `verify` and PR handoff are still pending at this stage; this explanation does not claim branch readiness or PR readiness.
