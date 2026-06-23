# Code Review M2 R3

Review ID: code-review-m2-r3
Stage: code-review
Round: 3
Reviewer: Codex code-review
Target: commit `c5655e7`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r3.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M2-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r3.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M2-CR3
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `c5655e7` (`Resolve per-reference resource lint review`).
- Tracked governing branch state: accepted proposal, approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, active plan, M1 audit and review, M2 R1/R2 reviews, accepted SRI-M2-CR1/SRI-M2-CR2 review-resolutions, and M2 R3 implementation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R49-R49d; `specs/skill-contract.test.md` T43; `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md` M2; `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md#code-review-m2-r2`.
- Validation evidence: M2 R3 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`, active plan validation notes, and direct reviewer fixture output recorded below.
- Implementation files reviewed: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/validator-fixtures.md`, active plan state, review-resolution, review log, and change metadata.

## Diff summary

The SRI-M2-CR2 resolution changes legacy skill-local resource linting to keep each matched resource path's span and evaluate external or illustrative context per reference. It adds paragraph-level instruction assembly so a resource-loading instruction split across adjacent lines can be evaluated as one instruction, tightens temporary architecture migration exceptions to skill, path, and instruction text, adds mixed-reference and individually qualified reference tests, and updates lifecycle evidence so M2 returns to code-review.

## Findings

## Finding SRI-M2-CR3

Finding ID: SRI-M2-CR3
Severity: major
Location: `scripts/skill_validation.py:953`; `scripts/skill_validation.py:1568`; `scripts/test-skill-validator.py:1031`
Evidence: T43 requires the bounded legacy lint to catch resource-loading references without becoming a broad Markdown path scanner, and it specifically protects artifact examples, code snippets, repository docs paths, and generated-artifact strings from false positives. The new `_iter_resource_instruction_lines` joins every contiguous nonblank non-heading line into one instruction. `_iter_unmapped_skill_local_resource_references` then applies any resource-loading verb found anywhere in that joined instruction to every resource-looking path in the joined block. A direct review fixture with two separate Markdown list items failed validation:

```md
- Use the user-provided references/external.md.
- The generated artifact may contain the string templates/architecture.md.
```

The validator reported:

```text
unmapped skill-local resource reference `templates/architecture.md`
```

That path is an artifact string, not an operative resource-loading instruction. The added mixed-line tests prove split continuation cases but do not cover adjacent independent list items, so the false-positive boundary regressed.
Required outcome: Preserve CR2's per-reference context behavior for genuine multi-line resource instructions while preventing a resource-loading verb in one Markdown instruction or list item from making a separate artifact/example path in another instruction operative.
Safe resolution path: Change instruction assembly so it only joins true continuation lines, or otherwise segments Markdown list items and independent instructions before applying `LEGACY_RESOURCE_LOADING_CONTEXT_PATTERN`. Add a regression where an external resource load list item followed by a generated-artifact or example path list item passes, while the existing CR2 split-continuation mixed-reference fixtures still fail for the unqualified path. Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selector-selected validation, generated-skill regression if selected, lifecycle validation, review artifact validation, change metadata validation, and `git diff --check --`.
needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. The per-reference ownership rule is implemented, but the paragraph assembly now violates T43's false-positive boundary for independent Markdown instructions.
- Test coverage: concern. CR2 mixed-reference tests cover wrapped instructions, reverse order, individual qualification, and illustrative plus operative paths on one line, but not adjacent list items where only one item contains a loading verb.
- Edge cases: concern. A generated-artifact or example path in a separate list item can be misclassified when the prior list item contains a loading verb.
- Error handling: pass. Existing mapped-resource diagnostics and failure behavior remain actionable.
- Architecture boundaries: pass. The diff does not normalize architecture resources, package outputs, or installed trees before M3.
- Compatibility: concern. Contributors could be forced to rewrite valid example/generated-artifact wording in published skills because of false-positive linting.
- Security/privacy: pass. No secrets, credentials, private hostnames, or unsafe logging were introduced.
- Derived artifact currency: pass. No generated adapter output was hand-edited; `python scripts/test-build-skills.py` was rerun as selected validation.
- Unrelated changes: pass. The diff is limited to validator behavior, validator tests, fixture evidence, and lifecycle/review state.
- Validation evidence: concern. Recorded validation commands are relevant and passed, but direct reviewer proof shows an untested false-positive path.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRI-M2-CR3`
Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
Verify readiness: not-claimed

This direct `code-review` invocation stops after recording the review result and lifecycle state. It does not apply the fix.
