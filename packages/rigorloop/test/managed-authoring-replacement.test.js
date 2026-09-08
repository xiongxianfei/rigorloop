import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, symlinkSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import fs from "node:fs";
import { syncBuiltinESMExports } from "node:module";
import { captureManagedBasis, replaceManagedAuthoring } from "../dist/lib/managed-authoring-replacement.js";

function fixture(t) {
  const projectRoot = mkdtempSync(join(tmpdir(), "authoring-replacement-"));
  t.after(() => rmSync(projectRoot, { recursive: true, force: true }));
  const roots = [".opencode/skills", ".opencode/commands"];
  for (const root of roots) mkdirSync(join(projectRoot, root), { recursive: true });
  writeFileSync(join(projectRoot, roots[0], "spec.md"), "original skill\n");
  writeFileSync(join(projectRoot, roots[1], "spec.md"), "original command\n");
  writeFileSync(join(projectRoot, "rigorloop.lock"), "original lock\n");
  writeFileSync(join(projectRoot, "rigorloop.yaml"), "original manifest\n");
  writeFileSync(join(projectRoot, "unrelated.txt"), "neighbor\n");
  const basis = captureManagedBasis({ projectRoot, roots });
  return { projectRoot, roots, basis,
    files: roots.map(root => ({ path: `${root}/design.md`, content: Buffer.from("new author\n") })),
    state: { "rigorloop.yaml": Buffer.from("new manifest\n"), "rigorloop.lock": Buffer.from("new lock\n") },
  };
}

test("authorized replacement publishes both roots and state, preserving neighbors", t => {
  const f = fixture(t);
  let verified = false;
  const result = replaceManagedAuthoring({ ...f, verifyInstalled: () => {
    assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "original lock\n");
    for (const root of f.roots) assert.equal(readFileSync(join(f.projectRoot, root, "design.md"), "utf8"), "new author\n");
    verified = true;
  }});
  assert.ok(verified);
  assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "new lock\n");
  assert.equal(readFileSync(join(f.projectRoot, "unrelated.txt"), "utf8"), "neighbor\n");
  assert.equal(readFileSync(join(result.retainedPaths.find(p => p.path === f.roots[0] && p.kind === "old").backup, "spec.md"), "utf8"), "original skill\n");
});

for (const point of ["staged", "saved:.opencode/skills", "published:.opencode/skills", "saved:.opencode/commands", "published:.opencode/commands", "verified", "saved:rigorloop.yaml", "published:rigorloop.yaml", "saved:rigorloop.lock", "published:rigorloop.lock"]) {
  test(`caught failure at ${point} restores exact original basis`, t => {
    const f = fixture(t);
    assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (phase === point) throw new Error("injected failure");
    }}), /injected failure/);
    assert.deepEqual(captureManagedBasis(f), f.basis);
    replaceManagedAuthoring(f);
    assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "new lock\n");
  });
}

test("installed verification failure restores roots before state publication", t => {
  const f = fixture(t);
  assert.throws(() => replaceManagedAuthoring({ ...f, verifyInstalled: () => { throw new Error("bad installed tree"); } }), /bad installed tree/);
  assert.deepEqual(captureManagedBasis(f), f.basis);
});

test("changed original basis blocks without replacement", t => {
  const f = fixture(t);
  writeFileSync(join(f.projectRoot, f.roots[0], "spec.md"), "local edit");
  assert.throws(() => replaceManagedAuthoring(f), { code: "managed-authoring-conflict" });
  assert.equal(readFileSync(join(f.projectRoot, f.roots[0], "spec.md"), "utf8"), "local edit");
  assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "original lock\n");
});

test("intervening shared-state writer survives conflict and rollback", t => {
  const f = fixture(t);
  let failure;
  try {
    replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (phase === "published:.opencode/skills") writeFileSync(join(f.projectRoot, "rigorloop.lock"), "independent writer\n");
    }});
  } catch (error) { failure = error; }
  assert.equal(failure.code, "managed-authoring-recovery-required");
  assert.ok(existsSync(failure.recoveryPath));
  assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "independent writer\n");
  assert.equal(readFileSync(join(failure.retainedPaths.find(p => p.path === f.roots[0] && p.kind === "old").backup, "spec.md"), "utf8"), "original skill\n");
});

test("rollback failure retains recoverable prior bytes and reports partial state", t => {
  const f = fixture(t);
  let failure;
  try {
    replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (phase === "published:.opencode/skills") throw new Error("publish failure");
      if (phase === "rollback") throw new Error("restore failure");
    }});
  } catch (error) { failure = error; }
  assert.equal(failure.code, "managed-authoring-recovery-required");
  assert.equal(readFileSync(join(failure.retainedPaths.find(p => p.path === f.roots[0] && p.kind === "old").backup, "spec.md"), "utf8"), "original skill\n");
});

