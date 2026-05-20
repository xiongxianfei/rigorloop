# Explain Change: Spec-Family Assets Progressive Disclosure

## Summary

This change applies assets-only progressive disclosure to the spec-family
skills while preserving the PR #79 behavior baseline. The final asset set is
deliberately small: full skeletons and substantial multi-field blocks live in
`assets/`, while trivial one-line row formats remain inline in `SKILL.md`.

The change also adds deterministic validator coverage, generated-output proof,
behavior-preservation evidence, review records, and a learn capture for the
asset-formalism lesson surfaced during implementation.

## Problem

PR #79 made `spec`, `spec-review`, and `test-spec` easier to scan without
changing behavior. The accepted follow-up was to apply the already-proven
`assets/` progressive-disclosure pattern to the spec family without hiding
rules, review judgment, enums, stop conditions, coverage obligations, lifecycle
boundaries, or validation duties outside `SKILL.md`.

The implementation also had to avoid formalism: an asset must earn its file by
being substantial enough to template. A one-line row whose format is already
defined inline is not enough.

## Decision Trail

| Decision point | Outcome | Source |
|---|---|---|
| Proposal direction | Use assets only for `spec`, `spec-review`, and `test-spec`; do not add `references/`, `scripts/`, or build-time partials. | `docs/proposals/2026-05-20-spec-family-assets-progressive-disclosure.md` |
| Proposal review | Five proposal-review findings were accepted and resolved before downstream reliance. | `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md` |
| Spec contract | `SFA-R1` through `SFA-R45` define the asset boundary, proof requirements, behavior preservation, generated-output proof, and validator coverage. | `specs/spec-family-assets-progressive-disclosure.md` |
| Test spec | `AC-SFA-001` through `AC-SFA-015` are mapped to deterministic checks and evidence. | `specs/spec-family-assets-progressive-disclosure.test.md` |
| Architecture | No separate architecture package was needed; the plan records no architecture, data, deployment, or security-boundary changes. | `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md` |
| Plan milestones | M1 built validator/baseline foundation; M2-M4 updated the three skills; M5 proved generated output; M6 removed trivial row assets. | `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md` |
| Reviews | Fifteen reviews are recorded; nine material findings were resolved; M6 closed clean. | `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md` |

## Diff Rationale By Area

| Area | Change | Reason | Source artifact | Evidence |
|---|---|---|---|---|
| `skills/spec/SKILL.md` and `skills/spec/assets/spec-skeleton.md` | Added a `Resource map`, moved the full spec skeleton to `spec-skeleton.md`, and kept requirement, acceptance-criterion, decision-log, modal guidance, enums, and settlement rules inline. | Preserve self-contained operating rules while moving substantial output structure out of the common path. | `SFA-R3`, `SFA-R4`, `SFA-R7`, `SFA-R8`, `SFA-R14` through `SFA-R22` | Skill validation, behavior-preservation evidence, token/cold-read evidence |
| `skills/spec-review/SKILL.md` and `skills/spec-review/assets/*` | Added only `review-result-skeleton.md` and `review-finding.md`; kept review dimensions, verdict enum, review policy, severity policy, recording rules, and sufficiency rules inline. | `spec-review` is deliberative, so assets may provide structure but not review judgment. | `SFA-R6`, `SFA-R9`, `SFA-R10`, `SFA-R23`, `SFA-R24` | Validator fixtures reject policy-shaped review asset labels; M3 reviews are closed |
| `skills/test-spec/SKILL.md` and `skills/test-spec/assets/*` | Added `test-spec-skeleton.md`, `test-case.md`, and `coverage-map-row.md`; preserved requirement/example coverage row variants; kept edge-case row format inline. | Full skeleton and multi-field blocks earn assets; trivial edge-case rows do not. | `SFA-R5`, `SFA-R11`, `SFA-R12`, `SFA-R14` through `SFA-R22` | M4 row-shape preservation evidence; M6 lean asset proof |
| `scripts/skill_validation.py` | Added spec-family asset inventory checks, resource-map checks, asset metadata/status/placeholder checks, review-class boundary checks, generated-output presence helper, and reduced approved asset inventory after M6. | Make the asset contract deterministic rather than review-only. | `SFA-R42`, `SFA-R43`, `AC-SFA-015` | `python scripts/test-skill-validator.py` passed with 142 tests |
| `scripts/test-skill-validator.py` and `tests/fixtures/skills/published-design/generated-output-presence/` | Added positive and negative fixture coverage for generated asset presence and spec-family asset validation boundaries. | Prove canonical mapped assets must appear under supplied generated output roots without making M1 generate real archives. | `SFA-R32`, `SFA-R42`, `AC-SFA-009`, `AC-SFA-015` | Validator tests and generated-output proof |
| `docs/changes/.../baseline.md` | Added change-local baseline summary. | Let reviewers inspect which PR #79 structures were being preserved without redefining PR #79 as the baseline. | `SFA-R25` through `SFA-R27`, `AC-SFA-014` | M1 review closed after baseline and validator foundation |
| `docs/changes/.../behavior-preservation.md` | Recorded source-to-asset preservation, behavior parity, token counts, cold-read checks, and the final lean asset set. | Prove extraction did not change output behavior or hide rules. | `SFA-R28` through `SFA-R31`, `SFA-R38` through `SFA-R41` | Code-review M2-M6 records |
| `docs/changes/.../generated-output-proof.md` | Recorded generated skill mirror proof, temporary adapter archive proof, adapter validation, archive inspection, tracked-tree deferral, and M6 refreshed proof. | Prove assets reach published generated output without hand-editing generated adapter bodies. | `SFA-R32` through `SFA-R37`, `AC-SFA-009` through `AC-SFA-011` | `build-skills`, `build-adapters`, `validate-adapters`, and archive inspection passed |
| Proposal/spec/test-spec/plan/change metadata/review records | Added and kept lifecycle artifacts current through proposal review, spec review, plan review, implementation milestones, material finding resolution, and clean code reviews. | Preserve traceability and make the branch reviewable without relying on chat-only history. | Workflow contract and active plan | Review artifact closeout validates 15 reviews and 9 resolved findings |
| `docs/learn/sessions/...` and `docs/learn/topics/skill-asset-design.md` | Captured the asset-formalism lesson from M6. | Future asset work should apply the substantial-template and metadata-to-content checks before creating files. | M6 discovery and `SFA-R3A` through `SFA-R3C` | Learn artifacts are scoped guidance, not a replacement for specs or validators |

