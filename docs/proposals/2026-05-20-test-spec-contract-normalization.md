# Proposal: Test-Spec Contract Normalization

## Status

accepted

Accepted after clean `proposal-review` round 2.

## Problem

The `test-spec` skill is behind the published-skill design contract. The other spec-family skills, `spec` and `spec-review`, were normalized in an earlier readability and self-containment pass, but `test-spec` was not. That leaves it a generation behind the contract that now governs published skill shape.

Concretely, `test-spec` lacks:

- `version` and `schema-version` front matter;
- a Workflow role block that states upstream, downstream, and must-not-claim boundaries;
- a fenced output skeleton, even though it produces a structured test-spec artifact with stable test-case IDs and coverage maps.

Its invocation stop conditions, including not generating tests from an unreviewed or unstable spec and not generating from a `not-ready` or `not-assessed` spec-review outcome, are embedded in the Rules list rather than surfaced as a visible contract boundary.

With RigorLoop now in external use, an adopter inspecting `test-spec` cold gets a less self-contained and less contract-compliant artifact than they get from `spec` or `spec-review`. This is a compliance gap, not a readability preference.

## Goals

- Add `version` and `schema-version` front matter to `test-spec`, matching the spec family.
- Add a Workflow role block stating `role_name`, `stage`, `upstream`, `downstream`, `summary`, and `must_not_claim`.
- Add a fenced output skeleton reflecting the existing required sections, test-case format, and coverage maps.
- Surface `test-spec` invocation stop conditions as a visible boundary rather than burying them in Rules.
- Preserve every rule, stop condition, coverage rule, and output obligation unchanged.

Priority order:

```text
1. preserved skill output quality
2. test-spec contract compliance
3. cross-skill consistency
```

Token cost is not a driver. This proposal adds missing contract-required structure to one skill and changes no behavior.

## Non-goals

- Do not change any normative rule, coverage rule, stop condition, or output obligation in `test-spec`.
- Do not change `test-spec`'s routing description behavior.
- Do not touch `spec` or `spec-review` in this proposal.
- Do not tabulate `test-spec`'s required-sections list or fence its enums in this proposal.
- Do not introduce `assets/`, `references/`, or `scripts/` packaging.
- Do not change adapter packaging or build scripts beyond what front-matter additions require.
- Do not retroactively rewrite generated adapter archives.

## Vision fit

fits the current vision

`VISION.md` commits RigorLoop to making artifacts easier to inspect, reason about, validate, and maintain. A skill that is behind the design contract imposes a hidden cost on every adopter who inspects it. Bringing `test-spec` into compliance closes that gap without changing what the skill does.

The proposal is falsified if normalization causes any of:

```text
- a normative rule, coverage rule, stop condition, or output obligation changes meaning;
- a lifecycle boundary is weakened or dropped;
- test-spec produces a materially different test spec on a representative input;
- the surfaced stop conditions differ in meaning from the Rules they were promoted from;
- routing behavior changes.
```

Compliance or consistency gains do not offset any of these failures.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Make test-spec contract-compliant before optimizing it | in scope | Goals, Recommended direction |
| Preserve test-spec behavior during normalization | in scope | Non-goals, Vision fit, Testing and verification strategy |
| Readability of test-spec through tabulation or enum fencing | deferred follow-up | Non-goals, Scope budget |
| Readability of spec and spec-review | deferred follow-up | Non-goals, Scope budget |
| Readability of the artifacts test-spec produces | deferred follow-up | Scope budget |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Normalize `test-spec` front matter, workflow role, stop-condition surfacing, and output skeleton | core to this proposal | This is the compliance gap the proposal exists to close. |
| Amend `specs/skill-contract.md` if a contract gap surfaces | same-slice dependency | Only needed if the current contract does not clearly define the expected field or skeleton shape. |
| Additive validator adjustment for new `test-spec` metadata | same-slice dependency | Included only if existing validation rejects the contract-compliant front matter or cannot check the required structure. |
| Rebuild or validate generated adapter outputs from canonical `skills/` | same-slice dependency | Required for current generated output when `skills/test-spec/SKILL.md` changes, unless the plan records an explicit deferral rationale. |
| Tabulate required-section prose or fence enums in `test-spec` | separate proposal | Presentation work belongs to the family-wide readability follow-up. |
| Apply readability changes to `spec` and `spec-review` | separate proposal | Family consistency should be handled in one later readability proposal. |
| Improve readability of test-spec-produced artifacts | separate proposal | This changes the produced artifact experience, not the skill contract normalization itself. |
| Introduce assets, references, scripts, or packaging changes | out of scope | Packaging is explicitly excluded from this normalization slice. |

