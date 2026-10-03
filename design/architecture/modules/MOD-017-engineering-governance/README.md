# Change and quality control composition

[MOD-017](module.json) owns handoff, authority and assessment meaning. [Operations](../MOD-018-engineering-operations/README.md) composes guidance, CLI and storage. These are target design rules; installed workflow adoption and runtime implementation remain separate.

## Gate and work-state semantics

Maintain a current structured handoff, not an activity history. Milestones describe checked progress and dependencies, with no mandatory reviewer or approval field. Optional interim advice remains advisory. After implementation there is one independent whole-change Code Review gate, followed by distinct final Verify. Corrections and reassessment stay within the same gate; a gate does not require permanent copies of every attempt.

The current handoff identifies goal/scope/authority, governing basis, progress, open issues and important rationale, relevant evidence, review standing, and next action with reason. Each fact has one owner. The context projection does not maintain its own editable approval or infer authority from a next-step suggestion. [Change control](modules/MOD-006-engineering-change-control/README.md#resume-and-progress) owns resumption interpretation.

## Review subjects and retained basis

The reviewer owns the conclusion, assessed scope, governing obligations, accountable provenance, limitations and unresolved findings. Retain enough support to understand a conclusion still being used; summaries often suffice. Full console logs and source copies are optional unless their actual bytes are necessary for a decision or selected preservation obligation. Earlier failed development runs need no records merely because they happened.

Review preparation is current input. It is not approval and cannot silently replace the assessed basis of a conclusion. The current assessment can be replaced by an explicit independent reassessment after corrections while retaining open obligations and useful support. Original approved scope remains identifiable when that approval is still being relied upon. Once superseded and no longer needed, intermediate detail may be compacted. No universal Candidate archive or predecessor chain is required.

Evidence reports identify procedure, relevant scope/basis, result, limitations and source. Distinguish an engineer's report of no subsequent changes from an actual defined comparison. File names, timestamps, status labels and digests alone do not establish relevance, meaning, adequate inspection or independent judgment. Git is an optional source of context, not required authority.

### Changes after approval

| Change affecting a currently relied-on conclusion | Required response |
| --- | --- |
| Demonstrably harmless wording/formatting or equivalent collection retry | Responsible engineer records the scope and cumulative impact rationale; retain approval without another review gate. |
| Material behavior, requirement, Interface, test expectation or supporting evidence change | Return to its owner, perform relevant checks and independently reassess affected scope/interactions in the same gate. |
| Missing comparison basis, unknown impact or contradictory evidence | Expose uncertainty and withhold unsupported current reliance. |
| Superseded working output with no remaining decision value | Replace or discard it without an activity-history entry. |

Assess effects, not file types or edit counts. A smoke-test pass cannot hide a different integration failure. Updating working evidence must not rewrite what a reviewer concluded from an earlier basis: keep a concise assessment-owned support summary or obtain a replacement assessment. Open findings survive omission and newer clean judgments until explicit attributable disposition. Resolved details may later be compacted when no current decision needs them.

The [Records owner](../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md#updating-current-state-without-losing-decision-meaning) owns representation; [CLI](../MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/README.md#record-an-assessment-finding-or-reliance-decision) owns task inputs. Update handoffs at meaningful decision changes or transfers, not after each edit or command. Mutability does not transfer reviewer authority to the implementer.

## Whole-change review and correction

The sequence shows the normal whole-change assessment and closeout dependency. Actor roles are not separate deployed services. Change control supplies context and authority interpretation; Review and verification supports assessment, while the named reviewer and verifier make the judgments.

<!-- architecture-diagram: whole-change-review-and-correction -->

```d2
shape: sequence_diagram
implementer: "Implementation\nowner"
route: "Coordination\nroute"
reviewer: "Independent\nCode Reviewer"
verifier: "Final Verify\nassessor"
records: "Command handling and\nWork record storage"
implementer -> route: "Complete required work/checks and declare review scope"
route -> records: "review prepare: select the scope and governing basis"
records -> route: "Return the prepared review scope"
route -> reviewer: "Request whole-change review of the prepared scope"
reviewer -> records: "review show: read the basis and outstanding findings"
records -> reviewer: "Return scope, current issues and supporting summaries"
reviewer -> reviewer: "Inspect selected files and assess the whole change"
reviewer -> records: "review record: update judgment and explicit applicability"
records -> reviewer: "Confirm the current review standing"
reviewer -> route: "Return applicable approval for the complete current candidate"
route -> verifier: "Request distinct final Verify with current evidence"
verifier -> verifier: "Assess whether evidence supports the completion claim"
verifier -> records: "verification record: save current acceptance support and rationale"
records -> verifier: "Confirm the actual committed Verify result"
verifier -> route: "Return the supported final Verification reference"
route -> records: "change complete: declare closeout within existing authority"
records -> route: "Confirm recorded completion and its verification basis"
```

Review records the independent conclusion and explicit applicability for the complete delivered scope. Missing or adverse conclusions remain visible; persistence success grants no approval. Verify separately assesses acceptance support, and change complete records the compact historical outcome within existing authority. No milestone review or new closeout approval is introduced.

### Correct and reassess

<!-- architecture-diagram: correct-and-reassess -->

```d2
shape: sequence_diagram
reviewer: "Independent\nCode Reviewer"
records: "Command handling and\nWork record storage"
route: "Coordination\nroute"
owner: "Responsible\ncorrection owner"
reviewer -> records: "Record actionable findings against inspected scope"
records -> reviewer: "Confirm the actual committed findings"
reviewer -> route: "Return findings and required outcomes"
route -> owner: "Assign corrections to the proper owner within authority"
owner -> owner: "Correct the subjects and perform relevant checks"
owner -> records: "review prepare: update current scope after checks"
records -> owner: "Confirm the actual committed correction result"
owner -> route: "Return revised scope and affected interactions"
route -> reviewer: "Request material-change reassessment in the same gate"
reviewer -> records: "review show: read revised basis and earlier support"
records -> reviewer: "Return scope, open issues and retained support"
reviewer -> reviewer: "Inspect material corrections and affected interactions"
reviewer -> records: "review record: update assessment and explicit applicability"
records -> reviewer: "Confirm the actual committed reassessment"
reviewer -> route: "Return the current judgment and its applicability"
```

An implementation defect returns to implementation; changed requirements/design return to their author and review owners. Independent reassessment may update the same current Review. Preserve unresolved findings, relevant support and adequate whole-change coverage; do not require all prior attempts or automatic rereading/rerunning of unaffected material. Unchanged-subject evidence collection retries do not automatically restart Code Review.

Concurrent submissions carry the inspected operational revision. Stale writes require rereading and explicit reconciliation; atomic persistence protects current state without a permanent version history. Interrupted transaction recovery establishes known storage outcomes and never replays engineering decisions.

## Completion and later corrections

Completion records what changed, why, delivered scope, actual review and verification support, exclusions and limitations. Selected attachments are retained only where useful. The account contains enough acceptance meaning to stand independently of disposable working records.

A completed Change is an immutable historical declaration, not a live assertion about today's system. Stop repository applicability comparisons for closed Changes. Later regression becomes a new problem or Change linked through the request source. If the original assessment itself was mistaken, append an attributable explanatory note without silently rewriting the original account. Closed work is not automatically reopened; external publication retains separate authority.

## Adoption and recovery

FUNC-078 prepares an explicit adoption disposition for the selected project and active Changes. Inputs include the current contract, exact work/evidence bases, target package/record compatibility, affected consumers and authority. The result lists which obligations are reused, which require renewed review, which work remains blocked, and which original evidence must be retained. It is not an automatic stage translation.

Adoption has preparation, physical replacement and activation decisions, without adding engineering review gates. Before replacement, retain a recoverable current contract and required original records. Verify candidate identity and complete selected compatibility. Installation performs only its supported bounded units and reports actual effects; it does not promise atomic whole-project rollback. Activation is permitted only when installed guidance, canonical policy, validators and selected recording support agree for the affected scope and the inspected active-work basis is still current.

On partial replacement or interruption, stop affected dependent operations and report which contract is actually intact. Reuse the earlier workflow only where all required earlier components remain compatible and available. Otherwise expose an unavailable workflow until explicit recovery or completed replacement; do not continue using a mixture or infer that rollback succeeded. Preserve unrelated work and historical evidence throughout. Two local agents racing adoption must not activate different interpretations against one unchanged work revision.

The database migration can precede or follow workflow adoption only when its own compatibility and preservation prerequisites are met. A transitional supported persistence backend may carry the successor semantic contract without SQLite; no speculative backend or command is advertised as supported. SQLite does not itself satisfy the workflow migration, and workflow adoption does not erase backup/restore or historical-byte obligations.

The [successor record contract](../MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/README.md#adoption-and-compatibility) settles activation granularity: one guarded transaction per selected Change. Project-wide success requires current activation for the complete explicitly selected set; partial activation is reported as partial, without converting unrelated work or promising a multi-Change atomic commit. The [installation extension](../MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/README.md) supplies exact replacement effects. V4 rollout qualifies the specified adapter over the existing filesystem transaction engine. SQLite migration is independently scheduled; only one backend is authoritative at a time, and active dual writes or fallback are forbidden after retirement.

## Verification intent

[The parent-owned test design](test-design.md) defines the adoption interactions that can fail despite child conformance. [Operations](../MOD-018-engineering-operations/README.md) owns handoff cooperation and its assurance boundary.
