# Customer-Portable Public Skill Evidence Test Spec

## Status

active

## Approval

Maintainer-approved on 2026-05-18 by direct user request. Status remains `active` because this test spec is the relied-on proof-planning surface for M1 implementation and downstream milestone validation.

## Related spec and plan

- Spec: [Customer-Portable Public Skill Evidence](customer-portable-public-skill-evidence.md), approved.
- Proposal: [Customer-Portable Public Skills and Token-Friendly Local Guidance](../docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md), accepted.
- Plan: [Customer-Portable Public Skills Execution Plan](../docs/plans/2026-05-18-customer-portable-public-skills.md), approved by plan-review R2.
- Change metadata: [change.yaml](../docs/changes/2026-05-18-customer-portable-public-skills/change.yaml).
- Review records:
  - `docs/changes/2026-05-18-customer-portable-public-skills/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-18-customer-portable-public-skills/reviews/plan-review-r2.md`
- Architecture: not required. The approved spec and plan define a public skill wording, workflow guidance, validation, report, benchmark, and generated-output validation change with no runtime architecture change.

## Testing strategy

- Static/unit: use `scripts/test-skill-validator.py` for stable phrase and concept checks covering customer-project portability guidance, forbidden required RigorLoop-internal dependency wording, and allowed project-local or conditional references.
- Contract/static: use `scripts/validate-skills.py` and manual review of canonical `skills/*/SKILL.md` plus `docs/workflows.md` to prove the public skill contract, workflow-guide ownership, portable defaults, ambiguity stops, and safety-preservation notes.
- Measurement: use `scripts/measure-skill-tokens.py` before M2 public skill wording edits and again after M2, recording before/after static measurements in `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.
- Dynamic benchmark: use a targeted customer fixture and either the existing token-cost benchmark harness or a focused first-slice manual report to prove runtime behavior in customer-project mode without RigorLoop repository-internal docs.
- Adapter integration: if canonical public skills change, generate temporary public adapter output from canonical `skills/` and validate it with `scripts/build-adapters.py` and `scripts/validate-adapters.py`.
- Lifecycle: use change metadata, review artifact, artifact lifecycle, generated skill, and diff checks to keep the non-trivial change traceable.
- Manual review: required for safety-preservation migration notes and dynamic result-quality judgment where exact natural-language assertions would be brittle.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
|---|---|---|
| `R1`-`R8` | `T4`, `T9`, `T12` | Core customer-project mode, no internal-doc dependency, bounded evidence, portable defaults, and ambiguity blocking. |
| `R9`-`R10` | `T2`, `T4`, `T9` | Local `docs/workflows.md` is used when present but is not an unconditional precondition. |
| `R11`-`R16` | `T2`, `T6`, `T13` | `workflow` ownership and concise customer-project portability guidance in `docs/workflows.md`. |
| `R17`-`R20` | `T3`, `T11`, `T13` | Audit-scoped touched skills and watchlist decisions. |
| `R21`-`R24` | `T5`, `T13` | Claim boundaries, stop conditions, output shape, review recording, verify, and PR readiness preservation. |
| `R25` | `T3`, `T4`, `T9` | `project-map` treats absent local governance/docs/specs as normal. |
| `R26`-`R28` | `T6`, `T13` | Static validation catches forbidden required dependencies while allowing project-local and conditional references. |
| `R29`-`R31` | `T7`, `T8`, `T13` | Static before/after measurement and report path. |
| `R32`-`R36` | `T9`, `T12`, `T13` | Targeted customer-fixture dynamic benchmark and required metrics. |
| `R37`-`R38` | `T10`, `T13` | Generated adapter output validates from canonical source; generated bodies are not hand-edited. |
| `R39` | `T1`, `T13` | Out-of-scope guardrails for CLI features, workflow YAML, generated docs, hard token gates, full release benchmark, and broad rewrites. |

## Example coverage map

| Example | Test IDs |
|---|---|
| `E1` proposal authoring without RigorLoop internals | `T4`, `T9` |
| `E2` local workflow guide present | `T2`, `T4`, `T9` |
| `E3` no safe default | `T4`, `T9` |
| `E4` project map orientation | `T3`, `T4`, `T9` |
| `E5` workflow creates local guidance | `T2`, `T9` |
| `E6` verify without validation evidence | `T5`, `T9` |

## Edge case coverage

| Edge case | Test IDs |
|---|---|
| `EC1` customer project lacks `docs/workflows.md` | `T4`, `T9` |
| `EC2` customer project has local `CONSTITUTION.md` | `T4`, `T9` |
| `EC3` customer project has local `specs/` | `T4`, `T6`, `T9` |
| `EC4` user asks to edit RigorLoop itself | `T4`, `T6` |
| `EC5` direct file target is a RigorLoop internal path | `T4`, `T6` |
| `EC6` sparse repository project-map | `T3`, `T9` |
| `EC7` review recording root cannot be selected | `T4`, `T5`, `T9` |
| `EC8` static check sees `docs/workflows.md when present` | `T6` |
| `EC9` static check sees `must read RigorLoop CONSTITUTION.md` | `T6` |
| `EC10` code-review audit finds no direct dependency | `T11` |
| `EC11` code-review audit finds direct dependency | `T11`, `T9` |
| `EC12` adapter generation unavailable locally | `T10`, `T13` |

## Test cases

### T1. First-slice scope and non-goals remain protected

- Covers: `R39`
- Level: integration, manual
- Fixture/setup: final implementation diff, active plan, change metadata.
- Steps:
  1. Inspect changed paths and the plan milestone evidence.
  2. Confirm the implementation does not add `rigorloop status`, `rigorloop validate`, workflow YAML, generated workflow docs, hard token gates, or full release benchmark requirements.
  3. Confirm the implementation does not rewrite every skill or hand-edit generated adapter skill bodies.
- Expected result: The diff stays within workflow guidance, audited canonical skill wording, focused validators, token reports, dynamic benchmark evidence, generated-output validation evidence, and lifecycle artifacts.
- Failure proves: The implementation exceeded the approved first slice.
- Automation location: `git diff --name-only`, `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`, manual review.

### T2. Workflow guide owns concise customer-project portability guidance

- Covers: `R9`-`R16`, `E2`, `E5`
- Level: static, contract
- Fixture/setup: `docs/workflows.md`, `skills/workflow/SKILL.md`.
- Steps:
  1. Assert `docs/workflows.md` includes a concise customer-project portability section.
  2. Assert the section states public skills operate in customer-project mode by default.
  3. Assert it says project-local artifacts are used when present and relevant.
  4. Assert it says RigorLoop repository-internal specs, docs, root governance, reports, and follow-up files are not required customer-project runtime evidence.
  5. Assert it says skills use portable defaults where safe and block on ambiguity where no safe default exists.
  6. Assert `workflow` owns creating or refreshing local `docs/workflows.md` without making that file mandatory for every stage skill invocation.
- Expected result: The local workflow guide can make a customer project self-guiding without becoming a universal precondition.
- Failure proves: Customer projects still lack a clear local guidance owner or `docs/workflows.md` was made too heavy.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, manual review.

### T3. Audit record justifies touched and untouched skills

- Covers: `R17`-`R20`, `R25`, `EC6`, `EC10`, `EC11`
- Level: contract, manual
- Fixture/setup: implementation audit evidence in the plan, change-local note, or token report; final changed paths.
- Steps:
  1. Confirm the audit identifies each touched skill and why it is touched.
  2. Confirm `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `verify`, `pr`, and `project-map` are updated only where audit evidence shows required or misleading RigorLoop-internal dependency risk.
  3. Confirm `code-review` remains unchanged unless the audit identifies a direct required RigorLoop-internal document dependency.
  4. Confirm `project-map` wording treats local `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` as optional project-local orientation inputs whose absence is normal.