## Context

The prior workflow audit classified `test-spec` as behind the published-skill design contract, while `spec` and `spec-review` were treated as compliant.

The accepted [RigorLoop Published Skill Design Contract](./2026-05-19-rigorloop-published-skill-design-contract.md) requires portable, self-contained published skills with clear workflow role, claim boundaries, and compact output expectations. `test-spec` is an artifact-producing lifecycle skill, so its missing role block and output skeleton are contract gaps.

This proposal is the first of a two-proposal sequence. Normalization happens first. A family-wide readability pass can then tabulate prose lists and fence enums across `spec`, `spec-review`, and `test-spec` consistently.

Normalization before optimization keeps the review surface narrow: a skill behind the contract reaches compliance before later readability, packaging, or optimization work.

## Baseline compliance audit

| Skill | Contract check | Current state | Evidence | Treatment |
|---|---|---|---|---|
| `spec` | `version` and `schema-version` front matter | present | `skills/spec/SKILL.md:3`, `skills/spec/SKILL.md:4` | no change |
| `spec` | Workflow role block | present | `skills/spec/SKILL.md:16` | no change |
| `spec` | fenced output skeleton | present | `skills/spec/SKILL.md:167` | no change |
| `spec-review` | `version` and `schema-version` front matter | present | `skills/spec-review/SKILL.md:3`, `skills/spec-review/SKILL.md:4` | no change |
| `spec-review` | Workflow role block | present | `skills/spec-review/SKILL.md:16` | no change |
| `spec-review` | fenced output skeleton | present | `skills/spec-review/SKILL.md:152` | no change |
| `test-spec` | `version` and `schema-version` front matter | missing | front matter in `skills/test-spec/SKILL.md:1` through `skills/test-spec/SKILL.md:5` has `name`, `description`, and `argument-hint` only | normalize |
| `test-spec` | Workflow role block | missing | no `## Workflow role`; `skills/test-spec/SKILL.md:8` starts the body directly after front matter | normalize |
| `test-spec` | fenced output skeleton | missing | no `## Output skeleton`; current output structure exists as required sections, test-case format, and coverage rules at `skills/test-spec/SKILL.md:51`, `skills/test-spec/SKILL.md:75`, and `skills/test-spec/SKILL.md:89` | normalize |
| `test-spec` | stop conditions surfaced | buried in Rules | stop conditions are Rules items at `skills/test-spec/SKILL.md:98` and `skills/test-spec/SKILL.md:99` | surface |

The implementation plan may refine line citations after proposal edits, but it must preserve this baseline finding: `test-spec` is the only spec-family skill in this proposal that lacks the contract-required structure.

## Options considered

### Option 1: Do nothing

Leave `test-spec` behind the contract.

Pros: zero effort and zero immediate regression risk.

Cons: `test-spec` remains non-compliant while adopters inspect it; the spec family remains inconsistent; the gap will have to be closed eventually and is cheap to close now.

### Option 2: Normalize and apply readability in one change

Add the missing contract-required structure and also tabulate lists and fence enums for `test-spec`.

Pros: one pass for `test-spec`.

Cons: mixes compliance work with presentation work; the readability pass should cover all three spec-family skills together for consistency; bundling repeats the scope-mixing failure mode already identified in prior discussion.

### Option 3: Normalize only; defer all readability to the family-wide follow-on

Add only the contract-required structure: front matter, Workflow role, output skeleton, and surfaced stop conditions. Defer tabulation and enum fencing to the readability proposal that covers all three spec-family skills.

Pros: single concern, clean rollback, smallest reviewable change, and consistent future readability treatment across the family.

