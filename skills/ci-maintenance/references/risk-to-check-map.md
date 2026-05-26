# Risk-To-Check Map

Use this reference to derive CI checks from changed surfaces. Adapt it to the project. The portable core is safe to consider in ordinary repositories; project-specific extensions apply only when the target project has the named surface.

Unmapped changed surfaces are not no-risk surfaces. If a changed path does not match this map, flag it for reviewer judgment, route it to a conservative boundary check, or both.

## Portable core

| Changed surface | PR check | Boundary check | Notes |
| --- | --- | --- | --- |
| workflow files | workflow syntax, lint, permission review, path-filter review | scheduled or manual full workflow validation | Treat trigger, token, secret, and path-filter changes as security-sensitive. |
| dependency manifests or lockfiles | deterministic install and affected tests with lockfile-keyed cache if caching is used | dependency audit or scheduled dependency validation when configured | Omit caching when no stable invalidation key exists. |
| source code | affected unit, component, or package checks from known project commands | full suite | Derive affected checks from changed paths and project conventions. |
| tests | changed tests and affected source checks | full suite | Test-only changes can still reveal affected source behavior. |
| generated files | generated-output drift check when configured | full generated-output validation | Do not invent generation commands. |
| documentation | link, structure, spell, or docs build checks when configured | full docs validation when configured | Docs-only does not mean no checks if docs tooling exists. |
| package or release metadata | package validation and smoke checks when configured | release verification when relevant | Release publishing and deployment templates need separate design. |
| container, environment, or secrets-adjacent config | reviewer flag plus available config lint or smoke check | conservative boundary validation | Use this row for common surfaces that are easy to miss; avoid secrets in PR workflows from forks. |

## Project-specific extensions

Use these only when the project has the corresponding surface.

| Project surface | Example PR check | Example boundary check | Notes |
| --- | --- | --- | --- |
| RigorLoop skills | skill validation | generated local skill mirror validation | Example only; non-RigorLoop projects do not need this. |
| RigorLoop generated adapters | adapter metadata or packaging checks | generated adapter archive validation | Example only; do not require adapter tooling in adopter projects. |
| repository validators | validator unit tests and affected lifecycle validation | broad smoke through the repository validation wrapper | Example only; use project-owned commands. |
| release metadata | package or release-note validation | release verification | Add release triggers only when the workflow owns release validation or packaging. |

## Review use

For each changed surface, record:

- PR coverage;
- boundary coverage;
- command source;
- intentionally deferred checks;
- unmapped surfaces and reviewer judgment needed.
