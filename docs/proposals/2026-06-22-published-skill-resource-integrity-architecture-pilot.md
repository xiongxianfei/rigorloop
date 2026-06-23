# Proposal: Published Skill Resource Integrity with an Architecture-Skill Pilot

## Status

accepted

## Problem

A recent architecture-authoring run exposed an installed-skill packaging defect.

The installed file:

```text
.agents/skills/architecture/SKILL.md
```

referenced:

```text
templates/architecture.md
templates/diagram-styles.mmd
templates/adr.md
```

but the installed architecture-skill directory contained only `SKILL.md`.
Attempts to load the referenced resources therefore failed. The architecture
stage continued by reconstructing the required arc42, C4, and ADR structure
from the skill body and disclosed the fallback.

That fallback prevented an unnecessary workflow stop, but it does not make the
package valid.

The observed defect could originate at several boundaries:

```text
canonical skill source
-> skill build
-> adapter/package assembly
-> release archive
-> target-specific installation
-> local installed skill tree
```

The current evidence proves only that the final installed payload and the
installed `SKILL.md` disagreed. It does not yet prove whether the canonical
resources never existed, the build omitted them, adapter packaging omitted them,
installation copied only `SKILL.md`, or the local installation was stale.

This is a resource-integrity problem, not an architecture-design problem.

The broader risk is that a skill can appear valid while referencing unavailable
local resources. Depending on what those resources own, that can produce
inconsistent artifacts across agents, silent output-shape drift, invented
template content, missing required legal, security, or schema language, false
confidence that generated adapters are self-contained, and late failures in
customer repositories.

The learn session correctly recorded the incident as a single observation
rather than immediately generalizing it to all skills. It also identified a
candidate follow-up: repair the architecture package and add a lightweight check
that every referenced skill-local asset, template, reference, or script exists.

This proposal is that owner-directed follow-up.

## Goals

- Identify the exact boundary where the architecture resource files were lost.
- Make the canonical architecture skill internally consistent.
- Ensure every skill-local resource named by `SKILL.md` exists in canonical
  source.
- Ensure mapped resources survive build, adapter packaging, release packaging,
  and installation.
- Replace ad hoc `templates/` references with the established `assets/`,
  `references/`, or `scripts/` resource classes unless the current skill
  contract is amended to support `templates/`.
- Add an explicit resource map to the architecture skill.
- Add deterministic resource-integrity validation.
- Add generated-package and clean-install parity proof.
- Preserve architecture skill behavior, required sections, review boundaries,
  and output quality.
- Keep runtime fallback behavior honest: a fallback may prevent unnecessary
  interruption, but it should not make a broken package pass validation.
- Use the architecture skill as the first real fixture for a reusable
  published-skill resource-integrity contract.

## Non-goals

- Do not claim that every published skill currently has missing resources.
- Do not hand-edit `.agents/skills/architecture/` as the durable fix.
- Do not treat a local copy operation as proof that canonical packaging is
  correct.
- Do not redesign the architecture lifecycle stage.
- Do not change arc42, C4, ADR, architecture-review, or lifecycle semantics.
- Do not move normative architecture rules out of `SKILL.md` merely to make the
  skill shorter.
- Do not add resources that do not earn their file.
- Do not introduce remote resource loading.
- Do not let skills download missing templates at runtime.
- Do not add a general package manifest or cryptographic installation protocol
  unless the first-slice evidence shows existing build parity checks are
  insufficient.
- Do not rewrite all skill resource layouts in this proposal.
- Do not hand-edit generated adapters or historical archives.

## Vision fit

fits the current vision

RigorLoop's installed skills are operating documentation for agents. A skill
that references absent resources is not self-contained and cannot reliably
produce reviewable, resumable artifacts.

This proposal strengthens installed-skill self-containment, generated-output
integrity, artifact consistency, customer-project reliability, and reviewability
of packaged resources.

