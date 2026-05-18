# Spec Review R1: Multi-Adapter Init and Proxy-Aware Adapter Download

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/multi-adapter-init-and-proxy-aware-download.md
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `SR1-F1`, `SR1-F2`, `SR1-F3`, `SR1-F4`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-log.md`
- Review resolution: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/review-resolution.md`
- Open blockers: spec contract gaps must be resolved before architecture, planning, test-spec, or implementation relies on this spec
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready

## Scope

Reviewed spec:

- `specs/multi-adapter-init-and-proxy-aware-download.md`

Related evidence:

- `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- `specs/rigorloop-cli-package-and-codex-init.md`
- `specs/rigorloop-cli-lockfile.md`

This review is isolated. It does not automatically hand off to architecture, planning, test-spec, or implementation.

## Findings By Severity

### SR1-F1 - opencode older-archive behavior conflicts with required multi-root lockfile shape

Finding ID: SR1-F1
Severity: blocking
Location: `MAI-R14`, `MAI-R40` through `MAI-R45`, `MAI-R51`, `MAI-R62` through `MAI-R64`, schema v2 example
Evidence: The spec says opencode descriptor roots are both `.opencode/skills` and `.opencode/commands`; opencode command aliases are installed when metadata declares them; older opencode archives lacking command-alias metadata may install without `.opencode/commands`; opencode lockfile entries must use `installed_roots` and `root_hashes`; multi-root entries must not use top-level `tree_sha256` or `file_count`. It does not define the `rigorloop.yaml` or `rigorloop.lock` shape when an older opencode archive installs skills only.
Required outcome: Define whether `.opencode/commands` is required, optional, or omitted for older opencode archives, and define the exact manifest and lockfile shape for that case.
Safe resolution path: Add explicit requirements that descriptor roots are possible roots, while trusted metadata determines required roots. For older opencode archives without command-alias metadata, either:
- block installation until command metadata exists; or
- allow skills-only installation with `installed_roots.skills` and `root_hashes.skills` only, omit `commands`, emit a stable warning code, and ensure `rigorloop.yaml` does not record `.opencode/commands`.

### SR1-F2 - `rigorloop.yaml` merge and conflict behavior is underspecified

Finding ID: SR1-F2
Severity: major
Location: `MAI-R47` through `MAI-R54`, Edge case 1
Evidence: The spec requires creating `rigorloop.yaml` when absent and recording each selected adapter and its roots. Edge case 1 says adding Claude Code updates or plans the adapter list without removing Codex. The spec does not define the `rigorloop.yaml` adapter shape for single-root versus multi-root adapters, whether `install_root` or `install_roots` is used, how existing adapter entries are matched or updated, what happens with duplicate adapter entries, or how unknown or malformed existing manifest fields are handled.
Required outcome: Define a testable manifest shape and update policy for adding or reinstalling adapters.
Safe resolution path: Add a `rigorloop.yaml` schema example and requirements for:
- single-root entries using `install_root`;
- multi-root entries using `install_roots`;
- updating only the selected adapter entry after verification;
- preserving unrelated valid adapter entries;
- blocking on duplicate selected adapter entries, malformed adapters, unsupported manifest schema, or unknown manifest fields that cannot be safely preserved.

### SR1-F3 - Trusted metadata shape is too vague for multi-root verification

Finding ID: SR1-F3
Severity: major
Location: `MAI-R20`, `MAI-R21`, `MAI-R34` through `MAI-R37`, `MAI-R40` through `MAI-R44`
Evidence: The spec says trusted metadata must include "expected tree hash data" and command alias paths, and the CLI must compare computed installed tree hashes to trusted metadata. It does not define exact metadata fields for single-root versus multi-root adapters, where per-root file counts live, how declared command aliases are represented, or how the CLI detects "older opencode archive" metadata that lacks command aliases.
Required outcome: Define the minimum trusted metadata contract needed by the CLI for all supported adapters.
Safe resolution path: Add a normative metadata shape or field list:
- single-root adapters include `install_root`, `tree_sha256`, and `file_count`;
- multi-root adapters include `install_roots` and `root_hashes` keyed by root role;
- opencode command aliases include a `command_aliases` section with count and exact paths when aliases are declared;
- absence of `command_aliases.opencode` is the only older-archive signal, and only for release ranges the spec allows.

### SR1-F4 - Proxy diagnostic fields are not precise enough for tests

Finding ID: SR1-F4
Severity: major
Location: `MAI-R77`, `MAI-R79` through `MAI-R84`, Observability
Evidence: The spec requires "download failure class", detected proxy-related environment variable names, and Node env-proxy support status, but it does not define allowed failure class values, which environment variable names are in scope, or the allowed status values for Node env-proxy support. `MAI-R82` allows reporting support status "when it can be determined without guessing", which leaves test authors and implementation to infer expected behavior.
Required outcome: Define stable diagnostic fields and allowed values.
Safe resolution path: Add explicit diagnostic enums or bounded values, for example:
- `proxy_env_vars_detected`: names only from `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `http_proxy`, `https_proxy`, `no_proxy`;
- `node_env_proxy_status`: `enabled`, `disabled`, `unsupported`, or `unknown`;
- `download_failure_class`: `dns`, `tls`, `timeout`, `http-status`, `proxy`, `network`, or `unknown`;
- `archive_url`: trusted public archive URL only.
Require JSON tests to assert these stable values while human output may remain concise.

