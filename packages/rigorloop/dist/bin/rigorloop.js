#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { inflateRawSync } from "node:zlib";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { EXIT, exitCodeForResult } from "../lib/command-result.js";

const ADAPTER = "codex";
const AGENTS_ROOT = ".agents";
const INSTALL_ROOT = ".agents/skills";
const DIRECTORY_PLAN = [AGENTS_ROOT, INSTALL_ROOT];
const LOCKFILE_WARNING = {
  code: "lockfile-spec-not-approved",
  message: "rigorloop.lock was not written because the durable lockfile contract is not approved.",
};

function packageInfo() {
  const here = dirname(fileURLToPath(import.meta.url));
  const packageJsonPath = join(here, "..", "..", "package.json");
  const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
  if (!packageJson.name || !packageJson.version) {
    throw new Error("Package name or version is missing.");
  }
  return {
    name: packageJson.name,
    version: packageJson.version,
  };
}

function parseFlags(args) {
  const flags = {
    json: false,
    quiet: false,
    debug: false,
    noColor: Boolean(process.env.NO_COLOR),
    dryRun: false,
    adapter: undefined,
    fromArchiveProvided: false,
    fromArchive: undefined,
    force: false,
  };

  const positional = [];
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--json") {
      flags.json = true;
    } else if (arg === "--quiet") {
      flags.quiet = true;
    } else if (arg === "--debug") {
      flags.debug = true;
    } else if (arg === "--no-color") {
      flags.noColor = true;
    } else if (arg === "--dry-run") {
      flags.dryRun = true;
    } else if (arg === "--adapter") {
      if (args[index + 1] && !args[index + 1].startsWith("--")) {
        flags.adapter = args[index + 1];
        index += 1;
      }
    } else if (arg === "--from-archive") {
      flags.fromArchiveProvided = true;
      if (args[index + 1] && !args[index + 1].startsWith("--")) {
        flags.fromArchive = args[index + 1];
        index += 1;
      }
    } else if (arg === "--force") {
      flags.force = true;
    } else {
      positional.push(arg);
    }
  }

  return { flags, positional };
}

function envelope(command, flags, overrides = {}) {
  const diagnostics = flags.debug ? { debug: true } : {};
  return {
    schema_version: 1,
    command,
    package: packageInfo(),
    cwd: process.cwd(),
    status: "success",
    summary: "",
    actions: [],
    artifacts: [],
    blockers: [],
    warnings: [],
    errors: [],
    diagnostics,
    ...overrides,
  };
}

