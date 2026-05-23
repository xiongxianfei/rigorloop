# Release Process Dry-Run Rehearsal

## Status

not a release

## Scope

This rehearsal proves the standing release-process gate can be executed in dry-run mode for the current historical npm release target without publishing a package.

Command:

```bash
RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.5
```

Result: pass.

No npm package was published. No tag, dist-tag, registry state, release evidence record, or public artifact was changed by this rehearsal.

## Standing Gate Coverage

The dry-run output explicitly recorded the standing release-process boundaries:

- generated-output currency must be proven by repository-owned drift/build/release-output checks;
- package preview and packed install smoke must prove package contents before publish;
- trusted publishing is preferred, and manual fallback requires release evidence;
- post-publish registry verification must cover npm view version, dist-tags, integrity, and fresh install or npx smoke;
- dry-run mode executes no publish command.

## Commands Rehearsed

The release gate selected these repository-owned checks:

| Gate item | Rehearsed command family |
| --- | --- |
| canonical skills | `python scripts/validate-skills.py` |
| skill regression | `python scripts/test-skill-validator.py` |
| generated skill drift | `python scripts/build-skills.py --check` |
| adapter distribution regression | `python scripts/test-adapter-distribution.py` |
| package preview / packed install smoke | `python scripts/test-npm-package-publication.py` |
| adapter release archives | `python scripts/build-adapters.py --version v0.1.5 --output-dir <temp-dir>` |
| release metadata / adapter artifacts / smoke / notes / security | `python scripts/validate-release.py --version v0.1.5 --release-output-dir <temp-dir> --release-commit <metadata-source-commit>` |

## Publication Boundary

The rehearsal did not run `npm publish`, `npm publish --provenance`, GitHub trusted publishing, staged publishing, `npm dist-tag`, or any registry write.

Registry verification was named as a post-publish requirement, but no live registry verification was performed because this was not a publish operation.

## Safety Review

- Tokens, OTPs, credentials, private environment dumps, hostnames, usernames, and machine-local paths are not recorded here.
- Temporary paths from the dry-run command are summarized as `<temp-dir>`.
- The release commit is summarized as `<metadata-source-commit>`.
- Command output is summarized rather than copied wholesale.

## Follow-up

Use this rehearsal as implementation evidence for the standing release-process contract. It is not release evidence for a real package version.
