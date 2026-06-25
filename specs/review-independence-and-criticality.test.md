# Review Independence and Criticality Test Spec

## Status

- active

## Related spec and plan

- Spec: [Review Independence and Criticality](review-independence-and-criticality.md), approved.
- Plan: [Independent Adversarial Review Gates Execution Plan](../docs/plans/2026-06-25-independent-adversarial-review-gates.md), approved by `plan-review-r2`.
- Proposal: [Independent Adversarial Review Gates for Automated Workflows](../docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md), accepted.
- Architecture: [System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260625 Independent Adversarial Review Gates](../docs/adr/ADR-20260625-independent-adversarial-review-gates.md), accepted.
- Spec-review: [spec-review-r2](../docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/spec-review-r2.md), approved.
- Architecture-review: [architecture-review-r1](../docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/architecture-review-r1.md), approved.
- Plan-review: [plan-review-r2](../docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/reviews/plan-review-r2.md), approved.

## Testing strategy

- Use unit and fixture-backed integration tests in `scripts/test-review-artifact-validator.py`, `scripts/review_artifact_validation.py`, `scripts/test-change-metadata-validator.py`, and `scripts/change_metadata_semantics.py` for manifest shape, packet inventory, phase receipts, clean-review sufficiency receipts, private-reasoning-safe fields, calibration records, and review artifact compatibility.
- Use lifecycle/state-sync integration tests in `scripts/test-artifact-lifecycle-validator.py`, `scripts/artifact_lifecycle_validation.py`, and `scripts/lifecycle_state_sync.py` for `review_gate_outcome`, risk-tier routing, `changes-requested` stop semantics, second-review disagreement, final holistic review gates, manual/profile-off compatibility, and active-plan state synchronization.
- Use skill-validator and generated-output tests in `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/test-build-skills.py`, and `scripts/build-skills.py --check` for canonical review-family guidance, code-review pilot behavior, direct isolated review compatibility, no finding quota, and no target-edit authority.
- Use public adapter archive proof whenever canonical `skills/` files change: `python scripts/build-adapters.py --version <manifest-version> --output-dir <tmpdir>` followed by `python scripts/validate-adapters.py --root <tmpdir> --version <manifest-version>`.
- Use selected validation routing tests in `scripts/test-select-validation.py`, `scripts/select-validation.py`, and `scripts/ci.sh` for new deterministic evidence paths, fixture paths, and generated proof surfaces.
- Use manual contract review only for policy statements that cannot be fully asserted structurally, such as sampling confidence-interval tuning, private rotating fixture custody, and bounded-evidence review quality.
- Do not add a hosted service, network dependency, external control plane, or semantic review-quality scorer.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R1d`, `AC1`, `AC2` | `T1`, `T2`, `T7`, `T17` | integration | Independence levels, L0 invalidity, same-model freshness, biased packet failure, context identity. |
| `R2`, `R11`, `AC8` | `T1`, `T7`, `T17` | integration | Standard, elevated, critical internal, and irreversible external action tier requirements. |
| `R3`-`R3d`, `AC2`, `AC3` | `T1`, `T2`, `T12`, `T19` | integration | Orchestrator-owned manifest, bounded fields, required manifest fields, immutable owner. |
| `R4`-`R4d`, `AC3` | `T2`, `T19` | integration | Verifiable initial packet inventory, revisions, hashes, aggregate packet hash, mismatch failure. |
| `R5`-`R5a`, `AC4`, `AC5` | `T2`, `T3`, `T5` | integration | Prohibited initial context, allowed workflow facts, evidence-menu and prior-finding deferral. |
| `R6`-`R6f`, `AC4` | `T3`, `T4` | integration | Blind-first risk map, risk classes, hypotheses, evidence-menu and result release ordering. |
| `R7`-`R7a` | `T3`, `T19` | integration | Phase receipts and fail-closed phase order. |
| `R8`-`R8d`, `AC5` | `T5` | integration | Rereview discovery, new findings, reconciliation categories, `failed-remediation`. |
| `R9`-`R9e` | `T6`, `T8`, `T15` | integration, manual | Reviewer-orchestrator separation, verdict ownership, auto-fix classification after verdict. |
| `R10`-`R10d`, `AC8` | `T7` | integration | Orchestrator-owned deterministic risk-tier classification and fail-closed ambiguity. |
| `R12`-`R12h`, `AC6`, `AC7`, `AC-RAI-018`, `RAI-021`-`RAI-023` | `T8` | integration | Native status mapping, normalized gate outcome, routable and unroutable `changes-requested`, blocked/inconclusive pause. |
| `R13`-`R13c`, `AC12` | `T9` | integration | Clean-review sufficiency receipt fields and insufficient receipt failure. |
| `R14`-`R14g`, `AC9`-`AC11` | `T10` | integration | Rollout sampling floor, elevated 100% second review, critical gate, disagreement stop, no majority override. |
| `R15`-`R15b` | `T10`, `T11`, manual sampling review | integration, manual | Measurement-driven steady-state sampling and rate-increase triggers. |
| `R16`-`R16d`, `AC14` | `T11` | integration, manual | Calibration records, recurrence versus novel defect, metrics by review skill and risk tier. |
| `R17`-`R17c` | `T1`, `T12`, `T19` | integration, manual | Private-reasoning-safe record shapes, forbidden fields, bounded free-form fields, audit path. |
| `R18`-`R18b`, `AC13` | `T13` | integration | Final holistic code review blocks `explain-change` and `verify` when missing or milestone-local only. |
| `R19`-`R19b` | `T14`, `T18` | integration, manual | Code-review pilot, manifest-only spec/plan review phase-one evidence, generated guidance proof. |
| `R20`-`R20d`, `AC15` | `T15` | integration, manual | Manual/profile-off compatibility, isolated review behavior, no finding quota. |
| Inputs and outputs | `T1`-`T3`, `T7`-`T11`, `T16`, `T19` | integration | Required manifest, packet, receipt, risk-tier, calibration, stop-reason, and outcome outputs. |
| State and invariants | `T1`, `T3`, `T6`, `T8`-`T10`, `T13`, `T15`, `T17` | integration | No L0 handoff, blind-first risk formation, clean evidence, disagreement stops, human authority. |
| Error and boundary behavior | `T1`-`T3`, `T7`-`T10`, `T13`, `T17` | integration | Missing evidence, equal context IDs, early release, insufficient clean receipt, critical action failure. |
| Compatibility and migration | `T14`, `T15`, `T18` | integration, manual | Direct isolated review unchanged, generated skills/adapters rebuilt only when skills change. |
| Observability | `T1`, `T8`, `T10`, `T11`, `T16` | integration | Manifest fields, calibration fields, stop reasons, metrics by skill and tier. |
| Security and privacy | `T12`, `T17` | integration, manual | No chain-of-thought, secrets, credentials, private keys, or sensitive operational details in records. |
| Performance expectations | `T20` | manual, smoke | Bounded evidence and cost-multiplier assumptions remain visible without broad reads. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T1`, `T3`, `T4`, `T9` | Standard-risk clean code review advances only with L1, blind-first receipts, and clean receipt. |
| `E2` | `T1`, `T2` | Same-context or unverifiable context is L0 and cannot advance. |
| `E3` | `T3`, `T4` | Validation results and evidence menu withheld until risk map receipt exists. |
| `E4` | `T5` | Rereview hides prior finding content until after blind-first pass and may report new findings. |
| `E5` | `T10` | Second-review material finding stops automatic continuation and routes to authorized resolution path. |
| `E6` | `T7`, `T17` | Irreversible external action requires human authority. |
| `E7` | `T9` | Clean receipt with only passing tests is invalid and produces inconclusive outcome. |
| `E8` | `T8` | `code-review changes-requested` routes to `review-resolution` only under active profile authority and valid evidence. |
| `E9` | `T8` | Unclassified code-review finding pauses with correction-loop stop reason. |
| `E10` | `T8`, `T15` | `spec-review changes-requested` without routing authority pauses for explicit user action. |

