import { createHash } from "node:crypto";

const SHA256_PATTERN = /^[0-9a-f]{64}$/i;
const SUPPORTED_SOURCES = new Set(["release-archive", "local-archive"]);
const SUPPORTED_ADAPTERS = new Set(["codex", "claude", "opencode"]);
const TOP_LEVEL_FIELDS = ["schema_version", "rigorloop", "manifest", "generated"];
const RIGORLOOP_FIELDS = ["package", "version"];
const MANIFEST_FIELDS = ["path", "sha256"];
const GENERATED_FIELDS = ["adapters"];
const ADAPTER_FIELDS = [
  "adapter",
  "release",
  "source",
  "archive",
  "archive_sha256",
  "installed_root",
  "installed_roots",
  "tree_hash_algorithm",
  "tree_sha256",
  "file_count",
  "root_hashes",
];
const SINGLE_ROOTS = {
  codex: ".agents/skills",
  claude: ".claude/skills",
};
const OPENCODE_ROOTS = {
  skills: ".opencode/skills",
  commands: ".opencode/commands",
};

function failure(kind, code, message, path = "rigorloop.lock") {
  return { ok: false, kind, code, message, path };
}

function unquote(value) {
  const trimmed = value.trim();
  if (trimmed.startsWith('"') && trimmed.endsWith('"')) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function parseScalar(value) {
  return unquote(value);
}

function isSha256(value) {
  return typeof value === "string" && SHA256_PATTERN.test(value);
}

function isNonNegativeInteger(value) {
  const text = String(value);
  return /^\d+$/.test(text) && Number.isInteger(Number.parseInt(text, 10));
}

function parseTopLevel(lines) {
  const sections = new Map();
  for (const line of lines) {
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*):(?:\s+(.*))?$/);
    if (match) {
      sections.set(match[1], match[2] ?? "");
    }
  }
  return sections;
}

function parseSection(lines, sectionName, allowedFields) {
  const fields = {};
  const start = lines.findIndex((line) => line === `${sectionName}:`);
  if (start < 0) {
    return { missing: true };
  }
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^[A-Za-z_][A-Za-z0-9_]*:/.test(line)) {
      break;
    }
    if (line.trim() === "") {
      continue;
    }
    const nestedMatch = line.match(/^  ([A-Za-z_][A-Za-z0-9_-]*):\s*$/);
    if (nestedMatch) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported nested field ${sectionName}.${nestedMatch[1]}`);
    }
    const match = line.match(/^  ([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$/);
    if (!match) {
      continue;
    }
    const [, key, value] = match;
    if (!allowedFields.includes(key)) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field ${sectionName}.${key}`);
    }
    if (value === undefined || value === "") {
      return failure("invalid", "invalid-lockfile", `Missing scalar value for ${sectionName}.${key}`);
    }
    fields[key] = parseScalar(value);
  }
  return { fields };
}

