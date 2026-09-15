# Skill simplification delivery plan

## Purpose / big picture

Make the required skill task easier to understand and perform while preserving every applicable obligation. Deliver the approved implement/code-review pilot, then assess and simplify the remaining capabilities in coherent batches. A justified unchanged package is an acceptable inventory disposition; an unassessed package is not. Preserve specialist behavior and current public interfaces throughout.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-15-skill-simplification/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Skill simplification](../proposals/2026-09-15-skill-simplification.md).
- Spec: [Skill Design](../design/skill/skill.md), especially SKL-SR-30–32, Inventory simplification and its model-owned acceptance scenarios.
- Architecture: Skill's existing views and SKL-DEC-06/07; specialist owners linked in its inventory table retain detailed behavior.
- Prior-contract test spec: none independently required for this initiative.
- Governing review records: [proposal-review](../changes/2026-09-15-skill-simplification/reviews/proposal-review.json) and [design-review](../changes/2026-09-15-skill-simplification/reviews/design-review.json). Read their current applicability and exact subjects through the CLI before reliance; this plan does not copy mutable judgments.
- Delivery and proof contracts: [Plan](../design/skill/authoring/plan.md), [Assessment](../design/skill/assessment.md), [Validation](../design/engineering/validation.md), [Packaging](../design/engineering/packaging.md) and the [Constitution](../../CONSTITUTION.md).

## Context and orientation

`skills/` is the authored product. Each entrypoint and its mapped references/assets form one package. Shared sources under `templates/shared/` and declared projection consumers retain their ownership. `scripts/lib/validation/skill_validation.py` contains recording-profile, installed-placement, plan-surface, structure and resource checks; its current recording and placement branches depend on inline headings. The pilot must reconcile those readers with the two new skill-local recording references in the approved Design. Supported test entrypoints are `tests/skill/test-skill-validator.py` and `tests/engineering/packaging/test-adapter-distribution.py`; their imported helpers remain part of the affected test surface.

Inspect sources directly for each family; this plan does not rely on project-map currency. Before editing a family, read its complete entrypoints, triggered/transitive methods, current owning Designs and relevant validator consumers. Outside the pilot, retain existing approved layouts. A need for a different layout, new resource architecture or changed behavior returns to Design and independent reassessment before implementation; this plan does not approve those decisions in advance.

Use registered `evidence.json` checks for milestone observations and registered review records for independent judgments. Group obligation mappings and before/after rationale by skill and responsibility in the existing evidence fields; avoid a new ledger or schema. Every mapping identifies the original subject, governing requirement/applicability, retained destination or justified supersession, affected consumers and proof. Evidence can refer to an implementation baseline commit for historical text; current obligations must remain understandable from current packages.

## Non-goals

- Change workflow policy, public invocations, closed vocabularies, record formats, permissions or required review/Verify gates.
- Apply the pilot's layout globally, force edits to compliant skills, or restore token-cost tooling and word-count targets.
- Build an agent-compliance harness, introduce mandatory prompt execution, or make an instruction inspection claim runtime behavior.
- Publish, push, release, merge or install into user environments. Local candidate generation and temporary installation checks stay inside owned test directories.

## Requirements covered

| Requirement or governing obligation | Allocation | Proof |
| --- | --- | --- |
| SKL-SR-30: full inventory, dispositions and preservation | M1 establishes the inventory; M1–M6 own the exact families below | TG-01, TG-04, TG-FINAL-02 |
| SKL-SR-31: pilot classification and independent recording selection | M1, with cross-family handoff assessment after M3 | TG-02, TG-03, TG-FINAL-01 |
| SKL-SR-32: useful improvement with complete ordinary/exceptional paths | Every changed entrypoint in M1–M6 | TG-02, TG-04, TG-05, both final groups |
| SKL-SR-01–15 and SKL-SR-24–27: common specialist, resource, portability and claim boundaries | Every applicable package in M1–M6 | TG-01–05 |
| SKL-SR-16–23: existing proposal-family obligations, with original applicability only | M2 | TG-04; no extension of earlier approvals |
| SKL-SR-28: existing Plan assets; SKL-SR-29: specialist interfaces | M2 for Plan; M1 and M3–M6 for the applicable specialists | TG-04, TG-05 |
| SKL-DEC-06/07: bounded pilot, complete inventory, local recording references | M1 realization; remaining scope M2–M6 | TG-01–05 |
| Assessment RC-SR-02/04/06/11–18: independent review, recording, reliance and final closeout | Each milestone handoff and final checkpoint | Current milestone judgments, TG-FINAL-01/02, distinct Verify |
| Constitution cleanup and Validation changed-set coverage | M1 evidence provenance reconciliation; every subsequent milestone's actual changed set | TG-06 and local selector checks |