The proposal is falsified if the architecture skill still references unavailable
local resources, canonical validation passes while clean installation omits a
mapped resource, generated adapters contain stale resource content, missing
required resources are silently treated as valid, architecture output behavior
changes unintentionally, the implementation fixes only one local `.agents`
directory, or validation relies on broad prose-path scanning instead of an
explicit resource map.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Fix the architecture skill's missing templates | in scope | Goals, Architecture resource contract |
| Determine the actual root cause | in scope | Root-cause evidence |
| Add resource-integrity validation | in scope | Resource-integrity contract |
| Preserve safe fallback behavior | in scope | Runtime fallback boundary |
| Prevent inconsistent architecture artifacts | in scope | Behavior-preservation proof |
| Generalize immediately to every skill defect | rejected option | Non-goals |
| Hand-copy files into `.agents` | rejected option | Options considered |
| Add a reusable skill-pack check | in scope | Recommended direction |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Architecture resource-chain audit | core to this proposal | The loss boundary is not yet known. |
| Architecture `SKILL.md` resource-map normalization | core to this proposal | Raw absent references created the defect. |
| Architecture structural resources | core to this proposal | Architecture and ADR skeletons are substantial structures if they earn files. |
| Diagram guidance resource | first-slice candidate | Classification depends on whether it is guidance or copied output. |
| Canonical resource-reference validation | core to this proposal | Prevents broken authored skills. |
| Generated adapter resource parity | same-slice dependency | Canonical correctness does not prove packaged correctness. |
| Clean target-install resource smoke | same-slice dependency | The observed defect was in an installed target. |
| Repository-wide mapped-resource audit | first-slice candidate | Reusable validation should be exercised across current skills. |
| Content-hash manifest for every installed skill | deferable follow-up | Inventory and byte parity may be sufficient initially. |
| Historical archive repair | out of scope | Published historical artifacts are immutable or compatibility-sensitive. |
| Runtime remote resource recovery | out of scope | It breaks self-containment and introduces network trust. |

## Context

The architecture stage handled the incident appropriately at runtime:

- it did not fabricate undocumented template content;
- it used explicit normative structure already present in `SKILL.md`;
- it disclosed the missing resources and fallback;
- it continued only because the skill body was sufficient to produce a safe
  artifact.

That behavior should remain an emergency runtime contingency. It should not
become the package contract.

The package contract should be:

```text
Every skill-local resource referenced by the skill exists in canonical source,
is included in generated output, and is present after installation.
```

The current skill contract already distinguishes packaged resources as
`assets/`, `references/`, and `scripts/`, and requires a `Resource map` when a
skill ships those resources. The architecture skill should follow that model
rather than introducing an ungoverned fourth `templates/` class unless the
published-skill contract is explicitly amended.

| Resource class | Use |
| --- | --- |
| `assets/` | Copy-and-fill output structures and reusable material |
| `references/` | Optional guidance loaded when relevant |
| `scripts/` | Deterministic repeated work |
| `SKILL.md` | Triggering, operating procedure, rules, routing, and resource map |

## Governing contract relationship

Generic published-skill resource-integrity requirements amend
`specs/skill-contract.md`.

That contract owns:

- accepted resource classes;
- resource-map verbs;
- path containment;
- mapped-resource existence;
- canonical-to-generated parity;
- installation parity;
- enforcement and compatibility rules.

The architecture pilot owns only:

- classification of the architecture resources;
- architecture output-behavior preservation;
- architecture package-chain audit;
- architecture-specific fixtures and clean-install proof.

Do not create a second generic resource contract that competes with
`specs/skill-contract.md`.

## Options considered

### Option 1: Copy the missing files into `.agents/skills/architecture/`

Pros:

- Fast local repair.
- Unblocks the current repository.

Cons:

- Fixes only one installed copy.
- Does not identify the lost-resource boundary.
- Will be overwritten by the next install or build.
- Does not protect Codex, Claude, opencode, or future releases.

Rejected.

