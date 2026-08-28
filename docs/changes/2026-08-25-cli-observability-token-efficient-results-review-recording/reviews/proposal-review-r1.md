# Proposal Review: Local CLI Observability and Token-Efficient Results

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md`

Reviewed artifact: `docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md` at `sha256:465d713954e897dc3976b407677487571a09a3137be2d77851f132eab3b9fa6a`
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CLIOBS-PR1, CLIOBS-PR2, CLIOBS-PR3, CLIOBS-PR4, CLIOBS-PR5
- Open blockers: command-family scope, JSON compatibility, required lookup capability, token-value success criteria, and proposal lifecycle validity require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: isolated stop; proposal revision followed by same-stage proposal rereview
- Automatic downstream handoff: none
- Claim limitations: this isolated review records judgment only; it does not settle the portable proposal, activate a governed change, authorize specification, or continue workflow

## Overall assessment

The selected direction is valuable and proportionate at the product level. A rotating local diagnostic sink can preserve command observability while a concise result projection reduces routine agent context. The proposal also maintains the essential boundary that logs are diagnostic and machine-local while Git-tracked artifacts remain lifecycle truth. Its privacy exclusions, non-semantic logging-failure rule, rollout slices, and architecture triggers are strong.

Four product contracts still permit materially different specifications. “Every CLI invocation” is broader than the lifecycle-specific problem and event vocabulary, leaving non-lifecycle commands unclassified. Concise JSON is selected as the new default while the compatibility mechanism for the current approved envelope remains an open question. Invocation lookup is described as optional even though the proposed concise-result contract relies on it for safe detail retrieval. Finally, the token outcome is called “material” without a provisional threshold or release decision rule, so the main benefit cannot yet be falsified against the added persistence and rotation complexity. Separately, the proposal omits the required status section and therefore fails repository lifecycle validation.

## Material findings

### Finding CLIOBS-PR1

Finding ID: CLIOBS-PR1

Severity: major

Location: `Goals`, `Initial intent preservation`, `Scope budget`, `Recommended Direction`, and `Expected Behavior Changes`

Evidence: The proposal requires a structured log for “every CLI invocation,” while the problem, event fields, CI discussion, and user intent concern governed lifecycle commands. Existing public commands also include setup and discovery operations whose change, lifecycle revision, request digest, and blocker semantics may not apply. The scope budget does not classify those command families or say whether unknown future commands are logged.

Required outcome: define an exhaustive command-family applicability rule for default logging, concise projections, invocation references, and CI forwarding, including non-lifecycle and future commands.

Safe resolution path: scope the first release to lifecycle commands and explicitly classify setup, version, log-discovery, and future commands as included, deferred, or exempt; alternatively retain all-command logging and define the minimal event and privacy contract for each family.

needs-decision rationale: the proposal author must choose whether the product boundary is lifecycle observability or universal CLI observability before the specification can close schemas and tests.

### Finding CLIOBS-PR2

Finding ID: CLIOBS-PR2

Severity: major

Location: `Context`, `Recommended Direction`, `Expected Behavior Changes`, `Rollout and Rollback`, `Risks and Mitigations`, and open question 2

Evidence: The proposal selects compact, operation-specific JSON as the default, but the approved governed lifecycle CLI contract requires a broad stable JSON envelope and equivalent human facts. The proposal leaves `--detail`, a format version, and a transition alias as alternatives. Those choices expose different compatibility, migration, adapter, and deprecation behavior, and human stderr ownership is similarly not stated for the transition.

Required outcome: choose a compatibility direction that identifies the default and detailed machine contracts, schema-version behavior, transition period, adapter expectations, and the matching human stdout/stderr ownership.

Safe resolution path: preserve the current `--format json` contract during an explicit compatibility window, introduce a separately named concise projection, retain a detailed alias, and make any default change only at a declared compatibility boundary with conformance tests for both forms.

needs-decision rationale: compatibility policy is a proposal-level product choice and cannot safely be delegated to implementation.

### Finding CLIOBS-PR3

Finding ID: CLIOBS-PR3

Severity: major

Location: `Goals`, `Scope budget`, `Recommended Direction`, `Expected Behavior Changes`, rollout step 3, and open question 8

Evidence: The proposal promises complete detail without rerunning a mutation and makes an invocation reference part of every concise result. It also says a read-only surface should retrieve one invocation. However, the scope budget marks correlation and lookup only as a `first-slice candidate`, and open question 8 asks whether lookup is required. A concise default without a guaranteed retrieval path would not satisfy the stated safety and token contract.

Required outcome: classify the minimum correlation, log-directory discovery, and single-invocation retrieval capabilities as same-slice dependencies, or remove the first-release reliance on those capabilities and define another deterministic detail-recovery path.

Safe resolution path: require a short invocation ID, a read-only log-path command, and a single-invocation lookup command in the same slice that changes default output; leave search, aggregation, and tailing out of scope.

needs-decision rationale: the selected concise-result model depends on lookup availability, so optional treatment leaves the proposal internally inconsistent.

### Finding CLIOBS-PR4

Finding ID: CLIOBS-PR4

Severity: major

Location: `Goals`, `Scope budget`, `Testing and Verification Strategy`, rollout step 5, open questions 3 and 10, and `Readiness`

Evidence: The proposal requires results to be “materially smaller” and makes token efficiency a primary outcome, but it supplies no provisional threshold, representative weighting, regression limit, or go/no-go rule. Measurement is a later slice even though the output projection may become default before its value is established. Counting lookup costs is required, but no criterion determines whether the persistence and rotation cost is justified.

Required outcome: define a falsifiable provisional success objective, baseline profiles, complete-interaction accounting, semantic-retention guardrails, and the release decision if the objective is not met.

Safe resolution path: baseline the current merged CLI for status, context, successful mutation, blocked mutation, and error flows; require a provisional reduction such as 30% in median default agent-facing bytes or estimated tokens while counting required lookups; prohibit loss of continuation-critical facts; and keep the concise projection opt-in if the threshold fails.

needs-decision rationale: the proposal author must select a value threshold and adoption rule before token efficiency can justify a new default.

### Finding CLIOBS-PR5

Finding ID: CLIOBS-PR5

Severity: major

Location: proposal artifact structure, between `Owning change record` and `Problem`

Evidence: The proposal has no `## Status` section. `python scripts/validate-artifact-lifecycle.py` rejects it with `missing required Status section`, so the artifact cannot pass the repository's proposal lifecycle contract or proceed as specification-ready evidence.

