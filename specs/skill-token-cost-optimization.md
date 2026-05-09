# Skill Token Cost Optimization

## Status

approved

## Related proposal

- [Skill Token Cost Optimization](../docs/proposals/2026-05-09-skill-token-cost-optimization.md)

## Goal and context

This spec defines how RigorLoop skill guidance must reduce unnecessary context and token cost during evidence collection without weakening correctness, reviewability, or validation coverage.

The behavior being specified is contributor-visible and public-skill-facing. It tightens the existing skill-contract evidence-reading rules so agents choose bounded evidence before broad reads when working with large files, repeated scans, generated output, validation logs, historical artifacts, or other high-volume surfaces.

This spec does not replace `specs/skill-contract.md`. It defines an accepted amendment that the skill-contract spec, selected skill text, tests, and generated public skill output must implement.

## Glossary

- `bounded evidence`: a small evidence surface such as a changed-path list, inventory, heading list, stable ID, count, matching line number, or targeted excerpt.
- `broad read`: a full-file read, broad recursive search, generated-output dump, validation log dump, or raw excerpt that includes substantially more text than the current question needs.
- `high-volume surface`: a file set, artifact, log, generated output tree, or historical record set likely to produce large output.
- `token-cost discipline`: selecting the smallest evidence surface that can answer the current question before broadening.
- `full-file-read escape condition`: a condition where correctness requires reading the full file or a broader section despite token cost.
- `output cap`: a tool or command setting that truncates returned text, such as a maximum output token setting. An output cap is a safety rail, not evidence-selection logic.
- `published skill text`: skill instructions shipped to users through local skill mirrors or public adapter packages.
- `repository-maintainer guidance`: instructions for maintaining this repository's canonical skill sources, generated mirrors, adapter output, validators, and release packaging.

## Examples first

### Example E1: broad search avoided for proposal context

Given an agent is authoring a proposal about skill evidence collection
When the agent needs to find related guidance
Then the agent starts with known proposal, spec, and workflow paths or heading searches
And it does not run a broad recursive search over all docs, specs, skills, and generated output as the first evidence step.

### Example E2: full-file read remains required for direct review

Given `spec-review` is reviewing a feature spec
When the whole spec is the review target
Then the reviewer reads the full spec
And token-cost guidance does not permit reviewing only search snippets.

### Example E3: output cap is not query design

Given a command can return thousands of matching lines
When an agent sets an output cap
Then the agent still narrows the query with path scope, stable IDs, `rg -l`, counts, headings, or targeted ranges before relying on the output cap.

### Example E4: validation semantics remain unchanged

Given a validation command has required checks
When normal output is summarized or failure-focused
Then the command still runs the same selected checks
And omitted details remain available through focused reruns, verbose output, or recorded failure paths.

### Example E5: public skill text stays portable

Given a public skill tells users how to collect evidence efficiently
When it names validation or project surfaces
Then it uses project-portable wording such as project workflow guide, local workflow contract, changed paths, validation logs, and project validation command
And it does not expose RigorLoop maintainer-only generator or adapter paths.

## Requirements

R1. The system MUST treat token-cost discipline as part of normalized skill behavior.

R1a. Token-cost discipline MUST be implemented as an amendment to the skill contract, not as a new workflow stage.

R1b. Token-cost discipline MUST NOT reduce required validation coverage, review obligations, artifact obligations, or workflow stage gates.

R2. Normalized skills that collect evidence from high-volume surfaces MUST prefer bounded evidence before broad reads.

R2a. Bounded evidence includes inventories, changed paths, headings, stable IDs, requirement IDs, test IDs, check IDs, path lists, counts, matching line numbers, diffs, and targeted excerpts.

R2b. Skills MUST guide agents to broaden from bounded evidence to neighboring context or full-file reads only when the bounded evidence is insufficient for the current decision.

R2c. Skills MUST NOT present a broad recursive search, generated-output dump, validation-log dump, or full-file read as the default first step for high-volume surfaces.

R3. Normalized skills MUST preserve full-file-read escape conditions.

R3a. A full-file read is required when the whole file is the review target.

R3b. A full-file read or broader section read is required when the relevant section cannot be isolated safely.

R3c. A full-file read or broader section read is required when surrounding context can change the conclusion.

R3d. A full-file read or broader section read is required when bounded searches conflict, are incomplete, or produce ambiguous evidence.

R3e. A full-file read is required when behavior-changing edits depend on the whole source-of-truth artifact.

R3f. Token-cost guidance MUST state or preserve that correctness outranks token savings.

R4. Output caps MUST be treated as safety rails, not evidence-selection strategy.

R4a. Skill guidance MUST NOT imply that setting an output cap makes a broad query acceptable as the normal first pass.

