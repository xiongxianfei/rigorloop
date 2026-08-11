# Test-Spec Revision Evidence R1

Stage: test-spec
Artifact: `specs/code-review-skill-simplification.test.md`
Date: 2026-08-10
Prior review: `test-spec-review-r1`

The revision accepts and addresses `CRSIM-TSR1` through `CRSIM-TSR4` without changing approved feature behavior:

- CMD1 now routes valid and invalid ledger records through one fail-closed function and proves that `unknown-disposition` precedes field and destination consistency checks.
- CMD10 and CMD11 own exact baseline and final measurements for common-path size, conditional-reference size, total package size, duplication clusters, inline templates, and mapped resources; T11, PRF-012, M1, and M3 cite them.
- Every test case now uses the closed test-case level vocabulary, while contract and migration remain coverage-map classifications. MP1 now names rationale, owner, stage, environment, evidence, pass, failure, rerun, and exact-step fields.
- CMD6 now uses `subprocess.run(..., check=True)` inside `tempfile.TemporaryDirectory`, so generation and validation fail fast and temporary output is cleaned on success or failure.
- MP1 is final-M3 proof only; preimplementation, M1, and M2 no longer require evidence that cannot exist yet. CMD11 reports a cluster as duplicated after the change unless it resolves to exactly one destination owner.

The revision retains deterministic fixtures, existing repository validators and package owners, independent semantic review, and the prohibition on target-agent runtime execution.

Ready for `test-spec-review-r2`.
