#!/usr/bin/env node

import { lstatSync, existsSync, readFileSync, realpathSync } from "node:fs";
import { createHash } from "node:crypto";
import { inflateRawSync } from "node:zlib";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { installCandidate } from "../lib/installer-replacement.js";

import { EXIT, exitCodeForResult } from "../lib/command-result.js";
import { adapterDescriptor, supportedAdapterNames } from "../lib/adapters.js";
import { validateOfficialArchiveUrl } from "../lib/official-archive-url.js";
import { runObservedCli } from "../lib/cli-observability.js";
import { resolveLogConfig } from "../lib/log-config.js";
import { isInvocationId, createInvocationId } from "../lib/diagnostic-event.js";
import { findInvocationEvents } from "../lib/log-inspection.js";
import { renderResult, RESULT_FORMATS } from "../lib/result-renderer.js";

const RECORDING_FAMILIES = new Set(["status","context","subject","change","activity","work","review","finding","blocker","evidence","applicability","decision","decisions","verify","observations","batch"]);
const isRecordingCommand = argv => RECORDING_FAMILIES.has(argv[0]);
const isRetiredCommand = argv => {
  const retired = command => ["compact", "lifecycle", "new-change"].includes(command);
  if (retired(parseFlags(argv).positional[0])) return true;
  try {
    // Reuse the pure logging grammar without inspecting environment overrides
    // or opening a sink. Leading logging options cannot restore file effects.
    return retired(parseFlags(resolveLogConfig(argv, {env: {}}).args).positional[0]);
  } catch { return false; }
};

let activeOutput = {};

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
    adapterOptionUsed: false,
    writeState: false,
    fromArchiveProvided: false,
    fromArchive: undefined,
    force: false,
    format: undefined,
    formatError: false,
  };

  const positional = [];
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--json") {
      flags.json = true;
      flags.format = "json";
    } else if (arg === "--format") {
      const value = args[++index];
      if (!RESULT_FORMATS.includes(value)) flags.formatError = true;
      else {
        flags.format = value;
        flags.json = value !== "human";
      }
    } else if (arg === "--quiet") {
      flags.quiet = true;
    } else if (arg === "--debug") {
      flags.debug = true;
    } else if (arg === "--no-color") {
      flags.noColor = true;
    } else if (arg === "--dry-run") {
      flags.dryRun = true;
    } else if (arg === "--adapter") {
      flags.adapterOptionUsed = true;
      if (args[index + 1] && !args[index + 1].startsWith("--")) {
        flags.adapter = args[index + 1];
        index += 1;
      }
    } else if (arg === "--write-state") {
      flags.writeState = true;
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
  if (["concise-json", "concise-human", "detailed-json"].includes(activeOutput.format)) {
    activeOutput.deferredRender = ({ invocationId, observability, exitCode }) => ({
      stdout: renderResult(result, {
        format: activeOutput.format,
        invocationId,
        observability,
        exitCode,
      }),
      stderr: "",
    });
  } else writeStdout(`${JSON.stringify(result, null, 2)}\n`);
}

function writeHuman(message, flags) {
  if (!flags.quiet) {
    writeStdout(message);
  }
}

function writeStdout(message) {
  activeOutput.stdout += message;
}

function writeStderr(message) {
  activeOutput.stderr += message;
}

function usage() {
  return `RigorLoop CLI

Usage:
  rigorloop --help
  rigorloop version
  rigorloop init codex|claude [--force] [--dry-run] [--json]
  --force: Replace existing destination skills. Local changes within replaced skill directories will be lost.
  rigorloop workflow-context [--change <id>] [--format human|json]
  rigorloop status --root PATH --change ID [--format text|json]
  rigorloop context --root PATH --change ID --input - [--format text|json]
  rigorloop subject inspect --root PATH --path FILE [--content none|full] [--format text|json]
  rigorloop <record-kind> show [ID] --root PATH --change ID [--format text|json]
  rigorloop <record-kind> add|set|record [ID] --root PATH --change ID --input - [--dry-run] [--format text|json]
  rigorloop change create|link --root PATH --change ID --input - [--dry-run] [--format text|json]
  rigorloop batch --root PATH --change ID --input - [--dry-run] [--format text|json]
  rigorloop record-store inspect --root PATH --change ID [--format text|json]
  rigorloop record-store check|record --root PATH --change ID --input - [--format text|json]
  rigorloop record-store recover --root PATH --change ID --transaction ID --expected-recovery DIGEST --action restore|complete [--format text|json]
  rigorloop logs path [--format human|json]
  rigorloop logs show <invocation-id> [--format human|json]

Commands:
  version                 Print package name and version.
  init codex|claude
                          Initialize verified target support.
  workflow-context        Report read-only project or exact-change workflow facts.
  status/context/show     Inspect explicitly selected recorded information; storage only.
  add/set/record/batch     Record explicit actor decisions; use per-command --help for exact selectors.
  record-store            Advanced inspection, replacement and recovery for v2/v3 records; storage only.
  logs                    Show the local log path or inspect one exact invocation.
`;
}

