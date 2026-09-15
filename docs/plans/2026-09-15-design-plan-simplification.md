# Design and Plan skill simplification

## Purpose / big picture

Make Plan's task, authority and applicable methods understandable before detailed recording construction, while preserving every applicable obligation. Retain Design's existing package with explicit assessment and prove that both authoring handoffs and supported installed packages remain complete. Keep the coupled guidance and reader changes in one reviewable implementation milestone.

## Current Handoff Summary

- Owning change record: [2026-09-15-design-plan-simplification](../changes/2026-09-15-design-plan-simplification/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in that record.

## Source artifacts

- Proposal: [Design and Plan simplification](../proposals/2026-09-15-design-plan-simplification.md); upstream review ID `proposal-review` in the owning registry.
- Spec: [Plan Design](../design/skill/authoring/plan.md), especially PLAN-SR-01–08, PLAN-DEC-02 and Authoring presentation; [Skill Design](../design/skill/skill.md) supplies the common preservation/resource contract.
- Architecture: those models plus the retained [Design authoring model](../design/skill/authoring/design.md). Exact approved Design Review ID `design-review` and registered member IDs `skill`, `plan`, `design` are the governing package; consume their current exact identities through CLI context, not reconstructed aggregate hashes.
- Prior-contract test spec: not applicable; acceptance intent belongs to the models and concrete verification allocation belongs to this plan.
- Proof and handoff policy: [Validation](../design/engineering/validation.md), [Assessment](../design/skill/assessment.md), [Packaging](../design/engineering/packaging.md) and [CONSTITUTION.md](../../CONSTITUTION.md).

## Context and orientation

Canonical skill sources are under `skills/`; inspect them directly for this scope. This plan does not rely on project-map currency. Plan currently holds detailed recording in its body, while `references/governed-plan-authoring.md` depends on that parent procedure. The selected change moves the complete profile into this existing reference and preserves body classification/stops. Design already has the selected core-first structure and remains unchanged.

`scripts/lib/validation/skill_validation.py` selects four recording references and otherwise falls back to an inline heading. Its plan-surface reader also uses that heading to select current `change.json` placement. Inspect installed-placement and normalized-layout callers as well; record an unaffected disposition where the Plan path cannot reach a reader, rather than changing unrelated review behavior. Existing tests in `tests/skill/skill_contract_tests.py` contain independent reference-fault fixtures; canonical guidance and asset tests live alongside them. Build/installation proof uses the existing adapter tools, not authored generated output.

## Non-goals

- No new skill, resource family, runtime selector, public operation, invocation, record schema, document format or shared policy.
- No changes to the retained Design package, Plan's three assets/fingerprints, reviewer procedures or unrelated capabilities unless a demonstrated required compatibility correction returns to its owning Design and receives appropriate review.
- No separate project-use pilot, token benchmark, length quota or recurring report. Semantic package assessment remains required under existing policy.
- No release, publication, merge or installation into active user environments; temporary qualification supplies no external authority.
- No closure of wider FU-015–018 adoption responsibilities.

## Requirements covered

| Requirement / obligation | Allocation | Proof |
| --- | --- | --- |
| PLAN-SR-08; SKL-SR-03/04/07/12/32 | M1: task-first equivalent with complete core and conditional procedure | TG-01, TG-02, TG-FINAL-01 |
| PLAN-SR-01/02/03 | M1: safe sequence, complete milestone/proof allocation and stable output | TG-01, TG-FINAL-01 |
| PLAN-SR-04/05/07 | M1: exact operations, authority, approved initialization and retry preservation | TG-01, TG-02 |
| PLAN-SR-06; SKL-SR-08–14 | M1: selected resources, unchanged assets and reader reconciliation | TG-02, TG-FINAL-02 |
| Retained Design responsibility, examples, view selection and exact handoff under DES-SR-01–22 where applicable | M1: complete-package retention and consumer correspondence | TG-01, TG-FINAL-01/02 |
| Existing Assessment closeout and Constitution validation/cleanup obligations | M1 proof and separate final checkpoint/Verify | All groups, final review and current registered evidence |

All eight Plan model boundary rows are allocated: input and composition to TG-01/02 and TG-FINAL-01; state and identity to TG-01; temporal and recovery to TG-01/02; compatibility and external/package conditions to TG-02 and TG-FINAL-02. Conditional external commands remain permission-bound; this initiative requires only local temporary qualification. No boundary is waived by a passing structural check.

## Milestones

### M1. Reconcile Plan guidance and its consumers

- Milestone kind: implementation.
- Engineering purpose: change the entrypoint, selected recording reference and affected readers together so every committed complete package retains its checks and authority boundaries.
- Requirements: all rows in Requirements covered; PLAN-DEC-02 supplies the presentation choice.
- Architecture responsibility: Plan owns placement and allocation; Skill owns common package rules; retained Design and Assessment supply the unchanged author/reviewer interfaces.
- Dependencies: current exact approved Proposal and Design packages; independent Delivery Review of this plan; an authorized implementation invocation.
- Implementation scope: Plan body/reference rewrite, directly affected recording/placement/layout checks and meaningful regression protection, complete Design retention evidence and integrated package/handoff qualification.
- Files/components likely touched: `skills/plan/SKILL.md`, `skills/plan/references/governed-plan-authoring.md`, `scripts/lib/validation/skill_validation.py`, directly affected helpers in `tests/skill/`, and this change's registered evidence. Existing Plan assets, shared sources and Design package are inspected preservation subjects.
- Required verification: TG-01 and TG-02 locally; TG-FINAL-01 and TG-FINAL-02 once the complete revised package is available, before milestone handoff.
- Evidence expectations: grouped original-to-surviving obligation mapping, independently selected fault cases with fail-before/pass-after observations where feasible, commands/results and exact subjects, named semantic assessor with actual handoff artifacts, both candidate identities and byte/resource observations.
- Implementation steps:
  1. Capture exact original packages and affected reader/test scope. Establish meaningful Plan reference-selection and current-placement negative proof before changing production readers. Preserve existing non-Plan protection; expected inputs must not be copied from the production selector table.
  2. Implement the approved body equivalent and complete the existing governed reference, removing its parent-procedure dependency. Keep full quality, shared applications, operation distinctions, assets and claim limits. Reconcile readers and incidental wording checks in the same slice.
  3. Map each removed/relocated coherent obligation to its surviving instruction or justified duplication removal. Inspect the retained Design package and unchanged reviewer contracts; surface any contradiction to the correct owner.
  4. Run focused proof, full relevant suites, fresh temporary candidate qualification and integrated handoff assessment. Resolve failures before handoff and preserve original failure evidence.
- Validation commands: V1–V6 below, and V7 for the complete branch engineering subject before final review/Verify. Exact commands and candidate paths belong in evidence.
- Expected observable result: a reader selects Plan's task and authority before recording detail, reaches complete applicable methods, emits unchanged complete plan output and cannot bypass required validation through heading removal. Design and both review handoffs remain usable.
- Completion criteria: all scope above delivered, each required group supported by current proof, both complete packages reconciled, no unresolved required correction, and an independently reviewable exact diff. A shorter entrypoint alone is insufficient.
- Required evidence: registered implementation/preservation/validation evidence and independent `m1-code-review` with exact affected subjects; findings retain reporter-owned disposition.
- Review handoff: independent Code Review of the whole slice against the exact approved Design/Delivery packages, all changed readers/tests and complete published guidance; include both integrated proof groups.
- Optional commit boundary: `M1: simplify Plan guidance with complete recording and consumer protection`. Tests may establish a failing baseline locally, but do not hand off a source-only or validator-only intermediate package as complete.
- Risks: heading removal silently bypasses checks; repetition removal loses a stop; delayed loading hides initialization authority; shared test changes weaken another skill.
- Rollback/recovery: restore the complete affected Plan body/reference/reader/test set coherently, preserve registered history and rerun affected checks. Do not repair failures by weakening guards, removing required tests, changing old judgments or overwriting user work.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: M1 and every in-scope correction complete with applicable milestone review.
- Assessment: fresh independent final whole-change Code Review of the entire change, including governing documents, actual delivered skills/readers/tests, preservation and integrated interactions.
- Evidence: exact final subjects, nonauthor basis, complete judgment and reporter-owned concern dispositions.
- Successor: distinct final Verify of the complete proposal/design/delivery/implementation/review/proof chain. Corrections return to their owner and require affected reassessment.

This checkpoint remains separate even with one implementation milestone. Integrated proof and milestone review cannot substitute for it.

## Change-level verification

### TG-FINAL-01. Complete authoring-to-review correspondence

- Covers: M1; PLAN-SR-01/02/03/08 and retained Design/Assessment interfaces.
- Demonstrate: actual Design output plus its exact review member map provide sufficient Plan inputs; a concrete filled output from the unchanged plan/milestone assets provides Delivery Review's required allocation. Resolve review IDs/member maps through current records without adding mutable approval state to the stable plan. Identify the first consumer that stops when a required input or current identity is missing.
- Evidence expectations: an independent nonauthor examines the revised package and concrete filled artifacts, recording starting scope, exact paths/identities, bounded trace, expected and observed fields and failure points. Existing current artifacts may supply the filled examples if they actually exercise these fields; otherwise prepare bounded temporary filled examples from the real assets. No invented reviewer approval or workflow execution claim. This is artifact correspondence, not a separate customer-use pilot.
- Freshness: refresh after relevant producer, consumer, asset or authority changes; an earlier conceptual Design Review trace alone cannot prove the implemented guidance.
- Non-applicability: none; the authoring/review composition is an explicit approved obligation.

### TG-FINAL-02. Complete supported packages

- Covers: M1; PLAN-SR-06/08, common resource integrity and Design retention.
- Demonstrate: fresh Codex and Claude candidates contain the complete current Plan and Design packages, including untriggered references and assets; transformed content follows the existing adapter rules and required local resources work in temporary installations. Unrelated skill selection and generated contracts remain intact.
- Evidence expectations: V4 build/validation/clean-install results, actual archive hashes and temporary paths, source-to-candidate/installed byte and resource comparisons, asset fingerprint and retained-source comparison. Existing adapter regressions supplement actual candidate proof.
- Freshness: rebuild after any relevant canonical source, resource, adapter or generation change. Unchanged final candidates may be reused only with affirmative exact-basis reasoning.
- Non-applicability: none; installed self-containment cannot be established by canonical prose alone.

## Validation plan

### TG-01. Semantic preservation and useful simplification

An independent nonauthor inspects exact original and revised Plan paths plus the complete retained Design package. In the existing review evidence, record the task context, loaded methods, bounded action, expected output/stop, actual surviving instructions and limitations. Compare a portable create/revise path, governed create/revise, approved initialization with absent/existing work, stale/unknown authority, late resource selection and interrupted/retried recording. Require complete quality/asset fields, no portable fallback from invalid governed authority, no inferred automation, no existing-work mutation and no save-as-approval claim. Inspect both ordinary and adopted-policy paths. Explain why each removed repetition is redundant and why retention remains useful. Semantic instruction meaning cannot be proved by word matching; no live agent benchmark is required. Refresh this assessment after relevant instruction, authority or asset changes.

### TG-02. Reader and output protection

Demonstrate Plan's valid selected reference without an inline profile, then missing boundary/trigger, wrong or unmapped selection, absent/unreadable/escaped reference, incomplete or wrong profile, and an unrelated/inline file that must not satisfy the selected path. Demonstrate current `change.json` plan/state/navigation distinction after relocation and rejection of retired placement. Keep existing non-Plan cases, asset fields/fingerprints and resource checks. Unknown values must reject before consistency checks for any changed closed selector. Add cases for distinct detection outcomes, not a Cartesian matrix. Inspect existing CLI persistence proof and preserve unchanged commands; the change does not justify inventing a new persistence protocol or racing live records.

### Repository-owned commands

| ID | Command | Purpose / allocation |
| --- | --- | --- |
| V1 | `python scripts/validate-skills.py skills/plan/SKILL.md skills/design/SKILL.md` | M1 canonical structure, resource map and asset checks; expand to `python scripts/validate-skills.py skills` for complete final selection. |
| V2 | `python tests/skill/test-skill-validator.py` | M1 full affected reader, guidance, resource and asset regressions after focused fail-first cases. |
| V3 | `python tests/engineering/packaging/test-adapter-distribution.py` | M1 full supported adapter and installation regressions, including current consumers. |
| V4 | Candidate commands below | M1 and final current package qualification for TG-FINAL-02. |
| V5 | `node scripts/validate-record-store.mjs docs/changes/2026-09-15-design-plan-simplification/change.json` | After stage-owned recording; structure/references, not approval. |
| V6 | `bash scripts/ci.sh --mode local` | Each actual changed set; includes required guide/model/record/CLI checks selected by repository policy. |
| V7 | `bash scripts/ci.sh --mode pr --base 851f5f9c49eea8f40c82db3aa18e5c96667d5026 --head HEAD` | Complete branch engineering validation before final review/Verify; original merged base includes proposal/Design/plan changes. Record resolved head and selected broad scope. |

Use `bash scripts/ci.sh --mode explicit --path PATH` only for focused iteration, replacing PATH with each actual affected path. A subset cannot establish whole-change readiness. Complete required broad smoke when selected; no selector or Markdown-wide exemption. Reuse passing proof only with exact unaffected source/environment reasoning; required fresh checks or relevant corrections override reuse.

```bash
plan_candidate_dir="$(mktemp -d /tmp/rigorloop-design-plan-candidate.XXXXXX)"
python scripts/build-adapters.py --version v1.0.0 --output-dir "$plan_candidate_dir"
python scripts/validate-adapters.py --version v1.0.0 --adapter-root "$plan_candidate_dir" --clean-install-smoke --skill plan --skill design
```

The version is a local qualification label, not a release. Keep actual paths/hashes/results in evidence, then clean only owned temporary outputs after reliance is preserved. No active installation, publication or network mutation is required. Failed or incomplete checks remain visible and block their dependent claim; a rerun records new evidence rather than rewriting the original result.

## Risks and recovery

- Required guidance may be moved without a safe trigger. Recover the complete body/reference pair and strengthen the boundary proof before reapplying extraction.
- A validator could accept a missing profile or select historical placement. Preserve fail-first negative detection and reconcile all actual callers, with unchanged-surface reasoning for excluded callers.
- A repeated safety instruction may serve a different path. Retain it until the obligation mapping and independent review establish equivalent coverage.
- An integrated trace may use hypothetical fields. Use actual filled assets/current records and expose the first missing-input stop; never fabricate approval or runtime execution.
- New evidence may make earlier proof stale. Preserve original identities, route corrections to their owner, and require appropriate reassessment. Record-store conflicts require current rereads and authorized recovery, not full-file reconstruction.

## Dependencies

- Current exact `proposal-review`, `design-review` and subsequent Delivery Review of this primary plan before implementation reliance or approved-work initialization.
- Existing local Python/Node toolchains and repository-owned validation commands; resolve actual environment in evidence.
- No source/asset/contract modification outside the approved package without owning-stage reconciliation and review.
- No persistent automation, external handoff or broader adoption authority is created by this plan.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-15 | One implementation milestone owns guidance, reference and reader changes. | These form one compatibility and rollback unit; every complete intermediate package must retain protection. | Separate source/validator milestones create a broken or unchecked intermediate state. |
| 2026-09-15 | Allocate integrated handoff and candidate proof before M1 handoff, then retain separate final whole-change review and Verify. | One milestone still contains cross-owner and installed-package boundaries. | Local helper checks or a milestone approval cannot prove complete composition or replace final gates. |
| 2026-09-15 | Retain Design and all current assets/shared policy; assess complete packages. | The approved Design selects useful Plan changes and justified Design retention. | Forced edits, a separate usage pilot and line quotas add no established benefit. |

## Readiness

See the owning change record for current workflow state. This plan defines stable execution and proof intent; only current independent Delivery Review supplies the corresponding approval for authorized implementation.
