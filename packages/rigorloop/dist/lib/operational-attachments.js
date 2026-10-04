import { openSync,closeSync,readSync,writeSync,fsyncSync,fstatSync,linkSync,unlinkSync,rmSync } from 'node:fs';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { fail } from './operational-contract.js';
import { directory,contained,regular,stat,syncDirectory } from './operational-files.js';
const MAX_BYTES=64*1024*1024;
const sameFile=(a,b)=>a&&b&&['dev','ino','size','mtimeMs','ctimeMs'].every(k=>a[k]===b[k]);
function sameBytes(first,second) {
  if(regular(first).size!==regular(second).size)return false;
  const left=openSync(first,'r'),right=openSync(second,'r');
  try {
    const a=Buffer.alloc(65536),b=Buffer.alloc(65536);
    for(;;) {
      const n=readSync(left,a,0,a.length,null),m=readSync(right,b,0,b.length,null);
      if(n!==m||!a.subarray(0,n).equals(b.subarray(0,m)))return false;
      if(!n)return true;
    }
  } finally {closeSync(left);closeSync(right);}
}
export function attachmentPath(root,changeId,name,{create=false}={}) {
  let path=join(root,'.rigorloop');
  for(const component of ['artifacts','changes',changeId])path=directory(join(path,component),create);
  return join(path,name);
}
export function captureAttachments(root,change,values,preview) {
  const selections=values.flatMap(e=>e.retain??[]);
  if(selections.length>64)fail('size-limit','Task exceeds 64 new attachments.');
  if(new Set(selections.map(s=>s.name)).size!==selections.length)fail('invalid-request','Duplicate attachment name.');
  if(selections.some(s=>change.attachments.some(a=>a.name===s.name)))fail('invalid-request','Existing retained attachment names cannot be overwritten; select the existing name or a new name.');
  let total=0,staging=null;const files=[],metadata=[],published=[];
  const dispose=()=>{if(staging)rmSync(staging,{recursive:true,force:true});};
  try {
    if(!preview&&selections.length) {
      const artifacts=directory(join(root,'.rigorloop/artifacts'),true);
      const parent=directory(join(artifacts,'.staging'),true);
      staging=directory(join(parent,randomUUID()),true);
    }
    for(const selection of selections) {
      const source=contained(root,selection.source),before=regular(source);
      if(before.size+total>MAX_BYTES)fail('size-limit','Task exceeds 64 MiB of new attachment bytes.');
      const input=openSync(source,'r'),stage=staging?join(staging,selection.name):null;
      let output=null,size=0;
      try {
        if(!sameFile(before,fstatSync(input)))fail('source-conflict','Attachment source changed before capture.');
        if(stage)output=openSync(stage,'wx',0o600);
        const bytes=Buffer.alloc(65536);let n;
        while((n=readSync(input,bytes,0,bytes.length,null))>0) {
          total+=n;size+=n;
          if(total>MAX_BYTES)fail('size-limit','Task exceeds 64 MiB of new attachment bytes.');
          if(output!==null){let offset=0;while(offset<n)offset+=writeSync(output,bytes,offset,n-offset);}
        }
        if(!sameFile(before,fstatSync(input))||!sameFile(before,stat(source)))fail('source-conflict','Attachment source changed during capture.');
        if(output!==null)fsyncSync(output);
      } finally {closeSync(input);if(output!==null)closeSync(output);}
      metadata.push({name:selection.name,media_type:selection.media_type,byte_count:size});
      if(stage)files.push({stage,name:selection.name});
    }
    return {
      metadata,dispose,published,
      publish() {
        for(const file of files) {
          const destination=attachmentPath(root,change.change_id,file.name,{create:true});
          if(regular(destination,true)) {
            if(!sameBytes(file.stage,destination))fail('destination-conflict','An unused attachment already has different bytes.');
          } else {
            try{linkSync(file.stage,destination);}catch(error){if(error.code==='EEXIST')fail('destination-conflict','Attachment destination changed.');throw error;}
            published.push(file.name);syncDirectory(join(destination,'..'));
          }
        }
      },
    };
  } catch(error){dispose();throw error;}
}
export function removeUnusedAttachments(root,changeId,names) {
  for(const name of names) {
    let path;
    try{path=attachmentPath(root,changeId,name);}catch(error){if(error.operationalCode==='invalid-request')continue;throw error;}
    if(regular(path,true)){unlinkSync(path);syncDirectory(join(path,'..'));}
  }
}
