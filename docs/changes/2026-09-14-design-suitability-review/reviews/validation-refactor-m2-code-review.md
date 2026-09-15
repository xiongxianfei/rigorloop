# Validation organization M2 independent Code Review

## Result

- Skill: code-review.
- Status: completed after correction assessment.
- Artifacts changed: this review only.
- Open blockers: none within M2.
- Next stage: fresh independent final whole-change Code Review, then distinct scoped Verify.
- Review status: approved.
- Material findings and Finding IDs: M2-CR-01 and M2-CR-02, both resolved below.
- Recording status: recorded, advisory-durable/manual; recording blocker: none.
- Review record: `reviews/validation-refactor-m2-code-review.md`.
- Assessment scope: advisory milestone assessment.
- Reviewed milestone: M2 of `docs/plans/2026-09-14-validation-test-organization.md`.
- Milestone closeout: closed for this scoped review; no lifecycle state changed.
- Remaining implementation milestones: none in this plan.
- Required review-resolution: no.
- Verify readiness: not-claimed; final whole-change review remains separate.

## Finding M2-CR-01

- Finding ID: M2-CR-01.
- Severity: major.
- Location: `scripts/validate-release.py:152–154`, `verify_prepared_release` command list.
- Scope: artifact-local implementation; producer is the prepared-release qualification path.
- Evidence: the function still invokes `scripts/test-skill-validator.py`, `scripts/test-adapter-distribution.py` and `scripts/test-npm-package-publication.py`. M2 deletes those paths and relocates the suites. `release-verify.sh` reaches this function, which calls `release_candidate.run(command, root)` directly, so the updated catalog cannot repair these invocations. Qualification fails when it attempts the absent first test script.
- Governing requirement: TEST-SR-10/17, retained actual release callers and M2's concrete caller reconciliation/proof allocation.
- Required outcome: prepared-release qualification invokes all three current suite locations with the same case scope and preserves failure and receipt behavior.
- Safe resolution path: implementation owner corrects the three production argv paths, inspects related callers/receipt expectations, and supplies focused regression or actual prepared-release evidence showing the relocated commands are reached. Reassess the corrected subject and any further consumer changes before M2 approval.
- Decision need: none; this is preservation of the approved release interface, not a new release policy.

## Review basis and limits

Author `/root` implemented the slice. Separate delegated reviewer `/root/validation_design_review` did not edit implementation and recorded this finding before author correction. The reviewer inspected baseline-relative diffs against `/tmp/validation-m2-baseline/sources.tar`, all moved suites/support modules, catalog and finite coverage bases, selector fixture paths, workflow command and contributor/map changes. Earlier M1 and pre-existing branch work are not attributed to this slice.

The discovered defect comes from an independent search of actual remaining production callers. Most inspected relocation changes preserve intended imports, selection and assertions. Sixteen current M2 subjects were inspected through the CLI and captured in `/tmp/validation-m2-review-subjects.json`; the finding's concrete source and absent paths establish the required correction independently of a passing local suite. The implementation actor's local/broad execution was still running at this first-pass judgment. No pending run is represented as success and no final M2 or branch-wide approval is given.

The finding source was separately inspected through CLI as `scripts/validate-release.py`, identity `sha256:475a0f259b70109a5786af0473f4a96baa0047578f9a522d01ef1979e13d9289`. That identity is the defective version, not an approval target for a corrected version.

## M2-CR-01 correction assessment

The author corrected only the three production suite argv paths in `verify_prepared_release`; receipt invalidation, command execution, failure handling and final receipt production remain unchanged. The real candidate integration failed before correction at release-integrity and passed afterward (`/tmp/validation-m2-release-caller-green.log`, one test in71.841s). Its receipt assertions now require all three relocated suite commands. Hosted providers remain simulated, while the prepared-release build/validation path uses real local commands.

Reviewer inspection accepts this correction and resolves M2-CR-01. This finding disposition does not yet approve M2: the complete current local/broad execution is still pending, and the eventual overall judgment must assess its results and exact final subjects. A separate exact publication-workflow routing correction selects the existing CLI/npm owner and has a failed-before/passed-after regression; no wildcard workflow exemption is added.

## Finding M2-CR-02

