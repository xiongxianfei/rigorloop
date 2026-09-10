import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { exitCodeForResult } from "../dist/lib/command-result.js";
import { adapterDescriptor, supportedAdapterNames } from "../dist/lib/adapters.js";
import { expectedArchiveUrl, validateOfficialArchiveUrl } from "../dist/lib/official-archive-url.js";

const packageRoot = resolve(import.meta.dirname, "..");
const packageJsonPath = join(packageRoot, "package.json");
const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
const cliPath = join(packageRoot, packageJson.bin.rigorloop);
const publicPackageVersion = packageJson.version;
const publicReleaseTag = `v${publicPackageVersion}`;
const publicMetadataFile = `adapter-artifacts-${publicReleaseTag}.json`;
const publicArchiveFile = `rigorloop-adapter-codex-${publicReleaseTag}.zip`;
const historicalSkillsOnlyPackageVersion = "0.3.3";
const historicalSkillsOnlyReleaseTag = `v${historicalSkillsOnlyPackageVersion}`;
const historicalSkillsOnlyMetadataFile = `adapter-artifacts-${historicalSkillsOnlyReleaseTag}.json`;

function runCli(args, options = {}) {
  return spawnSync(process.execPath, [options.cliPath ?? cliPath, ...args], {
    cwd: options.cwd ?? packageRoot,
    env: {
      ...process.env,
      RIGORLOOP_FILE_LOG: "off",
      RIGORLOOP_CONSOLE_LOG_LEVEL: "off",
      ...(options.env ?? {}),
    },
    encoding: "utf8",
  });
}

function tempProject() {
  return mkdtempSync(join(tmpdir(), "rigorloop-cli-test-"));
}

function listProject(root) {
  return readdirSync(root, { recursive: true }).sort();
}

function readProjectFile(root, path) {
  return readFileSync(join(root, path), "utf8");
}

function actionFor(output, path) {
  return output.actions.find((action) => action.path === path);
}

function assertNoInitMutation(root) {
  assert.deepEqual(listProject(root), []);
}

function assertNoStateFiles(root) {
  assert.equal(existsSync(join(root, "rigorloop.yaml")), false);
  assert.equal(existsSync(join(root, "rigorloop.lock")), false);
}

function assertStateFilesBytePreserved(root, before) {
  assert.equal(readProjectFile(root, "rigorloop.yaml"), before.manifest);
  assert.equal(readProjectFile(root, "rigorloop.lock"), before.lockfile);
}

