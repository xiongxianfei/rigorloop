# RigorLoop first-release implementation plan

- Status: in_progress
- Owner: maintainer + Codex
- Start date: 2026-04-19
- Last updated: 2026-04-19
- Related issue or PR: none
- Supersedes: none

## Purpose / big picture

Implement the first RigorLoop starter-kit release described by the approved workflow spec and repository architecture. The work should turn the repository from a generic template into a reviewable workflow product with canonical sources, simple structural validation, deterministic generated Codex compatibility output, machine-readable change metadata, and a proof-of-value example centered on the skill validator.

The plan keeps the implementation incremental. Guidance and source-of-truth alignment land before strict validation. Canonical skill cleanup is separated from validator and generator logic so risky content normalization is reviewable on its own. CI becomes a thin wrapper around repo-owned scripts only after those scripts are real.

The plan also keeps `.codex/skills/` stable on purpose. Contributors update canonical `skills/` first. Generated Codex compatibility output is refreshed only after canonical skills are good enough for a deliberate sync, not after every intermediate skill edit.

## Source artifacts

- Proposal: `docs/proposals/2026-04-19-rigorloop-project-direction.md`
- Proposal: `docs/proposals/2026-04-19-implementation-milestone-commit-policy.md`
- Exploration: `docs/proposals/2026-04-19-rigorloop-workflow-product.explore.md`
- Spec: `specs/rigorloop-workflow.md`
- Architecture: `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
- ADR: `docs/adr/ADR-20260419-repository-source-layout.md`
- Architecture-review findings: 2026-04-19 review in conversation approved the design and called out three follow-ups to carry into implementation:
  - keep validator-rule ownership explicit between schema files and validation scripts;
  - keep skill generation deterministic and minimal;
  - align contributor-facing guidance early so stale template behavior does not linger.
- Test spec: `specs/rigorloop-workflow.test.md`

## Context and orientation

- The repository still presents itself as a template in `README.md`, `scripts/ci.sh`, and `scripts/release-verify.sh`.
- `docs/workflows.md` still summarizes the older operational flow and does not yet reflect the approved lifecycle, fast lane, or the `ci` stage meaning from `specs/rigorloop-workflow.md`.
- `skills/` is the intended canonical workflow source, but `.codex/skills/` remains the current runtime compatibility surface and has already drifted from `skills/`.
- `.codex/PLANS.md` has been removed. All plan guidance must now point to `docs/plans/0000-00-00-example-plan.md`.
- `schemas/` and `docs/changes/` do not exist yet.
- Current CI in `.github/workflows/ci.yml` only shells out to `scripts/ci.sh`, which is still a template placeholder.
- Current release automation in `.github/workflows/release.yml` only shells out to `scripts/release-verify.sh`, which is still a template placeholder. Release automation is not the main focus of this initiative.
- There is no `docs/project-map.md` and no `.codex/CONSTITUTION.md`.
- The repository already has useful local surfaces for the implementation:
  - root guidance in `AGENTS.md`
  - public entrypoint in `README.md`
  - operational workflow summary in `docs/workflows.md`
  - plan index in `docs/plan.md`
  - canonical workflow skills in `skills/`
  - current runtime compatibility skills in `.codex/skills/`
  - CI integration in `.github/workflows/ci.yml`

## Non-goals

- Build a hosted platform, control plane, or general agent runtime.
- Introduce the larger `method/`, `adapters/`, or `dist/` layout in the first release.
- Design a richer skill metadata model than the intentionally simple first-release validator contract.
- Require the full artifact lifecycle for fast-lane changes.
- Redesign release automation beyond keeping repo guidance honest about its current behavior.
- Add subjective writing-quality or philosophy scoring to CI.
- Hide bulk skill-source cleanup inside validator or generator implementation.

## Requirements covered

| Requirement IDs | Planned implementation surface |
| --- | --- |
| `R1`-`R12c` | `README.md`, `docs/workflows.md`, `AGENTS.md`, `.github/pull_request_template.md`, canonical workflow skills under `skills/`, and reviewer-facing documentation |
| `R13`-`R19` | `scripts/validate-skills.py`, `scripts/test-skill-validator.py`, `tests/fixtures/skills/`, `scripts/build-skills.py`, `scripts/ci.sh`, `.github/workflows/ci.yml` |
| `R20`-`R24a` | `skills/`, `.codex/skills/`, root guidance, and any follow-on clarification needed in architecture/ADR docs |
| `R25`-`R27` | `schemas/change.schema.json`, `schemas/skill.schema.json`, `docs/changes/0001-skill-validator/`, PR template support, and verification/explain-change artifacts |

## Milestones

### M1. Align repository guidance and review surfaces

- Goal: Make the repository describe the approved RigorLoop workflow, public identity, and canonical-versus-generated boundaries before stricter validation lands.
- Requirements: `R1`-`R12`, `R20`-`R24`, `R27`
- Files/components likely touched:
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `.github/pull_request_template.md`
- Dependencies:
  - approved spec and architecture
  - no dependency on validator or generator scripts
- Tests to add/update:
  - no automated tests expected
  - update manual reviewer prompts in the PR template if needed
- Implementation steps:
  - replace template-facing README language with RigorLoop project positioning and contributor guidance
  - align `docs/workflows.md` to the approved lifecycle, fast-lane rules, milestone-commit expectations, and `ci` stage meaning
  - ensure `AGENTS.md` and PR template point reviewers to the right canonical and generated paths
  - record any remaining skill-text contradictions as explicit follow-up inputs for M3 and M4 instead of editing `skills/` or `.codex/skills/` in this milestone
- Validation commands:
  - `! rg -n "<PROJECT_NAME>|This template|Replace this" README.md docs/workflows.md AGENTS.md .github/pull_request_template.md`
  - `! rg -n "\\.codex/PLANS\\.md" README.md docs/workflows.md AGENTS.md .github/pull_request_template.md skills .codex/skills`
  - `git -c safe.directory=/home/xiongxianfei/data/20260419-rigorloop diff --check -- README.md docs/workflows.md AGENTS.md .github/pull_request_template.md skills`
- Expected observable result:
  - contributors can identify RigorLoop, the approved lifecycle, and canonical versus generated paths from the main docs without reading chat history
- Commit message: `M1: align repository guidance with approved workflow`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - canonical skill docs may need updates that are larger than expected because `skills/` and `.codex/skills/` already drift
- Rollback/recovery:
  - revert changed guidance files only; no generated output or schema work is coupled to this milestone

### M2. Add schema and metadata scaffolding

- Goal: Introduce the machine-readable contracts needed for traceability and simple skill metadata without overloading them with non-schema validation rules.
- Requirements: `R11`, `R20`-`R25g`
- Files/components likely touched:
  - `schemas/change.schema.json`
  - `schemas/skill.schema.json`
  - `scripts/validate-change-metadata.py`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
  - optional small doc updates that point to the new schema paths
- Dependencies:
  - M1 guidance alignment should already identify canonical authored paths
- Tests to add/update:
  - no dedicated test harness yet
  - JSON syntax validation for the schema files
  - valid and invalid `change.yaml` fixtures covering the required passing and failing metadata cases from `T5` through `T7`
- Implementation steps:
  - create `schemas/` as an authored root
  - define `change.schema.json` for the first-release `change.yaml` shape from `R25b`-`R25e`
  - define `skill.schema.json` only for per-skill machine-readable metadata shape
  - add a minimal metadata-validation command for `docs/changes/<change-id>/change.yaml` so later milestones can validate the golden-path traceability file against the first-release contract
  - create valid and invalid metadata fixtures that match the first-release schema contract and failing edge cases
  - keep Markdown section checks, uniqueness checks, placeholder rejection, and source-of-truth checks out of JSON Schema and in the future validator script
- Validation commands:
  - `python -m json.tool schemas/change.schema.json >/dev/null`
  - `python -m json.tool schemas/skill.schema.json >/dev/null`
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-title/change.yaml`
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-review/change.yaml`
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-validation-record/change.yaml`
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-review-shape/change.yaml`
  - `git -c safe.directory=/home/xiongxianfei/data/20260419-rigorloop diff --check -- schemas scripts/validate-change-metadata.py tests/fixtures/change-metadata`
- Expected observable result:
  - the repository has concrete schema files for change metadata and simple skill metadata shape, a working way to validate a sample `change.yaml`, and an explicit validator boundary
- Commit message: `M2: add first-release schema scaffolding`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - overfitting the schema to future workflow ideas instead of the approved first-release contract
- Rollback/recovery:
  - revert the new schema files only; no generated output or CI dependency should exist yet

### M3. Normalize canonical skill sources and add validator fixtures

- Goal: Make `skills/` satisfy the simple first-release contract and create explicit valid/invalid fixtures before implementing enforcement logic.
- Requirements: `R13`, `R15`, `R15a`, `R16`, `R20`-`R24`
- Files/components likely touched:
  - `skills/*/SKILL.md`
  - `tests/fixtures/skills/valid-basic/`
  - `tests/fixtures/skills/missing-name/`
  - `tests/fixtures/skills/missing-description/`
  - `tests/fixtures/skills/missing-expected-output/`
  - `tests/fixtures/skills/missing-title/`
  - `tests/fixtures/skills/duplicate-name/`
  - `tests/fixtures/skills/placeholder-text/`
- Dependencies:
  - M2 schema scaffolding if fixture metadata examples should follow `skill.schema.json`
- Tests to add/update:
  - fixture directories for the minimum valid and invalid cases from `R16`
- Implementation steps:
  - audit canonical `skills/` content against the simple validator contract
  - normalize canonical skills so they use one top-level title and one `## Expected output` section where missing
  - create fixture skill directories that capture the approved pass/fail cases
  - keep fixture content minimal and objective; do not add writing-quality checks
- Validation commands:
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^name:" "$f" || { echo "$f: missing name"; exit 1; }; done'`
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^description:" "$f" || { echo "$f: missing description"; exit 1; }; done'`
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^## Expected output$" "$f" || { echo "$f: missing ## Expected output"; exit 1; }; done'`
  - `! rg -n '\\b(TODO|TBD)\\b' skills/*/SKILL.md`
  - `python - <<'PY'\nfrom pathlib import Path\nbad = []\nfor path in sorted(Path('skills').glob('*/SKILL.md')):\n    lines = path.read_text().splitlines()\n    titles = [line for line in lines if line.startswith('# ') and not line.startswith('## ')]\n    if len(titles) != 1:\n        bad.append(f\"{path}: expected exactly one top-level title, found {len(titles)}\")\nif bad:\n    raise SystemExit('\\n'.join(bad))\nPY`
  - `python - <<'PY'\nfrom pathlib import Path\nimport re\nowners = {}\nfor path in sorted(Path('skills').glob('*/SKILL.md')):\n    text = path.read_text()\n    match = re.search(r'^name:\\s*(.+)$', text, re.M)\n    if not match:\n        raise SystemExit(f\"{path}: missing name\")\n    name = match.group(1).strip()\n    if name in owners:\n        raise SystemExit(f\"duplicate skill name: {name} in {owners[name]} and {path}\")\n    owners[name] = path\nPY`
  - `test -f tests/fixtures/skills/valid-basic/SKILL.md && test -f tests/fixtures/skills/missing-name/SKILL.md && test -f tests/fixtures/skills/missing-description/SKILL.md && test -f tests/fixtures/skills/missing-expected-output/SKILL.md && test -f tests/fixtures/skills/missing-title/SKILL.md && test -f tests/fixtures/skills/duplicate-name/first/SKILL.md && test -f tests/fixtures/skills/duplicate-name/second/SKILL.md && test -f tests/fixtures/skills/placeholder-text/SKILL.md`
  - `git diff --check -- skills tests/fixtures docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
- Expected observable result:
  - canonical skills are good enough for one deliberate generated sync in M4, and the repository has explicit fixture cases for the approved rule set
- Commit message: `M3: normalize canonical skills and add validator fixtures`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [x] milestone committed
- Risks:
  - bulk skill normalization may touch many files and create review noise
  - some existing skill content may imply stronger validation than the approved first-release contract
- Rollback/recovery:
  - revert only the affected skill-source files and fixtures; keep schema and guidance work intact

### M4. Implement simple validation and deterministic skill generation

- Goal: Ship the actual validator, fixture test runner, and deterministic `skills/` to `.codex/skills/` generation/drift logic.
- Requirements: `R15`-`R17`, `R20`-`R24a`
- Files/components likely touched:
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `scripts/build-skills.py`
  - `.codex/skills/`
- Dependencies:
  - M2 schema files
  - M3 canonical skill normalization and fixtures
- Tests to add/update:
  - fixture-driven validator test runner
  - generated-output drift check behavior
- Implementation steps:
  - implement a simple frontmatter parser and validation logic using minimal runtime assumptions
  - keep `skill.schema.json` responsible only for per-skill metadata shape
  - keep Markdown body checks, uniqueness checks, placeholder rejection, and canonical-versus-generated checks in `validate-skills.py`
  - implement `build-skills.py` as a deterministic minimal transform from `skills/` to `.codex/skills/`
  - regenerate `.codex/skills/` from canonical source only after M3 has made `skills/` good enough for a deliberate sync
  - treat `.codex/skills/` as tracked generated repository output after this first sync and make drift detection fail clearly when generated output is edited or stale
- Validation commands:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `git diff --check -- scripts .codex/skills docs/plans/2026-04-19-rigorloop-first-release-implementation.md`
- Expected observable result:
  - contributors can validate canonical skill structure locally and confirm that generated Codex compatibility output is in sync
- Commit message: `M4: implement skill validation and deterministic generation`
- Milestone closeout:
  - [x] validation passed
  - [x] progress updated
  - [x] decision log updated if needed
  - [x] validation notes updated
  - [ ] milestone committed
- Risks:
  - YAML frontmatter parsing may tempt the change into third-party dependencies the repo does not currently manage
  - generated-output churn may be larger than expected on first sync
- Rollback/recovery:
  - keep canonical skill content untouched if generator logic needs to be reverted
  - if generation semantics are wrong, regenerate `.codex/skills/` after fixing the script rather than hand-editing generated files

### M5. Replace template CI behavior with repository-owned checks

- Goal: Make CI run the actual repository validation commands instead of template placeholders.
- Requirements: `R9`, `R9a`, `R18`, `R19`, `R24`, `R27`
- Files/components likely touched:
  - `scripts/ci.sh`
  - `.github/workflows/ci.yml`
  - `docs/workflows.md`
  - `README.md`
- Dependencies:
  - M4 validator, fixture tests, and drift check must exist first
- Tests to add/update:
  - no new test harness beyond the checks already created
  - update CI documentation to name real commands
- Implementation steps:
  - replace template output in `scripts/ci.sh` with the actual first-release validation commands
  - keep `.github/workflows/ci.yml` as a thin wrapper around the repo script
  - ensure docs point contributors to the same commands CI runs
  - make release guidance honest if CI language or README still overstates release readiness
- Validation commands:
  - `bash scripts/ci.sh`
  - `git diff --check -- scripts/ci.sh .github/workflows/ci.yml README.md docs/workflows.md`
- Expected observable result:
  - local and CI validation use the same repo-owned commands for the first-release structural checks
- Commit message: `M5: wire repository CI to real validation commands`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - CI may become the first place that reveals portability issues in the scripts
- Rollback/recovery:
  - revert the CI wrapper and script together if the real commands are not stable yet

### M6. Publish the skill-validator golden path and change traceability

- Goal: Ship the proof-of-value example and the per-change traceability package for the validator change.
- Requirements: `R10`-`R14`, `R25`-`R27`
- Files/components likely touched:
  - `docs/changes/0001-skill-validator/proposal.md`
  - `docs/changes/0001-skill-validator/spec.md`
  - `docs/changes/0001-skill-validator/plan.md`
  - `docs/changes/0001-skill-validator/test-spec.md`
  - `docs/changes/0001-skill-validator/verify-report.md`
  - `docs/changes/0001-skill-validator/explain-change.md`
  - `docs/changes/0001-skill-validator/change.yaml`
  - `README.md`
- Dependencies:
  - M1 through M5 should already be complete so the example reflects actual implemented behavior
  - `specs/rigorloop-workflow.test.md` should exist before finalizing the test-spec and verify-report artifacts
- Tests to add/update:
  - no new automated tests expected beyond the repository checks already added
  - update the proof-of-value example artifacts to reflect actual commands and outcomes
- Implementation steps:
  - create the `docs/changes/0001-skill-validator/` directory as the change-local durable artifact home
  - use local artifacts to summarize and link to the already-approved top-level proposal, spec, architecture, and ADR rather than duplicating large documents verbatim
  - write `change.yaml` using the first-release schema and the real changed-file/validation evidence
  - update `README.md` so contributors can find the golden-path example
- Validation commands:
  - `bash scripts/ci.sh`
  - `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`
  - `git diff --check -- docs/changes/0001-skill-validator README.md`
- Expected observable result:
  - contributors can follow one concrete non-trivial change from artifacts to verification evidence and PR-ready explanation
- Commit message: `M6: publish skill-validator golden path artifacts`
- Milestone closeout:
  - [ ] validation passed
  - [ ] progress updated
  - [ ] decision log updated if needed
  - [ ] validation notes updated
  - [ ] milestone committed
- Risks:
  - the example may drift from the real implementation if artifact updates are left until too late
  - duplicating top-level proposal/spec text inside `docs/changes/` would add avoidable maintenance overhead
- Rollback/recovery:
  - keep the top-level approved artifacts unchanged and revert only the change-local example artifacts if needed

## Validation plan

- Planning-only validation:
  - confirm the active plan index points at this plan
  - keep milestone boundaries aligned with the approved requirement groups
- Implementation milestone validation:
  - M1 uses doc consistency and placeholder/reference checks
  - M2 uses JSON syntax validation for schema files plus change-metadata fixture validation
  - M3 uses canonical-skill and fixture inventory checks
  - M4 uses the validator, fixture tests, and build drift check
  - M5 uses `bash scripts/ci.sh` and workflow-wrapper checks
  - M6 uses full CI plus change-artifact checks
- Full-branch validation before `verify` and `pr`:
  - `bash scripts/ci.sh`
  - manual review that `README.md`, `docs/workflows.md`, `AGENTS.md`, `skills/`, `.codex/skills/`, `schemas/`, and `docs/changes/0001-skill-validator/` all agree on canonical-versus-generated behavior

## Risks and recovery

- Risk: skill-source normalization creates large diffs before enforcement scripts exist.
  - Recovery: keep normalization in M3, separate from validator/generator code, and review it independently before enforcing checks.
- Risk: frontmatter parsing adds unmanaged third-party dependencies.
  - Recovery: prefer a simple stdlib-based parser for the limited first-release YAML shape; revisit dependency management only if the approved contract cannot be implemented safely otherwise.
- Risk: `.codex/skills/` churn obscures meaningful logic changes.
  - Recovery: keep generator behavior deterministic and minimal; regenerate `.codex/skills/` only after canonical `skills/` reaches an agreed-good-enough checkpoint rather than after every intermediate edit.
- Risk: contributor guidance remains stale while CI starts enforcing new rules.
  - Recovery: finish M1 before M5 and do not enable real CI checks until root guidance and workflow docs are aligned.
- Risk: change-local example artifacts duplicate top-level planning artifacts excessively.
  - Recovery: use the `docs/changes/0001-skill-validator/` files as concise change-local wrappers that link to approved top-level artifacts where appropriate.
- Risk: release automation looks more complete than it really is.
  - Recovery: keep release changes scoped to truthful docs and avoid expanding release behavior in this initiative unless a real release need appears.

## Dependencies

- `plan-review` should happen before implementation starts because this is multi-milestone work.
- `test-spec` must be created at `specs/rigorloop-workflow.test.md` before implementation starts.
- M1 should complete before M5 so CI does not enforce behavior that docs still misdescribe.
- M2 should complete before M4 so validator and metadata behavior have explicit schema anchors.
- M3 should complete before M4 so the validator does not hide canonical-skill cleanup inside script work.
- `.codex/skills/` must not be refreshed during M1 through M3 except to recover from accidental drift; the intended generated sync point is M4.
- M4 should complete before M5 because CI depends on real scripts.
- M1 through M5 should complete before M6 so the golden-path example reflects implemented behavior rather than planned behavior.

## Progress

- [x] M1. Align repository guidance and review surfaces
- [x] M2. Add schema and metadata scaffolding
- [x] M3. Normalize canonical skill sources and add validator fixtures
- [x] M4. Implement simple validation and deterministic skill generation
- [ ] M5. Replace template CI behavior with repository-owned checks
- [ ] M6. Publish the skill-validator golden path and change traceability

- 2026-04-19: Completed M1 by aligning `README.md`, `docs/workflows.md`, `AGENTS.md`, and `.github/pull_request_template.md` to the approved lifecycle, fast-lane rules, milestone commit policy, and canonical-versus-generated boundaries.
- 2026-04-19: Follow-up after `code-review` to add the referenced workflow spec, test spec, architecture, ADR, and proposal artifacts to the branch so the new guidance resolves from git history instead of only from the working tree.
- 2026-04-19: Follow-up after second `code-review` to track `skills/` and `.codex/skills/` in git, align canonical `plan` and `implement` skill guidance to the approved milestone rules, and surface fast-lane eligibility and evidence rules directly in the root docs.
- 2026-04-19: User-directed follow-up overrides the original M1 sequencing guard and brings `skills/` plus `.codex/skills/` into the branch now so contributor guidance and tracked repository surfaces match.
- 2026-04-19: Completed M2 by adding `schemas/change.schema.json`, `schemas/skill.schema.json`, a stdlib-only `scripts/validate-change-metadata.py`, and valid plus invalid `tests/fixtures/change-metadata/` cases for `T5` through `T7`.
- 2026-04-19: Completed M3 by fixing the lone canonical top-level-title violation in `skills/architecture/SKILL.md`, adding the required `tests/fixtures/skills/` pass/fail cases, and correcting the M3 validation commands so they check the intended conditions with ripgrep.
- 2026-04-19: Completed M4 by shipping `scripts/validate-skills.py`, `scripts/test-skill-validator.py`, and `scripts/build-skills.py`, then performing the first deliberate `.codex/skills/` sync from canonical `skills/`.

## Decision log

- 2026-04-19: Treat `docs/plans/0000-00-00-example-plan.md` as the only plan-template source of truth. Rationale: `.codex/PLANS.md` has been removed and should not be recreated as a second plan surface.
- 2026-04-19: Keep validator ownership split explicit. Rationale: `schemas/skill.schema.json` should define only the machine-readable metadata shape, while `scripts/validate-skills.py` should enforce Markdown-body, cross-skill, and source-of-truth rules.
- 2026-04-19: Plan for deterministic minimal skill generation. Rationale: the first-release generator should make `.codex/skills/` a stable, reviewable derivative of `skills/` rather than a second authored tree.
- 2026-04-19: Normalize canonical skill content in its own milestone before script enforcement. Rationale: reviewable content cleanup is safer when it is not mixed with validator and generator logic.
- 2026-04-19: Update `.codex/skills/` only after canonical `skills/` is good enough for a deliberate sync. Rationale: frequent generated-output churn would create review noise and hide whether the canonical source is actually stable.
- 2026-04-19: Keep change-metadata validation stdlib-only in M2. Rationale: the repository does not manage YAML or JSON Schema dependencies yet, and the approved first-release contract is small enough for a focused parser and validator.
- 2026-04-19: Ship invalid metadata fixtures in M2, not later. Rationale: `specs/rigorloop-workflow.test.md` requires `T6` and `T7` coverage before code review, so M2 needs both passing and failing metadata cases.
- 2026-04-19: Keep `.codex/skills/` untouched in M3 even though `skills/` changed. Rationale: the approved plan and prior user direction defer generated compatibility sync until M4 after canonical skill content is stable.
- 2026-04-19: Replace the draft M3 `rg -L` checks with explicit per-file ripgrep loops. Rationale: ripgrep `-L` does not mean “files without match” in this repo workflow, so the original command text did not validate the intended conditions.
- 2026-04-19: Keep the first-release generator as a byte-for-byte copy from `skills/` to `.codex/skills/`. Rationale: a literal copy is the smallest deterministic transform and avoids warning-header churn in the generated review surface.
- 2026-04-19: Exercise the validator through its CLI in `scripts/test-skill-validator.py` instead of importing internals directly. Rationale: the approved command surface is `python scripts/validate-skills.py`, so fixture tests should prove that public entrypoint rather than only helper functions.

## Surprises and discoveries

- 2026-04-19: `.codex/PLANS.md` is already removed, but several docs had still referenced it before planning.
- 2026-04-19: `skills/` and `.codex/skills/` are both present and already drifted, including the `plan` and `implement` skills.
- 2026-04-19: Current CI and release workflows are thin wrappers over template shell scripts, so the real enforcement surface is still missing.
- 2026-04-19: `docs/workflows.md` still named the removed legacy plan-helper path during M1, so the doc had to stop naming that path to satisfy the no-stale-reference milestone gate.
- 2026-04-19: M1 guidance updates passed grep-based cleanup checks before review, but `code-review` caught that the branch still did not track the spec, architecture, ADR, and proposal artifacts those docs referenced.
- 2026-04-19: `code-review` also caught that `skills/` and `.codex/skills/` were still only working-tree content and that canonical `plan` and `implement` skill guidance lagged the approved milestone and fast-lane rules.
- 2026-04-19: `workflow` skill guidance still used `mini-spec` wording even though the approved fast lane now requires `spec -> implement -> verify -> pr`.
- 2026-04-19: The environment initially had `python3` but no `python` during early M2 work; after `python-is-python3` was installed, the repository command surface now matches the documented `python` commands.
- 2026-04-19: The canonical `skills/` tree was owned by `root:root`, so M3 could not edit the approved source-of-truth files until ownership was narrowed back to the current user for that path.
- 2026-04-19: The canonical skill corpus was already almost compliant; the only content fix needed for M3 was removing a second top-level heading from the architecture skill’s ADR example block.
- 2026-04-19: The M3 draft validation commands used ripgrep `-L` incorrectly, so they had to be corrected before the milestone could rely on them as pass/fail evidence.
- 2026-04-19: The first deliberate M4 drift check failed immediately because `.codex/skills/architecture/SKILL.md` was still stale after the M3 canonical fix, which confirmed the generator check was catching real drift before the first sync.

## Validation notes

- 2026-04-19 planning audit:
  - read `AGENTS.md`
  - read `docs/plan.md`
  - read `specs/rigorloop-workflow.md`
  - read `docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md`
  - read `docs/adr/ADR-20260419-repository-source-layout.md`
  - read `docs/workflows.md`
  - read `README.md`
  - read `.github/workflows/ci.yml`
  - read `.github/workflows/release.yml`
  - read `scripts/ci.sh`
  - read `scripts/release-verify.sh`
  - audited `skills/` and `.codex/skills/` presence and drift
- 2026-04-19 M1 validation:
  - `! rg -n "<PROJECT_NAME>|This template|Replace this" README.md docs/workflows.md AGENTS.md .github/pull_request_template.md` -> pass
  - `! rg -n "\\.codex/PLANS\\.md" README.md docs/workflows.md AGENTS.md .github/pull_request_template.md skills .codex/skills` -> pass
  - `git -c safe.directory=/home/xiongxianfei/data/20260419-rigorloop diff --check -- README.md docs/workflows.md AGENTS.md .github/pull_request_template.md skills` -> pass
- 2026-04-19 M1 follow-up after code review:
  - `git -c safe.directory=/home/xiongxianfei/data/20260419-rigorloop ls-files -- docs/proposals/2026-04-19-rigorloop-project-direction.md docs/proposals/2026-04-19-rigorloop-workflow-product.explore.md docs/proposals/2026-04-19-implementation-milestone-commit-policy.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md docs/adr/ADR-20260419-repository-source-layout.md` -> pass
  - `git -c safe.directory=/home/xiongxianfei/data/20260419-rigorloop diff --check --cached -- docs/proposals/2026-04-19-rigorloop-project-direction.md docs/proposals/2026-04-19-rigorloop-workflow-product.explore.md docs/proposals/2026-04-19-implementation-milestone-commit-policy.md specs/rigorloop-workflow.md specs/rigorloop-workflow.test.md docs/architecture/2026-04-19-rigorloop-first-release-repository-architecture.md docs/adr/ADR-20260419-repository-source-layout.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md` -> pass
- 2026-04-19 M1 follow-up after second code review:
  - `diff -qr skills .codex/skills` -> only `plan` and `implement` differed before canonical sync
  - `git ls-files -- skills/plan/SKILL.md skills/implement/SKILL.md .codex/skills/plan/SKILL.md .codex/skills/implement/SKILL.md` -> pass after staging skill trees
  - `git diff --check -- README.md docs/workflows.md skills/plan/SKILL.md skills/implement/SKILL.md docs/plans/2026-04-19-rigorloop-first-release-implementation.md` -> pass
  - `rg -n "mini-spec|mini spec" skills .codex/skills README.md docs/workflows.md` -> only `workflow` skill matched before final fast-lane wording sync
- 2026-04-19 M2 TDD and milestone validation:
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` -> expected pre-implementation failure because `scripts/validate-change-metadata.py` did not exist yet
  - `python3 -m json.tool schemas/change.schema.json >/dev/null` -> pass
  - `python3 -m json.tool schemas/skill.schema.json >/dev/null` -> pass
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` -> pass
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-title/change.yaml` -> fail as expected with missing `title`
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-review/change.yaml` -> fail as expected with missing `review`
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-validation-record/change.yaml` -> fail as expected with missing `validation[0].result`
  - `python3 scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-review-shape/change.yaml` -> fail as expected with non-integer `review.unresolved_items`
  - `git diff --check -- schemas scripts/validate-change-metadata.py tests/fixtures/change-metadata` -> pass
- 2026-04-19 M2 review follow-up after `code-review`:
  - `python --version` -> pass (`Python 3.12.3`)
  - `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml` -> pass
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-title/change.yaml` -> pass
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/missing-review/change.yaml` -> pass
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-validation-record/change.yaml` -> pass
  - `! python scripts/validate-change-metadata.py tests/fixtures/change-metadata/bad-review-shape/change.yaml` -> pass
- 2026-04-19 M3 TDD and milestone validation:
  - `python - <<'PY' ... top-level-title audit ... PY` -> expected pre-implementation failure because `skills/architecture/SKILL.md` had two top-level headings
  - `test -f tests/fixtures/skills/valid-basic/SKILL.md && ... && test -f tests/fixtures/skills/placeholder-text/SKILL.md` -> expected pre-implementation failure because the skill fixture tree did not exist yet
  - `sudo -n chown -R xiongxianfei:xiongxianfei skills` -> pass
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^name:" "$f" || { echo "$f: missing name"; exit 1; }; done'` -> pass
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^description:" "$f" || { echo "$f: missing description"; exit 1; }; done'` -> pass
  - `bash -lc 'for f in skills/*/SKILL.md; do rg -q "^## Expected output$" "$f" || { echo "$f: missing ## Expected output"; exit 1; }; done'` -> pass
  - `! rg -n '\\b(TODO|TBD)\\b' skills/*/SKILL.md` -> pass
  - `python - <<'PY'\nfrom pathlib import Path\nbad = []\nfor path in sorted(Path('skills').glob('*/SKILL.md')):\n    lines = path.read_text().splitlines()\n    titles = [line for line in lines if line.startswith('# ') and not line.startswith('## ')]\n    if len(titles) != 1:\n        bad.append(f\"{path}: expected exactly one top-level title, found {len(titles)}\")\nif bad:\n    raise SystemExit('\\n'.join(bad))\nPY` -> pass
  - `python - <<'PY'\nfrom pathlib import Path\nimport re\nowners = {}\nfor path in sorted(Path('skills').glob('*/SKILL.md')):\n    text = path.read_text()\n    match = re.search(r'^name:\\s*(.+)$', text, re.M)\n    if not match:\n        raise SystemExit(f\"{path}: missing name\")\n    name = match.group(1).strip()\n    if name in owners:\n        raise SystemExit(f\"duplicate skill name: {name} in {owners[name]} and {path}\")\n    owners[name] = path\nPY` -> pass
  - `test -f tests/fixtures/skills/valid-basic/SKILL.md && test -f tests/fixtures/skills/missing-name/SKILL.md && test -f tests/fixtures/skills/missing-description/SKILL.md && test -f tests/fixtures/skills/missing-expected-output/SKILL.md && test -f tests/fixtures/skills/missing-title/SKILL.md && test -f tests/fixtures/skills/duplicate-name/first/SKILL.md && test -f tests/fixtures/skills/duplicate-name/second/SKILL.md && test -f tests/fixtures/skills/placeholder-text/SKILL.md` -> pass
  - `git diff --check -- skills tests/fixtures docs/plans/2026-04-19-rigorloop-first-release-implementation.md` -> pass
- 2026-04-19 M4 TDD and milestone validation:
  - `python scripts/test-skill-validator.py` -> expected pre-implementation failure because `scripts/validate-skills.py` did not exist yet
  - `python scripts/build-skills.py --check` -> expected pre-implementation failure because `.codex/skills/architecture/SKILL.md` was still stale after the M3 canonical fix
  - `python scripts/test-skill-validator.py` -> pass
  - `python scripts/validate-skills.py` -> pass
  - `! python scripts/validate-skills.py .codex/skills` -> pass
  - `python scripts/build-skills.py` -> pass
  - `python scripts/build-skills.py --check` -> pass
  - `python - <<'PY' ... append deliberate drift marker to .codex/skills/architecture/SKILL.md ... PY` -> pass
  - `! python scripts/build-skills.py --check` -> pass
  - `python scripts/build-skills.py` -> pass
  - `python scripts/build-skills.py --check` -> pass
  - `git diff --check -- scripts .codex/skills docs/plans/2026-04-19-rigorloop-first-release-implementation.md` -> pass

## Outcome and retrospective

- Not started. Fill after implementation and verification are complete.

## Readiness

This plan has passed `plan-review`.

The required pre-implementation artifacts now exist. Implementation may begin with M1, provided the work continues to follow this plan, `specs/rigorloop-workflow.md`, and `specs/rigorloop-workflow.test.md`.