The Skill Design's eight acceptance dimensions are allocated as follows. These preserve its existing scenario scope; they are not an exhaustive test whitelist.

| Design dimension | Earliest proof and integrated follow-through |
| --- | --- |
| Input domain | M1/TG-02: isolated, planned, manual and governed paths; M2–M6/TG-04 for family-specific applicability. |
| State/lifecycle | M1/TG-02: no inferred planned/armed state; M3/TG-04 and TG-FINAL-01: milestone versus final review and Verify. |
| Identity/authority | M1/TG-01/02: exact basis, independent reviewer and preservation; M4/TG-04: repair/write authority. |
| Composition/path | M1/TG-03/05: selected references, assets and readers; TG-FINAL-01/02: handoff and full package. |
| Temporal/retry | M1/TG-02/03: late trigger, stale source/revision and retry guidance; TG-FINAL-01: producer/consumer agreement. |
| Failure/recovery | M1/TG-02/03: unavailable procedure and rejected/interrupted recording; M4/TG-04: specialist recovery. |
| Compatibility/migration | M1/TG-01/03/06: coexistence and provenance; M2–M6/TG-04 and TG-FINAL-02: retained contracts and complete dispositions. |
| External/environment | M1/TG-05: supported temporary candidate packages; M3/TG-04: external authority; TG-FINAL-02: final package without internal checkout dependencies. |

## Milestones

All six milestones are implementation slices. Before starting each, require current Delivery approval, current applicable upstream authority and the previous milestone's independent clean review. The ordered sequence limits shared-validator conflicts and makes every intermediate candidate usable. If a family needs no source edits, its evidence and independent retention assessment still complete that allocated slice. Do not create empty implementation changes to satisfy the sequence.

### M1. Implement and Code Review pilot

- Milestone kind: implementation.
- Engineering purpose: establish the approved resource/layout change and trustworthy consumer validation before extending simplification.
- Requirements: SKL-SR-01–15, SKL-SR-24–27, SKL-SR-29–32; Constitution cleanup for advisory provenance.
- Architecture responsibility: SKL-DEC-06/07; Skill pilot realization and resource selection; Assessment retains review meaning.
- Dependencies: current approved delivery package; exact source baselines; supported local validation tools.
- Implementation scope: `implement`, `code-review`, their new recording references and directly affected checks/package consumers; inventory all 19 names and owners without claiming their full assessment.
- Files/components likely touched: `skills/implement/`, `skills/code-review/`, `scripts/lib/validation/skill_validation.py`, relevant helpers under `tests/skill/`, `tests/engineering/packaging/test-adapter-distribution.py` when its protection is affected, and this change's evidence/provenance surfaces.
- Required verification: TG-01, TG-02, TG-03, TG-05 and TG-06.
- Evidence expectations: exact before/after obligation destinations and read-path comparison; meaningful failing-before/passing-after validator cases; recorded candidate checks; retained non-pilot protection.
- Implementation steps: reconcile advisory provenance under TG-06; capture pilot baselines; add negative relocation/profile-selection proof; create `governed-implementation-recording.md` and `governed-code-review-recording.md`; simplify bodies under the selected equivalent; reconcile validators; check complete packages and handoff.
- Validation commands: V1 for `skills/implement/SKILL.md skills/code-review/SKILL.md`; V2; V3; V4 with both pilot skills; V5 for current records; V6 for the actual changed set.
- Expected observable result: core work is identifiable before recording detail; each recording/planned/armed trigger reaches its complete method independently; missing or misplaced procedure cannot bypass validation.
- Completion criteria: both pilot packages satisfy the approved outcome with no missing obligation, unusable path or unresolved in-scope correction; all directly affected consumers and required checks agree.
- Required evidence: registered `m1-*` evidence checks and independent `m1-code-review` with explicit pilot usability judgment, disposition of unfavorable/uncertain improvement and consumer coverage.
- Review handoff: actual pilot diff, complete packages, affected checks, provenance treatment and implement-to-review interaction; record before corrections.
- Optional commit boundary: `M1: Simplify implement and code-review with complete recording paths`.
- Risks: recording incorrectly nested under automation; heading removal disables checks; broad layout enforcement changes other skills.
- Rollback/recovery: restore the pilot body/reference/validator/test slice together to its recorded baseline, retain evidence of failure, and regenerate candidates. Preserve unrelated source and existing reviews; never rewind record files to manufacture approval.

