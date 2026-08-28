import {
  closeSync, constants, existsSync, fsyncSync, fstatSync, ftruncateSync, lstatSync, mkdirSync,
  openSync, readFileSync, renameSync, unlinkSync, writeSync,
} from "node:fs";
import { performance } from "node:perf_hooks";
import { join, parse, relative, resolve, sep } from "node:path";

export const LOG_NAMES = Object.freeze(["rigorloop.jsonl", "rigorloop.1.jsonl", "rigorloop.2.jsonl", "rigorloop.3.jsonl", "rigorloop.4.jsonl"]);
export const MAX_LOG_BYTES = 5 * 1024 * 1024;
const LOCK = ".rigorloop-log.lock";
const NOFOLLOW = constants.O_NOFOLLOW ?? 0;
const PATH_IO = Object.freeze({ lstatSync });

function unsafe(message = "Unsafe log path.") { return Object.assign(new Error(message), { code: "RL_LOG_UNSAFE_PATH" }); }
function unavailable() { return Object.assign(new Error("Diagnostic append unavailable."), { code: "RL_LOG_UNAVAILABLE" }); }

function lstatIfExists(path, io = PATH_IO) {
  try { return io.lstatSync(path); }
  catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

function checkExistingComponents(target, io = PATH_IO) {
  const absolute = resolve(target);
  const root = parse(absolute).root;
  let cursor = root;
  for (const part of absolute.slice(root.length).split(sep).filter(Boolean)) {
    cursor = join(cursor, part);
    const info = lstatIfExists(cursor, io);
    if (!info) break;
    if (info.isSymbolicLink() || !info.isDirectory()) throw unsafe();
  }
}

export function ensureSafeLogRoot(directory, options = {}) {
  if (typeof directory !== "string" || !directory || resolve(directory) !== directory) throw unsafe("Log directory must be absolute.");
  checkExistingComponents(directory);
  if (!existsSync(directory)) mkdirSync(directory, { recursive: true, mode: 0o700 });
  return validateExistingLogRoot(directory, options);
}

export function validateExistingLogRoot(directory, options = {}, io = PATH_IO) {
  if (typeof directory !== "string" || !directory || resolve(directory) !== directory) throw unsafe("Log directory must be absolute.");
  checkExistingComponents(directory, io);
  const rootStat = lstatIfExists(directory, io);
  if (!rootStat) return null;
  if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) throw unsafe();
  if (options.platform !== "win32" && process.platform !== "win32" && (rootStat.mode & 0o077) !== 0) throw unsafe("Log directory permissions are too broad.");
  for (const name of [...LOG_NAMES, LOCK]) {
    const path = join(directory, name);
    if (relative(directory, path).startsWith("..")) throw unsafe();
    const info = lstatIfExists(path, io);
    if (info) {
      if (!info.isFile() || info.isSymbolicLink()) throw unsafe();
      if (process.platform !== "win32" && (info.mode & 0o077) !== 0) throw unsafe("Log file permissions are too broad.");
    }
  }
  return directory;
}

function sameFile(left, right) {
  return left.dev === right.dev && left.ino === right.ino;
}

function closeOwned(fd, expected, io) {
  try {
    io.closeSync(fd);
    return;
  } catch (initialError) {
    let current;
    try { current = fstatSync(fd); }
    catch (inspectionError) {
      if (inspectionError.code === "EBADF") throw initialError;
      throw unavailable();
    }
    if (expected && !sameFile(current, expected)) throw unavailable();
    try { closeSync(fd); }
    catch { throw unavailable(); }
    throw initialError;
  }
}

function acquire(directory, options, io) {
  const lock = join(directory, LOCK);
  const clock = options.lockClock ?? (() => performance.now());
  const wait = options.lockWait ?? ((milliseconds) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, milliseconds));
  const started = clock();
  for (let attempt = 0; attempt < 10; attempt += 1) {
    if (clock() - started > 1000) break;
    let fd = null;
    let identity = null;
    try {
      fd = io.openSync(lock, constants.O_RDWR | constants.O_CREAT | constants.O_EXCL | NOFOLLOW, 0o600);
      identity = fstatSync(fd);
      const inspected = io.fstatSync(fd);
      if (!inspected.isFile() || !sameFile(identity, inspected)) throw unavailable();
      return { fd, lock, identity };
    } catch (error) {
      if (fd !== null) {
        try {
          if (identity) closeOwned(fd, identity, io);
          else closeSync(fd);
        } catch { /* the stale lock remains fail-closed */ }
        throw unavailable();
      }
      if (error.code !== "EEXIST") throw error.code === "ELOOP" ? unsafe() : unavailable();
      if (attempt === 9 || options.wait === false) continue;
      const remaining = 1000 - (clock() - started);
      if (remaining <= 0) break;
      wait(Math.min(100, remaining));
    }
  }
  throw Object.assign(new Error("Log lock unavailable."), { code: "RL_LOG_UNAVAILABLE" });
}

