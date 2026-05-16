# npm publication evidence for v0.1.5

Status: pending-publication

This file is a pre-publication evidence scaffold. Trusted publishing is configured for `.github/workflows/release.yml`; final closeout remains pending until the workflow publishes `@xiongxianfei/rigorloop@0.1.5` and actual non-dry-run Codex adapter install proof is recorded.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.5"
  release_tag: "v0.1.5"
  source_commit: "5315a6d08b9d79e52d3276fd532b02f97c727e55"
  mode: "trusted-publishing"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.1.5.tgz"
  sha256: "pending"
  pack_command: "npm pack --prefix packages/rigorloop"
  content_check: "pending"
  smoke_result: "pending"

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

adapter_install_smoke:
  required_before_fu_close: true
  required_before_publish: "when official release assets are externally observable"
  command: "npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --json"
  temp_project: "pending"
  package_source: "published-npm"
  adapter: "codex"
  official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.5/rigorloop-adapter-codex-v0.1.5.zip"
  archive_sha256_verified: false
  tree_hash_verified: false
  result: "pending"
  ordering_gap: "pending trusted-publishing workflow execution"
  fu_010_closeout_blocked: true
```
