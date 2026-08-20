# Bugfix Skill Simplification

## Owning change record

Portable authoring. No governed change record exists for this proposal, and this artifact does not establish lifecycle state, review settlement, workflow activation, or downstream continuation.

## Status

under review

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

Operation, command authority, and repository-write authority are independent closed decisions. Naming `$bugfix` selects intent; it never grants unbounded command execution or writes.

```text
operation: diagnose-only | fix
command authority: not-required | current-bounded | absent-or-stale | invalid-or-ambiguous
write authority: none | portable-request-bound | governed-scope-bound | absent-or-stale | invalid-or-ambiguous
```

| Request shape | Operation | Authority consequence |
| --- | --- | --- |
| Explicitly explain, investigate, reproduce, or identify root cause | `diagnose-only` | No write grant, including when `$bugfix` is named |
| Explicitly fix, repair, or resolve one concrete defect | `fix` | Resolve exact command and write authority before side effects |
| Bare `$bugfix` with one concrete defect and no narrower outcome | `fix` | Establish portable request-bound authority only for that repository and defect, unless valid governed context supplies the narrower scope |
| No concrete defect | none | `blocked` |
| Conflicting diagnosis and repair instructions | `diagnose-only` | Diagnosis may proceed; mutation is `blocked` pending one explicit outcome |

Each writable fix binds repository identity, normalized defect target, authority source, permitted command owner or set, allowed path roots, allowed write categories, governing contract identity, and current evidence identities. Independent defects are separate invocations unless evidence proves one shared cause, behavior basis, correction scope, and proof bundle. Expanding diagnosis to fixing requires fresh authority and mutation preflight; only still-current diagnostic evidence may be reused.

Diagnosis may run exact inspection or reproduction commands under `current-bounded` authority but intentionally changes no tracked file. Unknown, destructive, privileged, network, database, or durable external effects require their existing separate authority or the command is skipped. Unexpected tracked or external mutation stops the invocation; generated and temporary effects are reported and restored when the project contract requires it.

Use independent closed evidence axes:

```text
reproduction: reproduced | deterministic-alternative | not-established | conflicting
contract basis: settled | resolvable-restoration | missing | conflicting | behavior-change-request
test feasibility: feasible | infeasible-with-rationale | unresolved
regression proof: failing-automated-test | deterministic-alternative | missing | conflicting
root-cause support: supported | uncertain | conflicting
```

`resolvable-restoration` means one exact current authoritative behavior basis defines the observable outcome, no equal- or higher-priority source conflicts, and the correction only restores conformance without adding, removing, broadening, narrowing, or reinterpreting behavior. Record its source path or identity, owner, precedence, affected behavior, expected result, and conflict check. Current implementation, a failing test, a report, or plausible expectation is insufficient by itself.

`deterministic-alternative` is an independently repeatable command, fixture, static contract check, or controlled manual procedure with exact inputs, environment assumptions, steps, expected observation, and completion condition. Subjective inspection is not proof. Test infeasibility is a feasibility result, never proof or mutation authority.

Use four phases with separate gates:

```text
diagnosis
→ proof authoring
→ production correction
→ post-fix validation
```

After reproduction, one settled or restoration basis, supported root cause, current bounded command authority, and current write authority exist, proof authoring may write only tests, fixtures, test-only helpers, or controlled reproduction artifacts within the exact scope. It may not change production behavior. Production correction remains blocked until a failing automated test exists, or until a complete deterministic alternative exists with `infeasible-with-rationale`.

| Test feasibility | Current regression evidence | Permitted next action |
| --- | --- | --- |
| `feasible` | `missing` or `deterministic-alternative` | Author the failing automated proof; production mutation remains blocked |
| `unresolved` | `deterministic-alternative` | Resolve feasibility; production mutation remains blocked |
| `infeasible-with-rationale` | complete `deterministic-alternative` | Production correction may proceed |
| Any recognized value | `failing-automated-test` | Production correction may proceed |
| Any recognized value | `missing` or `conflicting` after proof authoring | No production mutation; terminal result is `blocked` |

Before production mutation, record one proof identity with kind, procedure or command, fixture and input identities, environment assumptions, expected and observed pre-fix result, feasibility, and any infeasibility rationale. Post-fix validation reruns that identity unchanged and records the post-fix observation. A changed command, test, fixture, input, or environment is a new proof and cannot be reported as the original proof passing. One artifact may serve reproduction and regression roles only when this unchanged-identity rule holds.

