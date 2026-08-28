# Code Review M1 R2: CLI Observability and Token-Efficient Results

Review ID: code-review-m1-r2
Stage: code-review
Round: r2
Reviewer: Codex direct reviewer with artifact-and-criteria context reset
Status: changes-requested
Review date: 2026-08-25
Review mode: local direct review; the user explicitly requested no subagent reviewer
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L0
Author context ID: root-code-review-m1-r1-correction
Reviewer context ID: root-code-review-m1-r2-context-reset
Context separation mechanism: artifact-and-criteria-context-reset
Author context excluded: false
Risk tier: elevated
Risk-tier triggers: privacy-bounded-local-diagnostics; lifecycle-command-integration; token-adoption-proof
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: `CONSTITUTION.md`; `specs/cli-observability-and-token-efficient-results.md`; `docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md`; `docs/plans/2026-08-25-cli-observability-token-efficient-results.md`; `specs/cli-observability-and-token-efficient-results.test.md`
Formal criteria: code-review-rereview-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: CONSTITUTION.md@working-tree#sha256:25c0479714a44aa0dd9db8ba9830ea3588140d3daeac1706f572281ae2aeb0e0; specs/cli-observability-and-token-efficient-results.md@working-tree#sha256:de9ec40c11d33b4d199e79fea74374199d94133c8eed651546ed04d664bc1029; docs/adr/ADR-20260825-local-cli-observability-and-result-projection-boundary.md@working-tree#sha256:8df259dc5e97efa06535f785c25d575c366e2864b1fd88abde96fba6075b4fd4; docs/plans/2026-08-25-cli-observability-token-efficient-results.md@working-tree#sha256:004a4aceadd1a4dcbb9ab5a4e4a1eca075cad4dd4fd84617d1972d476cb403a2; specs/cli-observability-and-token-efficient-results.test.md@working-tree#sha256:8c509aeb9adf3f0b329f235fa729934210919fdbb93b24bb5d29e57d2af80e8a
Prompt template version: code-review-v1
Initial packet hash: sha256:a30866ff83c85ebe0eb0425c203cb2b401386ba99266d23daa8a0b983e7380e4
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Target: branch diff from `fcbbfda44a89945ee06cfa0c1b16dcbd39984036` to working tree `sha256:a30866ff83c85ebe0eb0425c203cb2b401386ba99266d23daa8a0b983e7380e4`
Reviewed milestone: M1, with the complete M1-M4 implementation correction present

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: three material implementation and proof findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CLIOBS-M1-CR7, CLIOBS-M1-CR8, CLIOBS-M1-CR9
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CLIOBS-M1-CR7, CLIOBS-M1-CR8, CLIOBS-M1-CR9
- Verify readiness: not-claimed

## Risk map

Affected behavior: result rendering; local diagnostic storage and lookup; lifecycle command integration; token-adoption measurement
Highest-impact failure modes: logging changes semantic truth; private values reach retained logs; invalid baseline authorizes a default; milestone evidence overstates direct proof
Changed boundaries: semantic-result/controller boundary; user-state filesystem boundary; lifecycle diagnostic/non-authority boundary; versioned measurement boundary
Evidence expected: exact diff inspection; negative logging probes; public process results; lifecycle byte comparisons; reproducible baseline; repository-owned validation
Areas requiring direct inspection: controller ordering; sink recovery; event projection; lookup; result renderer; measurement harness and baseline; focused and integration tests
Areas intentionally out of scope: hosted retention; network forwarding; v0.5 default adoption; package publication; release tagging
Risk classes considered: privacy; input validation; filesystem safety; failure recovery; concurrency; compatibility; lifecycle authority; token measurement; hosted-service security=not-applicable
Falsifiable review questions: Can logging failure change exit or repository bytes? Can a copied log settle state? Can control characters persist in any retained string? Do baseline bytes match the named pre-feature implementation?

## Prior-finding reconciliation

| Prior finding | Result | Evidence |
| --- | --- | --- |
| CLIOBS-M1-CR1 | resolved | Unsafe-path and clock/event construction probes preserve semantic dispatch and finalize observability as degraded. |
| CLIOBS-M1-CR2 | resolved | Absent-store lookup remains read-only. |
| CLIOBS-M1-CR3 | resolved | The controller attempts terminal logging before rendering one buffered result. |
| CLIOBS-M1-CR4 | resolved | Short writes roll back to the prior complete boundary; concurrent writers retain complete JSONL. |
| CLIOBS-M1-CR5 | partially resolved | Current bytes are measured from subprocesses, but the comparison baseline is not the recorded v0.4.x output; see CR7. |
| CLIOBS-M1-CR6 | partially resolved | Several missing partitions were added, but required cross-product and authority proofs remain absent; see CR8. |

## Findings

### Finding CLIOBS-M1-CR7

