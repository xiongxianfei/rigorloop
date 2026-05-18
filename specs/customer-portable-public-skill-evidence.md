# Customer-Portable Public Skill Evidence

## Status

approved

## Related proposal

- [Customer-Portable Public Skills and Token-Friendly Local Guidance](../docs/proposals/2026-05-18-customer-portable-public-skills-and-token-friendly-local-guidance.md)

## Goal and context

This spec defines the customer-portable evidence contract for public RigorLoop skills.

RigorLoop can now be installed outside this repository. In a customer project, public skills cannot assume RigorLoop repository-internal `specs/`, `docs/`, `CONSTITUTION.md`, `AGENTS.md`, reports, follow-up files, scripts, templates, or generated adapter internals exist. Public skills must work from the user's request, the skill's own concise operating contract, and project-local artifacts when those artifacts exist.

This spec narrows the first implementation slice to customer-project portability and token-friendly evidence behavior. It does not define new CLI features, hard token gates, workflow YAML, generated workflow docs, or a full rewrite of every skill.

## Glossary

- `customer project`: a repository using installed RigorLoop public skills outside the RigorLoop repository.
- `customer-project mode`: the default operating mode for public skills, where only the current project and installed skills may be assumed available.
- `RigorLoop repository mode`: operation inside the RigorLoop repository, or explicit user work on RigorLoop itself.
- `project-local artifact`: a file in the current project, such as local `docs/workflows.md`, `rigorloop.yaml`, `rigorloop.lock`, `docs/changes/<change-id>/change.yaml`, specs, plans, governance files, architecture records, source files, tests, or CI files.
- `RigorLoop repository-internal artifact`: this repository's internal specs, docs, reports, scripts, templates, root governance, generated mirrors, adapter output, or follow-up files when they are not project-local artifacts in the current customer project.
- `portable default`: the fallback path or behavior embedded in a public skill for use when project-local guidance is absent.
- `broad search`: a repository-wide or large-scope search for authoritative docs, specs, reports, generated output, or historical artifacts before bounded evidence has been tried.

## Examples first

### Example E1: proposal authoring without RigorLoop internals

Given a customer project has installed public skills
And it has no `CONSTITUTION.md`, no `AGENTS.md`, and no RigorLoop internal `specs/`
When `proposal` is asked to create a proposal with no explicit path
Then it uses the proposal skill's portable default path
And it does not search for RigorLoop repository governance files.

### Example E2: local workflow guide present

Given a customer project has `docs/workflows.md`
When `spec` needs artifact placement
Then it reads the relevant local workflow-guide section
And follows the local artifact-location guidance unless a higher-priority local source conflicts.

### Example E3: no safe default

Given a review skill cannot determine a selectable local change root
And no explicit change ID or project-local workflow guidance resolves it
When formal review recording is required
Then the skill reports recording blocked
And it does not invent a path or search for RigorLoop repository originals.

### Example E4: project map orientation

Given a customer repository has no `AGENTS.md`, no `CONSTITUTION.md`, and no `docs/project-map.md`
When `project-map` maps the repository
Then it continues from available project-local files such as `README.md`, package/config files, `src/`, `tests/`, local docs, and local specs
And treats absent governance files as normal.

### Example E5: workflow creates local guidance

Given a customer project is adopting RigorLoop
When artifact locations are missing or routing depends on local workflow guidance
Then `workflow` creates or refreshes the project-local `docs/workflows.md`
And other stage skills may use that local guide when present.

### Example E6: verify without validation evidence

Given a customer project has no validation command in local artifacts
When `verify` is asked to claim validation passed
Then it refuses that claim
And reports the missing validation surface.

## Requirements

R1. Public skills MUST operate in customer-project mode by default.

R2. Public skills MUST NOT require RigorLoop repository-internal artifacts as customer-project evidence.

R3. Public skills MAY use RigorLoop repository-internal artifacts only when the current repository is the RigorLoop repository, the user explicitly asks to work on RigorLoop itself, the file is the direct target of the task, or the file exists as a relevant project-local artifact.