## Edge case coverage

- `EC1`: Same-model review with verifiably fresh packet can satisfy L1: `T1`, `T2`.
- `EC2`: Different-model review with biased packet fails independence: `T2`.
- `EC3`: Prior rounds may be known as workflow facts, but finding content is deferred: `T5`.
- `EC4`: New rereview issue is recorded and may pause automation: `T5`, `T8`.
- `EC5`: Reviewer can record a supported finding while clean handoff remains unavailable: `T3`, `T8`, `T9`.
- `EC6`: Second reviewer inconclusive stops continuation: `T10`.
- `EC7`: Ambiguous elevated-risk trigger escalates or becomes inconclusive: `T7`.
- `EC8`: Critical internal security change uses L3 when policy allows non-human L3: `T7`, `T17`.
- `EC9`: Publication path requires human authority: `T17`.
- `EC10`: Tests-only clean receipt is invalid: `T9`.

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| `M1` Review gate evidence model and validators | `T1`, `T2`, `T3`, `T9`, `T11`, `T12`, `T19` | Manifest, initial packet, phase receipts, clean receipt, calibration record, and record safety. |
| `M2` Orchestration semantics and workflow-state gates | `T7`, `T8`, `T10`, `T13`, `T16`, `T19` | Gate outcome, risk tier, routing, second-review disagreement, final holistic review, lifecycle state. |
| `M3` Code-review pilot and review-family guidance | `T5`, `T6`, `T14`, `T15`, `T18` | Skill guidance, code-review pilot, manifest-only earlier stages, direct review compatibility, adapter proof. |
| `M4` Calibration fixtures and measurement evidence | `T10`, `T11`, `T12`, `T19` | Sampling floors, calibration metrics, fixture privacy, behavior preservation. |
| `M5` Generated guidance, docs alignment, and final proof | `T13`, `T14`, `T15`, `T18`, `T19`, `T20` | Final holistic review proof, generated skills/adapters, selected validation, behavior-preservation evidence. |

