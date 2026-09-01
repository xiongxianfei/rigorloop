# Impact-Aware Final Verification Architecture

## Owning change record

- `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`

## Related artifacts

- Proposal: [Simplify Final Verification and Retire Explain Change](../proposals/2026-08-31-simplify-final-verification-retire-explain-change.md)
- Spec: None yet; specification reconciliation follows this architecture.
- Plan: None yet.
- ADRs: [ADR-20260831-impact-aware-final-verification](../adr/ADR-20260831-impact-aware-final-verification.md)

## Introduction and Goals

This architecture removes the standalone `explain-change` stage and moves its durable rationale into successful final verification. It also changes final evidence selection from revision-wide invalidation to conservative impact-aware applicability while preserving explicit freshness rules, independent review, implementation ownership, and exact PR handoff.

The design serves contributors maintaining the workflow contract, agents performing final verification, reviewers relying on the final evidence basis, and PR preparers consuming the verified rationale. It must reduce redundant execution without turning impact classification into an unsupported test-skipping mechanism.

## Architecture Constraints

- Verify remains the sole owner of `branch-ready`; PR remains the owner of PR body and PR opening readiness.
- Verify may inspect and record final evidence but may not repair implementation, rewrite governing artifacts, settle reviews, or choose workflow routing.
- The approved Delivery plan remains the starting verification allocation. Verify does not rediscover or silently replace the delivery proof strategy.
- Unknown or ambiguous impact broadens verification. No filename, extension, directory, or author assertion is sufficient by itself to prove narrow impact.
- Explicit fresh-required policy, required hosted CI, and security-, release-, or environment-sensitive obligations override ordinary evidence reuse.
- Every final run performs an always-current readiness set against current repository and lifecycle state.
- `skills/` remains the only authored skill source; installed and released adapter packages remain generated output.
- Historical `explain-change` artifacts, skills, reviews, and lifecycle records remain readable under their original contract and are not migrated.
- Closed lifecycle, impact, freshness, evidence-decision, and outcome vocabularies fail closed before consistency checks.
- This implementing change remains governed by `stage-owned-change-local-v2` and completes its registered `explain-change -> verify -> pr` path before activation.

## Context and Scope

The affected system is the repository-owned workflow and its published skill packages:

```text
Approved proposal, design, and Delivery plan
                    |
       final reviewed subject and review evidence
                    |
                    v
                  Verify
        +-----------+------------+
        | impact and policy      |
        | evidence applicability |
        | required executions    |
        | current-state checks   |
        +-----------+------------+
                    |
          success only: verified
       explanation + evidence basis
                    |
                    v
                   PR
```

Repository maintainers author the contract. The lifecycle CLI and validators enforce stage identity, artifact ownership, compatibility, and review settlement. Verify performs semantic impact and evidence-applicability judgment, runs required checks, and records the final result. PR consumes that result without recomputing its rationale.

C4 system and container diagrams are not applicable because this change modifies a repository protocol and packaged guidance rather than adding a service, process, network integration, or deployment unit. The flow above captures the material authority boundary.

## Solution Strategy

Adopt one final-verification protocol with six coordinated parts:

1. Retire `explain-change` from the active stage graph, public skill inventory, generated adapters, and current artifact prerequisites.
2. Introduce `stage-owned-change-local-v3` as the active graph discriminator after one coherent release cutover; v1, v2, and unversioned records remain bounded historical compatibility inputs.
3. Make Verify classify final-diff impact against a closed set of system and delivery surfaces, starting from the Delivery plan's verification allocation.
4. Decide each required evidence item's applicability as `reuse`, `rerun`, or `newly-required`, with explicit rationale and conservative expansion on unknown impact.
5. Record the readiness verdict, evidence basis, and final change explanation together in the Verify-owned report only after all required evidence and current-state checks pass.
6. Make PR consume the exact successful Verify result while keeping external PR preparation and opening outside Verify authority.

The final explanation is a section of the successful Verify result rather than an independently settled artifact. Failed or inconclusive attempts may record blockers and evidence gaps but omit the final-explanation section.

## Building Block View

### Delivery verification map

