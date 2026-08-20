# CI-Maintenance Skill Simplification

## Owning change record

This proposal is governed by [change.yaml](../changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml). Mutable lifecycle status is owned by that change record.

## Problem

The published `ci-maintenance` package currently contains a 1,369-word, 9,653-byte `SKILL.md`, a 492-word risk-to-check reference, and a 153-word GitHub workflow skeleton. The root file mixes universal safety with detailed GitHub Actions authoring procedure, review procedure, caching and performance advice, risk-to-check mapping, output layout, and workflow handoff. Every invocation therefore pays for procedure that may not apply.

The current operation vocabulary also mixes actions with concerns:

```text
author new workflow
revise workflow
review workflow
optimize speed
harden security
add caching
audit coverage
```

`create`, `revise`, and `review` are operations. Performance, caching, permissions, triggers, coverage, and ordinary security hardening are concerns that can apply to any operation. Treating them as peer modes makes target-state rules, write authority, resource selection, and result claims harder to close.

The existing GitHub workflow skeleton creates a second safety problem. It contains pull-request, push, manual, and scheduled triggers plus both changed-risk and boundary jobs. Copying it can expose more triggers and jobs than the current request or project contract authorizes. The risk-to-check map has the opposite problem: its portable mapping method is useful only for coverage-sensitive work, but it is currently easy to load for narrow permissions, cache, timeout, or concurrency review.

The optimization must reduce actual loaded profiles while preserving command ownership, changed-risk coverage, least privilege, secret and fork safety, provider truthfulness, exact target identity, and hosted-CI claim boundaries. Moving text out of `SKILL.md` without closing resource triggers or reducing real assemblies would not be a successful simplification.

## Goals

- Reduce the loaded procedure for narrow review, coverage review, narrow revision, coverage-sensitive revision, and workflow creation.
- Separate operation, target kind, concern, provider, privileged authority, resource need, and structural composition into independent classifications.
- Keep universal command authority, coverage safety, permissions and secret safety, target identity, stop conditions, claim limits, and resource triggers in a compact `SKILL.md`.
- Add one conditional GitHub workflow-authoring reference for create and revise procedure.
- Retain the existing risk-to-check map as the conditional owner of changed-path coverage mapping and PR-versus-boundary separation.
- Simplify the existing GitHub workflow skeleton so it owns safe YAML structure without silently granting trigger or boundary-job authority.
- Define exact create, revise, and review semantics from target existence and current identity.
- Use one bounded single-file write protocol without a persistent transaction system.
- Preserve existing GitHub workflow, project validation-automation, and related platform-configuration behavior without requiring one provider-neutral authoring reference.
- Preserve portable behavior for non-RigorLoop repositories and fail closed for unsupported or ambiguous targets, providers, or authority.
- Measure every supported loaded assembly, the complete package, and canonical-through-installed resource parity.

## Non-goals

- Changing which project artifacts own validation commands, test coverage, release policy, deployment policy, or workflow routing.
- Running validation, waiting for CI, debugging a specific failing check, designing tests, or claiming that hosted CI passed.
- Designing privileged publishing, deployment, OIDC, long-lived-secret, self-hosted-runner, untrusted `pull_request_target`, or similarly sensitive workflows; bounded implementation under one exact current approved design remains supported.
- Adding a provider-neutral CI engine, workflow generator, policy engine, YAML rewriter, cache service, runtime helper, or packaged script.
- Introducing a new CI artifact lifecycle, persistent transaction record, write owner, or approval state.
- Migrating historical project workflows merely to adopt the simplified skeleton.
- Optimizing unrelated skills except directly coupled contracts, validators, fixtures, package generation, or architecture documentation.
- Opening a live test PR, executing a hosted workflow, or running Codex, Claude Code, opencode, or another target-agent runtime for acceptance.

## Vision fit

fits the current vision

The change reduces repeated ceremony and irrelevant context while preserving trustworthy Git-tracked automation, source-ranked evidence, explicit authority, human reviewability, and thin workflow wrappers around project-owned validation. It does not introduce a hosted control plane or replace engineering judgment with hidden runtime machinery.

## Context

`CONSTITUTION.md` requires repository validation logic to live in repo-owned scripts and says GitHub Actions workflows should remain thin wrappers that set up tooling and delegate to those scripts. It treats CI behavior as compatibility-sensitive. `docs/workflows.md` defines `ci-maintenance` as creating or updating hosted CI workflow files, validation automation, or platform configuration; it is not the skill for running validation or waiting for checks.

`specs/skill-contract.md` defines `ci-maintenance` as the visible stage label and canonical skill entrypoint. It permits packaged references and assets only through an explicit resource map, requires project-portable published wording, and requires mapped resource integrity across canonical, generated, packed, archived, and installed forms.

The current package already has one reference and one asset. No new resource class or loader is needed. The selected design adds one reference and narrows the responsibilities of the existing resources. A bounded architecture assessment should therefore expect `architecture-not-required` unless implementation discovers that safe authoring needs a new parser, generator, persistence surface, provider abstraction, or privileged-policy owner.

