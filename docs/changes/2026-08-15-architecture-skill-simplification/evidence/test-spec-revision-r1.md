# Test-Spec Revision Evidence R1: Architecture Skill Simplification

- Stage: test-spec
- Date: 2026-08-15
- Artifact ID: `test-spec`
- Artifact: `specs/architecture-skill-simplification.test.md`
- Prior reviewed revision: `9be51238`
- Authorizing findings: `ARSIM-TSR1`, `ARSIM-TSR2`
- Revision status: complete

The revision adds direct AC1 through AC10 traceability to stable cases, commands, and milestone timing. It also replaces the nonexistent underscored Python module invocation with `python scripts/test-skill-validator.py ArchitectureSkillSimplificationLedgerTests`, a planned M1 class executed by the same existing repository runner that the approved plan uses for focused M2 proof.

No requirement, boundary, interaction, test case, implementation milestone, feature behavior, architecture decision, or runtime acceptance mechanism changed. The revised proof map remains fully automated with no uncovered gap or manual procedure.
