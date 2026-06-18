# npm publication evidence for v0.3.2

Status: pending-publication

This file records the required live registry/download post-publish smoke contract. The pre-publish gate uses the packed package; the post-publish rows must record the externally observable `@xiongxianfei/rigorloop@0.3.2` package and matching GitHub release archives after publication.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.2"
  release_tag: "v0.3.2"
  source_commit: "93903a0"
  mode: "trusted-publishing"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.3.2.tgz"
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
    command: "npx @xiongxianfei/rigorloop@0.3.2 init codex --json"
    npm_version: "0.3.2"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-codex-v0.3.2.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "pending"
    file_counts:
      - "pending"
    command_output_summary: "pending post-publish live registry/download smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "post-publish live registry/download smoke"
    post_publish_closeout_blocked: true
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.2 init claude --json"
    npm_version: "0.3.2"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-claude-v0.3.2.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "pending"
    file_counts:
      - "pending"
    command_output_summary: "pending post-publish live registry/download smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "post-publish live registry/download smoke"
    post_publish_closeout_blocked: true
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.2 init opencode --json"
    npm_version: "0.3.2"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-opencode-v0.3.2.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - "pending"
    file_counts:
      - "pending"
    command_output_summary: "pending post-publish live registry/download smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "post-publish live registry/download smoke"
    post_publish_closeout_blocked: true
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.2 init codex` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-codex-v0.3.2.zip` | `.agents/skills` | pending | pending | pending post-publish live registry/download smoke | false | false | pending-publication | post-publish live registry/download smoke |
| claude | `npx @xiongxianfei/rigorloop@0.3.2 init claude` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-claude-v0.3.2.zip` | `.claude/skills` | pending | pending | pending post-publish live registry/download smoke | false | false | pending-publication | post-publish live registry/download smoke |
| opencode | `npx @xiongxianfei/rigorloop@0.3.2 init opencode` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-opencode-v0.3.2.zip` | `.opencode/skills`; `.opencode/commands` | pending | pending | pending post-publish live registry/download smoke | false | false | pending-publication | post-publish live registry/download smoke |
