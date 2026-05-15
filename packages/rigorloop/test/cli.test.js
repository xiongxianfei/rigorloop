import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { exitCodeForResult } from "../dist/lib/command-result.js";

const packageRoot = resolve(import.meta.dirname, "..");
const packageJsonPath = join(packageRoot, "package.json");
const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
const cliPath = join(packageRoot, packageJson.bin.rigorloop);

function runCli(args, options = {}) {
  return spawnSync(process.execPath, [options.cliPath ?? cliPath, ...args], {
    cwd: options.cwd ?? packageRoot,
    env: { ...process.env, ...(options.env ?? {}) },
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

function treeHashForEntries(entries) {
  const rows = entries
    .filter((entry) => !entry.directory && entry.name.startsWith(".agents/skills/"))
    .map((entry) => {
      const relativePath = entry.name.slice(".agents/skills/".length);
      const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
      return [relativePath, sha256(bytes)];
    })
    .sort(([left], [right]) => left.localeCompare(right));
  const manifest = `rigorloop-tree-hash-v1\n${rows.map(([path, hash]) => `${path}\t${hash}`).join("\n")}\n`;
  return sha256(Buffer.from(manifest, "utf8"));
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
  const archiveName = options.archiveName ?? "rigorloop-adapter-codex-v0.1.3.zip";
  const entries =
    options.entries ?? [
      {
        name: ".agents/skills/proposal/SKILL.md",
        bytes: Buffer.from("# Proposal\n\nUse proposal guidance.\r\n", "utf8"),
      },
      {
        name: ".agents/skills/verify/SKILL.md",
        bytes: Buffer.from("# Verify\n\nUse verify guidance.\n", "utf8"),
      },
    ];
  const archiveBytes = options.archiveBytes ?? createZip(entries);
  const archivePath = join(projectRoot, archiveName);
  writeFileSync(archivePath, archiveBytes);

  const metadata = {
    schema_version: 1,
    release: {
      version: "v0.1.3",
      source_repository: "xiongxianfei/rigorloop",
      source_commit: "0123456789abcdef0123456789abcdef01234567",
      release_tag: "v0.1.3",
      published_at: "2026-05-15",
    },
    metadata: {
      url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/adapter-artifacts-v0.1.3.json",
      sha256: sha256(Buffer.from("fixture metadata\n", "utf8")),
    },
    artifacts: [
      {
        adapter: "codex",
        archive: archiveName,
        url: `https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/${archiveName}`,
        sha256: sha256(archiveBytes),
        size_bytes: archiveBytes.length,
        install_root: ".agents/skills",
        tree_hash_algorithm: "rigorloop-tree-hash-v1",
        tree_sha256: treeHashForEntries(entries),
      },
    ],
    validation: {
      command: "python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.3",
      result: "pass",
    },
  };
  const finalMetadata = options.metadata ? options.metadata(metadata) : metadata;
  const metadataPath = join(projectRoot, "adapter-artifacts-v0.1.3.json");
  writeFileSync(metadataPath, JSON.stringify(finalMetadata, null, 2));
  return { archivePath, archiveName, metadataPath, metadata: finalMetadata, entries };
}

function fixturePackage(options = {}) {
  const root = mkdtempSync(join(tmpdir(), "rigorloop-package-test-"));
  mkdirSync(join(root, "dist", "bin"), { recursive: true });
  mkdirSync(join(root, "dist", "lib"), { recursive: true });
  mkdirSync(join(root, "dist", "metadata"), { recursive: true });
  writeFileSync(
    join(root, "package.json"),
    JSON.stringify(
      {
        name: packageJson.name,
        version: options.version ?? packageJson.version,
        type: "module",
        bin: packageJson.bin,
      },
      null,
      2,
    ),
  );
  copyFileSync(cliPath, join(root, "dist", "bin", "rigorloop.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "command-result.js"), join(root, "dist", "lib", "command-result.js"));

  if (options.metadata !== false) {
    const metadata = options.metadata ?? JSON.parse(readFileSync(join(packageRoot, "dist", "metadata", "adapter-artifacts-v0.1.3.json"), "utf8"));
    writeFileSync(join(root, "dist", "metadata", "adapter-artifacts-v0.1.3.json"), JSON.stringify(metadata, null, 2));
    const metadataBytes = Buffer.from(JSON.stringify(metadata, null, 2), "utf8");
    const release = options.release ?? {
      source_repository: "xiongxianfei/rigorloop",
      metadata_url: `data:application/json;base64,${metadataBytes.toString("base64")}`,
      metadata_sha256: sha256(metadataBytes),
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
    };
    writeFileSync(
      join(root, "dist", "metadata", "releases.json"),
      JSON.stringify(
        {
          schema_version: 1,
          releases: {
            "v0.1.3": release,
          },
        },
        null,
        2,
      ),
    );
  } else if (options.releaseIndex) {
    writeFileSync(join(root, "dist", "metadata", "releases.json"), JSON.stringify(options.releaseIndex, null, 2));
  }

  return { root, cliPath: join(root, "dist", "bin", "rigorloop.js") };
}

function runCliWithBundledMetadata(args, cwd, metadata, options = {}) {
  const packageFixture = fixturePackage({ metadata, release: options.release });
  return runCli(args, {
    cwd,
    cliPath: packageFixture.cliPath,
    env: options.env,
  });
}

test("T1 package metadata exposes one public binary and no archive files", () => {
  assert.equal(packageJson.name, "@xiongxianfei/rigorloop");
  assert.deepEqual(Object.keys(packageJson.bin), ["rigorloop"]);
  assert.equal(packageJson.bin.rigorloop, "dist/bin/rigorloop.js");

  const files = packageJson.files ?? [];
  assert.ok(!files.some((entry) => entry.endsWith(".zip")));
});

test("T2 help output shows only the implemented command surface", () => {
  const result = runCli(["--help"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /rigorloop\b/);
  assert.match(result.stdout, /rigorloop version/);
  assert.match(result.stdout, /rigorloop init --adapter codex/);
  assert.doesNotMatch(result.stdout, /\bnew-change\b/);
  assert.doesNotMatch(result.stdout, /\bstatus\b/);
  assert.doesNotMatch(result.stdout, /\bvalidate\b/);
});

test("T3 version output reports package identity", () => {
  const result = runCli(["version"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /@xiongxianfei\/rigorloop/);
  assert.match(result.stdout, /0\.1\.3/);
});

test("T4 unknown commands return usage errors", () => {
  const result = runCli(["unknown-command"]);

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /Unknown command/);
  assert.match(`${result.stdout}${result.stderr}`, /rigorloop --help/);
});

test("T5 unsupported adapters are blocked and do not write files", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "claude", "--json"], { cwd });

  assert.equal(result.status, 2);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "adapter-unsupported");
  assert.deepEqual(listProject(cwd), []);
});

test("T6 JSON envelope is stable and stdout contains JSON only", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });

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
  assert.equal(output.package.version, "0.1.3");
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
  const result = runCli(["init", "--adapter", "codex", "--dry-run"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /RigorLoop init dry run/);
  assert.doesNotThrow(() => {
    assert.throws(() => JSON.parse(result.stdout));
  });
});

