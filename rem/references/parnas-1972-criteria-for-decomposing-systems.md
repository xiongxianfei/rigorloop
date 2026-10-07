---
id: rem:reference:parnas
type: reference
source_type: research-paper
publication_year: 1972
evidence_family: parnas-information-hiding
method_metadata: ../metadata.md
---

# Parnas On the Criteria To Be Used in Decomposing Systems into Modules

## Key takeaway

A decomposition can localize likely changes when it hides the design knowledge those changes affect.

## Summary

The paper compares two decompositions of an example system. REM draws on its reasoning about information hiding and changeability. It is not evidence that a particular number of Modules, containment depth or allocation rule is universally correct.

## Current inspection and use limit

Retained REM inspection on 2026-10-06 covers the decomposition criterion on printed pages 1056–1057. This consolidation preserves that bounded source claim; it does not assert a new PDF or visual inspection.

## Publication identity
D. L. Parnas. *On the Criteria To Be Used in Decomposing Systems into Modules*. Communications of the ACM 15(12), 1053–1058, December 1972.

[Inspected academic-hosted copy](https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf).

## Located contribution

CACM 15(12), 1972, pp. 1053–1058; decomposition criterion pp. 1056–1057; DOI 10.1145/361598.361623.

Original design argument and worked comparison on hiding change-sensitive decisions. Not a controlled demonstration that every module hierarchy or encapsulation rule is beneficial.

The incoming reference additionally points to the decomposition comparison and “Changeability” on pp. 1055–1056, and reports visually inspecting p. 1056. These are attributed reading and inspection reports; the retained REM inspection above is the adopted basis.

## Evidence character
An analytical argument using a worked software example, not a randomized comparison across engineering organizations. It provides a mechanism to examine: which consumers know which decisions, and what changes when a hidden decision changes.

## Scope and limits
The argument depends on meaningful interfaces and on an informed expectation of change. No boundary removes all coupling. Excessive indirection or a wrong prediction of volatility can make a proposed decomposition unattractive. These cautions guide REM analysis; they are not a measured effect-size claim.

## What it does not establish
The paper does not require REM Module identity, a parent rule, a maximum depth, an immutable-ID implementation or one Module per Function. It does not prove that all future changes can remain local.

## REM use
[Boundary choices shape change propagation](../principles/boundary-choices-shape-change-propagation.md) and [Architecture allocation](../methods/architecture-allocation.md) turn the change-locality question into a comparison of candidate responsibility boundaries. The worksheet is REM-authored, not the paper’s procedure.

## Inspection provenance

Retained S10 record: Primary source inspected on 2026-10-06. This note identifies limited supporting reasoning, not approval of REM or its implementation. REM links to the publication without redistributing its text or figures.

The incoming reference supplied by the user reports access on 2026-10-07. Its previous inspection extent was reported as: selected comparison and criteria sections; printed page 1056 visually inspected. Its current extent was reported as: primary paper PDF and page image. These are attributed reports from the incoming document, not independent evidence that this consolidation performed those inspections. The adopted inspection scope is stated above.

[Method edition and KPS basis](../metadata.md) · [Claim-to-reference map](../SOURCES.md)
