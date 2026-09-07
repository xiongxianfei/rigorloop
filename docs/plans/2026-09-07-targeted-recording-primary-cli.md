# Targeted Recording and RigorLoop Record Format v2 delivery plan

## Purpose / big picture

Deliver the approved purpose-specific CLI over one recording engine and plain JSON v2 records. Actors supply decisions; the CLI performs selection, identity computation, construction, registration, preservation and recoverable persistence. Implementation is sequenced to prove the safety substrate before exposing the ordinary skill path.

## Current Handoff Summary

- Owning change record: [2026-09-07-targeted-recording-primary-cli](../changes/2026-09-07-targeted-recording-primary-cli/change.yaml).

Mutable activity, work progress, applicability, reviews and findings live only in that record and its registered supporting records. This plan carries stable intent. Its execution uses the currently supported explicit-recording-v1 recording interface; it does not migrate its own records to the format being designed.

## Source artifacts

- Proposal: [Make Targeted Recording the Primary CLI Interface](../proposals/2026-09-07-targeted-recording-primary-cli.md), registered proposal-review-r1.
- Behavioral requirements and architecture: [CLI](../design/cli/cli.md), [Workflow](../design/workflow/workflow.md), [Record Format](../design/record-format/record-format.md).
- Approved Design Review: [design-review](../changes/2026-09-07-targeted-recording-primary-cli/reviews/design-review.md). Its exact subjects and current applicability, not a Git branch or this plan, identify the approved basis.
- Prior-contract test spec: not applicable to this explicitly selected recording profile. The three model documents combine specification and architecture under the Constitution; no separate ADR or test-spec is introduced.

## Context and orientation

The existing recording foundation is packages/rigorloop/dist/lib/record-store.js, record-store-contract.js, record-store-files.js and record-store-cli.js, invoked from packages/rigorloop/dist/bin/rigorloop.js. This repository authors runtime modules under dist; adapter release archives are a different generated surface. Existing record-store tests cover v1 behavior. Reuse their persistence code only after demonstrating the new contract's safety outcomes.

The canonical v1 schema is schemas/explicit-recording-v1.schema.json, bundled by scripts/build-record-store-schema.mjs. Templates live under templates/explicit-recording/ with the packaged mirror under packages/rigorloop/dist/templates/explicit-recording/. Model documents already occupy their model-centered directories. Model-path/selector support is an existing baseline to preserve, not new unfinished implementation.

No project-map inference is needed: placement is grounded in these directly inspected runtime, schema, test and distribution surfaces. No latency or numerical token-saving promise is assumed.

## Non-goals

- No historical conversion, automatic applicability/readiness decisions, new lifecycle stage, authentication scheme, arbitrary repository edit, daemon or new OS guarantee.
- No migration of this v1 change or old review subjects to v2, even though the new writer supports explicitly created v2 roots.
- No release tag, publication, push, deployment, installation-infrastructure redesign or activation of a customer's project. Prepare and validate the coordinated adoption package; explicit release/activation authority remains separate.
- Do not weaken the accepted diagnostic freshness guarantee or v2 EntryRef namespaces to simplify implementation.

## Requirements covered

The following matrix allocates every model SR. Each TG is defined in its owning milestone; command IDs are defined under Validation plan.