function openOwned(path, io) {
  const before = io.lstatSync(path);
  if (!before.isFile() || before.isSymbolicLink()) throw unsafe();
  let fd = null;
  try {
    fd = io.openSync(path, constants.O_RDONLY | NOFOLLOW);
    const opened = io.fstatSync(fd);
    if (!opened.isFile() || !sameFile(before, opened)) throw unsafe();
    return { fd, identity: opened };
  } catch (error) {
    if (fd !== null) {
      try { closeOwned(fd, before, io); }
      catch { throw unavailable(); }
    }
    throw error;
  }
}

function readOwned(path, io) {
  const held = openOwned(path, io);
  try { return io.readFileSync(held.fd); }
  finally { closeOwned(held.fd, held.identity, io); }
}

function assertUnchangedOwned(path, expected, io) {
  const current = io.lstatSync(path);
  if (!current.isFile() || current.isSymbolicLink() || !sameFile(current, expected)) throw unsafe();
}

function validateMutation(directory, source, expectedSource, destination, options, io) {
  const ownedNames = new Set([...LOG_NAMES, LOCK]);
  if (!ownedNames.has(relative(directory, source))) throw unsafe();
  if (destination && !ownedNames.has(relative(directory, destination))) throw unsafe();
  if (!validateExistingLogRoot(directory, options, io)) throw unsafe();
  assertUnchangedOwned(source, expectedSource, io);
}

function rotate(directory, options, io) {
  const oldest = join(directory, LOG_NAMES[4]);
  if (existsSync(oldest)) {
    const held = openOwned(oldest, io);
    closeOwned(held.fd, held.identity, io);
    validateMutation(directory, oldest, held.identity, null, options, io);
    io.unlinkSync(oldest);
  }
  for (let index = 3; index >= 1; index -= 1) {
    const source = join(directory, LOG_NAMES[index]);
    if (!existsSync(source)) continue;
    const held = openOwned(source, io);
    closeOwned(held.fd, held.identity, io);
    const destination = join(directory, LOG_NAMES[index + 1]);
    validateMutation(directory, source, held.identity, destination, options, io);
    io.renameSync(source, destination);
  }
  const active = join(directory, LOG_NAMES[0]);
  if (existsSync(active)) {
    const held = openOwned(active, io);
    closeOwned(held.fd, held.identity, io);
    const destination = join(directory, LOG_NAMES[1]);
    validateMutation(directory, active, held.identity, destination, options, io);
    io.renameSync(active, destination);
  }
}

export function appendDiagnosticEvent(directory, encoded, options = {}) {
  const io = {
    closeSync, fsyncSync, fstatSync, ftruncateSync, lstatSync, openSync, readFileSync,
    renameSync, unlinkSync, writeSync, ...options.fs,
  };
  ensureSafeLogRoot(directory, options);
  const held = acquire(directory, options, io);
  let outcomeError = null;
  try {
    ensureSafeLogRoot(directory, options);
    const active = join(directory, LOG_NAMES[0]);
    const prior = existsSync(active) ? readOwned(active, io) : Buffer.alloc(0);
    const incoming = Buffer.from(encoded, "utf8");
    const mustRotate = prior.length + incoming.length > MAX_LOG_BYTES;
    const candidate = mustRotate ? incoming : Buffer.concat([prior, incoming]);
    const written = io.writeSync(held.fd, candidate, 0, candidate.length, 0);
    if (written !== candidate.length) throw unavailable();
    io.fsyncSync(held.fd);
    if (mustRotate) rotate(directory, options, io);
    else if (existsSync(active)) {
      const current = openOwned(active, io);
      closeOwned(current.fd, current.identity, io);
      assertUnchangedOwned(active, current.identity, io);
    }
    validateMutation(directory, held.lock, held.identity, active, options, io);
    io.renameSync(held.lock, active);
  } catch (error) {
    outcomeError = error.code === "RL_LOG_UNSAFE_PATH" ? error : unavailable();
  } finally {
    try { closeOwned(held.fd, held.identity, io); }
    catch { outcomeError ??= unavailable(); }
  }
  if (outcomeError) throw outcomeError;
}

export function readRetainedLogs(directory) {
  if (!validateExistingLogRoot(directory)) return [];
  const io = { closeSync, fstatSync, lstatSync, openSync, readFileSync };
  return LOG_NAMES.filter((name) => existsSync(join(directory, name))).map((name) => ({ name, content: readOwned(join(directory, name), io).toString("utf8") }));
}
