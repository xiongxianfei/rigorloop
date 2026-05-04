# Learn Artifact Model test spec

## Status

- active

## Related spec and plan

- Spec: [Learn Artifact Model](learn-artifact-model.md), approved.
- Proposal: [Optimize Learn Skill](../docs/proposals/2026-05-03-optimize-learn-skill.md), accepted.
- Plan: [Learn Artifact Model Implementation Plan](../docs/plans/2026-05-04-learn-artifact-model.md), active.
- Architecture: not required. The accepted proposal, approved spec, and approved plan scope the change to workflow governance, documentation, skill guidance, selector routing, and generated output without runtime architecture, persistence, deployment, or integration boundaries.
- Spec-review: approved after classification, deterministic session-record creation, no-record boundary, and periodic-window requirements were added.
- Plan-review: approved after selector recognition was moved before any `docs/learn/**` artifact creation or selector validation.

## Testing strategy

- Use manual contract review for contributor-facing workflow, governance, skill, and learn-index guidance where the behavior is human-readable process routing.
- Use selector integration tests for `docs/learn/README.md`, `docs/learn/sessions/**`, and `docs/learn/topics/**` path classification because selector behavior is executable repository logic.
- Use skill-validator integration tests for stable, machine-checkable `learn` guidance terms such as phase names, canonical paths, classification vocabulary, confirmation gates, bounded evidence, and generated-boundary wording.
- Use generated-output drift and adapter validation checks when canonical `skills/learn/SKILL.md` changes.
- Use lifecycle and explicit-path CI validation for top-level lifecycle artifacts, workflow specs, change-local artifacts, selector code, skill code, generated outputs, and plan closeout.
- Treat broad smoke as unnecessary unless plan, review, verify, or CI evidence elevates it.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`, `R45`, `R46` | `T1`, `T14` | manual, integration | Workflow contract and affected governance surfaces preserve trigger-based `learn` and retire temporary surfaces |
| `R2`, `R2a`, `R3`-`R7` | `T2`, `T10`, `T14` | manual, integration | Canonical `docs/learn/` namespace, optional index, no templates, no empty taxonomy |
| `R8`-`R13`, `R11a`, `R30` | `T3`, `T14` | manual | Session record as primary output, required fields, four phases, empty sessions, periodic windows |
| `R14`-`R18` | `T4`, `T11` | manual, integration | One primary classification, secondary routes, classification table, contributor confirmation gate |
| `R19`-`R25a` | `T5`, `T6`, `T14` | manual | Route behavior for all primary classifications, pre-session no-record closeout, no roadmap accumulation |
| `R26`-`R30` | `T7`, `T14` | manual | Trigger types do not lower evidence standard; single events do not create durable lessons without reusable evidence |
| `R31`-`R35` | `T8`, `T14` | manual | Topic files are curated guidance and preserve traceability when changed, removed, or absorbed |
| `R36`-`R43` | `T9`, `T11`, `T14` | manual, integration | Bounded evidence collection and trigger-specific evidence rules |
| `R44` | `T10`, `T14` | integration | Learn paths are known selector paths with lightweight validation |
| `R47` | `T12`, `T14` | integration | Generated Codex skill and public adapter outputs are refreshed through generators |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T5`, `T6` | Durable lesson plus `process-follow-up` secondary route goes to topic guidance and tracked follow-up, not roadmap |
| `E2` | `T7` | Maintainer-requested single event closes with `no-durable-lesson` and no derivative updates |
| `E3` | `T5`, `T8` | Behavior-changing lesson updates authoritative artifact and keeps topic guidance non-authoritative |
| `E4` | `T4` | Candidate classifications without confirmation do not route |
| `E5` | `T8` | Absorbed or removed topic entries preserve traceability |
| `E6` | `T9` | Explicit invocation reads targeted evidence rather than full governance files by default |
| `E7` | `T3` | Periodic frame records start date, end date, and window basis |

