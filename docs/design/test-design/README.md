# Test design

Start with the [shared rules](rules.md) for choosing scenarios, organizing scripts, writing assertions and maintaining useful protection. [System](../system.md#living-test-design-composition) owns those rules; [Design](../skill/authoring/design.md#living-test-design) owns their application in living models. [System](../system.md#repository-directory-layout) declares this supporting directory.

## Model test designs

System’s own [integrated acceptance](../system.md#integrated-acceptance) and [boundary scenarios](../system.md#boundary-scan-and-acceptance-scenarios) cover whole-system interactions. They remain distinct from the common policy in rules.md. Validation implements check selection, execution, isolation and reporting under that policy.

| Model | Coverage document | Case index |
| --- | --- | --- |
| Release | [Preparation, candidate qualification, authorized publication and recovery](../engineering/release/test-design/test-design.md) | [Release cases](../engineering/release/test-design/test-cases.json) |
| Skill parent | [Shared capability/resource contracts and parent interactions](../skill/test-design/test-design.md) | [Skill cases](../skill/test-design/test-cases.json) |
| Authoring | [Proposal, Design and Plan refinement and handoffs](../skill/authoring/test-design/test-design.md) | [Authoring cases](../skill/authoring/test-design/test-cases.json) |

These are the separately authored packages currently indexed here. Other models may keep their test design in their main document. An entry identifies the owning package; it does not certify implemented assertions, passing execution or completed adoption across all models. Each catalog documents its own provisional format and evidence limits.

## Where information belongs

Shared rules stay here. Model-specific strategy and selected cases stay in their owning model's `test-design/` directory. Executable sources remain under `tests/` and `packages/rigorloop/test/` following [Validation's source layout](../engineering/validation.md#test-sources-groups-and-fixtures). Delivery plans allocate changes, and evidence records hold actual results. Existing scaffolds remain in their canonical template or skill-asset locations.

The published Design skill carries [portable application guidance](../../../skills/design/references/model-authoring.md#living-test-design) for projects with their own layout; it does not require this repository's directory to exist after installation.
