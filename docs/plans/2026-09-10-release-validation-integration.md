# Simplify release validation integration

Owning change: [2026-09-10-release-validation-integration](../changes/2026-09-10-release-validation-integration/change.json).

## Scope

Implement the scoped Release-model correction selected by the maintainer: no required GitHub PR approval; retain protected PR/CI integration, independent engineering assessment, Verify and one protected release approval. Reconcile existing ordinary CI with authored release intent and the actual generated candidate. Keep historical validation, failure propagation and unrelated product behavior intact. Existing 1.0.0 intent is the reproduced input; no publication occurs as part of proof.

## M1 — One coherent preparation and check path

1. Author regression proof for invalid/pending/historical selection and version-independent current fixtures, using the observed four-check failure as the integrated baseline.
2. Reuse existing candidate preparation from an exact committed source in an isolated workspace. Both ordinary selected PR CI and direct main CI enter the same isolated preparation composition before their existing runners. Preserve every direct main gate and its existing execution order. Ordinary selected CI checks the prepared source and actual package overlay; route the current pending version through its prepared validator and retain historical commands. Reject mismatched inputs or failed preparation without executing downstream success claims. Do not mutate the original checkout or introduce another runner.
3. Make current CLI test expectations follow the tested package; preserve historical and incompatible-version cases. Complete required pending intent validation without fabricated results. Reconcile concise operator guidance and one-time setup.
4. Exercise selected CI on a source release with a new stable version, including actual archives, package metadata and installed targets. Retain original failing observations and inspect subject identity and clean-source preservation.

## Requirements and proof

| Obligation | Proof |
| --- | --- |
| REL-SR-02/08/09 | Invalid intent and source mismatch reject; pending and historical checks retain their own subjects; existing selector/runner regressions and real new-version CI. |
| REL-SR-22/24 | No manual metadata/hash edits; actual generated package inputs and explicit checked subject; CLI/npm negative suites remain selected. |
| REL-SR-23 | No change to provider approval or external publication execution; independent diff review confirms CI preparation cannot authorize publication. |

Run focused existing release/selector regressions first, then `bash scripts/ci.sh --mode pr --base cf6ed229b8314727f47c6dbe387510b4f6f548ac --head <committed-final-subject>`. Also run `bash scripts/ci.sh --mode main --base cf6ed229b8314727f47c6dbe387510b4f6f548ac --head <committed-final-subject>` on the same subject, plus existing direct-main dispatch/failure regressions. A selected-PR pass does not substitute for this direct-main path. The exact head is recorded in execution evidence. Reuse the existing full candidate verifier, npm publication tests and CLI tests instead of replacing them with success stubs. Model/prose checks and record validation apply to changed governing artifacts. Independent M1 assessment and fresh final whole-change Code Review precede distinct Verify and PR handoff.

## Recovery and remaining boundaries

Failed preparation retains diagnostics without changing the source checkout or public services. Revert this bounded CI/fixture/documentation slice together if needed; preserve operational release history and the existing publication safeguards. GitHub review-count removal is separately user-authorized remote configuration. npm trusted-publisher authentication and final candidate approval remain external prerequisites; no credentials, token fallback or real publication is part of regression proof.