| Requirements | Architecture boundary | Milestone and proof |
| --- | --- | --- |
| CLI-SR-02, CLI-SR-09, CLI-SR-10; RF-SR-01, RF-SR-02, RF-SR-06 | Stored schema/version/path/reference dispatch | M1 TG-01; M2 TG-02; M5 TG-07 |
| CLI-SR-04, CLI-SR-05, CLI-SR-06, CLI-SR-08; RF-SR-08 | Shared exclusion, identity checks, transaction and recovery | M2 TG-02; TG-FINAL-01 |
| CLI-SR-01, CLI-SR-14, CLI-SR-19, CLI-SR-21, CLI-SR-22; RF-SR-07; WF-SR-14, WF-SR-15 | Explicit scoped queries and subject inspection | M3 TG-03; TG-FINAL-01 |
| CLI-SR-17, CLI-SR-20 | Compact result rendering and observed-basis digest | M3 TG-04; M4 TG-05; TG-FINAL-01 |
| CLI-SR-03, CLI-SR-12, CLI-SR-13, CLI-SR-15, CLI-SR-16; RF-SR-03, RF-SR-04 | Lossless targeted candidate construction and batch | M4 TG-05; TG-FINAL-01 |
| CLI-SR-07, CLI-SR-11; RF-SR-05; WF-SR-01, WF-SR-02, WF-SR-04, WF-SR-05, WF-SR-06, WF-SR-12, WF-SR-13 | Actor-owned decisions, correction availability and attribution | M4 TG-06; M5 TG-07; TG-FINAL-01 |
| CLI-SR-18; WF-SR-03, WF-SR-07, WF-SR-08, WF-SR-09, WF-SR-10, WF-SR-11 | Guidance, exact review basis, model authority and coherent adoption | M5 TG-07/TG-08; TG-FINAL-02 |

All eight boundary rows in all three models are in scope. Input/reference/compatibility proof starts in M1, identity/temporal/failure proof in M2, read/diagnostic composition in M3, construction/state/correction proof in M4, and actor/distribution/adoption integration in M5. The local groups below name the distinct scenarios and the final groups cover their material interactions; milestone success is not complete-change correctness.

## Milestones

### M1. Versioned JSON structure and reference validation

- Milestone kind: implementation
- Engineering purpose: A pure validator admits exact v2 representation without changing existing v1 behavior.
- Requirements: RF-SR-01/02/06/08; CLI-SR-02/09/10
- Architecture responsibility: Record Format schema, namespaces and compatibility.
- Dependencies: None; preserve the supported v1 runtime.
- Implementation scope: Add separately versioned v2 stored and advanced request definitions, schema bundling and standalone validation. Add complete v2 fixtures/templates and JSON examples validation; retain v1 definitions unchanged. Runtime public activation is withheld.
- Files/components likely touched: schemas/, scripts/build-record-store-schema.mjs, scripts/validate-record-store.mjs, packages/rigorloop/dist/schemas/, record-store-contract.js, templates/explicit-recording/, packaged template mirror and record-store-contract tests.
- Required verification: TG-01 — Validate every record/field vocabulary with unknown-value regressions; body strings/escaping, duplicate keys, null/empty bounds, depth/byte limits, v2 origin, disjoint per-file IDs, field-specific EntryRef targets, missing/unsupported/cross-change references, cycles allowed without semantic reliance, same-candidate targets, v1 broad membership compatibility, and immutable-origin comparisons. Wrong extensions, dual manifests and mixed versions must fail closed.
- Evidence expectations: Focused automated positive/negative checks at the owned boundary, named command results, exact implementation/design subjects, and a concise explanation of any manual assessment.
- Implementation steps: Add failing contract cases; implement the bounded slice; run focused commands; reconcile the integrated candidate; hand off for independent Code Review.
- Validation commands: C1, C2, C3, resolved exactly in the command table below.
- Expected observable result: A pure validator admits exact v2 representation without changing existing v1 behavior.
- Completion criteria: All closed vocabularies have unknown-value rejection coverage; every reference field has valid and invalid target proof, and schema bundles/templates agree.
- Required evidence: Registered evidence.yaml check entries under this v1 change with subjects, procedure/result/summary; independent milestone code-review record with explicit applicability. Do not create routine standalone implementation or review logs.
- Review handoff: Independent Code Review of M1's implementation and its full required proof, before the next dependency starts.
- Optional commit boundary: `M1: Versioned JSON structure and reference validation`
- Risks: Record Format schema, namespaces and compatibility defects can invalidate later integrated claims; local success must not substitute for the required complete-change proof.
- Rollback/recovery: Keep v2 schema/fixture changes isolated; reverting M1 must not alter existing records or v1 schema bytes.

### M2. Extend the shared persistence substrate