### M2. Authoring and upstream reviews

- Milestone kind: implementation.
- Engineering purpose: reconcile the contiguous proposal-to-delivery authoring/review chain after the pilot's assessed result.
- Requirements: SKL-SR-01–30 and SKL-SR-32 under each requirement's existing applicability; SKL-SR-31 remains pilot-only.
- Architecture responsibility: Authoring and Assessment; existing proposal-family and Plan asset contracts.
- Dependencies: M1 clean review; each of the six specialist contracts and retained layout decisions.
- Implementation scope: `proposal`, `design`, `plan`, `proposal-review`, `design-review`, `delivery-review`; retain already-compliant content with reasons.
- Files/components likely touched: those six `skills/` directories and their actual structural/resource consumers in `scripts/lib/validation/` and `tests/skill/`; no new shared policy selected.
- Required verification: TG-01, TG-03 where consumers change, TG-04 and TG-05.
- Evidence expectations: six package dispositions, author/reviewer output and authority comparison, unchanged asset contracts or exact justified reconciliation, and current candidate checks.
- Implementation steps: inspect complete family packages; map redundant guidance to current owners; simplify within approved layouts; preserve conditional output groups and all asset metadata/fingerprints; check both ends of each author-to-review handoff.
- Validation commands: V1 for all six entrypoints; V2 when validator/helpers change; V3 for package consumer changes; V4 for changed family skills; V5 and V6.
- Expected observable result: direction, Design and delivery allocation remain distinguishable, with complete independent review and conditional recording paths and useful output structures.
- Completion criteria: all six packages have justified changes or retention, required obligations and proof remain intact, and any new layout/behavior decision has returned through its owning Design and review before reliance.
- Required evidence: registered `m2-*` checks and `m2-code-review`, including scope-specific retention or improvement rationale.
- Review handoff: entire family diff plus relied-on assets, methods, changed consumers and cross-skill outputs.
- Optional commit boundary: `M2: Simplify authoring and upstream review guidance`.
- Risks: turning structural assets into policy owners; importing the pilot equivalent without approval; authoring and review content drifting apart.
- Rollback/recovery: restore the affected author/reviewer package pair and its readers together; preserve unrelated pilot work and recorded findings.

### M3. Coordination, verification and external handoff

- Milestone kind: implementation.
- Engineering purpose: reconcile lifecycle consumers only after authoring and review interfaces are assessed.
- Requirements: SKL-SR-01–15, SKL-SR-24–27, SKL-SR-29/30/32; Workflow and Assessment closeout obligations.
- Architecture responsibility: Workflow, Assessment's Verify interface and Delivery Handoff.
- Dependencies: M2 clean review; M1 pilot packages; current routing/recording/verification contracts.
- Implementation scope: `route`, `verify`, `pr`; preserve existing automation support limits and all external-action prerequisites.
- Files/components likely touched: the three skill directories and directly affected structure/resource checks; CLI, record schemas and automation backend behavior remain unchanged.
- Required verification: TG-01, TG-03 where readers change, TG-04, TG-05 and the earliest TG-FINAL-01 assessment.
- Evidence expectations: isolated versus governed outcomes, milestone versus final whole-change review, successful Verify ownership, and preparation versus external mutation retain their distinctions.
- Implementation steps: consolidate repeated coordination/readiness guidance; preserve independently triggered resources, current record operations and unsupported-adapter stops; trace the M1/M2 outputs through route, final review, Verify and PR preparation.
- Validation commands: V1 for the three entrypoints; V2/V3 when their consumers change; V4 for changed skills; V5 and V6.
- Expected observable result: guidance is easier to follow without a shorter path granting lifecycle, automation, branch or external-action authority.
- Completion criteria: three dispositions and complete normal/denied/late-trigger handoffs; no conversion of evidence persistence into approval or continuation.
- Required evidence: registered `m3-*` checks, TG-FINAL-01 interim basis and `m3-code-review`.
- Review handoff: all three packages and interactions with approved authoring, implementation and review guidance.
- Optional commit boundary: `M3: Simplify coordination and final handoff guidance`.
- Risks: bypassing fresh final review; losing scoped Verify; treating generated or recorded state as external permission.
- Rollback/recovery: restore affected coordinator/consumer instructions and readers together; retain all prior package evidence and current authority limits.

