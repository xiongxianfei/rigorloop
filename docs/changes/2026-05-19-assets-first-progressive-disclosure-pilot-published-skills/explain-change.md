# Assets-First Progressive Disclosure Pilot Explain Change

Change: `2026-05-19-assets-first-progressive-disclosure-pilot-published-skills`
Date: 2026-05-19
Status: final closeout recorded

## Summary

This change proves the first packaged-resource progressive-disclosure pilot for
published skills by moving the `plan` skill's reusable output structure into
four packaged `assets/` templates while keeping execution rules in
`skills/plan/SKILL.md`.

It adds deterministic validator fixtures, rewrites only the approved `plan`
skill surface, updates adapter archive packaging so skill-local resources ship
with generated adapters, records behavior and token evidence, closes all three
implementation milestones through clean code review, and routes the resulting
deterministic change-local evidence through PR-mode selected CI.

## Problem

The published-skill design contract recommended progressive disclosure, but
prior skill rewrites stayed flat: `SKILL.md` carried the operating procedure,
output skeletons, examples, and repeated structures inline. That kept early
readability work low-risk but left packaged resources unproven.

The accepted proposal chose the narrowest useful pilot: `assets/` only, one
skill, no `references/`, no packaged `scripts/`, and no build-time partials.
The pilot needed to prove that the installed skill stays self-contained, that
adapter archives include non-empty skill-local assets, and that behavior parity
outranks token savings.

## Decision Trail

| Source | Decision or requirement | Effect in this change |
| --- | --- | --- |
| Proposal | Pilot `assets/` only on `plan`. | No other published skill body was rewritten for this pilot. |
| Proposal review | Clarify spec-slice dependency, handoff asset boundary, output skeleton boundary, and deterministic validation oracle. | The proposal, spec, plan, and tests name those boundaries before implementation. |
| `specs/skill-contract.md` R37-R38 | Keep the pilot follow-on and limited to exactly four normative `plan` assets. | `skills/plan/assets/` contains `plan-skeleton.md`, `milestone.md`, `current-handoff-summary.md`, and `decision-log-row.md`. |
| R39-R42 | Require `Resource map`, literal `COPY`, metadata comments, normative status, structural fingerprints, and drift behavior. | `skills/plan/SKILL.md`, assets, validator fixtures, and tests enforce the multi-file contract. |
| R43 | Keep validation deterministic and avoid broad semantic scoring. | Validator checks are path, metadata, section, placeholder, fingerprint, and resource-map based. |
| R44 | Prove no regression and at least 15 percent common-path token reduction. | Token evidence records a 15.04 percent `SKILL.md` reduction and total packaged content below the 10 percent hard cap. |
| R45 | Separate strict contract-era reference corpus from historical coverage corpus. | `behavior-parity.md` and `historical-coverage.md` use separate corpora and expectations. |
| Test spec T33-T36 | Sequence the proof into validator support, asset split, and final adapter/token/parity proof. | M1, M2, and M3 each close a reviewable implementation slice. |

