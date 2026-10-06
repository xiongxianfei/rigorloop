<!-- Generated from rem/methods/validate-stakeholder-outcomes.md; source SHA-256 0437ec639bfeb71aaf33a3cebd4e2d05913400035f342a24fb286bfc5934b917. Edit the owning REM source. -->

# Assess intended-use outcomes

## Purpose and basis

Assess whether a solution supports an identified stakeholder outcome in its intended or explicitly representative context.
This differs from conformance to specified criteria, addressed by [verification](rem-methods-plan-and-assess-verification.md).
It also differs from checking whether a requirement statement is clear and assessable during [Requirement Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md).
[NASA Product Validation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/sources/S05.md) supports assessing intended use against stakeholder expectations; REM selects the procedure below without claiming compliance with NASA's process.

## Inputs

Identify the stakeholder need and applicable governed [Scenario](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/scenarios.md), expected outcome, subject maturity and version, intended environment, stakeholder representatives and assessment authority.
Keep each governed Scenario's existing owning IR and primary Feature; a broader evaluation can assess several separately identified Scenarios.
Use the existing evidence and applicability rules from the [assurance model](rem-models-README.md#assurance).

## Procedure

1. Select the stakeholder outcome and situation, including relevant failure or degraded conditions. Explain whose outcome is being assessed.
2. Establish observable success criteria with the appropriate stakeholder representative before judging the result. Record assumptions and uncertainties in those expectations.
3. Select an appropriate model, prototype or product and assessment technique. Identify participants, environment and differences from intended operation. Early analysis or prototypes support only the questions and maturity actually assessed.
4. Plan the assessment and conduct it when the required subject, authority and conditions exist. Retain actual observations and anomalies; distinguish representative use from an author-only walkthrough.
5. Compare observations with the agreed outcome. Distinguish a product defect, inadequate assessment setup, mistaken requirement, changed need and insufficient evidence.
6. Record an attributable, scoped judgment, unsupported outcomes, limitations and corrective owner. A verification pass cannot fill a missing intended-use observation.
7. Reconcile changed needs through [Requirement Analysis](https://github.com/xiongxianfei/rigorloop/blob/main/rem/methods/requirement-analysis.md#analyze-the-rr-against-current-needs). Correct the responsible source and reassess affected outcomes; do not rewrite old success criteria to turn failure into success.

## Outputs and completion

Produce the intended-use assessment plan, actual observations if performed, conclusion against stakeholder expectations and unresolved corrective work.
Use existing [Operational Support](https://github.com/xiongxianfei/rigorloop/blob/main/rem/models/operational-support.md#engineering-knowledge-and-operational-records) for representation and retention.
The record must make verification and intended-use conclusions separately understandable even when one activity supplies evidence for both.

Completion means the declared outcome has an adequately supported judgment or an explicit unestablished result with its next evidence need.
This method adds no universal workflow gate, mandatory stakeholder meeting, numeric usability threshold or permission to execute external actions.

## Example and limits

A representative maintainer attempts to identify the Module accountable for an unfamiliar behavior using an exported architecture view.
Agree beforehand what constitutes a correct identification and explanation, and record help required or misleading presentation.
The [worked example](rem-practices-engineer-change-WORKED-EXAMPLE.md#assessment-plans) plans this activity but contains no observed participant results.
Fictional outcomes and a designer's expectation cannot establish actual stakeholder success.
