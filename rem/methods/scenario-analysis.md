# Scenario Analysis method

Use this method during Initial Requirement analysis to create and govern first-class black-box Scenarios, confirm the durable Feature needed by the IR, and expose candidate system obligations for later SR analysis.

The [Scenario concept](../concepts/README.md#requirement-analysis-entities) defines what a Scenario means.
The [Scenario model](../models/scenarios.md) owns Scenario identity, lifecycle, ownership, cardinality, and black-box constraints.
The [Requirement model](../models/requirements.md) owns the `IR → SR → AR` requirement tree.
The [System Design model](../models/system-design.md) owns Feature and Function semantics.

## Inputs

Start with:

- an IR and its current [5W2H analysis](5w2h.md);
- supported stakeholder, product, operational, or engineering context;
- existing Features when the need may extend an already durable capability;
- existing Scenarios when the situation may already be governed;
- known constraints and unresolved questions.

Do not begin from screens, APIs, Modules, code, or a preferred implementation.
Apply the [single consequential open-question rule](requirement-analysis.md#keep-one-consequential-open-question) to each Scenario: resolve what the available sources establish, then ask only the highest-value remaining question when clarification is needed.

## 1. Confirm the stakeholder goal and Feature

Ask what durable stakeholder-visible capability is needed to address the IR.
Reuse an existing Feature when the need extends a capability that already has the same engineering meaning.
Create or propose a new Feature only when the capability has independent durable meaning.

A Feature is not a Scenario.
One Feature normally has multiple Scenarios over its lifetime.

## 2. Identify materially distinct stakeholder situations

Identify situations that may expose meaningfully different system obligations. Look for differences in:

- actor or stakeholder role;
- goal;
- starting context;
- available information;
- trigger;
- externally meaningful state or condition;
- expected outcome;
- alternative, boundary, failure, or recovery outcome.

Do not create a new Scenario for every incidental variation.
Create a distinct Scenario when the situation has independent analysis value or is likely to reveal different system obligations.

## 3. Create or reuse the Scenario identity

Before authoring a new Scenario, check whether an existing governed Scenario already represents the same stakeholder situation.

Reuse the existing Scenario identity when refining wording or externally equivalent interaction without changing its engineering meaning.
Create a new Scenario when the stakeholder goal, primary Feature, or materially significant situation changes enough to represent different engineering meaning.

A new Scenario begins in `draft`.
The project representation selects the concrete ID syntax; `SCN-001` is illustrative.

## 4. Define the black-box Scenario

Describe:

- **title** — the stakeholder-visible goal or action, its subject, and any condition needed to distinguish the situation;
- **actor** — who pursues the outcome;
- **goal** — what the actor is trying to achieve;
- **context** — the relevant situation;
- **trigger** — what starts the Scenario;
- **preconditions** — externally meaningful conditions already true;
- **interaction** — actor actions and system responses visible at the system boundary;
- **expected outcome** — successful stakeholder-visible result;
- **alternative and failure outcomes** — materially different observable results when relevant.

Apply the [Scenario naming rules](../models/scenarios.md#clear-scenario-names), and compare the title with neighboring Scenarios before accepting it.
Let the project representation derive navigation labels from the authoritative identity and title; do not maintain an independent storage name.

Prefer actor/system interaction:

```text
Actor requests something observable
        ↓
System responds observably
        ↓
Actor obtains or fails to obtain the intended outcome
```

### Black-box rule

The Scenario MUST NOT define:

- Module allocation;
- Interface or API design;
- internal Function call sequences;
- database schemas or internal state representation;
- source files, classes, packages, crates, or services;
- algorithms, threads, queues, protocols, or implementation technology.

A stakeholder-visible channel or technology constraint may appear only when the IR itself requires that observable constraint.

A useful check is:

> Would this Scenario still be meaningful if the internal implementation were replaced?

If not, move the internal detail to later design work.

## 5. Analyze normal, alternative, boundary, and failure outcomes

Start with the normal success path, then examine only materially relevant variants.
Useful categories include:

- normal;
- legitimate alternative;
- boundary or limit;
- permission or actor variation;
- prior-state variation;
- failure;
- recovery where recovery is required.

Not every Scenario needs every category. Use stakeholder impact and behavioral difference rather than checklist completeness.

## 6. Extract candidate system obligations

For each meaningful interaction and outcome, ask:

> What must the system guarantee for this Scenario to succeed or fail correctly?

Record candidate obligations in analysis language.
Do not make them authoritative Functions or architecture.

For example:

```text
Scenario observation:
The system provides the entity matching a known identifier.

Candidate obligation:
The system must resolve a governed entity by stable identifier.
```

Failures often reveal obligations omitted by the normal path.

## 7. Reconcile candidate obligations into SRs

Use [Requirement Analysis](requirement-analysis.md#derive-system-requirements) to turn candidate obligations into independently assessable SRs.

One Scenario may inform several SRs.
One SR may be informed by several Scenarios.
This traceability is a graph and does not change the `IR → SR → AR` tree.

Every confirmed Scenario must eventually be accounted for by the IR's SR analysis: either one or more SRs cover the material obligations revealed by the Scenario, or the analysis explicitly concludes that existing obligations already cover it and no new SR is necessary.

## 8. Confirm Functions through SR analysis

Scenario Analysis may identify candidate behavior, but it does not make a Function authoritative.
For each SR, use [Requirement Analysis](requirement-analysis.md#derive-system-requirements) to confirm the logical Function or Functions required by the obligation.

```text
Scenario
    │ reveals candidate obligations
    ▼
   SR
    │ confirms logical behavior
    ▼
Function
```

Do not create one Function per Scenario or per SR merely to mirror those structures.

## 9. Confirm the Scenario

Move a Scenario from `draft` to `confirmed` when:

- its actor, goal, context, trigger, and preconditions are clear;
- its interaction and outcomes remain black-box;
- it belongs to one IR;
- it exercises one primary Feature;
- materially relevant alternatives or failures have been considered;
- unresolved questions that prevent trustworthy interpretation are resolved or explicit;
- reviewers can distinguish it from neighboring Scenarios.

Confirmation establishes the Scenario as current governed analysis knowledge.
It does not approve implementation, architecture, verification, or requirement satisfaction.

## 10. Maintain and obsolete Scenarios

When the stakeholder situation changes, decide whether to refine the existing Scenario or create a new one using the identity rules in the [Scenario model](../models/scenarios.md#identity-continuity).

Move a Scenario to `obsolete` when it no longer represents a current supported stakeholder situation.
Do not delete or rewrite historical meaning merely because a newer Scenario replaces it.
Configuration history preserves the Baselines in which the Scenario was current.

## Scenario quality review

Before accepting a Scenario, ask:

1. **Stakeholder** — Is the actor and goal clear?
2. **Black-box** — Does it avoid internal solution design?
3. **Behavioral** — Does it describe a meaningful situation rather than restating the Feature?
4. **Analytical** — Can it expose concrete system obligations?
5. **Distinct** — Does its title clearly distinguish the stakeholder situation from neighboring Scenarios and agree with its goal, context, and outcomes?
6. **Durable context** — Would it remain meaningful after an internal refactor?
7. **Traceable** — Is its owning IR and primary Feature clear, and is its SR coverage accounted for when Requirement Analysis completes?

## Completion criteria

Scenario Analysis for an IR is sufficiently complete when:

- the durable Feature is confirmed or an existing Feature is intentionally reused;
- the material stakeholder situations are represented by governed Scenarios rather than informal prose;
- each confirmed Scenario has stable identity and lifecycle state;
- each confirmed Scenario has exactly one owning IR and one primary Feature;
- each confirmed Scenario remains black-box;
- normal and materially relevant alternative/failure outcomes have been considered;
- candidate obligations have been reconciled through SR analysis;
- every confirmed Scenario is accounted for by the SR set or an explicit no-new-obligation conclusion;
- Scenario, Feature, SR, Function, and Verification are not treated as interchangeable concepts.

Scenario Analysis does not allocate architecture, define implementation, approve Requirements, or provide Verification Evidence.
