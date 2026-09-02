# M6 immutable-v2 lifecycle recording and dual read-back

Change ID: 2026-08-31-simplify-final-verification-retire-explain-change
Reviewed product subject: 9c364d6162a32a03ac63d81093e728fd0e41b0bc
Workflow Verify handoff subject: f3f1f440205e61be8da525b1fd7fe7e174db2604
Final review: code-review-final-r1 plus targeted PR-preflight rereviews through code-review-pr-preflight-r8
Explanation handoff: f3f1f440205e61be8da525b1fd7fe7e174db2604
Verify report: docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/verify-report.md
Lifecycle revision: sha256:ea70df83a1cce993a7f537c2f9fdeaf61b609d7dec445754d3574d7d564c3d35

## Bound runtime

- Source revision: `585c2beecea0ddda0ae11ed8f0b1a53b24310052`.
- Deterministic Git archive SHA-256: `d12bca65240cd19f71f2d438a736fb89e6d9504e51b1e8e1a488c1f97c78465c`; matched.
- Archived explain-change skill SHA-256: `912b3941bfc8e8077fb3fe416869ea530657423eec423bc85235213d9887110f`; matched.
- Archived Verify skill SHA-256: `7acc2efd8a91408b5e3c2cb77f8f56447af095b14c9ee8cd8a2ebae5dfcfa6ce`; matched.
- Archived lifecycle CLI SHA-256: `0faba4bfc7478c3575b560e2067794a25a4587039a3d31ab8b179ab16e557c7a`; matched.
- Execution location: fresh temporary `git archive` extraction with the repository's already-installed Node dependencies linked only for runtime dependency resolution; canonical source files were not replaced.

## Lifecycle mutation

- Operation: `record-validation`.
- Request: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/requests/record-m6-v2-verification.json`.
- Artifact: registered primary plan at SHA-256 `5bdf89552ab9a0f88988c62f5d9ae57dae8e12a184d18bb678fc73254fa81514`.
- Evidence: current `verify-report.md`, recording `Validation result: branch-ready` for the immutable reviewed subject.
- Prior lifecycle revision: `sha256:d5ce50a092eeef98c25e663969811d227cafb2fbe3c046f065d7846608608503`.
- CLI operation result: `success`, mutation status `recorded`.
- Immediate and final resulting lifecycle revision: `sha256:ea70df83a1cce993a7f537c2f9fdeaf61b609d7dec445754d3574d7d564c3d35`.

## Archived-v2 read-back

- Status: `success`.
- Contract: `stage-owned-change-local-v2`, activation `active`, authority `active` under the bound preactivation runtime.
- Current stage: `verify`; active milestone: `M6`.
- Unresolved findings: none; stale evidence: none; blockers: none.
- Permitted operations: `route-correction`, `record-validation`.
- Observed lifecycle revision: `sha256:ea70df83a1cce993a7f537c2f9fdeaf61b609d7dec445754d3574d7d564c3d35`.

## Current-runtime read-back

- Status: `success`.
- Contract: `stage-owned-change-local-v2`, activation `historical`, authority `historical` under the staged v3 candidate runtime.
- Current stage: `verify`; active milestone: `M6`.
- Unresolved findings: none; stale evidence: none; blockers: none.
- Permitted operations: none, as required for historical v2 state under the candidate runtime.
- Observed lifecycle revision: `sha256:ea70df83a1cce993a7f537c2f9fdeaf61b609d7dec445754d3574d7d564c3d35`.

## Interpretation

Both readers agree on the exact serialized lifecycle revision, current stage, active milestone, absence of findings, absence of stale evidence, and absence of blockers. Their authority projections differ intentionally: the bound v2 runtime supplies this change's preactivation closeout authority, while the current candidate treats the same record as readable history with no progression authority. Four PR-preflight fixture findings were routed, corrected, rereviewed, and returned before the refreshed 28-check PR gate and final validation registration. No activation, publication, release, tag, migration, or historical artifact mutation occurred.
