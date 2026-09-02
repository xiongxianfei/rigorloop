# Simplify Final Verification and Retire Explain Change

## Challenge

RigorLoop currently separates final change explanation from final verification:

```text
Code Review
-> Explain Change
-> Verify
-> PR
```

This order makes `explain-change` describe a reviewed change before `verify` establishes that the change is ready. In the common successful case, the separate stage adds a handoff and artifact lifecycle without contributing a distinct approval decision. When verification instead finds a defect or stale evidence, the correction and required rereview can invalidate the explanation, forcing the final path to repeat both `explain-change` and `verify`.

Final verification can also treat a new revision as invalidating broad prior evidence even when the later change cannot materially affect the surface that evidence proves. That behavior confuses revision identity with evidence applicability and can rerun unrelated product checks after a narrow metadata, documentation, or repository-policy change.

The current contract therefore creates avoidable ceremony and validation cost while producing the durable explanation before its final evidence basis is known.

## Goals

- Remove `explain-change` as a governed lifecycle stage and standalone published skill without losing durable change rationale.
- Make successful final verification generate the durable explanation of the exact verified change and evidence basis.
- Prevent failed verification attempts from producing explanations that immediately become stale.
- Make final verification distinguish current, applicable evidence from evidence invalidated by the final diff.
- Allow impact-based reuse of passing evidence while failing safely when applicability is uncertain.
- Rerun stale or newly required checks and preserve explicit fresh-evidence requirements from an approved plan or governing policy.
- Keep Verify independent from implementation repair and route findings to the owning stage.
- Preserve traceability from approved requirements and design through implementation, review, final evidence, explanation, and PR handoff.
- Reduce final-stage ceremony, validation execution, and agent context without weakening readiness guarantees.

## Scope and non-goals

This proposal covers the governed final-stage sequence, retirement of the authored and published `explain-change` skill package, Verify responsibilities, evidence currency and applicability policy, final explanation ownership, workflow routing, historical compatibility, and the evidence-and-explanation handoff consumed by PR preparation.

The initial intent is preserved as follows:

| Requested outcome or constraint | Treatment | Destination |
| --- | --- | --- |
| Retire the governed `explain-change` stage and standalone skill | in scope | Goals; Proposed direction |
| Produce the durable explanation only after successful final verification | in scope | Goals; Proposed direction |
| Select and reuse evidence according to actual final-change impact | in scope | Goals; Proposed direction |
| Broaden verification when impact is unknown or ambiguous | in scope | Proposed direction |
| Preserve plan- or policy-required fresh evidence | in scope | Proposed direction |
| Keep Verify read-only with respect to implementation repair | in scope | Proposed direction |
| Preserve requirement-to-evidence traceability and historical records | in scope | Goals; Proposed direction |
| Make PR consume the verified explanation and evidence basis | in scope | Proposed direction |
| Specify an exact impact-analysis algorithm, cache representation, dependency graph, or final artifact schema | deferred follow-up | Design after direction approval |

The scope budget is:

| Work family | Scope budget treatment | Boundary |
| --- | --- | --- |
| Final lifecycle order and routing | core to this proposal | Replace `Code Review -> Explain Change -> Verify -> PR` with `Code Review -> Verify -> PR`, retaining conditional stages before final verification where governed elsewhere. |
| Impact-aware evidence applicability and reuse | core to this proposal | Establish the policy and conservative fallback, not the detailed classifier or storage model. |
| Post-success explanation generation in Verify | same-slice dependency | Preserve the useful rationale output as part of the exact final evidence basis. |
| Standalone skill and published-resource retirement | same-slice dependency | Remove normal current entrypoints and generated publication surfaces coherently; do not erase history. |
| PR consumption of verified rationale | same-slice dependency | Change the handoff contract without moving PR preparation or opening into Verify. |
| Governing specs, guidance, validation, and generated-output alignment | separate implementation slice | Design and Delivery must allocate the coordinated compatibility update; this proposal does not prescribe its sequence. |
| More precise dependency modeling or evidence caching | deferable follow-up | Introduce only if conservative first-slice evidence shows it is needed. |

This proposal does not remove Code Review or final verification; permit arbitrary skipping of required checks; declare any filename, extension, or file class universally safe; make historical evidence permanently valid; weaken system requirements to reduce test execution; infer semantic correctness from filenames alone; require a complete machine-readable verification dependency graph; allow Verify to repair implementation; or settle the exact impact taxonomy, confidence model, evidence-currency schema, cache representation, or final Verify artifact format.

## Governing principle

> Final explanation should describe the verified change, and verification evidence should be rerun only when the final change can invalidate it or policy explicitly requires fresh proof.

## Proposed direction

Replace the separate explanation stage with one final verification gate:

```text
Code Review
-> Verify
   -> determine final change impact
   -> determine applicable verification
   -> reuse still-current evidence
   -> run stale or newly required checks
   -> decide readiness
   -> on success, generate the final change explanation
-> PR
```

`explain-change` will no longer be a governed lifecycle stage, mandatory prerequisite, standalone skill, or normal published skill package. Its useful responsibility moves into Verify. Historical explain-change artifacts and evidence remain readable historical records and require no migration.

Verify will decide readiness before producing the final durable explanation. A failed or inconclusive verification records its blockers and routes each correction to the owning stage; it produces no final explanation. After correction and any required rereview, Verify runs again, reusing only unaffected evidence, and generates the explanation only after the exact final change passes.

The successful explanation will cover what changed, why it changed, how it realizes approved requirements and design, important implementation choices, the evidence supporting readiness, and remaining limitations or residual risks. PR preparation will consume this verified explanation and its evidence basis rather than rationale authored before final verification. Verify continues to own `branch-ready`; PR continues to own PR content and opening readiness.

