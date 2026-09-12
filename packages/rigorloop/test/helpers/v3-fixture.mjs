import {readFileSync,readdirSync} from 'node:fs';
export const changeId='example-change';
export const prefix=`docs/changes/${changeId}/`;
export const manifest=prefix+'change.json';
export const encode=x=>JSON.stringify(x)+'\n';
export function fixture() {
 const dir=new URL('../../../../docs/design/cli/examples/records/v3-complete-store/',import.meta.url);
 return Object.fromEntries(readdirSync(dir,{recursive:true}).filter(p=>p.endsWith('.json')).map(p=>[prefix+p,readFileSync(new URL(p,dir),'utf8')]));
}
