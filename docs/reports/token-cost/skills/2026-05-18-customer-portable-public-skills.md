# Customer-Portable Public Skills Token Report

## Status

M3 measurement evidence recorded. Static after-change measurement, targeted customer-fixture benchmark evidence, and generated adapter validation evidence are recorded for the first slice.

## First-slice audit

The first-slice audit confirmed the implementation should touch only audit-proven risky skills plus workflow guidance:

| Skill | M1 audit decision | Reason |
|---|---|---|
| `proposal` | touch in M2 | Names local governance, project map, existing specs/ADRs, vision, and workflow guidance as evidence or gates; M2 must make those project-local, conditional, or repository-mode references. |
| `proposal-review` | touch in M2 | Reads standing instructions, vision/governance, linked specs/ADRs/plans, project map, and workflow guidance; M2 must prevent broad search for RigorLoop originals. |
| `spec` | touch in M2 | Inputs include governance, project map, related specs, architecture docs, and ADRs; M2 must make them project-local when present and relevant. |
| `plan` | touch in M2 | Inputs include governance, plan docs, project map, accepted proposal, spec, architecture, test spec, code/tests/CI; M2 must add customer-project mode wording. |
| `implement` | touch in M2 | Inputs include governance, specs, test specs, architecture, code/tests, and validation commands; M2 must make them project-local when present and relevant. |
| `workflow` | touch in M1 | Owns creating or refreshing local `docs/workflows.md`; M1 adds a short customer-project guide caveat. |
| `verify` | touch in M2 | Lists governance and lifecycle artifacts as verification inputs; M2 must make those optional project-local evidence and preserve no-false-claim boundaries. |
| `pr` | touch in M2 | Lists governance and lifecycle artifacts as PR evidence; M2 must add customer-local caveat and preserve readiness boundaries. |
| `project-map` | touch lightly in M2 | Correctly maps local repository artifacts, but M2 must say local governance/docs/specs are optional and absence is normal. |
| `code-review` | leave unchanged unless later audit proves risk | Current reviewed wording does not contain a concrete required RigorLoop-internal document dependency; changing it without need risks weakening safety-critical review guidance. |

The audit does not justify uniform wording edits across all public skills.

## Baseline static measurement

- Source revision: `4a2b8cdb4729f1950c162009fb502fb5eea370b1`
- Command: `python scripts/measure-skill-tokens.py`
- Date: 2026-05-18
- Measured skills root: `skills/`
- Skills measured: 23
- Total estimated tokens: 58,868
- Timing note: measured after lifecycle/test-spec/test-validator authoring but before this turn changed public skill text. No canonical `skills/` files were modified before the baseline command.

| Skill | Baseline estimated tokens |
|---|---:|
| `architecture` | 3,230 |
| `architecture-review` | 3,426 |
| `bugfix` | 941 |
| `ci` | 1,163 |
| `code-review` | 5,054 |
| `constitution` | 1,026 |
| `explain-change` | 1,765 |
| `explore` | 788 |
| `implement` | 4,268 |
| `learn` | 3,097 |
| `plan` | 3,364 |
| `plan-review` | 1,631 |
| `pr` | 2,473 |
| `project-map` | 1,027 |
| `proposal` | 3,047 |
| `proposal-review` | 3,110 |
| `research` | 885 |
| `spec` | 2,129 |
| `spec-review` | 1,992 |
| `test-spec` | 1,411 |
| `verify` | 3,783 |
| `vision` | 3,962 |
| `workflow` | 5,296 |
| Total public skills | 58,868 |

## After-change static measurement

- Source revision: working tree based on `4a2b8cdb4729f1950c162009fb502fb5eea370b1`
- Command: `python scripts/measure-skill-tokens.py`
- Date: 2026-05-18
- Measured skills root: `skills/`
- Skills measured: 23
- Total estimated tokens: 60,235
- Timing note: measured after M2 public skill wording and static validation changes.