test("original absent manifest is restored as absent after failed publication", t => {
  const f = fixture(t);
  rmSync(join(f.projectRoot, "rigorloop.yaml"));
  f.basis = captureManagedBasis(f);
  assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: p => {
    if (p === "published:rigorloop.yaml") throw new Error("stop");
  }}), /stop/);
  assert.deepEqual(captureManagedBasis(f), f.basis);
});

for (const location of [".opencode", ".opencode/skills", ".opencode/skills/link", "rigorloop.lock"]) {
  test(`unsafe symlink at ${location} blocks without following it`, t => {
    const f = fixture(t);
    const dest = join(f.projectRoot, location);
    rmSync(dest, { recursive: true, force: true });
    symlinkSync(join(f.projectRoot, "unrelated.txt"), dest);
    assert.throws(() => replaceManagedAuthoring(f));
    assert.equal(readFileSync(join(f.projectRoot, "unrelated.txt"), "utf8"), "neighbor\n");
  });
}

test("invalid or overlapping scope and escaped candidate paths fail closed", t => {
  const f = fixture(t);
  for (const roots of [["."], ["../outside"], [".opencode", ".opencode/skills"], ["rigorloop.lock"]]) {
    assert.throws(() => captureManagedBasis({ ...f, roots }));
  }
  for (const path of ["unrelated.txt", "../escape", ".opencode/skills/../escape"]) {
    assert.throws(() => replaceManagedAuthoring({ ...f, files: [{ path, content: Buffer.from("bad") }] }));
    assert.deepEqual(captureManagedBasis(f), f.basis);
  }
  assert.throws(() => replaceManagedAuthoring({ ...f, state: { ...f.state, unknown_value: Buffer.from("bad") } }));
});

function interleave(methods, inject, run) {
  const originals = Object.fromEntries(methods.map(name => [name, fs[name]]));
  try {
    for (const name of methods) fs[name] = (...args) => {
      inject(name, args, originals);
      return originals[name](...args);
    };
    syncBuiltinESMExports();
    run();
  } finally {
    Object.assign(fs, originals);
    syncBuiltinESMExports();
  }
}

for (const restoring of [false, true]) {
  test(`a writer after the final check cannot be overwritten during ${restoring ? "rollback" : "publication"}`, t => {
    const f = fixture(t);
    const target = join(f.projectRoot, "rigorloop.lock");
    let injected = false;
    interleave(["renameSync", "linkSync"], (_name, [from, to]) => {
      if (!injected && resolve(to) === target && String(from).includes(restoring ? ".rigorloop-authoring-old-" : "/new/")) {
        injected = true;
        writeFileSync(target, "independent after-check write\n");
      }
    }, () => {
      assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
        if (restoring && phase === "published:rigorloop.lock") throw new Error("force rollback");
      }}), { code: "managed-authoring-recovery-required" });
    });
    assert.ok(injected);
    assert.equal(readFileSync(target, "utf8"), "independent after-check write\n");
  });
}

test("a directory created after the final check is not replaced even when empty", t => {
  const f = fixture(t);
  const target = join(f.projectRoot, f.roots[0]);
  let injected = false;
  interleave(["renameSync", "mkdirSync"], (name, args, originals) => {
    if (!injected && resolve(name === "renameSync" ? args[1] : args[0]) === target) {
      injected = true;
      originals.mkdirSync(target, { mode: 0o700 });
    }
  }, () => assert.throws(() => replaceManagedAuthoring(f), { code: "managed-authoring-recovery-required" }));
  assert.ok(injected);
  assert.equal(fs.statSync(target).mode & 0o777, 0o700);
});

test("a late writer through an already open original descriptor keeps its bytes", t => {
  const f = fixture(t);
  const fd = fs.openSync(join(f.projectRoot, "rigorloop.lock"), "w");
  fs.writeSync(fd, "original lock\n");
  f.basis = captureManagedBasis(f);
  try {
    const result = replaceManagedAuthoring(f);
    fs.writeSync(fd, "late independent write\n");
    assert.match(readFileSync(result.retainedPaths.find(p => p.path === "rigorloop.lock" && p.kind === "old").backup, "utf8"), /late independent write/);
    assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "new lock\n");
  } finally { fs.closeSync(fd); }
});

