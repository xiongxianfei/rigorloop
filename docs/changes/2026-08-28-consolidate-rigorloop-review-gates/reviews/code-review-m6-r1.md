# Code Review M6 R1: Atomic Cutover

Review ID: code-review-m6-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review with fresh-assumption reset
Review date: 2026-08-30
Target: M6 implementation in commit `d48995e5`
Reviewed artifact: M6 implementation in commit `d48995e5`
Reviewed milestone: M6
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: CRG-M6-CR1, CRG-M6-CR2, CRG-M6-CR3

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m6-r1.md`; `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Open blockers: CRG-M6-CR1, CRG-M6-CR2, CRG-M6-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CRG-M6-CR1, CRG-M6-CR2, CRG-M6-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/code-review-m6-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: required
- Reviewed milestone: M6
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M6
- Required review-resolution: yes
- Finding IDs: CRG-M6-CR1, CRG-M6-CR2, CRG-M6-CR3
- Verify readiness: not-claimed

## Review inputs

- Actual diff: commit `d48995e5` against its first parent.
- Governing authority: CRG-R1 through CRG-R45, CRG-T01 through CRG-T17, the approved package-topology ADR, and M6 of the approved plan.
- Direct inspection: lifecycle request vocabulary, operation evaluation, stage routing, public context behavior, canonical workflow guidance, retired skill removal, adapter inventory, cutover validator, tests, and implementation evidence.
- Validation challenge: the recorded focused suites, generated archives, and 11-check broad smoke pass, but passing selection does not cover the three missing or contradictory behaviors below.

## Findings

### Finding CRG-M6-CR1

Finding ID: CRG-M6-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/lifecycle-contract.js:96-110`, `packages/rigorloop/dist/lib/lifecycle-operations.js:382-454`, and `packages/rigorloop/dist/lib/lifecycle-read.js:146-245`
Evidence: The cutover deletes the four skill entrypoints and replaces the forward stage graph, but the public lifecycle request validator still accepts `spec-review`, `architecture-review`, `plan-review`, and `test-spec-review` authorities. A direct `validateLifecycleRequest` reproduction accepts a `record-review` request with `stage_authority: spec-review`. Runtime code still derives those artifact-review authorities and retains a complete historical `plan-review` initialization branch. Existing tests continue to exercise those mutation paths. This keeps the retired mechanism executable instead of merely keeping its records readable.
Required outcome: Retired artifact-review stages must be rejected by current mutation and progression entrypoints while historical records remain readable evidence. Current Proposal Review, Design Review, Delivery Review, and Code Review behavior must retain direct regression coverage.
Safe resolution path: Remove the four retired names from mutation authority vocabularies and delete legacy artifact-review/plan-initialization branches that no current operation needs; keep parsing and read-only display of historical record text. Replace legacy mutation tests with explicit rejection tests and current package-review tests.
needs-decision rationale: none

### Finding CRG-M6-CR2

Finding ID: CRG-M6-CR2
Severity: major
Location: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/evidence/m6-atomic-cutover-implementation.md:21-26` and repository test inventory
Evidence: M6 evidence describes why a normal pre-adoption code revert should be safe, but no executable pre-adoption revert fixture exists. Repository search finds the required rollback scenario only in the approved spec, test spec, plan, and prose evidence; it does not find a cutover test that reverts the candidate surface and proves historical records are unchanged. CRG-T10 and CRG-T16, M6 completion criteria, and required M6 evidence explicitly require that proof.
Required outcome: The M6 evidence must be backed by a deterministic executable fixture proving that a pre-adoption code revert restores the prior public progression surface without rewriting existing historical records.
Safe resolution path: Add one focused filesystem-level cutover/revert fixture using tracked pre-cutover and candidate inventories, compare historical record bytes before and after, include it in the existing governed cutover or broad-smoke selection, and update M6 evidence with the exact command result. Do not add runtime topology metadata or migration logic.
needs-decision rationale: none

### Finding CRG-M6-CR3

Finding ID: CRG-M6-CR3
Severity: major
Location: `skills/workflow/references/governed-lifecycle-routing.md:24-31`
Evidence: The canonical procedure first says architecture and specification are mandatory Design Review members, then immediately preserves `architecture-not-required` routing that skips architecture and `architecture-ambiguous` routing. This contradicts CRG-R12 and the shipped consolidated graph, and can instruct workflow to produce a package the lifecycle engine rejects as incomplete.
Required outcome: Canonical workflow routing must state one unambiguous mandatory architecture/specification path and remove obsolete architecture-assessment skip outcomes.
Safe resolution path: Delete the three retired architecture-assessment bullets and retain only the current mandatory authoring, reconciliation, and `design-review` route plus the generic target-not-applicable rule where it still applies.
needs-decision rationale: none

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CRG-M6-CR1 retains executable legacy review mutation; CRG-M6-CR2 lacks required rollback proof; CRG-M6-CR3 contradicts mandatory package membership. |
| Test coverage | block | Passing suites do not reject all retired authorities or execute the required pre-adoption revert. |
| Edge and failure paths | block | The retired mutation path remains admitted and rollback is prose-only. |
| Architecture boundaries | block | Canonical routing permits an architecture skip that package composition rejects. |
| Compatibility | block | Historical readability is correctly preserved, but it is coupled to executable compatibility paths rather than read-only evidence. |
| Generated parity | pass | Temporary archives validate with 22 skills and no retired skill entrypoints. |
| Unrelated changes | pass | The implementation diff is bounded to M6 cutover surfaces and evidence. |
| Validation evidence | concern | All named commands pass, but their selection permits these gaps. |

## Handoff

M6 remains review-requested. Record dispositions, return the three corrections to the implementation owner, run focused retired-authority, rollback, and canonical-routing regressions, rerun the named M6 validation set, and submit the corrected immutable commit for fresh M6 Code Review.
