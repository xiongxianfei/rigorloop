// Repository consumers share the CLI's bounded archive/header discriminator.
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {RecordFiles,stop,MIB} from '../packages/rigorloop/dist/lib/record-store-files.js';
import {classifyRecordDirectory} from '../packages/rigorloop/dist/lib/record-discovery.js';
const [rootArg,id,revision,...extra]=process.argv.slice(2);
try{
 if(!rootArg||!id||extra.length)stop('invalid-input');
 const root=resolve(rootArg);let reader=new RecordFiles(root);
 if(revision){
  if(!/^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(revision))stop('invalid-input');
  const git=args=>execFileSync('git',['-C',root,...args],{maxBuffer:MIB+1,timeout:10000,stdio:['ignore','pipe','pipe']});
  if(git(['rev-parse','--verify',`${revision}^{commit}`]).toString().trim()!==revision)stop('invalid-input');
  const entry=path=>{
   reader.path(path);
   const raw=git(['ls-tree','-z',revision,'--',`:(literal)${path}`]).toString();
   if(!raw)return null;
   const match=/^(\d+) (blob|tree) ([a-f0-9]+)\t([^\0]+)\0$/.exec(raw);
   if(!match||match[4]!==path)stop('unsafe-path');
   return {mode:match[1],kind:match[2],object:match[3]};
  };
  const pathCheck=reader.path.bind(reader);
  reader={path:pathCheck,assert(){},inspect(path,directory=false){
   pathCheck(path);const parts=path.split('/');let e;
   for(let i=0;i<parts.length;i++){
    e=entry(parts.slice(0,i+1).join('/'));if(!e)return{info:null,chain:[]};
    if(i<parts.length-1||directory){if(e.mode!=='040000')stop('unsafe-path');}
    else if(!['100644','100755'].includes(e.mode))stop('unsafe-path');
   }
   return{info:e,chain:[],target:path};
  },read(path,limit=MIB){
   const {info}=this.inspect(path);if(!info)return null;
   const size=Number(git(['cat-file','-s',info.object]));if(size>limit)stop('limit-exceeded');
   return git(['cat-file','blob',info.object]);
  },*list(path){
   const {info}=this.inspect(path,true);if(!info)return;
   const raw=git(['ls-tree','-z',info.object]).toString();
   for(const line of raw.split('\0').filter(Boolean)){
    const match=/^(\d+) (?:blob|tree) [a-f0-9]+\t(.+)$/.exec(line);if(!match)stop('unsafe-path');
    yield {name:match[2],isSymbolicLink:()=>match[1]==='120000'};
   }
  }};
 }
 process.stdout.write(classifyRecordDirectory(reader,id)+'\n');
}catch(e){process.stderr.write((e.recordStoreCode??'io-failure')+'\n');process.exitCode=1;}
