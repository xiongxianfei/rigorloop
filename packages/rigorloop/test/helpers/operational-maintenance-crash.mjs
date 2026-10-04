// Test-only process interruption at the real filesystem publication boundary.
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
const rename=fs.renameSync;
fs.renameSync=function(from,to){
  const value=rename.apply(this,arguments);
  const point=process.env.RIGORLOOP_TEST_MAINTENANCE_CRASH;
  if(point==='rolled-back'&&String(to).endsWith('/manifest.json')&&JSON.parse(fs.readFileSync(to,'utf8')).rolled_back===true||point==='candidate'&&String(from).includes('/candidate/rigorloop.db')||point==='backup'&&String(from).includes('/.rigorloop-backup-')||point==='activated'&&String(to).endsWith('/manifest.json')&&JSON.parse(fs.readFileSync(to,'utf8')).phase==='activated')process.kill(process.pid,'SIGKILL');
  return value;
};
syncBuiltinESMExports();
