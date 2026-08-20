# CI-Maintenance Skill Simplification

## Owning change record

`docs/changes/2026-08-19-ci-maintenance-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md`

## Goal and context

Reduce the procedure loaded by narrow CI review and maintenance while preserving exact command authority, risk coverage, least privilege, secret and fork safety, target identity, concurrency safety, and truthful hosted-CI claims.

The shipped package becomes a compact universal `SKILL.md`, one conditional GitHub authoring reference, the existing conditional risk-to-check map, and a safer GitHub workflow skeleton. The change reorganizes published guidance; it does not create a workflow generator, CI policy engine, provider abstraction, persistent transaction service, or external platform mutator.

This specification is a focused amendment to the approved `specs/ci-maintenance-skill.md`. It supersedes only the legacy clauses explicitly listed under Compatibility and migration. Every unlisted legacy clause remains authoritative.

## Glossary

- `semantic risk placement`: the mapping from a changed path and material risk to an authoritative command, owned check, and required execution boundary.
- `GitHub serialization`: representation of an already settled semantic mapping as GitHub Actions events, filters, jobs, expressions, matrices, and dependencies.
- `privileged workflow context`: publishing, deployment, environment protection, OIDC or cloud credentials, long-lived secrets, self-hosted runners, untrusted `pull_request_target`, workflow privilege escalation, or an equivalent high-consequence surface.
- `conditional commit`: an atomic no-clobber create or an identity-guarded revision that fails instead of overwriting concurrent work.
- `batch manifest`: the invocation-local ordered set of targets, identities, dependencies, and intermediate-validity facts for a non-atomic multi-target request.
- `loaded assembly`: the unique packaged resource set required by an invocation; external project evidence is identified separately and is not counted as packaged skill content.

## Examples first

Example E1: narrow read-only review
Given one exact existing GitHub workflow and no coverage-sensitive judgment
When `ci-maintenance` reviews a timeout or cache detail
Then it loads only `SKILL.md`, performs no mutation, and reports hosted CI as `not-performed-by-ci-maintenance`.

Example E2: coverage-sensitive GitHub creation
Given an absent exact workflow target, authoritative project commands, and a complete current risk mapping
When ordinary workflow creation is authorized
Then the skill loads the root, GitHub authoring reference, risk map, and skeleton, prepares the complete file, and uses an atomic no-clobber create.

Example E3: privileged approved-design realization
Given one exact current approved privileged design and approving design review bound to the repository and target
When privileged GitHub creation is requested
Then the skill realizes only the specified design fields, retains compatible safe defaults for omitted fields, and stops when an omitted field cannot safely default.

Example E4: concurrent create
Given create preflight observes the target absent
When another actor creates the target before commit
Then the no-clobber create fails and the skill does not overwrite or adopt the new file.

Example E5: concurrent revision
Given revision binds prior identity `A`
When the target changes to identity `B` before commit
Then identity-guarded replacement fails and the skill reports `blocked`.

Example E6: ordered dependent batch
Given a project validation script and a workflow that invokes it
When both targets can be independently valid in provider-first order
Then all content and references are validated before writing, the script commits before the workflow, and group completion is claimed only after both succeed.

Example E7: unsupported atomic group
Given two targets cannot remain valid in any permitted intermediate repository state
When a multi-target request is classified
Then it returns `blocked-before-write` without mutation and routes any persistent transaction need to architecture.

Example E8: risk-placement conflict
Given the risk map requires a release-boundary check but requested GitHub composition places it only on pull requests
When authoring is evaluated
Then the authoring reference does not choose a new placement and the operation stops with the exact conflict.

## Requirements

R1. The canonical package MUST contain `skills/ci-maintenance/SKILL.md`, `skills/ci-maintenance/references/github-workflow-authoring.md`, `skills/ci-maintenance/references/risk-to-check-map.md`, and `skills/ci-maintenance/assets/github-workflow-skeleton.yml`, and MUST introduce no script, executable generator, policy engine, runtime helper, or provider-neutral authoring abstraction.

R2. The universal `SKILL.md` MUST own operation, target-kind, provider, concern, privilege, structure, and resource classification; exact target and identity resolution; authoritative-command rules; material-risk detection; least privilege; fork and secret safety; third-party action provenance; mutation authority; stops; claims; results; and handoff limits.