Current baseline measurements are:

| Surface | Words | Bytes |
| --- | ---: | ---: |
| `SKILL.md` | 1,369 | 9,653 |
| `references/risk-to-check-map.md` | 492 | 3,105 |
| `assets/github-workflow-skeleton.yml` | 153 | 1,637 |
| Complete package | 2,014 | 14,395 |

These measurements are baselines, not acceptance targets by themselves. Acceptance must show that every real loaded assembly becomes easier to scan without weakening behavior.

## Options Considered

### Option 1: Keep the current package

This has no migration cost. It preserves an overloaded operation model, keeps detailed authoring procedure on narrow review paths, and leaves an over-capable skeleton available for accidental copying.

### Option 2: Editorially compress `SKILL.md`

This may reduce total bytes with little package work. It does not create a real review-versus-authoring loading boundary, and aggressive compression risks hiding command, permissions, secret, and coverage safeguards.

### Option 3: Move all detailed procedure into one catch-all reference

This shortens the root file but forces narrow authorship, coverage review, and unrelated concern review through one large conditional resource. It also blurs the existing risk-map ownership boundary.

### Option 4: Add one authoring reference, retain the risk map, and simplify the asset

Keep universal safety and classification inline. Load GitHub authoring procedure only for create or revise, load the risk map only for coverage-sensitive judgment, and copy the skeleton only for creation or an explicitly authorized structural replacement. This creates genuine independent activation boundaries with a small package.

### Option 5: Split caching, permissions, triggers, performance, and coverage into separate references

This can minimize individual reads but creates many combinations, ordering rules, missing-resource states, and duplicated cross-cutting safety language. The concerns are too small and too interdependent to justify separate packages in the first version.

### Option 6: Add an executable generator or CI policy engine

An executable system could normalize YAML mechanically. It would add runtime, compatibility, provider, persistence, and testing surfaces without solving command ownership or risk judgment. The current problem is procedural composition, not missing computation.

## Recommended Direction

Choose Option 4:

```text
compact skills/ci-maintenance/SKILL.md
+ references/github-workflow-authoring.md
+ existing references/risk-to-check-map.md
+ simplified assets/github-workflow-skeleton.yml
+ no scripts
```

### Classify operation from target state

Use exactly three operations:

```text
create
revise
review
```

| Requested operation | Target state | Result |
| --- | --- | --- |
| `create` | Exact target absent | Creation may proceed after authority and resource checks |
| `create` | Target exists | Stop; require explicit `revise` |
| `revise` | Exact target exists and identity resolves | Revision may proceed after authority and resource checks |
| `revise` | Target absent | Stop; route to `create` |
| `review` | Exact target exists | Read-only review |
| `review` | Target absent | Read-only `missing-target` finding; suggest `create` |
| Any operation | Target, provider, path, or identity ambiguous | Stop |

A complete replacement of an existing workflow remains `revise`. Review never gains write authority. A correction requested after review starts begins a new `revise` operation and re-resolves target, provider, evidence, and authority.

### Classify target kind independently

Resolve exactly one target kind before provider-specific procedure:

```text
github-workflow
project-validation-automation
related-platform-configuration
external-platform-state
invalid-or-ambiguous-target
```

| Target kind | Review | Create or revise |
| --- | --- | --- |
| `github-workflow` | Supported | Supported through the packaged GitHub authoring procedure |
| `project-validation-automation` | Supported | Supported only from one exact project-owned path, syntax, command, validation, and authority contract |
| `related-platform-configuration` | Supported | Supported only from one exact project-native provider and configuration contract |
| `external-platform-state` | Evidence-bound review or route only | Unsupported; stop before external mutation |
| `invalid-or-ambiguous-target` | Stop or return an identity finding without mutation | Stop |

The project-native contract for a non-GitHub target is evidence supplied by the target project, not another packaged `ci-maintenance` resource. It must resolve the exact target path, provider or format, authoritative content source, validation method, and write authority. Missing or conflicting evidence stops rather than causing GitHub procedure to be translated or reconstructed.

Each mutating operation owns exactly one repository-file target. A request covering several workflow, validation-automation, or platform-configuration files enters the dependency-aware batch contract below. External host or account settings, branch protection, cloud environments, and other non-file state may be reviewed or routed, but this first version never mutates them.

### Classify concerns independently

After operation resolution, record zero or more concerns:

```text
coverage
performance
caching
permissions
triggers
ordinary-security-hardening
```

The concern set changes required judgment and resource selection, not write authority. Unknown concern values fail closed. Privileged workflow signals are not ordinary security concerns; they select a stop-and-route result.

### Use a closed provider classification

Classify the target provider before provider-specific interpretation:

```text
github-actions
project-native-other-provider
invalid-or-ambiguous-provider
```

GitHub Actions creation and revision use the new authoring reference. A project-native other provider may be reviewed when the project supplies one exact authoritative local contract and syntax source. Missing, conflicting, escaped, or ambiguous provider identity stops without guessing.

