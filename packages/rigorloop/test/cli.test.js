import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { exitCodeForResult } from "../dist/lib/command-result.js";
import {
  parseLockfile,
  serializeLockfile,
  sha256NormalizedText,
} from "../dist/lib/lockfile.js";
import {
  buildNewChangeDraft,
  renderChangeMetadata,
  validateChangeId,
  validateClassification,
  validateProfile,
  validateRisk,
} from "../dist/lib/new-change.js";
import { runNewChangePlan } from "../dist/lib/new-change-filesystem.js";
import { expectedArchiveUrl, validateOfficialArchiveUrl } from "../dist/lib/official-archive-url.js";

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
  copyFileSync(join(packageRoot, "dist", "lib", "lockfile.js"), join(root, "dist", "lib", "lockfile.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "new-change.js"), join(root, "dist", "lib", "new-change.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "new-change-filesystem.js"), join(root, "dist", "lib", "new-change-filesystem.js"));
  copyFileSync(join(packageRoot, "dist", "lib", "official-archive-url.js"), join(root, "dist", "lib", "official-archive-url.js"));

  if (options.metadata !== false) {
    const metadata = options.metadata ?? JSON.parse(readFileSync(join(packageRoot, "dist", "metadata", "adapter-artifacts-v0.1.3.json"), "utf8"));
    const metadataContent = typeof metadata === "string" ? metadata : JSON.stringify(metadata, null, 2);
    writeFileSync(join(root, "dist", "metadata", "adapter-artifacts-v0.1.3.json"), metadataContent);
    const metadataBytes = Buffer.from(metadataContent, "utf8");
    const release = options.release ?? {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: "v0.1.3",
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
      bundled_metadata_sha256: sha256(metadataBytes),
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
  } else {
    const releaseIndex =
      options.releaseIndex ?? {
        schema_version: 1,
        releases: {
          "v0.1.3": {
            source_repository: "xiongxianfei/rigorloop",
            release_tag: "v0.1.3",
            bundled_metadata: "adapter-artifacts-v0.1.3.json",
            bundled_metadata_sha256: "0".repeat(64),
          },
        },
      };
    writeFileSync(join(root, "dist", "metadata", "releases.json"), JSON.stringify(releaseIndex, null, 2));
  }

  return { root, cliPath: join(root, "dist", "bin", "rigorloop.js") };
}

function validLockfile(overrides = {}) {
  const source = overrides.source ?? "release-archive";
  const adapter = overrides.adapter ?? "codex";
  const schemaVersion = overrides.schemaVersion ?? 1;
  const treeHashAlgorithm = overrides.treeHashAlgorithm ?? "rigorloop-tree-hash-v1";
  return `schema_version: ${schemaVersion}

rigorloop:
  package: "@xiongxianfei/rigorloop"
  version: "0.1.3"

manifest:
  path: "rigorloop.yaml"
  sha256: "1111111111111111111111111111111111111111111111111111111111111111"

generated:
  adapters:
    - adapter: ${adapter}
      release: "v0.1.3"
      source: ${source}
      archive: "rigorloop-adapter-codex-v0.1.3.zip"
      archive_sha256: "2222222222222222222222222222222222222222222222222222222222222222"
      installed_root: ".agents/skills"
      tree_hash_algorithm: ${treeHashAlgorithm}
      tree_sha256: "3333333333333333333333333333333333333333333333333333333333333333"
      file_count: 23
`;
}

function lockfileWithUnknownMapping(section) {
  if (section === "rigorloop") {
    return validLockfile().replace("  version: \"0.1.3\"\n", "  version: \"0.1.3\"\n  future:\n    value: true\n");
  }
  if (section === "manifest") {
    return validLockfile().replace('  sha256: "1111111111111111111111111111111111111111111111111111111111111111"\n', '  sha256: "1111111111111111111111111111111111111111111111111111111111111111"\n  future:\n    value: true\n');
  }
  if (section === "generated") {
    return validLockfile().replace("  adapters:\n", "  future:\n    value: true\n  adapters:\n");
  }
  if (section === "adapter") {
    return validLockfile().replace("      file_count: 23\n", "      file_count: 23\n      future:\n        value: true\n");
  }
  throw new Error(`Unknown lockfile section fixture: ${section}`);
}

function runCliWithBundledMetadata(args, cwd, metadata, options = {}) {
  const packageFixture = fixturePackage({ metadata, release: options.release });
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
  assert.match(result.stdout, /rigorloop new-change <change-id>/);
  assert.doesNotMatch(result.stdout, /\bstatus\b/);
  assert.doesNotMatch(result.stdout, /\bvalidate\b/);
});

test("TNC-002 new-change requires a change id, title, and option values", () => {
  const cwd = tempProject();
  const cases = [
    [["new-change", "--title", "Missing id", "--json"], "missing-change-id"],
    [["new-change", "docs-only", "--json"], "missing-title"],
    [["new-change", "docs-only", "--title", "--json"], "missing-title"],
    [["new-change", "docs-only", "--title", "Docs", "--type", "--json"], "invalid-classification"],
    [["new-change", "docs-only", "--title", "Docs", "--risk", "--json"], "invalid-risk"],
    [["new-change", "docs-only", "--title", "Docs", "--profile", "--json"], "unsupported-profile"],
  ];

  for (const [args, expectedCode] of cases) {
    const result = runCli(args, { cwd });

    assert.equal(result.status, 4, args.join(" "));
    assert.equal(result.stderr, "");
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "error");
    assert.equal(output.errors[0].code, expectedCode);
    assert.deepEqual(listProject(cwd), []);
  }
});

