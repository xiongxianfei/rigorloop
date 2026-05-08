## Generated-output handling

Contributor-maintenance guidance only. Do not copy this block into published skills.

Edit canonical skill source under `skills/<skill>/SKILL.md`.
Do not hand-edit `.codex/skills/` or `dist/adapters/`.
Regenerate generated outputs from canonical source.
Validate drift with repository-owned checks.
Use concrete generated adapter file paths in selector-driven validation; do not pass `--path dist/adapters`.
Generated outputs are proof surfaces, not independent sources of truth.
Shared blocks are copied into skills and checked for drift; they are not generated into skills in v1.
