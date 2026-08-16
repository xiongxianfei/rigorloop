<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal prose paragraphs, keep complete sentences intact, and retain stable IDs and tables for repeated proof or mapping structures. -->

# PR Skill Simplification Contract

## Owning change record

`docs/changes/2026-08-16-pr-skill-simplification/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-08-16-pr-skill-simplification.md`

## Goal and context

Simplify the published `pr` skill into a compact universal submission contract, one conditionally loaded governed-readiness reference, and one structural PR-body asset. Preserve safe external action, exact verification binding, truthful hosted-CI reporting, idempotent existing-PR handling, and current lifecycle ownership. Amend the existing `verify` result/report contract only enough for `verify` to emit the immutable verification basis that `pr` consumes.

## Glossary

| Term | Meaning |
| --- | --- |
| verified subject | The exact head revision whose implementation and tests were verified. |
| handoff revision | The exact local revision eligible to become the remote and PR head; it equals the verified subject or its one permitted verify-owned evidence child. |
| verification basis | Verify-owned immutable repository, remote, base, merge-base, head-branch, and verified-subject identities. |
| evidence tail | The optional single direct-child commit containing only permitted final verification evidence. |
| matching PR | One host PR for the exact repository, remote, base branch, and head branch. |
| external success | A truthful fact that a push or PR mutation completed, independent of readiness. |

## Examples first

Example E1: portable preparation
Given current local verification evidence without a complete normalized basis
When the user explicitly requests `prepare-only`
Then the skill prepares truthful title and body content, performs no external mutation, and does not claim `pr-open-ready`.

Example E2: safe existing-PR reuse
Given one open matching PR whose head, base, title, and body already match the intended operation
When an ordinary `open` invocation runs
Then the skill preserves the PR identity, content, and open state and reports `reused`.

Example E3: draft publication requires separate authority
Given one matching draft PR
When submission intent is `open` without `publish-existing-draft`
Then the skill may reuse adequate content but must preserve draft state.

Example E4: remote contains unseen work
Given the local handoff revision is a strict ancestor of the remote head
When opening is requested
Then the relation is `local-ancestor-of-remote`, push is blocked, and no PR mutation occurs.

Example E5: base advances during opening
Given push or PR creation succeeds and the remote base then differs from the verified base
When final read-back runs
Then external success is reported truthfully, `pr-open-ready` is false, and fresh verification or the approved base-update route is required.

Example E6: concurrent PR creation
Given no PR exists during preflight and another actor creates the exact matching PR after push
When the mandatory post-push PR reread runs
Then the skill reclassifies to reuse or an explicitly authorized refresh and never creates a duplicate.

Example E7: body refresh lacks ownership
Given an existing PR body is stale and no explicit whole-body replacement authority exists
When refresh is considered
Then the existing body bytes remain unchanged and the operation blocks with the exact authority gap.

Example E8: governed signal is malformed
Given a structured owning-change signal is malformed or conflicts with another governed identity
When invocation classification runs
Then it stops as `invalid-or-ambiguous-governed-signal` without portable fallback.

## Requirements

R1. The published package MUST contain one compact `skills/pr/SKILL.md`, one `references/governed-pr-readiness.md`, and one `assets/pr-body-skeleton.md`; `skills/` MUST remain the sole authored source.

R2. `SKILL.md` MUST retain universal purpose, submission intent, exact repository and verification identity, actual-diff and working-tree safety, remote branch and PR classification, hosted-CI meanings, external operation ordering, stops, claims, and result semantics.

R3. The governed reference MUST own bounded change-pack, plan, review, rationale, verify, state-sync, release-sensitive, migration, and external-completion readiness aggregation and MUST have no lifecycle, routing, settlement, plan, review, or automation mutation authority.

R4. The PR-body asset MUST own only headings, ordering, placeholders, and repeated table shapes for its core, governed-traceability, and conditional-impact groups; procedure MUST own applicability, adequacy, readiness, authority, and claims.

R5. Every invocation MUST classify governed signals as exactly `no-governed-signal`, `single-governed-candidate`, or `invalid-or-ambiguous-governed-signal`; any explicit or structured signal counts even when malformed.

R6. Only `no-governed-signal` MAY use portable handling. A single candidate MUST load and validate the governed reference, while malformed, stale, conflicting, duplicated, unsafe, escaped, or ambiguous signals MUST stop without portable fallback.

