# Bugfix Skill Simplification

## Owning change record

Portable authoring. No governed change record exists for this proposal, and this artifact does not establish lifecycle state, review settlement, workflow activation, or downstream continuation.

## Status

draft

## Problem

The published `bugfix` skill is small, but its current narrative workflow leaves several high-impact decisions implicit. It does not distinguish a request to diagnose a defect from authority to mutate code, tests, or documentation. It permits non-reproduced fixes through an open-ended uncertainty statement, leaves contract-gap routing to judgment without a closed outcome, and does not define which proof substitutes are acceptable when an automated failing test is infeasible. Its expected output can also imply handoff directly to `explain-change` or `pr` even though changed implementation normally requires independent `code-review` first.

These gaps matter more than raw length. Bugfix work starts from uncertainty, often touches production behavior, and can easily turn a plausible theory into an unsupported patch. The skill should remain concise while making the evidence progression, mutation boundary, stop conditions, ownership, and completion claims explicit.

The current package is one 586-word, 3,761-byte `SKILL.md` with no references, assets, or scripts. Most of its procedure is common to every real fix, so adding conditional files merely to resemble larger optimized skills would increase the complete loaded profile without establishing a strong activation boundary.

## Goals

- Separate diagnosis-only requests from requests that authorize a fix.
- Define a closed evidence progression from expected behavior through reproduction, root cause, regression proof, minimal correction, and blast-radius validation.
- Route contract changes, unresolved conflicts, and design gaps to their owning stages instead of guessing in implementation.
- Preserve regression-test-first behavior while defining bounded alternative proof when an automated failing test is infeasible.
- Preserve direct and manual bugfix isolation and prevent bugfix from mutating workflow, review, plan, or artifact lifecycle state.
- Correct the handoff so implementation changes go to independent `code-review` before later rationale, verification, or PR stages.
- Reduce both words and bytes for the complete shipped package while preserving every current safety obligation and supported defect class.

## Non-goals

- Create a separate diagnosis skill, incident-management system, issue tracker integration, debugging runtime, test generator, or automated repair engine.
- Add packaged references, output assets, scripts, templates, or provider-specific tooling in the first version.
- Redesign the standard workflow, broaden bugfix autoprogression, or make bugfix a workflow-managed implementation profile.
- Define repository-specific test commands, debugging tools, language frameworks, or defect taxonomies beyond the portable control contract.
- Author new product behavior, approve specifications or architecture, settle reviews, claim verification, open PRs, or mutate external systems.
- Rewrite historical bugfix evidence or migrate existing project records merely to adopt the shorter contract.

## Vision fit

fits the current vision

The change makes defect work more inspectable and trustworthy by requiring visible evidence for expected behavior, root cause, regression proof, and validation. It reduces ceremony only where the text is redundant and strengthens the traceability chain where unsupported fixes could otherwise escape review.

## Context

`CONSTITUTION.md` requires regression coverage or an explicit failure reproduction path before a bug fix is complete, prohibits unverifiable claims, and requires externally observable behavior changes to follow an approved spec. `specs/skill-contract.md` classifies `bugfix` as an on-demand or support skill that needs an explicit trigger, output, handoff, stop conditions, and claim boundaries. `specs/rigorloop-workflow.md` and `docs/workflows.md` keep direct and bugfix invocations isolated or explicit-step by default.

The current skill already has the correct core sequence: understand expected behavior, reproduce, diagnose, add a regression test, fix minimally, verify, and update durable documentation. The proposal preserves that sequence. It changes the representation from open-ended narrative to a compact closed contract at the points where different agents could otherwise make materially different decisions.

Current authored and consumer evidence also shows no genuine need for a resource split. `bugfix` has no domain variant, provider branch, durable output template, or repeated executable helper. The best first slice is therefore semantic compression within the existing single-file package.

## Options Considered

### Option 0: Keep the current skill unchanged

This avoids compatibility work and package risk. It retains ambiguous diagnosis authority, open-ended non-reproduction behavior, incomplete claim boundaries, and incorrect downstream handoff possibilities. It also leaves `bugfix` behind the normalized support-skill contract.