function parseGeneratedSection(lines) {
  const start = lines.findIndex((line) => line === "generated:");
  if (start < 0) {
    return { missing: true };
  }
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^[A-Za-z_][A-Za-z0-9_-]*:/.test(line)) {
      break;
    }
    if (line.trim() === "" || line.startsWith("    ")) {
      continue;
    }
    const match = line.match(/^  ([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$/);
    if (!match) {
      continue;
    }
    const key = match[1];
    if (!GENERATED_FIELDS.includes(key)) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.${key}`);
    }
  }
  return {};
}

function parseAdapters(lines) {
  const adaptersStart = lines.findIndex((line, index) => line === "  adapters:" && lines[index - 1] === "generated:");
  if (adaptersStart < 0) {
    return { missing: true };
  }

  const adapters = [];
  let current;
  let nested;
  let rootHashRole;

  function pushCurrent() {
    if (current) {
      adapters.push(current);
    }
    current = undefined;
    nested = undefined;
    rootHashRole = undefined;
  }

  for (let index = adaptersStart + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^[A-Za-z_][A-Za-z0-9_-]*:/.test(line)) {
      break;
    }
    if (line.trim() === "") {
      continue;
    }
    const generatedFieldMatch = line.match(/^  ([A-Za-z_][A-Za-z0-9_-]*):/);
    if (generatedFieldMatch) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.${generatedFieldMatch[1]}`);
    }

    const startMatch = line.match(/^    - ([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$/);
    if (startMatch) {
      pushCurrent();
      current = {};
      const [, key, value] = startMatch;
      if (!ADAPTER_FIELDS.includes(key)) {
        return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.adapters[${adapters.length}].${key}`);
      }
      if (value === undefined || value === "") {
        return failure("invalid", "invalid-lockfile", `Missing scalar value for generated.adapters[${adapters.length}].${key}`);
      }
      current[key] = parseScalar(value);
      continue;
    }

    const fieldMatch = line.match(/^      ([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$/);
    if (fieldMatch && current) {
      const [, key, value] = fieldMatch;
      if (!ADAPTER_FIELDS.includes(key)) {
        return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.adapters[${adapters.length}].${key}`);
      }
      if (key === "installed_roots" || key === "root_hashes") {
        if (value !== undefined && value !== "") {
          return failure("invalid", "invalid-lockfile", `Expected mapping for generated.adapters[${adapters.length}].${key}`);
        }
        current[key] = {};
        nested = key;
        rootHashRole = undefined;
        continue;
      }
      if (value === undefined || value === "") {
        return failure("invalid", "invalid-lockfile", `Missing scalar value for generated.adapters[${adapters.length}].${key}`);
      }
      current[key] = parseScalar(value);
      nested = undefined;
      rootHashRole = undefined;
      continue;
    }

    const installedRootMatch = line.match(/^        ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (installedRootMatch && current && nested === "installed_roots") {
      current.installed_roots[installedRootMatch[1]] = parseScalar(installedRootMatch[2]);
      continue;
    }

    const rootHashRoleMatch = line.match(/^        ([A-Za-z_][A-Za-z0-9_-]*):\s*$/);
    if (rootHashRoleMatch && current && nested === "root_hashes") {
      rootHashRole = rootHashRoleMatch[1];
      current.root_hashes[rootHashRole] = {};
      continue;
    }

    const rootHashFieldMatch = line.match(/^          ([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (rootHashFieldMatch && current && nested === "root_hashes" && rootHashRole) {
      const [, key, value] = rootHashFieldMatch;
      if (!["tree_sha256", "file_count"].includes(key)) {
        return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.adapters[${adapters.length}].root_hashes.${rootHashRole}.${key}`);
      }
      current.root_hashes[rootHashRole][key] = key === "file_count" ? Number.parseInt(parseScalar(value), 10) : parseScalar(value);
      continue;
    }

    if (line.startsWith("      ") && current) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported lockfile adapter mapping near: ${line.trim()}`);
    }
  }
  pushCurrent();
  return { adapters };
}

function unexpectedFields(adapter, allowed) {
  return Object.keys(adapter).filter((field) => !allowed.includes(field));
}

function validateSingleRootAdapter(adapter, schemaVersion) {
  const allowed = [
    "adapter",
    "release",
    "source",
    "archive",
    "archive_sha256",
    "installed_root",
    "tree_hash_algorithm",
    "tree_sha256",
    "file_count",
  ];
  const unexpected = unexpectedFields(adapter, allowed);
  if (unexpected.length) {
    return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.adapters[].${unexpected[0]}`);
  }
  for (const field of allowed) {
    if (adapter[field] === undefined) {
      return failure("invalid", "invalid-lockfile", `Missing adapter field: ${field}`);
    }
  }
  if (adapter.adapter === "opencode") {
    return failure("unsupported", "unsupported-lockfile-shape", "opencode lockfile entries must use installed_roots.");
  }
  if (schemaVersion === 1 && adapter.adapter !== "codex") {
    return failure("unsupported", "unsupported-lockfile-shape", "schema_version 1 supports only Codex lockfile entries.");
  }
  if (adapter.installed_root !== SINGLE_ROOTS[adapter.adapter]) {
    return failure("unsupported", "unsupported-lockfile-shape", "Unsupported installed root.");
  }
  if (!isSha256(adapter.tree_sha256)) {
    return failure("invalid", "invalid-lockfile", "Adapter tree hash must be a SHA-256 value.");
  }
  if (!isNonNegativeInteger(adapter.file_count)) {
    return failure("invalid", "invalid-lockfile", "Adapter file_count must be a non-negative integer.");
  }
  adapter.file_count = Number.parseInt(adapter.file_count, 10);
  return undefined;
}

function validateMultiRootAdapter(adapter) {
  const allowed = [
    "adapter",
    "release",
    "source",
    "archive",
    "archive_sha256",
    "tree_hash_algorithm",
    "installed_roots",
    "root_hashes",
  ];
  const unexpected = unexpectedFields(adapter, allowed);
  if (unexpected.length) {
    return failure("unsupported", "unsupported-lockfile-shape", `Unsupported field generated.adapters[].${unexpected[0]}`);
  }
  for (const field of allowed) {
    if (adapter[field] === undefined) {
      return failure("invalid", "invalid-lockfile", `Missing adapter field: ${field}`);
    }
  }
  if (adapter.adapter !== "opencode") {
    return failure("unsupported", "unsupported-lockfile-shape", "Only opencode supports multi-root lockfile entries.");
  }
  const rootRoles = Object.keys(adapter.installed_roots).sort();
  const hashRoles = Object.keys(adapter.root_hashes).sort();
  if (!rootRoles.length || rootRoles.join("\n") !== hashRoles.join("\n")) {
    return failure("invalid", "invalid-lockfile", "installed_roots and root_hashes roles must match.");
  }
  for (const role of rootRoles) {
    if (!Object.hasOwn(OPENCODE_ROOTS, role) || adapter.installed_roots[role] !== OPENCODE_ROOTS[role]) {
      return failure("unsupported", "unsupported-lockfile-shape", "Unsupported opencode installed root.");
    }
    const hash = adapter.root_hashes[role];
    if (!hash || !isSha256(hash.tree_sha256)) {
      return failure("invalid", "invalid-lockfile", "Adapter root hash must be a SHA-256 value.");
    }
    if (!isNonNegativeInteger(hash.file_count)) {
      return failure("invalid", "invalid-lockfile", "Adapter root file_count must be a non-negative integer.");
    }
    hash.file_count = Number.parseInt(hash.file_count, 10);
  }
  return undefined;
}

function validateAdapter(adapter, schemaVersion) {
  if (!SUPPORTED_ADAPTERS.has(adapter.adapter)) {
    return failure("unsupported", "unsupported-lockfile-shape", "Unsupported lockfile adapter.");
  }
  if (!SUPPORTED_SOURCES.has(adapter.source)) {
    return failure("unsupported", "unsupported-lockfile-shape", "Unsupported lockfile adapter source.");
  }
  if (adapter.tree_hash_algorithm !== "rigorloop-tree-hash-v1") {
    return failure("unsupported", "unsupported-lockfile-shape", "Unsupported tree hash algorithm.");
  }
  if (!isSha256(adapter.archive_sha256)) {
    return failure("invalid", "invalid-lockfile", "Adapter archive hash must be a SHA-256 value.");
  }
  if (adapter.installed_roots !== undefined || adapter.root_hashes !== undefined) {
    if (schemaVersion !== 2) {
      return failure("unsupported", "unsupported-lockfile-shape", "Multi-root lockfile entries require schema_version 2.");
    }
    return validateMultiRootAdapter(adapter);
  }
  return validateSingleRootAdapter(adapter, schemaVersion);
}

export function parseLockfile(text) {
  if (typeof text !== "string" || !text.trim()) {
    return failure("invalid", "invalid-lockfile", "rigorloop.lock is empty or not text.");
  }
  if (/[\[\]{}]/.test(text)) {
    return failure("invalid", "invalid-lockfile", "rigorloop.lock is not valid strict YAML.");
  }

  const lines = text.replace(/\r\n?/g, "\n").split("\n");
  const top = parseTopLevel(lines);
  for (const key of top.keys()) {
    if (!TOP_LEVEL_FIELDS.includes(key)) {
      return failure("unsupported", "unsupported-lockfile-shape", `Unsupported top-level lockfile section: ${key}`);
    }
  }
  for (const key of TOP_LEVEL_FIELDS) {
    if (!top.has(key)) {
      return failure("invalid", "invalid-lockfile", `Missing top-level lockfile section: ${key}`);
    }
  }
  const schemaVersion = parseScalar(top.get("schema_version"));
  const parsedSchemaVersion = Number.parseInt(schemaVersion, 10);
  if (!/^\d+$/.test(schemaVersion) || ![1, 2].includes(parsedSchemaVersion)) {
    return failure("unsupported", "unsupported-lockfile-shape", "Unsupported lockfile schema_version.");
  }

  const rigorloop = parseSection(lines, "rigorloop", RIGORLOOP_FIELDS);
  if (rigorloop.ok === false) {
    return rigorloop;
  }
  const manifest = parseSection(lines, "manifest", MANIFEST_FIELDS);
  if (manifest.ok === false) {
    return manifest;
  }
  const generated = parseGeneratedSection(lines);
  if (generated.ok === false) {
    return generated;
  }
  if (rigorloop.missing || manifest.missing) {
    return failure("invalid", "invalid-lockfile", "Missing required lockfile section.");
  }
  if (rigorloop.fields.package !== "@xiongxianfei/rigorloop" || typeof rigorloop.fields.version !== "string") {
    return failure("invalid", "invalid-lockfile", "Invalid rigorloop package identity.");
  }
  if (manifest.fields.path !== "rigorloop.yaml" || !isSha256(manifest.fields.sha256)) {
    return failure("invalid", "invalid-lockfile", "Invalid manifest lockfile entry.");
  }

  const adapterResult = parseAdapters(lines);
  if (adapterResult.ok === false) {
    return adapterResult;
  }
  if (adapterResult.missing || !adapterResult.adapters.length) {
    return failure("invalid", "invalid-lockfile", "generated.adapters must contain at least one adapter entry.");
  }
  for (const adapter of adapterResult.adapters) {
    const adapterError = validateAdapter(adapter, parsedSchemaVersion);
    if (adapterError) {
      return adapterError;
    }
  }

  return {
    ok: true,
    lockfile: {
      schema_version: parsedSchemaVersion,
      rigorloop: rigorloop.fields,
      manifest: manifest.fields,
      generated: {
        adapters: adapterResult.adapters,
      },
    },
  };
}

export function serializeLockfile(lockfile) {
  const adapters = [...lockfile.generated.adapters].sort((left, right) => left.adapter.localeCompare(right.adapter));
  const lines = [
    `schema_version: ${lockfile.schema_version ?? 2}`,
    "",
    "rigorloop:",
    `  package: "${lockfile.rigorloop.package}"`,
    `  version: "${lockfile.rigorloop.version}"`,
    "",
    "manifest:",
    `  path: "${lockfile.manifest.path}"`,
    `  sha256: "${lockfile.manifest.sha256}"`,
    "",
    "generated:",
    "  adapters:",
  ];
  for (const adapter of adapters) {
    lines.push(
      `    - adapter: ${adapter.adapter}`,
      `      release: "${adapter.release}"`,
      `      source: ${adapter.source}`,
      `      archive: "${adapter.archive}"`,
      `      archive_sha256: "${adapter.archive_sha256}"`,
    );
    if (adapter.installed_roots) {
      lines.push(`      tree_hash_algorithm: ${adapter.tree_hash_algorithm}`, "      installed_roots:");
      for (const [role, root] of Object.entries(adapter.installed_roots)) {
        lines.push(`        ${role}: "${root}"`);
      }
      lines.push("      root_hashes:");
      for (const [role, hash] of Object.entries(adapter.root_hashes)) {
        lines.push(
          `        ${role}:`,
          `          tree_sha256: "${hash.tree_sha256}"`,
          `          file_count: ${hash.file_count}`,
        );
      }
    } else {
      lines.push(
        `      installed_root: "${adapter.installed_root}"`,
        `      tree_hash_algorithm: ${adapter.tree_hash_algorithm}`,
        `      tree_sha256: "${adapter.tree_sha256}"`,
        `      file_count: ${adapter.file_count}`,
      );
    }
  }
  return `${lines.join("\n")}\n`;
}

export function sha256NormalizedText(bytes) {
  let text = Buffer.isBuffer(bytes) ? bytes.toString("utf8") : String(bytes);
  if (text.charCodeAt(0) === 0xfeff) {
    text = text.slice(1);
  }
  return createHash("sha256").update(Buffer.from(text.replace(/\r\n?/g, "\n"), "utf8")).digest("hex");
}