function parseJsonResult(result) {
  assert.equal(result.stderr, "");
  return JSON.parse(result.stdout);
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function normalizeText(bytes) {
  let text = bytes.toString("utf8");
  if (text.charCodeAt(0) === 0xfeff) {
    text = text.slice(1);
  }
  return Buffer.from(text.replace(/\r\n?/g, "\n"), "utf8");
}

function treeRowsForEntries(entries, installRoot = ".agents/skills") {
  const rows = entries
    .filter((entry) => !entry.directory && entry.name.startsWith(`${installRoot}/`))
    .map((entry) => {
      const relativePath = entry.name.slice(`${installRoot}/`.length);
      const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
      return [relativePath, sha256(bytes)];
    })
    .sort(([left], [right]) => left.localeCompare(right));
  return rows;
}

function treeHashForRows(rows) {
  const manifest = `rigorloop-tree-hash-v1\n${rows.map(([path, hash]) => `${path}\t${hash}`).join("\n")}\n`;
  return sha256(Buffer.from(manifest, "utf8"));
}

function treeHashForEntries(entries, installRoot = ".agents/skills") {
  return treeHashForRows(treeRowsForEntries(entries, installRoot));
}

function fileCountForEntries(entries, installRoot = ".agents/skills") {
  return treeRowsForEntries(entries, installRoot).length;
}

function uint16(value) {
  const buffer = Buffer.alloc(2);
  buffer.writeUInt16LE(value);
  return buffer;
}

function uint32(value) {
  const buffer = Buffer.alloc(4);
  buffer.writeUInt32LE(value >>> 0);
  return buffer;
}

function createZip(entries) {
  const localParts = [];
  const centralParts = [];
  let offset = 0;

  for (const entry of entries) {
    const nameBytes = Buffer.from(entry.name, "utf8");
    const data = entry.directory ? Buffer.alloc(0) : entry.bytes;
    const localHeader = Buffer.concat([
      uint32(0x04034b50),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(0),
      uint16(0),
      uint32(0),
      uint32(data.length),
      uint32(data.length),
      uint16(nameBytes.length),
      uint16(0),
      nameBytes,
    ]);
    localParts.push(localHeader, data);

    const externalAttributes =
      entry.externalAttributes ?? (entry.directory ? (0o040755 << 16) | 0x10 : 0o100644 << 16);
    const centralHeader = Buffer.concat([
      uint32(0x02014b50),
      uint16(0x031e),
      uint16(20),
      uint16(0),
      uint16(0),
      uint16(0),
      uint16(0),
      uint32(0),
      uint32(data.length),
      uint32(data.length),
      uint16(nameBytes.length),
      uint16(0),
      uint16(0),
      uint16(0),
      uint16(0),
      uint32(externalAttributes),
      uint32(offset),
      nameBytes,
    ]);
    centralParts.push(centralHeader);
    offset += localHeader.length + data.length;
  }

  const centralDirectory = Buffer.concat(centralParts);
  const eocd = Buffer.concat([
    uint32(0x06054b50),
    uint16(0),
    uint16(0),
    uint16(entries.length),
    uint16(entries.length),
    uint32(centralDirectory.length),
    uint32(offset),
    uint16(0),
  ]);
  return Buffer.concat([...localParts, centralDirectory, eocd]);
}

function fixtureArchive(projectRoot, options = {}) {
  const adapter = options.adapter ?? "codex";
  const releaseTag = options.releaseTag ?? publicReleaseTag;
  const metadataFile = options.metadataFile ?? `adapter-artifacts-${releaseTag}.json`;
  const archiveName = options.archiveName ?? `rigorloop-adapter-${adapter}-${releaseTag}.zip`;
  const installRoot = options.installRoot ?? ".agents/skills";
  const entries =
    options.entries ?? [
      {
        name: `${installRoot}/proposal/SKILL.md`,
        bytes: Buffer.from("# Proposal\n\nUse proposal guidance.\r\n", "utf8"),
      },
      {
        name: `${installRoot}/verify/SKILL.md`,
        bytes: Buffer.from("# Verify\n\nUse verify guidance.\n", "utf8"),
      },
    ];
  const archiveBytes = options.archiveBytes ?? createZip(entries);
  const archivePath = join(projectRoot, archiveName);
  writeFileSync(archivePath, archiveBytes);

  const artifact = {
    adapter,
    archive: archiveName,
    url: `https://github.com/xiongxianfei/rigorloop/releases/download/${releaseTag}/${archiveName}`,
    sha256: sha256(archiveBytes),
    size_bytes: archiveBytes.length,
    install_root: installRoot,
    tree_hash_algorithm: "rigorloop-tree-hash-v1",
    tree_sha256: treeHashForEntries(entries, installRoot),
    file_count: fileCountForEntries(entries, installRoot),
  };
  if (options.installRoots) {
    delete artifact.install_root;
    delete artifact.tree_sha256;
    delete artifact.file_count;
    artifact.install_roots = options.installRoots;
    artifact.root_hashes = Object.fromEntries(
      Object.entries(options.installRoots).map(([role, root]) => [
        role,
        {
          tree_sha256: treeHashForEntries(entries, root),
          file_count: fileCountForEntries(entries, root),
        },
      ]),
    );
  }
  if (options.commandAliases) {
    artifact.command_aliases = options.commandAliases;
  }
  if (options.skillsOnlyCompatibility) {
    artifact.skills_only_compatibility = options.skillsOnlyCompatibility;
  }

  const metadata = {
    schema_version: 1,
    release: {
      version: releaseTag,
      source_repository: "xiongxianfei/rigorloop",
      source_commit: "0123456789abcdef0123456789abcdef01234567",
      release_tag: releaseTag,
      published_at: "2026-05-15",
    },
    metadata: {
      url: `https://github.com/xiongxianfei/rigorloop/releases/download/${releaseTag}/${metadataFile}`,
      sha256: sha256(Buffer.from("fixture metadata\n", "utf8")),
    },
    artifacts: [artifact],
    validation: {
      command: `python scripts/validate-adapters.py --root <release-output-dir> --version ${releaseTag}`,
      result: "pass",
    },
  };
  const finalMetadata = options.metadata ? options.metadata(metadata) : metadata;
  const metadataPath = join(projectRoot, metadataFile);
  writeFileSync(metadataPath, JSON.stringify(finalMetadata, null, 2));
  return { archivePath, archiveName, metadataPath, metadata: finalMetadata, entries };
}

function fixturePackage(options = {}) {
  const root = mkdtempSync(join(tmpdir(), "rigorloop-package-test-"));
  const version = options.version ?? packageJson.version;
  const releaseTag = options.releaseTag ?? `v${version}`;
  const metadataFile = options.metadataFile ?? `adapter-artifacts-${releaseTag}.json`;
  mkdirSync(join(root, "dist", "bin"), { recursive: true });
  mkdirSync(join(root, "dist", "lib"), { recursive: true });
  mkdirSync(join(root, "dist", "metadata"), { recursive: true });
  writeFileSync(
    join(root, "package.json"),
    JSON.stringify(
      {
        name: packageJson.name,
        version,
        type: "module",
        bin: packageJson.bin,
      },
      null,
      2,
    ),
  );
  copyFileSync(cliPath, join(root, "dist", "bin", "rigorloop.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "adapters.js"), join(root, "dist", "lib", "adapters.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "command-result.js"), join(root, "dist", "lib", "command-result.js"));
  for (const file of ["installer-replacement.js", "cli-observability.js", "diagnostic-event.js", "log-config.js", "log-inspection.js", "log-sink.js", "result-renderer.js"]) {
    copyFileSync(join(packageRoot, "dist", "lib", file), join(root, "dist", "lib", file));
  }
  copyFileSync(join(packageRoot, "dist", "lib", "official-archive-url.js"), join(root, "dist", "lib", "official-archive-url.js"));

  if (options.metadata !== false) {
    const metadata = options.metadata ?? JSON.parse(readFileSync(join(packageRoot, "dist", "metadata", metadataFile), "utf8"));
    const metadataContent = typeof metadata === "string" ? metadata : JSON.stringify(metadata, null, 2);
    writeFileSync(join(root, "dist", "metadata", metadataFile), metadataContent);
    const metadataBytes = Buffer.from(metadataContent, "utf8");
    const release = options.release ?? {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: releaseTag,
      bundled_metadata: metadataFile,
      bundled_metadata_sha256: sha256(metadataBytes),
    };
    writeFileSync(
      join(root, "dist", "metadata", "releases.json"),
      JSON.stringify(
        {
          schema_version: 1,
          releases: {
            [releaseTag]: release,
          },
        },
        null,
        2,
      ),
    );
  } else {
    const releaseIndex =
      options.releaseIndex ?? {
        schema_version: 1,
        releases: {
          [releaseTag]: {
            source_repository: "xiongxianfei/rigorloop",
            release_tag: releaseTag,
            bundled_metadata: metadataFile,
            bundled_metadata_sha256: "0".repeat(64),
          },
        },
      };
    writeFileSync(join(root, "dist", "metadata", "releases.json"), JSON.stringify(releaseIndex, null, 2));
  }

  return { root, cliPath: join(root, "dist", "bin", "rigorloop.js") };
}

function validV2Lockfile() {
  return `schema_version: 2

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "${publicPackageVersion}"

manifest:
  path: "rigorloop.yaml"
  sha256: "1111111111111111111111111111111111111111111111111111111111111111"

generated:
  adapters:
    - adapter: opencode
      release: "v${publicPackageVersion}"
      source: release-archive
      archive: "rigorloop-adapter-opencode-v${publicPackageVersion}.zip"
      archive_sha256: "2222222222222222222222222222222222222222222222222222222222222222"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      installed_roots:
        skills: ".opencode/skills"
        commands: ".opencode/commands"
      root_hashes:
        skills:
          tree_sha256: "3333333333333333333333333333333333333333333333333333333333333333"
          file_count: 23
        commands:
          tree_sha256: "4444444444444444444444444444444444444444444444444444444444444444"
          file_count: 5
    - adapter: codex
      release: "v${publicPackageVersion}"
      source: release-archive
      archive: "rigorloop-adapter-codex-v${publicPackageVersion}.zip"
      archive_sha256: "5555555555555555555555555555555555555555555555555555555555555555"
      installed_root: ".agents/skills"
      tree_hash_algorithm: rigorloop-tree-hash-v1
      tree_sha256: "6666666666666666666666666666666666666666666666666666666666666666"
      file_count: 23
`;
}

function runCliWithBundledMetadata(args, cwd, metadata, options = {}) {
  const packageFixture = fixturePackage({
    metadata,
    release: options.release,
    version: options.version,
    releaseTag: options.releaseTag,
    metadataFile: options.metadataFile,
  });
  return runCli(args, {
    cwd,
    cliPath: packageFixture.cliPath,
    env: options.env,
  });
}

function mockFetchModule(archiveUrl, archiveBytes) {
  const path = join(tempProject(), "mock-fetch.mjs");
  writeFileSync(
    path,
    `const archiveUrl = ${JSON.stringify(archiveUrl)};
const archiveBytes = Buffer.from(${JSON.stringify(archiveBytes.toString("base64"))}, "base64");
globalThis.fetch = async function fetch(url) {
  if (String(url) !== archiveUrl) {
    throw new Error("Unexpected fetch URL: " + String(url));
  }
  return {
    ok: true,
    status: 200,
    async arrayBuffer() {
      return archiveBytes.buffer.slice(archiveBytes.byteOffset, archiveBytes.byteOffset + archiveBytes.byteLength);
    }
  };
};
`,
    "utf8",
  );
  return path;
}

function mockFetchFailureModule(archiveUrl, options = {}) {
  const path = join(tempProject(), "mock-fetch-failure.mjs");
  writeFileSync(
    path,
    `const archiveUrl = ${JSON.stringify(archiveUrl)};
globalThis.fetch = async function fetch(url) {
  if (String(url) !== archiveUrl) {
    throw new Error("Unexpected fetch URL: " + String(url));
  }
  const error = new Error(${JSON.stringify(options.message ?? "mocked fetch failure")});
  ${options.code ? `error.code = ${JSON.stringify(options.code)};` : ""}
  ${options.causeCode ? `error.cause = { code: ${JSON.stringify(options.causeCode)} };` : ""}
  throw error;
};
`,
    "utf8",
  );
  return path;
}

function sensitiveProxyEnv() {
  return {
    HTTP_PROXY: "http://user:pass@private.proxy.internal:8080",
    HTTPS_PROXY: "https://token-secret@secure.proxy.internal:8443",
    NO_PROXY: "internal.service.local,localhost",
    http_proxy: "http://lower-user:lower-pass@lower.proxy.internal:8080",
    https_proxy: "",
    no_proxy: "",
    RIGORLOOP_PROXY_TOKEN: "do-not-report-token",
  };
}

function assertRedacted(text) {
  for (const forbidden of [
    "user:pass",
    "token-secret",
    "lower-user:lower-pass",
    "private.proxy.internal",
    "secure.proxy.internal",
    "lower.proxy.internal",
    "internal.service.local",
    "do-not-report-token",
    "http://user:pass@private.proxy.internal:8080",
    "https://token-secret@secure.proxy.internal:8443",
  ]) {
    assert.equal(text.includes(forbidden), false, forbidden);
  }
}

test("T1 package metadata exposes one public binary and publishable runtime policy", () => {
  assert.equal(packageJson.name, "@xiongxianfei/rigorloop");
  assert.equal(packageJson.version, publicPackageVersion);
  assert.equal(packageJson.private, undefined);
  assert.deepEqual(Object.keys(packageJson.bin), ["rigorloop"]);
  assert.equal(packageJson.bin.rigorloop, "dist/bin/rigorloop.js");
  assert.match(readFileSync(cliPath, "utf8"), /^#!\/usr\/bin\/env node\n/);
  assert.equal(packageJson.license, "MIT");
  assert.equal(existsSync(join(packageRoot, "LICENSE")), true);

  const files = packageJson.files ?? [];
  assert.deepEqual(files, ["dist/", "package.json", "README.md", "LICENSE"]);
  assert.ok(!files.some((entry) => entry.endsWith(".zip")));
  assert.ok(!files.some((entry) => entry === "dist/adapters/" || entry.startsWith("dist/adapters")));

  const scripts = packageJson.scripts ?? {};
  for (const scriptName of ["preinstall", "install", "postinstall", "prepare", "prepack"]) {
    assert.equal(scripts[scriptName], undefined, scriptName);
  }
  assert.deepEqual(packageJson.dependencies ?? {}, { yaml: "2.9.0" });
});

test('TNP-005 source metadata preserves historical release identities', () => {
  // Current candidate metadata is produced by Release, in its isolated package.
  // Actual packed metadata/archive parity is covered by release_candidate_tests.
  const historicalMetadata = readFileSync(join(packageRoot, "dist", "metadata", "adapter-artifacts-v0.5.0.json"));
  assert.equal(sha256(historicalMetadata), "74f2d940ce8ef358092609884e9377d0a3955c731e7f437ca63d995862227885");
});

// M5-DOC-001: Package README coverage for multi-adapter init, runtime roots, local archive fallback, and proxy guidance.
test("M5-DOC-001 package README documents multi-adapter init and fallback boundaries", () => {
  const readme = readFileSync(join(packageRoot, "README.md"), "utf8");

  assert.match(readme, /rigorloop init codex\|claude/);
  assert.match(readme, /\.agents\/skills/);
  assert.match(readme, /\.claude\/skills/);
  assert.match(readme, /--from-archive/);
  assert.match(readme, /NODE_USE_ENV_PROXY|--use-env-proxy/);
  assert.doesNotMatch(readme, /\.codex\/skills/);
  assert.doesNotMatch(readme, /Undici|dispatcher/);
});

test("TMAI-001 descriptor registry defines the exact supported adapter set", () => {
  assert.deepEqual(supportedAdapterNames(), ["codex", "claude"]);
  assert.deepEqual(adapterDescriptor("codex").installRoots, { skills: ".agents/skills" });
  assert.deepEqual(adapterDescriptor("claude").installRoots, { skills: ".claude/skills" });
  assert.equal(adapterDescriptor("opencode"), undefined);
  assert.equal(adapterDescriptor("codex").archiveName(`v${publicPackageVersion}`), `rigorloop-adapter-codex-v${publicPackageVersion}.zip`);
  assert.equal(adapterDescriptor("claude").archiveName(`v${publicPackageVersion}`), `rigorloop-adapter-claude-v${publicPackageVersion}.zip`);
  assert.equal(adapterDescriptor("cursor"), undefined);
});

test("T2 help output shows only the implemented command surface", () => {
  const result = runCli(["--help"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /rigorloop\b/);
  assert.match(result.stdout, /rigorloop version/);
  assert.match(result.stdout, /rigorloop init codex\|claude/);
  assert.doesNotMatch(result.stdout, /--adapter/);
  assert.doesNotMatch(result.stdout, /rigorloop (?:new-change|compact|lifecycle)\b/);
  assert.doesNotMatch(result.stdout, /set-status/);
  assert.doesNotMatch(result.stdout, /Undici|dispatcher|workflow YAML|generated workflow docs/i);
});

test("T3 version output reports package identity", () => {
  const result = runCli(["version"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /@xiongxianfei\/rigorloop/);
  assert.match(result.stdout, new RegExp("0\\.5\\.1".replaceAll("0\\.5\\.1", publicPackageVersion.replaceAll(".", "\\.")), ""));
});

test("T4 unknown commands return usage errors", () => {
  const result = runCli(["unknown-command"]);

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /Unknown command/);
  assert.match(`${result.stdout}${result.stderr}`, /rigorloop --help/);
});

test("TMAI-003 unsupported targets are blocked and do not write files", () => {
  const cwd = tempProject();
  const result = runCli(["init", "cursor", "--json"], { cwd });

  assert.equal(result.status, 2);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "target-unknown");
  assert.match(output.blockers[0].next_action, /codex, claude/);
  assertNoInitMutation(cwd);
});

test("TTNI-CLI-002 rejected alias targets fail before mutation", () => {
  for (const target of ["claude-code", "open-code", "openai", "codex-cli"]) {
    const cwd = tempProject();
    const result = runCli(["init", target, "--json"], { cwd });

    assert.equal(result.status, 2, target);
    assert.equal(result.stderr, "");
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "blocked", target);
    assert.equal(output.blockers[0].code, "target-unknown", target);
    assert.match(output.blockers[0].message, new RegExp(target.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")), target);
    assert.match(output.blockers[0].next_action, /codex, claude/, target);
    assertNoInitMutation(cwd);
  }
});

test("TTNI-CLI-003 removed adapter syntax fails before mutation", () => {
  const cases = [
    ["init", "--adapter", "codex", "--json"],
    ["init", "--adapter", "codex", "claude", "--json"],
    ["init", "codex", "--adapter", "claude", "--json"],
  ];

  for (const args of cases) {
    const cwd = tempProject();
    const result = runCli(args, { cwd });

    assert.equal(result.status, 4, args.join(" "));
    assert.equal(result.stderr, "");
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "error", args.join(" "));
    assert.equal(output.errors[0].code, "adapter-option-removed", args.join(" "));
    assert.match(output.errors[0].message, /removed in RigorLoop 0\.3\.0/, args.join(" "));
    assert.match(output.errors[0].next_action, /rigorloop init codex/, args.join(" "));
    assert.match(output.errors[0].next_action, /rigorloop init claude/, args.join(" "));
    assertNoInitMutation(cwd);
  }
});

test("TMAI-001 dry-run selects descriptors for all supported adapters", () => {
  const cases = [
    ["codex", ".agents/skills", `rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["claude", ".claude/skills", `rigorloop-adapter-claude-v${publicPackageVersion}.zip`],
  ];

  for (const [adapter, root, archive] of cases) {
    const cwd = tempProject();
    const result = runCli(["init", adapter, "--dry-run", "--json"], { cwd });

    assert.equal(result.status, 0, `${adapter}: ${result.stderr}`);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "success", adapter);
    assert.equal(output.planned_target.target, adapter);
    assert.equal(output.planned_target.install_root, root);
    assert.ok(output.unperformed_checks.includes("archive verification"));
    assert.deepEqual(listProject(cwd), [], adapter);
  }
});

test("RT-R30 init rejects obsolete workflow skill installations for every target", () => {
  const cases = [
    ["codex", ".agents/skills"],
    ["claude", ".claude/skills"],
  ];

  for (const [adapter, root] of cases) {
    const cwd = tempProject();
    const obsoleteSkill = join(cwd, root, "workflow");
    mkdirSync(obsoleteSkill, { recursive: true });
    writeFileSync(join(obsoleteSkill, "SKILL.md"), "# Obsolete workflow\n");
    const before = listProject(cwd);

    const result = runCli(["init", adapter, "--dry-run", "--json"], { cwd });

    assert.equal(result.status, 2, `${adapter}: ${result.stderr}`);
    const output = parseJsonResult(result);
    assert.equal(output.status, "blocked", adapter);
    assert.equal(output.blockers[0].code, "obsolete-workflow-skill", adapter);
    assert.equal(output.blockers[0].replacement, "route", adapter);
    assert.match(output.blockers[0].next_action, /remove .*workflow.*install and invoke route/i, adapter);
    assert.deepEqual(listProject(cwd), before, adapter);
    assert.equal(readProjectFile(cwd, `${root}/workflow/SKILL.md`), "# Obsolete workflow\n", adapter);
  }
});

test("RT-R30 init rejects a mixed installed route and workflow inventory", () => {
  const cwd = tempProject();
  for (const skill of ["route", "workflow"]) {
    const skillRoot = join(cwd, ".agents", "skills", skill);
    mkdirSync(skillRoot, { recursive: true });
    writeFileSync(join(skillRoot, "SKILL.md"), `# ${skill}\n`);
  }
  const before = listProject(cwd);

  const result = runCli(["init", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 2);
  const output = parseJsonResult(result);
  assert.equal(output.blockers[0].code, "mixed-route-workflow-skills");
  assert.equal(output.blockers[0].replacement, "route");
  assert.deepEqual(listProject(cwd), before);
});

test("RT-R30 init rejects an archive containing the obsolete workflow package", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [
      {
        name: ".agents/skills/workflow/SKILL.md",
        bytes: Buffer.from("# Obsolete workflow\n", "utf8"),
      },
    ],
  });
  const before = listProject(cwd);

  const result = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 2);
  const output = parseJsonResult(result);
  assert.equal(output.blockers[0].code, "obsolete-workflow-skill");
  assert.equal(output.blockers[0].replacement, "route");
  assert.deepEqual(listProject(cwd), before);
  assert.equal(existsSync(join(cwd, ".agents", "skills")), false);
});

