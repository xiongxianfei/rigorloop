# Skill Asset Design

[Skill](../../design/skill/skill.md) owns current packaged-resource requirements. This topic preserves a design lesson, not additional template policy.

## 2026-05-20: Require Assets To Earn Their File

- Source session: `docs/learn/sessions/2026-05-20-spec-family-asset-formalism.md`
- Primary classification: `durable-lesson`
- Secondary routes: `7ad33e1b1827c84dfa4e9fbbfc8b52a204b5139e:specs/spec-family-assets-progressive-disclosure.md`; `docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md`; `scripts/skill_validation.py`

Packaged skill assets should be substantial copy-and-fill structures, not ceremony around tiny row formats.

The spec-family asset pass showed the boundary:

- full skeleton assets can earn a file because they move real structure out of the common path;
- multi-field blocks can earn a file when field order or completeness is easy to get wrong;
- one-line rows usually do not earn a file when `SKILL.md` already carries the format rule.

Use the metadata-to-content ratio as a smell test. If the required metadata header is larger than the template body, keep the format inline unless the plan records a specific exception.

Do not treat multi-instance use as sufficient by itself. Multi-instance plus trivial shape still creates drift surface and formalism. Multi-instance plus substantial, error-prone shape is the stronger asset case.
