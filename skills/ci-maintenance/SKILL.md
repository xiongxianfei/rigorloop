---
name: ci-maintenance
version: "1.0.0"
schema-version: skill-readability-v1
description: >
  Author or review repository-owned CI workflows, validation automation, and related configuration when coverage, speed, caching, permissions, triggers, or ordinary hardening needs maintenance.
argument-hint: [operation, exact target path, concern, and command evidence]
---

# CI maintenance

Maintain CI infrastructure from project-owned commands and risk evidence. Ordinary authoring does not run validation, does not design tests, does not specify validation commands, or wait for checks; validation stays under `verify`. A bounded PR CI repair may run already-authoritative validation commands and observe the replacement hosted check under the rules below.

## Workflow role

- role_name: ci-maintenance
- stage: support
- upstream: user request, exact repository target, project-owned commands, risk evidence, and approved privileged design when applicable
- downstream: `explain-change` for ordinary workflow-managed authoring; none for an eligible bounded PR CI repair
- summary: Review or conditionally author repository-owned CI automation without inventing commands, policy, or external state.
- must_not_claim: unexecuted validation, unobserved hosted-CI status, verification, branch, PR, release, deployment, or lifecycle readiness

## Classification

Resolve independently:

- Operation: `create`, `revise`, or `review`. Create needs an absent target; revise needs an existing known identity; review never writes.
- Concern: `coverage`, `performance`, `caching`, `permissions`, `triggers`, `ordinary-security-hardening`.
- Target: `github-workflow`, `project-validation-automation`, `related-platform-configuration`, `external-platform-state`, `invalid-or-ambiguous-target`.
- Provider: `github-actions`, `project-native-other-provider`, `invalid-or-ambiguous-provider`.
- Privilege: `ordinary-workflow-context`, `privileged-approved-design`, `privileged-design-required`, `invalid-or-ambiguous-privilege-context`.
- Structure: `none`, `compose-from-skeleton`, `preserve-existing-structure`.
- Repair mode: `ordinary-infrastructure` or `bounded-pr-ci-repair`.

Unknown values fail before consistency checks. Ambiguous, escaped, conflicting, stale, or unsupported identities stop without changing operation or provider.

GitHub procedure applies only to repository-file GitHub workflows. Other files require an exact project-native contract for path, format, content/commands, validation, and authority. External state is review-or-route only.

## Bounded PR CI repair

Use `bounded-pr-ci-repair` only for an already-open PR with an exact failing run and head, current review and verification evidence, no open material finding, already-authoritative commands, and existing authority for each push or other external mutation.

The correction must only restore already-approved behavior. Reject this mode if it introduces or revises requirements, architecture, runtime implementation, dependencies, lifecycle schema, stage routing, review outcomes, or another decision-bearing contract. Ambiguity routes to the earliest affected owning stage.

For an eligible repair: inspect the failure, make the smallest correction, run the focused command and exact PR command already owned by the repository, prefer one coherent repair commit, push only under existing authority, and observe the replacement hosted check. Preserve current review, explanation, verification, and lifecycle evidence when their decision basis is unchanged. Do not create a new review round, explanation artifact, verify report, change record, or lifecycle-only commit solely because CI failed.

## Command, risk, and security boundaries

Do not invent validation commands. Allowed command sources are approved specs or test specs, plan validation sections, existing package scripts or CI conventions, and explicit user-provided commands. When none is reliable, report a blocker instead of guessing.

The project owns risks and commands. The risk map alone selects checks and boundaries; GitHub procedure serializes them. Coverage-sensitive work includes exclusions, boundary placement, unmapped risks, and changes to checked risks.

Default permissions are read-only. Add broader job-specific permissions only when a known workflow need requires them. Use dependency caches only when a stable invalidation key exists. Flag overbroad permissions, path filters that skip required checks, slow comprehensive checks on every PR, `pull_request_target` with untrusted code, missing risk coverage, and unmapped changed surfaces.

Privileged review is read-only. Mutation needs an exact approved design/review bound to repository and target, supplying events, scope, permissions, credentials/OIDC, runners, environments, forks/secrets, actions, and validation. Omitted choices default safely or stop; conversation never supplies them.

## Assemblies

Select one: `CIM0` narrow review; `CIM1` ordinary GitHub authoring; `CIM2` project-native file; `CIM3` external-state route; `CIM4` invalid stop; `CIM5` coverage review; `CIM6` coverage authoring; `CIM7` privileged review; `CIM8` approved privileged authoring. Add only triggered references and external evidence.

Creation adds the skeleton; revision adds it only for authorized replacement. Late predicates load additions before dependent action.

## Resource map

- READ `references/github-workflow-authoring.md` when a GitHub workflow is created or revised under ordinary or exact approved-design authority. It serializes settled policy and does not select coverage.
- READ `references/risk-to-check-map.md` when coverage-sensitive judgment is required. It owns semantic placement and must include current authoritative commands.
- COPY `assets/github-workflow-skeleton.yml` when creating a GitHub workflow or performing an explicitly authorized structural replacement. Fill every placeholder from current authority; do not emit placeholders.

Confirm every triggered resource is present, readable, inside the package, and from one package version. Missing, unreadable, escaped, contradictory, or mixed-version resources stop; do not reconstruct conditional procedure from memory. An untriggered resource does not block.

## Mutation safety

Prepare and validate the complete file. Create uses commit-time atomic no-clobber. Revise replaces only while identity matches. Plain overwrite is insufficient; read-back confirms but does not protect concurrency. Unsupported or uncertain primitives return `blocked`.

Idempotent success without writing requires current identity equal to intended identity and unchanged decision-bearing evidence. Otherwise reclassify from current state.

Classify batches as `independent`, `ordered-dependent`, or `atomic-group-required`. Prepare an invocation-local identity/dependency manifest before writes. Providers precede wrappers. Unsafe states or cycles return `blocked-before-write`. Results are `complete`, `partial-blocked`, or `blocked-before-write`; partials name completed and pending targets, blockers, and validity. Retry rebuilds the entire graph and adopts no stale manifest. Persistence requires architecture.

## Results and handoff

Report requested and actual operation, repair mode, target kind, provider, privilege, concerns, structure, assembly, target identity, mutation outcome, validation evidence, blockers, and hosted CI observation. Use `not-observed`, `pending`, `passed`, or `failed`; when observed, include the exact run and head.

Do not claim tests or hosted CI succeeded unless executed or observed. A bounded repair does not claim branch readiness, PR readiness, deployment readiness, release readiness, or lifecycle completion. Ordinary workflow-managed success hands off to `explain-change`; an eligible repair and other direct invocations stay isolated.

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
- Hosted CI observation: <not-observed | pending | passed | failed; exact run and head when observed>
- Next stage: <explain-change | none | blocked>
```

## Expected output

Return the filled result, a concise workflow diff or review finding summary, exact risk and authority evidence, and no unsupported readiness claim.