### Option 2: Remove the resource references and keep everything inline

Pros:

- Eliminates missing-file risk.
- Keeps the installed skill self-contained in one file.
- Simplifies packaging.

Cons:

- May make `SKILL.md` unnecessarily large.
- Reintroduces substantial output skeletons into the common path.
- Loses progressive disclosure where templates genuinely earn files.
- Does not exercise or repair packaged-resource support.

Acceptable only if the referenced resources duplicate the skill body and do not
earn separate files.

### Option 3: Package the three referenced files with the architecture skill

Pros:

- Fixes the observed architecture defect.
- Preserves the existing intended resource model.
- Small implementation surface.

Cons:

- Does not prevent recurrence in other skills.
- Does not prove resources survive all generation and installation boundaries.
- May preserve an unclear `templates/` resource class.

Insufficient alone.

### Option 4: Repair architecture resources and add canonical reference validation

Pros:

- Fixes the observed skill.
- Prevents canonical skills from naming absent resources.
- Produces reusable validation.

Cons:

- Still does not prove adapter or installed-tree parity.

Better, but incomplete.

### Option 5: Repair architecture resources and validate the complete packaging chain

Validate:

```text
canonical skill
-> built skill
-> adapter/package
-> clean installation
```

Pros:

- Fixes the observed defect.
- Identifies the actual loss boundary.
- Prevents canonical, generated, and installed drift.
- Creates a reusable resource-integrity model.
- Preserves skill self-containment.

Cons:

- Touches validators, build/package tests, and installation smoke.
- Requires explicit resource classification and fixtures.

Recommended.

## Recommended direction

Choose Option 5.

Use the architecture skill as a focused pilot for a general published-skill
resource-integrity contract.

The first slice should:

1. audit the architecture skill across every packaging boundary;
2. normalize its resource map;
3. package resources that earn their files;
4. remove stale or redundant references;
5. add canonical resource-reference validation;
6. add generated-output inventory or byte-parity checks;
7. add clean-install smoke for supported targets;
8. run the reusable validator across all current published skills before
   enabling repository-wide enforcement.

The downstream plan should consider these sequencing slices:

| Slice | Scope |
| --- | --- |
| M1 | Architecture resource-chain audit |
| M2 | Governing contract and validator fixtures |
| M3 | Architecture resource normalization and behavior preservation |
| M4 | Generated package parity |
| M5 | Packed clean-install smoke for all targets |
| M6 | Repository-wide audit and enforcement decision |

Root-cause discovery and canonical resource creation should not be combined in
the same slice. First identify the first divergent layer; then choose
whether to add, rename, package, or remove resources.

### Architecture resource contract

Recommended candidate layout:

```text
skills/architecture/
  SKILL.md
  assets/
    architecture-skeleton.md
    adr-skeleton.md
  references/
    diagram-conventions.md
```

| Current reference | Candidate location | Reason |
| --- | --- | --- |
| `templates/architecture.md` | `assets/architecture-skeleton.md` | Copy-and-fill architecture output structure |
| `templates/adr.md` | `assets/adr-skeleton.md` | Copy-and-fill ADR structure |
| `templates/diagram-styles.mmd` | `references/diagram-conventions.md` | Readable diagram guidance, if it is policy or convention |
| `templates/diagram-styles.mmd` | `assets/diagram-styles.mmd` | Use this only if it is literal copied Mermaid material |

The implementation plan should inspect the actual intended content before
choosing whether diagram styles are an asset or a reference. It should not
create a resource merely because a stale path exists; each resource should earn
its file.

The architecture `SKILL.md` should explicitly map every resource:

```md
## Resource map

- COPY `assets/architecture-skeleton.md` when creating a new architecture
  package.
  Fill all required sections. Do not emit unfilled placeholders.

- COPY `assets/adr-skeleton.md` when recording a material architecture decision.
  Fill decision, context, status, consequences, and alternatives.

- READ `references/diagram-conventions.md` when producing or reviewing C4,
  Mermaid, dependency, data-flow, or control-flow diagrams.
```

