# Published Skill Resource Integrity Architecture Pilot

## Status

Plan lifecycle state: active
Terminal disposition: none

- Owner: maintainer
- Start date: 2026-06-23
- Last updated: 2026-06-23
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved published-skill resource-integrity contract with the architecture skill as the first real fixture. The work must identify where the installed architecture resources were lost, normalize the canonical architecture skill, validate mapped resources deterministically, and prove generated, packed, and installed resource parity without hand-editing generated or installed output.

## Source artifacts

- Proposal: `docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md`
- Spec: `specs/skill-contract.md` R46-R55
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260623-published-skill-resource-integrity.md`
- Proposal review: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/proposal-review-r1.md`
- Spec review: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/spec-review-r1.md`
- Architecture review: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/architecture-review-r1.md`
- Test spec: `specs/skill-contract.test.md` T41-T48

## Context and orientation

`skills/` is the only authored skill source. Generated local Codex skill output, adapter package output, release archives, and target installed skill roots are derived surfaces and must not be hand-edited as the durable fix.

The current concrete defect is in `skills/architecture/SKILL.md`, which still contains legacy `templates/architecture.md`, `templates/diagram-styles.mmd`, and `templates/adr.md` instructions outside a `Resource map`. Root `templates/` contains the existing architecture, ADR, and diagram-style scaffolds, but `templates/` is not an approved skill-local packaged-resource class under R47e.

Existing implementation anchors:

- `scripts/skill_validation.py` and `scripts/validate-skills.py` own canonical skill validation.
- `scripts/test-skill-validator.py` and `tests/fixtures/skills/` own skill-validator regression fixtures.
- `scripts/build-skills.py` owns generated local Codex mirror output.
- `scripts/adapter_distribution.py`, `scripts/build-adapters.py`, `scripts/validate-adapters.py`, and `scripts/test-adapter-distribution.py` own generated adapter packages and release archives.
- `dist/adapters/README.md` and `dist/adapters/manifest.yaml` are tracked support surfaces; generated adapter skill bodies are release or temporary output for current releases.

## Non-goals

- Do not introduce `templates/` as an implicit packaged skill resource class.
- Do not hand-copy files into `.agents/`, `.codex/skills/`, `.claude/skills/`, `.opencode/skills/`, or generated adapter package output as the durable fix.
- Do not add remote resource loading, runtime downloading, or registry proof as implementation closeout.
- Do not redesign arc42, C4, ADR, architecture-review, or lifecycle semantics.
- Do not enable repository-wide hard enforcement for all existing skills until the audit is clean or drift is explicitly resolved, deferred, or excepted.
- Do not create a broad Markdown path scanner that classifies ordinary examples or repository paths as packaged resources.

## Requirements covered

- R46, R46a: M2 defines generic rules in `specs/skill-contract.md` implementation surfaces; M1, M3, and M6 keep architecture-pilot evidence separate.
- R47-R47e: M2 implements verb-to-class validation and `templates/` rejection; M3 migrates architecture resources to approved classes.
- R48-R48b: M2 validates canonical mapped-resource existence and packageability.
- R49-R49d: M2 adds bounded legacy-reference lint; M6 audits current skills and records any exceptions.
- R50-R50d: M4 implements relative-path plus raw-byte SHA-256 parity for generated, adapter, and archive output.
- R51, R51a: M4 adds transformation-contract validation and failure paths.
- R52-R52c: M1 records the required pre-change clean-installed target baseline; M5 turns that route into a reusable locally packed release-candidate clean-install gate; live registry proof remains release-owned.
- R53-R53b: M2 starts with audit-mode support, M6 handles repository-wide audit and enforcement decision, and new/changed skills are enforced after implementation.
- R54-R54d: M2 and M3 ensure package validation fails for missing mapped resources; M3 preserves only bounded disclosed runtime fallback behavior.
- R55-R55e: M1 records the complete architecture resource-chain audit before mutation; M3 classifies resources and preserves architecture behavior.

## SRI-PLAN1 acceptance criteria

