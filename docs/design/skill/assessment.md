# Review and Closeout

Model validation contract: model-document-v1

[Reviews and verification (MOD-007)](../../../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/module.json) owns independent assessment and completion meaning within [Governance](../../../design/architecture/modules/MOD-017-engineering-governance/README.md). [Workflow](workflow.md) owns progression. [Records](../cli/records.md) represents supplied judgments; persistence and schema validation never supply approval.

## Distinct assessments

| Assessment | Question and basis |
| --- | --- |
| Requirement Review | Is the proposed IR/SR basis, including reuse conclusions and supporting Feature/Scenario analysis, justified, scoped and assessable? |
| Integrated Design Review | Do logical Functions, accountable Modules, Interfaces, AR allocations and material realization coherently satisfy the accepted requirement basis? |
| Delivery Review | Can the plan's sequencing, dependencies, completion conditions, proof and recovery deliver the reviewed scope? |
| Whole-change Code Review | Is the complete actual delivery acceptable against accepted requirements, reviewed design and delivery intent, including interactions? |
| Final Verify | Do current evidence, applicable independent reviews and completed work justify the final completion claim? |

A reviewer must not author the assessed correction and then claim independent approval. Record actual assessor/contributor attribution and the independence basis; a role label alone is not proof. Review covers relevant code, tests, configuration, migrations, generated outputs, public instructions and documentation. Missing required evidence or material uncertainty cannot become a clean outcome by omission.

## Findings and corrections

Record material findings with concrete evidence, affected scope, the required outcome and accountable owner or explicit decision need. Distinguish a reproduced defect, a supported risk and an uncertain question. Open findings and blockers survive omission and a later clean assessment until explicitly resolved, withdrawn or deferred with accountable follow-up. Advisory findings remain meaningful even though their review cannot approve a gate.

Return corrections to their actual owner. Reassess the corrections and affected interactions while retaining adequate coverage of the complete current result. Do not automatically reread every unchanged file or rerun every unaffected test. Broad changes or uncertain impact may justify broader reassessment. Several attempts can occur within one whole-change gate; milestones require no approval cycle.

## Scope, applicability and support

Every relied-upon judgment identifies its actual assessed subjects, governing basis, conclusion, rationale and limitations. Preserve the distinction between original meaning and current applicability. Reported applicability is an accountable actor's claim; a compared observation establishes only the explicitly compared scope. A timestamp, commit ID, successful save or newly prepared candidate does not silently extend an earlier approval.

Replacing comparable Evidence may update the current account. Preserve the concise assessed support still needed to explain a retained judgment; detailed payloads are selective. Missing retained bytes must be exposed as limitations and cannot support new claims of availability. Later adverse evidence or a changed assessment remains recordable, while dependent reliance becomes visibly uncertain. A recorded accepted Basis retains its original acceptance decision when current support is lost; new acceptance and final-success reliance require current compatible support.

Pure bookkeeping does not automatically restart review. Changes that alter an obligation, outcome, source meaning or support require an explicit applicability disposition and, where needed, independent reassessment. Review preparation and context are reads/construction, not approval. The CLI checks structural prerequisites; the accountable actor judges engineering adequacy.

## Final verification and completion

Final Verify remains distinct from Code Review and authoring. It requires the current mandatory requirement/design/delivery/whole-change review basis, completed implementation, meaningful checks and explicit issue dispositions. Verify does not repair code and independently approve that repair itself.

Implementation defects return to implementation and applicable independent reassessment before renewed Verify. Requirement or design defects return upstream. An evidence-collection retry that changes no engineering subjects does not alone create another Code Review; contradictory new evidence must still be assessed for its effect on prior reliance.

Only a supplied successful final Verification with current support can justify `change complete`. Saving Verify does not itself close the Change. Completion retains delivered scope, reason, accepted basis, actual supporting review/Verify conclusions, limitations and selected attachments. It is a historical claim, not continuing health monitoring. Later regressions are new linked work. Explicit notes may correct an account without silently rewriting its original meaning.

## External handoff

PR preparation checks the actual delivered diff and applicability of its review/Verify basis against the refreshed repository state. Operational evidence recording does not automatically invalidate engineering approval, but cannot cover new engineering changes. PR submission needs applicable user authority and does not imply merge/release authority. Local validation cannot establish hosted CI success.

## Historical provenance

Earlier fixed dossier, milestone-gate and v3 record-preservation procedures are recoverable at commit `39be9c81`, path `docs/design/skill/assessment.md`. Their assessments retain their original meaning; the current contract does not relabel them as new approvals.

## Requirements

These stable local references reconcile the prior document contract with the current REM and Module owners linked above. They do not retain the superseded workflow or filesystem interface.