Do not rely on raw prose such as `Use templates/architecture.md`.

Keep these in `SKILL.md`: when architecture is required, workflow role, inputs,
architecture review boundary, arc42/C4/ADR obligations, security and
trust-boundary rules, stop conditions, claim boundaries, handoff behavior, and
resource usage instructions.

Resources may contain headings, field labels, placeholders, short fill
instructions, diagram examples, or conventions. Resources should not become
hidden owners of architecture trigger logic, required lifecycle stages, security
policy, review approval rules, status enums, or verification claims.

### Resource-integrity contract

For every explicit skill-local resource-map entry:

- the path should be relative to the skill root;
- the path should resolve inside the skill root;
- the file should exist;
- the resource class should match its verb;
- the resource should be packageable;
- path traversal should fail validation;
- no required resource should be supplied only by the maintainer repository root.

Recommended verb-to-class rules:

| Verb | Allowed path class |
| --- | --- |
| `COPY` | `assets/` |
| `READ` | `references/` |
| `RUN` | `scripts/` |

If `templates/` remains supported, the published-skill contract should
explicitly define its verb and packaging semantics. Do not add implicit support
only for architecture.

### Unmapped resource-reference boundary

Steady-state published skills should express skill-local resource dependencies
in the explicit `Resource map`.

Canonical validation checks mapped entries deterministically.

The first slice also adds a bounded migration lint for legacy skill-local
resource references outside the `Resource map`. It examines recognized
resource-loading instructions and approved skill-local prefixes such as:

- `assets/`
- `references/`
- `scripts/`
- legacy `templates/`

It does not treat arbitrary repository paths, artifact examples, or code
snippets as resource dependencies.

An unmapped skill-local resource reference fails validation or is recorded as
migration debt under an explicitly approved temporary exception.

### Resource parity identity

For generated-output parity, each mapped canonical resource should preserve its
relative path, file presence, and file identity in generated or adapter output.

For resources copied without transformation, parity is defined by:

- canonical relative path within the skill root;
- SHA-256 of raw file bytes.

File timestamps do not participate.

Line-ending normalization or content rewriting is not allowed unless an explicit
transformation contract names:

- input path;
- transformation owner;
- output path;
- expected output identity;
- validation command.

Target install roots may differ, but the relative path beneath the installed
skill root should match the canonical resource path.

For generated and installed output, compare canonical, generated, and installed
relative-file inventories. For mapped resources, compare raw-byte SHA-256 to
catch stale copies.

### Clean-install proof source

For clean-install parity, install the current package into empty temporary
repositories for each supported target:

```text
codex
claude
opencode
```

Then verify that the installed architecture skill contains `SKILL.md` and all
mapped assets, references, and scripts. The smoke should inspect the real
installed tree, not only a dry-run plan.

Pre-publish clean-install smoke should use the locally packed release candidate,
not an unpackaged source directory and not a dry-run plan.

Live registry installation is post-publish release evidence and is not required
to close the implementation milestone unless the release contract explicitly
requires it.

### Runtime fallback boundary

A runtime fallback is an emergency behavior, not a passing package state.

| Situation | Runtime behavior | Validation result |
| --- | --- | --- |
| Optional resource not needed for current invocation | Do not load it | pass |
| Mapped resource exists | Load according to resource map | pass |
| Required normative, schema, security, or legal resource is missing | Stop and report package-integrity blocker | fail |
| Required non-obvious structural asset is missing | Stop and report package-integrity blocker | fail |
| Redundant convenience resource is missing, but `SKILL.md` fully defines the complete contract | Continue only if output remains compliant; disclose fallback | package validation still fails |
| Agent would need to invent resource contents | Stop | fail |

A fallback should never cause canonical, build, or release validation to report
the package as valid.

### Root-cause evidence

Create:

```text
docs/changes/<change-id>/architecture-resource-chain-audit.md
```

Required matrix:

| Layer | Expected path | Present? | Content identity | Result |
| --- | --- | ---: | --- | --- |
| Canonical architecture skill | `<canonical path>` | yes/no | hash | pass/fail |
| Built skill output | `<build path>` | yes/no | hash | pass/fail |
| Codex package/archive | `<path>` | yes/no | hash | pass/fail |
| Claude package/archive | `<path>` | yes/no | hash | pass/fail |
| opencode package/archive | `<path>` | yes/no | hash | pass/fail |
| Clean Codex install | `.agents/skills/architecture/...` | yes/no | hash | pass/fail |
| Clean Claude install | target-specific path | yes/no | hash | pass/fail |
| Clean opencode install | target-specific path | yes/no | hash | pass/fail |

The audit should identify the first layer where expected and actual inventory
diverge.

## Expected behavior changes

- The architecture skill no longer references unavailable resources.
- Architecture and ADR skeletons are packaged if they earn their files.
- Diagram guidance is explicitly classified as an asset or reference.
- Missing mapped resources fail canonical validation.
- Generated adapters cannot silently omit mapped resources.
- Clean installation proves the actual installed skill is self-contained.
- Runtime fallbacks remain available only as disclosed contingencies.
- Architecture output behavior remains unchanged.

## Architecture impact

| Surface | Impact |
| --- | --- |
| Canonical architecture skill | Normalize resource map and paths |
| Architecture skill-local resources | Add, rename, or remove files according to classification |
| Skill validation | Validate mapped-resource existence and class |
| Skill build | Preserve mapped resource directories |
| Adapter/package build | Preserve inventory and content |
| Installation smoke | Verify architecture resources after install |
| Generated adapters | Rebuild or validate; never hand-edit |
| Project architecture artifacts | No intended content or path change |
| Runtime application code | No change |

Because this touches canonical source, build output, target packaging, and
installed payloads, architecture assessment is recommended before implementation
if the current packaging boundaries are not already documented.

## Testing and verification strategy

| Check ID | What is verified |
| --- | --- |
| `SRI-001` | Every architecture resource-map path exists in canonical source. |
| `SRI-002` | `COPY` points only to approved asset paths. |
| `SRI-003` | `READ` points only to approved reference paths. |
| `SRI-004` | Path traversal and repository-root dependencies fail. |
| `SRI-005` | Deleting `architecture-skeleton.md` from a fixture fails with a stable diagnostic. |
| `SRI-006` | Deleting `adr-skeleton.md` from a fixture fails. |
| `SRI-007` | A stale content copy in generated output fails parity validation. |
| `SRI-008` | Generated Codex package includes all architecture resources. |
| `SRI-009` | Generated Claude package includes all architecture resources. |
| `SRI-010` | Generated opencode package includes all architecture resources. |
| `SRI-011` | Clean Codex installation includes all mapped architecture resources. |
| `SRI-012` | Clean Claude installation includes all mapped architecture resources. |
| `SRI-013` | Clean opencode installation includes all mapped architecture resources. |
| `SRI-014` | A legacy `templates/...` instruction outside the Resource map is detected. |
| `SRI-015` | Ordinary repository paths and artifact examples are not falsely classified as skill-local resources. |
| `SRI-016` | After migration, all required skill-local resources are declared in the Resource map. |
| `SRI-017` | Architecture skill remains usable without RigorLoop repository-internal files. |
| `SRI-018` | Required arc42/C4/ADR output obligations remain unchanged. |
| `SRI-019` | Missing-resource runtime fallback is disclosed but does not make package validation pass. |
| `SRI-020` | No generated adapter output is hand-edited. |

Acceptance criteria:

| ID | Criterion |
| --- | --- |
| `AC-SRI-001` | The first layer that omitted the architecture resources is identified. |
| `AC-SRI-002` | Generic resource-integrity rules are specified as amendments to `specs/skill-contract.md`, not as a competing contract. |
| `AC-SRI-003` | The canonical architecture skill has an explicit resource map. |
| `AC-SRI-004` | Every mapped architecture resource exists in canonical source. |
| `AC-SRI-005` | Every mapped resource is present and current in generated output. |
| `AC-SRI-006` | Every mapped resource is present after clean Codex installation. |
| `AC-SRI-007` | Every mapped resource is present after clean Claude installation. |
| `AC-SRI-008` | Every mapped resource is present after clean opencode installation. |
| `AC-SRI-009` | Missing-resource fixtures fail with stable diagnostics. |
| `AC-SRI-010` | Stale generated resource content fails raw-byte SHA-256 parity validation. |
| `AC-SRI-011` | Architecture and ADR structural output obligations remain unchanged. |
| `AC-SRI-012` | Runtime fallback does not convert a broken package into a passing package. |
| `AC-SRI-013` | No generated or installed skill output is hand-edited as the durable fix. |
| `AC-SRI-014` | A legacy `templates/...` instruction outside the Resource map is detected. |
| `AC-SRI-015` | Ordinary repository paths and artifact examples are not falsely classified as skill-local resources. |
| `AC-SRI-016` | After migration, all required skill-local resources are declared in the Resource map. |
| `AC-SRI-017` | Pre-publish clean-install smoke uses the locally packed release candidate. |
| `AC-SRI-018` | Repository-wide enforcement is enabled only after the current mapped-resource audit is clean or separately resolved. |

Create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Required matrix:

| Surface | Baseline | New proof | Preservation |
| --- | --- | --- | --- |
| Architecture trigger | Current workflow rules | Same rules | preserved |
| arc42 sections | Current skill obligations | Skeleton/output comparison | preserved |
| C4 diagrams | Current skill obligations | Representative output | preserved |
| ADR structure | Current skill obligations | Skeleton/output comparison | preserved |
| Architecture review | Current review boundary | unchanged | preserved |
| Handoff | Current downstream routing | unchanged | preserved |
| Resource availability | installed resources missing | clean-install proof | strengthened |
| Generated package parity | unproven for named resources | inventory/hash proof | strengthened |

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Amend `specs/skill-contract.md` with focused published-skill
   resource-integrity requirements.
3. Review the spec.
4. Assess packaging architecture if ownership boundaries are not already
   explicit.
5. Write the test spec.
6. Write and review the implementation plan.
7. Record canonical/build/package/install baseline.
8. Normalize architecture resources and resource map.
9. Add canonical validation.
10. Add bounded legacy-reference lint.
11. Add generated-output raw-byte SHA-256 parity validation.
12. Add packed release-candidate clean target-install smoke.
13. Run a repository-wide mapped-resource audit.
14. Review implementation.
15. Verify generated and installed output.
16. Release through normal package generation.

Rollback:

- Restore the prior canonical architecture skill and resource layout together.
- Rebuild generated packages from canonical source.
- Do not restore a `SKILL.md` reference without restoring its resource.
- Remove new validation only if the prior package layout is restored and
  validated.
- Do not hand-copy files into installed target directories as rollback.
- Preserve the audit and finding history.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| The local install alone was stale, and canonical packaging is already correct | Audit every boundary before changing canonical files. |
| Resource validation overfits prose path mentions | Validate explicit resource-map entries and use only bounded migration lint for recognized resource-loading instructions. |
| Introducing assets moves hidden rules out of `SKILL.md` | Enforce the normative-content boundary. |
| Architecture resources duplicate the skill body | Apply the "earns its file" test; remove redundant references instead. |
| All-skill audit exposes unrelated existing drift | Record findings; expand scope only through explicit review decision. |
| Adapter parity tests become expensive | Use inventory/hash checks before full install smoke; keep full smoke target-scoped. |
| Runtime fallback hides broken packaging | Package validation remains failing even when runtime safely continues. |
| Installed paths differ by target | Validate each supported target independently. |