## Test cases

### T1. Independence manifest validates L1/L2/L3 and rejects L0 handoff

- Covers: `R1`-`R3d`, `R11`, `R17`, `AC1`, `AC2`, `E1`, `E2`, `EC1`
- Level: integration
- Fixture/setup:
  - Add review artifact and change-metadata fixtures under `tests/fixtures/review-artifacts/` and `tests/fixtures/change-metadata/`.
  - Use `scripts/review_artifact_validation.py` and `scripts/change_metadata_semantics.py`.
- Steps:
  - Create valid automated review fixtures for standard `L1`, elevated `L2`, and critical internal `L3`.
  - Assert each valid manifest records required fields from `R3b`, uses orchestrator-owned schema-bounded process evidence, and validates when the tier requirement is satisfied.
  - Create invalid fixtures with `L0`, identical `author_context_id` and `reviewer_context_id`, missing context separation mechanism, unsupported independence level, unsupported native review status, and missing reviewer context identity on an unverifiable platform.
  - Assert invalid fixtures cannot produce `review_gate_outcome: advance`.
- Expected result:
  - Valid L1/L2/L3 manifests pass, and L0 or unverifiable author-continuation fixtures fail closed.
- Failure proves:
  - Automated review handoff can advance without structural independence evidence.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure <fixture-root>`

### T2. Initial packet inventory and prohibited initial context are enforced

- Covers: `R1b`-`R5a`, `R17`, `AC2`-`AC4`, `E2`, `EC2`
- Level: integration
- Fixture/setup:
  - Fixtures with initial packet inventories, artifact paths, revisions, content hashes, `prompt_template_version`, and aggregate packet hashes.
  - Negative fixtures containing author self-assessment, desired outcome, prior finding content, validation-result summaries, evidence menu, auto-fix budget, or implementation safety narrative in the initial packet.
- Steps:
  - Validate a clean initial packet with tracked artifact paths, revisions, hashes, prompt template version, and aggregate hash.
  - Assert `author_context_excluded: true` alone is insufficient without inventory and hash evidence.
  - Assert missing inventory, missing aggregate hash, hash mismatch, or prohibited initial packet fields make handoff ineligible.
  - Assert different-model review still fails when the initial packet is biased or author-contaminated.
- Expected result:
  - Only verifiable, neutral initial packets pass; biased or merely attested packets fail closed.
- Failure proves:
  - The review context can be anchored by author claims or pass/fail evidence before independent risk formation.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-change-metadata-validator.py`

### T3. Phase receipts enforce blind-first evidence order

- Covers: `R5`-`R7a`, `AC4`, `AC5`, `E3`
- Level: integration
- Fixture/setup:
  - Review artifact fixtures with ordered phase receipts: `risk-map-recorded`, `evidence-menu-released`, `evidence-results-released`, `prior-findings-released`, and `verdict-recorded`.
  - Negative fixtures with missing receipts, repeated receipts, and evidence releases before risk-map recording.
- Steps:
  - Assert a valid automated review records phase receipts in the required order.
  - Assert validation-result summaries, evidence menu, implementation notes, and prior finding content cannot be released before the `risk-map-recorded` receipt.
  - Assert validation result content is released only after evidence request or evidence-challenge phase.
  - Assert missing or inconsistent phase receipts make the review ineligible for automatic handoff.
- Expected result:
  - Phase receipt order is structural and fail-closed.
- Failure proves:
  - Automation can claim blind-first review while releasing anchoring evidence too early.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T4. Risk map records risk classes and falsifiable hypotheses

- Covers: `R6`-`R6d`, `E1`, `E3`
- Level: integration
- Fixture/setup:
  - Clean and finding review fixtures with risk maps.
  - Negative fixtures missing affected behavior, highest-impact failure modes, changed boundaries, evidence expected, direct-inspection areas, out-of-scope areas, risk-class applicability, or falsifiable questions.