## Edge case coverage

- Maintainer-requested single event with no reusable pattern or systemic gap: `T7`
- Repeated finding already captured in a topic file or authoritative artifact: `T3`, `T8`
- One observation with one primary classification and one or more secondary routes: `T4`, `T5`
- Obsolete topic entry absorbed into an approved spec or other authoritative artifact: `T8`
- Process follow-up with no issue tracker and no active plan owner: `T6`
- Missing contributor confirmation: `T4`
- Topic file conflicts with higher-priority spec, ADR, workflow doc, skill file, proposal, plan, or action-owning artifact: `T8`
- Small explicit invocation that names one artifact: `T9`
- Periodic session with no observations in the selected window: `T3`, `T7`
- Canonical skill change requiring generated output refresh: `T12`
- Invalid learn artifact path or legacy `docs/learnings/**` or `docs/retrospectives/**` usage after adoption: `T2`, `T10`
- Private incident details that should not be committed verbatim: `T13`

## Test cases

### T1. Workflow and governance surfaces preserve trigger-based `learn` and retire temporary learn surfaces

- Covers: `R1`, `R45`, `R46`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `README.md` if implementation finds affected wording
- Steps:
  - Review touched workflow and governance surfaces.
  - Confirm `learn` remains periodic or explicitly invoked and is not described as a default final per-change stage.
  - Confirm the temporary learn-recording rule no longer acts as the final model.
  - Confirm affected surfaces point to `docs/learn/sessions/**`, `docs/learn/topics/**`, and action-owning artifacts where appropriate.
  - Confirm unaffected surfaces are recorded with rationale in the plan, test spec, or change-local artifacts.
  - Run the milestone M1 selector and CI commands from the active plan.
- Expected result:
  - Contributors see one final learn artifact model and no stale temporary closeout model for post-adoption learn sessions.
- Failure proves:
  - The implementation leaves contradictory workflow contracts or silently skips affected governance surfaces.
- Automation location:
  - Manual review during M1.
  - `python scripts/select-validation.py --mode explicit ...`
  - `bash scripts/ci.sh --mode explicit ...`

### T2. Canonical learn namespace is clear and lightweight

- Covers: `R2`, `R2a`, `R3`, `R4`, `R5`, `R6`, `R7`
- Level: manual, integration
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - selector output for representative learn paths
- Steps:
  - Confirm session records use `docs/learn/sessions/YYYY-MM-DD-<slug>.md`.
  - Confirm topic files use `docs/learn/topics/<topic>.md`.
  - Confirm new learn guidance does not authorize `docs/learnings/**` or `docs/retrospectives/**` as canonical learn surfaces.
  - Confirm the first implementation adds no session template, topic template, empty topic file, or fixed topic taxonomy.
  - Confirm topic file creation is tied to at least one confirmed durable lesson.
  - Run selector checks for `docs/learn/README.md`, `docs/learn/sessions/2026-05-04-example.md`, and `docs/learn/topics/verification.md`.
- Expected result:
  - The namespace is discoverable without adding prebuilt structure that the spec forbids.
- Failure proves:
  - The implementation either keeps legacy learn paths or adds structure before usage justifies it.
- Automation location:
  - Manual review during M2 and M3.
  - `python scripts/select-validation.py --mode explicit --path docs/learn/README.md --path docs/learn/sessions/2026-05-04-example.md --path docs/learn/topics/verification.md`

### T3. Session record guidance captures required fields, phases, empty outcomes, and periodic windows

- Covers: `R8`, `R9`, `R10`, `R11`, `R11a`, `R12`, `R13`, `R30`, `E7`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Confirm the session record is described as the primary learn-session output.
  - Confirm session guidance names trigger, trigger type, scope, evidence in scope, exclusions, prior learnings reviewed, observations, classification decisions, secondary routes, routing results, and no-learn rationale when applicable.
  - Confirm the ordered phases are `Frame`, `Observe`, `Classify`, and `Route`.
  - Confirm `Frame` establishes session path and, for periodic sessions, start date, end date, and window basis.
  - Confirm `Observe` requires evidence-bound observations, already-captured lesson checks, and an explicit no-observation result when appropriate.
  - Confirm empty sessions are valid and still produce a tracked session record after `Frame`.
