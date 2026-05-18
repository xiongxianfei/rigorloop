# Customer-Portable Public Skills Change Explanation

## Summary

This change makes public RigorLoop skills usable in customer projects that do not contain the RigorLoop repository's internal specs, docs, reports, governance files, follow-up files, scripts, templates, or generated adapter internals.

The implementation adds a concise customer-project portability rule to `docs/workflows.md`, adds project-local evidence wording to only the audited risky public skills, adds focused static validation for forbidden required internal-document dependencies, records before/after static skill token measurement, validates generated adapter output from canonical skills, and records a live customer-fixture dynamic benchmark.

The implementation milestones are closed. The active plan now hands off to `verify`; this explanation does not claim final verify, PR readiness, hosted CI, or Done.

## Problem

RigorLoop is installable outside this repository. Customer projects may have installed public skills, `rigorloop.yaml`, `rigorloop.lock`, optional local `docs/workflows.md`, local change roots, local specs/plans, and source files, but they usually do not have RigorLoop's internal repository artifacts.

Public skills that imply required reads of RigorLoop-internal `specs/`, `docs/`, `CONSTITUTION.md`, `AGENTS.md`, reports, or follow-ups are brittle and token-expensive in customer projects. The approved solution is to make skills carry the minimum portable operating contract, use project-local artifacts when present, and block on ambiguity when no safe default exists.

## Decision Trail