R3. The universal procedure MUST be sufficient for safe narrow read-only review without loading a conditional resource, and review MUST never acquire mutation authority.

R4. Operation MUST use exactly `create`, `revise`, and `review`; concern values MUST use only `coverage`, `performance`, `caching`, `permissions`, `triggers`, and `ordinary-security-hardening`; the two axes MUST remain independent.

R5. `create` MUST require an absent exact target, `revise` MUST require an existing exact target with a known identity, and `review` MUST remain read-only whether the exact target exists or is missing. An operation/target mismatch or ambiguous path, provider, or identity MUST stop without silently changing operation.

R6. Target kind MUST use exactly `github-workflow`, `project-validation-automation`, `related-platform-configuration`, `external-platform-state`, and `invalid-or-ambiguous-target`.

R7. Provider classification MUST use exactly `github-actions`, `project-native-other-provider`, and `invalid-or-ambiguous-provider` and MUST be evaluated independently from target kind.

R8. Only a repository-file `github-workflow` with provider `github-actions` MAY use packaged GitHub authoring procedure. A non-GitHub project-validation or related-configuration target MAY be mutated only when one exact project-native contract supplies its repository-file path, format or provider, authoritative content and command source, validation method, and write authority.

R9. `external-platform-state` MUST be review-or-route only, and no host setting, account setting, branch protection, cloud environment, or other non-file external surface MAY be mutated.

R10. Missing, stale, escaped, conflicting, unsupported, or ambiguous target, provider, storage, project-native contract, command authority, or write authority MUST fail closed without translating GitHub procedure or inferring syntax from general knowledge.

R11. Privilege classification MUST use exactly `ordinary-workflow-context`, `privileged-approved-design`, `privileged-design-required`, and `invalid-or-ambiguous-privilege-context`.

R12. Privileged review MUST remain read-only and MAY report design or implementation findings. Privileged create or revise MUST require one exact current approved design and approving design-review identity bound to the same repository and target; absent, stale, conflicting, non-approved, or ambiguous design authority MUST stop.

R13. The approved privileged design basis MUST identify the design artifact, approving design review, repository, target path, permitted events and branch/path scope, permissions, credential or OIDC model, runner class, environment protection, secret and fork behavior, third-party action policy, and validation method.

R14. Privileged realization MUST implement only explicitly specified design choices, MUST retain universal safe defaults only when compatible, and MUST stop when a required omitted field cannot safely default. Conversational approval or general knowledge MUST NOT supply a privileged field.

R15. The risk-to-check map MUST be the sole packaged owner of semantic risk placement: `changed path -> material risk -> owned check -> authoritative command -> required execution boundary`.

R16. Project-owned command contracts MUST own commands; the universal root plus project evidence MUST identify material risks; and the risk map plus universal stop rules MUST decide whether semantic coverage is sufficient.

R17. The GitHub authoring reference MUST consume settled semantic placement and own only its GitHub Actions serialization, ordinary authoring mechanics, and bounded realization of an exact approved privileged design. It MUST NOT choose PR-versus-boundary placement, invent a command, declare semantic risk coverage sufficient, approve a privileged design, or override the risk map.

R18. Coverage-sensitive work MUST load the risk map. This includes changed-path or material-risk coverage, path or trigger exclusions, PR-versus-merge/release/schedule/other-boundary placement, unmapped-risk audit, and commands, jobs, or matrices whose placement changes checked risks.

R19. Narrow permissions, cache, timeout, concurrency, or action-version judgment MUST NOT load the risk map unless it also makes a coverage claim or changes semantic coverage.

R20. A missing, incomplete, stale, or conflicting required mapping MUST stop coverage-sensitive work, and a mapping/composition disagreement MUST report the exact conflict instead of applying local precedence.

R21. The skeleton MUST own only safe YAML shape, ordering, comments, and placeholders: a name, explicitly authorized trigger placeholder, read-only default contents permission, project-derived concurrency, and one ordinary job with runner, timeout, checkout, setup, and project-command placeholders.

