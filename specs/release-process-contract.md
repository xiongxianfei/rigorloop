# Release Process Contract

## Status

approved

## Related proposal

- [RigorLoop Release Process Contract](../docs/proposals/2026-05-23-release-process-contract.md), accepted.
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-05-23-release-process-contract/reviews/proposal-review-r1.md), approved with observations and no material findings.
- Proposal review R2: [proposal-review-r2](../docs/changes/2026-05-23-release-process-contract/reviews/proposal-review-r2.md), approved with no material findings.

## Goal and context

This spec defines the standing RigorLoop release-process contract for packaging, publishing, verifying, and recording an already-reviewed and already-merged release candidate.

The release process is a recurring operation, not a new product decision. Routine publishes execute this contract and record durable release evidence. Changes to source behavior, package behavior, public skill behavior, adapter behavior, release surfaces, release gates, publication policy, provenance policy, or evidence policy still require the normal RigorLoop lifecycle before publication.

This spec does not replace release-specific specs such as [RigorLoop npm Publication](rigorloop-npm-publication.md). Release-specific specs remain authoritative for their named versions and package surfaces. This spec supplies the standing process for future routine publishes unless a later approved spec supersedes it.

## Glossary

- `release process`: The standing process for packaging, publishing, verifying, and recording a release after upstream changes are approved.
- `routine publish`: A publish operation for already-reviewed, already-merged work that introduces no new product, package, adapter, or release-policy decision.
- `release-process change`: A change to release gates, evidence, authentication, provenance, versioning, publication mechanics, release evidence location, or recovery rules.
- `release evidence`: The durable record under `docs/releases/v<version>.md` that proves what was published, from which source, through which gate, and with which registry and smoke verification.
- `release gate`: The required pre-publish validation boundary for the release candidate.
- `trusted publishing`: npm publication from supported CI/CD using OIDC rather than long-lived npm tokens.
- `manual fallback`: A non-preferred publish path used when trusted publishing is not yet available or an approved emergency path requires it.
- `generated-output currency`: Proof that generated skills, adapters, package metadata, lockfiles, or release-output surfaces are current from canonical source.
- `drift check`: A repository-owned generated-output validation command such as `skills.drift`, `adapters.drift`, or the current equivalent command named by the active release plan/spec.
- `release index`: Optional `docs/releases/index.md` summary of release evidence records.

## Examples first

Example E1: routine stable publish uses the standing process
Given a patch release candidate contains only already-reviewed, already-merged fixes
When the maintainer publishes the version
Then no new proposal/spec/plan is required for the publish operation itself
And `docs/releases/v<version>.md` records the release type, source commit, release gate, package preview, publish path, registry verification, and install smoke.

Example E2: release-process change requires lifecycle treatment
Given a maintainer wants to change the required release gate or npm provenance policy
When the change is proposed
Then it is a release-process change
And the change must go through the normal lifecycle before a routine publish relies on it.

Example E3: generated output drift blocks publish
Given adapter archives or generated skill output differ from canonical source
When the release gate runs the generated-output drift checks
Then the release gate fails
And the package must not publish until generated-output currency is restored or an approved spec records a different authoritative boundary.

Example E4: manual fallback keeps the full gate
Given trusted publishing is not yet configured for the first process rollout
When a maintainer uses manual fallback
Then the same release gate, package preview, local packed install smoke, registry verification, and evidence requirements still apply
And release evidence records why manual fallback was used without recording secrets, OTPs, tokens, or private environment values.

Example E5: bad package content after publish fixes forward
Given a package version is already published
And post-publish smoke discovers wrong package contents
When recovery starts
Then maintainers must not overwrite the published npm version
And release evidence records failed-after-publish status plus fix-forward, dist-tag correction, or deprecation action as applicable.

Example E6: release evidence stays out of the plan index
Given a routine publish is not part of an active lifecycle plan
When release evidence is recorded
Then `docs/releases/v<version>.md` and the release index are updated as required
And `docs/plan.md` is not updated solely because the routine publish happened.

## Requirements

### Process boundary

REL-R1. The release process MUST distinguish release-process changes from routine publish operations.

REL-R2. A routine publish MUST execute this standing release process without requiring a new proposal, spec, or plan when the publish introduces no new product, implementation, package-surface, adapter-surface, or release-policy decision.

REL-R3. A release-process change MUST go through the normal RigorLoop lifecycle before routine publishes rely on it.