- Milestone kind: implementation
- Engineering purpose: Both supported stored formats share one safety boundary; legacy records are never migrated.
- Requirements: CLI-SR-02/04/05/06/08/09/10; RF-SR-02/04/06/08
- Architecture responsibility: CLI filesystem, identity, publication and recovery.
- Dependencies: M1 reviewed.
- Implementation scope: Extend exact manifest/path dispatch and the shared advanced candidate pipeline for v2. Preserve advanced v1 input/result compatibility and safe recovery. Public targeted creation remains withheld until the complete adoption package is coherent.
- Files/components likely touched: record-store.js, record-store-files.js, record-store-contract.js, record-store-cli.js, scripts/validate-record-store.mjs and record-store workflow/CLI tests.
- Required verification: TG-02 — Exercise concurrent CLI writers and readers, stale target/revision/read basis, absent-root races, symlink/hardlink/path substitution, permission/I/O failure, prepare/publish/commit interruption and restore/complete. Verify coherent before/after or busy/recovery-required, exact recovery identities/bytes, unknown journal handling, post-publication basis drift handling, no-op precondition order, and lost-success stale retries. Test observed external edits at specified checks without claiming atomic control of external tools.
- Evidence expectations: Focused automated positive/negative checks at the owned boundary, named command results, exact implementation/design subjects, and a concise explanation of any manual assessment.
- Implementation steps: Add failing contract cases; implement the bounded slice; run focused commands; reconcile the integrated candidate; hand off for independent Code Review.
- Validation commands: C2, C3, C4, resolved exactly in the command table below.
- Expected observable result: Both supported stored formats share one safety boundary; legacy records are never migrated.
- Completion criteria: Fault injection proves each transaction phase and concurrent reader result; restore/complete preserve origin and registry atomically.
- Required evidence: Registered evidence.yaml check entries under this v1 change with subjects, procedure/result/summary; independent milestone code-review record with explicit applicability. Do not create routine standalone implementation or review logs.
- Review handoff: Independent Code Review of M2's implementation and its full required proof, before the next dependency starts.
- Optional commit boundary: `M2: Extend the shared persistence substrate`
- Risks: CLI filesystem, identity, publication and recovery defects can invalidate later integrated claims; local success must not substitute for the required complete-change proof.
- Rollback/recovery: Before publication rollback code normally; after any v2 save retain a capable reader/recovery implementation. Never downgrade an existing v2 root or remove recovery support for prepared transactions.

### M3. Scoped reads, subject identities and bounded receipts

- Milestone kind: implementation
- Engineering purpose: Readers expose useful scope and exact identities without deciding relevance or workflow readiness; diagnostic size cannot obstruct storage.
- Requirements: CLI-SR-01/14/17/19/20/21/22; RF-SR-07; WF-SR-14/15
- Architecture responsibility: CLI selection, observation and rendering.
- Dependencies: M2 reviewed.
- Implementation scope: Implement primary status/context/show including Verify and shared decisions, subject inspect, observation-detail paging, and the common bounded receipt renderer. Use internal/public test harnesses while normal activation is withheld.
- Files/components likely touched: CLI dispatcher/read adapters, result-renderer.js or focused recording renderer, observer in record-store.js, packaged schemas and CLI/query tests.
- Required verification: TG-03 and TG-04 — TG-03: all selector kinds/filters, empty/partial/missing scope, content vs summary, whole-item byte pagination, cursor validation, revision drift, full Verify/decisions, v1 origin unavailable, record_contract plus revision enabling first write, exact subject content/hash agreement, absent vs unreadable/unsafe subjects. TG-04: calculate observation digest from exact selected-store Subject traversal; B-to-C identical diagnostics conflict, absence/reappearance, silent-subject drift, dedup and retained-origin subjects, request-only reads excluded, recursive encoding stable. Demonstrate maximum receipt bound, omitted detail flags, advanced aggregate fallback, human/JSON parity, and no false rejection after publication/output loss.
- Evidence expectations: Focused automated positive/negative checks at the owned boundary, named command results, exact implementation/design subjects, and a concise explanation of any manual assessment.
- Implementation steps: Add failing contract cases; implement the bounded slice; run focused commands; reconcile the integrated candidate; hand off for independent Code Review.
- Validation commands: C2, C4, C5, resolved exactly in the command table below.
- Expected observable result: Readers expose useful scope and exact identities without deciding relevance or workflow readiness; diagnostic size cannot obstruct storage.
- Completion criteria: Every primary query family and all statuses have envelope/scope coverage; max-admissible observation density fits the receipt reserve without extra subject-count gate.
- Required evidence: Registered evidence.yaml check entries under this v1 change with subjects, procedure/result/summary; independent milestone code-review record with explicit applicability. Do not create routine standalone implementation or review logs.
- Review handoff: Independent Code Review of M3's implementation and its full required proof, before the next dependency starts.
- Optional commit boundary: `M3: Scoped reads, subject identities and bounded receipts`
- Risks: CLI selection, observation and rendering defects can invalidate later integrated claims; local success must not substitute for the required complete-change proof.
- Rollback/recovery: Read/renderer changes can be reverted independently before adoption; preserve prior advanced interfaces and any recorded format support.

