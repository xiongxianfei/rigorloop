# Allocation consistency and potential impact

MOD-004 owns the read-only results of FUNC-010 and FUNC-011 under SR-010 and SR-011. AR-060 allocates rule-based responsibility assessment and AR-061 allocates potential-impact composition. This is proposed Design, separate from runtime availability and from the [selected requirement evaluations](requirement-evaluation.md) supplied by actual reviewers.

## Logical boundary and shared state

An engineering participant supplies a selected model/state, declared profile and an explicit analysis request to MOD-004. MOD-004 owns logical admission, analysis and presentation of the result. The two operations below are logical contracts, not callable command spellings. No MOD-010 call, new engine-protocol operation or expansion of IF-013 is implied. A future external adapter must have its own reviewed consumer boundary and preserve all outcomes.

MOD-001 supplies coherent membership and content through IF-001 and MOD-003 supplies exact-profile interpretation through IF-002. Reuse the coherent read basis defined in [traversal](traversal.md#admission-and-coherent-inventory): current-state selection is bound to an immutable read, not repeated unlocked scans. Every observation carries the model/state/profile and membership/content identity, or explains which could not be established. No cross-state or cross-project stitching is permitted. Known partial observations survive only when attributable to the same established state.

Allocation inspection must be able to explain invalid or unfinished allocations. IF-002 diagnostic interpretation therefore supplies unambiguous known identities, typed facts and field-specific interpretation gaps without requiring a fully valid model. A missing allocation is an observation, not an invitation to fabricate one. Unparseable content, ambiguous identity and unknown profile/rules leave the affected scope incomplete. This does not weaken checked-write admission or turn interpreted fragments into accepted definitions. Existing storage AR-002/004/006 and interpretation AR-010 keep those contributions; no duplicate provider obligations are introduced.

## Allocation request and rule basis

`assess_allocation` receives:

- the selected model/state/profile and either all applicable allocation subjects or an explicit AR/Function subject set;
- identifiable declared allocation and consistency rules, with their exact source content and applicability predicates;
- declared lifecycle applicability, permitted deferral rules and any recorded deferral with its entity, source, responsible actor, scope and applicable conditions;
- acquisition/interpretation completeness and any declared unmodeled architecture or constraint scope.

Rules come from the selected profile and its explicitly adopted project constraints. Caller input identifies those rules; it cannot invent a weaker substitute. An explicitly narrower rule/subject selection is retained as such and cannot produce a whole-model claim. There is no implicit newest profile or hard-coded assumption that Draft means inactive. If the declared lifecycle applicability or rule interpretation cannot be established, the relevant subject is unassessed. Unsupported rule forms cannot be executed as supplied code or silently ignored.

The minimum interpreted rule operations are required primary-owner cardinality, allowed owner kind, stated deferral eligibility, and a declared comparison predicate on an AR owner and constrained Function owner. Supported comparison predicates are owner equality and declared Module containment ancestry where the selected rule explicitly chooses it. More complex semantic rules remain engineering-review-needed unless independently supported by the interpreter. A rule records whether it is applicable and which comparison direction is intended. Merely discovering different owner IDs is not a deciding predicate. Conflicting declared rules remain a reported rule-basis conflict unless their authoritative precedence is explicit; MOD-004 does not choose one opportunistically.

The assessment inventories all selected applicable ARs and Functions, their allocation facts, all relevant AR-to-Function constraints, and the Module identities/containment required by the selected rules. A Function can be the target of an incoming constraint authored elsewhere; required source membership must include those possible sources even for a small subject selection. Dependencies outside the requested subjects may be inspected to decide their findings, but are labeled supporting context rather than silently added assessed subjects.

Complete acquisition proves what definitions and facts are present in the declared model; it does not prove that all desired architecture has been modeled. Missing architecture or declared missing relevant constraint scope is explicitly unassessed/incomplete. An AR need not constrain a Function, and an intentionally empty constraint set is not invented into an error. Where a rule requires a constraint or the selected design declares it unfinished, its absence prevents a complete consistency conclusion. If the selection has no applicable subjects, report that fact and the applicability scope; never label an empty unmodeled architecture consistent.

## Allocation result and algorithm

For each selected subject, first establish applicable rules and identity resolution. Then inspect primary-owner cardinality and target kind. For each relevant AR-constrains-Function fact, retain both `AR → Module` and `AR → Function → Module` paths, their authored provenance, each target resolution and the deciding rule identity/content source. Missing or ambiguous steps stay visible in the path rather than disappearing through graph normalization.

A missing required allocation is a violation only when applicability, complete relevant scope and the deciding obligation are established. Preserve an explicitly permitted deferral as Deferred, naming the rule, recorded disposition and responsible follow-up; it is neither invented allocation nor completed allocation. An absent or out-of-scope deferral cannot override a deciding rule. When deferral eligibility is itself unknown, report review-needed/incomplete rather than assume permission. The profile's nondeferable duties remain nondeferable.

The per-subject result contains original selection, subject identity, applicable rule identity and source, observed typed paths, finding, reason, affected scope and any deferral or review question. Findings are:

| Finding | Meaning |
| --- | --- |
| Consistent | The stated decidable rule holds over complete relevant interpreted facts. This is scoped mechanical consistency only. |
| Violated | A stated applicable rule is demonstrably false; retain the deciding facts and exact rule. |
| Deferred | An identified declaration is permitted by the applicable rule and its conditions; the unresolved responsibility remains visible. |
| Review needed | Facts are available but engineering meaning or an undecidable/conflicting rule prevents a mechanical conclusion. |
| Incomplete | Required membership, architecture, interpretation, constraint or resolution is unavailable; preserve any attributable known findings. |
| Not applicable | A declared applicability rule excludes the subject; show that rule rather than silently drop the entity. |

Overall acquisition completeness, evaluated-scope completeness and findings are separate. The result lists every requested subject and every uncovered portion. Only a nonempty fully evaluated applicable scope with no violation, deferral, review question or gap may be summarized as mechanically consistent under its selected rules. A known violation remains visible even if another part is incomplete; counts do not discard negative findings. A fully inspected scope may legitimately contain review questions or deferrals without being a completed allocation set. No result creates an AR, moves a Function, grants approval or concludes requirement satisfaction.

An invalid request (unknown operation, unsupported request vocabulary, mixed model/state, or definitely nonexistent explicit subject) is Rejected with actionable scope diagnostics. Unknown profile/rule interpretation is Unsupported/Incomplete, not a false violation of an invented rule. Identity ambiguity in acquired subjects remains an incomplete finding. Cancellation or resource exhaustion reports the inspected and uninspected subjects; a lost response establishes no completed assessment. There is no hidden subject-count cutoff or latency promise.

Implementation of this design uses an indexed typed fact inventory and a deterministic iteration ordered by stable subject, rule and relationship identities. Rule decisions operate on recorded facts and explicit missingness, not traversal success alone. Keep provenance alongside unresolved fields. Parent ancestry comparison must detect cycles or missing ancestry; it cannot decide the predicate using a corrupted chain. Repeated paths are derived once, while each distinct applicable rule retains its own result.

## Potential-impact request and traversal composition

`assess_potential_impact` receives a nonempty set of proposed changed-entity identities, one selected model/state/profile, an explicit influence selection, and optional depth/entity-count limits. An influence selection is a nonempty finite set of allowed `(relationship type, traversal orientation)` pairs. Orientation is outgoing or incoming; a caller's “both” expands to both pairs. A uniform direction across selected types is the ordinary traversal special case. An empty influence selection, unknown types or orientations, malformed limits and mixed selections reject before exploration. Missing or ambiguous changed identities cannot become an empty successful impact result.

MOD-004 normalizes the influence selection once and applies it at every traversed edge. It reuses the pure breadth-first kernel from FUNC-009/AR-056 with the selected eligible-edge predicate. Combining separately completed traversals by type is not equivalent: a valid path can alternate types and orientations. The kernel must explore the one combined selected graph to preserve such paths, finite cycles and minimum depths. This internal reuse does not change IF-013's uniform-direction request contract.

The result retains the original changed subjects, normalized influence selection, exact state/profile/content basis and requested/effective limits. For every potential-impact candidate, retain at least one finite witness from an identified changed subject, with all intermediate identities, original typed edge orientations, traversal orientations and authored provenance. Deterministic multi-source breadth-first witnesses are sufficient. Do not claim a complete set of causes or a path from every changed subject to each candidate.

Changed subjects are listed separately as seeds with depth zero. The candidate list comprises returned reachable entities outside that seed set. A seed reached again through a cycle remains a selected changed subject; the returned edge subgraph preserves the relationship, but it does not create a duplicate candidate. Depth zero therefore yields no additional candidates and an explicit bound when further exploration was excluded; it is not proof that the proposed change has no effects. Entity-count limits include the distinct seeds, exactly as in traversal, and a count below the seed count rejects.

Ordinarily MOD-004 invokes its traversal kernel within the same bound analysis. If a caller supplies reusable traversal support, admit it only when the original starts, model/state/profile, content and membership identity, normalized influence pairs and all requested limits match exactly, and its producer/schema semantics are supported. Confirm every returned candidate's witness against that inventory and influence selection. A matching label or list of vertices cannot establish traversal completeness; accept Complete only from the trusted same-engine result with established acquisition/exploration guarantees, otherwise recompute or reject unsupported provenance. Foreign, narrower, broader, stale or merely similar results cannot be relabeled for this analysis. An ordinary IF-013 result can only match the uniform influence special case.

## Potential-impact outcomes

| Outcome | Meaning |
| --- | --- |
| Complete potential-impact scope | Traversal acquisition and exploration are complete for the exact influence graph; every returned candidate has an admitted witness. The result is still potential impact for engineering review. |
| Bounded potential-impact scope | Explicit traversal bounds limited exploration. Preserve the effective boundary and omitted/uninspected frontier, including seed-only results. |
| Incomplete potential-impact scope | Acquisition, interpretation, traversal or witness composition failed, was interrupted or exhausted resources. Preserve only attributable, validated partial witnesses and identify missing or unresolved scope. Incomplete takes precedence over a concurrent requested bound. |
| Rejected | A definite request or supplied-support mismatch prevents analysis. Report the mismatch and original selection; do not substitute another scope. |

An empty candidate list can be qualified as “No additional relationship-based potential impact beyond the selected change subjects in this fully explored influence scope” only for Complete. It never means no real-world effects or complete dependency knowledge. Empty Bounded/Incomplete results retain their limitation prominently and cannot be reported as no-impact. Missing eligible references propagate traversal incompleteness. All results identify excluded relationship families/domains by their explicit selection or known omissions; the system does not invent unrecorded dependencies to fill those gaps.

A reached Implementation or Evidence reference is a candidate for attention, not proof of behavior change, invalidation, stale verification, required tests or permission to modify anything. MOD-007's assessment authority and domain owners retain those judgments. These results do not write requirement status, operational review decisions or model relationships. A later state needs a fresh analysis; earlier witnesses preserve their original meaning.

## Cooperation, realization and design observations

The [registered responsibility diagram](README.md#allocation-and-impact-responsibilities) shows two result owners within MOD-004 sharing state capture and interpretation. Allocation needs the complete applicable inventory and diagnostic facts; it cannot be implemented by following only a starting neighborhood. Impact reuses traversal's eligible-edge exploration, not its result as an unqualified list.

Within the proposed shared local Rust engine, keep allocation analysis and potential-impact composition as pure components alongside traversal and view projection. MOD-001 retains I/O and coherence; MOD-003 retains profile interpretation. Allocation operates over indexes of identities, allocations, constraints, rules and explicit gaps. Impact supplies its normalized edge predicate to the shared traversal kernel and validates witness/result binding before presentation. These are intended source responsibilities, not claims that new files or a callable engine operation exist. No database, persistent inverse graph, D2 dependency, new process or network service is required by either analysis. Reader visualizations may consume the derived results later without taking analysis authority.

Transient indexes and results may be reused only for exact model/state/profile/membership/content and rule/influence identities. They are discardable; no derived fact becomes authoritative. The same storage exclusion and read-state guarantees apply regardless of physical process placement. Unsupported custody or exhausted resources remain incomplete. Public adapter/serialization adoption, performance qualification and runtime implementation remain separate work, while this logical boundary is fully specified.

SCN-009's ordinary path composes selected obligations, known owners and decisive rules into attributable findings. Its alternative of differing responsibility without a deciding rule yields Review needed; unfinished architecture yields Incomplete. SCN-010's ordinary path yields witnessed candidates; its bounded and missing-reference alternatives preserve traversal limits; absent/ambiguous changes or mismatched support reject. Neither Scenario is rewritten with internal design details.

| Criterion | Design inspection case |
| --- | --- |
| SR-010 C1 | Active AR/Function missing required owner; permitted deferral; unknown activity or deferral eligibility. Confirm separate violation, deferral and incomplete/review outcomes. |
| SR-010 C2 | An AR constrains a Function with different owners. Retain both exact paths and the selected deciding rule or its absence. |
| SR-010 C3 | Equality rule makes different owners a violation; an explicitly allowed ancestry rule may admit different owners; no deciding predicate yields Review needed. |
| SR-010 C4 | Missing architecture, hidden incoming constraint sources, interrupted membership and declared unfinished constraints prevent a complete consistency claim; known violations survive beside gaps. |
| SR-010 C5 | Mechanically consistent declared facts remain distinct from complete architectural allocation, semantic adequacy and satisfaction. |
| SR-011 C1 | Branching/cyclic multi-source graph yields each non-seed candidate once with an exact finite witness from a named changed subject, without all-causes attribution. |
| SR-011 C2 | Alternating selected relationship types/directions are traversed in one eligible graph. Changed state, starts, influence or limits reject supplied support; unrelated nodes never become established impact. |
| SR-011 C3 | Complete seed-only reachability yields qualified no-additional-impact; depth-zero or incomplete empty exploration does not. |
| SR-011 C4 | Requested bounds, missing target, cancellation, resource exhaustion and witness-composition failure propagate their exact scope without a completeness upgrade. |
| SR-011 C5 | Reached evidence/implementation remains potential impact for review and never changes applicability or outcome judgments automatically. |

These observations guide independent Design assessment and later verification. They are not executed runtime tests or claims that the requirements are implemented.
