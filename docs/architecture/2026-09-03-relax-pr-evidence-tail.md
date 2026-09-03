# Relaxed PR Evidence Tail Architecture

## Owning change record

- `docs/changes/2026-09-03-relax-pr-evidence-tail/change.yaml`

## Related artifacts

- Proposal: `docs/proposals/2026-09-03-relax-pr-evidence-tail.md`
- Spec: `specs/relax-pr-evidence-tail.md` (pending specification authoring)
- Plan: pending Delivery planning
- ADRs: none; this refines an existing PR validation boundary without adding a durable subsystem or ownership model

## Introduction and Goals

This architecture replaces a Git-topology proxy with direct validation of the safety property it was intended to protect. The reviewed product revision remains immutable verification input, while the eventual handoff may be any descendant whose post-review cumulative change contains only current, attributable review, workflow, and Verify evidence.

The design keeps the existing actors and ownership: Code Review identifies the reviewed product, Workflow records stage transitions, Verify owns `branch-ready` and the final explanation, and PR revalidates the local and remote handoff before external mutation.

## Architecture Constraints

- `skills/` remains the sole authored skill source.
- The published PR skill must remain portable and cannot hard-code this repository's maintainer-only paths as universal customer-project facts.
- Existing normalized Verify basis fields remain unchanged; no new persisted revision, tail, or PR transaction schema is introduced.
- `pr` remains read-only toward lifecycle, review, plan, Verify, merge, and release state.
- Existing remote branch, PR-state, refresh, draft, hosted-CI, push, retry, and read-back rules remain unchanged.
- Unknown, mixed, stale, conflicting, or unattributable changes fail closed.

## Context and Scope

The affected boundary sits between successful Verify and external PR mutation:

```text
Code Review subject ──► governed evidence suffix ──► local handoff
       │                         │                       │
       │                         ├─ review records       ├─ remote head
       │                         ├─ workflow receipts    └─ PR head
       │                         └─ Verify result
       └─ protected product and governing content
```

External Git and PR hosts remain existing dependencies. There is no new service, database, daemon, provider abstraction, or network protocol.

## Solution Strategy

Use two stable identities and one derived comparison:

1. Consume `verified_subject_revision` from the current successful Verify basis.
2. Derive the local handoff revision from the current branch head during PR preflight.
3. Require the verified subject to be an ancestor of or equal to the handoff.
4. Inspect the cumulative reviewed-subject-to-handoff change rather than requiring one direct-child commit.
5. Accept only current governed review, workflow, and Verify evidence for the exact change.
6. Reject product, contract, plan, dependency, configuration, generated-product, unrelated-documentation, unknown, mixed, stale, or unattributable changes.
7. Preserve the existing remote-base, branch-relation, PR-state, push, reread, and final read-back transaction.

This makes commit count and intermediate commit ownership non-authoritative while retaining exact final-state and authority checks.

## Building Block View

### Verify basis producer

The existing successful Verify report provides repository, remote, base, merge-base, head-branch, and reviewed-subject identities plus `branch-ready`. It does not store its own commit identity or a new tail schema.

### Evidence-suffix classifier

The PR procedure classifies the cumulative post-review change as either `none`, `evidence-only`, or `invalidating`. These are decision outcomes, not a new persisted vocabulary or lifecycle state.

For a governed change, evidence-only content is limited to the exact owning change pack's current formal review records, review log and conditional resolution, workflow transition requests or receipts, current mutable lifecycle state, and final Verify report and registration. The governed readiness reference resolves these surfaces from current project evidence rather than publishing repository-maintainer path mechanics as universal rules.

### Product-boundary guard

Any change outside the resolved evidence set is invalidating when it affects implementation, tests, specifications, architecture, plans, dependencies, configuration, generated product output, public documentation, or another governed change. Unknown and mixed changes are invalidating.

### External-operation guard

Existing PR behavior continues to bind the handoff to remote head and PR head, compare the verified base before each mutation boundary, prohibit force or overwrite operations, reconcile retries, and read back the final PR identity.

## Runtime View

### Evidence-only handoff