### M4. Defect and CI repair

- Milestone kind: implementation.
- Engineering purpose: assess the two repair capabilities together while preserving their distinct diagnosis, proof and mutation boundaries.
- Requirements: SKL-SR-01–15, SKL-SR-24–27, SKL-SR-29/30/32.
- Architecture responsibility: Skill's Bugfix, CI maintenance and bounded PR CI repair contracts.
- Dependencies: M3 clean review and stable review/verification handoffs.
- Implementation scope: `bugfix` and `ci-maintenance`; no change to accepted production behavior, hosted platform state or privileged-action policy.
- Files/components likely touched: both skill directories and directly affected validators/tests/resources.
- Required verification: TG-01, TG-03 when applicable, TG-04 and TG-05.
- Evidence expectations: diagnose-only versus fix; supported cause and identity-equal proof; ordinary versus privileged CI work; concurrent/partial write and bounded PR repair limits remain explicit.
- Implementation steps: map each authority and failure obligation; simplify only duplicated or superseded instructions; keep proof feasibility, safe write primitives and recovery methods complete; reconcile actual consumers.
- Validation commands: V1 for both entrypoints; V2/V3 when relevant; V4 for changed skills; V5 and V6.
- Expected observable result: the user request and evidence determine the same allowed action and stop condition with clearer instructions.
- Completion criteria: both skill dispositions preserve all closed values, denial outcomes, proof requirements and correction ownership, with no speculative relaxation to shorten guidance.
- Required evidence: registered `m4-*` checks and `m4-code-review` with authority and failure-path rationale.
- Review handoff: complete repair packages, actual diff, tests and any affected handoff consumer.
- Optional commit boundary: `M4: Simplify defect and CI repair guidance`.
- Risks: removing a rare but required denial/recovery rule; confusing CI review with authorized mutation.
- Rollback/recovery: restore each complete repair package and affected checks; preserve failing proof and refer unclear behavior to its owner.

### M5. Project foundations

- Milestone kind: implementation.
- Engineering purpose: simplify standing-artifact and orientation guidance without changing their distinct source-of-truth roles.
- Requirements: SKL-SR-01–15, SKL-SR-24–27, SKL-SR-29/30/32.
- Architecture responsibility: Project Foundations and its Vision, Constitution and Project Map children.
- Dependencies: M4 clean review; relevant foundation contracts.
- Implementation scope: `vision`, `constitution`, `project-map`; no change to this repository's vision, governing principles or observed architecture merely to demonstrate the skills.
- Files/components likely touched: those three skill directories and their current validators/resources.
- Required verification: TG-01, TG-03 when applicable, TG-04 and TG-05.
- Evidence expectations: canonical vision/derived README ownership, constitution authority, map freshness and bounded inference, exact output shape and partial-operation recovery survive.
- Implementation steps: inspect whole packages; remove repeated navigation/instructions within current layouts; preserve structural output aids and project-selected paths; assess no-change cases explicitly.
- Validation commands: V1 for all three entrypoints; V2/V3 when relevant; V4 for changed skills; V5 and V6.
- Expected observable result: each skill exposes its own artifact and limits without implying that orientation or installation adopts project policy.
- Completion criteria: three complete dispositions, with current output and source-preservation obligations proved or independently assessed.
- Required evidence: registered `m5-*` checks and `m5-code-review`.
- Review handoff: foundation packages and affected output/resource contracts.
- Optional commit boundary: `M5: Simplify project foundation guidance`.
- Risks: substituting prescribed architecture for observed orientation; losing canonical-source or recovery details.
- Rollback/recovery: restore affected package and checks together, retaining user artifacts and evidence; no regeneration of unrelated project documents.

### M6. Discovery, learning and inventory reconciliation

