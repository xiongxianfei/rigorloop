#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EXIT = {
  success: 0,
  warning: 0,
  blocked: 2,
  validationFailed: 3,
  usage: 4,
  overwriteRefused: 5,
  internal: 1,
};

const STATUS_TO_EXIT = {
  success: EXIT.success,
  warning: EXIT.warning,
  blocked: EXIT.blocked,
  error: EXIT.internal,
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
      flags.adapter = args[index + 1];
      index += 1;
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

function handleHelp(flags) {
  writeHuman(usage(), flags);
  return EXIT.success;
}

function handleVersion(flags) {
  const info = packageInfo();
  writeHuman(`${info.name} ${info.version}\n`, flags);
  return EXIT.success;
}

function invalidUsage(message, flags) {
  if (flags.json) {
    writeJson(
      envelope("unknown", flags, {
        status: "error",
        summary: message,
        errors: [
          {
            code: "invalid-usage",
            message,
            next_action: "Run rigorloop --help.",
          },
        ],
      }),
    );
  } else {
    process.stderr.write(`${message}\nRun rigorloop --help.\n`);
  }
  return EXIT.usage;
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
  return STATUS_TO_EXIT[result.status];
}

function handleInit(flags) {
  if (!flags.adapter) {
    return invalidUsage("Missing required option: --adapter codex.", flags);
  }
  if (flags.adapter !== "codex") {
    return unsupportedAdapter(flags.adapter, flags);
  }
  if (!flags.dryRun) {
    return invalidUsage("Only init --adapter codex --dry-run is implemented in M1.", flags);
  }

  const result = envelope("init", flags, {
    status: "success",
    summary: "RigorLoop init dry run completed. No files were written.",
  });

  if (flags.json) {
    writeJson(result);
  } else {
    writeHuman("RigorLoop init dry run completed.\nNo files were written.\n", flags);
  }
  return STATUS_TO_EXIT[result.status];
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
    return EXIT.internal;
  }
}

process.exitCode = main();
