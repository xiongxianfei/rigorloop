# Test design

Start with the [shared rules](rules.md) for choosing scenarios, organizing scripts, writing assertions and maintaining useful protection. [System](../system.md#living-test-design-composition) owns those rules; [Design](../skill/authoring/design.md#living-test-design) owns their application in living models. [System](../system.md#repository-directory-layout) declares this supporting directory.

## Model test designs

Apply the [selection procedure](rules.md#select-requirements-and-proof) before expanding a catalog. System's [test design](../system.md#test-design), integrated acceptance and boundary scenarios cover whole-system interactions, distinct from common policy. Validation owns check selection, execution, isolation and reporting. This navigation accounts for all 24 current document models; section-owned responsibilities appear within their owner's coverage, rather than as additional models.

| Model | Coverage document | Case index |
| --- | --- | --- |
| System | [Composition, shared-policy application and current reliance](../system.md#test-design) | Inline groups |
| Skill parent | [Shared capability/resource contracts and parent interactions](../skill/test-design/test-design.md) | [Skill cases](../skill/test-design/test-cases.json) |
| Workflow | [Coordination, authority, correction and continuation](../skill/workflow.md#test-design) | Inline groups |
| Authoring | [Proposal, Design and Plan refinement and handoffs](../skill/authoring/test-design/test-design.md) | [Authoring cases](../skill/authoring/test-design/test-cases.json) |
| Proposal | [Direction, scope and feasibility](../skill/authoring/proposal.md#test-design) | Inline groups |
| Design | [Reconciliation, ownership and sufficient proof intent](../skill/authoring/design.md#test-design) | Inline groups |
| Plan | [Sequencing and verification allocation](../skill/authoring/plan.md#test-design) | Inline groups |
| Assessment | [Independence, judgment, reliance and closeout](../skill/assessment.md#test-design) | Inline groups |
| Project Foundations | [Vision, governing rules and repository orientation together](../skill/project-foundations/project-foundations.md#test-design) | Inline groups |
| Vision | [Direction and generated README agreement](../skill/project-foundations/vision.md#test-design) | Inline groups |
| Constitution | [Governing principles and preserved authority](../skill/project-foundations/constitution.md#test-design) | Inline groups |
| Project Map | [Observed structure, uncertainty and safe updates](../skill/project-foundations/project-map.md#test-design) | Inline groups |
| Discovery | [Options, facts and decision-owner handoff](../skill/discovery/discovery.md#test-design) | Inline groups |
| Explore | [Distinct alternatives and bounded advice](../skill/discovery/explore.md#test-design) | Inline groups |
| Research | [Attributable evidence, confidence and limits](../skill/discovery/research.md#test-design) | Inline groups |
| Learning | [Supported lessons and accountable follow-up](../skill/learning.md#test-design) | Inline groups |
| Delivery Handoff | [Verified PR basis and external authority](../skill/delivery-handoff.md#test-design) | Inline groups |
| CLI | [Command interface, persistence and composed results](../cli/cli.md#test-design) | Inline groups |
| Records | [Stored contracts, identities and preservation](../cli/records.md#test-design) | Inline groups |
| Installation | [Acquisition, conflicts, replacement and partial failure](../cli/installation.md#test-design) | Inline groups |
| Engineering | [Development and qualification composition](../engineering/engineering.md#test-design) | Inline groups |
| Validation | [Admission, selection, execution and measured cost](../engineering/validation.md#test-design) | Inline groups |
| Packaging | [Canonical inputs, reproducible artifacts and consumers](../engineering/packaging.md#test-design) | Inline groups |
| Release | [Preparation, candidate qualification, authorized publication and recovery](../engineering/release/test-design/test-design.md) | [Release cases](../engineering/release/test-design/test-cases.json) |

An entry identifies durable coverage intent; it does not certify implemented assertions, passing execution or completed adoption. Release, Skill and Authoring retain their selected provisional catalog formats and evidence limits. Other models use proportionate inline groups. Group-level references account for requirements and material hazards without duplicating native method discovery. Implementation gaps and pending semantic procedures stay explicit with their owner; actual runs, assessments and mutable status belong in change records.

## Where information belongs

Shared rules stay here. Model-specific strategy and selected cases stay in their owning model's `test-design/` directory. Executable sources remain under `tests/` and `packages/rigorloop/test/` following [Validation's source layout](../engineering/validation.md#test-sources-groups-and-fixtures). Delivery plans allocate changes, and evidence records hold actual results. Existing scaffolds remain in their canonical template or skill-asset locations.

The published Design skill carries [portable application guidance](../../../skills/design/references/model-authoring.md#living-test-design) for projects with their own layout; it does not require this repository's directory to exist after installation.
