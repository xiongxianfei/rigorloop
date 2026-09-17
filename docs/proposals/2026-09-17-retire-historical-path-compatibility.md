# Retire remaining historical-path compatibility

## Challenge

Current validation still carries old path names, source-relocation aliases and special cases for retired documents and tools. They preserve comparisons against historical layouts and retain dedicated tests after the supported product behavior has moved. Current script routing also translates new locations back to predecessor names, so deleting aliases alone would break selection for live code.

The saved unfinished compatibility workspace overlaps work now merged in PRs #199 and #200. System-owned test rules, Release/Skill/Authoring test designs, executable test refinement and catalog admission are delivered; feature/proof operations and exclusive resources are retired. Restoring that workspace wholesale would reinstate superseded policy and removed tests. This proposal carries forward the remaining selected obligation against merged baseline `ddb7eb9e` while preserving the saved work and earlier judgments separately.

## Goals

- Retire all remaining historical-path compatibility identified in this round, including accepted generic flat model paths, without deferring a named family.
- Select validation directly from current declared ownership and locations, preserving meaningful checks for current files and ordinary deletions and renames.
- Remove exclusive aliases, shims, rules, tests and fixtures together; retain independently justified current rejection, containment, privacy and record-safety proof.
- Finish the remaining saved-work obligation without duplicating merged test-design work, reviving feature/proof support or treating historical reviews as current approval.

## Scope and non-goals

| Initial intent and family | Treatment | Scope budget treatment |
| --- | --- | --- |
| Five retired Skill archive mappings | in scope: remove special recognition and historical routing | core to this proposal |
| Old `docs/examples/` prefix | in scope: remove its special accepted/no-check category | core to this proposal |
| Absent historical model names, old directory locations and relocation aliases | in scope: remove substitution by a current model, including test/distribution aliases and historical source-to-receiver move pairing | core to this proposal |
| Generic flat model documents | in scope: withdraw their accepted-format contract; retain explicitly declared current project paths and the current portable model-directory format | core to this proposal |
| Old script/test/resource locations and retired tool/fixture classifications | in scope: replace predecessor-based live routing with current locations and remove historical-only aliases and special categories | core to this proposal |
| Legacy document deletion exceptions | in scope: remove special success/current-owner substitution for obsolete document families while preserving ordinary current-owner deletion handling | core to this proposal |
| Owning Designs, published guidance if affected, test intent, selector/executor consumers and compatibility communication | in scope | same-slice dependency |
| Shared rules, existing three model catalogs, script simplification and admission already merged in PR #199 | out of scope for reimplementation: preserve the current delivered behavior | out of scope |
| Broader detailed test-catalog adoption beyond the selected three models | deferred follow-up: current model owners retain proportionate coverage under System rules; this retirement does not silently authorize catalog rollout | separate proposal |
| Feature/proof operation withdrawal already merged in PR #200 | out of scope for reimplementation: retain current unsupported-input behavior and source authority | out of scope |
| Unrelated package/API/record-format compatibility, historical record-store exclusion, active release evidence and publication policy | out of scope: current obligations remain | out of scope |

A current path is not obsolete because it resembles a former layout. In particular, the explicitly declared System root `docs/design/system.md` remains current. Ordinary deleted/renamed current sources and selected live release evidence retain their owning checks. Historical record files and their original identities are not deletion targets. Representative package versions and filenames in otherwise useful fixtures are not automatically compatibility promises. No automatic customer-file conversion, archive rewrite, new permanent compatibility registry, runner replacement or broad model-catalog rollout is included.

## Governing principle

Current validation follows current declared ownership; retired layouts carry no continuing operational support promise.

## Proposed direction

Withdraw the historical-path support guarantee across every in-scope family, and reconcile current routing before removing its predecessor machinery. Unknown or unsupported input must remain visible and fail clearly, including when mixed with valid paths. Removing a compatibility category must not become a blanket ignore, invented successful check or silent loss of required validation.

Preserve Git discovery of ordinary additions, deletions and both rename endpoints. Current source ownership determines their protection. The ability to compare arbitrary pre-retirement layouts is intentionally withdrawn; no fallback may resurrect a removed name merely because Git can find it in history. Documentation must explain the supported current-layout boundary and how contributors can update their branch or comparison basis without changing the validator to accept old paths again.

Current declared repository model paths and the supported portable model-directory layout remain authoritative. Generic flat-model acceptance ends. Reconcile System, Validation and Authoring/Design wherever they explicitly promise the old format or old-range behavior, preserving stable model IDs and current examples. Old documents can remain readable project-authority source material without being accepted validation targets or automatic migration inputs.

Apply System's existing test-maintenance rules to retire historical compatibility obligations and their exclusive proof. Shared safety observations move to small current-layout fixtures when necessary. Current routing, mixed valid/unsupported inputs, actual deletion/rename discovery and the public model boundary require direct observations. Do not recreate the deleted compatibility inventory as a permanent per-filename negative-test ledger or replace historical exceptions with broad acceptance.

Completion accounts for every family above, reconciles all live consumers and removes exclusive maintenance. The saved proposal and scoped plans remain historical context; current merged contracts and fresh reviews own this work. Detailed behavior belongs to Design and exact sequencing, removal inventory and verification allocation belong to Delivery.

## Feasibility

Assessment: feasible within existing validation and model ownership, with no new dependency or subsystem. Direct inspection at `ddb7eb9e` found a five-entry Skill archive set, a separate examples-prefix category, explicit model aliases and generic model substitution, predecessor-based tooling routing, retired tool classifications and legacy prose-deletion handling in `validation_selection.py`. `validate_model_path` still accepts generic flat paths alongside current declared paths. Existing public-command, catalog and real Git selector suites provide usable boundaries for current behavior.

The saved-work comparison found 60 identical current files and 14 paths absent in both trees; 38 changed files include the later approved scope/review corrections and feature withdrawal. The 20 saved-only paths are the old proposal, two scoped plans, 16 old change/review/evidence records and one now-retired handoff test module. Both rename endpoints are counted, so this path comparison differs from the prior 131 status entries. These observations support selective continuation, not wholesale stash application or a claim that old approvals apply unchanged.

Material constraints are shared routing helpers, ordinary deletion proof, model-owned catalog admission and the change's own integration diff. A retirement must not leave its own required validation unexecutable or relax unknown-path failure to obtain a green run. Design must establish a coherent current-layout contract and Delivery must demonstrate the actual selected commands and integration range. No blocker to Design is known; unexplained live consumers block their removal until reconciled within this scope.

## Impact and major trade-offs

This deliberately breaks accepted flat-model inputs and some comparisons spanning obsolete layouts. Contributors using such inputs must adopt a supported current target or comparison basis; the tool must not silently rewrite their files. The benefit is a smaller operational contract and less historical-path maintenance. Generic Git handling, malformed-current-input rejection and current record integrity remain supported.

Retired tracked material remains recoverable through retained Git history; the saved local workspace remains preserved. Recovery restores a coherent matched contract/routing/test change rather than isolated aliases. This proposal grants no merge, release or publication authority and does not change already released artifacts.

## Decision requested

Confirm the user's selected direction through independent Proposal Review, then reconcile and independently review the affected Designs and Delivery allocation before implementation. Complete all named historical-path families in this change, preserve merged testing and feature-retirement outcomes, and carry the result through milestone review, fresh final whole-change review and distinct Verify. No named retirement family is deferred by this proposal, and no old saved assessment is retargeted.
