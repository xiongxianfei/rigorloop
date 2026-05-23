# Release v<version>

## Result

- Package: <name>
- Version: <version>
- Release type: <patch | minor | major | prerelease | hotfix | emergency>
- Routine publish: <yes | no>
- No new decision introduced: <yes | no>
- Source commit: <commit>
- Source branch: <branch>
- npm dist-tag: <tag>
- Publish path: <trusted-publishing | manual-token | manual-2fa | staged | not-published>
- Provenance: <automatic | --provenance | unavailable | not-used with reason>
- Status: <published | failed-before-publish | failed-during-publish | failed-after-publish | emergency-with-deferred-gate | rolled-back | deprecated | not-published>

## Related Lifecycle Evidence

- Related change record: <docs/changes/<change-id>/ or not-applicable>
- Upstream lifecycle approval: <path or not-applicable>
- Release-specific evidence: <docs/releases/<version>/release.yaml or not-applicable>
- Release notes: <docs/releases/<version>/release-notes.md or not-required with reason>

## Version Decision

Record why this version number and dist-tag are correct.

- Change summary: <summary>
- Version decision: <patch | minor | major | prerelease | no-op blocked>
- Dist-tag decision: <latest | next | beta | alpha | other>
- No-op check: <pass | fail with reason>
- Existing npm version check: <not-found | exists-blocked | not-applicable>

## Routine Publish Boundary

| Check | Result | Evidence |
| --- | --- | --- |
| release type recorded | <pass/fail> | <value> |
| no new product or implementation decision | <pass/fail> | <reason> |
| no release-process change | <pass/fail> | <reason> |
| no package name/scope change | <pass/fail/not-applicable> | <reason> |
| no adapter target/install-root change | <pass/fail/not-applicable> | <reason> |
| upstream breaking change approval | <pass/fail/not-applicable> | <path> |

## Preflight Gate

| Check | Result | Evidence |
| --- | --- | --- |
| clean worktree except intentional release artifacts | <pass/fail> | <command/result> |
| release notes or not-required rationale | <pass/fail/not-required> | <path/reason> |
| generated output current | <pass/fail> | <command/result> |
| tests / selected CI / broad smoke | <pass/fail> | <command/result> |
| package build or pack proof | <pass/fail/not-applicable> | <command/result> |
| package preview | <pass/fail> | <command/result> |
| local packed-install smoke | <pass/fail/not-applicable> | <command/result> |
| no unresolved release blockers | <pass/fail> | <evidence> |
| publish path selected | <pass/fail> | <value> |
| evidence path prepared | <pass/fail> | <path> |

Generated-output currency must be proven by repository-owned checks such as `skills.drift`, `adapters.drift`, `scripts/build-skills.py --check`, `scripts/build-adapters.py --check`, adapter archive validation, or the current equivalent named by the active release plan/spec.

## Package Contents

Summarize `npm pack --dry-run`, `npm pack`, or equivalent package preview.

- Package filename: <filename or not-applicable>
- Package size: <size or not-recorded>
- Integrity or checksum: <value or not-recorded>
- Included-file review: <summary>
- Unexpected inclusions: <none or summary>
- Unexpected exclusions: <none or summary>
- Secret-bearing file check: <pass/fail>

## Publish Event

- Command family: <npm publish | npm publish --provenance | trusted publishing workflow | not-published>
- Registry: <npm | not-published>
- Package reference: <package>@<version>
- Published at: <timestamp or not-published>
- Dist-tag: <tag or not-published>
- Provenance status: <automatic | --provenance | unavailable | not-used with reason>
- Manual fallback reason: <reason or not-applicable>

Do not include tokens, OTPs, credentials, private environment values, private hostnames, usernames, or machine-local paths.

## Registry Verification

| Check | Result | Evidence |
| --- | --- | --- |
| registry version query | <pass/fail/not-run> | <command/result> |
| dist-tag points correctly | <pass/fail/not-run> | <command/result> |
| integrity metadata available | <pass/fail/not-run> | <command/result> |
| fresh registry install smoke | <pass/fail/deferred/not-applicable> | <command/result or deferral> |
| CLI or npx smoke | <pass/fail/deferred/not-applicable> | <command/result or deferral> |

Registry verification is non-deferrable for emergency releases. Fresh install smoke may be deferred only under the emergency deferral contract.

## Emergency Deferrals

Use `none` for routine releases with no emergency deferrals.

| Deferred gate item | Approving owner or owning stage | Rationale | Reason pre-publish completion was impossible | Validation impact | Risk accepted | Follow-up location | Deadline or next lifecycle stage | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <item or none> | <owner/stage> | <reason> | <reason> | <impact> | <risk> | <path/issue> | <deadline/stage> | <open/completed/replaced/closed-by-owner> |

Failed gate evidence must remain visible as failed or deferred-with-owner-risk, not rewritten as passed.

Emergency release handling must not defer:

- release evidence creation;
- secret, token, OTP, credential, private environment, and machine-local path suppression;
- source commit and package version recording;
- npm package name and dist-tag recording when npm publication applies;
- publish path recording;
- post-publish registry verification;
- recovery or follow-up recording for deferred gates.

## Recovery / Rollback Notes

- Failure phase: <none | failed-before-publish | failed-during-publish | uncertain-publish-outcome | failed-after-publish>
- Registry state checked before retry: <pass/fail/not-applicable>
- Recovery action: <none | retry-before-publish | fix-forward | dist-tag correction | deprecate | owner-approved rationale>
- Published version overwrite attempted: no
- Notes: <summary>

## Follow-up

- Release announcement: <path/status or none>
- Deferred gate follow-up: <path/status or none>
- Deprecation or dist-tag follow-up: <path/status or none>
- Next release follow-up: <path/status or none>

## Evidence Safety Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| no npm tokens | <pass/fail> | <review/result> |
| no OTPs | <pass/fail> | <review/result> |
| no credentials or private keys | <pass/fail> | <review/result> |
| no private environment dumps | <pass/fail> | <review/result> |
| no hostnames or usernames | <pass/fail> | <review/result> |
| no home-directory or machine-local temp paths | <pass/fail> | <review/result> |
| command output summarized instead of pasted wholesale | <pass/fail> | <review/result> |
