# Proposal Review: Local CLI Observability and Token-Efficient Results

Review ID: proposal-review-r1
Stage: proposal-review
Round: r1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md`

Reviewed artifact: `docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md` at `sha256:c33ad29a273199cf5a5d8065f3415e71dfbe449764f7535fea91806beecc61ea`
Reviewed artifact path: docs/proposals/2026-08-25-cli-observability-and-token-efficient-results.md
Reviewed artifact identity: sha256:c33ad29a273199cf5a5d8065f3415e71dfbe449764f7535fea91806beecc61ea
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested
Material findings: CLIOBS-PR6, CLIOBS-PR7, CLIOBS-PR8

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CLIOBS-PR6, CLIOBS-PR7, CLIOBS-PR8
- Open blockers: request-fingerprint privacy, invalid-invocation applicability, and deferred CI ownership require proposal revision
- Proposal readiness: not ready for specification
- Immediate next stage: isolated stop; proposal revision followed by same-stage governed rereview
- Automatic downstream handoff: none
- Claim limitations: this formal review records judgment and may settle only the matching proposal entry; it does not authorize specification, workflow continuation, implementation, verification, or PR work

## Overall assessment

The revision resolves the five recording-only findings. It assigns every supported public command to a minimal logging family, selects an explicit v0.4.x-to-v0.5.0 compatibility path, makes log discovery and exact invocation lookup dependencies of concise-default adoption, establishes a falsifiable 30% median byte objective with a per-profile regression limit, and places lifecycle state solely in the owning governed change. The local rotating-log direction remains aligned with RigorLoop's Git-first vision because logs diagnose execution without becoming lifecycle evidence.

The proposal is also substantially more testable. Default changes are gated, lookup costs count toward token value, the current detailed JSON contract has a transition window, and logging failure cannot alter semantic operations. Three boundaries remain materially ambiguous. A digest derived from an unspecified request can persist information that the privacy contract otherwise prohibits. The universal invocation goal does not classify malformed or pre-dispatch invocations. CI forwarding is deferred but still appears in current architecture scope without a durable follow-up owner.

## Prior Finding Re-evaluation

| Prior finding | Rereview result | Evidence |
| --- | --- | --- |
| CLIOBS-PR1 | addressed | The command-family table covers lifecycle, repository setup, introspection, log inspection, and future command conformance. |
| CLIOBS-PR2 | addressed | v0.4.x preserves existing output, v0.5.0 is a gated compatibility boundary, and detailed JSON remains through v0.5.x. |
| CLIOBS-PR3 | addressed | Correlation, log-path discovery, and exact single-invocation lookup are same-slice dependencies. |
| CLIOBS-PR4 | addressed | The proposal defines representative profiles, complete-interaction accounting, a 30% median reduction, a 10% profile limit, and opt-in fallback. |
| CLIOBS-PR5 | addressed through governed ownership | The proposal has one stable owning-change link and no embedded mutable status; lifecycle validation passes for the governed artifact. |

## Material Findings

## Finding CLIOBS-PR6

Finding ID: CLIOBS-PR6

Severity: major

Location: `Recommended Direction`, start-event schema; `Non-goals`; `Risks and Mitigations`

Evidence: Start events include “a request digest where a request exists,” but the digest input and construction are unspecified. A digest of the raw request can disclose equality, enable guessing of low-entropy values, and remain derived from secrets or private request fields even though raw request data is prohibited. The invocation ID and explicit allowlisted identity fields already provide correlation, so the privacy cost is not justified by a named requirement.

Required outcome: remove the raw-request fingerprint or define a canonical input containing only explicitly allowlisted non-secret semantic identity fields, including the intended value, equality leakage, and privacy tests.

Safe resolution path: omit the request digest from the first release and use the invocation ID plus command, operation, change, lifecycle revision, and allowlisted artifact identities; add a semantic fingerprint later only through a separately reviewed schema need.

needs-decision rationale: the proposal author must decide whether cross-invocation request equality has sufficient user value to justify persistent fingerprinting.

## Finding CLIOBS-PR7

Finding ID: CLIOBS-PR7

Severity: major

Location: `Goals`, `Recommended Direction`, command-family table, and `Expected Behavior Changes`

Evidence: The goal says every CLI invocation is logged, while the refined contract covers every “supported public command.” Malformed arguments, unknown operations, incomplete requests, and failures before command-family selection do not belong to any listed family. These are precisely the failures for which later command observability is valuable, and logging raw arguments to recover them would violate the privacy boundary.

Required outcome: define the applicability boundary for invalid and pre-dispatch invocations and distinguish guaranteed logging from best-effort startup observability.

Safe resolution path: add an `invalid-input` family using only the common envelope, normalized command token when safely recognized, stable parser error code, and no raw arguments; state that failures before minimum logger initialization are unobservable and narrow “every invocation” to every invocation reaching that boundary.

needs-decision rationale: the proposal author must choose whether the guarantee covers only successfully classified commands or also best-effort invalid-input events.

## Finding CLIOBS-PR8

Finding ID: CLIOBS-PR8

Severity: major

Location: `Scope budget`, `Architecture Impact`, `Testing and Verification Strategy`, rollout step 6, `Decision Log`, and `Next Artifacts`

Evidence: CI forwarding is classified as a `deferable follow-up` and excluded from first-release claims, but current architecture work is still asked to decide how `scripts/ci.sh` forwards events, the architecture impact includes wrapper integration, and the next ADR includes wrapper forwarding. Rollout says the work will be “separately owned” without naming a follow-up artifact or owner. Downstream work can therefore either absorb the deferred integration or ignore an architecture obligation.

Required outcome: give CI retention exactly one treatment and durable owner, then align architecture, testing, rollout, decision-log, and next-artifact language with that choice.

Safe resolution path: classify hosted CI retention as a `separate proposal`, create or name its durable follow-up entry, and limit this proposal's architecture work to keeping the local event schema forwardable; retain local Python-wrapper semantic parity only where it requires no hosted retention contract.

needs-decision rationale: the proposal author must decide whether current architecture owns CI forwarding or only a forward-compatible local schema.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | Persistent local observability and excessive default output are distinct and well framed. |
| User value | pass | The proposal supports command reconstruction while reducing routine agent context. |
| Option diversity | pass | Terminal verbosity, local logging, a repository ledger, and hosted telemetry are materially different options. |
| Decision rationale | pass | Local rotating logs best preserve the Git-first and no-hosted-runtime boundary. |
| Vision fit | pass | Diagnostic local state supports inspectability without replacing durable repository evidence. |
| Scope control | block | CI forwarding has conflicting current-versus-follow-up ownership. |
| Architecture awareness | pass with revision | Persistence, concurrency, projection, and path safety are visible; CI ownership must be aligned. |
| Privacy and trust boundary | block | The unspecified request digest bypasses the otherwise strong allowlist model. |
| Invocation applicability | block | Invalid and pre-dispatch invocations are not classified under the universal logging promise. |
| Compatibility | pass | The v0.4.x transition, gated v0.5.0 default, schema distinction, and detailed retention are explicit. |
| Testability | pass with revision | The proof strategy is strong once invalid-input and fingerprint cases have one contract. |
| Risk honesty | pass | Leakage, storage, concurrency, failure isolation, compatibility, and false audit authority are addressed. |
| Rollout realism | pass with revision | The staged adoption gates are credible after the CI follow-up has an owner. |
| Readiness for spec | changes-requested | Resolve CLIOBS-PR6 through CLIOBS-PR8 and perform governed rereview. |

## Scope Preservation Review

- Scope-preservation result: changes-requested. The initial logging, rotation, severity, quiet-console, and token-efficiency goals remain visible, but the deferred CI work lacks a durable route and still overlaps current architecture scope.

## Recommended Proposal Edits

- Remove the unspecified request digest or restrict it to a documented canonical allowlist with an explicit value argument and privacy proof.
- Add invalid-input and pre-dispatch applicability rules, including the earliest guaranteed logging boundary and prohibited argument capture.
- Route hosted CI retention to one named separate proposal or follow-up and remove current architecture obligations that would silently reintroduce it.
- Preserve the current compatibility, lookup, measurement, lifecycle-pointer, and failure-isolation decisions.

## Recommendation

- Recommendation: changes-requested. Retain the selected local logging and concise-result direction, revise the three remaining boundaries, and perform another independent governed proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: initial intent is preserved, but the CI forwarding row lacks a durable follow-up owner and conflicts with current architecture scope
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r1`

## Formal-settlement group

- Review ID: `proposal-review-r1`
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md#proposal-review-r1`
- Proposal settlement: pending CLI registration and settlement attempt
- Governed change identity: `2026-08-25-cli-observability-token-efficient-results`
- Formal next-stage eligibility: blocked pending proposal revision, finding resolution, and approving rereview
