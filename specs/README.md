# Specs

Current design-authoring and composition navigation: [Design](../docs/design/skill/authoring/design.md) owns unified authoring, model conventions and validation mapping; [System](../docs/design/system.md) owns the bounded composition view. Canonical `skills/design/` replaces the two old authors; remaining specs, Level 2 architecture and ADR responsibilities retain their declared contracts. Historical inventories below do not establish the current public author list.

Use this directory only for behavior-changing work that benefits from an explicit contract.

- `specs/<feature>.md` describes the user-visible or system-visible behavior.
- `specs/<feature>.test.md` maps requirements and edge cases to tests.

Do not create specs for every tiny change. Use them when they help humans and Codex stay aligned.