| ID | Criterion |
| --- | --- |
| AC-SRI-PLAN1-1 | M1 requires clean-installed Codex baseline evidence. |
| AC-SRI-PLAN1-2 | M1 requires clean-installed Claude baseline evidence. |
| AC-SRI-PLAN1-3 | M1 requires clean-installed opencode baseline evidence. |
| AC-SRI-PLAN1-4 | M1 identifies the first divergent layer before architecture resources change. |
| AC-SRI-PLAN1-5 | M1 no longer contains optional installed-tree evidence language. |
| AC-SRI-PLAN1-6 | Missing clean-install tooling blocks M1 or is implemented minimally within M1; it is not deferred past M3. |
| AC-SRI-PLAN1-7 | M3 explicitly depends on reviewed, complete M1 baseline evidence. |
| AC-SRI-PLAN1-8 | M5 is reusable post-change regression enforcement, not first baseline proof. |
| AC-SRI-PLAN1-9 | Dry-run, archive-only, and unpackaged-source evidence cannot substitute for clean-installed target-tree proof. |
| AC-SRI-PLAN1-10 | No architecture resource mutation occurs before M1 code review closes. |

## Current Handoff Summary

- Current milestone: M1. Complete Architecture Resource-Chain Baseline
- Current milestone state: review-requested
- Last reviewed milestone: planning gate
- Review status: M1 implementation ready for code-review
- Remaining in-scope implementation milestones: M1, M2, M3, M4, M5, M6, M7
- Next stage: code-review M1
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: implementation milestones, code-review, any required review-resolution, explain-change, verify, and PR handoff have not run.

## Milestones

### M1. Complete Architecture Resource-Chain Baseline