R4b. Skill guidance SHOULD name low-volume query strategies such as filename-first searches, count-first searches, precise globs, stable IDs, and targeted range reads when those examples fit the skill.

R5. Summary-first and failure-focused output MUST preserve validation semantics.

R5a. Normal output budgets MAY reduce routine output volume.

R5b. Normal output budgets MUST NOT change selected check coverage, command exit behavior, failure detection, or required validation evidence.

R5c. When a command or skill output omits detail for readability, it MUST say how to request or obtain the omitted detail when the omission affects reviewability.

R6. The first implementation slice MUST update the normative contract and selected high-volume stage skills.

R6a. The first implementation slice MUST update `specs/skill-contract.md` to include the stricter token-cost behavior.

R6b. The first implementation slice MUST update `specs/skill-contract.test.md` or equivalent repo-owned tests to cover the stricter behavior.

R6c. The first implementation slice MUST include the major skills most likely to perform high-volume evidence collection: `proposal`, `proposal-review`, `spec`, `spec-review`, `plan`, `plan-review`, `implement`, `code-review`, `verify`, `pr`, and `learn`.

R6d. The first implementation slice MAY include additional skills that already carry evidence-collection guidance when doing so reduces drift without broadening the behavior contract.

R6e. The first implementation slice MUST NOT require a new `token-budget` skill.

R7. Public skill wording MUST remain project-portable.

R7a. Published skill text MUST use project-portable terms such as project workflow guide, local workflow contract, changed paths, generated output, validation logs, and project validation command.

R7b. Published skill text MUST NOT expose RigorLoop repository-maintainer-only source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation mechanics, or RigorLoop-local examples.

R7c. Repository-maintainer validation commands and generated-output procedures MAY remain in internal specs, tests, plans, contributor docs, and change-local evidence.

R8. Static validation MUST be narrow and reviewable.

R8a. Static validation MUST check for required token-cost guidance through stable sections, phrases, examples, or requirement coverage.

R8b. Static validation MUST preserve the full-file-read escape conditions.

R8c. Static validation MUST check the output-cap distinction where the implementation adds that wording to skill-contract surfaces.

R8d. Static validation MUST NOT perform broad natural-language quality scoring.

R9. Generated output and public adapters MUST remain deterministic derived output.

R9a. Canonical skill changes MUST be checked against generated local skill output.

R9b. Public adapter output MUST receive adapter drift check and adapter validation when public skill text changes.

R9c. The normal adapter validation commands for this change are:

```bash
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
```

R10. Reviewers MAY report broad, noisy evidence collection as a process defect when it materially affects a workflow artifact, review, implementation, or verification result.

R10a. A process-defect finding MUST identify the noisy evidence surface and the safer bounded evidence strategy.

R10b. A process-defect finding MUST NOT require reducing correctness checks, skipping required artifacts, or ignoring full-file-read escape conditions.

## Inputs and outputs

Inputs:

- accepted proposal for skill token-cost optimization;
- existing skill-contract spec;
- existing workflow efficient-evidence guidance;
- canonical skill files that collect evidence;
- generated local skill output and public adapter output when canonical skill text changes;
- skill validation, skill-regression, generated-output drift, and adapter validation scripts.

Outputs:

- updated skill-contract spec and test spec;
- updated selected canonical skills;
- regenerated or checked generated skill output;
- regenerated or checked public adapter output;
- validation evidence showing the stricter guidance is present and generated outputs are aligned.

## State and invariants

- `specs/skill-contract.md` remains the normative skill-contract source.
- This spec is an amendment that the skill-contract spec implements.
- The workflow stage order does not change.
- Required validation and review gates do not change.
- Correctness outranks token savings.
- Full-file-read escape conditions remain available.
- Published skill text remains project-portable.
- Generated local skill output and public adapter output remain derived, not hand-authored.

## Error and boundary behavior

- If bounded evidence is insufficient, conflicting, or ambiguous, the skill must broaden the read before making a review, implementation, verification, or readiness claim.
- If a full-file read is required by the escape conditions, failing to perform it is a review defect even if bounded evidence was cheaper.
- If a validation summary hides a failure cause needed for review, the agent must rerun or expose focused detail before claiming validation evidence.
- If static checks would block explicit negative guidance or escape-condition wording, the checks must be narrowed before they are relied on.
- If public skill portability conflicts with repository-maintainer validation detail, the public skill must stay portable and the maintainer detail must move to internal spec, plan, test, contributor, or change-local surfaces.

## Compatibility and migration

- Existing historical artifacts remain valid.
- Existing learn records do not need migration.
- Existing unmodified skills remain valid until touched by the approved implementation slice or later normalization work.
- Existing validation commands keep their semantics.
- Existing full-file review obligations remain valid.
- Rollback may revert the spec, test, skill, generated-output, and adapter-output changes together because no runtime data migration is involved.