R7. A missing, unreadable, escaped, stale, transformed, or mixed-version required reference MUST stop governed readiness judgment; an invalid or missing body asset MUST stop body generation and all external mutation.

R8. Submission intent MUST be exactly `open`, `draft`, or `prepare-only`; explicit `pr` defaults to `open`, while `draft` and `prepare-only` require explicit current authority.

R9. `prepare-only` MUST permit bounded local and available remote inspection and content construction, MUST perform no push, PR creation, refresh, publication, draft conversion, or other external mutation, and MUST report `prepared-not-opened` with `actual_external_mutation: none`.

R10. A blocker or provider limitation MUST NOT silently reclassify requested `open` or `draft` as successful `prepare-only`; requested intent, actual operation, blocker, and actual mutation MUST remain separate.

R11. Refresh authority MUST be exactly `none`, `explicit-title-refresh`, `explicit-full-replacement`, or `workflow-title-refresh`, and MUST bind the exact existing PR and permitted host-native field or whole body.

R12. Existing PR state-transition authority MUST be exactly `none`, `publish-existing-draft`, or `convert-existing-open-to-draft` and MUST require a separate explicit current instruction naming the exact PR and transition.

R13. Submission intent MUST NOT imply refresh or existing-state transition authority. Default `open` MUST preserve an existing draft, and explicit `draft` MUST preserve an existing open PR unless separate matching authority exists.

R14. First-version refresh MUST support only title replacement or explicitly authorized whole-body replacement. It MUST NOT parse or mutate Markdown sections, add hidden managed markers, or infer body ownership.

R15. An adequate existing PR MUST be reused without content or state mutation. Existing body bytes MUST remain unchanged unless explicit full-body replacement authority is current.

R16. Remote branch state MUST be exactly `absent`, `same`, `remote-ancestor-of-local`, `local-ancestor-of-remote`, `diverged`, or `ambiguous`, defined directionally relative to the local handoff revision.

R17. `remote-ancestor-of-local` MUST mean the remote head is a strict ancestor of the local handoff revision and MAY permit only a normal fast-forward push after baseline reread. `local-ancestor-of-remote` MUST mean remote contains work absent locally and MUST block push.

R18. `absent` MAY permit normal branch creation, `same` MUST perform no push, and `diverged` or `ambiguous` MUST stop. The skill MUST NOT force-push, delete, overwrite, rewrite, or implicitly replace a remote branch.

R19. Remote PR state MUST be exactly `absent`, `open`, `draft`, `closed`, `merged`, or `ambiguous` for the exact repository, host, head, and base.

R20. An absent matching PR MAY be created once after all readiness checks. Open or draft PRs MUST be reused when adequate and MAY be refreshed or transitioned only within independent current authority. Closed, merged, multiple, mismatched, or ambiguous PR state MUST stop without implicit reopening or duplicate creation.

R21. The operation result MUST be exactly `opened`, `draft-opened`, `updated`, `reused`, `prepared-not-opened`, or `blocked`.

R22. Hosted-CI state MUST be exactly `passed`, `failed`, `pending`, `unavailable`, `unobserved`, or `not-applicable`; unknown values MUST fail before consistency checks.

R23. `passed` MUST require current hosted evidence for the exact handoff revision at the PR head. `failed` MUST route required failure to its owner. `pending`, `unavailable`, or `unobserved` MUST never be described as passed and MAY permit initial opening only when current policy permits post-open CI. `not-applicable` MUST require current evidence.

R24. `verify` MUST remain the sole owner of `branch-ready` and MUST emit one normalized `verification_basis` through its existing portable result or governed verify-report surface.

R25. The normalized basis MUST contain immutable `repository_identity`, `remote_identity`, `base_branch`, `base_revision`, `merge_base_revision`, `head_branch`, and `verified_subject_revision` values; branch names MUST be resolved before readiness is reported.

R26. `pr` MUST consume and revalidate the basis and MUST NOT reconstruct it from command text, unresolved names, current Git state, arbitrary prose, or historical report conventions.

R27. Missing, stale, prose-only, command-only, unresolved, conflicting, or ambiguous verification evidence MAY support truthful preparation but MUST block `open`, `draft`, and `pr-open-ready` and route to fresh verification.

