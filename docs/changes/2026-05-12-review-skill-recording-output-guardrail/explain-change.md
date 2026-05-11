# Review Skill Recording and Status Output Guardrail Change Explanation

## Summary

This change makes formal lifecycle review output explicit about three separate states:

- the review verdict;
- review-recording status;
- status settlement recommendation.

It applies to `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`. The canonical skill changes are backed by static validator coverage and regenerated into the local Codex skill mirror and public adapter packages. PR #44 was narrowed before merge so review skills no longer directly update upstream lifecycle status; the follow-up proposal `docs/proposals/2026-05-12-downstream-upstream-status-settlement-before-reliance.md` owns that behavior.

## Problem

The repository already required material review findings to be recorded, but the operating flow still allowed a review skill to report a material finding in chat without creating the durable review artifacts or reporting a concrete blocker. The motivating lapse was a `plan-review` finding that was not recorded until challenged, followed by a first correction that omitted the finding `Location`.

A related learn session showed the same shape of drift for clean approvals: a review could say `approved` while the reviewed lifecycle artifact still said `Status: draft`. The narrowed direction is to make review output report recording state and a status-settlement recommendation while deferring direct settlement-before-reliance to downstream skills.

## Decision Trail

- Proposal: `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` accepted the guardrail for all formal review skills, not only `plan-review`.
- Learn session: `docs/learn/sessions/2026-05-12-review-approval-status-sync.md` motivated upstream lifecycle settlement before reliance for clean or approving outcomes.
- Spec: `specs/formal-review-recording.md` requirements `R24`-`R33a` define review-status, recording-status, and status-settlement recommendation output contracts.
- Test spec: `specs/formal-review-recording.test.md` tests `T21`-`T23` define static proof for recording status, status-settlement recommendation, and generated-output alignment.
- Plan: `docs/plans/2026-05-12-review-skill-recording-output-guardrail.md` split implementation into M1 recording status, M2 status-settlement recommendation, and M3 generated output/closeout.
- Architecture: no new architecture artifact was needed; `change.yaml` records `architecture.status: no-impact` because this is skill text, validation, generated-output, and lifecycle evidence work.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/formal-review-recording.md` | Added the formal output contract for review verdict, recording status, complete finding shape, change ID selection, and status settlement recommendation while deferring direct settlement-before-reliance. | Make recording behavior normative while keeping direct upstream lifecycle edits out of review skills. | Accepted proposal, spec-review finding `SR1`, requirements `R24`-`R33a`, PR #44 narrowing request. | Spec-review closeout in `review-resolution.md`; lifecycle validation through explicit CI. |
| `specs/formal-review-recording.test.md` | Added `T21`-`T23` coverage for recording-status fields, status-settlement recommendation, and generated output alignment. | Every new `MUST` needed an operational proof path, and the narrowing needed static proof that old direct status-settlement fields were removed. | Spec `R24`-`R33a`; plan M1-M3. | `python scripts/test-skill-validator.py`; explicit CI selected checks. |
| `scripts/test-skill-validator.py` | Added static assertions for the five formal review skills covering recording-status terms, status-settlement recommendation terms, finding shape, change ID selection, and direct status-settlement field removal. | Prevent future drift in the public review-skill output contract. | Test spec `T21`, `T22`, `T23`. | `python scripts/test-skill-validator.py` passed with 64 tests. |
| `skills/proposal-review/SKILL.md` | Added recording-status guidance and status-settlement recommendation; direct proposal status edits are deferred. | Proposal review can have material findings, but direct settlement belongs to downstream reliance work. | Spec `R25`-`R32`; follow-up proposal. | Skill validator and generated-output drift checks. |
| `skills/spec-review/SKILL.md` | Added recording-status guidance and status-settlement recommendation; direct spec status edits are deferred. | Spec review output must not leave recording implicit, but should not own upstream lifecycle settlement in this slice. | Spec `R25`-`R32`; follow-up proposal. | Skill validator and generated-output drift checks. |
| `skills/architecture-review/SKILL.md` | Added recording-status guidance and status-settlement recommendation; direct architecture/ADR status edits are deferred. | Architecture and ADR lifecycle settlement needs downstream reliance rules before direct edits. | Spec `R29`-`R33a`; follow-up proposal. | Skill validator and generated-output drift checks. |
| `skills/plan-review/SKILL.md` | Added recording-status guidance and status-settlement recommendation; direct plan readiness/lifecycle edits are deferred. | Plan readiness is plan-owned and should be settled by the downstream relying workflow rule, not review output alone. | Spec `R29`-`R33a`; follow-up proposal. | Skill validator and generated-output drift checks. |
| `skills/code-review/SKILL.md` | Added recording-status guidance and status-settlement recommendation; direct source or plan milestone edits are deferred. | Code-review clean status should not edit source files solely for review status. | Spec `R29`-`R33a`; follow-up proposal. | Skill validator and generated-output drift checks. |
| `docs/proposals/2026-05-12-downstream-upstream-status-settlement-before-reliance.md` | Added a draft follow-up proposal for downstream settlement before reliance. | Preserve the approval-status drift problem without keeping direct upstream status edits in PR #44. | PR #44 narrowing request; learn session. | Lifecycle validation and explicit CI. |
| `skills/workflow/SKILL.md` | Restored explicit review-resolution disposition vocabulary including `partially-accepted`. | Final broad smoke found workflow guidance no longer named a validator-required disposition. | Review artifact validator contract; `CONSTITUTION.md` and `docs/workflows.md` already name the same vocabulary. | `python scripts/test-review-artifact-validator.py`; `bash scripts/ci.sh --mode broad-smoke`. |
| `.codex/skills/**` | Regenerated local Codex runtime mirror for the five changed formal review skills. | Canonical skill changes must be reflected in runtime skill surfaces. | Spec `R15a`, `R33a`; test spec `T12`, `T23`. | `python scripts/build-skills.py --check`. |
| `dist/adapters/**` | Regenerated Claude, Codex, and opencode adapter skill output for the five changed formal review skills. | Public adapter output must match canonical skill behavior. | Spec `R15a`, `R33a`; token-cost spec versioned adapter guidance. | `python scripts/build-adapters.py --version 0.1.1 --check`; `python scripts/validate-adapters.py --version 0.1.1`. |
| `docs/changes/2026-05-12-review-skill-recording-output-guardrail/**` | Added change metadata, detailed review records, review log, review resolution, and this explanation. | Material proposal/spec review findings required durable records; ordinary non-trivial work required change-local reasoning. | Formal review recording spec; docs-changes baseline pack. | `validate-change-metadata`; `validate-review-artifacts --mode closeout`. |
| `docs/proposals/2026-05-12-review-skill-recording-output-guardrail.md` | Accepted proposal and later normalized `Recommended direction` heading spelling after lifecycle validation found the mismatch. | Lifecycle-managed proposal needed validator-compatible section naming before closeout. | Artifact lifecycle validator failure during M3 CI. | Corrected explicit CI passed after the heading fix. |
| `docs/plan.md` and active plan | Tracked milestone state through M1, M2, M3, final closeout readiness, PR handoff, and PR #44 narrowing. | The active plan owns current milestone and next-stage state. | Workflow plan policy and milestone-aware handoff. | Lifecycle validation and explicit CI. |

## Tests Added Or Changed

- `T21`: proves formal review output reports `Recording status` separately from review verdict, includes blocker semantics, complete material-finding shape, and deterministic change ID selection.
- `T22`: proves formal review output reports `Status settlement recommendation` separately from review verdict and recording status, and that direct status-settlement fields are absent from review skills.
- `T23`: proves canonical and generated formal review skills expose the same recording/status-settlement recommendation guardrail.

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
- PR #44 narrowing validation passed after replacing direct status-settlement wording with status-settlement recommendation wording and adding the downstream settlement follow-up proposal.
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
- Requiring review skills to directly update upstream lifecycle status: rejected for PR #44 because settlement-before-reliance is broader than the recording guardrail and belongs in a follow-up.
- Adding semantic runtime output validation in this slice: rejected because the approved first slice is structural/static; recurrence can trigger a later automation proposal.
- Hand-editing generated `.codex/skills` or `dist/adapters`: rejected because generated output must come from repository generators.

## Scope Control

This change did not add a new review stage, did not add `pr-review`, did not change review-resolution disposition vocabulary, did not require empty `review-resolution.md` files for no-material detailed records, and did not require review skills to update upstream lifecycle status directly.

Direct upstream status settlement before reliance is tracked in `docs/proposals/2026-05-12-downstream-upstream-status-settlement-before-reliance.md`.

## Risks And Follow-Ups

- The guardrail remains static guidance plus static validation. If a formal review again reports material findings without `Recording status: recorded` or `Recording status: blocked`, a follow-up proposal should add runtime/output validation.
- Generated output is current as of this change, but future canonical skill edits must rerun generated-output and adapter validation.
- Final `verify` and PR handoff are still pending at this stage; this explanation does not claim branch readiness or PR readiness.
