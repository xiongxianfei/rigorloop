---
schema: compact-decisions-v1
decisions:
  <decision-id>:
    decision_id: <decision-id>
    source:
      kind: <finding|issue>
      id: <source-id>
    decision: <durable-decision>
    rationale: <why-this-remains-constraining>
    affected_surfaces:
      - <surface>
    owner: <responsibility>
    applicability: <applicable|retained-pending-decision>
    applicable_since: sha256:<64-lowercase-hex>
---

# Material Decisions

The front matter is authoritative. Do not create this file when no material decision remains applicable.
