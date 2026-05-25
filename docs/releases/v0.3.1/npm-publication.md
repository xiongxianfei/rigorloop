# npm publication evidence for v0.3.1

Status: published

This file records the required live registry/download post-publish smoke contract. The pre-publish gate used the packed package; the post-publish rows record the externally observable `@xiongxianfei/rigorloop@0.3.1` package and matching GitHub release archives.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.1"
  release_tag: "v0.3.1"
  source_commit: "ffe9a6d0622b8cd97fee535bae245250f93cfc8c"
  mode: "trusted-publishing"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.3.1.tgz"
  sha256: "083b785795ddf088e8340a70508c14f67d0a78a711c0e9bc710016d58b15f0f6"
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
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.1"

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.1 init codex --json"
    npm_version: "0.3.1"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-codex-v0.3.1.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "sha256:d7ad8380f749131a3202686fab3efa3ee701eb68fa36a1a03c4c16163867a55e"
    file_counts:
      - "38"
    command_output_summary: "success; installed verified Codex target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.1 init claude --json"
    npm_version: "0.3.1"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-claude-v0.3.1.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "sha256:5e267126b3caca13c7590ba77365d5212b7d5e671a041aec7a7eaa7a9868061d"
    file_counts:
      - "38"
    command_output_summary: "success; installed verified Claude Code target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.1 init opencode --json"
    npm_version: "0.3.1"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-opencode-v0.3.1.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - ".opencode/skills=sha256:5e267126b3caca13c7590ba77365d5212b7d5e671a041aec7a7eaa7a9868061d"
      - ".opencode/commands=sha256:5d43590ad9bb3ed5272b37aa0b8508f0ad3094c297b55726757e9048de49506b"
    file_counts:
      - ".opencode/skills=38"
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
| codex | `npx @xiongxianfei/rigorloop@0.3.1 init codex` | `0.3.1` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-codex-v0.3.1.zip` | `.agents/skills` | `sha256:d7ad8380f749131a3202686fab3efa3ee701eb68fa36a1a03c4c16163867a55e` | `38` | success; installed verified Codex target support | true | true | pass | none |
| claude | `npx @xiongxianfei/rigorloop@0.3.1 init claude` | `0.3.1` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-claude-v0.3.1.zip` | `.claude/skills` | `sha256:5e267126b3caca13c7590ba77365d5212b7d5e671a041aec7a7eaa7a9868061d` | `38` | success; installed verified Claude Code target support | true | true | pass | none |
| opencode | `npx @xiongxianfei/rigorloop@0.3.1 init opencode` | `0.3.1` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.1/rigorloop-adapter-opencode-v0.3.1.zip` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=sha256:5e267126b3caca13c7590ba77365d5212b7d5e671a041aec7a7eaa7a9868061d`; `.opencode/commands=sha256:5d43590ad9bb3ed5272b37aa0b8508f0ad3094c297b55726757e9048de49506b` | `.opencode/skills=38`; `.opencode/commands=0` | success; installed verified opencode target support with skills-only compatibility warning | true | true | pass | none |
