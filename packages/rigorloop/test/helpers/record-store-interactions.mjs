import {executeRecordStore} from '../../dist/lib/record-store.js';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {spawnSync,execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {digest} from '../../dist/lib/record-store-files.js';
import {canonicalJSON} from '../../dist/lib/recording-observations.js';
const project=fileURLToPath(new URL('../../../../',import.meta.url));
const cli=fileURLToPath(new URL('../../dist/bin/rigorloop.js',import.meta.url));
const fixture=JSON.parse(readFileSync(new URL('../../../../tests/fixtures/rigorloop-records-v2/records.json',import.meta.url)));
const prefix='docs/changes/example/',mp=prefix+'change.json',rp=prefix+'reviews/design-review.json',ep=prefix+'evidence.json',vp=prefix+'verify-report.json';
export const SCENARIOS=['finding-with-neighbors','failed-verify-correction','applicability-reassessment','final-explanation-read'];
const encode=value=>JSON.stringify(value)+'\n';
const actor={id:'reviewer',role:'review'},app={value:'current',actor,reason:'Explicit benchmark declaration'};
const basisPath='docs/design/subject.md';
const engineeringBasis='Recorder requirement: a targeted edit preserves unrelated findings and their original judgment. A failed Verify check remains recordable after completion. Review approval does not close a Verify-owned blocker. The observer must report stale subjects without changing the recorded historical assessment. The test procedure compares the untouched entries and exact subject identities before and after the update.\n';
function setup(){const root=mkdtempSync(join(tmpdir(),'recording-interactions-'));mkdirSync(join(root,'docs/changes'),{recursive:true});mkdirSync(join(root,dirname(basisPath)),{recursive:true});writeFileSync(join(root,basisPath),engineeringBasis);const f=structuredClone(fixture),subject={path:basisPath,identity:digest(engineeringBasis)};function subjects(x){if(!x||typeof x!=='object')return;if(Object.hasOwn(x,'path')&&Object.hasOwn(x,'identity')){Object.assign(x,subject);return;}for(const v of Object.values(x))subjects(v);}for(const k of ['change','review','evidence','decisions','verify'])subjects(f[k]);f.review.findings=Array.from({length:24},(_,i)=>({...structuredClone(f.review.findings[0]),id:`neighbor-${i}`,evidence:`Observed case ${i}: ${engineeringBasis}`,required_outcome:`Preserve case ${i}'s stated invariant.`,origin:{...structuredClone(f.review.findings[0].origin),rationale:`Original case ${i}: ${engineeringBasis}`}}));f.change.blockers=[];f.decisions.decisions[0].source_refs=[{path:rp,id:'neighbor-0'}];f.evidence.checks=Array.from({length:12},(_,i)=>({...structuredClone(f.evidence.checks[0]),id:i?'check-'+(i+1):'check-1',result:'passed',summary:`Check ${i}: ${engineeringBasis}`}));const records={[mp]:f.change,[rp]:f.review,[ep]:f.evidence,[prefix+'material-decisions.json']:f.decisions,[vp]:f.verify};const writes=Object.entries(records).map(([path,value])=>({path,expected_identity:null,content:encode(value)}));const p=executeRecordStore({root,changeId:'example',operation:'record',request:{schema_version:2,contract:'rigorloop-records-v2',change_id:'example',expected_revision:null,reads:[],writes}});if(p.status!=='saved')throw Error(JSON.stringify(p));return{root,subject,records};}
const own=(object,keys)=>Object.fromEntries(keys.map(k=>[k,structuredClone(object[k])]));
function decisions(scenario,records,subject){const finding={reporter:actor,owner:{id:'implementer',role:'implement'},subjects:[subject],evidence:'Observed preservation defect in the selected engineering basis.',required_outcome:'Demonstrate unchanged neighboring entries.',state:'open',resolution:null,basis:{rationale:'The failed preservation guarantee requires correction.',supporting_judgment:{from_review:'design-review',rationale:'The selected independent review supplies the original assessed subject.'}}};if(scenario==='finding-with-neighbors')return[{op:'finding.add',target:{review:'design-review',id:'new-finding'},values:finding}];if(scenario==='failed-verify-correction')return[{op:'evidence.record',target:{id:'final-failure'},values:{actor:{id:'verifier',role:'verify'},subjects:[subject],result:'failed',procedure:'Compare neighboring records against the preservation requirement.',summary:'A neighbor changed during the simulated failed check.'}},{op:'blocker.add',target:{id:'verify-defect'},values:{...finding,reporter:{id:'verifier',role:'verify'},basis:{rationale:findingsRationale(),supporting_judgment:null}}}];if(scenario==='applicability-reassessment')return[{op:'applicability.set',target:{path:rp},values:{value:'stale',actor,reason:'Explicitly withdraw reliance pending reassessment.'}},{op:'review.record',target:{id:'design-review'},values:{...own(records[rp],['target','reviewer','contributors','independence_basis','subjects','judgment','body']),judgment:'approved',body:'The selected current subjects were independently reassessed against the preservation requirement.'},applicability:{...app,value:'current',reason:'Explicit reassessment against the current subjects.'}}];return[];}
function findingsRationale(){return 'Verify observed the defect; correction remains required despite recorded completion.';}
function baselineCandidate(records,operations){const copy=structuredClone(records),touched=new Set();for(const op of operations){if(op.op==='finding.add'||op.op==='blocker.add'){const {basis,...values}=op.values;let supporting=basis.supporting_judgment;if(supporting?.from_review){const r=copy[rp];supporting={...own(r,['reviewer','contributors','independence_basis','subjects','judgment']),rationale:supporting.rationale};}const entry={id:op.target.id,...values,origin:{...own(values,['reporter','subjects','evidence','required_outcome']),rationale:basis.rationale,supporting_judgment:supporting}};const path=op.op==='finding.add'?rp:mp;copy[path][op.op==='finding.add'?'findings':'blockers'].push(entry);touched.add(path);}else if(op.op==='evidence.record'){copy[ep].checks.push({id:op.target.id,...op.values});touched.add(ep);}else if(op.op==='applicability.set'){Object.assign(copy[mp].applicability.find(a=>a.path===op.target.path),op.values);touched.add(mp);}else{Object.assign(copy[rp],op.values);Object.assign(copy[mp].applicability.find(a=>a.path===rp),op.applicability);touched.add(rp);touched.add(mp);}}return{copy,touched};}
export function runInteraction(scenario,mode,{guidance=true}={}){
 if(!SCENARIOS.includes(scenario)||!['targeted','advanced'].includes(mode))throw Error('Unknown benchmark selection');
 const state=setup(),{root,subject,records}=state,pieces=[],calls=[],checkpoints=[];
 const skill=scenario==='failed-verify-correction'?'verify':'design-review';
 const add=(category,text)=>pieces.push({category,text});
 if(guidance&&mode==='advanced')add('guidance','Controlled comparison amendment: select advanced rigorloop-records-v2 request schema 2 for these identical v2 fixtures, overriding the historical skill profile v1-only selector. This is comparative maintenance tooling, not a shipped v2 normal path. Preserve all supplied decisions and neighbors.');
 if(guidance){const path=`skills/${skill}/SKILL.md`;add('guidance',mode==='targeted'?readFileSync(join(project,path),'utf8'):execFileSync('git',['show',`bd1c4bd3:${path}`],{cwd:project,encoding:'utf8'}));}
 function call(words,payload,extra=[]){const args=[...words,'--root',root,'--change','example',...(payload?['--input','-']:[]),'--format','json',...extra];if(words[0]==='subject'){const i=args.indexOf('--change');args.splice(i,2);}add('command',args.map(x=>x===root?'ROOT':x).join(' '));if(payload)add('request',encode(payload));const r=spawnSync(process.execPath,[cli,...args],{input:payload?encode(payload):undefined,encoding:'utf8',maxBuffer:16*1024*1024});calls.push(words.slice(0,2).filter(w=>!w.startsWith('--')).join('.'));add('response',r.stdout+r.stderr);if(r.status)throw Error(r.stdout+r.stderr);return JSON.parse(r.stdout);}
 try{
  const operations=decisions(scenario,records,subject);let snapshot;
  if(mode==='advanced')snapshot=call(['record-store','inspect']);else snapshot=call(['context'],{schema_version:1,select:scenario==='final-explanation-read'?[{kind:'verify',where:{}}]:[{kind:'review',where:{ids:['design-review']}},{kind:'activity',where:{}},...(scenario==='applicability-reassessment'?[{kind:'applicability',where:{paths:[rp]}}]:[])]});
  if(scenario==='final-explanation-read'){
   const report=mode==='advanced'?JSON.parse(snapshot.snapshot.records.find(r=>r.path===vp).content):snapshot.data.items[0].fields;
   return{scenario,mode,pieces,calls,semantic:report,basis:report.subjects};
  }
  if(mode==='targeted')call(['subject','inspect','--path',basisPath,'--content','full']);
  else{ // The full-record path needs the same engineering bytes and their hash.
   const script="const fs=require('node:fs'),crypto=require('node:crypto');const bytes=fs.readFileSync(process.argv[1]);process.stdout.write(JSON.stringify({content:bytes.toString('utf8'),identity:'sha256:'+crypto.createHash('sha256').update(bytes).digest('hex')})+'\\n');";
   add('command',`node -e ${script} ${basisPath}`);add('response',execFileSync(process.execPath,['-e',script,basisPath],{cwd:root,encoding:'utf8'}));calls.push('subject.read-and-hash');
  }
  const groups=scenario==='applicability-reassessment'?operations.map(op=>[op]):[operations];
  let currentRecords=records;
  for(const operations of groups){
  if(mode==='advanced'){
   const {copy,touched}=baselineCandidate(currentRecords,operations),request={schema_version:2,contract:'rigorloop-records-v2',change_id:'example',expected_revision:snapshot.revision,reads:[{path:subject.path,expected_identity:subject.identity}],writes:[...touched].map(path=>({path,expected_identity:snapshot.files.find(f=>f.path===path).identity,content:encode(copy[path])}))};
   if(scenario==='finding-with-neighbors')call(['record-store','check'],request);
   call(['record-store','record'],request);snapshot=call(['record-store','inspect']);
  }else{
   for(const op of operations){const words=op.op.split('.');const help=spawnSync(process.execPath,[cli,...words,'--help'],{encoding:'utf8'});if(help.status)throw Error(help.stderr);add('command',words.join(' ')+' --help');add('guidance',help.stdout);calls.push(words.join('.')+'.help');}
   const batch=operations.length>1,op=operations[0],words=batch?['batch']:[...op.op.split('.'),...(op.target.id?[op.target.id]:[]),...(op.target.review?['--review',op.target.review]:[])];const request={schema_version:1,interface:'targeted-recording-v1',contract:snapshot.record_contract,change_id:'example',expected_revision:snapshot.revision,reads:[subject],[batch?'operations':'operation']:batch?operations:op};
   if(scenario==='finding-with-neighbors')call(words,request,['--dry-run']);
   call(words,request);snapshot=call(['context'],{schema_version:1,select:operations.flatMap(op=>[{kind:op.op.split('.')[0],where:op.target.path?{paths:[op.target.path]}:{ids:[op.target.id],...(op.target.review?{review_ids:[op.target.review]}:{})}},...(op.applicability?[{kind:'applicability',where:{paths:[rp]}}]:[])])});
  }
  currentRecords=Object.fromEntries(Object.keys(records).map(path=>[path,JSON.parse(readFileSync(join(root,path),'utf8'))]));
  checkpoints.push(currentRecords);
  }
  const semantic=Object.fromEntries(Object.keys(records).map(path=>[path,JSON.parse(readFileSync(join(root,path),'utf8'))]));
  return{scenario,mode,pieces,calls,semantic,checkpoints,basis:[subject]};
 }finally{rmSync(root,{recursive:true,force:true});}
}
if(process.argv.includes('--measure')){
 const python=process.env.RIGORLOOP_TOKENIZER_PYTHON;if(!python)throw Error('Set RIGORLOOP_TOKENIZER_PYTHON to a Python with tiktoken==0.12.0');
 const runs=SCENARIOS.flatMap(s=>['advanced','targeted'].map(m=>runInteraction(s,m)));
 for(let i=0;i<runs.length;i+=2)if(canonicalJSON([runs[i].semantic,runs[i].checkpoints])!==canonicalJSON([runs[i+1].semantic,runs[i+1].checkpoints]))throw Error('Non-equivalent final semantics');
 const count=spawnSync(python,[fileURLToPath(new URL('./record-store-tokenize.py',import.meta.url))],{input:JSON.stringify(runs.map(r=>r.pieces)),encoding:'utf8',maxBuffer:16*1024*1024});if(count.status)throw Error(count.stderr);const totals=JSON.parse(count.stdout);
 process.stdout.write(encode({schema_version:1,tokenizer:totals.tokenizer,node:process.version,baseline:'bd1c4bd3',results:runs.map((r,i)=>({scenario:r.scenario,interface:r.mode,calls:r.calls.length,call_sequence:r.calls,...totals.runs[i]}))}));
}