test("T6 JSON envelope is stable and stdout contains JSON only", () => {
  const cwd = tempProject();
  const result = runCli(["init", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  for (const key of [
    "schema_version",
    "command",
    "package",
    "cwd",
    "status",
    "summary",
    "actions",
    "artifacts",
    "blockers",
    "warnings",
    "errors",
    "diagnostics",
  ]) {
    assert.ok(Object.hasOwn(output, key), key);
  }
  assert.equal(output.schema_version, 1);
  assert.equal(output.command, "init");
  assert.equal(output.package.name, "@xiongxianfei/rigorloop");
  assert.equal(output.package.version, publicPackageVersion);
  assert.equal(output.cwd, cwd);
  assert.ok(["success", "warning", "blocked", "error"].includes(output.status));
  assert.ok(Array.isArray(output.actions));
  assert.ok(Array.isArray(output.artifacts));
  assert.ok(Array.isArray(output.blockers));
  assert.ok(Array.isArray(output.warnings));
  assert.ok(Array.isArray(output.errors));
  assert.equal(typeof output.diagnostics, "object");
});

test("T7 human output is not JSON-fragment output", () => {
  const cwd = tempProject();
  const result = runCli(["init", "codex", "--dry-run"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /RigorLoop init dry run/);
  assert.doesNotThrow(() => {
    assert.throws(() => JSON.parse(result.stdout));
  });
});

test("T8 quiet mode does not change JSON shape or behavior", () => {
  const cwd = tempProject();
  const base = JSON.parse(
    execFileSync(process.execPath, [cliPath, "init", "codex", "--dry-run", "--json"], {
      cwd,
      encoding: "utf8",
      env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
    }),
  );
  const quietResult = runCli(["init", "codex", "--dry-run", "--json", "--quiet"], { cwd });

  assert.equal(quietResult.status, 0, quietResult.stderr);
  const quiet = JSON.parse(quietResult.stdout);
  assert.deepEqual(Object.keys(quiet), Object.keys(base));
  assert.equal(quiet.status, base.status);
});

test("T9 debug mode preserves stable top-level JSON fields", () => {
  const cwd = tempProject();
  const result = runCli(["init", "codex", "--dry-run", "--json", "--debug"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  for (const key of [
    "schema_version",
    "command",
    "package",
    "cwd",
    "status",
    "summary",
    "actions",
    "artifacts",
    "blockers",
    "warnings",
    "errors",
    "diagnostics",
  ]) {
    assert.ok(Object.hasOwn(output, key), key);
  }
  assert.equal(output.diagnostics.debug, true);
});

test("T10 color is disabled by flag and environment", () => {
  const withFlag = runCli(["--help", "--no-color"]);
  const withEnv = runCli(["--help"], { env: { NO_COLOR: "1" } });
  const ansiPattern = /\u001b\[[0-9;]*m/;

  assert.equal(withFlag.status, 0);
  assert.equal(withEnv.status, 0);
  assert.doesNotMatch(withFlag.stdout, ansiPattern);
  assert.doesNotMatch(withEnv.stdout, ansiPattern);
});

test("T11 exit-code mapping covers every public exit class", () => {
  const cases = [
    ["success", { status: "success", exit_class: "success" }, 0],
    ["warning", { status: "warning", exit_class: "success" }, 0],
    ["blocked", { status: "blocked", exit_class: "blocked" }, 2],
    ["validation failed", { status: "error", exit_class: "validation_failed" }, 3],
    ["invalid usage", { status: "error", exit_class: "invalid_usage" }, 4],
    ["mutation conflict", { status: "blocked", exit_class: "mutation_conflict" }, 5],
    ["internal", { status: "error", exit_class: "internal" }, 1],
  ];

  for (const [name, result, expected] of cases) {
    assert.equal(exitCodeForResult(result), expected, name);
  }
});

test("T11 command-path exit-code mapping is enforced for M1 command paths", () => {
  const cwd = tempProject();
  const success = runCli(["init", "codex", "--dry-run", "--json"], { cwd });
  const blocked = runCli(["init", "cursor", "--json"], { cwd });
  const usage = runCli(["unknown-command"], { cwd });

  assert.equal(success.status, 0);
  assert.equal(blocked.status, 2);
  assert.equal(usage.status, 4);
});

test("T12 default dry-run reports target and unperformed checks without state files", () => {
  const cwd=tempProject();const result=runCli(["init","codex","--dry-run","--json"],{cwd});
  assert.equal(result.status,0,result.stderr);const output=JSON.parse(result.stdout);
  assert.equal(output.planned_target.install_root,".agents/skills");assert.ok(output.unperformed_checks.includes("archive verification"));assertNoInitMutation(cwd);assert.equal(output.planned_manifest,undefined);assert.equal(output.planned_lockfile,undefined);
});

test("T13 init requires a target", () => {
  const cwd = tempProject();
  const result = runCli(["init"], { cwd });

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /codex, claude/);
  assert.deepEqual(listProject(cwd), []);
});

test("T14 missing local archive path is invalid input", () => {
  const cwd = tempProject();
  const result = runCli(["init", "codex", "--from-archive", "./missing.zip", "--json"], { cwd });

  assert.equal(result.status, 4);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);

  const missingValue = runCli(["init", "codex", "--from-archive", "--json"], { cwd });
  assert.equal(missingValue.status, 4);
  assert.equal(JSON.parse(missingValue.stdout).errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);
});

test("TMAI-009 wrong local archive for selected adapter fails before extraction", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  fixture.metadata.artifacts.push({
    ...fixture.metadata.artifacts[0],
    adapter: "claude",
    archive: `rigorloop-adapter-claude-v${publicPackageVersion}.zip`,
    url: expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: `rigorloop-adapter-claude-v${publicPackageVersion}.zip` }),
    install_root: ".claude/skills",
  });
  const result = runCliWithBundledMetadata(
    ["init", "claude", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 3);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "adapter-archive-mismatch");
  assert.equal(existsSync(join(cwd, ".claude")), false);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("T15 network mode uses bundled metadata before downloading the official archive", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: sha256(Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8")),
    },
  });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: { NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}` },
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assertNoStateFiles(cwd);
  assert.equal(output.artifacts[0].sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("TMAI-029 network mode downloads official archives for every supported adapter", () => {
  for (const adapter of supportedAdapterNames()) {
    const cwd = tempProject();
    const descriptor = adapterDescriptor(adapter);
    const options =
      adapter === "opencode"
        ? {
            adapter,
            installRoot: ".opencode/skills",
            installRoots: { skills: ".opencode/skills", commands: ".opencode/commands" },
            entries: [
              { name: ".opencode/skills/proposal/SKILL.md", bytes: Buffer.from("# Proposal\n", "utf8") },
              { name: ".opencode/commands/proposal.md", bytes: Buffer.from("# Proposal command\n", "utf8") },
            ],
            commandAliases: { opencode: { count: 1, paths: [".opencode/commands/proposal.md"] } },
          }
        : {
            adapter,
            installRoot: descriptor.primaryInstallRoot(),
          };
    const fixture = fixtureArchive(cwd, options);
    const archiveBytes = readFileSync(fixture.archivePath);
    const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
    fixture.metadata.artifacts[0].url = officialUrl;
    const packageFixture = fixturePackage({ metadata: fixture.metadata });
    const result = runCli(["init", adapter, "--json"], {
      cwd,
      cliPath: packageFixture.cliPath,
      env: { NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}` },
    });

    assert.equal(result.status, 0, adapter);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "success", adapter);
    assert.equal(output.planned_target.target, adapter);
    assertNoStateFiles(cwd);
  }
});