R4. Public skills MUST use project-local artifacts when those artifacts exist and are relevant to the task.

R5. Public skills MUST use bounded evidence before broad searches for workflow, path, status, review, validation, or artifact-placement evidence.

R6. Public skills MUST NOT broad-search for RigorLoop repository-internal specs, docs, reports, follow-up files, governance files, scripts, templates, generated mirrors, or adapter output in customer-project mode.

R7. Public skills MUST use portable defaults when project-local guidance is absent and the default is safe for the task.

R8. Public skills MUST block on ambiguity when project-local guidance is absent and no safe portable default exists.

R9. If local `docs/workflows.md` exists, public skills SHOULD use the relevant local section as the artifact-location and workflow-routing guide.

R10. Public skills MUST NOT make local `docs/workflows.md` an unconditional precondition for every task.

R11. The `workflow` skill MUST own creating or refreshing local `docs/workflows.md` when RigorLoop is being adopted, artifact locations are missing, or routing depends on local workflow guidance.

R12. Local `docs/workflows.md` guidance MUST include a concise customer-project portability section.

R13. The customer-project portability section in local workflow guidance MUST state that public skills operate in customer-project mode by default.

R14. The customer-project portability section in local workflow guidance MUST state that skills use project-local artifacts when present and relevant.

R15. The customer-project portability section in local workflow guidance MUST state that RigorLoop repository-internal specs, docs, root governance, reports, and follow-up files are not required customer-project runtime evidence.

R16. The customer-project portability section in local workflow guidance MUST state that skills use portable defaults where safe and block on ambiguity where no safe default exists.

R17. Proposal, proposal-review, spec, plan, implement, workflow, verify, pr, and project-map public skill wording MUST be updated in the first slice only where audit evidence shows required or misleading RigorLoop-internal document dependency risk.

R18. `code-review` public skill wording MUST remain unchanged in the first slice unless the audit finds a direct required RigorLoop-internal document dependency.

R19. A first-slice audit record MUST identify each touched skill and the reason it is touched.

R20. A first-slice audit record MUST identify any watchlist skill that remains unchanged and the reason it is not touched.

R21. Touched skill changes MUST preserve each skill's essential claim boundaries, stop conditions, required output shape, and safety-critical obligations.

R22. For each touched skill, implementation evidence MUST record removed or rewritten wording, why the rewrite is safe, and where the essential rule remains preserved.

R23. Review skills MUST preserve formal review recording, material finding shape, and review-resolution boundaries.

R24. Verify and PR skills MUST preserve validation, branch-readiness, PR-readiness, and no-false-claim boundaries.

R25. Project-map wording MUST treat local `AGENTS.md`, `CONSTITUTION.md`, `docs/`, and `specs/` as optional project-local orientation inputs whose absence is normal.

R26. Static validation MUST catch obvious required RigorLoop-internal document dependencies in public skill text.

R27. Static validation MUST NOT fail legitimate references to project-local specs, docs, governance files, architecture records, plans, or workflow guides when wording makes their project-local or conditional nature clear.

R28. Static validation MUST allow references guarded by conditions such as project-local, if present, when operating inside the RigorLoop repository, when this file is the review target, when the user provided this path, or when governing project docs exist.

R29. Static before/after token measurement MUST be recorded for first-slice public skill changes.

R30. The static token report MUST be recorded at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.md`.

R31. A matching machine-readable static report MAY be recorded at `docs/reports/token-cost/skills/2026-05-18-customer-portable-public-skills.yaml`.

R32. A targeted customer-fixture dynamic benchmark MUST be recorded for the first slice.

R33. The dynamic benchmark MUST use a customer fixture that excludes RigorLoop repository-internal root governance, internal specs, internal reports, `docs/follow-ups.md`, and `docs/project-map.md` unless the scenario is explicitly testing project-map creation or update behavior.

R34. The dynamic benchmark MUST include scenarios for `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `project-map`, `verify`, and `pr`.

