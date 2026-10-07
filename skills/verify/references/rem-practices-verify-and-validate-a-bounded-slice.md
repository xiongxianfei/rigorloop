<!-- Generated from rem/practices/verify-and-validate-a-bounded-slice.md; source SHA-256 0ad0b33fddccf315d0fb3a0c5fb7ba65741519bf75d12a0ea581fa4ad7e436b6. Edit the owning REM source. -->

---
id: "rem:practice:assessment"
type: "practice"
basis_kind: "REM-authored synthesis; current REM rules apply; sources qualified below"
---

# Verify and validate a bounded slice

## Key takeaway

Determine separately whether obligations are appropriate, whether the product meets them and whether intended use succeeds.

## Summary

This Practice combines assessment planning, evidence gathering and review for one bounded engineering outcome. It works before implementation as a planning activity and after implementation as an evidence-based evaluation. It never equates a completed template, accepted risk or planned test with product success.

## Goal and inputs
Use the current need, obligations, proposed or actual product, operating assumptions and relevant evidence. Identify the configuration and actual assessment/acceptance authority. A bounded slice is one outcome with enough participating behavior to examine its real interaction—not necessarily one isolated component.

**Requirements validation** asks whether the obligation is appropriate. **Product verification** asks whether the identified product satisfies it. **Product validation** asks whether intended use succeeds under the relevant conditions. Keep these objects explicit whenever using the words “verify” and “validate.” Model conformance is another bounded question: parentage, Scenario ownership, coverage, allocation and representation checks can establish compliance with model rules, not the appropriateness of obligations or the product’s actual outcome.

## Stage map
1. Frame claim, scope and authority.
2. Review the obligation and planned coverage.
3. Gather evidence at the available maturity.
4. Judge applicability and intended use.
5. Decide follow-up and preserve the record.

## Stage 1 — Frame the assessment
### Stage summary
**Goal:** know what is being assessed. **Why:** evidence is meaningful only relative to a claim and conditions. **Do:** state need, obligation, configuration and assumptions. **Observe:** hidden scope changes. **Success:** a bounded assessment question. **Next:** review criteria.

Write the proposition whose truth matters, not just a requirement identifier. Identify the relevant system/build and operating conditions, including the fault model or workload when material. Find who can authorize assessment and decide acceptance. Record parts unavailable for inspection or execution.

**Fallback:** an unspecified claim or unidentifiable configuration calls for clarification, not a generic “pass/fail” run.

## Stage 2 — Review obligation and coverage
### Stage summary
**Goal:** assess the right question by a credible approach. **Why:** accurate measurements can answer an irrelevant question. **Do:** review necessity and criteria, then select inspection, analysis, demonstration or test. **Observe:** proxy substitution and missing interactions. **Success:** justified coverage. **Next:** execution or a plan-only output.

Check the obligation against the need and assumptions. Define expected observations and meaningful violations before seeing results. Include normal, boundary and consequential failure conditions. Explain why component checks are sufficient or which integration checks remain necessary. For intended use, identify representative users, environment and acceptable assistance.

**Fallback:** do not manufacture thresholds or user preferences. Obtain them, state a proposal, or narrow the conclusion.

## Stage 3 — Gather evidence
### Stage summary
**Goal:** preserve what was actually established. **Why:** expected results cannot substitute for observation. **Do:** execute authorized safe work or retain the plan. **Observe:** anomalies and deviations. **Success:** evidence with known provenance. **Next:** evaluate applicability.

Confirm readiness and safety. When an assessment is performed, record actual configuration, conditions, inputs, procedure, observations and departures. Preserve unfavorable results. An analytical argument can count as evidence only with premises, Model and limitations available for review.

If implementation is unavailable, identify risks and keep product-execution procedures as plans. Performed inspection or analysis may still support a bounded design claim, with its actual subject, premises and limits; it cannot establish an unobserved implementation result. A procedure merely written for future use establishes assessment preparedness, not satisfaction. Never create a sample “passed” output that resembles an actual execution record.

**Fallback:** if the planned conditions cannot be reproduced safely or the evidence cannot be captured reliably, stop execution, preserve the plan and select a justified alternative assessment or narrower claim.

## Stage 4 — Evaluate conclusions and intended use
### Stage summary
**Goal:** make only the conclusion supported. **Why:** same identifier or successful part does not guarantee applicability. **Do:** compare evidence, conditions and need. **Observe:** contradictions and missing stakeholder context. **Success:** a qualified judgment. **Next:** follow-up decision.

Check whether observations meet the criteria, whether assumptions held and whether important coverage is absent. Separate a failure in design from invalid test setup or a requirement problem. For intended-use validation, ask whether the relevant outcome is achieved, not merely whether internal outputs look correct.

Example: valid content retained by Store does not establish that a reviewer selects the reviewed release. Conversely, a user succeeding with an ad hoc workaround may not establish the specified product obligation. Document both distinctions.

**Fallback:** resolve anomalies, collect further evidence, restrict the claim or revise the need/design. Do not average away a contradictory result.

## Stage 5 — Decide and preserve meaning
### Stage summary
**Goal:** keep decisions and evidence distinct. **Why:** acceptance can include uncertainty. **Do:** state supported scope, residual risk, authority and next action. **Observe:** waiver described as satisfaction. **Success:** an inspectable current judgment and preserved history. **Next:** release, further work or reassessment.

Record the actual decision-maker and decision when known. Keep an unmet requirement visible even if use is authorized under a waiver. Preserve evidence and its configuration so later changes can be assessed for applicability. Connect revised requirements and design assumptions back to the assessment plan.

## Troubleshooting and current summary
If a claimed pass has no performed assessment, reclassify it as a plan; performed inspection or analysis does not require product execution to support its own scoped conclusion. If evidence is for an old configuration, examine applicability. If reviewers dispute success, first compare claim meaning and criteria. Current summary fields are optional prose: what was assessed; actual evidence; supported scope; unresolved conditions; decision; next work.

## Basis and limits

NASA [verification](https://github.com/xiongxianfei/rigorloop/blob/main/rem/references/nasa-2016-systems-engineering-handbook.md#product-verification) and [validation](https://github.com/xiongxianfei/rigorloop/blob/main/rem/references/nasa-2016-systems-engineering-handbook.md#product-validation) support the assessment distinctions and reporting concerns. [Zave/Jackson](https://github.com/xiongxianfei/rigorloop/blob/main/rem/references/zave-jackson-1997-four-dark-corners.md#located-claims-and-inspected-extent) explains conditional satisfaction; [W3C PROV](https://github.com/xiongxianfei/rigorloop/blob/main/rem/references/w3c-2013-prov-overview.md#located-contribution) supports provenance descriptions. The operational composition is REM-authored. Specialized assurance and approved procedures remain project obligations. Deeper: [Assurance model](rem-models-README.md#assurance), [Verification](rem-methods-plan-and-assess-verification.md), [Intended-use validation](rem-methods-validate-stakeholder-outcomes.md) and [Worked assessment plans](rem-practices-WORKED-EXAMPLE.md#assessment-plans).
