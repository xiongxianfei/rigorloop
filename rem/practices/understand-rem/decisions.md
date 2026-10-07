# 8. How to reconstruct an REM decision

## 8. How to reconstruct an REM decision

When a reader asks why REM contains a particular rule, follow the links in this order.

### Example: Why does REM use `IR → SR → AR`?

1. Read the requirement definitions in [Concepts](../../concepts/requirements.md#requirements).
2. Read [needs and solutions](../../principles/needs-can-outlive-solutions.md) and [origin and realization](../../principles/origin-and-realization-answer-different-questions.md); these explain distinctions, not the exact hierarchy chosen by REM.
3. Read the containment and cross-domain rules in the [Requirement model](../../models/requirements.md).
4. Read [5W2H](../../methods/5w2h.md) and [Requirement Analysis](../../methods/requirement-analysis.md) to see how engineers create the three levels.

### Example: Why does REM keep Feature separate from Scenario?

1. Read [Scenario](../../concepts/scenarios.md#requirement-analysis-entities) and [Feature](../../concepts/system-and-architecture.md#system-and-architecture-assets).
2. Read the durable capability/behavior rationale in [System Design](../../models/system-design.md).
3. Read the [System Design model](../../models/system-design.md).
4. Read the [Scenario model](../../models/scenarios.md) and [Scenario Analysis](../../methods/scenario-analysis.md).

### Example: Why does SR confirm Function while AR allocates to Module?

1. Read [SR, AR, Function, and Module](../../concepts/README.md).
2. Read [component and system results](../../principles/component-results-do-not-establish-system-results.md), then the separate [allocation relationships](../../models/architecture-allocation.md).
3. Read the [Requirement model](../../models/requirements.md), [System Design model](../../models/system-design.md), and [Architecture Design model](../../models/architecture-design.md).
4. Read [Requirement Analysis](../../methods/requirement-analysis.md), [Functional Analysis](../../methods/functional-analysis.md), and [Architecture Allocation](../../methods/architecture-allocation.md).


### Why does REM use classic 4+1 architecture views?

Start with the [origin and reference](../../methods/architecture-views.md#origin-and-reference), then distinguish [REM's adoption and adaptation](../../methods/architecture-views.md#adoption-and-adaptation-in-rem) from the original framework. The method is the authoritative explanation of that distinction.

1. Read the [Architecture View and 4+1 Architecture View Graph concepts](../../concepts/system-and-architecture.md#system-and-architecture-assets).
2. Read [responsibility and realization](../../principles/responsibility-and-realization-can-have-different-boundaries.md) and [independent representations](../../principles/independent-representations-can-diverge.md).
3. Read the generated 4+1 projection rules in the [Architecture Design model](../../models/architecture-design.md#generated-41-architecture-views).
4. Read [4+1 Architecture Views](../../methods/architecture-views.md) to see how Logical, Process, Development, Physical, and Scenario views are generated from one authoritative semantic model.
5. Read the [Scenario model](../../models/scenarios.md) to see why the Scenario View derives internal architecture participation without changing the black-box Scenario itself.

REM uses 4+1 for generated comprehension and validation, not to create five independently authored architecture models.

### Example: Why can a Module contain Modules?

1. Read the [Module, Module containment, Interface, and Interface exposure concepts](../../concepts/system-and-architecture.md#system-and-architecture-assets).
2. Read [change propagation](../../principles/boundary-choices-shape-change-propagation.md), then [typed relationships and identity](../../models/README.md#representation).
3. Read [Module hierarchy and encapsulation](../../models/architecture-boundaries.md#module-hierarchy-and-encapsulation) in the Architecture Design model.
4. Read [Architecture Allocation](../../methods/architecture-allocation.md#establish-or-refine-the-module-hierarchy) for lowest-coherent allocation and boundary exposure.
5. Read the [Logical View](../../methods/views/logical.md#logical-view) to see how parent Modules are shown first and child responsibilities are progressively disclosed.

REM does not prescribe a universal maximum hierarchy depth. A project or implementation may impose a shallower supported depth as a representation constraint without changing REM's hierarchy semantics.

### Example: Why must a Feature or Function name explain its purpose?

1. Read [Clear engineering definitions](../../models/operational-support.md#clear-engineering-definitions).
2. Read the naming and definition criteria in the [System Design model](../../models/system-design.md#clear-names-and-boundaries).
3. Follow the Feature procedure in [Scenario Analysis](../../methods/scenario-analysis.md#step-1--confirm-or-reuse-the-feature), the Function procedure in [Functional Analysis](../../methods/functional-analysis.md), or the allocation procedure in [Architecture Allocation](../../methods/architecture-allocation.md).
4. Read [Operational Support](../../models/operational-support.md#naming-and-location) for the separate question of how a project represents that name in directories, filenames, or other storage.

This is the intended role of this file: it tells the reader which authoritative knowledge to follow rather than restating that knowledge here.

---
