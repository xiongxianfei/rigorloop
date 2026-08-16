# Architecture-review recording and settlement

Use this procedure only when the universal skill has established durable recording. Loading it grants no recording location, artifact settlement, automation, correction, or workflow authority.

## Recording placement and modes

For `advisory-durable`, write only to an explicit valid user path or project-authorized standalone evidence location. Do not create a governed root, formal review log, review resolution, lifecycle entry, artifact settlement, automation evidence, or workflow continuation. If no location resolves, preserve the complete judgment and findings in the result, report `recording_status: blocked`, and create no governed state.

For `formal-lifecycle`, require one exact governed change root and valid review-evidence placement. Write the review record before any settlement, synchronize the formal review log, and create or update review resolution only when findings or governing policy require it. Recording failure performs no target settlement.

Workflow-managed automation additionally requires current formal authority, reviewer independence, a neutral review packet or equivalent phase evidence, and bounded correction authority owned elsewhere. It returns control to workflow after recording and settlement; it does not advance routing.

For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

## Review identity

Every formal occurrence binds separate `review_subject`, `governing_basis`, and ordered optional `settlement_targets`, plus review ID, round, record path, and review-log path.

The governing basis identifies the governing specification path and content identity, approving spec-review identity, applicable architecture-assessment receipt, accepted proposal or decision basis when relevant, architecture-method contract path and identity, and repository revision.

A canonical-package subject identifies the exact canonical Markdown, linked diagram sources, related reviewed ADRs, and their content identities. A standalone ADR subject identifies the exact ADR, current canonical linkage, and content identity.

The no-impact subject binds the exact assessment receipt and proposal or specification basis. The proposal/spec-gap subject binds the exact upstream artifacts and architecture question or conflict. Both record-only surfaces use an empty settlement-target set and never create or settle a rationale, architecture, or ADR lifecycle entry. A direct formal record-only review without one stable subject identity blocks recording or remains advisory; never create an identity-free formal occurrence.

Judgment reuse requires the same subject, governing basis, ordered settlement targets, semantic status, review ID, and round. Any changed specification, approving review, assessment, decision basis, method identity, repository revision, target identity, or target order requires a new occurrence.

## Settlement eligibility

Read the complete `change.yaml` before settlement. Settle only the matching architecture entry or exact ADR target at `review-required`. Match artifact ID, kind, normalized path, content identity, authoring-evidence identity, repository revision, and governing basis. Preserve unrelated entries, milestone state, workflow routing, and reviewed artifact bytes.

Use one overall semantic status. Target disposition prevents unsupported mutation; it creates no partial approval.

- `approved`: every canonical architecture target becomes `approved`; every ADR becomes the intended `accepted` or `active` state recorded by current authoring evidence. A missing or ambiguous intended ADR state blocks the complete settlement.
- `changes-requested`: only targets named by material findings become `revision-required`; unaffected targets remain `review-required`.
- `blocked`: a `target:<artifact-id>` blocker affects only that target, a `target-set` blocker may affect all targets when its evidence covers the set, and a `review-occurrence` blocker performs no settlement.
- `inconclusive`: perform no target settlement by default and leave targets at `review-required`; only separate target-scoped blocker evidence may justify a blocked target.

No non-approved result approves a target or grants downstream eligibility. Recording failure, authority failure, stale identity, ambiguity, invalid lifecycle state, or unsupported intended state performs no target write.

## Prepared settlement manifest

Complete the durable review record, findings, review log, and required resolution before settlement preparation. Durably record the complete prepared settlement manifest on the existing formal-review evidence surface before the first target transition.

The manifest records a stable manifest ID and state, review ID and round, review-subject identity, governing-basis identity, ordered target set, and for every target its artifact ID, kind, path, content identity, authoring-evidence identity, validated pre-state, disposition, expected post-state, and settlement progress. Manifest state is exactly `prepared`, `partial`, `complete`, or `blocked`; these are evidence states, not lifecycle states or independent authority.

After preparation, re-read the complete change record, authority, basis, and target identities. Stop on drift before mutation. Apply compare-and-set writes in manifest order, recording or verifying each target completion against the same manifest. Only `complete` may report `settled` or downstream eligibility.

## Interruption, retry, and concurrency

An interruption after some exact writes reports `partial-retry-required`. Preserve the single semantic judgment and create no duplicate review, finding, log, or resolution evidence.

An identical retry reuses the exact review ID, round, judgment, subject, basis, manifest, target order, identities, authoring evidence, pre-states, dispositions, and expected post-states. Reconcile current state and complete only pending matching writes. Treat an already completed matching transition as idempotent.

Changed identity, state, order, basis, authority, manifest, or concurrent write blocks retry without adoption or unrelated mutation. Never reconstruct an absent manifest or use current state to infer an unrecorded intended write.

## Settlement result

Report `not-applicable`, `recorded-only`, `settled`, `partial-retry-required`, or `blocked` with the manifest identity when applicable, per-target dispositions and progress, exact blocker scope, state changed or unchanged, and claim limitations. Settlement never performs workflow continuation.
