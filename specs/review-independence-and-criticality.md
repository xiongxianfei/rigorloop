# Review Independence and Criticality

## Status

approved

## Related proposal

- [Independent Adversarial Review Gates for Automated Workflows](../docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md)

## Goal and context

This spec defines the contract for independent adversarial review gates in workflow-managed automated reviews.

The goal is to make automated review outcomes trustworthy by separating review judgment from authoring context, validation-result anchoring, prior-finding anchoring, and autoprogression incentives. The goal is not to increase finding count. Clean reviews remain valid when the review can show what it tried to falsify and why no material defect was found.

This spec supersedes the "hard fresh-session enforcement is out of scope" boundary in `specs/code-review-independence-under-autoprogression.md` for automated `code-review` once the first rollout phase lands. Existing evidence-backed clean-review and first-pass review-record requirements remain compatible unless a later approved spec replaces them.

No implementation or autoprogression behavior changes until this spec, its matching test spec, and the relevant implementation plan are approved.

## Glossary

- `automated review`: a formal lifecycle review invoked by a workflow-managed autoprogression profile rather than a direct isolated user request.
- `authoring context`: the session, agent, or invocation that authored or changed the reviewed artifact, ran implementation, or prepared validation for the reviewed artifact.
- `review context`: the session, agent, invocation, or human review boundary that performs the formal review.
- `fresh context`: a review context whose initial evidence packet is built from tracked artifacts and neutral routing metadata, with no inherited author chat, hidden reasoning, recent-work memory, implementation narrative, desired outcome, validation-result summary, evidence menu, prior finding content, or auto-fix budget.
- `independence level`: the recorded separation level for a review context, selected from `L0`, `L1`, `L2`, or `L3`.
- `L0`: author-continuation mode. The review is an uninterrupted continuation of the authoring context or cannot prove otherwise.
- `L1`: verifiably fresh context using the same model or reviewer type.
- `L2`: separate agent or independently created session. Model heterogeneity is optional unless a trigger requires it.
- `L3`: heterogeneous reviewer or human reviewer according to critical-risk policy.
- `irreversible external action`: deploy, publish, secret handling, destructive migration, privileged remote mutation, or another action that cannot be fully reviewed and reversed within the repository tree.
- `initial packet`: the bounded set of artifacts, revisions, hashes, and neutral routing metadata provided to the reviewer before independent risk-map recording.
- `evidence menu`: the list of validation evidence types or records available for request after the initial risk map is recorded.
- `phase receipt`: an immutable process event recording that a review phase completed or a later evidence category was released.
- `risk map`: the reviewer's recorded independent orientation before validation results, evidence menus, implementation narrative, or prior finding content is released.
- `review invocation manifest`: orchestrator-owned process metadata describing review target, independence level, context identifiers, initial packet, risk tier, phase receipts, and handoff eligibility.
- `review gate outcome`: normalized orchestration result derived from a stage-native review result and gate validity checks.
- `clean-review sufficiency receipt`: evidence that a clean automated review considered relevant risk classes, tested adversarial hypotheses, challenged validation evidence, and identified unreviewed surfaces.
- `second-review disagreement`: a material finding, blocked result, or inconclusive result from a required or sampled second review after the first review was clean.
- `failed-remediation`: a prior finding claimed or expected to be fixed but rediscovered independently during a blind-first rereview.

## Examples first

### Example E1: standard-risk automated code review advances

Given an automated `code-review` is classified as standard risk
And the orchestrator creates an L1 fresh context with a valid initial packet
When the reviewer records a risk map, requests validation evidence, challenges the evidence, and finds no material defect
Then the review may produce `clean-with-notes`
And the derived `review_gate_outcome` is `advance` only if the manifest, phase receipts, and clean-review sufficiency receipt are valid.

### Example E2: same-context review cannot advance

Given implementation completes in one context
When the same context immediately performs `code-review` without a verifiably fresh review context
Then the independence level is `L0`
And the automated review is ineligible for handoff with `review_gate_outcome: inconclusive`.