### M4. Targeted construction and purpose-specific commands

- Milestone kind: implementation
- Engineering purpose: All normal operations accept explicit decisions without full-file reconstruction, manual hashes or registry assembly.
- Requirements: CLI-SR-03/07/11/12/13/15/16/17; RF-SR-03/04/05; WF-SR-01/02/04/05/06/12/13
- Architecture responsibility: CLI lossless constructor and actor-owned operations.
- Dependencies: M3 reviewed.
- Implementation scope: Implement every admitted mutation and batch over the shared engine, source-span edits, explicit registration/applicability, concern-origin construction forms, preview and compact help. Complete public dispatch without invoking historical eligibility engines.
- Files/components likely touched: Targeted recording modules, CLI entry/dispatcher, constructor/parser, shared renderer, schema definitions and command-level tests.
- Required verification: TG-05 and TG-06 — TG-05: change.create/link, activity.set, work.add/set, review.record, finding.add/set, blocker.add/set, evidence.record, applicability.set, decision.record, verify.record, batch; omitted fields/neighbors/whitespace/body preserved, missing decisions rejected, v2 body token round-trip, origin null/direct/from-review construction, immutable origin under every update path, ID collisions, overlapping edits, allowed same-batch references, all-or-none rejection, no-op and retries, preview writes nothing/reserves nothing. TG-06: after completed activity Verify records failure+blocker, Route later records correction, reviewer approval cannot close Verify blocker, stale review identities are retained; role labels never authenticate and successful save never establishes approval.
- Evidence expectations: Focused automated positive/negative checks at the owned boundary, named command results, exact implementation/design subjects, and a concise explanation of any manual assessment.
- Implementation steps: Add failing contract cases; implement the bounded slice; run focused commands; reconcile the integrated candidate; hand off for independent Code Review.
- Validation commands: C2, C4, C5, resolved exactly in the command table below.
- Expected observable result: All normal operations accept explicit decisions without full-file reconstruction, manual hashes or registry assembly.
- Completion criteria: Each individual command and equivalent batch operation enters the same validator/publisher and proves relevant failure outcomes. No hidden semantic defaults or convenience readiness aliases.
- Required evidence: Registered evidence.yaml check entries under this v1 change with subjects, procedure/result/summary; independent milestone code-review record with explicit applicability. Do not create routine standalone implementation or review logs.
- Review handoff: Independent Code Review of M4's implementation and its full required proof, before the next dependency starts.
- Optional commit boundary: `M4: Targeted construction and purpose-specific commands`
- Risks: CLI lossless constructor and actor-owned operations defects can invalidate later integrated claims; local success must not substitute for the required complete-change proof.
- Rollback/recovery: Before adoption revert adapters without losing advanced read/recovery capability; constructor must never be replayed by recovery against newer state.

### M5. Coordinated consumers, compatibility and adoption proof