The approved plan supplies stable verification groups, governing SRs, affected architecture boundaries, expected evidence classes, and any fresh-required markers. Verify treats this map as the minimum planned evidence set and adds checks only when the final diff creates a new applicable surface or an always-current rule requires them.

### Impact classifier

The classifier maps the actual final diff and relevant repository state to closed surfaces such as runtime behavior, public API, state or persistence, migration, dependencies, build, packaging, generated output, security or authority, documentation, repository metadata, lifecycle governance, and external environment.

Each relevant surface resolves to `affected`, `unaffected`, or `unknown`. `unaffected` requires affirmative evidence; absence of an obvious match is not proof. `unknown` is a conservative result that expands verification.

### Evidence applicability evaluator

For each planned or newly applicable evidence item, the evaluator considers its proved surface, subject identity or cutoff, result, governing policy, environment sensitivity, and later changes. It emits exactly one decision:

| Decision | Meaning |
| --- | --- |
| `reuse` | Existing passing evidence remains applicable because later changes cannot materially affect its proved surface and no freshness policy overrides reuse. |
| `rerun` | Existing evidence is stale, affected, ambiguous, policy-fresh, environment-sensitive, or otherwise insufficient. |
| `newly-required` | The final diff introduces a surface or obligation not covered by the existing evidence map. |

The evaluator records reasoning; it does not treat a cache hit as a new pass. Existing unchanged-input validation caching remains an inner-loop execution optimization. Impact-based reuse is a final-readiness applicability decision over durable evidence and is independently governed.

### Always-current readiness set

Every final run directly checks the current governed change identity, final reviewed-subject and review identity, lifecycle and package consistency, closed review resolution, absence of blockers, current final diff classification, required artifact and evidence existence, generated-output currency when applicable, and the complete Verify result before PR handoff. Design fixes this responsibility set; Delivery may add but not remove policy-required checks.

### Verify result and explanation

The Verify-owned `docs/changes/<change-id>/verify-report.md` is the durable final result. A successful report contains:

- the verified subject and final review basis;
- the final impact classification;
- the planned evidence map and every `reuse`, `rerun`, or `newly-required` decision;
- commands actually run and observed CI status;
- always-current readiness results;
- the `branch-ready` verdict and normalized verification basis;
- the final change explanation, including purpose, requirement/design realization, important choices, evidence, limitations, and residual risk.

The report never embeds its own Git commit identity. The verified subject remains the reviewed product subject. The report and matching Verify-owned lifecycle recording form a closed evidence tail whose permitted paths and fields cannot contain product, spec, architecture, plan, dependency, generated-product, or unrelated documentation changes.

### Lifecycle and compatibility interpreter

After activation, v3 uses `code-review -> review-resolution when triggered -> ci-maintenance when triggered -> verify -> pr`. `explain-change` is not a v3 stage, active artifact kind, prerequisite, or public skill.

A new frozen activation manifest records the activating source revision and the complete set of pre-v3 v2 change IDs. V2 is accepted only for an exact manifest-listed change. Existing v1 and unversioned interpretation continues through the current v2 activation manifest. Unknown contract values, an unlisted v2 record, or v3 state containing active explain-change state fail before consistency interpretation.

### Published skill packages

The canonical `verify` package keeps universal outcome, authority, truthfulness, and stop rules inline. Conditional resources own final impact analysis, evidence applicability, and successful explanation generation. The standalone `explain-change` package is removed from authored current skills and generated current adapter inventories. Historical release archives remain immutable.

## Runtime View

### Successful final verification

1. Workflow resolves one v3 governed change after final holistic Code Review and any required resolution or CI maintenance.
2. Verify binds the exact reviewed subject, approved Design and Delivery authorities, plan verification map, final diff, and existing evidence.
3. Verify classifies every relevant impact surface. Any unknown surface expands the applicable verification set.
4. Verify evaluates every planned and newly applicable evidence item and records `reuse`, `rerun`, or `newly-required` with rationale.
5. Verify runs every rerun, newly required, fresh-required, and always-current check.
6. Only when all applicable results pass does Verify write one complete report containing the final explanation and `branch-ready` verdict.
7. The report and matching lifecycle recording form the closed Verify evidence tail. PR consumes that exact result.

