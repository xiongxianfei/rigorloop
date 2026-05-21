# Proposal-Family Assets Progressive Disclosure Explain Change

## Summary

This change adds assets-only progressive disclosure to the `proposal` and
`proposal-review` skills. The operating contracts stay in each `SKILL.md`;
copy-and-fill output structures move into skill-local `assets/` files. The
change also adds deterministic validator coverage, pinned behavior-preservation
evidence, generated-output proof, token/P evidence, and formal review records.

## Problem

`proposal` and `proposal-review` were carrying large inline output structures in
their common-path skill bodies. That made two high-visibility published skills
harder to scan while mixing operating rules with reusable copy-and-fill
templates. The accepted direction was to apply the existing assets pattern
without moving rules, enums, review judgment, lifecycle boundaries, or handoff
behavior out of `SKILL.md`.

## Decision Trail

| Stage | Decision |
| --- | --- |
| Proposal | Use assets only; defer `references/`, `scripts/`, and build-time partials. |
| Proposal review | Resolve `PFA-PR1` through `PFA-PR4`: require an explicit test-spec route, preserve conditional proposal sections, define a review-class validator boundary, and pin the baseline identity. |
| Spec | Requirements `PFA-R1` through `PFA-R55` define the asset inventory, resource maps, behavior-preservation proof, generated-output proof, token/P evidence, and lifecycle validation. |
| Architecture | No separate architecture package was created because adapter roots, lockfiles, CLI behavior, and release trust boundaries remain unchanged. |
| Plan | M1 created baseline and validators; M2 extracted `proposal`; M3 extracted `proposal-review`; M4 recorded generated-output, token, P, cold-read, and lifecycle evidence. |
| Reviews | Code reviews closed M1 through M4. Material findings `PFA-M1-CR1` and `PFA-M3-CR1` were accepted and resolved. |

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/proposal/SKILL.md` | Added a `COPY` resource map for `assets/proposal-skeleton.md` and replaced the inline full skeleton with compact asset-copy guidance. | Satisfy `PFA-R5`, `PFA-R7`, `PFA-R12` through `PFA-R22` while keeping proposal rules and conditional-section triggers in `SKILL.md`. | Spec, M2 plan milestone | `python scripts/validate-skills.py skills/proposal/SKILL.md`; behavior-preservation evidence |
| `skills/proposal/assets/proposal-skeleton.md` | Added the full proposal skeleton as a normative copy-and-fill asset. | Move substantial output structure out of the common path without changing required proposal sections. | `PFA-R7`, `PFA-R17` through `PFA-R22` | Validator asset metadata/resource-map tests; M2 code review |
| `skills/proposal-review/SKILL.md` | Added `COPY` resource-map entries for result and material-finding assets and kept review rules inline. | Preserve review-class judgment in `SKILL.md` while extracting only structural result/finding templates. | `PFA-R6`, `PFA-R10` through `PFA-R13`, `PFA-R23` through `PFA-R28` | `python scripts/validate-skills.py skills/proposal-review/SKILL.md`; M3 reviews |
| `skills/proposal-review/assets/review-result-skeleton.md` | Added the review result structure, including the pinned `## Result` heading and literal `Skill: proposal-review` field. | Preserve baseline result field parity after `PFA-M3-CR1`. | Baseline, `PFA-R36`, `PFA-R37` | `test_proposal_review_result_skeleton_preserves_baseline_result_block` |
| `skills/proposal-review/assets/material-finding.md` | Added one structural material-finding block. | Provide a copy-and-fill structure for material findings without moving material-finding sufficiency rules into assets. | `PFA-R10`, `PFA-R23`, `PFA-R24` | Proposal-review asset allowlist and forbidden-policy tests |
| `scripts/skill_validation.py` | Added proposal-family approved asset inventory, metadata/resource-map/placeholder checks, `proposal-review` structural-label allowlist, forbidden review-policy checks, and baseline/generated asset presence helpers. | Make asset constraints deterministic instead of relying on review judgment alone. | `PFA-R23` through `PFA-R32`, `PFA-R51`, `PFA-R52` | `python scripts/test-skill-validator.py` |
| `scripts/test-skill-validator.py` | Added positive and negative fixtures for proposal-family assets, review-class labels, generated-output presence, and baseline preservation. | Prove allowed assets pass and hidden-policy, extra-asset, missing-field, and non-allowlisted-label cases fail. | Test spec `T2`, `T4`, `T5`, `T6` | 152 validator tests passed |
| `docs/changes/.../baseline.md` | Recorded pinned branch point, source hashes, source structures, extracted destinations, and rules that remain in `SKILL.md`. | Make behavior preservation reviewable against a durable source instead of a moving "current state." | `PFA-R33` through `PFA-R35` | M1 review and lifecycle validation |
| `docs/changes/.../behavior-preservation.md` | Recorded source-to-asset parity and behavior-preservation matrices for M2 and M3. | Prove field sets, obligations, conditional sections, enums, review dimensions, recording, and handoff behavior are unchanged. | `PFA-R36` through `PFA-R39` | M2/M3 code reviews |
| `docs/changes/.../generated-output-proof.md` | Recorded generated mirror proof, temporary adapter archive proof, adapter validation, tracked-tree deferral, token/P evidence, cold-read proof, and no-hand-edit evidence. | Complete M4 requirements for generated output and installed-skill usability. | `PFA-R40` through `PFA-R50` | M4 validation and code review |
| `specs/proposal-family-assets-progressive-disclosure.md` | Added the approved contract for the proposal-family asset rollout. | Convert the accepted direction into testable requirements and acceptance criteria. | Proposal review R2 | Spec review R1 |
| `specs/proposal-family-assets-progressive-disclosure.test.md` | Added traceable tests and proof responsibilities for every requirement and edge case. | Ensure implementation and review had an approved proof route. | Test-spec approval | Lifecycle validation |
| `docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md` and `docs/plan.md` | Recorded milestone state, decisions, validation, reviews, and current handoff. | Keep the active plan as the live workflow state owner. | RigorLoop workflow contract | Review artifact and lifecycle validation |
| `docs/changes/.../review-*` and `reviews/*.md` | Recorded proposal/spec/plan/code reviews, material findings, dispositions, and clean review receipts. | Formal lifecycle reviews require durable records. | Review recording contract | `python scripts/validate-review-artifacts.py --mode closeout ...` |
| `docs/changes/.../change.yaml` | Indexed artifacts, requirements, validation commands, and changed files. | Keep change metadata current for lifecycle validation. | Docs changes contract | `python scripts/validate-change-metadata.py ...` |

