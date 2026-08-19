# Risk-To-Check Map

This reference is the sole semantic owner of `changed path -> material risk -> owned check -> authoritative command -> required execution boundary`. GitHub authoring serializes the settled result and cannot redefine it.

Unmapped changed surfaces are not no-risk surfaces. Stop for reviewer judgment, route to a conservative boundary check, or both. Missing, stale, incomplete, or conflicting command and placement evidence blocks coverage-sensitive work.

## Portable core

| Changed surface | PR check | Boundary check | Notes |
| --- | --- | --- | --- |
| workflow files | syntax, permission, and filter review | configured full workflow validation | Treat triggers, credentials, and exclusions as security-sensitive. |
| dependency manifests or lockfiles | deterministic install and affected tests | configured audit/full validation | Cache only with a stable lockfile key. |
| source code | affected project-owned checks | full suite | Use authoritative commands only. |
| tests | changed tests and affected source checks | full suite | Test-only changes can alter coverage. |
| generated files | configured drift check | configured full generation | Do not invent generation commands. |
| documentation | configured docs checks | configured full docs validation | Documentation may still be executable. |
| package or release metadata | configured package checks | release verification | Publishing needs separate design. |
| environment or secrets-adjacent config | conservative review and available lint | protected boundary validation | Never expose secrets to untrusted forks. |

## Project-specific extensions

| Project surface | Example PR check | Example boundary check | Notes |
| --- | --- | --- | --- |
| RigorLoop skills | skill validation | generated package parity | Example only; non-RigorLoop projects do not need this. |
| RigorLoop adapters | metadata/package checks | archive validation | Example only. |

Record every changed surface, material risk, command source, owned check, required boundary, intentionally deferred check, and unresolved mapping.