| ID | Required behavior |
| --- | --- |
| RC-SR-01 | Assessments MUST identify kind, actual scope, subjects, governing basis and limitations. Requirement, integrated Design, Delivery, advisory, whole-change Code Review and final Verify remain distinct; optional advice carries no lifecycle approval. |
| RC-SR-02 | Approval requiring independent review MUST come from a reviewer who did not author the reviewed contribution. The review MUST identify actual contributors and concrete separation evidence. A role label, a new turn of the author, passing validation, or the author's self-assessment MUST NOT establish independence. Missing separation evidence blocks reliance on approval while preserving any independently supported findings. |
| RC-SR-03 | A reviewer MUST assess the identified subject using the specialist method and record one justified judgment with its basis and limitations. The reviewer MUST apply the ordered combined-condition rule below to the required assessment scope: necessary authority or owner-decision impediments take precedence, then materially insufficient assessment basis, then required actionable corrections, then approval. Supported material findings MUST remain visible under every judgment. Optional improvement notes MUST NOT cause non-approval unless their evidence establishes an unmet governing requirement or decision criterion. These are reviewer decisions, not CLI selection or recording prerequisites. |
| RC-SR-04 | A required formal judgment MUST be durably recorded against its actual subjects before downstream reliance. Recording success, judgment, applicability, and continuation MUST remain separate conclusions. Failed or unsafe recording blocks reliance on an unrecorded approval; it MUST NOT erase the assessment or justify inventing a successful save. Record shapes and transport remain contract-selected. |
| RC-SR-05 | Before relying on an assessment or proof, the receiving actor MUST check its required current basis, scope, independence where required, applicable concerns, and relevant new evidence. Unknown, missing, stale, contradictory, or omitted required basis blocks reliance and requires explicit inspection, reassessment, or an owned blocker. Matching identities alone MUST NOT establish applicability; a retained old judgment MUST NOT silently acquire a revised subject. |
| RC-SR-06 | An author changing engineering work MUST identify affected assessments and proof, declare impact and applicability restrictions, and identify outstanding correction needs before downstream reliance. Revised engineering subjects require the appropriate independent reassessment. Any responsible actor may conservatively restrict applicability with an impact rationale. The responsible assessor decides renewed applicability; an author or route actor MUST NOT restore another actor's approval. Ambiguous or concurrent impact requires an owned blocker rather than assumption. |
| RC-SR-07 | A recording-only change MUST NOT automatically invalidate an engineering assessment solely because storage bytes or the record revision changed. The receiving assessor MUST classify the actual content and effect: altered engineering subjects, changed claim scope, new contradictory evidence, or material concerns require assessment under RC-SR-05/06. Original reviewed identities MUST remain truthful; bookkeeping classification MUST NOT retarget an old judgment or waive CLI conflict checks. |
| RC-SR-08 | Actionable findings and blockers MUST retain stable identity, reporter, meaningful basis, required outcome and correction owner. Omission or a later clean review MUST NOT dispose unresolved concerns; current accounts may be refined explicitly. |
| RC-SR-09 | The reporter owns concern-disposition assessment; the correction owner performs the repair. A disposition MUST state its justification, relevant proof, and any authorized residual risk or follow-up. Deferral MUST identify an authorized decision, accountable owner, tracked follow-up, and why it does not defeat a required acceptance condition; it MUST NOT waive mandatory final Code Review or other non-waivable obligations. A reviewer MUST NOT close another actor's blocker merely by approving corrected work. |
| RC-SR-10 | Corrections MUST return to the activity that owns the faulty subject or decision. A reviewer MUST record its finding before review-driven edits and MUST NOT edit and approve the same contribution. Returning corrected work means review-ready, not approved. Targeted reassessment may resolve a bounded finding, but affected package judgments and the final whole-change assessment MUST still be adequate and current before reliance. Workflow owns selection and recording of the correction destination. |
| RC-SR-11 | Successful final Verify MUST depend on one independent whole-change Code Review gate after complete implementation and required corrections. Optional interim advice may inform it but never substitutes. Reassessment remains within the same gate; milestones require no approval. |
| RC-SR-12 | Planning MUST allocate the complete implementation, required local/integrated checks, one whole-change review checkpoint and distinct Verify. Delivery Review MUST reject substituting milestone approval for whole-change adequacy. |
| RC-SR-13 | Final Verify MUST independently assess evidence/coherence in its distinct role and establish that the required requirement, design, delivery, implementation, review, correction, and proof obligations are satisfied on their current applicable basis. It MUST confirm RC-SR-11 and justified concern dispositions, assess affected authoritative and generated surfaces, and produce the final explanation and completion evidence only on success. It MUST NOT substitute its inspection for missing Code Review, use an unapproved self-authored correction as proof, or claim release/PR/external-action authority. |
| RC-SR-14 | Defects and contradictory evidence MUST remain recordable. Failed Verify MUST record its actual result and owned correction path. After completion, regressions are linked new work; errors in the original conclusion receive explicit notes rather than continuous applicability tracking. |
| RC-SR-15 | Required evidence MUST be sufficient and applicable to the current claim; new assessment does not by itself require every validation command to rerun. The assessor MUST identify which results remain usable and why: reuse requires an existing pass, known proved surfaces, current governing authority and subject/environment identity, affirmative unaffected evidence for those surfaces, and no freshness override. It MUST require new proof where subject, environment, procedure, dependency, or evidence changes defeat that basis. An explicitly required fresh execution or current-state check overrides ordinary reuse reasoning; a cache hit or execution label alone MUST NOT count as that proof. For a record containing multiple checks, an actor MUST restrict record-level applicability when a changed check defeats reliance and identify the affected scope; receiving assessors MUST inspect the individual results and subjects rather than infer universal success from record-level current. Test success MUST NOT substitute for independent engineering review, and a fresh review MUST NOT silently refresh stale test evidence. |
| RC-SR-16 | Adoption MUST map every affected shared policy clause to one retained or replacement owner, retain stable reference identities or explicit replacement mappings, and preserve historical records under their exact contracts. Old approvals MUST NOT be retargeted or reinterpreted as approval of this design. Conflicting historical/new authority blocks reliance until an authorized owner resolves it; no automatic migration or historical supersession is introduced. |
| RC-SR-17 | Consumer alignment MUST preserve specialist reasoning, sufficient evidence, truthful scope/consequence, and standalone invocation limits while removing duplicate normative ownership. Packaged guidance MUST be usable without this internal Design repository, load only the relevant assessment method and triggered resources, and have traceability to these requirements. Templates and examples MUST illustrate the same contract rather than introduce exceptions. No token-saving claim is justified without measurement. |
| RC-SR-18 | Assessment and closeout decisions MUST remain understandable from current authoritative project artifacts without Git history, PR access, network access, or prior chat. Missing runtime independence provenance, inaccessible required subjects, interrupted recording, or incompatible installed guidance MUST result in a bounded stop with a responsible next action. Local/runtime permissions and separately authorized external actions MUST remain independent of any recorded review or completion. |
| RC-SR-19 | The responsible assessor MUST judge whether an explanation edit preserves the same assessment or changes its supported reliance. A successful narrow edit MUST NOT restore applicability, establish independent review, rerun evidence or authorize continuation. Materially changed scope, newly missing basis or contradictory evidence requires explicit applicability/correction decisions; changed judgment, exact subjects, actors or evidence basis requires complete reassessment. |
| RC-SR-20 | PR readiness MUST identify the actual current cumulative delivery diff, branch and remote relation and adequate applicable review/Verify support. Non-Git engineering completion MUST NOT require Git fields. |
| RC-SR-21 | Historical assessments retain original meaning. New successor approval MUST use the current requirement-first contract and attributable assessment; import or installation MUST NOT promote old judgments. |
| RC-SR-22 | Verify MUST distinguish scoped checks from final completion and report actual execution and limitations. Successful scoped evidence does not establish final readiness. |
| RC-SR-23 | Later changes require a proportionate explicit reliance assessment before external handoff. Bookkeeping alone need not restart review; material changes, contradictions and unknown impact block renewed reliance until resolved. |