## Review Dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | Most requirements are clear, but opencode older-archive and proxy diagnostics leave multiple interpretations. |
| Normative language | pass | Normative keywords are generally used correctly. |
| Completeness | concern | Manifest merge behavior, metadata shape, optional opencode commands, and proxy diagnostic values are incomplete. |
| Testability | concern | Many requirements are testable, but SR1-F3 and SR1-F4 need exact data contracts before tests can be unambiguous. |
| Examples | concern | Examples cover current direction but do not cover older opencode archives or manifest merge conflicts. |
| Compatibility | concern | Schema v1 lockfile compatibility is covered; manifest compatibility and old opencode archive shape need clearer rules. |
| Observability | concern | Output categories are defined, but proxy diagnostic fields need stable values. |
| Security/privacy | pass | Sensitive proxy and path data exclusions are explicit. |
| Non-goals | pass | Scope exclusions are explicit, including Undici dispatcher deferral. |
| Acceptance criteria | concern | Acceptance criteria are observable but depend on unresolved metadata and manifest shape details. |

## Requirement Notes

- `MAI-R44` is reasonable as a compatibility direction, but it needs paired lockfile and manifest requirements for skills-only opencode installs.
- `MAI-R48` through `MAI-R54` need concrete shape and update semantics, not only "record" language.
- `MAI-R20` should stop at a precise metadata shape rather than "expected tree hash data".
- `MAI-R80` through `MAI-R82` need stable diagnostic field values for hermetic tests.

## Exact Wording Suggestions

Suggested `rigorloop.yaml` direction:

```yaml
adapters:
  - name: codex
    install_root: ".agents/skills"
  - name: opencode
    install_roots:
      skills: ".opencode/skills"
      commands: ".opencode/commands"
```

Suggested older opencode lockfile direction:

```yaml
installed_roots:
  skills: ".opencode/skills"
root_hashes:
  skills:
    tree_sha256: "<sha256>"
    file_count: 23
```

Suggested proxy diagnostic values:

```text
node_env_proxy_status: enabled | disabled | unsupported | unknown
download_failure_class: dns | tls | timeout | http-status | proxy | network | unknown
```

## Blocking Questions

- Does the spec want to support older opencode archives without command alias metadata as skills-only installs, or should the CLI block those archives for this new init surface?
- Should `rigorloop.yaml` use `install_root` for single-root adapters and `install_roots` for multi-root adapters, mirroring the lockfile distinction?

## Readiness

Review status: changes-requested.

Immediate next repository stage: spec revision.

Eventual `test-spec` readiness: not-ready until the findings above are resolved.
