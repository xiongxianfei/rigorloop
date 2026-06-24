# npm publication evidence for v0.3.3

Status: published

This file records the required live registry/download post-publish smoke contract. The pre-publish gate used the packed package; the post-publish rows record the externally observable `@xiongxianfei/rigorloop@0.3.3` package and matching GitHub release archives.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.3.3"
  release_tag: "v0.3.3"
  source_commit: "6f895a03"
  mode: "trusted-publishing"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.3.3.tgz"
  sha256: "cad8bfe85b9af206490c6879eb150ff53c4abd4206a74cd917a7c871b8eb8f7f"
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
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.3"

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init codex --json"
    npm_version: "0.3.3"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-codex-v0.3.3.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "sha256:9cdfba0fe8ff8c13b782f729199081ed9342104334bac5712c4402dcd3a65122"
    file_counts:
      - "44"
    command_output_summary: "success; installed verified Codex target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init claude --json"
    npm_version: "0.3.3"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-claude-v0.3.3.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "sha256:dcd94ba382633c1e64e0dcdde7b31fa1e24047066afb5d4bbe9868b4f6392a7f"
    file_counts:
      - "44"
    command_output_summary: "success; installed verified Claude Code target support"
    archive_sha256_verified: true
    tree_hash_verified: true
    result: "pass"
    closeout_blocker: "none"
    post_publish_closeout_blocked: false
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init opencode --json"
    npm_version: "0.3.3"
    temp_project: "fresh temporary project"
    package_source: "npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-opencode-v0.3.3.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - ".opencode/skills=sha256:dcd94ba382633c1e64e0dcdde7b31fa1e24047066afb5d4bbe9868b4f6392a7f"
      - ".opencode/commands=sha256:994ca3f37dc39057a6cf4d2f605395e1489f827ac70031e916c32cd19d801440"
    file_counts:
      - ".opencode/skills=44"
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
| codex | `npx @xiongxianfei/rigorloop@0.3.3 init codex` | `0.3.3` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-codex-v0.3.3.zip` | `.agents/skills` | `sha256:9cdfba0fe8ff8c13b782f729199081ed9342104334bac5712c4402dcd3a65122` | `44` | success; installed verified Codex target support | true | true | pass | none |
| claude | `npx @xiongxianfei/rigorloop@0.3.3 init claude` | `0.3.3` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-claude-v0.3.3.zip` | `.claude/skills` | `sha256:dcd94ba382633c1e64e0dcdde7b31fa1e24047066afb5d4bbe9868b4f6392a7f` | `44` | success; installed verified Claude Code target support | true | true | pass | none |
| opencode | `npx @xiongxianfei/rigorloop@0.3.3 init opencode` | `0.3.3` | npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-opencode-v0.3.3.zip` | `.opencode/skills`; `.opencode/commands` | `.opencode/skills=sha256:dcd94ba382633c1e64e0dcdde7b31fa1e24047066afb5d4bbe9868b4f6392a7f`; `.opencode/commands=sha256:994ca3f37dc39057a6cf4d2f605395e1489f827ac70031e916c32cd19d801440` | `.opencode/skills=44`; `.opencode/commands=0` | success; installed verified opencode target support with skills-only compatibility warning | true | true | pass | none |