test("T8 quiet mode does not change JSON shape or behavior", () => {
  const cwd = tempProject();
  const base = JSON.parse(
    execFileSync(process.execPath, [cliPath, "init", "--adapter", "codex", "--dry-run", "--json"], {
      cwd,
      encoding: "utf8",
    }),
  );
  const quietResult = runCli(["init", "--adapter", "codex", "--dry-run", "--json", "--quiet"], { cwd });

  assert.equal(quietResult.status, 0, quietResult.stderr);
  const quiet = JSON.parse(quietResult.stdout);
  assert.deepEqual(Object.keys(quiet), Object.keys(base));
  assert.equal(quiet.status, base.status);
});

test("T9 debug mode preserves stable top-level JSON fields", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json", "--debug"], { cwd });

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
  const success = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });
  const blocked = runCli(["init", "--adapter", "claude", "--json"], { cwd });
  const usage = runCli(["unknown-command"], { cwd });

  assert.equal(success.status, 0);
  assert.equal(blocked.status, 2);
  assert.equal(usage.status, 4);
});

test("T12 dry-run init plans scaffold writes without mutating the project", () => {
  const cwd = tempProject();
  const before = listProject(cwd);
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.planned_manifest.path, "rigorloop.yaml");
  assert.match(output.planned_manifest.content, /schema_version: 1/);
  assert.match(output.planned_manifest.content, /name: codex/);
  assert.match(output.planned_manifest.content, /install_root: ".agents\/skills"/);
  assert.equal(output.planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.deepEqual(output.actions.map((action) => action.path).slice(0, 3), [".agents", ".agents/skills", "rigorloop.yaml"]);
  assert.equal(actionFor(output, ".agents")?.type, "create-dir");
  assert.equal(actionFor(output, ".agents")?.status, "planned");
  assert.equal(actionFor(output, ".agents/skills")?.type, "create-dir");
  assert.equal(actionFor(output, ".agents/skills")?.status, "planned");
  assert.equal(actionFor(output, "rigorloop.yaml")?.type, "write");
  assert.deepEqual(listProject(cwd), before);
});

