import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { digest } from "../dist/lib/record-store-files.js";
import { validateV2Record } from "../dist/lib/record-format-v2.js";

// These actors are scenario data, not proof of an actual independent review.
const author={id:"author",role:"design"}, reviewer={id:"reviewer",role:"review"}, verifier={id:"verifier",role:"verify"};
const encode=value=>JSON.stringify(value)+"\n";
const markdown=value=>encode({...value,body:'Fixture reasoning; actor labels alone do not establish independent review.\n'});

test("TG-05 actors explicitly invalidate, reopen, report Verify failure, rereview and complete",t=>{
  const root=mkdtempSync(join(tmpdir(),"rigorloop-workflow-"));
  t.after(()=>rmSync(root,{recursive:true,force:true}));
  for(const dir of ["docs/changes","docs/design/workflow","docs/design/cli","docs/proposals"])mkdirSync(join(root,dir),{recursive:true});
  const wf="docs/design/workflow/workflow.md", cli="docs/design/cli/cli.md", proposal="docs/proposals/example.md";
  for(const path of [wf,cli])writeFileSync(join(root,path),readFileSync(new URL(`../../../${path}`,import.meta.url)));
  writeFileSync(join(root,proposal),"Fixture direction\n");
  const subject=path=>({path,identity:digest(readFileSync(join(root,path)))});
  const manifest="docs/changes/example/change.json", reviewPath="docs/changes/example/reviews/design-review.json", evidencePath="docs/changes/example/evidence.json", verifyPath="docs/changes/example/verify-report.json";
  const fixture=JSON.parse(readFileSync(new URL("../../../tests/fixtures/rigorloop-records-v2/storage-safety.json",import.meta.url)));
  const change=JSON.parse(fixture.request.writes[0].content);
  Object.assign(change,{proposal:subject(proposal),models:[{id:"workflow",subject:subject(wf)},{id:"cli",subject:subject(cli)}],blockers:[]});
  change.activity={stage:"design",status:"completed",owner:author,reason:"Explicit prior completion"};
  change.work[0].status="completed";
  const launcher=process.env.RIGORLOOP_TEST_PACKAGED_BIN ?? fileURLToPath(new URL("../dist/bin/rigorloop.js",import.meta.url));
  function invoke(operation,input) {
    const result=spawnSync(process.execPath,[launcher,"record-store",operation,"--root",root,"--change","example","--format","json",...(input?["--input","-"]:[])],{input:input?encode(input):undefined,encoding:"utf8"});
    assert.equal(result.status,0,result.stdout+result.stderr);
    return JSON.parse(result.stdout);
  }
  function save(sidecars={}) {
    const before=invoke("inspect"), identities=new Map(before.files.map(f=>[f.path,f.identity]));
    const contents={[manifest]:encode(change),...sidecars};
    const request={schema_version:2,contract:"rigorloop-records-v2",change_id:"example",expected_revision:before.revision,
      writes:Object.entries(contents).map(([path,content])=>({path,content,expected_identity:identities.get(path)??null})),
      reads:[wf,cli].map(path=>({path,expected_identity:subject(path).identity}))};
    const result=invoke("record",request);
    assert.ok(["saved","unchanged"].includes(result.status));
    for(const [path,content] of Object.entries(contents))assert.equal(readFileSync(join(root,path),"utf8"),content);
    return invoke("inspect");
  }
  save();
  const review={...fixture.review,reviewer,contributors:[author],subjects:[subject(wf),subject(cli)],judgment:"approved",findings:[]};
  const evidence={...fixture.evidence,checks:[{...fixture.evidence.checks[0],subjects:[subject(wf),subject(cli)],result:"passed"}]};
  change.records=[{path:reviewPath,kind:"review"},{path:evidencePath,kind:"evidence"}];
  change.applicability=change.records.map(r=>({path:r.path,value:"current",actor:reviewer,reason:"Explicit fixture assessment"}));
  save({[reviewPath]:markdown(review),[evidencePath]:encode(evidence)});
  const oldReview=readFileSync(join(root,reviewPath),"utf8"), oldActivity=structuredClone(change.activity);

  // Editing a reviewed model reports drift, but the CLI does not invalidate or route.
  writeFileSync(join(root,wf),readFileSync(join(root,wf),"utf8")+"\nFixture correction.\n");
  const drift=invoke("inspect");
  assert.ok(drift.observations.some(o=>o.code==="subject-drift"));
  assert.deepEqual(JSON.parse(drift.snapshot.records.find(r=>r.path===manifest).content).activity,oldActivity);
  assert.equal(readFileSync(join(root,reviewPath),"utf8"),oldReview);
  change.models[0].subject=subject(wf);
  change.applicability=change.applicability.map(a=>({...a,value:"stale",actor:author,reason:"Reviewed model changed; do not rely on old proof"}));
  save();
  assert.equal(readFileSync(join(root,reviewPath),"utf8"),oldReview);

  // Route can select the completed owner without a derived pending-owner list.
  change.activity={stage:"design",status:"in-progress",owner:author,reason:"Route explicitly reopens completed owner"};
  change.work[0].status="in-progress";
  save();

  // Verify originates its own defect, preserving old review and failed evidence.
  const blocker={...fixture.review.findings[0],id:"verify-defect",reporter:verifier,owner:author,subjects:[subject(wf)],state:"open",resolution:null};
  blocker.origin={...Object.fromEntries(['reporter','subjects','evidence','required_outcome'].map(k=>[k,structuredClone(blocker[k])])),rationale:'Synthetic Verify finding.',supporting_judgment:null};
  change.blockers=[blocker];
  change.activity={stage:"verify",status:"blocked",owner:verifier,reason:"New defect found at Verify"};
  evidence.checks[0]={...evidence.checks[0],actor:verifier,subjects:[subject(wf)],result:"failed"};
  save({[evidencePath]:encode(evidence)});
  assert.equal(existsSync(join(root,verifyPath)),false);
  assert.equal(readFileSync(join(root,reviewPath),"utf8"),oldReview);
  change.activity={stage:"design",status:"in-progress",owner:author,reason:"Route selects correction owner for Verify blocker"};
  save();
  assert.equal(JSON.parse(readFileSync(join(root,manifest))).blockers[0].state,"open");

  // Returning a correction does not resolve its blocker or silently renew review.
  change.work[0].status="ready";
  save();
  assert.equal(readFileSync(join(root,reviewPath),"utf8"),oldReview);
  review.subjects=[subject(wf),subject(cli)];
  evidence.checks[0]={...evidence.checks[0],subjects:[subject(wf),subject(cli)],result:"passed"};
  change.applicability=change.applicability.map(a=>({...a,value:"current",actor:a.path===reviewPath?reviewer:verifier,reason:"Explicit new assessment"}));
  save({[reviewPath]:markdown(review),[evidencePath]:encode(evidence)});
  assert.equal(change.blockers[0].state,"open");

  // Only the actor's final replacement closes its blocker and records completion.
  blocker.state="resolved"; blocker.resolution={actor:verifier,rationale:"Correction reassessed",evidence_refs:[{path:evidencePath,id:evidence.checks[0].id}]};
  change.work[0].status="completed";
  change.activity={stage:"verify",status:"completed",owner:verifier,reason:"Explicit fixture final decision"};
  change.records.push({path:verifyPath,kind:"verify"});
  change.applicability.push({path:verifyPath,value:"current",actor:verifier,reason:"Explicit successful assessment"});
  const report={...fixture.verify,verifier,subjects:[subject(wf),subject(cli)]};
  save({[verifyPath]:markdown(report)});
  assert.equal(JSON.parse(readFileSync(join(root,manifest))).activity.status,"completed");
});

test("TG-05 reviewer role text is recordable attribution, not authenticated independence",()=>{
  // Actual independence is assessed by the separate M3 walkthrough, not this fixture.
  const fixture=JSON.parse(readFileSync(new URL("../../../tests/fixtures/rigorloop-records-v2/storage-safety.json",import.meta.url)));
  fixture.review.reviewer={id:"author",role:"review"};
  assert.doesNotThrow(()=>validateV2Record("review",fixture.review));
  assert.equal(fixture.review.reviewer.id,fixture.review.contributors[0].id);
  assert.notEqual(fixture.review.reviewer.role,fixture.review.contributors[0].role);
});