for (const restoring of [false, true]) {
  test(`ancestor substitution cannot redirect ${restoring ? "rollback" : "publication"}`, t => {
    const f = fixture(t);
    const root = join(f.projectRoot, f.roots[0]);
    const neighbor = join(f.projectRoot, "neighbor");
    mkdirSync(neighbor, { mode: 0o700 });
    writeFileSync(join(neighbor, "unrelated.txt"), "keep");
    let injected = false;
    interleave(["linkSync"], (_name, [from, to]) => {
      if (!injected && resolve(to) === join(root, restoring ? "spec.md" : "design.md") && String(from).includes(restoring ? ".rigorloop-authoring-old-" : "/new/")) {
        injected = true;
        fs.renameSync(root, `${root}-detached-by-writer`);
        symlinkSync(neighbor, root);
      }
    }, () => assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (restoring && phase === "published:.opencode/skills") throw new Error("force restoration");
    }}), { code: "managed-authoring-recovery-required" }));
    assert.ok(injected);
    assert.deepEqual(fs.readdirSync(neighbor), ["unrelated.txt"]);
    assert.equal(fs.statSync(neighbor).mode & 0o777, 0o700);
    assert.equal(readFileSync(join(neighbor, "unrelated.txt"), "utf8"), "keep");
  });
}

test("a substituted directory is never opened for chmod", t => {
  const f = fixture(t);
  const root = join(f.projectRoot, f.roots[0]);
  const neighbor = join(f.projectRoot, "neighbor");
  mkdirSync(neighbor, { mode: 0o700 });
  let injected = false;
  interleave(["openSync"], (_name, [path]) => {
    if (!injected && resolve(path) === root) {
      injected = true;
      fs.rmdirSync(root);
      symlinkSync(neighbor, root);
    }
  }, () => { try { replaceManagedAuthoring(f); } catch (error) { assert.equal(error.code, "managed-authoring-recovery-required"); } });
  assert.equal(fs.statSync(neighbor).mode & 0o777, 0o700);
});

test("rollback restores directory modes and the caller's restrictive umask", t => {
  const f = fixture(t);
  fs.chmodSync(join(f.projectRoot, f.roots[0]), 0o775);
  f.basis = captureManagedBasis(f);
  const previous = process.umask(0o077);
  try {
    assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (phase === "published:rigorloop.lock") throw new Error("mode restoration");
    }}), /mode restoration/);
    assert.deepEqual(captureManagedBasis(f), f.basis);
    assert.equal(process.umask(), 0o077);
  } finally { process.umask(previous); }
});

for (const symlink of [false, true]) {
  test(`project root substitution (${symlink ? "symlink" : "directory"}) cannot redirect publication`, t => {
    const f = fixture(t);
    const original = `${f.projectRoot}-original`;
    const neighbor = `${f.projectRoot}-neighbor`;
    t.after(() => { rmSync(original, { recursive: true, force: true }); rmSync(neighbor, { recursive: true, force: true }); });
    assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (phase === "staged") {
        fs.cpSync(f.projectRoot, neighbor, { recursive: true });
        fs.renameSync(f.projectRoot, original);
        if (symlink) symlinkSync(neighbor, f.projectRoot);
        else fs.renameSync(neighbor, f.projectRoot);
      }
    }}), { code: "managed-authoring-recovery-required" });
    assert.equal(readFileSync(join(f.projectRoot, f.roots[0], "spec.md"), "utf8"), "original skill\n");
    assert.equal(existsSync(join(f.projectRoot, f.roots[0], "design.md")), false);
    assert.equal(readFileSync(join(original, "rigorloop.lock"), "utf8"), "original lock\n");
  });
}

for (const restoring of [false, true]) {
  test(`root substitution during ${restoring ? "rollback detachment" : "backup"} preserves unrelated destination bytes`, t => {
    const f = fixture(t);
    const original = `${f.projectRoot}-original`;
    const neighbor = `${f.projectRoot}-neighbor`;
    t.after(() => { rmSync(original, { recursive: true, force: true }); rmSync(neighbor, { recursive: true, force: true }); });
    let injected = false;
    let unrelated;
    interleave(["renameSync"], (_name, [from, to], originals) => {
      const wanted = restoring ? (String(to).includes("detached-") || String(to).includes("rollback-")) : (String(to).includes("/old/3") || String(to).includes("authoring-old-"));
      if (!injected && from === "rigorloop.lock" && wanted) {
        injected = true;
        const priorCwd = process.cwd();
        const destination = resolve(to);
        fs.cpSync(f.projectRoot, neighbor, { recursive: true });
        originals.renameSync(f.projectRoot, original);
        symlinkSync(neighbor, f.projectRoot);
        unrelated = destination.replace(f.projectRoot, neighbor);
        mkdirSync(resolve(unrelated, ".."), { recursive: true });
        writeFileSync(unrelated, "independent unrelated bytes");
        assert.equal(priorCwd, f.projectRoot);
      }
    }, () => assert.throws(() => replaceManagedAuthoring({ ...f, checkpoint: phase => {
      if (restoring && phase === "published:rigorloop.lock") throw new Error("force rollback detachment");
    }}), { code: "managed-authoring-recovery-required" }));
    assert.ok(injected);
    assert.equal(readFileSync(unrelated, "utf8"), "independent unrelated bytes");
  });
}