- Milestone kind: implementation.
- Engineering purpose: complete optional support families and reconcile the initiative's full inventory before final assessment.
- Requirements: SKL-SR-01–15, SKL-SR-24–27, SKL-SR-29/30/32.
- Architecture responsibility: Discovery, Learning and Skill inventory ownership; final full-inventory preservation under SKL-DEC-06.
- Dependencies: M5 clean review and all preceding family dispositions.
- Implementation scope: `explore`, `research`, `learn`; reconcile FU-015–018 through their existing owners using actual accepted evidence, without declaring unrelated consolidation complete.
- Files/components likely touched: the three skill directories, directly affected consumers, registered evidence and `docs/follow-ups.md` only for supported disposition/navigation updates.
- Required verification: TG-01, TG-03 where applicable, TG-04, TG-05 and TG-FINAL-02; refresh TG-FINAL-01 where later changes affect its basis.
- Evidence expectations: optional triggers, attribution/confidence, discovery-to-owner handoff and confirmed lesson adoption remain complete; all 19 skills have one accepted disposition and no hidden remainder.
- Implementation steps: simplify or retain each support package; preserve shared discovery source and consumer parity; reconcile all milestone evidence; generate the final supported candidates and hand the complete result to final review after milestone assessment.
- Validation commands: V1 for all canonical skills; V2/V3 if changed protection needs fresh proof; V4 for the full inventory; V5 and V6.
- Expected observable result: useful optional support remains optional, and every published capability is accounted for without declaring the pilot universally conformant.
- Completion criteria: all three support packages and the full inventory meet their obligations; same-slice defects and required consumer work are resolved before review; no later cleanup is needed for completeness.
- Required evidence: registered `m6-*` and integrated checks, plus `m6-code-review`; final whole-change review is separately required below.
- Review handoff: support packages, aggregate inventory dispositions, actual full candidate evidence and any remaining limitation requiring owner resolution.
- Optional commit boundary: `M6: Simplify discovery and learning and reconcile the skill inventory`.
- Risks: creating a mandatory discovery stage; converting a learning suggestion into adopted policy; treating a count of 19 as semantic completion.
- Rollback/recovery: restore affected support packages/consumers and reopen their evidence applicability; retain earlier accepted work and expose any lost full-inventory claim.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all six implementation milestones and required corrections complete, with their required independent reviews and integrated proof.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change, all 19 dispositions, changed validators/resources and cross-milestone interactions.
- Evidence: exact final subjects, concrete nonauthor reviewer separation, one judgment, supported findings or no-finding rationale and current concern dispositions.
- Successor: distinct final Verify of the complete chain; only successful Verify records final explanation/completion evidence. Corrections return to their owner and require affected reassessment and a current integrated final judgment.

This checkpoint applies even if some skills are retained unchanged. Integration checks, milestone reviews and verification-group non-applicability cannot substitute for it.

## Change-level verification

### TG-FINAL-01. Complete workflow handoff and authority preservation

- Covers: SKL-SR-04/24–27/30–32; M1–M3 and any later changed consumer; Assessment RC-SR-11–18.
- Demonstrate: follow the revised authoring-to-review-to-plan-to-implementation-to-review-to-Verify guidance through representative isolated and governed paths. Confirm recording is independently triggered, manual work does not arm automation, review does not mutate the author's subject or routing, a final milestone cannot replace final whole-change review, and missing/conflicting proof prevents the corresponding claim.
- Evidence expectations: independent instruction inspection at M3, refreshed against final affected subjects after M6. Use each producer's actual output structure as the next consumer's input; identify the first point where a missing field, unsupported assumption or stale identity would stop work. This is semantic package assessment, not a claim to have executed a customer workflow.
- Non-applicability: not applicable; no individual milestone alone proves this complete chain. Execute additional focused manual scenarios only if material uncertainty remains, with the explicit basis below.

### TG-FINAL-02. Complete inventory and supported package composition

- Covers: SKL-SR-08–15/30/32; M1–M6, Packaging's current resource-integrity boundary and Constitution cleanup.
- Demonstrate: every canonical skill appears once in the inventory and has reviewed improvement or retention evidence; final Codex and Claude candidates contain all required resources and current shared projections, including untriggered files. The pilot's structure/recording selection has not imposed a new layout on other skills. No current reliance needs an unclassified advisory file or retired instruction source.
- Evidence expectations: final inventory-to-evidence reconciliation; V1 across `skills/`; V4 on a fresh final candidate with all skills; V5/V6; independent review of the complete subject set. Record paths, candidate identities, actual commands, observations and applicable limitations in registered evidence.
- Non-applicability: not applicable; combined inventory, overlapping shared consumers and final package identities require change-level assessment.

