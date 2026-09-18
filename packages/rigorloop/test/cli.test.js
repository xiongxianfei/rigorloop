import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  readlinkSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { exitCodeForResult } from "../dist/lib/command-result.js";
import { adapterDescriptor, supportedAdapterNames } from "../dist/lib/adapters.js";
import {
  expectedArchiveUrl,
  validateOfficialArchiveUrl,
} from "../dist/lib/official-archive-url.js";

const packageRoot = resolve(import.meta.dirname, "..");
const packageJsonPath = join(packageRoot, "package.json");
const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
const cliPath = join(packageRoot, packageJson.bin.rigorloop);
const publicPackageVersion = packageJson.version;
const publicReleaseTag = `v${publicPackageVersion}`;
const publicMetadataFile = `adapter-artifacts-${publicReleaseTag}.json`;

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

function tempProject(t) {
  const directory = mkdtempSync(join(tmpdir(), "rigorloop-cli-test-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  return directory;
}

function listProject(root) {
  return readdirSync(root, { recursive: true }).sort();
}

function projectSnapshot(root) {
  const entries = [];
  function visit(path = "") {
    const absolute = join(root, path);
    const info = lstatSync(absolute);
    if (info.isSymbolicLink()) {
      entries.push([path, "link", info.mode, readlinkSync(absolute)]);
    } else if (info.isDirectory()) {
      entries.push([path, "directory", info.mode]);
      for (const name of readdirSync(absolute).sort()) visit(path ? `${path}/${name}` : name);
    } else {
      assert.ok(info.isFile(), `Unexpected fixture type: ${path}`);
      entries.push([path, "file", info.mode, readFileSync(absolute).toString("base64")]);
    }
  }
  visit();
  return entries;
}

// Instrument the real child process, before its named node:fs imports bind.
// Probe files live outside the project whose preservation is being observed.
function installationProbe(t, { statePaths = [], archivePath, failAfterPublish } = {}) {
  const directory = tempProject(t);
  const eventsPath = join(directory, "events.jsonl");
  const preload = join(directory, "installation-probe.mjs");
  writeFileSync(eventsPath, "");
  writeFileSync(preload, `import fs from "node:fs";
import { syncBuiltinESMExports } from "node:module";
import { resolve, join } from "node:path";
import { fileURLToPath } from "node:url";
const statePaths = new Set(${JSON.stringify(statePaths)});
const archivePath = ${JSON.stringify(archivePath ?? null)};
const failAfterPublish = ${JSON.stringify(failAfterPublish ?? null)};
const append = fs.appendFileSync;
const readlink = fs.readlinkSync;
const emit = event => append(${JSON.stringify(eventsPath)}, JSON.stringify(event) + "\\n");
function pathOf(value) {
  if (typeof value === "number") value = "/proc/self/fd/" + value;
  if (value instanceof URL) value = fileURLToPath(value);
  if (Buffer.isBuffer(value)) value = value.toString();
  if (typeof value !== "string") return null;
  const path = resolve(value);
  const anchored = /^\\/proc\\/self\\/fd\\/(\\d+)(?:\\/(.*))?$/.exec(path);
  if (!anchored) return path;
  return join(readlink("/proc/self/fd/" + anchored[1]), anchored[2] ?? "");
}
function guard(method, value) {
  const path = pathOf(value);
  if (statePaths.has(path) || (path === archivePath && /^(read|open|createReadStream)/.test(method))) {
    emit({ kind: "forbidden-access", method, path });
    throw Error("Installation attempted forbidden fixture access");
  }
}
for (const method of ["readFileSync", "openSync", "readSync", "statSync", "lstatSync", "accessSync", "existsSync", "realpathSync", "readlinkSync", "createReadStream", "readFile", "open", "read", "stat", "lstat", "access", "exists", "realpath", "readlink"]) {
  const original = fs[method];
  fs[method] = function (...args) { guard(method, args[0]); return original.apply(this, args); };
}
for (const method of ["readFile", "open", "stat", "lstat", "access", "realpath", "readlink"]) {
  const original = fs.promises[method];
  fs.promises[method] = async function (...args) { guard(method, args[0]); return original.apply(this, args); };
}
const link = fs.linkSync;
fs.linkSync = function (...args) {
  const destination = pathOf(args[1]);
  const result = link.apply(this, args);
  if (destination === failAfterPublish) {
    emit({ kind: "published-fault", path: destination });
    throw Error("Controlled failure after actual second-unit publication");
  }
  return result;
};
globalThis.fetch = async function () {
  emit({ kind: "acquisition-attempt" });
  throw Error("Unexpected installation acquisition");
};
syncBuiltinESMExports();
emit({ kind: "loaded" });
`);
  return {
    env: { NODE_OPTIONS: `--import ${preload}` },
    reset() { writeFileSync(eventsPath, ""); },
    events() { return readFileSync(eventsPath, "utf8").trim().split("\n").filter(Boolean).map(JSON.parse); },
  };
}

function readProjectFile(root, path) {
  return readFileSync(join(root, path), "utf8");
}

function assertNoInitMutation(root) {
  assert.deepEqual(listProject(root), []);
}

function assertNoStateFiles(root) {
  assert.equal(existsSync(join(root, "rigorloop.yaml")), false);
  assert.equal(existsSync(join(root, "rigorloop.lock")), false);
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
  const entries = options.entries ?? [
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

function fixturePackage(t, options = {}) {
  const root = mkdtempSync(join(tmpdir(), "rigorloop-package-test-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
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
  copyFileSync(
    join(packageRoot, "dist", "lib", "adapters.js"),
    join(root, "dist", "lib", "adapters.js"),
  );
  copyFileSync(
    join(packageRoot, "dist", "lib", "command-result.js"),
    join(root, "dist", "lib", "command-result.js"),
  );
  for (const file of [
    "installer-replacement.js",
    "cli-observability.js",
    "diagnostic-event.js",
    "log-config.js",
    "log-inspection.js",
    "log-sink.js",
    "result-renderer.js",
  ]) {
    copyFileSync(join(packageRoot, "dist", "lib", file), join(root, "dist", "lib", file));
  }
  copyFileSync(
    join(packageRoot, "dist", "lib", "official-archive-url.js"),
    join(root, "dist", "lib", "official-archive-url.js"),
  );

  if (options.metadata !== false) {
    const metadata =
      options.metadata ??
      JSON.parse(readFileSync(join(packageRoot, "dist", "metadata", metadataFile), "utf8"));
    const metadataContent =
      typeof metadata === "string" ? metadata : JSON.stringify(metadata, null, 2);
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
    const releaseIndex = options.releaseIndex ?? {
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
    writeFileSync(
      join(root, "dist", "metadata", "releases.json"),
      JSON.stringify(releaseIndex, null, 2),
    );
  }

  return { root, cliPath: join(root, "dist", "bin", "rigorloop.js") };
}

function runCliWithBundledMetadata(t, args, cwd, metadata, options = {}) {
  const packageFixture = fixturePackage(t, {
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

function mockFetchModule(t, archiveUrl, archiveBytes) {
  const path = join(tempProject(t), "mock-fetch.mjs");
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

function mockFetchFailureModule(t, archiveUrl, options = {}) {
  const path = join(tempProject(t), "mock-fetch-failure.mjs");
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

test("T1 package metadata exposes one public binary and publishable runtime policy", (t) => {
  assert.equal(packageJson.name, "@xiongxianfei/rigorloop");
  assert.equal(packageJson.private, undefined);
  assert.deepEqual(Object.keys(packageJson.bin), ["rigorloop"]);
  assert.equal(packageJson.bin.rigorloop, "dist/bin/rigorloop.js");
  assert.match(readFileSync(cliPath, "utf8"), /^#!\/usr\/bin\/env node\n/);
  assert.equal(packageJson.license, "MIT");
  assert.equal(existsSync(join(packageRoot, "LICENSE")), true);

  const files = packageJson.files ?? [];
  assert.deepEqual(files, ["dist/", "package.json", "README.md", "LICENSE"]);
  assert.ok(!files.some((entry) => entry.endsWith(".zip")));
  assert.ok(
    !files.some((entry) => entry === "dist/adapters/" || entry.startsWith("dist/adapters")),
  );

  const scripts = packageJson.scripts ?? {};
  for (const scriptName of ["preinstall", "install", "postinstall", "prepare", "prepack"]) {
    assert.equal(scripts[scriptName], undefined, scriptName);
  }
  assert.deepEqual(packageJson.dependencies ?? {}, { yaml: "2.9.0" });
});

test("TNP-005 source metadata preserves historical release identities", (t) => {
  // Current candidate metadata is produced by Release, in its isolated package.
  // Actual packed metadata/archive parity is covered by release_candidate_tests.
  const historicalMetadata = readFileSync(
    join(packageRoot, "dist", "metadata", "adapter-artifacts-v0.5.0.json"),
  );
  assert.equal(
    sha256(historicalMetadata),
    "74f2d940ce8ef358092609884e9377d0a3955c731e7f437ca63d995862227885",
  );
});

// M5-DOC-001: Package README coverage for multi-adapter init, runtime roots, local archive fallback, and proxy guidance.
test("M5-DOC-001 package README documents multi-adapter init and fallback boundaries", (t) => {
  const readme = readFileSync(join(packageRoot, "README.md"), "utf8");

  assert.match(readme, /rigorloop init codex\|claude/);
  assert.match(readme, /\.agents\/skills/);
  assert.match(readme, /\.claude\/skills/);
  assert.match(readme, /--from-archive/);
  assert.match(readme, /NODE_USE_ENV_PROXY|--use-env-proxy/);
  assert.doesNotMatch(readme, /\.codex\/skills/);
  assert.doesNotMatch(readme, /Undici|dispatcher/);
});

test("TMAI-001 descriptor registry defines the exact supported adapter set", (t) => {
  assert.deepEqual(supportedAdapterNames(), ["codex", "claude"]);
  assert.deepEqual(adapterDescriptor("codex").installRoots, { skills: ".agents/skills" });
  assert.deepEqual(adapterDescriptor("claude").installRoots, { skills: ".claude/skills" });
  assert.equal(adapterDescriptor("opencode"), undefined);
  assert.equal(
    adapterDescriptor("codex").archiveName(`v${publicPackageVersion}`),
    `rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
  );
  assert.equal(
    adapterDescriptor("claude").archiveName(`v${publicPackageVersion}`),
    `rigorloop-adapter-claude-v${publicPackageVersion}.zip`,
  );
  assert.equal(adapterDescriptor("cursor"), undefined);
});

test("T2 help output shows only the implemented command surface", (t) => {
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

test("T3 version output reports package identity", (t) => {
  const result = runCli(["version"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /@xiongxianfei\/rigorloop/);
  assert.match(result.stdout, new RegExp(publicPackageVersion.replaceAll(".", "\\.")));
});

test("T4 unknown commands return usage errors", (t) => {
  const result = runCli(["unknown-command"]);

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /Unknown command/);
  assert.match(`${result.stdout}${result.stderr}`, /rigorloop --help/);
});

test("TMAI-003 unsupported targets are blocked and do not write files", (t) => {
  const cwd = tempProject(t);
  const result = runCli(["init", "cursor", "--json"], { cwd });

  assert.equal(result.status, 2);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "target-unknown");
  assert.match(output.blockers[0].next_action, /codex, claude/);
  assertNoInitMutation(cwd);
});

test("TTNI-CLI-002 rejected alias targets fail before mutation", (t) => {
  for (const target of ["claude-code", "open-code", "openai", "codex-cli"]) {
    const cwd = tempProject(t);
    const result = runCli(["init", target, "--json"], { cwd });

    assert.equal(result.status, 2, target);
    assert.equal(result.stderr, "");
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "blocked", target);
    assert.equal(output.blockers[0].code, "target-unknown", target);
    assert.match(
      output.blockers[0].message,
      new RegExp(target.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")),
      target,
    );
    assert.match(output.blockers[0].next_action, /codex, claude/, target);
    assertNoInitMutation(cwd);
  }
});

test("TTNI-CLI-003 removed adapter syntax fails before mutation", (t) => {
  const cases = [
    ["init", "--adapter", "codex", "--json"],
    ["init", "--adapter", "codex", "claude", "--json"],
    ["init", "codex", "--adapter", "claude", "--json"],
  ];

  for (const args of cases) {
    const cwd = tempProject(t);
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

test("TMAI-001 dry-run selects descriptors for all supported adapters", (t) => {
  const cases = [
    ["codex", ".agents/skills", `rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    ["claude", ".claude/skills", `rigorloop-adapter-claude-v${publicPackageVersion}.zip`],
  ];

  for (const [adapter, root, archive] of cases) {
    const cwd = tempProject(t);
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

test("RT-R30 init rejects obsolete workflow skill installations for every target", (t) => {
  const cases = [
    ["codex", ".agents/skills"],
    ["claude", ".claude/skills"],
  ];

  for (const [adapter, root] of cases) {
    const cwd = tempProject(t);
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
    assert.match(
      output.blockers[0].next_action,
      /remove .*workflow.*install and invoke route/i,
      adapter,
    );
    assert.deepEqual(listProject(cwd), before, adapter);
    assert.equal(
      readProjectFile(cwd, `${root}/workflow/SKILL.md`),
      "# Obsolete workflow\n",
      adapter,
    );
  }
});

test("RT-R30 init rejects a mixed installed route and workflow inventory", (t) => {
  const cwd = tempProject(t);
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

test("RT-R30 init rejects an archive containing the obsolete workflow package", (t) => {
  const cwd = tempProject(t);
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
    t,
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

test("T6 JSON envelope is stable and stdout contains JSON only", (t) => {
  const cwd = tempProject(t);
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

test("T7 human output is not JSON-fragment output", (t) => {
  const cwd = tempProject(t);
  const result = runCli(["init", "codex", "--dry-run"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /RigorLoop init dry run/);
  assert.doesNotThrow(() => {
    assert.throws(() => JSON.parse(result.stdout));
  });
});

test("T8 quiet mode does not change JSON shape or behavior", (t) => {
  const cwd = tempProject(t);
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

test("T9 debug mode preserves stable top-level JSON fields", (t) => {
  const cwd = tempProject(t);
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

test("T10 color is disabled by flag and environment", (t) => {
  const withFlag = runCli(["--help", "--no-color"]);
  const withEnv = runCli(["--help"], { env: { NO_COLOR: "1" } });
  const ansiPattern = /\u001b\[[0-9;]*m/;

  assert.equal(withFlag.status, 0);
  assert.equal(withEnv.status, 0);
  assert.doesNotMatch(withFlag.stdout, ansiPattern);
  assert.doesNotMatch(withEnv.stdout, ansiPattern);
});

test("T11 exit-code mapping covers every public exit class", (t) => {
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

test("T12 default dry-run reports target and unperformed checks without state files", (t) => {
  const cwd = tempProject(t);
  const result = runCli(["init", "codex", "--dry-run", "--json"], { cwd });
  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.planned_target.install_root, ".agents/skills");
  assert.ok(output.unperformed_checks.includes("archive verification"));
  assertNoInitMutation(cwd);
  assert.equal(output.planned_manifest, undefined);
  assert.equal(output.planned_lockfile, undefined);
});

test("T13 init requires a target", (t) => {
  const cwd = tempProject(t);
  const result = runCli(["init"], { cwd });

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /codex, claude/);
  assert.deepEqual(listProject(cwd), []);
});

test("T14 missing local archive path is invalid input", (t) => {
  const cwd = tempProject(t);
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

test("TMAI-009 wrong local archive for selected adapter fails before extraction", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  fixture.metadata.artifacts.push({
    ...fixture.metadata.artifacts[0],
    adapter: "claude",
    archive: `rigorloop-adapter-claude-v${publicPackageVersion}.zip`,
    url: expectedArchiveUrl({
      releaseTag: `v${publicPackageVersion}`,
      archive: `rigorloop-adapter-claude-v${publicPackageVersion}.zip`,
    }),
    install_root: ".claude/skills",
  });
  const result = runCliWithBundledMetadata(
    t,
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

test("T15 network mode uses bundled metadata before downloading the official archive", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, {
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: sha256(
        Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8"),
      ),
    },
  });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: { NODE_OPTIONS: `--import ${mockFetchModule(t, officialUrl, archiveBytes)}` },
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assertNoStateFiles(cwd);
  assert.equal(output.artifacts[0].sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(
    readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"),
    "# Proposal\n\nUse proposal guidance.\n",
  );
});

test("TMAI-029 network mode downloads official archives for every supported adapter", (t) => {
  for (const adapter of supportedAdapterNames()) {
    const cwd = tempProject(t);
    const descriptor = adapterDescriptor(adapter);
    const fixture = fixtureArchive(cwd, { adapter, installRoot: descriptor.primaryInstallRoot() });
    const archiveBytes = readFileSync(fixture.archivePath);
    const officialUrl = expectedArchiveUrl({
      releaseTag: `v${publicPackageVersion}`,
      archive: fixture.archiveName,
    });
    fixture.metadata.artifacts[0].url = officialUrl;
    const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
    const result = runCli(["init", adapter, "--json"], {
      cwd,
      cliPath: packageFixture.cliPath,
      env: { NODE_OPTIONS: `--import ${mockFetchModule(t, officialUrl, archiveBytes)}` },
    });

    assert.equal(result.status, 0, adapter);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "success", adapter);
    assert.equal(output.planned_target.target, adapter);
    assertNoStateFiles(cwd);
  }
});

test("TMAI-029 network failure reports bounded proxy diagnostics in JSON", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchFailureModule(t, officialUrl, {
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
  assert.match(
    output.diagnostics.node_env_proxy_status,
    /^(enabled|disabled|unsupported|unknown)$/,
  );
  assert.deepEqual(output.diagnostics.proxy_env_vars_detected, [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "http_proxy",
  ]);
  assert.match(output.blockers[0].next_action, /--from-archive/);
  assertRedacted(JSON.stringify(output));
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("TMAI-030 proxy diagnostic enums and env-var allowlist are stable", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
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
      NODE_OPTIONS: `--import ${mockFetchFailureModule(t, officialUrl, { message: "proxy connection failed", code: "ERR_PROXY_CONNECTION_FAILED" })}`,
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
  assert.match(
    output.diagnostics.node_env_proxy_status,
    /^(enabled|disabled|unsupported|unknown)$/,
  );
  assert.match(
    output.diagnostics.download_failure_class,
    /^(dns|tls|timeout|http-status|proxy|network|unknown)$/,
  );
  assert.equal(JSON.stringify(output).includes("ALL_PROXY"), false);
  assert.equal(JSON.stringify(output).includes("not-allowed.example.invalid"), false);
});

test("CR-M4-R1-F1 node_env_proxy_status reports enabled with --use-env-proxy", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
  const result = spawnSync(
    process.execPath,
    [
      "--use-env-proxy",
      "--import",
      mockFetchFailureModule(t, officialUrl, {
        message: "proxy connection failed",
        code: "ERR_PROXY_CONNECTION_FAILED",
      }),
      packageFixture.cliPath,
      "init",
      "codex",
      "--json",
    ],
    {
      cwd,
      env: {
        ...process.env,
        RIGORLOOP_LOG_DIR: join(cwd, "logs"),
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

test("TMAI-031 human proxy failure output is actionable and redacted", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
  const result = runCli(["init", "codex"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchFailureModule(t, officialUrl, { message: "proxy refused private.proxy.internal", code: "ERR_PROXY_CONNECTION_FAILED" })}`,
    },
  });

  assert.equal(result.status, 2);
  assert.equal(result.stdout, "");
  assert.match(result.stderr, /adapter codex/);
  assert.match(
    result.stderr,
    new RegExp(`release v${publicPackageVersion.replaceAll(".", "\\.")}`),
  );
  assert.match(result.stderr, /failure class proxy/);
  assert.match(result.stderr, new RegExp(officialUrl.replaceAll(".", "\\.")));
  assert.match(result.stderr, /--from-archive/);
  assertRedacted(result.stderr);
});

test("TMAI-032 proxy diagnostics do not mask archive verification failures", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const wrongArchiveBytes = Buffer.from(readFileSync(fixture.archivePath));
  wrongArchiveBytes[wrongArchiveBytes.length - 1] =
    wrongArchiveBytes[wrongArchiveBytes.length - 1] ^ 0xff;
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      ...sensitiveProxyEnv(),
      NODE_OPTIONS: `--import ${mockFetchModule(t, officialUrl, wrongArchiveBytes)}`,
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

test("T15 network mode rejects non-official archive URLs before fetch", (t) => {
  const cases = [
    ["data URL", "data:application/octet-stream;base64,AAAA"],
    ["wrong host", `https://example.com/rigorloop-adapter-codex-v${publicPackageVersion}.zip`],
    [
      "wrong owner",
      `https://github.com/other/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
    ],
    [
      "wrong release",
      `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.2/rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
    ],
    [
      "wrong archive",
      `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/other.zip`,
    ],
    [
      "query",
      `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip?download=1`,
    ],
    [
      "hash",
      `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip#fragment`,
    ],
    [
      "http",
      `http://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
    ],
    [
      "raw",
      `https://raw.githubusercontent.com/xiongxianfei/rigorloop/v${publicPackageVersion}/rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
    ],
  ];

  for (const [name, url] of cases) {
    const cwd = tempProject(t);
    const fixture = fixtureArchive(cwd);
    fixture.metadata.artifacts[0].url = url;
    const result = runCliWithBundledMetadata(t, ["init", "codex", "--json"], cwd, fixture.metadata);
    assert.equal(result.status, 3, name);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "error", name);
    assert.equal(output.errors[0].code, "non-official-archive-url", name);
    assert.equal(output.errors[0].path, "metadata.artifacts[codex].url", name);
    assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false, name);
  }
});

test("T15 official archive URL helper accepts only exact release archive URLs", (t) => {
  const releaseTag = `v${publicPackageVersion}`;
  for (const adapter of supportedAdapterNames()) {
    const archive = adapterDescriptor(adapter).archiveName(releaseTag);
    const officialUrl = expectedArchiveUrl({ releaseTag, archive });
    assert.equal(
      officialUrl,
      `https://github.com/xiongxianfei/rigorloop/releases/download/v${publicPackageVersion}/${archive}`,
    );
    assert.deepEqual(validateOfficialArchiveUrl({ url: officialUrl, releaseTag, archive }), {
      ok: true,
    });
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

test("T16 bundled metadata hash verification uses the bundled release index", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  fixture.metadata.artifacts[0].url = `data:application/octet-stream;base64,${archiveBytes.toString("base64")}`;
  const packageFixture = fixturePackage(t, {
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

test("T16 bundled metadata bytes are verified before parsing", (t) => {
  const cwd = tempProject(t);
  const packageFixture = fixturePackage(t, {
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

test("T16 missing metadata trust root blocks network install", (t) => {
  const cwd = tempProject(t);
  const packageFixture = fixturePackage(t, {
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

test("T16 runtime release metadata environment override is ignored", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({
    releaseTag: `v${publicPackageVersion}`,
    archive: fixture.archiveName,
  });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage(t, {
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: `v${publicPackageVersion}`,
      bundled_metadata: `adapter-artifacts-v${publicPackageVersion}.json`,
      bundled_metadata_sha256: sha256(
        Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8"),
      ),
    },
  });

  const result = runCli(["init", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: {
      NODE_OPTIONS: `--import ${mockFetchModule(t, officialUrl, archiveBytes)}`,
      RIGORLOOP_RELEASE_METADATA_URL: "http://127.0.0.1:9/attacker.json",
    },
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(
    readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"),
    "# Proposal\n\nUse proposal guidance.\n",
  );
});

test("T17 incompatible local archive release is blocked", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd, { archiveName: "rigorloop-adapter-codex-v0.1.2.zip" });
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "release-version-incompatible");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T18 local archive mode uses bundled metadata and no metadata flag", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.artifacts[0].sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(output.artifacts[0].tree_sha256, fixture.metadata.artifacts[0].tree_sha256);
  assert.equal(
    readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"),
    "# Proposal\n\nUse proposal guidance.\n",
  );
  assert.doesNotMatch(result.stdout, /metadata/);
});

test("T18 runtime local metadata environment override is ignored", (t) => {
  const cwd = tempProject(t);
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
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
    { env: { RIGORLOOP_METADATA_FILE: attackerMetadataPath } },
  );

  assert.equal(result.status, 0, result.stderr);
  assert.equal(
    readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"),
    "# Proposal\n\nUse proposal guidance.\n",
  );
});

test("T19 missing bundled metadata blocks local archive install", (t) => {
  const cwd = tempProject(t);
  const archive = createZip([
    {
      name: ".agents/skills/proposal/SKILL.md",
      bytes: Buffer.from("# Proposal\n", "utf8"),
    },
  ]);
  writeFileSync(join(cwd, `rigorloop-adapter-codex-v${publicPackageVersion}.zip`), archive);
  const packageFixture = fixturePackage(t, { metadata: false });
  const result = runCli(
    [
      "init",
      "codex",
      "--from-archive",
      `./rigorloop-adapter-codex-v${publicPackageVersion}.zip`,
      "--json",
    ],
    {
      cwd,
      cliPath: packageFixture.cliPath,
    },
  );

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "metadata-unavailable");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("TTNI-INST-001 default init installs single-root targets without state files", (t) => {
  const cases = [
    { adapter: "codex", root: ".agents/skills" },
    { adapter: "claude", root: ".claude/skills" },
  ];

  for (const { adapter, root } of cases) {
    const cwd = tempProject(t);
    const fixture = fixtureArchive(cwd, { adapter, installRoot: root });
    const result = runCliWithBundledMetadata(
      t,
      ["init", adapter, "--from-archive", `./${fixture.archiveName}`, "--json"],
      cwd,
      fixture.metadata,
    );

    assert.equal(result.status, 0, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "success", adapter);
    assert.equal(output.state_files.action, "skipped", adapter);
    assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false, adapter);
    assert.equal(existsSync(join(cwd, "rigorloop.lock")), false, adapter);
    assert.equal(
      readProjectFile(cwd, `${root}/proposal/SKILL.md`),
      "# Proposal\n\nUse proposal guidance.\n",
      adapter,
    );
    assert.equal(
      readProjectFile(cwd, `${root}/verify/SKILL.md`),
      "# Verify\n\nUse verify guidance.\n",
      adapter,
    );
  }
});

test("T26 overwrite conflicts are refused without replacing user files", (t) => {
  const cwd = tempProject(t);
  writeFileSync(join(cwd, ".agents"), "user file\n");
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", fixture.archivePath, "--json", "--force"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.ok(output.blockers.length);
});

test("T26 leaf install-root file conflict is refused without replacing user files", (t) => {
  const cwd = tempProject(t);
  mkdirSync(join(cwd, ".agents"));
  writeFileSync(join(cwd, ".agents", "skills"), "user file\n");
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", fixture.archivePath, "--json", "--force"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents/skills"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.ok(output.blockers.length);
});

test("T26 existing adapter files cause destination conflicts without replacing user files", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "proposal"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), "user file\n");
  const result = runCliWithBundledMetadata(
    t,
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

test("T29 release metadata shape and validation result are validated", (t) => {
  const cwd = tempProject(t);
  const wrongRepo = fixtureArchive(cwd, {
    metadata(metadata) {
      metadata.release.source_repository = "example/not-rigorloop";
      return metadata;
    },
  });
  const wrongRepoResult = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${wrongRepo.archiveName}`, "--json"],
    cwd,
    wrongRepo.metadata,
  );

  assert.equal(wrongRepoResult.status, 3);
  assert.equal(JSON.parse(wrongRepoResult.stdout).errors[0].code, "metadata-invalid");

  const missingFieldProject = tempProject(t);
  const missingField = fixtureArchive(missingFieldProject, {
    metadata(metadata) {
      delete metadata.metadata.sha256;
      return metadata;
    },
  });
  const missingFieldResult = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${missingField.archiveName}`, "--json"],
    missingFieldProject,
    missingField.metadata,
  );

  assert.equal(missingFieldResult.status, 3);
  assert.equal(JSON.parse(missingFieldResult.stdout).errors[0].code, "metadata-invalid");

  const noCodexProject = tempProject(t);
  const noCodex = fixtureArchive(noCodexProject, {
    metadata(metadata) {
      metadata.artifacts[0].adapter = "claude";
      return metadata;
    },
  });
  const noCodexResult = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${noCodex.archiveName}`, "--json"],
    noCodexProject,
    noCodex.metadata,
  );

  assert.equal(noCodexResult.status, 2);
  assert.equal(JSON.parse(noCodexResult.stdout).blockers[0].code, "metadata-unavailable");

  const wrongRootProject = tempProject(t);
  const wrongRoot = fixtureArchive(wrongRootProject, {
    metadata(metadata) {
      metadata.artifacts[0].install_root = ".codex/skills";
      return metadata;
    },
  });
  const wrongRootResult = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${wrongRoot.archiveName}`, "--json"],
    wrongRootProject,
    wrongRoot.metadata,
  );

  assert.equal(wrongRootResult.status, 3);
  assert.equal(JSON.parse(wrongRootResult.stdout).errors[0].code, "metadata-invalid");

  const validationFailProject = tempProject(t);
  const validationFail = fixtureArchive(validationFailProject, {
    metadata(metadata) {
      metadata.validation.result = "fail";
      return metadata;
    },
  });
  const validationFailResult = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${validationFail.archiveName}`, "--json"],
    validationFailProject,
    validationFail.metadata,
  );

  assert.equal(validationFailResult.status, 3);
  assert.equal(JSON.parse(validationFailResult.stdout).errors[0].code, "metadata-invalid");
});

test("T30 archive traversal paths are rejected", (t) => {
  const parent = tempProject(t);
  const cwd = join(parent, "project");
  mkdirSync(cwd);
  writeFileSync(join(parent, "escape.txt"), "existing parent file\n");
  const snapshot = () =>
    readdirSync(parent, { recursive: true })
      .sort()
      .map((path) => {
        const absolute = join(parent, path);
        return [
          path,
          lstatSync(absolute).isDirectory() ? null : readFileSync(absolute).toString("base64"),
        ];
      });
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "../escape.txt", bytes: Buffer.from("escape\n", "utf8") }],
  });
  const before = snapshot();
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-path-traversal");
  assert.deepEqual(snapshot(), before);
});

test("T31 archive entries must remain under .agents/skills", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "proposal/SKILL.md", bytes: Buffer.from("# Proposal\n", "utf8") }],
  });
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-install-root-invalid");

  const supportProject = tempProject(t);
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
    t,
    ["init", "codex", "--from-archive", `./${supportFixture.archiveName}`, "--json"],
    supportProject,
    supportFixture.metadata,
  );

  assert.equal(supportResult.status, 0, supportResult.stderr);
  assert.equal(existsSync(join(supportProject, "AGENTS.md")), false);
  assert.equal(readProjectFile(supportProject, ".agents/skills/proposal/SKILL.md"), "# Proposal\n");
});

test("T33 symlink archive entries are rejected", (t) => {
  const cwd = tempProject(t);
  const fixture = fixtureArchive(cwd, {
    entries: [
      {
        name: ".agents/skills/proposal/SKILL.md",
        bytes: Buffer.from("target", "utf8"),
        externalAttributes: 0o120777 << 16,
      },
    ],
  });
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-symlink-entry");
});

test("T34 archive verification failures use exit code 3", (t) => {
  const checksumProject = tempProject(t);
  const checksumFixture = fixtureArchive(checksumProject, {
    metadata(metadata) {
      metadata.artifacts[0].sha256 = "0".repeat(64);
      return metadata;
    },
  });
  const checksum = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${checksumFixture.archiveName}`, "--json"],
    checksumProject,
    checksumFixture.metadata,
  );
  assert.equal(checksum.status, 3);
  assert.equal(JSON.parse(checksum.stdout).errors[0].code, "archive-sha-mismatch");

  const sizeProject = tempProject(t);
  const sizeFixture = fixtureArchive(sizeProject, {
    metadata(metadata) {
      metadata.artifacts[0].size_bytes += 1;
      return metadata;
    },
  });
  const size = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${sizeFixture.archiveName}`, "--json"],
    sizeProject,
    sizeFixture.metadata,
  );
  assert.equal(size.status, 3);
  assert.equal(JSON.parse(size.stdout).errors[0].code, "archive-size-mismatch");

  const treeProject = tempProject(t);
  const treeFixture = fixtureArchive(treeProject, {
    metadata(metadata) {
      metadata.artifacts[0].tree_sha256 = "f".repeat(64);
      return metadata;
    },
  });
  const tree = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", `./${treeFixture.archiveName}`, "--json"],
    treeProject,
    treeFixture.metadata,
  );
  assert.equal(tree.status, 3);
  assert.equal(JSON.parse(tree.stdout).errors[0].code, "tree-hash-mismatch");
});

test("DIST independent tree representation and unknown algorithm precedence", (t) => {
  for (const [target, root] of [["codex", ".agents/skills"], ["claude", ".claude/skills"]]) {
    for (const algorithm of ["rigorloop-tree-hash-v2", "rigorloop-tree-hash-v1", undefined]) {
      const cwd = tempProject(t);
      // Literal manifest order, independent of both hashing implementations.
      // V1 preserves a previously agreeing Unicode pair; v2 covers the formerly
      // divergent punctuation, case ties and unnormalized Unicode byte order.
      const names = algorithm === "rigorloop-tree-hash-v2"
        ? ["A.md", "Z.md", "a-b.md", "a.md", "a_b.md", "c.bin", "e\u0301.md", "t.md", "ß.md", "é.md", "İ.md"]
        : ["ß.md", "t.md"];
      const normalized = names.map(name => [`proposal/${name}`, name === "c.bin"
        ? Buffer.from([0xef, 0xbb, 0xbf, 0, 13, 10, 255]) : Buffer.from("Text\nkeep  \n")]);
      const selected = algorithm ?? "rigorloop-tree-hash-v1";
      const expected = sha256(Buffer.from(`${selected}\n` + normalized
        .map(([path, bytes]) => `${path}\t${sha256(bytes)}\n`).join("")));
      const fixture = fixtureArchive(cwd, { adapter: target, installRoot: root,
        entries: [...normalized].reverse().map(([path, bytes]) => ({ name: `${root}/${path}`,
          bytes: path.endsWith(".md") ? Buffer.from("\ufeffText\r\nkeep  \r") : bytes })),
        metadata(metadata) {
          metadata.artifacts[0].tree_sha256 = expected;
          metadata.artifacts[0].file_count = normalized.length;
          if (algorithm === undefined) delete metadata.artifacts[0].tree_hash_algorithm;
          else metadata.artifacts[0].tree_hash_algorithm = algorithm;
          return metadata;
        },
      });
      const args = ["init", target, "--from-archive", `./${fixture.archiveName}`, "--force", "--json"];
      const valid = runCliWithBundledMetadata(t, args, cwd, fixture.metadata);
      assert.equal(valid.status, 0, valid.stdout + valid.stderr);
      for (const [path, bytes] of normalized) assert.deepEqual(readFileSync(join(cwd, root, path)), bytes);
      const before = projectSnapshot(cwd);
      for (const unknownValue of ["unknown_value", ""]) {
        const invalid = structuredClone(fixture.metadata);
        invalid.artifacts[0].tree_hash_algorithm = unknownValue;
        invalid.artifacts[0].tree_sha256 = "0".repeat(64);
        const unknown = runCliWithBundledMetadata(t, args, cwd, invalid);
        assert.equal(unknown.status, 3, unknown.stdout + unknown.stderr);
        assert.equal(JSON.parse(unknown.stdout).errors[0].code, "metadata-invalid");
        assert.equal(JSON.parse(unknown.stdout).errors[0].message, "Unsupported tree hash algorithm in adapter metadata.");
        invalid.artifacts[0].tree_hash_algorithm = selected;
        const inconsistent = runCliWithBundledMetadata(t, args, cwd, invalid);
        assert.equal(inconsistent.status, 3, inconsistent.stdout + inconsistent.stderr);
        assert.equal(JSON.parse(inconsistent.stdout).errors[0].code, "tree-hash-mismatch");
        assert.deepEqual(projectSnapshot(cwd), before);
      }
    }
  }
});

for (const [target, installRoot] of [
  ["codex", ".agents/skills"],
  ["claude", ".claude/skills"],
]) {
  test(`DIST conflict preflight and force preserve unrelated content and ignore state: ${target}`, (t) => {
    const cwd = tempProject(t);
    const fixture = fixtureArchive(cwd, { adapter: target, installRoot });
    const args = ["init", target, "--from-archive", `./${fixture.archiveName}`, "--json"];
    writeFileSync(join(cwd, "rigorloop.yaml"), "not: [yaml");
    symlinkSync(join(cwd, "missing-state-target"), join(cwd, "rigorloop.lock"));
    const probe = installationProbe(t, {
      statePaths: [join(cwd, "rigorloop.yaml"), join(cwd, "rigorloop.lock")],
    });
    let result = runCliWithBundledMetadata(t, args, cwd, fixture.metadata, { env: probe.env });
    assert.equal(result.status, 0, result.stdout + result.stderr);
    assert.deepEqual(probe.events(), [{ kind: "loaded" }], "fresh install inspected state");
    const first = fixture.entries.find(
      (e) => e.name.startsWith(`${installRoot}/`) && !e.directory,
    ).name;
    const unit = `${installRoot}/${first.slice(installRoot.length + 1).split("/")[0]}`;
    writeFileSync(join(cwd, unit, "obsolete.txt"), "local edit");
    mkdirSync(join(cwd, installRoot, "unrelated"));
    writeFileSync(join(cwd, installRoot, "unrelated", "keep"), "keep");
    const beforeConflict = projectSnapshot(cwd);
    probe.reset();
    result = runCliWithBundledMetadata(t, args, cwd, fixture.metadata, { env: probe.env });
    assert.equal(result.status, 5, result.stdout + result.stderr);
    assert.ok(JSON.parse(result.stdout).blockers.some((b) => b.path === unit));
    assert.deepEqual(probe.events(), [{ kind: "loaded" }], "conflict inspected state");
    assert.deepEqual(projectSnapshot(cwd), beforeConflict);
    probe.reset();
    result = runCliWithBundledMetadata(t, [...args, "--force"], cwd, fixture.metadata, { env: probe.env });
    assert.equal(result.status, 0, result.stdout + result.stderr);
    assert.deepEqual(probe.events(), [{ kind: "loaded" }], "force inspected state");
    assert.equal(existsSync(join(cwd, unit, "obsolete.txt")), false);
    assert.equal(readFileSync(join(cwd, installRoot, "unrelated", "keep"), "utf8"), "keep");
    assert.equal(readFileSync(join(cwd, "rigorloop.yaml"), "utf8"), "not: [yaml");
    assert.ok(lstatSync(join(cwd, "rigorloop.lock")).isSymbolicLink());
    assert.equal(readlinkSync(join(cwd, "rigorloop.lock")), join(cwd, "missing-state-target"));
    assert.ok(JSON.parse(result.stdout).retained.length > 0);
  });

  test(`DIST dry-run observes no acquisition or project mutation: ${target}`, (t) => {
    // Network/default and local/force retain both acquisition boundaries without
    // multiplying equivalent archive-verification scenarios.
    for (const local of [false, true]) {
      const cwd = tempProject(t);
      const fixture = fixtureArchive(cwd, {
        adapter: target,
        installRoot,
        metadata(metadata) {
          metadata.artifacts[0].skill_names = ["proposal", "verify"];
          return metadata;
        },
      });
      mkdirSync(join(cwd, installRoot, "proposal"), { recursive: true });
      writeFileSync(join(cwd, installRoot, "proposal", "local.md"), "preserve local change");
      mkdirSync(join(cwd, installRoot, "unrelated"));
      writeFileSync(join(cwd, installRoot, "unrelated", "keep"), "unrelated");
      writeFileSync(join(cwd, "rigorloop.yaml"), "malformed: [");
      symlinkSync(join(cwd, "missing-state"), join(cwd, "rigorloop.lock"));
      const probe = installationProbe(t, {
        archivePath: fixture.archivePath,
        statePaths: [join(cwd, "rigorloop.yaml"), join(cwd, "rigorloop.lock")],
      });
      const before = projectSnapshot(cwd);
      const args = ["init", target, "--dry-run", ...(local ? ["--from-archive", fixture.archivePath, "--force"] : ["--json"])];
      const result = runCliWithBundledMetadata(t, args, cwd, fixture.metadata, { env: probe.env });
      assert.equal(result.status, 0, result.stdout + result.stderr);
      assert.deepEqual(probe.events(), [{ kind: "loaded" }], "dry-run acquired an archive or inspected state");
      assert.deepEqual(projectSnapshot(cwd), before, "dry-run changed private project content");
      if (local) {
        assert.equal(result.stderr, "");
        assert.match(result.stdout, /archive verification and complete destination preflight are unperformed/);
        assert.ok(result.stdout.includes(`replace: ${installRoot}/proposal`));
        assert.ok(result.stdout.includes(`create: ${installRoot}/verify`));
        assert.match(result.stdout, /Local changes within replaced skill directories will be lost/);
      } else {
        const output = parseJsonResult(result);
        assert.equal(output.status, "success");
        assert.deepEqual(output.preliminary_conflicts, [`${installRoot}/proposal`]);
        assert.deepEqual(output.completed, []);
        assert.deepEqual(output.retained, []);
        assert.deepEqual(output.unperformed_checks, ["archive acquisition", "archive verification", "complete candidate preflight"]);
        assert.deepEqual(output.actions.map(({ path, action, status }) => ({ path, action, status })), [
          { path: `${installRoot}/proposal`, action: "conflict", status: "planned" },
          { path: `${installRoot}/verify`, action: "create", status: "planned" },
        ]);
        assert.equal(output.state_files.action, "skipped");
      }
    }
  });

  for (const format of ["json", "human"]) {
    test(`DIST public partial installation and retry preserve actual state: ${target} ${format}`, (t) => {
      const cwd = tempProject(t);
      const first = `${installRoot}/a`;
      const partial = `${installRoot}/design`;
      const untouched = `${installRoot}/z`;
      const entries = [
        { name: `${first}/SKILL.md`, bytes: Buffer.from("first\n") },
        { name: `${partial}/SKILL.md`, bytes: Buffer.from("second\n") },
        { name: `${partial}/resource.md`, bytes: Buffer.from("resource\n") },
        { name: `${untouched}/SKILL.md`, bytes: Buffer.from("last\n") },
      ];
      const fixture = fixtureArchive(cwd, { adapter: target, installRoot, entries });
      const packageFixture = fixturePackage(t, { metadata: fixture.metadata });
      mkdirSync(join(cwd, partial), { recursive: true });
      writeFileSync(join(cwd, partial, "old.md"), "retained original\n");
      mkdirSync(join(cwd, installRoot, "unrelated"));
      writeFileSync(join(cwd, installRoot, "unrelated", "keep"), "unrelated\n");
      writeFileSync(join(cwd, "rigorloop.yaml"), "invalid: [");
      symlinkSync(join(cwd, "missing-state"), join(cwd, "rigorloop.lock"));
      const statePaths = [join(cwd, "rigorloop.yaml"), join(cwd, "rigorloop.lock")];
      const fault = installationProbe(t, { statePaths, failAfterPublish: join(cwd, partial, "SKILL.md") });
      const args = ["init", target, "--from-archive", fixture.archivePath, ...(format === "json" ? ["--json"] : [])];
      const result = runCli([...args, "--force"], { cwd, cliPath: packageFixture.cliPath, env: fault.env });
      assert.equal(result.status, 5, result.stdout + result.stderr);
      assert.deepEqual(fault.events(), [
        { kind: "loaded" },
        { kind: "published-fault", path: join(cwd, partial, "SKILL.md") },
      ]);
      let output;
      if (format === "json") {
        output = parseJsonResult(result);
        assert.equal(output.schema_version, 1);
        assert.equal(output.command, "init");
        assert.equal(output.status, "blocked");
        assert.equal(output.blockers[0].code, "partial-installation-failed");
        assert.match(output.blockers[0].next_action, /Preserve partial files and retained originals/);
      } else {
        assert.equal(result.stdout, "");
        const lines = result.stderr.trim().split("\n");
        assert.deepEqual(lines.slice(0, -1), ["Controlled failure after actual second-unit publication"]);
        output = JSON.parse(lines.at(-1));
      }
      assert.deepEqual(output.completed, [first]);
      assert.equal(output.failed, partial);
      assert.deepEqual(output.untouched, [untouched]);
      assert.equal(readProjectFile(cwd, `${first}/SKILL.md`), "first\n");
      assert.equal(readProjectFile(cwd, `${partial}/SKILL.md`), "second\n");
      assert.deepEqual(readdirSync(join(cwd, partial)), ["SKILL.md"]);
      assert.equal(existsSync(join(cwd, untouched)), false);
      assert.equal(output.retained.length, 1);
      assert.equal(output.retained[0].path, partial);
      const backup = output.retained[0].backup;
      assert.equal(resolve(backup), backup);
      assert.ok(backup.startsWith(`${cwd}/.rigorloop-install-retained-`));
      assert.ok(!backup.slice(cwd.length).includes("/skills/"));
      assert.deepEqual(readdirSync(backup), ["old.md"]);
      assert.equal(readFileSync(join(backup, "old.md"), "utf8"), "retained original\n");
      // The injected error follows the real hardlink, before scratch unlink.
      // Preserve that allowed private candidate as well as the retained original.
      const retention = resolve(backup, "..");
      const retainedBeforeRetry = projectSnapshot(retention);
      const staged = readdirSync(retention).filter(name => name.startsWith("candidate-"));
      assert.equal(staged.length, 1);
      assert.equal(readFileSync(join(retention, staged[0]), "utf8"), "second\n");
      assert.equal(lstatSync(join(retention, staged[0])).ino, lstatSync(join(cwd, partial, "SKILL.md")).ino);

      const retryProbe = installationProbe(t, { statePaths });
      const beforeRetry = projectSnapshot(cwd);
      const retry = runCli(args, { cwd, cliPath: packageFixture.cliPath, env: retryProbe.env });
      assert.equal(retry.status, 5, retry.stdout + retry.stderr);
      assert.deepEqual(retryProbe.events(), [{ kind: "loaded" }]);
      if (format === "json") {
        const rejected = parseJsonResult(retry);
        assert.deepEqual(rejected.blockers.map(({ code, path }) => ({ code, path })), [
          { code: "destination-conflict", path: first },
          { code: "destination-conflict", path: partial },
        ]);
      } else {
        assert.match(retry.stderr, /Installation stopped: destination skills already exist/);
        assert.ok(retry.stderr.includes(first));
        assert.ok(retry.stderr.includes(partial));
      }
      assert.deepEqual(projectSnapshot(cwd), beforeRetry);
      retryProbe.reset();
      const forced = runCli([...args, "--force"], { cwd, cliPath: packageFixture.cliPath, env: retryProbe.env });
      assert.equal(forced.status, 0, forced.stdout + forced.stderr);
      assert.deepEqual(retryProbe.events(), [{ kind: "loaded" }]);
      for (const entry of entries) assert.equal(readProjectFile(cwd, entry.name), entry.bytes.toString());
      assert.deepEqual(readdirSync(join(cwd, partial)).sort(), ["SKILL.md", "resource.md"]);
      assert.equal(readProjectFile(cwd, `${installRoot}/unrelated/keep`), "unrelated\n");
      assert.equal(readProjectFile(cwd, "rigorloop.yaml"), "invalid: [");
      assert.equal(readlinkSync(join(cwd, "rigorloop.lock")), join(cwd, "missing-state"));
      assert.deepEqual(projectSnapshot(retention), retainedBeforeRetry);
      if (format === "json") {
        const completed = parseJsonResult(forced);
        assert.equal(completed.status, "success");
        assert.deepEqual(completed.completed, [first, partial, untouched]);
        assert.deepEqual(completed.actions.map(({ path, action }) => ({ path, action })), [
          { path: first, action: "replace" },
          { path: partial, action: "replace" },
          { path: untouched, action: "create" },
        ]);
        assert.deepEqual(completed.retained.map(({ path }) => path), [first, partial]);
        assert.equal(completed.state_files.action, "skipped");
      } else {
        assert.equal(forced.stderr, "");
        assert.ok(forced.stdout.includes(`replace: ${first}`));
        assert.ok(forced.stdout.includes(`replace: ${partial}`));
        assert.ok(forced.stdout.includes(`create: ${untouched}`));
        assert.match(forced.stdout, /Local changes within replaced skill directories will be lost/);
      }
    });
  }
}
test("DIST retired state flag and OpenCode reject even with force before acquisition", (t) => {
  for (const args of [
    ["init", "codex", "--write-state"],
    ["init", "opencode"],
    ["init", "opencode", "--from-archive", "missing.zip"],
  ]) {
    const cwd = tempProject(t);
    const result = runCli([...args, "--force", "--json"], { cwd });
    assert.equal(result.status, 2, result.stdout + result.stderr);
    assertNoInitMutation(cwd);
  }
});

test("DIST all candidate conflicts are reported before absent units are installed", (t) => {
  const cwd = tempProject(t);
  const entries = ["a", "b", "c"].map((name) => ({
    name: `.agents/skills/${name}/SKILL.md`,
    bytes: Buffer.from(name),
  }));
  const fixture = fixtureArchive(cwd, { entries });
  mkdirSync(join(cwd, ".agents/skills/a"), { recursive: true });
  mkdirSync(join(cwd, ".agents/skills/c"));
  writeFileSync(join(cwd, ".agents/skills/c/SKILL.md"), "c");
  const result = runCliWithBundledMetadata(
    t,
    ["init", "codex", "--from-archive", fixture.archiveName, "--json"],
    cwd,
    fixture.metadata,
  );
  assert.equal(result.status, 5, result.stdout + result.stderr);
  assert.deepEqual(
    JSON.parse(result.stdout).blockers.map((b) => b.path),
    [".agents/skills/a", ".agents/skills/c"],
  );
  assert.equal(existsSync(join(cwd, ".agents/skills/b")), false);
});

test("DIST retired authoring guards preserve installed and candidate entries even with force", (t) => {
  for (const skill of ["spec", "architecture"])
    for (const installed of [false, true]) {
      const cwd = tempProject(t);
      const fixture = fixtureArchive(
        cwd,
        installed
          ? {}
          : {
              entries: [
                { name: `.agents/skills/${skill}/SKILL.md`, bytes: Buffer.from("retired") },
              ],
            },
      );
      if (installed) {
        mkdirSync(join(cwd, `.agents/skills/${skill}`), { recursive: true });
        writeFileSync(join(cwd, `.agents/skills/${skill}/SKILL.md`), "local");
      }
      const result = runCliWithBundledMetadata(
        t,
        ["init", "codex", "--from-archive", fixture.archiveName, "--force", "--json"],
        cwd,
        fixture.metadata,
      );
      assert.equal(result.status, 2, result.stdout + result.stderr);
      assert.equal(
        JSON.parse(result.stdout).blockers[0].code,
        installed ? "retired-authoring-installation" : "retired-authoring-candidate",
      );
      if (installed)
        assert.equal(readFileSync(join(cwd, `.agents/skills/${skill}/SKILL.md`), "utf8"), "local");
      else assert.equal(existsSync(join(cwd, ".agents")), false);
    }
});