Final verification will use the approved Delivery package's requirement and verification allocation as its initial evidence map. It will ask which required evidence exists, which evidence remains applicable, which evidence is stale, and which new evidence the final diff requires. This preserves the reverse traceability path from evidence through implementation and allocated work to system requirements and approved direction without creating a new lifecycle artifact merely for evidence mapping.

Evidence applicability will depend on actual impact, not revision identity alone. Verify will classify the relevant system and delivery surfaces changed by the final diff, such as runtime behavior, public API, persistence, migration, dependencies, build and packaging, generated outputs, security or authority boundaries, documentation, and repository metadata. Design will define the exact classification model.

Previously passing evidence may remain current when Verify can establish that subsequent changes cannot materially affect the surface that evidence demonstrates. Evidence becomes stale and must be rerun when the final change can affect that surface. Newly applicable checks must also run. A narrow repository-metadata change may therefore retain product-test evidence only after Verify establishes that build inputs, packaging, generated outputs, runtime behavior, governed artifact discovery, and other relevant surfaces are unaffected; the filename alone is never sufficient proof.

Impact uncertainty expands verification rather than narrowing it:

> Known narrow impact may narrow verification; unknown impact must not.

Impact-based reuse cannot override explicit freshness obligations. Checks marked fresh-required by an approved Delivery plan or governing policy, release-sensitive validation, security- or environment-sensitive evidence, required hosted CI, and mandated broad smoke still run when applicable. Verify also retains a small always-current readiness set for current repository identity, lifecycle consistency, review closeout, required artifact and evidence existence, unresolved blockers, and other state whose meaning depends on the final repository state. Design will settle the exact mandatory set.

Verify remains read-only with respect to implementation and upstream governed artifacts. It may identify an implementation defect, missing design behavior, verification-allocation gap, stale review, or CI/environment issue, but it routes the problem to its owner instead of modifying implementation and continuing. Corrections follow the applicable owner, review, and Verify loop.

## Feasibility

**Assessment: Feasible.** The current authored skills already overlap on the actual diff, approved decisions, requirements, review evidence, validation, and traceability. Verify already owns final evidence applicability, aggregation, and the `branch-ready` verdict, while `explain-change` owns rationale without an independent approval claim. Moving rationale generation after the verdict can therefore remove a stage without removing a distinct approval authority.

The larger uncertainty is safe impact-based evidence reuse. The approved Delivery package, final diff, requirement identities, plan verification allocation, review records, and existing validation evidence provide a credible starting basis. A conservative first design can reuse only evidence that is clearly unaffected, rerun evidence that is clearly affected, and broaden verification whenever applicability cannot be established. No complete dependency graph or advanced cache is required to enter Design.

Responsible Design work must reconcile the Constitution, approved workflow and autoprogression specs, current Verify and PR contracts, authored and published skill surfaces, generated-package validation, and contributor guidance as one compatibility-sensitive change. No conceptual blocker requires the separate stage to remain, but approval of this proposal does not itself amend those current authorities.

## Impact and major trade-offs

The final path becomes `Code Review -> Verify -> PR`, removing one skill invocation, handoff, and invalidation relationship. Verify becomes more consequential because it owns final impact analysis, evidence applicability and refresh, readiness judgment, and post-success explanation generation. Its public package should use progressive disclosure so specialized impact guidance and explanation-generation procedure do not burden every scoped verification request.

Impact-based reuse can materially lower validation cost after narrow late changes. The corresponding risk is unsound reuse caused by incorrect impact classification. Conservative expansion on uncertainty and non-overridable freshness policy are approval-critical safeguards, even when they reduce the optimization benefit.

The explanation becomes more trustworthy because it describes the exact change and evidence basis that passed final verification. The deliberate trade-off is that no final readiness explanation exists before verification succeeds; failed attempts retain blocker evidence rather than a misleading final narrative.

This direction supersedes the final-stage ownership decision in `docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md`, which deliberately kept `explain-change` separate and made its current artifact a Verify prerequisite. It also requires downstream amendment of current constitutional and specification rules that mandate both stages. Historical accepted proposals, skills, and explain-change records remain valid evidence of the contract under which they were produced.

## Decision requested

Approve the direction to:

1. Remove `explain-change` from the governed RigorLoop lifecycle and retire its standalone authored and published skill package.
2. Make Verify generate the final durable change explanation only after final verification succeeds, with no final explanation from failed or inconclusive attempts.
3. Remove a current explain-change artifact as a prerequisite for Verify.
4. Require Verify to classify the impact of the actual final diff before selecting final verification work.
5. Allow reuse of previously passing evidence only when Verify can establish that the final change does not affect the surface the evidence proves.
6. Rerun stale or newly applicable evidence and broaden verification when impact is unknown or ambiguous.
7. Preserve explicit fresh-evidence requirements and an always-current final-readiness set despite otherwise reusable evidence.
8. Keep Verify read-only with respect to implementation and route findings to their owning stage and required review loop.
9. Make PR preparation consume the explanation and evidence basis produced by successful Verify while preserving existing Verify and PR claim boundaries.
10. Preserve historical Explain Change artifacts and evidence without migration.

Approval authorizes Design to revise final verification around impact-aware evidence reuse and post-verification explanation generation, including coordinated amendment of the current final-stage contract. It does not approve the exact impact-classification algorithm, evidence-currency or cache schema, verification dependency representation, mandatory-check set, explanation format, implementation sequence, or validation plan.
