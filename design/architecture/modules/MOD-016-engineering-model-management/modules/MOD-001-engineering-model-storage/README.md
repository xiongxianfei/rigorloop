# Definition storage and current knowledge

[MOD-001](module.json) owns definition, identity-reference and recorded-rationale custody through [IF-001](../../../../interfaces/IF-001-engineering-definition-access/interface.json). MOD-003 supplies interpretation and candidate findings through [IF-002](../../../../interfaces/IF-002-engineering-model-interpretation-and-identity-checks/interface.json); MOD-002 prepares revisions and MOD-004 presents the resulting knowledge. This is proposed Design for SR-001–005 and existing AR-001–009, with the same single accountable owners. A structurally accepted save is not engineering approval or a satisfaction judgment.

## Selected state, membership and identity

A request identifies the governed project/model, selected state or current-state selection, declared profile and requested subject/scope. Stable entity identity designates an entity; it does not designate its revision, physical path or the model state. Bind a current selection once to immutable captured membership/content, or acquire it under the model-wide read exclusion defined by [the shared capture contract](../MOD-004-engineering-context-and-traceability/traversal.md#admission-and-coherent-inventory). Never reselect current separately for identity, definition, references and rationale.

Capture the profile-declared complete identity-bearing membership before claiming unique resolution or absence. Names, types and paths are attributes, not alternatives to identity. Distinct records sharing an identity remain ambiguous; matching display names with different identities are valid. An unavailable collection or unparseable identity-bearing record prevents a complete uniqueness or absence conclusion, even if the visible portion has one match. A derived index is keyed by model, state, profile and membership/content identity; it is disposable and cannot conceal stale or omitted members.

MOD-001 obtains raw retained bytes and their profile declaration before calling MOD-003. IF-002 interprets only supplied inputs and exposes the applicable governing definitions or exact resolvable references, without recursively retrieving its own interpretation context. Unknown or unavailable profiles do not select a newer fallback. Return available attributable content with the precise affected scope; distinguish absence in a completely inspected state from unsupported interpretation, unavailable state, partial acquisition and failed access.

Current definitions are read directly from their owning model files. Required current references and associated rationale use the same captured state. No Change replay, original chat, agent memory or operational store is a prerequisite. Historical Baselines use their original interpretation through their separately owned [state-control design](../../../MOD-017-engineering-governance/state-control.md); unavailable requested history is not replaced by current content.

## Confirmed definition and rationale retention

The caller supplies an explicit authorized save or same-entity revision, expected base, exact candidate, selected profile and required write scope. MOD-002 owns revision intent; MOD-001 alone owns acceptance and retained effects. Supported profile/shape, complete identity and any affected reference/containment checks come from IF-002 against the complete resulting candidate, including unchanged entities on which those checks depend. Preliminary author checks cannot replace the storage-owned final checks.

Use the shared local filesystem custody mechanism already selected for relationship retention: stage complete candidate bytes separately; hold model write exclusion through final base/profile/authority comparison, candidate checks, publication and actual-effect inspection. Candidate identity includes membership and content, not just the edited record. Coherent readers use matching exclusion or a proven immutable snapshot. Advisory locking does not control arbitrary external editors; if required custody cannot be maintained, withhold confirmation and coherent affected reads rather than claiming repeated scans establish atomicity.

Before the first authoritative change, durably record the base, candidate identity, affected members and intended resulting membership in an owned unresolved-write marker outside authored model membership. Persist and flush required candidate content and directory metadata under the qualified filesystem protocol. Publish the exact supplied content at its owning locations, preserving unaffected material. Confirm a save only after readback establishes the complete requested resulting membership/bytes and the unresolved marker can be durably resolved. A temporary buffer, successful parser check or process-local cache is not confirmed retention.

Session exit and elapsed time do not delete accepted definitions or still-relied-on reasoning. New sessions reopen retained files and reconstruct derived indexes. Storage hosting and disaster recovery are outside this contract; supported platform durability must be qualified before a runtime claims it. The design neither assumes a Git commit is a save nor substitutes MOD-011's operational database for the engineering model.

<!-- architecture-diagram: retain-current-knowledge -->

```d2
shape: sequence_diagram
caller: "Authorized caller\nRevision owner when applicable"
store: "Definition storage\nMOD-001"
rules: "Interpretation and validation\nMOD-003"
files: "Retained model files and\nowned recovery metadata"
caller -> store: "IF-001: exact candidate, expected base and authority"
store -> store: "Stage candidate; acquire model write exclusion"
store -> rules: "IF-002: check actual complete candidate and profile"
rules -> store: "Return scoped findings bound to candidate identity"
store -> files: "Persist unresolved-write marker before publication"
store -> files: "Publish and durably retain requested members"
store -> files: "Read back exact resulting content and membership"
store -> files: "Resolve marker only after confirmed complete effects"
store -> caller: "Return retained state or known incomplete effects"
```

The sequence shows confirmed retention, including a combined definition/rationale write where required. A rejected candidate has no accepted effect. A failure before or during publication reports known effects and unresolved scope. After interruption or restart, a durable unresolved marker blocks coherent affected reads and further writes until the storage owner inspects exact before/candidate/current bytes and membership. Foreign or ambiguous content stops reconciliation; no blind retry, assumed rollback or overwrite of intervening edits is allowed. A confirmed save survives lost response delivery; the caller reads actual state before reconciling another request. The marker is custody metadata, not a permanent activity history.

## Recorded rationale and its association

Rationale remains engineering content under its owning model, using the existing source-qualified references and retained Markdown sections or decision documents. It is not an operational Review or a new REM Decision entity. A definition's existing source/locator fields identify the owned rationale section. Preserve its recorded context, chosen outcome, rationale, alternatives and consequences; an explicitly recorded absence of considered alternatives is distinguishable from an unrecorded field. Keep the section and its documentary association accessible while current definitions rely on it, regardless of whether the originating Change explanation is compacted.

The author supplies the following association information in the owning rationale section or associated documentary table: governed model and entity identity, exact definition-content identity and declared profile, rationale locator, author/decision owner, declared application scope and the basis for considering the reasoning applicable to that definition. The captured read result additionally binds the exact rationale bytes and selected model state. A qualified profile adapter or participant-assisted read supplies these normalized values to IF-001; if a representation cannot provide them, return an unsupported or unresolved association instead of guessing. This defines the documentary content and semantic exchange, not a new public machine schema or automatic semantic assessor.

Avoid recursive identity construction. First finalize the candidate definition, including its stable source/locator reference; compute the exact content identity of those candidate definition bytes. Then prepare the rationale section and association referring to that identity/profile. The definition reference identifies the section by locator, not by a hash of the section that in turn contains the definition hash. Capture the rationale's own content identity and the combined resulting model identity as output observations outside the hashed members. Stage and retain the complete combined write set under the same acceptance boundary. A required reference missing from the candidate cannot receive confirmed complete accessible-rationale status.

On a definition edit, the old association remains attributable to its original content/profile. Stable entity identity or an unchanged title cannot renew applicability. The responsible author may explicitly retain the reasoning after inspecting the change, recording the new definition-content association, actor and reason; otherwise current applicability is unresolved or the reasoning is shown as historical only. Retention preserves that supplied basis without certifying decision correctness. A changed rationale section is captured under its actual bytes; it cannot borrow the earlier section's identity or approval.

If a rationale document must move or a definition reference changes, reconcile both in the candidate. The source-reference change alters definition content and therefore needs a correctly recomputed association. Required current reference closure is validated before complete retention. Retirement of still-relied-on rationale requires explicit dependency disposition under SR-024; a missing operational Change, expired session or old file date is not a retirement decision. No operation invents missing reasoning from unrelated history.

## Current reading and separate context outcomes

<!-- architecture-diagram: read-current-knowledge -->

```d2
shape: sequence_diagram
reader: "Later-session reader"
views: "Views and traceability\nMOD-004"
store: "Definition storage\nMOD-001"
rules: "Interpretation and validation\nMOD-003"
reader -> views: "Select entity and current or retained state"
views -> store: "IF-001: acquire one coherent state and identity scope"
store -> rules: "IF-002: interpret captured content and profile"
rules -> store: "Return governing definitions and explicit gaps"
store -> views: "Return resolved content, references and rationale basis"
views -> views: "Separate definition, required context and rationale outcomes"
views -> reader: "Present current meaning and recorded limits without replay"
```

[MOD-004's presentation contract](../MOD-004-engineering-context-and-traceability/README.md#current-definition-and-rationale-presentation) owns the result the reader sees. Storage retains independent outcomes for content availability/completeness and rationale availability/applicability. A complete definition with unavailable rationale stays accessible; if reasoning is required for explanatory context, that context remains incomplete. Missing optional history does not invalidate complete current content. A good diagnostic is not a fabricated definition or a judgment of satisfaction.

## Realization and acceptance intent

The proposed local model engine reuses MOD-001 acquisition/custody, MOD-003 pure interpretation/checking, MOD-002 candidate editing and MOD-004 derived projection. The existing engine design selects Rust components; these model services are logical responsibilities within that realization, not separate deployments. Files under the owning engineering-model directories remain authoritative; private staged writes and recovery metadata stay outside model membership. Derived indexes and browser output are rebuildable. This refines the existing filesystem storage choice without adopting operational SQLite, a hosted service or a new external authoring command.

The participant-facing save/revision/rationale requests are the existing logical IF-001 inputs with explicit state and authority. A callable command or editor adapter requires separate compatibility and implementation qualification. The currently generated browser can display the Design and source references; it does not thereby implement these model-write services or full normalized rationale retrieval. Schema validity, Design review and actual runtime verification remain separate.

| Scenario / allocation | Required Design observation |
| --- | --- |
| SCN-005 then SCN-001; SR-001 / AR-001–002 | Confirm exact checked retained bytes, end the caller session and retrieve the same identity/type/content in a later session. Selected state/profile and failures remain explicit. |
| SR-002 / AR-003–004 | Check all required identity-bearing members; distinguish blank or duplicate identity, equal names with distinct IDs, complete absence, ambiguity and incomplete inspection. |
| SCN-002; SR-003 / AR-005 | MOD-002 preserves identity across supported name/content/location edits; inspect the complete moved subtree and unchanged reference scope, reject target collision or changed base, and report uncertain publication truthfully. |
| SCN-003/004; SR-004 / AR-006–007 | Read current content and required references without Changes or private memory; expose missing required context separately from optional unavailable history. |
| SCN-006 then SCN-003/004; SR-005 / AR-008–009 | Retrieve all five recorded reasoning fields with their exact association; retain current reliance after Change cleanup and show missing or stale rationale without fabrication or automatic renewal. |
| Interruption, competing writer or lost save response | Persist affected uncertainty across restart, withhold false coherent success and reconcile actual bytes/membership before retry. |

The direct IR-001 outcome is a later participant who can identify the current obligation, capability, behavior or responsibility and inspect its applicable recorded reasoning without the original conversation. Walk both an intact current model and one with missing required context: understandable complete knowledge and an explicit bounded gap are distinct correct outcomes. Stable identity, selected-state fidelity and selective retention support this outcome; counts of files or allocated ARs do not establish it.
