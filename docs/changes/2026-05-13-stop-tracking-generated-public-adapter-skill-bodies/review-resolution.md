# Stop Tracking Generated Public Adapter Skill Bodies Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the v0.1.3 generated public adapter skill-body untracking proposal.

Closeout status: closed

## Resolution Entries

### proposal-review-r1

Review closeout: closed

#### PAU-R1

Finding ID: PAU-R1
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Revise the proposal before spec/plan so the v0.1.3 release scope explicitly includes updates to root contributor and workflow guidance affected by retiring tracked public adapter skill bodies, or records why a higher-priority source makes those updates unnecessary.
Rationale: The proposal changes a contributor-facing source/install contract. `CONSTITUTION.md` currently says local Codex users install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/`, and that public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window. Once `v0.1.3` removes tracked generated skill bodies, downstream spec and implementation need an explicit guidance-update target for `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` or a documented unaffected rationale.
Chosen action: Add root guidance alignment to the proposal. The release scope must audit and update `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `dist/adapters/README.md`, and release notes when their wording would otherwise preserve the old tracked adapter skill-body install contract.
Safe resolution path: Add a proposal section or revise Architecture impact / Goals / Testing to require updating affected root and workflow guidance in the same release slice, including `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` when their current wording would become stale. Then rerun proposal-review.
Validation target: `proposal-review-r2` approves the revised proposal with PAU-R1 closed.
Validation evidence: The proposal now includes `Root guidance alignment`, lists affected surfaces including `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `dist/adapters/README.md`, and release notes, adds root-guidance audit validation, and adds acceptance criteria for updated or explicitly unaffected root guidance. `proposal-review-r2` approved the revised proposal with no material findings.

### proposal-review-r2

No material findings.

### spec-review-r1

Review closeout: closed

#### SGPA-SR1

Finding ID: SGPA-SR1
Disposition: accepted
Owner: spec author
Owning stage: spec
Required outcome: The spec must explicitly define its relationship to earlier approved adapter specs before downstream architecture, planning, or test-spec work relies on it.
Rationale: `specs/multi-agent-adapters-first-public-release.md` defines tracked generated adapter packages under `dist/adapters/<adapter>/` as the public adapter package surface and requires validation to fail when generated packages are missing or stale. The new `v0.1.3` spec instead requires only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` to remain tracked under `dist/adapters/`, with complete adapter packages generated into temporary output and release archives. Both directions can be valid across release phases, but the new spec does not state that it supersedes the prior tracked-package contract for `v0.1.3` and later.
Chosen action: Add a `Relationship to prior adapter specs` section to `specs/stop-tracking-generated-public-adapter-skill-bodies.md`. The section states that, for `v0.1.3` and later, this spec supersedes tracked-package and repository-tree install requirements from prior adapter specs while preserving adapter support, generation, validation, release archives, metadata, checksums, and smoke/release verification obligations. Also add version scope, tracked-surface, validation-replacement, test-spec coverage, and acceptance criteria.
Safe resolution path: Add a section such as `Relationship to prior adapter specs` that says this spec supersedes the tracked-package and repository-tree install requirements from `specs/multi-agent-adapters-first-public-release.md` and the compatibility-window portions of `specs/public-adapter-artifact-migration-examples-concise-skill-release.md` for `v0.1.3` and later, while preserving adapter support, generated output validation, release archive generation, metadata, checksums, and smoke/validation obligations through temporary or release-output artifacts.
Validation target: `spec-review-r2` approves the revised spec with SGPA-SR1 closed.
Validation evidence: The spec now includes `Relationship to prior adapter specs`, version-scope requirements `R0` through `R0b`, tracked-surface requirements `R15a` through `R15d`, validation-replacement requirements `R41a` through `R41g`, test-spec coverage requirements `R62` through `R68`, and acceptance criteria for supersession scope and preserved active obligations. `spec-review-r2` approved the revised spec with no material findings.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.
