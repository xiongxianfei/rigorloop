import assert from 'node:assert/strict';
import {writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {actor,project,createInput,invoke} from './operational-fixture.mjs';
export const reviewer={id:'reviewer-b',role:'review'};
export const envelope=(revision,input)=>({...createInput(),expected_revision:revision,input});
export const observation={method:'reported',actor:reviewer,scope:'Assessed candidate',summary:'Reviewer reports the assessment applies to this scope'};
export function fixture(t) {
  const root=project(t);writeFileSync(join(root,'implementation.txt'),'implementation candidate');
  const created=invoke(root,['change','create'],createInput());assert.equal(created.exit,0,JSON.stringify(created));
  return {root,revision:created.result.revision};
}
export const prepare=(scope='formal')=>({purpose:'code',scope,selection:[{path:'implementation.txt',state:'present'}],basis_refs:[],plan_path:null,coverage_rationale:'Complete delivered implementation',description:'Whole implementation',actor});
export const assessment=(subjects,judgment='approved')=>({reviewer,contributors:[actor],independence_basis:'Reviewer did not author implementation',judgment,assessed_subjects:subjects,governing_basis:[],summary:'Reviewed delivered scope',rationale:['The implementation satisfies the selected scope'],limitations:[],evidence_refs:[],support:[]});
export const applicability={value:'current',actor:reviewer,rationale:'No intervening material changes reported',observation};

export function deliveryFixture(t) {
  const state=fixture(t),root=state.root;
  const send=(words,input)=>{
    const revision=invoke(root,['change','context'],{schema_version:2,interface:'targeted-recording-v2',contract:'rigorloop-records-v4',selectors:[{kind:'change',id:'navigation'}],include_observations:false}).result.revision;
    const result=invoke(root,words,envelope(revision,input));assert.equal(result.exit,0,JSON.stringify(result));return result;
  };
  const subjects=[];
  for(const [kind,file] of [['requirements','requirements.md'],['design','architecture.md']]) {
    writeFileSync(join(root,file),kind+' definition');
    const basis={id:kind,kind,decision:'proposed',selection:[{path:file,state:'present'}],actor,rationale:'Defines the accepted work scope',review:null};
    send(['change','update'],{basis});
    send(['review','prepare',kind],{...prepare(),purpose:kind,selection:basis.selection,basis_refs:[{kind:'basis',id:kind}]});
    const review=invoke(root,['review','show',kind]).result.items.find(i=>i.kind==='review').value;
    subjects.push(...review.prepared.subjects);
    send(['review','record',kind],{assessment:assessment(review.prepared.subjects),applicability});
    send(['change','update'],{basis:{...basis,decision:'accepted',review:{kind:'review',id:kind}}});
  }
  writeFileSync(join(root,'plan.md'),'Complete implementation and relevant checks; one whole-change review then Verify');
  send(['change','update'],{plan:'plan.md',work:[{id:'milestone',status:'completed',owner:actor,scope:'Complete navigation behavior',locations:['implementation.txt'],remaining:null,check_refs:[],blocker_ids:[],completion_reason:'Implementation and relevant checks completed'}]});
  for(const [purpose,file] of [['delivery','plan.md'],['code','implementation.txt']]) {
    send(['review','prepare',purpose],{...prepare(),purpose,selection:[{path:file,state:'present'}],plan_path:purpose==='delivery'?file:null,basis_refs:[{kind:'basis',id:'requirements'},{kind:'basis',id:'design'}]});
    const review=invoke(root,['review','show',purpose]).result.items.find(i=>i.kind==='review').value;
    send(['review','record',purpose],{assessment:{...assessment(review.prepared.subjects),governing_basis:subjects},applicability});
  }
  const verification={scope:'final',verifier:{id:'verifier-c',role:'verify'},subjects:[],governing_basis:subjects,review_refs:['requirements','design','delivery','code'].map(id=>({kind:'review',id})),evidence_refs:[],observation:{...observation,actor:{id:'verifier-c',role:'verify'}},outcome:'success',summary:'The completed scope meets its accepted basis',rationale:['Assessed current implementation, review conclusions and completion criteria'],limitations:[],support:[]};
  const closeout={actor:{id:'verifier-c',role:'verify'},verification:'final',summary:'Navigation delivered',reason:'Accepted scope is complete',delivered_scope:'Navigation behavior',governing_references:['requirements.md','architecture.md','plan.md'],limitations:['External publication was not performed'],retained_attachments:[]};
  return {root,send,verification,closeout};
}
