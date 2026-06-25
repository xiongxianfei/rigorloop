# Behavior Preservation Evidence

Change ID: 2026-06-25-independent-adversarial-review-gates-for-automated-workflows
Milestone: M4. Calibration fixtures and measurement evidence
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
| Downstream escape evidence | Escapes are review-calibration inputs. | Calibration records with `Downstream escape: yes` must include escape stage and analysis fields. | strengthened |

## M4 notes

The M4 public fixture is intentionally a defect-class and record-shape example. It is not the measured seeded-defect corpus and must not be used as evidence that seeded-defect recall is calibrated.

M4 keeps review quality measurement separated from finding count. The measured fields are recurrence detection, novel-defect detection, second-review disagreement, downstream escape, false-positive rate, inconclusive rate, receipt quality, review duration, review skill, and risk tier.