Project validation automation and related platform configuration may be created or revised for a project-native other provider only when the same exact local contract also supplies the target path, content and command authority, validation method, and bounded write authority. The skill does not translate GitHub procedure into another provider or infer syntax from general knowledge. A non-GitHub hosted-workflow target without that complete contract stops.

Use this closed compatibility matrix:

| Target kind | Provider or storage | Mutation support |
| --- | --- | --- |
| `github-workflow` | `github-actions` repository file | Supported |
| `github-workflow` | Other provider | Invalid combination |
| `project-validation-automation` | Exact repository-file project-native contract | Supported |
| `related-platform-configuration` | Exact repository-file project-native contract | Supported |
| `external-platform-state` | Host, account, cloud, environment, or repository setting | Review or route only |
| Any target | Ambiguous provider, storage, or identity | Stop |

### Separate ordinary from privileged workflow context

Classify privileged context and current design authority independently from operation:

```text
ordinary-workflow-context
privileged-approved-design
privileged-design-required
invalid-or-ambiguous-privilege-context
```

Publishing, deployment, environment protection changes, OIDC or cloud credentials, long-lived secrets, self-hosted runners, untrusted `pull_request_target`, workflow-to-workflow privilege escalation, and equivalent high-consequence signals establish privileged context. They do not by themselves prove design authority.

| Operation | Privileged authority | Result |
| --- | --- | --- |
| `review` | Ordinary, approved, or missing design | Perform read-only review and report design or implementation findings |
| `review` | Stale, conflicting, or ambiguous authority | Return an `inconclusive` authority finding without mutation |
| `create` or `revise` | One exact current approved design bound to the target | Implement only the bounded approved design |
| `create` or `revise` | Required design absent | Stop and route to the project’s architecture or security design owner |
| `create` or `revise` | Design stale, conflicting, or ambiguous | Stop |

`ci-maintenance` never authors the hardened design, interprets conversational approval as design authority, broadens permissions or credentials beyond the design, or partially implements an unresolved privileged target. Loading a procedure or recognizing a privileged signal grants no mutation authority.

### Bind approved privileged implementation to one exact design

Privileged GitHub authoring requires a current external design basis containing at least:

```text
design artifact identity
approving design-review identity
repository and exact target path
permitted events and branch or path scope
permissions
credential or OIDC model
runner class
environment-protection behavior
secret and fork behavior
third-party action policy
required validation method
```

The design and approving review must bind the same repository and target identity as the mutation. A stale design, non-approved review, mismatched target, or changed decision-bearing basis stops. Every privileged field follows this rule:

```text
explicitly specified by the current approved design:
  implement exactly within that bound

not specified:
  retain the universal safe default when compatible, otherwise stop

inferred from conversational wording or general knowledge:
  forbidden
```

The minimal skeleton remains a structural starting point only. It never authorizes privileged events, permissions, runners, credentials, environments, secrets, or jobs.

### Keep universal obligations inline

The compact root file remains responsible for:

- distinguishing CI infrastructure maintenance from validation execution, test design, failure debugging, verification, and PR work;
- resolving exact operation, target kind, target, provider, target state, and current identity;
- resolving commands only from authoritative project sources and never inventing commands, secrets, action SHAs, or tool versions;
- checking that changed material risks have an owned check or an explicit gap;
- least privilege, fork and secret safety, third-party action provenance, and dangerous-event recognition;
- concern classification, privileged-context classification, resource triggers, and missing-resource behavior;
- review read-only behavior and mutation authority;
- universal stop conditions, claim boundaries, result fields, and handoff limits.

The root must remain self-sufficient for a safe narrow read-only review. It must not reconstruct a missing conditional resource from memory.

### Separate risk placement from GitHub composition

Use one ownership invariant:

```text
risk map decides what must run and at which boundary;
GitHub authoring reference serializes that settled mapping.
```

| Decision | Owner |
| --- | --- |
| Which material risks exist | Universal `SKILL.md` plus project evidence |
| Which project command proves each risk | Project-owned command contract |
| Which check runs the command and at which PR, merge, release, schedule, or other boundary | `risk-to-check-map.md` |
| Whether the semantic mapping covers the material risks | Risk map plus universal stop rules |
| How a settled mapping becomes GitHub jobs, events, `if` expressions, paths, matrices, and dependencies | `github-workflow-authoring.md` |
| YAML ordering and placeholders | Skeleton |

The authoring reference may explain GitHub mechanics for realizing a PR or boundary check, but it does not choose semantic placement, declare coverage sufficient, replace a missing project command, or override the risk map. When the current mapping and requested GitHub composition disagree, stop and report the exact unmapped or conflicting risk.

### Give the GitHub authoring reference one responsibility

`references/github-workflow-authoring.md` owns detailed ordinary GitHub Actions creation and revision plus bounded realization of an exact approved privileged design:

- event, branch, path, job, expression, matrix, and dependency composition after authority and semantic risk placement are established;
- serialization of the risk map's selected PR and boundary checks without redefining placement;
- concurrency and cancellation behavior;
- cache eligibility, key inputs, invalidation, restore-key limits, and write safety;
- timeout and matrix bounds;
- third-party action version policy supplied by the project;
- complete YAML preparation and static validation;
- exact target identity revalidation, operation-specific conditional commit, and read-back;
- exact retry behavior for a one-file write.

For an approved privileged design, it owns only exact realization of design-specified GitHub fields. It does not select the privilege model, infer missing privileged fields, or broaden permissions, credentials, events, runners, environments, jobs, or action policy. Unspecified fields retain the universal safe default when that is compatible with the design; otherwise the operation stops.

It does not own validation commands, semantic check placement, risk sufficiency, privileged-design approval, lifecycle state, workflow routing, hosted-CI status, or PR readiness. Loading it grants no mutation authority.

### Narrow the risk-to-check map trigger

Retain `references/risk-to-check-map.md` and load it only when judgment involves:

- changed-path or material-risk coverage;
- path filters or trigger exclusions that can remove coverage;
- PR checks versus merge, release, scheduled, or other boundary checks;
- unmapped risk or coverage-gap audit;
- commands, jobs, or matrices whose placement changes which risks are checked.

A narrow permissions, cache, timeout, concurrency, or action-version review does not load the map unless it also makes a coverage claim. A revision to triggers, path filters, job commands, job inclusion, or check placement is coverage-sensitive and must load it.

The reference owns the portable `changed path -> material risk -> owned check -> authoritative command -> required execution boundary` method. Coverage-sensitive work cannot proceed without a complete current mapping. RigorLoop-specific examples are explicitly examples for a target repository that exposes those surfaces, not universal customer-project requirements.

### Make the skeleton minimally safe and structural

Simplify `assets/github-workflow-skeleton.yml` to contain only:

- a workflow name placeholder;
- an explicitly selected authorized trigger placeholder;
- read-only default contents permission;
- concurrency with project-derived group and cancellation behavior;
- one ordinary job with runner, timeout, checkout, setup, and project-command placeholders.

The asset owns YAML shape, ordering, comments, and placeholders. It does not own trigger choice, branch filters, path filters, command authority, action versions, cache policy, permissions beyond the safe default, boundary-job applicability, secrets, or adequacy.

The asset contains no schedule, push, manual trigger, boundary job, release job, deployment job, secret, OIDC permission, self-hosted runner, or `pull_request_target` example. The authoring reference adds a boundary job only when the current risk map selects that boundary and current project authority permits its GitHub realization.

### Separate structure mode from operation

Use:

```text
structure_mode:
  none
  compose-from-skeleton
  preserve-existing-structure
```

`create` uses `compose-from-skeleton`. `revise` normally preserves the existing structure while replacing the complete validated file. An explicit structural replacement may use the skeleton only when current user or project authority permits a full structural rewrite. `review` uses no skeleton. A missing skeleton blocks creation or authorized structural replacement, but not review or a compatible structure-preserving revision.

The first version does not parse or update managed YAML regions. Every revision still prepares and replaces one complete workflow file; preserving structure means composing against the existing validated organization rather than copying the skeleton.

### Define exhaustive loaded assemblies

| Assembly | Conditions | Loaded package content |
| --- | --- | --- |
| `CIM0-narrow-review` | `review`; no coverage-sensitive concern | `SKILL.md` |
| `CIM1-coverage-review` | `review`; coverage-sensitive concern | `SKILL.md` plus risk-to-check map |
| `CIM2-create` | ordinary GitHub `create` | `SKILL.md`, authoring reference, risk-to-check map, and copied skeleton |
| `CIM3-narrow-revise` | ordinary GitHub `revise`; no coverage-sensitive change; preserve structure | `SKILL.md` plus authoring reference |
| `CIM4-coverage-revise` | ordinary GitHub `revise`; coverage-sensitive change; preserve structure | `SKILL.md`, authoring reference, and risk-to-check map |
| `CIM5-structural-revise` | ordinary GitHub `revise`; explicit structural replacement | `SKILL.md`, authoring reference, copied skeleton, and risk-to-check map when coverage-sensitive |
| `CIM6-project-native-authoring` | project validation automation or related platform configuration; exact project-native contract; `create` or `revise` | `SKILL.md`, plus risk-to-check map when coverage-sensitive; project-native contract is external evidence |
| `CIM7-privileged-approved-create` | privileged GitHub `create`; exact current approved design and approving review | `SKILL.md`, authoring reference, risk-to-check map, copied skeleton, and external approved-design evidence |
| `CIM8-privileged-approved-revise` | privileged GitHub `revise`; exact current approved design and approving review | `SKILL.md`, authoring reference, external approved-design evidence, risk-to-check map when coverage-sensitive, and copied skeleton only for authorized structural replacement |

`CIM5`, `CIM6`, and `CIM8` have coverage-sensitive and non-coverage variants where the risk-map trigger is independent. `CIM5` and `CIM8` also report structure-preserving and structural-replacement variants when applicable. Every variant must be reported rather than averaged away. Project-native review uses the matching review assembly plus the project-supplied contract. External project contracts, approved designs, and approving reviews are identified and loaded as evidence but are not counted as packaged skill content.

