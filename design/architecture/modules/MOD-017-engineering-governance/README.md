# Change and quality control composition

[MOD-017](module.json) owns cooperation among Change control, Assurance and Authoring guidance. Child records retain direct Function, state and AR ownership. These design rules address SR-079–083 and are maintained directly here as the design evolves. Implementation and customer workflow adoption remain separately evidenced. Cross-parent cooperation belongs to the [architecture composition](../../README.md#requirement-first-workflow-composition).

## Gate and work-state semantics

Milestone state describes planned/active/completed/blocked work and its checks; it contains no mandatory reviewer assignment or approval reference. Milestone completion requires the recorded scope and required checks to be complete, with known defects explicitly addressed. A blocked dependency blocks affected work; unrelated authorized work need not become a separate approval cycle.

A formal gate is identified by the selected Change and assessment purpose. A whole-change gate remains the same gate across candidate corrections. Each assessment attempt has its own identity, reviewer provenance, exact candidate subjects, governing basis, judgment, findings and rationale. Its predecessor/correction links explain renewed assessment without overwriting earlier subjects. Advisory feedback has separate scope and cannot become an approved formal attempt by relabeling it.

The current approval is an explicit applicability conclusion for the complete current candidate, not the attempt with the latest timestamp, a global clean flag or an inherited approval attached to stable file names. A candidate identifies affected code, tests, configuration, migrations, generated outputs, skills and documentation, including relevant additions and deletions. Repository revision alone is insufficient for a dirty or partially selected checkout; supported subject inspection must bind the actual content and dependency scope.

## Whole-change review and correction

[Change control's resume-and-progress design](modules/MOD-006-engineering-change-control/README.md#resume-and-progress) supplies attributable work context and authority analysis. The interaction below owns the cooperation of that contribution with assurance and the independent assessment roles. Record access denotes the supported Command handling and Work record storage boundary; actors submit explicit results rather than asking persistence to choose judgments. The first sequence shows a complete candidate receiving applicable approval and a distinct Verify assessment. The second isolates the correction exchange. Each sequence names responsible roles; it does not introduce new deployed services. Change control supplies context and authority analysis, and Review and verification supplies evidence-applicability support to the independent assessor. Runtime placement and implemented commands require their own implementation observations.

<!-- architecture-diagram: whole-change-review-and-correction -->

```d2
shape: sequence_diagram
implementer: "Implementation\nowner"
route: "Coordination\nroute"
reviewer: "Independent\nCode Reviewer"
verifier: "Final Verify\nassessor"
records: "Command handling and\nWork record storage"
implementer -> route: "Complete the implementation scope and required checks"
route -> reviewer: "Request whole-change review of the exact current candidate"
reviewer -> reviewer: "Assess requirements, design, delivery and interactions"
reviewer -> records: "Record the candidate, basis, approval and coverage"
records -> reviewer: "Confirm the actual committed review result"
reviewer -> route: "Return applicable approval for the complete current candidate"
route -> verifier: "Request distinct final Verify with current evidence"
verifier -> verifier: "Assess whether evidence supports the completion claim"
verifier -> records: "Record the scoped Verify result and rationale"
records -> verifier: "Confirm the actual committed Verify result"
verifier -> route: "Return the supported completion result"
```

Implementation reaches this handoff after its complete agreed scope and required checks are ready; milestone completion alone does not invoke this gate. Coordination inspects current context and authority before each dependent handoff. The reviewer and Verify assessor use Review and verification (MOD-007) for evidence-applicability support; those roles own the judgments. The diagram's successful path assumes approval and completion are supported. Findings instead follow the correction sequence below; failed or inconclusive Verify cannot be reported as completion.

### Correct and reassess

<!-- architecture-diagram: correct-and-reassess -->

```d2
shape: sequence_diagram
reviewer: "Independent\nCode Reviewer"
records: "Command handling and\nWork record storage"
route: "Coordination\nroute"
owner: "Responsible\ncorrection owner"
reviewer -> records: "Record findings against the inspected candidate"
records -> reviewer: "Confirm the actual committed findings"
reviewer -> route: "Return findings and required outcomes"
route -> owner: "Assign corrections to the proper owner within authority"
owner -> owner: "Correct the subjects and perform relevant checks"
owner -> records: "Record changed subjects, evidence and correction links"
records -> owner: "Confirm the actual committed correction result"
owner -> route: "Return the revised candidate and affected interactions"
route -> reviewer: "Request reassessment within the same whole-change gate"
reviewer -> reviewer: "Assess corrections and complete-current-candidate coverage"
reviewer -> records: "Record a new assessment; preserve earlier attempts"
records -> reviewer: "Confirm the actual committed reassessment"
reviewer -> route: "Return the current judgment and its applicability"
```

The correction exchange can repeat without creating another gate. An implementation defect returns to implementation; changed requirements or architecture return to their upstream owners and applicable upstream review before renewed downstream reliance. The correction owner cannot approve their own repair. Reassessment covers the changed subjects and affected interactions, with justified reuse of unaffected support; it does not require a mechanical reread of every unchanged file. Optional interim advice has no whole-change approval authority. A one-milestone Change still has one whole-change review gate.

Each handoff relies on current subjects, authority and an actual reconciled recording outcome. Record conflicts or uncertain commitment require rereading and reconciliation before reliance, as described in [Change control](modules/MOD-006-engineering-change-control/README.md#resume-and-progress). Verify cannot repair and approve an engineering defect itself. A collection retry without engineering changes repeats the affected verification; new contrary evidence returns applicability to the assessment owner. [Operations' existing SCN-079–081 groups](../MOD-018-engineering-operations/test-design.md) retain the integrated proof intent; rendering this interaction does not establish that proof.

Concurrent actors may produce observations or attempts, but a decision offered for a stale candidate cannot silently settle the current gate. An update carries the inspected work/record basis and preserves unrelated facts. On conflict, the caller rereads relevant context and explicitly re-evaluates the decision; it does not replay stale intent against a fresh revision automatically. A late adverse observation remains visible even if another actor previously recorded approval. Contradictory evidence returns to the assessment owner before renewed reliance.

## Adoption and recovery

FUNC-078 prepares an explicit adoption disposition for the selected project and active Changes. Inputs include the current contract, exact work/evidence bases, target package/record compatibility, affected consumers and authority. The result lists which obligations are reused, which require renewed review, which work remains blocked, and which original evidence must be retained. It is not an automatic stage translation.

Adoption has preparation, physical replacement and activation decisions, without adding engineering review gates. Before replacement, retain a recoverable current contract and required original records. Verify candidate identity and complete selected compatibility. Installation performs only its supported bounded units and reports actual effects; it does not promise atomic whole-project rollback. Activation is permitted only when installed guidance, canonical policy, validators and selected recording support agree for the affected scope and the inspected active-work basis is still current.

On partial replacement or interruption, stop affected dependent operations and report which contract is actually intact. Reuse the earlier workflow only where all required earlier components remain compatible and available. Otherwise expose an unavailable workflow until explicit recovery or completed replacement; do not continue using a mixture or infer that rollback succeeded. Preserve unrelated work and historical evidence throughout. Two local agents racing adoption must not activate different interpretations against one unchanged work revision.

The database migration can precede or follow workflow adoption only when its own compatibility and preservation prerequisites are met. A transitional supported persistence backend may carry the successor semantic contract without SQLite; no speculative backend or command is advertised as supported. SQLite does not itself satisfy the workflow migration, and workflow adoption does not erase backup/restore or historical-byte obligations.

The [successor record contract](../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md#atomic-publication-and-adoption) settles activation granularity: one guarded transaction per selected Change. Project-wide success requires current activation for the complete explicitly selected set; partial activation is reported as partial, without converting unrelated work or promising a multi-Change atomic commit. The [installation extension](../MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/README.md) supplies exact replacement effects. V4 rollout qualifies the specified adapter over the existing filesystem transaction engine. SQLite migration is independently scheduled; only one backend is authoritative at a time, and active dual writes or fallback are forbidden after retirement.

## Verification intent

[The parent-owned test design](test-design.md) defines the adoption interactions that can fail despite child conformance. [Operations](../MOD-018-engineering-operations/README.md) owns handoff cooperation and its assurance boundary.