test("TMAI-029 network failure reports bounded proxy diagnostics in JSON", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchFailureModule(officialUrl, {
        message: "getaddrinfo ENOTFOUND private.proxy.internal",
        code: "ENOTFOUND",
      })}`,
    },
  });

  assert.equal(result.status, 2, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "release-download-failed");
  assert.equal(output.diagnostics.adapter, "codex");
  assert.equal(output.diagnostics.release, `v${publicPackageVersion}`);
  assert.equal(output.diagnostics.archive_url, officialUrl);
  assert.equal(output.diagnostics.download_failure_class, "dns");
  assert.match(output.diagnostics.node_env_proxy_status, /^(enabled|disabled|unsupported|unknown)$/);
  assert.deepEqual(output.diagnostics.proxy_env_vars_detected, ["HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy"]);
  assert.match(output.blockers[0].next_action, /--from-archive/);
  assertRedacted(JSON.stringify(output));
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("TMAI-030 proxy diagnostic enums and env-var allowlist are stable", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      HTTP_PROXY: "http://proxy.example.invalid:8080",
      HTTPS_PROXY: "http://secure.example.invalid:8080",
      NO_PROXY: "localhost",
      http_proxy: "http://lower.example.invalid:8080",
      https_proxy: "http://lower-secure.example.invalid:8080",
      no_proxy: "127.0.0.1",
      ALL_PROXY: "http://not-allowed.example.invalid:8080",
      NODE_OPTIONS: `--import ${mockFetchFailureModule(officialUrl, { message: "proxy connection failed", code: "ERR_PROXY_CONNECTION_FAILED" })}`,
    },
  });

  assert.equal(result.status, 2, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.deepEqual(output.diagnostics.proxy_env_vars_detected, [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "http_proxy",
    "https_proxy",
    "no_proxy",
  ]);
  assert.match(output.diagnostics.node_env_proxy_status, /^(enabled|disabled|unsupported|unknown)$/);
  assert.match(output.diagnostics.download_failure_class, /^(dns|tls|timeout|http-status|proxy|network|unknown)$/);
  assert.equal(JSON.stringify(output).includes("ALL_PROXY"), false);
  assert.equal(JSON.stringify(output).includes("not-allowed.example.invalid"), false);
});

test("CR-M4-R1-F1 node_env_proxy_status reports enabled with --use-env-proxy", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = spawnSync(
    process.execPath,
    [
      "--use-env-proxy",
      "--import",
      mockFetchFailureModule(officialUrl, { message: "proxy connection failed", code: "ERR_PROXY_CONNECTION_FAILED" }),
      packageFixture.cliPath,
      "init",
      "codex",
      "--json",
    ],
    {
      cwd,
      env: {
        ...process.env,
        HTTP_PROXY: "http://proxy.example.invalid:8080",
        HTTPS_PROXY: "",
        NO_PROXY: "",
        http_proxy: "",
        https_proxy: "",
        no_proxy: "",
      },
      encoding: "utf8",
    },
  );

  assert.equal(result.status, 2, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.diagnostics.node_env_proxy_status, "enabled");
  assert.equal(output.diagnostics.download_failure_class, "proxy");
  assert.deepEqual(output.diagnostics.proxy_env_vars_detected, ["HTTP_PROXY"]);
});

test("TMAI-031 human proxy failure output is actionable and redacted", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = runCli(["init", "codex"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchFailureModule(officialUrl, { message: "proxy refused private.proxy.internal", code: "ERR_PROXY_CONNECTION_FAILED" })}`,
    },
  });

  assert.equal(result.status, 2);
  assert.equal(result.stdout, "");
  assert.match(result.stderr, /adapter codex/);
  assert.match(result.stderr, new RegExp("release v0\\.5\\.1".replaceAll("0\\.5\\.1", publicPackageVersion.replaceAll(".", "\\.")), ""));
  assert.match(result.stderr, /failure class proxy/);
  assert.match(result.stderr, new RegExp(officialUrl.replaceAll(".", "\\.")));
  assert.match(result.stderr, /--from-archive/);
  assertRedacted(result.stderr);
});