- Steps:
  - Validate a risk map that records all `R6b` fields, applicable and non-applicable risk classes, and falsifiable questions for applicable classes.
  - Assert a clean review cannot advance when the risk map lacks material risk coverage or records only generic boilerplate.
- Expected result:
  - Automated review records independent adversarial orientation before evidence challenge.
- Failure proves:
  - Review can degrade into format checking or "tests passed" approval without falsification intent.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`

### T5. Rereview defers prior findings and preserves new-finding discovery

- Covers: `R8`-`R8d`, `R19a`, `AC5`, `E4`, `EC3`, `EC4`
- Level: integration
- Fixture/setup:
  - Prior finding and rereview fixtures with phase receipts and reconciliation records.
  - Skill-validator assertions for rereview guidance in `skills/code-review/SKILL.md` and minimal manifest language for `skills/spec-review/SKILL.md` and `skills/plan-review/SKILL.md`.
- Steps:
  - Assert prior finding content is absent until after blind-first pass and `prior-findings-released`.
  - Assert rereview may record `new-finding` before reconciliation.
  - Assert reconciliation accepts exactly `resolved`, `still-present`, `failed-remediation`, `reopened`, `superseded`, and `new-finding`.
  - Assert `failed-remediation` is required when a claimed fix is rediscovered during blind-first review.
- Expected result:
  - Rereview remains a full independent pass and records both old and new defects accurately.
- Failure proves:
  - Later review rounds can collapse into fix-confirmation-only checks.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-skill-validator.py`

### T6. Reviewer verdict remains separate from orchestrator continuation and auto-fix classification

- Covers: `R9`-`R9e`, `R20a`, `R20b`
- Level: integration, manual
- Fixture/setup:
  - Code-review finding fixtures with native verdicts, auto-fix classification records, and orchestrator routing records.
  - Canonical review and workflow skills.
- Steps:
  - Assert review records own finding discovery, severity, evidence, required outcome, native result, verdict, and confidence.
  - Assert orchestrator records own continuation, round-limit, profile state, next-stage invocation, manifest ownership, risk-tier classification, and normalized outcome.
  - Assert auto-fix classification appears only after finding and verdict recording.
  - Assert skill guidance does not tell reviewers to suppress findings to preserve autoprogression.
- Expected result:
  - Verdict discovery is independent from routing and fixability.
- Failure proves:
  - Reviewers can optimize judgment around correction-loop convenience.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`

### T7. Risk-tier classifier is deterministic, orchestrator-owned, and fail-closed

- Covers: `R2`, `R10`-`R11`, `AC8`, `E6`, `EC7`, `EC8`
- Level: integration
- Fixture/setup:
  - Artifact-lifecycle fixtures with affected paths and changed-surface metadata for standard, elevated, critical internal, and irreversible external action triggers.
  - Ambiguous trigger fixtures and missing-evidence fixtures.
- Steps:
  - Assert standard-risk changes require L1, elevated-risk triggers require L2, critical internal triggers require L3, and irreversible external actions require human authority.
  - Assert public API, workflow/validator, generated-output machinery, compatibility/migration, security, release packaging, auth, state, concurrency, and multi-component triggers classify elevated when present.
  - Assert privilege boundary, high-impact security change, destructive migration, and critical review/release policy classify critical internal.
  - Assert deploy, publish, credential/secret handling, privileged remote mutation, and irreversible external migration require human authority.
  - Assert ambiguous matches use the higher plausible tier or produce inconclusive when the higher tier cannot be satisfied.
- Expected result:
  - Risk tier cannot be under-classified by author assertion or missing evidence.
- Failure proves:
  - High-risk review can receive a lower independence or authority requirement.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`

### T8. Gate outcome mapping and stop routing preserve reviewer verdicts

- Covers: `R12`-`R12h`, `R12f1`-`R12f5`, `AC6`, `AC7`, `AC-RAI-018`, `RAI-021`-`RAI-023`, `E8`, `E9`, `E10`
- Level: integration
- Fixture/setup:
  - Artifact-lifecycle fixtures for native `approved`, `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive`.
  - Active and inactive profile fixtures for `implementation-through-verify`.
  - Findings with valid and invalid `auto_fix_class`.