R28. The verified subject and handoff revision MUST be identical unless exactly one direct-child verify-owned evidence commit exists. That commit MAY change only the final verify report and matching owning change record or expressly required verify-owned state-sync evidence, with change-record edits limited to final verification evidence and verify-owned readiness or routing fields.

R29. Any product, test, spec, architecture, plan, dependency, configuration, generated output, unrelated documentation, other lifecycle-owner change, multi-commit tail, or non-direct parent relation after the verified subject MUST invalidate opening readiness.

R30. The operation MUST bind exact repository, remote, verified base branch and revision, verified merge-base identity, head branch, verified subject, optional evidence-tail identity, handoff revision, intended title/body identity, and matching PR identity when present.

R31. Before any external write, the skill MUST resolve the local target, working tree, actual diff, verification basis, handoff revision, current remote base, directional remote-head relation, matching PR state, and applicable independent authorities.

R32. Immediately before push, the current remote base MUST equal the verified base and the observed remote-head baseline MUST still match the classified relation.

R33. After push and before PR mutation, the skill MUST reread remote head, remote base, and matching PR state and MUST require remote head to equal the handoff revision and base to equal the verified base.

R34. Immediately before PR mutation, the skill MUST reread matching PR identity, head, base, title, body identity, and draft state and reclassify when concurrent state changed.

R35. After creation, reuse, refresh, or transition, the skill MUST read back PR URL, number, state, head, base branch, current base identity, title, and body identity before claiming the external result or `pr-open-ready`.

R36. The local handoff revision, pushed remote head, and PR head MUST be identical for `pr-open-ready`; the verified base and applicable merge-base contract MUST remain current through final read-back.

R37. Retry MUST reconcile observed remote and PR state instead of blindly replaying create, push, refresh, or transition and MUST never create a duplicate matching PR.

R38. External success and readiness MUST remain separate. If a write succeeds and a decision-bearing identity changes before read-back, the result MUST report the successful write truthfully, set `pr-open-ready: false`, and require fresh verification or the approved base-update route.

R39. `pr` MUST own only `pr-body-ready` and `pr-open-ready`, MUST NOT mutate `change.yaml`, workflow routing, artifact settlement, plan state, review state, merge state, release state, or publication state, and MUST have no downstream continuation.

R40. Every result MUST report requested intent, actual operation, actual external mutation or none, actual PR state or none, `pr-body-ready`, `pr-open-ready`, hosted-CI state, blockers, exact URL only after read-back, and claim limitations.

R41. The core body group MUST contain Summary, Why, What changed, Tests and verification, Risks and rollback, Reviewer notes, and Follow-ups. Governed and impact groups MUST be included only when applicable; unresolved required data MUST be an explicit blocker and no placeholder MAY remain.

R42. Before canonical skill edits, the change MUST record semantic-rule, literal-compatibility, verification-basis, static-scenario, and baseline-measurement evidence with one disposition for every current behaviorally significant rule and consumed literal.

R43. Every new or changed closed vocabulary MUST reject unknown values before consistency checks and MUST have an unknown-value regression test.

R44. Measurement MUST use LF-normalized canonical authored files, UTF-8 bytes, Unicode whitespace-separated words, and each unique procedural resource once. It MUST report PR0 portable, PR1 governed, asset, representative composition, and total package separately.

R45. PR0 and PR1 procedural profiles MUST each decrease from the 1,678-word, 11,375-byte baseline without semantic loss; total or representative growth MUST be reported and justified and no fixed percentage MAY override safety.

R46. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude, and opencode resources MUST preserve required inventory and raw-byte parity through repository-owned tooling.

R47. Acceptance MUST use deterministic static operation fixtures, contract and package validators, parity checks, and ordinary lifecycle review. It MUST NOT open a live acceptance PR, execute a target-agent runtime, grade transcripts, add a prose classifier, or add a permanent tokenizer or simplicity validator.

R48. If exact basis ownership requires a new durable evidence surface or refresh requires a managed-section parser, ownership protocol, provider runtime abstraction, persistent PR transaction record, or new state owner, the bounded architecture assessment MUST return `architecture-required` before planning.

