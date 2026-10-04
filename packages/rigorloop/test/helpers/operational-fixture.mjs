import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync,writeFileSync,rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { randomUUID } from 'node:crypto';
import { fileURLToPath } from 'node:url';
export const cli = process.env.RIGORLOOP_TEST_PACKAGED_BIN ?? fileURLToPath(new URL('../../dist/bin/rigorloop.js', import.meta.url));
export const actor = { id: 'engineer-a', role: 'implement' };
export function project(t) {
  const root = mkdtempSync(join(tmpdir(), 'rigorloop-operational-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  writeFileSync(join(root, '.rigorloop.json'), JSON.stringify({ schema_version: 1, project_id: randomUUID() }));
  return root;
}
export function createInput(overrides = {}) {
  return structuredClone({
    schema_version: 2, interface: 'targeted-recording-v2', contract: 'rigorloop-records-v4',
    change_id: 'navigation', expected_revision: null, reads: [],
    input: {
      intent: { goal: 'Repair navigation', scope: 'View selection', exclusions: ['External publication'] },
      request: { locator: 'local:request-1', content: 'Correct the selected view.', captured_by: actor },
      authority: { source: 'Explicit project-owner request', allowed: ['Implement and check navigation'], limits: ['No publication'], reported_by: actor },
      activity: { stage: 'implement', status: 'in-progress', owner: actor, reason: 'Authorized navigation work' },
      next_action: { action: 'Inspect navigation behavior', owner: actor, rationale: 'Identify the affected view mapping.' },
    }, ...overrides,
  });
}
export function invoke(root, words, input, extra = []) {
  const args = [...words, '--root', root, '--change', 'navigation', '--format', 'json', ...extra];
  if (input !== undefined) args.push('--input', '-');
  const p = spawnSync(process.execPath, [cli, ...args], { input: input === undefined ? undefined : typeof input === 'string' ? input : JSON.stringify(input), encoding: 'utf8', timeout: 10000 });
  assert.ifError(p.error);
  assert.ok(p.stdout.trim(), p.stderr);
  return { exit: p.status, result: JSON.parse(p.stdout), stderr: p.stderr };
}
export const databasePath = root => join(root, '.rigorloop/rigorloop.db');
