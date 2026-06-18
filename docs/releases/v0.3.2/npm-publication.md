# npm publication evidence for v0.3.2

Status: published

This file records the required live registry/download post-publish smoke contract. The pre-publish gate used the packed package; the post-publish rows record the externally observable `@xiongxianfei/rigorloop@0.3.2` package and matching GitHub release archives.

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
  sha256: "b43d56ba72425fe8fc16d93effa2bd5be1cf4fee7cba8dc7f9e08bd6b81b800b"
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
  published: true
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.2"

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
      - "sha256:85e8d06de1aeb7525148756fdae7bf9aa5a6052351eae6dbb1e21519c2bbfa30"
    file_counts:
      - "40"
    command_output_summary: "success; installed verified Codex target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
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
      - "sha256:9203601e3ddba1024d35a80e45598e73d7b8dfee0ed3017a340b5d0ee8c2316d"
    file_counts:
      - "40"
    command_output_summary: "success; installed verified Claude Code target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
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
      - ".opencode/skills=sha256:9203601e3ddba1024d35a80e45598e73d7b8dfee0ed3017a340b5d0ee8c2316d"
      - ".opencode/commands=sha256:5d43590ad9bb3ed5272b37aa0b8508f0ad3094c297b55726757e9048de49506b"
    file_counts:
      - ".opencode/skills=40"
      - ".opencode/commands=0"
    command_output_summary: "success; installed verified opencode target support with skills-only compatibility warning"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.2 init codex` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-codex-v0.3.2.zip` | `.agents/skills` | `sha256:85e8d06de1aeb7525148756fdae7bf9aa5a6052351eae6dbb1e21519c2bbfa30` | `40` | success; installed verified Codex target support | true | true | pass | none |
| claude | `npx @xiongxianfei/rigorloop@0.3.2 init claude` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-claude-v0.3.2.zip` | `.claude/skills` | `sha256:9203601e3ddba1024d35a80e45598e73d7b8dfee0ed3017a340b5d0ee8c2316d` | `40` | success; installed verified Claude Code target support | true | true | pass | none |
| opencode | `npx @xiongxianfei/rigorloop@0.3.2 init opencode` | `0.3.2` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.2/rigorloop-adapter-opencode-v0.3.2.zip` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=sha256:9203601e3ddba1024d35a80e45598e73d7b8dfee0ed3017a340b5d0ee8c2316d`; `.opencode/commands=sha256:5d43590ad9bb3ed5272b37aa0b8508f0ad3094c297b55726757e9048de49506b` | `.opencode/skills=40`; `.opencode/commands=0` | success; installed verified opencode target support with skills-only compatibility warning | true | true | pass | none |
