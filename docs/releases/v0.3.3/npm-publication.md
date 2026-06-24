# npm publication evidence for v0.3.3

Status: pending-publication

This file records the required live registry/download post-publish smoke contract. The pre-publish gate uses the packed package; the post-publish rows remain blocked until the externally observable `@xiongxianfei/rigorloop@0.3.3` package and matching GitHub release archives are available.

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
  published: false
  package_url: ""

target_init_smoke:
  codex:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init codex --json"
    npm_version: "0.3.3"
    temp_project: "pending post-publication fresh temporary project"
    package_source: "pending npm registry"
    target: "codex"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-codex-v0.3.3.zip"
    installed_roots:
      - ".agents/skills"
    tree_hashes:
      - "pending post-publication tree hash"
    file_counts:
      - "pending post-publication file count"
    command_output_summary: "pending post-publication live smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live registry/download smoke pending"
    post_publish_closeout_blocked: true
  claude:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init claude --json"
    npm_version: "0.3.3"
    temp_project: "pending post-publication fresh temporary project"
    package_source: "pending npm registry"
    target: "claude"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-claude-v0.3.3.zip"
    installed_roots:
      - ".claude/skills"
    tree_hashes:
      - "pending post-publication tree hash"
    file_counts:
      - "pending post-publication file count"
    command_output_summary: "pending post-publication live smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live registry/download smoke pending"
    post_publish_closeout_blocked: true
  opencode:
    command: "npx @xiongxianfei/rigorloop@0.3.3 init opencode --json"
    npm_version: "0.3.3"
    temp_project: "pending post-publication fresh temporary project"
    package_source: "pending npm registry"
    target: "opencode"
    official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-opencode-v0.3.3.zip"
    installed_roots:
      - ".opencode/skills"
      - ".opencode/commands"
    tree_hashes:
      - "pending .opencode/skills tree hash"
      - "pending .opencode/commands tree hash"
    file_counts:
      - "pending .opencode/skills file count"
      - "pending .opencode/commands file count"
    command_output_summary: "pending post-publication live smoke"
    archive_sha256_verified: false
    tree_hash_verified: false
    result: "pending-publication"
    closeout_blocker: "live registry/download smoke pending"
    post_publish_closeout_blocked: true
```

| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| codex | `npx @xiongxianfei/rigorloop@0.3.3 init codex` | `0.3.3` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-codex-v0.3.3.zip` | `.agents/skills` | pending post-publication tree hash | pending post-publication file count | pending post-publication live smoke | false | false | pending-publication | live registry/download smoke pending |
| claude | `npx @xiongxianfei/rigorloop@0.3.3 init claude` | `0.3.3` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-claude-v0.3.3.zip` | `.claude/skills` | pending post-publication tree hash | pending post-publication file count | pending post-publication live smoke | false | false | pending-publication | live registry/download smoke pending |
| opencode | `npx @xiongxianfei/rigorloop@0.3.3 init opencode` | `0.3.3` | pending npm registry | `https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.3/rigorloop-adapter-opencode-v0.3.3.zip` | `.opencode/skills`; `.opencode/commands` | pending .opencode/skills tree hash; pending .opencode/commands tree hash | pending .opencode/skills file count; pending .opencode/commands file count | pending post-publication live smoke | false | false | pending-publication | live registry/download smoke pending |
