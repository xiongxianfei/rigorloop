# Principle 19: Generate architecture views from one authoritative semantic model

## Relationship and why

Readers ask different questions about the same architecture, so a useful view selects and emphasizes information for a particular concern. Independently maintaining the same architectural facts in each presentation creates opportunities for disagreement. Deriving views from their authoritative owners keeps the presentations connected, while separate fidelity and reading-task assessments check whether they are accurate and understandable.

## REM commitment

Use complementary architecture views to address distinct concerns. REM adopts the five 4+1 concerns through its [documented adaptation](../methods/architecture-views.md#adoption-and-adaptation-in-rem): Logical, Process, Development, Physical, and Scenario. Derive them from authoritative engineering knowledge and choose presentations that make their concerns understandable. Views may select, collapse, or emphasize information for comprehension, but they must preserve semantic meaning, ownership, and provenance and must not become a second source of truth.
Keep authoritative knowledge, semantic projection, and rendered presentation distinct. Knowledge may include structured facts and authored explanations under their declared owners; rendering an owning explanation does not create another source of architecture truth. Identify the source state and derivation rules so views remain traceable and regenerable.

Apply [explicit view selection](../methods/architecture-views.md#view-selection-and-tailoring) to omit, combine or supplement presentations with a reason while preserving applicable concern coverage.

## Application

Use the [Architecture View method](../methods/architecture-views.md) for the five concerns, projection provenance and generation/assessment cycle.
[Knowledge, projection, and presentation](../methods/view-presentation.md) owns authored explanations, progressive disclosure, faithful labels, accessible full names and identities, and assessment of actual reading tasks.
The [Process View](../methods/views/process.md) owns runtime topology, focused interaction/lifecycle/control-flow/timing/concurrency model selection and the prohibition on deriving execution order from Logical reachability.
Apply [explicit view selection and tailoring](../methods/architecture-views.md#view-selection-and-tailoring) to omit, combine or supplement presentations with a reason while preserving applicable concern coverage.
