# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/stop-tracking-generated-public-adapter-skill-bodies.md
Reviewed artifact: specs/stop-tracking-generated-public-adapter-skill-bodies.md
Review date: 2026-05-13
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Outcome

- Review status: changes-requested
- Material findings: SGPA-SR1
- Blocking findings: none

## Review Inputs

- Spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Proposal: `docs/proposals/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Prior adapter specs: `specs/multi-agent-adapters-first-public-release.md`, `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Governing guidance: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Findings

### SGPA-SR1 - Cross-spec supersession is not explicit

Finding ID: SGPA-SR1
Severity: major
Location: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`, missing relationship to prior approved adapter-package specs.

Evidence: The spec requires tracked files under `dist/adapters/` to be limited to `dist/adapters/README.md` and `dist/adapters/manifest.yaml`, and requires generated adapter instruction entrypoints, opencode command wrappers, and skill bodies not to remain tracked package fragments. Earlier approved adapter specs define `dist/adapters/<adapter>/` as generated tracked adapter packages and require validation to fail when generated adapter packages are missing or stale. The new spec does not state which prior tracked-package requirements are superseded for `v0.1.3` and later.

Required outcome: The spec must explicitly define its relationship to earlier approved adapter specs before downstream architecture, planning, or test-spec work relies on it.

Safe resolution path: Add a `Relationship to prior adapter specs` section that says this spec supersedes the tracked-package and repository-tree install requirements from `specs/multi-agent-adapters-first-public-release.md` and the compatibility-window portions of `specs/public-adapter-artifact-migration-examples-concise-skill-release.md` for `v0.1.3` and later, while preserving adapter support, generated output validation, release archive generation, metadata, checksums, and smoke/validation obligations through temporary or release-output artifacts.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most requirements are precise, but cross-spec precedence is ambiguous. See SGPA-SR1. |
| Normative language | pass | The spec uses testable `MUST`, `SHOULD`, and `MUST NOT` language. |
| Completeness | concern | Normal, release, guidance, token-cost, rollback, and boundary cases are covered; prior-spec migration needs explicit settlement. |
| Testability | pass | Requirements map to tracked-file checks, temp-output validation, archive validation, root-guidance audit, token-cost validation, and release verification. |
| Examples | pass | Examples are concrete and align with the requirements. |
| Compatibility | concern | Compatibility is addressed for users and release phases, but not enough for prior approved spec requirements. See SGPA-SR1. |
| Observability | pass | Release validation, root-guidance audit, metadata paths, and token-cost source observability are named. |
| Security/privacy | pass | Secrets, private paths, checksum integrity, and `.codex/skills/` public-source avoidance are covered. |
| Non-goals | pass | Deferred scope is explicit and enforceable. |
| Acceptance criteria | pass | Acceptance criteria are observable and match the release contract. |

## Eventual Test-Spec Readiness

Conditionally-ready after SGPA-SR1 is resolved. The spec already contains enough concrete behavior for a test spec once the prior-spec supersession scope is explicit.

## Recommended Next Stage

Immediate next repository stage: spec revision and `spec-review-r2`.

Do not proceed to architecture, plan, or test-spec until SGPA-SR1 is closed.
