# Retire the Specs Tree and Stale Validation Material

## Challenge

The first cleanup consolidated many old documents and retired token-cost, ledger and fixed-log checks, but the repository still divides current authority between living Designs and retained specifications. Some tests preserve old wording or instrumentation, while others use historical inputs to protect current rejection behavior. Contributors cannot safely distinguish those purposes from filenames alone.

At baseline `7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e`, `specs/` contains 116 tracked files, including 54 test specifications, two YAML resources and reference/template material. `tests/fixtures/` contains 235 tracked files across eight families; executable and embedded fixtures also exist elsewhere. Incremental removals have left substantial mixed authority and dependencies. The user now requests one repository-wide run that removes the entire specs tree and all stale tests and fixtures identified across the repository.

## Goals

- Remove `specs/` completely from the current repository, including its references, templates and machine-readable resources after useful responsibilities are reconciled.
- Make current owning Designs sufficient to understand the retained requirements, decisions and acceptance intent without retrieving retired specs.
- Assess the complete repository test and fixture population, remove stale cases and exclusive or orphaned fixtures, and refine useful tests that still depend on obsolete representations.
- Keep meaningful current behavior, negative and regression protection, package integrity and review evidence supported by current sources.
- Finish one coherent initiative with explicit whole-scope disposition, rather than repeatedly moving unresolved spec families into later cleanup proposals.

## Scope and non-goals

| Initial user intent or required dependency | Initial goal treatment | Scope budget treatment | Boundary |
| --- | --- | --- | --- |
| Remove all specifications and test specifications | in scope | core to this proposal | Every tracked member of `specs/`, including mixed sources, indexes, templates, reference material and YAML, must receive a complete disposition. An empty current specs tree is the completion target. |
| Refine current Design | in scope | core to this proposal | Skill, CLI and Engineering owners retain only important still-applicable requirements, decisions and acceptance obligations; obsolete obligations receive explicit retirement. No wholesale copying or renamed legacy-document collection. |
| Remove stale test cases | in scope | core to this proposal | Assess all repository test entrypoints, discovered cases and embedded/helper-generated cases, not only files named after removed specs. Remove retired-behavior, redundant historical and wording-only checks when their protective value is no longer current. |
| Remove stale fixtures | in scope | core to this proposal | Assess tracked fixtures, inline data, fixture builders and their consumers across the repository. Delete exclusive or orphaned obsolete data; refine retained cases to use appropriate current fixtures. Historical invalid inputs remain when needed to prove current rejection. |
| Reconcile executable and published consumers | in scope | same-slice dependency | Update current guidance, validation selection, generators, resource manifests, CLI repository assumptions, packaging, templates and affected examples whenever they depend on removed sources. |
| Resolve dependent legacy architecture and ADR clauses | in scope | same-slice dependency | Reconcile remaining current authority or references required to remove the specs tree. Remove obsolete coupled sources when their remaining responsibilities are resolved; do not impose an unrelated all-archive deletion target. |
| Preserve recoverable history and current evidence | in scope | same-slice dependency | Use Git for retired material, preserve uncommitted content before removal, and retain understandable evidence needed for current reliance without rewriting historical judgments. |
| Redesign unrelated product behavior or perform release operations | out of scope | out of scope | No new validation platform, measurement programme, archive service, permanent retirement ledger, release publication or customer-governance adoption. |

One owning change governs the complete target. Design and Delivery may organize coherent responsibility groups and reviewable milestones, but those groups do not silently narrow the final objective. A newly discovered required dependency remains in scope; a materially different product decision returns to its owner. Any proposed exclusion that prevents complete specs removal or leaves identified stale validation material must be an explicit scope-change decision, not a completion claim.

This is repository-specific consolidation. It does not ban customers from using specification documents or remove an independently supported public capability merely because its implementation mentions a generic `specs/` path. Retained public behavior must have a current owner and appropriate proof after the repository's own legacy sources disappear.

## Governing principle

Keep current knowledge and useful protection with their present owners; retain obsolete material through recoverable history.

