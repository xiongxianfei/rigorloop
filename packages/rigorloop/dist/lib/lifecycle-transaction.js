import { randomBytes, createHash } from "node:crypto";
import { chmodSync, closeSync, existsSync, fsyncSync, lstatSync, openSync, readFileSync, renameSync, statSync, unlinkSync, writeFileSync, writeSync } from "node:fs";
import { basename, dirname, join } from "node:path";

export const TRANSACTION_PHASES = Object.freeze(["prepared", "replaced"]);

function lifecycleError(code, message) {
  const error = new Error(`${code}: ${message}`);
  error.code = code;
  return error;
}

function digest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

export function lifecycleTransactionPaths(changePath) {
  const directory = dirname(changePath);
  return {
    lock: join(directory, ".rigorloop-lifecycle.lock"),
    recovery: join(directory, ".rigorloop-lifecycle-recovery.json"),
  };
}

function syncDirectory(path) {
  const fd = openSync(dirname(path), "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
}

function exclusiveJson(path, value) {
  const fd = openSync(path, "wx", 0o600);
  try {
    writeSync(fd, `${JSON.stringify(value, null, 2)}\n`, null, "utf8");
    fsyncSync(fd);
  } finally {
    closeSync(fd);
  }
  chmodSync(path, 0o600);
  syncDirectory(path);
}

function replaceJson(path, value) {
  const temporary = `${path}.tmp`;
  writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`, { encoding: "utf8", mode: 0o600, flag: "wx" });
  const fd = openSync(temporary, "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
  renameSync(temporary, path);
  syncDirectory(path);
}

function processIsLive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === "EPERM"; }
}

export function inspectLifecycleLock(changePath) {
  const { lock } = lifecycleTransactionPaths(changePath);
  if (!existsSync(lock)) return { state: "absent", path: lock };
  if (lstatSync(lock).isSymbolicLink() || !lstatSync(lock).isFile()) return { state: "unsafe", path: lock };
  try {
    const record = JSON.parse(readFileSync(lock, "utf8"));
    return { state: processIsLive(record.pid) ? "live" : "orphaned", path: lock, record };
  } catch {
    return { state: "unverifiable", path: lock };
  }
}

function acquireLock(changePath, changeId, nonce) {
  const { lock } = lifecycleTransactionPaths(changePath);
  try {
    exclusiveJson(lock, { schema_version: 1, change_id: changeId, pid: process.pid, nonce, started_at: new Date().toISOString() });
    return lock;
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
    const inspection = inspectLifecycleLock(changePath);
    if (inspection.state === "live") throw lifecycleError("RL_OPERATION_BUSY", "another lifecycle transaction owns the change lock");
    throw lifecycleError("RL_RECOVERY_REQUIRED", "an orphaned or unverifiable lifecycle lock requires named repair");
  }
}

function removeIfExists(path) {
  if (existsSync(path)) {
    unlinkSync(path);
    syncDirectory(path);
  }
}

function writeCandidate(changePath, bytes, nonce) {
  const path = join(dirname(changePath), `.rigorloop-lifecycle-candidate-${nonce}`);
  writeFileSync(path, bytes, { flag: "wx", mode: 0o600 });
  const fd = openSync(path, "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
  return path;
}

function fault(options, point) {
  const action = options?.fault?.(point);
  if (!action) return;
  const error = lifecycleError("RL_POST_VALIDATION_FAILED", `fault injected at ${point}`);
  error.simulatedCrash = action === "crash";
  throw error;
}

export function runLifecycleTransaction({ changePath, changeId, expectedRevision, currentRevision, candidateBytes, candidateRevision, validateCandidate, fault: faultHook }) {
  if (expectedRevision !== currentRevision) throw lifecycleError("RL_STALE_OPERATION", "expected lifecycle revision is not current");
  if (!Buffer.isBuffer(candidateBytes)) candidateBytes = Buffer.from(candidateBytes, "utf8");
  const priorBytes = readFileSync(changePath);
  const priorMode = statSync(changePath).mode & 0o777;
  const nonce = randomBytes(16).toString("hex");
  const paths = lifecycleTransactionPaths(changePath);
  let lockAcquired = false;
  let candidatePath;
  let replaced = false;
  let simulatedCrash = false;
  try {
    acquireLock(changePath, changeId, nonce);
    lockAcquired = true;
    if (existsSync(paths.recovery)) throw lifecycleError("RL_RECOVERY_REQUIRED", "an interrupted lifecycle transaction requires reconciliation");
    candidatePath = writeCandidate(changePath, candidateBytes, nonce);
    const bundle = {
      schema_version: 1,
      change_id: changeId,
      nonce,
      phase: "prepared",
      prior_sha256: digest(priorBytes),
      candidate_sha256: digest(candidateBytes),
      candidate_file: basename(candidatePath),
      prior_mode: priorMode,
      prior_bytes_base64: priorBytes.toString("base64"),
    };
    exclusiveJson(paths.recovery, bundle);
    fault({ fault: faultHook }, "after-recovery-prepared");
    renameSync(candidatePath, changePath);
    chmodSync(changePath, priorMode);
    candidatePath = undefined;
    syncDirectory(changePath);
    replaced = true;
    fault({ fault: faultHook }, "after-replace-before-phase");
    replaceJson(paths.recovery, { ...bundle, phase: "replaced" });
    fault({ fault: faultHook }, "after-replaced-phase");
    const persisted = readFileSync(changePath);
    if (digest(persisted) !== bundle.candidate_sha256 || validateCandidate(persisted) !== true) {
      throw lifecycleError("RL_POST_VALIDATION_FAILED", "persisted candidate failed post-validation");
    }
    removeIfExists(paths.recovery);
    removeIfExists(paths.lock);
    lockAcquired = false;
    return { status: "success", prior_sha256: bundle.prior_sha256, candidate_sha256: bundle.candidate_sha256, lifecycle_revision: candidateRevision };
  } catch (error) {
    simulatedCrash = Boolean(error.simulatedCrash);
    if (replaced && !simulatedCrash) {
      const restorePath = writeCandidate(changePath, priorBytes, `${nonce}-restore`);
      renameSync(restorePath, changePath);
      chmodSync(changePath, priorMode);
      syncDirectory(changePath);
      if (!readFileSync(changePath).equals(priorBytes)) throw lifecycleError("RL_POST_VALIDATION_FAILED", "prior bytes could not be restored");
      removeIfExists(paths.recovery);
    }
    if (!simulatedCrash && candidatePath) removeIfExists(candidatePath);
    if (!simulatedCrash && lockAcquired) removeIfExists(paths.lock);
    throw error;
  }
}

export function inspectLifecycleRecovery(changePath) {
  const paths = lifecycleTransactionPaths(changePath);
  if (!existsSync(paths.recovery)) return { state: "absent", path: paths.recovery };
  try {
    if (lstatSync(paths.recovery).isSymbolicLink() || !lstatSync(paths.recovery).isFile()) throw new Error("unsafe recovery path");
    const bundle = JSON.parse(readFileSync(paths.recovery, "utf8"));
    if (bundle.schema_version !== 1 || !TRANSACTION_PHASES.includes(bundle.phase) || typeof bundle.prior_bytes_base64 !== "string" || !/^\.rigorloop-lifecycle-candidate-[a-f0-9]{32}$/.test(bundle.candidate_file) || !Number.isInteger(bundle.prior_mode) || bundle.prior_mode < 0 || bundle.prior_mode > 0o777) throw new Error("invalid recovery bundle");
    const current = digest(readFileSync(changePath));
    const observed = current === bundle.prior_sha256 ? "prior" : current === bundle.candidate_sha256 ? "candidate" : "unknown";
    return { state: "present", path: paths.recovery, bundle, observed };
  } catch {
    return { state: "unsafe", path: paths.recovery };
  }
}

export function reconcileInterruptedTransaction({ changePath, changeId, validateCandidate }) {
  const inspection = inspectLifecycleRecovery(changePath);
  if (inspection.state === "absent") return { status: "nothing-to-reconcile" };
  if (inspection.state !== "present" || inspection.observed === "unknown") throw lifecycleError("RL_RECOVERY_REQUIRED", "recovery state is malformed or does not match known identities");
  const nonce = randomBytes(16).toString("hex");
  const lock = acquireLock(changePath, changeId, nonce);
  try {
    const abandonedCandidate = join(dirname(changePath), inspection.bundle.candidate_file);
    if (inspection.observed === "candidate" && validateCandidate(readFileSync(changePath)) !== true) {
      const prior = Buffer.from(inspection.bundle.prior_bytes_base64, "base64");
      if (digest(prior) !== inspection.bundle.prior_sha256) throw lifecycleError("RL_RECOVERY_REQUIRED", "recovery prior identity is invalid");
      const restore = writeCandidate(changePath, prior, `${nonce}-restore`);
      renameSync(restore, changePath);
      chmodSync(changePath, inspection.bundle.prior_mode);
      syncDirectory(changePath);
      if (digest(readFileSync(changePath)) !== inspection.bundle.prior_sha256) throw lifecycleError("RL_POST_VALIDATION_FAILED", "recovery restoration could not be verified");
      removeIfExists(inspection.path);
      removeIfExists(abandonedCandidate);
      return { status: "restored-prior" };
    }
    removeIfExists(inspection.path);
    removeIfExists(abandonedCandidate);
    return { status: inspection.observed === "candidate" ? "committed-candidate" : "abandoned-prepared" };
  } finally {
    removeIfExists(lock);
  }
}