## Open questions

### 1. Should `templates/` become a supported packaged-resource class?

Decision:

```text
No. Normalize architecture resources into the established assets/ and
references/ classes. Add templates/ only through a future skill-contract
amendment with a distinct semantic need.
```

### 2. Should generated parity compare file presence only or file contents?

Decision:

```text
Compare both relative paths and raw-byte SHA-256. Presence-only checks cannot
detect stale packaged copies.
```

### 3. Should resource validation scan arbitrary Markdown path references?

Decision:

```text
No broad scan. Use explicit resource-map validation plus a bounded
legacy-reference lint for recognized resource-loading instructions and prefixes.
```

### 4. Should missing resources always stop skill execution?

Decision:

```text
No at runtime, but yes for package validation. Stop when a missing resource owns
normative, schema, security, legal, or non-obvious structural content. A bounded
disclosed fallback may continue only when the resource is redundant convenience
material and SKILL.md already contains the complete contract.
```

### 5. Should the generic validator be enabled for all published skills immediately?

Decision:

```text
No. Implement validator in audit mode, audit all current published skills,
resolve or explicitly defer current drift, then enable repository-wide
enforcement. Require enforcement for all new or changed skills immediately.
```

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-22 | Treat the incident as package integrity, not architecture design failure. | Installed instructions referenced unavailable local resources. | Rewrite the produced architecture artifact. |
| 2026-06-22 | Audit the full canonical-to-install chain. | The current evidence does not identify the loss boundary. | Assume the installer alone is broken. |
| 2026-06-22 | Prefer established resource classes. | Assets, references, and scripts already have clear progressive-disclosure semantics in the skill contract. | Add implicit `templates/` support for one skill. |
| 2026-06-22 | Validate explicit resource maps. | Deterministic and less brittle than scanning arbitrary prose. | Regex every path-like string in every skill. |
| 2026-06-22 | Preserve fallback only as runtime contingency. | Safe continuation is useful, but broken packaging should remain visible. | Treat fallback as package success. |
| 2026-06-22 | Amend `specs/skill-contract.md` for generic rules. | The existing skill contract already owns published-skill resource classes, resource maps, and generated-output boundaries. | Create a second generic resource-integrity contract. |
| 2026-06-22 | Add bounded unmapped legacy-reference lint. | The observed defect used raw `templates/...` instructions outside a Resource map. | Validate only existing resource-map entries; broadly scan every Markdown path. |
| 2026-06-22 | Define ordinary parity as skill-root relative path plus raw-byte SHA-256. | Test specs need deterministic identity and stale-copy detection. | Presence-only parity; timestamp-based checks; implicit line-ending normalization. |
| 2026-06-22 | Use locally packed release candidates for pre-publish clean-install proof. | Implementation closeout should prove the package that would be published, while live registry smoke belongs to release evidence. | Install from unpackaged source directory; require live registry proof before implementation closeout. |

## Next artifacts

```text
proposal-review
spec: published skill resource integrity
spec-review
architecture, if package/build boundaries need clarification
architecture-review, if architecture is required
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

Potential future proposals after this proposal settles:

- Generated skill-package resource manifest if inventory/hash checks prove
  insufficient.
- Historical adapter archive diagnostics.
- Resource-integrity reporting in the package CLI.
- Broader progressive-disclosure normalization if the all-skill audit reveals
  recurring legacy resource classes.

## Follow-on artifacts

- Proposal-review: [proposal-review-r1](../changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/proposal-review-r1.md).

## Readiness

Accepted after clean proposal-review. Ready for `spec` as an amendment to
`specs/skill-contract.md`.

## Core invariant

```text
A published skill must never instruct an agent to load a skill-local resource
that was not packaged with that skill.

Canonical source, generated packages, and installed target trees must agree on
every mapped resource.

A runtime fallback may preserve useful work, but it must never hide or validate
a broken skill package.
```