- Milestone kind: implementation
- Engineering purpose: A fully consistent implementation/guidance/distribution package is reviewable for explicit adoption, with honest token evidence and no split normal paths.
- Requirements: CLI-SR-18; RF-SR-06/08; WF-SR-03/07/08/09/10/11 plus integrated requirements above
- Architecture responsibility: Workflow guidance, model ownership, templates and supported adapters.
- Dependencies: M4 reviewed; all earlier safety/projection evidence available.
- Implementation scope: Reconcile the exact adoption surfaces below, update skill guidance/resources and templates, validate packaged CLI/adapters, and demonstrate complete interactions. Prepare one coherent adoption diff for normal v2 creation; retain explicit advanced v1 compatibility creation. No release/customer activation is performed by this milestone.
- Files/components likely touched: Canonical skills and shared references, governance/spec/model navigation, templates, scripts/validation_selection.py, skill/model/example validators, scripts/build-adapters.py support, dist/adapters/README.md and manifest.yaml; packaged runtime and resources.
- Required verification: TG-07 and TG-08 — TG-07: every supported adapter maps to canonical targeted instructions, bounded per-operation help, explicit independence/downstream assessment and correction ownership. New primary roots require v2 only at coherent adoption; existing v1/historical roots retain identities/handlers, unknown clients fail closed, no fallback to old eligibility or manual reconstruction. Confirm exact model/example paths, owner-based validation selection and record-store metadata dispatch for both manifests. TG-08: controlled complete-interaction comparison against advanced full-record path on identical fixtures, measuring loaded guidance, reads, writes, previews/retries and follow-up reads; record tokenizer/version/totals and call counts without asserting a numerical saving.
- Evidence expectations: Focused automated positive/negative checks at the owned boundary, named command results, exact implementation/design subjects, and a concise explanation of any manual assessment.
- Implementation steps: Add failing contract cases; implement the bounded slice; run focused commands; reconcile the integrated candidate; hand off for independent Code Review.
- Validation commands: C1–C10 as applicable; TG-FINAL-01/02, resolved exactly in the command table below.
- Expected observable result: A fully consistent implementation/guidance/distribution package is reviewable for explicit adoption, with honest token evidence and no split normal paths.
- Completion criteria: All required adoption rows have exact reviewed diffs or justified unaffected dispositions; no required dependency deferred. Full integration and generated-output checks pass before activation is proposed.
- Required evidence: Registered evidence.yaml check entries under this v1 change with subjects, procedure/result/summary; independent milestone code-review record with explicit applicability. Do not create routine standalone implementation or review logs.
- Review handoff: Independent Code Review of M5's implementation and its full required proof, before the next dependency starts.
- Optional commit boundary: `M5: Coordinated consumers, compatibility and adoption proof`
- Risks: Workflow guidance, model ownership, templates and supported adapters defects can invalidate later integrated claims; local success must not substitute for the required complete-change proof.
- Rollback/recovery: Before external activation revert coordinated consumer/default changes together. Once users have v2 data, keep version-aware readers and explicit recovery; reverting guidance is not migration and must not revive an incompatible writer.

### M6. Final verification and durable explanation

- Milestone kind: lifecycle-closeout
- Engineering purpose: Independently establish final artifact/code/test coherence after all implementation milestones and review corrections.
- Requirements: WF-SR-03/08/09/10; all integrated TG-FINAL requirements.
- Architecture responsibility: Workflow final assessment, with CLI storage-only persistence.
- Dependencies: M1–M5 reviewed and required corrections reassessed; current evidence and review applicability explicitly established.
- Implementation scope: No new runtime work; newly found defects return to the responsible implementation/design milestone.
- Files/components likely touched: Only change-local evidence, review applicability, blockers and success-only Verify report through supported recording.
- Required verification: TG-FINAL-01 and TG-FINAL-02.
- Evidence expectations: Exact final subjects, named check results, proof coverage and durable explanation only on success.
- Implementation steps: Verify current evidence and reviews; repeat affected integrated checks where subject drift requires it; record failed evidence/blockers or an explicit successful assessment.
- Validation commands: C4–C10 as applicable plus final record-store inspect/check.
- Expected observable result: A truthful final assessment; storage success never substitutes for verification.
- Completion criteria: All in-scope work and required proof are accounted for; unresolved required concerns prevent justified completion.
- Required evidence: evidence.yaml and, only on success, verify-report.md in the current v1 change. No conversion to v2 is part of this plan.
- Review handoff: Isolated stop; PR/publication/customer activation require their own authority.
- Risks: Stale final subjects or missing transitive guidance can invalidate otherwise passing checks.
- Rollback/recovery: Record defects and explicitly assign their correction; do not fabricate success or delete historical evidence.