- Expected result: Skill changes are audit-scoped, and `code-review` is protected unless concrete risk exists.
- Failure proves: The first slice became a broad uniform rewrite or missed a required watchlist decision.
- Automation location: `git diff --name-only`, `scripts/test-skill-validator.py` if stable audit checks are added, manual review.

### T4. Public skill wording uses project-local evidence and safe fallback behavior

- Covers: `R1`-`R10`, `R21`, `R22`, `R25`, `E1`-`E4`, `EC1`-`EC7`
- Level: static, contract
- Fixture/setup: touched canonical skill files under `skills/`.
- Steps:
  1. Inspect touched skills for customer-project mode wording.
  2. Confirm they do not require RigorLoop repository-internal artifacts as customer-project evidence.
  3. Confirm RigorLoop repository-internal artifacts are allowed only for RigorLoop repository mode, explicit user work on RigorLoop itself, direct file targets, or relevant project-local files.
  4. Confirm relevant project-local artifacts are used when present.
  5. Confirm bounded evidence comes before broad searches for workflow, path, status, review, validation, or placement evidence.
  6. Confirm skills use portable defaults when safe and block on ambiguity when no safe default exists.
- Expected result: Installed public skills can operate in customer projects from the user request, project-local artifacts, and the skill's portable contract.
- Failure proves: The public skill surface still depends on absent RigorLoop repository context or lacks safe absence behavior.
- Automation location: `scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, manual review.

### T5. Safety-critical obligations are preserved in touched skills

- Covers: `R21`-`R24`, `E6`, `EC7`
- Level: manual, contract
- Fixture/setup: migration note for each touched skill; final diff.
- Steps:
  1. For every touched skill, inspect the migration note for removed or rewritten wording, why the rewrite is safe, and where the essential rule remains preserved.
  2. Confirm claim boundaries, stop conditions, and required output shape are preserved.
  3. For review skills, confirm formal review recording, material finding shape, and review-resolution boundaries are preserved.
  4. For `verify` and `pr`, confirm validation, branch-readiness, PR-readiness, and no-false-claim boundaries are preserved.
- Expected result: Portability wording does not delete rigor, review evidence, validation, or readiness boundaries.
- Failure proves: Token-friendly wording removed required behavior.
- Automation location: manual code-review checklist, `scripts/validate-skills.py`, `scripts/validate-review-artifacts.py`.

### T6. Static validator catches forbidden required dependencies without banning local docs

- Covers: `R12`-`R16`, `R26`-`R28`, `EC3`-`EC5`, `EC8`, `EC9`
- Level: unit, integration
- Fixture/setup: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, validator fixtures or inline test cases.
- Steps:
  1. Add or update static checks for obvious required RigorLoop-internal dependency wording, such as `must read RigorLoop CONSTITUTION.md` or `read the RigorLoop workflow spec before proceeding`.
  2. Add allowed examples for `if present`, `project-local`, `when operating inside the RigorLoop repository`, `when this file is the review target`, `when the user provided this path`, and `when governing project docs exist`.
  3. Run `python scripts/test-skill-validator.py`.
  4. Run `python scripts/validate-skills.py`.
- Expected result: Forbidden required internal-doc wording fails, while legitimate project-local or conditional references pass.
- Failure proves: Static validation is either too weak to prevent regression or too broad for customer projects with their own docs/specs.
- Automation location: `scripts/test-skill-validator.py`, `scripts/validate-skills.py`.

### T7. Baseline static token measurement is captured before M2 skill edits

- Covers: `R29`-`R31`
- Level: smoke, manual
- Fixture/setup: M1 before public skill wording edits; `scripts/measure-skill-tokens.py`; token report path.
- Steps:
  1. Before M2 public skill wording edits, run `python scripts/measure-skill-tokens.py`.
  2. Record the baseline command, date, source revision, measured skill paths, and summary in `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.
  3. If baseline was not captured before edits, reconstruct from a named tracked revision in a clean checkout or worktree and record the ref, command, and environment.
  4. Confirm M2 does not proceed without baseline evidence.