- Expected result:
  - A contributor can run a learn session without relying on a hidden template, while still capturing all required session fields.
- Failure proves:
  - Session records would be incomplete, template-dependent, or able to skip empty-session accountability.
- Automation location:
  - Manual review during M1 and M3.

### T4. Classification records preserve one primary classification and stop routing without confirmation

- Covers: `R14`, `R15`, `R16`, `R17`, `R18`, `E4`
- Level: manual, integration
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `scripts/test-skill-validator.py`
  - generated skill output after M3
- Steps:
  - Confirm the allowed primary classifications are exactly `observation`, `durable-lesson`, `artifact-update`, `decision`, `direction`, `process-follow-up`, and `no-durable-lesson`.
  - Confirm secondary routes are described as derivative routes and do not become additional primary classifications.
  - Confirm the classification decisions record includes observation ID, proposed primary classification, final primary classification, secondary routes, confirmed-by value, and rationale.
  - Confirm routing does not proceed until every routed observation has a contributor-confirmed final classification.
  - Confirm candidate classifications may be recorded without updating topic files, ADRs, proposals, follow-ups, or action-owning artifacts.
  - Run skill-validator regression tests after stable wording is added.
- Expected result:
  - The skill cannot convert observations into durable guidance or follow-up artifacts without contributor confirmation.
- Failure proves:
  - The classification model is ambiguous or permits unilateral routing by the agent.
- Automation location:
  - Manual review during M3.
  - `python scripts/test-skill-validator.py`

### T5. Routing rules send each primary classification to the correct destination

- Covers: `R19`, `R20`, `R21`, `R22`, `R23`, `R33`, `E1`, `E3`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Confirm `observation` routes to the session record only.
  - Confirm `durable-lesson` routes to a topic file with date, short lesson, source-session link, primary classification, and secondary routes when present.
  - Confirm `artifact-update` routes to the affected authoritative artifact and links back from the session record.
  - Confirm `decision` routes to ADR or another decision artifact and links from the session record and relevant topic entry.
  - Confirm `direction` routes to a proposal or trackable follow-up and is not encoded as topic-file policy.
  - Confirm behavior-changing lessons update the action-owning artifact rather than relying on the topic file as source of truth.
- Expected result:
  - Each classification has one clear route and topic files cannot become policy by accident.
- Failure proves:
  - The implementation leaves contributors free to choose inconsistent or non-authoritative routing surfaces.
- Automation location:
  - Manual review during M1 and M3.

### T6. Follow-up and no-record boundaries avoid roadmap accumulation

- Covers: `R24`, `R25`, `R25a`, `E1`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Confirm `process-follow-up` routes to a linked issue when available, an active plan when one owns the work, or a proposal when no tracker or active plan exists.
  - Confirm `docs/roadmap.md` is not presented as the fallback for learn follow-ups.
  - Confirm `no-durable-lesson` routes to the session record with no-learn rationale and whether follow-up was scheduled.
  - Confirm review-visible no-record surfaces are allowed only for pre-session trigger closeout when `learn` does not actually run as a session.
- Expected result:
  - Learn follow-ups become tracked work or proposals, and no-record closeout cannot be used after a learn session reaches `Frame`.
- Failure proves:
  - The implementation still allows aspirational lists or chat-only/no-record closeout for actual learn sessions.
- Automation location:
  - Manual review during M1 and M3.

### T7. Trigger type does not lower the evidence standard