1. PR consumes a current successful Verify result.
2. It resolves the reviewed subject and local handoff.
3. If they are equal, no suffix exists and ordinary readiness continues.
4. If the reviewed subject is not an ancestor, readiness blocks.
5. Otherwise PR evaluates the cumulative suffix against the exact governed change and current lifecycle evidence.
6. Current attributable evidence proceeds regardless of commit count or direct-parent topology.
7. PR performs the unchanged remote transaction and final read-back.

### Invalidating suffix

If any protected or unclassified surface changed, PR performs no new external mutation, reports the invalidating paths or authority gap, and routes to fresh review or Verify as appropriate.

### Stale evidence

If lifecycle validation, review closeout, Verify registration, or content identity is stale or conflicting, the suffix is not evidence-only. PR blocks and names the owning stage rather than inferring freshness from paths or commit messages.

## Deployment View

The change ships through the existing canonical skill and adapter generation pipeline. Canonical edits are made under `skills/pr/` and, when wording must align, `skills/verify/`. Repository specs, fixtures, validators, and release-candidate metadata are updated through their current owners and existing deterministic tooling. No generated adapter skill body is hand-edited or tracked as source.

## Crosscutting Concepts

### Authority and trust

Path membership is necessary but not sufficient. Governed evidence must agree with the exact change identity, current formal review records, lifecycle validation, review closeout, and Verify registration. Commit messages and author names grant no authority.

### Final-state comparison

Readiness is based on the cumulative final diff from reviewed subject to handoff. Intermediate commit count, direct-parent shape, and stage-owner labels do not independently invalidate an unchanged product boundary.

### Fail-closed behavior

Non-ancestor relationships, unresolved governed identity, multiple candidate changes, mixed evidence and product changes, stale hashes, unknown paths, invalid lifecycle state, or incomplete Verify evidence block before push or PR mutation.

### Compatibility

Historical reports and PRs remain historical. New PR invocations use the refined predicate. A current successful normalized Verify basis remains required, and legacy incomplete evidence remains preparation-only.

### Recovery

Product or governing drift returns to the earliest affected owner and requires the applicable rereview and fresh Verify. Evidence-only corrections may remain additive; no squash, reset, rebase, or force push is required by this design.

## Architecture Decisions

No ADR is required. The decision refines the validation predicate inside the already approved PR package and does not add a durable subsystem, persistence model, provider abstraction, or cross-component ownership boundary.

## Quality Requirements

| Quality | Scenario | Measure |
| --- | --- | --- |
| Safety | Product content changes after final Code Review | PR opening blocks before external mutation and identifies the invalidating surface. |
| Composability | Final review, workflow transition, and Verify require several additive evidence commits | PR readiness accepts the current evidence-only suffix regardless of commit count. |
| Auditability | A reviewer inspects why a suffix was accepted | The result identifies the reviewed subject, handoff, evidence classification, and current owning evidence. |
| Portability | A customer project uses different governed paths | The public skill resolves project-local evidence rather than assuming repository-maintainer paths. |
| Recovery | An evidence correction is needed after review | The correction remains additive and does not require history rewriting or force push. |

## Risks and Technical Debt

- Evidence classification is more semantic than counting commits. Deterministic fixtures must cover allowed, mixed, unknown, and stale suffixes so proportionality does not become permissiveness.
- `change.yaml` contains both identity and mutable lifecycle data. Acceptance must require current authoritative validation and constrain the suffix to lifecycle-owned state rather than treating the whole file as trusted solely by path.
- The PR skill remains prose-driven rather than gaining a new executable engine. Tests can prove the published contract and scenarios, but runtime judgment still depends on disciplined evidence inspection.

## Glossary

- **Reviewed subject:** exact product revision named by final Code Review and the successful Verify basis.
- **Handoff revision:** current local branch head eligible to become the remote and PR head.
- **Evidence suffix:** cumulative final change between reviewed subject and handoff containing only current attributable review, workflow, and Verify evidence.
- **Invalidating change:** any protected, unknown, mixed, stale, conflicting, or unattributable post-review change.

## Next artifacts

- Specification reconciliation.
- Design Review of this architecture and the resulting specification as one exact package.

## Follow-on artifacts

- None yet.

## Readiness

Architecture authoring is complete and ready for specification reconciliation. Design authority remains withheld until the specification exists and Design Review approves the exact package.