- Expected result: The before measurement is deterministic and reviewable before the measured skill text changes.
- Failure proves: Static before/after evidence cannot be trusted.
- Automation location: `scripts/measure-skill-tokens.py`, token report manual review, plan/code-review evidence.

### T8. After-change static measurement compares against the M1 baseline

- Covers: `R29`-`R31`
- Level: smoke, manual
- Fixture/setup: M3 after M2 skill edits; M1 baseline report.
- Steps:
  1. Run `python scripts/measure-skill-tokens.py` after M2 skill edits.
  2. Record after-change totals for touched skills and total public skill delta.
  3. Compare after-change measurements against the M1 baseline.
  4. If a YAML companion report exists, confirm it matches the Markdown summary.
- Expected result: The static report contains baseline, after-change, and delta evidence for first-slice public skill changes.
- Failure proves: The change cannot demonstrate static token-cost impact.
- Automation location: `scripts/measure-skill-tokens.py`, optional report validation if repository-owned validation exists.

### T9. Targeted customer-fixture dynamic benchmark proves runtime portability

- Covers: `R1`-`R10`, `R25`, `R32`-`R36`, `E1`-`E6`, `EC1`-`EC7`, `EC11`
- Level: e2e, manual
- Fixture/setup:
  - Customer fixture with installed public skills, `rigorloop.yaml`, `rigorloop.lock`, optional local `docs/workflows.md`, local `docs/changes/<change-id>/`, local `specs/`, source files, and tests.
  - Fixture deliberately excludes RigorLoop repository-internal root governance, internal specs, internal reports, `docs/follow-ups.md`, and `docs/project-map.md` unless the scenario is explicitly testing project-map creation or update.
