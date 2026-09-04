import { createHash, randomBytes } from "node:crypto";
import {
  chmodSync,
  closeSync,
  existsSync,
  fsyncSync,
  lstatSync,
  mkdirSync,
  openSync,
  readFileSync,
  realpathSync,
  renameSync,
  rmSync,
  statSync,
  unlinkSync,
  writeSync,
} from "node:fs";
import { dirname, join, resolve, sep } from "node:path";

import { parseCompactYaml, validateCompactPath, validateCompactRecord } from "./compact-contract.js";
import { serializeLifecycleYaml } from "./lifecycle-contract.js";

const MAX_REQUEST_BYTES = 1024 * 1024;
const MAX_FILE_BYTES = 8 * 1024 * 1024;
const MAX_TRANSACTION_BYTES = 64 * 1024 * 1024;

function sha256(bytes) {
  return `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
}

function fail(code, summary) {
  const error = new Error(summary);
  error.code = code;
  return error;
}

function sorted(values) {
  return [...values].sort((left, right) => Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8")));
}

function bytes(value) {
  if (value === null) return null;
  return Buffer.isBuffer(value) ? Buffer.from(value) : Buffer.from(value, "utf8");
}

function exactKeys(actual, expected, code, summary) {
  const left = sorted(Object.keys(actual));
  const right = sorted(Object.keys(expected));
  if (left.length !== right.length || left.some((value, index) => value !== right[index])) throw fail(code, summary);
}

function diagnostic(code, summary, invariant, operation = null, nextOperation = null) {
  return { code, summary, invariant, scope: operation === null ? "progression" : "operation", operation, identities: [], next_operation: nextOperation };
}

function result(candidate, status, { affectedPaths = [], bytesChanged = false, error = null, resultingRevision = null } = {}) {
  const common = {
    schema: "compact-result-v1",
    status,
    change_id: candidate?.changeId ?? null,
    prior_lifecycle_revision: candidate?.priorLifecycleRevision ?? null,
    resulting_lifecycle_revision: resultingRevision,
    affected_paths: affectedPaths,
    bytes_changed: bytesChanged,
    blockers: [],
    errors: [],
    next_operation: status === "recovery-required" ? "recover" : null,
    projection: null,
  };
  if (error) {
    const safeCode = typeof error.code === "string" && /^RL_[A-Z0-9_]+$/.test(error.code) ? error.code : "RL_TRANSACTION_FAILED";
    const safeSummary = safeCode === error.code && typeof error.message === "string" ? error.message : "Compact transaction failed safely";
    common.errors.push(diagnostic(safeCode, safeSummary, safeCode === "RL_STALE_OPERATION" ? "expected-file-identity" : "compact-transaction", status === "recovery-required" ? "recover" : candidate?.request?.operation ?? null, status === "recovery-required" ? "recover" : null));
  }
  validateCompactRecord(common, "compact-result-v1");
  return common;
}

function validateDigest(value, label) {
  if (typeof value !== "string" || !/^sha256:[a-f0-9]{64}$/.test(value)) throw fail("RL_INVALID_REQUEST", `${label} must be a SHA-256 identity`);
}

export function evaluateCompactCandidate({ request, currentFiles, candidateFiles, resolvedCandidateFiles = {}, candidateLifecycleRevision, validateCandidateSet }) {
  validateCompactRecord(request, "compact-operation-v1");
  validateDigest(candidateLifecycleRevision, "candidate lifecycle revision");
  if (!currentFiles || Array.isArray(currentFiles) || typeof currentFiles !== "object") throw fail("RL_INVALID_REQUEST", "current files must be a mapping");
  exactKeys(request.expected_files, currentFiles, "RL_STALE_OPERATION", "expected files must bind the complete evaluator input");
  const normalizedCurrent = Object.create(null);
  for (const path of sorted(Object.keys(currentFiles))) {
    validateCompactPath(path);
    const current = bytes(currentFiles[path]);
    const expected = request.expected_files[path];
    const state = current === null ? "absent" : "present";
    const identity = current === null ? null : sha256(current);
    if (expected.path !== path || expected.state !== state || expected.identity !== identity) throw fail("RL_STALE_OPERATION", "an expected file identity is stale or contradictory");
    normalizedCurrent[path] = current;
  }

  const files = Object.create(null);
  if (!candidateFiles || Array.isArray(candidateFiles) || typeof candidateFiles !== "object") throw fail("RL_INVALID_REQUEST", "derived candidate files must be a mapping");
  for (const path of sorted(Object.keys(candidateFiles))) {
    if (!Object.hasOwn(normalizedCurrent, path)) throw fail("RL_INVALID_REQUEST", "every affected path must have an expected-file binding");
    const declaration = candidateFiles[path];
    let candidateBytes = null;
    if (declaration.action === "replace") {
      candidateBytes = declaration.source === "inline" ? Buffer.from(declaration.content, "utf8") : bytes(resolvedCandidateFiles[declaration.source_path]);
      if (candidateBytes === null || sha256(candidateBytes) !== declaration.identity) throw fail("RL_INVALID_REQUEST", "candidate content identity is missing or contradictory");
    }
    files[path] = {
      path,
      priorBytes: normalizedCurrent[path],
      priorIdentity: normalizedCurrent[path] === null ? null : sha256(normalizedCurrent[path]),
      candidateBytes,
      candidateIdentity: candidateBytes === null ? null : sha256(candidateBytes),
    };
    if (files[path].priorIdentity === files[path].candidateIdentity) throw fail("RL_INVALID_REQUEST", "candidate files must contain only paths whose authoritative state changes");
  }
  const affectedPaths = sorted(Object.keys(files));
  if (affectedPaths.length === 0) throw fail("RL_INVALID_REQUEST", "a compact mutation must affect at least one file");
  const candidateSet = Object.fromEntries(sorted(Object.keys(normalizedCurrent)).map((path) => [path, Object.hasOwn(files, path) ? files[path].candidateBytes : normalizedCurrent[path]]));
  if (typeof validateCandidateSet !== "function" || validateCandidateSet(normalizedCurrent, request.expected_lifecycle_revision) !== true) throw fail("RL_STALE_OPERATION", "current set failed complete-set validation");
  if (validateCandidateSet(candidateSet, candidateLifecycleRevision) !== true) throw fail("RL_INVALID_REQUEST", "candidate set failed complete-set validation");
  return {
    request,
    requestBytes: Buffer.byteLength(JSON.stringify(request), "utf8"),
    changeId: request.change_id,
    priorLifecycleRevision: request.expected_lifecycle_revision,
    candidateLifecycleRevision,
    currentFiles: normalizedCurrent,
    candidateSet,
    files,
    affectedPaths,
  };
}

function transactionPaths(root, changeId) {
  validateCompactPath(changeId, "change id");
  if (changeId.includes("/")) throw fail("RL_UNSAFE_PATH", "change id must be one safe path segment");
  const base = join(root, ".rigorloop", "transactions");
  const directory = join(base, changeId);
  return { base, directory, lock: join(directory, "lock"), recovery: join(directory, "recovery.yaml"), prior: join(directory, "prior"), candidate: join(directory, "candidate") };
}

function assertContained(root, path) {
  const rootPath = resolve(root);
  const target = resolve(root, path);
  if (target !== rootPath && !target.startsWith(`${rootPath}${sep}`)) throw fail("RL_UNSAFE_PATH", "path escapes the repository root");
  return target;
}

function assertSafeAncestors(root, repositoryPath) {
  validateCompactPath(repositoryPath);
  const target = assertContained(root, repositoryPath);
  const parent = dirname(target);
  const relativeParts = repositoryPath.split("/").slice(0, -1);
  let cursor = resolve(root);
  for (const part of relativeParts) {
    cursor = join(cursor, part);
    if (!existsSync(cursor)) throw fail("RL_UNSAFE_PATH", "authoritative parent directory is missing");
    const status = lstatSync(cursor);
    if (status.isSymbolicLink() || !status.isDirectory()) throw fail("RL_UNSAFE_PATH", "authoritative path crosses an unsafe parent");
  }
  if (existsSync(target)) {
    const status = lstatSync(target);
    if (status.isSymbolicLink() || !status.isFile()) throw fail("RL_UNSAFE_PATH", "authoritative path is not a regular file");
  }
  return { target, parent };
}

function syncFile(path) {
  const fd = openSync(path, "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
}

function syncDirectory(path) {
  const fd = openSync(path, "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
}

function ensurePrivateDirectory(path, { create = true } = {}) {
  if (!existsSync(path)) {
    if (!create) throw fail("RL_RECOVERY_REQUIRED", "transaction directory is missing");
    mkdirSync(path, { mode: 0o700 });
  }
  const status = lstatSync(path);
  if (status.isSymbolicLink() || !status.isDirectory() || (status.mode & 0o077) !== 0) throw fail("RL_UNSAFE_PATH", "transaction directory must be a private regular directory");
  chmodSync(path, 0o700);
}

function prepareTransactionDirectory(root, changeId) {
  const paths = transactionPaths(root, changeId);
  const rigorloop = join(root, ".rigorloop");
  if (!existsSync(rigorloop)) {
    try { mkdirSync(rigorloop, { mode: 0o700 }); } catch (error) { if (error.code !== "EEXIST") throw error; }
    syncDirectory(root);
  }
  if (lstatSync(rigorloop).isSymbolicLink() || !lstatSync(rigorloop).isDirectory()) throw fail("RL_UNSAFE_PATH", "local state root is unsafe");
  if (!existsSync(paths.base)) {
    try { mkdirSync(paths.base, { mode: 0o700 }); } catch (error) { if (error.code !== "EEXIST") throw error; }
    syncDirectory(rigorloop);
  }
  if (lstatSync(paths.base).isSymbolicLink() || !lstatSync(paths.base).isDirectory()) throw fail("RL_UNSAFE_PATH", "transaction root is unsafe");
  if (existsSync(paths.directory)) ensurePrivateDirectory(paths.directory);
  else {
    try { mkdirSync(paths.directory, { mode: 0o700 }); } catch (error) { if (error.code !== "EEXIST") throw error; }
    ensurePrivateDirectory(paths.directory);
    syncDirectory(paths.base);
  }
  if ((statSync(paths.directory).mode & 0o777) !== 0o700) throw fail("RL_UNSAFE_PATH", "transaction directory permissions are not private");
  if (statSync(paths.directory).dev !== statSync(root).dev) throw fail("RL_UNSUPPORTED_DURABILITY", "transaction state is not on the repository filesystem");
  return paths;
}

function writePrivate(path, content, flag = "wx") {
  const fd = openSync(path, flag, 0o600);
  try {
    let offset = 0;
    while (offset < content.length) offset += writeSync(fd, content, offset, content.length - offset);
    fsyncSync(fd);
  } finally {
    closeSync(fd);
  }
  chmodSync(path, 0o600);
}

function processIsLive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === "EPERM"; }
}

function acquireLock(paths, changeId, requestedTransactionId = null) {
  const transactionId = requestedTransactionId ?? randomBytes(16).toString("hex");
  try {
    writePrivate(paths.lock, Buffer.from(`${JSON.stringify({ schema_version: 1, change_id: changeId, transaction_id: transactionId, pid: process.pid })}\n`));
    syncDirectory(paths.directory);
    return transactionId;
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
    const status = lstatSync(paths.lock);
    if (status.isSymbolicLink() || !status.isFile() || (status.mode & 0o077) !== 0) throw fail("RL_UNSAFE_PATH", "compact transaction lock is unsafe");
    let live = false;
    try { live = processIsLive(JSON.parse(readFileSync(paths.lock, "utf8")).pid); } catch {}
    throw fail(live ? "RL_OPERATION_BUSY" : "RL_RECOVERY_REQUIRED", live ? "another compact writer owns the change lock" : "an unverifiable compact lock requires recovery");
  }
}

function recoveryBytes(recovery) {
  validateCompactRecord(recovery, "compact-recovery-v1");
  return Buffer.from(serializeLifecycleYaml(recovery), "utf8");
}

function replaceRecovery(paths, recovery) {
  const temporary = join(paths.directory, ".recovery-next");
  writePrivate(temporary, recoveryBytes(recovery));
  renameSync(temporary, paths.recovery);
  syncDirectory(paths.directory);
}

function cleanup(paths) {
  if (existsSync(paths.directory)) rmSync(paths.directory, { recursive: true });
  if (existsSync(paths.base)) syncDirectory(paths.base);
}

function invokeFault(hook, point) {
  const action = hook?.(point);
  if (!action) return;
  const error = fail("RL_TRANSACTION_FAILED", `transaction interrupted at ${point}`);
  error.simulatedCrash = action === "crash";
  throw error;
}

function currentBytes(root, path) {
  const { target } = assertSafeAncestors(root, path);
  return existsSync(target) ? readFileSync(target) : null;
}

function stateMatches(actual, expectedIdentity) {
  return expectedIdentity === null ? actual === null : actual !== null && sha256(actual) === expectedIdentity;
}

function readCandidateSet(root, candidate) {
  return Object.fromEntries(sorted(Object.keys(candidate.currentFiles)).map((path) => [path, currentBytes(root, path)]));
}

function allAffectedMatch(root, candidate, side) {
  return candidate.affectedPaths.every((path) => stateMatches(currentBytes(root, path), candidate.files[path][`${side}Identity`]));
}

function enforceLimits(candidate) {
  if (candidate.requestBytes > MAX_REQUEST_BYTES) throw fail("RL_LIMIT_EXCEEDED", "semantic request exceeds 1 MiB");
  let combined = 0;
  for (const item of Object.values(candidate.files)) {
    for (const content of [item.priorBytes, item.candidateBytes]) {
      if (content === null) continue;
      if (content.length > MAX_FILE_BYTES) throw fail("RL_LIMIT_EXCEEDED", "authoritative compact file exceeds 8 MiB");
      combined += content.length;
    }
  }
  if (combined > MAX_TRANSACTION_BYTES) throw fail("RL_LIMIT_EXCEEDED", "combined transaction content exceeds 64 MiB");
}

function replaceAuthoritative(root, item, sourcePath, nonce) {
  const { target, parent } = assertSafeAncestors(root, item.path);
  if (sourcePath === null) {
    if (existsSync(target)) unlinkSync(target);
    syncDirectory(parent);
    return;
  }
  const temporary = join(parent, `.rigorloop-compact-${nonce}-${randomBytes(8).toString("hex")}`);
  writePrivate(temporary, readFileSync(sourcePath));
  renameSync(temporary, target);
  syncFile(target);
  syncDirectory(parent);
}

function restorePrior(root, paths, recovery) {
  for (const item of recovery.affected_files) replaceAuthoritative(root, item, item.prior_content === null ? null : join(root, item.prior_content), `${recovery.transaction_id}-restore`);
  for (const item of recovery.affected_files) if (!stateMatches(currentBytes(root, item.path), item.prior_identity)) throw fail("RL_RECOVERY_REQUIRED", "prior set restoration did not match its recorded identity");
}

function loadRecovery(root, paths) {
  if (!existsSync(paths.recovery)) throw fail("RL_RECOVERY_REQUIRED", "recovery metadata is missing");
  const raw = readFileSync(paths.recovery);
  const recovery = parseCompactYaml(raw.toString("utf8"), "compact-recovery-v1");
  for (const item of recovery.affected_files) {
    for (const [contentPath, identity] of [[item.prior_content, item.prior_identity], [item.candidate_content, item.candidate_identity]]) {
      if (contentPath === null) continue;
      const absolute = assertContained(root, contentPath);
      if (!existsSync(absolute) || lstatSync(absolute).isSymbolicLink() || !lstatSync(absolute).isFile() || (statSync(absolute).mode & 0o077) !== 0 || sha256(readFileSync(absolute)) !== identity) throw fail("RL_RECOVERY_REQUIRED", "recovery content is missing, unsafe, or tampered");
    }
  }
  return { raw, recovery, identity: sha256(raw) };
}

function observedRecoveryState(root, recovery) {
  const observed = Object.create(null);
  for (const item of recovery.affected_files) {
    const current = currentBytes(root, item.path);
    const side = stateMatches(current, item.prior_identity) ? "prior" : stateMatches(current, item.candidate_identity) ? "candidate" : "unknown";
    if (side === "unknown") throw fail("RL_RECOVERY_REQUIRED", "an authoritative file does not match either recoverable state");
    observed[item.path] = current;
    if (recovery.phase === "prepared" && side !== "prior") throw fail("RL_RECOVERY_REQUIRED", "prepared recovery state contradicts authoritative files");
    if (recovery.phase === "persisted" && (side !== "candidate" || item.replacement_status !== "replaced")) throw fail("RL_RECOVERY_REQUIRED", "persisted recovery state contradicts authoritative files");
  }
  if (recovery.phase === "prepared" && recovery.affected_files.some((item) => item.replacement_status !== "pending")) throw fail("RL_RECOVERY_REQUIRED", "prepared recovery status is contradictory");
  return observed;
}

export function inspectCompactTransaction({ root, changeId }) {
  try {
    const paths = transactionPaths(root, changeId);
    if (!existsSync(paths.directory)) return { status: "clear", recovery_identity: null };
    ensurePrivateDirectory(paths.directory, { create: false });
    if (existsSync(paths.recovery)) {
      const loaded = loadRecovery(root, paths);
      return { status: "recovery-required", recovery_identity: loaded.identity, phase: loaded.recovery.phase };
    }
    if (existsSync(paths.lock)) {
      try {
        const lock = JSON.parse(readFileSync(paths.lock, "utf8"));
        return { status: processIsLive(lock.pid) ? "busy" : "recovery-required", recovery_identity: null };
      } catch { return { status: "recovery-required", recovery_identity: null }; }
    }
    return { status: "recovery-required", recovery_identity: null };
  } catch {
    return { status: "recovery-required", recovery_identity: null };
  }
}

export function runCompactTransaction({ root, candidate, validateCandidateSet, fault, durabilityProbe = () => true }) {
  let paths;
  let transactionDirectoryCreated = false;
  let lockAcquired = false;
  let recoveryWritten = false;
  let authoritativeChanged = false;
  try {
    enforceLimits(candidate);
    realpathSync(root);
    for (const path of sorted(Object.keys(candidate.currentFiles))) assertSafeAncestors(root, path);
    const prospectivePaths = transactionPaths(root, candidate.changeId);
    transactionDirectoryCreated = !existsSync(prospectivePaths.directory);
    paths = prospectivePaths;
    prepareTransactionDirectory(root, candidate.changeId);
    if (existsSync(paths.recovery)) throw fail("RL_RECOVERY_REQUIRED", "an unresolved compact transaction requires recovery");
    const transactionId = acquireLock(paths, candidate.changeId);
    lockAcquired = true;
    invokeFault(fault, "after-lock");
    if (durabilityProbe() !== true) throw fail("RL_UNSUPPORTED_DURABILITY", "required file and directory durability primitives are unavailable");
    const transactionDevice = statSync(paths.directory).dev;
    for (const path of candidate.affectedPaths) {
      const { parent } = assertSafeAncestors(root, path);
      if (statSync(parent).dev !== transactionDevice) throw fail("RL_UNSUPPORTED_DURABILITY", "an authoritative file is not on the transaction filesystem");
      syncDirectory(parent);
    }

    const observedSet = readCandidateSet(root, candidate);
    const expectedMatches = Object.keys(candidate.currentFiles).every((path) => stateMatches(observedSet[path], candidate.currentFiles[path] === null ? null : sha256(candidate.currentFiles[path])));
    if (!expectedMatches) {
      if (allAffectedMatch(root, candidate, "candidate") && validateCandidateSet(readCandidateSet(root, candidate), candidate.candidateLifecycleRevision) === true) {
        cleanup(paths);
        return result(candidate, "already-applied", { resultingRevision: candidate.candidateLifecycleRevision });
      }
      throw fail("RL_STALE_OPERATION", "expected lifecycle or file identity is no longer current");
    }
    if (candidate.request.expected_lifecycle_revision !== candidate.priorLifecycleRevision) throw fail("RL_STALE_OPERATION", "expected lifecycle revision is no longer current");
    if (validateCandidateSet(observedSet, candidate.priorLifecycleRevision) !== true) throw fail("RL_STALE_OPERATION", "current set failed complete-set validation");
    if (validateCandidateSet(candidate.candidateSet, candidate.candidateLifecycleRevision) !== true) throw fail("RL_INVALID_REQUEST", "candidate set failed complete-set validation");
    syncDirectory(root);
    mkdirSync(paths.prior, { mode: 0o700 });
    mkdirSync(paths.candidate, { mode: 0o700 });
    const recovery = {
      schema: "compact-recovery-v1",
      transaction_id: transactionId,
      change_id: candidate.changeId,
      phase: "prepared",
      prior_lifecycle_revision: candidate.priorLifecycleRevision,
      candidate_lifecycle_revision: candidate.candidateLifecycleRevision,
      affected_files: [],
    };
    for (const [index, path] of candidate.affectedPaths.entries()) {
      const item = candidate.files[path];
      const name = String(index).padStart(4, "0");
      const priorContent = item.priorBytes === null ? null : `.rigorloop/transactions/${candidate.changeId}/prior/${name}`;
      const candidateContent = item.candidateBytes === null ? null : `.rigorloop/transactions/${candidate.changeId}/candidate/${name}`;
      if (item.priorBytes !== null) writePrivate(join(paths.prior, name), item.priorBytes);
      if (item.candidateBytes !== null) writePrivate(join(paths.candidate, name), item.candidateBytes);
      recovery.affected_files.push({ path, prior_state: item.priorBytes === null ? "absent" : "present", prior_identity: item.priorIdentity, prior_content: priorContent, candidate_state: item.candidateBytes === null ? "absent" : "present", candidate_identity: item.candidateIdentity, candidate_content: candidateContent, replacement_status: "pending" });
    }
    syncDirectory(paths.prior);
    syncDirectory(paths.candidate);
    invokeFault(fault, "after-preparation");
    writePrivate(paths.recovery, recoveryBytes(recovery));
    syncDirectory(paths.directory);
    recoveryWritten = true;
    invokeFault(fault, "after-recovery-prepared");
    recovery.phase = "replacing";
    replaceRecovery(paths, recovery);
    invokeFault(fault, "after-phase-replacing");
    for (const item of recovery.affected_files) {
      replaceAuthoritative(root, item, item.candidate_content === null ? null : join(root, item.candidate_content), transactionId);
      authoritativeChanged = true;
      item.replacement_status = "replaced";
      replaceRecovery(paths, recovery);
      invokeFault(fault, `after-replace:${item.path}`);
    }
    const persisted = readCandidateSet(root, candidate);
    if (!allAffectedMatch(root, candidate, "candidate") || validateCandidateSet(persisted, candidate.candidateLifecycleRevision) !== true) throw fail("RL_TRANSACTION_FAILED", "persisted candidate failed complete-set validation");
    recovery.phase = "persisted";
    replaceRecovery(paths, recovery);
    for (const item of recovery.affected_files) {
      const { parent } = assertSafeAncestors(root, item.path);
      if (item.candidate_identity !== null) syncFile(join(root, item.path));
      syncDirectory(parent);
    }
    invokeFault(fault, "after-persisted-readback");
    invokeFault(fault, "during-cleanup");
    cleanup(paths);
    return result(candidate, "success", { affectedPaths: candidate.affectedPaths, bytesChanged: true, resultingRevision: candidate.candidateLifecycleRevision });
  } catch (error) {
    if (error.simulatedCrash) {
      return result(candidate, "recovery-required", { affectedPaths: authoritativeChanged ? candidate.affectedPaths : [], bytesChanged: authoritativeChanged, error, resultingRevision: null });
    }
    if (paths && recoveryWritten) {
      try {
        const { recovery } = loadRecovery(root, paths);
        restorePrior(root, paths, recovery);
        cleanup(paths);
        authoritativeChanged = false;
      } catch (recoveryError) {
        return result(candidate, "recovery-required", { affectedPaths: candidate.affectedPaths, bytesChanged: authoritativeChanged, error: recoveryError });
      }
    } else if (paths && lockAcquired) cleanup(paths);
    else if (paths && transactionDirectoryCreated && existsSync(paths.directory) && !existsSync(paths.lock) && !existsSync(paths.recovery)) cleanup(paths);
    const status = error.code === "RL_OPERATION_BUSY" ? "busy" : error.code === "RL_RECOVERY_REQUIRED" ? "recovery-required" : "rejected";
    return result(candidate, status, { affectedPaths: authoritativeChanged ? candidate.affectedPaths : [], bytesChanged: authoritativeChanged, error });
  }
}

export function recoverCompactTransaction({ root, changeId, action, expectedRecoveryIdentity, readCompleteSet, validateCandidateSet }) {
  let candidate = { changeId, priorLifecycleRevision: null };
  let paths;
  let recoveryLockAcquired = false;
  try {
    if (!["restore-prior", "accept-candidate"].includes(action)) throw fail("RL_INVALID_REQUEST", "unknown recovery action");
    if (typeof readCompleteSet !== "function" || typeof validateCandidateSet !== "function") throw fail("RL_INVALID_REQUEST", "recovery requires the canonical complete-set reader and validator");
    validateDigest(expectedRecoveryIdentity, "expected recovery identity");
    paths = transactionPaths(root, changeId);
    ensurePrivateDirectory(paths.directory, { create: false });
    const loaded = loadRecovery(root, paths);
    candidate = { changeId, priorLifecycleRevision: loaded.recovery.prior_lifecycle_revision };
    if (loaded.identity !== expectedRecoveryIdentity) throw fail("RL_RECOVERY_REQUIRED", "recovery identity is stale");
    const observedBeforeRecovery = observedRecoveryState(root, loaded.recovery);
    if (existsSync(paths.lock)) {
      const lockStatus = lstatSync(paths.lock);
      if (lockStatus.isSymbolicLink() || !lockStatus.isFile() || (lockStatus.mode & 0o077) !== 0) throw fail("RL_RECOVERY_REQUIRED", "recovery lock is unsafe");
      let live = false;
      let lockRecord = null;
      try { lockRecord = JSON.parse(readFileSync(paths.lock, "utf8")); live = processIsLive(lockRecord.pid); } catch {}
      if (live) throw fail("RL_OPERATION_BUSY", "a live compact writer owns the recovery lock");
      if (!lockRecord || lockRecord.change_id !== changeId || lockRecord.transaction_id !== loaded.recovery.transaction_id) throw fail("RL_RECOVERY_REQUIRED", "recovery lock does not match its transaction");
      unlinkSync(paths.lock);
    }
    acquireLock(paths, changeId, loaded.recovery.transaction_id);
    recoveryLockAcquired = true;
    if (action === "restore-prior") {
      const alreadyPrior = loaded.recovery.affected_files.every((item) => stateMatches(observedBeforeRecovery[item.path], item.prior_identity));
      if (loaded.recovery.phase === "prepared" && alreadyPrior) {
        if (validateCandidateSet(readCompleteSet({ root, changeId }), loaded.recovery.prior_lifecycle_revision) !== true) throw fail("RL_RECOVERY_REQUIRED", "prior set failed complete-set validation");
        cleanup(paths);
        return result(candidate, "success", { affectedPaths: [], bytesChanged: false, resultingRevision: loaded.recovery.prior_lifecycle_revision });
      }
      restorePrior(root, paths, loaded.recovery);
      if (validateCandidateSet(readCompleteSet({ root, changeId }), loaded.recovery.prior_lifecycle_revision) !== true) throw fail("RL_RECOVERY_REQUIRED", "restored prior set failed complete-set validation");
      cleanup(paths);
      return result(candidate, "success", { affectedPaths: loaded.recovery.affected_files.map((item) => item.path), bytesChanged: true, resultingRevision: loaded.recovery.prior_lifecycle_revision });
    }
    if (loaded.recovery.phase !== "persisted") throw fail("RL_RECOVERY_REQUIRED", "candidate acceptance requires a persisted recovery phase");
    const observed = Object.fromEntries(loaded.recovery.affected_files.map((item) => [item.path, currentBytes(root, item.path)]));
    if (!loaded.recovery.affected_files.every((item) => stateMatches(observed[item.path], item.candidate_identity)) || validateCandidateSet(readCompleteSet({ root, changeId }), loaded.recovery.candidate_lifecycle_revision) !== true) throw fail("RL_RECOVERY_REQUIRED", "candidate set is incomplete or invalid");
    cleanup(paths);
    return result(candidate, "success", { affectedPaths: loaded.recovery.affected_files.map((item) => item.path), bytesChanged: false, resultingRevision: loaded.recovery.candidate_lifecycle_revision });
  } catch (error) {
    if (recoveryLockAcquired && paths && existsSync(paths.lock)) {
      try { unlinkSync(paths.lock); syncDirectory(paths.directory); } catch {}
    }
    const status = error.code === "RL_OPERATION_BUSY" ? "busy" : "recovery-required";
    return result(candidate, status, { error });
  }
}