test("TNC-003 change id validation accepts one safe path segment only", () => {
  for (const id of ["a", "docs-typo", "feature123"]) {
    assert.deepEqual(validateChangeId(id), { ok: true });
  }

  for (const id of [
    "../outside",
    "a/b",
    "a\\b",
    ".hidden",
    "-bad",
    "bad-",
    "bad id",
    "bad%2Fid",
    "bad%5Cid",
    "a:b",
    "bad\nid",
  ]) {
    const result = validateChangeId(id);
    assert.equal(result.ok, false, id);
    assert.equal(result.code, "invalid-change-id");
  }
});

test("TNC-004 classification token validation is exact", () => {
  const longValid = "a".repeat(64);
  for (const value of ["docs", "workflow", "cli-123", longValid]) {
    assert.deepEqual(validateClassification(value), { ok: true });
  }

  for (const value of [
    "",
    "High",
    "security review",
    "../x",
    "medium/high",
    "bad%2Fx",
    "bad\\x",
    "bad\nx",
    "1bad",
    "a".repeat(65),
  ]) {
    const result = validateClassification(value);
    assert.equal(result.ok, false, value);
    assert.equal(result.code, "invalid-classification");
  }
});

test("TNC-005 risk and profile validation are exact", () => {
  for (const risk of ["low", "medium", "high"]) {
    assert.deepEqual(validateRisk(risk), { ok: true });
  }
  for (const risk of ["", "High", "critical", "medium/high"]) {
    const result = validateRisk(risk);
    assert.equal(result.ok, false, risk);
    assert.equal(result.code, "invalid-risk");
  }

  for (const profile of ["standard", "minimal"]) {
    assert.deepEqual(validateProfile(profile), { ok: true });
  }
  for (const profile of ["", "Standard", "full", "minimal/fast"]) {
    const result = validateProfile(profile);
    assert.equal(result.ok, false, profile);
    assert.equal(result.code, "unsupported-profile");
  }
});

test("TNC-006 generated change metadata defaults and field order are deterministic", () => {
  const metadata = renderChangeMetadata({
    changeId: "docs-typo",
    title: "Fix docs typo",
    classification: "default",
    risk: "medium",
  });

  assert.equal(metadata, renderChangeMetadata({
    changeId: "docs-typo",
    title: "Fix docs typo",
    classification: "default",
    risk: "medium",
  }));
  assert.deepEqual(
    metadata
      .split("\n")
      .filter((line) => /^[a-z_]+:/.test(line))
      .map((line) => line.split(":")[0]),
    [
      "change_id",
      "title",
      "classification",
      "risk",
      "artifacts",
      "requirements",
      "tests",
      "validation",
      "changed_files",
      "review",
    ],
  );
  assert.match(metadata, /^change_id: "docs-typo"\n/);
  assert.match(metadata, /\nclassification: "default"\n/);
  assert.match(metadata, /\nrisk: "medium"\n/);
  assert.match(metadata, /\nartifacts: \{\}\n/);
  assert.match(metadata, /\nrequirements: \[\]\n/);
  assert.match(metadata, /\nchanged_files: \[\]\nreview:\n  status: "pending"\n  unresolved_items: 0\n/);
});