Cons: `test-spec` briefly remains less readable than ideal until the follow-on lands.

## Recommended direction

Choose Option 3.

Normalize `test-spec` to the contract and nothing more. Readability is deferred to the family-wide follow-on so all three spec-family skills get consistent treatment in one pass.

Concrete changes to `skills/test-spec/SKILL.md`:

| Change | Description |
|---|---|
| Add front-matter version fields | Add `version: "1.0.0"` and `schema-version: skill-readability-v1` to match `spec` and `spec-review`, unless the contract names a newer current schema. |
| Add Workflow role block | Use `role_name: test-spec`; `stage: authoring`; `upstream`: approved spec, spec-review findings, approved plan; `downstream`: implement; `summary`: design the proof mapping requirements, examples, and edge cases to tests before implementation; `must_not_claim`: implementation completion, code-review approval, verification, branch readiness, or PR readiness. |
| Add fenced output skeleton | Add a fenced skeleton reflecting the existing required sections, existing test-case format, and existing coverage maps. The skeleton documents the shape `test-spec` already produces and adds no new obligation. |
| Surface stop conditions | Promote the unreviewed or unstable spec and `not-ready` or `not-assessed` spec-review stop conditions from Rules into a visible stop-conditions area, matching the existing spec-family boundary style. |

This proposal will not attempt:

```text
- tabulation of the required-sections list;
- enum fencing;
- changes to spec or spec-review;
- packaging changes;
- routing or description changes;
- normative rule, coverage rule, stop condition, or output obligation changes.
```

## Content-preservation proof

Implementation must record a preservation matrix before `code-review` for every moved or skeletonized rule, stop condition, coverage rule, and output obligation.

| Source content | Existing location | New location | Change type | Preservation proof |
|---|---|---|---|---|
| Unreviewed or unstable spec stop condition | Rules item in `skills/test-spec/SKILL.md` | dedicated `Stop conditions` section | moved | exact text or meaning preserved |
| `not-ready` or `not-assessed` spec-review stop condition | Rules item in `skills/test-spec/SKILL.md` | dedicated `Stop conditions` section | moved | exact text or meaning preserved |
| Required test-spec section list | Required sections in `skills/test-spec/SKILL.md` | fenced output skeleton | skeletonized | same section set |
| Test-case ID and field format | Test case format in `skills/test-spec/SKILL.md` | fenced output skeleton | skeletonized | same format and required fields |
| Coverage map obligations | Required sections and Coverage rules in `skills/test-spec/SKILL.md` | fenced output skeleton | skeletonized | same coverage obligations |

Acceptance criteria:

```text
- Each promoted stop condition has a source and destination recorded.
- The output skeleton contains the same required section set as the existing rule text.
- The skeleton does not add or remove any coverage-map obligation.
- The representative output comparison shows no material output change.
```

A structural pass alone is insufficient if behavior-significant wording moved.

## Expected behavior changes

- A reader inspecting `test-spec` sees the same front-matter, Workflow role, and output-skeleton shape as `spec` and `spec-review`.
- `test-spec` passes the published-skill design contract checks for front matter, Workflow role, and output skeleton.
- The stop conditions are visible as a boundary rather than buried in Rules.
- `test-spec` produces the same test spec on a representative input as before.
- No coverage rule, stop condition, output obligation, or routing behavior changes.

## Architecture impact

| Surface | Impact |
|---|---|
| `skills/test-spec/SKILL.md` | Front-matter version fields, Workflow role block, fenced output skeleton added; stop conditions surfaced; normative content unchanged. |
| `scripts/validate-skills.py` | May need an additive update if validation does not recognize or check the new contract-compliant structure. |
| Adapter outputs | Current generated output must be rebuilt or validated from canonical `skills/`, unless the plan records an explicit deferral rationale; no hand editing. |
| `spec`, `spec-review` skills | No change. |
| Skill packaging or build pipeline | No intended change. |

## Generated adapter output boundary

This proposal does not retroactively rewrite legacy adapter archives.

If `skills/test-spec/SKILL.md` changes, current generated adapter output must be rebuilt or validated from canonical `skills/`, unless the plan records an explicit deferral with rationale. Generated adapter skill bodies must not be hand-edited.