### Failed or inconclusive verification

1. Verify records the exact failed, missing, stale, conflicting, or ambiguous evidence and its owning correction stage.
2. It does not emit a final change explanation or `branch-ready` verdict.
3. Workflow routes correction to specification, architecture, plan, implementation, Code Review, CI maintenance, or external evidence acquisition as applicable.
4. After correction and required rereview, Verify starts a new attempt. Unaffected evidence may be reused only after re-evaluation against the new final diff and policy.

### Narrow late change

1. Previously passing product evidence exists for the reviewed subject.
2. A later permitted stage-evidence or repository-metadata change appears in the final diff.
3. Verify determines whether it affects build inputs, packaging, generated output, runtime behavior, governed discovery, security, or another evidence surface.
4. Clearly unaffected product evidence may remain current; affected evidence reruns; ambiguity broadens verification.

### Verify recording identity

1. The reviewed product subject `S` and final-review evidence `R` exist before Verify.
2. Verify evaluates `S` plus the permitted stage-evidence tail and writes report content `V` without embedding its own commit hash.
3. Lifecycle registration binds the report content identity and exact permitted write set.
4. PR handoff checks that no change outside the closed Verify evidence tail occurred after the verified subject. Any product or governing drift invalidates the result and returns to the appropriate review or Verify boundary.

### Retry and interruption

An interrupted run with no complete registered report has no successful explanation or readiness authority. An identical registered success replay is idempotent. A changed subject, review, plan allocation, policy, evidence item, report content, or lifecycle revision requires re-evaluation; no partial result is silently adopted.

## Deployment View

Activation is one repository and release compatibility boundary covering governance, workflow specs, lifecycle schema and engine, validators, canonical skills and resources, templates, docs, fixtures, generated adapter packages, manifests, and release validation.

Before any v3 record exists, rollback restores the last coherent v2 package and leaves the unused v3 activation manifest as historical evidence. After a v3 record exists, recovery is forward through a compatible corrective release. Returning v2 to the default would require a separately approved migration design because v3 records have no explain-change obligation.

This change itself completes under v2. The release cutover may occur only after it and every other nonterminal pre-v3 change has completed or is explicitly excluded by validated policy.

## Crosscutting Concepts

### Traceability

Verify traces evidence backward through concrete implementation and allocated plan work to stable SRs, architecture realization, and the accepted proposal. The final explanation renders that same verified chain for humans; it does not create new requirements or authority.

### Evidence currency

Evidence currency combines identity, applicability, and policy. Revision change alone is insufficient to invalidate all evidence, while an unchanged filename or command is insufficient to preserve it. Reuse requires a passing result, known proved surface, affirmative non-impact reasoning, current governing authority, and no freshness override.

### Freshness policy

Freshness has three architectural classes: `always-current`, `fresh-required`, and `impact-sensitive`. Unknown values fail closed. `always-current` belongs to final repository and lifecycle state; `fresh-required` comes from approved policy or Delivery allocation; `impact-sensitive` may be reused only through the applicability evaluator.

### Authority

Plan owns initial verification allocation. Verify owns applicability judgment, required executions, final evidence aggregation, explanation, and `branch-ready`. Workflow owns routing. Owning authoring or implementation stages make corrections. Code Review owns review judgment. PR owns PR preparation and opening.

### Security and privacy

Impact and evidence records use repository-relative paths, stable IDs, command identities, and bounded rationale. They must not persist secrets, credentials, private environment dumps, usernames, hostnames, or machine-local absolute paths. Security-sensitive proof remains fresh-required unless a stronger governing policy says otherwise.

### Progressive disclosure

Scoped verification does not load final-impact or explanation procedure. Final readiness loads one coherent applicability resource; successful final readiness additionally applies the explanation section. Resource loading never grants lifecycle or correction authority.

### Validation

Deterministic validation checks structure, closed values, required mappings, lifecycle compatibility, report shape, package parity, and forbidden active explain-change surfaces. Semantic review and Verify own whether impact classification and reuse rationale are adequate.

## Architecture Decisions