### Option 1: Editorially shorten the current narrative

This could reduce words and bytes with minimal change. It would not close the operational ambiguities because the same prose would still mix classification, evidence, mutation, and handoff. A smaller ambiguous skill is not a meaningful safety improvement.

### Option 2: Compact one-file contract with closed classifications

This retains one `SKILL.md`, removes repetition, and adds explicit operation, evidence, authority, stop, result, and handoff rules. Every invocation loads the same smaller package, and the common fix path does not pay for navigation or duplicated reference context. This is the recommended option.

### Option 3: Compact root plus a conditional fix-execution reference

This would make diagnosis-only requests cheaper by loading detailed mutation procedure only for fixes. Current repository evidence does not establish `bugfix` as a frequent diagnosis-only routing surface, and a full fix would load at least as much content as today. The split should be reconsidered only if measured usage demonstrates a real diagnosis-only profile and both profiles improve.

### Option 4: Separate diagnosis and bugfix skills

This creates a second trigger and handoff boundary without a distinct artifact, review gate, or durable owner. It increases selection ambiguity and conflicts with the repository rule against creating skills for behavior that belongs inside an existing owner.

### Option 5: Add scripts or an executable repair engine

Deterministic automation could standardize some steps, but reproduction, tests, debuggers, and validation commands are project-specific. An engine would add runtime, architecture, portability, and acceptance surfaces far beyond a text-contract optimization.

## Recommended Direction

Keep `bugfix` as a single-resource package and rewrite `SKILL.md` as a compact support-stage contract.

Use two operations:

```text
diagnose-only
fix
```

An explicit request to explain, investigate, or identify root cause selects `diagnose-only` and grants no file mutation. An explicit request to fix, repair, resolve, or use `$bugfix` against a concrete defect selects `fix`. Ambiguous intent permits diagnosis but blocks mutation until the user supplies fix authority. Late evidence cannot silently broaden diagnosis into repair.

Use closed evidence states:

```text
reproduction:
  reproduced
  alternative-proof
  not-reproduced
  conflicting

contract basis:
  settled
  resolvable-restoration
  missing
  conflicting
  behavior-change-request

regression proof:
  failing-automated-test
  deterministic-alternative
  infeasible-with-rationale
  missing
```

`alternative-proof` is a pre-fix deterministic proof such as an exact command, fixture, static contract check, or controlled manual reproduction. It is not a guess based on code inspection. `infeasible-with-rationale` records why an automated regression test cannot be created and still requires another exact verification surface before mutation. `not-reproduced`, `conflicting`, or `missing` proof blocks mutation unless the current contract defines a narrower safe diagnostic-only result.

Use a closed root-cause vocabulary:

```text
implementation-defect
contract-gap
integration-mismatch
data-or-migration
race-or-timing
configuration-or-environment
test-defect
external-dependency
unknown
```

Unknown or conflicting classification remains visible and cannot support a fixed claim. Root-cause classification identifies the likely owner and blast radius; it does not itself authorize mutation.

Preserve the current test-first preference, but distinguish proof obligations from a particular test framework. A fix becomes eligible only when expected behavior has one current basis, reproduction or exact alternative proof exists, root cause is evidence-supported, mutation authority is current, and regression proof is prepared before production changes. A behavior-change request or conflicting contract routes to `spec`; a new long-lived design decision routes to `architecture`; an environment-only or external-dependency result routes to its owner instead of patching unrelated product code.

For governed context, use the same fail-closed signal model as other published skills:

```text
no-governed-signal
single-governed-candidate
invalid-or-ambiguous-governed-signal
```

A valid governed candidate may read the exact current change, plan, and approved commands needed to bound the fix. Loading or discovering that context never grants workflow mutation. Invalid, conflicting, escaped, duplicated, or stale signals stop without falling back to portable behavior. Bugfix writes only the authorized implementation, regression proof, narrowly required durable documentation, and bugfix-owned execution evidence. It does not create or advance a workflow run, change plan or milestone state, settle reviews, or claim downstream readiness.