### Example E3: validation evidence does not anchor the risk map

Given an automated review has available test output
When the reviewer has not recorded an initial risk map
Then the orchestrator withholds validation-result summaries and the evidence menu
And releases the evidence menu only after the `risk-map-recorded` phase receipt exists.

### Example E4: prior findings do not narrow rereview

Given an automated rereview follows a prior material finding
When the reviewer begins the new review
Then the reviewer may know prior rounds occurred but does not receive prior finding content until after the blind-first pass
And may record new findings before reconciling prior findings.

### Example E5: second reviewer finds a material issue

Given a standard-risk clean review is sampled during rollout
When the second independent reviewer records a material finding
Then the first clean review does not overrule it
And automatic continuation stops for review-resolution, owner decision, or an authorized follow-up review.

### Example E6: critical external action requires human authority

Given a change includes package publication or secret-handling behavior
When the review gate classifies the change as critical risk
Then human authority is required before any clean review can advance the automated workflow.

### Example E7: clean receipt is insufficient

Given an automated review says only "tests passed and the change looks correct"
When no risk classes, hypotheses, direct proof, validation challenge, or unreviewed surfaces are recorded
Then the clean-review sufficiency receipt is invalid
And the review cannot advance the automated workflow.

### Example E8: code-review changes-requested routes under profile authority

Given automated `code-review` runs under an active `implementation-through-verify` profile
And the review records native `changes-requested`
And every finding has valid `auto_fix_class`
And the independence manifest, phase receipts, and correction-loop policy all permit another round
When the orchestrator evaluates `review_gate_outcome: stop`
Then the orchestrator may route to `review-resolution` under the profile authority
And records the authorizing profile, round number, and satisfied independence evidence.

### Example E9: unclassified code-review finding pauses

Given automated `code-review` runs under an active `implementation-through-verify` profile
And the review records native `changes-requested`
And at least one finding has `auto_fix_class: none`
When the orchestrator evaluates `review_gate_outcome: stop`
Then the orchestrator pauses with stop reason `correction-finding-unclassified`
And does not route to `review-resolution` even though the profile could otherwise authorize correction rounds.

### Example E10: spec-review changes-requested without routing authority pauses

Given automated `spec-review` records native `changes-requested`
And no active profile independently authorizes automatic resolution for that review stage
When the orchestrator evaluates `review_gate_outcome: stop`
Then the orchestrator pauses with stop reason `changes-requested-not-routable`
And requires explicit user action before spec revision or downstream continuation.

## Requirements

R1. Automated reviews MUST use a valid independence level of `L1`, `L2`, or `L3` before they can advance an automated workflow.

R1a. `L0` MUST NOT be valid for automated lifecycle review handoff.

R1b. If the platform cannot expose enough identity or provenance data to distinguish the review context from the authoring context, the review MUST be treated as `L0` for automated handoff.

R1c. Same-model review MAY satisfy `L1` only when the review context is verifiably fresh and receives a clean initial packet.

R1d. Different-model review MUST NOT compensate for a biased or author-contaminated initial packet.

R2. Independence levels MUST use this policy:

| Risk tier | Required level | Rule |
| --- | --- | --- |
| Standard | `L1` | Same model is allowed in a verifiably fresh context. |
| Elevated | `L2` | A separately created agent or session is required; model heterogeneity is optional unless a specific trigger requires it. |
| Critical internal change | `L3` | Heterogeneous or human review is required according to project policy. |
| Irreversible external action | human authority | Human authority is required; heterogeneous LLM review alone is insufficient. |

R3. The orchestrator MUST own the review invocation manifest.

R3a. The reviewer MUST NOT be able to rewrite the manifest after later evidence is released.

R3b. The manifest MUST record:

