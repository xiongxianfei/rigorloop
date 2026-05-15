# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/rigorloop-cli-package-and-codex-init.md
Reviewed artifact: specs/rigorloop-cli-package-and-codex-init.md
Review date: 2026-05-15
Recording status: recorded
Status: changes-requested

## Scope

Reviewed the draft first-slice CLI package and Codex init contract against the accepted scaffolding CLI proposal, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `docs/project-map.md`, the current adapter release-archive ADR, and related adapter packaging specs.

The review focused on whether the spec is precise enough for architecture, test-spec, and implementation without guessing. No implementation code was reviewed.

## Dimension Results

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | block | Local archive metadata input, generated `rigorloop.yaml` structure, and exit-code behavior for expected verification failures are ambiguous. |
| Normative language | concern | Most requirements use normative language correctly, but `R50`, `R57`/`R59`, and the error-boundary section leave conditional behavior too open for a public command contract. |
| Completeness | concern | Normal, dry-run, overwrite, archive traversal, and lockfile boundaries are covered, but offline/local archive verification and config file shape are incomplete. |
| Testability | block | Tests cannot assert local archive verification, generated manifest shape, or checksum/tree-hash exit codes without adding behavior not present in the spec. |
| Examples | pass | Examples are concrete and aligned with the intended first slice. |
| Compatibility | concern | The additive rollout and no-publication boundary are clear, but `latest` compatibility and existing `rigorloop.yaml` merge/update behavior need later tightening. |
| Observability | pass | Human and JSON output surfaces, warnings, diagnostics, and verification-step errors are described. |
| Security/privacy | concern | Archive traversal and network limits are covered, but local archive metadata trust is underspecified. |
| Non-goals | pass | Exclusions for `new-change`, `status`, `validate`, lockfile writes, workflow YAML, npm publication, and non-Codex adapters are explicit. |
| Acceptance criteria | concern | Acceptance criteria are observable except for the parts depending on unspecified metadata source, config shape, and exit code semantics. |

## Findings

### SR1-F1: `--from-archive` cannot be implemented offline without a metadata input contract

Finding ID: SR1-F1

Severity: major

Location: `specs/rigorloop-cli-package-and-codex-init.md:177`, `specs/rigorloop-cli-package-and-codex-init.md:235`, `specs/rigorloop-cli-package-and-codex-init.md:337`

Evidence: `R24` defines `--from-archive <path>` as local archive installation mode, and `R50` requires local archive installation to verify against official or explicitly supplied release metadata before extraction. The inputs list includes an optional local archive path and official GitHub release metadata, but it does not define any command option, sidecar filename convention, metadata path, metadata hash input, or offline trust rule for explicitly supplied metadata. Example E5 also says the command verifies against "provided or discovered official metadata," but the spec never says how metadata is provided.

Required outcome: The spec must define the observable metadata source contract for `--from-archive`, including whether local archive mode requires network metadata, accepts a metadata file option, discovers a sidecar metadata file, or blocks when metadata is unavailable.

Safe resolution path: Add a small input contract such as `--metadata <path>` for local archive metadata, define its required hash or trust behavior, and state that offline `--from-archive` blocks when neither verified sidecar metadata nor explicit metadata is available. Alternatively, remove the offline implication and require network metadata for `--from-archive`, but then update examples and failure behavior accordingly.

### SR1-F2: The generated `rigorloop.yaml` public shape is not specified

Finding ID: SR1-F2

Severity: major

Location: `specs/rigorloop-cli-package-and-codex-init.md:191`, `specs/rigorloop-cli-package-and-codex-init.md:195`, `specs/rigorloop-cli-package-and-codex-init.md:197`, `specs/rigorloop-cli-package-and-codex-init.md:199`

Evidence: `R30` requires actual init to create `rigorloop.yaml`, while `R32` through `R34` require it to record `schema_version: 1`, selected adapter `codex`, install root `.agents/skills`, and archive source. The spec does not define the YAML object shape, keys, nesting, or required example output. Because `rigorloop.yaml` is a public config surface, architecture and tests would have to invent the structure.

Required outcome: The spec must define the minimum generated `rigorloop.yaml` shape for this first slice, including exact keys and values that tests can assert.

Safe resolution path: Add a normative minimal YAML example and requirement such as:

```yaml
schema_version: 1
adapters:
  - name: codex
    install_root: .agents/skills
    source:
      type: release-archive
      version: v0.1.3
```

If validation command placeholders remain out of scope, state that first-slice generated `rigorloop.yaml` must not include `validation.commands`; otherwise define the exact inactive/example shape.

### SR1-F3: Expected archive verification failures conflict with the exit-code contract

Finding ID: SR1-F3

Severity: major

Location: `specs/rigorloop-cli-package-and-codex-init.md:142`, `specs/rigorloop-cli-package-and-codex-init.md:280`, `specs/rigorloop-cli-package-and-codex-init.md:365`, `specs/rigorloop-cli-package-and-codex-init.md:370`

Evidence: `R12` reserves exit code `1` for internal or unexpected errors and exit code `3` for validation failed. `R60` says checksum mismatch, size mismatch, tree-hash mismatch, invalid metadata hash, or path traversal must produce status `error`. The boundary section then says those expected verification failures exit `1` with status `error` unless a later test spec adopts a narrower validation-failed code. These are not internal unexpected errors; they are expected adapter/archive validation failures.

Required outcome: The spec must define one stable exit-code mapping for expected metadata/archive verification failures before test-spec or implementation.

Safe resolution path: Map checksum mismatch, size mismatch, tree-hash mismatch, invalid metadata hash, and archive traversal to exit code `3` with status `error`, or explicitly redefine exit code `1` to include expected security verification failures. The safer public CLI contract is to keep `1` for internal/unexpected errors and use `3` for verification failures.

## Requirement Notes

- `R28` uses "compatible official release" for `latest` without defining compatibility. This is not a material blocker if the first implementation path tests pinned/local versions first, but the spec should eventually define whether `latest` resolves to the package's concrete installed version, a metadata compatibility range, or the latest GitHub release tag.
- Existing valid `rigorloop.yaml` behavior is described as "reports it as existing" in edge case 1, but the spec should later decide whether a valid file missing the Codex adapter is updated, blocked, or left unchanged.

## Recommendation

Request changes before architecture, test-spec, or implementation rely on this spec.

Immediate next repository stage: spec revision.

Eventual test-spec readiness: not-ready until `SR1-F1`, `SR1-F2`, and `SR1-F3` are resolved and spec-review reruns.

Stop condition: public CLI configuration and archive verification contracts are not yet precise enough for downstream test-spec or implementation.