REL-R4. A change to package name, npm scope, public adapter target, install root, release evidence location, release gate, authentication policy, provenance policy, versioning policy, or publish mechanics MUST NOT be treated as a routine publish.

REL-R5. A breaking release MAY use the routine publish operation only when the breaking source or public behavior change has already completed its required upstream lifecycle.

REL-R6. Release evidence MUST record the release type and whether the publish introduced no new decision.

### Version and dist-tag decision

REL-R7. A release MUST NOT publish when there is no source, package, generated-output, or release-artifact change to publish.

REL-R8. Release evidence MUST record the selected version, release type, and npm dist-tag before publish.

REL-R9. Patch release classification MUST be limited to backward-compatible fixes, docs, validation, packaging, or internal workflow changes that do not add public API or public behavior.

REL-R10. Minor release classification MUST be used for backward-compatible public behavior, CLI, skill, adapter, or packaging capability additions.

REL-R11. Major release classification MUST be used for breaking public API, skill contract, adapter contract, install root, archive format, or CLI behavior changes.

REL-R12. Prerelease publication MUST use a non-`latest` dist-tag such as `next`, `beta`, `alpha`, or an approved equivalent.

REL-R13. Stable publication MUST use `latest` only when the release is intended for stable adoption.

### Release gate

REL-R14. A release MUST pass the full release gate before publish unless it is an emergency release with recorded owner-approved gate deferrals under REL-R14a and REL-R63.

For emergency releases:

- every non-deferred gate item MUST pass before publish;
- every deferred gate item MUST be named explicitly;
- every deferred gate item MUST have owner approval, reason, validation impact, and follow-up location;
- release evidence creation, secret suppression, version/dist-tag recording, package identity recording, publish path recording, and post-publish registry verification MUST NOT be deferred.

REL-R14a. Emergency release gate deferrals are exceptions, not an alternate normal release path.

An emergency deferral record MUST include:

- emergency rationale;
- approving owner or owning stage;
- deferred gate item;
- reason the gate cannot complete before publish;
- validation impact;
- risk accepted by the owner;
- follow-up artifact or issue;
- deadline or next lifecycle stage for resolution.

A deferred gate item MUST remain open in release evidence until completed, replaced by an approved recovery action, or closed by an explicit owner decision.

Emergency deferrals MUST NOT suppress failed gate evidence. If a gate ran and failed, release evidence MUST record it as failed or deferred-with-owner-risk, not as passed.

REL-R15. The release gate MUST include clean working tree proof, except for intentional release artifacts recorded in release evidence.

REL-R16. The release gate MUST include release notes or a recorded reason release notes are not required.

REL-R17. The release gate MUST include package-content preview evidence before publish.

REL-R18. The release gate MUST include generated-output currency proof before publish.

REL-R19. Generated-output currency proof MUST run `skills.drift`, `adapters.drift`, or the current equivalent generated-output drift checks named by the active release spec or plan.

REL-R20. A release MUST fail before publish when required generated-output drift checks fail.

REL-R21. The release gate MUST include the repository-owned tests, selected CI, broad smoke, or release-specific validation commands named by the active release spec or plan.

REL-R22. The release gate MUST include package build or package pack proof when the release publishes an npm package.

REL-R23. The release gate MUST include local packed-install smoke before npm publish.

REL-R24. The release gate MUST record that no unresolved release blockers remain.

REL-R25. The release gate MUST record the selected publish authentication/provenance path before publish.

REL-R26. The release gate MUST prepare the release evidence path before publish.

REL-R27. Automation MAY run the release gate, but automation MUST NOT hide or omit required release evidence.

### Release evidence

REL-R28. Every publish attempt under this process MUST create or update release evidence under `docs/releases/v<version>.md`.

REL-R29. Release evidence MUST be linked from a related change record when the release is tied to a lifecycle change.

REL-R30. Release evidence for routine publishes MUST NOT update `docs/plan.md` unless the release is part of an active lifecycle plan.

REL-R31. Routine publishes SHOULD update `docs/releases/index.md` when the release index exists or is introduced by the release-process implementation.

REL-R32. Release evidence MUST record package name, version, release type, source commit, source branch, npm dist-tag, publish path, provenance mode, and final status.

REL-R33. Release evidence MUST record the version decision rationale.

REL-R34. Release evidence MUST record preflight gate results for clean worktree, release notes, generated-output currency, validation, package preview, and local packed-install smoke.

