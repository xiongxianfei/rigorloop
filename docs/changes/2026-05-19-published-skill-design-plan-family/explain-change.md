# Published Skill Design Plan Family Explain Change

Change: `2026-05-19-published-skill-design-plan-family`
Date: 2026-05-19
Status: ready for verify

## Summary

This change continues the published-skill design rollout for the next lifecycle
pair after the proposal and spec families: `plan` and `plan-review`.

It creates the plan-family lifecycle evidence, adds deterministic regression
coverage for that evidence, rewrites only the two target skill bodies to the
published-skill design contract, records clean code-review receipts for all
implementation milestones, and moves the active plan into final closeout.

## Problem

Published RigorLoop skills are installed into customer-project environments
where adopters may not have RigorLoop maintainer-only repository files. The
skills therefore need to be portable operating documentation: their
frontmatter must route reliably, their bodies must execute the workflow, and
their output/validation boundaries must preserve lifecycle claims.

The earlier proposal-family and spec-family rollouts handled `proposal`,
`proposal-review`, `spec`, and `spec-review`. The next pair was `plan` and
`plan-review` because they own execution planning, current handoff state,
formal plan review, and pre-implementation readiness.

## Decision Trail

| Source | Decision or requirement | Effect in this change |
|---|---|---|
| Proposal | Continue published-skill design through small skill-family slices. | Created a separate plan-family rollout instead of broad all-skill rewrite. |
| `specs/skill-contract.md` | Published skills use `description` for routing, workflow-role blocks for lifecycle ownership, output skeletons, self-containment, resource-map rules, behavior preservation, parity evidence, and token discipline. | `plan` and `plan-review` now opt into `skill-readability-v1` and carry the required sections. |
| `specs/skill-contract.test.md` `T25` | Audit and evidence must exist before skill rewrites. | Added `skill-audit.md`, `routing-coverage.md`, `behavior-preservation.md`, and `behavior-parity.md`. |
| `T26` | Deterministic validator support must stay static and bounded. | Added focused plan-family regression coverage in `scripts/test-skill-validator.py`; no production validator behavior changed. |
| `T27` | The rewrite must preserve lifecycle behavior. | Recorded final preservation and parity evidence for `plan` and `plan-review`. |
| `T28` | Generated skill and adapter proof must come from canonical `skills/`. | Ran generated-skill checks and temporary adapter archive build/validation. |
| Plan M1 | Audit and scaffold evidence first. | Created evidence files and token baselines. |
| Plan M2 | Add deterministic proof only if needed. | Added regression tests for evidence shape and boundaries. |
| Plan M3 | Rewrite only `plan` and `plan-review`. | Updated the two skill bodies and final evidence; left other skills untouched. |

Architecture work was not required because this slice changed skill text,
tests, and lifecycle evidence only. It did not add runtime components,
persistence, APIs, deployment, or hard-to-reverse data flow.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
|---|---|---|---|---|
| `docs/plans/2026-05-19-published-skill-design-plan-family.md` | Created and maintained the active plan, milestone states, validation notes, decisions, surprises, and final closeout handoff. | The workflow requires a concrete plan body for planned multi-milestone work and a single current handoff owner. | Plan skill contract, active plan policy, `T25`-`T28`. | Plan-review R1, code-review M1/M2/M3, lifecycle validation. |
| `docs/plan.md` | Added the plan-family rollout to the active plan index during planning. | `docs/plan.md` is the lifecycle index; concrete plan content lives under `docs/plans/`. | Plan file policy. | Artifact lifecycle validation and selected CI. |
| `docs/changes/.../change.yaml` | Recorded requirements, tests, changed files, validation evidence, and latest clean review pointer. | Non-trivial planned work needs durable change metadata and validation evidence. | Workflow contract and change metadata validation. | `python scripts/validate-change-metadata.py`. |
| `docs/changes/.../review-log.md` and `reviews/*.md` | Recorded plan-review and M1/M2/M3 code-review receipts. | Formal lifecycle reviews must be recorded; clean reviews use receipts, not empty review resolutions. | Formal review recording contract. | `python scripts/validate-review-artifacts.py --mode closeout`. |
| `docs/changes/.../skill-audit.md` | Classified `plan` and `plan-review` against the existence gate and rollout findings. | M1 needed evidence before any rewrite. | `T25`, plan M1. | Plan-family regression tests and code-review M1. |
| `docs/changes/.../routing-coverage.md` | Recorded positive triggers, near misses, competing skills, prompt fixtures, and final M3 routing result. | Routing tests are fixture/transcript evidence, not runtime auto-selection proof. | `R29`, `R35`, `T25`, `T27`. | `test_published_design_plan_family_routing_coverage_fixture_is_bounded`. |
| `docs/changes/.../behavior-preservation.md` | Recorded behavior-significant rules and M3 preservation locations. | Rewriting skill text must not weaken plan-state ownership or formal review semantics. | `R36`, `T27`. | `test_published_design_plan_family_preservation_and_parity_are_scaffolded`. |
| `docs/changes/.../behavior-parity.md` | Recorded representative parity cases and final token deltas. | The rewrite needed proof that lifecycle behavior and token budget were preserved. | `T27`, token budget decision. | Token measurement and plan-family regression tests. |
| `specs/skill-contract.test.md` | Added plan-family test cases `T25` through `T28`. | The test spec needed traceable coverage before implementation. | Test-spec stage and approved plan. | Test-spec validation and selected CI. |
| `scripts/test-skill-validator.py` | Added focused plan-family regression tests and readability opt-in assertions. | The deterministic proof belongs in fixture-style regression checks, not broad semantic scoring. | `T26`, `T27`. | `python scripts/test-skill-validator.py` passed 115 tests. |
| `skills/plan/SKILL.md` | Added `version`, `schema-version`, routing-focused description, workflow role, project-local/self-containment wording, and compact output skeleton. | `plan` needed to be portable, route through `description`, preserve handoff/state ownership, and satisfy the readability contract. | `R27`-`R35`, `T27`. | `python scripts/validate-skills.py`, plan-family regression, token measurement. |
| `skills/plan-review/SKILL.md` | Added `version`, `schema-version`, routing-focused description, workflow role, compact output skeleton, and tighter review guidance. | `plan-review` needed clearer near-miss routing and explicit review-stage claim boundaries without weakening recording behavior. | `R27`-`R35`, `T27`. | `python scripts/validate-skills.py`, plan-family regression, token measurement. |