- Steps:
  - Assert native `approved` and `clean-with-notes` map to `advance` only when independence, evidence, recording, clean receipt, and escalation gates pass.
  - Assert native `changes-requested` maps to `stop`.
  - Assert `stop` routes to `review-resolution` only with active profile authorization, valid independence manifest, required phase/sufficiency evidence, and correction-loop budget.
  - Assert `auto_fix_class: none` pauses with profile-specific stop reason such as `correction-finding-unclassified`.
  - Assert unroutable stages pause with `changes-requested-not-routable`.
  - Assert native `blocked` and `inconclusive` pause regardless of profile authorization.
  - Assert any review-resolution route records authorizing profile, round number, and independence evidence without modifying the reviewer's verdict.
- Expected result:
  - Orchestration consumes normalized outcomes and preserves review-stage ownership.
- Failure proves:
  - `stop` can be misread as uniform pause or allowed to bypass profile/evidence gates.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths <paths>`

### T9. Clean-review sufficiency receipt is complete and not replaced by passing validation

- Covers: `R13`-`R13c`, `AC12`, `E1`, `E7`, `EC5`, `EC10`
- Level: integration
- Fixture/setup:
  - Clean automated review fixtures with sufficiency receipts.
  - Negative fixtures that cite only passing tests or omit risk classes, hypotheses, direct proof, validation challenge, unreviewed surfaces, or no-finding rationale.
- Steps:
  - Assert valid clean receipts include target identity, independence level, inspected governing artifacts, risk classes, adversarial hypotheses, direct proof or reproduction, validation evidence challenge, unreviewed surfaces, confidence, and no-finding rationale.
  - Assert passing validation alone does not satisfy the clean receipt.
  - Assert materially incomplete clean receipts produce `review_gate_outcome: inconclusive`.
- Expected result:
  - Clean reviews remain valid only when backed by affirmative adversarial evidence.
- Failure proves:
  - "Tests passed" can substitute for independent review.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`

### T10. Second-review sampling, disagreement, and escalation gate automatic continuation

- Covers: `R14`-`R15b`, `AC9`-`AC11`, `E5`, `EC6`
- Level: integration, manual
- Fixture/setup:
  - Lifecycle fixtures with rollout sample counts, standard-risk clean review totals, elevated-risk clean reviews, critical-risk reviews, and second-review outcomes.
  - Calibration records for second-review material finding, `blocked`, and `inconclusive`.
- Steps:
  - Assert rollout standard-risk clean reviews fail when sample rate is below 20%.
  - Assert standard-risk sampling rate cannot reduce before at least 10 independently reviewed clean outcomes.
  - Assert elevated-risk clean reviews require second review at 100%.
  - Assert critical-risk reviews satisfy L3 or human authority gate.
  - Assert second-review material finding, `blocked`, or `inconclusive` prevents automatic continuation.
  - Assert first review cannot overrule disagreement and majority-vote approval is not used.
  - Manually review steady-state sampling controls for disagreement confidence interval and rate-increase triggers.
- Expected result:
  - Clean-review sampling and disagreement are enforceable handoff gates.
- Failure proves:
  - Calibration can become optional or cost-reduced before evidence supports it.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`

### T11. Calibration records distinguish fixture mode, disagreement, escapes, and metrics by skill and tier

- Covers: `R15`-`R16d`, `AC14`
- Level: integration, manual
- Fixture/setup:
  - Public seeded defect-class fixtures under `tests/fixtures/review-artifacts/`.
  - Calibration record fixtures with recurrence-detection, novel-defect detection, disagreement, downstream escape, false-positive, inconclusive, receipt-quality, and duration fields.
- Steps:
  - Assert public fixtures document defect classes without claiming to be the full private corpus.
  - Assert calibration records distinguish recurrence-detection from novel-defect detection.
  - Assert records include second-review disagreement, downstream escape, false-positive rate, inconclusive rate, receipt quality, review duration, review skill, and risk tier.
  - Manually verify private or access-controlled rotating fixture guidance is preserved when practical.
- Expected result:
  - Calibration evidence is measurable without overfitting public fixtures or aggregating away skill/tier differences.
- Failure proves:
  - Seeded-defect recall can be gamed or metrics can hide high-risk review failures.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/test-artifact-lifecycle-validator.py`

### T12. Manifests and records reject private reasoning and unsafe free-form fields

- Covers: `R3c`, `R3d`, `R17`-`R17c`, Security/privacy
- Level: integration, manual
- Fixture/setup:
  - Valid records using closed vocabulary fields, stable identifiers, paths, hashes, check IDs, and evidence references.
  - Invalid records with private chain-of-thought labels, hidden reasoning labels, secrets, credentials, private keys, unbounded manifest prose, or evidence-free assertions.
- Steps:
  - Assert validators reject forbidden private-reasoning fields and unbounded free-form manifest fields.
  - Assert records prefer structural references over narrative process claims.
  - Manually audit sampled valid records for excessive narrative and private reasoning leakage where structural validation is insufficient.
