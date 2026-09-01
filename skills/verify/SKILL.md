---
name: verify
description: >
  Run final verification and produce durable change rationale only on success before PR handoff. Use to verify artifact-code-test coherence,
  requirement coverage, validation commands, CI readiness, drift, release safety, and scoped direct validation checks.
argument-hint: [feature name, branch, plan path, spec path, or verification scope]
---

# Verification gate

Prove that the requested scope, current evidence, implementation, tests, and governing artifacts agree. `verify` owns `branch-ready`; `pr` owns `pr-body-ready` and `pr-open-ready`.

## Purpose

Trace current evidence backward through implementation and allocated work to governing SRs and the approved proposal direction.

Perform either a bounded evidence check or a final readiness assessment without taking ownership from authoring, review, workflow, or PR stages. Final verification validates the reviewed final change pack before PR and creates the final durable explanation. It generates the final explanation only after successful final readiness.

Final verification is scoped evidence and must not own artifact settlement, milestone state, or routing. For planned work, use `change.yaml` to assess current state and treat the plan and upstream artifacts as read-only.

## When to use

Use this skill for an explicit validation surface, a direct branch-readiness assessment, or governed final verification after implementation, review closeout, and triggered CI maintenance are complete.

## When not to use

Do not use it to replace code-review, settle upstream artifacts, repair implementation, prepare or open a PR, or claim hosted CI that was not observed.

## Workflow role

`verify` evaluates evidence and records only verify-owned results. The `workflow` skill owns lifecycle progression, and `pr` owns PR preparation and opening. A successful workflow-managed verification hands off to `pr`; it never invokes `pr` itself.

Run `ci-maintenance` first when hosted workflow automation, validation automation, or related platform configuration must change.

## Project-local evidence

Public skills operate in customer-project mode by default. Use project-local instructions, specs, plans, change records, code, tests, validation, and `docs/workflows.md` when present and relevant. Do not require RigorLoop repository-internal specs, docs, reports, or governance files in customer projects. Use portable defaults where safe and block on ambiguity.

## Requested outcome and target

Classify exactly one requested outcome:

- `scoped-verification`: verify one explicit command, artifact, requirement, or evidence surface.
- `branch-readiness`: assess one resolved repository branch or commit and exactly one governed change or explicit evidence root.
- `workflow-final-verification`: assess a valid governed change whose canonical current stage is final `verify`.

A direct request may establish `branch-readiness`, but only after the branch or commit and one evidence root resolve without ambiguity. Words such as “ready”, “final”, or “closeout” do not establish `workflow-final-verification`; current governed lifecycle evidence does. Treat release sensitivity as an evidence-applicability flag, never as publication authority. Stop on an unknown outcome or a missing, ambiguous, stale, mismatched, or conflicting target.

## Resource profiles

Loaded procedure and execution authority are independent:

| Profile | Final readiness | Boundary-first | Loaded package |
| --- | --- | --- | --- |
| `VP0-scoped` | no | no | this file |
| `VP0B-scoped-boundary` | no | yes | this file plus the boundary reference |
| `VP1-final-readiness` | yes | no | this file plus the branch-readiness reference |
| `VP1B-final-readiness-boundary` | yes | yes | this file plus both references |

Use execution mode `isolated` for direct checks and direct branch-readiness assessments. Use `governed-final` only when current governed evidence establishes final `verify` for the same change. Never infer the mode from conversational wording.

### V3 final-readiness profile

V3 is the only current executable final-readiness contract. Final readiness loads impact analysis and evidence applicability; successful results then load explanation guidance and use the v3 report skeleton. Failed or inconclusive attempts emit no final explanation. Scoped verification loads none of those resources. Historical v1/v2 records remain readable evidence but grant no current progression authority.

## Execution authority

An `isolated` result does not mutate lifecycle state, perform governed recording unless explicitly authorized by an existing contract, or invoke `pr`. It may name `pr` only as a possible next stage.

In `governed-final`, perform only verify-owned recording, then return the result to `workflow` for progression. Verification authority is separate from implementation, correction, lifecycle-transition, and PR authority.

Under armed workflow automation, use fresh actual-run evidence for correctness-bearing, security-sensitive, release-sensitive, lifecycle, review-closeout, metadata, generated-output, and required test-suite checks. `cache hits` may support only informational sub-checks when current and identified. A `verify failure` pauses automation and `does not trigger automatic repair`. A pass reports `pr` next and records that human authorization for `pr` is required.

## Inputs to read

Read only evidence needed for the classified outcome. This may include the relevant spec, architecture or ADR, plan and `change.yaml`, actual diff, tests, validation output, observed CI, review and review-resolution evidence, release metadata, generated artifacts, project instructions, and CI definitions.