- Milestone state: review-requested
- Goal: Identify the first divergent resource-chain layer before changing any canonical architecture resource reference, file, resource map, packaging behavior, or installed output.
- Requirements: R55, R55a, R55b
- Files/components likely touched:
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/architecture-resource-chain-audit.md`
  - optional minimum audit tooling only if no supported installation inspection path can produce the required baseline:
    - `scripts/audit-skill-resource-chain.py`
    - `scripts/test-skill-resource-chain-audit.py`
  - source inspection only for `skills/architecture/`, `templates/`, generated local mirror output, adapter/release-candidate archives, and real target install roots
- Dependencies:
  - approved proposal, spec, architecture, and ADR
- Tests to add/update:
  - audit helper tests only if M1 must add `scripts/audit-skill-resource-chain.py`
- Implementation steps:
  - inventory the pre-change canonical architecture skill references and current skill-local files
  - build the pre-change generated local skill mirror
  - build pre-change Codex, Claude, and opencode adapter/release candidates
  - install those pre-change candidates into empty temporary Codex, Claude, and opencode target projects through the current supported local-archive init route: `node packages/rigorloop/dist/bin/rigorloop.js init <target> --from-archive <archive> --json`
  - inspect the real installed architecture skill trees for all three targets
  - record expected resource, actual result, relative path, presence, raw-byte SHA-256 when files exist, status, commands used, temporary roots used, whether the local observed installation was reproducible, whether the defect predates package assembly, and whether any layer could not be inspected
  - identify the first resource-chain layer where expected and actual inventory diverge
  - distinguish existing root `templates/` scaffolds from packageable skill-local resources
  - keep M1 limited to baseline evidence; do not modify `skills/architecture/SKILL.md`, architecture skill-local resources, generated adapter content, archive layout, or installation behavior
  - if the CLI local-archive route cannot inspect all three installed target trees, add only the smallest audit-only helper needed for baseline inspection or mark M1 blocked
- Validation commands:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-audit-release-output`
  - `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-audit-release-output`
  - `node packages/rigorloop/dist/bin/rigorloop.js init codex --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-codex-v0.3.2.zip --json` from an empty Codex temp project
  - `node packages/rigorloop/dist/bin/rigorloop.js init claude --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-claude-v0.3.2.zip --json` from an empty Claude temp project
  - `node packages/rigorloop/dist/bin/rigorloop.js init opencode --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-opencode-v0.3.2.zip --json` from an empty opencode temp project
  - `python scripts/audit-skill-resource-chain.py --skill architecture --release-output-dir /tmp/rigorloop-sri-audit-release-output --target codex --target claude --target opencode` if M1 adds the audit-only helper
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/architecture-resource-chain-audit.md`
- Expected observable result: audit names the first divergent layer and blocks resource creation until complete canonical, built, adapter/archive, release-candidate, and clean-installed Codex, Claude, and opencode evidence is recorded.
- Commit message: `M1: record architecture resource-chain audit`
- Milestone closeout:
  - pre-change canonical resource inventory recorded
  - pre-change built-skill inventory recorded
  - pre-change adapter/archive inventories recorded for Codex, Claude, and opencode
  - pre-change clean-installed target inventories recorded for Codex, Claude, and opencode
  - first divergent layer identified
  - no architecture resource or resource-reference change occurred during M1
  - audit commands and evidence are replayable
  - validation passed
  - code review closes cleanly
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - audit may expose that release/archive tooling or package metadata cannot yet inspect all installed roots
  - local installed state may be stale and not representative
- Rollback/recovery:
  - clean-installed Codex, Claude, and opencode target-tree inspection is mandatory baseline evidence; if an installed target cannot be inspected, M1 is blocked and M3 must not begin
  - do not substitute archive presence, dry-run output, or an unpackaged source directory for installed-tree proof

`architecture-resource-chain-audit.md` must contain this matrix:

| Layer | Candidate/source | Expected resource | Actual result | Raw SHA-256 | Status |
| --- | --- | --- | --- | --- | --- |
| Canonical skill source | working tree | legacy referenced paths/resources | present/missing | hash or N/A | pass/fail |
| Generated local mirror | pre-change build | same relative inventory | present/missing | hash or N/A | pass/fail |
| Codex adapter/archive | pre-change candidate | same relative inventory | present/missing | hash or N/A | pass/fail |
| Claude adapter/archive | pre-change candidate | same relative inventory | present/missing | hash or N/A | pass/fail |
| opencode adapter/archive | pre-change candidate | same relative inventory | present/missing | hash or N/A | pass/fail |
| Clean Codex install | empty temp project | installed architecture tree | present/missing | hash or N/A | pass/fail |
| Clean Claude install | empty temp project | installed architecture tree | present/missing | hash or N/A | pass/fail |
| Clean opencode install | empty temp project | installed architecture tree | present/missing | hash or N/A | pass/fail |

The audit must also record:

- first divergent layer;
- whether the local observed installation was reproducible;
- whether the defect predates package assembly;
- whether any layer could not be inspected;
- commands used;
- temporary roots used.

A layer marked unproved blocks M1 closeout.

### M2. Canonical Resource-Integrity Validator and Fixtures

- Milestone state: planned
- Goal: Implement deterministic canonical validation for resource maps, approved resource classes, path containment, mapped-resource existence, and bounded legacy-reference lint.
- Requirements: R46-R49d, R53-R53b, R54-R54a
- Files/components likely touched:
  - `scripts/skill_validation.py`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `tests/fixtures/skills/published-design/`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/validator-fixtures.md`
- Dependencies:
  - M1 audit recorded
  - test spec approved
- Tests to add/update:
  - fixture for valid `COPY assets/...`, `READ references/...`, and `RUN scripts/...`
  - fixture for missing mapped resource
  - fixture for path traversal
  - fixture for `COPY references/...`, `READ assets/...`, and `RUN assets/...`
  - fixture for legacy `templates/...` outside `Resource map`
  - fixture proving ordinary `docs/...`, code snippets, and artifact examples are not false positives
  - fixture for approved temporary migration exception if the final validator supports exceptions
