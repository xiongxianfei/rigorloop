# Code Review R3

Review ID: code-review-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: M3. Measurement, dynamic benchmark, adapters, and lifecycle evidence
Reviewed artifact: docs/plans/2026-05-18-customer-portable-public-skills.md
Review date: 2026-05-18
Recording status: recorded
Status: changes-requested

## Review Inputs

- Diff/review surface:
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`
  - `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md`
  - `docs/reports/token-cost/skills/fixtures/customer-portable-public-skills/`
  - `docs/changes/2026-05-18-customer-portable-public-skills/change.yaml`
  - `docs/changes/2026-05-18-customer-portable-public-skills/explain-change.md`
  - `docs/plans/2026-05-18-customer-portable-public-skills.md`
- Governing spec: `specs/customer-portable-public-skill-evidence.md`
- Test spec: `specs/customer-portable-public-skill-evidence.test.md`
- Plan milestone: `docs/plans/2026-05-18-customer-portable-public-skills.md`, M3
- Validation evidence:
  - `python scripts/measure-skill-tokens.py`
  - customer fixture exclusion check
  - `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-BxELAV`
  - `python scripts/validate-adapters.py --root /tmp/rigorloop-adapters-m3-BxELAV --version v0.1.5`
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - lifecycle and diff checks recorded in the active plan

## Diff Summary

M3 records after-change static token measurement and comparison, adds a synthetic customer fixture, adds a targeted dynamic benchmark report, records generated adapter build/validation evidence from temporary output, and updates change-local/plan evidence for M3 handoff.

## Findings

### CPS-M3-CR1

Location: `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills-dynamic-benchmark.md`

Finding ID: CPS-M3-CR1
Severity: major

Evidence: The report states, "Live `codex exec` scenario execution was not run" and records runtime counters such as `Input tokens`, `Largest command output`, `Full-file reads`, and `Broad searches` as `not-measured` for every required scenario. The same table marks every scenario's `Result quality` as `pass` and records "Attempted broad search for RigorLoop internals" as `no`.

Required outcome: M3 must provide dynamic benchmark evidence that can support the approved runtime portability claim for the required customer-fixture scenarios, including the required R36 fields for input tokens, largest command output, full-file reads, broad searches, local guide use, portable-default or ambiguity behavior, and attempted reliance on absent RigorLoop internals.

Safe resolution path: Run a targeted dynamic benchmark or an approved dry-run mechanism that produces per-scenario evidence for the required fields, then update the benchmark report and token report. If live execution is impossible, revise the evidence so `Result quality` is not marked `pass` for runtime behavior and record the benchmark gap as a blocker instead of closing M3.

## Outcome

- Review status: changes-requested
- Material findings: CPS-M3-CR1
- Blocking findings: none
- Recording: detailed review record, review log, and open review-resolution entry recorded
- Immediate next repository stage: review-resolution for `CPS-M3-CR1`, then implementation fix
- Isolation: direct code-review request stops here and does not automatically continue into review-resolution or fixes

## Checklist Coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | R32 requires a targeted customer-fixture dynamic benchmark, and R36 requires runtime evidence fields. The current report records those fields as `not-measured` while marking scenario quality `pass`. |
| Test coverage | concern | Static and lifecycle validation passed, but T9 expects dynamic benchmark evidence for the required scenarios. The current report is primarily fixture/static-contract evidence. |
| Edge cases | concern | The fixture excludes the required internal docs, but no scenario run proves behavior when those files are absent. |
| Error handling | pass | The skill wording and static checks preserve portable defaults, ambiguity blocking, and no-false-claim behavior. |
| Architecture boundaries | pass | No runtime architecture, CLI, workflow YAML, generated workflow docs, hard token gates, or full release benchmark suite changes were introduced. |
| Compatibility | pass | Generated adapter output validation from canonical skills passed using temporary archives. |
| Security/privacy | pass | The synthetic fixture contains no customer secrets or private credentials. |
| Derived artifact currency | pass | `python scripts/build-skills.py --check` and temporary adapter validation passed. |
| Unrelated changes | pass | M3 changes are limited to measurement/report/fixture/adapter evidence and lifecycle updates. |
| Validation evidence | concern | Static token measurement, adapter validation, and lifecycle checks are credible; dynamic runtime evidence is insufficient. |

## No-Finding Rationale

Not applicable. One material finding requires changes before M3 can close.

## Residual Risks

- M3 remains open until dynamic benchmark evidence is fixed and code-review reruns.
- This review does not claim branch readiness, PR readiness, CI status, final verification, or successful M3 closeout.

## Recommended Next Stage

Enter review-resolution for `CPS-M3-CR1`, then return to implementation for M3 fixes and rerun `code-review`.
