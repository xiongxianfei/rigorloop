#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { inflateRawSync } from "node:zlib";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { EXIT, exitCodeForResult } from "../lib/command-result.js";
import { adapterDescriptor, supportedAdapterNames } from "../lib/adapters.js";
import { parseLockfile, serializeLockfile, sha256NormalizedText } from "../lib/lockfile.js";
import { buildNewChangeDraft, parseNewChangeArgs } from "../lib/new-change.js";
import { runNewChangePlan } from "../lib/new-change-filesystem.js";
import { validateOfficialArchiveUrl } from "../lib/official-archive-url.js";

const LOCKFILE_PATH = "rigorloop.lock";

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
  rigorloop init --adapter codex|claude|opencode [--dry-run] [--json]
  rigorloop new-change <change-id> --title <title> [--dry-run] [--json]

Commands:
  version                 Print package name and version.
  init --adapter codex|claude|opencode
                          Initialize a verified adapter install plan.
  new-change              Plan a change metadata scaffold.
`;
}

function releaseForPackage(version) {
  return `v${version}`;
}

function sourceForFlags(flags, info, descriptor) {
  if (flags.fromArchiveProvided) {
    return {
      type: "local-archive",
      archive: basename(flags.fromArchive),
      inputPath: flags.fromArchive,
    };
  }

  return {
    type: "release-archive",
    release: releaseForPackage(info.version),
    archive: descriptor.archiveName(releaseForPackage(info.version)),
  };
}

function manifestAdapterBlock(source, descriptor, artifact) {
  const sourceLines =
    source.type === "local-archive"
      ? [`      type: local-archive`, `      archive: "${source.archive}"`]
      : [`      type: release-archive`, `      release: "${source.release}"`];
  const installRoots = rootsForArtifact(descriptor, artifact);
  const rootLines =
    descriptor.name !== "opencode" && Object.keys(installRoots).length === 1
      ? [`    install_root: "${Object.values(installRoots)[0]}"`]
      : [
          `    install_roots:`,
          ...Object.entries(installRoots).map(([role, root]) => `      ${role}: "${root}"`),
        ];

  return `  - name: ${descriptor.name}
${rootLines.join("\n")}
    source:
${sourceLines.join("\n")}`;
}

function parseManifestAdapterBlocks(content) {
  if (!content.includes("schema_version: 1") || !content.includes("adapters:")) {
    return { error: { code: "invalid-config", message: "Existing rigorloop.yaml is not compatible with the init contract." } };
  }
  const lines = content.replace(/\r\n?/g, "\n").split("\n");
  const adapterStart = lines.findIndex((line) => line === "adapters:");
  const blocks = [];
  let current = [];
  for (const line of lines.slice(adapterStart + 1)) {
    if (line.startsWith("  - name: ")) {
      if (current.length) {
        blocks.push(current);
      }
      current = [line];
    } else if (current.length) {
      current.push(line);
    } else if (line.trim() !== "") {
      return { error: { code: "invalid-config", message: "Existing rigorloop.yaml has malformed adapter entries." } };
    }
  }
  if (current.length) {
    blocks.push(current);
  }
  const adapters = [];
  for (const block of blocks) {
    const name = block[0].slice("  - name: ".length).trim();
    const descriptor = adapterDescriptor(name);
    if (!descriptor) {
      return { error: { code: "invalid-config", message: `Existing rigorloop.yaml includes unsupported adapter ${name}.` } };
    }
    adapters.push({ name, block: block.join("\n").replace(/\n+$/, "") });
  }
  return { adapters };
}

function manifestContent(info, source, descriptor, existingContent) {
  const selectedBlock = manifestAdapterBlock(source, descriptor, source.artifact);
  if (existingContent) {
    const parsed = parseManifestAdapterBlocks(existingContent);
    if (!parsed.error) {
      const preserved = parsed.adapters.filter((entry) => entry.name !== descriptor.name).map((entry) => entry.block);
      return `schema_version: 1
rigorloop:
  package: "${info.name}"
  package_version: "${info.version}"
adapters:
${[...preserved, selectedBlock].join("\n")}
`;
    }
  }
  return `schema_version: 1
rigorloop:
  package: "${info.name}"
  package_version: "${info.version}"
