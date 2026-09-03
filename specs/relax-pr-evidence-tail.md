<!-- Template: spec-skeleton-v1 | Skill: spec | Template status: normative | Maintained alongside: skills/spec/SKILL.md | Readability contract: use normal Markdown prose and retain stable IDs and tables. -->

# Relax PR Evidence Tail Contract

## Owning change record

`docs/changes/2026-09-03-relax-pr-evidence-tail/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

`docs/proposals/2026-09-03-relax-pr-evidence-tail.md`

## Goal and context

Replace the PR skill's exact one-direct-child evidence-commit exception with a proportional rule that accepts a current attributable evidence-only suffix of any commit count. Preserve the actual safety property: no unreviewed product or governing change may enter the PR handoff after final Code Review.

This contract supersedes only the single-commit/direct-child definitions and requirements in `specs/pr-skill-simplification.md`, including its glossary entries for `handoff revision` and `evidence tail`, R28, the multi-commit portion of R29, INT-003's single-tail wording, EC7's topology assumption, AC-PRSIM-002, and directly equivalent prose. Every other PR submission, authority, remote, CI, retry, mutation, read-back, packaging, and claim requirement remains current.

## Glossary

| Term | Meaning |
| --- | --- |
| reviewed subject | The exact product revision named by final Code Review and the successful Verify basis. |
| handoff revision | The current local revision eligible to become the remote and PR head. |
| evidence suffix | The cumulative final change between reviewed subject and handoff containing only current attributable review, workflow, and Verify evidence for the exact governed change. |
| protected surface | Implementation, test, specification, architecture, plan, dependency, configuration, generated-product, public-documentation, identity, or other decision-bearing content that requires review when changed. |
| attributable evidence | Change-local evidence whose path, content identity, stage owner, and current lifecycle references agree for the exact governed change. |

## Examples first

Example E1: normal governed closeout
Given final Code Review names product revision `S`
And later commits record the final review, route into Verify, and record a successful Verify result
When PR evaluates handoff `H`
Then it accepts the suffix regardless of commit count when the cumulative `S..H` change contains only current attributable evidence.

Example E2: product drift
Given a successful Verify result names reviewed subject `S`
And implementation or test content differs between `S` and handoff `H`
When PR evaluates readiness
Then it blocks before external mutation and routes the drift to its owner.

Example E3: mixed suffix
Given the suffix contains valid review evidence and an unrelated documentation change
When PR classifies the cumulative change
Then the suffix is invalidating as a whole and opening does not proceed.

Example E4: stale lifecycle evidence
Given every post-review path is under the exact change root
But the review digest, lifecycle state, or Verify registration is stale or inconsistent
When PR evaluates attribution
Then path membership alone is insufficient and readiness blocks.

Example E5: same revision
Given the reviewed subject equals the local handoff revision
When every other PR readiness condition passes
Then no evidence suffix is required and ordinary opening may proceed.

## Requirements

R1. `pr` MUST consume the current successful Verify basis and retain `verified_subject_revision` as the reviewed product identity.

R2. The local handoff revision MUST equal the current local branch head selected for push and PR creation or reuse.

R3. The reviewed subject MUST equal or be a Git ancestor of the handoff revision; a non-ancestor, missing, or ambiguous relationship MUST block opening.

R4. When the identities differ, `pr` MUST evaluate the cumulative final change from reviewed subject to handoff and MUST NOT require a fixed commit count, direct-child relationship, linear first-parent shape, commit-message pattern, or stage-owner label as an independent readiness condition.

R5. The suffix classification MUST be exactly `none`, `evidence-only`, or `invalidating`; an unknown or unresolved classification MUST fail closed before consistency checks.

R6. `none` MUST apply only when reviewed subject and handoff are identical.

R7. `evidence-only` MUST require every cumulative post-review change to be current attributable review, workflow, or Verify evidence for the exact governed change.

R8. Permitted review evidence MAY include current formal review records, `review-log.md`, conditional `review-resolution.md`, and their matching registered identities.

R9. Permitted workflow evidence MAY include exact same-change lifecycle operation requests or receipts and current mutable lifecycle, review, milestone, correction, validation, or routing state in the owning change record.

R10. Permitted Verify evidence MAY include the final Verify report and its matching current registration in the owning change record.

R11. Evidence path membership, file naming, commit messages, or author identity alone MUST NOT establish attribution.

R12. Governed attribution MUST require one exact change identity, current lifecycle validation, closed review state, current referenced content identities, and a current successful Verify report and registration.

R13. A change to implementation, tests, specifications, architecture, plans, dependencies, configuration, generated product output, public documentation outside the exact governed evidence pack, another governed change, or another decision-bearing surface MUST be `invalidating`.

R14. Mixed evidence and protected changes, unknown paths, stale identities, conflicting ownership, missing required evidence, unsafe paths, or ambiguous classification MUST be `invalidating`.

R15. Mutable change-record edits MUST be attributable to current lifecycle, review, milestone, correction, validation, or routing ownership; changes to the change identity, classification, risk, governed artifact content, or another non-lifecycle owner MUST be invalidating.

R16. An `invalidating` suffix MUST block push and PR mutation under a clean-readiness claim, identify the affected paths or authority gap, and route to the earliest applicable review, authoring, implementation, or Verify owner.

R17. An `evidence-only` suffix MUST preserve Verify's existing `branch-ready` authority and MUST NOT independently create, repair, or upgrade readiness.

R18. The handoff revision, pushed remote head, and PR head MUST still be identical before `pr-open-ready` may be true.

R19. Existing verified-base, merge-base, remote-branch, matching-PR, hosted-CI, refresh, draft, retry, mutation-order, and read-back requirements MUST remain unchanged.

R20. `pr` MUST NOT mutate lifecycle, review, workflow, Verify, plan, merge, release, or publication state while classifying the suffix.

R21. Historical Verify reports and merged PRs MUST remain historical and MUST NOT be reinterpreted as new readiness decisions.

R22. The revised public skill MUST remain customer-project portable and MUST resolve governed evidence from project-local authority without publishing repository-maintainer source, generation, archive, or release mechanics.

R23. Canonical, generated, archived, release-candidate, and clean-installed Codex, Claude Code, and opencode packages MUST preserve the revised PR and directly coupled Verify wording with raw-byte parity through existing tooling.

R24. Every new closed vocabulary introduced by this change MUST reject unknown values explicitly before dependent consistency checks and MUST have an unknown-value regression test.

## Important scenarios

- A final review receipt, review log update, workflow transition request, change-record transition, Verify report, and Verify registration occupy several commits but no protected surface changes: the suffix is `evidence-only`.
- A change-local review file exists but is not referenced by current review state: attribution fails and the suffix is `invalidating`.
- The owning `change.yaml` changes only current final-review, stage-transition, and Verify-registration state and passes authoritative lifecycle validation: it may be evidence-only.
- The owning `change.yaml` also changes its `change_id`, classification, risk, or governed artifact map without matching owner authority: the suffix is invalidating.
- A specification edit is later reverted before handoff so the cumulative reviewed-to-handoff product content is unchanged: commit count or intermediate history alone does not invalidate; current final content and evidence authority govern readiness.
- A merge commit exists after the reviewed subject but its cumulative final difference is current attributable evidence only: merge topology alone does not invalidate.
- The remote base advances after local suffix validation: existing base-currentness rules still block `pr-open-ready` and require fresh verification or the approved base-update route.

## Acceptance conditions

- A real governed evidence suffix shaped like the closeout used by PR #169 is accepted without a one-commit exception.
- Same-revision handoff remains accepted.
- Product, governing, mixed, unknown, stale, and cross-change suffixes block before external mutation.
- Current Verify ownership and every existing external-operation safety boundary remain intact.
- Published package and adapter parity remain deterministic.

## Inputs and outputs

Inputs are the successful Verify basis and report, reviewed subject, local handoff, cumulative Git diff, exact governed change identity, current lifecycle and review evidence, remote state, and intended PR operation. Output adds one suffix classification and its supporting evidence or blocker to the existing PR readiness result; it creates no new durable state.

## State and invariants

- The reviewed subject remains the product revision approved by final Code Review.
- Evidence-only suffixes never authorize product drift.
- Commit count and topology are not substitutes for final-state and authority validation.
- Verify owns `branch-ready`; PR owns PR-body and PR-opening readiness.
- PR classification is read-only.
- External success remains distinct from readiness.

## Error and boundary behavior

Non-ancestor revisions, unresolved change identity, invalid lifecycle state, open review closeout, stale Verify registration, unsafe path, protected change, mixed suffix, cross-change evidence, missing attribution, or unknown classification blocks before external mutation. A failure after an independently authorized external write remains reported truthfully under the unchanged PR transaction contract.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22, R23, R24

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | R3, R5, R6, R7, R13, R14, R24 | BND-INPUT-001 | - |
| state-lifecycle | applicable | R7, R8, R9, R10, R12, R15, R16, R17, R20, R21 | BND-STATE-001 | - |
| identity-authority | applicable | R1, R2, R3, R7, R11, R12, R15, R17, R18, R20 | BND-AUTH-001 | - |
| composition-path | applicable | R4, R7, R8, R9, R10, R13, R14, R15, R22, R23 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | R2, R3, R4, R16, R18, R19, R21 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | R3, R12, R14, R15, R16, R19 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | R4, R19, R21, R22, R23 | BND-COMPAT-001 | - |
| external-environment | applicable | R2, R3, R18, R19 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | R3, R5, R6, R7, R13, R14, R24 | same revision, ancestor, non-ancestor, none, evidence-only, invalidating, unknown | suffix classification is closed and unknown fails first | valid classification continues; invalid or unknown blocks | R24 |
| BND-STATE-001 | state-lifecycle | R7, R8, R9, R10, R12, R15, R16, R17, R20, R21 | current, stale, open, closed, registered, missing, conflicting, historical | evidence must remain current and PR classification mutates no lifecycle state | current evidence may proceed; other states block or remain historical | R20 |
| BND-AUTH-001 | identity-authority | R1, R2, R3, R7, R11, R12, R15, R17, R18, R20 | reviewed subject, handoff, exact change, evidence owner, Verify authority, remote and PR heads | names and paths alone grant no authority; Verify remains branch-ready owner | matching current authority proceeds; mismatch blocks | R17 |
| BND-COMPOSE-001 | composition-path | R4, R7, R8, R9, R10, R13, R14, R15, R22, R23 | review evidence, workflow evidence, Verify evidence, protected surface, mixed suffix, generated package | every cumulative change is attributable evidence or the whole suffix invalidates | coherent evidence proceeds; mixed, protected, or package drift blocks | R14 |
| BND-TEMPORAL-001 | temporal-retry | R2, R3, R4, R16, R18, R19, R21 | reviewed subject, additive evidence, handoff, push, PR mutation, read-back, retry | current final state and authority govern; remote identities are reread | stable state proceeds; changed state reclassifies or blocks | R19 |
| BND-RECOVERY-001 | failure-recovery | R3, R12, R14, R15, R16, R19 | invalidating change, stale evidence, partial external success, correction, fresh review, fresh Verify | no invalid suffix is repaired or ignored by PR | block and route before write; preserve truthful external facts after write | R16 |
| BND-COMPAT-001 | compatibility-migration | R4, R19, R21, R22, R23 | old one-commit rule, new proportional rule, historical reports, mixed package, rollback | current invocations use one coherent rule and historical evidence gains no new authority | coherent current packages proceed; historical remains historical; mixed blocks | R21 |
| BND-ENV-001 | external-environment | R2, R3, R18, R19 | local Git, remote Git, PR host, unavailable or changed state | local handoff, remote head, and PR head agree before readiness | matching environment proceeds; unavailable or changed state limits action or claims | R18 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | R4, R7, R8, R9, R10, R13, R14 | BND-INPUT-001, BND-COMPOSE-001 | several valid evidence commits are rejected by topology alone or a protected change hides beside evidence | classify the cumulative suffix by content and authority, accepting only wholly evidence-only outcomes |
| INT-002 | R11, R12, R15, R17, R20 | BND-STATE-001, BND-AUTH-001, BND-COMPOSE-001 | a path-shaped or self-authored record acquires readiness authority | require current lifecycle, review, and Verify identities while keeping PR read-only |
| INT-003 | R2, R3, R18, R19 | BND-AUTH-001, BND-TEMPORAL-001, BND-ENV-001 | a locally valid suffix is pushed against changed base or remote state | preserve exact handoff and remote rereads before readiness |
| INT-004 | R16, R19, R21 | BND-TEMPORAL-001, BND-RECOVERY-001, BND-COMPAT-001 | an invalid suffix is rewritten, grandfathered, or silently retried | route to the owner and require current review or Verify without reinterpreting history |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | regression | R4, R7, R8, R9, R10 | BND-COMPOSE-001, BND-TEMPORAL-001 | PRTAIL-001 | - |
| E2 | regression | R13, R16 | BND-COMPOSE-001, BND-RECOVERY-001 | PRTAIL-002 | - |
| E3 | regression | R14, R16 | BND-INPUT-001, BND-COMPOSE-001 | PRTAIL-003 | - |
| E4 | regression | R11, R12, R14 | BND-STATE-001, BND-AUTH-001 | PRTAIL-004 | - |
| E5 | illustration | R6 | BND-INPUT-001 | - | - |

## Compatibility and migration

Current PR invocations adopt the proportional suffix rule atomically across the canonical PR package, directly coupled Verify wording, tests, and generated adapters. Historical reports, branches, and merged PRs remain unchanged and gain no current authority. Rollback restores the prior one-direct-child wording and its fixtures as one coherent package without rewriting repository history.

## Observability

Each PR result reports the reviewed subject, local handoff, suffix classification, supporting evidence or invalidating paths, requested and actual operation, remote and PR identities, CI state, blockers, and claim limitations. No new logs, metrics service, or persistent transaction record is introduced.

## Security and privacy

The change preserves actual-diff inspection, secret and sensitive-content checks, exact repository and remote identity, no-force push behavior, and fail-closed ambiguity. It introduces no credentials, new data collection, external persistence, or personal-data processing.

## Accessibility and UX

No user interface is introduced. Published Markdown and PR results must use concise terms, identify why a suffix was accepted or rejected, and avoid exposing repository-maintainer-only mechanics in customer-facing instructions.

## Performance expectations

Suffix inspection must remain bounded to the reviewed-subject-to-handoff comparison and exact current governed evidence. No fixed commit-count or repository-size performance target is introduced, and no new network calls are required beyond existing PR readiness checks.

## Edge cases

EC1. Reviewed subject equals handoff: classify `none`.

EC2. Reviewed subject is not an ancestor: classify `invalidating` and block.

EC3. Multiple evidence commits affect only exact current review, workflow, and Verify evidence: classify `evidence-only`.

EC4. One suffix commit combines permitted evidence and a protected change: classify `invalidating`.

EC5. Every changed path is under the change root but one identity is stale or unreferenced: classify `invalidating`.

EC6. Intermediate history changed and restored protected content, leaving no cumulative protected difference: topology alone does not invalidate the current final state.

EC7. The suffix contains evidence for another change ID: classify `invalidating`.

EC8. Remote state changes after classification: apply existing reread and readiness rules.

## Non-goals

- New stored revision, evidence-tail, or PR transaction schemas.
- A fixed maximum evidence-commit count or direct-parent requirement.
- Post-review changes to product, governing artifacts, dependencies, configuration, tests, or generated product output.
- History rewriting, force pushing, automatic merging, or expanded external mutation.
- Redesigning PR body refresh, draft transitions, hosted CI, remote relations, or provider integrations.
- Reinterpreting historical Verify or PR outcomes.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-PRTAIL-001 | Same-revision and multi-commit current evidence-only handoffs are accepted without a fixed topology rule. |
| AC-PRTAIL-002 | Reviewed subject must equal or precede handoff in Git ancestry. |
| AC-PRTAIL-003 | Cumulative suffix classification uses the closed `none`, `evidence-only`, and `invalidating` outcomes and rejects unknown values. |
| AC-PRTAIL-004 | Current final review, review closeout, workflow transition, Verify report, and Verify registration may compose as evidence-only. |
| AC-PRTAIL-005 | Path membership or commit metadata alone cannot establish evidence authority. |
| AC-PRTAIL-006 | Product, governing, mixed, unknown, stale, and cross-change suffixes block before external mutation. |
| AC-PRTAIL-007 | Verify remains the sole `branch-ready` owner and PR classification remains read-only. |
| AC-PRTAIL-008 | Local handoff, pushed remote head, and PR head still agree before `pr-open-ready`. |
| AC-PRTAIL-009 | Existing remote, PR, CI, refresh, draft, retry, mutation, and read-back protections remain unchanged. |
| AC-PRTAIL-010 | Historical evidence remains unchanged and mixed current package wording fails validation. |
| AC-PRTAIL-011 | Canonical and supported generated/installed packages preserve the revised contract with deterministic parity. |
| AC-PRTAIL-012 | No new runtime service, dependency, lifecycle stage, persistent transaction, or stored revision identity is introduced. |

## Open questions

None.

## Next artifacts

- Design Review of this specification with `docs/architecture/2026-09-03-relax-pr-evidence-tail.md`.
- Delivery plan after Design approval.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review with the exact architecture package. Implementation and PR readiness remain unclaimed.
