# Boundary-first compact core

Boundary model version: boundary-first-v1

Use this method to inspect outcome-changing conditions and actual interactions in the project's current governing Designs. The version identifies this packaged method, not an accepted feature/proof document format. Preserve current requirement and scenario identities; do not create BND, INT or PRF records or a separate test-spec stage.

## Compact scan

Before a qualifying stage-owned decision, ask:

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

The scan identifies material conditions, not a requirement for another artifact, record or exhaustive scenario inventory. For each relevant condition, name the governing obligation and observable outcome; unresolved behavior belongs with its owner.

## Core dimensions

Consider all eight dimensions, using the owning model's selected scenario convention and explaining material non-applicability. Do not manufacture cases for irrelevant dimensions.

| Dimension | Question |
| --- | --- |
| Input domain | Which valid, missing, malformed, boundary and unknown values change the result? |
| State/lifecycle | Which current, stale, intermediate or terminal states change the permitted outcome? |
| Identity/authority | Which actor, scope, identity, approval or freshness facts permit or prohibit action? |
| Composition/path | Which public, helper, sibling, alternate or bypass paths must agree? |
| Temporal/retry | Which order, duplicate, retry or concurrent event changes the outcome? |
| Failure/recovery | What survives interruption, partial work, failed restoration or a missing dependency? |
| Compatibility/migration | Which supported prior/current combinations, retired inputs or authorized adoption paths differ? |
| External/environment | Which filesystem, resource, network, platform or external response changes the result? |

## Interactions and examples

Select an interaction when one condition changes another condition's success, rejection, authority, recovery or stop outcome. For example, a retry through a helper must recheck authority if it can become stale between attempts. Use actual hazards, incidents and requirement-grounded counterexamples; do not enumerate every dimension combination. If no additional interaction matters, explain that conclusion in the owning Design rather than inventing an interaction record.

Examples illustrate the governing behavior rather than define its complete boundary. An observed regression retains its meaningful failure observation; a newly discovered unowned outcome returns to its behavior owner. Use independent expected observations, preserved state and prohibited side effects to distinguish the intended defect from unrelated setup failure.

## Consumption and upstream gaps

Read the exact current approved requirement/scenario rows and relevant interaction rationale. Preserve their identities and do not infer new behavior from historical approval, a filename or a passing check. Expand the selected context when it is missing, stale, ambiguous, contradictory or insufficient for the observed condition.

A new or changed required outcome returns to Design. Missing execution allocation for settled behavior returns to Plan. A defective implementation or test returns to its implementation owner under the selected review policy. Historical source interpretation preserves authority and original meaning but does not restore retired feature/proof operations or authorize customer conversion.

## Structural validation and semantic review

Structural validation checks the selected current document/resource contract and reference integrity. It cannot decide applicability, sufficient interactions, meaningful proof, independent approval or completion. Semantic review judges the actual outcomes, allocation, implementation and evidence at the reviewer's owned boundary. Missing required guidance stops the dependent action; never reconstruct a retired method to continue.