test("TNC-007 YAML scalar escaping preserves shape and omits local details", () => {
  const metadata = renderChangeMetadata({
    changeId: "yaml-case",
    title: '  Title: "quoted" # hash [brackets]  ',
    classification: "docs",
    risk: "high",
  });

  assert.match(metadata, /title: "  Title: \\"quoted\\" # hash \[brackets\]  "/);
  assert.doesNotMatch(metadata, new RegExp(tmpdir().replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  assert.doesNotMatch(metadata, /TOKEN|SECRET|username|hostname|process\.env/);
});

test("TNC-008 new-change dry-run JSON envelope and change object are stable", () => {
  const cwd = tempProject();
  const result = runCli(["new-change", "json-case", "--title", "JSON Case", "--dry-run", "--json"], { cwd });

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
  assert.equal(output.command, "new-change");
  assert.equal(output.status, "success");
  assert.deepEqual(output.change, {
    change_id: "json-case",
    root: "docs/changes/json-case",
    metadata_path: "docs/changes/json-case/change.yaml",
    profile: "standard",
  });
  assert.equal(output.planned_change_metadata.path, "docs/changes/json-case/change.yaml");
  assert.match(output.planned_change_metadata.content, /title: "JSON Case"/);
  assert.deepEqual(listProject(cwd), []);
});

test("TNC-009 standard profile creates only change.yaml", () => {
  const cwd = tempProject();
  const result = runCli(["new-change", "adapter-install-cli", "--title", "Adapter install CLI", "--type", "workflow"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /docs\/changes\/adapter-install-cli/);
  assert.ok(existsSync(join(cwd, "docs/changes/adapter-install-cli/change.yaml")));
  assert.ok(!existsSync(join(cwd, "docs/changes/adapter-install-cli/explain-change.md")));
  assert.ok(!existsSync(join(cwd, "rigorloop.yaml")));
  assert.ok(!existsSync(join(cwd, "rigorloop.lock")));
  assert.deepEqual(listProject(join(cwd, "docs/changes/adapter-install-cli")), ["change.yaml"]);

  const metadata = readProjectFile(cwd, "docs/changes/adapter-install-cli/change.yaml");
  assert.match(metadata, /classification: "workflow"/);
  assert.doesNotMatch(metadata, /implementation-complete|review-complete|verification-complete|pr-ready|proposal-accepted/);
});

test("TNC-010 minimal profile creates only metadata and returns durable-reasoning warning", () => {
  const cwd = tempProject();
  const result = runCli(["new-change", "docs-typo", "--title", "Fix docs typo", "--type", "docs", "--profile", "minimal", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = parseJsonResult(result);
  assert.equal(output.status, "warning");
  assert.equal(output.warnings[0].code, "durable-reasoning-not-scaffolded");
  assert.ok(existsSync(join(cwd, "docs/changes/docs-typo/change.yaml")));
  assert.ok(!existsSync(join(cwd, "docs/changes/docs-typo/explain-change.md")));
  assert.deepEqual(output.planned_change_metadata.content.includes("artifacts: {}"), true);
  assert.deepEqual(listProject(join(cwd, "docs/changes/docs-typo")), ["change.yaml"]);
});

test("TNC-011 dry-run JSON reports every planned mutation and writes nothing", () => {
  const cwd = tempProject();
  const before = listProject(cwd);
  const result = runCli(["new-change", "new-feature", "--title", "New feature", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = parseJsonResult(result);
  assert.equal(output.status, "success");
  assert.deepEqual(output.actions.map((action) => action.path), [
    "docs",
    "docs/changes",
    "docs/changes/new-feature",
    "docs/changes/new-feature/change.yaml",
  ]);
  for (const path of ["docs", "docs/changes", "docs/changes/new-feature"]) {
    assert.equal(actionFor(output, path)?.type, "create-dir");
    assert.equal(actionFor(output, path)?.status, "planned");
    assert.equal(typeof actionFor(output, path)?.reason, "string");
  }
  assert.equal(actionFor(output, "docs/changes/new-feature/change.yaml")?.type, "write");
  assert.equal(actionFor(output, "docs/changes/new-feature/change.yaml")?.status, "planned");
  assert.deepEqual(listProject(cwd), before);
});

test("TNC-012 existing safe directories and unrelated files are preserved", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, "docs/changes/existing-root"), { recursive: true });
  writeFileSync(join(cwd, "docs/changes/existing-root/notes.md"), "keep me\n");
  const before = listProject(cwd);

  const dryRun = runCli(["new-change", "existing-root", "--title", "Existing Root", "--dry-run", "--json"], { cwd });

  assert.equal(dryRun.status, 0, dryRun.stderr);
  const dryRunOutput = parseJsonResult(dryRun);
  assert.equal(dryRunOutput.status, "success");
  assert.equal(actionFor(dryRunOutput, "docs")?.status, "existing");
  assert.equal(actionFor(dryRunOutput, "docs/changes")?.status, "existing");
  assert.equal(actionFor(dryRunOutput, "docs/changes/existing-root")?.status, "existing");
  assert.equal(actionFor(dryRunOutput, "docs/changes/existing-root/change.yaml")?.status, "planned");
  assert.deepEqual(listProject(cwd), before);
  assert.equal(readProjectFile(cwd, "docs/changes/existing-root/notes.md"), "keep me\n");
  assert.ok(!existsSync(join(cwd, "docs/changes/existing-root/change.yaml")));

  const actual = runCli(["new-change", "existing-root", "--title", "Existing Root", "--json"], { cwd });

  assert.equal(actual.status, 0, actual.stderr);
  const output = parseJsonResult(actual);
  assert.equal(actionFor(output, "docs")?.status, "existing");
  assert.equal(actionFor(output, "docs/changes")?.status, "existing");
  assert.equal(actionFor(output, "docs/changes/existing-root")?.status, "existing");
  assert.equal(actionFor(output, "docs/changes/existing-root/change.yaml")?.status, "done");
  assert.equal(readProjectFile(cwd, "docs/changes/existing-root/notes.md"), "keep me\n");
  assert.ok(existsSync(join(cwd, "docs/changes/existing-root/change.yaml")));
});

test("TNC-013 directory path conflicts block before mutation", () => {
  const cases = [
    ["docs", (cwd) => writeFileSync(join(cwd, "docs"), "file\n")],
    ["docs/changes", (cwd) => {
      mkdirSync(join(cwd, "docs"));
      writeFileSync(join(cwd, "docs/changes"), "file\n");
    }],
    ["docs/changes/conflict-root", (cwd) => {
      mkdirSync(join(cwd, "docs/changes"), { recursive: true });
      writeFileSync(join(cwd, "docs/changes/conflict-root"), "file\n");
    }],
  ];

  for (const [conflictPath, setup] of cases) {
    const cwd = tempProject();
    setup(cwd);
    const before = listProject(cwd);
    const result = runCli(["new-change", "conflict-root", "--title", "Conflict", "--json"], { cwd });

    assert.equal(result.status, 5, conflictPath);
    const output = parseJsonResult(result);
    assert.equal(output.status, "blocked");
    assert.equal(output.blockers[0].code, "path-not-directory");
    assert.equal(output.blockers[0].path, conflictPath);
    assert.equal(actionFor(output, conflictPath)?.status, "blocked");
    assert.deepEqual(listProject(cwd), before);
  }
});

test("TNC-014 symlink path conflicts block before mutation", (t) => {
  const cases = [
    ["docs", (cwd) => {}],
    ["docs/changes", (cwd) => mkdirSync(join(cwd, "docs"))],
    ["docs/changes/symlink-case", (cwd) => mkdirSync(join(cwd, "docs/changes"), { recursive: true })],
  ];

  for (const [conflictPath, setup] of cases) {
    const cwd = tempProject();
    const target = join(cwd, `outside-target-${conflictPath.replaceAll("/", "-")}`);
    setup(cwd);
    mkdirSync(target);
    try {
      symlinkSync(target, join(cwd, conflictPath), "dir");
    } catch (error) {
      t.skip(`symlink unavailable: ${error.message}`);
      return;
    }

    const result = runCli(["new-change", "symlink-case", "--title", "Symlink Case", "--json"], { cwd });

    assert.equal(result.status, 5, conflictPath);
    const output = parseJsonResult(result);
    assert.equal(output.status, "blocked", conflictPath);
    assert.equal(output.blockers[0].code, "path-not-directory", conflictPath);
    assert.equal(output.blockers[0].path, conflictPath);
    assert.equal(actionFor(output, conflictPath)?.status, "blocked");
    assert.ok(!existsSync(join(target, "change.yaml")));
    assert.ok(!existsSync(join(target, "explain-change.md")));
    assert.deepEqual(listProject(target), []);
  }
});

test("TNC-015 forbidden artifacts, network-adjacent files, and project files are not touched", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, "docs/changes/scope-case"), { recursive: true });
  writeFileSync(join(cwd, "docs/changes/scope-case/explain-change.md"), "existing draft\n");
  writeFileSync(join(cwd, "rigorloop.yaml"), "existing manifest\n");
  writeFileSync(join(cwd, "rigorloop.lock"), "existing lock\n");

  const result = runCli(["new-change", "scope-case", "--title", "Scope Case", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = parseJsonResult(result);
  assert.equal(output.status, "success");
  assert.equal(readProjectFile(cwd, "rigorloop.yaml"), "existing manifest\n");
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), "existing lock\n");
  assert.equal(readProjectFile(cwd, "docs/changes/scope-case/explain-change.md"), "existing draft\n");
  assert.ok(!existsSync(join(cwd, ".agents")));
  assert.ok(!existsSync(join(cwd, ".claude")));
  assert.ok(!existsSync(join(cwd, ".opencode")));
  assert.deepEqual(output.artifacts, [
    {
      path: "docs/changes/scope-case/change.yaml",
      kind: "change-metadata",
      status: "created",
    },
  ]);
});

test("TNC-016 existing change.yaml is not overwritten", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, "docs/changes/new-feature"), { recursive: true });
  writeFileSync(join(cwd, "docs/changes/new-feature/change.yaml"), "existing: true\n");
  writeFileSync(join(cwd, "docs/changes/new-feature/explain-change.md"), "keep\n");
  const before = listProject(cwd);

  const result = runCli(["new-change", "new-feature", "--title", "New feature", "--json"], { cwd });

  assert.equal(result.status, 5);
  const output = parseJsonResult(result);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "path-exists");
  assert.equal(output.blockers[0].path, "docs/changes/new-feature/change.yaml");
  assert.equal(readProjectFile(cwd, "docs/changes/new-feature/change.yaml"), "existing: true\n");
  assert.deepEqual(listProject(cwd), before);
});