function logCommandFormat(args) {
  const index = args.indexOf("--format");
  if (index < 0) return "human";
  return args[index + 1];
}

function handleLogs(args, invocation) {
  const [operation, identity] = args;
  const format = logCommandFormat(args);
  if (!["human", "json"].includes(format)) {
    activeOutput.terminalClass = "expected-rejection";
    writeStderr("RL_INVALID_REQUEST: unknown log output format\n");
    return 4;
  }
  if (operation === "show" && identity && !isInvocationId(identity)) {
    activeOutput.terminalClass = "expected-rejection";
    const result = { schema_version: 1, command: "logs", operation: "show", status: "error", code: "RL_INVALID_INVOCATION_ID", events: [], warnings: [] };
    if (format === "human") writeStderr("RL_INVALID_INVOCATION_ID: invalid invocation identity\n");
    else writeStdout(`${JSON.stringify(result, null, 2)}\n`);
    return 4;
  }
  if (invocation.loggingIssue) {
    activeOutput.terminalClass = "logging-failure";
    const code = invocation.loggingIssue.code ?? "RL_LOG_UNAVAILABLE";
    const result = { schema_version: 1, command: "logs", operation, status: "error", errors: [{ code }] };
    if (format === "human") writeStderr(`${code}: local log storage is unavailable\n`);
    else writeStdout(`${JSON.stringify(result, null, 2)}\n`);
    return 3;
  }
  if (operation === "path") {
    activeOutput.terminalClass = "success";
    const result = { schema_version: 1, command: "logs", operation: "path", status: "success", path: invocation.logDirectory };
    writeStdout(format === "human" ? `${result.path}\n` : `${JSON.stringify(result, null, 2)}\n`);
    return 0;
  }
  if (operation === "show" && identity) {
    const lookup = findInvocationEvents(invocation.logDirectory, identity);
    const result = { schema_version: 1, command: "logs", operation: "show", invocation_id: identity, ...lookup };
    if (format === "human") {
      if (lookup.status === "error") writeStderr(`${lookup.code}: invocation ${identity} was not available\n`);
      else writeStdout(`${lookup.events.map((event) => JSON.stringify(event)).join("\n")}\n`);
    } else writeStdout(`${JSON.stringify(result, null, 2)}\n`);
    activeOutput.terminalClass = lookup.status === "success"
      ? "success"
      : lookup.status === "warning"
        ? "diagnostic-warning"
        : lookup.code === "RL_LOG_NOT_FOUND"
          ? "expected-rejection"
          : "logging-failure";
    return lookup.status === "error" ? (lookup.code === "RL_INVALID_INVOCATION_ID" ? 4 : 3) : 0;
  }
  activeOutput.terminalClass = "expected-rejection";
  writeStderr("RL_INVALID_REQUEST: logs requires path or show <invocation-id>\n");
  return 4;
}

function releaseForPackage(version) {
  return `v${version}`;
}


function rootsForArtifact(descriptor, artifact) {
  if (artifact?.install_roots) {
    return artifact.install_roots;
  }
  if (artifact?.install_root) {
    return { skills: artifact.install_root };
  }
  return descriptor.installRoots;
}


