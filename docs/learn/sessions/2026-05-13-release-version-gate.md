# Release Version Gate Learn Session

## Frame

- Trigger: explicit maintainer invocation asking why `scripts/release-verify.sh` needs the release version name added and what best practices apply.
- Trigger type: maintainer request / review-finding retrospective.
- Scope:
  - `CR-M1-1` from the v0.1.3 generated public adapter skill-body untracking work.
  - M1 implementation and accepted review-finding fix.
  - Release-gate design around version-specific release contracts.
- Evidence reviewed:
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/reviews/code-review-m1-r1.md`
  - `docs/changes/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies/review-resolution.md`
  - commits `4503926` and `70a5440`
  - `scripts/release-verify.sh`
  - `scripts/test-adapter-distribution.py`
  - prior session `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md`
- Explicit exclusions:
  - This session does not claim M1 code-review rerun, PR readiness, final verification, release publication, or CI status.
  - This session does not create new authoritative release policy.
  - This session does not update release tooling beyond recording the lesson.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/learn/topics/token-cost-measurement.md`

## Observe

### O1: The version allowlist is a release-contract guard, not just duplication

`scripts/release-verify.sh` rejects unsupported release tags before running release checks. That is useful because release gates are not generic smoke tests: each published version can have a different validation contract, artifact model, compatibility boundary, and evidence shape.

For `v0.1.3`, the release contract changed. The gate had to stop treating tracked `dist/adapters/<adapter>/` package trees as the adapter proof surface and instead build/validate release archives with `--release-output-dir` and `--release-commit`.

The original M1 implementation added `v0.1.3` to `validate_release_output()` but not to the maintainer-facing shell gate. That created `CR-M1-1`: direct validation supported the new version, but `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` still failed as unsupported.

### O2: Version-specific behavior should be explicit, but not scattered

Adding `v0.1.3` to the script was necessary because the script intentionally maintains a supported-release allowlist and command contract. The problem was not "version name appears in a script." The problem was that release-version behavior was split across several places:

- `scripts/adapter_distribution.py` had `RELEASE_TARGETS` and v0.1.3 validation behavior.
- `scripts/release-verify.sh` had its own supported-target case statement and command list.
- Tests initially covered direct validator behavior but not the shell release gate for v0.1.3.

The fix added the missing shell-gate behavior and a dry-run regression test.

### O3: Best practice is release profiles, with fail-closed unsupported versions

Release gates should fail closed for unsupported release tags. They should not infer a new release contract from a version string alone when artifact semantics changed.

For a small script, an explicit case statement or table is acceptable. As version-specific branches grow, the safer shape is a single release profile map or config object that centralizes:

- supported release tag;
- adapter manifest version;
- whether tracked adapter drift checks are required;
- whether release archives are required;
- how release output is generated;
- whether `--release-commit` is required and where it comes from;
- required validation commands.

That profile should have regression tests for each supported release and for each contract transition.

### O4: New release artifact models need end-to-end gate tests

The earlier PR CI incident already showed that release artifact changes are easy to validate in one layer while missing another layer. `CR-M1-1` is the same class at a smaller scale: the direct validator was updated, but the maintainer-facing release gate was not.

For release migrations, tests must cover the public/final command the maintainer runs, not only the helper function it delegates to.

## Classify

| Observation | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record | evidence from `CR-M1-1` and fix commit | Explains why the version appears in the script. |
| O2 | durable-lesson candidate | pending confirmation | possible future release tooling refactor proposal if this repeats | pending contributor confirmation | The evidence shows a reusable pattern, but this session should not create new release policy by itself. |
| O3 | durable-lesson candidate | pending confirmation | possible topic entry or release tooling spec/ADR if accepted | pending contributor confirmation | Best-practice guidance is plausible and evidence-backed, but routing needs confirmation. |
| O4 | durable-lesson candidate | pending confirmation | may reinforce prior CI/release validation lesson | pending contributor confirmation | Evidence overlaps with the prior PR CI incident and this review finding. |

## Route

- Session record created: `docs/learn/sessions/2026-05-13-release-version-gate.md`.
- No topic file updated in this session.
- No authoritative artifact updated in this session.
- Candidate durable guidance pending contributor confirmation:
  - When a release changes artifact semantics, update the maintainer-facing release gate and add a direct gate-level dry-run test in the same slice.
  - Keep release gates fail-closed with explicit supported targets, but centralize version behavior into a release profile/table when branches grow.

## Practical answer

We add the version name inside `scripts/release-verify.sh` because the script is the maintainer-facing final release gate. It should fail closed for unknown release tags and should only run the validation sequence that is explicitly approved for that release contract.

For `v0.1.3`, the release contract is not the same as `v0.1.2`:

- `v0.1.2` introduced archives while keeping tracked repository-tree adapter packages.
- `v0.1.3` retires tracked generated adapter package bodies and validates adapters from release-output archives.

So `v0.1.3` needed explicit script behavior:

- accept the tag;
- build or use a release-output directory;
- pass `--release-output-dir` and `--release-commit`;
- skip tracked adapter package drift checks.

Best practice:

1. Fail closed for unsupported release tags.
2. Make version-specific release contracts explicit.
3. Keep the version behavior centralized, preferably as a release profile/table once the script has more than a couple branches.
4. Add a dry-run test for the exact maintainer command.
5. Avoid only testing helper functions when the actual release entrypoint is a shell gate.
6. Refactor when duplication starts hiding required changes; do not prematurely make every release infer behavior from naming conventions.

## Validation

No validation commands were run for this session beyond evidence inspection. The session adds only this Markdown record.
