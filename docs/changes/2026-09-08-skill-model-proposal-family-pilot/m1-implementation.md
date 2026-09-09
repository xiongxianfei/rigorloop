# M1 implementation evidence

Owning change: [change.json](change.json). Implements M1/TG-01–03 of the approved plan. This is implementation evidence, not milestone approval or final Verify.

The four selected pilot files now classify invocation before detailed recording. Existing references carry the complete v2 profile; project governance determines the proposal pointer. Adopted review policy and the retained unadopted scope-failure rule are explicitly separated. The production validator requires the mapped selected reference, body boundary and classification/load trigger even with no inline heading; escaped, unreadable, absent or malformed profiles fail. Current proposal-review placement uses v2 while legacy document-grammar fixtures retain their independent coverage. Archive profile comparison reads the selected references on all supported adapters.

## Proof and maintenance

New focused tests failed before the change (three failures), then passed. Their production-boundary mutations cover missing expected-revision content, absent resource with complete unrelated/inline text, escaped symlink, invalid UTF-8, unknown mapped path, missing body boundary/load trigger and wrong v2 review placement. Existing non-pilot normal-writer regression remains. The full skill suite's initial fixture/old-wording failures were corrected by supplying the required package to asset fixtures, preserving legacy grammar selection, and replacing unconditional old scope-status wording assertions with checks of the complete conditional adopted/portable rule. No test was deleted.

A raw-byte comparison against the pre-M1 inventory found exactly the four approved canonical files changed and 133 other canonical files unchanged. This includes all 17 non-pilot bodies, all pilot assets and shared policy/gate resources. No third pilot or shared-source behavior change is introduced. [Procedure/output walkthrough](m1-procedure-walkthrough.md) supplies bounded before/after and filled artifact evidence for independent assessment; it does not claim actual target-agent execution.

## Current-candidate metadata dependency

Inspection found `test_v0_5_1_bundled_candidate_metadata_matches_generated_route_only_archives` directly compares the packaged current metadata to `_local_release_candidate_metadata`. Used the existing `adapter_distribution.build_adapter_archives` and `_prepare_local_cli_release_candidate` builders for v0.5.1 in temporary directories, then copied their generated current metadata and current index entry into `packages/rigorloop/dist/metadata/`. The existing index order was preserved; only the current candidate hash changed in `releases.json`. The generated metadata contains exact archive sizes/hashes; no hash was invented. The full adapter suite includes the dependent comparison, which passed. A separate raw-byte SHA-256/index check passed. Historical release metadata files and index entries remain unchanged. No release, external installation or publication occurred.

## Commands actually run

| Command | Result |
| --- | --- |
| `python scripts/test-skill-validator.py -k targeted` | Initial red: three failures. Final focused proof: three tests passed. |
| `python scripts/test-skill-validator.py` | Final 357 tests passed after fixture/conditional-rule corrections. |
| `python scripts/validate-skills.py` | Gate A passed for all 19 skills. |
| `python scripts/build-skills.py` and `python scripts/build-skills.py --check` | Generation and drift check passed. |
| `python scripts/test-build-skills.py` | Seven tests passed. |
| `python scripts/test-adapter-distribution.py` | Full suite passed, including current metadata and all supported archive profile comparisons. Negative fixture diagnostics are expected within passing tests, not a release execution result. |
| Existing `adapter_distribution.build_adapter_archives('v0.5.1', output)` and `_prepare_local_cli_release_candidate('v0.5.1', output)` | Generated temporary candidates and current metadata through existing owning builders. |
| `python scripts/validate-adapters.py --version v0.5.1 --adapter-root "$skill_candidate_dir"` | Gate B passed against the generated temporary candidate directory. |
| Python pre/post canonical-byte comparison and current metadata/index SHA-256 check | Passed; four selected changes, 133 unchanged files; historical index entries preserved. |
| `python scripts/validate-documentation-prose.py --mode enforce --path docs/changes/2026-09-08-skill-model-proposal-family-pilot/m1-procedure-walkthrough.md` | Passed. |
| `git diff --check` | Passed. |

The exact changed implementation subjects are registered in the M1 evidence check. Approved Design and Delivery requirements are unchanged; changes to inspected baseline pilot subjects are the implementation those packages selected, not new engineering requirements. M1 still requires independent Code Review before M2; all current common source definitions remain in place during this slice. The rollback unit is the four pilot files plus their coupled validators/archive selection and regenerated current candidate metadata.