test("T13 init requires --adapter codex", () => {
  const cwd = tempProject();
  const result = runCli(["init"], { cwd });

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /--adapter codex/);
  assert.deepEqual(listProject(cwd), []);
});

test("T14 missing local archive path is invalid input", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--from-archive", "./missing.zip", "--json"], { cwd });

  assert.equal(result.status, 4);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);

  const missingValue = runCli(["init", "--adapter", "codex", "--from-archive", "--json"], { cwd });
  assert.equal(missingValue.status, 4);
  assert.equal(JSON.parse(missingValue.stdout).errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);
});

test("T15 network mode blocks when official release metadata is unavailable", () => {
  const cwd = tempProject();
  const packageFixture = fixturePackage({
    release: {
      source_repository: "xiongxianfei/rigorloop",
      metadata_url: "http://127.0.0.1:9/adapter-artifacts-v0.1.3.json",
      metadata_sha256: "0".repeat(64),
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
    },
  });
  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "release-unavailable");
  assert.deepEqual(listProject(cwd), []);
});

test("T16 network mode verifies release metadata and archive before install", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  fixture.metadata.artifacts[0].url = `data:application/octet-stream;base64,${archiveBytes.toString("base64")}`;
  const metadataBytes = Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8");
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      metadata_url: `data:application/json;base64,${metadataBytes.toString("base64")}`,
      metadata_sha256: sha256(metadataBytes),
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
    },
  });
  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "warning");
  assert.equal(output.planned_lockfile.generated.adapters[0].source, "release-archive");
  assert.equal(output.planned_lockfile.generated.adapters[0].archive_sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("T16 network metadata hash verification uses the bundled release index", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  fixture.metadata.artifacts[0].url = `data:application/octet-stream;base64,${archiveBytes.toString("base64")}`;
  const metadataBytes = Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8");
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      metadata_url: `data:application/json;base64,${metadataBytes.toString("base64")}`,
      metadata_sha256: "0".repeat(64),
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
    },
  });

  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 3);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "metadata-sha256-mismatch");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T16 metadata bytes are verified before parsing", () => {
  const cwd = tempProject();
  const packageFixture = fixturePackage({
    metadata: false,
    releaseIndex: {
      schema_version: 1,
      releases: {
        "v0.1.3": {
          source_repository: "xiongxianfei/rigorloop",
          metadata_url: "data:application/json;base64,bm90LWpzb24=",
          metadata_sha256: "0".repeat(64),
          bundled_metadata: "adapter-artifacts-v0.1.3.json",
        },
      },
    },
  });

  const result = runCli(["init", "--adapter", "codex", "--json"], {
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
        "v0.1.3": {
          source_repository: "xiongxianfei/rigorloop",
          metadata_url: "data:application/json,%7B%7D",
          bundled_metadata: "adapter-artifacts-v0.1.3.json",
        },
      },
    },
  });

  const result = runCli(["init", "--adapter", "codex", "--json"], {
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
  fixture.metadata.artifacts[0].url = `data:application/octet-stream;base64,${archiveBytes.toString("base64")}`;
  const metadataBytes = Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8");
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      metadata_url: `data:application/json;base64,${metadataBytes.toString("base64")}`,
      metadata_sha256: sha256(metadataBytes),
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
    },
  });

  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: { RIGORLOOP_RELEASE_METADATA_URL: "http://127.0.0.1:9/attacker.json" },
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("T17 incompatible local archive release is blocked", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, { archiveName: "rigorloop-adapter-codex-v0.1.2.zip" });
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "release-version-incompatible");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T18 local archive mode uses bundled metadata and no metadata flag", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "warning");
  assert.equal(output.planned_lockfile.generated.adapters[0].archive_sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(output.planned_lockfile.generated.adapters[0].tree_sha256, fixture.metadata.artifacts[0].tree_sha256);
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
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
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
  writeFileSync(join(cwd, "rigorloop-adapter-codex-v0.1.3.zip"), archive);
  const packageFixture = fixturePackage({ metadata: false });
  const result = runCli(["init", "--adapter", "codex", "--from-archive", "./rigorloop-adapter-codex-v0.1.3.zip", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
  });

  assert.equal(result.status, 2);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "metadata-unavailable");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("T20 actual init writes minimum manifest and Codex install root without lockfile", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "warning");
  assert.equal(output.warnings[0].code, "lockfile-spec-not-approved");
  assert.deepEqual(output.actions.map((action) => action.path).slice(0, 3), [".agents", ".agents/skills", "rigorloop.yaml"]);
  assert.equal(actionFor(output, ".agents")?.status, "done");
  assert.equal(actionFor(output, ".agents/skills")?.status, "done");
  assert.equal(actionFor(output, "rigorloop.yaml")?.status, "done");
  assert.equal(existsSync(join(cwd, ".agents")), true);
  assert.equal(existsSync(join(cwd, ".agents", "skills")), true);
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), true);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);

  const manifest = readProjectFile(cwd, "rigorloop.yaml");
  assert.match(manifest, /schema_version: 1/);
  assert.match(manifest, /package: "@xiongxianfei\/rigorloop"/);
  assert.match(manifest, /package_version: "0\.1\.3"/);
  assert.match(manifest, /name: codex/);
  assert.match(manifest, /install_root: ".agents\/skills"/);
  assert.match(manifest, /type: local-archive/);
  assert.match(manifest, /archive: "\.\/rigorloop-adapter-codex-v0\.1\.3\.zip"/);
});

