# Spec Review R1: CLI Observability and Token-Efficient Results

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/cli-observability-and-token-efficient-results.md`
Reviewed artifact: `sha256:60a0fc29fd429e56673d87b32bccd6d2411dbfaba7f2bf5f5d6b02f38e6e612a`
Review date: 2026-08-25
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CLIOBS-SR1, CLIOBS-SR2, CLIOBS-SR3
- Open blockers: retained-ID expiry evidence, configuration failure behavior, and concise/adoption applicability are not deterministic
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: same-stage rereview required after the three bounded contract corrections

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-log.md`
- Review resolution: `docs/changes/2026-08-25-cli-observability-token-efficient-results/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required
- Governed change identity: `2026-08-25-cli-observability-token-efficient-results`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: three requirement-owned outcomes are incomplete or ambiguous

## Automated review

- Automation mode: workflow-managed-automated
- Automation evidence: `review-invocation-spec-review-r1.yaml`
- Automation result: bounded specification correction eligible; independent rereview required before promotion

## Findings

## Finding CLIOBS-SR1

Finding ID: CLIOBS-SR1
Severity: major
Location: R13, R19, R34, EC5, BND-STATE-001, and BND-ENV-001
Evidence: R19 requires `RL_LOG_EXPIRED` when an invocation has rotated out, but random invocation IDs have no ordering information and the contract defines only five scanned log files. EC5 refers to rotation metadata without defining an owned, bounded, privacy-safe representation. An implementation cannot prove that an arbitrary absent ID expired rather than never existed without inventing durable state outside the specified scan boundary.
Required outcome: Either remove the expired/not-found distinction or define the exact bounded evidence, ownership, retention, privacy, and lookup rules that prove expiry without introducing an unbounded index or hidden governed state.
Safe resolution path: Collapse absent retained IDs to `RL_LOG_NOT_FOUND` in the first release and reserve `RL_LOG_EXPIRED` for a later contract with an explicit bounded index.
needs-decision rationale: none

## Finding CLIOBS-SR2

Finding ID: CLIOBS-SR2
Severity: major
Location: R11, R12, R15-R17, E4, EC3, EC6, EC9, BND-INPUT-001, and INT-001
Evidence: R11 requires an override to be “contained” but names no containment root, so every absolute directory can be treated as contained in itself or rejected by an invented policy. R15/E4 require a logging-failure stderr diagnostic while R17 and EC6 admit `--console-log-level off`, without stating whether the emergency diagnostic bypasses `off`. Existing broad permissions also degrade observability without a closed code or a specified mutation policy.
Required outcome: Define the containment boundary for selected directories, the symlink and existing-permission behavior, and one deterministic relationship between `off` and the single emergency logging diagnostic.
Safe resolution path: Treat the selected absolute directory as the containment root for owned descendants, refuse symlink components, do not chmod pre-existing entries, use `RL_LOG_UNSAFE_PATH` for unsafe paths or permissions, and state whether `off` suppresses the emergency diagnostic.
needs-decision rationale: none

## Finding CLIOBS-SR3

Finding ID: CLIOBS-SR3
Severity: major
Location: R23-R25, R29-R31, E2, E7, INT-003, INT-005, and AC7-AC10
Evidence: The closed concise field list does not define which command/outcome requires each continuation fact; “normally” leaves the two-line requirement's exceptions open; and the adoption gate does not identify the frozen baseline, representative fixture ownership, aggregation rule for the median, or the local Python wrappers covered by R31. Tests could pass incompatible projections or select a favorable corpus while claiming the same requirements.
Required outcome: Add a command/outcome applicability matrix for concise fields, close the human-output exceptions, and define versioned benchmark fixture ownership, baseline comparison, median calculation, and the exact wrapper surface covered by this release.
Safe resolution path: Specify mandatory common fields plus lifecycle and rejection conditionals, enumerate the only line-budget exceptions, pin a repository-owned benchmark manifest and v0.4.x baseline, use an unweighted median across named profiles, and enumerate the current local wrappers after repository inspection.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | concern |
| completeness | block |
| testability | block |
| examples | pass |
| compatibility | concern |
| observability | block |
| security/privacy | concern |
| non-goals | pass |
| acceptance criteria | concern |

## Boundary assessment

All eight dimensions are classified and structurally valid. The retained-state outcome lacks evidence ownership, the configuration interaction has conflicting interpretations, and the composition/compatibility gates lack closed proof inputs. Examples remain illustrative and do not independently create behavior.

## Recommendation

Apply the three bounded corrections and perform a fresh independent spec review. Architecture assessment, planning, and test-spec authoring remain blocked until approval.

## Claim limitations

This review does not approve the specification, settle architecture, authorize planning, establish test-spec readiness, or claim implementation, verification, branch, CI, or PR readiness.
