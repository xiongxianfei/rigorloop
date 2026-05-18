# Customer-Portable Public Skills Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the customer-portable public skills change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: plan-review-r2
Review closeout: code-review-r1
Review closeout: code-review-r2
Review closeout: code-review-r3
Review closeout: code-review-r4

## Resolution Entries

### proposal-review-r1

Review closeout: closed

#### CPS-PR1

Finding ID: CPS-PR1
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Align the proposal's `Readiness` section with the current reviewed state before downstream spec or planning relies on it.
Rationale: The proposal now includes the requested first-slice boundary, repository mode boundary, missing-guidance behavior, static-check precision, safety-preservation checklist, generated-adapter validation requirement, `project-map` caveat, and focused spec path. However, its readiness section still says "Changes requested before spec/plan," which contradicts relying on the proposal as ready for the next authoring stage.
Chosen action: Updated the proposal `Readiness` section to say it is ready for focused spec after proposal-review acceptance.
Safe resolution path: Either update `Readiness` to state readiness for focused spec after proposal acceptance, or intentionally keep it blocked and record the remaining blocker. Then rerun proposal-review.
Validation target: Revised proposal readiness section and review closeout.
Validation evidence: Proposal readiness now states "Ready for focused spec after proposal-review acceptance." Focused artifact validation passed after the proposal revision.

## Validation Evidence

- `proposal-review-r1` recorded `CPS-PR1`.
- The proposal readiness section now states readiness for focused spec after proposal-review acceptance.
- `proposal-review-r2` recorded no material findings.
- `spec-review-r1` recorded no material findings.
- `plan-review-r1` recorded `CPS-PLAN-1`.
- `plan-review-r2` recorded no material findings and closed `CPS-PLAN-1`.
- `code-review-r1` recorded no material findings for M1.
- `code-review-r2` recorded no material findings for M2.
- `code-review-r3` recorded `CPS-M3-CR1`.
- `code-review-r4` recorded no material findings and closed `CPS-M3-CR1`.
- `review-log.md` records no open findings.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

Review closeout: closed

#### CPS-PLAN-1

Finding ID: CPS-PLAN-1
Disposition: accepted
Owner: plan author
Owning stage: plan
Required outcome: The plan must capture baseline static token measurement before skill wording changes, or explicitly define a deterministic reconstruction method from a named tracked revision.
Rationale: M3 depends on completed M2 skill wording and static validation, but M3 also says to run static skill token measurement before and after the skill changes. That sequencing risks losing the true pre-change baseline required by the approved spec.
Chosen action: Moved baseline static token measurement into M1 before M2 public skill wording changes. M2 now depends on recorded M1 baseline evidence and stops if the baseline is missing. M3 now runs after-change static measurement, compares against the M1 baseline, runs the targeted dynamic benchmark, validates generated adapter output, and records comparison evidence.
Stop state: Do not proceed to test-spec or implementation until the plan records a deterministic baseline measurement path and plan-review is rerun.
Safe resolution path: Move the baseline static token measurement into M1 or a pre-M2 dependency, then keep M3 for after-change measurement and comparison report. Alternatively, state the exact tracked ref and command used to reconstruct the baseline before M2 changes begin.
Validation target: Revised plan and plan-review rerun.
Validation evidence: Plan revision recorded. `plan-review-r2` approved the revised sequencing with no material findings.

### plan-review-r2

No material findings.

### code-review-r1

No material findings.

### code-review-r2

No material findings.

### code-review-r3

Review closeout: closed

#### CPS-M3-CR1

Finding ID: CPS-M3-CR1
Disposition: accepted
Owner: implementation author
Owning stage: implement
Decision owner: maintainer
Required outcome: M3 must provide dynamic benchmark evidence that supports the approved runtime portability claim for the required customer-fixture scenarios, including R36 runtime fields, or explicitly block M3 instead of marking scenario runtime result quality as passing.
Rationale: The current benchmark report says live `codex exec` scenario execution was not run and records runtime counters as `not-measured`, but it also marks each scenario result quality as `pass` and records no broad searches or missing-internal reliance. That is insufficient independent proof of dynamic runtime behavior.
Chosen action: Ran targeted live `codex exec --json --ephemeral --skip-git-repo-check` scenarios against a temporary customer fixture with generated Codex adapter skills installed and root governance removed. Updated the dynamic benchmark report and token report with measured input tokens, largest command output, full-file reads, broad searches, local guide use, portable-default or ambiguity behavior, attempted reliance on absent RigorLoop internals, and result quality.
Stop state: Closed by `code-review-r4`. Do not claim verify, PR readiness, or Done until downstream final closeout gates complete.
Decision needed: none; maintainer accepted the finding and required live dynamic evidence.
Safe resolution path: Run a targeted benchmark or approved dry-run mechanism that produces the required fields, then update the benchmark report, token report, plan, and change metadata. If execution is impossible, mark runtime result quality as blocked or inconclusive and keep M3 from closing until the owner accepts a changed proof standard.
Validation target: Updated dynamic benchmark report and rerun code-review for M3.
Validation evidence: Live scenario JSONL and analyzer summaries recorded under `docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/`; token report and dynamic benchmark report updated. `code-review-r4` accepted the updated dynamic benchmark evidence with no material findings.

### code-review-r4

No material findings.
