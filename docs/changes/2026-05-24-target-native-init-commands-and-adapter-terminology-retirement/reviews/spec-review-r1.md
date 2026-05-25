# Spec Review R1: Target-Native Init

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/target-native-init.md
Status: changes-requested

## Review Inputs

- Spec: `specs/target-native-init.md`
- Accepted proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Proposal-review approval: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/proposal-review-r3.md`
- Current related specs: `specs/multi-adapter-init-and-proxy-aware-download.md`, `specs/rigorloop-cli-lockfile.md`, `specs/rigorloop-cli-package-and-codex-init.md`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `TNI-SR1`, `TNI-SR2`, `TNI-SR3`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: `TNI-SR1`, `TNI-SR2`, `TNI-SR3`
- Immediate next stage: spec revision

## Findings

## Finding TNI-SR1

Finding ID: TNI-SR1
Severity: major
Location: `Dry-run, JSON, and output`, TNI-R65 through TNI-R67.
Evidence: TNI-R65 says "`--dry-run` MUST report planned target-root writes and planned state-file writes without mutating files." TNI-R66 says default `rigorloop init <target> --dry-run --json` "MUST NOT report planned creation or update of `rigorloop.yaml` or `rigorloop.lock`." TNI-R67 separately requires planned state-file content for `--write-state --dry-run --json`. Read literally, TNI-R65 requires planned state-file writes for every dry-run, while TNI-R66 forbids them for default dry-run.
Required outcome: Make the dry-run state-file planning requirements internally consistent for default init and `--write-state`.
Safe resolution path: Revise TNI-R65 so it says dry-run reports planned state-file writes only when state-file writes are in scope for the requested command, such as `--write-state`. Keep TNI-R66 requiring default dry-run to omit planned state-file creation/update, and keep TNI-R67 requiring `--write-state --dry-run --json` to report planned target-oriented state-file content.
needs-decision rationale: none

## Finding TNI-SR2

Finding ID: TNI-SR2
Severity: major
Location: `State-file schemas`, TNI-R43, TNI-R44, TNI-R57; Acceptance criteria AC-TNI-008.
Evidence: TNI-R43 and TNI-R44 say new state-file content written by `--write-state` "MUST NOT use `adapter` or `adapters`." TNI-R57's required lockfile shape includes archive filename values such as `rigorloop-adapter-codex-v0.3.0.zip` and `rigorloop-adapter-opencode-v0.3.0.zip`. The accepted proposal defers archive filename renaming as a non-user-visible internal/archive concern, while AC-TNI-008 correctly narrows the check to user-visible `adapter` or `adapters` keys.
Required outcome: Clarify that target-oriented state-file requirements prohibit user-visible schema keys named `adapter` or `adapters`, while allowing explicitly permitted historical archive filename values.
Safe resolution path: Revise TNI-R43, TNI-R44, AC-TNI-008, and any related examples to distinguish schema keys from values. State that new state-file schemas must not use `adapter` or `adapters` as user-visible keys, while archive filename values may retain historical names until a separate internal archive rename is approved.
needs-decision rationale: none

## Finding TNI-SR3

Finding ID: TNI-SR3
Severity: major
Location: `Install behavior`, TNI-R15 through TNI-R17; `State-file schemas`, TNI-R59 through TNI-R64; `Error and boundary behavior`, item 11; edge cases EC4 through EC9.
Evidence: TNI-R15 through TNI-R17 require default init to preserve `rigorloop.yaml` and `rigorloop.lock` byte-for-byte. Error behavior item 11 says default init preserves malformed state files unchanged "unless the malformed state is needed to make a safe mutation decision." TNI-R60 says default init preserves legacy state files unchanged, while TNI-R61 through TNI-R63 define migration behavior only for `--write-state`. The spec does not define when default install-only init must parse existing state to detect drift/conflicts before mutating target roots, or whether malformed state blocks default init when target roots already exist.
Required outcome: Define when default install-only init must parse existing state files for mutation safety, and how malformed or ambiguous state affects default init.
Safe resolution path: Add requirements that separate byte preservation from safety checks. For example, default init must not write state files, but when an existing state file records the selected target or an install root that would be mutated, the CLI must parse enough valid state to detect drift/conflicts before replacement. Define whether malformed state blocks only when the selected target/root is implicated, or always blocks when any target root mutation is planned. Keep the chosen rule testable for malformed manifest, malformed lockfile, selected target drift, unrelated target entries, and no existing target root.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most command and release-smoke requirements are clear, but dry-run and default-init state parsing need revision. |
| normative language | concern | The spec uses testable MUST language, but TNI-R65 conflicts with TNI-R66 and TNI-R43/TNI-R44 overreach relative to archive filename values. |
| completeness | concern | The spec covers command syntax, targets, state schemas, metadata verification, docs, and smoke gates; default-init malformed-state behavior is incomplete. |
| testability | concern | Tests cannot unambiguously assert default dry-run planned state-file fields or malformed-state default-init behavior until findings are resolved. |
| examples | pass | Examples cover normal default init, managed state, removed `--adapter`, opencode, dry-run release-smoke limits, and legacy state. |
| compatibility | concern | Legacy state files are recognized, but default install-only behavior around malformed or drifted state needs a precise rule. |
| observability | pass | JSON, human output, verification failure categories, and release evidence surfaces are named. |
| security/privacy | pass | Trusted metadata, archive URL trust, extraction safety, state-file secrecy, and diagnostic privacy are covered. |
| non-goals | pass | Non-goals preserve skill behavior, defer internal archive/path renames, reject aliases, and exclude repair commands. |
| acceptance criteria | concern | AC-TNI-008 is better scoped than TNI-R43/TNI-R44; acceptance criteria need alignment after spec revision. |

## Eventual test-spec readiness

not-ready

The test spec should wait until dry-run state-file planning, state-file key/value terminology, and default-init state parsing behavior are revised and reviewed.

## Stop condition

Revise the spec to resolve `TNI-SR1`, `TNI-SR2`, and `TNI-SR3`, then rerun spec-review before architecture, plan, test-spec, or implementation relies on `specs/target-native-init.md`.