Completion requires rerunning the original reproduction or its exact alternative, the regression proof, and the smallest surrounding validation justified by blast radius. The output reports commands actually run, unexecuted checks, remaining uncertainty, changed surfaces, and the next owning stage. When implementation changed, the immediate next stage is `code-review`; later `explain-change`, `verify`, and `pr` remain separate gates. Diagnosis-only returns findings and owner routing with no automatic continuation.

## Expected Behavior Changes

- Root-cause questions remain read-only unless the user separately authorizes a fix.
- Direct `$bugfix` with a concrete defect remains an explicit fix invocation and remains isolated from automatic downstream stages.
- A missing or conflicting expected-behavior contract no longer permits a speculative product patch. Restoration may proceed only from one exact current basis that does not invent new behavior.
- Non-reproducible failures require deterministic alternative proof or stop; code inspection alone does not become successful reproduction.
- Regression-test exceptions require a specific infeasibility rationale and another exact proof surface.
- Weakening a test is treated as a test-defect correction only when current contract evidence supports the new expectation.
- Successful fix output routes implementation changes to independent `code-review`, not directly to `explain-change` or `pr`.
- Result claims distinguish diagnosis, applied correction, local proof, and downstream readiness. Bugfix never claims review, verification, CI, branch, PR, release, deployment, or lifecycle completion.

## Architecture Impact

Expected assessment: `architecture-not-required`.

The change retains the existing published-skill package, canonical `skills/bugfix/SKILL.md` source, generated adapter pipeline, and project-local command model. It adds no resource, schema, state owner, service, parser, external integration, persistent transaction, or executable runtime.

Architecture becomes required if implementation introduces a debugging or repair engine, persistent bug transaction, cross-stage state owner, external issue or incident integration, repository-independent command abstraction, or a separate diagnosis skill with its own durable lifecycle.

## Testing and Verification Strategy

Add deterministic contract fixtures for at least:

- diagnosis-only requests that attempt no mutation;
- explicit fixes with a reproduced failure and failing regression test;
- ambiguous intent that blocks mutation;
- non-reproduced failures with and without acceptable alternative proof;
- missing, conflicting, and behavior-changing contract bases;
- implementation, test, environment, external dependency, race, and unknown root causes;
- test weakening without contract evidence;
- governed valid, malformed, stale, conflicting, and duplicated signals;
- attempted workflow, review, plan, verification, or PR-state mutation;
- successful fix handoff to `code-review` and diagnosis-only owner routing;
- exact reproduction rerun and blast-radius validation requirements;
- unknown closed-vocabulary values failing before consistency checks.

Create a rule-disposition ledger for every behaviorally meaningful line in the current `bugfix` skill and a literal-consumer inventory for validator- or documentation-sensitive terms. Prove canonical, generated, packed, archived, release-candidate, and installed package parity with existing repository tooling.

Measure LF-normalized Unicode whitespace-separated words and UTF-8 bytes for the current and proposed root. Because no resource is added, the root and complete package are the same measurement. Acceptance requires both measures to decrease; moving text to contributor-only evidence does not count as semantic preservation unless one current owner remains.

Use static scenarios and ordinary independent reviews. Do not execute Codex, Claude Code, opencode, another target agent, a live repair task, or an external issue or incident system as acceptance machinery.

## Rollout and Rollback

Author the focused bugfix-skill contract amendment, record exact legacy-rule dispositions, update the canonical skill and directly coupled validators or workflow guidance, and validate generated/install parity. Historical bugfix evidence and project artifacts are not rewritten.

