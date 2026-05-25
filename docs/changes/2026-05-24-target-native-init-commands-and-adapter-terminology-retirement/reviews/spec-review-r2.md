# Spec Review R2: Target-Native Init

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex spec-review
Target: specs/target-native-init.md
Status: approved

## Review Inputs

- Revised spec: `specs/target-native-init.md`
- R1 review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r1.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Accepted proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`

## Result

- Skill: spec-review
- Review status: approved
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: none
- Immediate next stage: architecture or plan, if architecture is not required by the next workflow decision

## Findings

No material findings.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | pass | Dry-run planning, target-native commands, state-file schemas, and default-init safety parsing are explicit. |
| normative language | pass | MUST/MAY requirements are testable and no longer conflict on dry-run state planning or state-file terminology. |
| completeness | pass | The spec covers command surface, install behavior, state schemas, metadata verification, release smoke, docs, and migration behavior. |
| testability | pass | Requirements can be mapped to CLI tests, docs sweeps, metadata checks, and packed/live smoke tests. |
| examples | pass | Examples cover default init, `--write-state`, removed `--adapter`, opencode, dry-run smoke limits, and legacy state. |
| compatibility | pass | Legacy state files, older lockfile schemas, `0.2.x` rollback, and deferred internal names are addressed. |
| observability | pass | JSON output, human output, state-file actions, verification failures, and release evidence are specified. |
| security/privacy | pass | Trusted metadata, official URLs, extraction safety, state-file secrecy, and diagnostic privacy are preserved. |
| non-goals | pass | Internal archive/path renames, target aliases, repair commands, and dry-run-only release smoke remain out of scope. |
| acceptance criteria | pass | Acceptance criteria now align with dry-run behavior, schema-key terminology, and malformed-state safety. |

## R1 Closeout

- `TNI-SR1` resolved: dry-run reports state-file plans only when state writes are in scope, while default dry-run remains install-only.
- `TNI-SR2` resolved: target-oriented schema-key requirements now distinguish prohibited adapter-oriented keys from allowed historical archive filename values.
- `TNI-SR3` resolved: default init preserves state files byte-for-byte but performs safety parsing before target-root mutation, and malformed or ambiguous state blocks non-dry-run mutation.

## Eventual test-spec readiness

ready

## Stop condition

None. This review is isolated and does not automatically start architecture, plan, test-spec, or implementation work.
