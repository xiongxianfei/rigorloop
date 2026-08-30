# Conditional proposal gates

Load this reference once when one or more specialized predicates are true. The parent skill owns universal vision, intent, scope, materiality, status, recording, claims, and handoff. This reference specializes gate procedure and grants no recording or lifecycle authority.

## Vision exception gate

Apply when `vision_exception_context` is true. Classify the outcome as `revise proposal`, `revise vision`, or `record explicit exception`.

An explicit exception names the approving owner or owning stage, evidence for the conflict, why proposal revision is not chosen, why vision revision is not chosen, where the exception is recorded, and whether it is one-time or establishes a future vision-revision trigger. Require proposal disclosure in `Impact and major trade-offs` and `Decision requested`, and record the outcome in review evidence; for non-trivial changes recommend carrying the rationale into `explain-change.md`.

## Standing artifact gate

Apply when `standing_artifact_context` is true. This standing artifact gate requires bootstrap proposals proceeding without a required standing artifact to disclose the bootstrap exception and owner decision in `Impact and major trade-offs` and `Decision requested`. Request revision if the disclosure is missing or when the proposal silently bypasses a `VISION.md` absence gate for a first substantive proposal or a `CONSTITUTION.md` absence gate for governance adoption, workflow-governance changes, or source-of-truth changes.

Merely citing a standing artifact does not activate this gate. The proposal must depend on missing standing authority, a bootstrap exception, or an equivalent current decision.

## Scope-budget review

Apply when `scope_budget_context` is true. Scope-budget applicability is proposal/proposal-review judgment, not validator inference.

Use scope budget treatment values `core to this proposal`, `first-slice candidate`, `same-slice dependency`, `separate implementation slice`, `deferable follow-up`, `separate proposal`, or `out of scope`.

For broad or multi-workstream proposals, check whether current scope, same-slice dependencies, separate implementation slices, deferable follow-ups, separate proposals, and out-of-scope work are classified clearly enough for downstream reliance.

Return `changes-requested` when a broad or multi-workstream proposal lacks required scope-budget classification. Return `changes-requested` when the proposal hides follow-up work, silently narrows a user request, leaves a treatment or reason blank, omits follow-up routing, or uses a misleading treatment value.

Small single-decision proposals may omit a scope budget when omission does not create silent narrowing, hidden follow-up risk, or multi-workstream ambiguity. Do not request a scope budget solely as routine ceremony. Accept non-standard treatment values only when they are clear and create no downstream ambiguity.

## Composition and ambiguity

Apply every true gate independently and do not invent precedence. Late predicate discovery completes before final status. If current evidence cannot decide whether a predicate applies and the difference could change approval, block approval and identify the smallest owning decision.

This reference must not redefine review status, materiality, recording, settlement, correction, claim, or handoff policy. A contradiction with `SKILL.md` or the recording reference is a package defect and stops dependent work.