- Expected result:
  - Review evidence is auditable without preserving private reasoning or sensitive information.
- Failure proves:
  - The independence evidence surface can leak private reasoning or become prose ceremony.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - Manual calibration audit checklist.

### T13. Final holistic code review blocks explain-change and verify when missing or milestone-local only

- Covers: `R18`-`R18b`, `AC13`
- Level: integration
- Fixture/setup:
  - Lifecycle fixtures with implementation milestones, local code-review receipts, final holistic code-review receipts, explain-change readiness, verify readiness, generated output changes, and review resolutions.
- Steps:
  - Assert automated transition to `explain-change` or `verify` fails when no final holistic code review exists.
  - Assert a final review that covers only the last milestone fails.
  - Assert a valid final holistic review records complete final diff, cross-milestone interactions, proposal/spec/test-spec/architecture/plan, review resolutions, final validation selection, generated or derived artifacts, and cross-milestone scope.
- Expected result:
  - Final implementation closeout cannot rely on only milestone-local review.
- Failure proves:
  - Cross-milestone or generated-output defects can escape into explain-change or verify.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`

### T14. Code-review pilot and review-family guidance match Phase 1 scope

- Covers: `R19`-`R19b`, `R20`, `AC12`, `AC13`, `AC15`
- Level: integration, manual
- Fixture/setup:
  - Canonical skill files: `skills/code-review/SKILL.md`, `skills/spec-review/SKILL.md`, `skills/plan-review/SKILL.md`, `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, `skills/review-resolution/SKILL.md`, and `skills/architecture-review/SKILL.md` when touched.
- Steps:
  - Assert `code-review` contains the full pilot guidance for initial packet, risk map, evidence challenge, prior-finding reconciliation, clean sufficiency receipt, and final holistic review.
  - Assert automated `spec-review` and `plan-review` guidance records at least review invocation manifests during Phase 1 without requiring the full blind-first protocol.
  - Assert skill text preserves direct isolated review behavior and does not let reviewers edit the reviewed target.
  - Assert no finding quota is introduced.
- Expected result:
  - Phase 1 migrates code-review fully while collecting manifest evidence for earlier review stages.
- Failure proves:
  - The first-slice rollout either over-migrates review skills or fails to protect the code-review surface.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`

### T15. Manual and profile-off review behavior remains compatible

- Covers: `R20`-`R20d`, `AC15`, `E10`
- Level: integration, manual
- Fixture/setup:
  - Direct isolated review fixtures and profile-off lifecycle fixtures.
  - Canonical review skill guidance.
- Steps:
  - Assert direct isolated review invocations remain isolated by default.
  - Assert profile-off review behavior does not require automated-review manifests unless used as automated handoff evidence.
  - Assert no review path requires every review to produce a finding.
  - Assert no metric or guidance introduces finding-count quota, average finding target, or percentage-failed target.
- Expected result:
  - Existing manual and profile-off workflows stay compatible.
- Failure proves:
  - The automated gate contract leaks into direct manual review or incentivizes false findings.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-skill-validator.py`

### T16. Stop reasons and observability fields are distinct and reviewable

- Covers: Inputs and outputs, Observability, `R12`, `R14`, `R16`
- Level: integration
- Fixture/setup:
  - Lifecycle and review artifact fixtures for invalid manifest, missing evidence, insufficient clean receipt, risk escalation failure, second-review disagreement, human-authority failure, and unroutable changes-requested.
- Steps:
  - Assert stop reasons distinguish independence failure, invalid manifest, missing initial packet, missing phase receipt, insufficient clean receipt, risk-tier escalation failure, second-review disagreement, human-authority requirement, and unroutable changes-requested.
  - Assert manifests expose independence level, context IDs, separation mechanism, risk tier, initial-packet hash, phase receipts, native result, and gate outcome.
  - Assert calibration records expose sample rate, second reviewer type, independence level, material disagreements, severity disagreements, evidence gaps, escapes, and fixture mode.
- Expected result:
  - Operators can determine why automation stopped without reading private reasoning.
- Failure proves:
  - Stop conditions collapse into vague pauses or unverifiable clean handoffs.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - `python scripts/test-review-artifact-validator.py`

### T17. Critical external actions require human authority and protect secrets

- Covers: `R2`, `R11`, `R14d`, Security/privacy, `E6`, `EC8`, `EC9`
- Level: integration, manual
- Fixture/setup:
  - Fixtures declaring publication, deployment, credential/secret handling, privileged remote mutation, or irreversible external migration.
  - Human authority record fixtures with decision identity or role but no sensitive details.