- Implementation steps:
  - parse explicit `Resource map` entries through stable, bounded rules
  - validate verb-to-class, path containment, file existence, and repository-root dependency boundaries
  - add bounded migration lint for recognized resource-loading instructions using `assets/`, `references/`, `scripts/`, and legacy `templates/`
  - expose stable diagnostics suitable for test assertions
  - keep existing packaged script and plan asset validation behavior intact
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path tests/fixtures/skills/published-design`
- Expected observable result: canonical validation catches the original defect class and avoids broad path false positives.
- Commit message: `M2: validate mapped skill-local resources`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - Markdown parsing could overfit the current skill wording
  - legacy lint could over-classify examples
- Rollback/recovery:
  - keep deterministic resource-map validation and narrow or audit-mode the legacy lint if false positives appear.

### M3. Architecture Resource Normalization and Behavior Preservation

- Milestone state: planned
- Goal: Normalize the architecture skill resources and `Resource map` without changing architecture output behavior.
- Requirements: R47-R48b, R49, R54-R54d, R55c-R55e
- Files/components likely touched:
  - `skills/architecture/SKILL.md`
  - `skills/architecture/assets/architecture-skeleton.md`
  - `skills/architecture/assets/adr-skeleton.md`
  - `skills/architecture/references/diagram-conventions.md` or `skills/architecture/assets/diagram-styles.mmd`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/behavior-preservation.md`
- Dependencies:
  - M1 complete resource-chain audit closed after code review
  - clean-installed Codex, Claude, and opencode baseline evidence present
  - first divergent layer identified
  - M2 canonical validator available
  - test spec approved
- Tests to add/update:
  - validator fixture or direct canonical validation covering architecture `Resource map`
  - behavior-preservation matrix for trigger behavior, arc42 sections, C4 obligations, ADR structure, review boundary, and handoff semantics
- Implementation steps:
  - inspect existing root `templates/architecture.md`, `templates/adr.md`, and `templates/diagram-styles.mmd`
  - decide whether each resource earns a skill-local file or should be removed as redundant
  - add approved `assets/` and `references/` resources only where they earn files
  - replace raw legacy `templates/...` load instructions with explicit `Resource map` entries and load conditions
  - preserve normative rules in `SKILL.md` and keep resources limited to skeletons, field labels, placeholders, short fill instructions, or diagram conventions
  - record behavior-preservation evidence
  - stop before implementation if any baseline target installation remains uninspected or if the first divergent layer has not been identified
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/behavior-preservation.md`
- Expected observable result: architecture skill no longer references unavailable resources, retains the same required architecture artifact obligations, and changes only after the reviewed M1 baseline identifies the first divergent layer.
- Commit message: `M3: normalize architecture skill resources`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - moving too much normative content out of `SKILL.md`
  - adding resources that duplicate inline rules and do not earn files
- Rollback/recovery:
  - reinline any resource whose content proves normative or redundant, and keep only resource-map entries that point to earned packaged files.

### M4. Generated Package and Archive Resource Parity

- Milestone state: planned
- Goal: Prove mapped resources survive generated local mirror output, generated adapter package output, and release archives with matching relative paths and raw-byte SHA-256 unless a transformation contract applies.
- Requirements: R50-R51a, R55a
- Files/components likely touched:
  - `scripts/build-skills.py`
  - `scripts/adapter_distribution.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-build-skills.py`
  - `scripts/test-adapter-distribution.py`
  - `tests/fixtures/adapters/`
  - `tests/fixtures/skills/published-design/generated-output-presence/`
- Dependencies:
  - M2 mapped-resource inventory API or equivalent helper
  - M3 architecture resource map and files
- Tests to add/update:
  - generated local mirror includes mapped resources and fails stale bytes
  - generated adapter package includes mapped resources for Codex, Claude, and opencode
  - release archive validation fails missing mapped resources and stale mapped bytes
  - transformation contract failure fixture if transformed resources are supported in the first slice
- Implementation steps:
  - centralize mapped-resource inventory and raw-byte SHA-256 identity collection
  - compare canonical-to-generated local mirror parity
  - compare canonical-to-generated adapter package parity
  - compare canonical-to-release-archive parity
  - fail stable diagnostics for missing, stale, unexpected transformation, and missing transformation contract cases
- Validation commands:
  - `python scripts/test-build-skills.py`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-release-output`
  - `python scripts/validate-adapters.py --version v0.3.2 --release-output-dir /tmp/rigorloop-sri-release-output`
- Expected observable result: stale or missing mapped resources fail before a release package can be treated as valid.
- Commit message: `M4: validate generated resource parity`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - adapter archive validation currently handles text entries and may need careful raw-byte handling
  - transformation support could become too broad for first slice
