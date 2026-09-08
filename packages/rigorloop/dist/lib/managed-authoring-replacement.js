// Private filesystem transaction for the explicitly authorized authoring upgrade.
// Archive trust and recorded-tree eligibility remain the installer's responsibility.
import { lstatSync, readdirSync, readFileSync, mkdirSync, mkdtempSync, writeFileSync, renameSync, linkSync, realpathSync } from "node:fs";
import { createHash, randomBytes } from "node:crypto";
import { resolve, join, dirname, basename } from "node:path";

const SETTLED = "Settled.\n";
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

function assertAuthority(projectRoot, authority) {
  if (realpathSync(projectRoot) !== projectRoot) throw failure("Project root is no longer safe.");
  for (const [path, dev, ino] of authority) {
    const info = stat(join(projectRoot, path));
    if (!info?.isDirectory() || info.isSymbolicLink() || info.dev !== dev || info.ino !== ino) {
      throw failure("The original project root or installation ancestor changed.");
    }
  }
}

function safePath(projectRoot, path, authority) {
  if (authority) assertAuthority(projectRoot, authority);
  else if (realpathSync(projectRoot) !== projectRoot || !lstatSync(projectRoot).isDirectory()) throw failure("Unsafe project root.");
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


// As in RecordFiles.withParent, the synchronous CLI pins the verified parent
// inode as cwd. Basename-only writes cannot follow a replaced ancestor.
function withParent(projectRoot, path, action, authority) {
  const target = safePath(projectRoot, path, authority);
  const parent = dirname(target);
  const identity = lstatSync(parent);
  if (!identity.isDirectory()) throw failure("Unsafe replacement parent.");
  const cwd = process.cwd();
  try {
    process.chdir(parent);
    const opened = lstatSync(".");
    if (opened.dev !== identity.dev || opened.ino !== identity.ino) throw failure("Replacement parent changed.");
    safePath(projectRoot, path, authority);
    const current = lstatSync(parent);
    if (current.dev !== identity.dev || current.ino !== identity.ino) throw failure("Replacement parent changed.");
    return action(basename(target));
  } finally { process.chdir(cwd); }
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
  const parents = new Set(["."]);
  for (const root of roots) {
    let parent = dirname(root);
    while (parent !== ".") { parents.add(parent); parent = dirname(parent); }
  }
  const authority = [...parents].sort().map(path => {
    const info = lstatSync(path === "." ? selected.projectRoot : safePath(selected.projectRoot, path));
    return [path, info.dev, info.ino];
  });
  const basis = Object.fromEntries(selected.paths.map(path => [path, snapshot(safePath(selected.projectRoot, path))]));
  if (roots.some(path => basis[path]?.kind !== "directory")) throw failure("A recorded managed root is missing or unsafe.");
  if (STATE_PATHS.some(path => basis[path] && basis[path].kind !== "file")) throw failure("Unsafe managed state file.");
  return { $ancestors: authority, ...basis };
}

// Private recovery evidence survives process interruption. It is not project
// workflow state and cannot authorize accepting a partial installed tree.
export function inspectManagedAuthoringRecovery({ projectRoot, roots, shared = false }) {
  projectRoot = resolve(projectRoot);
  const pending = [];
  for (const name of readdirSync(projectRoot).filter(name => name.startsWith(".rigorloop-authoring-"))) {
    const directory = join(projectRoot, name);
    if (!stat(directory)?.isDirectory()) continue;
    const marker = join(directory, "recovery-basis.json");
    if (!stat(marker)) continue;
    try {
      if (!stat(marker).isFile()) throw failure("Unsafe recovery evidence.");
      const settlement = join(directory, "settled");
      if (stat(settlement)) {
        if (!stat(settlement).isFile() || readFileSync(settlement, "utf8") !== SETTLED) throw failure("Unknown or unsafe recovery settlement.");
        continue;
      }
      const record = JSON.parse(readFileSync(marker, "utf8"));
      if (!equal(Object.keys(record).sort(), ["candidate", "original", "roots"]) || !Array.isArray(record.roots) || !record.roots.length) throw failure("Unknown recovery evidence shape.");
      const selected = scope(projectRoot, record.roots);
      if (!shared && !record.roots.some(root => roots.includes(root))) continue;
      for (const basis of [record.original, record.candidate]) {
        if (!basis || !equal(Object.keys(basis).sort(), [...selected.paths].sort())) throw failure("Incomplete recovery basis.");
      }
      const actual = Object.fromEntries(selected.paths.map(path => [path, snapshot(safePath(projectRoot, path))]));
      const outcome = equal(actual, record.original) ? "original" : equal(actual, record.candidate) ? "candidate" : null;
      if (!outcome) throw failure("Interrupted replacement has a partial or independently changed target/state basis.");
      pending.push({ path: name, outcome, roots: record.roots });
    } catch (error) {
      return { pending, blocker: { code: "managed-authoring-recovery-required", path: name, message: error.message, next_action: "Preserve partial content and intervening changes. Restore a coherent original target/state pair from the separate operator backup, or have the installation owner reconcile independent shared-state changes. Do not delete the lockfile, recovery evidence or refresh hashes to accept a partial tree." } };
    }
  }
  return { pending };
}

export function settleManagedAuthoringRecovery({ projectRoot, roots, shared = false }) {
  const inspected = inspectManagedAuthoringRecovery({ projectRoot, roots, shared });
  if (inspected.blocker) throw failure(inspected.blocker.message, inspected.blocker.code);
  for (const entry of inspected.pending) {
    const authority = captureManagedBasis({ projectRoot, roots: entry.roots }).$ancestors;
    withParent(resolve(projectRoot), `${entry.path}/settled`, name => writeFileSync(name, SETTLED, { flag: "wx" }), authority);
  }
}

export function replaceManagedAuthoring({ projectRoot, roots, basis, files, state, verifyInstalled = () => {}, checkpoint = () => {} }) {
  const selected = scope(projectRoot, roots);
  projectRoot = selected.projectRoot;
  if (!equal(Object.keys(basis ?? {}).sort(), ["$ancestors", ...selected.paths].sort()) || !equal(captureManagedBasis({ projectRoot, roots }), basis)) {
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
  const retained = [];
  const authority = basis.$ancestors;
  function assertCurrent() {
    assertAuthority(projectRoot, authority);
    for (const path of selected.paths) {
      if (!equal(snapshot(safePath(projectRoot, path)), expected[path])) throw failure("An independent write changed the replacement basis.");
    }
    for (const [backup, original] of saved) {
      if (!equal(snapshot(backup), original)) throw failure("The retained original changed during replacement.");
    }
  }
  function detach(path, kind) {
    // Neither endpoint traverses a mutable ancestor. The private name is fresh,
    // unpredictable and not exposed before the move; retained copies are never
    // automatically deleted. No destination traverses the staging pathname.
    return withParent(projectRoot, path, name => {
      const privateName = `.rigorloop-authoring-${kind}-${randomBytes(32).toString("hex")}`;
      if (stat(privateName)) throw failure("Private detachment name collision.");
      renameSync(name, privateName);
      const backup = join(projectRoot, dirname(path), privateName);
      retained.push({ path, backup, kind });
      return backup;
    }, authority);
  }
  function saveOriginal(path) {
    assertCurrent();
    const backup = detach(path, "old");
    moves.push({ kind: "saved", backup, path });
    expected[path] = null;
    saved.set(backup, basis[path]);
    assertCurrent();
  }
  function publish(path, source, node, record = true) {
    function install(relative, from, value, attach) {
      assertCurrent();
      safePath(projectRoot, relative);
      if (value.kind === "file") {
        // link is an atomic no-clobber publication on the same filesystem.
        // rename would overwrite a writer arriving after the final check.
        withParent(projectRoot, relative, name => linkSync(from, name), authority);
        attach(value);
      } else {
        withParent(projectRoot, relative, name => {
          // Set the creation mode exactly; never reopen a public path to chmod.
          // This main-thread synchronous section restores process state on error.
          const mask = process.umask(0);
          try { mkdirSync(name, { mode: value.mode & 0o7777 }); }
          finally { process.umask(mask); }
        }, authority);
        const directory = { ...value, entries: [] };
        attach(directory);
        for (const [name, child] of value.entries) {
          install(`${relative}/${name}`, join(from, name), child, entry => {
            directory.entries.push([name, entry]);
            directory.entries.sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0);
          });
        }
      }
    }
    install(path, source, node, value => {
      expected[path] = value;
      if (record) moves.push({ kind: "published", path });
    });
    assertCurrent();
  }
  try {
    mkdirSync(join(stage, "new"));
    for (const root of roots) mkdirSync(join(stage, "new", root), { recursive: true });
    for (const { path, content } of files) {
      const destination = safePath(join(stage, "new"), path);
      mkdirSync(dirname(destination), { recursive: true });
      writeFileSync(destination, content, { flag: "wx" });
    }
    for (const path of STATE_PATHS) writeFileSync(join(stage, "new", path), state[path], { flag: "wx" });
    const candidate = Object.fromEntries(selected.paths.map(path => [path, snapshot(join(stage, "new", path))]));
    const original = Object.fromEntries(selected.paths.map(path => [path, basis[path]]));
    writeFileSync(join(stage, "recovery-basis.json"), JSON.stringify({ roots, original, candidate }), { flag: "wx" });
    checkpoint("staged");
    assertCurrent();
    for (const [i, path] of selected.paths.entries()) {
      // Verify the installed roots before either shared state file is published.
      if (i === roots.length) { verifyInstalled(); checkpoint("verified"); assertCurrent(); }
      if (expected[path]) {
        saveOriginal(path);
        checkpoint(`saved:${path}`);
      }
      const source = join(stage, "new", path);
      if (!equal(snapshot(source), candidate[path])) throw failure("Staged candidate changed before publication.");
      publish(path, source, candidate[path]);
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
        if (last.kind === "published") {
          // Detach before inspecting; never recursively delete a public path.
          // If a writer won this source race, retain its bytes and report it.
          const wanted = expected[last.path];
          const detached = detach(last.path, "rollback");
          expected[last.path] = null;
          saved.set(detached, wanted);
          assertCurrent();
        } else {
          // Restoring originals uses the same exclusive publication primitives.
          publish(last.path, last.backup, basis[last.path], false);
        }
        moves.pop();
      }
      withParent(projectRoot, `${basename(stage)}/settled`, name => writeFileSync(name, SETTLED, { flag: "wx" }), authority);
      error.recoveryPath = stage;
      error.retainedPaths = retained;
      error.restored = true;
    } catch (recoveryError) {
      throw Object.assign(failure(`Replacement stopped; preserve the recovery directory and operator backup, inspect intervening changes, and restore a coherent original basis before retry. ${recoveryError.message}`, "managed-authoring-recovery-required"), { recoveryPath: stage, retainedPaths: retained, cause: error });
    }
    throw error;
  }
  // Keep the detached originals outside the selected installation roots. An
  // already-open writer can still write an old inode after its last check;
  // deleting that backup automatically could lose the independent write.
  // The operator may remove this directory after inspecting the completed pair.
  withParent(projectRoot, `${basename(stage)}/settled`, name => writeFileSync(name, SETTLED, { flag: "wx" }), authority);
  return { backupPath: stage, retainedPaths: retained };
}