test("TNC-017 partial write failure reports done and failed actions", () => {
  const cwd = tempProject();
  const draft = buildNewChangeDraft({
    changeId: "partial-failure",
    title: "Partial Failure",
    classification: "default",
    risk: "medium",
    profile: "standard",
  });
  const fsOps = {
    lstatSync,
    mkdirSync,
    writeFileSync() {
      throw new Error("simulated write failure");
    },
  };

  const execution = runNewChangePlan({
    cwd,
    draft,
    flags: { dryRun: false },
    profile: "standard",
    fsOps,
  });

  assert.equal(execution.result.status, "error");
  assert.equal(exitCodeForResult({ status: execution.result.status, exit_class: execution.exit_class }), 1);
  assert.equal(execution.result.summary, "RigorLoop new-change failed while writing files.");
  for (const path of ["docs", "docs/changes", "docs/changes/partial-failure"]) {
    assert.equal(actionFor(execution.result, path)?.status, "done");
  }
  assert.equal(actionFor(execution.result, "docs/changes/partial-failure/change.yaml")?.status, "failed");
  assert.equal(execution.result.errors[0].code, "write-failed");
  assert.equal(execution.result.errors[0].path, "docs/changes/partial-failure/change.yaml");
  assert.deepEqual(execution.result.artifacts, [
    {
      path: "docs/changes/partial-failure/change.yaml",
      kind: "change-metadata",
      status: "failed",
    },
  ]);
  assert.ok(existsSync(join(cwd, "docs/changes/partial-failure")));
  assert.ok(!existsSync(join(cwd, "docs/changes/partial-failure/change.yaml")));
});