| Skill | After estimated tokens |
|---|---:|
| `architecture` | 3,230 |
| `architecture-review` | 3,426 |
| `bugfix` | 941 |
| `ci` | 1,163 |
| `code-review` | 5,054 |
| `constitution` | 1,026 |
| `explain-change` | 1,765 |
| `explore` | 788 |
| `implement` | 4,421 |
| `learn` | 3,097 |
| `plan` | 3,518 |
| `plan-review` | 1,631 |
| `pr` | 2,665 |
| `project-map` | 1,163 |
| `proposal` | 3,189 |
| `proposal-review` | 3,255 |
| `research` | 885 |
| `spec` | 2,288 |
| `spec-review` | 1,992 |
| `test-spec` | 1,411 |
| `verify` | 3,969 |
| `vision` | 3,962 |
| `workflow` | 5,396 |
| Total public skills | 60,235 |

## Static comparison

Total public skill delta: +1,367 estimated tokens.

| Skill | Baseline estimated tokens | After estimated tokens | Delta | Notes |
|---|---:|---:|---:|---|
| `workflow` | 5,296 | 5,396 | +100 | M1 local workflow-guide ownership caveat. |
| `proposal` | 3,047 | 3,189 | +142 | M2 project-local evidence contract. |
| `proposal-review` | 3,110 | 3,255 | +145 | M2 project-local evidence contract. |
| `spec` | 2,129 | 2,288 | +159 | M2 project-local evidence contract. |
| `plan` | 3,364 | 3,518 | +154 | M2 project-local evidence contract. |
| `implement` | 4,268 | 4,421 | +153 | M2 project-local evidence contract. |
| `verify` | 3,783 | 3,969 | +186 | M2 project-local evidence plus no-false-validation claim boundary. |
| `pr` | 2,473 | 2,665 | +192 | M2 project-local evidence plus PR readiness claim boundary. |
| `project-map` | 1,027 | 1,163 | +136 | M2 optional project-local orientation caveat. |
| Untouched public skills | 28,371 | 28,371 | 0 | No first-slice wording changes. |
| Total public skills | 58,868 | 60,235 | +1,367 | Increase is accepted for customer-portability contract clarity. |

## Dynamic benchmark summary

Targeted live customer-fixture benchmark evidence is recorded in [2026-05-18-customer-portable-public-skills-dynamic-benchmark.md](2026-05-18-customer-portable-public-skills-dynamic-benchmark.md).

Tracked fixture path:

```text
docs/reports/token-cost/skills/fixtures/customer-portable-public-skills/
```

Live fixture path:

```text
/tmp/rigorloop-customer-portable-live-fixture
```

Fixture exclusion check:

```bash
test ! -e /tmp/rigorloop-customer-portable-live-fixture/AGENTS.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/CONSTITUTION.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/docs/follow-ups.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/docs/project-map.md
```

Result: passed.