Validation must prove the published adapter `test-spec` skill reflects the canonical skill change, or record why generated output is intentionally deferred. Candidate validation commands, using the repository's current adapter version from `dist/adapters/manifest.yaml`, are:

```bash
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --check
python scripts/validate-adapters.py --version v0.1.5
```

## Testing and verification strategy

| Level | What is verified | How |
|---|---|---|
| Behavior parity | A representative test spec generated before and after covers the same requirements, examples, and edge cases with the same structure. | Run `test-spec` against a representative spec and compare output. |
| Stop-condition preservation | Surfaced stop conditions match the Rules they were promoted from. | Diff the rule text against the new stop-conditions section. |
| Output-skeleton fidelity | The skeleton reflects the existing required sections and test-case format, adding no obligation. | Compare skeleton against the existing required-sections list and coverage-map rules. |
| Contract compliance | `test-spec` passes published-skill design contract checks for front matter, Workflow role, and output skeleton. | Run the structural validator or the repository-owned validation command named by the plan. |
| Cold-read | A fresh reader can locate `test-spec`'s role, output shape, and stop conditions without external context. | Review by a non-author or reviewer acting from the installed-skill perspective. |

The implementation proof must include the content-preservation matrix named above. The plan must name the exact representative input used for behavior parity and the validator or manual review surface used for contract compliance.

## Implementation decisions

### Schema version

Use `schema-version: skill-readability-v1`.

Rationale: this is a normalization-only change. `spec` and `spec-review` already use this schema version, and no approved newer schema version is identified for the spec-family skills.

Fallback: if `specs/skill-contract.md` names a newer required schema before implementation begins, update `test-spec` to that value and record the contract citation.

### Stop-condition shape

Use a dedicated `Stop conditions` section.

Rationale: invocation-blocking conditions should be visible before the normal artifact-generation procedure. Keeping them only in Rules would not fully solve the stated cold-read boundary problem.

Recommended implementation wording:

```md
## Stop conditions

Stop and report the blocker instead of producing a test spec when:

- the source spec is unreviewed, unstable, or not approved for test-spec work;
- the relevant spec-review outcome is `not-ready` or `not-assessed`;
- required upstream artifacts are missing or ambiguous.

These stop conditions preserve the existing Rules behavior. They do not add new
blocking states.
```

The preservation matrix must prove that each surfaced stop condition maps back to existing Rules text and that no new blocking state is added.

### Proof route

Default route: test-spec amendment is approved.

Rationale: the implementation changes `skills/test-spec/SKILL.md` structure by adding contract-required front matter, a Workflow role block, a fenced output skeleton, and a dedicated `Stop conditions` section. A focused test-spec amendment should define proof obligations for:

- front matter presence and values;
- Workflow role fields;
- output skeleton fidelity;
- stop-condition preservation;
- behavior parity on a representative input;
- generated adapter validation or explicit deferral.

Implementation must not begin until this test-spec amendment is approved, unless the plan cites exact existing contract and test coverage proving that a plan-only route is already sufficient.

Decision tree:

```text
1. If specs/skill-contract.md already defines the required shape:
   use a focused test-spec amendment.

2. If specs/skill-contract.md does not define the required shape:
   use a coupled spec/test-spec amendment packet.

3. If both existing contract and existing tests already prove the obligations:
   record that exact proof route in the plan and proceed plan-only.
```

## Amendment sequencing

This proposal may proceed as a plan-only implementation only if the existing published-skill design contract and test coverage already define:

- `version` and `schema-version` front-matter expectations;
- Workflow role block expectations;
- artifact-producing skill output skeleton expectations;
- stop-condition preservation proof;
- behavior-parity proof for representative outputs.

If any of these are missing, the plan must add the necessary spec or test-spec amendment before implementation begins.

Implementation must not begin until the plan names one approved proof route. The default route for this proposal is route 2:

1. existing contract and tests are sufficient;
2. test-spec amendment is approved;
3. spec/test-spec amendment packet is approved.

## Rollout and rollback

Rollout:

1. Review this proposal through `proposal-review`.
2. Use the default proof route, `test-spec amendment is approved`, unless the plan cites exact existing coverage for a plan-only route or discovers a contract gap requiring a spec/test-spec amendment packet.
3. Amend `specs/skill-contract.test.md` for the focused proof route, or amend `specs/skill-contract.md` plus its test spec if the contract gap route applies.
4. Plan a single-milestone change to normalize `test-spec`.
5. Run `plan-review`.
6. Amend the validator if needed for `test-spec`'s contract-compliant structure.
7. Implement the normalization and record the content-preservation matrix before `code-review`.
8. Use `code-review` to verify behavior parity, output-skeleton fidelity, and stop-condition preservation.
9. Verify validators and rebuild or validate current generated adapter output from canonical `skills/`, unless the plan explicitly defers generated output with rationale.
10. Prepare the PR.

Rollback:

- The change should land as a focused commit with the prior version available in Git.
- Front-matter additions are additive; reverting removes them without affecting downstream consumers.
- Surfaced stop conditions can revert to their prior Rules placement without behavior change.
- No packaged resources are added, so there is no adapter-packaging rollback surface.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Surfacing stop conditions accidentally changes their meaning | Require the content-preservation matrix to record source, destination, change type, and preservation proof for each promoted stop condition. |
| The output skeleton implies a new obligation | Require the content-preservation matrix to prove the skeleton preserves the existing required section set, test-case format, and coverage-map obligations. |
| Validator rejects the new front matter | Make any validator change additive and land it before or with the `test-spec` change. |
| Adopters depended on `test-spec`'s old internal shape | Output structure is unchanged; only metadata and stop-condition placement change. |
| Generated adapter output drifts from canonical skill source | Rebuild or validate current generated adapter output from canonical `skills/`, or require an explicit plan deferral rationale. |
| Scope creeps into readability work | Non-goals and scope budget explicitly route tabulation and enum fencing to the follow-on proposal. |

## Open questions

None.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-20 | Split `test-spec` normalization from family readability. | Compliance work and presentation work have different risk profiles and rollback contracts; bundling them was flagged as a recurring scope-mixing failure mode. | Bundle normalization and readability. |
| 2026-05-20 | Normalize before the readability pass. | A skill behind the contract should reach compliance before consistent family-wide readability work. | Readability first; skip normalization. |
| 2026-05-20 | Defer all readability to the family-wide follow-on. | All three spec-family skills should get consistent readability treatment in one later pass. | Apply readability to `test-spec` here. |
| 2026-05-20 | Keep routing description unchanged. | The description routes adequately; changing it adds risk without serving the compliance goal. | Rewrite the description. |
| 2026-05-20 | Use `schema-version: skill-readability-v1`. | This normalizes `test-spec` to the existing spec-family schema unless the approved contract names a newer required value before implementation. | Introduce a new schema generation. |
| 2026-05-20 | Use a dedicated `Stop conditions` section. | Invocation-blocking conditions should be visible before the normal artifact-generation procedure. | Leave stop conditions only in Rules with clearer wording. |
| 2026-05-20 | Use `test-spec amendment is approved` as the default proof route. | The implementation changes the skill structure enough that focused proof obligations should be approved before implementation unless existing coverage is precisely cited. | Assume plan-only proof without citations; require a full spec/test-spec packet by default. |

## Next artifacts

```text
proposal-review
test-spec amendment and matching review by default
spec/test-spec amendment packet only if the plan finds a contract gap
plan-only route only if the plan cites exact existing contract and test coverage
plan
plan-review
validator amendment (if needed for new front matter or structural checks)
implementation: test-spec normalization
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Proposal-review: approved in [proposal-review-r2](../changes/2026-05-20-test-spec-contract-normalization/reviews/proposal-review-r2.md).
- Spec amendment: [Skill Contract](../../specs/skill-contract.md).

## Readiness

Accepted and ready for the approved proof-route work.

Core invariant:

```text
This proposal changes test-spec's structure and metadata to match the
published-skill design contract. It does not change what test-spec does.

Every rule, coverage rule, stop condition, and output obligation is preserved.
test-spec produces the same test spec on a representative input after
normalization as before it.
```
