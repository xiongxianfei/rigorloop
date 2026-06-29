# npm publication evidence for v0.3.4

Status: pending-publication

This file records the required live registry/download post-publish smoke contract. The pre-publish gate uses the packed package; the post-publish rows remain blocked until `@xiongxianfei/rigorloop@0.3.4` and matching GitHub release archives are externally observable.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.4"
  release_tag: "v0.3.4"
  source_commit: "4b8a03ed"
  mode: "trusted-publishing"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.3.4.tgz"
  sha256: "pending-publication"
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
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.4"

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init codex --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "pending npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-codex-v0.3.4.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "pending-publication"
    file_counts:
      - "pending-publication"
    command_output_summary: "pending live npm registry and GitHub release archive smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke"
    post_publish_closeout_blocked: true
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init claude --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "pending npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-claude-v0.3.4.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "pending-publication"
    file_counts:
      - "pending-publication"
    command_output_summary: "pending live npm registry and GitHub release archive smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke"
    post_publish_closeout_blocked: true
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init opencode --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "pending npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-opencode-v0.3.4.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - ".opencode/skills=pending-publication"
      - ".opencode/commands=pending-publication"
    file_counts:
      - ".opencode/skills=pending-publication"
      - ".opencode/commands=pending-publication"
    command_output_summary: "pending live npm registry and GitHub release archive smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live post-publish smoke"
    post_publish_closeout_blocked: true
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.4 init codex` | `0.3.4` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-codex-v0.3.4.zip` | `.agents/skills` | pending-publication | pending-publication | pending live npm registry and GitHub release archive smoke | false | false | pending-publication | live post-publish smoke |
| claude | `npx @xiongxianfei/rigorloop@0.3.4 init claude` | `0.3.4` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-claude-v0.3.4.zip` | `.claude/skills` | pending-publication | pending-publication | pending live npm registry and GitHub release archive smoke | false | false | pending-publication | live post-publish smoke |
| opencode | `npx @xiongxianfei/rigorloop@0.3.4 init opencode` | `0.3.4` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-opencode-v0.3.4.zip` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=pending-publication`; `.opencode/commands=pending-publication` | `.opencode/skills=pending-publication`; `.opencode/commands=pending-publication` | pending live npm registry and GitHub release archive smoke | false | false | pending-publication | live post-publish smoke |