- Finding ID: M2-CR-02.
- Severity: major.
- Location: `.github/workflows/publish-github-packages.yml`, release-tag checkout and Verify package before publication step.
- Scope: artifact-local workflow compatibility; implementation/CI-maintenance owner.
- Evidence: the workflow accepts a release tag and checks out that selected tag before running package proof. The M2 command now unconditionally names the relocated npm suite. Independent `git ls-tree v0.3.3 -- scripts/test-npm-package-publication.py tests/engineering/packaging/test-npm-package-publication.py` shows that supported historical tag contains only the old script. The hardcoded new path therefore fails before verification for that tag. The author surfaced this concern; this reviewer independently checked the full workflow sequence and historical path evidence before recording it.
- Governing requirement: TEST-SR-10/17 compatibility and actual callers, and the plan's preservation of release behavior.
- Required outcome: the existing selected-tag workflow executes the real suite present in that checkout, supporting both pre-move and post-move tags without skipping required proof or manufacturing a pass.
- Safe resolution path: choose the current path when it exists, otherwise the actual old suite path when present; fail explicitly if neither exists. Exercise the actual workflow shell step with current-path, old-path and missing-suite checkout fixtures, including nonzero test propagation. This adds no alias source and changes no publication permission.
- Decision need: none; preserving the existing tag-selected operation is within the approved compatibility scope.
- Current disposition: open; M2 remains changes-requested until author correction and independent reassessment.

## M2-CR-02 correction assessment

The workflow now chooses the current suite when present, otherwise the real old suite present in the selected historical checkout, and explicitly fails when neither exists. The new npm test parses the actual workflow with the existing YAML dependency and executes that exact shell block in owned temporary checkouts. Current-only, historical-only, both, missing and nonzero-suite cases passed after the historical case failed before correction (`/tmp/validation-m2-tag-layout-green.log`, one method with five scenarios). It observes dispatch and exit propagation rather than merely asserting source text. Candidate integration copies the three current workflow files alongside relocated test sources; existing tracked-file staging preserves their coherent bytes.

The reviewer accepts this correction and resolves M2-CR-02. It changes no tag input, credentials, publication step or external permission. Required final applicable execution remains pending before the renewed overall M2 judgment.

## Final M2 reassessment and exact subjects

The reviewer inspected the corrected source, both real failure-before/success-after observations, the executed workflow-shell scenarios and complete final logs. The final seventeen identities below were obtained with CLI subject inspection and confirmed unchanged after the final candidate/package runs. The earlier first-pass findings retain their original meaning; this section renews the overall judgment for the corrected subjects rather than calling the original defective version approved.

| Subject | Identity |
| --- | --- |
| `tests/skill/test-skill-validator.py` | `sha256:cbb87842ff1921372c411c8515fa9b2ad2ead1b881d7ba5fb7257a0d0f52e885` |
| `tests/skill/review_independence_skill_phrases.py` | `sha256:f768f7e0fdfb277b30b6cdaaad398149b0e2fcce1cf496ab16f7cd4ce6800ed8` |
| `tests/engineering/packaging/test-adapter-distribution.py` | `sha256:0cb181f89d6753bbe3d7a0a56c34a2390b1bff548c53e0aefc1b6cb494f7eda6` |
| `tests/engineering/packaging/test-npm-package-publication.py` | `sha256:17fa925872f79b4f6198d43dd118d08c20cc153dc5babb449ee2ea69832cd248` |
| `tests/engineering/release/test-release-transaction.py` | `sha256:e27a19515a4e86c2e781e21685cce59bd3b7b7ebaf95b857fd2d7500518913e2` |
| `tests/engineering/release/release_candidate_tests.py` | `sha256:00a6b4b8c210aa42bc2c1ed79fb63566174a6a7a60d99e74d586559f0cb0258a` |
| `tests/engineering/release/release_coordination_tests.py` | `sha256:0c9e2d3c3e8137a25b7f23941d9c056fa6c82ecd575b0efdea9a7bea06878de7` |
| `tests/engineering/release/release_execution_tests.py` | `sha256:3e87f1f6ac3c1046873c11289a3063555ef71b4e46215f4dbe72ee63ddb342ea` |
| `tests/engineering/release/release_evidence_tests.py` | `sha256:9816b0405154b96bb29c11c39005e98b1976e34bd90f37ae92a81bb349a7ca75` |
| `scripts/validation_selection.py` | `sha256:1d0e75c1e0943d89eb913ca9c837d6f09f6eebe805a4e0f6521e7372343d5747` |
| `tests/engineering/validation/test-select-validation.py` | `sha256:92dbc89f2253032af5cced278b86ef5b56e5a722a5f46bdda7a41931f9c04d8f` |
| `tests/engineering/validation/test-validation-execution.py` | `sha256:c1eb565327164a70e57d8bfee8a5ce10b83e9397f9fb1256a92d09ce67199a29` |
| `.github/workflows/publish-github-packages.yml` | `sha256:540a4ef7ee36c1234aaa904b6829f356126480eb55722902483bcc9d90528596` |
| `docs/design/skill/skill.md` | `sha256:ddb2458d430d17559e571fb605b6c812e901f310d96da7e015d749020afac02b` |
| `CONTRIBUTING.md` | `sha256:be2d0b9a35f33f1b987fe9df9ef31f49780877107c8b0285216c1b83b1732d1e` |
| `docs/project-map.md` | `sha256:58cbc8b70ef0dcb80a50e8d44769fa726f281ec00ec1bff4089c5ad04caaa924` |
| `scripts/validate-release.py` | `sha256:39cd61cc32b030c50190f7327356027d75f16b91c680599ed39b20ae10757680` |

