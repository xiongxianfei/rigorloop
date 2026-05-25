# Proposal Review: Target-Native Init Commands and Adapter Terminology Retirement

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review
Target: docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md
Status: changes-requested

## Review Inputs

- Proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- User direction: publish 0.3.0, remove `--adapter` totally, accept only `codex`, `claude`, and `opencode`, make default init install-only, add `--write-state` for state files, use packed smoke before publish and live smoke after publish.
- Governance: `AGENTS.md`, `CONSTITUTION.md`, `docs/workflows.md`
- Related current specs named by the proposal: `specs/multi-adapter-init-and-proxy-aware-download.md`, `specs/rigorloop-cli-lockfile.md`

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: `TINIT-PR1-F1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: `TINIT-PR1-F1`
- Immediate next stage: proposal revision
- Eventual spec readiness: not-ready
- Stop condition: revise the proposal and rerun proposal-review before spec, test-spec, plan, or implementation relies on the state-file terminology boundary.
- No automatic downstream handoff: this review is isolated and does not start spec, plan, test-spec, or implementation work.

## Material Findings

### TINIT-PR1-F1 - State-file key terminology boundary conflicts across sections

Finding ID: TINIT-PR1-F1
Severity: major
Location: `Public Terminology Boundary`; `Non-goals`; `Scope Budget`; `Managed State Direction`; `Internal Naming Boundary`; `Architecture Impact`; `Decision Log`.
Evidence: The public terminology boundary says "Internal code names, archive filenames, release metadata field names, lockfile keys, and historical evidence may continue to use `adapter` until a separate compatibility-sensitive migration is approved." The same proposal later says user-visible state keys in `rigorloop.yaml` and `rigorloop.lock` "should not continue to use `adapter`" and that the first-slice boundary is to "rename user-visible state-file keys away from adapter." The scope budget and decision log also classify user-visible manifest and lockfile key renaming as in-scope for this proposal. The non-goals entry "Do not rename internal `dist/adapters/`, archive filename, lockfile, or manifest implementation surfaces" can be read as excluding the same state schema work unless "implementation surfaces" is narrowed.
Required outcome: The proposal must consistently state whether `rigorloop.yaml` and `rigorloop.lock` user-visible keys are renamed in v0.3.0, and must distinguish that from non-user-visible internals that remain deferred.
Safe resolution path: Edit `Public Terminology Boundary` to remove "lockfile keys" from the deferred internal list or qualify it as non-user-visible/historical internals only. Edit the non-goals line to say non-user-visible internal `dist/adapters/`, archive filenames, package-bundled metadata fields, and implementation names are deferred, while `--write-state` user-visible state-file schema keys are in scope for target-oriented names. Keep the Scope Budget, Internal Naming Boundary, Architecture Impact, tests, and Decision Log aligned on that boundary.
needs-decision rationale: The proposal owner must confirm the first-slice boundary for `rigorloop.yaml` and `rigorloop.lock` keys before spec authors can define the 0.3.0 state-file contract.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly separates UX terminology, release-smoke gaps, and default state-file friction. |
| User value | pass | The value is concrete: shorter target-native commands, no default state files to remove, and stronger release validation. |
| Option diversity | pass | The proposal considers keeping `--adapter`, documented alias, deprecated alias, hard removal, top-level target commands, and state-file defaults. |
| Decision rationale | concern | The 0.3.0 hard-removal and install-only decisions are well motivated, but state-file key migration rationale is contradicted by the public terminology boundary. |
| Scope control | concern | Scope is generally well bounded, but the lockfile/manifest key boundary is ambiguous enough to block downstream reliance. |
| Architecture awareness | concern | The proposal recognizes release metadata, archive names, and state schemas as different surfaces, but one section collapses lockfile keys into deferred internals. |
| Testability | pass | The proposed command, docs, smoke, metadata, and state-file checks are testable. |
| Risk honesty | pass | Compatibility, metadata drift, dry-run smoke, docs drift, and full internal rename churn are named. |
| Rollout realism | pass | Packed pre-publish and live post-publish gates are realistic and correctly separate immutable npm publish risk from post-publish evidence. |
| Readiness for spec | block | Spec should wait until `TINIT-PR1-F1` is resolved because it determines the observable state-file schema. |

## Scope Preservation

Initial user goals are preserved:

- Use `init codex`, `init claude`, and `init opencode` directly: in scope.
- Remove `--adapter` totally for 0.3.0: in scope.
- Accept only `codex`, `claude`, and `opencode`: in scope.
- Show `@latest` for manual quick start and pinned versions for automation: in scope.
- Use packed smoke before publish and live registry/download smoke after publish: in scope.
- Avoid default `rigorloop.yaml` and `rigorloop.lock`: in scope.
- Add `--write-state`: in scope.
- Preserve existing state by default and overwrite with `--write-state`: in scope.
- Avoid full internal rename unless necessary: in scope, but state-file user-visible keys need the consistency fix above.

## Recommended Edits

- Remove or qualify the sentence saying "lockfile keys" may continue to use `adapter` until a separate migration.
- Narrow the non-goal about "lockfile, or manifest implementation surfaces" so it does not contradict the in-scope rename of user-visible `rigorloop.yaml` and `rigorloop.lock` keys.
- Keep the first-slice boundary phrasing consistent everywhere: public CLI/docs and user-visible state-file keys use target terminology; non-user-visible internal adapter paths/archive filenames/package-bundled metadata fields stay deferred.
- After revision, rerun proposal-review before writing or amending the specs.

## Recommendation

Changes requested. The proposal is directionally strong and preserves the user's requested product decisions, but it should not advance to spec until `TINIT-PR1-F1` is resolved.
