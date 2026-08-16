# Architecture-review recording and settlement

Use only after durable recording is established. Loading grants no location, settlement, automation, correction, or workflow authority.

## Recording modes

`advisory-durable` writes only to an explicit valid user path or authorized standalone location. It creates no governed root, formal log or resolution, lifecycle entry, settlement, automation evidence, or workflow continuation. Without a safe location, return the complete judgment and findings with `recording_status: blocked` and create no governed state.

`formal-lifecycle` requires one exact governed root and valid evidence placement. Write the review before settlement, synchronize the review log, and use review resolution only when required. Recording failure permits no settlement.

Workflow-managed automation requires current formal authority, reviewer independence, neutral phase evidence, and separately owned correction authority; it returns control without advancing routing. For automated `bounded-review-fix` authoring, reset review context to the tracked artifact, governing sources, formal review criteria, and relevant recorded findings before reviewing. Record the review result before any automation-driven downstream action. Do not rely on hidden authoring reasoning from the preceding stage. Do not edit the reviewed artifact during review.

## Review identity

Every formal occurrence binds separate `review_subject`, `governing_basis`, ordered optional `settlement_targets`, review ID, round, record path, and log path. The governing basis identifies the governing specification and identity, approving spec-review, architecture-assessment receipt, relevant accepted decision, architecture-method contract and identity, and repository revision.

A canonical subject identifies exact canonical Markdown, linked diagrams, related ADRs, and content identities. An ADR subject identifies the exact ADR, canonical linkage, and identity. The no-impact subject binds its assessment and proposal or specification basis; the proposal/spec-gap subject binds its upstream artifacts and architecture question. These record-only surfaces use an empty settlement-target set and create or settle no lifecycle entry. A formal record-only review without one stable subject blocks recording or remains advisory; never create an identity-free formal occurrence.

Reuse requires the same subject, basis, ordered targets, status, review ID, and round. Any changed specification, approving review, assessment, decision, method, revision, target identity, or target order requires a new occurrence.

## Settlement eligibility and disposition

Read the complete `change.yaml` before settlement. Settle only the matching architecture entry or exact ADR target at `review-required`; match artifact ID, kind, normalized path, content identity, authoring-evidence identity, repository revision, and basis. Preserve unrelated entries, milestone state, routing, and reviewed bytes.

One overall status applies; target disposition creates no partial approval.

- `approved`: every canonical architecture target becomes `approved`; ADRs use the intended `accepted` or `active` state from current authoring evidence. A missing or ambiguous intended ADR state blocks all settlement.
- `changes-requested`: only targets named by material findings become `revision-required`; unaffected targets remain `review-required`.
- `blocked`: `target:<artifact-id>` affects that target, `target-set` may affect the evidenced set, and `review-occurrence` performs no settlement.
- `inconclusive`: no settlement by default; only separate target-scoped blocker evidence may block a target.

No non-approved result approves a target. Recording or authority failure, stale identity, ambiguity, or invalid state performs no write.

## Prepared settlement manifest

Complete the review, findings, log, and required resolution, then durably record the complete prepared settlement manifest on existing formal-review evidence before the first target transition. It binds manifest ID and state, review ID and round, subject and basis identities, target order, and each target’s artifact ID, kind, path, content and authoring-evidence identities, pre-state, disposition, expected post-state, and settlement progress. State is exactly `prepared`, `partial`, `complete`, or `blocked`; these are evidence states, not lifecycle authority.

After preparation, re-read authority, basis, targets, and complete change state. Stop on drift, then compare-and-set in manifest order and record or verify completion. Only `complete` reports `settled` or eligibility.

## Retry and concurrency

Interruption after exact writes reports `partial-retry-required`, preserves one judgment, and creates no duplicate review, finding, log, or resolution evidence. An identical retry reuses every review, subject, basis, manifest, target, authoring-evidence, pre-state, disposition, and expected-state identity and completes only pending matching writes; completed matching writes are idempotent.

Changed identity, state, order, basis, authority, manifest, or concurrent evidence blocks retry without adoption or unrelated mutation. Never reconstruct an absent manifest or infer an unrecorded write.

## Settlement result

Report `not-applicable`, `recorded-only`, `settled`, `partial-retry-required`, or `blocked`, plus manifest identity, dispositions, progress, blocker scope, state change, and claim limits when applicable. Settlement performs no workflow continuation.
