# npm publication evidence for v0.1.4

Status: published

FU-010 is closed by this evidence: `@xiongxianfei/rigorloop@0.1.4` is publicly visible on npm, post-publication npx smoke passed, and the real non-dry-run Codex adapter install path passed from the published package.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.4"
  release_tag: "v0.1.4"
  source_commit: "8221134e08674040b05145241b20fbfcf0c530cf"
  mode: "bootstrap"
  published_at: "2026-05-16T20:11:25Z"

workflow:
  release_workflow: ".github/workflows/release.yml"
  release_workflow_run: "https://github.com/xiongxianfei/rigorloop/actions/runs/25971083444"
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
  next_release_requirement: "configure trusted publishing before the next npm publication"

bootstrap:
  used: true
  approving_maintainer: "flyingbear"
  publish_command: "npm publish xiongxianfei-rigorloop-0.1.4.tgz --access public --registry=https://registry.npmjs.org"

npm:
  published: true
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.1.4"
  latest: "0.1.4"
  npm_view_result: "pass"

npx_smoke:
  help: "pass"
  version: "pass"
  dry_run_init: "pass"

adapter_install_smoke:
  required_before_fu_close: true
  required_before_publish: "when official release assets are externally observable"
  command: "npx @xiongxianfei/rigorloop@0.1.4 init --adapter codex --json"
  temp_project: "<redacted-temp-project>"
  package_source: "published-npm"
  adapter: "codex"
  official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.4/rigorloop-adapter-codex-v0.1.4.zip"
  archive_sha256: "6c44d186c28507d44573666453b76b6d1568fa49f4f152d10151feafe04858b1"
  archive_sha256_verified: true
  tree_sha256: "af477470c492a1b68303b462824a055b72a0ede0912616c1c641053f923d5bd4"
  tree_hash_verified: true
  file_count: 23
  generated_root: ".agents/skills"
  generated_files_exist: true
  result: "pass"
  ordering_gap: null
  fu_010_closeout_blocked: false
  ran_at: "2026-05-16T20:17:40Z"
```
