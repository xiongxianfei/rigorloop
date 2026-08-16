# Proposal Review: PR Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-16-pr-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-16-pr-skill-simplification.md` at commit `06662261`
Review date: 2026-08-16
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PRSIM-PR1, PRSIM-PR2, PRSIM-PR3
- Open blockers: verification-tail binding, existing-PR content authority, and remote concurrency behavior require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision
- Automatic downstream handoff: none
- Claim limitations: this review does not approve the proposal, authorize specification, open or update a pull request, or continue the workflow

## Overall assessment

The proposal selects the right package direction: a compact universal submission contract, one conditional governed-readiness reference, and one structural PR-body asset. The conditional reference follows a real lifecycle-evidence boundary, while target identity, remote safety, hosted-CI truthfulness, operation selection, external-action authority, and claims remain universal.

The proposal also improves several underspecified behaviors in the current skill. It gives remote PR states and hosted CI closed vocabularies, separates portable and governed assemblies, makes the body structure reusable without moving policy into the asset, and rejects a provider engine, target-agent execution, and live acceptance PR creation.

Three execution contracts remain incomplete. Exact equality between the verified commit and final PR head conflicts with the repository's durable final-verification recording flow. Refreshing an existing PR does not have a closed authority and content-ownership rule. Finally, remote branch divergence and a PR created concurrently between preflight and mutation do not have deterministic reconciliation behavior.

## What is strong

### Progressive disclosure follows a real governed boundary

Portable PR preparation does not need change-pack aggregation, lifecycle coherence checks, or governed traceability fields. Loading the governed reference from fail-closed signals while retaining submission safety inline is proportionate.

### External-action safety remains universal

Exact repository, remote, head, base, verification, CI, push, read-back, stop, and claim behavior remains available before an optional resource loads.

### Output ownership is appropriately structural

The proposed asset owns headings, ordering, labels, and placeholders. Applicability, readiness, CI meaning, refresh authority, and handoff remain procedural policy.

### Acceptance avoids unrelated runtime machinery

Deterministic scenarios, package parity, repository validators, and ordinary PR review are sufficient for this content refactor. A target-agent runtime or sacrificial live PR would add nondeterministic external state without proving the package contract better.

## Material findings

### PRSIM-PR1 — Major: exact verified-head equality conflicts with durable final-verification recording

Finding ID: PRSIM-PR1
Severity: major
Location: `Recommended Direction` sections `Exact verified-revision sequence` and `Readiness and result model`
Evidence: The proposal requires the verify report's exact head, the local head, the pushed remote head, and the PR head to be identical. Under the repository workflow, final `verify` durably records `verify-report.md` and synchronizes matching change-local lifecycle evidence after validating the decision-bearing branch revision. That required evidence-only commit becomes the PR handoff revision even though it does not change implementation, contracts, or generated output. Requiring literal equality would make a correctly recorded governed verify result stale as soon as its own evidence is committed.
Required outcome: Distinguish the verified subject revision from the final handoff revision and define one closed, verifiable evidence-only tail that may follow the verified subject without invalidating it.
Safe resolution path: Bind `verified_subject_revision` to the exact revision covered by final validation and bind `handoff_revision` to the pushed and PR head. Permit only a contiguous verify-owned tail containing the final verify report and matching change-local state or routing synchronization, with exact allowed paths and identities. Require a fresh verify for any product, test, contract, generated, dependency, configuration, or unrelated documentation change after the verified subject. Validate the tail independently before opening or refreshing the PR.
needs-decision rationale: none; this preserves exact evidence binding while accommodating the repository's existing durable verification contract.

### PRSIM-PR2 — Major: existing-PR refresh authority and content ownership are not closed

Finding ID: PRSIM-PR2
Severity: major
Location: `Recommended Direction` sections `Invocation and operation model`, `Remote-state operation matrix`, and `Risks and Mitigations`
Evidence: An open or draft matching PR selects `refresh-primary-pr`, which may update a stale title or body. The proposal says to preserve unrelated content ownership but does not define how ownership is recognized, whether an ordinary direct `$pr` invocation authorizes replacement of text edited by a person, or what happens when generated and user-authored content are mixed. Two conforming implementations could either overwrite reviewer context or refuse every useful refresh.
Required outcome: Separate reuse from mutation and define explicit refresh authority plus fail-closed handling for unknown or mixed PR-body ownership.
Safe resolution path: Let ordinary invocation reuse an already adequate matching PR without mutation. Require an explicit user request or current same-change workflow authority naming refresh before title or body replacement. Read the current title, body, and draft state before mutation; preserve draft status unless separately authorized to publish. When ownership is unknown or content mixes generated and user-authored sections, stop unless explicit replacement authority identifies the allowed fields or sections. Do not add hidden managed markers in this first simplification unless separately specified and reviewed.
needs-decision rationale: none; reuse remains idempotent and refresh gains a deterministic authority boundary.

### PRSIM-PR3 — Major: remote branch divergence and concurrent PR creation lack deterministic reconciliation