Late discovery of coverage sensitivity loads the map before dependent judgment or writing. Late discovery of structural replacement loads the skeleton before composition. Late discovery of privileged context reclassifies authority before mutation; approved design may permit bounded implementation, while missing or ambiguous authority stops. A missing triggered resource or required project-native contract blocks only the dependent assembly.

### Use conditional single-file commits

For create or revise:

1. Resolve the exact repository, target kind, provider or format, path, operation, concerns, structure mode, authority, and prior identity.
2. Resolve every referenced project command, trigger, permission, runner, action version, cache input, platform field, and coverage obligation that applies to the target from current evidence.
3. Prepare the complete intended target content without mutating the target.
4. Validate target syntax, closed vocabularies, command authority, and the applicable trigger, path-filter, permissions, secret, action-provenance, cache, timeout, matrix, platform, and risk-coverage rules.
5. Re-read target identity and every decision-bearing input immediately before commit.
6. Commit exactly one classified CI target through the operation-specific conditional primitive.
7. Read back and validate the complete file and intended identity; do not treat read-back as concurrency protection.
8. Report the actual operation and evidence; do not claim hosted execution.

Creation and revision use different commit conditions:

```text
create:
  atomic no-clobber creation

revise:
  identity-guarded replacement bound to the validated prior content identity
```

Create fails if another actor creates the target after preflight; it never replaces an existing file. Revise uses compare-and-swap, an exclusive transient lock with identity revalidation, or an equivalent safe primitive that fails rather than overwriting a changed file. A plain overwrite-capable rename is insufficient.

If the environment cannot provide the required no-clobber or identity-guarded operation, or if the conditional write fails or leaves uncertain bytes, report `blocked`. A later invocation resolves current state afresh. It may accept idempotent success without another write only when the current file equals the exact intended identity and every decision-bearing input remains unchanged. Otherwise it reclassifies from current target state. Unrelated, partial, stale, ambiguous, or concurrently changed content is never adopted or overwritten. No persistent lock manager or transaction manifest is introduced for a one-file operation.

### Make multi-target work dependency-aware

Multi-target requests remain non-atomic, but they are not treated as dependency-free. Before writing, classify the complete target set:

```text
independent
ordered-dependent
atomic-group-required
```

| Batch classification | Result |
| --- | --- |
| `independent` | Targets may commit independently when each remains valid after its commit |
| `ordered-dependent` | Prepare all targets, validate cross-target references, then commit in proven dependency order |
| `atomic-group-required` | Stop before the first write; the first version cannot provide required multi-file atomicity |

The in-memory batch manifest binds each target ID, kind, path, prior identity, intended identity, dependencies, and `independently_valid_after_commit` judgment. Before the first write:

1. resolve every target, authority, and prior identity;
2. prepare every intended file;
3. validate every cross-target path, command, format, and reference;
4. prove the commit order leaves each intermediate repository state valid.

Dependency providers, such as project-owned validation commands or required configuration, commit before thin workflow wrappers and externally visible entrypoints. If updating a provider would invalidate its current consumers before those consumers change, the provider is not independently valid in that order; choose another proven order or classify the batch `atomic-group-required` and stop.

Use exactly these aggregate results:

```text
complete
partial-blocked
blocked-before-write
```

`partial-blocked` reports completed targets, pending targets, their current identities, the exact blocker, whether every completed target remains independently valid, and the required fresh retry or correction. It never implies group success. Without a persistent batch transaction, retry re-resolves the complete target graph, authorities, identities, dependencies, and intermediate-validity proof from current repository state; it never continues blindly from an in-memory operation list. A need for exact resumable multi-file transaction semantics changes the architecture assessment to required.

### Preserve truthful results and ownership

Use separate result fields for:

```text
operation
target kind
target
provider
concerns
structure mode
operation result
changed risks covered
known coverage gaps
commands referenced
validation performed
hosted CI observation
handoff
```

`hosted CI observation` is fixed to `not-performed-by-ci-maintenance`. The skill reports configuration inspection and static validation it actually performed, plus commands referenced but not executed. It never reports `pending`, `passed`, `failed`, or another hosted execution state. Hosted-check observation and readiness remain with the project’s verification, PR, or CI-diagnostic owner. Static inspection or local validation never becomes a hosted-CI pass claim.

`ci-maintenance` writes only the exact authorized classified CI target file for the current operation. It does not change specs, test specs, plans, product implementation, review evidence, lifecycle state, workflow routing, verification evidence, or PR state. In workflow-managed use, it returns control to `workflow`; isolated use stops after its own result.

## Expected Behavior Changes