## Validation plan

### Verification groups and evidence method

| Group | Required observation and proof boundary |
| --- | --- |
| TG-01 | A skill/obligation destination exists under the right owner and retains applicability. Compare exact source groups to revised package or justify retention; all 19 names need substantive dispositions. Record contributor rationale and independent assessment, not a new machine-scored ledger. |
| TG-02 | The pilot's core task is understandable before recording construction. Independently inspect isolated, planned, armed, manual-recording and late-trigger paths, plus absent/stale/conflicting authority and unsupported adapters. Required recording/recovery instructions retain revision/read identity, targeted operations, no false save/approval and preservation of neighboring records. Existing CLI regression proof supports executable persistence; instruction inspection establishes the mapping to those commands. |
| TG-03 | Relevant structural validators detect missing/unmapped/escaped/unreadable/wrong/stale resources and unsupported closed selectors after relocation, including a removed body heading. Add meaningful negative tests before changing the reader when feasible; verify they fail on the intended defect and pass after correction. Preserve actual non-pilot checks and useful existing tests. |
| TG-04 | Each family's actual instructions preserve its specialist outcomes, conditional evidence, output shapes, handoff, failure handling and authority. Independent before/after inspection explains a concrete improvement or retention and assesses full selected paths. M2 covers author/review pairing; M3 readiness/external limits; M4 identity/proof/recovery; M5 source-of-truth/orientation; M6 optional support and lesson adoption. |
| TG-05 | Actual generated archives and temporary installed packages retain inventory, resource paths and raw-byte parity under both supported adapters. Pair body selection with required transitive references/assets; check changed shared sources against every declared consumer if an owned correction requires such a change. |
| TG-06 | Resolve the validation placement of `docs/reviews/2026-09-15-skill-simplification-proposal-review.md` before a whole-branch claim. Preserve its original bytes in a scoped baseline commit before any retirement; retain exact commit/path provenance in registered evidence. Formal reviews replace current reliance. Remove that unclassified working-tree artifact only after confirming recoverability and reconciling live links/readers. Do not rewrite the advisory judgment as formal approval, add a catch-all selector exemption, or delete uncommitted evidence. If current reliance requires retaining it, return the exact placement decision to its existing owner before dependent completion. |

For semantic TG-01/02/04 and TG-FINAL-01, the reviewer is an independent nonauthor using the actual package and current project authority. The bounded action is to trace the declared representative path, check each required instruction and resulting artifact/handoff, and record expectation, observation and limits in the normal review. Deterministic structure checks cannot judge instruction meaning or usability. Changed instructions, resources, governance or relevant evidence invalidate reuse for the affected claim. A material unresolved scenario needs an explicit starting state, bounded action, expected result, observed artifacts and freshness limits in existing evidence; no blanket live-agent benchmark is selected.

### Repository-owned commands

Run the smallest relevant command first, then complete every selected or plan-required check. The following are exact command forms; replace skill paths only with the milestone's named targets.

| ID | Command and use |
| --- | --- |
| V1 | `python scripts/validate-skills.py skills/implement/SKILL.md skills/code-review/SKILL.md` for M1; use the exact named family entrypoints for M2–M5 and `python scripts/validate-skills.py skills` for M6/final. Checks structure, resources and the applicable current contract. |
| V2 | `python tests/skill/test-skill-validator.py` for changed validator/helper protection; once sufficient focused cases pass, complete this suite for the affected reader change. |
| V3 | `python tests/engineering/packaging/test-adapter-distribution.py` for changed packaging consumers. Existing unchanged reader proof may be reused only with explicit current unaffected-basis reasoning. |
| V4 | Run the candidate commands below for every milestone that changes a published package and again on the final combined candidate. A retention-only milestone can reuse an unchanged candidate with justified applicability. |
| V5 | `node scripts/validate-record-store.mjs docs/changes/2026-09-15-skill-simplification/change.json` after required recording; this checks structure/references, not engineering approval. |
| V6 | `bash scripts/ci.sh --mode local` against the actual changed set, including moves/deletions. Use `bash scripts/ci.sh --mode explicit --path PATH` for focused iteration, substituting each actual changed path. Unclassified paths or missing prerequisites require resolution; an explicit subset cannot establish complete local readiness. |

