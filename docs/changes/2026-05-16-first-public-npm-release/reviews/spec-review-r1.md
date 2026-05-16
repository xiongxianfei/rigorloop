# Spec Review R1 - RigorLoop npm Publication

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/rigorloop-npm-publication.md
Reviewed artifact: specs/rigorloop-npm-publication.md
Review date: 2026-05-16
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: SR1-F1, SR1-F2
- Recording status: recorded
- Recording blocker: none
- Reviewed artifact: specs/rigorloop-npm-publication.md
- Review log: ../review-log.md
- Review resolution: ../review-resolution.md
- Immediate next stage: spec

## Scope

This review covers the first public npm publication spec for `@xiongxianfei/rigorloop@0.1.4`. It checks whether the publication contract is precise enough for architecture, planning, test-spec, and implementation without guessing.

## Findings

### SR1-F1 - First-publication bootstrap conflicts with release workflow ownership

Finding ID: SR1-F1
Severity: blocking

Location: `specs/rigorloop-npm-publication.md` requirements R36, R38-R40, and R53-R55.

Evidence: R36 says the existing `.github/workflows/release.yml` "MUST own npm publication for this slice." R38 through R40 say the release workflow must run the release gate, package-content validation, and packed-package smoke before npm publication. R53 then allows one-time manual bootstrap publication if trusted publishing cannot be configured before first publication, and R55 requires bootstrap to run the same checks. The spec does not define whether manual bootstrap publishes a workflow-produced tarball, a locally produced tarball, or whether the workflow's publish job is skipped for `v0.1.4`.

Problem: Architecture and implementation would have to invent the first-publication path. The current wording can be read as both "release.yml owns publication" and "a maintainer publishes manually." That is not one testable release contract.

Required outcome: Define mutually exclusive publication modes and the artifact identity rule for the first publish.

Safe resolution path: Add a "Publication modes" section:

```md
Trusted-publishing mode:
- `.github/workflows/release.yml` runs release verification, package-content validation, packed-package smoke, and `npm publish` through OIDC.
- This is the normal mode after bootstrap.

Bootstrap mode:
- Used only for `@xiongxianfei/rigorloop@0.1.4` when npm cannot configure trusted publishing before package creation.
- `.github/workflows/release.yml` or `bash scripts/release-verify.sh v0.1.4` still owns release readiness.
- The maintainer may manually run `npm publish <tarball>` only for the exact packed tarball whose filename, SHA-256, source commit, and smoke result are recorded.
- `release.yml` publish job is enabled for future trusted-publishing releases after trusted publisher setup.
```

### SR1-F2 - Publication acceptance does not prove the real Codex adapter install path

Finding ID: SR1-F2
Severity: major

Location: `specs/rigorloop-npm-publication.md` requirements R4, R19, R46, R64, R68, and R81-R83.

Evidence: The spec maps the npm package to compatible adapter release `v0.1.4` and requires bundled metadata `adapter-artifacts-v0.1.4.json`. The user-facing public flow is `npx @xiongxianfei/rigorloop@latest init --adapter codex`. However, packed-package smoke only requires `init --adapter codex --dry-run --json`; local archive smoke is only `SHOULD` when a fixture is available; post-publication verification only `SHOULD` run the dry-run init command. No requirement proves that the official `v0.1.4` Codex adapter archive named by bundled metadata exists, is reachable, and verifies through an actual install.

Problem: The package can satisfy acceptance while the primary non-dry-run `init --adapter codex` user flow is broken by missing GitHub release assets, stale bundled metadata, or archive mismatch.

Required outcome: Require actual adapter install proof before FU-010 closes.

Safe resolution path: Add requirements:

```md
Before FU-010 closes, verification MUST run an actual `init --adapter codex --json` from the packed or published package in a temporary project and prove the official `v0.1.4` Codex archive named by bundled metadata is reachable and verifies successfully.

If npm publish happens before GitHub release assets are externally observable, publication evidence MUST record the temporary ordering gap and FU-010 MUST remain open until actual install smoke passes.
```

The spec should also clarify whether this proof is required before npm publication, before FU-010 closeout, or both. The safer minimum is before FU-010 closeout.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | block | Bootstrap and workflow ownership create two plausible publish paths. |
| Normative language | concern | The spec uses clear `MUST` language, but some `MUST`s conflict. |
| Completeness | block | Real adapter install availability is not required before closeout. |
| Testability | concern | Tarball checks are testable; bootstrap artifact identity is not yet testable. |
| Examples | concern | Examples cover dry-run and tarball shape but not actual adapter installation. |
| Compatibility | pass | Version alignment and deferred follow-ups are explicit. |
| Observability | concern | Publication evidence exists, but bootstrap tarball identity needs a precise field set. |
| Security/privacy | pass | Package-content and token boundaries are generally strong. |
| Non-goals | pass | FU-006 through FU-009 remain out of scope. |
| Acceptance criteria | concern | Acceptance can pass without proving the primary non-dry-run install path. |

## Readiness

Immediate next repository stage: spec revision.

Eventual test-spec readiness: not-ready.

Stop condition: Do not proceed to architecture, plan, test-spec, or implementation until SR1-F1 and SR1-F2 are resolved in the spec and spec-review reruns.
