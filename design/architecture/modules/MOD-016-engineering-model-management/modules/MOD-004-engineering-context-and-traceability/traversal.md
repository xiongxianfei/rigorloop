# Scoped relationship traversal

MOD-004 owns FUNC-009 and AR-056 under SR-009. This proposed design completes the SCN-008 relationship-reading collaboration. The selected requirement and Function remain authoritative; this document defines their architectural realization. It does not describe implemented traversal or an assessment of implementation.

## Boundary and responsibility

MOD-016 provides [IF-013](../../../../interfaces/IF-013-scoped-engineering-relationship-traversal/interface.json) to MOD-010. MOD-010 owns request admission at its public boundary and presentation of the returned result; MOD-016 owns the composed contract. MOD-004 performs traversal. MOD-001 supplies state-bound identity/content through IF-001; MOD-003 interprets the selected profile through IF-002. The parent contract does not create a second Function, AR or owner of child state.

IF-007 remains selected-state inspection for Baseline analysis. IF-012 remains architecture snapshot generation, comparison and recovery. A traversal result neither retains a Baseline nor publishes a browser artifact. IF-001 and IF-002 stay internal to Project model; adding an Operations consumer to the parent contract does not expose them wholesale.

AR-056 is necessary because owning FUNC-009 alone does not state the lower-level obligation to preserve complete, bounded and incomplete traversal meaning at MOD-004's result boundary. Storage AR-002/004/006 and interpretation AR-010 remain applicable to their existing selected-scope completeness, identity, references and profile guarantees; no duplicate AR is created for the same guarantee. Browser-specific AR-043 is not treated as a complete general-traversal obligation. The collaboration below explains how those reused guarantees supply the required inventory.

## Admission and coherent inventory

A request supplies one project/model and selected state, its declared profile, one or more start identities, a nonempty set of profile-defined relationship types and one direction: outgoing, incoming or both. Optional limits are maximum depth and maximum returned entity count. Unknown names or directions, malformed limits and conflicting state references reject before consistency-dependent exploration. Starts must resolve uniquely; absent or ambiguous starts reject with the affected identity and scope. No default direction or alternate Baseline is substituted.

Selecting current means the model's coherent state at admission, not an endlessly changing live graph. MOD-001 binds that selection to a consistent immutable read basis before MOD-004 explores it. An existing immutable state/export is directly usable. A current-state provider must establish a consistent snapshot, or model-wide read exclusion while acquiring the selected membership and bytes; before/after timestamps or an unlocked directory scan are insufficient. If the provider cannot establish this basis, return incomplete acquisition with its cause. This selects a required storage capability, not a new persistent Baseline, storage engine or guarantee that today's repository tools already provide it.

IF-001 capture enumerates the full profile-declared model membership and authoritative relationship-bearing content within the selected state. Member digests alone do not establish that an omitted member does not exist. Completeness must cover enumeration and required reads. The full inventory is needed even for a single start: an incoming edge can be authored on a previously unrelated entity. Requests selecting relationship types still require the complete inventory of possible sources for those types. A supplied arbitrary subset cannot be relabeled a complete model; either acquire the declared complete membership or report incomplete acquisition.

MOD-003 interprets the captured bytes using that same state/profile through IF-002. MOD-001's interpreted retrieval may already supply that result; MOD-004 must reuse its bound interpretation rather than mix it with another profile or re-read live sources. Unsupported definitions, uninterpretable required relationship-bearing content and incomplete identity scope remain explicit. Completeness of an acquired inventory, structural validity and engineering adequacy are different conclusions.

An acquisition failure before starts can be established returns incomplete, not a claim that the starts are absent. A confirmed absent or ambiguous start in an adequately inspected scope is rejected. Known observations may be retained only if attributable to the same established read state; otherwise the result has no admitted observations and identifies the unresolved acquisition scope.

## Graph and traversal semantics

The interpreted graph consists of stable entity identities and typed authored edges. Each edge retains its original source, relationship type, target, source member and field/containment provenance. Parentage comes from the profile's authoritative containment representation. Incoming adjacency is derived by reversing traversal orientation over those same edges; it is not authored a second time. Changing only direction changes exploration, never the stored source/target fact.