test("TMAI-032 proxy diagnostics do not mask archive verification failures", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const wrongArchiveBytes = Buffer.from(readFileSync(fixture.archivePath));
  wrongArchiveBytes[wrongArchiveBytes.length - 1] = wrongArchiveBytes[wrongArchiveBytes.length - 1] ^ 0xff;
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, wrongArchiveBytes)}`,
    },
  });

  assert.equal(result.status, 3, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "archive-sha-mismatch");
  assert.equal(output.blockers.length, 0);
  assert.equal(output.diagnostics.download_failure_class, undefined);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("T15 network mode rejects non-official archive URLs before fetch", () => {
  const cases = [
    ["data URL", "data:application/octet-stream;base64,AAAA"],
    ["wrong host", `https://example.com/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["wrong owner", `https://github.com/other/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["wrong release", `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.2/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["wrong archive", `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/other.zip`],
    ["query", `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip?download=1`],
    ["hash", `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip#fragment`],
    ["http", `http://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["raw", `https://raw.githubusercontent.com/xiongxianfei/rigorloop/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
  ];

  for (const [name, url] of cases) {
    const cwd = tempProject();
    const fixture = fixtureArchive(cwd);
    fixture.metadata.artifacts[0].url = url;
    const result = runCliWithBundledMetadata(["init", "codex", "--json"], cwd, fixture.metadata);
    assert.equal(result.status, 3, name);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "error", name);
    assert.equal(output.errors[0].code, "non-official-archive-url", name);
    assert.equal(output.errors[0].path, "metadata.artifacts[codex].url", name);
    assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false, name);
  }
});

