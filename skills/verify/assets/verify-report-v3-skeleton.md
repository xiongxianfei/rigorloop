# Verify report: <change title>

> Inactive until the `stage-owned-change-local-v3` final-verification contract is activated.

## Result payload

```json final-verification-v3
{
  "protocol_version": 3,
  "outcome": "<pending | successful | failed | inconclusive | interrupted | stale>",
  "basis": "<fill normalized repository, subject, review, Design, Delivery, and final-diff identities>",
  "basis_status": "<classify each required authority>",
  "impact": "<one entry per relevant surface>",
  "evidence": "<one applicability entry per required obligation>",
  "always_current": "<the complete mandatory check set>",
  "ci_status": "<passed | failed | pending | unavailable | not-required>",
  "blockers": "<list>",
  "residual_risks": "<list>",
  "branch_ready": "<true only for a complete registered success>",
  "explanation": "<complete successful explanation object, otherwise null>"
}
```