- Steps:
  - Assert irreversible external action fixtures cannot advance with L3 heterogeneous LLM review alone.
  - Assert human authority is required before automated clean-review handoff can support an irreversible external action.
  - Assert human authority records avoid secrets, credentials, private keys, and sensitive operational detail.
  - Assert critical internal non-external changes may use configured L3 heterogeneous or human review according to policy.
- Expected result:
  - External irreversible actions preserve a human authority boundary.
- Failure proves:
  - Automation can approve publication, deployment, or secret-handling changes without required authority.
- Automation location:
  - `python scripts/test-artifact-lifecycle-validator.py`
  - Manual security/privacy review.

### T18. Canonical skill changes prove both local skill output and public adapter archives

- Covers: `R19`, Compatibility and migration, `PR1-F1`
- Level: integration, smoke
- Fixture/setup:
  - Canonical `skills/` changes from M3 and M5.
  - Current adapter manifest version from `dist/adapters/manifest.yaml`.
  - Temporary output directory for adapter archives.
- Steps:
  - Run local skill validation and generated local skill drift checks.
  - Build temporary public adapter archives from canonical skills.
  - Validate the temporary adapter archive root with the same manifest version.
  - Assert no generated public adapter package output is hand-edited or tracked as source for v0.1.3+ behavior.
- Expected result:
  - Canonical skill updates remain valid for both local runtime output and public adapter archives.