function pathState(path) {
  try { return lstatSync(path).isDirectory() ? "directory" : "file"; }
  catch (error) { if (["ENOENT", "ENOTDIR"].includes(error.code)) return "absent"; throw error; }
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
  if (
    !descriptor ||
    descriptor.source_repository !== "xiongxianfei/rigorloop" ||
    descriptor.release_tag !== release ||
    !isNonEmptyString(descriptor.bundled_metadata)
  ) {
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

function loadVerifiedBundledMetadata(info) {
  const release = loadReleaseDescriptor(info);
  const releaseTag = releaseForPackage(info.version);
  if (release.blocker) {
    return release;
  }
  const descriptor = release.descriptor;
  if (!isSha256(descriptor.bundled_metadata_sha256)) {
    return {
      blocker: metadataBlocker(
        "metadata-trust-root-unavailable",
        "Bundled release metadata index is missing a trusted bundled metadata SHA-256.",
        "releases.json",
        "Use a CLI package version that bundles a trusted adapter metadata hash.",
      ),
    };
  }
  let metadataBytes;
  try {
    metadataBytes = readFileSync(join(metadataDirectory(), descriptor.bundled_metadata));
  } catch {
    return {
      blocker: metadataBlocker(
        "metadata-unavailable",
        `Bundled adapter metadata is unavailable for Codex ${releaseTag}.`,
        descriptor.bundled_metadata,
        "Use a CLI package version that bundles metadata for this adapter release.",
      ),
    };
  }
  const verifiedMetadata = parseVerifiedMetadataBytes(metadataBytes, descriptor.bundled_metadata_sha256);
  if (verifiedMetadata.error) {
    return { error: verifiedMetadata.error };
  }
  return { metadata: verifiedMetadata.metadata, descriptor };
}

function loadJsonFile(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

async function fetchBytes(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw Object.assign(new Error(`HTTP ${response.status}`), { downloadFailureClass: "http-status" });
  }
  return Buffer.from(await response.arrayBuffer());
}

const PROXY_ENV_VAR_ALLOWLIST = ["HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy"];
const DOWNLOAD_FAILURE_CLASSES = new Set(["dns", "tls", "timeout", "http-status", "proxy", "network", "unknown"]);

function detectedProxyEnvVars(env = process.env) {
  return PROXY_ENV_VAR_ALLOWLIST.filter((name) => Object.prototype.hasOwnProperty.call(env, name) && env[name]);
}

function nodeEnvProxyStatus(env = process.env, execArgv = process.execArgv) {
  const nodeOptions = String(env.NODE_OPTIONS ?? "");
  const useEnvProxy = String(env.NODE_USE_ENV_PROXY ?? "").toLowerCase();
  // CR-M4-R1-F1: Node can enable fetch env-proxy via env vars or the runtime flag.
  if (nodeOptions.includes("--use-env-proxy") || execArgv.includes("--use-env-proxy") || ["1", "true", "yes"].includes(useEnvProxy)) {
    return "enabled";
  }
  if (detectedProxyEnvVars(env).length > 0) {
    return "disabled";
  }
  return "unknown";
}

function downloadFailureClass(error) {
  if (DOWNLOAD_FAILURE_CLASSES.has(error?.downloadFailureClass)) {
    return error.downloadFailureClass;
  }
  const code = String(error?.code ?? error?.cause?.code ?? "").toUpperCase();
  const message = String(error?.message ?? "").toLowerCase();
  if (["ENOTFOUND", "EAI_AGAIN"].includes(code)) {
    return "dns";
  }
  if (code.includes("CERT") || code.includes("TLS") || message.includes("certificate") || message.includes("tls")) {
    return "tls";
  }
  if (code.includes("TIMEOUT") || code === "ABORT_ERR" || message.includes("timeout") || message.includes("timed out")) {
    return "timeout";
  }
  if (code.includes("PROXY") || message.includes("proxy")) {
    return "proxy";
  }
  if (["ECONNRESET", "ECONNREFUSED", "EHOSTUNREACH", "ENETUNREACH"].includes(code) || message.includes("fetch failed")) {
    return "network";
  }
  return "unknown";
}

function downloadFailureDiagnostics(error, artifact, descriptor, metadata) {
  return {
    adapter: descriptor.name,
    release: metadata.release.version,
    archive_url: artifact.url,
    download_failure_class: downloadFailureClass(error),
    node_env_proxy_status: nodeEnvProxyStatus(),
    proxy_env_vars_detected: detectedProxyEnvVars(),
  };
}

function downloadFailureBlocker(error, artifact, descriptor, metadata) {
  const diagnostics = downloadFailureDiagnostics(error, artifact, descriptor, metadata);
  return {
    code: "release-download-failed",
    message: `Network download failed for adapter ${descriptor.name} release ${metadata.release.version} (failure class ${diagnostics.download_failure_class}).`,
    path: artifact.url,
    next_action: `Download ${artifact.url} and rerun with --from-archive ./${artifact.archive}.`,
    diagnostics,
  };
}

function parseVerifiedMetadataBytes(bytes, expectedSha256) {
  const actualSha256 = sha256(bytes);
  if (actualSha256 !== expectedSha256) {
    return {
      error: {
        code: "metadata-sha256-mismatch",
        message: "Bundled adapter metadata SHA-256 does not match the bundled release index.",
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


function validateMetadata(metadata, info, descriptor) {
  const release = releaseForPackage(info.version);
  if (!metadata || metadata.schema_version !== 1) {
    return { error: { code: "metadata-invalid", message: "Adapter metadata schema_version must be 1." } };
  }
  if (metadata.release?.version !== release || metadata.release?.release_tag !== release) {
    return {
      blocker: metadataBlocker("release-version-incompatible", `Adapter metadata is not compatible with ${release}.`),
    };
  }
  if (metadata.release?.source_repository !== "xiongxianfei/rigorloop") {
    return { error: { code: "metadata-invalid", message: "Adapter metadata source repository is not trusted." } };
  }
  if (!isNonEmptyString(metadata.release?.source_commit) || !isNonEmptyString(metadata.release?.published_at)) {
    return { error: { code: "metadata-invalid", message: "Adapter metadata release identity is incomplete." } };
  }
  if (!isNonEmptyString(metadata.metadata?.url) || !isSha256(metadata.metadata?.sha256)) {
    return { error: { code: "metadata-invalid", message: "Adapter metadata URL or SHA-256 is missing or invalid." } };
  }
  if (metadata.validation?.result !== "pass") {
    return { error: { code: "metadata-invalid", message: "Adapter metadata validation result is not pass." } };
  }
  if (!isNonEmptyString(metadata.validation?.command)) {
    return { error: { code: "metadata-invalid", message: "Adapter metadata validation command is missing." } };
  }
  const artifact = metadata.artifacts?.find((entry) => entry.adapter === descriptor.name);
  if (!artifact) {
    return { blocker: metadataBlocker("metadata-unavailable", `Adapter metadata does not include ${descriptor.displayName}.`) };
  }
  if (!isNonEmptyString(artifact.archive) || !isNonEmptyString(artifact.url) || !isSha256(artifact.sha256) || !Number.isInteger(artifact.size_bytes) || artifact.size_bytes < 0) {
    return { error: { code: "metadata-invalid", message: `${descriptor.displayName} adapter artifact metadata is incomplete.` } };
  }
  if (artifact.tree_hash_algorithm && artifact.tree_hash_algorithm !== "rigorloop-tree-hash-v1") {
    return { error: { code: "metadata-invalid", message: "Unsupported tree hash algorithm in adapter metadata." } };
  }
  if (artifact.install_roots || artifact.root_hashes) {
    if (!artifact.install_roots || !artifact.root_hashes) {
      return { error: { code: "metadata-invalid", message: `${descriptor.displayName} multi-root metadata is incomplete.` } };
    }
    for (const [role, root] of Object.entries(artifact.install_roots)) {
      if (descriptor.installRoots[role] !== root) {
        return { error: { code: "metadata-invalid", message: `${descriptor.displayName} adapter install root for ${role} is not supported.` } };
      }
      const rootHash = artifact.root_hashes[role];
      if (!rootHash || !isSha256(rootHash.tree_sha256) || !Number.isInteger(rootHash.file_count) || rootHash.file_count < 0) {
        return { error: { code: "metadata-invalid", message: `${descriptor.displayName} root hash metadata is incomplete.` } };
      }
    }
  } else {
    if (!isSha256(artifact.tree_sha256) || !Number.isInteger(artifact.file_count) || artifact.file_count < 0) {
      return { error: { code: "metadata-invalid", message: `${descriptor.displayName} adapter single-root metadata is incomplete.` } };
    }
    if ((artifact.install_root ?? "").replace(/\/$/, "") !== descriptor.primaryInstallRoot()) {
      return { error: { code: "metadata-invalid", message: `${descriptor.displayName} adapter install root is not ${descriptor.primaryInstallRoot()}.` } };
    }
  }
  if (artifact.command_aliases || artifact.skills_only_compatibility) return {error: {code: "metadata-invalid", message: "Retired command aliases are unsupported."}};
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

function unsafePathCode(name, descriptor, artifact) {
  if (!name || name.startsWith("/") || name.startsWith("\\") || /^[A-Za-z]:/.test(name) || name.includes("\\")) {
    return "archive-path-traversal";
  }
  if (name.split("/").some((part) => part === ".." || part === "")) {
    return "archive-path-traversal";
  }
  const allowedRoots = Object.values(rootsForArtifact(descriptor, artifact));
  if (!allowedRoots.some((root) => name.startsWith(`${root}/`))) {
    return "archive-install-root-invalid";
  }
  return undefined;
}

function isArchiveSupportEntry(name) {
  return name === "AGENTS.md" || name === "CLAUDE.md";
}

function fileRowsForTreeRoot(entries, installRoot) {
  return entries
    .filter((entry) => !entry.directory && entry.name.startsWith(`${installRoot}/`))
    .map((entry) => {
      const relativePath = entry.name.slice(`${installRoot}/`.length);
      const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
      return [relativePath, sha256(bytes)];
    })
    .sort(([left], [right]) => left.localeCompare(right));
}


function rootHashesForEntries(entries, descriptor, artifact) {
  return Object.fromEntries(
    Object.entries(rootsForArtifact(descriptor, artifact)).map(([role, root]) => {
      const rows = fileRowsForTreeRoot(entries, root);
      return [
        role,
        {
          tree_sha256: treeHashForRows(rows),
          file_count: rows.length,
        },
      ];
    }),
  );
}

function treeHashForRows(rows) {
  const manifest = `rigorloop-tree-hash-v1\n${rows.map(([path, hash]) => `${path}\t${hash}`).join("\n")}\n`;
  return sha256(Buffer.from(manifest, "utf8"));
}


function presentPath(path) {
  try { lstatSync(resolve(process.cwd(), path)); return true; }
  catch (error) { if (["ENOENT", "ENOTDIR"].includes(error.code)) return false; throw error; }
}

function authoringPaths(descriptor, skill) {
  return [`${descriptor.primaryInstallRoot()}/${skill}`];
}

function retiredAuthoringPaths(descriptor, entries) {
  return ["spec", "architecture"].flatMap(skill => authoringPaths(descriptor, skill)).filter(path =>
    entries ? entries.some(entry => entry.name === path || entry.name.startsWith(`${path}/`)) : presentPath(path));
}


function obsoleteWorkflowSkillBlocker(descriptor, entries = []) {
  const installRoot = descriptor.primaryInstallRoot();
  const obsoletePath = `${installRoot}/workflow`;
  const replacementPath = `${installRoot}/route`;
  const archiveHasObsolete = entries.some(
    (entry) => entry.name === obsoletePath || entry.name.startsWith(`${obsoletePath}/`),
  );
  const archiveHasReplacement = entries.some(
    (entry) => entry.name === replacementPath || entry.name.startsWith(`${replacementPath}/`),
  );
  const installedObsolete = pathState(resolve(process.cwd(), obsoletePath)) !== "absent";
  const installedReplacement = pathState(resolve(process.cwd(), replacementPath)) !== "absent";

  if (!archiveHasObsolete && !installedObsolete) {
    return undefined;
  }

  const mixed = archiveHasReplacement || installedReplacement;
  return {
    code: mixed ? "mixed-route-workflow-skills" : "obsolete-workflow-skill",
    message: mixed
      ? `Current ${descriptor.displayName} skill inventory contains both obsolete workflow and replacement route packages.`
      : `Current ${descriptor.displayName} skill inventory contains the obsolete workflow package.`,
    path: obsoletePath,
    replacement: "route",
    next_action: `Remove ${obsoletePath}, then install and invoke route. Persisted workflow.automation state does not require migration.`,
  };
}


function inspectArchive(archiveBytes, artifact, descriptor) {
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
    const pathCode = unsafePathCode(entry.name, descriptor, artifact);
    if (pathCode) {
      return { error: { code: pathCode, message: `Archive entry is not allowed: ${entry.name}`, path: entry.name } };
    }
    if (entry.symlink) {
      return { error: { code: "archive-symlink-entry", message: `Archive symlink entry is not allowed: ${entry.name}`, path: entry.name } };
    }
    installEntries.push(entry);
  }

  const files = installEntries.filter((entry) => !entry.directory);
  const rootHashes = rootHashesForEntries(files, descriptor, artifact);
  for (const [role, hash] of Object.entries(rootHashes)) {
    const expected = artifact.root_hashes?.[role] ?? { tree_sha256: artifact.tree_sha256, file_count: artifact.file_count };
    if (expected.tree_sha256 && hash.tree_sha256 !== expected.tree_sha256) {
      return { error: { code: "tree-hash-mismatch", message: "Installed tree hash does not match metadata." } };
    }
    if (expected.file_count !== undefined && hash.file_count !== expected.file_count) {
      return { error: { code: "tree-hash-mismatch", message: "Installed tree file count does not match metadata." } };
    }
  }
  return { entries: files, archiveHash, rootHashes, treeHash: rootHashes.skills?.tree_sha256, fileCount: rootHashes.skills?.file_count ?? files.length };
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
    writeStderr(`${message}\n${error.next_action ?? "Run rigorloop --help."}\n`);
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
    next_action: "Provide an existing supported adapter archive path or omit --from-archive.",
  });
}

function unsupportedAdapter(adapter, flags) {
  const result = envelope("init", flags, {
    status: "blocked",
    summary: adapter === 'opencode' ? 'OpenCode support is retired. Use Codex or Claude Code.' : `Target '${adapter}' is not supported.`,
    blockers: [
      {
        code: "target-unknown",
        message: `Target '${adapter}' is not supported.`,
        next_action: `Use one of: ${supportedAdapterNames().join(", ")}.`,
      },
    ],
  });

  if (flags.json) {
    writeJson(result);
  } else {
    writeStderr(`${result.summary}\nUse one of: ${supportedAdapterNames().join(", ")}.\n`);
  }
  return exitCodeForResult({ ...result, exit_class: "blocked" });
}

function removedAdapterSyntax(flags) {
  const targets = supportedAdapterNames();
  const result = envelope("init", flags, {
    status: "error",
    summary: "`init --adapter` was removed in RigorLoop 0.3.0.",
    errors: [
      {
        code: "adapter-option-removed",
        message: "`init --adapter` was removed in RigorLoop 0.3.0.",
        next_action: `Use target-native init: ${targets.map((target) => `rigorloop init ${target}`).join(", ")}.`,
      },
    ],
  });
  if (flags.json) {
    writeJson(result);
  } else {
    writeStderr(`${result.summary}\n${result.errors[0].next_action}\n`);
  }
  return exitCodeForResult({ ...result, exit_class: "invalid_usage" });
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
  });
  if (blockers[0]?.diagnostics) {
    result.diagnostics = { ...result.diagnostics, ...blockers[0].diagnostics };
  }
  if (flags.json) {
    writeJson(result);
  } else {
    writeStderr(`${result.summary}\n${blockers.map(b => b.path ?? "").filter(Boolean).join("\n")}\n${blockers[0]?.next_action ?? "Resolve the blocker before running init."}\n`);
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
  });
  if (flags.json) {
    writeJson(result);
  } else {
    writeStderr(`${result.summary}\n`);
  }
  return exitCodeForResult({ ...result, exit_class: "validation_failed" });
}

async function archiveWorkForInit(flags, info, descriptor) {


  const bundledMetadata = loadVerifiedBundledMetadata(info);
  if (bundledMetadata.blocker || bundledMetadata.error) {
    if (flags.dryRun) {
      return {};
    }
    return bundledMetadata;
  }
  const metadata = bundledMetadata.metadata;
  const validation = validateMetadata(metadata, info, descriptor);
  if (validation.blocker || validation.error) {
    if (flags.dryRun) return {};
    return validation;
  }
  const artifact = validation.artifact;
  if (flags.dryRun) return {artifact};

  if (flags.fromArchiveProvided) {
    const archiveName = basename(flags.fromArchive);
    if (archiveName !== artifact.archive || !archiveName.includes(metadata.release.version)) {
      if (!archiveName.startsWith(`rigorloop-adapter-${descriptor.name}-`)) {
        return {
          error: {
            code: "adapter-archive-mismatch",
            message: `Local archive ${archiveName} is not a ${descriptor.displayName} adapter archive.`,
            path: flags.fromArchive,
          },
          artifact,
        };
      }
      return {
        blocker: metadataBlocker(
          "release-version-incompatible",
          `Local archive ${archiveName} is not compatible with ${metadata.release.version}.`,
          flags.fromArchive,
          `Use the ${descriptor.displayName} adapter archive matching the installed CLI package version.`,
        ),
      };
    }
    const archiveBytes = readFileSync(resolve(process.cwd(), flags.fromArchive));
    const inspected = inspectArchive(archiveBytes, artifact, descriptor);
    if (inspected.error) {
      return { error: inspected.error, artifact };
    }
    return { artifact, entries: inspected.entries, archiveHash: inspected.archiveHash, treeHash: inspected.treeHash };
  }

  let archiveBytes;
  const urlValidation = validateOfficialArchiveUrl({
    url: artifact.url,
    releaseTag: metadata.release.version,
    archive: artifact.archive,
  });
  if (!urlValidation.ok) {
    return {
      error: {
        code: urlValidation.code,
        message: urlValidation.message,
        path: urlValidation.path ?? "metadata.artifacts[codex].url",
      },
      artifact,
    };
  }
  try {
    archiveBytes = await fetchBytes(artifact.url);
  } catch (error) {
    return {
      blocker: downloadFailureBlocker(error, artifact, descriptor, metadata),
    };
  }
  const inspected = inspectArchive(archiveBytes, artifact, descriptor);
  if (inspected.error) {
    return { error: inspected.error, artifact };
  }
  return { artifact, entries: inspected.entries, archiveHash: inspected.archiveHash, treeHash: inspected.treeHash };
}

async function handleInit(flags, initArgs = []) {
  if (flags.adapterOptionUsed) return removedAdapterSyntax(flags);
  if (flags.writeState) return writeBlockedResult(flags, {actions: [], artifacts: []}, "--write-state is retired.", [{code: "state-writing-retired", message: "Installation does not manage project state.", next_action: "Install without --write-state; use --force only for explicit destination replacement."}]);
  if (initArgs.length !== 1) return invalidUsage(`init requires exactly one target: ${supportedAdapterNames().join(", ")}.`, flags, "init");
  const descriptor = adapterDescriptor(initArgs[0]);
  if (!descriptor) return unsupportedAdapter(initArgs[0], flags);
  if (flags.fromArchiveProvided && (!flags.fromArchive || !existsSync(resolve(flags.fromArchive)))) return invalidArchivePath("Provide an existing local archive path.", flags);
  const plan = {actions: [], artifacts: []};
  const archive = await archiveWorkForInit(flags, packageInfo(), descriptor);
  if (archive.error) return writeValidationErrorResult(flags, plan, archive.error);
  if (archive.blocker) return writeBlockedResult(flags, plan, archive.blocker.message, [archive.blocker]);
  const retired = retiredAuthoringPaths(descriptor, archive.entries);
  const installedRetired = retiredAuthoringPaths(descriptor);
  if (retired.length || installedRetired.length) {
    const paths = [...new Set([...retired, ...installedRetired])];
    return writeBlockedResult(flags, plan, "Retired authoring entries require separate inspection.", paths.map(path => ({code: retired.includes(path) ? "retired-authoring-candidate" : "retired-authoring-installation", path, message: `Retired entry: ${path}`, next_action: "Preserve local content and inspect the exact retired entry separately. Use a package containing design. --force does not remove noncandidate entries."})));
  }
  const obsolete = obsoleteWorkflowSkillBlocker(descriptor, archive.entries);
  if (obsolete) return writeBlockedResult(flags, plan, obsolete.message, [obsolete]);
  const root = descriptor.primaryInstallRoot();
  const files = archive.entries?.map(entry => ({path: entry.name, content: entry.name.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes})) ?? (archive.artifact?.skill_names ?? []).map(name => ({path: `${root}/${name}/SKILL.md`, content: Buffer.alloc(0)}));
  let installed = {units: [], conflicts: [], completed: [], retained: []};
  try {
    if (files.length) installed = installCandidate({projectRoot: process.cwd(), files, roots: [root], force: flags.force, dryRun: flags.dryRun});
    else if (!flags.dryRun) throw new Error("Verified archive contains no installable files.");
  } catch (error) {
    if (error.conflicts) return writeBlockedResult(flags, plan, "Installation stopped: destination skills already exist.", error.conflicts.map(path => ({code: "destination-conflict", path, message: `Existing destination: ${path}`, next_action: "Run again with --force to replace these skills. Local changes within replaced skill directories will be lost."})), "mutation_conflict");
    const result = envelope("init", flags, {status: "blocked", summary: error.message, completed: error.completed ?? [], failed: error.failed ?? null, untouched: error.untouched ?? [], retained: error.retained ?? [], blockers: [{code: error.code ?? "partial-installation-failed", message: error.message, next_action: "Preserve partial files and retained originals; inspect the reported paths before retrying. --force does not bypass safety checks."}]});
    if (flags.json) writeJson(result); else writeStderr(`${result.summary}\n${JSON.stringify({completed: result.completed, failed: result.failed, untouched: result.untouched, retained: result.retained})}\n`);
    return exitCodeForResult({...result, exit_class: "mutation_conflict"});
  }
  const result = envelope("init", flags, {
    status: "success",
    summary: flags.dryRun ? `RigorLoop init dry run: ${descriptor.displayName} installation; archive verification and complete destination preflight are unperformed.` : `Installed ${descriptor.displayName} skills.`,
    actions: installed.units.map(path => ({path, action: installed.conflicts.includes(path) ? (flags.force ? "replace" : "conflict") : "create", status: flags.dryRun ? "planned" : "completed"})),
    artifacts: archive.artifact ? [archive.artifact] : [],
    planned_target: {target: descriptor.name, install_root: root},
    completed: installed.completed, retained: installed.retained,
    state_files: {action: "skipped", reason: "Installation does not read or write project state."},
    ...(flags.dryRun ? {unperformed_checks: ["archive acquisition", "archive verification", "complete candidate preflight"], preliminary_conflicts: installed.conflicts} : {}),
    warnings: flags.force ? [{code: "explicit-replacement", message: "Replace existing destination skills. Local changes within replaced skill directories will be lost."}] : [],
  });
  if (flags.json) writeJson(result); else writeHuman(`${result.summary}\n${result.actions.map(a => `${a.action}: ${a.path}`).join("\n")}\n${result.retained.map(r => `Retained original: ${r.path} -> ${r.backup}`).join("\n")}\n${flags.force ? result.warnings[0].message : ""}\n`, flags);
  return EXIT.success;
}

async function dispatchMain(rawArgs, invocation) {
  try {
    if (isRecordingCommand(rawArgs)) {
      const {executeRecordingCli} = await import("../lib/recording-cli.js");
      const execution = executeRecordingCli(rawArgs, invocation.recordStoreOptions);
      activeOutput.terminalClass = execution.exitCode === 0 ? "success" : "expected-rejection";
      activeOutput.deferredRender = () => ({stdout: execution.format === "json" ? execution.json : execution.human, stderr: ""});
      return execution.exitCode;
    }
    // Contract-separated explicit recording; no lifecycle transition evaluator.
    if (rawArgs[0] === "record-store") {
      const { executeRecordStoreCli } = await import("../lib/record-store-cli.js");
      const execution = executeRecordStoreCli(rawArgs.slice(1), invocation.recordStoreOptions);
      activeOutput.terminalClass = execution.exitCode === 0 ? "success" : "expected-rejection";
      activeOutput.deferredRender = () => execution.format === "json"
        ? { stdout: `${JSON.stringify(execution.result)}\n`, stderr: "" }
        : execution.exitCode === 0 ? { stdout: execution.human, stderr: "" } : { stdout: "", stderr: execution.human };
      return execution.exitCode;
    }
    if (rawArgs[0] === "logs") return handleLogs(rawArgs.slice(1), invocation);
    if (rawArgs[0] === "workflow-context") {
      const { executeWorkflowContext } = await import("../lib/workflow-context.js");
      const execution = executeWorkflowContext(rawArgs.slice(1));
      activeOutput.terminalClass = execution.exitCode === 0 ? "success" : execution.exitCode === 2 || execution.exitCode === 4 ? "expected-rejection" : "internal-error";
      activeOutput.deferredRender = () => execution.format === "json"
        ? { stdout: `${JSON.stringify(execution.result, null, 2)}\n`, stderr: "" }
        : execution.exitCode === 0
          ? { stdout: execution.human, stderr: "" }
          : { stdout: "", stderr: execution.human };
      return execution.exitCode;
    }
    const { flags, positional } = parseFlags(rawArgs);
    activeOutput.format = flags.format;
    if (flags.formatError) return invalidUsage("Unknown result format.", flags);
    const [command] = positional;

    if (!command || command === "--help" || command === "-h") {
      return handleHelp(flags);
    }
    if (command === "version") {
      return handleVersion(flags);
    }
    if (command === "init") {
      return handleInit(flags, positional.slice(1));
    }

    return invalidUsage(`Unknown command: ${command}`, flags);
  } catch (error) {
    activeOutput.terminalClass = "internal-error";
    writeStderr("Unexpected internal error.\n");
    return exitCodeForResult({ status: "error", exit_class: "internal" });
  }
}

export async function main(rawArgs = process.argv.slice(2), invocation = {}) {
  activeOutput = { ...invocation, stdout: "", stderr: "", deferredRender: null, terminalClass: null };
  const exitCode = await dispatchMain(rawArgs, invocation);
  return {
    exitCode,
    terminalClass: activeOutput.terminalClass,
    render: (context) => activeOutput.deferredRender
      ? activeOutput.deferredRender(context)
      : { stdout: activeOutput.stdout, stderr: activeOutput.stderr },
  };
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const rawArgs = process.argv.slice(2);
  if (rawArgs[0] === "record-store" || isRecordingCommand(rawArgs) || isRetiredCommand(rawArgs)) {
    // Retired commands reject before any diagnostic file effects. The recorder
    // owns its complete grammar and result envelope. Historical
    // logging flags and environment must not consume or replace either.
    const execution = await main(rawArgs);
    const rendered = execution.render({ invocationId: createInvocationId(), observability: "disabled", exitCode: execution.exitCode });
    if (rendered.stdout) process.stdout.write(rendered.stdout);
    if (rendered.stderr) process.stderr.write(rendered.stderr);
    process.exitCode = execution.exitCode;
  } else {
    process.exitCode = await runObservedCli(rawArgs, (args, invocation) =>
      // Logging preprocessing cannot turn a historical invocation into a
      // recorder invocation by removing leading flags.
      main(args[0] === "record-store" ? ["record-store", ...rawArgs] : isRecordingCommand(args) ? [args[0], ...rawArgs] : args, invocation),
    { cliVersion: packageInfo().version });
  }
}
