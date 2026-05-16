# npm publication evidence for v0.1.4

Status: pending-publication

This file is a pre-publication evidence scaffold. FU-010 remains open until this file records public npm publication and actual non-dry-run Codex adapter install proof.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.4"
  release_tag: "v0.1.4"
  source_commit: "c9cfaf24949d5b2093ee250d216e7762ca2fdf41"
  mode: "bootstrap"

workflow:
  release_workflow: ".github/workflows/release.yml"
  published_by_workflow: false
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.1.4.tgz"
  sha256: "c6e683f26c9f6c15d27c880178843e0a53047f90b6773682c720e0294898637b"
  pack_command: "npm pack --prefix packages/rigorloop"
  content_check: "pass"
  smoke_result: "pass"

trusted_publishing:
  configured: false
  workflow: ".github/workflows/release.yml"
  id_token_write: false

bootstrap:
  used: false
  approving_maintainer: "pending"
  publish_command: "pending"

npm:
  published: false
  package_url: "pending"

adapter_install_smoke:
  required_before_fu_close: true
  required_before_publish: "when official release assets are externally observable"
  command: "npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json"
  temp_project: "pending"
  package_source: "packed-tarball"
  adapter: "codex"
  official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.4/rigorloop-adapter-codex-v0.1.4.zip"
  archive_sha256_verified: false
  tree_hash_verified: false
  result: "pending"
  ordering_gap: "GitHub release assets are externally observable; npm publication is blocked until maintainer npm authentication is available"
  fu_010_closeout_blocked: true
```
