# Spec Revision R1 Evidence: Workflow Skill Simplification

## Finding resolved

`WFSIM-SR1` is addressed by adding `WPS-stateless-automation-command` as the seventh valid assembly.

The revision:

- reserves `WPS` for `status` or `off` with no selected change and no active run;
- keeps `WPB` limited to new-target bootstrap that must establish governed identity;
- requires `WPS` to load only `SKILL.md` and the automation reference;
- preserves `no-active-run` and prohibits state creation;
- updates measurement and static-fixture coverage;
- updates the input boundary, example ownership, invariants, edge case, and acceptance mapping.

No lifecycle, automation persistence, command, or authority behavior changed from the accepted proposal.