test("T15 official archive URL helper accepts only exact release archive URLs", () => {
  const releaseTag = `v${publicPackageVersion}`;
  for (const adapter of supportedAdapterNames()) {
    const archive = adapterDescriptor(adapter).archiveName(releaseTag);
    const officialUrl = expectedArchiveUrl({ releaseTag, archive });
    assert.equal(officialUrl, `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/${archive}`);
    assert.deepEqual(validateOfficialArchiveUrl({ url: officialUrl, releaseTag, archive }), { ok: true });
  }
  const archive = `rigorloop-adapter-codex-v${publicPackageVersion}.zip`;
  assert.equal(
    validateOfficialArchiveUrl({
      url: `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip?download=1`,
      releaseTag,
      archive,
    }).code,
    "non-official-archive-url",
  );
});

test("T16 bundled metadata hash verification uses the bundled release index", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  fixture.metadata.artifacts[0].url = `data:application/octet-stream;base64,${archiveBytes.toString("base64")}`;
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: "0".repeat(64),
    },
  });

  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 3);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "metadata-sha256-mismatch");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T16 bundled metadata bytes are verified before parsing", () => {
  const cwd = tempProject();
  const packageFixture = fixturePackage({
    metadata: "not-json",
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: "0".repeat(64),
    },
  });

  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "metadata-sha256-mismatch");
});

test("T16 missing metadata trust root blocks network install", () => {
  const cwd = tempProject();
  const packageFixture = fixturePackage({
    metadata: false,
    releaseIndex: {
      schema_version: 1,
      releases: {
        [`v${publicPackageVersion}`]: {
          source_repository: "xiongxianfei/rigorloop",
          bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
        },
      },
    },
  });

  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "metadata-trust-root-unavailable");
});