### Checklist and rationale

| Criterion | Result and concrete basis |
| --- | --- |
| Spec alignment | Pass: M2 relocates four entrypoints, four imported release modules and the test-only Skill helper according to TEST-SR-17; production helpers remain in scripts. |
| Test coverage | Pass: all926 pre-migration Python IDs remain; routing and actual workflow-shell regression cases add protection. No pre-existing assertion or case was removed. Receipt assertions expose omitted release-suite execution. |
| Edge cases | Pass: old/new/helper paths, unknown paths, selected historical tags, both layouts, missing suite and failing suite are addressed at their actual observation boundaries. |
| Error handling | Pass: release receipt invalidation and failure propagation are unchanged; missing historical/current workflow tests reject explicitly, and failed test status remains unsuccessful. |
| Architecture boundaries | Pass: package tests remain colocated, test-only helper stays with Skill, runtime release fixture producer/path are unchanged, and catalog/coverage hashes are explicit assessed literals. |
| Compatibility | Pass after M2-CR-01/02: prepared-release direct callers and selected-tag workflow now execute the appropriate real suites. Existing exact check IDs and case scope survive. |
| Security/privacy | Pass within scope: permissions, publication steps and credential access are unchanged. Tests use owned local state and simulated hosted providers; no publication occurred. |
| Derived artifact currency | Pass for tested scope: real package suite, candidate chain, archive construction/validation and local installation observations execute. No hosted availability or released artifact claim follows. |
| Unrelated changes | Pass: comparison uses pre-M2 source tar, separating earlier dirty work. Project-map refresh explicitly limits its current claim to inspected test/caller areas. |
| Validation evidence | Pass through the combined current evidence described below; the unsuccessful full run remains unsuccessful and is not relabelled green. |

The release candidate fixture now copies/stages the current tests tree because tests no longer arrive implicitly with scripts. It also copies current release/CI/publication workflow sources so tests inspect the coherent candidate source. This repairs fixture completeness without changing expected product behavior. Shared skill/adapter roots retain suite and selector path/qualification consumers; no exclusive input is deleted. Current production old-path references are limited to the intentionally supported historical checkout fallback and selector deletion routing.

### Final evidence applicability

The full `bash scripts/ci.sh --mode local --broad-smoke --jobs 4` run was unsuccessful:1358 check/case rows passed and one candidate integration failed. The reviewer inspected the diagnostic boundary results; archive build/validation and required boundary work did execute and pass, with no unstarted/blocked/cancelled task rows. The unsuccessful aggregate phase verdict is preserved.

The late edits were confined to the npm workflow-layout regression, the publication shell step and the candidate fixture's coherent workflow copies. The unchanged successful rows remain useful because their protected source/test inputs and execution contracts were unaffected by those edits. Their checks were actually executed, not inferred from selection. The affected package population and candidate observation were rerun on the final exact sources:

- `python tests/engineering/packaging/test-npm-package-publication.py`:8 tests passed in27.868s, including actual workflow-shell execution and package boundaries (`/tmp/validation-final-package.log`).
- Real candidate integration `ReleaseCandidateIntegrationTests.test_actual_candidate_build_and_packed_metadata_chain`: one passed in73.292s (`/tmp/validation-final-candidate.log`), with final receipt checks, coherent workflow inputs and relocated real suite execution.

These final passes replace reliance on the earlier failed candidate and stale package/workflow observations for their affected scope. They do not turn the earlier aggregate command into a passing invocation. Combined current evidence covers the required observations without repeating unaffected1358 rows solely for a new aggregate label. The durable author M2 evidence records the actual commands, failures, corrections, discovery and limitations; no hosted CI is claimed.

No material concern remains in M2. Proceed to the plan's distinct independent final whole-change assessment. This milestone judgment does not approve the accumulated branch, historical initiatives, publication or final Verify.