R35. The dynamic benchmark MUST include `code-review` only if `code-review` skill wording changes.

R36. Dynamic benchmark evidence MUST record whether runs attempted broad searches for RigorLoop-internal docs, whether they relied on missing RigorLoop repository specs, whether local `docs/workflows.md` was used when present, whether portable defaults or ambiguity blocking were used, input tokens, largest command output, full-file reads, broad searches, and result-quality status.

R37. If canonical public skills change, generated public adapter output MUST be validated from canonical `skills/` using temporary or release-output generation.

R38. Generated adapter skill bodies MUST NOT be hand-edited to satisfy this spec.

R39. This first slice MUST NOT implement `rigorloop status`, `rigorloop validate`, workflow YAML, generated workflow docs, hard token gates, or a full release benchmark suite.

## Inputs and outputs

Inputs:

- explicit user path, change ID, or instruction;
- project-local source files, tests, docs, specs, plans, architecture records, governance files, workflow guides, and change-local artifacts when present and relevant;
- installed public skill text;
- local `rigorloop.yaml` and `rigorloop.lock` when present and relevant;
- RigorLoop repository-internal artifacts only under the allowed repository-mode or direct-target conditions in R3.

Outputs:

- updated canonical public skill text for the audited first-slice skills;
- concise customer-project portability guidance in `docs/workflows.md`;
- audit evidence for touched and untouched watchlist skills;
- static validation checks and passing evidence;
- static token report and optional YAML report;
- targeted customer-fixture dynamic benchmark evidence;
- generated adapter validation evidence when public skills change.

## State and invariants

- Public skills remain user-facing operating contracts, not references to private RigorLoop repository context.
- Customer projects may be self-guiding through local `docs/workflows.md`, but stage skills do not require that file for every task.
- Missing RigorLoop repository-internal files in a customer project are normal, not errors.
- Safety-critical review, verification, material-finding, mutation-safety, and release-boundary behavior remains in public skill text or another project-available operating surface.
- `skills/` remains the authored source for public skills.
- Generated adapters remain generated output.

## Error and boundary behavior

- If artifact placement has no safe portable default and no local guidance, the skill MUST block and ask for the path.
- If formal review recording has no selectable local change root, the review skill MUST report recording blocked instead of inventing a path.
- If upstream lifecycle or status evidence is missing or ambiguous, the skill MUST block reliance on that status.
- If validation commands or validation evidence are missing, verify and PR skills MUST NOT claim validation passed.
- If a user explicitly provides a path that conflicts with governance, safety, schema, or security constraints, the skill MUST report the conflict and not silently prefer the path.
- If a customer project has local specs or governance files, skills MUST treat them as project-local inputs and MUST NOT infer they are RigorLoop repository originals.

## Compatibility and migration

- Existing RigorLoop repository workflows remain valid in RigorLoop repository mode.
- Customer projects without `docs/workflows.md` remain supported through portable defaults and ambiguity blocking.
- Existing customer projects with local `docs/workflows.md` may continue using it as the local artifact-location guide.
- Generated adapter packages remain generated from canonical skill source.
- No CLI feature, workflow YAML, generated workflow docs, or status/validate command behavior changes are introduced by this spec.
- Rollback is limited to reverting canonical skill wording, workflow guidance, validator checks, reports, and generated-output validation changes from the first slice.

## Observability

- Static validation results MUST name the checked command and result.
- Static token measurement MUST record before/after totals for touched skills and total public skill delta.
- Dynamic benchmark reports MUST summarize broad searches, full-file reads, largest command output, input tokens, result-quality status, and any attempted dependency on absent RigorLoop internals.
- Generated adapter validation evidence MUST name the generation output location and validation command result.

## Security and privacy

- Skills MUST NOT ask customer projects to expose secrets, private keys, tokens, private repository metadata, or unrelated machine-local paths to satisfy this portability contract.
- Dynamic benchmark fixtures MUST avoid real customer secrets and SHOULD use synthetic data.
- Public skill text MUST NOT expose repository-maintainer-only implementation details such as internal generator paths, selector constraints, shared-block mechanics, or drift-check implementation mechanics.