- Rollback/recovery:
  - enforce untransformed parity first and explicitly defer transformation support beyond failing incomplete contracts if implementation complexity exceeds first-slice scope.

### M5. Reusable Packed Clean-Install Regression Gate

- Milestone state: planned
- Goal: Turn the minimum pre-change clean-install proof established in M1 into a reusable, automated pre-publish regression gate for the normalized architecture resources.
- Requirements: R52-R52c, R55a
- Files/components likely touched:
  - `scripts/adapter_distribution.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/clean-install-proof.md`
- Dependencies:
  - M4 release archive parity
  - M1 complete clean-install baseline and inspection route
  - test spec approved
- Tests to add/update:
  - reusable post-change clean install from locally packed archives writes target skill roots under empty temporary projects
  - reusable gate rejects dry-run or unpackaged source proof
  - reusable gate detects missing and stale installed mapped resources
- Implementation steps:
  - productionize or reuse the M1 installed-tree inspection route as a repository-owned pre-publish clean-install command or validation mode
  - verify the post-change chain: canonical normalized resources, generated packages, locally packed release candidate, and clean Codex, Claude, and opencode installations
  - use locally packed release-candidate archives as the install source
  - install into empty target projects for Codex, Claude, and opencode
  - inspect real installed skill roots and compare mapped resource relative paths and raw-byte SHA-256
  - record proof and any target-specific root mapping
  - keep M5 out of the initial loss-boundary decision; M1 already owns first baseline evidence and root-cause identification
- Validation commands:
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-install-release-output`
  - `python scripts/validate-adapters.py --version v0.3.2 --release-output-dir /tmp/rigorloop-sri-install-release-output`
  - repository-owned clean-install smoke command added by this milestone
- Expected observable result: reusable post-change clean-install gate proves normalized mapped architecture resources at the expected relative path and byte identity in all target installed trees.
- Commit message: `M5: add reusable clean-install resource gate`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - existing archive extraction helpers may not model the public installer path closely enough
  - target-specific root differences could obscure relative-path comparison
- Rollback/recovery:
  - keep archive parity as a prerequisite and record any target installer gap as a blocker rather than accepting dry-run or source-directory proof.

M5 relationship to M1:

- M1 is the one complete pre-change diagnostic baseline and identifies the first divergent layer.
- M5 is the reusable post-change enforcement and release-quality regression proof.

### M6. Repository-Wide Audit and Enforcement Decision

- Milestone state: planned
- Goal: Run the reusable validator across current published skills, resolve architecture drift, and decide whether global enforcement can be enabled now.
- Requirements: R53-R53b, R49d
- Files/components likely touched:
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/repository-wide-resource-audit.md`
  - `scripts/skill_validation.py`
  - current changed `skills/**/SKILL.md` only if audit finds in-scope drift that must be resolved before enforcement
- Dependencies:
  - M2 canonical validator
  - M3 architecture normalization
  - M4 and M5 parity proof
- Tests to add/update:
  - audit-mode output fixture if audit mode is a separate command option
  - enforcement fixture proving new or changed skills cannot introduce mapped-resource debt
- Implementation steps:
  - run audit mode across all current published skills
  - resolve in-scope architecture drift
  - record unrelated drift as follow-up, approved exception, or deferred debt in review-visible evidence
  - enable hard enforcement for new or changed skills
  - enable repository-wide enforcement only if the audit is clean or all drift is explicitly resolved, deferred, or excepted
- Validation commands:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit --path skills --path scripts/skill_validation.py --path scripts/test-skill-validator.py`
- Expected observable result: current skill resource-integrity state is known, and enforcement state matches the approved rollout boundary.
- Commit message: `M6: audit published skill resource integrity`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - audit may uncover unrelated skill drift that should not silently expand scope
  - global enforcement may need a temporary baseline exception file or audit-only closeout
- Rollback/recovery:
  - keep new/changed enforcement and audit evidence, but defer global enforcement with owner-visible rationale if unrelated baseline debt remains.

### M7. Lifecycle Closeout and Release-Gate Alignment

- Milestone state: planned
- Goal: Close the planned initiative with rationale, validation evidence, final lifecycle state synchronization, and PR-ready handoff only after all implementation milestones are closed.
- Requirements: R46-R55 evidence coverage
- Files/components likely touched:
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/explain-change.md`
  - `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
  - `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`
  - `docs/plan.md`
- Dependencies:
  - M1-M6 closed
  - all required code-review and review-resolution complete
- Tests to add/update:
  - none unless final validation exposes missing coverage
- Implementation steps:
  - update change metadata with final changed files, validation commands, and review records
  - write explain-change linking actual diff to proposal, spec, architecture, plan, tests, and reviews
  - run final selected validation and broader smoke required by the active plan/test spec
  - update plan body and index only when lifecycle state changes are true
  - hand off to verify, then PR after verify passes
- Validation commands:
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plan.md --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/explain-change.md`
  - final validation bundle named by the approved test spec and active plan
