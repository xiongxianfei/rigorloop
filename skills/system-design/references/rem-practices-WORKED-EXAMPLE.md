<!-- Generated from rem/practices/WORKED-EXAMPLE.md; source SHA-256 6ec0c6a6a2608d5ac9a52dd32a20da0da71ffdfa969c420d271d95bf36ae7e0d. Edit the owning REM source. -->

# Worked example: inspect responsibility offline

## Status and scope

This is a fictional, bounded design illustration using REM's existing rules.
All identities below belong only to this example.
The example selects an offline architecture viewer for one maintainer inspecting one known Function; it is not a claim that a product was implemented, tested or accepted.

## Reconcile the request

RR: “During an offline review, I need to find who owns this behavior.”
For this illustration, assume the existing model lacks an offline inspection capability and contains the selected Function and its primary Module.
After comparing the request with that model, introduce one need rather than one requirement for every UI element.

| Definition | Meaning and relationship |
| --- | --- |
| IR-EX-01 — Identify responsibility during offline review | A maintainer needs to identify the accountable Module for a selected Function while network access is unavailable. |
| FEAT-EX-01 — Inspect responsibility offline | Durable capability confirmed by IR-EX-01. |
| SCN-EX-01 — Find the owner of a Function without network access | Owned by IR-EX-01; primary Feature FEAT-EX-01; informs SR-EX-01. |
| SR-EX-01 — Show accountable responsibility offline | Under IR-EX-01, the viewer shall display the selected Function's recorded primary Module and source state without a network request. Confirms FUNC-EX-01. |
| FUNC-EX-01 — Resolve and present accountable responsibility | Reads a selected Function identity and an exported model, returns its primary Module and source state, and reports absent/invalid mappings explicitly. Realizes FEAT-EX-01. |
| AR-EX-01 — Resolve responsibility from the exported model | Under SR-EX-01, MOD-EX-01 shall resolve the selected Function to its recorded primary Module using the supplied snapshot, preserving source identity and reporting a missing or invalid mapping explicitly. |
| MOD-EX-01 — Responsibility inspection | Primary owner of FUNC-EX-01 and accountable Module for AR-EX-01. Owns model lookup, presentation and invalid-mapping handling in this bounded example. |

There is one parent IR per SR, one parent SR per AR, and one accountable Module per Function/AR.
The AR refines the local lookup and integrity obligation; the SR's complete offline outcome still needs integrated verification.
No additional Module or Interface is invented for this single-responsibility illustration.
If later decomposition creates significant Module interactions, architecture must define their contracts and reconcile the allocations.

## Seven-question analysis

Each requirement accounts for all seven questions at its own level.
These are illustrative supplied assumptions, not observations about real users.

| Question | IR-EX-01 | SR-EX-01 | AR-EX-01 |
| --- | --- | --- | --- |
| What | Ownership is difficult to determine during offline review. | The viewer presents the recorded primary Module and source state for a selected Function. | The responsible Module resolves the mapping from the supplied snapshot and detects missing/invalid data. |
| Why | The maintainer needs an accountable contact or responsibility boundary. | An explicit source-qualified result enables the offline inspection capability. | Incorrect or invented mappings would misdirect the review. |
| Who | Maintainer reviewing engineering behavior. | Viewer user and the source-model owner. | MOD-EX-01's implementer and assessor. |
| When | Network access is unavailable during a review. | When the user selects a Function in an opened export. | When lookup is requested against the supplied snapshot. |
| Where | A local copy of the project architecture information. | The viewer's offline inspection boundary. | Model lookup within MOD-EX-01. |
| How | Provide an inspectable local representation without assuming a particular renderer. | Resolve the recorded relationship and display it with source identity; report unavailable mappings. | Validate reference resolution and return the accountable Module or an explicit error using only the supplied data. |
| How much | One known Function and its recorded primary owner in this slice; no invented performance target. | Preserve the selected relationship and source state; issue no network request. | Cover present, absent and invalid references; preserve input state. |

No consequential open question remains under these supplied assumptions.
If the meaning of ownership is actually unresolved, retain that question and keep dependent decisions provisional; do not replace it with a guessed answer.

## Black-box Scenario

The maintainer has a valid local export and no network access.
They open it, select the known Function and inspect its recorded accountable Module and source state.
The expected outcome is that they can identify the recorded responsibility and recognize which engineering state it describes.
If the export lacks the mapping, the viewer reports that absence rather than presenting an inferred owner.
These steps describe stakeholder-observable interaction; the Module lookup sequence belongs to architecture explanation, not to the governed Scenario.

## Design and selected views

MOD-EX-01 owns the lookup behavior and rendered explanation.
The export is a read-only derived snapshot; the current engineering model remains authoritative.
The technical realization is a local viewer and bundled data under MOD-EX-01, without a new first-class realization entity.

| Concern | Selected presentation and rationale |
| --- | --- |
| Logical | Show the Function, accountable Module, source-state relationship and invalid-mapping boundary. |
| Development | Combine with the Logical explanation for this small slice, explicitly identifying the viewer and model-lookup code responsibilities. A code unit remains distinct from a Module. |
| Process | Describe local lookup and error handling in prose; omit a separate topology diagram because the slice adds no concurrent participant or execution boundary. |
| Physical | Record the local export/browser placement and offline assumptions; omit a separate deployment diagram because no additional host or deployment relationship is introduced. |
| Scenario | Walk through the selected stakeholder outcome and its failure case against the above design. Keep internal participation outside SCN-EX-01. |

An omission concerns a separate presentation, not the underlying architectural question.
If a project requires a particular view artifact, that obligation still applies.

## Assessment plans

| Question | Planned assessment | Current result |
| --- | --- | --- |
| Verification of SR-EX-01 | For an identified viewer/export version with networking disabled and requests observed, select a known Function; compare the displayed primary Module and source state with the independently prepared source model; confirm no network request. | Not executed; conformance unestablished. |
| Verification of AR-EX-01 | Exercise present, absent and invalid mapping inputs; check exact owner resolution or explicit error, source identity and unchanged snapshot data. | Not executed; conformance unestablished. |
| Intended-use validation of IR-EX-01/SCN-EX-01 | With a representative maintainer, agree a task and correct outcome beforehand. Observe whether they identify and explain the accountable responsibility and source state from the offline viewer; retain confusion and help required. | No participant assessment; intended-use success unestablished. |

Passing the mapping check alone would not establish network independence or user comprehension.
A result from a different snapshot needs an applicability assessment before reuse.
If every technical check passes but the participant mistakes a supporting Module for the accountable owner, return the presentation or requirement issue to its owner and reassess; keep the original result intact.

## Exit

This example ends at an illustrative design and assessment plan.
Actual implementation, evidence, independent project reviews and acceptance remain unperformed.
