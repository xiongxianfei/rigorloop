import {fixture} from './helpers/v3-fixture.mjs';
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {parseV3Record, validateV3Record, validateV3Set, validateV3Preservation, validateV3Creation} from '../dist/lib/record-format-v3.js';
import {requestFormat, V3_FORMAT} from '../dist/lib/record-store-format.js';
const read=p=>JSON.parse(readFileSync(new URL(`../../../docs/design/record-format/examples/${p}`,import.meta.url),'utf8'));
const encode=x=>JSON.stringify(x)+'\n';
const prefix='docs/changes/example-change/';
const edit=(files,path,fn)=>{const value=JSON.parse(files[prefix+path]);fn(value);files[prefix+path]=encode(value);};
const fail=fn=>assert.throws(fn,e=>['invalid-input','unsupported-contract','broken-reference'].includes(e.recordStoreCode));
test('TG-01 complete v3 store and standalone design examples conform without narrative conversion',()=>{
 assert.equal(validateV3Set('example-change',fixture()).size,5);
 for(const path of ['v3-review-limitations-update/before.json','v3-review-limitations-update/after.json','v3-finding-correction/stored-review.json','v3-finding-correction/updated-review.json'])validateV3Record('review',read(path));
 for(const path of ['v3-verify-without-evidence/verify-report.json','v3-verify-limitations-update/before.json'])validateV3Record('verify',read(path));
});
test('TG-01 explanation collections allow repeated reasons and preserve multiline bytes',()=>{
 const r=read('v3-review-limitations-update/before.json');r.rationale.push(r.rationale[0]);r.limitations=[];
 assert.deepEqual(parseV3Record('review',encode(r)),r);
 for(const field of ['summary','assessment_scope']) {const b=structuredClone(r);b[field]=' \n\t';fail(()=>validateV3Record('review',b));}
 for(const bad of [[],[''],[' \n'],null]) {const b=structuredClone(r);b.rationale=bad;fail(()=>validateV3Record('review',b));}
});
test('TG-01 unknown_value closed fields kinds enums and dual explanation reject',()=>{
 const r=read('v3-review-limitations-update/before.json');
 for(const field of ['body','sections','unknown_value'])fail(()=>validateV3Record('review',{...r,[field]:'unexpected'}));
 fail(()=>validateV3Record('unknown_value',r));fail(()=>validateV3Record('review',{...r,judgment:'unknown_value'}));
 for(const field of ['reporter','owner']){const b=structuredClone(r);b.findings[0][field].role='unknown_value';fail(()=>validateV3Record('review',b));}
 const b=structuredClone(r);b.findings[0].state='unknown_value';fail(()=>validateV3Record('review',b));
});
test('TG-01 optional conditional basis is closed and complete when present',()=>{
 const v=read('v3-verify-limitations-update/before.json');validateV3Record('verify',v);const absent=structuredClone(v);delete absent.verification_basis;validateV3Record('verify',absent);
 for(const bad of [null,{}, {...v.verification_basis,unknown_value:'x'},{...v.verification_basis,head_branch:' '}])fail(()=>validateV3Record('verify',{...v,verification_basis:bad}));
 fail(()=>validateV3Record('verify',{...v,changes:[]}));fail(()=>validateV3Record('verify',{...v,outcome:'failed'}));
});
test('TG-02 v3 finding current fields can change while identity and blockers retain their own invariants',()=>{
 const before=fixture();const finding=read('v3-finding-correction/stored-review.json').findings[0];
 edit(before,'reviews/final-code-review.json',r=>r.findings=[finding]);
 const after=structuredClone(before);edit(after,'reviews/final-code-review.json',r=>{r.findings[0].evidence='Corrected evidence';r.findings[0].reporter.id='correct-reporter';r.findings[0].subjects=[];r.findings[0].state='resolved';r.findings[0].resolution={actor:{id:'reviewer-a',role:'review'},rationale:'Withdraw mistaken report',evidence_refs:[]};});
 validateV3Preservation('example-change',before,after);
 for(const fn of [r=>r.findings=[],r=>r.findings[0].id='renamed',r=>r.findings[0].origin={},r=>r.findings[0].state='open']){const bad=structuredClone(after);edit(bad,'reviews/final-code-review.json',fn);fail(()=>validateV3Preservation('example-change',before,bad));}
 const stored=JSON.parse(readFileSync(new URL('../../../tests/fixtures/rigorloop-records-v3/records.json',import.meta.url))).change;
 const blocker=stored.blockers[0];assert.ok(blocker?.origin);edit(before,'change.json',r=>r.blockers=[blocker]);
 const bad=structuredClone(before);edit(bad,'change.json',r=>r.blockers[0].origin.rationale='rewrite');fail(()=>validateV3Preservation('example-change',before,bad));
});
test('TG-02 mixed versions and broken typed references reject reject',()=>{
 const files=fixture();edit(files,'evidence.json',r=>r.schema_version=2);fail(()=>validateV3Set('example-change',files));
 const bad=fixture();edit(bad,'verify-report.json',r=>r.evidence_refs=[{path:prefix+'reviews/final-code-review.json',id:'final-code-review'}]);fail(()=>validateV3Set('example-change',bad));
});
test('TG-02 advanced request schema remains 2 while v3 stored schema is 3',()=>{
 const files=fixture(),request={schema_version:2,contract:'rigorloop-records-v3',change_id:'example-change',expected_revision:null,writes:Object.entries(files).map(([path,content])=>({path,content,expected_identity:null})),reads:[]};
 assert.equal(requestFormat(request),V3_FORMAT);validateV3Record('request',request);validateV3Creation(request,false);
 fail(()=>validateV3Record('request',{...request,schema_version:3}));fail(()=>requestFormat({...request,contract:'unknown_value'}));fail(()=>validateV3Creation(request,true));
});