REL-R35. Release evidence MUST summarize package contents and unexpected included or excluded files.

REL-R36. Release evidence MUST record publish command family, registry, package reference, publish time, dist-tag, and provenance status without recording secrets.

REL-R37. Release evidence MUST record post-publish registry verification for version, dist-tag, integrity metadata, fresh install smoke, and CLI/npx smoke when applicable.

REL-R38. Release evidence MUST record recovery/rollback notes for failed or partially failed release attempts.

REL-R39. Release evidence MUST NOT contain npm tokens, OTPs, credentials, private keys, private environment dumps, hostnames, usernames, or machine-local path dependencies.

REL-R40. Initial release evidence validation MUST use artifact lifecycle validation plus a release-evidence checklist.

REL-R41. A dedicated release-evidence validator MAY be added only after the evidence shape stabilizes through later approved work.

### npm publication

REL-R42. npm publication SHOULD use trusted publishing from supported CI/CD with OIDC.

REL-R43. Manual fallback MAY be used for the first release-process rollout or an approved emergency path, but manual fallback MUST NOT relax the release gate, package preview, local packed-install smoke, registry verification, or evidence requirements.

REL-R44. Release evidence MUST record why manual fallback was used.

REL-R45. Publish evidence MUST record command family, not secret-bearing command output.

REL-R46. Provenance SHOULD be automatic through trusted publishing when trusted publishing is used.

REL-R47. When trusted publishing is unavailable and supported CI/CD provenance is used, the publish path SHOULD use supported provenance generation such as `npm publish --provenance`.

REL-R48. Stable releases MUST publish to `latest`; prereleases MUST publish to a non-`latest` dist-tag unless a later approved release policy explicitly allows otherwise.

REL-R49. Staged publishing MUST NOT be required in the first release-process implementation.

REL-R50. Staged publishing MAY be proposed after trusted publishing works reliably.

### Post-publish verification

REL-R51. Post-publish verification MUST query the public registry rather than relying on local build output.

REL-R52. Post-publish verification MUST check `npm view <package>@<version> version` or the current equivalent registry query.

REL-R53. Post-publish verification MUST check that dist-tags point as intended.

REL-R54. Post-publish verification MUST check that registry integrity metadata is available when npm exposes it for the package version.

REL-R55. Post-publish verification MUST run fresh install smoke from the registry-published package unless an emergency deferral record under REL-R14a names the reason, owner approval, validation impact, and follow-up location.

REL-R56. Post-publish verification MUST run CLI or `npx` smoke when the package exposes a CLI.

### Failure and emergency behavior

REL-R57. A release attempt that fails before publish MUST stop and record failed-before-publish evidence.

REL-R58. A release attempt that fails during publish MUST record the failure and verify whether the version exists on the registry before retry.

REL-R59. A release attempt with uncertain publish outcome MUST verify registry state before any retry.

REL-R60. A release attempt that fails after publish MUST record failed-after-publish evidence.

REL-R61. A bad package-content release MUST use fix-forward and, when appropriate, deprecation or dist-tag correction.

REL-R62. A published npm version MUST NOT be overwritten by this process.

REL-R63. Emergency release evidence MUST record any gate deferrals allowed by REL-R14 and REL-R14a.

For each deferred gate, release evidence MUST record:

- deferred gate item;
- approving owner or owning stage;
- emergency rationale;
- reason for deferral;
- validation impact;
- risk accepted;
- follow-up location;
- deadline or next lifecycle stage.

Emergency evidence MUST also prove that all non-deferred gates passed and that all non-deferrable release requirements were satisfied.

REL-R64. Emergency release deferral MUST NOT remove the requirement to record release evidence and post-publish registry verification.

### Non-deferrable release requirements

REL-R65. Emergency release handling MUST NOT defer release evidence creation.

REL-R66. Emergency release handling MUST NOT defer secret, token, OTP, credential, private environment, and machine-local path suppression.

REL-R67. Emergency release handling MUST NOT defer source commit and package version recording.

REL-R68. Emergency release handling MUST NOT defer npm package name and dist-tag recording when npm publication applies.

REL-R69. Emergency release handling MUST NOT defer publish path recording.

REL-R70. Emergency release handling MUST NOT defer post-publish registry verification.

REL-R71. Emergency release handling MUST NOT defer recovery or follow-up recording for deferred gates.