R22. The skeleton MUST contain no built-in schedule, push, manual trigger, boundary, release, deployment, secret, OIDC, self-hosted-runner, or `pull_request_target` example and MUST NOT authorize commands, action versions, caches, trigger filters, elevated permissions, credentials, environments, secrets, or privileged jobs.

R23. Structure mode MUST use exactly `none`, `compose-from-skeleton`, and `preserve-existing-structure`. Create MUST compose from the skeleton, review MUST use none, ordinary revise MUST preserve validated existing organization, and only explicit current structural-replacement authority MAY select the skeleton for revise.

R24. Every revision MUST still prepare and conditionally replace one complete target file; the first version MUST NOT introduce managed YAML regions or a general YAML rewrite engine.

R25. The packaged loaded assemblies MUST be exactly: `CIM0-narrow-review` (root); `CIM1-coverage-review` (root and risk map); `CIM2-ordinary-github-create` (root, authoring reference, risk map, skeleton); `CIM3-narrow-github-revise` (root and authoring reference); `CIM4-coverage-github-revise` (root, authoring reference, risk map); `CIM5-structural-github-revise` (root, authoring reference, skeleton, plus risk map only when coverage-sensitive); `CIM6-project-native-authoring` (root plus risk map only when coverage-sensitive and exact external project contract); `CIM7-privileged-approved-create` (root, authoring reference, risk map, skeleton, and exact external approved design/review); and `CIM8-privileged-approved-revise` (root, authoring reference, exact external approved design/review, plus risk map and skeleton only when their independent predicates apply).

R26. Every supported invocation MUST resolve to exactly one assembly and MUST report conditionally included resources and loaded external evidence separately. A late-discovered predicate MUST load every newly required resource before dependent judgment or mutation.

R27. A missing, unreadable, escaped, mixed-version, or contradictory triggered resource MUST block dependent work, and the root MUST NOT reconstruct its procedure or structure from memory.

R28. The GitHub authoring reference MUST contain distinct ordinary and approved-design realization branches; loading either branch MUST NOT grant mutation or design authority.

R29. Every mutating invocation MUST resolve one exact repository-file target, prior state or identity, intended content identity, evidence basis, validation method, and commit condition before mutation.

R30. Create MUST use an atomic no-clobber commit whose commit point fails if the target is no longer absent; it MUST never replace a file that appeared after preflight.

R31. Revise MUST use an identity-guarded replacement whose commit point proves the current identity still equals the validated prior identity through compare-and-swap, an exclusive transient lock, or an equivalent safe primitive; it MUST never overwrite concurrently changed content.

R32. A plain overwrite-capable rename and post-write read-back MUST NOT be treated as concurrency protection. Read-back MUST confirm intended bytes after a successful conditional commit.

R33. When the supported environment cannot provide the required no-clobber or identity-guarded primitive, or when commit/read-back is uncertain, mutation MUST return `blocked` without weakening the concurrency claim.

R34. Idempotent success without another write MUST require current content identity equal to the intended identity and every decision-bearing evidence identity unchanged; otherwise a retry MUST reclassify from current state.

R35. Multi-target requests MUST classify exactly as `independent`, `ordered-dependent`, or `atomic-group-required` before the first write.

R36. Every batch MUST use an invocation-local manifest that identifies each target ID, kind, path, prior identity or absence, intended identity, dependencies, authoritative validation, and whether the target is independently valid after commit.

R37. Before the first batch write, the skill MUST resolve and prepare every intended target, validate every cross-target path and command, and prove that the selected order preserves a safe intermediate repository state.

R38. Independent targets MAY commit independently. Ordered-dependent targets MUST commit dependency providers before thin workflow or externally visible wrappers. A target MUST NOT commit when its required dependency is incomplete or when it cannot remain independently valid in the resulting partial state.

R39. `atomic-group-required` MUST return `blocked-before-write` and MUST perform no mutation. The first version MUST NOT claim multi-file atomicity or introduce a persistent batch transaction.

R40. Aggregate batch result MUST use exactly `complete`, `partial-blocked`, and `blocked-before-write`. `partial-blocked` MUST identify completed targets, pending targets, the blocker, and each completed target's intermediate validity and MUST NOT imply group success.

R41. Batch retry MUST re-resolve the entire target/dependency graph and all identities from current repository state; it MUST NOT blindly continue an in-memory or stale manifest or adopt unrelated partial state.