- review ID;
- review stage;
- review target;
- base and head revision when applicable;
- native review status when known;
- derived `review_gate_outcome` when known;
- independence level;
- author context ID when available;
- reviewer context ID;
- context separation mechanism;
- risk tier;
- risk-tier triggers;
- risk-tier classifier;
- governing artifacts;
- formal criteria;
- initial-packet inventory;
- prompt template version or equivalent invocation template identifier;
- initial-packet hash;
- manifest owner;
- phase receipts.

R3c. The manifest MUST use schema-bounded fields for process evidence. Free-form fields SHOULD be short, evidence-referential, and bounded by length.

R3d. The manifest MUST NOT include private chain-of-thought, hidden reasoning, author self-assessment, desired outcome, or persuasive implementation narrative.

R4. The initial packet MUST be verifiable rather than merely attested.

R4a. The initial packet inventory MUST record each included tracked artifact path, revision, and content hash.

R4b. The manifest MUST record an `initial_packet_sha256` or equivalent aggregate hash over the initial packet.

R4c. `author_context_excluded: true` MUST NOT be the only proof that author context was excluded.

R4d. A missing packet inventory, missing packet hash, or mismatch between recorded and delivered packet evidence MUST make the review ineligible for automatic handoff.

R5. Before initial risk-map recording, the reviewer MUST NOT receive:

- author hidden reasoning;
- author chain-of-thought;
- author self-assessment;
- claims that the change is correct;
- desired review outcome;
- autoprogression round budget;
- message that approval is needed to continue;
- auto-fix eligibility;
- implementation-stage safety narrative;
- prior reviewer conclusion;
- prior finding content;
- validation-result summaries;
- evidence menu.

R5a. The reviewer MAY know objective workflow facts, including review target identity, review stage, governing artifact paths, formal criteria, and that prior review rounds or resolution records exist.

R6. The automated review protocol MUST be blind-first.

R6a. The reviewer MUST record a risk map before validation-result summaries, evidence menus, implementation notes, or prior finding content are released.

R6b. The risk map MUST include affected behavior, highest-impact failure modes, changed boundaries, evidence expected, areas requiring direct inspection, and intentionally out-of-scope areas.

R6c. The reviewer MUST record applicable and non-applicable risk classes with a brief evidence-based reason.

R6d. The reviewer MUST formulate falsifiable review questions for applicable risk classes.

R6e. The evidence menu MUST be released only after the `risk-map-recorded` phase receipt exists.

R6f. Validation result content MUST be released only after the reviewer requests evidence from the evidence menu or reaches the evidence-challenge phase.

R7. The manifest MUST record phase receipts for:

- `risk-map-recorded`;
- `evidence-menu-released`;
- `evidence-results-released`;
- `prior-findings-released` when applicable;
- `verdict-recorded`.

R7a. A missing phase receipt, inconsistent phase order, or early release of forbidden context MUST make the review ineligible for automatic handoff.

R8. Rereview MUST preserve independent defect discovery.

R8a. Prior finding content MUST be hidden until after the blind-first pass.

R8b. The reviewer MAY report new findings in any review round.

R8c. Prior finding reconciliation MUST classify items as `resolved`, `still-present`, `failed-remediation`, `reopened`, `superseded`, or `new-finding`.

R8d. `failed-remediation` MUST be recorded when a prior finding was claimed or expected to be fixed but is independently rediscovered during the blind-first pass.

R9. Reviewer and orchestrator responsibilities MUST remain separate.

R9a. The reviewer owns finding discovery, severity, evidence, required outcome, native review result, verdict, and confidence.

R9b. The orchestrator owns workflow continuation, round-limit enforcement, profile state, next-stage invocation, manifest ownership, risk-tier classification, and normalized gate outcome.

R9c. The reviewer MUST NOT suppress a finding because it would pause automation, exceed a correction budget, delay verify, or require owner attention.

R9d. Auto-fix classification MUST occur after finding and verdict recording.

R9e. Auto-fix classification SHOULD use a separate classifier invocation from the reviewer when the workflow supports that separation.

