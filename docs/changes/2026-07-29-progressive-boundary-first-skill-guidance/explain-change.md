# Change rationale: Progressive Boundary-First Skill Guidance

## Summary

This change makes concise boundary awareness automatic in ten governed skills
without requiring the user to name `boundary-first-method-v1`.
It replaces one large shared reference with a compact core plus owner-specific
feature and proof guidance, lets downstream stages consume approved IDs instead
of recreating the model, and removes artifact-lifecycle validation from
skill-only path selection while preserving it for actual lifecycle artifacts.

The capability remains `pending`.
This branch prepares and proves one coherent candidate bundle; it does not
activate the capability or publish a release.

## Problem

The previous design loaded the same full boundary model into every related
skill and relied too heavily on explicit method-name invocation.
That was inconvenient for users, duplicated context across stages, encouraged
stage-local reinterpretation, and made a skill-only change select a lifecycle
checker that did not own published skill prose.
At the same time, deleting boundary coverage or lifecycle validation wholesale
would have weakened correctness for behavior-changing specs and governed
artifacts.

## Decision trail

- The proposal selected Option 2: one compact core, stage-family references,
  and approved artifact-slice consumption.
- `PBS-R001` through `PBS-R038` define the resulting trigger, ownership,
  routing, compatibility, projection, and recovery contract.
- ADR-20260729 makes `specs/boundary-first-resources.yaml` the sole closed
  projection manifest and separates the tracked activation transaction from
  temporary generated, archive, and install proof.
- The plan divided implementation into M1 resource projection, M2 shipped skill
  guidance, M3 selector routing, and M4 package and activation readiness.
- `PRF-001` through `PRF-023` connect the approved boundary and interaction IDs
  to concrete tests and milestone evidence.

## Diff rationale by area

| Area | Change | Why | Source and evidence |
| --- | --- | --- | --- |
| Canonical boundary resources | Added a compact scan, feature-authoring guidance, proof guidance, and the closed resource manifest. | Preserve one semantic model while loading only the guidance each stage owns. | `PBS-R012`-`PBS-R024`; ADR-20260729; `evidence/m1-resource-projection.md` |
| Projection and validation | Made manifest parsing fail closed, projected exactly 14 governed resources, and added containment, atomic restoration, drift, interruption, retry, and identity checks. | A partial or unsafe projection must never become an accepted candidate. | `PBS-R013`-`PBS-R015`, `PBS-R032`-`PBS-R038`; M1; `PRF-005`, `PRF-008`, `PRF-011`-`PRF-013` |
| Ten governed skills | Added the same prompt-independent four-question compact scan; owner stages load feature/proof guidance and downstream stages begin from approved slices. | Boundary awareness should be automatic but concise, with no Cartesian scenario inventory or downstream semantic redefinition. | `PBS-R005`-`PBS-R024`; M2; `evidence/m2-skill-guidance.md` |
| Validation selector | Removed the skill-path branch that selected artifact-lifecycle validation; retained skill checks, selector regression, lifecycle-owned paths, and mixed-set composition. | Published skill text is not a lifecycle artifact, but real proposals, specs, plans, architecture, reviews, and change records still require lifecycle validation. | `PBS-R025`-`PBS-R031`; M3; `evidence/m3-selector-routing.md` |
| Adapter and package validation | Required exact governed resource inventory across generated, archived, and clean-installed Codex, Claude, and opencode packages; added closed skill selection and narrow invocation-portability checks. | Package proof must preserve byte identity and portability without tracking generated adapter bodies or interpreting arbitrary Markdown. | `PBS-R032`-`PBS-R038`; `skill-contract.md` R3l; M4; `evidence/m4-package-readiness.md` |
| Activation state | Kept `specs/boundary-first-activation.yaml` pending and proved active/rollback behavior only in fixtures. | Automatic formal adoption starts only after an explicit coherent activation transaction. | `PBS-R003`-`PBS-R006`, `PBS-R034`-`PBS-R036`; ADR-20260729 |
| Change-local evidence | Recorded milestone evidence, independent review packets, resolutions, and final holistic review. | Review history and workflow state must be reconstructable without mutable status in the plan body. | `change.yaml`, `review-log.md`, `review-resolution.md`, final holistic review R1 |