- Covers: `R26`, `R27`, `R28`, `R29`, `R30`, `E2`
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - `specs/rigorloop-workflow.md`
- Steps:
  - Confirm maintainer request, cadence trigger, incident response, contributor observation, and explicit invocation are all valid learn triggers.
  - Confirm none of those trigger types lowers the evidence standard for durable lessons.
  - Confirm a single event remains `observation` or `no-durable-lesson` unless evidence shows reusable pattern or systemic gap.
  - Confirm maintainer-driven rule adoption without accumulated evidence routes to proposal work that may later produce an ADR.
  - Confirm sessions with no durable lessons are recorded as valid empty outcomes.
- Expected result:
  - The trigger decides whether a session may run; evidence decides what the session captures.
- Failure proves:
  - Maintainer-requested or incident-triggered sessions can manufacture durable lessons from thin evidence.
- Automation location:
  - Manual review during M1 and M3.

### T8. Topic files remain curated, non-authoritative, and traceable

- Covers: `R31`, `R32`, `R33`, `R34`, `R35`, `E3`, `E5`
- Level: manual
- Fixture/setup:
  - `docs/learn/README.md`
  - `skills/learn/SKILL.md`
  - `specs/rigorloop-workflow.md`
  - representative topic-file guidance if implementation adds real topic content
- Steps:
  - Confirm topic files are described as curated guidance, not workflow, product, architecture, validation, skill, implementation, or decision contracts.
  - Confirm topic files do not override `CONSTITUTION.md`, approved specs, accepted ADRs, approved architecture docs, workflow docs, skill files, accepted proposals, active plans, or action-owning artifacts.
  - Confirm topic entries may be added, revised, superseded, absorbed, or removed.
  - Confirm removal or absorption preserves traceability through a session link, authoritative-artifact link, topic-file edit rationale, or explain-change rationale.
- Expected result:
  - Topic guidance remains useful for discovery without competing with higher-priority artifacts.
- Failure proves:
  - The implementation can create quasi-policy topic files or erase lesson history without traceability.
- Automation location:
  - Manual review during M1 and M3.

### T9. Learn evidence collection is bounded and trigger-specific

- Covers: `R36`, `R37`, `R38`, `R39`, `R40`, `R41`, `R42`, `R43`, `E6`
- Level: manual, integration
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm evidence collection starts from trigger statement and named artifacts.
  - Confirm relevant learn index, sessions, and topics are checked only when present and relevant to the trigger or topic.
  - Confirm governance and workflow context are checked for need, then read by summaries/headings/exact sections before full-file reads.
  - Confirm periodic sessions inspect changes in the selected window when relevant.
  - Confirm incident sessions inspect incident reports and related artifacts when present.
  - Confirm explicit invocations inspect user-named artifacts and artifacts implied by the stated pattern.
  - Run skill-validator regression tests for stable bounded-evidence wording.
- Expected result:
  - Small learn invocations stay cheap while still using enough evidence for classification and routing.
- Failure proves:
  - The skill either becomes too expensive by default or too thin to justify evidence-bound observations.
- Automation location:
  - Manual review during M3.
  - `python scripts/test-skill-validator.py`

### T10. Selector recognizes learn paths without lifecycle-validating raw session content

- Covers: `R44`
- Level: integration
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - representative paths:
    - `docs/learn/README.md`
    - `docs/learn/sessions/2026-05-04-example.md`
    - `docs/learn/topics/verification.md`
- Steps:
  - Add selector regression tests for the representative learn paths.
  - Run `python scripts/test-select-validation.py`.
  - Run explicit selector validation for the representative learn paths.
  - Confirm the paths are classified as known learn artifact paths.
  - Confirm selector output has no `unclassified-path` or manual-routing blocker for those paths.
  - Confirm session and topic files are not routed through lifecycle validation for specs, plans, ADRs, or architecture artifacts.
- Expected result:
  - Targeted validation can reason about learn artifacts without imposing lifecycle-managed artifact rules on raw session records or curated topic files.
- Failure proves:
  - Learn artifacts remain invisible to validation routing or are over-validated as the wrong artifact class.
