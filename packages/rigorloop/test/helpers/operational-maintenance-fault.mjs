// Faults alter real inputs or fail real cleanup after the relevant boundary.
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
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
  const statement=prepare.call(this,sql,...args);
  if(point==='preview-writer'&&!triggered&&sql==='SELECT kind,id FROM accounts WHERE change_id=? ORDER BY kind,id') {
    const all=statement.all.bind(statement);
    statement.all=(...parameters)=>{
      const result=all(...parameters);triggered=true;
      const child=spawnSync(process.execPath,[process.env.RIGORLOOP_TEST_CLI,'change','update','--root',process.env.RIGORLOOP_TEST_ROOT,'--change','navigation','--input','-','--format','json'],{encoding:'utf8',input:fs.readFileSync(process.env.RIGORLOOP_TEST_WRITER_INPUT),timeout:20000});
      fs.writeFileSync(process.env.RIGORLOOP_TEST_WRITER_RESULT,JSON.stringify({status:child.status,stdout:child.stdout}));
      if(child.status!==0)throw new Error('Concurrent writer failed: '+child.stdout);
      return result;
    };
  }
  return statement;
};
fs.renameSync=function(from,to){
  const result=rename.apply(this,arguments);
  if(String(to).endsWith('/manifest.json')&&JSON.parse(fs.readFileSync(to,'utf8')).phase==='activated'){activated=true;if(point==='activation-receipt')throw Object.assign(new Error('Injected activation durability failure'),{code:'EIO'});}
  return result;
};
fs.unlinkSync=function(path){
  if(point==='legacy-cleanup'&&activated&&String(path)==='lock'&&process.cwd().includes('/record-store/'))throw Object.assign(new Error('Injected source cleanup failure'),{code:'EACCES'});
  return unlink.apply(this,arguments);
};
syncBuiltinESMExports();
