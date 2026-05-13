# Public Adapter Artifact Migration Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the public adapter artifact migration, examples relocation, and concise skill release change.

Closeout status: open

## Resolution Entries

### proposal-review-r1

No material findings.

### spec-review-r1

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

Review closeout: closed

#### PR-001

Finding ID: PR-001
Disposition: accepted
Status: resolved
Owner: plan author
Owning stage: plan
Chosen action: Revise M5 so the token-cost benchmark validation command uses an executable `scripts/run-token-cost-benchmarks.py` invocation, or explicitly add a benchmark-runner CLI change and tests to the implementation scope.
Rationale: The current plan names `--version`, but the runner currently exposes `--release`. A non-executable final validation command would create a predictable late release-readiness failure.
Validation target: M5 names an executable token benchmark command using the public adapter release output or generated temporary public adapter output, and a plan-review rerun confirms the validation command is reliable.
Validation evidence: M5 updated to use `python scripts/run-token-cost-benchmarks.py --release v0.1.2 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`; `plan-review-r2` approved the revised plan with no material findings.

### plan-review-r2

No material findings.

### code-review-m1-r1

No material findings.

### code-review-m2-r1

Review closeout: open

#### PAAM-M2-CR1

Finding ID: PAAM-M2-CR1
Disposition: needs-decision
Status: unresolved
Owner: implementation author
Owning stage: implement M2 review-resolution
Decision owner: implementation author
Decision needed: Decide whether adapter artifact metadata must name the release commit under validation, or whether a reviewed release policy permits metadata to name a pre-metadata archive source commit.
Stop state: M2 remains `resolution-needed`; do not proceed to M3 until this finding is resolved and M2 returns to code-review.
Chosen action: pending owner decision
Required outcome: Release validation must reject adapter artifact metadata whose `release.source_commit` does not match the release commit under validation, unless a reviewed release policy explicitly permits that mismatch.
Safe resolution: Add direct validation for `release.source_commit` against the release commit input used by validation, add a negative regression test for source-commit mismatch, and either update the metadata to the accepted source commit model or record an approved policy exception if the metadata intentionally points to a pre-metadata archive source commit.
Validation target: Source-commit mismatch regression fails before the fix, passes after the fix, and `python scripts/validate-release.py --version v0.1.2 --release-output-dir <release-output-dir>` rejects mismatched source commits.
Validation evidence: pending
