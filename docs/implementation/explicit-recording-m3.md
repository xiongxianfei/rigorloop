# Explicit Recording M3 — Isolated Implementation Evidence

## Authority and scope

The user authorized M3 after the clean advisory M2 Code Review. This permits the prospective workflow/model integration in the [delivery plan](../plans/2026-09-05-explicit-recording-and-model-centered-design.md), not ordinary activation, historical-contract conversion or new Design behavior. Profile: `IP0-isolated`. `rigorloop workflow-context` still reports `RL_CONTEXT_CHANGE_NOT_FOUND`; no registered milestone or automation state is inferred. Existing unrelated changes are preserved.

## Design dependency (historical preflight)

M3 requires TG-05 actor scenarios and TG-06 model/requirement verification mapping, including model-aware boundary validation. The [Workflow design](../design/workflow.md), Adoption support surfaces and completion check, explicitly requires model-scoped ownership and boundary/proof references to be defined before validator recognition changes. Its Boundary scan and Risks sections still identify this as unfinished Design reconciliation. The current [Design review](../reviews/explicit-recording-and-model-centered-design.md) resolves the external-edit guarantee, not this separate mapping obligation. The [Delivery review](../reviews/explicit-recording-and-model-centered-design-delivery.md) likewise retains the obligation and forbids defining new normative behavior through validator implementation.

The current validator only accepts top-level `specs/*.md` paths and expects the existing four-section feature boundary record. Both model documents instead contain eight concise scenario rows and explicitly disclaim equivalence to that record. Merely allowing `docs/design/` paths would neither define nor verify the model contract. Treating those rows as a replacement serialization without an author-owned decision would silently change the rule.

The smallest next step is a Design-owner clarification in the existing model documents: define how their existing requirement/scenario references map to validation and plan-owned proof, preserving one file per model. Independent Design assessment must precede dependent validator or skill changes. No extra Design files, OS investigation or storage work is needed. This evidence selects no new serialization, removes no proof obligation and does not reopen the resolved M2 concurrency decision.

## Preflight result (historical)

- Skill: implement
- Status: blocked
- Completed scope: M3 authority, dependency and validator preflight
- Artifacts changed: this implementation evidence only
- Tests added or updated: none; no production correction attempted
- Validation performed: `node packages/rigorloop/dist/bin/rigorloop.js workflow-context --change 2026-09-05-explicit-recording-and-model-centered-design --format json`; `python scripts/validate-boundary-first.py --check --path docs/design/workflow.md --path docs/design/cli.md`
- Validation result: context reports the absent registered change; boundary command exits 1 with two `BFR-INVALID-CHANGED-PATH` errors
- Open blockers: model-file boundary/reference contract remains explicitly unowned by implementation
- Next stage: blocked pending Workflow/CLI Design reconciliation and affected independent review
- Claim limitations: no M3 implementation completion, Code Review, activation, lifecycle settlement, Verify, commit or push

## Current implementation basis

The user authorized the model-validation refinement, independent Design rereview and M3 resumption. The [current Design rereview](../reviews/explicit-recording-and-model-centered-design.md), Model-validation mapping section, resolved the preceding dependency. Implementation uses that reviewed two-model package, the existing advisory Delivery Review and M2 clean rereview. No formal lifecycle state is inferred or initialized. No project-map inference is needed; implementation follows the exact approved inventory and directly inspected sources.

Model-only document checks now dispatch separately from historical feature/activation validation. They require contained nonsymlink model paths, the explicit contract marker, exact table headings/columns, stable unique requirement IDs, each known dimension once, local references and reasoned non-applicability. Unknown vocabulary fails closed. A model-only public check works without activation/change records and reports `structure-and-references-only`; historical and mixed validation retain their activation checks. It never invokes the recorder or writes status.

Eleven stage entrypoints have concise prospective profiles with model-owned record/field responsibilities, explicit identity-based recording, independent review, stale-evidence handling and success-only Verify. Model documents supply record shapes and validation mapping; historical shape/transition resources are not loaded as new-contract prerequisites. Existing substantive stage duties, permissions and proof remain. Governance adds scoped prospective text rather than replacing active historical rules. Ordinary activation remains disabled.

### Exact inventory and retained surfaces