Use the closed root-cause vocabulary:

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

Apply these consistency and routing rules before either write gate, from top to bottom; the first matching row owns the action and terminal result:

| Condition | Required action and terminal result |
| --- | --- |
| Any unknown closed value, conflicting axis, unsafe identity, or invalid authority | No write; `blocked` |
| Cause `contract-gap`, or basis `missing`, `conflicting`, or `behavior-change-request` | No bugfix mutation; `routed-to-owner` for `spec` or the exact contract owner |
| Cause `unknown`, or reproduction or root cause remains unresolved | No production mutation or fixed claim; `diagnosis-incomplete` |
| Cause `test-defect` with `settled` or `resolvable-restoration` basis | A bounded test correction may proceed through the phase gates; speculative weakening is forbidden |
| Cause `configuration-or-environment` or `external-dependency` with one settled product contract and current resilience-correction scope | A bounded product correction may proceed through the phase gates |
| Cause `configuration-or-environment` or `external-dependency` without that exact product basis and scope | No product mutation; `routed-to-owner` |
| New long-lived design decision is required | No bugfix mutation; `routed-to-owner` for `architecture` |
| Supported diagnosis-only result with no owner action needed | No write; `diagnosis-complete` |
| Remaining supported cause with current authority, eligible basis, and proof gate | Perform only the bounded phase write; no terminal success until validation completes |
| Correction and the unchanged reproduction, proof, and blast-radius checks pass | `fix-applied` |
| Another identified owner must act | `routed-to-owner` |

Every completed invocation emits exactly one terminal result: `diagnosis-complete`, `diagnosis-incomplete`, `fix-applied`, `routed-to-owner`, or `blocked`. Internal investigation may continue, but a completion claim cannot combine terminal results.

For governed context, use the same fail-closed signal model as other published skills:

```text
no-governed-signal
single-governed-candidate
invalid-or-ambiguous-governed-signal
```

A valid governed candidate may read the exact current change, plan, and approved commands needed to bound the fix. Loading or discovering that context never grants workflow mutation. Invalid, conflicting, escaped, duplicated, or stale signals stop without falling back to portable behavior.

Use this exact repository-write boundary:

| Context and operation | Permitted writes |
| --- | --- |
| Portable `diagnose-only` | None |
| Portable `fix`, proof authoring | Request-bound tests, fixtures, test-only helpers, or controlled reproduction artifacts within the recorded defect scope |
| Portable `fix`, production correction | Request-bound implementation and explicitly scoped directly coupled non-authoritative documentation or examples |
| Governed `diagnose-only` | None |
| Governed `fix`, proof authoring | Exact governed tests, fixtures, test-only helpers, controlled reproduction artifacts, and existing explicitly authorized bugfix evidence destination |
| Governed `fix`, production correction | Exact governed implementation and existing evidence destination; directly coupled non-authoritative documentation only when the governing scope names it |

The following surfaces are always read-only to `bugfix`: proposals, specifications, architecture and ADRs, plans, `change.yaml`, workflow or automation state, reviews and review resolution, explain-change artifacts, verify evidence, PR artifacts, and release or publication state. Normative documentation changes route to the owning skill. If governed execution evidence is required but no exact existing bugfix-owned destination and authority resolve, report evidence in the invocation output and stop before claiming durable recording; do not invent a path, lifecycle entry, or workflow state. Every permitted write must remain within the exact current target and authority scope.

Completion requires rerunning the original reproduction or exact alternative, the identity-equal regression proof, and the smallest surrounding validation justified by blast radius. The output reports operation, terminal result, authority classifications, repository and defect scope, commands actually run, proof identity, unexecuted checks, uncertainty, changed surfaces, and next owner. When implementation changed, the immediate next stage is `code-review`; later `explain-change`, `verify`, and `pr` remain separate gates. No stage continues automatically.

## Expected Behavior Changes

