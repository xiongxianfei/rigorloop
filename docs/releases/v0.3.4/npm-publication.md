# npm publication evidence for v0.3.4

Status: published

This file records the required live registry/download post-publish smoke contract. The pre-publish gate used the packed package; the post-publish rows passed after `@xiongxianfei/rigorloop@0.3.4` and matching GitHub release archives became externally observable.

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
  sha256: "4b2a1e0e4be0092bd4e3f1894557365735850b79a2adf3488b02ec68581f594e"
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
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.4"
  published_at: "2026-06-29T13:30:28.873Z"
  dist_tag_latest: "0.3.4"
  integrity: "sha512-dfA0vEMwDkhLwYPSVvdwUFie/JZ9+JTND7M5PJ8N4q54giHWWTfaNzuVlSI0DzJUGm0St523m6mzJb+F121NxA=="
  tarball: "https://registry.npmjs.org/@xiongxianfei/rigorloop/-/rigorloop-0.3.4.tgz"

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init codex --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-codex-v0.3.4.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "sha256:fc0e4030dd43e06995c780518d66d643867a1b24e858cc2a762740ea996faa17"
    file_counts:
      - "47"
    command_output_summary: "fresh npx init returned status success with verified Codex target support and no blockers"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init claude --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-claude-v0.3.4.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "sha256:5569b475074833b6a9f233e7e0e21ac2a84cd9fbc8be2d7df070c46cd183f589"
    file_counts:
      - "47"
    command_output_summary: "fresh npx init returned status success with verified Claude Code target support and no blockers"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.4 init opencode --json"
    npm_version: "0.3.4"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-opencode-v0.3.4.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - ".opencode/skills=sha256:5569b475074833b6a9f233e7e0e21ac2a84cd9fbc8be2d7df070c46cd183f589"
      - ".opencode/commands=sha256:b9beece61c967adf20cd12d9290849c7137f8b59032a2ec45d85a960869eaa30"
    file_counts:
      - ".opencode/skills=47"
      - ".opencode/commands=10"
    command_output_summary: "fresh npx init returned status success with verified opencode target support, command aliases installed, and no blockers"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.4 init codex --json` | `0.3.4` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-codex-v0.3.4.zip` | `.agents/skills` | `sha256:fc0e4030dd43e06995c780518d66d643867a1b24e858cc2a762740ea996faa17` | `47` | status success with verified Codex target support and no blockers | true | true | pass | none |
| claude | `npx @xiongxianfei/rigorloop@0.3.4 init claude --json` | `0.3.4` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-claude-v0.3.4.zip` | `.claude/skills` | `sha256:5569b475074833b6a9f233e7e0e21ac2a84cd9fbc8be2d7df070c46cd183f589` | `47` | status success with verified Claude Code target support and no blockers | true | true | pass | none |
| opencode | `npx @xiongxianfei/rigorloop@0.3.4 init opencode --json` | `0.3.4` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.4/rigorloop-adapter-opencode-v0.3.4.zip` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=sha256:5569b475074833b6a9f233e7e0e21ac2a84cd9fbc8be2d7df070c46cd183f589`; `.opencode/commands=sha256:b9beece61c967adf20cd12d9290849c7137f8b59032a2ec45d85a960869eaa30` | `.opencode/skills=47`; `.opencode/commands=10` | status success with verified opencode target support, command aliases installed, and no blockers | true | true | pass | none |
