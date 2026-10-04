// Faults alter real inputs or fail real cleanup after the relevant boundary.
import fs from 'node:fs';
import {DatabaseSync} from 'node:sqlite';
import {syncBuiltinESMExports} from 'node:module';
const point=process.env.RIGORLOOP_TEST_MAINTENANCE_FAULT;
const prepare=DatabaseSync.prototype.prepare,rename=fs.renameSync,unlink=fs.unlinkSync;
let triggered=false,activated=false;
DatabaseSync.prototype.prepare=function(sql,...args){
  if(point==='recapture'&&!triggered&&sql==='SELECT change_id FROM changes ORDER BY change_id'){
    triggered=true;
    const path=process.env.RIGORLOOP_TEST_BACKUP_MEMBER;
    fs.writeFileSync(path,Buffer.alloc(fs.readFileSync(path).length,88));
  }
  return prepare.call(this,sql,...args);
};
fs.renameSync=function(from,to){
  const result=rename.apply(this,arguments);
  if(String(to).endsWith('/manifest.json')&&JSON.parse(fs.readFileSync(to,'utf8')).phase==='activated')activated=true;
  return result;
};
fs.unlinkSync=function(path){
  if(point==='legacy-cleanup'&&activated&&String(path)==='lock'&&process.cwd().includes('/record-store/'))throw Object.assign(new Error('Injected source cleanup failure'),{code:'EACCES'});
  return unlink.apply(this,arguments);
};
syncBuiltinESMExports();