Candidate commands use an owned temporary output directory and the same local qualification label for build and validation; `v1.0.0` is not a release declaration:

```bash
skill_candidate_dir="$(mktemp -d /tmp/rigorloop-skill-candidate.XXXXXX)"
python scripts/build-adapters.py --version v1.0.0 --output-dir "$skill_candidate_dir"
python scripts/validate-adapters.py --version v1.0.0 --adapter-root "$skill_candidate_dir" --clean-install-smoke --skill implement --skill code-review
```

For M2–M5, select the changed family with repeated `--skill` arguments. For M6/final, omit `--skill` to assess all installed packages. Record the owned output path and archive identities, retain evidence needed for reliance, then clean only those owned temporary outputs under the repository cleanup policy. Never generate into authored or active installation roots.

The local selector owns any applicable additional CLI, model, schema and regression commands. In M1 it must retain recording/resource rejection protection while the instructions move; do not invent new CLI behavior tests for an unchanged CLI. No timing stress test is required merely for a wording change: existing deterministic persistence tests and instruction-to-command inspection address the preserved retry/recovery contract. Required fresh proof or new material uncertainty overrides reuse.

## Risks and recovery

- Shorter text can hide obligations or increase unnecessary indirection. Restore the relevant complete instructions or retain the original package; a passing structure check is insufficient to close the milestone.
- Shared-reader changes can affect skills outside the current family. Inspect the declared consumer set, validate all affected paths, and include required consumer corrections in the same slice. A new policy/architecture decision returns to Design; materially changed milestone scope requires reviewed replanning.
- New skill-local references may be missing from a candidate or installed tree. Restore the complete body/reference/reader slice, regenerate and recheck the same boundary; do not patch generated output by hand.
- Advisory provenance and other record-only changes can be unclassified by whole changed-set validation. TG-06 resolves the known advisory surface using existing cleanup authority; unknown new evidence placement remains an explicit owner issue, never a Markdown-wide exemption.
- Stale or conflicting record writes require fresh scoped reads and reassessment; preserve partial evidence and use only the CLI's supported recovery. Rollback cannot restore reviewer applicability automatically.

## Dependencies

- The exact proposal, Design and Delivery review subjects must remain current before implementation. Plan initialization adds missing work only after current Delivery approval and only if work is absent; subsequent work decisions belong to Route.
- M1 → M2 → M3 → M4 → M5 → M6, with independent milestone review between slices. This ordering controls shared-resource/validator overlap; it does not make discovery mandatory in customer workflows.
- Structural negative cases precede relevant reader changes where feasible; complete package proof accompanies each changed family. Full integration and whole-change review follow all required implementation/corrections, then distinct Verify.
- Preserve the approved Design scope: a new layout/resource architecture beyond its existing equivalents returns to the owner before implementation. Unassessed work stays allocated here; a blocked family is not silently removed from the inventory goal.
- Git commits preserve explicit implementation boundaries and advisory provenance. Remote Git, PR, release and installation actions require their separately applicable authority.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-15 | Deliver the pilot first, followed by five complete capability families. | The pilot establishes resource/reader treatment; coherent families preserve meaningful handoffs and keep the 19-skill commitment explicit. | One global rewrite hides specialist differences; pilot-only completion drops scope; one milestone per file adds ceremony without a distinct boundary. |
| 2026-09-15 | Reconcile package and validator consumers within each changed family. | Every intermediate candidate must be complete and reviewable. | Deferring consumer fixes to final closeout leaves broken packages and invalid milestone evidence. |
| 2026-09-15 | Use independent instruction assessment for meaning and automated tests for executable structure/persistence. | These observe different failure boundaries under Validation TEST-SR-15/16. | Token counts, literal wording freezes and a new runtime compliance harness do not establish the required improvement. |
| 2026-09-15 | Preserve advisory bytes in Git before retiring their unclassified live path once formal records own reliance. | Existing cleanup authority can reconcile provenance without changing validation policy or rewriting judgment. | Deleting uncommitted evidence loses history; retaining a new catch-all exception hides incomplete changed-set coverage. |

## Readiness

- See the owning change record for current workflow state.
- Remaining completion gates: independent Delivery Review, approved-plan work initialization, each implementation milestone and its independent review, required integration proof, fresh final whole-change Code Review and distinct successful Verify. This plan establishes none of those outcomes by existing.