For placement, prefer the explicit target; current change or plan metadata; governing schema; project workflow guide; then a safe portable default. Block when authority remains ambiguous. For planned records, bounded queries may orient the read, but escalate to full `change.yaml` for whole-record review, disputed or unsupported state, or forensic reconstruction.

For work governed by consolidated gates, require the current accepted proposal evidence, approved Design Review ID and exact member map, approved Delivery Review ID and exact member map, implementation and Code Review evidence, and current validation results. A review-required, partial, stale, or historical-only package blocks final readiness. This evidence requirement does not merge Verify with any earlier gate.

## Evidence truthfulness

- Distinguish `passed`, `failed`, `skipped`, `pending`, `not-run`, and `unknown`; reject unknown closed-vocabulary values before consistency checks.
- A configured command is not an actual run. Never present an unrun, interrupted, or stale command as proof.
- local validation is not observed hosted CI; report CI only from current observed evidence.
- Distinguish current from stale evidence and stop when relied-on evidence is missing, conflicting, or insufficient.
- Check generated-output currency against its governing source; do not infer currency from file presence.
- Accept manual proof only when the governing contract permits it and the record names the check, result, reason, performer, date, and evidence. Use `manual by design` only when intentional.
- Respect network, publication, destructive-action, credential, and external-state boundaries before collecting evidence.
- A scoped result cannot support a broader readiness claim unless the broader evidence set is deliberately assembled and verified.

## Verification dimensions

Evaluate applicable dimensions as `pass`, `concern`, or `block`: requirement and test coverage; test validity; architecture coherence; artifact lifecycle state; plan completion; validation and CI evidence; generated-output and documentation drift; review closeout; risk and release evidence; and branch state.

## Operating sequence

1. Classify outcome, exact target, execution mode, and resource profile.
2. Resolve evidence authority and load only triggered resources.
3. Map requirements or requested checks to tests, changed files, and current evidence.
4. Run named targeted proof; for planned initiatives or authoritative triggers, also run the project's broad validation command when required.
5. Check drift, blockers, claim limits, and the permitted handoff.
6. Report the verdict and exact commands actually run.

When `broad_smoke_required: true` appears in governing evidence, missing broad smoke blocks final readiness. Inspect `verify-report.md` for required normal-change manual proof and release metadata for release smoke or release manual proof.

## Review and lifecycle closeout

For material review findings, inspect `review-resolution.md`, `review-log.md`, and the project's review-artifact closeout validation. Block on `Closeout status: open`, `needs-decision`, missing final dispositions, missing required `Validation evidence`, or open findings. Block unless closeout validation passes. `Closeout status: closed` requires final dispositions and no open findings.

A stage-owned non-approval outcome that blocks progress or requires revision needs a same-stage later review round or explicit reviewer or owner closeout; `review-resolution.md` alone is not a silent substitute. For no-material review events, no-material detailed records need `review-log.md` but not an empty `review-resolution.md`.

For governed work, verify every implementation milestone is closed and current change-local state agrees with the stable plan. A stale touched, referenced, generated, or authoritative lifecycle-managed artifact blocks readiness; unrelated baseline debt is a warning. Required governing artifacts that exist only in untracked local state cannot support `branch-ready`.

## Generated Markdown readability

When this skill creates or updates generated or generator-shaped Markdown:

- Write ordinary prose as normal Markdown paragraphs. Do not split a sentence across physical source lines merely for wrapping or clause separation; multiple sentences may remain in one paragraph.
- Preserve stable IDs for requirements, findings, commands, milestones, and evidence; use tables for repeated mappings.
- Keep commands fenced or table-owned when they carry proof.
- Diagrams are optional. Use them only when they reduce cognitive load and map to real artifacts, stages, components, actors, or states.
- Do not require manual-proof contracts from this readability guidance alone; use governing project rules when manual proof is otherwise required.

## Outputs

Produce the classified outcome, exact target and execution mode, verdict, traceability, commands and results, CI status or gap, drift, blockers, claim limits, and permitted next stage.

For `branch-readiness` and `workflow-final-verification`, emit one normalized `verification_basis` in the portable result or governed verify report. It contains immutable resolved values for:

```yaml
repository_identity: <exact repository identity>
remote_identity: <exact remote identity>
base_branch: <resolved branch>
base_revision: <immutable revision>
merge_base_revision: <immutable revision>
head_branch: <resolved branch>
verified_subject_revision: <immutable revision>
```

Do not substitute commands, unresolved names, or prose for these fields. Missing or ambiguous values block `branch-ready`.

## Handoff

- Normal next stage: return a clean governed-final result to `workflow` for handoff to `pr`.
- Conditional next stages: route CI-infrastructure gaps to `ci-maintenance`, verification-allocation gaps to `plan`, behavior-contract gaps to `spec`, and other failures to their exact owning stage. Verify never repairs and continues.
- Direct requests remain isolated unless explicitly broadened; stop when blockers remain.

