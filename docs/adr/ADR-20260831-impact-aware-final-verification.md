# ADR-20260831-impact-aware-final-verification: Consolidate Explanation into Impact-Aware Verify

## Owning change record

`docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/change.yaml`

## Context

RigorLoop currently requires `Code Review -> Explain Change -> Verify -> PR`. The explanation has no independent approval authority, is produced before final readiness is known, and becomes stale when Verify routes a correction. Final Verify also requires broad fresh execution in circumstances where a later revision cannot affect the surface demonstrated by existing passing evidence.

The replacement must preserve durable rationale, final evidence truthfulness, explicit freshness policy, review and correction ownership, historical compatibility, and PR claim boundaries. It must also resolve the recording identity problem created when Verify produces durable evidence after assessing a reviewed subject.

## Decision

For newly governed changes under `stage-owned-change-local-v3`, use `Code Review -> Verify -> PR` after any triggered review resolution and CI maintenance. Remove `explain-change` from the active stage graph, current lifecycle vocabulary, required artifact set, authored public skill inventory, and generated current adapter packages. Historical v1 and v2 records remain readable under their registered contracts and are never migrated merely to remove the stage.

Verify starts from the approved Delivery plan's verification allocation, classifies the actual final diff across closed impact surfaces, and evaluates each required evidence item as `reuse`, `rerun`, or `newly-required`. Reuse requires affirmative proof that later changes cannot materially affect the evidence's proved surface. `unknown` or ambiguous impact expands verification. Explicit fresh-required, always-current, hosted-CI, security-sensitive, release-sensitive, and environment-sensitive obligations override ordinary reuse.

On failure or inconclusive evidence, Verify records blockers and routes them to the owner but produces no final change explanation and no `branch-ready` verdict. On success, one Verify-owned report records the exact reviewed subject, final review basis, impact classification, evidence decisions, commands and observed results, always-current checks, normalized verification basis, residual risk, and final change explanation. PR consumes this exact successful result.

The Verify report does not embed its own Git commit identity. The reviewed product subject remains fixed, while the report and matching Verify-owned lifecycle recording form a closed post-review evidence tail. Any product, requirement, architecture, plan, dependency, generated-product, or unrelated documentation change in that tail invalidates the result and routes to the applicable owner or review boundary.

Impact-based evidence reuse is distinct from validation execution caching. Cache hits remain inner-loop optimizations and cannot independently establish final readiness. This decision supersedes ADR-20260818's `S -> R -> E -> verify` tail for v3 with `S -> R -> V`, where `V` is the successful Verify result and explanation. It also supersedes ADR-20260523's universal final-gate actual-run consequence only for impact-sensitive evidence affirmatively shown current; its cache safety, local-state, privacy, and cache-only closeout prohibitions remain.

Activation is atomic. A new frozen manifest binds every pre-v3 v2 change ID to its old contract. Existing v1 and unversioned interpretation remains governed by the current activation manifest. New-change scaffolding emits v3 only after coherent activation, and unknown or unlisted prior values fail closed. The implementing v2 change completes its registered old path before cutover.

## Alternatives considered

- Keep `explain-change` and make it shorter: rejected because the premature artifact and invalidation cycle remain.
- Generate explanation before the readiness decision inside Verify: rejected because a failed attempt would still create stale final rationale.
- Generate a separate post-Verify explanation stage: rejected because it recreates the retired lifecycle boundary and can diverge from the verdict basis.
- Treat every new revision as invalidating all evidence: rejected because revision identity is not evidence applicability and imposes avoidable cost.
- Trust filenames or author-declared narrowness: rejected because semantic impact may cross build, packaging, generated, security, or governed-discovery boundaries.
- Use execution cache hits as final evidence reuse: rejected because cache identity and semantic evidence applicability are different claims.
- Reinterpret all historical records under v3: rejected because it would invalidate settled evidence and introduce missing obligations retroactively.

## Consequences

The common final path loses one skill, handoff, artifact prerequisite, and stale-rationale loop. The successful explanation becomes stronger because it shares the exact evidence basis and readiness decision consumed by PR.

Verify gains semantic responsibility for impact, applicability, execution selection, evidence aggregation, and rationale. Its package needs progressive disclosure, closed vocabularies, conservative fallback, and durable explanation guidance. Plans and Delivery Review must provide enough verification allocation for Verify to start from an approved map.

The lifecycle engine, validators, governance, specs, templates, docs, fixtures, package manifests, generated adapters, release validation, and current architecture must activate v3 coherently. Historical compatibility readers and a v3 activation manifest add bounded complexity. Before v3 creation rollback may restore v2; afterward recovery is forward-compatible.

Evidence execution should fall after narrow late changes, but classification errors are safety-sensitive. Unknown impact therefore sacrifices optimization before it sacrifices proof. Explicit freshness policy always wins.

## Follow-up

- Reconcile the feature specification with the v3 lifecycle, evidence-applicability, report, identity, failure, and compatibility boundaries.
- Design Review must approve the exact architecture, ADR, and specification package.
- Delivery planning must allocate atomic activation, removal inventory, validation, generated-package parity, historical fixtures, impact-classification proof, evidence-tail proof, and rollback.