R42. Every operation result MUST report requested operation, actual operation, target kind, provider, privilege class, concerns, structure mode, selected assembly, target identity, mutation outcome, validation evidence, blockers, and hosted CI observation.

R43. Hosted CI observation MUST use the fixed value `not-performed-by-ci-maintenance`; static inspection, local validation, configured commands, or file read-back MUST NOT be reported as hosted CI passed, failed, or pending.

R44. `ci-maintenance` MUST NOT claim test success it did not execute, hosted-CI success, verification readiness, branch readiness, PR readiness, deployment readiness, release readiness, or lifecycle completion.

R45. The migration MUST maintain separate semantic-rule and literal-consumer ledgers and MUST give every current rule, path, heading, result value, concern, target kind, provider, assembly, placeholder, and parser-sensitive literal one disposition and owner.

R46. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have a regression test whose fixture or test name clearly identifies the unknown-value case.

R47. Measurement MUST use LF-normalized canonical authored files, Unicode whitespace-separated words, UTF-8 bytes, and each unique loaded or copied resource exactly once per assembly.

R48. Measurement MUST report the root, both references, skeleton, complete package, every fixed assembly, and every conditional `CIM5`, `CIM6`, and `CIM8` variant separately; external project contracts and approved designs MUST be disclosed as loaded evidence but excluded from packaged-content totals.

R49. Every real supported loaded assembly MUST strictly decrease in both words and bytes from its frozen pre-change equivalent; the complete package size MUST remain visible and MUST NOT substitute for per-assembly proof.

R50. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode resources MUST preserve required inventory and raw-byte parity through existing repository tooling.

R51. Published skill text MUST remain project-portable and MUST keep repository-maintainer source paths, generated mirrors, adapter mechanics, selector constraints, drift checks, and release procedure in contributor or governing surfaces rather than shipped procedure.

R52. Acceptance MUST use deterministic contract scenarios, syntax checks, validators, package/resource integrity, package-chain parity, and exact measurement. It MUST NOT open a live test PR, run a hosted workflow, execute a target-agent runtime, or add a prose-grading gate.

R53. The bounded architecture assessment MUST return `architecture-required` if safe implementation needs a persistent mutation receipt, managed locking service, multi-file transaction surface, managed YAML parser, provider-neutral abstraction, external platform-state integration, new persistent authority owner, or equivalent cross-process coordination.

R54. Where this focused specification lists an amended legacy clause, the replacement requirements in its compatibility table MUST govern the overlapping behavior and every coupled validator, fixture, reference, asset, and consumer MUST migrate atomically; unlisted requirements in `specs/ci-maintenance-skill.md` MUST remain in force.

## Inputs and outputs

Inputs are the approved proposal and review evidence, current `ci-maintenance` package, authoritative project command and risk evidence, target repository files and identities, optional exact project-native contracts, optional approved privileged designs and reviews, coupled skill-package contracts, validators, fixtures, and generated package metadata.

Outputs are a read-only review result or exact repository-file mutation result, the simplified canonical package, focused contract and proof-map updates, semantic and literal ledgers, deterministic scenarios, assembly measurements, package parity evidence, and stage-owned lifecycle evidence.

## State and invariants

- `skills/` remains the only authored skill source.
- Operation, target kind, provider, concern, privilege, structure, and resource selection remain independent axes.
- Semantic risk placement has one owner; GitHub serialization cannot redefine it.
- Privileged design approval remains outside `ci-maintenance`.
- Review is always read-only and external platform state is never mutated.
- Each mutating target uses a conditional one-file commit; multi-target work is explicitly non-atomic.
- Configured commands and local validation remain distinct from executed hosted-CI evidence.
- Every real loaded assembly improves; root-only reduction is insufficient.

## Error and boundary behavior

