# Authoring test design

Owner: [Authoring](../authoring.md), model ID `authoring`. The [index](test-cases.json) declares three case groups under [System's shared test-quality rules](../../../test-design/rules.md#start-from-supported-outcomes).

This package covers goal refinement, authorized handoffs and corrections across Proposal, Design and Plan. The [model responsibility inventory](../authoring.md#responsibility-inventory) defines their boundaries. The five AUTH-SR requirements retain their identities and behavior.

## Proof dependencies

AUTH-RF-003/004 rely on [Design's living coverage contract](../design.md#living-test-design) and [Plan's proof allocation](../plan.md) to assess whether the model retains its scenario and the plan assigns an adequate observation. AUTH-SH-002/004 apply [Assessment's exact-subject and independence rules](../../assessment.md) to the handoff. Skill's SKL-AR-004 references this package for internal authoring interactions.

## Case groups

| Group | Cases | Distinct failures to expose |
| --- | ---: | --- |
| [Refinement](cases/refinement.json) | 4 | Weakened approved goal; identities lost through work regrouping; coverage rationale stranded in a plan; isolated checks substituted for composed proof. |
| [Scope and handoff](cases/scope-handoff.json) | 4 | Direct correction expands scope; changed case detail is omitted from review; mutable results enter stable artifacts; saving or authorship substitutes for independent judgment. |
| [Correction and reconciliation](cases/correction-reconciliation.json) | 4 | A gap reaches the wrong owner; a changed upstream basis is ignored; live references or historical subjects are damaged during a move; missing prerequisites cause invented dependent work. |

All **12 cases** are proposed independent-review procedures and collectively reference all five parent requirements. They have no executable realization links. That is a statement of the selected observation method and pending assessment, not a claim that no prior review occurred or that 12 automated tests need to be written. Case counts and requirement references establish accounting only.

Keep these twelve scenarios because their failure boundaries differ. Weakening the approved outcome, losing a requirement identity, stranding coverage in Plan and allocating an insufficient observation require different corrections. Likewise, a case omitted from the review package differs from a basis that changes during authoring; artifact-location reconciliation differs from missing required input. Related decision alternatives use named variants with one defining fault. Do not combine these outcomes merely to reduce the count, or turn each variant into another mandatory case.

## Synthetic artifact fixture

The fictional `batch-import-package` is the single shared setup basis for the three groups. It is a bounded engineering example, not a complete stored record or a new product requirement. No RigorLoop record-schema conformance is claimed for this table. Fixture labels are private inputs; they are not repository files to create or public commands to run. Each case compares the coherent baseline with its specified counterexample.

| Fixture artifact or fact | Explicit baseline |
| --- | --- |
| Direction | The authorized user wants a local batch import that either commits every valid row or commits none when any row is invalid. No remote publication or automatic downstream execution is authorized. |
| Proposal | `import-direction` records that goal and scope. The fictional direction decision and its independent assessment apply to the exact baseline proposal. |
| Design | Model `importer`, subject label D0, owns IMPORT-SR-01: an input row has an integer ID, a nonempty value and no duplicate ID in the batch. IMPORT-SR-02: an invalid batch leaves the destination unchanged; a valid batch commits all rows. Its technical design validates the complete batch before the write boundary. |
| Test design | IMPORT-TC-01 observes all rows committed for a valid batch. IMPORT-TC-02 establishes a valid baseline, makes the middle row invalid and observes rejection plus an unchanged destination. The model owns their rationale, observations and fixture roles, with realization explicitly proposed. |
| Concrete inputs | Valid rows are `(1, alpha)`, `(2, beta)`, `(3, gamma)`; the defining invalid variant replaces the middle value with an empty value. The destination initially contains only `(9, retained)`. A rejected batch leaves exactly that original row; a successful batch adds all three new rows. |
| Plan | M1 allocates input validation for IMPORT-SR-01; M2 allocates the batch write boundary and real temporary-destination proof for IMPORT-SR-02. The plan references both model-owned cases and will select actual project-supported commands during delivery allocation. No command execution or passing result is assumed. |
| Authority and identities | The baseline proposal and D0 Design have fictional separately attributable settled assessments. The plan remains an authored draft. D0/D1 are explanatory labels; a real assessment records actual inspected identities. A case explicitly changes the relevant authority or identity fact. |
| Unrelated work and evidence | An independently authorized wording correction has a complete separate basis. Current results and mutable activity, if any, belong to their evidence/record owners; no such values are embedded in the stable proposal, Design or plan. |
| Case and review identities | C0 is the original model-owned case file. C1 is a changed case file with the same case IDs. R0 is an earlier assessment of its exact original paths/identities. D0, D1, C0, C1 and R0 are fictional labels; they do not stand for an existing repository approval. |
| Command-allocation correction | For AUTH-SH-001 only, the fictional project declares old-batch-check and current-batch-check equivalent for the same full-batch destination-preservation observation. These are opaque fixture labels, not executable commands supplied by this repository. |

Use a fresh private artifact copy per case/variant. Keep the unchanged starting facts and identities visible, apply only the named fault and inspect the resulting artifact or handoff decision. The partial-write counterexample leaves exactly `(9, retained)` and `(1, alpha)`; the correct invalid-batch outcome contains only `(9, retained)`. AUTH-CR-001's duplicate-key variant removes the corresponding Design behavior from this baseline; it does not silently redefine the intended behavior. AUTH-CR-002 explicitly adds an index-preservation obligation in D1 to make the stale allocation observable. AUTH-CR-003 is an authorized current move with concrete live consumers, not a matrix of retired paths to keep operationally supported.

## Review method and supporting checks

Each case gives concrete conditions, actions, independently expected outputs or decisions, prohibited effects and a pending assessment. The primary technique is a walkthrough. Within it, compare valid/invalid partitions, correction-owner decision alternatives, identity transitions and preservation properties as relevant. Inspect the complete relied-on path and actual outputs; a list of matching headings or requirement IDs cannot expose a weakened goal or inadequate proof allocation.

Present the compliant control and the specified faulty candidate under the same authority/basis. Inspect what differs and whether that difference exposes the named failure. AUTH-SH-003 places progress, approval and fabricated run results in separate candidate copies so one invalid field cannot mask another. For each procedure record the inspected inputs and candidate, expected versus observed decision, preserved subjects and remaining limitations. A reviewer must assess the candidate independently; restating the JSON's expected text is not evidence of the composed outcome.

The reviewer records the exact source/fixture/output identities, observations, counterexample disposition and limits through the existing Assessment/evidence owner. Authoring this catalog is not executing those reviews. A synthetic walkthrough cannot establish target-agent runtime behavior; a future evaluation harness would require an explicit environment, authority, reproducibility and evidence design.

Existing [authority checks](../../../../../tests/skill/skill_authority_tests.py) inspect authoring instructions for prohibited settlement wording and artifact assets for mutable-status headings. Existing [shared refinement checks](../../../../../tests/skill/skill_shared_policy_tests.py) inspect responsibility statements, traceability fields and the lack of added lifecycle authority. They provide useful structural support but do not establish the twelve composed outcomes, so they are not linked as executable realization of these cases. Their detailed mechanical ownership remains with Skill and the child methods.

The native aggregate remains [test-skill-validator.py](../../../../../tests/skill/test-skill-validator.py). This review-only catalog has no executable case population to compare with its full discovery count. Do not generate Python tests that merely assert the JSON's own expected text, invent a test method for a manual review, or delete existing unlinked regressions. If executable coverage is later added, link its real callable and verify trusted native discovery at that time.

## Catalog contract

Authoring explicitly adopts the structural field/type, ID, path, fixture, variant, closed-vocabulary and realization rules in [Skill's catalog contract](../../test-design/test-design.md#catalog-contract), with these local bindings. Skill owns those shared field conventions; Authoring owns these scenarios and their scope. The local bindings below identify the exact reused representation.

| Binding | Authoring value |
| --- | --- |
| Index format | `authoring-test-catalog-draft`, integer `format_version: 2`. |
| Group format | `authoring-test-cases-draft`, integer `format_version: 2`. |
| Owner | Model `authoring`; Design `docs/design/skill/authoring/authoring.md`; strategy `docs/design/skill/authoring/test-design/test-design.md`. Every group repeats this exact owner. |
| Group membership | Exactly the three paths explicitly listed in `test-cases.json`, under this package's `cases/`. Adjacent JSON has no implicit authority. |
| Requirements | Resolve only to the Authoring parent's AUTH-SR requirement table. Synthetic IMPORT-SR labels are fixture data, not requirement references in the catalog. |
| Fixtures | `profile` references the current strategy file containing the shared synthetic setup. Group-local initial conditions select that setup; no command, automatic merge or class inheritance is implied. |
| Observation method | Current cases use `independent-review`, boundary `review`, technique `walkthrough` and exact existing Markdown section targets. Each is `proposed`, with an empty test list and an explicit pending assessment in gaps. |
| Scope | Required nonempty strings `model`, `boundary`, `entrypoint`, `coverage_claim`, with no other fields. Boundary names goal refinement, authorized handoffs and corrections. |
| Entry and discovery | The scope's entrypoint identifies the existing supporting suite; it does not dispatch these review cases. Zero executable links make no full-family coverage claim. |

All other field constraints are unchanged from the explicitly referenced contract. Unknown fields and closed values reject before consistency checks; duplicate keys, unsafe/escaped/symlinked paths, missing groups, duplicate IDs, nonexistent requirements/sections and inconsistent realization states are invalid. JSON prose and fixture data never become executable expressions. Version 2 follows the selected convention; it implies neither a previously shipped Authoring version 1 nor a migration promise.

## Validation and maintenance

Author checks parse the index and groups, resolve declared ownership and shared contract, check fields/closed values/unique IDs/fixtures/requirements/section targets, and verify local links. Main-model and prose validation still apply. Independent assessment decides semantic sufficiency; author checks do not perform the twelve reviews.

[Validation](../../../engineering/validation.md#authoring-test-design-admission-contract) defines admission for the strategy, index and three groups. A passing main-model check does not establish catalog admission. Implementation allocation and observed tooling limitations are recorded in the [owning change](../../../../changes/2026-09-17-model-test-design/change.json).

Maintain cases when a goal, requirement relationship, scope, observation, fixture or responsibility changes. Preserve case identities through moves and update affected current references without rewriting historical approval subjects. Keep detailed child rules with Proposal, Design and Plan; keep Skill's broader interactions referenced rather than copied. Delivery allocates any future proof implementation, while actual results and judgments remain in evidence.