| Approved scope | Implemented surfaces | Retained surfaces and rationale |
| --- | --- | --- |
| WF-MAP-01/10 | `CONSTITUTION.md`, `AGENTS.md` | Historical precedence and lifecycle rules remain outside the isolated profile. |
| WF-MAP-02–06 | `specs/rigorloop-workflow.md`, `specs/compact-current-state-change-record.md` | Historical schemas, semantic handlers, records and prior findings remain untouched; no conversion. |
| WF-MAP-07 | `docs/architecture/system/architecture.md`, Source of truth | Unrelated architecture, ADRs and historical runtime flow remain readable; no new architecture sidecar. |
| WF-MAP-08/09 and stage consumers | `skills/architecture/SKILL.md`, `skills/spec/SKILL.md`, `skills/route/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, `skills/design-review/SKILL.md`, `skills/plan/SKILL.md`, `skills/delivery-review/SKILL.md`, `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, `skills/verify/SKILL.md` | Existing references/assets retain historical procedures and generic engineering methods. New profiles use project model contracts for shapes, rather than adding or loading historical package/transition scaffolds. No new resource chains or public skill are introduced. Support skills retain their own artifact duties; prospective governance covers their actor-owned blocker/evidence obligations without arming automation. |
| Adoption support / TG-06 | `specs/skill-contract.md`, `specs/boundary-first-proof-model.md`, `scripts/boundary_first_validation.py`, `scripts/validate-boundary-first.py`, `scripts/test-boundary-first-validation.py`, `scripts/test-skill-validator.py` | Historical boundary reference projections and skill validator stay unchanged; no new resource shape requires changing their validation. Model interpretation is a separate explicit path, not a widened historical parser. |
| TG-05 | `packages/rigorloop/test/record-store-workflow.test.js` | Uses the unchanged M2 dispatcher fixture and storage modules. Simulated roles are not actual reviewer provenance. |
| M4-only integration | None in this slice | Public contract/command registration, workflow-context activation metadata, scaffolds, generated public adapters, support manifest, CI selection/cutover and rollback agreement remain M4. Temporary skill generation is checked here; no installed mirror or public archive is hand-edited. |

### Requirement-to-check mapping

The stable plan owns allocation. This implementation evidence names concrete proof for that allocation without moving design truth or current progress into the plan. TG-01/02 cases are in `record-store-contract.test.js`, TG-03/04 in `record-store-cli.test.js`, TG-05 in `record-store-workflow.test.js` plus the independent walkthrough, and TG-06 in `ModelRecordTests` and `ExplicitRecordingGuidanceTests`. Later-stage allocations are explicitly not claimed complete.

| Requirement | Concrete allocation/proof |
| --- | --- |
| WF-SR-01 | TG-05 exact actor replacements; inspect/save leave activity unchanged unless supplied. |
| WF-SR-02 | TG-01 all record representations; TG-05 current subjects, activity, registry and blockers. |
| WF-SR-03 | TG-05 attribution validator case plus independent walkthrough of same-contributor review; role text cannot establish separation. |
| WF-SR-04 | TG-05 model drift, explicit stale applicability and route-selected correction owner. |
| WF-SR-05 | TG-05 Verify-originated blocker and failed evidence with absent success report. |
| WF-SR-06 | TG-05 completed-owner reopening, retained blocker and review on correction return. |
| WF-SR-07 | TG-06 current model paths/tables and canonical profile reachability; independent cross-model walkthrough. |
| WF-SR-08 | TG-05 two exact model subjects, retained old review bytes and reassessment; TG-06 stable local ID/reference validation. |
| WF-SR-09 | TG-05 explicit final Verify replacement and stale-evidence refusal in walkthrough; later complete-change readiness remains TG-FINAL-01. |
| WF-SR-10 | TG-02 historical rejection and TG-06 unchanged historical boundary tests; full adoption TG-07/TG-FINAL-02 remain M4. |
| CLI-SR-01 | TG-03 read-only inspect/check; TG-05 drift observation without activity mutation. |
| CLI-SR-02 | TG-01 closed vocabulary/reference cases; TG-03 malformed argument and safe rejection cases. |
| CLI-SR-03 | TG-05 asserts exact submitted bytes after every save; TG-03 preserves unnamed files. |
| CLI-SR-04 | TG-04 revision/read/write checks and competing subprocess; TG-05 declares current model read identities. |
| CLI-SR-05 | TG-04 mixed snapshot rejection and interrupted multi-record publication. |
| CLI-SR-06 | TG-04 explicit complete/restore, observed third-state stops and committed rollback refusal. |
| CLI-SR-07 | TG-05 old subject drift and stale applicability remain separate from storage rejection. |
| CLI-SR-08 | TG-04 stale retry and refreshed identical request; no incremental workflow operation. |
| CLI-SR-09 | TG-03 unsafe targets; ER-M2-004 five sibling late-parent tests. |
| CLI-SR-10 | TG-02/03 historical/new contract separation; final integrated cutover remains TG-07/TG-FINAL-02. |
| CLI-SR-11 | TG-03 text/JSON dispatcher, truthful selector errors and safe diagnostics. |