REL-R72. Fresh install smoke MAY be deferred only when the emergency record names the reason, owner approval, validation impact, and follow-up location. Registry verification itself remains mandatory.

## Inputs and outputs

Inputs:

- accepted release-process contract proposal;
- already-reviewed release candidate source;
- selected version and release type;
- package name and package root when npm publication applies;
- release notes or a recorded not-required rationale;
- generated-output drift checks named by the active release spec or plan;
- release validation commands named by the active release spec or plan;
- npm publish path: `trusted-publishing`, `manual-token`, `manual-2fa`, or later approved mode.

Outputs:

- `docs/releases/v<version>.md` release evidence;
- optional `docs/releases/index.md` release index update;
- change-record link to release evidence when applicable;
- package preview evidence;
- local packed-install smoke evidence;
- publish event evidence;
- registry verification evidence;
- recovery or rollback notes when applicable.

## State and invariants

- Routine publish is an operation, not a new product decision.
- Release-process changes remain lifecycle-managed changes.
- Release evidence is version-scoped durable proof under `docs/releases/v<version>.md`.
- `docs/plan.md` remains a lifecycle index and is not a routine release ledger.
- Generated output is proven current by drift checks or current equivalent generated-output validation, not by assertion.
- Published npm versions are immutable for this process and are recovered by fix-forward, deprecation, or dist-tag correction.
- Release evidence never stores secrets or private machine state.

## Error and boundary behavior

- If the release gate fails, publish MUST stop.
- If generated-output currency cannot be proven, publish MUST stop unless a later approved spec records a different authoritative generated-output boundary.
- If the selected version already exists on npm, publish MUST stop and release evidence MUST record whether this is a duplicate attempt, recovery attempt, or no-op.
- If package preview contains unexpected required omissions or forbidden inclusions, publish MUST stop.
- If local packed-install smoke fails, publish MUST stop.
- If npm authentication, 2FA, provenance, or network failure occurs during publish, release evidence MUST record the failure without recording secrets.
- If post-publish registry verification fails, the release MUST be marked failed-after-publish until corrected or explained through recovery notes.
- If a release is tied to an active lifecycle plan, the plan surfaces MUST follow the governing workflow closeout rules in addition to this release evidence contract.

## Compatibility and migration

This spec is forward-looking for routine releases after approval. Historical releases remain valid as historical records even when they lack this spec's evidence shape.

The first implementation may use manual fallback while trusted publishing is configured, but must preserve the full release gate and registry verification. Staged publishing, automated release CLI, dedicated release-evidence validation, release announcement automation, and backport/LTS policy remain follow-on work unless later approved.

Release-specific specs may impose stricter requirements for a named package, version, adapter surface, or release line. They must not weaken this standing release process without an approved release-process change.

Rollback for this process is to revise the release-process spec through the normal lifecycle. Rollback of an already-published bad package uses fix-forward, dist-tag correction, or deprecation; it does not overwrite the published version.

## Observability

- Release evidence MUST be sufficient to reconstruct version, release type, source commit, package, dist-tag, gate result, generated-output proof, package preview, publish event, registry result, smoke result, and recovery notes.
- Release evidence SHOULD record concise command/result summaries rather than large logs.
- Release evidence SHOULD include links or references to CI runs when CI was used, but external CI logs MUST NOT be the only durable proof.
- Validation output SHOULD identify which release-gate checks passed, failed, or were deferred under emergency approval.
- Release evidence MUST identify `trusted-publishing`, `manual-token`, `manual-2fa`, or approved equivalent publish path without exposing credentials.

## Security and privacy

- Release evidence MUST NOT include tokens, OTPs, credentials, private keys, private environment dumps, private registry credentials, hostnames, usernames, home-directory paths, or machine-local temporary paths.
- Manual fallback MUST preserve npm 2FA and token policy requirements and MUST NOT record OTPs.
- Long-lived npm tokens SHOULD NOT be the default publication path.
- Trusted publishing SHOULD be preferred because it avoids long-lived publish tokens.
- Release commands and validators SHOULD redact or omit secret-bearing environment and npm auth output.
- Package preview and release evidence MUST treat unexpected secret-bearing files as release blockers.

## Accessibility and UX

No end-user UI is introduced by this spec.

Contributor-facing release evidence and release index entries SHOULD use stable headings, concise tables, and command/result summaries so maintainers can inspect release state without reading full logs.

## Performance expectations

