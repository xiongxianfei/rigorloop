// Local process identity is deliberately separate from PID and elapsed age.
import { readFileSync, readdirSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { fail, parseInput } from './operational-contract.js';
import { directory, regular, stat, durableWrite, syncDirectory } from './operational-files.js';

export function processIdentity(pid = process.pid) {
  if (process.platform !== 'linux') fail('unsupported-runtime', 'Maintenance process exclusion is currently qualified on Linux only.');
  const boot = readFileSync('/proc/sys/kernel/random/boot_id', 'utf8').trim();
  const fields = readFileSync(`/proc/${pid}/stat`, 'utf8').split(') ').slice(1).join(') ').split(' ');
  return { boot, start: fields[19] };
}
export function ownerAbsent(owner) {
  if (!owner || !Number.isSafeInteger(owner.pid) || owner.pid < 1 || typeof owner.boot !== 'string' || typeof owner.start !== 'string') return false;
  try {
    const current = processIdentity(owner.pid);
    // A different process incarnation proves the original owner no longer exists.
    return current.boot !== owner.boot || current.start !== owner.start;
  } catch (error) {
    if (error.code !== 'ENOENT') return false;
    try { process.kill(owner.pid, 0); return false; } catch (probe) { return probe.code === 'ESRCH'; }
  }
}
export function owner() { return { pid: process.pid, ...processIdentity() }; }

export async function fence(info, task, operationId = randomUUID()) {
  const runtime = directory(join(info.root, '.rigorloop'), true);
  const maintenance = directory(join(runtime, 'maintenance'), true);
  const access = directory(join(runtime, 'access'), true);
  const path = join(maintenance, 'active.json');
  const value = { operation_id: operationId, project_id: info.id, task, owner: owner() };
  try { durableWrite(path, JSON.stringify(value)); syncDirectory(maintenance); }
  catch (error) { if (error.code === 'EEXIST') fail('store-busy', 'An explicit maintenance operation already owns the fence.'); throw error; }
  const release = () => {
    regular(path);
    if (readFileSync(path, 'utf8') !== JSON.stringify(value)) fail('destination-conflict', 'Maintenance fence ownership changed.');
    unlinkSync(path); syncDirectory(maintenance);
  };
  try {
    const deadline = Date.now() + 5000;
    for (;;) {
      let active = false;
      for (const name of readdirSync(access)) {
        if (!/^[a-f0-9-]{36}\.json$/.test(name)) fail('store-unavailable', 'Unrecognized admission lease; ownership is uncertain.');
        const leasePath = join(access, name); if (!stat(leasePath)) continue;
        regular(leasePath); const bytes = readFileSync(leasePath), lease = parseInput(bytes);
        if (lease.project_id !== info.id) fail('project-mismatch', 'Admission lease belongs to another project.');
        if (ownerAbsent(lease.owner)) {
          if (stat(leasePath) && readFileSync(leasePath).equals(bytes)) { unlinkSync(leasePath); syncDirectory(access); }
        } else active = true;
      }
      if (!active) return { runtime, maintenance, path, value, release };
      if (Date.now() >= deadline) fail('store-busy', 'Admitted operations have not left the store; no replacement was attempted.');
      await new Promise(resolve => setTimeout(resolve, 50));
    }
  } catch (error) { release(); throw error; }
}