### Scenario-row and combined-hazard mapping

Each cell uses the exact model path plus the existing dimension label; no new boundary ID series is introduced. TG-06 structural tests check all eight rows in each model, not their semantic adequacy.

| Dimension label | `docs/design/workflow.md` proof | `docs/design/cli.md` proof |
| --- | --- | --- |
| Input domain | TG-05 Verify blocker and incomplete/false independence walkthrough | TG-01 closed records and TG-03 exact replacements |
| State/lifecycle | TG-05 reopen completed owner | TG-05 explicit completion does not block later correction recording |
| Identity/authority | TG-05 retained subjects and same-contributor walkthrough | TG-04 stale identities and ER-M2-004 containment |
| Composition/path | TG-05 two model subjects and independent walkthrough | TG-03 dispatcher/helper and TG-04 recovery siblings |
| Temporal/retry | TG-05 retained review after model edit; walkthrough rejects replay | TG-04 live contender and lost-response retry |
| Failure/recovery | TG-05 Verify failure without success report | TG-04 interruption, restore/complete and mixed-state rejection |
| Compatibility/migration | TG-02 unchanged historical contract and TG-06 historical feature tests; integrated adoption M4 | TG-02/03 historical write refusal; integrated adoption M4 |
| External/environment | TG-05 fresh disposable root/records and independent walkthrough without Git/PR history | TG-03 safe errors, TG-04 observed external edits; final-window external-edit exclusion retained |

Workflow combined hazards (changed subject plus old approval, completed owner plus correction, and cross-model edits plus reliance) use TG-05 and the walkthrough. CLI combined hazards (stale review plus correction, competing writer plus basis drift, and partial commit plus retry/external edit) use TG-04/05. TG-FINAL-01/02 remain the later cross-milestone integration proof, not a substitute for this scoped coverage.

## Validation and independent handoff

Tests first: the seven new `ModelRecordTests` initially produced six failing assertions across four test methods because current models/markers were unrecognized and the public command demanded activation data. The prospective-guidance test initially failed for all eleven missing profiles. Both focused checks passed after implementation. The new public-recorder TG-05 scenario passed against the unchanged M2 runtime; it expands proof rather than correcting storage behavior.

The first full skill test run found two quick-guide placement failures caused by the added profiles. Their quick guides were moved earlier without changing semantics; the targeted placement/profile tests and full rerun now pass. No passing structural test substitutes for semantic review.

- `python scripts/validate-skills.py skills`: passes, 20 canonical skills.
- `python scripts/test-skill-validator.py`: final rerun passes, 366 tests.
- `python scripts/test-boundary-first-validation.py`: passes, 78 tests after ER-M3-001 correction.
- `python scripts/validate-boundary-first.py --check --path docs/design/workflow.md --path docs/design/cli.md`: passes, structure/reference-only.
- `npm --prefix packages/rigorloop test`: passes, 525 total / 523 passed / two existing skips / zero failures.
- `python scripts/build-skills.py --check`: passes again after quick-guide relocation, using disposable generated output.
- `node scripts/build-record-store-schema.mjs --check` and `git diff --check`: pass.

### Independent semantic walkthrough

Actor `/root/m3_walkthrough` was separately delegated a raw scenario and the canonical route, Design Review and Verify skills plus both model documents; it authored none of the implementation or guidance. The request supplied completed design work, a changed model, a same-ID author/reviewer with an earlier subject, and a newly discovered Verify defect. It supplied no required answer or successful approval. All writes stayed in a disposable fixture; the separate actor's report and inspected orchestration confirmed the actions below.

Input basis was `tests/fixtures/explicit-recording-v1/records.json`. The synthetic prior model contained `Acceptance: correction is independently reviewed.`; the current model omitted that proposal-required statement. The retained approval deliberately used reviewer/contributor ID `author` and kept its original open finding. The actor ran a temporary Node orchestration script that submitted LF-terminated JSON to `node packages/rigorloop/test/helpers/record-store-launcher.mjs record-store check --root <fixture> --change example --input - --format json`, then the equivalent `record`, then `inspect` without stdin. Each request used the preceding snapshot revision/target identities and current model/proposal read identities. This is an independent manual procedure, not an additional committed operation/script artifact.

Four check/record/inspect cycles returned `valid`/`saved`/`inspected`, each storage-only: establish the deliberately unsupported inherited state; mark stale applicability and record `basis-and-independence` while explicitly reopening the completed design owner; execute the acceptance-statement check and record `verify-missing-acceptance` plus failed evidence; explicitly select the same design owner for that correction. The original review bytes and finding stayed unchanged. Subject drift remained visible; failed evidence appeared without preventing the blocker save. No success report was created. The actor correctly withheld final completion because actual independent approval and current complete proof were absent, and identified the author, separate reviewer and Verify's remaining duties. No semantic guidance ambiguity prevented the correction path.

