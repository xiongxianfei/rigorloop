// Test-only binding fault at the real commit boundary. No public task hook.
import { DatabaseSync } from 'node:sqlite';
const execute=DatabaseSync.prototype.exec;
DatabaseSync.prototype.exec=function(sql) {
  if(sql==='COMMIT') {
    if(process.env.RIGORLOOP_TEST_COMMIT_FAULT==='after')execute.call(this,sql);
    throw new Error('test-only private binding failure');
  }
  return execute.call(this,sql);
};
