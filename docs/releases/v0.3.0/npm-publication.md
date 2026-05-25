# npm publication evidence for v0.3.0

Status: pending-publication

This file records the required live registry/download post-publish smoke contract. The pre-publish gate uses the packed package; the post-publish rows stay pending until `@xiongxianfei/rigorloop@0.3.0` and the matching GitHub release archives are externally observable.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.0"
  release_tag: "v0.3.0"
  source_commit: "02a9d7d6d514fc99908abf32898494dbbbae00c9"
  mode: "bootstrap"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: false
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.3.0.tgz"
  sha256: "pending"
  pack_command: "npm pack --prefix packages/rigorloop"
  content_check: "pass"
  smoke_result: "pass"

trusted_publishing:
  configured: true
  workflow: ".github/workflows/release.yml"
  id_token_write: true

bootstrap:
  used: false
  approving_maintainer: null
  publish_command: null

npm:
  published: false
  package_url: "pending"

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.0 init codex --json"
    npm_version: "0.3.0"
    temp_project: "pending"
    package_source: "npm registry"
    target: "codex"
    official_archive_url: "<pending public archive URL>"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "<pending live tree sha256>"
    file_counts:
      - "<pending live file count>"
    command_output_summary: "<pending live command output summary>"
    archive_sha256_verified: pending
    tree_hash_verified: pending
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke not run"
    post_publish_closeout_blocked: true
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.0 init claude --json"
    npm_version: "0.3.0"
    temp_project: "pending"
    package_source: "npm registry"
    target: "claude"
    official_archive_url: "<pending public archive URL>"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "<pending live tree sha256>"
    file_counts:
      - "<pending live file count>"
    command_output_summary: "<pending live command output summary>"
    archive_sha256_verified: pending
    tree_hash_verified: pending
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke not run"
    post_publish_closeout_blocked: true
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.0 init opencode --json"
    npm_version: "0.3.0"
    temp_project: "pending"
    package_source: "npm registry"
    target: "opencode"
    official_archive_url: "<pending public archive URL>"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - ".opencode/skills=<pending skills tree sha256>"
      - ".opencode/commands=<pending commands tree sha256>"
    file_counts:
      - ".opencode/skills=<pending skills file count>"
      - ".opencode/commands=<pending commands file count>"
    command_output_summary: "<pending live command output summary>"
    archive_sha256_verified: pending
    tree_hash_verified: pending
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke not run"
    post_publish_closeout_blocked: true
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.0 init codex` | `0.3.0` | npm registry | `<pending public archive URL>` | `.agents/skills` | `<pending live tree sha256>` | `<pending live file count>` | `<pending live command output summary>` | pending | pending | pending-publication | live post-publish smoke not run |
| claude | `npx @xiongxianfei/rigorloop@0.3.0 init claude` | `0.3.0` | npm registry | `<pending public archive URL>` | `.claude/skills` | `<pending live tree sha256>` | `<pending live file count>` | `<pending live command output summary>` | pending | pending | pending-publication | live post-publish smoke not run |
| opencode | `npx @xiongxianfei/rigorloop@0.3.0 init opencode` | `0.3.0` | npm registry | `<pending public archive URL>` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=<pending skills tree sha256>`; `.opencode/commands=<pending commands tree sha256>` | `.opencode/skills=<pending skills file count>`; `.opencode/commands=<pending commands file count>` | `<pending live command output summary>` | pending | pending | pending-publication | live post-publish smoke not run |