test("TNC-018 new-change output modes follow shared CLI rules", () => {
  const humanCwd = tempProject();
  const human = runCli(["new-change", "human-case", "--title", "Human Case"], { cwd: humanCwd });

  assert.equal(human.status, 0, human.stderr);
  assert.equal(human.stderr, "");
  assert.match(human.stdout, /docs\/changes\/human-case/);
  assert.doesNotMatch(human.stdout, /^\s*\{/);

  const quietCwd = tempProject();
  const quietJson = runCli(["new-change", "quiet-case", "--title", "Quiet Case", "--json", "--quiet"], { cwd: quietCwd });

  assert.equal(quietJson.status, 0, quietJson.stderr);
  assert.equal(parseJsonResult(quietJson).status, "success");

  const debugCwd = tempProject();
  const debugJson = runCli(["new-change", "debug-case", "--title", "Debug Case", "--json", "--debug"], { cwd: debugCwd });
  const debugOutput = parseJsonResult(debugJson);

  assert.equal(debugJson.status, 0);
  assert.equal(debugOutput.schema_version, 1);
  assert.equal(debugOutput.command, "new-change");
  assert.deepEqual(debugOutput.diagnostics, { debug: true });

  const noColorCwd = tempProject();
  const noColor = runCli(["new-change", "no-color-case", "--title", "No Color Case", "--no-color"], {
    cwd: noColorCwd,
    env: { NO_COLOR: "1" },
  });

  assert.equal(noColor.status, 0, noColor.stderr);
  assert.doesNotMatch(noColor.stdout, /\u001b\[[0-9;]*m/);

  const invalidCwd = tempProject();
  const before = listProject(invalidCwd);
  const invalid = runCli(["new-change", "invalid-option", "--title", "Invalid Option", "--bad", "--json"], { cwd: invalidCwd });

  assert.equal(invalid.status, 4);
  assert.equal(parseJsonResult(invalid).errors[0].code, "invalid-usage");
  assert.deepEqual(listProject(invalidCwd), before);
});

test("TNC-019 new-change is additive and local-only", () => {
  const cwd = tempProject();
  const result = runCli(["new-change", "non-git-project", "--title", "Non Git Project", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(parseJsonResult(result).status, "success");
  assert.ok(!existsSync(join(cwd, ".git")));
  assert.ok(existsSync(join(cwd, "docs/changes/non-git-project/change.yaml")));
});

test("TNC-020 generated metadata validates with repository schema", () => {
  const cwd = tempProject();
  const standard = runCli(["new-change", "schema-standard", "--title", "Schema Standard"], { cwd });
  const minimal = runCli(["new-change", "schema-minimal", "--title", "Schema Minimal", "--profile", "minimal"], { cwd });

  assert.equal(standard.status, 0, standard.stderr);
  assert.equal(minimal.status, 0, minimal.stderr);
  const validator = resolve(packageRoot, "..", "..", "scripts", "validate-change-metadata.py");
  execFileSync("python", [validator, join(cwd, "docs/changes/schema-standard/change.yaml")], { encoding: "utf8" });
  execFileSync("python", [validator, join(cwd, "docs/changes/schema-minimal/change.yaml")], { encoding: "utf8" });
});

test("TNC-021 command scope is proportional to scaffolded paths", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, "unrelated/deep/tree"), { recursive: true });
  writeFileSync(join(cwd, "unrelated/deep/tree/file.txt"), "untouched\n");

  const result = runCli(["new-change", "scoped", "--title", "Scoped", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = parseJsonResult(result);
  assert.deepEqual(output.actions.map((action) => action.path), [
    "docs",
    "docs/changes",
    "docs/changes/scoped",
    "docs/changes/scoped/change.yaml",
  ]);
  assert.equal(readProjectFile(cwd, "unrelated/deep/tree/file.txt"), "untouched\n");
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
  assert.equal(output.planned_lockfile.generated.adapters[0].tree_hash_algorithm, "rigorloop-tree-hash-v1");
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

test("T15 network mode uses bundled metadata before downloading the official archive", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({ releaseTag: "v0.1.3", archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: "v0.1.3",
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
      bundled_metadata_sha256: sha256(Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8")),
    },
  });
  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: { NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}` },
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.planned_lockfile.generated.adapters[0].source, "release-archive");
  assert.equal(output.planned_lockfile.generated.adapters[0].archive_sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
});

test("T15 network mode rejects non-official archive URLs before fetch", () => {
  const cases = [
    ["data URL", "data:application/octet-stream;base64,AAAA"],
    ["wrong host", "https://example.com/rigorloop-adapter-codex-v0.1.3.zip"],
    ["wrong owner", "https://github.com/other/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip"],
    ["wrong release", "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.2/rigorloop-adapter-codex-v0.1.3.zip"],
    ["wrong archive", "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/other.zip"],
    ["query", "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip?download=1"],
    ["hash", "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip#fragment"],
    ["http", "http://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip"],
    ["raw", "https://raw.githubusercontent.com/xiongxianfei/rigorloop/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip"],
  ];

  for (const [name, url] of cases) {
    const cwd = tempProject();
    const fixture = fixtureArchive(cwd);
    fixture.metadata.artifacts[0].url = url;
    const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--json"], cwd, fixture.metadata);
    assert.equal(result.status, 3, name);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "error", name);
    assert.equal(output.errors[0].code, "non-official-archive-url", name);
    assert.equal(output.errors[0].path, "metadata.artifacts[codex].url", name);
    assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false, name);
  }
});

test("T15 official archive URL helper accepts only exact release archive URLs", () => {
  const releaseTag = "v0.1.3";
  const archive = "rigorloop-adapter-codex-v0.1.3.zip";
  const officialUrl = expectedArchiveUrl({ releaseTag, archive });
  assert.equal(officialUrl, "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip");
  assert.deepEqual(validateOfficialArchiveUrl({ url: officialUrl, releaseTag, archive }), { ok: true });
  assert.equal(
    validateOfficialArchiveUrl({
      url: "https://github.com/xiongxianfei/rigorloop/releases/download/v0.1.3/rigorloop-adapter-codex-v0.1.3.zip?download=1",
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
      release_tag: "v0.1.3",
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
      bundled_metadata_sha256: "0".repeat(64),
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

test("T16 bundled metadata bytes are verified before parsing", () => {
  const cwd = tempProject();
  const packageFixture = fixturePackage({
    metadata: "not-json",
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: "v0.1.3",
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
      bundled_metadata_sha256: "0".repeat(64),
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
  const officialUrl = expectedArchiveUrl({ releaseTag: "v0.1.3", archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({
    metadata: fixture.metadata,
    release: {
      source_repository: "xiongxianfei/rigorloop",
      release_tag: "v0.1.3",
      bundled_metadata: "adapter-artifacts-v0.1.3.json",
      bundled_metadata_sha256: sha256(Buffer.from(JSON.stringify(fixture.metadata, null, 2), "utf8")),
    },
  });

  const result = runCli(["init", "--adapter", "codex", "--json"], {
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
  assert.equal(output.status, "success");
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

test("T20 actual init writes minimum manifest, Codex install root, and lockfile", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.warnings.some((warning) => warning.code === "lockfile-spec-not-approved"), false);
  assert.deepEqual(output.actions.map((action) => action.path).slice(0, 4), [".agents", ".agents/skills", "rigorloop.yaml", "rigorloop.lock"]);
  assert.equal(actionFor(output, ".agents")?.status, "done");
  assert.equal(actionFor(output, ".agents/skills")?.status, "done");
  assert.equal(actionFor(output, "rigorloop.yaml")?.status, "done");
  assert.equal(actionFor(output, "rigorloop.lock")?.status, "done");
  assert.equal(existsSync(join(cwd, ".agents")), true);
  assert.equal(existsSync(join(cwd, ".agents", "skills")), true);
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), true);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), true);

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

test("T26 adapter file content conflicts fail installed-tree verification without replacing user files", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "proposal"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), "user file\n");
  const result = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json", "--force"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 3);
  assert.equal(readProjectFile(cwd, ".agents/skills/proposal/SKILL.md"), "user file\n");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "installed-tree-mismatch");
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
  const wrongRepoResult = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${wrongRepo.archiveName}`, "--json"], cwd, wrongRepo.metadata);

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
    ["init", "--adapter", "codex", "--from-archive", `./${missingField.archiveName}`, "--json"],
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
    ["init", "--adapter", "codex", "--from-archive", `./${validationFail.archiveName}`, "--json"],
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

test("T41 dry-run lockfile output is planned only and never durably written", () => {
  const newProject = tempProject();
  const dryRun = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd: newProject });

  assert.equal(dryRun.status, 0, dryRun.stderr);
  assert.equal(JSON.parse(dryRun.stdout).planned_lockfile.generated.adapters[0].tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.equal(existsSync(join(newProject, "rigorloop.lock")), false);
});

test("TLF-012 network install writes a complete lockfile after verification", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({ releaseTag: "v0.1.3", archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const result = runCli(["init", "--adapter", "codex", "--json"], {
    cwd,
    cliPath: packageFixture.cliPath,
    env: { NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}` },
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.warnings.some((warning) => warning.code === "lockfile-spec-not-approved"), false);
  assert.equal(actionFor(output, "rigorloop.lock")?.status, "done");
  assert.equal(output.artifacts.find((artifact) => artifact.path === "rigorloop.lock")?.status, "created");
  const parsed = parseLockfile(readProjectFile(cwd, "rigorloop.lock"));
  assert.equal(parsed.ok, true);
  const entry = parsed.lockfile.generated.adapters[0];
  assert.equal(parsed.lockfile.rigorloop.package, "@xiongxianfei/rigorloop");
  assert.equal(parsed.lockfile.rigorloop.version, "0.1.3");
  assert.equal(parsed.lockfile.manifest.path, "rigorloop.yaml");
  assert.equal(parsed.lockfile.manifest.sha256, sha256NormalizedText(readProjectFile(cwd, "rigorloop.yaml")));
  assert.equal(entry.release, "v0.1.3");
  assert.equal(entry.source, "release-archive");
  assert.equal(entry.archive, fixture.archiveName);
  assert.equal(entry.archive_sha256, fixture.metadata.artifacts[0].sha256);
  assert.equal(entry.installed_root, ".agents/skills");
  assert.equal(entry.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.equal(entry.tree_sha256, fixture.metadata.artifacts[0].tree_sha256);
  assert.equal(entry.file_count, 2);
});

test("TLF-013 and TLF-014 local archive install writes portable local-archive lockfile", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const absoluteArchivePath = fixture.archivePath;
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", absoluteArchivePath, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.warnings.some((warning) => warning.code === "lockfile-spec-not-approved"), false);
  const lockfile = readProjectFile(cwd, "rigorloop.lock");
  const parsed = parseLockfile(lockfile);
  assert.equal(parsed.ok, true);
  const entry = parsed.lockfile.generated.adapters[0];
  assert.equal(entry.source, "local-archive");
  assert.equal(entry.release, "v0.1.3");
  assert.equal(entry.archive, fixture.archiveName);
  assert.equal(entry.archive_sha256, fixture.metadata.artifacts[0].sha256);
  assert.doesNotMatch(lockfile, new RegExp(absoluteArchivePath.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  assert.doesNotMatch(lockfile, /\/tmp|\\\\|TOKEN|SECRET|hostname|username/);
});

test("TLF-013 failed verification does not create or update rigorloop.lock", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd, {
    metadata(metadata) {
      metadata.artifacts[0].sha256 = "0".repeat(64);
      return metadata;
    },
  });
  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
  assert.equal(JSON.parse(result.stdout).errors[0].code, "archive-sha-mismatch");
});

test("CR3-F1 pre-existing extra installed file fails tree verification before lockfile write", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "custom"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "custom", "NOTE.md"), "user file\n");

  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 3, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "installed-tree-mismatch");
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
  assert.equal(readProjectFile(cwd, ".agents/skills/custom/NOTE.md"), "user file\n");
});

test("CR3-F1 pre-existing modified or partial installed tree fails before lockfile write", () => {
  const modifiedProject = tempProject();
  const modifiedFixture = fixtureArchive(modifiedProject);
  mkdirSync(join(modifiedProject, ".agents", "skills", "proposal"), { recursive: true });
  mkdirSync(join(modifiedProject, ".agents", "skills", "verify"), { recursive: true });
  writeFileSync(join(modifiedProject, ".agents", "skills", "proposal", "SKILL.md"), "modified\n");
  writeFileSync(join(modifiedProject, ".agents", "skills", "verify", "SKILL.md"), "# Verify\n\nUse verify guidance.\n");

  const modified = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${modifiedFixture.archiveName}`, "--json"],
    modifiedProject,
    modifiedFixture.metadata,
  );

  assert.equal(modified.status, 3, modified.stderr);
  assert.equal(JSON.parse(modified.stdout).errors[0].code, "installed-tree-mismatch");
  assert.equal(existsSync(join(modifiedProject, "rigorloop.lock")), false);
  assert.equal(readProjectFile(modifiedProject, ".agents/skills/proposal/SKILL.md"), "modified\n");

  const partialProject = tempProject();
  const partialFixture = fixtureArchive(partialProject);
  mkdirSync(join(partialProject, ".agents", "skills", "proposal"), { recursive: true });
  writeFileSync(join(partialProject, ".agents", "skills", "proposal", "SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");

  const partial = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${partialFixture.archiveName}`, "--json"],
    partialProject,
    partialFixture.metadata,
  );

  assert.equal(partial.status, 3, partial.stderr);
  assert.equal(JSON.parse(partial.stdout).errors[0].code, "installed-tree-mismatch");
  assert.equal(existsSync(join(partialProject, "rigorloop.lock")), false);
});

test("CR3-F1 exact existing installed tree may create lockfile with trusted metadata tree", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  mkdirSync(join(cwd, ".agents", "skills", "proposal"), { recursive: true });
  mkdirSync(join(cwd, ".agents", "skills", "verify"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), "# Proposal\n\nUse proposal guidance.\n");
  writeFileSync(join(cwd, ".agents", "skills", "verify", "SKILL.md"), "# Verify\n\nUse verify guidance.\n");

  const result = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(result.status, 0, result.stderr);
  const parsed = parseLockfile(readProjectFile(cwd, "rigorloop.lock"));
  assert.equal(parsed.ok, true);
  const entry = parsed.lockfile.generated.adapters[0];
  assert.equal(entry.tree_sha256, fixture.metadata.artifacts[0].tree_sha256);
  assert.equal(entry.file_count, 2);
});

test("CR3-F1 installed-tree mismatch leaves existing lockfile unchanged", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const first = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);
  assert.equal(first.status, 0, first.stderr);
  const before = readProjectFile(cwd, "rigorloop.lock");

  mkdirSync(join(cwd, ".agents", "skills", "custom"), { recursive: true });
  writeFileSync(join(cwd, ".agents", "skills", "custom", "NOTE.md"), "user file\n");
  const rerun = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(rerun.status, 2, rerun.stderr);
  assert.equal(JSON.parse(rerun.stdout).blockers[0].code, "generated-output-drift");
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), before);
});

test("TLF-015 reinstall through a different source mode updates the Codex lockfile entry", () => {
  const existingProject = tempProject();
  const fixture = fixtureArchive(existingProject);
  const actual = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    existingProject,
    fixture.metadata,
  );

  assert.equal(actual.status, 0, actual.stderr);
  const firstLockfile = readProjectFile(existingProject, "rigorloop.lock");
  const archiveBytes = readFileSync(fixture.archivePath);
  const officialUrl = expectedArchiveUrl({ releaseTag: "v0.1.3", archive: fixture.archiveName });
  fixture.metadata.artifacts[0].url = officialUrl;
  const packageFixture = fixturePackage({ metadata: fixture.metadata });
  const rerun = runCli(["init", "--adapter", "codex", "--json"], {
    cwd: existingProject,
    cliPath: packageFixture.cliPath,
    env: { NODE_OPTIONS: `--import ${mockFetchModule(officialUrl, archiveBytes)}` },
  });

  assert.equal(rerun.status, 0, rerun.stderr);
  const first = parseLockfile(firstLockfile).lockfile;
  const second = parseLockfile(readProjectFile(existingProject, "rigorloop.lock")).lockfile;
  assert.equal(first.generated.adapters.length, 1);
  assert.equal(second.generated.adapters.length, 1);
  assert.equal(first.generated.adapters[0].source, "local-archive");
  assert.equal(second.generated.adapters[0].source, "release-archive");
  assert.equal(first.generated.adapters[0].tree_sha256, second.generated.adapters[0].tree_sha256);
});

test("TLF-023 and TLF-024 drifted generated file blocks before replacement", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const first = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);
  assert.equal(first.status, 0, first.stderr);
  const lockfileBefore = readProjectFile(cwd, "rigorloop.lock");
  const modifiedPath = ".agents/skills/proposal/SKILL.md";
  writeFileSync(join(cwd, modifiedPath), "modified generated output\n");

  const rerun = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(rerun.status, 2, rerun.stderr);
  const output = JSON.parse(rerun.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "generated-output-drift");
  assert.equal(output.blockers[0].adapter, "codex");
  assert.equal(output.blockers[0].installed_root, ".agents/skills");
  assert.equal(output.blockers[0].expected_tree_sha256, parseLockfile(lockfileBefore).lockfile.generated.adapters[0].tree_sha256);
  assert.match(output.blockers[0].actual_tree_sha256, /^[0-9a-f]{64}$/);
  assert.equal(readProjectFile(cwd, modifiedPath), "modified generated output\n");
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), lockfileBefore);
});

test("TLF-025 missing generated output root represented in lockfile blocks before replacement", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const first = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);
  assert.equal(first.status, 0, first.stderr);
  const lockfileBefore = readProjectFile(cwd, "rigorloop.lock");
  rmSync(join(cwd, ".agents", "skills"), { recursive: true, force: true });

  const rerun = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(rerun.status, 2, rerun.stderr);
  const output = JSON.parse(rerun.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "generated-output-missing");
  assert.equal(output.blockers[0].adapter, "codex");
  assert.equal(output.blockers[0].installed_root, ".agents/skills");
  assert.equal(output.blockers[0].expected_tree_sha256, parseLockfile(lockfileBefore).lockfile.generated.adapters[0].tree_sha256);
  assert.equal(existsSync(join(cwd, ".agents", "skills")), false);
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), lockfileBefore);
});

test("TLF-026 generated output root as file exits 5 with existing lockfile", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const first = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);
  assert.equal(first.status, 0, first.stderr);
  const lockfileBefore = readProjectFile(cwd, "rigorloop.lock");
  rmSync(join(cwd, ".agents", "skills"), { recursive: true, force: true });
  writeFileSync(join(cwd, ".agents", "skills"), "not a directory\n");

  const rerun = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(rerun.status, 5, rerun.stderr);
  const output = JSON.parse(rerun.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents/skills");
  assert.equal(readProjectFile(cwd, ".agents/skills"), "not a directory\n");
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), lockfileBefore);
});

test("TLF-027 generated file path as directory exits 5 without lockfile update", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  const first = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);
  assert.equal(first.status, 0, first.stderr);
  const lockfileBefore = readProjectFile(cwd, "rigorloop.lock");
  rmSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"), { force: true });
  mkdirSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md"));

  const rerun = runCliWithBundledMetadata(["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"], cwd, fixture.metadata);

  assert.equal(rerun.status, 5, rerun.stderr);
  const output = JSON.parse(rerun.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents/skills/proposal/SKILL.md");
  assert.equal(readProjectFile(cwd, "rigorloop.lock"), lockfileBefore);
});

test("TLF-001 valid lockfile fixture parses and serializes deterministically", () => {
  const parsed = parseLockfile(validLockfile());

  assert.equal(parsed.ok, true);
  assert.equal(parsed.lockfile.schema_version, 1);
  assert.equal(parsed.lockfile.rigorloop.package, "@xiongxianfei/rigorloop");
  assert.equal(parsed.lockfile.rigorloop.version, "0.1.3");
  assert.equal(parsed.lockfile.manifest.path, "rigorloop.yaml");
  assert.equal(parsed.lockfile.generated.adapters[0].adapter, "codex");
  assert.equal(parsed.lockfile.generated.adapters[0].tree_hash_algorithm, "rigorloop-tree-hash-v1");

  const first = serializeLockfile(parsed.lockfile);
  const second = serializeLockfile(parsed.lockfile);
  assert.equal(first, second);
  assert.doesNotMatch(first, /\/tmp|\\\\|generatedAt|username|hostname|TOKEN|SECRET/);
});

test("TLF-007 missing required lockfile fields are invalid config", () => {
  const missingPackage = validLockfile().replace('  package: "@xiongxianfei/rigorloop"\n', "");
  const parsed = parseLockfile(missingPackage);

  assert.equal(parsed.ok, false);
  assert.equal(parsed.kind, "invalid");
  assert.equal(parsed.code, "invalid-lockfile");
});

test("TLF-005 and TLF-006 unsupported lockfile shape blocks before mutation", () => {
  const cases = [
    ["unknown top-level", `${validLockfile()}\nfuture:\n  value: true\n`],
    ["unknown nested", validLockfile().replace("  version: \"0.1.3\"\n", "  version: \"0.1.3\"\n  future: true\n")],
    ["unknown rigorloop mapping", lockfileWithUnknownMapping("rigorloop")],
    ["unknown manifest mapping", lockfileWithUnknownMapping("manifest")],
    ["unknown generated mapping", lockfileWithUnknownMapping("generated")],
    ["unknown adapter mapping", lockfileWithUnknownMapping("adapter")],
    ["unsupported schema", validLockfile({ schemaVersion: 2 })],
    ["unsupported adapter", validLockfile({ adapter: "claude" })],
    ["unsupported source", validLockfile({ source: "mirror" })],
    ["unsupported tree hash", validLockfile({ treeHashAlgorithm: "other-tree-hash" })],
  ];

  for (const [name, text] of cases) {
    const parsed = parseLockfile(text);
    assert.equal(parsed.ok, false, name);
    assert.equal(parsed.kind, "unsupported", name);
    assert.equal(parsed.code, "unsupported-lockfile-shape", name);
  }
});

test("TLF-003 dry-run write plan includes rigorloop.lock and writes nothing", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(actionFor(output, "rigorloop.lock")?.type, "write");
  assert.equal(actionFor(output, "rigorloop.lock")?.status, "planned");
  assert.equal(output.artifacts.find((artifact) => artifact.path === "rigorloop.lock")?.status, "planned");
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);
});

test("TLF-004 malformed existing lockfile blocks before mutation with exit 4", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  writeFileSync(join(cwd, "rigorloop.lock"), "not: [valid\n");
  const result = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 4, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-lockfile");
  assert.equal(actionFor(output, "rigorloop.lock")?.status, "blocked");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("TLF-005 existing lockfile with unknown fields blocks before mutation with exit 2", () => {
  const cwd = tempProject();
  const fixture = fixtureArchive(cwd);
  writeFileSync(join(cwd, "rigorloop.lock"), `${validLockfile()}\nfuture:\n  value: true\n`);
  const result = runCliWithBundledMetadata(
    ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
    cwd,
    fixture.metadata,
  );

  assert.equal(result.status, 2, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "unsupported-lockfile-shape");
  assert.equal(actionFor(output, "rigorloop.lock")?.status, "blocked");
  assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false);
});

test("TLF-005 existing lockfile with unknown nested mapping blocks before mutation with exit 2", () => {
  for (const [name, lockfile] of [
    ["rigorloop", lockfileWithUnknownMapping("rigorloop")],
    ["adapter", lockfileWithUnknownMapping("adapter")],
  ]) {
    const cwd = tempProject();
    const fixture = fixtureArchive(cwd);
    writeFileSync(join(cwd, "rigorloop.lock"), lockfile);
    const result = runCliWithBundledMetadata(
      ["init", "--adapter", "codex", "--from-archive", `./${fixture.archiveName}`, "--json"],
      cwd,
      fixture.metadata,
    );

    assert.equal(result.status, 2, name);
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, "blocked", name);
    assert.equal(output.blockers[0].code, "unsupported-lockfile-shape", name);
    assert.equal(actionFor(output, "rigorloop.lock")?.status, "blocked", name);
    assert.equal(existsSync(join(cwd, ".agents", "skills", "proposal", "SKILL.md")), false, name);
  }
});

test("TLF-008 manifest normalization hash is stable", () => {
  const withCrLf = 'schema_version: 1\r\nrigorloop:\r\n  package: "@xiongxianfei/rigorloop"\r\n';
  const withLf = 'schema_version: 1\nrigorloop:\n  package: "@xiongxianfei/rigorloop"\n';

  assert.equal(sha256NormalizedText(Buffer.from(withCrLf, "utf8")), sha256NormalizedText(Buffer.from(withLf, "utf8")));
});