Unknown vocabulary, target/operation mismatch, ambiguous target or provider, missing project contract, absent or stale privileged authority, incomplete risk mapping, missing triggered resources, unsupported conditional-write capability, concurrent target change, unsafe dependency ordering, required atomic grouping, uncertain read-back, package drift, and forbidden claims fail closed with the exact blocker and decision owner.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R53, R54

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R4, R5, R6, R7, R11, R23, R35, R40, R42, R43, R46 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R5, R12, R29, R30, R31, R33, R34, R35, R38, R39, R40, R41 | BND-STATE-001 | - |
| identity-authority | applicable | R5, R8, R9, R10, R12, R13, R14, R16, R20, R23, R28, R29, R30, R31, R34 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R15, R17, R18, R19, R21, R22, R23, R24, R25, R26, R27, R28, R50, R51 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R29, R30, R31, R32, R33, R34, R36, R37, R38, R40, R41 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R20, R27, R30, R31, R33, R34, R39, R40, R41, R53 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R21, R22, R23, R24, R25, R45, R46, R47, R48, R49, R50, R51, R54 | BND-COMPAT-001 | - |
| external-environment | applicable | R8, R9, R10, R13, R29, R30, R31, R32, R33, R43, R44, R50, R52, R53 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R4, R5, R6, R7, R11, R23, R35, R40, R42, R43, R46 | closed operations, concerns, target kinds, providers, privilege classes, structure modes, batch classes, aggregate results, hosted observation, and unknown values | exactly one value applies on singular axes and unknowns fail before consistency checks | valid classification proceeds or returns an exact stop | R4 |
| BND-STATE-001 | state-lifecycle | R5, R12, R29, R30, R31, R33, R34, R35, R38, R39, R40, R41 | target absent/existing/changed, design current/stale, single-target prepared/committed/blocked, batch pre-write/partial/complete, and fresh retry | no operation silently changes kind and no partial batch implies group completion | exact result or unchanged stop | R5 |
| BND-AUTH-001 | identity-authority | R5, R8, R9, R10, R12, R13, R14, R16, R20, R23, R28, R29, R30, R31, R34 | project command owner, risk-map owner, GitHub serializer, skeleton, approved design owner, user/project mutation authority, and forbidden inferred authority | resource loading, target existence, or conversation never broadens authority | bounded read/write or fail-closed route | R12 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R15, R17, R18, R19, R21, R22, R23, R24, R25, R26, R27, R28, R50, R51 | universal root, two references, skeleton, nine assembly families and variants, project evidence, generated packages, and missing-resource paths | each semantic rule and structural shape has one owner | one exact assembly loads or dependent work blocks | R25 |
| BND-TEMPORAL-001 | temporal-retry | R29, R30, R31, R32, R33, R34, R36, R37, R38, R40, R41 | preflight, preparation, identity reread, conditional commit, read-back, concurrent write, partial batch, and fresh retry | commit-time predicates protect current state and retries never adopt stale manifests | success, exact partial result, or blocked retry | R30 |
| BND-RECOVERY-001 | failure-recovery | R20, R27, R30, R31, R33, R34, R39, R40, R41, R53 | missing mapping/resource, unavailable conditional primitive, failed commit, uncertain bytes, unsafe batch order, atomic-group need, and architecture escalation | no unknown file or partial state is reconstructed, overwritten, or adopted | unchanged stop, fresh reclassification, or architecture-required | R33 |
| BND-COMPAT-001 | compatibility-migration | R21, R22, R23, R24, R25, R45, R46, R47, R48, R49, R50, R51, R54 | old flat package, split package, historical workflow, amended and retained legacy clauses, safe skeleton creation, structure-preserving revision, literals, measurements, and package forms | historical files are not migrated solely for package adoption, unlisted legacy requirements remain authoritative, and amended consumers migrate atomically | prospective migration passes atomically or blocks | R54 |
| BND-ENV-001 | external-environment | R8, R9, R10, R13, R29, R30, R31, R32, R33, R43, R44, R50, R52, R53 | GitHub repository file, project-native repository file, external host state, filesystem primitives, local syntax tools, generated adapters, hosted CI, and unavailable environments | local evidence never becomes hosted execution and external state remains read-only | deterministic local proof, exact route, or blocked mutation | R43 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4, R5, R6, R7, R8, R10, R25, R26 | BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | an invalid target/provider combination or late concern selects under-scoped procedure | invalid combinations stop and late predicates load the exact additional resources before judgment |
| INT-002 | R12, R13, R14, R21, R22, R25, R28 | BND-AUTH-001, BND-COMPOSE-001, BND-ENV-001 | packaged procedure or skeleton invents privileged design authority | exact external approved design bounds realization; omissions default safely or block |
| INT-003 | R15, R16, R17, R18, R19, R20 | BND-AUTH-001, BND-COMPOSE-001 | the serializer chooses semantic check placement or a narrow concern avoids required risk analysis | the risk map remains sole placement owner and every coverage-sensitive path loads it |
| INT-004 | R29, R30, R31, R32, R33, R34 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | a concurrent create/revise is overwritten because atomic rename or read-back is mistaken for compare-and-swap | commit-time absence or identity guard fails closed; read-back only confirms successful bytes |
| INT-005 | R35, R36, R37, R38, R39, R40, R41 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | a dependent wrapper commits before its provider or partial work is reported as group success | prepare all, prove safe order, commit providers first, and report exact partial or pre-write blocker |
| INT-006 | R42, R43, R44, R47, R48, R49, R50, R52 | BND-COMPOSE-001, BND-COMPAT-001, BND-ENV-001 | relocation hides semantic loss, a real profile grows, or static proof becomes a hosted-CI claim | ledgers, per-assembly measurements, parity checks, and fixed hosted observation all pass |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | R3, R25 | BND-COMPOSE-001 | - | - |
| E2 | illustration | R25 | BND-COMPOSE-001 | - | - |
| E3 | regression | R12, R13, R14 | BND-AUTH-001 | CIMSIM-PR5 | - |
| E4 | regression | R30, R32, R33 | BND-TEMPORAL-001 | CIMSIM-PR6 | - |
| E5 | regression | R31, R32, R33 | BND-TEMPORAL-001 | CIMSIM-PR6 | - |
| E6 | regression | R38, R40 | BND-STATE-001, BND-TEMPORAL-001 | CIMSIM-PR7 | - |
| E7 | regression | R39, R53 | BND-RECOVERY-001 | CIMSIM-PR7 | - |
| E8 | regression | R20 | BND-AUTH-001 | CIMSIM-PR4 | - |