R49. Published skill text MUST remain customer-project portable and MUST keep repository-maintainer source, generation, archive, release, install, and parity mechanics in contributor or governing surfaces rather than shipped procedure.

## Inputs and outputs

Inputs are current local and remote Git identities, verify-owned evidence, actual diff and working tree, repository guidance, optional governed change evidence, requested submission and mutation authority, host PR state, hosted-CI evidence, and the structural body asset. Outputs are prepared content or one confirmed external PR result, readiness booleans, hosted-CI state, blockers, and claim limitations.

## State and invariants

- `skills/` is the only authored skill source.
- Loading a reference grants no mutation authority.
- `verify` owns branch readiness; `pr` consumes it.
- Preparation is externally read-only.
- Push is never forced and remote work is never overwritten.
- Existing PR content and state are preserved without exact independent authority.
- External-operation success does not imply readiness.
- `pr` never settles lifecycle state or advances workflow.

## Error and boundary behavior

Unknown vocabulary, invalid governed signals, missing resources, stale verification, dirty or unattributable work, unsafe ancestry, moved base, multiple PRs, insufficient refresh or state-transition authority, changed concurrent state, hosted-CI contradictions, failed read-back, and identity mismatch fail closed. Failure before an authorized external call performs no external mutation. Failure after a confirmed write reports the external fact without overstating readiness.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R5, R6, R8, R11, R12, R16, R19, R21, R22, R43 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R8, R9, R13, R15, R16, R17, R18, R19, R20, R23, R37, R38, R39 | BND-STATE-001 | - |
| identity-authority | applicable | R5, R6, R11, R12, R13, R24, R25, R26, R28, R30, R36, R39 | BND-AUTH-001 | - |
| composition-path | applicable | R1, R2, R3, R4, R6, R7, R41, R42, R46, R49 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R28, R31, R32, R33, R34, R35, R36, R37, R38 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R7, R10, R18, R20, R23, R27, R29, R32, R33, R34, R35, R36, R37, R38 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R14, R24, R25, R26, R27, R42, R43, R44, R45, R46, R49 | BND-COMPAT-001 | - |
| external-environment | applicable | R9, R16, R17, R18, R19, R20, R22, R23, R31, R32, R33, R34, R35, R36, R38, R47 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R5, R6, R8, R11, R12, R16, R19, R21, R22, R43 | governed signal, intent, refresh authority, state-transition authority, branch state, PR state, operation result, and CI state vocabularies | unknown values fail before consistency checks | one valid classification proceeds; invalid input stops | R43 |
| BND-STATE-001 | state-lifecycle | R8, R9, R13, R15, R16, R17, R18, R19, R20, R23, R37, R38, R39 | preparation, absent or existing branch/PR, mutation, read-back, reuse, blocked, or changed state | authority is independent and external success never settles lifecycle or implies readiness | safe operation reports exact state; unsupported state remains unchanged | R38 |
| BND-AUTH-001 | identity-authority | R5, R6, R11, R12, R13, R24, R25, R26, R28, R30, R36, R39 | portable or governed identity, verification owner, refresh scope, PR-state transition, and exact base/head tuple | loading and submission intent grant no unrelated authority | exact current authority permits only its bounded action; ambiguity stops | R13 |
| BND-COMPOSE-001 | composition-path | R1, R2, R3, R4, R6, R7, R41, R42, R46, R49 | universal skill, governed reference, structural asset, verify result/report, generated packages | one owner per rule and every required resource remains portable and present | valid package loads once; missing or drifting composition stops | R1 |
| BND-TEMPORAL-001 | temporal-retry | R28, R31, R32, R33, R34, R35, R36, R37, R38 | verified subject, evidence tail, preflight, push, reread, PR mutation, read-back, retry, and concurrent change | every decision-bearing identity is current at its use and retries reclassify | matching state completes once; changed state blocks or truthfully limits readiness | R37 |
| BND-RECOVERY-001 | failure-recovery | R7, R10, R18, R20, R23, R27, R29, R32, R33, R34, R35, R36, R37, R38 | missing evidence, blocked-before-write, partial external success, failed read-back, concurrent creation, or stale basis | no unsupported replay, inference, overwrite, or readiness claim | no-write failure blocks; confirmed partial success is reported and reconciled | R38 |
| BND-COMPAT-001 | compatibility-migration | R14, R24, R25, R26, R27, R42, R43, R44, R45, R46, R49 | normalized or legacy verify evidence, structural or semantic rule, parser-sensitive literal, canonical or derived resource | legacy evidence never gains inferred exactness and package parity remains exact | current basis proceeds; incomplete history routes to fresh verify; package drift blocks | R27 |
| BND-ENV-001 | external-environment | R9, R16, R17, R18, R19, R20, R22, R23, R31, R32, R33, R34, R35, R36, R38, R47 | local Git, remote Git, host PR, hosted CI, unavailable service, or concurrent actor | external facts are reread and never fabricated | safe calls succeed and read back; unavailability or change limits mutation or claims | R35 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R5, R6, R7 | BND-INPUT-001, BND-AUTH-001, BND-COMPOSE-001 | malformed governed evidence disappears and portable opening proceeds | every governed signal is classified and invalid signals stop without fallback |
| INT-002 | R8, R9, R10, R11, R12, R13 | BND-INPUT-001, BND-STATE-001, BND-AUTH-001 | creation intent silently grants refresh, publication, conversion, or preparation writes | each independent authority permits only its closed action and preparation writes nothing |
| INT-003 | R24, R25, R26, R27, R28, R29 | BND-AUTH-001, BND-COMPAT-001, BND-TEMPORAL-001 | historical or post-verify changes are inferred as an exact current basis | verify emits immutable identities and only the one closed evidence tail preserves readiness |
| INT-004 | R16, R17, R18, R31, R32 | BND-STATE-001, BND-TEMPORAL-001, BND-ENV-001 | ambiguous ancestry or remote work is overwritten | directional ancestry and immediate baseline reread permit only normal safe creation or fast-forward |
| INT-005 | R19, R20, R33, R34, R35, R37 | BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | stale preflight or retry creates a duplicate or mutates the wrong PR | post-push reread reclassifies and exact read-back confirms one matching PR |
| INT-006 | R32, R33, R35, R36, R38 | BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | base changes after verification while a successful external write is mistaken for readiness | external success is preserved as fact while readiness becomes false and fresh verification is required |
| INT-007 | R14, R15, R41 | BND-AUTH-001, BND-COMPOSE-001, BND-COMPAT-001 | a generated section refresh overwrites reviewer-authored body text | body bytes are preserved unless whole-body replacement is explicit; no section parser exists |
| INT-008 | R22, R23, R40 | BND-INPUT-001, BND-STATE-001, BND-ENV-001 | unavailable, pending, or stale CI is reported as passed | CI vocabulary and exact-head evidence constrain both body text and readiness claims |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | regression | R9 | BND-STATE-001 | PRSIM-PR4 | - |
| E2 | illustration | R15, R20 | BND-STATE-001, BND-ENV-001 | - | - |
| E3 | regression | R12, R13 | BND-AUTH-001 | PRSIM-PR4 | - |
| E4 | regression | R16, R17, R18 | BND-STATE-001, BND-ENV-001 | PRSIM-PR5 | - |
| E5 | regression | R32, R33, R35, R36, R38 | BND-TEMPORAL-001, BND-RECOVERY-001 | PRSIM-PR5 | - |
| E6 | illustration | R33, R34, R37 | BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E7 | regression | R11 | BND-AUTH-001 | PRSIM-PR6 | - |
| E8 | illustration | R5, R6 | BND-INPUT-001, BND-AUTH-001 | - | - |