test("T16 runtime release metadata environment override is ignored", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({ releaseTag: `v${publicPackageVersion}`, archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: sha256(Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8")),
    },
  });

  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}`,
      RIGORLOOP_RELEASE_METADATA_URL: "http://127.0.0.1:9/attacker.json",
    },
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("T17 incompatible local archive release is blocked", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, { archiveName: "rigorloop-adapter-codex-v0.1.2.zip" });
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "release-version-incompatible");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T18 local archive mode uses bundled metadata and no metadata flag", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.artifacts[0].sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(output.artifacts[0].tree_sha256, fixture.metadata.artifacts[0].tree_sha256);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
  assert.doesNotMatch(result.stdout, /metadata/);
});

test("T18 runtime local metadata environment override is ignored", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const attackerMetadataPath = join(cwd, "attacker-metadata.json");
  writeFileSync(
    attackerMetadataPath,
    JSON.stringify({
      ...fixture.metadata,
      artifacts: [{ ...fixture.metadata.artifacts[0], sha256: "0".repeat(64) }],
    }),
  );

  const result = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
    { env: { RIGORLOOP_METADATA_FILE: attackerMetadataPath } },
  );

  assert.equal(result.status, 0, result.stderr);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("T19 missing bundled metadata blocks local archive install", () => {
  const cwd = tempProject();
  const archive = createZip([
    {
      name: ".agents/skills/proposal/SKILL.md",
      bytes: Buffer.from("# Proposal\n", "utf8"),
    },
  ]);
  writeFileSync(join(cwd, `rigorloop-adapter-codex-v${publicPackageVersion}.zip`), archive);
  const packageFixture = fixturePackage({ metadata: false });
  const result = runCli(["init", "codex", "--from-archive", `./rigorloop-adapter-codex-v${publicPackageVersion}.zip`, "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "metadata-unavailable");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("TTNI-INST-001 default init installs single-root targets without state files", () => {
  const cases = [
    { adapter: "codex", root: ".agents/skills" },
    { adapter: "claude", root: ".claude/skills" },
  ];

  for (const { adapter, root } of cases) {
    const cwd = tempProject();
    const fixture = fixtureArchive(cwd, { adapter, installRoot: root });
    const result = runCliWithBundledMetadata(["init", adapter, "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

    assert.equal(result.status, 0, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "success", adapter);
    assert.equal(output.state_files.action, "skipped", adapter);
    assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false, adapter);
    assert.equal(existsSync(join(cwd, "rigorloop.lock")), false, adapter);
    assert.equal(readProjectFile(cwd, `${root}/proposal/SKILL.md`), "# Proposal\n\nUse proposal guidance.\n", adapter);
    assert.equal(readProjectFile(cwd, `${root}/verify/SKILL.md`), "# Verify\n\nUse verify guidance.\n", adapter);
  }
});

test("T26 overwrite conflicts are refused without replacing user files", () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, ".agents"), "user file\n");
  const fixture=fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", fixture.archivePath, "--json", "--force"], cwd, fixture.metadata);

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.ok(output.blockers.length);
});

test("T26 leaf install-root file conflict is refused without replacing user files", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, ".agents"));
  writeFileSync(join(cwd, ".agents", "skills"), "user file\n");
  const fixture=fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", fixture.archivePath, "--json", "--force"], cwd, fixture.metadata);

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents/skills"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.ok(output.blockers.length);
});

test("T26 adapter file content conflicts fail installed-tree verification without replacing user files", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "proposal"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), "user file\n");
  const result = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 5);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "user file\n");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "destination-conflict");
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("T29 release metadata shape and validation result are validated", () => {
  const cwd = tempProject();
  const wrongRepo = fixtureArchive(cwd, {
    metadata(metadata) {
      metadata.release.source_repository = "example/not-rigorloop";
      return metadata;
    },
  });
  const wrongRepoResult = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${wrongRepo.archiveName}`, "--json"], cwd, wrongRepo.metadata);

  assert.equal(wrongRepoResult.status, 3);
  assert.equal(JSON.parse(wrongRepoResult.stdout).errors[0].code, "metadata-invalid");

  const missingFieldProject = tempProject();
  const missingField = fixtureArchive(missingFieldProject, {
    metadata(metadata) {
      delete metadata.metadata.sha256;
      return metadata;
    },
  });
  const missingFieldResult = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${missingField.archiveName}`, "--json"],
    missingFieldProject,
    missingField.metadata,
  );

  assert.equal(missingFieldResult.status, 3);
  assert.equal(JSON.parse(missingFieldResult.stdout).errors[0].code, "metadata-invalid");

  const noCodexProject = tempProject();
  const noCodex = fixtureArchive(noCodexProject, {
    metadata(metadata) {
      metadata.artifacts[0].adapter = "claude";
      return metadata;
    },
  });
  const noCodexResult = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${noCodex.archiveName}`, "--json"],
    noCodexProject,
    noCodex.metadata,
  );

  assert.equal(noCodexResult.status, 2);
  assert.equal(JSON.parse(noCodexResult.stdout).blockers[0].code, "metadata-unavailable");

  const wrongRootProject = tempProject();
  const wrongRoot = fixtureArchive(wrongRootProject, {
    metadata(metadata) {
      metadata.artifacts[0].install_root = ".codex/skills";
      return metadata;
    },
  });
  const wrongRootResult = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${wrongRoot.archiveName}`, "--json"],
    wrongRootProject,
    wrongRoot.metadata,
  );

  assert.equal(wrongRootResult.status, 3);
  assert.equal(JSON.parse(wrongRootResult.stdout).errors[0].code, "metadata-invalid");

  const validationFailProject = tempProject();
  const validationFail = fixtureArchive(validationFailProject, {
    metadata(metadata) {
      metadata.validation.result = "fail";
      return metadata;
    },
  });
  const validationFailResult = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${validationFail.archiveName}`, "--json"],
    validationFailProject,
    validationFail.metadata,
  );

  assert.equal(validationFailResult.status, 3);
  assert.equal(JSON.parse(validationFailResult.stdout).errors[0].code, "metadata-invalid");
});

test("T30 archive traversal paths are rejected", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "../escape.txt", bytes: Buffer.from("escape\n", "utf8") }],
  });
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-path-traversal");
  assert.equal(existsSync(join(cwd, "escape.txt")), false);
});