The request's relationship types and direction apply uniformly to every step. Outgoing follows source to target, incoming target to source, and both admits either traversal orientation. Self-edges and cross-domain cycles are permitted when the governing profile permits those relationship types. A requirement-parent cycle remains a structural defect; discovering it cannot be disguised as a harmless cross-domain cycle or used to certify valid parentage. Report the defect and affected incomplete scope.

MOD-004 performs deterministic multi-source breadth-first exploration. Unique starts, adjacency entries and ties are ordered by stable identity and typed edge identity. Starts have depth zero. Discovery assigns each entity its minimum hop distance from any start; one request fixes state, types and direction, so the visited key is selected-state identity plus entity identity. Enqueue each entity once at first discovery. Retain encountered eligible edges even when their targets are already visited, so deduplicating visits does not erase cycle/back-edge relationships.

For a finite inventory and no requested boundary or interruption, queue exhaustion establishes all reachable entities under the selected types and direction. There is no hidden depth or result-count default. Material resource exhaustion returns incomplete; it cannot be relabeled a successful implicit cap. After index construction and deterministic ordering, traversal-phase work is proportional to admitted vertices and eligible edges. Acquisition, interpretation and sorting add their own work; memory holds inventory/adjacency, visited entities, frontier and retained edges; this is an algorithmic design, not a measured latency or capacity promise.

The result represents supporting paths finitely. It returns the traversed typed edge subgraph and a predecessor witness for each discovered non-start entity, from which finite start-to-entity paths can be reconstructed. Original edge orientation and traversal orientation remain distinguishable. It does not enumerate every possible cyclic walk. For bounded traversal, edges beyond the requested exploration boundary are not presented as explored; retained frontier diagnostics name any observed excluded edge without making its target a returned entity.

## Limits and outcomes

Maximum depth is a nonnegative integer. Depth zero returns the admitted starts and does not expand their adjacency. A depth N request expands only entities whose minimum depth is below N, retaining eligible edges reached from those expansions and entities up to depth N. Multi-source minimum depth prevents an entity first reachable along a longer path from hiding descendants within a shorter start's boundary.

Maximum entity count includes the distinct starts and must be at least their count. Smaller values reject with the minimum needed to represent the request. Results use deterministic breadth-first order. Reaching the count alone does not prove that additional entities exist: continue only the inspections needed to establish queue exhaustion or the next eligible unseen entity. If another entity would exceed the bound, stop the requested selection and expose that excluded frontier; do not claim unrestricted reachability. Requested depth and count compose by applying both; report which boundary actually prevented exploration and retain both requested values.

Acquisition completeness and exploration outcome are separate fields in the logical result. Every result retains the original request, selected state/profile, captured membership/content identity when established, returned entities/edges, bounds and diagnostics. Before any positive result, all required inventory and interpretation must be complete and coherent.

| Outcome | Meaning and required disclosure |
| --- | --- |
| Complete | Admitted request, complete required acquisition/interpretation and exhaustive exploration without an effective requested boundary. Report requested limits even if they did not exclude anything. Only this outcome establishes unrestricted reachability for the selected types/direction. |
| Bounded | The explicit depth or count selection was fulfilled and an effective boundary prevented unrestricted exploration. Identify requested/effective bounds and omitted or uninspected frontier. Fulfilled requested selection is distinct from full reachability. |
| Incomplete | Acquisition, interpretation or exploration is unavailable, interrupted, invalid in relevant scope or resource-limited. Identify the phase, affected member/path/frontier and reason; retain only attributable partial observations. This takes precedence over a simultaneous requested bound. |
| Rejected | A definite admission error such as missing/ambiguous start, unknown type/direction, invalid bound or mixed project/state/baseline. Identify the request defect and correction needed; do not substitute another request. |

At a depth boundary, unrestricted completeness may be claimed only if the complete inventory independently proves that no additional eligible reachability was excluded; otherwise the result is Bounded with boundary adjacency uninspected. A completely explored start with no eligible edges is Complete with no related entities beyond the starts. Missing references, absent adjacency due to incomplete capture, or interrupted inspection can never produce that empty-complete conclusion.

