# Independent representations can diverge

Identity: `rem:principle:representations`.

## Key takeaway

Agreement between separately maintained representations is a condition to maintain, not a property of having similar names.

## Summary

When the same engineering fact appears in several mutable places, an update to one place does not logically update the others. Derivation, reconciliation or another explicit maintenance mechanism is needed when agreement matters. A derived copy or historical snapshot can be useful without becoming another authoritative owner.

## Statement and explanation
Suppose a responsibility is reassigned in a design table but its old owner remains in a diagram. Both documents can remain well formed while their meanings disagree. A generated view can also be stale if it was generated before the change or interpreted the source incorrectly.

## Source basis and REM synthesis

The possibility of disagreement follows from independent updates. [W3C PROV-Overview](../references/w3c-2013-prov-overview.md#located-contribution) supplies background on attribution and derivation. It does not prove that one database or generation alone ensures correctness. REM's [representation model](../models/README.md#representation) separately selects one authoritative representation per semantic fact.

## Applications
Within REM, maintained links, deliberate projections, replicas and reviewed snapshots retain the declared authoritative source for each fact. A concern-specific view can repeat a subset of facts for comprehension, provided its authoritative basis and update responsibility remain intelligible.

## Limits
Historical snapshots are intentionally different from current definitions. A summary can legitimately omit irrelevant detail without contradicting the canonical source. Byte equality is therefore neither required nor sufficient for semantic agreement. Authority can be distributed across named owners rather than one physical store.

## Challenge
Compare the meaning and selected state, not only hashes or identifiers. If generation changes a relationship or omits a condition essential to the reader’s decision, the output is inadequate even when reproducible.

## Deeper knowledge
[Knowledge, projection and presentation](../methods/view-presentation.md); [Evolution model](../models/README.md#evolution); [Architecture Views](../methods/architecture-views.md); [Engineer a change](../practices/engineer-a-change.md).