R10. Risk-tier classification MUST be orchestrator-owned and fail closed.

R10a. Risk tier MUST be determined by deterministic checks against affected paths, changed surfaces, metadata, declared workflow actions, and explicit review triggers.

R10b. Author self-assessment MUST NOT be the sole input to risk-tier classification.

R10c. Ambiguous matches MUST use the higher plausible tier.

R10d. If the classifier lacks enough evidence to choose a tier, the review MUST be `inconclusive` unless the higher plausible tier can be satisfied.

R11. Risk-tier triggers MUST include at least:

| Tier | Trigger examples |
| --- | --- |
| Elevated | public API behavior, workflow or validator behavior, generated-output machinery, compatibility or migration logic, concurrency, persistent state, release packaging, authentication or authorization, security-relevant configuration, multi-component changes |
| Critical internal | privilege boundary, high-impact security change, destructive internal migration, critical review or release policy change |
| Irreversible external action | deploy, publish, credential or secret handling, privileged remote mutation, irreversible external migration |

R12. Automated review gates MUST preserve stage-native review statuses and expose a derived `review_gate_outcome`.

R12a. `review_gate_outcome` MUST be one of `advance`, `stop`, `blocked`, or `inconclusive`.

R12b. The orchestrator MUST consume `review_gate_outcome` rather than relying only on stage-specific string comparisons.

R12c. Native `approved` maps to `advance` only when required independence, evidence, recording, and escalation gates pass.

R12d. Native `clean-with-notes` maps to `advance` only when no open material finding remains and required independence, evidence, clean-receipt, recording, and escalation gates pass.

R12e. Native `changes-requested` maps to `stop`.

R12f. `review_gate_outcome: stop` MUST mean the review gate did not produce a clean advance. It MUST NOT be interpreted as "pause all automation" by default.

R12f1. When `review_gate_outcome: stop` arises from native `changes-requested`, the orchestrator MUST evaluate routing in this order:

1. If an active workflow profile independently authorizes a `review-resolution` route for this review stage, the independence manifest is valid, required sufficiency or phase receipts are recorded, and the profile correction-loop policy permits another round, the orchestrator MAY route to `review-resolution`.
2. Otherwise, the orchestrator MUST pause the profile with stop reason `changes-requested-not-routable` and report the missing authorization condition.

R12f2. A `review-resolution` route from `review_gate_outcome: stop` MUST record the authorizing profile, round number, and satisfied independence evidence.

R12f3. When `review_gate_outcome: stop` cannot route because the active correction-loop policy rejects the finding set, the orchestrator MUST use the profile-specific stop reason when one exists, such as `correction-finding-unclassified`.

R12f4. Native `blocked` and native `inconclusive` MUST pause regardless of profile authorization. These verdicts MUST NOT route to automatic resolution.

R12f5. Review routing eligibility MUST NOT modify the reviewer's verdict. The reviewer records native `changes-requested`, `blocked`, or `inconclusive` based on the artifact, and the orchestrator independently evaluates whether continuation is authorized.

R12g. Native `blocked` maps to `blocked`.

R12h. Native `inconclusive` maps to `inconclusive`.

R13. A clean automated review MUST include a clean-review sufficiency receipt before it can advance.

R13a. The receipt MUST include review target identity, independence level, governing artifacts inspected, risk classes considered, adversarial hypotheses tested, direct proofs or reproductions performed, validation evidence challenged, unreviewed or uncertain surfaces, confidence, and no-finding rationale.

R13b. Passing validation alone MUST NOT satisfy the clean-review sufficiency receipt.

R13c. A clean receipt that lacks material risk coverage MUST produce `review_gate_outcome: inconclusive`.

R14. Second-review sampling and escalation MUST affect handoff eligibility.

R14a. During rollout, standard-risk clean automated reviews MUST be sampled at no less than 20%.