Architecture work was not required. The change affects Markdown contracts,
static validators, deterministic fixtures, adapter archive contents, and
change-local evidence. It does not add runtime services, persistence, APIs,
deployment boundaries, or hard-to-reverse data flow.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` | Recorded the accepted proposal with proposal-review clarifications. | Establishes the assets-first pilot direction and constraints. | Proposal review APD-PR1 through APD-PR4. | Proposal-review R2 and lifecycle validation. |
| `specs/skill-contract.md` | Added R37-R45 for the assets-first `plan` pilot. | Makes the pilot contract normative and testable. | Accepted proposal and spec review. | Spec-review R1. |
| `specs/skill-contract.test.md` | Added T33-T36 for scope, resource-map/metadata/drift, skeleton/handoff boundaries, and adapter/token/parity proof. | Test-spec stage needed concrete proof before implementation. | R37-R45. | Owner-approved test spec and selected CI. |
| `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` | Created and maintained the active plan, milestone states, decisions, validation notes, and final closeout handoff. | Planned multi-milestone work needs one live plan-body state owner. | Plan policy and T33-T36. | Plan-review R2 and code-review M1/M2/M3. |
| `docs/plan.md` | Added the initiative to the active plan index and kept next-stage state synchronized. | `docs/plan.md` is the lifecycle index. | Plan file policy. | Artifact lifecycle validation. |
| `docs/changes/.../change.yaml` | Recorded requirements, changed files, validation commands, and review/closeout evidence. | Non-trivial work needs durable change metadata. | Workflow contract. | `validate-change-metadata.py`. |
| `docs/changes/.../review-log.md`, `review-resolution.md`, and `reviews/*.md` | Recorded proposal, spec, plan, and code reviews, including APD-CR1 resolution and clean M3 review. | Formal lifecycle reviews require durable evidence. | Review recording contract. | `validate-review-artifacts.py`. |
| `scripts/skill_validation.py` | Added scoped deterministic `plan` asset-pilot validation. | M1 needed validator support for exact asset count, metadata, resource-map coverage, placeholders, forbidden root dependencies, fingerprints, and section parity. | R39-R43, T34. | `scripts/test-skill-validator.py` fixtures. |
| `scripts/test-skill-validator.py` and `tests/fixtures/skills/published-design/*` | Added positive and negative plan asset fixtures, including missing metadata, missing resource-map entry, non-`COPY`, missing fields, root dependency, fingerprint mismatch, and section mismatch. | Direct regression proof was required before changing the real skill. | T33-T35 and APD-CR1. | `python scripts/test-skill-validator.py`. |
| `skills/plan/SKILL.md` | Shortened common-path body, added `Resource map`, retained lifecycle and handoff rules, and pointed to packaged assets for full output structure. | Proves progressive disclosure while keeping rules in `SKILL.md`. | R37-R41, R44. | `validate-skills.py`, `test-skill-validator.py`, token evidence, code-review M2/M3. |
| `skills/plan/assets/*.md` | Added four normative structural templates with metadata, fingerprints, and placeholders. | Assets are copied/fillable structures, not hidden workflow policy. | R38, R40-R42. | Asset fixtures, validator checks, behavior preservation. |
| `scripts/adapter_distribution.py` | Included skill-local `assets/`, `references/`, and `scripts/` files in expected adapter archive output when present. | Adapter archives must preserve installed-skill self-containment for packaged resources. | R43a, T36. | Adapter fixture test and archive validation. |
| `scripts/test-adapter-distribution.py` and `tests/fixtures/adapters/portable-with-assets/*` | Added a regression test proving a packaged asset appears in codex, claude, and opencode archives and is validated by archive drift checks. | M3 needed direct adapter packaging proof for non-empty skill-local resources. | T36. | Failing-before-passing adapter test. |
| `scripts/validation_selection.py` and `scripts/test-select-validation.py` | Classified `adapter-packaging.md`, `historical-coverage.md`, and `token-cost.md` as deterministic change-local lifecycle evidence. | PR #75 hosted CI initially blocked on manual routing for these evidence files even though they are validated through `artifact_lifecycle.validate`. | Final closeout CI-maintenance. | `python scripts/test-select-validation.py`; PR-mode selected CI. |
| `docs/changes/.../behavior-preservation.md` | Recorded behavior-sensitive `plan` rules and preserved locations. | Moving structure to assets must not move lifecycle policy. | R41, R44a. | Code-review M2/M3. |
| `docs/changes/.../behavior-parity.md` | Recorded strict reference-corpus parity and milestone asset reuse. | No-regression evidence must cover plan sections, handoff, decision log, validation, claim boundaries, and recording discipline. | R44a, R44e, R45a-R45b. | M3 review and recorded reference corpus. |
| `docs/changes/.../historical-coverage.md` | Recorded historical corpus coverage separately from strict parity. | Older plans are coverage evidence, not current-contract structural references. | R45c-R45d. | M3 review. |
| `docs/changes/.../adapter-packaging.md` | Recorded real generated archive inventory for all four `plan` assets across codex, claude, and opencode. | Adapter packaging proof must be explicit and reviewable. | T36. | Build, validate, and direct archive inspection. |
| `docs/changes/.../token-cost.md` | Recorded baseline and final common-path and packaged-content measurements. | The pilot must demonstrate improvement, not just mechanism. | R44b-R44d. | `measure-skill-tokens.py`. |

## Tests Added Or Changed

`scripts/test-skill-validator.py` gained plan-asset pilot coverage for:

- exact four-asset inventory;
- required metadata, normative status, structural fingerprints, and maintained-alongside comments;
- resource-map coverage with literal `COPY`, trigger condition, fields to fill, and no unfilled placeholders;
- visible placeholders;
- forbidden repository-root internal dependencies;
- full-skeleton section-set parity;
- direct APD-CR1 missing resource-map-entry proof.

`scripts/test-adapter-distribution.py` gained
`test_adapter_archives_include_packaged_skill_assets`, which first failed
because generated archives omitted `assets/template.md`, then passed after
packaged resource copying was added.

The test level is intentionally static and fixture-based. The governing spec
for this pilot rejects broad semantic scoring and requires deterministic
validators plus review-recorded parity evidence.

## Validation Evidence Available Before Final Verify

Validation recorded before this final explanation includes:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/measure-skill-tokens.py --skills-root skills
python scripts/build-skills.py --check
python scripts/test-adapter-distribution.py
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m3-adapters-final
python scripts/validate-adapters.py --root /tmp/rigorloop-m3-adapters-final --version v0.1.5
python scripts/validate-change-metadata.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/change.yaml
python scripts/validate-review-artifacts.py docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check -- ...
bash scripts/ci.sh --mode explicit ...
```

Latest selected CI after M3 code-review recording passed:

- `review_artifacts.validate`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`

M3 selected CI also passed the skill and adapter checks:

- `skills.validate`
- `skills.regression`
- `skills.generation_regression`
- `skills.drift`
- `adapters.regression`
- `adapters.drift`
- `adapters.validate`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`

The full `python scripts/test-adapter-distribution.py` run exits 0 but emits
the existing stdout diagnostic:

```text
token-cost report validation failed: dynamic_runtime.runs: missing required benchmark architecture-review
```

That diagnostic is recorded as residual noise, not a failing M3 validation.
Final local verify passed, then PR #75 hosted CI exposed a selector-maintenance
gap for three deterministic change-local evidence files. The selector fix
passed:

```bash
python scripts/test-select-validation.py
bash scripts/ci.sh --mode pr --base 9d1487500b4ea62909c98975e694611f71139b04 --head HEAD
```

Hosted CI passed on PR #75 after the selector maintenance was pushed. The
agent-owned final closeout is recorded; human review and merge remain outside
this plan's agent-owned closeout.

## Review Resolution Summary

Material findings were recorded and closed in
`docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-resolution.md`.

| Disposition | Count |
| --- | ---: |
| accepted | 6 |
| rejected | 0 |
| deferred | 0 |
| partially accepted | 0 |
| needs decision | 0 |

Closed material findings:

- proposal-review: APD-PR1, APD-PR2, APD-PR3, APD-PR4;
- plan-review: APD-PLR1;
- code-review M1: APD-CR1.

Clean implementation review receipts:

- `code-review-m1-r2`;
- `code-review-m2-r1`;
- `code-review-m3-r1`.

## Alternatives Rejected

| Alternative | Why not used |
| --- | --- |
| Do nothing. | Progressive disclosure would remain guidance without a packaged-resource proof. |
| Add `assets/`, `references/`, and `scripts/` together. | Too much surface area for the first pilot; scripts and references add separate semantics and safety concerns. |
| Retrofit `proposal` or `proposal-review`. | The proposal intentionally avoided reopening settled or in-flight skill rewrites. |
| Keep the full plan skeleton duplicated in `SKILL.md` and `assets/plan-skeleton.md`. | The accepted output-skeleton boundary makes the asset the reviewed equivalent template and avoids drift-prone duplication. |
| Treat historical plans as strict parity references. | R45 requires historical plans to be coverage evidence only because they predate the current contract. |
| Hand-edit generated adapter output. | Adapter proof must come from canonical `skills/` and generated archives. |
| Add broad prose scoring to validators. | R43 forbids broad semantic scoring for this pilot. |

## Scope Control

Preserved non-goals:

- no changes to `proposal`, `proposal-review`, `spec`, `spec-review`, `code-review`, `verify`, or `pr` skill bodies;
- no packaged `references/` or packaged `scripts/` shipped by the `plan` pilot;
- no build-time partials or include syntax;
- no adapter install-root, lockfile, release archive trust-boundary, or CLI behavior changes;
- no hand-edited generated public adapter output;
- no hidden workflow rules in assets;
- no strict structural parity claim for historical plans.

## Risks And Follow-Ups

Remaining risks are closeout and follow-on risks, not known implementation
defects:

- human review and merge remain outside this plan's agent-owned closeout;
- the existing token-cost diagnostic in `test-adapter-distribution.py` remains
  visible stdout noise despite exit 0;
- future packaged-resource proposals should choose patterns by skill type:
  constructive skills primarily use `assets/`, while deliberative skills
  should usually consider `references/` first.

The active plan is closed as done for agent-owned final closeout after PR #75
and hosted CI success.