Finding ID: PRSIM-PR3
Severity: major
Location: `Recommended Direction` sections `Invocation and operation model` and `Exact verified-revision sequence`
Evidence: The proposal resolves matching PR state before push, pushes the branch, rereads only the remote head, and then performs create, refresh, or reuse using the earlier PR classification. Another actor may create or change the matching PR between preflight and mutation. The proposal also does not classify whether the remote branch is absent, equal, ahead, safely fast-forwardable, or diverged, and it does not explicitly prohibit force-push or remote overwrite as a recovery tactic.
Required outcome: Add a closed remote-branch state model and require a fresh matching-PR classification immediately before the external PR mutation.
Safe resolution path: Classify the remote branch as `absent`, `same`, `fast-forwardable`, `ahead`, `diverged`, or `ambiguous`. Permit only creation of an absent branch or a verified non-force fast-forward update; never force-push, delete, or overwrite a remote branch. After push and remote-head confirmation, reread the exact repository/head/base PR state. If a matching PR appeared concurrently, reconcile and reuse it rather than creating a duplicate. Changed base, head, identity, or ambiguous host evidence stops or restarts resolution before mutation.
needs-decision rationale: none; the selected universal remote-safety boundary remains valid after adding these states.

## Architecture assessment

The expected bounded result remains `architecture-not-required`. The revisions can reuse current verification evidence, Git remote and PR state, explicit user or workflow authority, and the existing packaged-skill model.

Architecture becomes required only if resolution introduces a new durable PR transaction record, managed-body ownership schema, provider-neutral execution layer, cross-process lock, lifecycle state, or write owner.

## Acceptance criteria to add

| ID | Criterion |
| --- | --- |
| `AC-PRSIM-001` | Verification records an exact verified subject revision separately from the final handoff revision. |
| `AC-PRSIM-002` | Only one closed verify-owned evidence tail may follow the verified subject without fresh final verification. |
| `AC-PRSIM-003` | Any decision-bearing or unrelated post-verify change invalidates PR readiness. |
| `AC-PRSIM-004` | The pushed remote head and PR head equal the validated handoff revision. |
| `AC-PRSIM-005` | Reusing an adequate matching PR requires no body mutation. |
| `AC-PRSIM-006` | Refreshing title or body requires explicit current refresh authority. |
| `AC-PRSIM-007` | Unknown or mixed existing content ownership blocks replacement unless exact replacement authority is present. |
| `AC-PRSIM-008` | Draft publication requires separate explicit authority. |
| `AC-PRSIM-009` | Remote branch state uses one closed vocabulary with deterministic push behavior. |
| `AC-PRSIM-010` | The skill never force-pushes, deletes, or implicitly overwrites a remote branch. |
| `AC-PRSIM-011` | Matching PR state is reread after push and immediately before PR mutation. |
| `AC-PRSIM-012` | A concurrently created matching PR is reconciled and reused rather than duplicated. |
| `AC-PRSIM-013` | Portable and governed procedural profiles both decrease from baseline. |
| `AC-PRSIM-014` | Canonical, generated, archived, release-candidate, and installed resources retain required parity. |
| `AC-PRSIM-015` | No target-agent runtime or live acceptance PR is used for acceptance. |

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Flat lifecycle, submission, CI, and body concerns are concrete and measured. |
| User value | pass | Portable PR preparation and governed submission should both become easier to scan. |
| Option diversity | pass | Flat, editorial, asset-only, one-reference, fragmented, and executable alternatives are materially distinct. |
| Decision rationale | pass | One governed reference and one structural asset follow genuine activation boundaries. |
| Vision fit | pass | The change improves inspectability and portability without weakening evidence truthfulness. |
| Scope control | pass | Provider engines, new lifecycle state, live acceptance PRs, release behavior, and workflow mutation remain excluded. |
| Universal submission safety | pass | Target, remote, verification, CI, operation, push, read-back, stops, and claims remain inline. |
| Verification binding | block | Literal head equality conflicts with the required verify-owned recording tail. |
| Existing-PR authority | block | Refresh may replace externally edited content without a closed ownership or authorization rule. |
| Remote concurrency | block | Branch divergence and a PR created after preflight are not deterministically handled. |
| Resource failure | pass | Missing governed procedure blocks governed readiness but does not weaken portable safety. |
| Output ownership | pass | The asset remains structural and conditional groups are procedure-selected. |
| Testing boundary | pass | Static proof, package parity, and ordinary review are proportionate; runtime and live PR acceptance are excluded. |
| Measurement | pass | Real portable and governed loaded profiles must both decrease, with package totals reported separately. |
| Architecture awareness | pass with revisions | No architecture work is plausible if the findings reuse existing evidence and authority models. |
| Readiness for spec | changes-requested | PRSIM-PR1 through PRSIM-PR3 require proposal revision. |

## Scope Preservation Review

- Scope-preservation result: pass; simplification, progressive disclosure, external-action safety, lifecycle read-only behavior, branch creation, governed proposal authoring, and formal review are visible and classified.

## Recommended Proposal Edits

- Recommended edits: add verified-subject and handoff-revision semantics with a closed verify-owned evidence tail; separate reuse from explicitly authorized refresh; add remote-branch states and post-push PR reconciliation; then update scenarios, risks, measurements, and acceptance criteria before rereview.

## Recommendation

- Recommendation: revise the proposal to resolve PRSIM-PR1 through PRSIM-PR3, then run a new independent proposal review against the committed revision. No automatic downstream handoff follows this review.

## Specialized-gate group

- Active gate predicates: `initial_intent_table_context`, `scope_budget_context`
- Gate outcomes: pass; every initial objective and public-skill work item has a visible treatment and bounded destination
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record

## Formal-settlement group

- Review ID: proposal-review-r1
- Review record: `docs/changes/2026-08-16-pr-skill-simplification/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-16-pr-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-pr-skill-simplification/review-resolution.md`
- Proposal settlement: revision-required
- Governed change identity: `2026-08-16-pr-skill-simplification`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