adapters:
${selectedBlock}
`;
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

function rootHashesForArtifact(descriptor, artifact) {
  if (artifact?.root_hashes) {
    return artifact.root_hashes;
  }
  return Object.fromEntries(
    Object.keys(rootsForArtifact(descriptor, artifact)).map((role) => [
      role,
      {
        tree_sha256: artifact?.tree_sha256 ?? "<planned-after-install>",
        file_count: artifact?.file_count ?? "<planned-after-install>",
      },
    ]),
  );
}

function usesMultiRootLockfile(descriptor, artifact) {
  return descriptor.name === "opencode" || Object.keys(rootsForArtifact(descriptor, artifact)).length > 1;
}

function lockfileEntryForAdapter(info, source, artifact, descriptor, rootHashes = rootHashesForArtifact(descriptor, artifact)) {
  const entry = {
    adapter: descriptor.name,
    release: releaseForPackage(info.version),
    source: source.type,
    archive: source.archive,
    archive_sha256: artifact?.sha256 ?? "<planned>",
    tree_hash_algorithm: "rigorloop-tree-hash-v1",
  };
  if (usesMultiRootLockfile(descriptor, artifact)) {
    return {
      ...entry,
      installed_roots: rootsForArtifact(descriptor, artifact),
      root_hashes: rootHashes,
    };
  }
  const [role] = Object.keys(rootsForArtifact(descriptor, artifact));
  return {
    ...entry,
    installed_root: rootsForArtifact(descriptor, artifact)[role],
    tree_sha256: rootHashes[role].tree_sha256,
    file_count: rootHashes[role].file_count,
  };
}

function plannedLockfile(info, source, manifest, descriptor) {
  const artifact = source.artifact;
  return {
    schema_version: 2,
    rigorloop: {
      package: info.name,
      version: info.version,
    },
    manifest: {
      path: "rigorloop.yaml",
      sha256: sha256NormalizedText(manifest),
    },
    generated: {
      adapters: [lockfileEntryForAdapter(info, source, artifact, descriptor)],
    },
  };
}

function existingLockfileEntries(selectedAdapter) {
  const lockfileAbsolutePath = resolve(process.cwd(), LOCKFILE_PATH);
  if (!existsSync(lockfileAbsolutePath)) {
    return [];
  }
  const parsed = parseLockfile(readFileSync(lockfileAbsolutePath, "utf8"));
  if (!parsed.ok) {
    return [];
  }
  return parsed.lockfile.generated.adapters.filter((entry) => entry.adapter !== selectedAdapter);
}

function lockfileForVerifiedInstall(info, source, manifest, artifact, rootHashes, descriptor) {
  const adapters = [
    ...existingLockfileEntries(descriptor.name),
    lockfileEntryForAdapter(info, source, artifact, descriptor, rootHashes),
  ];
  return {
    schema_version: 2,
    rigorloop: {
      package: info.name,
      version: info.version,
    },
    manifest: {
      path: "rigorloop.yaml",
      sha256: sha256NormalizedText(manifest),
    },
    generated: {
      adapters,
    },
  };
}

function compatibleManifest(content, descriptor, artifact) {
  if (descriptor.name === "opencode" && !rootsForArtifact(descriptor, artifact).commands && content.includes(".opencode/commands")) {
    return false;
  }
  return (
    content.includes("schema_version: 1") &&
    content.includes(`name: ${descriptor.name}`) &&
    content.includes(`"${Object.values(rootsForArtifact(descriptor, artifact))[0]}"`)
  );
}

function pathState(path) {
  if (!existsSync(path)) {
    return "absent";
  }
  return statSync(path).isDirectory() ? "directory" : "file";
}

function directoryKind(path, descriptor, artifact) {
  if (Object.values(rootsForArtifact(descriptor, artifact)).includes(path)) {
    return `${descriptor.name}-install-root`;
  }
  return `${descriptor.name}-adapter-root`;
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

function releaseListedForSkillsOnlyCompatibility(marker, release) {
  if (!marker) {
    return false;
  }
  const releases = Array.isArray(marker) ? marker : marker.releases;
  return Array.isArray(releases) && releases.includes(release);
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
  if (artifact.command_aliases?.opencode) {
    if (descriptor.name !== "opencode" || !artifact.install_roots?.commands) {
      return { error: { code: "metadata-invalid", message: "opencode command alias metadata requires the opencode commands root." } };
    }
    const aliasPaths = opencodeCommandAliasPaths(artifact);
    if (
      !Number.isInteger(artifact.command_aliases.opencode.count) ||
      !Array.isArray(aliasPaths) ||
      artifact.command_aliases.opencode.count !== aliasPaths.length ||
      aliasPaths.some((aliasPath) => !isNonEmptyString(aliasPath) || !aliasPath.startsWith(`${descriptor.installRoots.commands}/`))
    ) {
      return { error: { code: "metadata-invalid", message: "opencode command alias metadata is incomplete." } };
    }
  }
  // CR-M3-R2-F1: opencode commands root is valid only with declared command aliases.
  if (descriptor.name === "opencode" && artifact.install_roots?.commands && !artifact.command_aliases?.opencode) {
    return {
      blocker: metadataBlocker(
        "opencode-command-aliases-missing",
        "Opencode commands root metadata requires command_aliases.opencode.",
        artifact.archive,
        "Use opencode metadata that declares command aliases, or use explicitly compatible skills-only metadata without the commands root.",
      ),
    };
  }
  // CR-M3-R1-F1: skills-only opencode compatibility must be explicit in trusted metadata.
  if (descriptor.name === "opencode" && !artifact.command_aliases?.opencode && !rootsForArtifact(descriptor, artifact).commands) {
    const marker = artifact.skills_only_compatibility ?? metadata.compatibility?.opencode_skills_only;
    if (!releaseListedForSkillsOnlyCompatibility(marker, release)) {
      return {
        blocker: metadataBlocker(
          "opencode-skills-only-compatibility-unmarked",
          "Opencode skills-only archive metadata is not explicitly marked compatible.",
          artifact.archive,
          "Use an opencode archive with command alias metadata or bundled trusted skills-only compatibility metadata.",
        ),
      };
    }
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
  return name === "AGENTS.md";
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

function opencodeCommandAliasPaths(artifact) {
  const aliases = artifact?.command_aliases?.opencode;
  if (!aliases) {
    return undefined;
  }
  if (Array.isArray(aliases.paths)) {
    return aliases.paths;
  }
  if (aliases.aliases && typeof aliases.aliases === "object") {
    return Object.values(aliases.aliases);
  }
  return [];
}

function treeHashForEntries(entries, descriptor) {
  return treeHashForRows(fileRowsForTreeRoot(entries, descriptor.primaryInstallRoot()));
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

function rowsEqual(left, right) {
  if (left.length !== right.length) {
    return false;
  }
  return left.every(([path, hash], index) => path === right[index][0] && hash === right[index][1]);
}

function fileRowsForFilesystem(root) {
  const rows = [];
  function visit(relativeDirectory) {
    const absoluteDirectory = resolve(process.cwd(), root, relativeDirectory);
    for (const name of readdirSync(absoluteDirectory).sort()) {
      const relativePath = relativeDirectory ? `${relativeDirectory}/${name}` : name;
      const absolutePath = resolve(process.cwd(), root, relativePath);
      const stat = statSync(absolutePath);
      if (stat.isDirectory()) {
        visit(relativePath);
      } else if (stat.isFile()) {
        const bytes = relativePath.endsWith(".md") ? normalizeText(readFileSync(absolutePath)) : readFileSync(absolutePath);
        rows.push([relativePath, sha256(bytes)]);
      }
    }
  }
  visit("");
  return rows.sort(([left], [right]) => left.localeCompare(right));
}

function treeHashForFilesystem(root) {
  const rows = fileRowsForFilesystem(root);
  return {
    rows,
    treeHash: treeHashForRows(rows),
    fileCount: rows.length,
  };
}

function currentLockfileEntries() {
  const lockfileAbsolutePath = resolve(process.cwd(), LOCKFILE_PATH);
  if (!existsSync(lockfileAbsolutePath)) {
    return [];
  }
  const parsed = parseLockfile(readFileSync(lockfileAbsolutePath, "utf8"));
  if (!parsed.ok) {
    return [];
  }
  return parsed.lockfile.generated.adapters;
}

function currentLockfileEntry(descriptor) {
  return currentLockfileEntries().find((entry) => entry.adapter === descriptor.name);
}

function installedTreeMismatchError(actualTree, expectedTreeHash, expectedFileCount) {
  return {
    code: "installed-tree-mismatch",
    message: "Installed adapter tree does not match trusted metadata.",
    expected_tree_sha256: expectedTreeHash,
    actual_tree_sha256: actualTree.treeHash,
    expected_file_count: expectedFileCount,
    actual_file_count: actualTree.fileCount,
  };
}

function verifyInstalledTree(entries, artifact, descriptor, { allowMissingOrEmpty = false } = {}) {
  const expectedRootHashes = rootHashesForEntries(entries, descriptor, artifact);
  for (const [role, root] of Object.entries(rootsForArtifact(descriptor, artifact))) {
    const expectedRows = fileRowsForTreeRoot(entries, root);
    const expectedTreeHash = artifact.root_hashes?.[role]?.tree_sha256 ?? artifact.tree_sha256;
    const expectedFileCount = artifact.root_hashes?.[role]?.file_count ?? expectedRows.length;

    if (!existsSync(resolve(process.cwd(), root))) {
      if (allowMissingOrEmpty) {
        continue;
      }
      return { error: installedTreeMismatchError({ treeHash: "<missing>", fileCount: 0 }, expectedTreeHash, expectedFileCount) };
    }

    const actualTree = treeHashForFilesystem(root);
    if (allowMissingOrEmpty && actualTree.fileCount === 0) {
      continue;
    }
    if (!rowsEqual(actualTree.rows, expectedRows) || actualTree.treeHash !== expectedTreeHash || actualTree.fileCount !== expectedFileCount) {
      return { error: installedTreeMismatchError(actualTree, expectedTreeHash, expectedFileCount) };
    }
  }
  return { ok: true, rootHashes: expectedRootHashes, expectedFileCount: expectedRootHashes.skills?.file_count ?? 0, treeHash: expectedRootHashes.skills?.tree_sha256 };
}

function generatedOutputConflictBlocker(entries) {
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
    if (pathState(resolve(process.cwd(), directory)) === "file") {
      return {
        code: "overwrite-refused",
        message: `${directory} exists and is not a directory.`,
        path: directory,
        next_action: "Move the existing file before running init.",
      };
    }
  }

  for (const entry of entries) {
    if (pathState(resolve(process.cwd(), entry.name)) === "directory") {
      return {
        code: "overwrite-refused",
        message: `${entry.name} exists and is not a file.`,
        path: entry.name,
        next_action: "Move the existing directory before running init.",
      };
    }
  }

  return undefined;
}

function lockfileDriftBlocker(lockfileEntry) {
  if (!lockfileEntry) {
    return undefined;
  }
  if (lockfileEntry.installed_roots) {
    for (const [role, root] of Object.entries(lockfileEntry.installed_roots)) {
      const rootHash = lockfileEntry.root_hashes[role];
      const blocker = lockfileDriftBlocker({
        adapter: lockfileEntry.adapter,
        installed_root: root,
        tree_sha256: rootHash.tree_sha256,
        file_count: rootHash.file_count,
      });
      if (blocker) {
        return blocker;
      }
    }
    return undefined;
  }

  const rootState = pathState(resolve(process.cwd(), lockfileEntry.installed_root));
  if (rootState === "absent") {
    return {
      code: "generated-output-missing",
      message: "Codex generated output recorded in rigorloop.lock is missing.",
      adapter: lockfileEntry.adapter,
      installed_root: lockfileEntry.installed_root,
      expected_tree_sha256: lockfileEntry.tree_sha256,
      actual_tree_sha256: null,
      next_action: "Restore the recorded generated output or resolve drift before running init.",
    };
  }
  if (rootState !== "directory") {
    return {
      code: "overwrite-refused",
      message: `${lockfileEntry.installed_root} exists and is not a directory.`,
      path: lockfileEntry.installed_root,
      next_action: "Move the existing file before running init.",
    };
  }

  const actualTree = treeHashForFilesystem(lockfileEntry.installed_root);
  if (actualTree.treeHash !== lockfileEntry.tree_sha256 || actualTree.fileCount !== lockfileEntry.file_count) {
    return {
      code: "generated-output-drift",
      message: "Codex generated output differs from rigorloop.lock.",
      adapter: lockfileEntry.adapter,
      installed_root: lockfileEntry.installed_root,
      expected_tree_sha256: lockfileEntry.tree_sha256,
      actual_tree_sha256: actualTree.treeHash,
      expected_file_count: lockfileEntry.file_count,
      actual_file_count: actualTree.fileCount,
      next_action: "Resolve generated output drift before running init.",
    };
  }

  return undefined;
}

function firstLockfileDriftBlocker() {
  for (const entry of currentLockfileEntries()) {
    const blocker = lockfileDriftBlocker(entry);
    if (blocker) {
      return blocker;
    }
  }
  return undefined;
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
  if (descriptor.name === "opencode") {
    for (const aliasPath of opencodeCommandAliasPaths(artifact) ?? []) {
      if (!files.some((entry) => entry.name === aliasPath)) {
        return {
          error: {
            code: "opencode-command-alias-missing",
            message: "Declared opencode command alias is missing from archive.",
            path: aliasPath,
          },
        };
      }
    }
  }
  return { entries: files, archiveHash, rootHashes, treeHash: rootHashes.skills?.tree_sha256, fileCount: rootHashes.skills?.file_count ?? files.length };
}

function addArchiveActions(plan, entries, descriptor) {
  const installRoot = descriptor.primaryInstallRoot();
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
    let existingMatches = false;
    if (state === "file") {
      const relativePath = entry.name.slice(`${installRoot}/`.length);
      const existingBytes = relativePath.endsWith(".md")
        ? normalizeText(readFileSync(resolve(process.cwd(), entry.name)))
        : readFileSync(resolve(process.cwd(), entry.name));
      const entryBytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
      existingMatches = Buffer.compare(existingBytes, entryBytes) === 0;
    }
    plan.actions.push({
      type: "copy",
      path: entry.name,
      status: state === "absent" ? "pending" : existingMatches ? "skipped" : "blocked",
      reason:
        state === "absent"
          ? `Install verified ${descriptor.displayName} adapter file.`
          : existingMatches
            ? `${entry.name} already matches verified ${descriptor.displayName} adapter content.`
            : `${entry.name} already exists.`,
    });
    plan.artifacts.push({
      path: entry.name,
      kind: "adapter-file",
      status: state === "absent" ? "pending" : existingMatches ? "existing" : "blocked",
    });
    if (state !== "absent" && !existingMatches) {
      plan.blockers.push({
        code: "overwrite-refused",
        message: `${entry.name} already exists.`,
        path: entry.name,
        next_action: "Move the existing file before running init.",
      });
    }
  }
}

function writeArchiveEntries(entries, descriptor) {
  const installRoot = descriptor.primaryInstallRoot();
  for (const entry of entries) {
    const outputPath = resolve(process.cwd(), entry.name);
    mkdirSync(dirname(outputPath), { recursive: true });
    const relativePath = entry.name.slice(`${installRoot}/`.length);
    const bytes = relativePath.endsWith(".md") ? normalizeText(entry.bytes) : entry.bytes;
    writeFileSync(outputPath, bytes);
  }
}

function initWarnings(descriptor, artifact) {
  if (
    descriptor.name === "opencode" &&
    artifact &&
    !artifact.command_aliases?.opencode &&
    !rootsForArtifact(descriptor, artifact).commands
  ) {
    return [
      {
        code: "opencode-command-aliases-not-declared",
        message: "Selected opencode archive metadata does not declare command aliases; only skills were installed.",
      },
    ];
  }
  return [];
}

function directoryPlanForRoots(roots) {
  return [...new Set(Object.values(roots).flatMap((root) => [root.split("/").slice(0, -1).join("/"), root]).filter(Boolean))];
}

function planDirectoryActions(flags, descriptor, artifact) {
  const actions = [];
  const artifacts = [];
  const blockers = [];
  let parentBlocked = false;

  const directoryPlan = directoryPlanForRoots(rootsForArtifact(descriptor, artifact));
  const rootParent = directoryPlan[0];
  for (const relativePath of directoryPlan) {
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
        kind: directoryKind(relativePath, descriptor, artifact),
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
        kind: directoryKind(relativePath, descriptor, artifact),
        status: "existing",
      });
    } else {
      actions.push({
        type: "create-dir",
        path: relativePath,
        status: "blocked",
        reason:
          state === "blocked-by-parent"
            ? `${relativePath} cannot be created because ${rootParent} is not a directory.`
            : `${relativePath} exists and is not a directory.`,
      });
      artifacts.push({
        path: relativePath,
        kind: directoryKind(relativePath, descriptor, artifact),
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
      if (relativePath === rootParent) {
        parentBlocked = true;
      }
    }
  }

  return { actions, artifacts, blockers };
}

function addLockfilePlan(flags, actions, artifacts, blockers, errors) {
  const lockfileAbsolutePath = resolve(process.cwd(), LOCKFILE_PATH);
  if (!existsSync(lockfileAbsolutePath)) {
    actions.push({
      type: "write",
      path: LOCKFILE_PATH,
      status: flags.dryRun ? "planned" : "pending",
      reason: flags.dryRun
        ? "Plan durable lockfile content."
        : "Write durable lockfile after verified Codex adapter install.",
    });
    artifacts.push({
      path: LOCKFILE_PATH,
      kind: "project-lockfile",
      status: flags.dryRun ? "planned" : "pending",
    });
    return;
  }

  const parsed = parseLockfile(readFileSync(lockfileAbsolutePath, "utf8"));
  if (parsed.ok) {
    actions.push({
      type: "write",
      path: LOCKFILE_PATH,
      status: flags.dryRun ? "planned" : "pending",
      reason: flags.dryRun
        ? "Plan update to supported rigorloop.lock."
        : "Update supported rigorloop.lock after verified Codex adapter install.",
    });
    artifacts.push({
      path: LOCKFILE_PATH,
      kind: "project-lockfile",
      status: flags.dryRun ? "planned" : "pending",
    });
    return;
  }

  actions.push({
    type: "write",
    path: LOCKFILE_PATH,
    status: "blocked",
    reason: parsed.message,
  });
  artifacts.push({
    path: LOCKFILE_PATH,
    kind: "project-lockfile",
    status: "blocked",
  });

  if (parsed.kind === "unsupported") {
    blockers.push({
      code: parsed.code,
      message: parsed.message,
      path: LOCKFILE_PATH,
      next_action: "Use a compatible CLI version or resolve the unsupported lockfile shape.",
    });
  } else {
    errors.push({
      code: parsed.code,
      message: parsed.message,
      path: LOCKFILE_PATH,
      next_action: "Repair or move rigorloop.lock before running init.",
    });
  }
}

function buildInitPlan(flags, descriptor, artifact) {
  const info = packageInfo();
  const source = sourceForFlags(flags, info, descriptor);
  if (artifact) {
    source.artifact = artifact;
  }
  const manifestPath = "rigorloop.yaml";
  const manifestAbsolutePath = resolve(process.cwd(), manifestPath);
  const existingManifest = existsSync(manifestAbsolutePath) ? readFileSync(manifestAbsolutePath, "utf8") : undefined;
  const manifest = manifestContent(info, source, descriptor, existingManifest);
  const actions = [];
  const artifacts = [];
  const blockers = [];
  const errors = [];

  if (flags.fromArchiveProvided && (!flags.fromArchive || flags.fromArchive.startsWith("--"))) {
    errors.push({
      code: "invalid-archive-path",
      message: "Missing required value for --from-archive.",
      path: "--from-archive",
      next_action: `Provide an existing ${descriptor.displayName} adapter archive path or omit --from-archive.`,
    });
  } else if (flags.fromArchiveProvided && !existsSync(resolve(process.cwd(), flags.fromArchive))) {
    errors.push({
      code: "invalid-archive-path",
      message: `Local archive path does not exist: ${flags.fromArchive}`,
      path: flags.fromArchive,
      next_action: `Provide an existing ${descriptor.displayName} adapter archive path or omit --from-archive.`,
    });
  }

  const directoryPlan = planDirectoryActions(flags, descriptor, artifact);
  actions.push(...directoryPlan.actions);
  artifacts.push(...directoryPlan.artifacts);
  blockers.push(...directoryPlan.blockers);

  if (existingManifest !== undefined) {
    const parsedManifest = parseManifestAdapterBlocks(existingManifest);
    if (parsedManifest.error) {
      errors.push({
        code: parsedManifest.error.code,
        message: parsedManifest.error.message,
        path: manifestPath,
        next_action: "Review or move the existing file before running init.",
      });
    } else if (parsedManifest.adapters.filter((entry) => entry.name === descriptor.name).length > 1) {
      blockers.push({
        code: "duplicate-adapter-entry",
        message: `Existing rigorloop.yaml contains duplicate ${descriptor.displayName} adapter entries.`,
        path: manifestPath,
        next_action: "Remove duplicate adapter entries before running init.",
      });
    } else if (compatibleManifest(existingManifest, descriptor, artifact)) {
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
      actions.push({
        type: "write",
        path: manifestPath,
        status: flags.dryRun ? "planned" : "pending",
        reason: `Update rigorloop.yaml for ${descriptor.displayName} adapter.`,
      });
      artifacts.push({
        path: manifestPath,
        kind: "project-manifest",
        status: flags.dryRun ? "planned" : "pending",
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

  addLockfilePlan(flags, actions, artifacts, blockers, errors);

  return {
    info,
    source,
    manifest,
    actions,
    artifacts,
    blockers,
    errors,
    planned_lockfile: plannedLockfile(info, source, manifest, descriptor),
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

function newChangeUsageError(error, flags) {
  return commandError("new-change", error.message, flags, {
    code: error.code,
    message: error.message,
    next_action: "Run rigorloop new-change <change-id> --title <title>.",
  });
}

function handleNewChange(rawArgs) {
  const parsed = parseNewChangeArgs(rawArgs, process.env);
  if (parsed.error) {
    return newChangeUsageError(parsed.error, parsed.flags);
  }

  const draft = buildNewChangeDraft(parsed.value);
  const execution = runNewChangePlan({
    cwd: process.cwd(),
    draft,
    flags: parsed.flags,
    profile: parsed.value.profile,
  });
  const result = envelope("new-change", parsed.flags, {
    ...execution.result,
  });

  if (parsed.flags.json) {
    writeJson(result);
  } else if (result.status === "blocked") {
    process.stderr.write(`${result.summary}\n${result.blockers[0].message}\n`);
  } else if (result.status === "error") {
    process.stderr.write(`${result.summary}\n${result.errors[0].message}\n`);
  } else if (parsed.flags.dryRun) {
    writeHuman(`RigorLoop new-change dry run completed.\n${draft.planned_change_metadata.path}\n`, parsed.flags);
  } else {
    writeHuman(`RigorLoop change metadata scaffold created.\n${draft.change.root}\n${draft.change.metadata_path}\n`, parsed.flags);
  }

  return exitCodeForResult({
    status: result.status,
    exit_class: execution.exit_class,
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
    summary: `Adapter '${adapter}' is not supported.`,
    blockers: [
      {
        code: "adapter-unknown",
        message: `Adapter '${adapter}' is not supported.`,
        next_action: `Use one of: ${supportedAdapterNames().join(", ")}.`,
      },
    ],
  });

  if (flags.json) {
    writeJson(result);
  } else {
    process.stderr.write(`${result.summary}\nUse one of: ${supportedAdapterNames().join(", ")}.\n`);
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
  if (blockers[0]?.diagnostics) {
    result.diagnostics = { ...result.diagnostics, ...blockers[0].diagnostics };
  }
  if (flags.json) {
    writeJson(result);
  } else {
    process.stderr.write(`${result.summary}\n${blockers[0]?.next_action ?? "Resolve the blocker before running init."}\n`);
  }
  return exitCodeForResult({ ...result, exit_class: exitClass });
}

function exitClassForBlockers(blockers) {
  return blockers.some((blocker) => blocker.code === "overwrite-refused") ? "mutation_conflict" : "blocked";
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

async function archiveWorkForInit(flags, info, descriptor) {
  if (flags.dryRun && !flags.fromArchiveProvided) {
    return {};
  }

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
    if (
      flags.dryRun &&
      !["opencode-command-aliases-missing", "opencode-skills-only-compatibility-unmarked"].includes(validation.blocker?.code)
    ) {
      return {};
    }
    return validation;
  }
  const artifact = validation.artifact;

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
    // CR-M2-R2-F1: dry-run planning must use trusted metadata roots without reading or extracting archive bytes.
    if (flags.dryRun) {
      return { artifact };
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

async function handleInit(flags) {
  if (!flags.adapter) {
    return invalidUsage("Missing required option: --adapter codex|claude|opencode.", flags, "init");
  }
  const descriptor = adapterDescriptor(flags.adapter);
  if (!descriptor) {
    return unsupportedAdapter(flags.adapter, flags);
  }
  if (flags.fromArchiveProvided && (!flags.fromArchive || flags.fromArchive.startsWith("--"))) {
    return invalidArchivePath("Missing required value for --from-archive.", flags);
  }
  if (flags.fromArchiveProvided && !existsSync(resolve(process.cwd(), flags.fromArchive))) {
    return invalidArchivePath(`Local archive path does not exist: ${flags.fromArchive}`, flags);
  }

  const info = packageInfo();
  let plan = buildInitPlan(flags, descriptor);
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
  const deferrableRootBlockers =
    descriptor.name === "opencode" &&
    plan.blockers.length > 0 &&
    plan.blockers.every((blocker) => String(blocker.path ?? "").startsWith(".opencode/commands"));
  if (plan.blockers.length > 0 && !deferrableRootBlockers) {
    return writeBlockedResult(flags, plan, plan.blockers[0].message, plan.blockers, exitClassForBlockers(plan.blockers));
  }

  const archiveWork = await archiveWorkForInit(flags, info, descriptor);
  if (archiveWork.artifact && !archiveWork.blocker && !archiveWork.error) {
    plan = buildInitPlan(flags, descriptor, archiveWork.artifact);
    if (plan.errors.length > 0) {
      return writeValidationErrorResult(flags, plan, plan.errors[0]);
    }
    if (plan.blockers.length > 0) {
      return writeBlockedResult(flags, plan, plan.blockers[0].message, plan.blockers, exitClassForBlockers(plan.blockers));
    }
  }
  if (archiveWork.entries) {
    const conflict = generatedOutputConflictBlocker(archiveWork.entries);
    if (conflict) {
      return writeBlockedResult(flags, plan, conflict.message, [conflict], "mutation_conflict");
    }
    const drift = firstLockfileDriftBlocker();
    if (drift) {
      return writeBlockedResult(
        flags,
        plan,
        drift.message,
        [drift],
        drift.code === "overwrite-refused" ? "mutation_conflict" : "blocked",
      );
    }
    const installedTree = verifyInstalledTree(archiveWork.entries, archiveWork.artifact, descriptor, { allowMissingOrEmpty: true });
    if (installedTree.error) {
      return writeValidationErrorResult(flags, plan, installedTree.error);
    }
    addArchiveActions(plan, archiveWork.entries, descriptor);
  }

  if (archiveWork.blocker) {
    return writeBlockedResult(flags, plan, archiveWork.blocker.message, [archiveWork.blocker]);
  }
  if (archiveWork.error) {
    return writeValidationErrorResult(flags, plan, archiveWork.error);
  }
  if (plan.blockers.length > 0) {
    return writeBlockedResult(flags, plan, plan.blockers[0].message, plan.blockers, exitClassForBlockers(plan.blockers));
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
        const pendingCopyPaths = new Set(
          plan.actions.filter((action) => action.type === "copy" && action.status === "pending").map((action) => action.path),
        );
        writeArchiveEntries(archiveWork.entries.filter((entry) => pendingCopyPaths.has(entry.name)), descriptor);
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
    if (archiveWork.entries) {
      const lockfileAction = plan.actions.find((action) => action.path === LOCKFILE_PATH);
      const lockfileArtifact = plan.artifacts.find((artifact) => artifact.path === LOCKFILE_PATH);
      if (lockfileAction?.status === "pending") {
        const lockfilePreviouslyExists = existsSync(resolve(process.cwd(), LOCKFILE_PATH));
        const verifiedInstalledTree = verifyInstalledTree(archiveWork.entries, archiveWork.artifact, descriptor);
        if (verifiedInstalledTree.error) {
          return writeValidationErrorResult(flags, plan, verifiedInstalledTree.error);
        }
        const lockfile = lockfileForVerifiedInstall(
          plan.info,
          plan.source,
          plan.manifest,
          archiveWork.artifact,
          verifiedInstalledTree.rootHashes,
          descriptor,
        );
        writeFileSync(resolve(process.cwd(), LOCKFILE_PATH), serializeLockfile(lockfile), "utf8");
        plan.planned_lockfile = lockfile;
        lockfileAction.status = "done";
        lockfileAction.reason = lockfilePreviouslyExists
          ? `Updated durable lockfile for verified ${descriptor.displayName} adapter install.`
          : `Wrote durable lockfile for verified ${descriptor.displayName} adapter install.`;
        if (lockfileArtifact) {
          lockfileArtifact.status = lockfilePreviouslyExists ? "updated" : "created";
        }
      }
    }
  }

  const warnings = initWarnings(descriptor, archiveWork.artifact);
  const result = envelope("init", flags, {
    status: warnings.length > 0 ? "warning" : "success",
    summary: flags.dryRun
      ? "RigorLoop init dry run completed. No files were written."
      : archiveWork.entries
        ? `RigorLoop initialized with verified ${descriptor.displayName} adapter files.`
        : `RigorLoop initialized with ${descriptor.displayName} scaffold.`,
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
          archiveWork.entries
            ? `RigorLoop initialized with verified ${descriptor.displayName} adapter files.`
            : `RigorLoop initialized with ${descriptor.displayName} scaffold.`,
          archiveWork.entries ? "rigorloop.lock was written." : "No adapter files were installed.",
        ];
    for (const warning of warnings) {
      lines.push(`warning ${warning.code}: ${warning.message}`);
    }
    writeHuman(`${lines.join("\n")}\n`, flags);
  }
  return exitCodeForResult({ ...result, exit_class: "success" });
}

async function main() {
  try {
    const rawArgs = process.argv.slice(2);
    if (rawArgs[0] === "new-change") {
      return handleNewChange(rawArgs.slice(1));
    }

    const { flags, positional } = parseFlags(rawArgs);
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
    if (command === "new-change") {
      return handleNewChange(rawArgs.slice(rawArgs.indexOf("new-change") + 1));
    }

    return invalidUsage(`Unknown command: ${command}`, flags);
  } catch (error) {
    process.stderr.write(`Unexpected error: ${error.message}\n`);
    return exitCodeForResult({ status: "error", exit_class: "internal" });
  }
}

process.exitCode = await main();