- `create`, `revise`, and `review` become the only operations; optimization and hardening requests become concern flags.
- GitHub workflows, project validation automation, and related platform configuration become explicit target kinds rather than implicit exceptions.
- Multi-target requests classify independence and dependencies, prove safe intermediate states, and stop before unsupported atomic groups.
- Create on an existing target and revise on an absent target fail closed instead of silently reclassifying.
- Review remains read-only, and later correction starts a fresh revision.
- Narrow reviews load only the universal root; coverage-sensitive reviews additionally load the risk map.
- GitHub creation and revision load one authoring reference; review does not.
- Workflow creation always receives risk mapping and a minimal skeleton.
- Narrow structure-preserving revisions do not load the skeleton or risk map unless their content affects coverage.
- Privileged targets remain reviewable; create or revise proceeds only under one exact current approved design and otherwise stops and routes.
- Privileged approved-design creation and revision use named assemblies and a bounded GitHub realization branch.
- Project-native non-GitHub targets may be reviewed or authored only under one exact local syntax, validation, and authority contract; GitHub procedure is never translated implicitly.
- The skeleton no longer advertises unauthorized schedules, push triggers, manual triggers, boundary jobs, or privileged features.
- Create uses atomic no-clobber commit; revise uses identity-guarded replacement; read-back confirms content but is not concurrency protection.
- Partial multi-target completion reports exact completed and pending targets and never implies group success.
- Results report only CI-maintenance-owned inspection and static-validation evidence and never report hosted execution state.

Existing project workflows remain unchanged until an explicit create or revise operation targets them. Historical skill artifacts and packages are not rewritten solely to adopt the new package shape.

## Architecture Impact

Perform a bounded architecture assessment. The expected result is `architecture-not-required` when all of the following hold:

- the existing skill-package model already supports one additional mapped reference;
- mapped resources retain existing raw-byte parity and path rules;
- the revision uses complete-file composition, existing no-clobber or identity-guarded transient file primitives, and fresh batch re-resolution without a parser or persistent transaction surface;
- GitHub-specific behavior remains packaged guidance and project-native behavior remains supplied by exact local contracts rather than a runtime abstraction;
- privileged workflow design remains outside `ci-maintenance` ownership while bounded implementation under approved design uses existing authority.

A documentation-only architecture correction is appropriate if current architecture inventory depicts `ci-maintenance` as permanently flat.

Architecture becomes required if implementation introduces a workflow generator, managed-section parser, provider-neutral execution layer, persistent mutation receipt, managed locking service, resumable multi-file transaction surface, external platform-state integration, new authorization state, privileged-policy owner, or independent runtime component.

## Testing and Verification Strategy

Before implementation, inventory separately:

- semantic rules that must remain true;
- parser- or validator-sensitive literals;
- current resource-map paths and verbs;
- target-kind, provider, operation, concern, privileged-authority, structure-mode, hosted-observation, and result vocabularies;
- package generation, archive, release-candidate, and install consumers.

Add deterministic contract fixtures for at least:

- every operation and target-state row;
- every target kind, project-native contract prerequisite, and invalid or ambiguous target result;
- independent, ordered-dependent, and atomic-group-required multi-target classification;
- cross-target path and command validation, provider-before-wrapper ordering, safe intermediate states, partial results, and fresh-graph retry;
- review correction starting a new revision;
- every concern value and an unknown concern;
- GitHub, supported project-native review and authoring, and invalid or ambiguous provider cases;
- privileged read-only review, approved-design implementation, missing design fields, stale design, target mismatch, non-approved review, and ambiguous authority;
- every loaded assembly and the declared coverage and structure variants of `CIM5` through `CIM8`;
- late coverage and structure discovery;
- missing triggered reference, map, or skeleton;
- command-source, permission, secret, fork, action provenance, cache, timeout, matrix, path-filter, and trigger failures;
- create races proving no-clobber behavior, revise races proving identity-guarded behavior, unavailable conditional-write primitives, and idempotent complete-file retry;
- risk-map placement versus GitHub serialization conflicts;
- review making no write;
- the fixed `not-performed-by-ci-maintenance` hosted-observation value and rejection of hosted execution states;
- local or static validation not becoming hosted-CI success;
- unknown closed-vocabulary values failing before consistency checks.

Carry at least these acceptance outcomes into the focused specification:

| ID | Acceptance outcome |
| --- | --- |
| `AC-CIMSIM-015` | PR-versus-boundary semantic placement has one owner: the risk map. |
| `AC-CIMSIM-016` | GitHub authoring serializes but never redefines the selected mapping. |
| `AC-CIMSIM-017` | Coverage-sensitive work requires a complete current risk mapping. |
| `AC-CIMSIM-018` | Mapping and GitHub-composition conflicts stop. |
| `AC-CIMSIM-019` | Every privileged create or revise has one named assembly. |
| `AC-CIMSIM-020` | Privileged implementation binds an exact approved design and approving review. |
| `AC-CIMSIM-021` | Missing privileged fields retain safe defaults or block and are never inferred. |
| `AC-CIMSIM-022` | The skeleton grants no privileged authority. |
| `AC-CIMSIM-023` | Privileged design remains outside `ci-maintenance` ownership. |
| `AC-CIMSIM-024` | Create cannot overwrite a target that appears after preflight. |
| `AC-CIMSIM-025` | Revise cannot overwrite content changed after validation. |
| `AC-CIMSIM-026` | Read-back is confirmation, not concurrency protection. |
| `AC-CIMSIM-027` | Missing conditional-write support produces `blocked`. |
| `AC-CIMSIM-028` | Idempotent success requires intended content and unchanged evidence. |
| `AC-CIMSIM-029` | Every multi-target request records dependencies or explicit independence. |
| `AC-CIMSIM-030` | Cross-target paths and commands validate before the first write. |
| `AC-CIMSIM-031` | Thin wrappers do not commit before required project-owned command targets. |
| `AC-CIMSIM-032` | Unsupported atomic-group requirements block before mutation. |
| `AC-CIMSIM-033` | Partial completion cannot imply group success. |
| `AC-CIMSIM-034` | Retry re-resolves the complete current target graph. |

