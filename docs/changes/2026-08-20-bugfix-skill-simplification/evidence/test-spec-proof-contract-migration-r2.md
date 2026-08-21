# Test-Spec Proof-Contract Migration R2

- Stage: workflow
- Operation: governed proof-contract migration
- Reason: the active test specification has implementation reliance but T14 and its source identities encode the superseded strict-reduction contract
- Preserved identity: artifact ID `test-spec` at `specs/bugfix-skill-simplification.test.md`
- Authorized revision: update only governing identities and proof obligations affected by truth-first metric acceptance
- Preserved reliance: M1 evidence and M2 implementation/review history remain valid; no completed proof is reinterpreted as proving the revised T14 outcome
- Required fresh gate: independent `test-spec-review-r2` before implementation resumes
- State ownership: workflow authorizes the reopen; `test-spec` owns content and authoring transition; `test-spec-review` owns settlement