- Automation location:
  - `scripts/test-select-validation.py`
  - `scripts/select-validation.py`

### T11. Skill-validator coverage protects stable learn guidance

- Covers: `R10`-`R18`, `R36`-`R43`
- Level: integration
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
- Steps:
  - Add stable assertions for required learn guidance terms: canonical paths, phase names, primary classification, secondary routes, confirmation gate, no-durable-lesson, topic authority, bounded evidence, and generated-output boundary.
  - Add negative assertions for stale terms such as canonical `docs/retrospectives/**`, canonical `docs/learnings/**`, and temporary pre-refactor learn-surface wording.
  - Run skill validation and skill-validator regression tests.
- Expected result:
  - Stable process terms remain present while obsolete learn-routing guidance is rejected.
- Failure proves:
  - Future edits could silently regress the contributor-visible learn process or reintroduce old surfaces.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`

### T12. Generated skill and adapter output is deterministic

- Covers: `R47`
- Level: integration
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `.codex/skills/learn/SKILL.md`
  - `dist/adapters/claude/.claude/skills/learn/SKILL.md`
  - `dist/adapters/codex/.agents/skills/learn/SKILL.md`
  - `dist/adapters/opencode/.opencode/skills/learn/SKILL.md`
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run generated-output drift checks.
  - Run adapter validation.
  - Confirm generated files were changed only through generators, not by hand.
- Expected result:
  - Runtime skill mirrors and public adapter output match canonical `skills/learn/SKILL.md`.
- Failure proves:
  - Generated outputs are stale, manually edited, or inconsistent with canonical source.
- Automation location:
  - `python scripts/build-skills.py`
  - `python scripts/build-adapters.py --version 0.1.1`
  - `python scripts/build-skills.py --check`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T13. Security and privacy boundaries are preserved for learn outputs

- Covers: security and privacy behavior from the approved spec
- Level: manual
- Fixture/setup:
  - `skills/learn/SKILL.md`
  - `docs/learn/README.md`
  - any incident-session guidance changed by implementation
- Steps:
  - Confirm learn guidance says incident-triggered sessions summarize sensitive evidence rather than committing secrets or private incident details verbatim.
  - Confirm learn outputs do not introduce authentication, authorization, credential storage, external service, or private data collection behavior.
  - Confirm generated-output guidance still requires repository-owned generators.
- Expected result:
  - Learn artifacts remain contributor-visible without exposing credentials, tokens, private keys, private incident data, or unnecessary machine-local details.
- Failure proves:
  - The implementation could leak sensitive evidence through durable learn artifacts.
- Automation location:
  - Manual review during M3 and M4.

### T14. Final explicit-path CI proves touched surfaces are coherent

- Covers: `R1`-`R47`
- Level: smoke, integration, manual
- Fixture/setup:
  - all files changed by M1 through M3
  - `docs/changes/2026-05-04-learn-artifact-model/change.yaml`
  - `docs/changes/2026-05-04-learn-artifact-model/explain-change.md`
- Steps:
  - Run the final validation commands named in M4 of the active plan.
  - Confirm lifecycle validation includes the proposal, feature spec, test spec, workflow spec, workflow test spec, plan index, plan body, and change-local artifacts.
  - Confirm explicit-path CI includes governance docs, workflow summary, learn README, feature spec, test spec, workflow spec/test spec, canonical skill, selector tests, skill-validator tests, generated skill output, generated adapter output, plan surfaces, and change-local artifacts.
  - Confirm final manual review sees no conflict between spec, test spec, plan, workflow docs, skill guidance, selector behavior, and generated output.
- Expected result:
  - The full changed surface gives one coherent learn artifact model and is ready for `code-review`.
- Failure proves:
  - Milestone-local checks passed but the integrated contributor-facing contract still drifted.
- Automation location:
  - M4 validation commands in `docs/plans/2026-05-04-learn-artifact-model.md`.

## Fixtures and data

- Use real repository files as fixtures for manual contract review.
- Add selector regression cases to `scripts/test-select-validation.py` for:
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-05-04-example.md`
  - `docs/learn/topics/verification.md`