## Compatibility and migration

The migration is atomic across the canonical `pr` package and directly coupled verify result/report wording and fixtures. Existing historical verify evidence remains readable but cannot authorize opening without the normalized immutable basis. New writers emit the normalized basis; `pr` never backfills or infers old evidence. Rollback restores the flat `pr` skill and previous verify wording, removes the new reference and asset, and regenerates derived packages without rewriting historical reports.

## Observability

The change is observable through exact operation results, requested and actual action fields, readiness booleans, hosted-CI state, remote and PR read-back identities, resource maps, semantic and literal ledgers, verification-basis fixtures, profile measurements, and canonical-through-installed parity evidence. Configured commands and executed commands remain distinct.

## Security and privacy

The skill must inspect the actual diff for secrets and sensitive content before external mutation and must not expose credentials. Unsafe repository, path, remote, host, or authority evidence fails closed. No new credential store, external persistence, or personal-data processing is introduced.

## Accessibility and UX

No end-user interface is introduced. Published Markdown and generated PR bodies must remain readable, use stable headings and concise tables where appropriate, and contain no placeholders.

## Performance expectations

Both PR0 portable and PR1 governed procedural assemblies must be smaller in LF-normalized words and bytes than the current flat baseline. No runtime latency or remote-provider performance contract is introduced.