The targeted live scenarios cover `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `project-map`, `verify`, and `pr`. `code-review` was not included because `skills/code-review/SKILL.md` did not change.

Summary:

| Scenario | Input tokens | Largest command output tokens | Full-file reads | Broad searches | Runtime result |
|---|---:|---:|---:|---:|---|
| `proposal-customer-no-internal-docs` | 52,705 | 146 | 0 | 0 | pass |
| `proposal-review-customer-local-artifacts` | 52,535 | 146 | 0 | 0 | pass |
| `spec-customer-local-workflow-guide` | 32,881 | 146 | 0 | 0 | pass |
| `plan-customer-local-spec-and-code` | 53,651 | 179 | 0 | 0 | pass |
| `implement-customer-plan-handoff` | 95,034 | 146 | 0 | 0 | pass |
| `workflow-customer-route-no-internal-docs` | 61,141 | 146 | 0 | 0 | pass |
| `project-map-customer-repo-orientation` | 69,708 | 146 | 0 | 3 | pass-with-warning |
| `verify-customer-final-pack` | 73,941 | 146 | 0 | 1 | pass-with-warning |
| `pr-customer-ready-handoff` | 79,827 | 1,840 | 0 | 0 | pass |

## Safety-preservation notes

M1 only added local workflow-guide portability wording and the short `workflow` caveat.

M2 added concise customer-project mode and project-local evidence wording to audited risky skills. The edits do not remove existing claim boundaries, stop conditions, output sections, review-recording obligations, validation rules, or readiness boundaries.

| Skill | Removed or rewritten wording | Why safe | Essential rule preserved where |
|---|---|---|---|
| `proposal` | Added a `Project-local evidence` contract around existing references to standing instructions, `VISION.md`, `CONSTITUTION.md`, `docs/project-map.md`, local specs/ADRs, and `docs/workflows.md`. | Existing proposal gates and output shape remain; the new wording clarifies these are project-local or otherwise bounded sources in customer-project mode. | `Inputs to read`, `Evidence access`, `Artifact placement`, `Required sections`, `Vision fit`, and `Standing artifact gates`. |
| `proposal-review` | Added a `Project-local evidence` contract around proposal-review evidence references. | Review dimensions, vision-fit review, standing artifact gate review, formal recording, and material finding behavior are unchanged. | `Evidence access`, `Review dimensions`, `Vision fit review`, `Standing artifact gate review`, `Recording status`, and material finding sections. |
| `spec` | Added a `Project-local evidence` contract around governance, project map, related specs, architecture records, and interface/data-contract inputs. | Spec output path, required sections, upstream settlement, and requirement format are unchanged; local docs are still usable when present. | `Inputs to read`, `Upstream status settlement`, `Output path`, `Artifact placement`, `Required sections`, and `Requirement format`. |
| `plan` | Added a `Project-local evidence` contract around governance, plan index, proposal/spec/architecture/test/code/CI inputs. | Plan readiness and downstream-gate boundaries remain unchanged; local `docs/workflows.md` is still used only when placement matters. | `Inputs to read`, `Upstream status settlement`, `Output paths`, `Artifact placement`, `Outputs`, `Handoff`, and readiness sections. |
| `implement` | Added a `Project-local evidence` contract around plan/spec/test/architecture/code/validation inputs. | TDD, first-pass completeness, milestone-aware handoff, no-false-claim, and validation layering rules are unchanged. | `Quick operating guide`, `Inputs to read`, `Evidence access`, `Claims this skill must not make`, `First-pass completeness`, and `Milestone-aware handoff`. |
| `verify` | Added a `Project-local evidence` contract and explicit no-passed-validation claim boundary for missing validation evidence. | Branch-ready ownership, PR-ready prohibition, direct verify isolation, and validation dimensions remain unchanged. | `Purpose`, `Inputs to read`, `Claims this skill must not make`, `Direct verify`, `Workflow-managed final verify`, and `Verification dimensions`. |
| `pr` | Added a `Project-local evidence` contract and explicit readiness/no-false-claim boundary. | PR readiness checks, branch-ready dependency on `verify`, material finding closeout checks, and evidence-owned claims remain unchanged. | `When not to use`, `Readiness checks`, `Claims this skill must not make`, `Artifact placement`, and `Handoff`. |
| `project-map` | Added a `Customer-project orientation` caveat for local `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` as optional local inputs. | Mapping remains allowed to inspect real local repository artifacts; absence of governance/docs/specs is now normal rather than blocking. | `Inputs to read`, `Rules`, `Evidence collection efficiency`, `When full-file read is required`, and `Expected output`. |
| `code-review` | No wording change. | Audit found no direct required RigorLoop-internal document dependency; avoiding unnecessary edits preserves safety-critical independent-review wording. | Existing `code-review` skill. |

## Generated adapter validation

Canonical public skills changed, so generated public adapter output was validated from canonical `skills/`.

Commands:

```bash
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-BxELAV
python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m3-BxELAV --version v0.1.5
```

Result: passed. Generated adapter skill bodies were not hand-edited.