- Expected observable result: plan, change metadata, review records, rationale, validation evidence, and PR handoff are synchronized.
- Commit message: `M7: close published skill resource integrity plan`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks:
  - final lifecycle state could become stale across plan index, plan body, and change metadata
- Rollback/recovery:
  - keep the plan active until all required downstream gates are actually complete; do not mark Done based on readiness alone.

## Validation plan

- `git diff --check -- docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md docs/plan.md docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot specs/skill-contract.md docs/architecture/system/architecture.md docs/adr/ADR-20260623-published-skill-resource-integrity.md`: whitespace and patch hygiene for planning and upstream settlement.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md --path specs/skill-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260623-published-skill-resource-integrity.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plan.md`: lifecycle status and artifact shape for touched lifecycle artifacts.
- `python scripts/validate-change-metadata.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`: change metadata integrity.
- `python scripts/validate-review-artifacts.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`: review record/log integrity.
- `python scripts/test-skill-validator.py`: canonical resource-map and legacy lint regression coverage.
- `python scripts/validate-skills.py`: current canonical skill validation.
- `python scripts/test-build-skills.py`: generated local mirror behavior.
- `python scripts/build-skills.py --check`: generated local mirror proof.
- `python scripts/test-adapter-distribution.py`: generated adapter and release archive regression coverage.
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-release-output`: locally packed release-candidate archive generation.
- `python scripts/validate-adapters.py --version v0.3.2 --release-output-dir /tmp/rigorloop-sri-release-output`: release-candidate archive validation.
- M1 clean-install baseline commands: pre-change target-installed resource-chain proof.
- clean-install smoke command added or hardened by M5: reusable post-change target-installed resource parity proof.
- final `bash scripts/ci.sh --mode explicit ...` or broader command named by the approved test spec: final scoped CI-equivalent proof.

## Risks and recovery

- Risk: The initial defect was caused by stale local install state rather than canonical or generated output.
  - Recovery: M1 records the first divergent layer before resource normalization and avoids treating local installed state alone as root cause.
- Risk: Legacy-reference lint creates false positives for artifact examples.
  - Recovery: Keep lint bounded to recognized resource-loading instructions and approved prefixes; add false-positive fixtures before enforcement.
- Risk: Architecture resource extraction moves hidden policy out of `SKILL.md`.
  - Recovery: Keep trigger logic, review boundaries, stop conditions, lifecycle semantics, and security rules in `SKILL.md`; record behavior-preservation evidence.
- Risk: Clean-install smoke becomes too expensive or requires unavailable user tools.
  - Recovery: M1 uses the existing local-archive CLI route or adds the smallest audit-only helper; M5 productionizes that proof as reusable automation. Keep live registry proof release-owned unless the release contract changes.
- Risk: Repository-wide audit finds unrelated existing drift.
  - Recovery: Record drift and either resolve, defer, or except it explicitly; do not silently expand the implementation scope.

## Dependencies

- `architecture-review-r1` approval is the settlement basis for architecture `approved` and ADR `accepted` status.
- `plan-review` must approve this plan before test-spec.
- `test-spec` must map R46-R55 and the milestones to concrete tests before implementation.
- M1 complete clean-install baseline MUST close before M3.
- M2 validator helpers should exist before M3 relies on canonical validation.
- M3 architecture normalization depends on the reviewed M1 baseline.
- M4 generated/archive parity follows M3.
- M5 reusable clean-install enforcement follows M4 and reuses or productionizes the M1 inspection route.

