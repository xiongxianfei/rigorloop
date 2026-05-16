# npm publication evidence for v0.1.5

Status: published

Trusted publishing through `.github/workflows/release.yml` published `@xiongxianfei/rigorloop@0.1.5`. The npm registry reports provenance attestations, post-publication npx smoke passed, and the real non-dry-run Codex adapter install path passed from the published package.

```yaml
publication:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.5"
  release_tag: "v0.1.5"
  source_commit: "fb04caacfa5f32ae1d7c53814ab7174856428f89"
  mode: "trusted-publishing"
  published_at: "2026-05-16T20:48:55Z"

workflow:
  release_workflow: ".github/workflows/release.yml"
  release_workflow_run: "https://github.com/xiongxianfei/rigorloop/actions/runs/25972557168"
  published_by_workflow: true
  unsupported_tags_rejected: true

tarball:
  filename: "xiongxianfei-rigorloop-0.1.5.tgz"
  sha256: "9fcdcfa6f79896030bfe3ea06943bdc650da2fefbe1d432c07d1b12f23aac10e"
  pack_command: "npm pack --prefix packages/rigorloop"
  content_check: "pass"
  smoke_result: "pass"

trusted_publishing:
  configured: true
  workflow: ".github/workflows/release.yml"
  id_token_write: true
  provenance: true
  provenance_predicate_type: "https://slsa.dev/provenance/v1"

bootstrap:
  used: false
  approving_maintainer: null
  publish_command: null

npm:
  published: true
  package_url: "https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.1.5"
  latest: "0.1.5"
  npm_view_result: "pass"

npx_smoke:
  help: "pass"
  version: "pass"

adapter_install_smoke:
  required_before_fu_close: true
  required_before_publish: "when official release assets are externally observable"
  command: "npx @xiongxianfei/rigorloop@0.1.5 init --adapter codex --json"
  temp_project: "<redacted-temp-project>"
  package_source: "published-npm"
  adapter: "codex"
  official_archive_url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.5/rigorloop-adapter-codex-v0.1.5.zip"
  archive_sha256: "97991ad31b0926ea3bcf8ab98d6aa0f93511ab25a51157d9fa701c1e822a32fd"
  archive_sha256_verified: true
  tree_sha256: "af477470c492a1b68303b462824a055b72a0ede0912616c1c641053f923d5bd4"
  tree_hash_verified: true
  file_count: 23
  generated_root: ".agents/skills"
  generated_files_exist: true
  result: "pass"
  ordering_gap: null
  fu_010_closeout_blocked: false
  ran_at: "2026-05-16T20:49:38Z"
```
