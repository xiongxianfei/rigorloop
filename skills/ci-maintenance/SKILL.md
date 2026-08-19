---
name: ci-maintenance
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Author or review repository-owned CI workflows, validation automation, and related configuration when coverage, speed, caching, permissions, triggers, or ordinary hardening needs maintenance.
argument-hint: [operation, exact target path, concern, and command evidence]
---

# CI maintenance

Maintain CI infrastructure from project-owned commands and risk evidence. Review is read-only. It does not run validation, does not design tests, does not specify validation commands, and does not wait for existing CI checks; validation execution stays under `verify`. It does not mutate external platform state or establish verification, branch, PR, release, or deployment readiness.

## Workflow role

- role_name: ci-maintenance
- stage: support
- upstream: user request, exact repository target, project-owned commands, risk evidence, and approved privileged design when applicable
- downstream: `explain-change` only in workflow-managed execution
- summary: Review or conditionally author repository-owned CI automation without inventing commands, policy, or external state.
- must_not_claim: validation execution, hosted-CI status, verification, branch, PR, release, deployment, or lifecycle readiness

## Classification

Resolve each axis independently before loading resources or writing.

- Operation: exactly `create`, `revise`, or `review`. Create requires an absent exact target; revise requires an existing target with a known identity; review never writes and may report `missing-target`.
- Concern: any applicable values from `coverage`, `performance`, `caching`, `permissions`, `triggers`, and `ordinary-security-hardening`.
- Target kind: exactly `github-workflow`, `project-validation-automation`, `related-platform-configuration`, `external-platform-state`, or `invalid-or-ambiguous-target`.
- Provider: exactly `github-actions`, `project-native-other-provider`, or `invalid-or-ambiguous-provider`.
- Privilege: exactly `ordinary-workflow-context`, `privileged-approved-design`, `privileged-design-required`, or `invalid-or-ambiguous-privilege-context`.
- Structure: exactly `none`, `compose-from-skeleton`, or `preserve-existing-structure`.

Unknown values fail before consistency checks. Ambiguous, escaped, conflicting, stale, or unsupported identities stop without changing operation or provider.

Only a repository-file GitHub workflow may use GitHub authoring procedure. Other repository-file targets require one exact project-native contract covering path, format/provider, authoritative content and command source, validation, and write authority. `external-platform-state` is review-or-route only.

## Command, risk, and security boundaries

Do not invent validation commands. Allowed command sources are approved specs or test specs, plan validation sections, existing package scripts or CI conventions, and explicit user-provided commands. When none is reliable, report a blocker instead of guessing.

The project identifies material risks and owns commands. The risk map alone selects checks and required execution boundaries. GitHub procedure only serializes a settled mapping. Coverage-sensitive work includes changed-path coverage, exclusions, boundary placement, unmapped-risk audit, and any job or matrix change that changes checked risks.

Default permissions are read-only. Add broader job-specific permissions only when a known workflow need requires them and record the rationale. Use dependency caches only when a stable invalidation key exists. Flag overbroad permissions, path filters that skip required checks, slow comprehensive checks on every PR, `pull_request_target` with untrusted code, missing risk coverage, and unmapped changed surfaces.

Privileged review remains read-only. Privileged create or revise requires one exact current approved design and approving review bound to the repository and target. The design supplies events, scope, permissions, credentials or OIDC, runners, environment protection, fork/secret behavior, action policy, and validation. Omitted choices retain compatible universal safe defaults or stop; conversation never supplies them.

## Assemblies

Select one family, then add only triggered structure or coverage resources:

- `CIM0`: narrow GitHub review; root only.
- `CIM1`: ordinary GitHub create/revise; add GitHub authoring.
- `CIM2`: project-native file work; root plus exact external project contract.
- `CIM3`: external-state review/route; root only.
- `CIM4`: invalid or ambiguous; root then stop.
- `CIM5`: coverage-sensitive GitHub review; add risk map.
- `CIM6`: coverage-sensitive GitHub create/revise; add GitHub authoring and risk map.
- `CIM7`: privileged review; root plus exact design evidence.
- `CIM8`: privileged approved create/revise; add GitHub authoring and exact design evidence, plus risk map when coverage-sensitive.

Creation adds the skeleton. Revision adds it only with explicit structural-replacement authority; ordinary revision preserves validated structure. Late coverage, structure, or privilege evidence loads the newly required resource before dependent judgment or mutation.

## Resource map

- READ `references/github-workflow-authoring.md` when a GitHub workflow is created or revised under ordinary or exact approved-design authority. It serializes settled policy and does not select coverage.
- READ `references/risk-to-check-map.md` when coverage-sensitive judgment is required. It owns semantic placement and must include current authoritative commands.
- COPY `assets/github-workflow-skeleton.yml` when creating a GitHub workflow or performing an explicitly authorized structural replacement. Fill every placeholder from current authority; do not emit placeholders.

Confirm every triggered resource is present, readable, inside the package, and from one package version. Missing, unreadable, escaped, contradictory, or mixed-version resources stop; do not reconstruct conditional procedure from memory. An untriggered resource does not block.

## Mutation safety

Prepare and validate the complete target file before mutation. Create uses atomic no-clobber: commit succeeds only if the target is still absent. Revise uses identity-guarded replacement: commit succeeds only if current identity still equals the validated prior identity. A plain overwrite-capable rename is insufficient. Read-back confirms intended bytes after a successful conditional commit but is not concurrency protection. Unsupported or uncertain primitives return `blocked`.

Idempotent success without writing requires current identity equal to intended identity and unchanged decision-bearing evidence. Otherwise reclassify from current state.

For multiple targets, classify exactly `independent`, `ordered-dependent`, or `atomic-group-required`. Build an invocation-local manifest with identities, dependencies, validation, and intermediate validity; prepare and validate everything before writing. Ordered work commits dependency providers before wrappers. Unsafe intermediate state or a cycle returns `blocked-before-write`. Aggregate result is exactly `complete`, `partial-blocked`, or `blocked-before-write`; partial results name completed and pending targets, blockers, and validity. Retry rebuilds the entire graph and adopts no stale manifest. Persistent coordination requires architecture.

## Results and handoff

Report requested and actual operation, target kind, provider, privilege, concerns, structure, assembly, target identity, mutation outcome, validation evidence, blockers, and `hosted CI observation: not-performed-by-ci-maintenance`.

Do not claim test or hosted-CI success, verification readiness, branch readiness, PR readiness, deployment readiness, release readiness, or lifecycle completion. Workflow-managed success hands off to `explain-change`; direct invocation stays isolated.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads. Prefer check IDs, requirement IDs, file paths, counts, line citations, and targeted excerpts.

## When full-file read is required

Read the full file when the whole file is the review target, bounded searches disagree, surrounding context changes the conclusion, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Output skeleton

```md
Result

- Skill: ci-maintenance
- Status: <created | updated | reviewed | blocked>
- Requested operation: <value>
- Actual operation: <value>
- Target: <kind, provider, path, identity>
- Classification: <privilege, concerns, structure, assembly>
- Mutation outcome: <result>
- Validation evidence: <evidence>
- Blockers: <none or exact blockers>
- Hosted CI observation: not-performed-by-ci-maintenance
- Next stage: <explain-change | none | blocked>
```

## Expected output

Return the filled result, a concise workflow diff or review finding summary, exact risk and authority evidence, and no unsupported readiness claim.