function writeJson(result) {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

function writeHuman(message, flags) {
  if (!flags.quiet) {
    process.stdout.write(message);
  }
}

function usage() {
  return `RigorLoop CLI

Usage:
  rigorloop --help
  rigorloop version
  rigorloop init --adapter codex [--dry-run] [--json]

Commands:
  version                 Print package name and version.
  init --adapter codex    Initialize the first-slice Codex adapter plan.
`;
}

function releaseForPackage(version) {
  return `v${version}`;
}

function sourceForFlags(flags, info) {
  if (flags.fromArchiveProvided) {
    return {
      type: "local-archive",
      archive: flags.fromArchive,
    };
  }

  return {
    type: "release-archive",
    release: releaseForPackage(info.version),
    archive: `rigorloop-adapter-codex-${releaseForPackage(info.version)}.zip`,
  };
}

function manifestContent(info, source) {
  const sourceLines =
    source.type === "local-archive"
      ? [`      type: local-archive`, `      archive: "${source.archive}"`]
      : [`      type: release-archive`, `      release: "${source.release}"`];

  return `schema_version: 1
rigorloop:
  package: "${info.name}"
  package_version: "${info.version}"
adapters:
  - name: codex
    install_root: "${INSTALL_ROOT}"
    source:
${sourceLines.join("\n")}
`;
}

function plannedLockfile(source) {
  const artifact = source.artifact;
  return {
    schema_version: 1,
    tree_hash_algorithm: "rigorloop-tree-hash-v1",
    generated: {
      adapters: [
        {
          adapter: ADAPTER,
          source: source.type,
          archive: source.type === "local-archive" ? basename(source.archive) : source.archive,
          archive_sha256: artifact?.sha256 ?? "<planned>",
          installed_root: INSTALL_ROOT,
          tree_sha256: artifact?.tree_sha256 ?? "<planned-after-install>",
        },
      ],
    },
  };
}

function compatibleManifest(content) {
  return (
    content.includes("schema_version: 1") &&
    content.includes("name: codex") &&
    content.includes(`install_root: "${INSTALL_ROOT}"`)
  );
}

function pathState(path) {
  if (!existsSync(path)) {
    return "absent";
  }
  return statSync(path).isDirectory() ? "directory" : "file";
}

function directoryKind(path) {
  return path === AGENTS_ROOT ? "codex-agent-root" : "codex-install-root";
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

function metadataDirectory() {
  const here = dirname(fileURLToPath(import.meta.url));
  return join(here, "..", "metadata");
}

function releaseIndexPath() {
  return join(metadataDirectory(), "releases.json");
}

function loadReleaseDescriptor(info) {
  const release = releaseForPackage(info.version);
  let index;
  try {
    index = loadJsonFile(releaseIndexPath());
  } catch {
    return {
      blocker: metadataBlocker(
        "metadata-trust-root-unavailable",
        "Bundled release metadata index is unavailable.",
        "releases.json",
        "Use a CLI package version that bundles release metadata for this adapter release.",
      ),
    };
  }

  const descriptor = index?.schema_version === 1 ? index.releases?.[release] : undefined;
  if (!descriptor || descriptor.source_repository !== "xiongxianfei/rigorloop" || !isNonEmptyString(descriptor.bundled_metadata)) {
    return {
      blocker: metadataBlocker(
        "metadata-trust-root-unavailable",
        `Bundled release metadata index does not define a trusted Codex metadata source for ${release}.`,
        "releases.json",
        "Use a CLI package version that bundles release metadata for this adapter release.",
      ),
    };
  }
  return { descriptor };
}

function loadNetworkReleaseDescriptor(info) {
  const release = loadReleaseDescriptor(info);
  if (release.blocker) {
    return release;
  }
  const descriptor = release.descriptor;
  if (!isNonEmptyString(descriptor.metadata_url) || !isSha256(descriptor.metadata_sha256)) {
    return {
      blocker: metadataBlocker(
        "metadata-trust-root-unavailable",
        "Bundled release metadata index is missing a trusted metadata URL or SHA-256.",
        "releases.json",
        "Use a CLI package version that bundles a trusted release metadata hash.",
      ),
    };
  }
  return { descriptor };
}

function bundledMetadataPath(info) {
  const release = loadReleaseDescriptor(info);
  if (release.blocker) {
    return { blocker: release.blocker };
  }
  return { path: join(metadataDirectory(), release.descriptor.bundled_metadata) };
}

function loadJsonFile(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

async function fetchBytes(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return Buffer.from(await response.arrayBuffer());
}

function parseVerifiedMetadataBytes(bytes, expectedSha256) {
  const actualSha256 = sha256(bytes);
  if (actualSha256 !== expectedSha256) {
    return {
      error: {
        code: "metadata-sha256-mismatch",
        message: "Release metadata SHA-256 does not match the bundled release index.",
      },
    };
  }
  try {
    return { metadata: JSON.parse(bytes.toString("utf8")) };
  } catch (error) {
    return {
      error: {
        code: "metadata-invalid",
        message: `Release metadata JSON is invalid: ${error.message}`,
      },
    };
  }
}

function metadataBlocker(code, message, path, nextAction = "Use a compatible verified Codex adapter archive.") {
  return {
    code,
    message,
    path,
    next_action: nextAction,
  };
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.length > 0;
}

function isSha256(value) {
  return typeof value === "string" && /^[0-9a-f]{64}$/i.test(value);
}

function validateMetadata(metadata, info) {
  const release = releaseForPackage(info.version);
  if (!metadata || metadata.schema_version !== 1) {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata schema_version must be 1.") };
  }
  if (metadata.release?.version !== release || metadata.release?.release_tag !== release) {
    return {
      blocker: metadataBlocker("release-version-incompatible", `Adapter metadata is not compatible with ${release}.`),
    };
  }
  if (metadata.release?.source_repository !== "xiongxianfei/rigorloop") {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata source repository is not trusted.") };
  }
  if (!isNonEmptyString(metadata.release?.source_commit) || !isNonEmptyString(metadata.release?.published_at)) {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata release identity is incomplete.") };
  }
  if (!isNonEmptyString(metadata.metadata?.url) || !isSha256(metadata.metadata?.sha256)) {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata URL or SHA-256 is missing or invalid.") };
  }
  if (metadata.validation?.result !== "pass") {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata validation result is not pass.") };
  }
  if (!isNonEmptyString(metadata.validation?.command)) {
    return { blocker: metadataBlocker("metadata-invalid", "Adapter metadata validation command is missing.") };
  }
  const artifact = metadata.artifacts?.find((entry) => entry.adapter === ADAPTER);
  if (!artifact) {
    return { blocker: metadataBlocker("adapter-unknown", "Adapter metadata does not include Codex.") };
  }
  if (
    !isNonEmptyString(artifact.archive) ||
    !isNonEmptyString(artifact.url) ||
    !isSha256(artifact.sha256) ||
    !Number.isInteger(artifact.size_bytes) ||
    artifact.size_bytes < 0 ||
    !isSha256(artifact.tree_sha256)
  ) {
    return { blocker: metadataBlocker("metadata-invalid", "Codex adapter artifact metadata is incomplete.") };
  }
  if ((artifact.install_root ?? "").replace(/\/$/, "") !== INSTALL_ROOT) {
    return { blocker: metadataBlocker("metadata-invalid", "Codex adapter install root is not .agents/skills.") };
  }
  if (artifact.tree_hash_algorithm && artifact.tree_hash_algorithm !== "rigorloop-tree-hash-v1") {
    return { blocker: metadataBlocker("metadata-invalid", "Unsupported tree hash algorithm in adapter metadata.") };
  }
  return { artifact };
}

function readUInt16(buffer, offset) {
  return buffer.readUInt16LE(offset);
}

function readUInt32(buffer, offset) {
  return buffer.readUInt32LE(offset);
}

function findEndOfCentralDirectory(buffer) {
  for (let offset = buffer.length - 22; offset >= 0; offset -= 1) {
    if (readUInt32(buffer, offset) === 0x06054b50) {
      return offset;
    }
  }
  throw Object.assign(new Error("Archive is not a valid ZIP file."), { code: "archive-invalid" });
}

function parseZipEntries(buffer) {
  const eocd = findEndOfCentralDirectory(buffer);
  const entryCount = readUInt16(buffer, eocd + 10);
  const centralOffset = readUInt32(buffer, eocd + 16);
  let offset = centralOffset;
  const entries = [];

  for (let index = 0; index < entryCount; index += 1) {
    if (readUInt32(buffer, offset) !== 0x02014b50) {
      throw Object.assign(new Error("Archive central directory is invalid."), { code: "archive-invalid" });
    }
    const method = readUInt16(buffer, offset + 10);
    const compressedSize = readUInt32(buffer, offset + 20);
    const uncompressedSize = readUInt32(buffer, offset + 24);
    const nameLength = readUInt16(buffer, offset + 28);
    const extraLength = readUInt16(buffer, offset + 30);
    const commentLength = readUInt16(buffer, offset + 32);
    const externalAttributes = readUInt32(buffer, offset + 38);
    const localOffset = readUInt32(buffer, offset + 42);
    const name = buffer.subarray(offset + 46, offset + 46 + nameLength).toString("utf8");

    if (readUInt32(buffer, localOffset) !== 0x04034b50) {
      throw Object.assign(new Error("Archive local header is invalid."), { code: "archive-invalid" });
    }
    const localNameLength = readUInt16(buffer, localOffset + 26);
    const localExtraLength = readUInt16(buffer, localOffset + 28);
    const dataStart = localOffset + 30 + localNameLength + localExtraLength;
    const compressed = buffer.subarray(dataStart, dataStart + compressedSize);
    let bytes;
    if (method === 0) {
      bytes = compressed;
    } else if (method === 8) {
      bytes = inflateRawSync(compressed);
    } else {
      throw Object.assign(new Error("Archive uses unsupported compression."), { code: "archive-unsupported-compression" });
    }
    if (bytes.length !== uncompressedSize) {
      throw Object.assign(new Error("Archive entry size is invalid."), { code: "archive-invalid" });
    }

    const unixMode = (externalAttributes >>> 16) & 0xffff;
    entries.push({
      name,
      bytes,
      directory: name.endsWith("/"),
      symlink: (unixMode & 0o170000) === 0o120000,
    });
    offset += 46 + nameLength + extraLength + commentLength;
  }

  return entries;
}

function unsafePathCode(name) {
  if (!name || name.startsWith("/") || name.startsWith("\\") || /^[A-Za-z]:/.test(name) || name.includes("\\")) {
    return "archive-path-traversal";
  }
  if (name.split("/").some((part) => part === ".." || part === "")) {
    return "archive-path-traversal";
  }
  if (!name.startsWith(`${INSTALL_ROOT}/`)) {
    return "archive-install-root-invalid";
  }
  return undefined;
}

function isArchiveSupportEntry(name) {
  return name === "AGENTS.md";
}

function fileRowsForTree(entries) {
  return entries
    .filter((entry) => !entry.directory)
    .map((entry) => {
      const relativePath = entry.name.slice(`${INSTALL_ROOT}/`.length);
      const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
      return [relativePath, sha256(bytes)];
    })
    .sort(([left], [right]) => left.localeCompare(right));
}

function treeHashForEntries(entries) {
  const manifest = `rigorloop-tree-hash-v1\n${fileRowsForTree(entries)
    .map(([path, hash]) => `${path}\t${hash}`)
    .join("\n")}\n`;
  return sha256(Buffer.from(manifest, "utf8"));
}

function inspectArchive(archiveBytes, artifact) {
  if (artifact.size_bytes !== undefined && archiveBytes.length !== artifact.size_bytes) {
    return { error: { code: "archive-size-mismatch", message: "Archive size does not match metadata." } };
  }
  const archiveHash = sha256(archiveBytes);
  if (artifact.sha256 && archiveHash !== artifact.sha256) {
    return { error: { code: "archive-sha-mismatch", message: "Archive SHA-256 does not match metadata." } };
  }

  let entries;
  try {
    entries = parseZipEntries(archiveBytes);
  } catch (error) {
    return { error: { code: error.code ?? "archive-invalid", message: error.message } };
  }

  const installEntries = [];
  for (const entry of entries) {
    if (isArchiveSupportEntry(entry.name)) {
      continue;
    }
    const pathCode = unsafePathCode(entry.name);
    if (pathCode) {
      return { error: { code: pathCode, message: `Archive entry is not allowed: ${entry.name}`, path: entry.name } };
    }
    if (entry.symlink) {
      return { error: { code: "archive-symlink-entry", message: `Archive symlink entry is not allowed: ${entry.name}`, path: entry.name } };
    }
    installEntries.push(entry);
  }

  const files = installEntries.filter((entry) => !entry.directory);
  const treeHash = treeHashForEntries(files);
  if (artifact.tree_sha256 && treeHash !== artifact.tree_sha256) {
    return { error: { code: "tree-hash-mismatch", message: "Installed tree hash does not match metadata." } };
  }
  return { entries: files, archiveHash, treeHash };
}

function addArchiveActions(plan, entries) {
  const directories = new Set();
  for (const entry of entries) {
    const parts = entry.name.split("/");
    parts.pop();
    while (parts.length > 2) {
      directories.add(parts.join("/"));
      parts.pop();
    }
  }
  for (const directory of [...directories].sort()) {
    const state = pathState(resolve(process.cwd(), directory));
    plan.actions.push({
      type: "create-dir",
      path: directory,
      status: state === "absent" ? "pending" : state === "directory" ? "skipped" : "blocked",
      reason: state === "absent" ? `Create ${directory}.` : state === "directory" ? `${directory} already exists.` : `${directory} exists and is not a directory.`,
    });
    plan.artifacts.push({
      path: directory,
      kind: "adapter-directory",
      status: state === "absent" ? "pending" : state === "directory" ? "existing" : "blocked",
    });
    if (state === "file") {
      plan.blockers.push({
        code: "overwrite-refused",
        message: `${directory} exists and is not a directory.`,
        path: directory,
        next_action: "Move the existing file before running init.",
      });
    }
  }
  for (const entry of entries) {
    const state = pathState(resolve(process.cwd(), entry.name));
    plan.actions.push({
      type: "copy",
      path: entry.name,
      status: state === "absent" ? "pending" : "blocked",
      reason: state === "absent" ? "Install verified Codex adapter file." : `${entry.name} already exists.`,
    });
    plan.artifacts.push({
      path: entry.name,
      kind: "adapter-file",
      status: state === "absent" ? "pending" : "blocked",
    });
    if (state !== "absent") {
      plan.blockers.push({
        code: "overwrite-refused",
        message: `${entry.name} already exists.`,
        path: entry.name,
        next_action: "Move the existing file before running init.",
      });
    }
  }
}

function writeArchiveEntries(entries) {
  for (const entry of entries) {
    const outputPath = resolve(process.cwd(), entry.name);
    mkdirSync(dirname(outputPath), { recursive: true });
    const relativePath = entry.name.slice(`${INSTALL_ROOT}/`.length);
    const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
    writeFileSync(outputPath, bytes);
  }
}

function planDirectoryActions(flags) {
  const actions = [];
  const artifacts = [];
  const blockers = [];
  let parentBlocked = false;

  for (const relativePath of DIRECTORY_PLAN) {
    const state = parentBlocked ? "blocked-by-parent" : pathState(resolve(process.cwd(), relativePath));
    if (state === "absent") {
      actions.push({
        type: "create-dir",
        path: relativePath,
        status: flags.dryRun ? "planned" : "pending",
        reason: `Create ${relativePath}.`,
      });
      artifacts.push({
        path: relativePath,
        kind: directoryKind(relativePath),
        status: flags.dryRun ? "planned" : "pending",
      });
    } else if (state === "directory") {
      actions.push({
        type: "create-dir",
        path: relativePath,
        status: "skipped",
        reason: `${relativePath} already exists.`,
      });
      artifacts.push({
        path: relativePath,
        kind: directoryKind(relativePath),
        status: "existing",
      });
    } else {
      actions.push({
        type: "create-dir",
        path: relativePath,
        status: "blocked",
        reason:
          state === "blocked-by-parent"
            ? `${relativePath} cannot be created because ${AGENTS_ROOT} is not a directory.`
            : `${relativePath} exists and is not a directory.`,
      });
      artifacts.push({
        path: relativePath,
        kind: directoryKind(relativePath),
        status: "blocked",
      });
      if (state !== "blocked-by-parent") {
        blockers.push({
          code: "overwrite-refused",
          message: `${relativePath} exists and is not a directory.`,
          path: relativePath,
          next_action: `Move the existing file before running init.`,
        });
      }
      if (relativePath === AGENTS_ROOT) {
        parentBlocked = true;
      }
    }
  }

  return { actions, artifacts, blockers };
}

function buildInitPlan(flags, artifact) {
  const info = packageInfo();
  const source = sourceForFlags(flags, info);
  if (artifact) {
    source.artifact = artifact;
  }
  const manifestPath = "rigorloop.yaml";
  const manifestAbsolutePath = resolve(process.cwd(), manifestPath);
  const manifest = manifestContent(info, source);
  const actions = [];
  const artifacts = [];
  const blockers = [];
  const errors = [];

  if (flags.fromArchiveProvided && (!flags.fromArchive || flags.fromArchive.startsWith("--"))) {
    errors.push({
      code: "invalid-archive-path",
      message: "Missing required value for --from-archive.",
      path: "--from-archive",
      next_action: "Provide an existing Codex adapter archive path or omit --from-archive.",
    });
  } else if (flags.fromArchiveProvided && !existsSync(resolve(process.cwd(), flags.fromArchive))) {
    errors.push({
      code: "invalid-archive-path",
      message: `Local archive path does not exist: ${flags.fromArchive}`,
      path: flags.fromArchive,
      next_action: "Provide an existing Codex adapter archive path or omit --from-archive.",
    });
  }

  const directoryPlan = planDirectoryActions(flags);
  actions.push(...directoryPlan.actions);
  artifacts.push(...directoryPlan.artifacts);
  blockers.push(...directoryPlan.blockers);

  if (existsSync(manifestAbsolutePath)) {
    const existingManifest = readFileSync(manifestAbsolutePath, "utf8");
    if (compatibleManifest(existingManifest)) {
      actions.push({
        type: "write",
        path: manifestPath,
        status: flags.dryRun ? "planned" : "skipped",
        reason: "Compatible rigorloop.yaml already exists.",
      });
      artifacts.push({
        path: manifestPath,
        kind: "project-manifest",
        status: "existing",
      });
    } else {
      errors.push({
        code: "invalid-config",
        message: "Existing rigorloop.yaml is not compatible with the first-slice Codex init contract.",
        path: manifestPath,
        next_action: "Review or move the existing file before running init.",
      });
    }
  } else {
    actions.push({
      type: "write",
      path: manifestPath,
      status: flags.dryRun ? "planned" : "pending",
      reason: "Create first-slice RigorLoop project manifest.",
    });
    artifacts.push({
      path: manifestPath,
      kind: "project-manifest",
      status: flags.dryRun ? "planned" : "pending",
    });
  }

  return {
    info,
    source,
    manifest,
    actions,
    artifacts,
    blockers,
    errors,
    planned_lockfile: plannedLockfile(source),
  };
}

function handleHelp(flags) {
  writeHuman(usage(), flags);
  return EXIT.success;
}

function handleVersion(flags) {
  const info = packageInfo();
  writeHuman(`${info.name} ${info.version}\n`, flags);
  return EXIT.success;
}

function commandError(command, message, flags, error) {
  if (flags.json) {
    writeJson(
      envelope(command, flags, {
        status: "error",
        summary: message,
        errors: [error],
      }),
    );
  } else {
    process.stderr.write(`${message}\n${error.next_action ?? "Run rigorloop --help."}\n`);
  }
  return exitCodeForResult({ status: "error", exit_class: "invalid_usage" });
}

function invalidUsage(message, flags, command = "unknown") {
  return commandError(command, message, flags, {
    code: "invalid-usage",
    message,
    next_action: "Run rigorloop --help.",
  });
}

function invalidArchivePath(message, flags) {
  return commandError("init", message, flags, {
    code: "invalid-archive-path",
    message,
    path: flags.fromArchive,
    next_action: "Provide an existing Codex adapter archive path or omit --from-archive.",
  });
}

function unsupportedAdapter(adapter, flags) {
  const result = envelope("init", flags, {
    status: "blocked",
    summary: `Adapter '${adapter}' is not supported in this slice.`,
    blockers: [
      {
        code: "adapter-unsupported",
        message: `Adapter '${adapter}' is not supported in this slice.`,
        next_action: "Use --adapter codex.",
      },
    ],
  });

  if (flags.json) {
    writeJson(result);
  } else {
    process.stderr.write(`${result.summary}\nUse --adapter codex.\n`);
  }
  return exitCodeForResult({ ...result, exit_class: "blocked" });
}

function writeBlockedResult(flags, plan, summary, blockers, exitClass = "blocked") {
  for (const action of plan.actions) {
    if (action.status === "pending") {
      action.status = "blocked";
      action.reason = "Blocked before mutation.";
    }
  }
  for (const artifact of plan.artifacts) {
    if (artifact.status === "pending") {
      artifact.status = "blocked";
    }
  }
  const result = envelope("init", flags, {
    status: "blocked",
    summary,
    actions: plan.actions,
    artifacts: plan.artifacts,
    blockers,
    planned_manifest: {
      path: "rigorloop.yaml",
      content: plan.manifest,
    },
    planned_lockfile: plan.planned_lockfile,
  });
  if (flags.json) {
    writeJson(result);
  } else {
    process.stderr.write(`${result.summary}\n${blockers[0]?.next_action ?? "Resolve the blocker before running init."}\n`);
  }
  return exitCodeForResult({ ...result, exit_class: exitClass });
}

function writeValidationErrorResult(flags, plan, error) {
  for (const action of plan.actions) {
    if (action.status === "pending") {
      action.status = "blocked";
      action.reason = "Blocked by archive verification failure.";
    }
  }
  for (const artifact of plan.artifacts) {
    if (artifact.status === "pending") {
      artifact.status = "blocked";
    }
  }
  const result = envelope("init", flags, {
    status: "error",
    summary: error.message,
    actions: plan.actions,
    artifacts: plan.artifacts,
    errors: [error],
    planned_manifest: {
      path: "rigorloop.yaml",
      content: plan.manifest,
    },
    planned_lockfile: plan.planned_lockfile,
  });
  if (flags.json) {
    writeJson(result);
  } else {
    process.stderr.write(`${result.summary}\n`);
  }
  return exitCodeForResult({ ...result, exit_class: "validation_failed" });
}

async function archiveWorkForInit(flags, info) {
  if (flags.dryRun) {
    return {};
  }

  if (flags.fromArchiveProvided) {
    let metadata;
    const bundled = bundledMetadataPath(info);
    if (bundled.blocker) {
      return {
        blocker: metadataBlocker(
          "metadata-unavailable",
          "Bundled adapter metadata is unavailable for Codex v0.1.3.",
          "adapter-artifacts-v0.1.3.json",
          "Use a CLI package version that bundles metadata for this adapter release.",
        ),
      };
    }
    try {
      metadata = loadJsonFile(bundled.path);
    } catch {
      return {
        blocker: metadataBlocker(
          "metadata-unavailable",
          "Bundled adapter metadata is unavailable for Codex v0.1.3.",
          "adapter-artifacts-v0.1.3.json",
          "Use a CLI package version that bundles metadata for this adapter release.",
        ),
      };
    }
    const validation = validateMetadata(metadata, info);
    if (validation.blocker) {
      return { blocker: validation.blocker };
    }
    const artifact = validation.artifact;
    const archiveName = basename(flags.fromArchive);
    if (archiveName !== artifact.archive || !archiveName.includes(metadata.release.version)) {
      return {
        blocker: metadataBlocker(
          "release-version-incompatible",
          `Local archive ${archiveName} is not compatible with ${metadata.release.version}.`,
          flags.fromArchive,
          "Use the Codex adapter archive matching the installed CLI package version.",
        ),
      };
    }
    const archiveBytes = readFileSync(resolve(process.cwd(), flags.fromArchive));
    const inspected = inspectArchive(archiveBytes, artifact);
    if (inspected.error) {
      return { error: inspected.error, artifact };
    }
    return { artifact, entries: inspected.entries, archiveHash: inspected.archiveHash, treeHash: inspected.treeHash };
  }

  const release = loadNetworkReleaseDescriptor(info);
  if (release.blocker) {
    return { blocker: release.blocker };
  }
  const descriptor = release.descriptor;
  let metadataBytes;
  try {
    metadataBytes = await fetchBytes(descriptor.metadata_url);
  } catch {
    return {
      blocker: metadataBlocker(
        "release-unavailable",
        "Official Codex adapter release metadata is unavailable.",
        descriptor.metadata_url,
        "Retry later or use --from-archive with a compatible local archive.",
      ),
    };
  }
  const verifiedMetadata = parseVerifiedMetadataBytes(metadataBytes, descriptor.metadata_sha256);
  if (verifiedMetadata.error) {
    return { error: verifiedMetadata.error };
  }
  const metadata = verifiedMetadata.metadata;
  const validation = validateMetadata(metadata, info);
  if (validation.blocker) {
    return { blocker: validation.blocker };
  }
  const artifact = validation.artifact;
  let archiveBytes;
  try {
    archiveBytes = await fetchBytes(artifact.url);
  } catch {
    return {
      blocker: metadataBlocker(
        "release-unavailable",
        "Official Codex adapter archive is unavailable.",
        artifact.url,
        "Retry later or use --from-archive with a compatible local archive.",
      ),
    };
  }
  const inspected = inspectArchive(archiveBytes, artifact);
  if (inspected.error) {
    return { error: inspected.error, artifact };
  }
  return { artifact, entries: inspected.entries, archiveHash: inspected.archiveHash, treeHash: inspected.treeHash };
}

async function handleInit(flags) {
  if (!flags.adapter) {
    return invalidUsage("Missing required option: --adapter codex.", flags, "init");
  }
  if (flags.adapter !== "codex") {
    return unsupportedAdapter(flags.adapter, flags);
  }
  if (flags.fromArchiveProvided && (!flags.fromArchive || flags.fromArchive.startsWith("--"))) {
    return invalidArchivePath("Missing required value for --from-archive.", flags);
  }
  if (flags.fromArchiveProvided && !existsSync(resolve(process.cwd(), flags.fromArchive))) {
    return invalidArchivePath(`Local archive path does not exist: ${flags.fromArchive}`, flags);
  }

  const info = packageInfo();
  const plan = buildInitPlan(flags);
  if (plan.errors.length > 0) {
    const result = envelope("init", flags, {
      status: "error",
      summary: plan.errors[0].message,
      actions: plan.actions,
      artifacts: plan.artifacts,
      errors: plan.errors,
      planned_manifest: {
        path: "rigorloop.yaml",
        content: plan.manifest,
      },
      planned_lockfile: plan.planned_lockfile,
    });
    if (flags.json) {
      writeJson(result);
    } else {
      process.stderr.write(`${result.summary}\n${plan.errors[0].next_action}\n`);
    }
    return exitCodeForResult({ ...result, exit_class: "invalid_usage" });
  }
  if (plan.blockers.length > 0) {
    return writeBlockedResult(flags, plan, plan.blockers[0].message, plan.blockers, "mutation_conflict");
  }

  const archiveWork = await archiveWorkForInit(flags, info);
  if (archiveWork.artifact) {
    plan.source.artifact = archiveWork.artifact;
    plan.planned_lockfile = plannedLockfile(plan.source);
  }
  if (archiveWork.entries) {
    addArchiveActions(plan, archiveWork.entries);
  }

  if (archiveWork.blocker) {
    return writeBlockedResult(flags, plan, archiveWork.blocker.message, [archiveWork.blocker]);
  }
  if (archiveWork.error) {
    return writeValidationErrorResult(flags, plan, archiveWork.error);
  }
  if (plan.blockers.length > 0) {
    return writeBlockedResult(flags, plan, plan.blockers[0].message, plan.blockers, "mutation_conflict");
  }

  if (!flags.dryRun) {
    const manifestAction = plan.actions.find((action) => action.path === "rigorloop.yaml");
    const directoryActions = plan.actions.filter((action) => action.type === "create-dir" && action.status === "pending");
    for (const directoryAction of directoryActions) {
      mkdirSync(resolve(process.cwd(), directoryAction.path));
      directoryAction.status = "done";
      plan.artifacts.find((artifact) => artifact.path === directoryAction.path).status = "created";
    }
    if (manifestAction?.status === "pending") {
      writeFileSync(resolve(process.cwd(), "rigorloop.yaml"), plan.manifest, "utf8");
      manifestAction.status = "done";
      plan.artifacts.find((artifact) => artifact.path === "rigorloop.yaml").status = "created";
    }
    if (archiveWork.entries) {
      try {
        writeArchiveEntries(archiveWork.entries);
        for (const action of plan.actions.filter((action) => action.type === "copy" && action.status === "pending")) {
          action.status = "done";
          plan.artifacts.find((artifact) => artifact.path === action.path).status = "created";
        }
      } catch (error) {
        const result = envelope("init", flags, {
          status: "error",
          summary: "Adapter installation failed after scaffold writes.",
          actions: plan.actions,
          artifacts: plan.artifacts,
          errors: [
            {
              code: "partial-installation-failed",
              message: error.message,
              partial_state: "scaffold files may have been written; adapter files may be incomplete.",
            },
          ],
          planned_manifest: {
            path: "rigorloop.yaml",
            content: plan.manifest,
          },
          planned_lockfile: plan.planned_lockfile,
        });
        if (flags.json) {
          writeJson(result);
        } else {
          process.stderr.write(`${result.summary}\n${error.message}\n`);
        }
        return exitCodeForResult({ ...result, exit_class: "internal" });
      }
    }
  }

  const warnings = flags.dryRun ? [] : [LOCKFILE_WARNING];
  const result = envelope("init", flags, {
    status: warnings.length > 0 ? "warning" : "success",
    summary: flags.dryRun
      ? "RigorLoop init dry run completed. No files were written."
      : archiveWork.entries
        ? "RigorLoop initialized with verified Codex adapter files."
        : "RigorLoop initialized with Codex scaffold.",
    actions: plan.actions,
    artifacts: plan.artifacts,
    warnings,
    planned_manifest: {
      path: "rigorloop.yaml",
      content: plan.manifest,
    },
    planned_lockfile: plan.planned_lockfile,
  });

  if (flags.json) {
    writeJson(result);
  } else {
    const lines = flags.dryRun
      ? ["RigorLoop init dry run completed.", "No files were written."]
      : [
          "RigorLoop initialized with Codex scaffold.",
          "rigorloop.lock was not written because the durable lockfile contract is not approved.",
        ];
    writeHuman(`${lines.join("\n")}\n`, flags);
  }
  return exitCodeForResult({ ...result, exit_class: "success" });
}

async function main() {
  try {
    const { flags, positional } = parseFlags(process.argv.slice(2));
    const [command] = positional;

    if (!command || command === "--help" || command === "-h") {
      return handleHelp(flags);
    }
    if (command === "version") {
      return handleVersion(flags);
    }
    if (command === "init") {
      return handleInit(flags);
    }

    return invalidUsage(`Unknown command: ${command}`, flags);
  } catch (error) {
    process.stderr.write(`Unexpected error: ${error.message}\n`);
    return exitCodeForResult({ status: "error", exit_class: "internal" });
  }
}

process.exitCode = await main();