test("T24 write plan represents parent and leaf directory states before mutation", () => {
  const parentOnlyProject = tempProject();
  mkdirSync(join(parentOnlyProject, ".agents"));
  const parentOnlyFixture = fixtureArchive(parentOnlyProject);
  const parentOnly = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${parentOnlyFixture.archiveName}`, "--json"],
    parentOnlyProject,
    parentOnlyFixture.metadata,
  );

  assert.equal(parentOnly.status, 0, parentOnly.stderr);
  const parentOnlyOutput = JSON.parse(parentOnly.stdout);
  assert.equal(actionFor(parentOnlyOutput, ".agents")?.status, "skipped");
  assert.equal(actionFor(parentOnlyOutput, ".agents/skills")?.status, "done");

  const existingDirsProject = tempProject();
  mkdirSync(join(existingDirsProject, ".agents", "skills"), { recursive: true });
  const existingDirsFixture = fixtureArchive(existingDirsProject);
  const existingDirs = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${existingDirsFixture.archiveName}`, "--json"],
    existingDirsProject,
    existingDirsFixture.metadata,
  );

  assert.equal(existingDirs.status, 0, existingDirs.stderr);
  const existingDirsOutput = JSON.parse(existingDirs.stdout);
  assert.equal(actionFor(existingDirsOutput, ".agents")?.status, "skipped");
  assert.equal(actionFor(existingDirsOutput, ".agents/skills")?.status, "skipped");
});