- Add stable learn guidance assertions to `scripts/test-skill-validator.py`.
- No session template, topic template, empty topic file, fixed taxonomy, issue-tracker fixture, external service fixture, or background index fixture is required.

## Mocking/stubbing policy

- Do not mock repository path classification for selector tests; use the real selector API or CLI helpers used by existing selector tests.
- Do not mock generated output drift; run the existing repository generators and `--check` modes.
- Manual review may use representative learn-session examples in prose, but implementation must not commit those examples as templates unless a later approved change permits templates.
- No network, issue tracker, database, or external service should be stubbed because the spec does not introduce those integrations.

## Migration or compatibility tests

- Confirm existing pre-adoption learning notes outside `docs/learn/` may remain unless a later approved migration plan relies on them.
- Confirm new post-adoption learn sessions and topic guidance use `docs/learn/sessions/**` and `docs/learn/topics/**`.
- Confirm rollback is documented as restoring the prior temporary-surface workflow rule and removing or superseding new learn-path selector classification.
- Confirm no migration of historical notes into `docs/learn/` is performed in this slice.

## Observability verification

- Learn observability is artifact-based. Manual review must confirm session records expose trigger, scope, evidence, observations, classifications, routing, derivative links, and no-learn rationale through skill guidance and the learn index.
- Selector observability is JSON output from `scripts/select-validation.py`, including `classified_paths`, `unclassified_paths`, `selected_checks`, `blocking_results`, and rationale.
- Generated-output observability is drift-check output from `build-skills.py --check` and `build-adapters.py --check`.

## Security/privacy verification

- Covered by `T13`.
- Manual review must confirm learn guidance warns against committing secrets, credentials, tokens, private keys, private incident data, or unnecessary machine-local details.
- No additional security automation is required because the feature does not add runtime authentication, authorization, or secret-handling code.

## Performance checks

- Covered by `T9` through bounded-evidence guidance and skill-validator assertions.
- No benchmark is required because the implementation does not add runtime code, background jobs, indexes, caches, storage, or network calls.
- Manual review must confirm the skill avoids full-reading every governance artifact by default.

## Manual QA checklist

- Confirm workflow/governance docs preserve `learn` as periodic or explicitly invoked.
- Confirm `docs/learn/README.md` is an index only.
- Confirm no session/topic templates, empty topic files, or fixed taxonomy were added.
- Confirm the `learn` skill names all four phases and all seven primary classifications.
- Confirm the `learn` skill requires contributor confirmation before routing.
- Confirm single-event and maintainer-request guidance preserves the evidence standard.
- Confirm topic authority and traceability rules are present.
- Confirm selector output recognizes representative learn paths.
- Confirm generated outputs were refreshed through repository generators.
- Confirm final plan, explain-change, and validation evidence match the real diff.

## What not to test

- Do not test runtime application behavior; none is introduced.
- Do not test issue tracker integration; the spec only defines routing when a tracker exists and fallback to active plan or proposal.
- Do not add snapshot-only tests for contributor-facing prose.
- Do not test a fixed session or topic template because templates are explicitly deferred.
- Do not test migration of historical notes into `docs/learn/`; migration is out of scope.
- Do not require broad smoke unless a later review or verification gate elevates it.

## Uncovered gaps

- None. All `MUST` requirements and named edge cases have a planned manual, integration, or smoke proof surface.

## Next artifacts

- Implement M1 through M4 in [Learn Artifact Model Implementation Plan](../docs/plans/2026-05-04-learn-artifact-model.md).
- Run `code-review` after M4 validation and before downstream verify/explain-change/PR gates.

## Follow-on artifacts

- None yet.

## Readiness

Active proof-planning surface. Implementation may proceed with M1 of the active plan.
