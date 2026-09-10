# 1.0.0 release preparation evidence

Status: blocked before release-preparation merge and publication. This is operational release evidence, not approval of new engineering behavior or a successful Verify.

## Inputs and decision

The maintainer approved 1.0.0 and the proposed GitHub setup on 2026-09-10. Source preparation is 59aed9c05f9019cafa36a2f3f5923ccee0d313af on release/v1, based on merged source cf6ed229b8314727f47c6dbe387510b4f6f548ac. The previous public npm/GitHub version observed was 0.5.0. Version selection is major because the merged changes retire public commands, skills and runtime record formats. The four-file preparation changes the package/lock version and adds tracked release intent and compatibility notes; it changes no release implementation or validation policy.

## Completed setup

GitHub API readback confirmed main protection with one required PR approval, strict ci status check, administrator enforcement and no force-push/deletion. The release environment requires individual reviewer xiongxianfei, protected-branch deployments and no administrator bypass. RELEASE_EVIDENCE_REF is refs/heads/release-evidence.

npm whoami and npm trust list @xiongxianfei/rigorloop returned 401. No npm credential was exposed or changed. The trusted publisher must name repository xiongxianfei/rigorloop, workflow release.yml and environment release. RELEASE_TRUSTED_PUBLISHER was deliberately not set without establishing that npm configuration. The repository has only the current account as collaborator; it cannot approve its own preparation PR under the selected rule. An eligible independent reviewer or an explicit owner-selected policy correction is needed; no bypass was attempted.

## Candidate proof and independent review

The actual prepare_candidate builder ran on the exact local preparation source and release/v1 ref against public baseline0.5.0, with a separate temporary output. This is premerge local proof, not a main-branch candidate or hosted publication authorization.

Candidate b512c90267c2ac79088ab8b8b7cffcd3ff1a8048625612aaa9aca328397e394b passed profile, preflight and release-integrity. The existing bash scripts/release-verify.sh v1.0.0 --prepared-candidate command ran as part of the builder; release-integrity took43.15 seconds. Its nine constituent checks passed, including actual packed CLI initialization for Codex, Claude and opencode. The output contains real generated archives, their metadata/index projection, tarball and sealed verification receipts. No public service was written.

The independent nonauthor reviewer approved the corrected four-file release content and independently checked the candidate seal and receipts. Its original finding corrected the notes to state spec/architecture → design and workflow → route, while preserving the already-existing Design Review and Delivery Review gates. That content approval explicitly did not claim selected-CI, branch readiness or publication success.

Earlier local attempts are not passes: the first rejected a source-ref name containing dots before mutation; subsequent preparation rejected missing required Result fields and the missing v prefix in the notes heading. Both content issues were corrected before the passing candidate above.

## Required PR checks: failed

Executed:

```bash
bash scripts/ci.sh --mode pr --base cf6ed229b8314727f47c6dbe387510b4f6f548ac --head 59aed9c05f9019cafa36a2f3f5923ccee0d313af
```

All four selected checks failed:

| Check | Observed failure | Required disposition |
| --- | --- | --- |
| artifact_lifecycle.validate | The authored standing intent lacks complete sections that the candidate builder adds later. | Reconcile source-input validation with complete generated operational evidence; do not assert pending results passed. |
| release.validate | Historical recorded-source validation rejects v1.0.0 as unsupported. | The validation owner must reconcile selection with the adopted candidate path, preserving required checks. |
| rigorloop_cli.test | Current tests and bundled metadata still expect0.5.1; changed source package reports1.0.0. | Reconcile version-bound fixtures and actual package consumers without weakening regression assertions. |
| npm_package_publication.test | The raw source package lacks v1.0.0 bundled metadata/index that the candidate build supplies; seven tests fail. | Reconcile the inspected package subject and its actual generated metadata; preserve all-target installed proof. |

The passing candidate does not waive these failed required PR checks. No fresh successful final Verify, ready PR, release approval, publication or public closeout is claimed.

## Outstanding ownership

The CI/release integration correction requires the existing validation and Release owners, with its actual scope independently assessed before relying on changed selection or fixtures. npm setup requires an authenticated maintainer. The required preparation PR approval needs an eligible reviewer. After those prerequisites, the supported workflow must prepare from the actual merged source and present its exact candidate for approval before publication. Retain actual failures and inspect public state before retrying any public operation.

Initial merged Release workflow run34450506437 stopped before publication on missing trusted-publisher configuration intent; its execute job was skipped. No release1.0.0 tag, GitHub release or npm package was created during this preparation.
