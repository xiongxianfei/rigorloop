# Code Review R5

Review ID: code-review-r5
Stage: code-review
Round: 5
Reviewer: Codex code-review
Target: working tree M3 implementation slice
Reviewed artifact: README.md; packages/rigorloop/README.md; packages/rigorloop/package.json; packages/rigorloop/dist/bin/rigorloop.js; packages/rigorloop/dist/metadata/adapter-artifacts-v0.3.0.json; packages/rigorloop/dist/metadata/releases.json; scripts/adapter_distribution.py; scripts/npm_package_validation.py; scripts/release-verify.sh; scripts/test-adapter-distribution.py; scripts/test-npm-package-publication.py; docs/releases/v0.3.0/
Review date: 2026-05-24
Status: changes-requested
Recording status: recorded

## Outcome

- Review status: changes-requested
- Material findings: TNI-CR5-F1
- Blocking findings: none
- Reviewed milestone: M3. Release, Docs, And Package Validation Hardening
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3, M4
- Required review-resolution: yes
- Next stage: review-resolution for TNI-CR5-F1

## Review inputs

- Diff/review surface: working tree diff for M3 package versioning, bundled v0.3.0 metadata, README/release docs, release verification scripts, npm package publication smoke, adapter distribution validation, and active plan handoff updates.
- Tracked governing branch state: not claimed; governing target-native init artifacts are local workflow artifacts in the current working tree.
- Governing artifacts: `specs/target-native-init.md`, `specs/target-native-init.test.md`, `docs/plans/2026-05-24-target-native-init-commands.md`, `docs/adr/ADR-20260524-target-native-init-state-boundary.md`.
- Validation evidence: M3 validation notes in the active plan and `change.yaml`, including `npm test --prefix packages/rigorloop`, `python scripts/test-npm-package-publication.py`, `python scripts/test-adapter-distribution.py`, `python scripts/validate-release.py --version v0.3.0 ...`, `RELEASE_OUTPUT_DIR=... RELEASE_COMMIT=... bash scripts/release-verify.sh v0.3.0`, docs sweep, lifecycle validation, review-artifact validation, and patch hygiene.

## Diff summary

M3 updates public usage to target-native `init <target>` commands, bumps the npm package to `0.3.0`, adds bundled v0.3.0 release metadata, extends package smoke to run real non-dry-run default and `--write-state` installs for `codex`, `claude`, and `opencode`, adds v0.3.0 release notes/evidence, and updates release verification to build and validate v0.3.0 archives. The implementation also allows top-level `CLAUDE.md` as a release archive support entry so real Claude archives pass verification.

## Findings

### TNI-CR5-F1

Finding ID: TNI-CR5-F1
Severity: major
Location: `scripts/adapter_distribution.py`; `docs/releases/v0.3.0/npm-publication.md`; `specs/target-native-init.test.md`; `docs/plans/2026-05-24-target-native-init-commands.md`
Evidence: The approved test spec says `TTNI-SMOKE-003` post-publish live registry/download evidence must name the npm version, public archive URLs, installed roots, tree hashes, file counts, and command output summary for every target. The observability section also says release evidence validation must name live post-publish smoke, tree hashes, and file counts. The M3 plan calls for post-publish evidence schema/test updates for live registry/download smoke entries. The current `target_init_smoke` rows in `docs/releases/v0.3.0/npm-publication.md` contain command, package source, target, archive URL, boolean verification flags, result, and closeout blocker only. The validator in `scripts/adapter_distribution.py` checks target set, command, target, archive URL, result, and boolean archive/tree verification, but it does not require installed root(s), tree hash value(s), file count(s), command output summary, or negative fixture coverage proving those fields are required.
Required outcome: Extend the v0.3.0 post-publish live-smoke evidence contract and tests so recorded evidence for each target includes the fields required by `TTNI-SMOKE-003` and release evidence validation enforces them before published evidence can pass.
Safe resolution path: Add target-smoke evidence fields for installed root(s), tree hash value(s), file count(s), and command output summary in `docs/releases/v0.3.0/npm-publication.md`, using pending placeholders before publication and real values after live smoke. Update `_validate_npm_publication_evidence` so `published` v0.3.0 evidence fails when any target row omits those fields, and consider requiring pending placeholders while status is `pending-publication` so the execution contract is visible before publish. Add direct release validation tests in `scripts/test-adapter-distribution.py` for missing target-smoke detail fields and for complete published target-smoke evidence. Keep pre-publish packed-package smoke and target-native docs validation unchanged.
needs-decision rationale: none

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | M3 aligns with TNI-R86 through TNI-R90 for packed-package pre-publish smoke, but the post-publish evidence contract for TNI-R91 / `TTNI-SMOKE-003` is under-specified in validation. |
| Test coverage | block | There is no direct negative/positive release validation test proving v0.3.0 live smoke evidence must include installed roots, tree hashes, file counts, and command output summary. |
| Edge cases | concern | Pending post-publish evidence correctly blocks closeout, but a later `published` row can pass without recording the detailed proof fields named by the test spec. |
| Error handling | pass | The reviewed M3 parser/runtime changes do not introduce a new error-handling regression in the target-native init path. |
| Architecture boundaries | pass | The implementation keeps deferred `dist/adapters/`, archive filenames, and package-bundled metadata field naming while changing public commands and state behavior. |
| Compatibility | pass | Historical release validation remains version-scoped, and v0.3.0 package validation does not rewrite old release evidence. |
| Security/privacy | pass | The reviewed evidence and validators avoid secrets, raw proxy values, and absolute temp paths in committed release evidence. |
| Derived artifact currency | pass | Bundled v0.3.0 metadata is versioned and validated against generated release archives; no generated public adapter skill bodies are hand-edited. |
| Unrelated changes | pass | The reviewed M3 changes stay within package/release/docs validation surfaces plus the small archive support-entry allowance needed for real Claude archives. |
| Validation evidence | concern | Recorded validation passed, but it does not compensate for the missing post-publish evidence-detail enforcement. |

## No-finding rationale

Not applicable; one material finding requires review-resolution before M3 can close.

## Residual risks

- The packed-package pre-publish smoke path appears materially stronger than v0.2.0 and directly exercises real non-dry-run installs. The open risk is the post-publish evidence schema allowing thin pass rows after publication.

## Milestone handoff

- Reviewed milestone: M3. Release, Docs, And Package Validation Hardening
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes, for `TNI-CR5-F1`
- Remaining in-scope implementation milestones: M3, M4
- Next stage: review-resolution for `TNI-CR5-F1`
- Final closeout readiness: not ready; M3 has an open material finding and M4, final explain-change, verify, and PR handoff remain open.
