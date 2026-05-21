# Skill-Contract Sufficiency Assessment

Date: 2026-05-21
Milestone: M1
Status: sufficient

## Scope

This assessment covers whether `specs/skill-contract.md` is sufficient authority for review-family assets, parser-conformance checks, and generated-output asset presence before first-slice review skill edits begin.

## Assessment

`specs/skill-contract.md` is sufficient for M1 to proceed under the approved review-family spec and active test spec.

The existing skill contract already covers:

- packaged `assets/` as skill-local resources;
- `COPY` resource-map usage for copy-and-fill templates;
- metadata, placeholder, and maintained-alongside expectations through the existing asset rollout pattern;
- canonical `skills/` as authored source;
- generated output as derived from canonical skill sources rather than hand-edited source.

The review-family spec adds the feature-specific contract for:

- the first-slice review skills;
- parser-owned material-finding labels;
- byte-identical material-finding parser-owned field blocks;
- review-class asset policy boundaries;
- valid and invalid material-finding fill proof;
- no severity-enum validation in this slice.

Those feature-specific rules can be implemented as validator coverage under the approved spec and test spec without a `specs/skill-contract.md` amendment.

## Result

No skill-contract amendment packet is required before M2 skill edits.

If later milestones need build-time partials, packaged references, packaged scripts, or a broader generated-output contract, that is outside this slice and must return to proposal/spec.

## Validation

- `python scripts/test-skill-validator.py`: pass
- `python scripts/test-review-artifact-validator.py`: pass
- `python scripts/validate-skills.py`: pass
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`: pass
- `git diff --check --`: pass
