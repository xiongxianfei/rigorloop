# Markdown Readability Behavior Preservation

## Status

- Result: M2 generated artifact guidance aligned
- Scope: selected skills, selected skeleton assets, and generated-output proof
- Owner: implement M2
- Date: 2026-07-04

## Surface Matrix

| Surface | Baseline | New proof | Preservation |
| --- | --- | --- | --- |
| Rendered Markdown | Skill and skeleton documents render as ordinary Markdown. | Added guidance sections and metadata comments only. | preserved |
| Generated artifact shape | Proposal, spec, plan, and test-spec skeletons owned section order. | Skeletons now declare the readability contract while preserving existing sections. | preserved |
| Skill guidance | Skills already directed artifact creation from canonical authored sources. | Selected skills now name semantic source lines, stable IDs, tables, optional diagrams, and no readability-implied manual-proof contracts. | strengthened |
| Manual-proof contracts | The approved proposal and spec exclude manual-proof contracts from the first slice. | Guidance says not to require manual-proof contracts from readability rules alone. | preserved |
| Diagrams | Diagrams were not required by generated artifact skeletons. | Guidance encourages diagrams only when they reduce cognitive load. | preserved |
| Generated adapter output | Public adapter output is derived from canonical skill sources. | `build-skills --check` and adapter distribution tests provide generated-output currency proof. | preserved |
| Historical docs | Historical Markdown is not part of M2 migration scope. | No mass reflow or historical rewrite is included. | preserved |

## Cold-Read Checks

| Question | Answer |
| --- | --- |
| Can a reviewer find the readability rules in selected skills? | Yes; each selected skill has `Generated Markdown readability`. |
| Can a reviewer find the skeleton readability declaration? | Yes; each selected skeleton has `Readability contract:` metadata near the top. |
| Can a reviewer identify manual-proof scope? | Yes; each selected skill states that readability guidance does not require manual-proof contracts. |
| Can a reviewer identify diagram policy? | Yes; each selected skill says diagrams are optional and must reduce cognitive load. |
| Can a reviewer verify generated-output currency? | Yes; use the M2 validation commands recorded in the plan and change metadata. |

## No-Migration Proof

M2 does not reflow historical Markdown.
M2 does not hand-edit generated public adapter bodies.
M2 does not make skeleton comments the policy owner.
The governing spec remains the policy owner, and skeletons own output shape.