## Edge cases

EC1. Remote evidence is unavailable during `prepare-only`: content may be prepared with explicit evidence limits and no opening readiness.

EC2. The remote branch appears between classification and push: the baseline is reread and the operation is reclassified or blocked.

EC3. Multiple matching PRs exist: state is `ambiguous` and no mutation occurs.

EC4. An adequate draft exists for default `open`: it is reused without publication.

EC5. Whole-body replacement is authorized but title refresh is not: only the body may change.

EC6. Push succeeds but PR creation fails: push is reported as external success, opening is blocked, and retry rereads rather than blindly recreating.

EC7. The verify evidence tail changes an unrelated field in `change.yaml`: verification is stale and opening blocks.

EC8. Hosted CI is pending for the exact head and policy permits post-open CI: opening may proceed, but the result and body say pending rather than passed.

EC9. A complete matching PR is merged: the skill reports the merged PR and stops without lifecycle completion or duplicate creation.

EC10. A required package resource is missing from an installed adapter: the dependent operation stops and parity validation fails.

## Non-goals

- Automatic merge, approval, release, deployment, publication, labels, reviewers, or downstream continuation.
- A provider-specific engine, new CLI, persistent PR transaction schema, or provider-neutral runtime abstraction.
- Markdown section mutation, managed markers, or body provenance parsing.
- Broader `verify` redesign beyond its existing result/report verification-basis contract.
- Lifecycle, plan, review, or workflow mutation by `pr`.
- Live acceptance PR creation or target-agent execution.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-PRSIM-001 | Exact verified subject and handoff identities are independently represented and safely related. |
| AC-PRSIM-002 | Only one direct-child verify-owned evidence commit with closed paths and fields may follow the verified subject. |
| AC-PRSIM-003 | Local handoff, pushed remote head, and PR head are identical for `pr-open-ready`. |
| AC-PRSIM-004 | Preparation performs zero external writes. |
| AC-PRSIM-005 | Submission, refresh, and existing-state transition authorities remain independent. |
| AC-PRSIM-006 | Adequate existing PRs are reused without mutation and draft/open state is preserved by default. |
| AC-PRSIM-007 | Body bytes change only under explicit whole-body replacement; no section mutation exists. |
| AC-PRSIM-008 | Directional branch relations prevent force, overwrite, delete, or loss of unseen remote work. |
| AC-PRSIM-009 | Remote base, head, and PR state are reread at every decision boundary and confirmed after mutation. |
| AC-PRSIM-010 | Concurrent matching-PR creation is reconciled without duplication. |
| AC-PRSIM-011 | Hosted-CI states are closed, exact-head-bound, and truthfully reported. |
| AC-PRSIM-012 | External success and readiness are separate when state changes concurrently. |
| AC-PRSIM-013 | Verify remains branch-ready owner and emits the complete normalized immutable basis on existing surfaces. |
| AC-PRSIM-014 | Legacy or incomplete verification evidence permits preparation only and routes opening to fresh verify. |
| AC-PRSIM-015 | Governed readiness is conditional, read-only, fail-closed, and cannot fall back from invalid signals. |
| AC-PRSIM-016 | Structural body groups have one asset owner without policy ownership or placeholders. |
| AC-PRSIM-017 | Unknown closed-vocabulary values fail before consistency checks and have regression tests. |
| AC-PRSIM-018 | PR0 and PR1 procedural profiles both decrease and total package change is reported separately. |
| AC-PRSIM-019 | Canonical, generated, archived, release-candidate, and clean-installed resources retain required parity. |
| AC-PRSIM-020 | Acceptance opens no live test PR and runs no target-agent runtime. |

## Open questions

None.

## Next artifacts

- Independent `spec-review`.
- Bounded architecture assessment.
- Execution plan and test specification after approval.

## Follow-on artifacts

None yet

## Readiness

Ready for independent `spec-review`.