test("T21 existing manifest handling is non-destructive", () => {
  const validProject = tempProject();
  const existingManifest = `schema_version: 1
rigorloop:
  package: "@xiongxianfei/rigorloop"
  package_version: "0.1.3"
adapters:
  - name: codex
    install_root: ".agents/skills"
    source:
      type: local-archive
      archive: "./rigorloop-adapter-codex-v0.1.3.zip"
`;
  writeFileSync(join(validProject, "rigorloop.yaml"), existingManifest);
  const validFixture = fixtureArchive(validProject);
  const validResult = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${validFixture.archiveName}`, "--json"],
    validProject,
    validFixture.metadata,
  );

  assert.equal(validResult.status, 0, validResult.stderr);
  assert.equal(readProjectFile(validProject, "rigorloop.yaml"), existingManifest);
  assert.ok(JSON.parse(validResult.stdout).actions.some((action) => action.path === "rigorloop.yaml" && action.status === "skipped"));

  const invalidProject = tempProject();
  writeFileSync(join(invalidProject, "rigorloop.yaml"), "schema_version: 99\n");
  const invalidResult = runCli(["init", "--adapter", "codex", "--json"], { cwd: invalidProject });

  assert.equal(invalidResult.status, 4);
  assert.equal(readProjectFile(invalidProject, "rigorloop.yaml"), "schema_version: 99\n");
  const output = JSON.parse(invalidResult.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-config");
});

test("T22 local archive mode plans local-archive manifest source", () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, "rigorloop-adapter-codex-v0.1.3.zip"), "placeholder archive fixture\n");
  const result = runCli(["init", "--adapter", "codex", "--from-archive", "./rigorloop-adapter-codex-v0.1.3.zip", "--dry-run", "--json"], {
    cwd,
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.match(output.planned_manifest.content, /type: local-archive/);
  assert.match(output.planned_manifest.content, /archive: "\.\/rigorloop-adapter-codex-v0\.1\.3\.zip"/);
  assert.equal(output.planned_lockfile.generated.adapters[0].source, "local-archive");
  assert.equal(output.planned_lockfile.generated.adapters[0].archive, "rigorloop-adapter-codex-v0.1.3.zip");
  assert.deepEqual(listProject(cwd), ["rigorloop-adapter-codex-v0.1.3.zip"]);

  const actualProject = tempProject();
  const actualFixture = fixtureArchive(actualProject);
  const actual = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", "./rigorloop-adapter-codex-v0.1.3.zip"],
    actualProject,
    actualFixture.metadata,
  );

  assert.equal(actual.status, 0, actual.stderr);
  const manifest = readProjectFile(actualProject, "rigorloop.yaml");
  assert.match(manifest, /type: local-archive/);
  assert.match(manifest, /archive: "\.\/rigorloop-adapter-codex-v0\.1\.3\.zip"/);
});

test("T23 generated manifest avoids forbidden claims and validation commands", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  const manifest = readProjectFile(cwd, "rigorloop.yaml");
  assert.doesNotMatch(manifest, /branch-ready|pr-ready|pr-body-ready|pr-open-ready|workflow-accepted|validation-success|lockfile-authority/);
  assert.doesNotMatch(manifest, /validation:\s*\n\s*commands:/);
});

test("T26 overwrite conflicts are refused without replacing user files", () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, ".agents"), "user file\n");
  const result = runCli(["init", "--adapter", "codex", "--json", "--force"], { cwd });

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents");
  assert.equal(actionFor(output, ".agents")?.status, "blocked");
  assert.equal(actionFor(output, ".agents/skills")?.status, "blocked");
});

test("T26 leaf install-root file conflict is refused without replacing user files", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, ".agents"));
  writeFileSync(join(cwd, ".agents", "skills"), "user file\n");
  const result = runCli(["init", "--adapter", "codex", "--json", "--force"], { cwd });

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents/skills"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents/skills");
  assert.equal(actionFor(output, ".agents")?.status, "skipped");
  assert.equal(actionFor(output, ".agents/skills")?.status, "blocked");
});

test("T26 adapter file overwrite conflicts are refused without replacing user files", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "proposal"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), "user file\n");
  const result = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json", "--force"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 5);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "user file\n");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents/skills/proposal/SKILL.md");
});

test("T29 release metadata shape and validation result are validated", () => {
  const cwd = tempProject();
  const wrongRepo = fixtureArchive(cwd, {
    metadata(metadata) {
      metadata.release.source_repository = "example/not-rigorloop";
      return metadata;
    },
  });
  const wrongRepoResult = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${wrongRepo.archiveName}`, "--json"], cwd, wrongRepo.metadata);

  assert.equal(wrongRepoResult.status, 2);
  assert.equal(JSON.parse(wrongRepoResult.stdout).blockers[0].code, "metadata-invalid");

  const missingFieldProject = tempProject();
  const missingField = fixtureArchive(missingFieldProject, {
    metadata(metadata) {
      delete metadata.metadata.sha256;
      return metadata;
    },
  });
  const missingFieldResult = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${missingField.archiveName}`, "--json"],
    missingFieldProject,
    missingField.metadata,
  );

  assert.equal(missingFieldResult.status, 2);
  assert.equal(JSON.parse(missingFieldResult.stdout).blockers[0].code, "metadata-invalid");

  const noCodexProject = tempProject();
  const noCodex = fixtureArchive(noCodexProject, {
    metadata(metadata) {
      metadata.artifacts[0].adapter = "claude";
      return metadata;
    },
  });
  const noCodexResult = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${noCodex.archiveName}`, "--json"],
    noCodexProject,
    noCodex.metadata,
  );

  assert.equal(noCodexResult.status, 2);
  assert.equal(JSON.parse(noCodexResult.stdout).blockers[0].code, "adapter-unknown");

  const wrongRootProject = tempProject();
  const wrongRoot = fixtureArchive(wrongRootProject, {
    metadata(metadata) {
      metadata.artifacts[0].install_root = ".codex/skills";
      return metadata;
    },
  });
  const wrongRootResult = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${wrongRoot.archiveName}`, "--json"],
    wrongRootProject,
    wrongRoot.metadata,
  );

  assert.equal(wrongRootResult.status, 2);
  assert.equal(JSON.parse(wrongRootResult.stdout).blockers[0].code, "metadata-invalid");

  const validationFailProject = tempProject();
  const validationFail = fixtureArchive(validationFailProject, {
    metadata(metadata) {
      metadata.validation.result = "fail";
      return metadata;
    },
  });
  const validationFailResult = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${validationFail.archiveName}`, "--json"],
    validationFailProject,
    validationFail.metadata,
  );

  assert.equal(validationFailResult.status, 2);
  assert.equal(JSON.parse(validationFailResult.stdout).blockers[0].code, "metadata-invalid");
});