## Proposed direction

Complete the transition from retained repository specifications to the existing Design hierarchy. Reconcile important knowledge by responsibility and preserve only what current behavior, safety, maintenance and acceptance require. Requirements not retained must have an explicit retirement disposition; preserving every historical detail is not the goal. Useful non-document resources receive maintained homes under their responsible owners rather than forcing the old directory to survive.

Treat specification retirement and test maintenance as one coherent change. For each responsibility group, distinguish tests that remain useful, tests needing refinement, and tests that should disappear. Establish retained protection before relying on a reduced suite, resolve actual consumers alongside removals, and keep current validation selection meaningful for changed and deleted inputs. A deleted test must never be replaced by a fabricated pass or an empty check under its old name.

Use a concise change-level disposition of source families, important retained obligations, retirement decisions and consumer reconciliation. It supports this initiative's review and recovery; it is not a new permanent inventory service. Current Designs remain focused on their contracts rather than accumulating old migration narratives.

Completion requires the specs tree to be absent, current owners and consumers to stand alone, the full candidate population to have a justified disposition, identified stale cases and fixtures to be removed, and required proof and independent whole-change assessment to support the result. Current operation must not fetch retired sources from Git. Detailed engineering choices belong to Design; sequencing, concrete checks and proof allocation belong to Delivery.

## Feasibility

Assessment: feasible enough to enter Design, with substantial coordination across existing owners. The merged cleanup and fixed-log retirement demonstrate recoverable source removal, explicit retirement of obsolete checks, preserved current negative proof and coordinated selector changes. The repository already has System composition and Skill, CLI and Engineering owners; a new top-level model or validation platform is not a prerequisite.

Bounded inspection confirms real remaining dependencies: boundary validation reads `specs/boundary-first-activation.yaml` and the proof-model spec; resource packaging reads `specs/boundary-first-resources.yaml` and `specs/references/`; CLI workflow context and published guidance still describe specification locations. The existing catalog and test entrypoints expose places to audit, including 21 Python test scripts and 22 CLI JavaScript test files, without treating those counts as a complete discovery inventory or evidence that any case is stale. Relevant starting points are [System](../design/system.md), [Validation](../design/engineering/validation.md), [Packaging](../design/engineering/packaging.md), [boundary resource consumption](../../scripts/boundary_first_reference.py) and [boundary validation](../../scripts/boundary_first_validation.py).

The material constraints are mixed current authority, generated/resource coupling, legitimate historical negative inputs and historical evidence whose identities must remain intact. Current Designs need selective refinement rather than an assumed blanket replacement. No known blocker prevents Design work. An unowned surviving obligation, unresolved public compatibility effect, unknown test protection or unrecoverable deleted content would block the affected removal and final completion until resolved. An inventory or a lower file/test count alone cannot establish success.

## Impact and major trade-offs

This retires the remaining repository-local legacy specification authority through reviewed Design adoption. Contributor instructions and real consumers must change coherently, and important behavior may need clearer current contracts before its old source can leave. The benefit is a self-contained Design hierarchy and a test suite with explainable current purpose; the cost is a broader coordinated change with cross-family review and regression risk.

Retaining useful old-version rejection fixtures is compatible with removing stale fixtures. Likewise, preserving required behavior does not require keeping its old document or every historical test assertion. The final result is judged by current contract fidelity and useful protection, not maximum deletion volume or measured token savings.

## Decision requested

Approve this complete repository-wide scope as the successor cleanup initiative: remove all of `specs/`, refine current owners with important surviving knowledge, and remove identified stale tests and fixtures after resolving their consumers and retained protection. Approve coherent milestones within this one scope and no silent deferral of difficult spec families. The [owning change](../changes/2026-09-14-retire-specs-and-stale-tests/change.json) records current state and review evidence.

This direction authorizes downstream Design and Delivery preparation after independent Proposal Review. It does not itself approve exact deletions, detailed contracts, implementation readiness, publication or merge.