test("T31 archive entries must remain under .agents/skills", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "proposal/SKILL.md", bytes: Buffer.from("# Proposal\n", "utf8") }],
  });
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-install-root-invalid");

  const supportProject = tempProject();
  const supportFixture = fixtureArchive(supportProject, {
    entries: [
      {
        name: ".agents/skills/proposal/SKILL.md",
        bytes: Buffer.from("# Proposal\n", "utf8"),
      },
      {
        name: "AGENTS.md",
        bytes: Buffer.from("Support instructions are not installed by this slice.\n", "utf8"),
      },
    ],
  });
  const supportResult = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${supportFixture.archiveName}`, "--json"],
    supportProject,
    supportFixture.metadata,
  );

  assert.equal(supportResult.status, 0, supportResult.stderr);
  assert.equal(existsSync(join(supportProject, "AGENTS.md")), false);
  assert.equal(readProjectFile(supportProject, ".agents/skills/proposal/SKILL.md"), "# Proposal\n");
});

test("T33 symlink archive entries are rejected", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [
      {
        name: ".agents/skills/proposal/SKILL.md",
        bytes: Buffer.from("target", "utf8"),
        externalAttributes: 0o120777 << 16,
      },
    ],
  });
  const result = runCliWithBundledMetadata(["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-symlink-entry");
});

test("T34 archive verification failures use exit code 3", () => {
  const checksumProject = tempProject();
  const checksumFixture = fixtureArchive(checksumProject, {
    metadata(metadata) {
      metadata.artifacts[0].sha256 = "0".repeat(64);
      return metadata;
    },
  });
  const checksum = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${checksumFixture.archiveName}`, "--json"],
    checksumProject,
    checksumFixture.metadata,
  );
  assert.equal(checksum.status, 3);
  assert.equal(JSON.parse(checksum.stdout).errors[0].code, "archive-sha-mismatch");

  const sizeProject = tempProject();
  const sizeFixture = fixtureArchive(sizeProject, {
    metadata(metadata) {
      metadata.artifacts[0].size_bytes += 1;
      return metadata;
    },
  });
  const size = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${sizeFixture.archiveName}`, "--json"],
    sizeProject,
    sizeFixture.metadata,
  );
  assert.equal(size.status, 3);
  assert.equal(JSON.parse(size.stdout).errors[0].code, "archive-size-mismatch");

  const treeProject = tempProject();
  const treeFixture = fixtureArchive(treeProject, {
    metadata(metadata) {
      metadata.artifacts[0].tree_sha256 = "f".repeat(64);
      return metadata;
    },
  });
  const tree = runCliWithBundledMetadata(
    ["init", "codex", "--from-archive", `./${treeFixture.archiveName}`, "--json"],
    treeProject,
    treeFixture.metadata,
  );
  assert.equal(tree.status, 3);
  assert.equal(JSON.parse(tree.stdout).errors[0].code, "tree-hash-mismatch");
});


for (const [target, installRoot] of [['codex','.agents/skills'],['claude','.claude/skills']]) {
  test(`DIST conflict preflight and force preserve unrelated content and ignore state: ${target}`,()=>{
    const cwd=tempProject();const fixture=fixtureArchive(cwd,{adapter:target,installRoot});
    const args=['init',target,'--from-archive',`./${fixture.archiveName}`,'--json'];
    writeFileSync(join(cwd,'rigorloop.yaml'),'not: [yaml');symlinkSync('/missing-state-target',join(cwd,'rigorloop.lock'));
    let result=runCliWithBundledMetadata(args,cwd,fixture.metadata);assert.equal(result.status,0,result.stdout+result.stderr);
    const first=fixture.entries.find(e=>e.name.startsWith(`${installRoot}/`)&&!e.directory).name;
    const unit=`${installRoot}/${first.slice(installRoot.length+1).split('/')[0]}`;
    writeFileSync(join(cwd,unit,'obsolete.txt'),'local edit');mkdirSync(join(cwd,installRoot,'unrelated'));writeFileSync(join(cwd,installRoot,'unrelated','keep'),'keep');
    result=runCliWithBundledMetadata(args,cwd,fixture.metadata);assert.equal(result.status,5,result.stdout+result.stderr);assert.ok(JSON.parse(result.stdout).blockers.some(b=>b.path===unit));
    result=runCliWithBundledMetadata([...args,'--force'],cwd,fixture.metadata);assert.equal(result.status,0,result.stdout+result.stderr);
    assert.equal(existsSync(join(cwd,unit,'obsolete.txt')),false);assert.equal(readFileSync(join(cwd,installRoot,'unrelated','keep'),'utf8'),'keep');assert.equal(readFileSync(join(cwd,'rigorloop.yaml'),'utf8'),'not: [yaml');assert.ok(lstatSync(join(cwd,'rigorloop.lock')).isSymbolicLink());
    assert.ok(JSON.parse(result.stdout).retained.length>0);
  });
}
test('DIST retired state flag and OpenCode reject even with force before acquisition',()=>{
  for(const args of [['init','codex','--write-state'],['init','opencode'],['init','opencode','--from-archive','missing.zip']]) {
    const cwd=tempProject();const result=runCli([...args,'--force','--json'],{cwd});assert.equal(result.status,2,result.stdout+result.stderr);assertNoInitMutation(cwd);
  }
});

test('DIST all candidate conflicts are reported before absent units are installed', () => {
  const cwd = tempProject();
  const entries = ['a', 'b', 'c'].map(name => ({name: `.agents/skills/${name}/SKILL.md`, bytes: Buffer.from(name)}));
  const fixture = fixtureArchive(cwd, {entries});
  mkdirSync(join(cwd, '.agents/skills/a'), {recursive: true});
  mkdirSync(join(cwd, '.agents/skills/c'));
  writeFileSync(join(cwd, '.agents/skills/c/SKILL.md'), 'c');
  const result = runCliWithBundledMetadata(['init', 'codex', '--from-archive', fixture.archiveName, '--json'], cwd, fixture.metadata);
  assert.equal(result.status, 5, result.stdout + result.stderr);
  assert.deepEqual(JSON.parse(result.stdout).blockers.map(b => b.path), ['.agents/skills/a', '.agents/skills/c']);
  assert.equal(existsSync(join(cwd, '.agents/skills/b')), false);
});

test('DIST retired authoring guards preserve installed and candidate entries even with force', () => {
  for (const skill of ['spec', 'architecture']) for (const installed of [false, true]) {
    const cwd = tempProject();
    const fixture = fixtureArchive(cwd, installed ? {} : {entries: [{name: `.agents/skills/${skill}/SKILL.md`, bytes: Buffer.from('retired')}]});
    if (installed) { mkdirSync(join(cwd, `.agents/skills/${skill}`), {recursive: true}); writeFileSync(join(cwd, `.agents/skills/${skill}/SKILL.md`), 'local'); }
    const result = runCliWithBundledMetadata(['init', 'codex', '--from-archive', fixture.archiveName, '--force', '--json'], cwd, fixture.metadata);
    assert.equal(result.status, 2, result.stdout + result.stderr);
    assert.equal(JSON.parse(result.stdout).blockers[0].code, installed ? 'retired-authoring-installation' : 'retired-authoring-candidate');
    if (installed) assert.equal(readFileSync(join(cwd, `.agents/skills/${skill}/SKILL.md`), 'utf8'), 'local');
    else assert.equal(existsSync(join(cwd, '.agents')), false);
  }
});