## Accessibility and UX

No user interface is involved.

## Performance expectations

- Static validation MUST remain narrow and phrase/path based rather than broad semantic scoring.
- Dynamic benchmarks SHOULD be targeted to the first-slice scenarios and MUST NOT require the full release benchmark suite.
- Skills SHOULD prefer bounded evidence, targeted headings, stable IDs, path lists, counts, diffs, and short excerpts before broad reads.

## Edge cases

EC1. Customer project lacks `docs/workflows.md`: use a portable default if safe; otherwise block on ambiguity.

EC2. Customer project has local `CONSTITUTION.md`: treat it as project-local governance when relevant; do not treat it as the RigorLoop repository constitution.

EC3. Customer project has local `specs/`: use relevant local specs when present; do not broad-search for RigorLoop internal specs.

EC4. User asks to edit RigorLoop itself: repository-mode access to RigorLoop internal docs is allowed when relevant.

EC5. Direct file target is a RigorLoop internal doc path: the skill may read that file because it is the task target.

EC6. `project-map` runs in a sparse repository: continue from available local files and record missing orientation inputs when needed.

EC7. Review recording root cannot be selected: report recording blocked instead of inventing `docs/changes/<change-id>/`.

EC8. Static check sees `docs/workflows.md when present`: allow it.

EC9. Static check sees `must read RigorLoop CONSTITUTION.md`: fail it.

EC10. `code-review` audit finds no direct required internal-doc dependency: leave `code-review` unchanged.

EC11. `code-review` audit finds a direct required RigorLoop-internal dependency: include the minimal rewrite and add the optional `code-review-customer-diff-small` dynamic benchmark scenario.

EC12. Canonical public skills change but adapter generation tooling is unavailable locally: report the inability, do not hand-edit generated adapter bodies, and preserve the validation gap for review.

## Non-goals

- Do not copy full RigorLoop repository specs into customer projects.
- Do not make local `docs/workflows.md` mandatory for every skill invocation.
- Do not rewrite every public skill in one slice.
- Do not weaken safety-critical review, verification, material-finding, mutation-safety, or release-boundary rules.
- Do not implement `rigorloop status`, `rigorloop validate`, workflow YAML, generated workflow docs, or new CLI behavior.
- Do not introduce hard token gates.
- Do not run the full release benchmark suite unless a later artifact adds that scope.

## Acceptance criteria

- Proposal status is settled to `accepted` before this spec is relied on.
- `docs/workflows.md` receives concise customer-project portability guidance.
- `proposal`, `proposal-review`, `spec`, `plan`, `implement`, `workflow`, `verify`, `pr`, and `project-map` are audited and updated only where customer-project-risky wording is present.
- `code-review` remains unchanged unless direct required RigorLoop-internal dependency wording is found.
- Audit evidence identifies each touched skill and why it is touched.
- Migration evidence records removed or rewritten wording, why it is safe, and where essential behavior remains preserved.
- Static validation catches obvious required RigorLoop-internal document dependencies without blocking legitimate project-local docs/spec references.
- Static token before/after report is recorded at the required skills report path.
- Targeted customer-fixture dynamic benchmark is recorded for the required scenarios.
- Dynamic benchmark evidence shows public skills do not require RigorLoop repository-internal docs in customer projects.
- Canonical skill validation passes.
- Generated public adapter output validates from canonical skills when public skills change.
- No generated adapter skill body is hand-edited.
- No out-of-scope CLI, workflow YAML, generated workflow doc, hard token gate, full release benchmark, or broad skill rewrite work is added.

## Open questions

None.

The `code-review` first-slice treatment is a contingency rather than an open question: it remains unchanged unless audit evidence finds a direct required RigorLoop-internal document dependency.

## Next artifacts

```text
spec-review
plan
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Customer-portable public skills execution plan](../docs/plans/2026-05-18-customer-portable-public-skills.md)

## Readiness

Approved and ready for plan-review through the active execution plan.
