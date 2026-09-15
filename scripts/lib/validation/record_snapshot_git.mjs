// Exact local snapshot reads must not redirect, replace objects, fetch or write traces.
import {devNull} from 'node:os';
import {realpathSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
export function snapshotGitEnvironment() {
  return {
    PATH: process.env.PATH ?? '', LANG: 'C', LC_ALL: 'C',
    GIT_CONFIG_NOSYSTEM: '1', GIT_CONFIG_GLOBAL: devNull,
    GIT_NO_REPLACE_OBJECTS: '1', GIT_NO_LAZY_FETCH: '1',
    GIT_ALLOW_PROTOCOL: '', GIT_OPTIONAL_LOCKS: '0', GIT_TERMINAL_PROMPT: '0',
  };
}

export function assertSnapshotRoot(root) {
  const actual = execFileSync('git', ['-C', root, 'rev-parse', '--show-toplevel'], {
    env: snapshotGitEnvironment(), maxBuffer: 1024 * 1024, timeout: 10000,
    stdio: ['ignore', 'pipe', 'pipe'],
  }).toString().trim();
  if (realpathSync(actual) !== realpathSync(root)) throw new Error('snapshot root mismatch');
}