Roll back by reverting the canonical skill, focused contract, fixtures, and directly coupled documentation together. No data migration or external rollback is required. If the new classifications prove too verbose or fail to improve the complete package, retain the current one-file structure and restore the accepted legacy text rather than hiding cost in a new reference.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Closed classifications make a small skill longer | Remove narrative duplication and require strict complete-package word and byte reduction. |
| Diagnosis-only broadens the skill trigger unexpectedly | Keep frontmatter explicit, preserve direct `$bugfix` as fix authority for a concrete defect, and test ambiguous ordinary questions. |
| Strong reproduction rules block legitimate hard-to-reproduce defects | Permit exact deterministic alternative proof with named uncertainty and blast-radius controls; do not permit unsupported inference. |
| Contract-gap routing adds unnecessary ceremony for obvious regressions | Allow `resolvable-restoration` only when one current authoritative behavior basis exists and no new observable contract is invented. |
| Root-cause vocabulary becomes a false certainty | Keep `unknown` as a valid diagnostic result that blocks fixed claims and routes further investigation. |
| Bugfix starts duplicating `implement` or workflow lifecycle procedure | Keep only defect-specific evidence and mutation rules; delegate milestone state, review, routing, verification, and PR ownership. |
| Compatibility is lost during compression | Require complete rule and literal inventories plus focused preservation fixtures before changing the canonical skill. |
| Root shrinkage hides generated or package growth | Measure the complete shipped package and validate every package/install projection. |

## Open Questions

None at proposal level.

The specification may choose exact field names and fixture representation, but it should preserve the operation, evidence-state, ownership, handoff, and measurement semantics selected here.

## Decision Log

- Keep one compact `SKILL.md`; do not add references, assets, or scripts in the first version.
- Optimize authority and evidence semantics rather than pursuing a resource split without a proven conditional profile.
- Support exactly `diagnose-only` and `fix` operations.
- Treat direct `$bugfix` against a concrete defect as explicit fix authority while keeping all continuation explicit-step.
- Require reproduction or deterministic alternative proof before mutation.
- Route conflicting or behavior-changing contracts to their owning stages.
- Keep governed-signal validation fail-closed without granting workflow-state authority.
- Route changed implementation to `code-review` and keep later gates separate.
- Require strict word and byte reduction for the complete package.
- Use deterministic static acceptance and existing package tooling; do not use target-agent runtime execution.

## Next Artifacts

- Focused `bugfix` skill-contract specification or amendment.
- Bounded architecture assessment, expected `architecture-not-required`.
- Execution plan and independent plan review.
- Test specification and independent test-spec review.

## Follow-on Artifacts

None yet

## Readiness

Ready for independent proposal review. This portable proposal is not accepted, does not establish a governed change, and is not ready for specification until proposal-review approves it.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `bugfix` skill | in scope | Goals; Recommended Direction; Expected Behavior Changes |
| Select the best solution rather than fragmenting by default | in scope | Options Considered; Recommended Direction |
| Create a new branch | in scope | Delivery branch `proposal/bugfix-skill-simplification` |
| Generate a durable proposal | in scope | This artifact |
| Perform independent `$proposal-review` | in scope | Readiness; Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Compact universal bugfix contract | core to this proposal | It owns the selected behavior and size improvement. |
| Diagnosis-versus-fix authority | core to this proposal | It closes the highest-risk ambiguity. |
| Reproduction, contract, cause, and regression-proof states | core to this proposal | They make mutation eligibility and claims deterministic. |
| Governed-signal and lifecycle write boundaries | same-slice dependency | The public skill must remain safe inside active planned work. |
| Focused spec and test-spec amendments | separate implementation slice | They are required downstream artifacts after proposal approval. |
| Canonical skill, fixtures, and directly coupled validator changes | separate implementation slice | They implement and prove the later approved contract. |
| Generated, archived, and installed parity | same-slice dependency | Published-skill compatibility must be proven with the implementation. |
| Separate diagnosis skill | out of scope | It lacks a distinct durable artifact or gate and would fragment ownership. |
| Conditional execution reference | deferable follow-up | Reconsider only if measured real usage proves a diagnosis-only loading profile and both profiles improve. |
| Debugging or automated repair engine | out of scope | It adds runtime and architecture beyond text-contract optimization. |
| Workflow autoprogression changes | out of scope | Bugfix remains isolated or explicit-step under the current workflow contract. |