## Tests Added Or Changed

| Test/proof | What it proves |
| --- | --- |
| Proposal-family asset fixtures in `scripts/test-skill-validator.py` | Approved asset inventories, metadata, statuses, visible placeholders, `COPY` resource maps, and no filler placeholder text validate deterministically. |
| `proposal-review` allowed-label and forbidden-policy tests | Review assets accept only approved structural fields and reject review-policy labels or prose. |
| Non-allowlisted neutral-label regression tests | `Architecture impact`, `Testability notes`, `Rollout realism`, and `Strategic value` fail even when they do not match the forbidden-policy regex. |
| `test_proposal_review_result_skeleton_preserves_baseline_result_block` | The review result asset must preserve the pinned `## Result` heading and literal `Skill: proposal-review` field. |
| Generated asset presence fixture coverage | Proposal-family mapped assets are checked for generated skill and adapter output presence. |
| Manual preservation matrices | Field parity, conditional-section behavior, and rule ownership are preserved against the pinned baseline. |
| Manual token/P/cold-read proof | Common-path size, total package footprint, P estimates, asset usage clarity, and no-hand-edit evidence are recorded. |

## Validation Evidence Available Before Final Verify

Representative commands recorded in the active plan and `change.yaml`:

- `python scripts/test-skill-validator.py` - pass, 152 tests
- `python scripts/validate-skills.py` - pass, 23 skill files
- `python scripts/validate-skills.py skills/proposal/SKILL.md` - pass
- `python scripts/validate-skills.py skills/proposal-review/SKILL.md` - pass
- `python scripts/build-skills.py --check --output-dir /tmp/rigorloop-pfa-m4-skills-final-wybuIX/skills` - pass
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu` - pass
- `python scripts/validate-adapters.py --root /tmp/rigorloop-pfa-m4-adapters-final-bT9gTu --version v0.1.5` - pass
- Python `zipfile` inspection of temporary adapter archives - pass
- `python scripts/build-adapters.py --check --version v0.1.5 --verbose` - expected tracked-tree deferral
- `python scripts/measure-skill-tokens.py` - pass
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/change.yaml` - pass
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure` - pass
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` - pass
- `git diff --check --` - pass

No hosted CI, final verify, branch readiness, or PR readiness is claimed by this
artifact.

## Review Resolution Summary

`review-resolution.md` has `Closeout status: closed`.

Material findings:

- Proposal review: 4 accepted and resolved (`PFA-PR1` through `PFA-PR4`).
- Code review M1: 1 accepted and resolved (`PFA-M1-CR1`).
- Code review M3: 1 accepted and resolved (`PFA-M3-CR1`).

Clean review events after resolution:

- `proposal-review-r2`
- `spec-review-r1`
- `plan-review-r1`
- `code-review-m1-r2`
- `code-review-m2-r1`
- `code-review-m3-r2`
- `code-review-m4-r1`

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Do nothing | Leaves large skeletons in common-path skill bodies. |
| Add `references/`, `scripts/`, or build-time partials | Too broad for this slice and risks hiding rule-heavy guidance or changing authoring mechanics. |
| Apply assets only to `proposal` | Leaves the proposal family inconsistent and misses a narrow, structural review-result use case. |
| Add row-only assets | The approved asset guidance says tiny rows usually do not earn files. |
| Hand-edit generated adapter output | Violates the generated-output trust boundary; temporary generated archives provide proof instead. |
| Treat total-token reduction as the success metric | Skeleton assets can increase packaged footprint; the goal is common-path readability and maintainability with P recorded. |

## Scope Control

The change did not add packaged `references/`, packaged `scripts/`, build-time
partials, adapter install-root changes, lockfile changes, CLI behavior changes,
or assets for unrelated skills. Review dimensions, enums, recording rules,
Vision fit rules, standing artifact gates, scope rules, lifecycle boundaries,
and handoff behavior remain in `SKILL.md`.

## Risks And Follow-Ups

- Tracked expanded adapter output remains stale debt for `dist/adapters/`; M4
  records a deferral after temporary generated archive proof passed.
- Total packaged skill footprint grows, especially for skeleton assets. The
  proof records common-path reduction separately and records P for each asset.
- Final closeout is not complete until `verify` and PR handoff run.
- Follow-on proposals for `references/`, `scripts/`, or build-time partials
  remain out of scope.

## Readiness

The active plan says all implementation milestones are closed and the next
stage is the final closeout sequence. This explanation is ready for `verify`,
but it does not claim final verification, branch readiness, PR readiness, or CI
success.
