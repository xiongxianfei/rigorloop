# ADR-20260624-implementation-through-verify-autoprogression: Separately Armed Implementation Autoprogression Through Verify

## Status

accepted

## Context

RigorLoop can already reduce redundant prompts for proposal-to-plan authoring through the separately armed `authoring-through-plan-review` profile. That profile intentionally stops before `test-spec` and implementation because implementation crosses materially different risk surfaces: code execution, dependency mutation, generated output, test fixtures, review-driven correction, validation cost, and external PR or publication boundaries.

The accepted proposal and approved spec amendments define a sibling implementation profile. The profile should let a user separately authorize deterministic post-planning progress while preserving human control over owner decisions, governing-artifact changes, non-converging review loops, verify failures, and PR publication.

This is a durable architecture decision because it changes workflow orchestration, profile persistence shape, material finding metadata, review-resolution evidence, phase-gated rollout, validation freshness rules, and generated skill behavior.

## Decision

Add a closed, separately armed workflow profile:

```text
implementation-through-verify
```

The user-facing authorization `auto-through: verify` maps to the internal profile value `implementation-through-verify`. This authorization is change-local and independent from `authoring-through-plan-review`; authoring authorization never implies implementation authorization.

Persist implementation-profile authorization as its own change-local record with separate profile key, state, phase, `authorized_by`, `authorized_at`, change ID, cancellation data, activation baseline, and audit pointers. Profile policy metadata remains authorization and audit evidence only. Existing workflow-state owners continue to own current stage, next stage, review status, branch readiness, PR readiness, and active-plan live state.

Activation requires approved clean planning, explicit ordered implementation milestones, complete test-spec inputs, durable implementation-profile authorization, working-tree baseline, absent or excluded unrelated dirty changes, approved commands, clean governing artifacts, unambiguous artifact placement, and workflow-state synchronization.

The profile uses persisted rollout phases:

```text
A: audit-only decisions and stop-condition simulation
B: test-spec settlement, implementation milestones, independent code-review, bounded reviewer-declared correction loops, and final clean code-review
C: Phase B behavior plus explain-change, fresh verify, completion before PR
```

The orchestrator refuses transitions outside the persisted phase. Phase advancement requires recorded promotion evidence linked to dogfood-cycle audit records and stop-condition fixture results.

Before implementation, the profile runs `test-spec` authoring and deterministic test-spec settlement. Settlement records input identities for the approved spec, relevant architecture or ADRs, plan, and test spec. The first milestone's code-review rechecks those identities and pauses on mismatch.

Every milestone runs in approved order and receives independent code-review before closing. Material code-review findings include reviewer-owned `auto_fix_class`:

```text
none
mechanical
declared-safe
```

Missing classification is `none` and pauses. The orchestrator cannot infer or upgrade auto-fix eligibility. `mechanical` is restricted to closed deterministic kinds. `declared-safe` requires a deterministic recipe, bounded paths, forbidden paths, inputs, outputs, acceptance criteria, required validation, and production-code behavior proof when applicable.

Automatic correction rounds are bounded to three per milestone. Each round must shrink unresolved findings, introduce no new finding ID or class, stay path-local, avoid new dependencies or scope, avoid substantive governing-artifact edits, and use only approved commands. A new finding pauses even when it may be valid; new discovery is a human-decision moment.

Phase C may run `explain-change` and `verify` only after all milestones are clean and a final full code-review confirms the governing contract. Final verify uses fresh actual-run evidence for correctness-bearing, security-sensitive, release-sensitive, artifact lifecycle, review closeout, change metadata, generated-output, and required test-suite checks. Verify failure pauses without automatic repair.

Successful Phase C completion records branch readiness through workflow-state synchronization from verify evidence, reports `pr` next, and stops. The profile must not open a hosted PR, push branches, publish packages, trigger deployments, post to external systems, or request remote review.

## Alternatives considered

### Widen `authoring-through-plan-review`

Rejected because authoring authorization must not silently authorize implementation, code execution, review-driven edits, or validation cost.

### Add unrestricted `auto=true`

Rejected because it has no bounded meaning and invites inferred auto-fix safety, PR publication, or external effects.

### Let the orchestrator infer simple fixes

Rejected because apparent simplicity can conceal product, compatibility, architecture, or owner decisions. Reviewer-declared classification is the authority boundary.

### Stop permanently after clean code-review

Rejected as the final target because `explain-change` and `verify` are internal evidence stages with deterministic inputs after clean review. The phased rollout still proves the implementation/review loop before enabling Phase C.

### Open PR automatically

Rejected because hosted PR creation can trigger CI cost, reviewer notifications, deployment hooks, and external publication effects. PR opening needs separate explicit human authorization and a separate proposal if automated later.

## Consequences

- Workflow-managed implementation can reduce redundant routing prompts after clean planning without changing profile-off behavior.
- Material finding records and review-resolution evidence must carry enough structured data to reconstruct every automatic correction.
- Code-review remains the authority for auto-fix classification, while the orchestrator only enforces declared recipes and guardrails.
- Implementation-profile loops are intentionally conservative: better review discovery after a fix pauses instead of being chased automatically.
- Phase gating requires durable promotion evidence and fixture coverage before `explain-change` and `verify` autoprogression can run.
- Final verify cannot rely on stale cache evidence for sensitive or correctness-bearing checks.
- No new service, database, background worker, deployment target, hosted PR mutation, package publication, or remote infrastructure boundary is introduced.

## Follow-up

- Architecture-review this ADR and the canonical architecture package update.
- Plan implementation of profile persistence, phase gating, test-spec settlement, reviewer-owned classification fields, correction-loop enforcement, audit records, final fresh verify rules, and PR-boundary stop behavior.
- Update canonical skills, validators, schemas, test specs, and generated adapters after implementation changes authored guidance.
- Use Phase B dogfood and synthetic stop-condition fixture evidence before enabling Phase C.