## Tests added or changed

- Projection tests prove exact manifest vocabulary, inventory, identities,
  no-follow containment, interruption recovery, input-drift restoration, and
  deterministic retry.
- Boundary validation tests prove pending-versus-active behavior, atomic
  activation closure, compatibility, rollback, and fail-closed state handling.
- Skill tests prove the shared compact scan, stage-family resource ownership,
  prompt-independent behavior, scenario stop rules, and upstream gap routing.
- Selector tests prove skill-only, lifecycle-only, mixed, generated-skill, and
  selector-owning changed sets.
- Adapter tests prove exact package inventory, clean-install parity, closed
  selections, portability, and the narrow command-versus-variable/math/path
  boundaries required by `skill-contract.md` R3l.

These are repository-owned unit and integration layers because the behavior is
deterministic, local, and package-oriented; no hosted service or manual runtime
is needed to prove it.

## Validation evidence available before final verify

The final holistic review independently reran and passed:

| Command or suite | Result |
| --- | --- |
| Boundary reference tests | 28 passed |
| Boundary activation tests | 63 passed; live state remains `pending` |
| Skill validator tests | 282 passed with 16 documented skips |
| Selector tests | 141 passed |
| Artifact-lifecycle tests | 162 passed |
| Adapter distribution tests | 148 passed |
| Projection, skill, generated-skill, change-metadata, and review-artifact validators | passed |
| Exact ten-skill, three-adapter build and clean install | passed |
| `git diff --check` | passed |

The recorded broad-smoke result predates only review-evidence updates and is not
treated as final verification evidence.
Final `verify` will rerun the required command ledger against the final branch.

## Review resolution summary

The durable [review resolution](review-resolution.md) closes 66 material
findings: 65 accepted and fixed, and one rejected with contract-based rationale.
No finding remains open, no disposition is `needs-decision`, every milestone has
a clean closing review, and the final holistic review is clean.

The repeated M4 review rounds ultimately removed speculative rendered-Markdown
interpretation and kept the published-skill portability check within R3l's
narrow static scope.
The retained checker uses exact approved workflow records plus bounded lexical
checks with direct positive and negative regression coverage.

## Alternatives rejected

- Keeping the full shared reference or changing only trigger wording preserved
  unnecessary context loading.
- Giving each stage an independent model risked semantic drift.
- Generating per-stage context packets or adding a runtime service introduced
  mutable machinery without solving ownership.
- Hard byte or token budgets would turn measurements into brittle policy.
- Deleting lifecycle validation wholesale would remove protection from actual
  lifecycle-managed artifacts; only the skill-only selector route was removed.

## Scope control

This change does not activate the capability, publish adapters, introduce a
runtime service, rename `boundary-first-v1`, require Cartesian scenario sets,
move semantic ownership into validators, or make downstream stages author
upstream outcomes.
Generated packages and clean-install trees remain temporary and untracked.

## Risks and follow-ups

- Real activation and its immutable rollback release remain a later explicit
  transaction; the current tracked state is intentionally `pending`.
- The portability recognizer is more intricate than the original raw regex,
  but its vocabulary, exact records, scope, and adversarial tests are closed.
- Hosted CI has not been observed in this local workflow; final verification
  can claim only the repository-owned commands it actually runs.

PR-mode preflight later exposed one selector registration omission for the new
canonical resource-manifest YAML. The focused
[PR-readiness selector bug-fix evidence](evidence/pr-readiness-selector-bugfix.md)
records the failing reproduction, test-first correction, and scoped routing
result. This does not change the approved contract; it completes the M3 path
registration required by `PBS-R026` and `PBS-R027`.
Independent final code-review R2 approved the correction with no material
findings before fresh verification.

The reviewed implementation and durable rationale are ready for final
verification, not yet for PR handoff.