- Steps:
  1. Run or manually record the targeted scenarios: `proposal-customer-no-internal-docs`, `proposal-review-customer-local-artifacts`, `spec-customer-local-workflow-guide`, `plan-customer-local-spec-and-code`, `implement-customer-plan-handoff`, `workflow-customer-route-no-internal-docs`, `project-map-customer-repo-orientation`, `verify-customer-final-pack`, and `pr-customer-ready-handoff`.
  2. Run `code-review-customer-diff-small` only if `code-review` skill wording changes.
  3. For each run, record attempted broad searches for RigorLoop-internal docs, reliance on missing RigorLoop repository specs, local `docs/workflows.md` use when present, portable-default behavior, ambiguity blocking, input tokens, largest command output, full-file reads, broad searches, and result-quality status.
  4. Fail or block readiness if a required scenario depends on absent RigorLoop repository internals or has failed result quality.
- Expected result: Runtime behavior in a customer fixture follows local evidence, portable defaults, and ambiguity stops without searching for unavailable RigorLoop internals.
- Failure proves: Static wording changed but runtime behavior remains brittle or token-wasteful.
- Automation location: `scripts/run-token-cost-benchmarks.py` if adapted for the first-slice fixture, otherwise structured manual benchmark report under `docs/reports/token-cost/skills/`.

### T10. Generated public adapter output validates from canonical skills

- Covers: `R37`, `R38`, `EC12`
- Level: integration
- Fixture/setup: canonical public skill changes, temporary adapter output directory.
- Steps:
  1. If canonical public skills changed, run `python scripts/build-adapters.py --version <current-or-next-version> --output-dir <tmp-output>`.
  2. Run `python scripts/validate-adapters.py --root <tmp-output> --version <current-or-next-version>`.
  3. Confirm generated adapter skill bodies are not hand-edited to satisfy this spec.
  4. If local adapter generation is unavailable, record the command, failure, blocker, and smallest next action without editing generated bodies.
- Expected result: Public adapter output is generated from canonical `skills/` and validates from temporary or release output.
- Failure proves: Public installed skills may drift from canonical source or generated output was treated as authored source.
- Automation location: `scripts/build-adapters.py`, `scripts/validate-adapters.py`, `git diff --name-only`.

### T11. Code-review contingency remains explicit

- Covers: `R18`, `R35`, `EC10`, `EC11`
- Level: contract, manual
- Fixture/setup: audit evidence and final diff.
- Steps:
  1. If the audit finds no direct required RigorLoop-internal dependency in `code-review`, confirm `skills/code-review/SKILL.md` is unchanged.
  2. If the audit finds a direct dependency, confirm the rewrite is minimal and preserves safety-critical independent-review behavior.
  3. If `code-review` changes, confirm the dynamic benchmark includes `code-review-customer-diff-small`.
- Expected result: `code-review` is not edited without evidence, and any required edit carries matching dynamic proof.
- Failure proves: A safety-critical skill was changed unnecessarily or without runtime evidence.
- Automation location: `git diff -- skills/code-review/SKILL.md`, manual review, dynamic benchmark report.

### T12. Security, privacy, and performance boundaries hold

- Covers: `R1`-`R8`, `R32`-`R36`
- Level: manual, contract
- Fixture/setup: dynamic benchmark fixture, public skill text, benchmark reports.
- Steps:
  1. Confirm skills do not ask customer projects to expose secrets, private keys, tokens, private repository metadata, or unrelated machine-local paths to satisfy portability.
  2. Confirm dynamic benchmark fixtures use synthetic data and no real customer secrets.
  3. Confirm static validation remains phrase/path based rather than broad semantic scoring.
  4. Confirm dynamic benchmarks are targeted to first-slice scenarios and do not require the full release benchmark suite.
  5. Confirm benchmark evidence separates static size, input tokens, largest command output, full-file reads, broad searches, and result quality.
- Expected result: Portability proof is useful without adding privacy risk, hard token gates, or broad benchmark cost.
- Failure proves: The implementation made customer projects expose unsafe data or expanded validation cost beyond the approved slice.
- Automation location: manual review, token report, dynamic benchmark report.

### T13. Lifecycle, generated skill, and change-local validation remain coherent

- Covers: `R12`-`R39`
- Level: integration
- Fixture/setup: final changed artifacts.
- Steps:
  1. Run `python scripts/test-skill-validator.py`.
  2. Run `python scripts/validate-skills.py`.
  3. Run `python scripts/build-skills.py --check`.
  4. Run `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`.
  5. Run `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills`.
  6. Run artifact lifecycle validation over the proposal, spec, this test spec, plan, plan index, change metadata, review log, review resolution, and formal review records.
  7. Run `git diff --check --`.