- [ADR-20260831-impact-aware-final-verification](../adr/ADR-20260831-impact-aware-final-verification.md) — retires the standalone explanation stage, adopts v3 final verification, distinguishes semantic evidence reuse from execution caching, and records rationale only in successful Verify output.

This ADR supersedes the active `S -> R -> E -> verify` direction in [ADR-20260818-ordered-final-review-stage-evidence-tail](../adr/ADR-20260818-ordered-final-review-stage-evidence-tail.md) for v3 changes. It also supersedes the final-gate universal actual-run consequence in [ADR-20260523-validation-idempotency-cache-hit-safety](../adr/ADR-20260523-validation-idempotency-cache-hit-safety.md) only where approved impact-sensitive evidence remains current; unchanged-input cache hits remain inner-loop-only and cannot independently establish final readiness.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Safety | Verify cannot establish whether a late change affects existing evidence. | Impact resolves `unknown`, verification expands, and no reuse-only readiness verdict is permitted. |
| Efficiency | A late change is affirmatively isolated from product behavior and product evidence surfaces. | Product evidence remains current while surface-specific and always-current checks run. |
| Traceability | A reviewer reads a successful Verify report. | The report connects proposal, SRs, architecture, plan allocation, reviewed implementation, evidence decisions, verdict, and explanation. |
| Failure integrity | Verification finds a defect or stale review. | The attempt records the blocker, emits no final explanation, and grants no `branch-ready`. |
| Identity safety | Verify records its own report after evaluating the reviewed subject. | The report binds `S` and `R`, omits its own commit hash, and the closed evidence tail contains no product or governing drift. |
| Policy compliance | A plan marks a check fresh-required. | Verify reruns it even when impact analysis would otherwise allow reuse. |
| Historical compatibility | A completed v2 change contains explain-change evidence. | The exact manifest-listed record remains readable without mutation or v3 reinterpretation. |
| Package coherence | A supported adapter is generated or released. | Current packages contain Verify with mapped resources, omit standalone explain-change, and mixed packages fail validation. |

## Risks and Technical Debt

- Incorrect non-impact classification could reuse unsound evidence. The affirmative proof requirement, `unknown` fallback, reviewable rationale, and fresh-policy override mitigate but do not eliminate semantic judgment risk.
- Verify becomes a larger responsibility boundary. Progressive disclosure and one normalized report prevent the common path from absorbing every specialized procedure.
- The v3 activation manifest and v1/v2 compatibility readers add bounded legacy complexity. They are preferable to silently applying a new graph to old evidence.
- Report recording after substantive proof creates an identity boundary. The closed Verify evidence tail and content registration avoid self-referential commit fields, but Delivery must allocate direct recovery and drift tests.
- Current guidance distributes final-stage rules across governance, specs, skills, schemas, validators, fixtures, and generated packages. Activation must inventory all current surfaces and reject mixed versions.
- Impact-based reuse is semantic and may initially be conservative enough to yield modest savings. Precision may improve only through later evidence, not by weakening the unknown fallback.

## Glossary

- **Verified subject:** The exact final reviewed product and governing-change subject whose behavior and evidence Verify evaluates.
- **Impact surface:** A system or delivery area whose change can affect the applicability of evidence.
- **Evidence applicability:** The judgment that prior evidence still proves its intended surface for the verified subject.
- **Evidence reuse:** Final-readiness reliance on an existing pass after affirmative applicability evaluation; not an execution cache hit.
- **Always-current check:** A check whose meaning depends on the current repository, lifecycle, review, or report state and therefore runs in every final attempt.
- **Fresh-required check:** Evidence that governing policy or approved Delivery allocation requires to be newly executed for the final attempt.
- **Impact-sensitive check:** Evidence that may remain current when later changes cannot affect its proved surface.
- **Verify evidence tail:** The closed report and lifecycle-recording writes after the reviewed subject; it may contain no product or governing drift.
- **V3 contract:** `stage-owned-change-local-v3`, the lifecycle graph without standalone test-spec or explain-change stages.

## Next artifacts

- Specification reconciliation.
- Design Review of this architecture, the ADR, and the specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

The architecture and ADR are ready for specification reconciliation. They do not authorize implementation and remain unapproved until Design Review accepts the exact package.