test("T30 archive traversal paths are rejected", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "../escape.txt", bytes: Buffer.from("escape\n", "utf8") }],
  });
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-path-traversal");
  assert.equal(existsSync(join(cwd, "escape.txt")), false);
});

test("T31 archive entries must remain under .agents/skills", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    entries: [{ name: "proposal/SKILL.md", bytes: Buffer.from("# Proposal\n", "utf8") }],
  });
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

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
    ["init", "--adapter", "codex", "--from-archive", `./${supportFixture.archiveName}`, "--json"],
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
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

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
    ["init", "--adapter", "codex", "--from-archive", `./${checksumFixture.archiveName}`, "--json"],
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
    ["init", "--adapter", "codex", "--from-archive", `./${sizeFixture.archiveName}`, "--json"],
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
    ["init", "--adapter", "codex", "--from-archive", `./${treeFixture.archiveName}`, "--json"],
    treeProject,
    treeFixture.metadata,
  );
  assert.equal(tree.status, 3);
  assert.equal(JSON.parse(tree.stdout).errors[0].code, "tree-hash-mismatch");
});

test("T41 lockfile is planned output only and never durably written", () => {
  const newProject = tempProject();
  const dryRun = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd: newProject });

  assert.equal(dryRun.status, 0, dryRun.stderr);
  assert.equal(JSON.parse(dryRun.stdout).planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.equal(existsSync(join(newProject, "rigorloop.lock")), false);

  const existingProject = tempProject();
  const fixture = fixtureArchive(existingProject);
  writeFileSync(join(existingProject, "rigorloop.lock"), "existing-lock\n");
  const actual = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    existingProject,
    fixture.metadata,
  );

  assert.equal(actual.status, 0, actual.stderr);
  assert.equal(readProjectFile(existingProject, "rigorloop.lock"), "existing-lock\n");
  const output = JSON.parse(actual.stdout);
  assert.equal(output.planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.ok(output.warnings.some((warning) => warning.code === "lockfile-spec-not-approved"));
});
