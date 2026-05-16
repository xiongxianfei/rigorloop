import { lstatSync, mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const DEFAULT_FS_OPS = {
  lstatSync,
  mkdirSync,
  writeFileSync,
};

function lstatRelative(cwd, relativePath, fsOps) {
  try {
    return fsOps.lstatSync(resolve(cwd, relativePath));
  } catch (error) {
    if (error.code === "ENOENT") {
      return undefined;
    }
    throw error;
  }
}

function newChangeAction(type, path, status, reason) {
  return { type, path, status, reason };
}

function newChangeBlocker(code, path, message) {
  return {
    code,
    message,
    path,
    next_action: code === "path-exists"
      ? "Choose a new change id or move the existing file before rerunning."
      : "Replace the conflicting path with a directory before rerunning.",
  };
}

function newChangeWriteError(path, error) {
  return {
    code: "write-failed",
    message: `Failed to write ${path}: ${error.message}`,
    path,
    next_action: "Inspect filesystem permissions and rerun the command after resolving the write failure.",
  };
}

export function planNewChangeWrite(cwd, draft, fsOps = DEFAULT_FS_OPS) {
  const directories = ["docs", "docs/changes", draft.change.root];
  const actions = [];
  const blockers = [];

  for (const relativePath of directories) {
    const stat = lstatRelative(cwd, relativePath, fsOps);
    if (!stat) {
      actions.push(newChangeAction("create-dir", relativePath, "planned", "Directory will be created."));
    } else if (stat.isDirectory() && !stat.isSymbolicLink()) {
      actions.push(newChangeAction("create-dir", relativePath, "existing", "Directory already exists."));
    } else {
      actions.push(newChangeAction("create-dir", relativePath, "blocked", "Path exists and is not a directory."));
      blockers.push(newChangeBlocker("path-not-directory", relativePath, "Planned directory path exists and is not a directory."));
      return { actions, blockers };
    }
  }

  const metadataStat = lstatRelative(cwd, draft.change.metadata_path, fsOps);
  if (metadataStat) {
    actions.push(newChangeAction("write", draft.change.metadata_path, "blocked", "File already exists and will not be overwritten."));
    blockers.push(newChangeBlocker("path-exists", draft.change.metadata_path, "Planned change metadata file already exists."));
  } else {
    actions.push(newChangeAction("write", draft.change.metadata_path, "planned", "Change metadata file will be written."));
  }

  return { actions, blockers };
}

export function artifactForNewChange(draft, status) {
  return {
    path: draft.change.metadata_path,
    kind: "change-metadata",
    status,
  };
}

export function applyNewChangePlan(cwd, actions, draft, fsOps = DEFAULT_FS_OPS) {
  for (const action of actions) {
    if (action.type === "create-dir" && action.status === "planned") {
      try {
        fsOps.mkdirSync(resolve(cwd, action.path));
      } catch (error) {
        action.status = "failed";
        action.reason = "Directory creation failed.";
        return { ok: false, error: newChangeWriteError(action.path, error) };
      }
      action.status = "done";
      action.reason = "Directory created.";
    }
  }

  const metadataAction = actions.find((action) => action.path === draft.change.metadata_path);
  if (metadataAction?.status === "planned") {
    try {
      fsOps.writeFileSync(resolve(cwd, draft.change.metadata_path), draft.planned_change_metadata.content, "utf8");
    } catch (error) {
      metadataAction.status = "failed";
      metadataAction.reason = "Change metadata file write failed.";
      return { ok: false, error: newChangeWriteError(draft.change.metadata_path, error) };
    }
    metadataAction.status = "done";
    metadataAction.reason = "Change metadata file written.";
  }

  return { ok: true };
}

export function runNewChangePlan({ cwd, draft, flags, profile, fsOps = DEFAULT_FS_OPS }) {
  const writePlan = planNewChangeWrite(cwd, draft, fsOps);
  const blocked = writePlan.blockers.length > 0;
  const warnings =
    profile === "minimal" && !blocked
      ? [
          {
            code: "durable-reasoning-not-scaffolded",
            message: "new-change created only change metadata; durable reasoning remains a later workflow requirement.",
          },
        ]
      : [];

  let applyResult = { ok: true };
  if (!flags.dryRun && !blocked) {
    applyResult = applyNewChangePlan(cwd, writePlan.actions, draft, fsOps);
  }

  const failed = !applyResult.ok;
  const artifactStatus = failed ? "failed" : blocked ? "blocked" : flags.dryRun ? "planned" : "created";

  return {
    exit_class: failed ? "internal" : blocked ? "mutation_conflict" : "success",
    result: {
      status: failed ? "error" : blocked ? "blocked" : warnings.length > 0 ? "warning" : "success",
      summary: failed
        ? "RigorLoop new-change failed while writing files."
        : blocked
          ? "RigorLoop new-change blocked before writing files."
          : flags.dryRun
            ? "RigorLoop new-change dry run completed. No files were written."
            : "RigorLoop change metadata scaffold created.",
      actions: writePlan.actions,
      artifacts: [artifactForNewChange(draft, artifactStatus)],
      blockers: writePlan.blockers,
      warnings,
      errors: failed ? [applyResult.error] : [],
      change: draft.change,
      planned_change_metadata: draft.planned_change_metadata,
    },
  };
}