R14b. During rollout, the system MUST collect at least 10 independently reviewed standard-risk clean outcomes before reducing the standard-risk sampling rate.

R14c. Elevated-risk clean automated reviews MUST receive second review at 100% during rollout and steady state unless a later accepted proposal revises the policy.

R14d. Critical-risk reviews MUST satisfy their configured `L3` or human authority gate.

R14e. A second reviewer's material finding, `blocked` result, or `inconclusive` result MUST prevent automatic continuation.

R14f. The first review MUST NOT overrule second-review disagreement, and the system MUST NOT use majority-vote approval to advance.

R14g. Second-review disagreement MUST route to review-resolution, owner decision, or another formally authorized review according to the finding and governing workflow state. Ordinary first-review native `changes-requested` routing is governed by `R12f`, not by `R14g`.

R15. Steady-state standard-risk sampling SHOULD be measurement-driven.

R15a. The standard-risk sample rate SHOULD be high enough to bound the observed material-disagreement rate with a project-defined confidence interval.

R15b. Sampling SHOULD increase after workflow changes, model changes, prompt changes, calibration misses, or downstream material escapes.

R16. Calibration MUST distinguish known-fixture recurrence from novel-defect detection.

R16a. Public fixtures MAY document defect classes and examples.

R16b. Measured calibration SHOULD use private or access-controlled rotating fixture instances when practical.

R16c. Calibration records MUST distinguish recurrence-detection, novel-defect detection, second-review disagreement, downstream escape, false-positive rate, inconclusive rate, receipt quality, and review duration.

R16d. Calibration metrics MUST be tracked by review skill and risk tier.

R17. Review records and manifests MUST avoid private reasoning leakage.

R17a. Record formats MUST prefer closed vocabulary fields, stable identifiers, paths, hashes, check IDs, and evidence references.

R17b. Validators SHOULD reject forbidden private-reasoning fields and unbounded free-form manifest fields.

R17c. Calibration SHOULD audit sampled records for private reasoning leakage, excessive narrative, and evidence-free assertions.

R18. A final holistic code review MUST occur before automated implementation flow transitions to `explain-change` or `verify`.

R18a. The final holistic review MUST cover the complete final diff, cross-milestone interactions, governing proposal/spec/test-spec/architecture/plan, review resolutions, final validation selection, generated or derived artifacts, and cross-milestone scope.

R18b. A final holistic review MUST NOT be only the last milestone's local review.

R19. Phase 1 rollout MUST pilot the full contract in automated `code-review`.

R19a. During Phase 1, automated `spec-review` and `plan-review` SHOULD at least record review invocation manifests even before adopting the full blind-first protocol.

R19b. Phase 1 evidence MAY trigger acceleration of full `spec-review`, `architecture-review`, or `plan-review` adoption.

R20. Manual and profile-off review behavior MUST remain compatible.

R20a. Direct isolated review invocations remain isolated by default.

R20b. Profile-off review behavior MUST NOT require automated-review manifests unless the review is being used as an automated handoff gate.

R20c. This spec MUST NOT require every review to produce a finding.

R20d. This spec MUST NOT establish a finding-count quota, average finding target, or percentage-failed target.

## Inputs and outputs

Inputs:

- review target identity;
- actual tracked artifact, diff, commit range, or review surface;
- base and head revision when applicable;
- governing proposal, spec, test spec, architecture, ADR, and plan when applicable;
- formal review criteria;
- workflow stage and profile state;
- author context identifier when available;
- platform-supported review context identifier;
- affected paths and changed-surface metadata;
- declared workflow actions, including external-boundary actions;
- validation evidence inventory and results, staged by phase;
- prior review and resolution records, staged by phase.

Outputs:

- review invocation manifest;
- initial-packet inventory and hash;
- phase receipts;
- risk map;
- risk-tier classification;
- stage-native review result;
- normalized `review_gate_outcome`;
- clean-review sufficiency receipt when applicable;
- prior-finding reconciliation when applicable;
- second-review calibration record when applicable;
- stop reason when handoff is ineligible.