## Tests Added Or Changed

`scripts/test-skill-validator.py` gained plan-family coverage:

- `test_published_design_plan_family_routing_coverage_fixture_is_bounded`
- `test_published_design_plan_family_audit_records_deterministic_gaps`
- `test_published_design_plan_family_preservation_and_parity_are_scaffolded`
- `test_skill_readability_plan_family_opts_into_contract`

These tests prove deterministic evidence shape, not natural-language routing
quality or runtime model selection. The M3 TDD loop first failed because
`plan` and `plan-review` had not yet opted into `skill-readability-v1`; it
passed after the skill-body rewrite and evidence updates.

## Validation Evidence Available Before Final Verify

Validation recorded so far:

```bash
python scripts/test-skill-validator.py -k plan_family
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/measure-skill-tokens.py --skills-root skills
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-plan-family-adapters-m3
python scripts/validate-adapters.py --root /tmp/rigorloop-plan-family-adapters-m3 --version v0.1.5
python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-plan-family/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-published-skill-design-plan-family
git diff --check -- ...
bash scripts/ci.sh --mode explicit ...
```

The latest selected CI for M3 passed these selected checks:

- `skills.validate`
- `skills.regression`
- `skills.generation_regression`
- `skills.drift`
- `adapters.drift`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`

Token evidence:

| Skill | Baseline estimated tokens | Final estimated tokens | Delta | Result |
|---|---:|---:|---:|---|
| `plan` | 3518 | 3862 | +9.78% | within +10% hard cap |
| `plan-review` | 1631 | 1794 | +9.99% | within +10% hard cap |

Hosted CI has not been observed for this local branch yet. Final `verify` and
PR readiness are intentionally not claimed by this explanation.

## Review Resolution Summary

No material review findings were recorded for this plan-family rollout.

Clean review receipts:

- `plan-review-r1`
- `code-review-m1-r1`
- `code-review-m2-r1`
- `code-review-m3-r1`

No `review-resolution.md` was required because all formal reviews were clean
or approved with no material findings.

## Alternatives Rejected

| Alternative | Why not used |
|---|---|
| Rewrite all remaining skills now. | The approved rollout is incremental; this slice is limited to `plan` and `plan-review`. |
| Modify production validator logic in M2. | M1 found no production validator gap; deterministic evidence checks were sufficient. |
| Add broad semantic routing tests. | The spec/test-spec require bounded fixture evidence, not runtime model auto-selection scoring. |
| Hand-edit generated adapter output. | Canonical authored skill source is `skills/`; adapter proof uses temporary generated archives. |
| Let token cost exceed the hard cap. | The approved budget is zero target, +5% tolerance with rationale, +10% hard cap. The M3 draft was compacted to stay under the cap. |
| Change `implement`, `code-review`, or workflow stage ownership in this slice. | Those are separate skill families or workflow contracts outside the approved plan-family scope. |

## Scope Control

Preserved non-goals:

- no all-skill rewrite;
- no `implement`, `code-review`, `verify`, `pr`, or `workflow` edits;
- no skill merge, retirement, rename, removal, or ownership change;
- no workflow stage-order change;
- no `when_to_use` requirement;
- no broad semantic scoring or runtime skill auto-selection claim;
- no generated public adapter source edits;
- no branch-ready, PR-ready, or final verification claim.

## Risks And Follow-Ups

Remaining risks are downstream lifecycle risks, not known implementation
defects:

- final `verify` still needs to rerun the required proof set and check artifact
  coherence;
- PR handoff must summarize the actual diff and validation evidence without
  claiming hosted CI until observed;
- final lifecycle closeout must update plan state only after the downstream
  completion events actually happen.

After this explanation was recorded, the active plan was updated to report:

```text
Next stage: verify
Remaining completion gates: verify, PR handoff, hosted CI observation if a PR
is opened, merge, and final lifecycle closeout.
```

This explanation does not claim final verification or PR readiness.