Measure words and bytes for `SKILL.md`, each reference, the asset, every loaded assembly, and the complete package. Acceptance requires all primary real profiles to decrease from their comparable current loaded content. Package growth must remain visible and justified; a shorter root alone is not success.

Run the existing skill, resource-map, portability, package-generation, generated-output, archive, release-candidate, and clean-install validation named by the eventual plan and test spec. Prove canonical, generated, packed, archived, and installed path and byte parity for every mapped resource. Do not open a live test PR, execute a hosted workflow, or run a target-agent runtime for acceptance.

Ordinary proposal review, spec review, code review, verification, and PR review remain the semantic review surfaces. No separate prose-grading or runtime acceptance stage is introduced.

## Rollout and Rollback

Implement the root file, new reference, revised risk map, and revised skeleton as one package change after the proposal, spec, architecture assessment, plan, and test spec are approved. Update directly coupled fixtures, validators, package metadata, generated archives, and install-proof surfaces in the same implementation slices defined by the plan.

Validate canonical resources first, then package generation and parity, then repository-wide checks. Do not migrate existing project workflows automatically.

Rollback reverts the complete `ci-maintenance` package and its directly coupled contract, fixture, validator, and generated-package changes together. Because no runtime, schema, persistent transaction, or external state is introduced, rollback is a source and package reversal. Workflows explicitly revised by later independent invocations are outside this package-refactor rollback.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Safety rules move out of the common path | Narrow review could miss a dangerous condition | Keep command, coverage, permission, secret, provider, privilege, stop, and claim rules inline; use semantic inventory fixtures |
| Concern classification omits a resource | Judgment could use incomplete procedure | Use closed concern values, exhaustive assemblies, late-loading rules, and unknown-value failures |
| Minimal skeleton is treated as complete policy | Copied workflows could gain unsupported behavior | Keep only safe structure and placeholders; prohibit policy ownership in the asset |
| Risk map is skipped for a coverage-affecting edit | Material changed risks could lose checks | Define coverage-sensitive edits explicitly and test late trigger discovery |
| Conditional commit is unavailable | User-authored CI changes could be overwritten by a generic replacement | Block rather than weakening no-clobber or identity-guarded semantics |
| Project-native behavior becomes misleading | General knowledge could be mistaken for target-project syntax or authority | Require one exact local target, syntax, content, validation, and write-authority contract |
| Multi-target order exposes an invalid intermediate state | A workflow or command target could temporarily reference incompatible content | Prepare and cross-validate all targets, prove safe order, or stop as atomic-group-required |
| Multi-target work is reported as atomic | A partially completed request could be overstated | Use closed aggregate results and report exact completed, pending, and independently valid targets |
| Privileged work is mistaken for ordinary hardening | Sensitive credentials or deployment could be authored without design | Separate read-only review, approved-design implementation, missing design, and ambiguous authority |
| Hosted execution is inferred from static proof | CI-maintenance could overreach verification or PR ownership | Use the fixed hosted-observation value and prohibit execution-state results |
| Root shrinks while real assemblies grow | Apparent simplification would increase actual context | Measure every assembly and total package separately; require comparable primary-profile reduction |
| Literal relocation breaks validation or packaging | CI or resource checks could fail silently | Maintain separate semantic and literal inventories and prove canonical-through-installed parity |

## Open Questions

None at proposal level. Exact metadata field names, fixture names, byte targets, and validation commands belong to the specification, execution plan, and test specification after the decision is approved.

## Decision Log

- Use one GitHub authoring reference rather than a catch-all reference or many concern-specific references.
- Retain the existing risk-to-check map, narrow its trigger to coverage-sensitive judgment, and make it the sole semantic check-placement owner.
- Retain and simplify the existing GitHub workflow skeleton rather than adding another asset.
- Use exactly `create`, `revise`, and `review` as operations.
- Preserve `github-workflow`, `project-validation-automation`, and `related-platform-configuration` as explicit target kinds.
- Classify multi-target requests as independent, ordered-dependent, or atomic-group-required; preserve one-file conditional commits without claiming multi-file atomicity.
- Treat performance, caching, permissions, triggers, coverage, and ordinary hardening as independent concerns.
- Keep privileged workflow design outside authoring while permitting read-only review and bounded implementation under one exact current approved design.
- Represent privileged approved-design creation and revision with named design-bound assemblies.
- Use the packaged authoring reference only for GitHub Actions; require exact project-native contracts for other supported targets instead of translating GitHub procedure.
- Report `hosted CI observation: not-performed-by-ci-maintenance` and no hosted execution state.
- Use atomic no-clobber creation and identity-guarded complete-file revision; add no persistent lock or transaction model.
- Preserve historical project workflows until explicitly targeted.
- Exclude scripts, generators, live hosted execution, and target-agent runtime acceptance.

