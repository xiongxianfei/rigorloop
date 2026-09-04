---
schema: compact-verify-v1
verification_id: <verification-id>
subjects:
  <subject-id>:
    subject_id: <subject-id>
    path: <repository-relative-path>
    identity: sha256:<64-lowercase-hex>
verdict: passed
impact: <low|standard|high|critical>
evidence_reused: []
evidence_rerun: []
limitations: []
residual_risks: []
explanation: <what-changed-and-why>
handoff: <ready|ready-with-limitations>
recorded_at: <rfc3339-timestamp>
---

# Verify Report

## Evidence basis

- Reused current evidence: <evidence IDs or None>
- Rerun evidence: <evidence IDs or None>

The front matter is authoritative. External PR, release, or deployment handoff may be described here when applicable but is not required for lifecycle completion.