## Tests Added Or Changed

| Test surface | What changed | What it proves |
|---|---|---|
| `scripts/test-skill-validator.py` | Added spec-family asset contract checks and generated-output presence tests. | Mapped assets require `COPY`, valid metadata, approved statuses, valid placeholders, review-class boundaries, baseline-summary presence, and generated-output presence. |
| Generated-output fixtures | Added valid and missing-asset generated-output fixture shapes. | A canonical mapped asset missing from a supplied generated root fails deterministically. |
| Review-class fixtures | Added forbidden policy-label cases and allowed structural label cases. | `spec-review` assets may contain structural fields such as `Severity`, but not policy labels such as `Severity policy`. |
| Test-spec row-shape proof | Added/updated coverage around requirement and example coverage-map variants. | Requirement coverage preserves four cells; example coverage preserves three cells and does not gain a `Level` column. |

This is the right test level because the behavior is mostly static contract
validation and generated-output presence, not runtime application behavior.

## Validation Evidence Before Final Verify

Recorded validation includes:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/measure-skill-tokens.py`
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m6-adapters-ohAnao`
- `python scripts/validate-adapters.py --root /tmp/rigorloop-m6-adapters-ohAnao --version v0.1.5`
- Python `zipfile` inspection confirming current mapped assets are present and removed row assets are absent in all three temporary adapter archives
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`
- `git diff --check -- .`

Final verify has not run yet.

## Review Resolution Summary

Review resolution is closed:
`docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/review-resolution.md`.

- Reviews covered: 15
- Material findings resolved: 9
- Unresolved findings: 0
- Dispositions: 9 accepted, 0 rejected, 0 deferred, 0 needs-decision

The major implementation findings resolved generated-output presence coverage,
requirement modal preservation, review-class policy-label validation, and
test-spec coverage-map row-shape parity. M5 and M6 code reviews found no
blocking or required-change findings.

## Alternatives Rejected

- Add `references/` or `scripts/`: rejected because the approved scope was
  assets-only and behavior preservation outranked larger progressive-disclosure
  changes.
- Move rules or review judgment into assets: rejected because `SKILL.md` remains
  the operating contract.
- Keep one-line row assets: rejected in M6 because they duplicated inline format
  rules, had poor metadata-to-content ratio, and created drift surface without a
  meaningful common-path reduction.
- Require tracked-tree adapter proof as a hard blocker: rejected where known
  stale expanded-tree debt remains; temporary generated archive proof and
  adapter validation are still mandatory and were completed.
- Add a new architecture artifact: rejected because this change does not alter
  architecture, data flow, persistence, deployment, public adapter roots, or
  trust boundaries.

## Scope Control

The change does not add packaged `references/`, packaged `scripts/`, build-time
partials, routing changes, adapter install-root changes, lockfile changes, CLI
behavior changes, release archive trust-boundary changes, or assets for
unrelated lifecycle skills.

Generated public adapter bodies were not hand-edited. Temporary generated
output was used for proof.

## Risks And Follow-Ups

- Historical review records mention row assets that M6 later removed; they
  remain valid historical evidence, while current governing artifacts and
  generated-output proof reflect the lean asset set.
- Tracked expanded adapter tree debt remains deferred separately from temporary
  generated archive proof.
- Follow-up proposals remain separate for packaged `references/`, packaged
  `scripts/`, produced-artifact readability, and build-time partials.

## Readiness

All in-scope implementation milestones are closed and explain-change is now
recorded. The active plan may hand off to final `verify`; this artifact does
not claim final verify, branch readiness, PR readiness, or hosted CI status.
