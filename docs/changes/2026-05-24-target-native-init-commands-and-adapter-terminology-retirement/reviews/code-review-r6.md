# Code Review R6

Review ID: code-review-r6
Stage: code-review
Round: 6
Reviewer: Codex code-review
Target: working tree M3 implementation slice after TNI-CR5-F1 resolution
Reviewed artifact: scripts/adapter_distribution.py; scripts/test-adapter-distribution.py; docs/releases/v0.3.0/npm-publication.md; docs/plans/2026-05-24-target-native-init-commands.md; docs/plan.md; docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md
Review date: 2026-05-24
Status: approved
Recording status: recorded

## Outcome

- Review status: clean-with-notes
- Material findings: none
- Blocking findings: none
- Reviewed milestone: M3. Release, Docs, And Package Validation Hardening
- Milestone closeout: closed
- Remaining implementation milestones: M4
- Required review-resolution: no
- Next stage: implement M4. Lifecycle Closeout And Broad Validation

## Review inputs

- Diff/review surface: working tree changes for v0.3.0 post-publish live-smoke evidence, npm publication evidence validation, release validation fixture tests, review-resolution, and active plan handoff updates.
- Tracked governing branch state: not claimed; this review evaluates the local working tree implementation and lifecycle artifacts.
- Governing artifacts: `specs/target-native-init.md`, `specs/target-native-init.test.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/adr/ADR-20260524-target-native-init-state-boundary.md`, and `code-review-r5` finding `TNI-CR5-F1`.
- Validation evidence: recorded M3 validation after `TNI-CR5-F1`, including `python scripts/test-adapter-distribution.py`, `python scripts/test-npm-package-publication.py`, `npm test --prefix packages/rigorloop`, `python scripts/validate-release.py --version v0.3.0 --release-output-dir /tmp/tmp.cWJYJ5cs7M --release-commit 02a9d7d6d514fc99908abf32898494dbbbae00c9`, `RELEASE_OUTPUT_DIR=/tmp/tmp.cWJYJ5cs7M RELEASE_COMMIT=02a9d7d6d514fc99908abf32898494dbbbae00c9 bash scripts/release-verify.sh v0.3.0`, change metadata validation, lifecycle validation, review-artifact validation, and patch hygiene.

## Diff summary

The M3 fix extends `docs/releases/v0.3.0/npm-publication.md` so each `target_init_smoke` row records npm version, package source, public archive URL, installed root(s), tree hash value(s), file count(s), command output summary, verification flags, result, and closeout blocker. Pending-publication rows now carry explicit placeholders and keep post-publish closeout blocked.

`scripts/adapter_distribution.py` now validates v0.3.0 `target_init_smoke` rows separately from historical `adapter_install_smoke` rows. Published rows must replace placeholders with real public archive URLs, installed roots, `sha256:<hash>` tree values, numeric file counts, command summaries, `pass` results, true verification flags, and cleared closeout blockers. The opencode row must name both `.opencode/skills` and `.opencode/commands` and map tree hash and file count values for both roots.

`scripts/test-adapter-distribution.py` adds direct fixtures for pending placeholders, complete published target-smoke evidence, missing installed roots, missing tree hashes, missing file counts, missing command output summary, incomplete opencode root coverage, and published placeholder leakage.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | `TTNI-SMOKE-003` requires live post-publish evidence to name npm version, public archive URLs, installed roots, tree hashes, file counts, and command output summary; the v0.3.0 evidence and validator now require those fields. |
| Test coverage | pass | `scripts/test-adapter-distribution.py` has positive and negative validator tests for complete published rows, pending placeholders, each missing detail field, incomplete opencode root coverage, and published placeholder leakage. |
| Edge cases | pass | Published evidence rejects pending markers, requires `pass` plus true archive/tree verification, and requires opencode's two roots with mapped tree hash and file count values. |
| Error handling | pass | Validator diagnostics identify missing root, tree hash, file count, command summary, pending placeholder, and opencode root mapping failures with target-specific messages. |
| Architecture boundaries | pass | The fix stays in post-publish evidence and validation; it does not change target-native init runtime behavior, archive metadata generation, state schema, or deferred internal adapter naming. |
| Compatibility | pass | Historical non-v0.3.0 publication evidence keeps the `adapter_install_smoke` path; v0.3.0 uses version-scoped `target_init_smoke`. |
| Security/privacy | pass | Committed pending evidence uses placeholders and does not record live temp paths, secrets, credentials, or private runtime values. |
| Derived artifact currency | pass | The v0.3.0 release evidence is validator-backed, and release validation was rerun against generated release artifacts after the fix. |
| Unrelated changes | pass | The reviewed fix is scoped to post-publish target-smoke evidence and validation plus lifecycle handoff records. |
| Validation evidence | pass | Recorded validation includes the full distribution test suite, package publication tests, package CLI tests, v0.3.0 release validation, release verification, lifecycle validation, review-artifact validation, and patch hygiene. |

## No-finding rationale

`TNI-CR5-F1` required the post-publish live-smoke evidence contract to become enforceable before published evidence can pass with thin rows. The implementation adds the required evidence fields, enforces them in the v0.3.0 validator path, and includes direct tests for every named omission and opencode's multi-root requirement. The change remains version-scoped and does not alter pre-publish packed-package smoke or target-native init runtime behavior.

## Residual risks

- Live registry/download smoke remains pending until `@xiongxianfei/rigorloop@0.3.0` and the matching public release archives are externally observable. That is expected release-execution evidence, not a pre-publish implementation blocker.
- M4 lifecycle closeout, final explain-change, verify, and PR handoff remain open.

## Milestone handoff

- Reviewed milestone: M3. Release, Docs, And Package Validation Hardening
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: M4
- Next stage: implement M4. Lifecycle Closeout And Broad Validation
- Final closeout readiness: not ready; M4, final explain-change, verify, and PR handoff have not happened yet.
