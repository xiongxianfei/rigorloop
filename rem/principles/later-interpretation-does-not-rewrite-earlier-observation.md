# Later interpretation does not rewrite earlier observation

Identity: `rem:principle:history`.

## Key takeaway

A revised explanation can change today’s conclusion without changing what was observed under yesterday’s conditions.

## Summary

A record of an observation, an interpretation of it and a current reliance decision serve different purposes. Keeping their meanings distinguishable allows corrections and learning without falsely implying that earlier reviewers had later information.

## Statement and explanation
An earlier test may have passed its stated criterion. Later work can reveal that the criterion omitted a failure mode. The original result remains a result of that earlier test; the broader confidence should change. Correcting an inaccurately recorded observation is also possible, but the correction and reason should remain attributable when the history matters.

## Source basis and REM synthesis

[NASA verification](../references/nasa-2016-systems-engineering-handbook.md#product-verification) identifies conditions and discrepancies; [PROV-Overview](../references/w3c-2013-prov-overview.md#located-contribution) discusses attribution, versioning and derivation. Separating earlier observations from later interpretation is REM's synthesis. It does not prescribe an event-store architecture; REM's [Evolution model](../models/README.md#evolution) preserves historical engineering meaning beyond observations alone.

## Applications
Reassess old evidence after requirement, interface or implementation changes. Preserve the old context and explain why reliance is retained, narrowed or withdrawn. Maintain a concise current explanation so a reader need not reconstruct the whole change history just to understand today’s design.

## Limits
Historical retention has privacy, security and cost constraints. This Principle does not demand endless retention, byte-for-byte duplication of every transient file or one version-control product. Select what is needed to justify actual reliance and comply with project obligations.

## Challenge
A current document that says an obsolete conclusion “was always false” without explaining the newly learned condition can obscure the real lesson. A history that cannot identify its subject is equally weak.

## Deeper knowledge
[Evolution model](../models/README.md#evolution); [Engineer a change](../practices/engineer-a-change.md); [Review an existing system](../practices/review-an-existing-system.md).
