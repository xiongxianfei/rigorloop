# Behavior Preservation Evidence

Change ID: 2026-06-25-independent-adversarial-review-gates-for-automated-workflows
Milestone coverage: M4. Calibration fixtures and measurement evidence; M5. Generated guidance, docs alignment, and final proof
Status: active evidence

## M4 preservation matrix

| Surface | Baseline | M4 proof | Result |
| --- | --- | --- | --- |
| Manual review behavior | Manual and isolated reviews use existing review statuses and records. | Calibration record validation only runs when `Calibration record: yes` or calibration fields are present. Existing non-calibration review records remain outside this new check. | preserved |
| Profile-off review behavior | Profile-off review artifacts may still record ordinary clean receipts or material findings without automated handoff evidence. | Lifecycle sampling gates are evaluated by `evaluate_automated_review_gate_route` for workflow-managed review-gate routing, not by direct isolated review invocation. | preserved |
| No finding quota | Clean reviews remain valid when required sufficiency and calibration evidence is present. | M4 validates sample rates, second-review disagreement, and metric separation; it does not require any minimum finding count. | preserved |
| Public calibration fixtures | Public fixtures document representative defect classes and record shape. | `Fixture corpus scope: defect-class-example-not-measured-corpus` is required for public defect-class fixtures. | strengthened |
| Private measured calibration | The spec allows private or access-controlled rotating fixture instances for measured calibration. | Public fixture validation does not claim the public corpus is complete; private rotating fixture custody remains a calibration responsibility outside committed fixtures. | preserved |
| Sampling floor | Rollout standard-risk clean review sampling had to be policy-enforced. | Lifecycle and review-artifact tests reject standard-risk rollout sample rates below 20% and reject rate reduction before 10 independently reviewed clean outcomes. | strengthened |
| Elevated-risk clean review | Elevated-risk clean reviews require second review. | Lifecycle and review-artifact tests reject elevated-risk clean review records without second-review evidence. | strengthened |
| Critical-risk authority | Critical-risk clean reviews require explicit L3 or human authority according to tier. | Lifecycle routing and calibration fixtures now reject critical-internal records without satisfied L3/human authority and reject irreversible external action records unless human authority is satisfied. | strengthened |
| Calibration control fields | Calibration control values were intended to be closed yes/no fields. | `Sample-rate reduction requested`, `Second review required`, `Automatic continuation`, and `Critical authority satisfied` now reject unsupported values instead of silently treating them as false. | strengthened |
| Parser-order diagnostics | Closed-vocabulary input validation must run before downstream gate derivation and outcome consistency. | T10g, T10g-bis, T10g-ter, T10g-quater, T11g, and direct review probes verify malformed critical-authority fields return field-specific parser stop reasons before generic mismatch symptoms. | strengthened |
| Downstream escape evidence | Escapes are review-calibration inputs. | Calibration records with `Downstream escape: yes` must include escape stage and analysis fields. | strengthened |

## M4 notes

The M4 public fixture is intentionally a defect-class and record-shape example. It is not the measured seeded-defect corpus and must not be used as evidence that seeded-defect recall is calibrated.

M4 keeps review quality measurement separated from finding count. The measured fields are recurrence detection, novel-defect detection, second-review disagreement, downstream escape, false-positive rate, inconclusive rate, receipt quality, review duration, review skill, and risk tier.

Manual reviews and profile-off review behavior remain unaffected by the M4 R1 resolution because the added authority gate is evaluated for critical review-gate/calibration evidence, and the closed yes/no parsing applies only to calibration control fields. Existing standard-risk public calibration fixtures continue to pass with explicit `Critical authority kind: n/a` and `Critical authority satisfied: no`; paired negative fixtures now prove future regressions fail closed.

The fail-closed return shape for critical-authority parse and requirement failures is `profile_state="paused"` with `next_stage=None`. M4 R2 corrected the parser ordering so unsupported authority kinds and non-boolean authority satisfaction values cannot be hidden behind `review-gate-outcome-mismatch-given-gate-state`.

## M5 preservation matrix

| Surface | Baseline | M5 proof | Result |
| --- | --- | --- | --- |
| Contributor workflow guidance | `docs/workflows.md` summarizes workflow-managed standard execution and lifecycle state ownership. | Added the independent adversarial `code-review` gate, clean automated handoff gates, and final holistic review precondition to the Autoprogression section. | strengthened |
| Canonical stage skills | M3 updated canonical `code-review`, `workflow`, `implement`, `spec-review`, and `plan-review` guidance for the Phase 1 pilot. | M5 reruns local skill validation, skill tests, generated local skill drift checks, and public adapter archive validation using the current `dist/adapters/manifest.yaml` version. | preserved |
| Public adapter output | For v0.1.3 and later, generated public adapter skill bodies are release archives, not tracked source. | M5 builds adapter archives into a temporary directory and validates that temporary root; no generated public adapter package output is committed or hand-edited. | preserved |
| Final holistic review gate | Automated implementation flow must not enter `explain-change` or `verify` on a milestone-local review only. | Existing lifecycle tests cover missing final holistic review, milestone-local-only review, and valid final holistic review evidence; M5 records the command rerun before code-review handoff. | strengthened |
| Manual and profile-off review behavior | Direct isolated reviews and profile-off reviews do not require automated-review manifests unless used as automated handoff evidence. | Skill tests and lifecycle routing preserve direct/profile-off compatibility; M5 changes only workflow-managed guidance and proof records. | preserved |
| No finding quota | Review quality is measured through sensitivity, escapes, disagreement, evidence, and calibration quality, not finding count. | Skill tests assert no minimum-finding quota; behavior evidence records that sampling and calibration controls do not require every review to find an issue. | preserved |
| Review cost visibility | The proposal expected higher per-review cost during rollout, especially for sampled standard-risk clean reviews and elevated-risk second reviews. | T20 manual evidence remains visible here: rollout sampling starts at at least 20%, cannot reduce before 10 independently reviewed standard-risk clean outcomes, elevated-risk clean reviews remain second-reviewed at 100%, and standard-risk steady-state reductions stay tied to measured disagreement confidence rather than an unreviewed cost cut. | preserved |
| Bounded evidence | Review stages should start from bounded evidence packets and expand only when needed. | Code-review guidance retains bounded evidence access and direct proof requirements; M5 validation uses selector-selected explicit-path proof before broad smoke. | preserved |

## M5 notes

M5 does not introduce a new runtime service, persistence surface, adapter source tree, or review-family rollout beyond the approved Phase 1 scope. The only contributor-facing workflow edit is a concise summary of behavior already required by the approved spec and canonical stage skills.

Final lifecycle closeout is still not claimed by M5 implementation. The final holistic code review is a required downstream review gate before `explain-change` or `verify`; this M5 evidence records that the precondition is documented and test-covered.
