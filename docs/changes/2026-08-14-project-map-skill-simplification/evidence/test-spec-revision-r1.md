# Test-Spec Revision R1 Evidence

- Stage: `test-spec`
- Operation: `revise-primary-test-spec`
- Artifact: `specs/project-map.test.md`
- Revision date: 2026-08-14
- Triggering review: `test-spec-review-r1`
- Triggering finding: `PMAPTSR-PR1`
- Prior reviewed revision: `15aeff1e`
- Prior content identity: `6d9de320e227a098e456d1b3b8331ccd3b3cc1c3c602f24e6fdf8786a27b0178`
- Revised content identity: `0798e6d9e68540037bebd1884ccde2895d168e61388efc891d3ce48dd2b54914`
- Result: `review-required`

The user rejected manual semantic review as a test-spec acceptance obligation and assigned final human judgment to ordinary PR review. The revision removes MP0 and MP1, converts every affected proof obligation to deterministic automated evidence, removes manual proof from milestone gates, and keeps final semantic judgment outside the scripted test procedure.

The revision preserves the approved behavioral requirements, boundary and interaction IDs, test cases, commands, milestones, package-parity coverage, no-target-runtime boundary, and implementation scope. It does not claim PR review has occurred.

Validation target: `test-spec-review-r2`.