- Failure proves:
  - Skill guidance can pass local validation while breaking Codex, Claude, or opencode public adapter archives.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-build-skills.py`
  - `python scripts/build-skills.py --check`
  - `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`

### T19. Change metadata, review artifacts, and lifecycle state stay synchronized

- Covers: Inputs and outputs, `R3`, `R4`, `R7`, `R12`, `R17`, M1-M5 closeout
- Level: integration
- Fixture/setup:
  - The change root `docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/`.
  - Active plan, plan index, proposal, spec, test spec, architecture, ADR, review log, review resolution, and review records.
- Steps:
  - Validate review artifact structure and closeout.
  - Validate change metadata for artifact pointers, review summaries, validation ledger, and changed files.
  - Validate artifact lifecycle over explicit paths including the test spec after authoring.
  - Assert active plan and `docs/plan.md` current next-stage projections remain synchronized before downstream implementation handoff.
- Expected result:
  - Lifecycle evidence remains coherent as the change moves from test-spec to implementation.
- Failure proves:
  - Downstream implementation could rely on stale or contradictory artifact state.
- Automation location:
  - `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-25-independent-adversarial-review-gates-for-automated-workflows.md --path specs/review-independence-and-criticality.md --path specs/review-independence-and-criticality.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260625-independent-adversarial-review-gates.md --path docs/plans/2026-06-25-independent-adversarial-review-gates.md --path docs/plan.md --path docs/changes/2026-06-25-independent-adversarial-review-gates-for-automated-workflows/change.yaml`

### T20. Bounded evidence and review-cost expectations remain visible

- Covers: Performance expectations, Testing strategy, `R15`
- Level: manual, smoke
- Fixture/setup:
  - Review skill guidance, workflow docs, and calibration records touched by M3-M5.
- Steps:
  - Confirm review guidance uses bounded evidence packets and targeted review surfaces instead of broad repository reads without risk justification.
  - Confirm rollout documentation or behavior-preservation evidence preserves the expected 2-3x review-cost assumption for sampled standard-risk clean reviews.
  - Confirm steady-state sampling reduction remains tied to rollout floor and disagreement confidence criteria rather than a fixed unreviewed cost cut.
- Expected result:
  - The implementation preserves the proposal's cost realism and evidence-bounding constraints.
- Failure proves:
  - Review independence becomes too expensive to operate or reverts to shallow evidence because cost is hidden.
- Automation location:
  - Manual review during M3-M5.
  - `python scripts/test-skill-validator.py` for stable bounded-evidence guidance when canonical skill text changes.

## Fixtures and data

- Review artifact fixtures under `tests/fixtures/review-artifacts/`:
  - valid and invalid independence manifests;
  - valid and invalid initial packet inventories and hashes;
  - phase receipt order fixtures;
  - clean-review sufficiency receipts;
  - prior-finding reconciliation fixtures;
  - calibration and second-review records;
  - private-reasoning and unbounded-field rejection fixtures.
- Change metadata fixtures under `tests/fixtures/change-metadata/`:
  - valid automated review gate evidence summaries;
  - invalid missing manifest, missing packet hash, mismatched review counts, and unsafe evidence references.
- Artifact lifecycle fixtures under `tests/fixtures/artifact-lifecycle/`:
  - risk-tier routing;
  - native result to `review_gate_outcome` mapping;
  - `changes-requested` routable and unroutable paths;
  - blocked/inconclusive pause;
  - final holistic review precondition.
- Skill validator fixtures under `tests/fixtures/skills/` only when a stable skill contract assertion needs positive or negative fixture coverage.
- Temporary adapter archive output directories created with `mktemp -d`; generated public adapter archives are not committed.

## Mocking/stubbing policy

- Do not mock parser or validator exit behavior for `review_artifact_validation.py`, `change_metadata_semantics.py`, `artifact_lifecycle_validation.py`, `validate-review-artifacts.py`, `validate-change-metadata.py`, or `validate-artifact-lifecycle.py` when testing contract behavior.
- Do not mock `build-adapters.py` or `validate-adapters.py` for final generated adapter proof; use a temporary output directory.
- Unit tests may construct synthetic fixture files, manifests, phase receipts, and change metadata records to isolate parser behavior.
- Manual tests may inspect policy wording, but they must not replace executable coverage for any structurally testable `MUST`.
- Private or access-controlled calibration fixture instances are not required to be committed; public fixtures document defect classes and validator behavior.

## Migration or compatibility tests

- `T15` proves direct isolated and profile-off review behavior remains compatible.
- `T8` proves existing authorized `code-review changes-requested -> review-resolution` routing remains available when active profile and evidence gates pass.
- `T14` proves Phase 1 does not force the full blind-first protocol onto `spec-review` and `plan-review`, while still recording manifest evidence.
- `T18` proves public adapter release-archive validation remains compatible with v0.1.3+ generated-output policy.
- `T19` proves lifecycle state remains synchronized when the test spec becomes active and implementation begins.

## Observability verification

- `T1`, `T8`, `T10`, `T11`, and `T16` verify observable process fields: independence level, context IDs, separation mechanism, risk tier, packet hash, phase receipts, native result, gate outcome, sample rate, second reviewer type, material disagreement, evidence gaps, escapes, fixture mode, and stop reason.
- Stop reasons must distinguish independent-review context failure, invalid manifest, missing initial packet, missing evidence, insufficient clean receipt, risk escalation failure, second-review disagreement, human authority requirement, unroutable `changes-requested`, and correction-loop finding classification failure.

## Security/privacy verification

- `T12` verifies manifests and records reject private chain-of-thought, hidden reasoning, secrets, credentials, private keys, unbounded free-form process fields, and evidence-free assertions where structurally detectable.
- `T17` verifies human authority records for irreversible external actions record role or decision identity without exposing credentials or sensitive operational details.
- Calibration fixture guidance keeps private or access-controlled rotating fixtures out of broad public disclosure when used to measure novel-defect detection.

## Performance checks

- `T20` manually verifies bounded evidence and rollout cost expectations.
- Fixture-backed validators should use targeted path sets and explicit fixture roots; they should not require broad repository reads for ordinary test runs.
- Adapter archive proof uses temporary generated output and should run only when canonical `skills/` changes or final generated proof requires it.

## Manual QA checklist

- Confirm every `MUST` requirement has at least one automated or explicit manual proof row in the requirement coverage map.
- Confirm examples E1-E10 and edge cases EC1-EC10 are covered.
- Confirm no test asserts a finding quota or rewards finding count.
- Confirm clean review tests require affirmative evidence, not merely passing validation.
- Confirm implementation does not add a hosted service, database, or persistent external control plane.
- Confirm generated public adapter archives are built and validated in temporary output when canonical skills change.

## What not to test and why

- Do not test semantic review quality with an automated scoring model; that is a separate proposal and not part of this first slice.
- Do not require exact wording for seeded defects; calibration should detect intended defect classes.
- Do not require public disclosure of private rotating calibration fixtures.
- Do not test different model vendors as mandatory for standard-risk review; the spec treats model diversity as a risk-tier control.
- Do not test real deployment, publication, secret rotation, or privileged remote mutation. Use declared-action fixtures and human-authority record validation unless a later approved release or deployment workflow requires a real external action.
- Do not add tests that require every review to produce a finding.

## Uncovered gaps

None. Sampling confidence interval thresholds, private fixture custody, and heterogeneous/human reviewer selection details remain policy surfaces for later proposals, but this test spec covers the first-slice contract in the approved spec and plan.

## Next artifacts

- `implement` M1 after this test spec is recorded and lifecycle state is synchronized.

## Follow-on artifacts

None yet.

## Readiness

This active test spec is the proof-planning surface for the linked execution plan and its implementation milestones.