## Change-level verification

### TG-FINAL-01. Complete correction and safe recording interaction

- Covers: M1–M4; CLI-SR-01–22, RF-SR-01–08, WF-SR-01–06/09/12–15 across input, state, identity, composition, temporal, failure, compatibility and external boundaries.
- Demonstrate: Fresh agent gets contract/revision through primary context, inspects exact subjects, records evidence+blocker after completion, Route acts separately, correction evidence/review follow, reporter disposes, Verify records final explanation, downstream reads full report/decisions. Repeat material variants for v1 compatibility, conflicts, interrupted batch/recovery and maximum diagnostic density including B→C continuation conflict.
- Evidence expectations: Public CLI end-to-end subprocess tests through C4; retained before/after invariants and compact result assertions in tests, with summarized actual outcomes in registered evidence. Failure cases assert no false save/rejection, no mixed snapshot, and truthful origin/subjects.
- Non-applicability: None; these behaviors cross schema, construction, query, publisher and actor guidance.

### TG-FINAL-02. Consumer and package coherence

- Covers: M5; CLI-SR-18, RF-SR-06/08, WF-SR-03/07–11.
- Demonstrate: Packed CLI and all supported adapter archives contain agreeing schemas, resources and examples; normal skills use targeted commands, historical profiles remain explicit, unknown contracts fail closed, read-only model checks confer no approval, no customer activation or publication occurs.
- Evidence expectations: C6–C10, generated package/manifest checks and a bounded human review of actor-decision/independence wording. Automation proves resource presence and behavior; human review is necessary for engineering meaning and adequate context.
- Non-applicability: No live publication proof or new OS certification; release infrastructure is unchanged. Release-owner validation remains mandatory at a later actually selected release.

## Validation plan

Commands below are repository-owned entry points. Implementation adds focused cases under their existing harnesses; no command result is claimed by this plan. C2's record-store prefix is the required home for new recording suites so focused selection includes them.

| ID | Exact command | Purpose and timing |
| --- | --- | --- |
| C1 | `node scripts/build-record-store-schema.mjs --check` | M1/M5 canonical and packaged schema parity; extend the existing builder to include v2. |
| C2 | `node --test packages/rigorloop/test/record-store-*.test.js` | M1–M4 focused representation, CLI and persistence proofs including new cases. |
| C3 | `python scripts/test-change-metadata-validator.py` | M1/M2 contract-aware repository metadata compatibility, including v2 manifest dispatch. |
| C4 | `npm --prefix packages/rigorloop test` | M2–M5 public integration and historical regression. |
| C5 | `python scripts/validate-boundary-first.py --check --path docs/design/cli/cli.md --path docs/design/workflow/workflow.md --path docs/design/record-format/record-format.md` | Model structure only; M3–M5, not semantic approval. |
| C6 | `python scripts/validate-skills.py skills` and `python scripts/test-skill-validator.py` | M5 normalized skills, references and instruction boundaries. |
| C7 | `python scripts/test-boundary-first-validation.py` and `python scripts/test-select-validation.py` | M5 model/example routing and closed validation vocabulary. |
| C8 | `python scripts/test-adapter-distribution.py` | M5 supported archive generation, mapped-resource integrity and parity using temporary outputs. |
| C9 | `python scripts/test-npm-package-publication.py` and `python scripts/test-release-transaction.py` | M5 package contents and retained release safety without publication. |
| C10 | `git diff --check` | Every milestone's whitespace integrity, not behavioral proof. |

Token comparison is a controlled manual/automated hybrid under TG-08: run the same finding append, evidence+blocker, applicability/reassessment and final-read tasks through both interfaces against isolated equal fixtures. Save totals, tool/tokenizer versions and interpretation in registered evidence; do not commit transcripts or operation requests. A count without loaded skill content and required follow-up reads is insufficient. Reviewer assesses whether observations support the stated benefit, not an invented threshold.

At a separately authorized release, use bash scripts/release-verify.sh with that release's exact approved tag and tracked release notes; no tag is selected by this plan and no unsupported future tag is treated as tested.

## Adoption surface allocation