## Compatibility and migration

The split is prospective. Existing project workflows are not rewritten merely to adopt the safer skeleton. Creation and explicitly authorized structural replacement use the current skeleton; normal revision preserves the validated existing organization while replacing the complete file. The canonical skill, both references, skeleton, focused contract, consumers, validators, fixtures, resource mappings, and generated package inventories migrate atomically.

This amendment applies the following closed legacy-clause dispositions:

| Existing clause | Disposition | Replacement authority |
| --- | --- | --- |
| `CIM-R25` | superseded for skeleton contents | R21-R23 define the minimal structural skeleton and independent structure mode |
| `CIM-R34` | narrowed; no universal PR-versus-boundary placement default | R15-R20 make the current risk map the semantic placement owner |
| `CIM-R45` | superseded for mutation under approved design; external policy design remains out of scope | R11-R14 and R25-R28 permit only exact approved-design realization |
| `CIM-R53` | narrowed; changed-surface coverage is mandatory only for coverage-sensitive review | R18-R20 and R25 distinguish narrow from coverage review |
| `CIM-R59` | superseded for skeleton validation | R21-R23 validate the minimal safe skeleton without built-in PR or boundary jobs, cache policy, or privileged behavior |

All other clauses in `specs/ci-maintenance-skill.md`, including the canonical skill identity, command-source constraints, least-privilege behavior, hard-rename compatibility, resource-map integrity, generated adapter validation, and unchanged repository-workflow boundary, remain authoritative unless a replacement row above names them.

Rollback restores the prior flat skill and prior mapped-resource expectations without rewriting customer workflow files. Semantic-rule and literal-consumer ledgers distinguish preserved behavior from moved procedure and deliberate skeleton removals.

## Observability

Results expose the closed classifications, exact target and evidence identities, selected resources, external design or project contract identities, conditional commit outcome, batch dependencies and partial state, local validation evidence, blockers, and the fixed hosted-CI observation. Measurements report words and bytes for every real assembly and complete package.

## Security and privacy

The skill must not invent, expose, or log credentials, secrets, private keys, tokens, unnecessary personal data, or inaccessible evidence. Default permissions remain read-only, fork and secret behavior remains explicit, privileged fields require approved design, paths remain within the exact repository target, and external platform state is never mutated.