### Boundary scan and acceptance scenarios

| Dimension | Requirement basis | Distinct outcome to demonstrate |
| --- | --- | --- |
| Input domain | RC-SR-01 | Unknown contracts, malformed references or unsupported scope stop the affected operation without inferred defaults. |
| State/lifecycle | RC-SR-01 | Progress, accepted basis, review judgment, final Verify and historical completion remain distinct; saved state alone advances none. |
| Identity/authority | RC-SR-01 | The actual responsible actor, declared scope and current support govern reliance; an identifier or role label does not establish authority. |
| Composition/path | RC-SR-01 | Changed producer and consumer contracts are reconciled together, including packaged conditional resources and referenced engineering definitions. |
| Temporal/retry | RC-SR-01 | A changed basis requires rereading and proportionate reassessment; an old submission does not acquire current authority on retry. |
| Failure/recovery | RC-SR-01 | Interrupted work exposes its actual outcome and an owned next step without erasing unresolved issues or inventing success. |
| Compatibility/migration | RC-SR-01 | Retired procedures remain historical; successor behavior requires explicit applicable adoption/import and cannot relabel old approval. |
| External/environment | RC-SR-01 | Local engineering results remain separate from installed, published or hosted outcomes; required observations must actually be made. |

## Test design

Inspect the current responsibilities and boundary scenarios against the owning REM model and Module contract. Structural checks establish format only; independent review judges semantic coverage. Runtime record behavior is exercised by the package’s operational store, update, reliance, review and maintenance tests; skill guidance is assessed in actual generated archives with the resource validator and independent scenario inspection. Required combined and negative proof is allocated in the adoption plan.
