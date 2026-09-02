# Impact-Aware Final Verification

## Owning change record

`docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Simplify Final Verification and Retire Explain Change](../docs/proposals/2026-08-31-simplify-final-verification-retire-explain-change.md)

## Goal and context

RigorLoop must replace the separate `explain-change -> verify` closeout sequence with one final Verify stage that selects evidence according to actual impact, preserves explicit freshness requirements, decides readiness, and produces the durable final explanation only when the exact verified subject is ready for PR handoff.

This contract removes ceremony without weakening review, traceability, failure handling, historical readability, or final-readiness authority.

## Glossary

- **Verified subject:** The exact final reviewed product and governing-change subject evaluated by Verify.
- **Impact surface:** A system or delivery area whose change can affect evidence applicability.
- **Proved surface:** The behavior, artifact, environment, or policy property demonstrated by one evidence item.
- **Evidence applicability:** Whether an existing result still proves its intended surface for the verified subject.
- **Always-current:** Evidence or a check whose meaning depends on current repository or lifecycle state and must be evaluated in every final attempt.
- **Fresh-required:** Evidence that an approved plan or governing policy requires to be newly executed for the final attempt.
- **Impact-sensitive:** Evidence that may remain current when later changes cannot affect its proved surface.
- **Verify evidence tail:** The closed Verify report and matching lifecycle-recording writes after the reviewed subject.
- **V3:** `stage-owned-change-local-v3`, the active lifecycle contract without standalone test-spec or explain-change stages.

## Examples first

Example E1: Successful final verification produces the explanation
Given final holistic Code Review is current and all required evidence passes
When Verify completes its impact, applicability, execution, and current-state checks
Then Verify records `branch-ready`, the final evidence basis, and the final change explanation in one successful report for PR consumption

Example E2: Failed verification produces no final explanation
Given Verify finds a failing check, stale review, missing allocation, or ambiguous impact
When the attempt concludes
Then it records the blocker and owning correction stage, emits no final change explanation, and grants no `branch-ready`

Example E3: Clearly unaffected evidence remains current
Given product tests passed for the reviewed subject
And a later repository-metadata change is affirmatively shown not to affect runtime, build, packaging, generated output, governed discovery, or another proved product surface
When Verify evaluates applicability
Then the product-test evidence may be reused while metadata-specific and always-current checks still run

Example E4: Unknown impact expands verification
Given a later change may affect a required evidence surface but the effect cannot be established confidently
When Verify classifies impact
Then the surface is `unknown`, prior evidence is not reused on that basis, and verification broadens

Example E5: Freshness policy overrides reuse
Given an approved plan marks hosted CI or a release-sensitive check fresh-required
And the final diff appears unrelated to its proved surface
When Verify selects final evidence
Then the check still reruns or obtains the required fresh observation

Example E6: Correction preserves only unaffected evidence
Given a Verify failure routes an implementation correction and required rereview
When Verify runs again on the corrected subject
Then it re-evaluates every evidence item and may reuse only evidence affirmatively unaffected by the correction and current policy

Example E7: PR consumes the exact Verify result
Given Verify records a successful report and no later invalidating drift occurs
When PR prepares its handoff
Then it consumes that report's explanation and evidence basis without authoring a competing final rationale

Example E8: Historical explanation remains historical
Given a completed v1 or v2 change contains an explain-change artifact or stage record
When current tooling reads the record
Then it remains readable as historical evidence but grants no current lifecycle progression and is not interpreted as a v3 prerequisite

Example E9: Product drift after Verify invalidates readiness
Given a successful Verify report exists for reviewed subject `S`
When a later commit changes product, governing design, plan allocation, dependencies, generated product, or unrelated documentation outside the permitted Verify tail
Then the prior `branch-ready` result is stale and the change returns to the applicable owner, review, or Verify boundary

## Requirements

| ID | Requirement |
| --- | --- |
| FV-R1 | Newly governed v3 changes MUST use the final sequence `code-review -> review-resolution when triggered -> ci-maintenance when triggered -> verify -> pr` and MUST NOT route through `explain-change`. |
| FV-R2 | V3 lifecycle state, routing, schemas, validators, current templates, and public stage inventories MUST NOT require or create an active `explain-change` stage or artifact. |
| FV-R3 | Verify MUST NOT require a current explain-change artifact as a final-readiness prerequisite for v3 changes. |
| FV-R4 | Historical explain-change artifacts, review evidence, release archives, and settled v1 or v2 lifecycle records MUST remain readable without migration or retroactive invalidation, but MUST grant no current progression authority. |
| FV-R5 | `stage-owned-change-local-v3` MUST be the sole current executable lifecycle contract after coherent activation; current tooling MUST NOT maintain v1/v2 progression branches or a compatibility allowlist. |
| FV-R6 | Any non-v3 or unknown contract presented for current progression, any contract-class mismatch, and any v3 state containing active explain-change values MUST fail closed before consistency interpretation. |
| FV-R7 | The implementing v2 change MUST complete through the last coherent v2 package before v3 activation; the activated package MUST NOT reinterpret or continue its historical state. |
| FV-R8 | Final Verify MUST resolve exactly one repository, governed change, verified subject, final holistic Code Review basis, approved Design package, approved Delivery plan, and final diff before selecting evidence. |
| FV-R9 | Verify MUST use the approved Delivery plan's verification allocation as the initial required evidence map and MUST NOT silently replace or weaken it. |
| FV-R10 | Verify MUST classify every relevant final-diff surface using a closed impact vocabulary whose outcomes distinguish `affected`, `unaffected`, and `unknown`. |
| FV-R11 | Impact classification MUST cover every applicable runtime, API, persistence, migration, dependency, build, packaging, generated-output, security or authority, documentation, repository-metadata, lifecycle-governance, and external-environment surface without requiring inapplicable surfaces to be treated as affected. |
| FV-R12 | `unaffected` MUST require affirmative evidence that the final change cannot materially affect the surface; filename, extension, directory, author assertion, or absence of an obvious match alone MUST NOT establish it. |
| FV-R13 | `unknown` or ambiguous impact MUST expand verification and MUST NOT narrow it. |
| FV-R14 | Every required evidence item MUST receive exactly one final applicability decision: `reuse`, `rerun`, or `newly-required`; unknown decision values MUST fail closed. |
| FV-R15 | `reuse` MUST require an existing passing result, a known proved surface, current governing authority, affirmative non-impact reasoning, sufficient identity or cutoff evidence, and no applicable freshness override. |
| FV-R16 | `rerun` MUST apply when evidence is affected, stale, failing, conflicting, ambiguous, environment-invalidated, policy-fresh, or otherwise insufficient for its claim. |
| FV-R17 | `newly-required` MUST apply when the final diff or current policy introduces a relevant obligation absent from the approved evidence map; a material plan allocation gap MUST route to plan ownership rather than be silently normalized by Verify. |
| FV-R18 | Every evidence obligation MUST use exactly one freshness class: `always-current`, `fresh-required`, or `impact-sensitive`; unknown freshness values MUST fail closed. |
| FV-R19 | Always-current checks MUST cover current change and repository identity, reviewed-subject and review identity, lifecycle and package consistency, review closeout, blocker state, final diff classification, required artifact and evidence existence, and complete Verify-result consistency. |
| FV-R20 | Approved plan or governing-policy fresh requirements, required hosted CI, and applicable security-, release-, or environment-sensitive proof MUST override ordinary impact-based reuse. |
| FV-R21 | Impact-based evidence reuse MUST remain distinct from execution caching; a cache hit MUST NOT independently establish a new pass or final readiness. |
| FV-R22 | Verify MUST run every applicable `rerun`, `newly-required`, `fresh-required`, and `always-current` check and MUST report the exact commands and observed results. |
| FV-R23 | A failed or inconclusive Verify attempt MUST record blockers and evidence gaps, MUST identify the owning correction stage, MUST omit the final change explanation, and MUST NOT grant `branch-ready`. |
| FV-R24 | Verify MUST remain read-only with respect to implementation and upstream governed artifacts and MUST return correction to the owning stage with required rereview rather than repairing and continuing. |
| FV-R25 | A later Verify attempt MUST re-evaluate all evidence against the corrected subject and MAY reuse only evidence that remains affirmatively applicable under current policy. |
| FV-R26 | A successful Verify report MUST record the verified subject, final review basis, approved package identities, final impact classification, every evidence decision and rationale, actual-run results, observed CI status or gap, always-current results, normalized verification basis, residual risks, and `branch-ready`. |
| FV-R27 | A successful Verify report MUST contain the final durable explanation of what changed, why it changed, how it realizes approved requirements and design, important implementation choices, supporting evidence, limitations, and residual risks. |
| FV-R28 | The final explanation MUST be absent from failed and inconclusive reports and MUST NOT exist as a separately settled v3 lifecycle artifact. |
| FV-R29 | PR preparation MUST consume the exact current successful Verify explanation and evidence basis and MUST NOT introduce a competing authoritative rationale or new authoritative artifact reference without revalidation. |
| FV-R30 | Verify MUST continue to own `branch-ready`; PR MUST continue to own PR-body and PR-opening readiness; Workflow MUST continue to own routing. |
| FV-R31 | The verified subject MUST remain the reviewed product subject, and the successful Verify report MUST NOT embed its own Git commit identity. |
| FV-R32 | The Verify report and matching lifecycle recording MUST form a closed evidence tail whose allowed paths and fields exclude product, requirement, architecture, plan, dependency, generated-product, and unrelated documentation changes. |
| FV-R33 | Any invalidating change after the verified subject or any mismatch in subject, review, plan, policy, evidence, report, or lifecycle identity MUST stale the prior result and route to the applicable owner or review boundary. |
| FV-R34 | Interrupted or partial Verify output MUST grant no readiness authority; an identical complete registered replay MUST be idempotent, while any changed basis MUST be evaluated as a new attempt. |
| FV-R35 | The standalone authored `skills/explain-change/` package and its current generated publication entries MUST be removed at v3 activation; historical release archives MUST remain unchanged. |
| FV-R36 | The `verify` package MUST use progressive disclosure so scoped verification does not load final-impact or explanation procedure, while final readiness loads all procedure needed for applicability and successful explanation. |
| FV-R37 | Governance, workflow specs, architecture, skills, resources, templates, schemas, validators, fixtures, docs, adapter manifests, generated packages, and release validation MUST activate the v3 contract coherently; mixed current packages MUST fail validation. |
| FV-R38 | Every new closed validator vocabulary introduced by this change MUST reject an unknown value explicitly before consistency checks and MUST have an unknown-value regression test. |

## Important scenarios

- A documentation change alters generated-site build inputs; Verify classifies build and generated-output surfaces as affected despite the `.md` extension.
- A `.gitignore` change can alter generated-output discovery or package contents; reuse is allowed only after those surfaces are affirmatively excluded.
- A review-evidence-only tail changes no product surface but still requires always-current lifecycle, review, diff, and report checks.
- A dependency lockfile changes after tests pass; dependency, build, packaging, runtime, security, and environment impact are evaluated rather than assumed.
- Hosted CI passed for an earlier subject but policy requires current hosted evidence; local success cannot substitute.
- A plan omitted verification for a newly exposed migration path; Verify routes to plan and emits no final explanation.
- Verify passes substantive checks but report recording is interrupted; no branch-ready authority exists until one complete report and lifecycle record are current.
- A current adapter package still publishes `explain-change` after v3 activation; package parity fails even when canonical workflow text is correct.

## Acceptance conditions

- The active v3 graph contains no standalone explain-change stage or prerequisite.
- Every final evidence item is traceable to its planned or newly applicable obligation and one closed applicability decision.
- Narrow reuse is supported only by affirmative surface reasoning; uncertainty broadens.
- Fresh-policy and always-current proof cannot be bypassed by impact classification.
- Failed attempts contain blockers but no final explanation or branch-ready claim.
- Successful reports contain one PR-consumable explanation bound to the exact evidence basis.
- Historical records remain readable without executable authority, and current mixed packages fail closed.

## Inputs and outputs

Inputs are the accepted proposal and Proposal Review ID, approved Design package, approved Delivery plan and verification allocation, exact final reviewed subject and Code Review evidence, review resolution, triggered CI-maintenance result, actual final diff, existing validation and CI evidence, generated-output state, lifecycle state, and applicable freshness policy.

Outputs are a failed or inconclusive Verify result containing blockers and ownership, or one successful `verify-report.md` containing impact and applicability reasoning, required executions, readiness evidence, normalized verification basis, `branch-ready`, and the final explanation. The result never performs implementation repair, workflow routing, PR creation, publication, release, or deployment.

## State and invariants

- V3 has no active explain-change stage or independently settled final-explanation artifact.
- A final explanation exists only inside a successful current Verify result.
- `branch-ready` implies every required evidence item has one valid decision and every required execution or observation passed.
- `reuse` never changes a prior result into a new actual run.
- The approved plan remains the initial evidence authority; Verify may add obligations but cannot erase them.
- Unknown impact, freshness, decision, lifecycle, or outcome values cannot support readiness.
- The verified subject and final-review basis remain stable across the Verify evidence tail.
- Historical contract interpretation never grants current progression authority.

## Error and boundary behavior

- Missing or ambiguous target, review, package, plan, diff, evidence, surface, policy, or identity blocks the dependent decision.
- A failed required command blocks readiness and routes to its owner; successful unrelated checks do not downgrade the blocker.
- A new normative behavior or missing system requirement routes to specification ownership.
- A missing technical realization routes to architecture ownership.
- A missing verification allocation routes to plan ownership.
- An implementation defect routes to implementation and required Code Review.
- A stale or incomplete formal review routes to its review owner or resolution flow.
- A hosted CI requirement remains unsatisfied until current hosted evidence is observed.
- A report write, read-back, or lifecycle-registration failure leaves the attempt without successful readiness authority.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: FV-R1, FV-R2, FV-R3, FV-R4, FV-R5, FV-R6, FV-R7, FV-R8, FV-R9, FV-R10, FV-R11, FV-R12, FV-R13, FV-R14, FV-R15, FV-R16, FV-R17, FV-R18, FV-R19, FV-R20, FV-R21, FV-R22, FV-R23, FV-R24, FV-R25, FV-R26, FV-R27, FV-R28, FV-R29, FV-R30, FV-R31, FV-R32, FV-R33, FV-R34, FV-R35, FV-R36, FV-R37, FV-R38

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | FV-R8, FV-R9, FV-R10, FV-R11, FV-R12, FV-R13, FV-R14, FV-R15, FV-R16, FV-R17, FV-R18, FV-R20, FV-R21, FV-R22 | BND-INPUT-001 | - |
| state-lifecycle | applicable | FV-R1, FV-R2, FV-R3, FV-R4, FV-R5, FV-R6, FV-R7, FV-R23, FV-R25, FV-R26, FV-R28, FV-R33, FV-R34, FV-R35, FV-R37 | BND-STATE-001 | - |
| identity-authority | applicable | FV-R8, FV-R9, FV-R17, FV-R23, FV-R24, FV-R26, FV-R29, FV-R30, FV-R31, FV-R32, FV-R33 | BND-AUTH-001 | - |
| composition-path | applicable | FV-R9, FV-R19, FV-R21, FV-R26, FV-R27, FV-R29, FV-R32, FV-R35, FV-R36, FV-R37 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | FV-R23, FV-R25, FV-R31, FV-R32, FV-R33, FV-R34 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | FV-R13, FV-R16, FV-R17, FV-R20, FV-R22, FV-R23, FV-R24, FV-R25, FV-R33, FV-R34 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | FV-R4, FV-R5, FV-R6, FV-R7, FV-R28, FV-R35, FV-R37 | BND-COMPAT-001 | - |
| external-environment | applicable | FV-R16, FV-R18, FV-R20, FV-R21, FV-R22, FV-R26 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | FV-R8, FV-R9, FV-R10, FV-R11, FV-R12, FV-R13, FV-R14, FV-R15, FV-R16, FV-R17, FV-R18, FV-R20, FV-R21, FV-R22 | target exact or ambiguous; surface affected, unaffected, or unknown; evidence pass, fail, stale, missing, or conflicting; decision reuse, rerun, or newly-required; freshness always-current, fresh-required, or impact-sensitive | Every required input resolves under a closed value before readiness; unaffected and reuse require affirmative evidence. | Exact sufficient inputs permit selection and execution; ambiguity, unknown impact, or insufficient evidence broadens or blocks. | FV-R14 |
| BND-STATE-001 | state-lifecycle | FV-R1, FV-R2, FV-R3, FV-R4, FV-R5, FV-R6, FV-R7, FV-R23, FV-R25, FV-R26, FV-R28, FV-R33, FV-R34, FV-R35, FV-R37 | current v3 or historical non-v3 record; attempt pending, failed, inconclusive, successful, interrupted, or stale; report absent, partial, current, or stale | Only a complete current successful v3 Verify result contains final explanation and grants branch-ready; historical state grants no progression. | Current v3 success permits PR handoff; historical or other non-success state withholds readiness and stops or routes. | FV-R26 |
| BND-AUTH-001 | identity-authority | FV-R8, FV-R9, FV-R17, FV-R23, FV-R24, FV-R26, FV-R29, FV-R30, FV-R31, FV-R32, FV-R33 | proposal, Design, Delivery, reviewed subject, review, Verify, Workflow, PR, and correction-owner identities; current, stale, missing, or mismatched authority | Each stage writes only its owned surface; Verify never repairs or routes; PR consumes only current Verify authority. | Current identities permit judgment and handoff; stale or mismatched authority blocks and names the owner. | FV-R30 |
| BND-COMPOSE-001 | composition-path | FV-R9, FV-R19, FV-R21, FV-R26, FV-R27, FV-R29, FV-R32, FV-R35, FV-R36, FV-R37 | plan map to evidence; diff to impact; evidence to verdict; verdict to explanation; Verify result to PR; canonical skill to generated package | One traceable chain produces one authoritative successful result; cache, historical skill, or PR prose cannot bypass it. | Coherent composition supports readiness; missing mappings or mixed packages block. | FV-R26 |
| BND-TEMPORAL-001 | temporal-retry | FV-R23, FV-R25, FV-R31, FV-R32, FV-R33, FV-R34 | first attempt, correction, rereview, retry, interruption, identical replay, changed-basis replay, later drift | Every attempt binds one subject and basis; identical complete replay is idempotent; changed basis requires re-evaluation. | Retry succeeds only from current evidence; interruption and drift withhold or stale readiness. | FV-R34 |
| BND-RECOVERY-001 | failure-recovery | FV-R13, FV-R16, FV-R17, FV-R20, FV-R22, FV-R23, FV-R24, FV-R25, FV-R33, FV-R34 | unknown impact, failed check, missing allocation, stale review, report failure, owner correction, rereview, reattempt | Verify records and routes but never repairs; unaffected evidence is reconsidered rather than automatically discarded or retained. | Safe recovery returns through the owning stage and a new final attempt; unresolved failure blocks. | FV-R24 |
| BND-COMPAT-001 | compatibility-migration | FV-R4, FV-R5, FV-R6, FV-R7, FV-R28, FV-R35, FV-R37 | historical non-v3 record; current v3 record; coherent or mixed package; pre- or post-v3 activation | Historical evidence remains readable but only v3 grants current execution; unknown, non-v3 progression, or mixed state fails closed. | Coherent activation enables v3; prior records remain non-executable history; invalid classification blocks. | FV-R5 |
| BND-ENV-001 | external-environment | FV-R16, FV-R18, FV-R20, FV-R21, FV-R22, FV-R26 | local command, hosted CI, release environment, security environment, cache context, current or changed environment | Local evidence never claims hosted observation; environment-sensitive and explicitly fresh proof remains fresh-required. | Required current observation supports readiness; unavailable or stale external evidence blocks or remains a named gap. | FV-R20 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | FV-R12, FV-R13, FV-R15, FV-R20 | BND-INPUT-001, BND-ENV-001 | A narrow-looking diff is classified unaffected while policy or environment makes prior evidence stale. | Freshness and environment override reuse; uncertainty broadens. |
| INT-002 | FV-R23, FV-R24, FV-R25, FV-R33 | BND-STATE-001, BND-AUTH-001, BND-RECOVERY-001, BND-TEMPORAL-001 | Verify repairs a failure or carries prior evidence across a changed basis without owner correction and rereview. | Verify routes the blocker; a new attempt re-evaluates all evidence after authorized correction. |
| INT-003 | FV-R26, FV-R27, FV-R29, FV-R31, FV-R32 | BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001 | Generating the final explanation creates a self-referential or unreviewed product identity. | The report binds the reviewed subject, omits its own commit identity, and only closed Verify evidence writes follow review. |
| INT-004 | FV-R4, FV-R5, FV-R6, FV-R35, FV-R37 | BND-STATE-001, BND-COMPOSE-001, BND-COMPAT-001 | Current packages remove explain-change while tooling grants historical records progression or publishes mixed stage inventories. | V3 activates coherently; historical records remain readable only; non-v3 progression, mixed, or unknown state fails closed. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | FV-R22, FV-R26, FV-R27, FV-R29 | BND-STATE-001, BND-COMPOSE-001 | - | - |
| E2 | illustration | FV-R23, FV-R24 | BND-STATE-001, BND-RECOVERY-001 | - | - |
| E3 | illustration | FV-R12, FV-R15, FV-R19, FV-R22 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E4 | illustration | FV-R13, FV-R16 | BND-INPUT-001, BND-RECOVERY-001 | - | - |
| E5 | illustration | FV-R18, FV-R20 | BND-INPUT-001, BND-ENV-001 | - | - |
| E6 | illustration | FV-R24, FV-R25, FV-R33 | BND-AUTH-001, BND-TEMPORAL-001, BND-RECOVERY-001 | - | - |
| E7 | illustration | FV-R26, FV-R27, FV-R29, FV-R30 | BND-AUTH-001, BND-COMPOSE-001 | - | - |
| E8 | illustration | FV-R4, FV-R5, FV-R35 | BND-STATE-001, BND-COMPAT-001 | - | - |
| E9 | illustration | FV-R31, FV-R32, FV-R33 | BND-AUTH-001, BND-TEMPORAL-001 | - | - |

## Compatibility and migration

V3 activates through one coherent release after the implementing v2 change and every other nonterminal pre-v3 change completes or is explicitly closed. The activated runtime has one executable contract and no frozen v1/v2 continuation list.

No historical explain-change artifact, review, skill archive, or completed change is rewritten. Historical release archives retain the tooling that produced their records, but current tooling does not progress those records. Current authored and generated skill inventories remove explain-change. Before any v3 record exists, rollback may restore the prior coherent v2 package; after a v3 record exists, recovery is forward-compatible.

## Observability

Every final result exposes the exact target, verified subject, review and package identities, impact surfaces, evidence decisions and rationale, commands and results, CI status or gap, always-current checks, blockers, claim limits, normalized verification basis, and permitted next stage. Diagnostics identify unknown values, missing allocations, stale evidence, invalid tail changes, and mixed-package surfaces by stable IDs or paths.

No new telemetry service, database, network API, or background observer is required.

## Security and privacy

Final evidence and impact rationale must use repository-relative paths and bounded identities. They must not persist secrets, credentials, tokens, usernames, hostnames, machine-local absolute paths, private environment dumps, or unrelated sensitive input. Security-sensitive evidence is fresh-required unless a stronger governing policy explicitly defines another safe rule.

## Accessibility and UX

The contract is text-first and requires no visual-only interpretation. Final reports use clear tables or lists for repeated impact and evidence decisions, expand specialized terms at first use, and keep blocker ownership and next action readable without reconstructing internal state.

## Performance expectations

Verify should avoid rerunning impact-sensitive evidence that is affirmatively current, while never imposing a fixed runtime budget or weakening required proof. Impact analysis should start from the approved plan map and final diff rather than performing an unbounded rediscovery scan. Unknown impact may increase runtime and is an intentional safety cost.

## Edge cases

EC1. A Markdown file feeds packaging or generated documentation; documentation extension does not establish unaffected impact.

EC2. `.gitignore` changes artifact discovery; repository metadata classification expands to generated and lifecycle surfaces.

EC3. The final diff contains only Verify-owned report and lifecycle fields after subject `S`; product evidence may remain applicable, but always-current tail checks still run.

EC4. A reused evidence item passed locally while hosted CI is fresh-required; local evidence cannot satisfy the hosted obligation.

EC5. A plan verification group lacks a proved-surface description; Verify cannot justify reuse and routes the allocation gap to plan.

EC6. One evidence item proves several surfaces and one is affected; the evidence reruns unless the approved map supports a narrower independently valid result.

EC7. A correction changes only a test fixture that controls product proof; relevant evidence is affected even when production code is unchanged.

EC8. The successful report is written but lifecycle registration fails; no current branch-ready authority exists.

EC9. A historical release archive still contains explain-change; it remains immutable history and is not a current-package parity failure.

EC10. A current generated adapter contains explain-change after v3 activation; parity and release validation fail.

## Non-goals

- Defining a universal static dependency graph for every repository.
- Treating filenames, extensions, directories, or author declarations as semantic proof.
- Making historical evidence permanently current.
- Turning execution cache hits into final pass evidence.
- Allowing Verify to repair implementation, author plan allocation, settle review, route workflow, or open PRs.
- Removing Code Review, final verification, hosted CI requirements, security proof, release proof, or policy-required broad smoke.
- Migrating completed historical changes or rewriting historical release archives.
- Requiring external services, databases, telemetry, or complete machine-readable semantic graphs.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| FV-AC1 | A v3 lifecycle context routes from final Code Review and triggered stages directly to Verify, with no explain-change prerequisite. |
| FV-AC2 | Failed and inconclusive Verify attempts contain blocker ownership and no final explanation or branch-ready claim. |
| FV-AC3 | A successful Verify result contains the complete evidence basis and final explanation consumed by PR. |
| FV-AC4 | Every required evidence item has one valid freshness class and one `reuse`, `rerun`, or `newly-required` decision. |
| FV-AC5 | Unknown impact and unknown closed-vocabulary values fail safely and have direct regression coverage. |
| FV-AC6 | A narrow known-unaffected change reuses relevant product evidence while always-current and surface-specific checks run. |
| FV-AC7 | A fresh-required check reruns despite otherwise unaffected impact. |
| FV-AC8 | A plan allocation gap, implementation defect, stale review, and external CI gap each route to the correct owner without Verify repair. |
| FV-AC9 | The Verify evidence tail accepts only permitted report and lifecycle writes and invalidates product or governing drift. |
| FV-AC10 | PR consumes the exact current successful Verify report without creating a competing authoritative explanation. |
| FV-AC11 | Current authored and generated v3 packages omit standalone explain-change while historical archives remain unchanged. |
| FV-AC12 | Historical v1 and v2 records remain readable without current progression authority, while non-v3 progression, unknown, mismatched, and mixed states fail closed. |
| FV-AC13 | Scoped Verify does not load final-impact or explanation resources; final readiness loads the complete required procedure. |
| FV-AC14 | Repository lifecycle, review, skill, adapter, generated-output, and explicit-path validation pass for the coherently activated surfaces. |

## Open questions

None. Exact implementation modules, request schemas, report field serialization, milestone sequencing, concrete checks, and release cutover commands belong to Delivery planning within this approved behavior and architecture.

## Next artifacts

- Design Review of this specification with `docs/architecture/2026-08-31-impact-aware-final-verification.md` and `docs/adr/ADR-20260831-impact-aware-final-verification.md`.
- Execution plan after Design Review approval.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review reconciliation with the architecture and ADR. This specification does not authorize delivery planning until the exact design package is approved.