An unresolved target on an eligible traversed edge yields Incomplete with its authored provenance and affected path. Defects outside the requested relationship scope do not invent reachable entities; if they prevent interpreting the required inventory or establishing source membership, acquisition remains incomplete. A lost execution response cannot establish Complete: MOD-010 reports unavailable/incomplete execution with the original request identity. A later retry is a new explicit read of a selected state, never a silent mix with prior partial results.

## Logical and Process views

The owning [Logical and Process diagrams](README.md#general-traversal-views) show IF-013 composition and state-bound traversal interaction.

## Development and Physical realization

Use one pure traversal component over the shared engine's interpreted model representation, with a request-bound inventory, forward/inverse index and breadth-first frontier. Keep acquisition and state binding in the storage contribution and profile interpretation in its existing contribution. Within the proposed Rust engine crate, the traversal component sits beside projection and returns typed derived data before any browser-specific layout or serialization. The existing finite Requirements tree remains a consumer presentation grammar; it is not the traversal algorithm and must not be reported as full SR-009 realization.

This read component requires no D2 invocation, output publication, new service or persistent inverse relationship store. The Node adapter may call the Project model boundary through a separately qualified operation in the selected engine protocol; this logical design does not assign a CLI command spelling or modify the supported operation catalogue. Any callable protocol extension must preserve IF-013's admission/outcome distinctions and the current browser protocol's compatibility. The component can run in the existing proposed engine process with bounded caller-controlled cancellation; source read consistency remains a provider responsibility regardless of process placement.

A transient read snapshot/index is discarded with the request. A reusable immutable inventory may be shared only under the exact state/profile/membership identity; changing state invalidates it. Memory or acquisition limits are failures to complete that scope, not undocumented request truncation. No runtime implementation, storage technology adoption or product qualification is claimed here.

## Scenario walkthrough and criterion coverage

SCN-008 remains the stakeholder-facing Scenario. Its ordinary, alternative and failure outcomes map to this cooperation without adding internal details to the Scenario record.

| SR-009 criterion | Design obligation and inspection case |
| --- | --- |
| 1: all reachable entities | Complete selected inventory and unrestricted breadth-first queue exhaustion. Inspect a chain longer than any UI expansion convention and branching requirement ancestry/descendency; all reachable identities and witness paths remain present. |
| 2: reverse facts | Derived inverse adjacency preserves authored provenance. Inspect an incoming edge authored outside the starting neighborhood; changing only direction finds it without a second authored reverse edge. |
| 3: cycles | Visited minimum-depth entities plus retained typed cycle edges. Inspect a cross-domain cycle, self-edge and multiple starts with different path lengths; termination retains reachability. A requirement-parent cycle receives its own structural diagnostic. |
| 4: requested bounds | Explicit depth/count rules and deterministic prefix/frontier. Inspect depth zero, a shallower second start, cap equal to start count, invalid smaller cap, combined bounds and exhaustion before a requested cap. Bound fulfillment never silently means unrestricted completeness. |
| 5: incomplete results | Separate acquisition/exploration outcomes with affected scope. Inspect omitted source membership, missing eligible target, unreadable required content, interruption and resource exhaustion; none returns complete empty. |
| 6: admission | Exact selected-state and profile validation. Inspect absent/ambiguous starts, unknown type/direction, invalid limit and mixed model/Baseline identities; no fallback scope is used. |

These are design review and later verification observations, not executed tests or satisfaction claims. MOD-004 owns traversal outcome proof; MOD-001 owns coherent membership/content acquisition, MOD-003 owns interpretation, and MOD-010 owns preserving the composed request/result meaning. The integrated observation must exercise those contributions together before any system verification claim. Impact analysis, automatic requirement evaluation and general allocation adequacy remain separate responsibilities.

## Internal analysis reuse

[Allocation and potential-impact analysis](allocation-and-impact.md) retains its own result obligations in AR-060/061. Potential impact reuses the pure breadth-first kernel with a normalized finite set of permitted relationship-type/orientation pairs. The ordinary traversal request expands its selected types and uniform direction into that set; its existing IF-013 admission and result meaning stay unchanged. An internal impact invocation can choose different directions by type, applying the resulting eligibility predicate at every edge in one exploration. Splitting by type and unioning results would miss mixed-type paths. Exact request/state/limit binding and all existing acquisition, witness, cycle and completeness invariants remain mandatory. This internal composition introduces no new public IF-013 operation or supported engine protocol.
