# Workflow Skill Simplification Explain Change

## Summary

This change makes the published `workflow` skill materially smaller for generic routing while preserving its lifecycle authority, fail-safe classification, automation, guide-authoring, review, milestone, claim, and handoff contracts.

The universal `SKILL.md` falls from 4,333 to 2,710 words. `WP0-generic-routing` is 37.5% smaller by words and 36.9% smaller by bytes; every other valid assembly is also smaller. Total package content grows 1.2% by words and 3.1% by bytes because three conditional procedures and their exact safety boundaries are now explicit. The change reports that maintenance cost instead of presenting relocation as deletion.

## Problem

The prior 496-line workflow skill loaded ordinary routing, governed lifecycle procedure, armed automation, review-gate procedure, and project workflow-guide authoring for every invocation. It also repeated lifecycle, isolation, placement, readiness, and stop rules across several sections. That made common routing harder to scan and gave repeated behavior more than one textual owner.

The goal was to separate procedure by the authority that activates it, not to weaken workflow rigor.

## Decision trail

- The proposal selected O3: a compact universal dispatcher, three conditionally loaded procedure references, the existing boundary reference, and the existing structural guide skeleton.
- R1-R20 define package ownership, the four evidence predicates, seven valid assemblies, transient bootstrap, stateless commands, one-way reference dependencies, and fail-safe resource loading.
- R21-R27 require separate semantic/literal ledgers and honest assembly versus total-package measurement.
- R28-R30 require deterministic acceptance without a target-agent runtime and preserve lifecycle behavior.
- R31 required a recorded architecture assessment. It returned `architecture-required` because responsibility moved from one file to one package; the owning architecture document was updated and approved without a new ADR.
- R32 requires atomic canonical, generated, archived, installed, and rollback package behavior.
- M1 froze the semantic, literal, scenario, and size baseline; M2 refactored the canonical package and validators; M3 measured final assemblies and proved package parity.

## Diff rationale by area

| Area | Change | Reason | Source and proof |
| --- | --- | --- | --- |
| `skills/workflow/SKILL.md` | Consolidated universal routing, evidence precedence, unknown-state behavior, classification, portability, isolation, stops, claims, resource checks, handoff, and boundary method. | `WP0` must classify and stop safely without conditional resources. | R1-R6, R15-R18, R30; T1-T2, T6-T9; final holistic review. |
| Governed lifecycle reference | Added governed identity interpretation, bounded mutation, architecture applicability, settlement, transitions, milestones, review return, final review, and closeout. | Decisions that depend on current `change.yaml` need one authoritative procedure even when read-only. | R10-R11; T3, T12, T14; M2 reviews. |
| Automation reference | Added command, identity, bootstrap, stateless status/off, packets, receipts, budgets, review/correction, pause, and promotion procedure. | Automation procedure applies only to explicit commands or durable authorization and must consume rather than redefine lifecycle transitions. | R6-R9, R12, R19-R20; T3-T7, T12-T14. |
| Guide-authoring reference and skeleton | Moved creation/refresh, customization, migration, and skeleton-use procedure behind guide-authoring evidence while retaining the skeleton as layout only. | Ordinary routing should not load guide-writing procedure, and the asset must not become a policy owner. | R13-R14; T5, T7, T10. |
| Architecture document and assessment | Recorded one skill-owned package, universal-before-conditional loading, one-way dependencies, bootstrap/stateless behavior, fail-safe resources, and atomic package parity. | The responsibility location changed even though runtime, persistence, and deployment architecture did not. | R31; architecture reviews R1-R2. |
| Skill-validator tests | Added six focused workflow-package contract tests and redirected older assertions to the resource that now owns each procedure. | Existing deterministic owners should prove triggers, assemblies, bootstrap, ownership, universal stops, and structural skeleton boundaries without a model runtime. | R25, R28-R30; T1-T10; 297-test pass. |
| Rule/literal ledgers and fixtures | Recorded 26 semantic rules, 15 literal dependencies, 16 scenarios, closed classifications, destinations, and invalid-value fixtures. | No behavior may disappear, and accidental wording consumers must not become policy owners. | R21-R24; CMD1, MP1-MP2. |
| Measurements and package proof | Recorded resource hashes, words, bytes, all assemblies, boundary additions, total package size, failed-first compatibility evidence, adapter archives, and temporary installs. | Common-path improvement and package maintenance cost require separate, reproducible evidence. | R26-R29, R32; T10-T15; M3 review. |
| Selector routing debt | Recorded complete owner-approved deferrals for the two one-change ledgers and three static fixtures. | Keeps non-recurring evidence visible and blocked from generic routing without creating permanent simplicity infrastructure. | Existing owner-deferral contract; CMD1, MP1, MP2, and focused consumer proof remain mandatory. |
| Change-local review and lifecycle evidence | Recorded proposal, spec, architecture, plan, test-spec, milestone, correction, and final holistic reviews plus dispositions and state transitions. | Formal gates and all 12 material findings require durable evidence before verification. | Workflow contract; review-resolution closeout. |

