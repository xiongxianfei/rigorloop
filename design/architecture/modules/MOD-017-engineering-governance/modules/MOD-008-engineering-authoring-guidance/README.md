# Authoring guidance

Responsibility and allocation are defined in [module.json](module.json).

## Supporting contracts

These documents retain detailed clauses and proof under this Module; they are not additional REM entities.

- [Authoring Design](authoring.md)
- [Constitution Design](constitution.md)
- [Engineering authoring](design-authoring.md)
- [Discovery Design](discovery.md)
- [Explore Design](explore.md)
- [Project Foundations Design](project-foundations.md)
- [Project Map Design](project-map.md)
- [Request and proposal intake](requirement-analysis.md)
- [Research Design](research.md)
- [Vision Design](vision.md)

## IR-006 guidance and assessment

[Applicable authoring guidance and task assessment](guidance.md) defines source/profile selection, bounded correction, worked examples and prepared semantic tasks for SR-032–034 and AR-079–081. MOD-017 retains the IF-008 boundary; MOD-012 composes its results with existing assurance and recording. The two Process diagrams are generated from the same owning contract.

## Guidance and assessment interaction

<!-- architecture-diagram: guidance-selection-and-correction -->

```d2
shape: sequence_diagram
participant: "Author or agent"
procedure: "Skill procedures\nMOD-012"
governance: "IF-008\nMOD-017 / MOD-008 contribution"
sources: "Selected canonical sources"
participant -> procedure: "Activity, adopted profile, subjects and authority"
procedure -> governance: "Select applicable guidance"
governance -> sources: "Inspect exact owners, versions, rules and examples"
sources -> governance: "Selected content or explicit availability/conflict gaps"
governance -> procedure: "Source-bound selection and applicability explanation"
procedure -> governance: "Explain authoring or identified correction"
governance -> procedure: "Expected result, checks, unresolved decisions and limits"
procedure -> participant: "Usable bounded explanation and source navigation"
```

<!-- architecture-diagram: assess-guidance-tasks -->

```d2
shape: sequence_diagram
maintainer: "Guidance maintainer\nand task observer"
participant: "Task participant"
procedure: "Skill procedures\nMOD-012"
guidance: "IF-008\nMOD-008 via MOD-017"
assurance: "IF-014\nMOD-007 via MOD-017"
records: "Commands and records\nIF-004"
maintainer -> procedure: "Prepared inputs, expected outcomes, group and source basis"
procedure -> guidance: "Prepare semantic task context before performance"
guidance -> procedure: "Identified method or explicit missing assessment basis"
maintainer -> participant: "Perform authorized task using selected guidance"
participant -> maintainer: "Actual output, rule explanation and help used"
maintainer -> procedure: "Observed results, checks, gaps and interruptions"
procedure -> guidance: "Compare actual outcomes with prepared expectations"
guidance -> procedure: "Bounded task results, findings and unassessed scope"
procedure -> assurance: "Prepare supplied method/observations or assessor judgment"
assurance -> procedure: "Exact content and reliance limitations"
procedure -> records: "Explicit authorized retention, when selected"
records -> procedure: "Actual outcome and selected retained readback"
procedure -> maintainer: "Attributable result; saved status separate from success"
```

The first sequence is the guided alternative of SCN-031/032/033/040; direct human use reads the same sources. The second is SCN-034's assessment alternative with optional governed retention. Missing source context stops dependent explanation. Missing task observations leaves its result unassessed; no sequence arrow asserts successful participant execution or a formal approval.