## State and invariants

- Automated review handoff never uses `L0`.
- The orchestrator owns manifest creation and handoff eligibility.
- The reviewer forms initial risks before validation results, evidence menus, implementation narratives, or prior finding content.
- Reviewer verdict is not optimized for autoprogression continuation.
- Clean review is valid only with sufficient affirmative evidence.
- Second-review disagreement prevents automatic continuation.
- Human authority is required for irreversible external actions.
- Finding count is a diagnostic signal, not a quality target.

## Error and boundary behavior

- Missing or invalid manifest produces `review_gate_outcome: inconclusive`.
- Missing initial-packet inventory or hash produces `review_gate_outcome: inconclusive`.
- `reviewer_context_id` equal to `author_context_id`, when both are present, produces `L0` and prevents handoff.
- Missing context identity on a platform that cannot otherwise prove separation produces `L0` for handoff.
- Early release of validation results, evidence menu, or prior finding content before required phase receipts prevents handoff.
- Missing clean-review sufficiency receipt prevents clean handoff.
- Ambiguous risk-tier classification uses the higher plausible tier or becomes `inconclusive`.
- Required second-review disagreement prevents automatic continuation.
- Critical-risk irreversible external action without human authority prevents automatic continuation.
- A review may still record independently supported findings even when missing evidence prevents a clean handoff.

## Compatibility and migration

- This spec strengthens automated review gates; it does not change direct isolated review behavior by default.
- This spec preserves stage-native review statuses while adding `review_gate_outcome` for orchestration.
- This spec supersedes the no-hard-fresh-session boundary for automated `code-review` once the `code-review` pilot lands.
- Existing code-review first-pass records and evidence-backed clean review requirements remain compatible.
- Existing workflow-stage autoprogression profiles remain inactive unless explicitly armed according to their governing specs.
- Generated skills and adapters must be rebuilt only during implementation slices that change canonical skill sources.
- Public adapter generated output must not be hand-edited.

## Observability

- Review manifests expose independence level, context identifiers, separation mechanism, risk tier, initial-packet hash, phase receipts, native review result, and `review_gate_outcome`.
- Calibration records expose sample rate, second-reviewer type, independence level, material disagreements, severity disagreements, evidence gaps, escapes, and fixture mode.
- Stop reasons distinguish independence failure, invalid manifest, missing evidence, insufficient clean receipt, risk-tier escalation failure, second-review disagreement, and human-authority requirement.
- Metrics are reported by review skill and risk tier.

## Security and privacy

- Manifests and receipts must not record private chain-of-thought, hidden reasoning, secrets, credentials, or private keys.
- Initial-packet hashes and artifact revisions are allowed process evidence.
- Human authority records for critical-risk external actions should record decision identity or role without exposing private credentials or sensitive operational details.
- Private or access-controlled calibration fixtures should be protected from broad disclosure when used to measure novel-defect detection.

## Accessibility and UX

Not applicable to end-user UI. Contributor-facing review outputs should remain scan-first and use stable field labels so humans can quickly identify status, stop reason, evidence, and next action.

## Performance expectations

- Standard-risk automated review cost is expected to increase during rollout because of blind-first review, sufficiency receipts, and sampling.
- Rollout planning should assume roughly a 2-3x review-cost multiplier for sampled standard-risk clean reviews until measured data supports tuning.
- Steady-state sampling may reduce standard-risk cost only after the rollout evidence floor and disagreement confidence criteria are satisfied.
- The contract should use bounded evidence packets and targeted review surfaces to avoid broad repository reads without risk justification.

## Edge cases

EC1. Same model, clean packet: A same-model review may advance as `L1` only when context identity and clean-packet evidence prove separation.

EC2. Different model, biased packet: A different-model review receiving author conclusions or desired outcome is not independent for handoff.