## Progress

- 2026-06-23: plan created after proposal, spec, and architecture approval.
- 2026-06-23: revised plan to resolve SRI-PLAN1 by requiring complete pre-change installed-target baseline evidence before architecture resource changes.
- 2026-06-23: authored resource-integrity test-spec coverage in `specs/skill-contract.test.md` T41-T48 after clean plan-review-r2.
- 2026-06-23: owner approved the test-spec coverage and M1 remains ready for implementation.
- 2026-06-23: started M1 implementation. Scope is limited to pre-change architecture resource-chain evidence, audit documentation, and minimum audit-only tooling only if the supported install path cannot produce installed-tree proof.
- 2026-06-23: completed M1 audit evidence in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/architecture-resource-chain-audit.md`; first divergent layer is canonical skill source.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-23 | Split root-cause audit before architecture resource creation. | R55 requires identifying the loss boundary before adding, renaming, packaging, or removing architecture resources. | Combine audit and canonical resource edits in one milestone. |
| 2026-06-23 | Sequence validator before architecture normalization. | The architecture skill should be normalized against the same deterministic contract that will protect later skills. | Fix architecture first and add reusable validation afterward. |
| 2026-06-23 | Require minimum clean-install inspection in M1 before architecture resource changes. | R55/R55a require the complete resource chain, including all target installations, to be audited before mutation. | Defer installed-tree evidence until M5. |
| 2026-06-23 | Retain M5 as reusable post-change clean-install enforcement. | The baseline and the durable regression gate serve different purposes. | Remove later clean-install automation after one diagnostic audit. |

## Surprises and discoveries

- Existing `skill_validation.py` already contains packaged-resource and plan-asset validation patterns that should be reused rather than replaced.
- Existing `build-skills.py` already copies all canonical skill files into generated local mirror output, which is useful evidence but does not by itself prove adapter archive or installed-target parity.
- The current `validate-adapters.py` archive-validation interface uses `--root`, not `--release-output-dir`; M1 used and recorded the supported `--root` flag.
- The architecture resource defect predates package assembly: `skills/architecture/` contains only `SKILL.md` while `SKILL.md` references `templates/...` paths, and generated, archived, and clean-installed outputs preserve that incomplete inventory.
- Clean opencode local-archive install completed with `opencode-command-aliases-not-declared`; this did not block architecture skill-root inspection.

## Validation notes

- 2026-06-23: planning-stage validation passed:
  - `git diff --check -- docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot specs/skill-contract.md docs/architecture/system/architecture.md docs/adr/ADR-20260623-published-skill-resource-integrity.md docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md docs/plan.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md --path specs/skill-contract.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260623-published-skill-resource-integrity.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`
- 2026-06-23: SRI-PLAN1 plan-revision validation passed with the same command set; plan-review-r2 closed the finding.
- 2026-06-23: test-spec authoring validation passed:
  - `git diff --check -- docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot specs/skill-contract.md specs/skill-contract.test.md docs/architecture/system/architecture.md docs/adr/ADR-20260623-published-skill-resource-integrity.md docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md docs/plan.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-22-published-skill-resource-integrity-architecture-pilot.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260623-published-skill-resource-integrity.md --path docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md --path docs/plan.md`
  - `python scripts/validate-change-metadata.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
  - `python scripts/validate-review-artifacts.py docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`
- 2026-06-23: M1 implementation validation passed:
  - `python scripts/build-skills.py --check`
  - `python scripts/build-skills.py --output-dir /tmp/rigorloop-sri-audit-generated-skills`
  - `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-audit-release-output`
  - `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-audit-release-output`
  - `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init codex --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-codex-v0.3.2.zip --json`
  - `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init claude --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-claude-v0.3.2.zip --json`
  - `node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init opencode --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-opencode-v0.3.2.zip --json`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/architecture-resource-chain-audit.md`

## Outcome and retrospective

- Not started. This section is final-only while the plan is active.

## Readiness

- See `Current Handoff Summary`.
- Ready for plan-review rerun for SRI-PLAN1.
