# Explain Change: Cost-Bounded Rigor M2 Selected Skill Reminders

## Summary

This change implements the M2 selected-skill reminder slice from the accepted cost-bounded-rigor proposal. It keeps the full bounded-evidence rule in `docs/workflows.md`, leaves `proposal` and `proposal-review` unchanged with rationale, adds one concise path/state lookup reminder to `workflow`, and adds focused static proof for the selected surfaces.

The slice also creates the focused M2 spec, test spec, plan, change metadata, and durable review evidence needed to make the work traceable. It does not implement validation-budget guidance, lifecycle token-cost summary artifacts, release or adapter changes, dynamic benchmark requirements, hard token gates, or progressive-loading restructuring.

## Problem

After PR #54 completed the first cost-bounded-rigor slice, the next approved slice was to add minimal bounded-evidence wording in selected public skill surfaces. The problem was narrow: selected skills should reduce broad path/state searches without duplicating the full `docs/workflows.md` rule or expanding into later workstreams.

## Decision Trail

| Source | Decision |
|---|---|
| Proposal | M2 is bounded evidence wording in selected skill surfaces, limited to `proposal`, `proposal-review`, and `workflow`. M3-M5 remain separate slices. |
| Focused M2 spec | Requirements `R1`-`R19` define selected surfaces, no-change rationale, concise reminders, stable static proof, diagnostic token measurement, and forbidden surfaces. |
| M2 test spec | Test cases `T1`-`T11` map the spec to final diff review, selected skill audit, focused static proof, selected validation, token measurement, and review evidence. |
| Plan | M1 is the only implementation milestone: selected skill reminder audit and implementation. |
| Architecture | Not required. Spec-review and plan-review found no runtime, selector, release, adapter, security-boundary, or hard-to-reverse architecture change. |
| Review | `CBR-M2-CR2-1` was accepted and resolved by replacing an exact full-sentence assertion with smaller stable behavior-cue checks. |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `specs/cost-bounded-rigor-m2-selected-skill-reminders.md` | Added focused M2 contract. | The prior approved spec was first-slice-only, so M2 needed its own normative scope before implementation. | Proposal M2 rollout; spec requirements `R1`-`R19`. | `spec-review-r1`; artifact lifecycle validation. |
| `specs/cost-bounded-rigor-m2-selected-skill-reminders.test.md` | Added active test spec. | The selected-skill wording needed traceable proof without broad runtime or release tests. | M2 spec; plan-review. | Maintainer-approved test spec; selected lifecycle validation. |
| `docs/plans/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders.md` | Added and maintained the M2 execution plan. | The work needed a narrow plan after PR #54 merged and the first-slice spec no longer governed M2. | Proposal rollout; focused M2 spec. | Plan-review records, validation notes, state-sync updates. |
| `docs/plan.md` | Updated lifecycle index state. | The active plan index must point to the current stage and not leave stale handoff state. | Plan file policy; active M2 plan. | Artifact lifecycle validation. |
| `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md` | Marked the first-slice plan done after PR #54. | M2 planning depends on the merged first slice being settled rather than treated as still active. | PR #54 outcome; plan index policy. | Selected lifecycle validation. |
| `skills/workflow/SKILL.md` | Added one concise path/state lookup reminder. | `workflow` lacked a local cue to start from active plan, artifact metadata, `docs/workflows.md`, default paths, and targeted headings before broader searches. | M2 `R7`-`R10`; M2 selected skill audit. | `test_cost_bounded_rigor_m2_selected_skill_reminders`; code-review. |
| `skills/proposal/SKILL.md` | Unchanged with rationale. | Existing wording already had artifact-placement lookup, broad path-search avoidance, bounded evidence, and full-file-read escape behavior. Editing it would be wording churn. | M2 `R11`, `R12`, `R19`. | Plan selected skill audit; static proof checks existing terms. |
| `skills/proposal-review/SKILL.md` | Unchanged with rationale. | Existing wording already satisfied the M2 contract for lookup, broad-search avoidance, bounded evidence, and full-file-read escape behavior. | M2 `R11`, `R12`, `R19`. | Plan selected skill audit; static proof checks existing terms. |
| `scripts/test-skill-validator.py` | Added focused selected-skill reminder proof. | Static proof gives durable regression coverage for selected surfaces without natural-language scoring. | M2 `R13`, `R14`; test spec `T5`. | `python scripts/test-skill-validator.py`; selected CI. |
| `docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/*` | Added change metadata, review log, review-resolution, and review receipts. | Formal lifecycle reviews and material findings need durable evidence rather than chat-only state. | Workflow review-recording rules; M2 plan. | `validate-review-artifacts.py --mode closeout`; selected CI. |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
|---|---|---|
| `test_cost_bounded_rigor_m2_selected_skill_reminders` | Selected skills contain bounded-evidence/full-file escape cues, do not copy the full workflow evidence sequence, proposal/proposal-review retain path lookup terms, and workflow has path/state lookup cues. | M2 is wording/static-proof work, so repository-file static proof is enough and avoids runtime or release tests. |
| Selected skill audit in the plan | `proposal` and `proposal-review` were intentionally unchanged, while `workflow` was edited. | M2 allows no-change rationale when a selected skill already satisfies the contract. |
| Static token measurement | Skill token cost remained diagnostic-only. | M2 requires warning-only token-cost measurement and does not introduce hard gates. |
| Review-resolution for `CBR-M2-CR2-1` | The brittle exact-sentence assertion was replaced with separate stable cues. | M2 `R14` and test spec `T5` prohibit freezing one exact sentence. |