- Expected result: Public skill, lifecycle, generated-skill, review, metadata, and whitespace checks pass before downstream verify and PR.
- Failure proves: The proof surface or lifecycle state is stale, inconsistent, or not reviewable.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-05-18-customer-portable-public-skills`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check --`

## Fixtures and data

- Customer dynamic benchmark fixture:

```text
customer-fixture/
  rigorloop.yaml
  rigorloop.lock
  docs/workflows.md
  docs/changes/example-change/change.yaml
  docs/changes/example-change/explain-change.md
  specs/customer-feature.md
  docs/plans/customer-plan.md
  src/
  tests/
```

- The customer fixture MUST deliberately exclude root `CONSTITUTION.md`, root `AGENTS.md`, RigorLoop internal `specs/`, RigorLoop internal `docs/reports/`, `docs/follow-ups.md`, and `docs/project-map.md` unless a scenario explicitly tests local project-map creation or update behavior.
- Static token report path: `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.
- Optional machine-readable report path: `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.yaml`.
- Temporary adapter output path: implementation-chosen temporary directory outside tracked source.

## Mocking/stubbing policy

- Static validator tests should use small inline positive and negative text samples when possible.
- Dynamic benchmark fixtures may use synthetic source, tests, local specs, and local lifecycle artifacts.
- Dynamic benchmark dry-runs may prove fixture assembly and report structure, but customer-project runtime behavior requires either live run evidence or a manual result-quality record that states what was not executed.
- Do not mock generated adapter validation; use repository-owned adapter generation and validation scripts, or record the local tooling blocker.

## Migration or compatibility tests

- Existing RigorLoop repository mode remains valid: T4 allows repository-internal artifacts when operating inside the RigorLoop repository, when the user asks to work on RigorLoop itself, when the file is the direct target, or when the file is relevant and project-local.
- Existing customer projects without `docs/workflows.md` remain supported through portable defaults or ambiguity blocking: T4 and T9.
- Existing customer projects with local docs/specs/governance files remain supported as project-local evidence: T4, T6, and T9.
- Generated adapter packages remain generated from canonical skills: T10.

## Observability verification

- Static validation results must name command and result: T6 and T13.
- Static token measurement must record before/after totals for touched skills and total public skill delta: T7 and T8.
- Dynamic benchmark reports must summarize broad searches, full-file reads, largest command output, input tokens, result-quality status, and attempted dependency on absent RigorLoop internals: T9.
- Generated adapter validation evidence must name the generation output location and validation command result: T10.

## Security/privacy verification

- T12 verifies no customer secrets, private keys, tokens, private repository metadata, or unrelated machine-local paths are required.
- T9 fixtures use synthetic customer-project data.
- T4 and T12 verify public skill text does not expose repository-maintainer-only implementation details as required customer evidence.

## Performance checks

- T6 verifies static validation stays narrow and phrase/path based.
- T7 and T8 verify static token measurement remains diagnostic and recorded.
- T9 verifies runtime evidence behavior, including broad searches, full-file reads, largest command output, and input tokens.
- T12 verifies the first slice does not expand into the full release benchmark suite or hard token gates.

## Manual QA checklist

- Confirm every touched skill has a migration note preserving essential claim boundaries, stop conditions, required output shape, and safety-critical obligations.
- Confirm `docs/workflows.md` is concise and does not make itself mandatory for every task.
- Confirm `project-map` treats absent local governance/docs/specs as normal.
- Confirm `verify` and `pr` do not claim validation or readiness without evidence.
- Confirm any benchmark result-quality failure blocks readiness or has an explicit owner-approved disposition.

## What not to test

- Do not test new CLI commands such as `rigorloop status` or `rigorloop validate`; they are out of scope.
- Do not test workflow YAML or generated workflow docs; they are out of scope.
- Do not run a full release benchmark suite unless a later approved artifact broadens the scope.
- Do not test generated adapter skill bodies as authored source; validate generated output from canonical `skills/`.
- Do not use broad semantic scoring of public skill prose; use focused phrase/path checks and manual review.

## Uncovered gaps

None. Live dynamic benchmark execution may be implemented as a focused fixture/report if the existing benchmark harness cannot express all first-slice scenarios; that is a test implementation choice, not a spec gap, as long as T9 evidence fields are recorded.

## Next artifacts

- implement
- code-review for each completed implementation milestone
- explain-change
- verify
- pr

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface. Proposal, spec, and plan review are complete; ready for M1 implementation. Implementation must start by preserving or reconstructing the static token baseline before public skill wording changes.
