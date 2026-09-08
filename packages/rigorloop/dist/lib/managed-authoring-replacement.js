// Private filesystem transaction for the explicitly authorized authoring upgrade.
// Archive trust and recorded-tree eligibility remain the installer's responsibility.
import { lstatSync, readdirSync, readFileSync, mkdirSync, mkdtempSync, writeFileSync, renameSync, rmSync, realpathSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve, join, dirname } from "node:path";

const STATE_PATHS = ["rigorloop.yaml", "rigorloop.lock"];
const failure = (message, code = "managed-authoring-conflict") => Object.assign(new Error(message), { code });
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);

function stat(path) {
  try { return lstatSync(path); } catch (error) { if (error.code === "ENOENT") return null; throw error; }
}

function relativePath(path) {
  if (typeof path !== "string" || !path || path.includes("\\") || path.includes("\0") || path.split("/").some(p => !p || p === "." || p === "..")) {
    throw failure("Unsafe managed replacement path.");
  }
  return path;
}

function safePath(projectRoot, path) {
  relativePath(path);
  let current = projectRoot;
  const pieces = path.split("/");
  for (let i = 0; i < pieces.length; i++) {
    current = join(current, pieces[i]);
    const info = stat(current);
    if (info?.isSymbolicLink() || (info && i < pieces.length - 1 && !info.isDirectory())) {
      throw failure("Managed replacement refuses symlinks or unsafe ancestors.");
    }
  }
  return current;
}

function snapshot(path) {
  const info = stat(path);
  if (!info) return null;
  if (info.isDirectory()) return { kind: "directory", mode: info.mode, entries: readdirSync(path).sort().map(name => [name, snapshot(join(path, name))]) };
  if (info.isFile()) return { kind: "file", mode: info.mode, hash: createHash("sha256").update(readFileSync(path)).digest("hex") };
  throw failure("Managed replacement requires regular files and directories.");
}

function scope(projectRoot, roots) {
  projectRoot = resolve(projectRoot);
  if (realpathSync(projectRoot) !== projectRoot || !lstatSync(projectRoot).isDirectory()) throw failure("Unsafe project root.");
  if (!Array.isArray(roots) || !roots.length) throw failure("Missing selected roots.");
  const paths = [...roots, ...STATE_PATHS];
  for (const path of paths) relativePath(path);
  if (paths.some((a, i) => paths.some((b, j) => i !== j && (a === b || a.startsWith(`${b}/`))))) throw failure("Overlapping replacement scope.");
  return { projectRoot, paths };
}

export function captureManagedBasis({ projectRoot, roots }) {
  const selected = scope(projectRoot, roots);
  const basis = Object.fromEntries(selected.paths.map(path => [path, snapshot(safePath(selected.projectRoot, path))]));
  if (roots.some(path => basis[path]?.kind !== "directory")) throw failure("A recorded managed root is missing or unsafe.");
  if (STATE_PATHS.some(path => basis[path] && basis[path].kind !== "file")) throw failure("Unsafe managed state file.");
  return basis;
}

export function replaceManagedAuthoring({ projectRoot, roots, basis, files, state, verifyInstalled = () => {}, checkpoint = () => {} }) {
  const selected = scope(projectRoot, roots);
  projectRoot = selected.projectRoot;
  if (!equal(Object.keys(basis ?? {}).sort(), [...selected.paths].sort()) || !equal(captureManagedBasis({ projectRoot, roots }), basis)) {
    throw failure("The original managed installation basis changed before replacement.");
  }
  if (!state || !equal(Object.keys(state).sort(), [...STATE_PATHS].sort()) || STATE_PATHS.some(p => !Buffer.isBuffer(state[p]))) {
    throw failure("Replacement requires exactly the two verified state-file byte values.");
  }
  if (!Array.isArray(files) || !files.length) throw failure("Missing verified candidate files.");
  const seen = new Set();
  for (const file of files) {
    relativePath(file.path);
    if (!Buffer.isBuffer(file.content) || seen.has(file.path) || !roots.some(root => file.path.startsWith(`${root}/`))) {
      throw failure("Candidate file is duplicate, unsafe or outside the selected roots.");
    }
    seen.add(file.path);
  }

  const stage = mkdtempSync(join(projectRoot, ".rigorloop-authoring-"));
  const expected = { ...basis };
  const saved = new Map();
  const moves = [];
  function assertCurrent() {
    for (const path of selected.paths) {
      if (!equal(snapshot(safePath(projectRoot, path)), expected[path])) throw failure("An independent write changed the replacement basis.");
    }
    for (const [backup, original] of saved) {
      if (!equal(snapshot(backup), original)) throw failure("The retained original changed during replacement.");
    }
  }
  function move(from, to, path, after, backupChange) {
    assertCurrent();
    if (stat(to)) throw failure("A replacement destination unexpectedly exists.");
    renameSync(from, to);
    moves.push({ from, to, path, before: expected[path], backupChange });
    expected[path] = after;
    if (backupChange) saved.set(to, basis[path]);
  }
  try {
    mkdirSync(join(stage, "new"));
    mkdirSync(join(stage, "old"));
    for (const root of roots) mkdirSync(join(stage, "new", root), { recursive: true });
    for (const { path, content } of files) {
      const destination = safePath(join(stage, "new"), path);
      mkdirSync(dirname(destination), { recursive: true });
      writeFileSync(destination, content, { flag: "wx" });
    }
    for (const path of STATE_PATHS) writeFileSync(join(stage, "new", path), state[path], { flag: "wx" });
    const candidate = Object.fromEntries(selected.paths.map(path => [path, snapshot(join(stage, "new", path))]));
    checkpoint("staged");
    assertCurrent();
    for (const [i, path] of selected.paths.entries()) {
      // Verify the installed roots before either shared state file is published.
      if (i === roots.length) { verifyInstalled(); checkpoint("verified"); assertCurrent(); }
      const target = safePath(projectRoot, path);
      if (expected[path]) {
        move(target, join(stage, "old", String(i)), path, null, true);
        checkpoint(`saved:${path}`);
      }
      const source = join(stage, "new", path);
      if (!equal(snapshot(source), candidate[path])) throw failure("Staged candidate changed before publication.");
      move(source, target, path, candidate[path], false);
      checkpoint(`published:${path}`);
    }
    assertCurrent();
  } catch (error) {
    try {
      assertCurrent();
      while (moves.length) {
        checkpoint("rollback");
        assertCurrent();
        const last = moves.at(-1);
        if (stat(last.from)) throw failure("Rollback destination changed independently.");
        renameSync(last.to, last.from);
        expected[last.path] = last.before;
        if (last.backupChange) saved.delete(last.to);
        moves.pop();
      }
      rmSync(stage, { recursive: true });
    } catch (recoveryError) {
      throw Object.assign(failure(`Replacement stopped; preserve the recovery directory and operator backup, inspect intervening changes, and restore a coherent original basis before retry. ${recoveryError.message}`, "managed-authoring-recovery-required"), { recoveryPath: stage, cause: error });
    }
    throw error;
  }
  // The target/state pair is coherent. A cleanup problem must not attempt to
  // roll it back through a possibly partially removed backup directory.
  try { rmSync(stage, { recursive: true }); } catch { return { cleanupPath: stage }; }
  return {};
}
