---
schema: compact-review-v1
review_id: <review-id>
target:
  target_id: <target-id>
  target_kind: <proposal|design-package|delivery-package|milestone|final-code>
round: <positive-integer>
subjects:
  <subject-id>:
    subject_id: <subject-id>
    path: <repository-relative-path>
    identity: sha256:<64-lowercase-hex>
reviewer_authority: <proposal-review|design-review|delivery-review|code-review>
outcome: <approved|changes-requested|blocked|inconclusive>
recording_status: recorded
open_findings: {}
material_decisions: []
limitations: []
recorded_at: <rfc3339-timestamp>
---

# <review target> Review

## Open findings

<Current findings with stable ID, severity, affected surface, blocking effect, owner, required next action, and disposition; write "None" only for a clean current review.>

The front matter is authoritative. This body may explain the current judgment without duplicating superseded rounds.
