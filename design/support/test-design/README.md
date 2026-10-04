# Test design

Start with the [shared rules](rules.md) for choosing scenarios, organizing scripts, writing assertions and maintaining useful protection. [System](../../architecture/composition.md#living-test-design-composition) owns those rules; [Design](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md#proportionate-design-and-proof) owns their application in living models. [System](../../architecture/composition.md#repository-directory-layout) declares this supporting directory.

## Model test designs

Apply the [selection procedure](rules.md#select-requirements-and-proof) before expanding a catalog. System's [test design](../../architecture/composition.md#test-design), integrated acceptance and boundary scenarios cover whole-system interactions, distinct from common policy. Validation owns check selection, execution, isolation and reporting. This navigation accounts for all 24 current document models; section-owned responsibilities appear within their owner's coverage, rather than as additional models.

| Model | Coverage document | Case index |
| --- | --- | --- |
| System | [Composition, shared-policy application and current reliance](../../architecture/composition.md#test-design) | Inline groups |
| Skill parent | [Shared capability/resource contracts and parent interactions](../../architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/test-design/test-design.md) | [Skill cases](../../architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/test-design/test-cases.json) |
| Workflow | [Coordination, authority, correction and continuation](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md#test-design) | Inline groups |
| Authoring | [Proposal, Design and Plan refinement and handoffs](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/test-design/test-design.md) | [Authoring cases](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/test-design/test-cases.json) |
| Proposal | [Direction, scope and feasibility](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/requirement-analysis.md#test-design) | Inline groups |
| Design | [Reconciliation, ownership and sufficient proof intent](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md#test-design) | Inline groups |
| Plan | [Sequencing and verification allocation](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/planning.md#test-design) | Inline groups |
| Assessment | [Independence, judgment, reliance and closeout](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md#test-design) | Inline groups |
| Project Foundations | [Vision, governing rules and repository orientation together](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-foundations.md#test-design) | Inline groups |
| Vision | [Direction and generated README agreement](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/vision.md#test-design) | Inline groups |
| Constitution | [Governing principles and preserved authority](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/constitution.md#test-design) | Inline groups |
| Project Map | [Observed structure, uncertainty and safe updates](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-map.md#test-design) | Inline groups |
| Discovery | [Options, facts and decision-owner handoff](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/discovery.md#test-design) | Inline groups |
| Explore | [Distinct alternatives and bounded advice](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/explore.md#test-design) | Inline groups |
| Research | [Attributable evidence, confidence and limits](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/research.md#test-design) | Inline groups |
| Learning | [Supported lessons and accountable follow-up](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-009-engineering-learning/learning.md#test-design) | Inline groups |
| Delivery Handoff | [Verified PR basis and external authority](../../architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/delivery-handoff.md#test-design) | Inline groups |
| CLI | [Command interface, persistence and composed results](../../architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md#test-design) | Inline groups |
| Records | [Stored contracts, identities and preservation](../../architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md#test-design) | Inline groups |
| Installation | [Acquisition, conflicts, replacement and partial failure](../../architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md#test-design) | Inline groups |
| Engineering | [Development and qualification composition](../development.md#test-design) | Inline groups |
| Validation | [Admission, selection, execution and measured cost](../validation.md#test-design) | Inline groups |
| Packaging | [Canonical inputs, reproducible artifacts and consumers](../../architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md#test-design) | Inline groups |
| Release | [Preparation, candidate qualification, authorized publication and recovery](../../architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/test-design/test-design.md) | [Release cases](../../architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/test-design/test-cases.json) |

An entry identifies durable coverage intent; it does not certify implemented assertions, passing execution or completed adoption. Release, Skill and Authoring retain their selected provisional catalog formats and evidence limits. Other models use proportionate inline groups. Group-level references account for requirements and material hazards without duplicating native method discovery. Implementation gaps and pending semantic procedures stay explicit with their owner; actual runs, assessments and mutable status belong in change records.

## Where information belongs

Shared rules stay here. Model-specific strategy and selected cases stay in their owning model's `test-design/` directory. Executable sources remain under `tests/` and `packages/rigorloop/test/` following [Validation's source layout](../validation.md#test-sources-groups-and-fixtures). Delivery plans allocate changes, and evidence records hold actual results. Existing scaffolds remain in their canonical template or skill-asset locations.

The published Design skill carries [portable application guidance](../../../skills/architecture-design/SKILL.md) for projects with their own layout; it does not require this repository's directory to exist after installation.