## Observability

- Validation failures should identify the missing token-cost guidance, missing escape condition, portability issue, generated-output drift, or adapter validation failure.
- Review and verify artifacts should cite the concrete commands run rather than generic success claims.
- No runtime logs, metrics, traces, or audit events are required because this is repository workflow and skill guidance behavior.

## Security and privacy

- Token-cost guidance MUST NOT encourage committing or pasting secrets, credentials, tokens, private keys, private incident data, unnecessary machine-local paths, or private user data.

- Summary-first output SHOULD reduce unnecessary exposure of large logs or generated output.

- When sensitive evidence is relevant, skills MUST prefer summarized or redacted evidence that still supports the required review or validation conclusion.

## Accessibility and UX

No user-interface behavior is involved.

The contributor experience requirement is that skill guidance stays concise enough to scan and does not become a long tutorial.

## Performance expectations

- The first validation slice MUST remain static and repository-local.
- The first validation slice MUST NOT add broad semantic quality scoring.
- Skill and adapter validation should remain suitable for normal pre-PR validation.
- Token-cost guidance should reduce unnecessary evidence volume in normal agent turns, but no exact token-count metric is required.

## Edge cases

1. If a short artifact is the relevant source of truth, reading the whole artifact may be the smallest sufficient evidence surface.
2. If a generated-output tree is the review target, the agent may need summaries plus targeted generated excerpts rather than every generated file.
3. If a command fails, failure output may exceed the normal output budget only as much as needed to diagnose the failure.
4. If the user explicitly asks to show full command output, the agent may provide the requested output while still avoiding unrelated broad reads.
5. If the first bounded search shows the search terms are noisy, the agent must narrow the next query rather than repeating broad searches with different output caps.
6. If an implementation modifies exact wording in a governing artifact, the relevant section or whole file must be read as needed to preserve the contract.
7. If public skill text needs to mention validation commands, it must do so through project-portable wording unless the adopting project supplies a local command.
8. If a reviewer needs to reconstruct a process-defect finding, the finding must cite the broad evidence surface and the bounded alternative, not just say "too many tokens."

## Non-goals

- Do not change workflow stage order.
- Do not add a new token-budget skill.
- Do not reduce required validation coverage.
- Do not remove full-file-read obligations.
- Do not replace formal artifacts with chat summaries.
- Do not add broad natural-language quality scoring.
- Do not expose repository-maintainer-only generated-output or adapter mechanics in published skill text.
- Do not migrate historical learn sessions or historical proposals.

## Acceptance criteria

- A reviewer can identify this spec as an amendment to the existing skill contract.
- A reviewer can confirm that correctness outranks token savings.
- A reviewer can identify the bounded-evidence-first behavior.
- A reviewer can identify the full-file-read escape conditions.
- A reviewer can confirm that output caps are not treated as query design.
- A reviewer can confirm that validation semantics are not weakened.
- A reviewer can identify the first-slice skills in scope.
- A reviewer can confirm that no standalone token-budget skill is required.
- A reviewer can confirm that public skill wording remains project-portable.
- A reviewer can confirm that static validation is narrow and not broad semantic scoring.
- A reviewer can confirm that generated skill drift, adapter drift, and adapter validation are required when public skill text changes.

## Open questions

- Should `docs/workflows.md` receive new wording, or is the existing efficient-evidence summary sufficient once the skill contract and skills are tightened?
- Should additional lower-volume skills be included in the first implementation slice to avoid drift, or deferred to later normalization work?

These questions do not block spec review because the required behavior and minimum first slice are defined.

## Architecture no-impact rationale

Architecture surface: no-impact-rationale.

This change updates workflow guidance, the skill contract, selected skill text, validation coverage, generated skill output, and public adapter output. It does not introduce or revise runtime components, system boundaries, data flow ownership, persistence, deployment topology, release architecture, cache/indexing strategy, security boundaries, adapter packaging architecture, or the C4 plus arc42 plus ADR architecture-package method.

No canonical architecture package update is required. No C4 diagram update is required. No ADR is required.

## Next artifacts

- Architecture-review of the no-impact rationale.
- Test spec mapping each requirement to concrete validation and manual review coverage.
- Execution plan for the skill-contract, skill text, generated output, adapter validation, and lifecycle artifacts.

## Follow-on artifacts

- Spec-review: approved on 2026-05-09 with no material findings; clean review settled artifact-locally.
- Architecture: no-impact rationale recorded in this spec on 2026-05-09.

## Readiness

Ready for `architecture-review`.

The approved contract has no runtime architecture impact. Architecture-review can review the no-impact rationale before test-spec and planning continue.
