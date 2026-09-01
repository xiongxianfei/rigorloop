# M6 immutable-v2 lifecycle recording and dual read-back

Change ID: 2026-08-31-simplify-final-verification-retire-explain-change
Reviewed product subject: c93e38340170c9c0e336bb6e3e253469ec4380ac
Workflow Verify handoff subject: b81522d8aa806491cca5d92bfd8100939b4fc99c
Final review: code-review-final-r1
Explanation handoff: b81522d8aa806491cca5d92bfd8100939b4fc99c
Verify report: docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/verify-report.md
Lifecycle revision: sha256:917d52d2720b058730f9574e0f9ade02ef540e40479b3b5b4d32024dd1a81489

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
- Prior lifecycle revision: `sha256:11225897cffdd293f71be471b02378b93a2b4631d394371a3b2ac6c8bcc35ad6`.
- CLI operation result: `success`, mutation status `recorded`.
- Immediate and final resulting lifecycle revision: `sha256:917d52d2720b058730f9574e0f9ade02ef540e40479b3b5b4d32024dd1a81489`.

## Archived-v2 read-back

- Status: `success`.
- Contract: `stage-owned-change-local-v2`, activation `active`, authority `active` under the bound preactivation runtime.
- Current stage: `verify`; active milestone: `M6`.
- Unresolved findings: none; stale evidence: none; blockers: none.
- Permitted operations: `route-correction`, `record-validation`.
- Observed lifecycle revision: `sha256:917d52d2720b058730f9574e0f9ade02ef540e40479b3b5b4d32024dd1a81489`.

## Current-runtime read-back

- Status: `success`.
- Contract: `stage-owned-change-local-v2`, activation `historical`, authority `historical` under the staged v3 candidate runtime.
- Current stage: `verify`; active milestone: `M6`.
- Unresolved findings: none; stale evidence: none; blockers: none.
- Permitted operations: none, as required for historical v2 state under the candidate runtime.
- Observed lifecycle revision: `sha256:917d52d2720b058730f9574e0f9ade02ef540e40479b3b5b4d32024dd1a81489`.

## Interpretation

Both readers agree on the exact serialized lifecycle revision, current stage, active milestone, absence of findings, absence of stale evidence, and absence of blockers. Their authority projections differ intentionally: the bound v2 runtime supplies this change's preactivation closeout authority, while the current candidate treats the same record as readable history with no progression authority. No activation, publication, release, tag, migration, or historical artifact mutation occurred.
