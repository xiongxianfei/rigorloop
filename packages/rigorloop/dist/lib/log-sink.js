import { appendFileSync, closeSync, existsSync, lstatSync, mkdirSync, openSync, readFileSync, renameSync, statSync, unlinkSync, writeFileSync } from "node:fs";
import { dirname, join, parse, relative, resolve, sep } from "node:path";

export const LOG_NAMES = Object.freeze(["rigorloop.jsonl", "rigorloop.1.jsonl", "rigorloop.2.jsonl", "rigorloop.3.jsonl", "rigorloop.4.jsonl"]);
export const MAX_LOG_BYTES = 5 * 1024 * 1024;
const LOCK = ".rigorloop-log.lock";

function unsafe(message = "Unsafe log path.") { return Object.assign(new Error(message), { code: "RL_LOG_UNSAFE_PATH" }); }

function checkExistingComponents(target) {
  const absolute = resolve(target);
  const root = parse(absolute).root;
  let cursor = root;
  for (const part of absolute.slice(root.length).split(sep).filter(Boolean)) {
    cursor = join(cursor, part);
    if (!existsSync(cursor)) break;
    if (lstatSync(cursor).isSymbolicLink()) throw unsafe();
  }
}

export function ensureSafeLogRoot(directory, options = {}) {
  if (!resolve(directory) || resolve(directory) !== directory) throw unsafe("Log directory must be absolute.");
  checkExistingComponents(directory);
  if (!existsSync(directory)) mkdirSync(directory, { recursive: true, mode: 0o700 });
  const rootStat = lstatSync(directory);
  if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) throw unsafe();
  if (options.platform !== "win32" && process.platform !== "win32" && (rootStat.mode & 0o077) !== 0) throw unsafe("Log directory permissions are too broad.");
  for (const name of [...LOG_NAMES, LOCK]) {
    const path = join(directory, name);
    if (relative(directory, path).startsWith("..")) throw unsafe();
    if (existsSync(path)) {
      const info = lstatSync(path);
      if (!info.isFile() || info.isSymbolicLink()) throw unsafe();
      if (process.platform !== "win32" && (info.mode & 0o077) !== 0) throw unsafe("Log file permissions are too broad.");
    }
  }
  return directory;
}

function acquire(directory, options = {}) {
  const lock = join(directory, LOCK);
  const started = Date.now();
  for (let attempt = 0; attempt < 10 && Date.now() - started <= 1000; attempt += 1) {
    try { return { fd: openSync(lock, "wx", 0o600), lock }; }
    catch (error) {
      if (error.code !== "EEXIST") throw error;
      if (options.wait !== false) Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, Math.min(100, 1000 - (Date.now() - started)));
    }
  }
  throw Object.assign(new Error("Log lock unavailable."), { code: "RL_LOG_UNAVAILABLE" });
}

function rotate(directory, incomingBytes) {
  const active = join(directory, LOG_NAMES[0]);
  if (!existsSync(active) || statSync(active).size + incomingBytes <= MAX_LOG_BYTES) return;
  const oldest = join(directory, LOG_NAMES[4]);
  if (existsSync(oldest)) unlinkSync(oldest);
  for (let index = 3; index >= 1; index -= 1) {
    const source = join(directory, LOG_NAMES[index]);
    if (existsSync(source)) renameSync(source, join(directory, LOG_NAMES[index + 1]));
  }
  renameSync(active, join(directory, LOG_NAMES[1]));
}

export function appendDiagnosticEvent(directory, encoded, options = {}) {
  ensureSafeLogRoot(directory, options);
  const held = acquire(directory, options);
  try {
    ensureSafeLogRoot(directory, options);
    rotate(directory, Buffer.byteLength(encoded));
    const active = join(directory, LOG_NAMES[0]);
    if (!existsSync(active)) writeFileSync(active, "", { mode: 0o600, flag: "wx" });
    appendFileSync(active, encoded, { encoding: "utf8", mode: 0o600 });
  } finally {
    closeSync(held.fd);
    unlinkSync(held.lock);
  }
}

export function readRetainedLogs(directory) {
  ensureSafeLogRoot(directory);
  return LOG_NAMES.filter((name) => existsSync(join(directory, name))).map((name) => ({ name, content: readFileSync(join(directory, name), "utf8") }));
}
