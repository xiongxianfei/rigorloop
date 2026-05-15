#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { EXIT, exitCodeForResult } from "../lib/command-result.js";

const ADAPTER = "codex";
const INSTALL_ROOT = ".agents/skills";
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
  return {
    schema_version: 1,
    tree_hash_algorithm: "rigorloop-tree-hash-v1",
    generated: {
      adapters: [
        {
          adapter: ADAPTER,
          source: source.type,
          archive: source.type === "local-archive" ? basename(source.archive) : source.archive,
          archive_sha256: "<planned>",
          installed_root: INSTALL_ROOT,
          tree_sha256: "<planned-after-install>",
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

function buildInitPlan(flags) {
  const info = packageInfo();
  const source = sourceForFlags(flags, info);
  const manifestPath = "rigorloop.yaml";
  const manifestAbsolutePath = resolve(process.cwd(), manifestPath);
  const installRootAbsolutePath = resolve(process.cwd(), INSTALL_ROOT);
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

  const agentsState = pathState(resolve(process.cwd(), ".agents"));
  const installRootState = pathState(installRootAbsolutePath);
  if (agentsState === "file") {
    actions.push({
      type: "create-dir",
      path: INSTALL_ROOT,
      status: "blocked",
      reason: ".agents exists and is not a directory.",
    });
    artifacts.push({
      path: INSTALL_ROOT,
      kind: "codex-install-root",
      status: "blocked",
    });
    blockers.push({
      code: "overwrite-refused",
      message: ".agents exists and is not a directory.",
      path: ".agents",
      next_action: "Move the existing file before running init.",
    });
  } else if (installRootState === "file") {
    actions.push({
      type: "create-dir",
      path: INSTALL_ROOT,
      status: "blocked",
      reason: `${INSTALL_ROOT} exists and is not a directory.`,
    });
    artifacts.push({
      path: INSTALL_ROOT,
      kind: "codex-install-root",
      status: "blocked",
    });
    blockers.push({
      code: "overwrite-refused",
      message: `${INSTALL_ROOT} exists and is not a directory.`,
      path: INSTALL_ROOT,
      next_action: "Move the existing file before running init.",
    });
  } else {
    actions.push({
      type: "create-dir",
      path: INSTALL_ROOT,
      status: flags.dryRun ? "planned" : installRootState === "directory" ? "skipped" : "pending",
      reason: installRootState === "directory" ? "Codex install root already exists." : "Create Codex install root.",
    });
    artifacts.push({
      path: INSTALL_ROOT,
      kind: "codex-install-root",
      status: installRootState === "directory" ? "existing" : flags.dryRun ? "planned" : "pending",
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

function handleInit(flags) {
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
    for (const action of plan.actions) {
      if (action.status === "pending") {
        action.status = "blocked";
        action.reason = "Blocked by mutation conflict.";
      }
    }
    for (const artifact of plan.artifacts) {
      if (artifact.status === "pending") {
        artifact.status = "blocked";
      }
    }
    const result = envelope("init", flags, {
      status: "blocked",
      summary: plan.blockers[0].message,
      actions: plan.actions,
      artifacts: plan.artifacts,
      blockers: plan.blockers,
      planned_manifest: {
        path: "rigorloop.yaml",
        content: plan.manifest,
      },
      planned_lockfile: plan.planned_lockfile,
    });
    if (flags.json) {
      writeJson(result);
    } else {
      process.stderr.write(`${result.summary}\n${plan.blockers[0].next_action}\n`);
    }
    return exitCodeForResult({ ...result, exit_class: "mutation_conflict" });
  }

  if (!flags.dryRun) {
    const manifestAction = plan.actions.find((action) => action.path === "rigorloop.yaml");
    const installRootAction = plan.actions.find((action) => action.path === INSTALL_ROOT);
    if (manifestAction?.status === "pending") {
      writeFileSync(resolve(process.cwd(), "rigorloop.yaml"), plan.manifest, "utf8");
      manifestAction.status = "done";
      plan.artifacts.find((artifact) => artifact.path === "rigorloop.yaml").status = "created";
    }
    if (installRootAction?.status === "pending") {
      mkdirSync(resolve(process.cwd(), INSTALL_ROOT), { recursive: true });
      installRootAction.status = "done";
      plan.artifacts.find((artifact) => artifact.path === INSTALL_ROOT).status = "created";
    }
  }

  const warnings = flags.dryRun ? [] : [LOCKFILE_WARNING];
  const result = envelope("init", flags, {
    status: warnings.length > 0 ? "warning" : "success",
    summary: flags.dryRun
      ? "RigorLoop init dry run completed. No files were written."
      : "RigorLoop initialized with Codex scaffold. Adapter archive installation is deferred to the archive verification milestone.",
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

function main() {
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

process.exitCode = main();