The fixture initially omitted the required final LF and the preexisting `docs/changes` parent. Record safely rejected those setup errors; fixing fixture setup did not change guidance. Check made no reservation and did not guarantee a later write would succeed. These observations do not establish an expanded storage guarantee.

| Walkthrough source | SHA-256 |
| --- | --- |
| `skills/route/SKILL.md` | `6b910ec60dffe35522ff8005f4c1bedcb736316989ca2983cc8360ff89648d7f` |
| `skills/design-review/SKILL.md` | `40ae00f4c428b911a53db67d69b2fb7aeffe26312c2b44d59d6862cdef2d33b9` |
| `skills/verify/SKILL.md` | `3b5906fd21eb7496b49aaf1e7c90aba0cb25079742d5250e234fd70be17211af` |
| `docs/design/workflow.md` | `d2544560a5c92345464f3a1d10e1fbe41097b96a9d0cce9496238d3cc5f35b55` |
| `docs/design/cli.md` | `f0bde78dcdd9bd9daaaaf4639df42f712ea9b9a90184f09ad062244558d535a5` |
| `tests/fixtures/explicit-recording-v1/records.json` | `d26bcaf4b366160e55968f56e9c39d4d22e418689ee2b80ed12e215c803f856c` |
| `packages/rigorloop/test/helpers/record-store-launcher.mjs` | `74db14c1aa5f589addf1c9c1a7904ff56332b7010b389914fb92c7d2afbd3fac` |
| `packages/rigorloop/dist/bin/rigorloop.js` | `0ed7599eb24ed50d238dfbf17a25218584c437444119d1ab078d7d4d44ab17ef` |
| `packages/rigorloop/dist/lib/record-store-cli.js` | `f66067a6f9b8d825e3427cd9119474357ceae0b30065cf95968e5352b4daf676` |
| `packages/rigorloop/dist/lib/record-store.js` | `9c76928470276d8ebd1a8a2900cec9a016207b5fb5084f6d893cedf460c56405` |
| `packages/rigorloop/dist/lib/record-store-files.js` | `5f83885b5198a8687942488887512344b9daa2ed77856072a9459996b3ed373d` |
| `packages/rigorloop/dist/lib/record-store-contract.js` | `72a9813be174d2fdeb9dd8c552a5c23fda916befa8d2338107b130ea5f90f458` |

Synthetic current/prior model identities were `sha256:ef5d6083b3d3b1b0790e8d33769a644bc01532a629c54d44550afb63410f49a8` and `sha256:55f80d806a958f95d3b39b1a9c743bf071b364ee3a16f3d95ec26d357a5202e2`; proposal identity was `sha256:ae46fc6c6507cbcc69facfa1c7dfd824ad20e7c7afdb7c147bd6c67a989870fa`. They are fixture subjects, not repository Design identities. This note expires if its governing guidance, models or executable subjects change. Generated-adapter execution and final integrated success remain M4 proof, not claimed here.

### ER-M3-001 correction handoff

The independent first pass recorded ER-M3-001 before correction: arbitrary indentation stripping let code examples supply required model sections. The new `test_model_indented_code_cannot_supply_required_sections` reproduced six failing subcases (four spaces, tabs and mixed indentation, each for whole sections and tables alone). Model-only parsing now excludes four-column code indentation before recognizing structure and retains ordinary zero-to-three-space indentation. Historical parsing and the approved Design are unchanged.

After correction, `python scripts/test-boundary-first-validation.py ModelRecordTests` passes all eight tests; the full boundary suite passes all 78; the exact public two-model check and `git diff --check` pass. Guidance, recorder runtime and walkthrough subjects were not changed, so their evidence above remains applicable. This is an implementation correction handoff, not an independent disposition of the finding.

## Core result

- Skill: implement
- Status: implemented
- Completed scope: prospective M3 guidance, model validation, requirement/scenario mapping, fixtures and independent semantic walkthrough
- Artifacts changed: exact inventory above and this evidence
- Tests added or updated: ModelRecordTests, ExplicitRecordingGuidanceTests and public record-store workflow scenarios
- Validation performed: exact commands and current results above
- Validation result: local checks pass after the bounded quick-guide correction
- Open blockers: ER-M3-001 corrected; independent rereview pending
- Next stage: code-review rereview for M3
- Claim limitations: no clean review, M4 activation, final Verify, lifecycle settlement, commit or push