## Accessibility and UX

No end-user interface is added. Published Markdown and YAML comments must use clear labels, complete sentences where prose applies, stable result values, and no unresolved placeholders in final output.

## Performance expectations

Every supported loaded assembly must decrease in words and bytes. No runtime latency, hosted service-level, or target-agent performance contract is introduced. Cache or matrix performance changes remain evidence-bound concerns rather than automatic goals.

## Edge cases

EC1. A missing review target yields a read-only `missing-target` finding and no create operation.

EC2. A GitHub workflow is paired with a non-GitHub provider: the combination stops before provider procedure loads.

EC3. A path-filter edit appears narrow but can remove material coverage: the risk map becomes required before mutation.

EC4. A privileged design omits a permission that cannot safely default: mutation stops rather than inferring it.

EC5. The target appears after create preflight or changes after revise validation: the conditional commit fails without overwrite.

EC6. Read-back differs after a successful commit primitive: success is not claimed and current bytes are treated as uncertain.

EC7. A batch has one independently valid completed provider and one blocked wrapper: the result is `partial-blocked`, not `complete`.

EC8. A batch retry starts after unrelated changes: it rebuilds the graph and identities rather than resuming the old manifest.

EC9. The skeleton is missing during narrow structure-preserving revise: revision can proceed if no structural or coverage predicate requires it.

EC10. A real assembly shrinks while total package grows: the assembly gate may pass, but total package growth remains reported for review.

## Non-goals

- Running validation, waiting for hosted CI, debugging a failing check, designing tests, verifying a branch, or opening a PR.
- Designing privileged publishing, deployment, OIDC, secret, runner, or environment policy.
- Mutating external host or account state.
- Adding provider-neutral generation, managed YAML regions, persistent locks, transaction receipts, or multi-file atomicity.
- Migrating historical workflows solely to adopt the skeleton.
- Optimizing unrelated skills except directly coupled contracts, validators, fixtures, mappings, or package surfaces.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC1 | Every R-clause maps to direct deterministic proof in the test specification. |
| AC2 | The package contains one compact root, one GitHub authoring reference, the risk map, one minimal skeleton, and no scripts or runtime engine. |
| AC3 | Operation, target, provider, concern, privilege, structure, and resource axes use closed independent classifications and unknown values fail first. |
| AC4 | The risk map alone owns semantic placement; the GitHub reference only serializes the settled mapping. |
| AC5 | Every ordinary, project-native, structural, coverage-sensitive, and privileged approved-design invocation selects one exhaustive assembly. |
| AC6 | Privileged mutation binds an exact current approved design and never infers missing privileged choices. |
| AC7 | Create uses atomic no-clobber and revise uses identity-guarded replacement; read-back is confirmation rather than concurrency protection. |
| AC8 | Multi-target requests prove dependencies and safe intermediate validity, report exact partial state, and block unsupported atomic groups before writing. |
| AC9 | External platform state remains read-only and hosted observation remains `not-performed-by-ci-maintenance`. |
| AC10 | The minimal skeleton contains no built-in privileged, boundary, push, schedule, or manual behavior. |
| AC11 | Semantic and literal ledgers cover every current rule and consumed literal. |
| AC12 | Every real assembly decreases in words and bytes, conditional variants and external evidence are disclosed, and complete package size remains visible. |
| AC13 | Canonical-through-installed inventories and raw bytes match across supported adapters. |
| AC14 | Acceptance uses deterministic local proof and executes no hosted workflow, live PR, target-agent runtime, or prose-grading gate. |
| AC15 | Architecture becomes required when safe implementation needs a new persistent coordination, transaction, parser, provider, external-state, or authority owner. |
| AC16 | Every overlap with the approved legacy CI-maintenance contract has one explicit disposition, and unlisted legacy clauses remain authoritative. |

## Open questions

None. Exact fixture names and conditional-write implementation choices may be settled in planning and the test specification while preserving R29 through R41.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after review settlement.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`. This artifact does not claim review approval, architecture settlement, plan readiness, implementation readiness, verification, branch readiness, hosted-CI completion, or PR readiness.
