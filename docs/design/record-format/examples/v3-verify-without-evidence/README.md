# Proposed v3 Verify without proof references

[verify-report.json](verify-report.json) is a complete proposed v3 Verify record under [RF-SR-05/07/09](../../record-format.md#requirements). It contains the required explanation fields and the success-only outcome, but its evidence_refs and review_refs arrays are empty. No verification_basis object is needed for the illustrated non-Git scope.

This is a deliberate contrast between a structurally recordable success assertion and justified completion. The record provides no actual successful checks or independent assessments; neither its outcome nor its populated explanation can establish readiness. The subject identity and actor are synthetic, and the containing store is omitted.

The proposed contract permits structurally valid but inadequately supported claims to remain recordable so actors can correct them. Responsible Verify policy still prohibits claiming successful closeout without its required basis. This example is Design material, not an executed assessment; validation cannot establish adequate evidence.
