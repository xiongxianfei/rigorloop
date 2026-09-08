import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync, readdirSync, symlinkSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
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
  replaceManagedAuthoring({ ...f, verifyInstalled: () => {
    assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "original lock\n");
    for (const root of f.roots) assert.equal(readFileSync(join(f.projectRoot, root, "design.md"), "utf8"), "new author\n");
    verified = true;
  }});
  assert.ok(verified);
  assert.equal(readFileSync(join(f.projectRoot, "rigorloop.lock"), "utf8"), "new lock\n");
  assert.equal(readFileSync(join(f.projectRoot, "unrelated.txt"), "utf8"), "neighbor\n");
  assert.ok(!readdirSync(f.projectRoot).some(p => p.startsWith(".rigorloop-authoring-")));
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
  assert.equal(readFileSync(join(failure.recoveryPath, "old", "0", "spec.md"), "utf8"), "original skill\n");
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
  assert.equal(readFileSync(join(failure.recoveryPath, "old", "0", "spec.md"), "utf8"), "original skill\n");
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