EC3. Prior rounds exist: The reviewer may know prior rounds exist but does not receive prior finding content until reconciliation.

EC4. Reviewer finds a new issue during rereview: The finding is recorded and may pause automation even when it was not in the previous finding list.

EC5. Reviewer cannot inspect tests but finds a clear spec mismatch: The review may record the supported finding, but cannot claim a clean handoff.

EC6. Second reviewer is inconclusive: Automatic continuation stops; the first clean review does not override the inconclusive result.

EC7. Elevated-risk trigger ambiguity: The classifier uses elevated or critical risk when trigger evidence is ambiguous.

EC8. Critical internal security change: L3 heterogeneous review may be acceptable when no irreversible external action is authorized and project policy allows it.

EC9. Publication path: Human authority is required before automated clean-review handoff can support an irreversible publish action.

EC10. Clean receipt only cites passing tests: The clean receipt is invalid and the gate outcome is `inconclusive`.

## Non-goals

- Do not require every review to produce a finding.
- Do not score review quality by finding count.
- Do not require different model vendors for every review.
- Do not expose private chain-of-thought.
- Do not let validation results substitute for independent review.
- Do not let previous findings narrow rereview to fix confirmation.
- Do not let reviewers edit the target artifact during review.
- Do not introduce a hosted review service or persistent external control plane.
- Do not automatically resolve findings through this spec.
- Do not change PR opening, publishing, deployment, or external-boundary authority.

## Acceptance criteria

AC1. An automated review with `L0` cannot produce `review_gate_outcome: advance`.

AC2. An automated review records an orchestrator-owned manifest with distinct context evidence or fails closed.

AC3. The initial packet inventory includes paths, revisions, hashes, prompt template version, and aggregate hash.

AC4. Validation results and evidence menu are withheld until after the risk map is recorded.

AC5. Prior finding content is withheld until reconciliation.

AC6. Stage-native `approved` and `clean-with-notes` map to `advance` only after independence, evidence, recording, and escalation gates pass.

AC7. `changes-requested`, `blocked`, and `inconclusive` map to `stop`, `blocked`, and `inconclusive` respectively.

AC8. Standard, elevated, critical internal, and irreversible external action tiers enforce their required independence or authority levels.

AC9. A second reviewer's material finding, blocked result, or inconclusive result prevents automatic continuation.

AC10. Rollout samples at least 20% of standard-risk clean reviews and collects at least 10 independently reviewed standard-risk clean outcomes before rate reduction.

AC11. Elevated-risk clean reviews receive second review at 100% unless a later accepted proposal revises the policy.

AC12. Clean automated review requires a sufficiency receipt with risk classes, hypotheses, direct proof, validation challenge, unreviewed surfaces, and no-finding rationale.

AC13. Final automated transition to `explain-change` or `verify` requires a holistic final code review.

AC14. Calibration metrics separate recurrence-detection, novel-defect detection, disagreement, escapes, false positives, inconclusive rate, receipt quality, and review duration by skill and risk tier.

AC15. Manual and profile-off review behavior remains compatible.

AC-RAI-018. `changes-requested` reviews route to `review-resolution` only when an active profile and its independence, evidence, and policy gates all permit; otherwise they pause.

## Test IDs

RAI-021. `review_gate_outcome: stop` is interpreted by the orchestrator per `R12f`, not as a uniform "pause all automation."

RAI-022. `blocked` and `inconclusive` outcomes pause regardless of profile authorization.

RAI-023. A route to `review-resolution` records the authorizing profile, round number, and independence evidence.

## Open questions

None.

The proposal-review directives were resolved into this spec's requirements. Future changes to sample rates, risk triggers, or second-review authority should use the normal proposal/spec flow.

## Next artifacts

- architecture-review
- matching test spec
- execution plan

## Follow-on artifacts

- Spec-review approved with no open findings in `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/spec-review-r2.md`.
- Architecture package update and ADR authored for architecture-review.

## Readiness

Ready for `architecture-review`.
