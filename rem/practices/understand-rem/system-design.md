# 3. System Design

## 3. System Design

REM System Design is built from the [Feature and Function concepts](../../concepts/system-and-architecture.md#system-and-architecture-assets), the [enduring-need explanation](../../principles/needs-can-outlive-solutions.md) and [shared clarity rule](../../models/operational-support.md#clear-engineering-definitions), and the [System Design model](../../models/system-design.md).

The essential structure is:

```text
IR ── confirms ──────> Feature
Scenario ─exercises──> Feature
SR ── confirms ──────> Function
Feature ─realizedBy──> Function
```

### Why Feature exists

A Feature is durable because one stakeholder-visible capability can be exercised through many Scenarios over its lifetime.

For example:

```text
Feature: Engineering Knowledge Search

Scenario: find by identifier
Scenario: search by text
Scenario: filter by requirement type
Scenario: agent discovers related architecture
```

The Scenarios may change or become obsolete while the Feature retains its identity.

### Why Function exists

A Function represents logical system behavior rather than a requirement statement or implementation component.

The SR establishes what the system must satisfy.
The Function expresses the behavior the system performs to satisfy that obligation.

[Clear engineering definitions](../../models/operational-support.md#clear-engineering-definitions) connects naming to engineering meaning.
The [System Design model](../../models/system-design.md#clear-names-and-boundaries) defines Feature and Function clarity criteria. [Scenario Analysis](../../methods/scenario-analysis.md#step-1--confirm-or-reuse-the-feature) applies them to capabilities, [Requirement Analysis](../../methods/requirement-analysis.md#derive-system-requirements) derives the SR obligations, and [Functional Analysis](../../methods/functional-analysis.md) confirms the Functions those SRs require.
The [Operational Support model](../../models/operational-support.md#naming-and-location) separately owns representation choices such as deriving filenames from an ID and title.

[Requirement Analysis](../../methods/requirement-analysis.md#derive-system-requirements) owns SR derivation.
[Functional Analysis](../../methods/functional-analysis.md) owns confirmation and boundary definition of Functions from those SRs and reconciliation of Feature realization.

---