## Stop conditions

Stop before a dependent verdict or downstream handoff when the target is unresolved; applicable proof is missing, stale, conflicting, or failing; review or milestone closeout is open; lifecycle state drifts; required generated output or manual proof is not current; or the claim exceeds the verified scope.

A missing or unreadable triggered reference is a package-integrity blocker: stop before dependent interpretation, verdict, recording, or handoff. The skill must not reconstruct, recall, or partially invent missing conditional procedure. An untriggered reference does not load and does not block the applicable profile.

## Claims this skill must not make

Do not claim:

- PR-ready, PR body ready, `pr-body-ready`, or `pr-open-ready`;
- review passed unless the current owning review evidence is cited;
- CI passed unless hosted CI was actually observed, or the statement is explicitly local validation only;
- generated or derived artifacts are current without direct currency proof;
- `branch-ready` from a scoped check, unresolved lifecycle state, local-only governing artifacts, or unresolved named edge-case proof.

Progress means work that has happened so far.
Readiness means the next stage that can happen.
Closeout means the current artifact or stage satisfied its checklist.
Done means final lifecycle state after required gates are complete.
Readiness is not Done. `branch-ready` is neither PR body readiness nor lifecycle Done.

## Evidence collection efficiency

Use bounded evidence before broad reads or raw excerpts.
Use summary and stable-ID first reasoning before broad reads or raw excerpts.
Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations, matching line numbers, diffs, and targeted excerpts when inspecting large files, generated output, validation logs, or repeated scans.
Output caps are safety rails, not evidence-selection strategy.
Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.
Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Boundary-first method

Run this compact scan before any stage-owned decision that can change observable behavior, and whenever the input cites an active boundary contract or stable boundary, interaction, or proof ID. Do not wait for the user to name the method.

1. Which inputs or actors can change the outcome?
2. Which state or timing conditions can change the outcome?
3. Which public, sibling, helper, or alternate path can change the outcome?
4. Which failure, retry, recovery, compatibility, or external condition can change the outcome?

If the work is non-behavioral, cites no active boundary identity, and the scan finds no outcome-changing condition, continue under the ordinary stage contract. The scan alone does not create a formal record, ID, proof map, artifact, or user-visible scenario inventory.

Start with the exact approved rows cited for the current decision. Expand approved context only when an ID or outcome is missing, stale, unknown, ambiguous, conflicting, escaped, or insufficient to explain observed behavior. A new or changed normative outcome routes to `spec`. A pre-implementation verification-allocation gap routes to `plan`. Historical contracts grant no current progression authority. Downstream stages do not redefine or rename upstream IDs.

Add a scenario only for a distinct outcome or material authority, trust, state, timing, recovery, path, compatibility, external-dependency, incident, or regression hazard. Stop when every applicable boundary and selected interaction has direct proof; do not build a Cartesian inventory.

Capability state controls formal adoption: `pending` never claims active adoption; after activation, new behavior-changing specs adopt automatically, grandfathered non-substantive revisions remain valid, and `design-review` must block an undecidable substantive-revision classification. Explain concisely when a formal record is created or an upstream gap blocks progress; do not request redundant consent for contract-required adoption. Structural validation cannot author, repair, or approve semantic content.

Confirm contract-to-proof-to-implementation coherence and unresolved-gap closure. Stop verification before readiness claims when evidence is missing or stale, an ID is unknown, or a discovery still requires upstream ownership.

## Resource map

- READ `references/requirement-to-delivery-model.md` when tracing final evidence backward to implementation, requirements, and proposal direction.
- READ `references/branch-readiness-verification.md` for `branch-readiness` or `workflow-final-verification` after exact target resolution.
- READ `references/boundary-first-method-v1.md` when the final approved boundary, interaction, or proof trace is missing, stale, unknown, ambiguous, conflicting, or insufficient for verification.
- READ `references/final-impact-analysis-v3.md` only for an active v3 final-readiness attempt after exact target resolution.
- READ `references/evidence-applicability-v3.md` only for an active v3 final-readiness attempt after impact classification.
- READ `references/successful-explanation-v3.md` only after an active v3 final-readiness attempt has succeeded.
- COPY `assets/verify-report-v3-skeleton.md` only when recording an active v3 final-readiness result.

Conditional references specialize their activation context; they cannot override this file or each other's owned contract. A contradiction is a package defect and stops dependent work.

## Expected output

Start with:

```md
## Result

- Skill: verify
- Status:
- Artifacts changed:
- Open blockers:
- Next stage:
- Validation:
- Readiness:
```

Then give the verdict, target and execution mode, traceability, validation evidence, CI status or gap, drift, remaining risk, and claim-bounded readiness statement.