- Release validation MAY be slower than ordinary inner-loop validation because it is a publication gate for immutable public artifacts.
- Release evidence SHOULD remain concise enough for review; large command logs SHOULD be linked or summarized rather than pasted wholesale.
- Release gate automation SHOULD avoid redundant generated-output or package-build work when repository-owned validation can safely reuse exact prior evidence, but such caching MUST NOT weaken required release proof.

## Edge cases

EC1. A routine publish includes a breaking change that already completed upstream lifecycle: the publish can be routine, but release evidence must identify the major release decision and upstream approval path.

EC2. A maintainer discovers the npm version already exists before publish: the attempt stops and evidence records no publish, unless this is an approved recovery attempt after an earlier failed/uncertain publish.

EC3. Trusted publishing is configured but unavailable during first rollout: manual fallback may be used only with full gate evidence and recorded reason.

EC4. A release publishes successfully but registry integrity metadata is temporarily unavailable: evidence records the failed check and the release remains failed-after-publish until follow-up verification records the final state or an approved rationale.

EC5. Generated adapter archives are release-output rather than tracked source: evidence records the authoritative generated-output boundary and validates temporary or release-output artifacts.

EC6. A release is both a routine publish and part of an active lifecycle plan: release evidence is still written under `docs/releases/v<version>.md`, and the active plan is updated only as required by the lifecycle plan.

EC7. A release is an emergency: deferred gates require owner approval and evidence under REL-R14a and REL-R63, but registry verification and secret suppression remain required.

EC8. A routine release has no package-preview evidence: the release is blocked, publish must not proceed, and emergency deferral rules do not apply.

EC9. An emergency release defers fresh registry install smoke because the registry install path is temporarily unavailable after publication: publish may proceed only when release evidence records approving owner, emergency rationale, deferred gate item, validation impact, risk accepted, follow-up location, deadline, all non-deferred gates passed, and post-publish registry verification passed. Release evidence status remains emergency-with-deferred-gate until follow-up closes.

EC10. A release evidence record defers post-publish registry verification: validation fails because registry verification is non-deferrable.

EC11. A deferred gate is listed without approving owner or validation impact: validation fails and publish must not proceed under the emergency exception.

## Non-goals

- Do not define new package contents, CLI behavior, public skill behavior, adapter layout, lockfile semantics, or release archive trust boundaries.
- Do not define deployment for non-npm infrastructure.
- Do not define backport/LTS policy.
- Do not require full proposal/spec/plan ceremony for each routine publish.
- Do not build a fully automated release CLI in this spec.
- Do not require staged publishing in the first release-process implementation.
- Do not backfill historical release evidence.
- Do not use external CI logs as the only durable release evidence.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-REL-001 | The spec defines the release process as a standing contract. |
| AC-REL-002 | Routine publishes are allowed to execute the standing process without new proposal/spec/plan when no new decision is introduced. |
| AC-REL-003 | Release-process changes are lifecycle-managed and cannot be smuggled into routine publish operations. |
| AC-REL-004 | Version, release type, and dist-tag are recorded before publish. |
| AC-REL-005 | Routine releases pass the full release gate before publish. Emergency releases may publish with deferred gate items only when release evidence satisfies REL-R14, REL-R14a, and REL-R63; non-deferred gates, non-deferrable release requirements, and post-publish registry verification remain mandatory. |
| AC-REL-006 | Generated-output currency is proven by drift checks or current equivalents. |
| AC-REL-007 | Package preview and local packed-install smoke are recorded before npm publish. |
| AC-REL-008 | Trusted publishing is preferred, manual fallback is allowed for first rollout/emergency, and neither path relaxes the gate. |
| AC-REL-009 | Post-publish registry verification records version, dist-tag, integrity metadata, and fresh install/CLI smoke. |
| AC-REL-010 | Release evidence exists at `docs/releases/v<version>.md` for every publish attempt. |
| AC-REL-011 | Release evidence contains no secrets or private machine state. |
| AC-REL-012 | Failed-before, failed-during, and failed-after publish states have distinct recovery behavior. |
| AC-REL-013 | Bad published package content uses fix-forward, deprecation, or dist-tag correction, not overwrite. |
| AC-REL-014 | Routine release evidence does not update `docs/plan.md` unless tied to an active lifecycle plan. |

## Open questions

None.

## Next artifacts

```text
spec-review
test-spec
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Approved after `spec-review-r2`.