Finding ID: CLIOBS-M1-CR7
Severity: major
Location: `docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json` and `scripts/measure-cli-result-bytes.py`
Evidence: Replaying the six detailed interactions against pre-feature revision `bcc7ef14ae45e8df737d8a97e72eff3a3823446b` produced normalized byte counts `1035, 1422, 969, 511, 725, 1045` for status, context, mutation-success, mutation-blocked, validation-failure, and unexpected-error respectively. The checked-in baseline records `820, 1050, 760, 980, 800, 700` and contains no source revision or reproducible baseline-command mapping. The current eligibility result therefore compares real concise output with unsubstantiated baseline values.
Required outcome: Record the reproducible pre-feature v0.4.x detailed measurements and bind them to an exact source revision and deterministic detailed command mapping; add a regression that rejects missing or altered baseline provenance.
Safe resolution path: Update the immutable baseline values and provenance, validate the provenance in the measurement harness, rerun C06/C10, and report the recalculated result without changing defaults.
needs-decision rationale: none

### Finding CLIOBS-M1-CR8

Finding ID: CLIOBS-M1-CR8
Severity: major
Location: `packages/rigorloop/test/cli-observability.test.js`, `packages/rigorloop/test/cli-invocation-observability.test.js`, and milestone evidence M2-M4
Evidence: The approved T06 matrix requires every public command family crossed with success, blocked/rejected, unexpected-error, and thresholds, but current tests exercise one successful version invocation and a success threshold. T07 lacks environment-off, console-off failure, and several failure partitions. T12 has no repository-byte/semantic equivalence test across recorded, disabled, unsafe, and lock-failure states. T14 has no adversarial copied-log non-authority test. The M3/M4 evidence nevertheless reports the complete groups as passed.
Required outcome: Add direct deterministic tests for the specified family/severity/channel matrix and the diagnostic-only lifecycle authority boundary, or narrow the evidence claims and keep the milestone blocked where approved proof remains absent.
Safe resolution path: Extend the focused suites with table-driven controller/public-process tests, lifecycle state snapshots across diagnostic states, and adversarial copied-log checks, then rerun C01-C05 and update evidence to exact results.
needs-decision rationale: none

### Finding CLIOBS-M1-CR9

Finding ID: CLIOBS-M1-CR9
Severity: major
Location: `packages/rigorloop/dist/lib/diagnostic-event.js`
Evidence: Top-level strings are normalized, but allowlisted string collections such as `codes`, `finding_ids`, and `milestone_ids` are copied unchanged. A lifecycle completion event can therefore retain newline/control characters through those fields, contrary to R9's event-string normalization boundary.
Required outcome: Normalize or reject every string value in allowlisted collection fields and fail closed on unsupported value shapes without exposing the rejected input.
Safe resolution path: Add a typed field projector for scalar and string-list event fields plus unknown-value/control-character regressions.
needs-decision rationale: none

## Checklist

| Item | Result |
| --- | --- |
| Spec alignment | block: R9 and R29 evidence are not yet satisfied. |
| Test coverage | block: T06, T07, T12, and T14 claims exceed direct proof. |
| Error handling | pass for the six prior correction paths. |
| Architecture boundaries | pass for controller ordering and read-only inspection. |
| Compatibility | pass in focused legacy/new renderer and packed-package probes. |
| Security/privacy | block on unnormalized string-list event fields. |
| Derived artifact currency | block on incorrect baseline measurements. |
| Unrelated changes | noted: the lifecycle ownership regression is a bounded prerequisite repair. |

## Requirement-fidelity receipt

Requirement-fidelity gate: required
Requirement-fidelity applicability: applicable
Requirement-fidelity affected paths: packages/rigorloop/dist/lib/diagnostic-event.js; packages/rigorloop/test/cli-observability.test.js; packages/rigorloop/test/cli-invocation-observability.test.js; scripts/measure-cli-result-bytes.py; docs/reports/token-cost/cli/v0.4.x-detailed-baseline.json
Requirement-fidelity matched path triggers: specs/; docs/changes/**/reviews/
Requirement-fidelity matched category triggers: closed enums; generated-output or package parity validators; review-recording contracts
Requirement-fidelity review stage: code-review
Requirement-fidelity packet order: spec clause > architecture boundary > actual diff > direct probes > validation evidence > prior-finding reconciliation
Requirement-property decomposition evidence: present
Relevant spec clauses decomposed: yes
Property matrix complete: no; CR8 identifies missing direct partitions
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Requirement-fidelity outcome: changes-requested

## Independent-review receipts

Strict blind-first independence is not claimed because prior findings were already known in this local context. The risk map was re-derived from governing artifacts and the actual diff before prior-finding reconciliation. No clean-review sufficiency receipt is issued because material findings remain.

## Handoff

Workflow automation should route these findings through review-resolution, return to implementation for bounded correction, then request code-review M1 R3. No owner decision is required.