## Tests added or changed

- T1-T7 prove predicates, the seven assemblies, bootstrap order, stateless commands, ownership, contradiction handling, and required-resource stops.
- T8-T9 prove duplicate removal and separate literal classification without freezing incidental headings.
- T10-T11 prove exact mapped-resource presence, containment, generated parity, and structural assets.
- T12-T14 prove lifecycle preservation, failure/recovery behavior, semantic ownership, measurement, and rollback.
- T15 proves acceptance excludes target-agent runtimes, prompts, transcripts, credentials, network, and nondeterministic retry evidence.
- Six permanent focused tests in `scripts/test-skill-validator.py` enforce durable package properties. Change-local ledgers, scenarios, measurements, and semantic judgment remain evidence rather than a new permanent simplicity validator.

## Validation evidence available before final verify

- CMD1: 26 rules, 15 literals, 16 scenarios; unknown values rejected.
- Canonical workflow skill validation passed.
- `scripts/test-skill-validator.py`: 297 tests passed, 16 skipped.
- `scripts/test-build-skills.py`: seven tests passed.
- Generated-skill drift checking passed in temporary output.
- `scripts/test-adapter-distribution.py`: 150 tests passed.
- Trusted `v0.3.6` CMD7 built and clean-installed the selected workflow skill for Codex, Claude, and OpenCode.
- Boundary-first, change-metadata, review-structure, and diff-whitespace checks passed.
- No target agent, network call, publication, or generated package hand-edit was used.

The first M3 adapter run failed because the shortened file omitted the exact cross-adapter invocation-equivalence block and duplicated Codex command spans outside its analyzer-owned location. The repair restored one compact universal block, removed duplicates, added the missed semantic rule, updated measurements, passed focused portability/archive tests, then passed the complete 150-test suite and fresh all-target install proof.

The first final PR-mode validation run then exposed one additional governed-contract dependency: the common path still needed to name `partially-accepted` as part of the closed review-resolution disposition vocabulary. The correction restored the full five-value vocabulary, registered the dependency separately from semantic-rule ownership, refreshed measurements, and passed the 103-test review-artifact suite before the complete PR gate was rerun.

That rerun reached the guide-system gate and exposed another portable-default dependency: the common path listed both canonical plan paths but no longer rejected `docs/changes/<change-id>/plan.md`. The correction restored the compact index/body/non-canonical distinction and registered its existing guide-validator consumer without changing validation logic.

The first final verify selection also failed closed on five unregistered one-change evidence paths. Repository-maintainer deferrals now name each exact ledger or fixture, why it should not become a recurring selector class, which direct proof remains mandatory, and its follow-up evidence. No selector or validator code changed, and the deferrals cannot match other paths.

## Review resolution summary

All 12 material findings are accepted and resolved; there are no `needs-decision` or open review-log findings. They cover proposal trigger/ownership/failure contracts, stateless automation, architecture wording, proof-map commands, and M2 universal/bootstrap/ledger corrections. See `review-resolution.md` for the durable dispositions without repeating review transcripts.

## Alternatives rejected

- Keeping the prior skill leaves the 4,333-word common path and repeated ownership unchanged.
- Editorial compression alone cannot stop generic invocations from loading governed, automation, and guide procedure.
- Automation-only extraction leaves governed and guide-authoring procedure mixed into ordinary routing.
- A routing engine introduces a new runtime, error model, compatibility boundary, and owner without evidence that prose orchestration is insufficient.
- A permanent size gate or target-runtime prompt journey would make an unstable metric or model behavior the acceptance owner.

## Scope control

The change does not alter stage order, stage obligations, `change.yaml` schema, automation persistence, review outcomes, milestone semantics, downstream authority, specialized stage skills, or `docs/workflows.md`. It introduces no runtime, scheduler, selector service, state store, dependency, deployment, permanent simplicity validator, or target-agent acceptance system. Canonical authorship remains under `skills/`; adapter packages remain derived.

## Risks and follow-ups

The package has more files, so exact resource triggers and archive/install parity remain important drift controls. The universal cross-adapter invocation block is parser-sensitive and must remain one exact owner. Semantic meaning still requires human or independent review because structural tests cannot prove prose equivalence. Token counts remain advisory and were omitted because the repository has no required pinned tokenizer for this change.

The five selector deferrals are exact-path repository-maintainer decisions. They do not waive CMD1, MP1, MP2, or focused package/literal-consumer checks and do not create a generic evidence bypass.

No follow-up is required for the scoped change. Other skill optimizations require separate proposals.

## Readiness

All implementation milestones and material finding resolutions are closed. This explanation covers the final reviewed implementation through `7915d753`, its first final review recorded in `92b129d1`, and the later exact-path selector deferrals. A focused final rereview is required before the `verify` gate resumes; this artifact does not claim branch, PR, release, or merge readiness.