## Next Artifacts

After an approving proposal rereview:

1. focused `ci-maintenance` skill-contract specification;
2. bounded architecture assessment and any required documentation correction;
3. execution plan and plan review;
4. test specification and test-spec review;
5. implementation, code review, explanation, verification, and PR handoff under the normal workflow.

## Follow-on Artifacts

- Approved focused specification: `specs/ci-maintenance-skill-simplification.md`.
- Bounded architecture assessment: `docs/changes/2026-08-19-ci-maintenance-skill-simplification/architecture-assessment.md`.
- Approved execution plan: `docs/plans/2026-08-19-ci-maintenance-skill-simplification.md`.
- Approved test specification: `specs/ci-maintenance-skill-simplification.test.md`.
- Implementation, formal reviews, explanation, and verification evidence under the owning change root.

## Readiness

Proposal authoring completed after addressing `CIMSIM-PR1` through `CIMSIM-PR7` and handed the direction to proposal review. The isolated R3 review is preserved as historical judgment; current governed lifecycle readiness and routing are owned by the linked change record.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `ci-maintenance` skill | In scope | Problem, Goals, Recommended Direction |
| Separate operations from optimization and hardening concerns | In scope | Classify operation; Classify concerns independently |
| Use progressive disclosure with one authoring reference, the existing map, and the existing asset | In scope | Recommended Direction; resource ownership sections |
| Preserve command authority, least privilege, secret safety, and changed-risk coverage | In scope | Keep universal obligations inline; Testing and Verification Strategy |
| Measure before and after loaded context, not only root-file size | In scope | Context; Testing and Verification Strategy |
| Avoid scripts, generators, live CI, and target-agent runtime acceptance | In scope | Non-goals; Testing and Verification Strategy |
| Resolve target compatibility, privileged authority, and hosted-CI claim findings | In scope | Target-kind classification; privileged matrix; truthful results |
| Resolve policy ownership, privileged assemblies, conditional writes, and multi-target dependencies | In scope | Risk-placement ownership; loaded assemblies; conditional commits; dependency-aware batches |
| Create a new branch | Completed as an execution prerequisite | Branch `proposal/ci-maintenance-skill-simplification` |
| Generate a proposal and then run proposal review | In scope with separate authority | This artifact; Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact root classification, universal safety, stops, claims, and result contract | core to this proposal | Defines the public common-path behavior |
| New GitHub workflow-authoring reference | same-slice dependency | Creates the primary progressive-disclosure boundary |
| Risk-to-check map trigger and portable wording | same-slice dependency | Coverage behavior must remain complete and correctly conditional |
| Minimal GitHub workflow skeleton | same-slice dependency | Existing structural owner currently exposes over-broad examples |
| Operation, target-kind, concern, provider, privilege-authority, structure, and resource fixtures | same-slice dependency | Proves the closed behavioral model |
| Project-native validation-automation and platform-configuration compatibility | same-slice dependency | Preserves existing public target coverage without another packaged provider method |
| Risk-placement versus GitHub-serialization ownership | same-slice dependency | Prevents duplicate semantic policy owners |
| Approved privileged-design authoring assemblies | same-slice dependency | Preserves bounded supported mutation without transferring design authority |
| Conditional no-clobber and identity-guarded file commits | same-slice dependency | Prevents concurrent work from being overwritten |
| Dependency-aware non-atomic batch behavior | same-slice dependency | Makes multi-target ordering and partial results safe and truthful |
| Skill, package, resource-parity, portability, and unknown-value validation | same-slice dependency | Required compatibility and fail-closed proof |
| Before-and-after assembly measurements | same-slice dependency | Simplification must be demonstrated on real profiles |
| Bounded architecture assessment | first-slice candidate | Confirms no new owner, parser, runtime, or persistence surface is needed |
| Architecture inventory correction if it depicts a flat package | first-slice candidate | Documentation may need to reflect the accepted package boundary |
| Privileged publishing, deployment, OIDC, or self-hosted workflow design | out of scope | Requires separate architecture and security authority; bounded implementation of an approved design remains in scope |
| Generic non-GitHub provider method | out of scope | Project-native contracts preserve supported targets without inventing a provider-neutral method |
| External host, account, branch-protection, environment, or cloud-state mutation | out of scope | Requires a separate external-operation and architecture decision |
| Workflow generator, managed YAML parser, policy engine, or runtime helper | out of scope | Materially expands architecture and acceptance surface |
| Automatic migration of historical project workflows | out of scope | Not required to simplify the skill package safely |