| Source | Decision or requirement | Impact on the diff |
|---|---|---|
| Proposal | Treat RigorLoop repository docs/specs as internal development authority, not required customer-project evidence. | Public skill wording now says local docs/specs/governance are project-local when present and relevant. |
| Proposal review | First slice must be audit-first, mode-aware, and limited to high-risk skills. | Only `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `verify`, `pr`, `project-map`, and `workflow` changed; `code-review` stayed unchanged. |
| Spec R1-R10 | Public skills operate in customer-project mode by default and must not require RigorLoop internals. | Added project-local evidence sections to audited risky skills. |
| Spec R11-R16 | `workflow` owns creating or refreshing local `docs/workflows.md`; stage skills use it only when present. | Added `docs/workflows.md` customer-project portability section and a short `workflow` skill caveat. |
| Spec R17-R25 | Preserve essential claim boundaries, output obligations, and safety behavior. | Token report records safety-preservation notes for each touched skill. |
| Spec R26-R28 | Add focused static validation without banning legitimate project-local docs/specs. | `scripts/test-skill-validator.py` now checks forbidden required RigorLoop-internal dependency wording and allowed guarded references. |
| Spec R29-R36 | Record static before/after token measurement and targeted customer-fixture dynamic benchmark evidence. | Added the token report, synthetic customer fixture, live benchmark runs, JSONL/analyzer summaries, and dynamic benchmark report. |
| Spec R37-R38 | Validate generated public adapter output from canonical skills; do not hand-edit generated bodies. | Adapter archives were built and validated from canonical `skills/`; generated bodies were not edited. |
| Plan M1 | Audit, workflow guidance, and baseline measurement before skill wording edits. | Baseline static tokens were measured before M2. |
| Plan M2 | Update only audited risky public skills and static validators. | Skill wording and validator tests changed. |
| Plan M3 | Record after-change measurement, dynamic evidence, adapter validation, and lifecycle evidence. | Measurement reports, fixture, run evidence, adapter validation evidence, and review records changed. |
| Code review R3 | `CPS-M3-CR1`: static-only benchmark evidence could not support runtime portability claims. | Replaced the rejected benchmark evidence with live `codex exec` scenario JSONL and analyzer summaries. |
| Code review R4 | Clean review for M3. | Closed `CPS-M3-CR1` and moved the plan to final closeout readiness. |

Architecture was not required because this is a public skill wording, validation, documentation, measurement, and lifecycle-evidence change with no runtime architecture change.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test or evidence |
|---|---|---|---|---|
| `docs/workflows.md` | Added `Customer-project portability`. | Establishes the project-local rule: use local artifacts when present, do not require RigorLoop internals, use safe defaults or block on ambiguity. | R11-R16, M1 | `test_customer_project_portability_workflow_guide`; M1 validation. |
| `skills/workflow/SKILL.md` | Added a short customer-project workflow guide caveat. | Makes `workflow` the owner for creating or refreshing local `docs/workflows.md` without making RigorLoop internals required. | R11, R13-R16, M1 | `test_workflow_skill_customer_project_guide_caveat`. |
| `skills/proposal/SKILL.md` | Added `Project-local evidence`. | Prevents proposal work in customer projects from treating local governance/spec/doc references as RigorLoop-repository dependencies. | R1-R10, R17-R25, M2 | M2 static validator and safety-preservation note. |
| `skills/proposal-review/SKILL.md` | Added `Project-local evidence`. | Keeps proposal review grounded in proposal/user/local artifacts without broad-searching for RigorLoop originals. | R1-R10, R17-R25, M2 | M2 static validator and safety-preservation note. |
| `skills/spec/SKILL.md` | Added `Project-local evidence`. | Makes specs use local workflows, local specs, local architecture, and local governance only when present and relevant. | R1-R10, M2 | M2 static validator and safety-preservation note. |
| `skills/plan/SKILL.md` | Added `Project-local evidence`. | Keeps planning evidence customer-local and preserves portable defaults or ambiguity blocks. | R1-R10, M2 | M2 static validator and safety-preservation note. |
| `skills/implement/SKILL.md` | Added `Project-local evidence`. | Ensures implementation starts from local plan/spec/test/architecture/code/validation evidence, especially the active plan handoff, without requiring RigorLoop internals. | R1-R10, R17-R25, M2 | M2 static validator and safety-preservation note. |
| `skills/verify/SKILL.md` | Added `Project-local evidence` and a no-false-validation-claim boundary. | Prevents final verification from treating absent RigorLoop governance as required and preserves validation-evidence honesty. | R1-R10, R17-R25, M2 | M2 static validator; live `verify-customer-final-pack` benchmark. |
| `skills/pr/SKILL.md` | Added `Project-local evidence` and readiness/no-false-claim wording. | Keeps PR preparation based on local diff/evidence/verify output rather than absent RigorLoop internals. | R1-R10, R17-R25, M2 | M2 static validator; live `pr-customer-ready-handoff` benchmark. |
| `skills/project-map/SKILL.md` | Added `Customer-project orientation`. | `project-map` can read local `docs/`, `specs/`, `AGENTS.md`, or `CONSTITUTION.md` when present, but absence is normal and should not trigger searches for RigorLoop originals. | R18, R25, EC10-EC11, M2 | `test_project_map_treats_local_orientation_inputs_as_optional`; live `project-map-customer-repo-orientation` benchmark. |
| `scripts/test-skill-validator.py` | Added customer-portable static checks. | Proves the public workflow/skill surfaces contain the required local evidence contract and block obvious required RigorLoop-internal dependencies while allowing guarded project-local references. | R26-R28, T2-T6, M1-M2 | `python scripts/test-skill-validator.py`. |
| `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md` | Added audit evidence, baseline/after static measurement, safety notes, dynamic summary, and adapter validation evidence. | Centralizes first-slice measurement and migration evidence outside release reports. | R29-R38, T7-T10, M1-M3 | Baseline 58,868 estimated tokens; after-change 60,235 estimated tokens; adapter validation passed. |
| `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md` | Added live customer-fixture dynamic benchmark results. | Proves runtime customer-project portability instead of relying on static wording alone. | R32-R36, T9, `CPS-M3-CR1` | Live `codex exec` JSONL and analyzer summaries for required scenarios. |
| `docs/reports/token-cost/skills/fixtures/customer-portable-public-skills/` | Added synthetic customer fixture. | Provides a clean customer project with local workflow/config/change/spec/plan/source/test files and no RigorLoop internals. | R33, T9, T12 | Fixture exclusion command passed. |
| `docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/` | Added prompts, JSONL, and analyzer summaries. | Preserves per-scenario runtime evidence for input tokens, command output, reads, searches, and result quality. | R36, T9, `CPS-M3-CR1` | Analyzer summaries record measured fields for each scenario. |
| `docs/proposals/...`, `specs/customer-portable-public-skill-evidence.md`, `specs/customer-portable-public-skill-evidence.test.md`, `docs/plans/...`, `docs/plan.md` | Added and maintained lifecycle artifacts. | Keeps the change traceable through proposal, spec, test spec, plan milestones, review outcomes, and active plan handoff. | Workflow contract and AGENTS lifecycle rules | Lifecycle validator and review artifact validator passed. |
| `docs/changes/.../review-log.md`, `review-resolution.md`, `reviews/*.md`, `change.yaml` | Recorded formal review evidence and metadata. | Required because formal lifecycle reviews found material findings and later closed them. | Formal review recording rules | `validate-review-artifacts` and `validate-change-metadata` passed. |

`skills/code-review/SKILL.md` did not change. The audit found no direct required RigorLoop-internal dependency, and the proposal explicitly warned against editing this safety-critical skill without a concrete need.

## Tests Added Or Changed

The main executable test changes are in `scripts/test-skill-validator.py`.

| Test area | What it proves | Why this level is appropriate |
|---|---|---|
| Workflow portability checks | `docs/workflows.md` and `workflow` contain the customer-project portability and local-guide ownership rules. | These are static public wording contracts. |
| M2 skill local evidence checks | Audited skills contain customer-project mode, project-local evidence, no required RigorLoop internals, portable defaults, ambiguity blocking, and local `docs/workflows.md` guidance. | Public skill behavior is text-driven, so static proof is the right first gate. |
| Required internal dependency detector examples | Obvious required RigorLoop-internal dependency wording is rejected while guarded project-local or direct-target references remain allowed. | This keeps validation precise and avoids banning legitimate customer `docs/` or `specs/`. |
| `project-map` optional-local-input check | Local `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` are optional orientation inputs. | `project-map` is a special case that should map customer repositories without requiring RigorLoop originals. |
| Published surface checks | Published skill text stays portable and avoids required RigorLoop-internal dependencies. | This guards the public skill contract from regression. |

No product runtime tests were added because the change does not alter CLI/runtime product behavior.

## Validation Evidence Available Before Final Verify

Recorded validation includes:

```bash
python scripts/measure-skill-tokens.py
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-BxELAV
python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m3-BxELAV --version v0.1.5
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-live
codex exec --json --ephemeral --skip-git-repo-check "<scenario prompt>"
python scripts/analyze-codex-jsonl.py <scenario>.jsonl --summary-output <scenario>.analysis.yaml --run-id <scenario>
python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml
python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
git diff --check --
```

Static token measurement:

| Measurement | Estimated tokens |
|---|---:|
| Baseline before M2 skill wording | 58,868 |
| After M2 skill wording | 60,235 |
| Delta | +1,367 |

Live dynamic benchmark:

| Scenario | Runtime result |
|---|---|
| `proposal-customer-no-internal-docs` | pass |
| `proposal-review-customer-local-artifacts` | pass |
| `spec-customer-local-workflow-guide` | pass |
| `plan-customer-local-spec-and-code` | pass |
| `implement-customer-plan-handoff` | pass |
| `workflow-customer-route-no-internal-docs` | pass |
| `project-map-customer-repo-orientation` | pass-with-warning |
| `verify-customer-final-pack` | pass-with-warning |
| `pr-customer-ready-handoff` | pass |

The warnings are recorded rather than hidden: `project-map` performed expected repository-orientation searches, and `verify` performed one bounded local governance absence check. No scenario relied on absent RigorLoop repository internals.

This is pre-verify evidence only. Final `verify` has not yet run.

## Review Resolution Summary

Review resolution is recorded in `docs/changes/2026-05-18-customer-portable-public-skills/review-resolution.md`.

| Finding | Disposition | Closeout |
|---|---|---|
| `CPS-PR1` | accepted | closed by proposal revision and proposal-review R2 |
| `CPS-PLAN-1` | accepted | closed by plan revision and plan-review R2 |
| `CPS-M3-CR1` | accepted | closed by live dynamic benchmark fix and code-review R4 |

Review-resolution closeout status is closed, and `review-log.md` records no open findings.

## Alternatives Rejected

| Alternative | Why rejected |
|---|---|
| Rewrite every public skill for uniform wording. | The accepted scope required audit-first edits to high-risk skills only. |
| Require `docs/workflows.md` for every task. | Customer projects may not have it; stage skills must use portable defaults when safe and block on ambiguity when needed. |
| Treat customer `docs/` or `specs/` paths as forbidden. | Customer projects can legitimately have local docs/specs; the risk is requiring RigorLoop repository-internal docs. |
| Edit `code-review` preemptively. | It is safety-critical and audit found no direct required internal-doc dependency. |
| Hand-edit generated adapter skill bodies. | The single-authored source model requires generated adapters to be built from canonical `skills/`. |
| Close M3 with static-only benchmark evidence. | `CPS-M3-CR1` correctly found that runtime portability needs measured dynamic evidence or an honest blocked state. |
| Run a full release benchmark suite. | The spec limits this first slice to targeted customer-fixture scenarios, not a release benchmark expansion. |

## Scope Control

The change preserves these non-goals:

- no `rigorloop status`;
- no `rigorloop validate`;
- no workflow YAML;
- no generated workflow docs;
- no hard token gates;
- no full release benchmark suite;
- no generated adapter body edits;
- no broad skill rewrite;
- no `code-review` wording change.

## Risks And Follow-Ups

Residual risks before final verify:

- The static skill text grew by 1,367 estimated tokens. The increase is recorded because portability wording was added rather than optimized away.
- The live dynamic benchmark is targeted to the first slice. It proves the required scenarios, not all possible customer workflows.
- `project-map` and `verify` have recorded warning-level broad-search counts. The report treats those as bounded and expected, but final verify should still inspect the benchmark evidence for drift.
- Plan index state is still active because final closeout, verify, and PR handoff are not complete.

Recommended next stage: `verify`.
