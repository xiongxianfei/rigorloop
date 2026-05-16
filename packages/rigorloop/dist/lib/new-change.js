const CHANGE_ID_PATTERN = /^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
const CLASSIFICATION_PATTERN = /^[a-z][a-z0-9-]{0,63}$/;
const VALID_RISKS = new Set(["low", "medium", "high"]);
const VALID_PROFILES = new Set(["standard", "minimal"]);

function result(ok, code, message) {
  return ok ? { ok: true } : { ok: false, code, message };
}

export function validateChangeId(value) {
  if (typeof value !== "string" || !CHANGE_ID_PATTERN.test(value)) {
    return result(false, "invalid-change-id", "Change id must be a lowercase repository-safe path segment.");
  }
  return result(true);
}

export function validateClassification(value) {
  if (typeof value !== "string" || !CLASSIFICATION_PATTERN.test(value)) {
    return result(false, "invalid-classification", "Classification must be a lowercase token.");
  }
  return result(true);
}

export function validateRisk(value) {
  if (!VALID_RISKS.has(value)) {
    return result(false, "invalid-risk", "Risk must be low, medium, or high.");
  }
  return result(true);
}

export function validateProfile(value) {
  if (!VALID_PROFILES.has(value)) {
    return result(false, "unsupported-profile", "Profile must be standard or minimal.");
  }
  return result(true);
}

function yamlString(value) {
  return JSON.stringify(String(value));
}

export function renderChangeMetadata({ changeId, title, classification, risk }) {
  return `change_id: ${yamlString(changeId)}
title: ${yamlString(title)}
classification: ${yamlString(classification)}
risk: ${yamlString(risk)}
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  status: "pending"
  unresolved_items: 0
`;
}

export function buildNewChangeDraft({ changeId, title, classification = "default", risk = "medium", profile = "standard" }) {
  const root = `docs/changes/${changeId}`;
  const metadataPath = `${root}/change.yaml`;
  return {
    change: {
      change_id: changeId,
      root,
      metadata_path: metadataPath,
      profile,
    },
    planned_change_metadata: {
      path: metadataPath,
      content: renderChangeMetadata({ changeId, title, classification, risk }),
    },
  };
}

function parseOptionValue(args, index, code, message) {
  const value = args[index + 1];
  if (value === undefined || value.startsWith("--")) {
    return {
      error: {
        code,
        message,
      },
      consumed: 0,
    };
  }
  return { value, consumed: 1 };
}

export function parseNewChangeArgs(args, env = process.env) {
  const flags = {
    json: false,
    quiet: false,
    debug: false,
    noColor: Boolean(env.NO_COLOR),
    dryRun: false,
  };
  for (const arg of args) {
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
    }
  }

  const options = {
    classification: "default",
    risk: "medium",
    profile: "standard",
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
    } else if (arg === "--title") {
      const parsed = parseOptionValue(args, index, "missing-title", "--title requires a non-empty value.");
      if (parsed.error) {
        return { flags, error: parsed.error };
      }
      options.title = parsed.value;
      index += parsed.consumed;
    } else if (arg === "--type") {
      const parsed = parseOptionValue(args, index, "invalid-classification", "--type requires a classification token.");
      if (parsed.error) {
        return { flags, error: parsed.error };
      }
      options.classification = parsed.value;
      index += parsed.consumed;
    } else if (arg === "--risk") {
      const parsed = parseOptionValue(args, index, "invalid-risk", "--risk requires low, medium, or high.");
      if (parsed.error) {
        return { flags, error: parsed.error };
      }
      options.risk = parsed.value;
      index += parsed.consumed;
    } else if (arg === "--profile") {
      const parsed = parseOptionValue(args, index, "unsupported-profile", "--profile requires standard or minimal.");
      if (parsed.error) {
        return { flags, error: parsed.error };
      }
      options.profile = parsed.value;
      index += parsed.consumed;
    } else if (arg.startsWith("--")) {
      return {
        flags,
        error: {
          code: "invalid-usage",
          message: `Unknown option for new-change: ${arg}`,
        },
      };
    } else {
      positional.push(arg);
    }
  }

  const [changeId, ...extra] = positional;
  if (!changeId) {
    return {
      flags,
      error: {
        code: "missing-change-id",
        message: "new-change requires <change-id>.",
      },
    };
  }
  if (extra.length > 0) {
    return {
      flags,
      error: {
        code: "invalid-usage",
        message: "new-change accepts exactly one <change-id>.",
      },
    };
  }
  const changeIdValidation = validateChangeId(changeId);
  if (!changeIdValidation.ok) {
    return { flags, error: changeIdValidation };
  }
  if (!options.title || options.title.length === 0) {
    return {
      flags,
      error: {
        code: "missing-title",
        message: "new-change requires --title <title>.",
      },
    };
  }
  const classificationValidation = validateClassification(options.classification);
  if (!classificationValidation.ok) {
    return { flags, error: classificationValidation };
  }
  const riskValidation = validateRisk(options.risk);
  if (!riskValidation.ok) {
    return { flags, error: riskValidation };
  }
  const profileValidation = validateProfile(options.profile);
  if (!profileValidation.ok) {
    return { flags, error: profileValidation };
  }

  return {
    flags,
    value: {
      changeId,
      title: options.title,
      classification: options.classification,
      risk: options.risk,
      profile: options.profile,
    },
  };
}