The approved CLI-MAP-01–07 and WF-MAP-01–10 inventories remain the source of displaced-rule ownership. M5 reconciles them through these exact current entry surfaces; source resources reached by these entries must receive an exact changed-or-unaffected disposition before the coherent adoption diff can pass Code Review.

| Surface | Exact paths and treatment |
| --- | --- |
| Governance and contracts | CONSTITUTION.md, AGENTS.md, specs/rigorloop-workflow.md, specs/skill-contract.md, specs/compact-current-state-change-record.md, specs/governed-lifecycle-cli.md, specs/boundary-first-proof-model.md, docs/architecture/system/architecture.md; amend only contract-selected responsibility/placement/interface sections and retain historical rules. |
| Ordinary stage skills | skills/proposal/SKILL.md, skills/proposal-review/SKILL.md, skills/architecture/SKILL.md, skills/spec/SKILL.md, skills/design-review/SKILL.md, skills/plan/SKILL.md, skills/delivery-review/SKILL.md, skills/implement/SKILL.md, skills/code-review/SKILL.md, skills/route/SKILL.md, skills/verify/SKILL.md; replace their explicit-recording full-record path with targeted procedure. |
| Support skill consumers | skills/bugfix/SKILL.md, skills/ci-maintenance/SKILL.md, skills/pr/SKILL.md, skills/research/SKILL.md, skills/explore/SKILL.md, skills/learn/SKILL.md; review their workflow interactions and update only if the new profile is consumed. |
| Shared authoring/review resources | Relevant files under the above skills' references/ and assets/ selected by their resource maps; expand and record each exact path before M5 edits, preserve historical procedure by explicit profile and reject missing resources. No installed .agents/.codex copies are authored. |
| Validation and distribution | scripts/skill_validation.py, scripts/boundary_first_validation.py, scripts/validation_selection.py, scripts/validate-record-store.mjs, scripts/build-record-store-schema.mjs, scripts/build-adapters.py, scripts/validate-adapters.py, dist/adapters/README.md, dist/adapters/manifest.yaml; generated archives are temporary release outputs, never hand-edited source. |

This allocation is a bounded resource-closure task, not permission to rewrite entire files. Discovery of an unallocated semantic requirement returns to Design; a newly identified implementation resource within the declared boundary receives plan allocation before reliance.

## Risks and recovery

- Lossless editing and immutable origin interact with advanced writes: prove preservation before exposing targeted commands; use exact prepared bytes during recovery.
- Closed v2 namespaces intentionally differ from v1 membership: dispatch by stored contract, never reinterpret old IDs or invent missing origin.
- Diagnostic scans can be large: stream/count/hash within existing store limits and prepare fitting receipts before publication; do not add an undocumented subject-count restriction.
- Consumer adoption can drift across transitive resources: M5 cannot close with required dependencies deferred or parallel ordinary full-file paths retained.
- A public name collision with an existing command is a Design reconciliation issue, not permission to fall through to historical semantics.
- Failure after a v2 root exists requires compatible readers/recovery even if the user-facing adoption is rolled back. No plan step rewrites old root contracts.

## Dependencies

M1 → M2 → M3 → M4 → M5 → M6. Each implementation milestone receives independent Code Review before its dependent milestone. Delivery Review approves this exact plan against the exact current Design Review; later model or material plan changes require the appropriate rereview. Final Verify does not substitute for missing milestone proof.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-07 | Establish representation and recoverable persistence before targeted writes. | Every public adapter must enter a proven shared boundary. | Separate per-command writers and broad public activation before safety proof. |
| 2026-09-07 | Keep activation/publication separate from the reviewed adoption package. | Proposal and design exclude release activation; intermediate incomplete surfaces must not become a normal user path. | Publishing a helper early or silently replacing installed guidance. |
| 2026-09-07 | Keep this initiative's existing v1 change record. | New v2 format support is not a historical migration design. | Renaming existing review files or fabricating origin during implementation. |

## Readiness

See the owning change record for current workflow state. Remaining completion gates are independent Delivery Review, implementation and Code Review for M1–M5, required correction reassessment, and successful final Verify. This plan does not claim those outcomes.
