---
id: rem:reference:kruchten
type: reference
source_type: research-paper
publication_year: 1995
repository_year: 2020
evidence_family: kruchten-4plus1
method_metadata: ../metadata.md
---

# Kruchten Architectural Blueprints The 4 1 View Model

## Key takeaway

Complementary views answer different architectural questions, and the set can be tailored.

## Summary

The original 4+1 paper describes logical, process, development and physical views, related through scenarios. REM uses it as a concern-driven starting point rather than requiring five separate deliverables for every change.

## Current inspection and use limit

Consolidation inspection on 2026-10-07 rechecked manuscript pages 12–13 in text: mappings, tailoring, iterative process and scenario-driven discussion. No new visual-inspection claim is made. The 2020 repository upload is distinct from the 1995 publication.

## Publication identity
Philippe Kruchten. *Architectural Blueprints—The “4+1” View Model of Software Architecture*. IEEE Software 12(6), 42–50, November 1995.

[Repository record](https://arxiv.org/abs/2006.04975) · [Inspected manuscript](https://arxiv.org/pdf/2006.04975).

The arXiv deposit is dated 2020. The filename uses the original publication year, not the repository upload year.

## Located contributions

IEEE Software 12(6), 1995, pp. 42–50; author-deposited manuscript, especially Mapping between views, manuscript pp. 10–12, and Tailoring the model, manuscript p. 13. DOI 10.1109/52.469759.

Original complementary-view proposal; mappings between concerns need not be one-to-one, and useless views can be omitted. Its logical view and internal scenario walkthroughs are adapted, not copied as REM’s stakeholder Scenario semantics.

Text on manuscript page 12 discusses non-one-to-one logical/development mappings. Page 13 permits omission of unhelpful views and combined descriptions when appropriate; it also presents iterative and scenario-driven development. REM retains material concern coverage when tailoring. This source is a design-process example, not a universal phase sequence.

## Scope and independence
A practitioner architecture model illustrated through systems examples. It is separate from Parnas’s decomposition argument and from NASA guidance, although concepts overlap. Neither overlap nor publication prestige proves REM’s effectiveness.

## What it does not establish
No obligation to create a diagram merely to fill a slot, no one-to-one mapping between responsibilities and deployment units, and no right to infer runtime order from structural dependency lines. The last prohibition is an REM reasoning safeguard: reachability alone leaves scheduling underspecified.

## REM use

The [Architecture model](../models/architecture-design.md#generated-41-architecture-views) establishes source and view authority; [Architecture views](../methods/architecture-views.md) selects concern coverage. [View presentation](../methods/view-presentation.md) assesses source fidelity and reader tasks. REM’s projection and review procedures remain authored synthesis.

## Inspection provenance

Retained S11 record: Primary source inspected on 2026-10-06; mapping and tailoring passages rechecked on 2026-10-07. This note identifies limited supporting reasoning, not approval of REM or its implementation. REM links to the publication without redistributing its text or figures.

The incoming reference supplied by the user reports access on 2026-10-07. Its previous inspection extent was reported as: selected full-text view/mapping/tailoring sections; manuscript pages 12–13 visually inspected. Its current extent was reported as: primary paper PDF and page image. These are attributed reports from the incoming document, not independent evidence that this consolidation performed those inspections. The adopted inspection scope is stated above.

[Method edition and KPS basis](../metadata.md) · [Claim-to-reference map](../SOURCES.md)