- Root-cause questions remain read-only unless the user separately authorizes a fix.
- Direct `$bugfix` with a concrete defect and no narrower requested outcome remains an explicit fix invocation and remains isolated from automatic downstream stages; explicit diagnosis wording remains read-only.
- A missing or conflicting expected-behavior contract no longer permits a speculative product patch. Restoration may proceed only from one exact current basis that does not invent new behavior.
- Non-reproducible failures require deterministic alternative proof or stop; code inspection alone does not become successful reproduction.
- Regression-test exceptions classify feasibility separately, require a specific infeasibility rationale and deterministic regression proof, and never treat infeasibility itself as proof.
- A diagnosis expanded into a fix reruns mutation preflight against current identities and authority.
- Diagnosis commands require bounded side-effect authority despite making no intentional tracked-file changes.
- Proof-authoring writes are permitted before production mutation only within the exact test and reproduction scope.
- Post-fix validation reruns the exact proof identity established before production correction.
- Portable and governed fixes use exact write sets; all upstream lifecycle and review artifacts remain read-only.
- Every cross-axis state produces one terminal result, and `unknown` cause never supports `fix-applied`.
- Weakening a test is treated as a test-defect correction only when current contract evidence supports the new expectation.
- Successful fix output routes implementation changes to independent `code-review`, not directly to `explain-change` or `pr`.
- Result claims distinguish diagnosis, applied correction, local proof, and downstream readiness. Bugfix never claims review, verification, CI, branch, PR, release, deployment, or lifecycle completion.

## Architecture Impact

Expected assessment: `architecture-not-required`.

The change retains the existing published-skill package, canonical `skills/bugfix/SKILL.md` source, generated adapter pipeline, and project-local command model. It adds no resource, schema, state owner, service, parser, external integration, persistent transaction, or executable runtime.

Architecture becomes required if implementation introduces a debugging or repair engine, persistent bug transaction, cross-stage state owner, external issue or incident integration, repository-independent command abstraction, or a separate diagnosis skill with its own durable lifecycle.

## Testing and Verification Strategy

Add deterministic contract fixtures for at least:

- diagnosis-only requests that attempt no mutation, including explicit `$bugfix` diagnosis wording;
- explicit fixes with a reproduced failure and failing regression test;
- bare `$bugfix` with one concrete defect, conflicting intent, no concrete defect, and late diagnosis-to-fix expansion;
- command authority and side effects for read-only, generated, destructive, privileged, network, database, and external-state commands;
- exact repository, defect, path-root, write-category, command-owner, and governing-basis scope;
- ambiguous intent that blocks mutation;
- non-established failures with and without acceptable deterministic alternative proof;
- missing, conflicting, and behavior-changing contract bases;
- every mutation-eligibility row, test infeasibility without proof, and shared versus distinct reproduction/regression evidence;
- proof-authoring eligibility, forbidden production mutation before proof, and identity-equal post-fix proof reruns;
- implementation, test, environment, external dependency, race, and unknown root causes;
- restoration basis, cross-axis conflicts, owner routing, terminal results, and independent-defect decomposition;
- test weakening without contract evidence;
- governed valid, malformed, stale, conflicting, and duplicated signals;
- portable and governed write boundaries, missing governed evidence destinations, non-authoritative docs, and attempted proposal, spec, architecture, plan, change-record, workflow, review, verification, or PR-state mutation;
- successful fix handoff to `code-review` and diagnosis-only owner routing;
- exact reproduction rerun and blast-radius validation requirements;
- unknown closed-vocabulary values failing before consistency checks.

Create a rule-disposition ledger for every behaviorally meaningful line in the current `bugfix` skill and a literal-consumer inventory for validator- or documentation-sensitive terms. Prove canonical, generated, packed, archived, release-candidate, and installed package parity with existing repository tooling.

Measure LF-normalized Unicode whitespace-separated words and UTF-8 bytes for the current and proposed root. Because no resource is added, the root and complete package are the same measurement. Acceptance requires both measures to decrease; moving text to contributor-only evidence does not count as semantic preservation unless one current owner remains.

Use static scenarios and ordinary independent reviews. Do not execute Codex, Claude Code, opencode, another target agent, a live repair task, or an external issue or incident system as acceptance machinery.

Proposal acceptance requires all of the following:

| ID | Criterion |
| --- | --- |
| `AC-BUGSIM-013` | Explicit diagnosis wording selects `diagnose-only` even when `$bugfix` is named. |
| `AC-BUGSIM-014` | Bare `$bugfix` selects `fix` only with one concrete defect and no narrower requested outcome. |
| `AC-BUGSIM-015` | Conflicting intent blocks mutation, and later diagnosis-to-fix expansion reruns mutation preflight. |
| `AC-BUGSIM-016` | Automated-test feasibility and regression proof are independent closed axes. |
| `AC-BUGSIM-017` | `infeasible-with-rationale` alone never authorizes mutation. |
| `AC-BUGSIM-018` | Every mutation-eligibility combination yields fix, diagnose/route, or blocked-before-write. |
| `AC-BUGSIM-019` | Shared reproduction and regression evidence is accepted only under the exact unchanged-evidence rule. |
| `AC-BUGSIM-020` | Portable and governed diagnosis perform no writes. |
| `AC-BUGSIM-021` | Portable and governed fixes write only their exact authorized implementation, test, evidence, and non-authoritative documentation surfaces. |
| `AC-BUGSIM-022` | Upstream lifecycle, review, verification, PR, release, and publication surfaces remain read-only. |
| `AC-BUGSIM-023` | Missing governed evidence placement never creates an implicit path or lifecycle state. |
| `AC-BUGSIM-024` | Unknown closed-vocabulary values fail before consistency checks. |
| `AC-BUGSIM-025` | Operation, command authority, and repository-write authority are separate closed decisions. |
| `AC-BUGSIM-026` | Bare `$bugfix` selects fix intent without granting writes outside one request-bound or governed defect scope. |
| `AC-BUGSIM-027` | Every writable fix binds repository, defect, authority, command, path, write-category, contract, and evidence identities. |
| `AC-BUGSIM-028` | Diagnosis runs only bounded commands and performs no intentional tracked-file or external-state mutation. |
| `AC-BUGSIM-029` | Proof-authoring and production-correction writes use separate eligibility gates. |
| `AC-BUGSIM-030` | Missing regression proof permits only otherwise-authorized proof authoring and blocks production mutation. |
| `AC-BUGSIM-031` | Post-fix validation uses the exact proof identity established before production mutation. |
| `AC-BUGSIM-032` | Deterministic alternative proof records exact procedure, inputs, environment, observations, and limitations. |
| `AC-BUGSIM-033` | `resolvable-restoration` binds one conflict-free authoritative behavior basis and introduces no observable behavior. |
| `AC-BUGSIM-034` | Every cross-axis state has one deterministic action and terminal result. |
| `AC-BUGSIM-035` | Root cause `unknown` never authorizes production mutation or `fix-applied`. |
| `AC-BUGSIM-036` | Contract gaps and behavior-change requests route to the contract owner without bugfix mutation. |
| `AC-BUGSIM-037` | Test-defect correction requires a settled or restoration basis and cannot weaken expectations speculatively. |
| `AC-BUGSIM-038` | Independent defects are decomposed unless one cause, basis, scope, and proof bundle is established. |
| `AC-BUGSIM-039` | No runtime agent, repair engine, external issue integration, or persistent bug transaction is introduced. |

## Rollout and Rollback

Author the focused bugfix-skill contract amendment, record exact legacy-rule dispositions, update the canonical skill and directly coupled validators or workflow guidance, and validate generated/install parity. Historical bugfix evidence and project artifacts are not rewritten.

Roll back by reverting the canonical skill, focused contract, fixtures, and directly coupled documentation together. No data migration or external rollback is required. If the new classifications prove too verbose or fail to improve the complete package, retain the current one-file structure and restore the accepted legacy text rather than hiding cost in a new reference.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Closed classifications make a small skill longer | Remove narrative duplication and require strict complete-package word and byte reduction. |
| Diagnosis-only broadens the skill trigger unexpectedly | Keep frontmatter explicit, preserve direct `$bugfix` as fix intent for a concrete defect, and test ambiguous ordinary questions. |
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
- Make explicit requested outcome authoritative; treat bare `$bugfix` against a concrete defect as fix intent only when no narrower outcome is stated.
- Separate operation intent, command authority, and request-bound or governed repository-write authority.
- Require fresh mutation preflight when diagnosis later expands to repair.
- Separate reproduction, automated-test feasibility, regression proof, and root-cause support; infeasibility is never proof.
- Permit bounded proof authoring after non-proof prerequisites pass; require exact regression proof before production mutation.
- Bind post-fix validation to the unchanged pre-fix proof identity.
- Use exact restoration evidence, deterministic cause/basis routing, one terminal result, and one defect scope per invocation.
- Route conflicting or behavior-changing contracts to their owning stages.
- Keep governed-signal validation fail-closed without granting workflow-state authority.
- Use exact portable and governed write sets; keep upstream lifecycle and review surfaces read-only.
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

Ready for same-stage proposal rereview. This portable proposal is not accepted, does not establish a governed change, and is not ready for specification until proposal-review approves it.

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