Required outcome: add the required stable status section without claiming settlement that the recording-only review cannot grant.

Safe resolution path: add `## Status` with an explicit draft or changes-requested statement, preserve the portable/no-governed-change ownership declaration, and update status only through an authorized later lifecycle action.

needs-decision rationale: none; the authoring stage can correct the required proposal structure without changing the selected direction.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass with revision | The observability and token problems are clear, but the affected command families are not. |
| User value | pass with revision | Local history and concise results are useful; the token value needs a measurable adoption rule. |
| Option diversity | pass | Terminal detail, local logs, repository ledger, and hosted telemetry are materially different choices. |
| Decision rationale | pass | The local rotating sink best preserves the Git-first boundary without increasing routine output. |
| Vision fit | pass | The direction improves inspectability and agent ergonomics without replacing durable repository evidence. |
| Scope control | block | Universal versus lifecycle-only coverage and required lookup are not closed. |
| Architecture awareness | pass | Persistence, concurrency, path safety, projection boundaries, and wrapper integration are correctly flagged. |
| Privacy and trust boundary | pass with revision | The allowlist and prohibited-data rules are strong once command-family applicability is exhaustive. |
| Compatibility | block | The default JSON migration and human channel contract remain undecided. |
| Testability | block | Token value lacks a threshold and lookup is not yet a required dependency. |
| Artifact lifecycle validity | block | The required proposal status section is absent. |
| Risk honesty | pass | The proposal directly addresses leakage, disk bounds, concurrency, log failure, repetition, compatibility, and false audit authority. |
| Rollout realism | pass with revision | The staged rollout is sound once compatibility and measurement become adoption gates. |
| Readiness for spec | changes-requested | Resolve CLIOBS-PR1 through CLIOBS-PR5 and perform same-stage rereview. |

## Scope Preservation Review

- Scope-preservation result: changes-requested. The proposal preserves the requested logging, severity, rotation, quiet console, and token-friendly output goals, but the scope budget must make invocation lookup a dependency and classify all command families before downstream work.

## Recommended Proposal Edits

- Add a command-family applicability table covering lifecycle, setup, discovery, log-inspection, and future commands.
- Replace compatibility open question 2 with a selected, versioned migration and deprecation policy for JSON and human channels.
- Change invocation correlation, log-path discovery, and single-invocation lookup from candidate treatment to same-slice dependencies for concise-default adoption.
- Add a provisional end-to-end token or byte objective, representative profiles, semantic guardrails, and an opt-in fallback if the objective fails.
- State whether CI forwarding is required for initiative completion or a later enhancement; avoid claiming hosted-runner observability before its retained output is accessible.
- Add the required proposal status section with no unsupported settlement claim.

## Recommendation

- Recommendation: changes-requested. Retain the rotating local log and concise-result direction, resolve the five findings, and perform a new isolated proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: the scope budget preserves the initial user goals but fails to make a required lookup capability mandatory and does not classify every affected command family
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-25-cli-observability-token-efficient-results-review-recording/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r1`

## Formal-settlement group

- Review ID: `proposal-review-r1`
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results-review-recording/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results-review-recording/review-resolution.md#proposal-review-r1`
- Proposal settlement: not-settled; the recording-only root has no proposal lifecycle authority
- Governed change identity: none; recording-only root `2026-08-25-cli-observability-token-efficient-results-review-recording`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