## Validation Evidence Before Final Verify

Validation already recorded for this slice includes:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/measure-skill-tokens.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders`
- `bash scripts/ci.sh --mode explicit ...` for the selected skill, lifecycle, review-artifact, and change-metadata paths
- `git diff --check -- ...`

Hosted CI has not been observed for this branch. Final `verify` has not run yet.

## Review Resolution Summary

`review-resolution.md` is closed.

Counts by disposition:

- Accepted: 1
- Rejected: 0
- Deferred: 0
- Partially accepted: 0
- Needs decision: 0

The accepted finding was `CBR-M2-CR2-1`: the first static proof required an exact full sentence. The fix replaced that assertion with smaller stable cues while preserving selected-surface and forbidden-sequence checks. Later code-review rounds `code-review-m1-r3` and `code-review-m1-r4` recorded no material findings.

See `docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/review-resolution.md`.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Edit every public skill. | M2 is limited to `proposal`, `proposal-review`, and `workflow`; broader skill wording belongs to later slices. |
| Copy the full bounded-evidence sequence into selected skills. | `docs/workflows.md` owns the full rule; selected skills should only carry concise local reminders. |
| Force wording churn in `proposal` and `proposal-review`. | Both already satisfied the M2 contract, so the plan records no-change rationale instead. |
| Add validation-selector or release changes. | Validation-budget, release, adapter, and broad-smoke behavior are explicitly out of M2 scope. |
| Require a dynamic benchmark comparison. | M2 changes selected skill wording and static proof only; dynamic comparison is advisory unless a later approved plan or test spec requires it. |
| Keep exact full-sentence static proof. | `CBR-M2-CR2-1` showed that this violated M2 `R14` and test spec `T5`. |

## Scope Control

Preserved non-goals:

- no edits to `implement` or `code-review`;
- no validation-selector behavior changes;
- no broad-smoke trigger changes;
- no release validation or adapter packaging changes;
- no lifecycle token-cost summary artifact;
- no dynamic benchmark requirement;
- no hard token gate;
- no generated public adapter skill bodies reintroduced as tracked source;
- no full progressive-loading restructuring.

## Risks And Follow-Ups

Risks:

- Hosted CI has not been observed for this branch.
- Final `verify` still needs to check artifact-code-test coherence before PR handoff.

Follow-ups:

- M3 validation-budget guidance remains a later slice.
- M4 lifecycle token-cost summaries remain a later conditional slice.
- M5 progressive-loading follow-through remains separate from this M2 wording slice.

## Readiness

M1 implementation and code-review are closed. `CBR-M2-CR2-1` is accepted and resolved. This explain-change artifact has selected validation evidence recorded in the active plan and change metadata. The next lifecycle stage is `verify`.
