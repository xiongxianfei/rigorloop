/* Synthetic selected accounts prove reader states, not real AR satisfaction. */
const assert=require('node:assert/strict');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const puppeteer=require(process.env.REM_PUPPETEER);
(async()=>{
  const browser=await puppeteer.launch({executablePath:process.env.REM_CHROMIUM,headless:true,args:['--no-sandbox']});
  try {
    const page=await browser.newPage(),errors=[],network=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
    await page.setOfflineMode(true);
    for(const width of [1440,390]) {
      await page.setViewport({width,height:900});
      for(const [name,implementation,verification] of [
        ['partial','Partial','Not assessed'],['passed','Implemented','Passed'],
        ['failed','Partial','Failed'],['stale','Unknown','Needs reassessment']]) {
        const base=pathToFileURL(path.join(process.argv[2],name+'.html')).href;
        for(const route of ['requirements/AR-046','entity/AR-046']) {
          await page.goto(base+'#'+route);await page.waitForSelector('.delivery-assessment-detail');await page.$$eval('.delivery-assessment-detail details',nodes=>nodes.forEach(n=>n.open=true));
          const body=await page.$eval('.delivery-assessment-detail',n=>n.innerText);
          assert.match(body,new RegExp('Implementation: '+implementation));
          assert.match(body,new RegExp('Verification: '+verification));
          assert.match(body,/fixture-assessor/);assert.match(body,/2026-10-05T10:00:00Z/);
          assert.equal(await page.$$eval('.delivery-criterion',n=>n.length),12);
          assert.match(body,/Repository observation 1/);
          assert.match(await page.$eval('main',n=>n.innerText),/Definition: Draft/);
          if(name==='stale') {
            assert.match(body,/Historical acceptance criterion assessment/);
            assert.match(body,/Historical outcome: Partial/);
            assert.match(body,/definition changed/);
            assert.doesNotMatch(await page.$eval('.delivery-criterion',n=>n.innerText),/New current criterion/);
          } else if(name!=='passed') assert.match(body,/Remaining gap: Customer scope not exercised/);
          await page.$eval('.delivery-assessment-detail details',n=>n.open=true);
          assert.match(await page.$eval('.delivery-assessment-detail .assessment-sources',n=>n.innerText),/fixture-change.*fixture-evidence/);
          assert.match(await page.$eval('.delivery-assessment-detail .assessment-sources',n=>n.innerText),/sha256:[0-9a-f]{64}/);
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`viewport overflow ${name} ${route} ${width}: `+await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(n=>n.getBoundingClientRect().right>innerWidth).slice(0,8).map(n=>n.className+' '+n.tagName+' '+n.getBoundingClientRect().right).join(', ')));
          assert.equal(await page.evaluate(()=>globalThis.untrustedAssessmentExecuted),undefined);
        }
        for(const [id,state] of [['SR-085','Covered'],['SR-009','Gap'],['IR-002','Not reviewed']]) {
          await page.goto(base+'#requirements/'+id);await page.waitForSelector('.requirement-evaluation-detail');
          const body=await page.$eval('.requirement-evaluation-detail',n=>n.innerText);
          assert.match(body,new RegExp('Design: '+state));
          assert.doesNotMatch(body,/Preview only/);
          assert.match(body,/Child Design:/);assert.match(body,/Child Implementation:/);assert.match(body,/Child Verification:/);
          if(id==='SR-009')assert.match(body,/AR required.*MOD-004/);
          if(id==='IR-002')assert.match(body,/Stakeholder outcome basis: not reviewed/);
          if(id==='SR-085')assert.equal(await page.$$eval('.evaluation-criteria li',n=>n.length),6);
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`Design viewport overflow ${id} ${width}`);
        }
        await page.goto(base+'#requirements/AR-001');await page.waitForSelector('.delivery-assessment-detail');await page.$$eval('.delivery-assessment-detail details',nodes=>nodes.forEach(n=>n.open=true));
        assert.match(await page.$eval('.delivery-assessment-detail',n=>n.innerText),/No implementation or verification assessments are included for this requirement/);
      }
      for(const [name,state] of [['covered','Covered'],['gap','Gap'],['stale','Needs reassessment']]) {
        const base=pathToFileURL(path.join(process.argv[2],'ir-'+name+'.html')).href;
        for(const route of ['requirements/IR-002','entity/IR-002']) {
          await page.goto(base+'#'+route);await page.waitForSelector('.requirement-evaluation-detail');
          const body=await page.$eval('.requirement-evaluation-detail',n=>n.innerText);
          assert.match(body,new RegExp('Design: '+state));
          assert.match(body,/Implementation: Unknown/);assert.match(body,/Verification: Not assessed/);
          assert.match(body,/stakeholder outcomes/i);assert.doesNotMatch(body,/Stakeholder outcome basis: not reviewed/);
          assert.equal(await page.$$eval('.evaluation-criteria li',n=>n.length),1);
          if(name==='stale')assert.match(body,/Relied-upon SR account missing or changed/);
          await page.$$eval('.requirement-evaluation-detail details',nodes=>nodes.forEach(n=>n.open=true));
          assert.match(await page.$eval('.outcome-basis-sources',n=>n.innerText),/Reviewed stakeholder outcome basis: sha256:/);
          assert.equal(await page.$$eval('.outcome-basis-sources a',n=>n.length),8);
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`IR outcome overflow ${name} ${route} ${width}`);
          await page.click('.outcome-basis-sources a');await page.waitForFunction(()=>location.hash.includes('SR-008'));
        }
      }
    }
    const v2=pathToFileURL(path.join(process.argv[2],'v2.html')).href;
    for(const width of [1440,390]) {
      await page.setViewport({width,height:900});
      for(const [id,impl,verification] of [['IR-002','Implemented','Passed'],['SR-085','Implemented','Passed'],['SR-050','Unknown','Not assessed'],['AR-046','Implemented','Needs reassessment']]) {
        for(const route of ['requirements/','entity/']) {
          await page.goto(v2+'#'+route+id);await page.waitForSelector('.delivery-assessment-detail');
          await page.$$eval('.delivery-assessment-detail details',nodes=>nodes.forEach(n=>n.open=true));
          const body=await page.$eval('.delivery-assessment-detail',n=>n.innerText);
          assert.match(body,new RegExp('Implementation: '+impl));assert.match(body,new RegExp('Verification: '+verification));
          assert.match(body,/fixture-assessor/);assert.match(body,/sha256:/);
          if(id==='IR-002')assert.match(body,/Delivery outcome basis/);
          if(id==='AR-046') {assert.match(body,/Competing assessments/);assert.match(body,/Historical outcome: Failed/);assert.match(body,/open-issue/);}
          assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`v2 overflow ${id} ${width}`);
        }
      }
      await page.goto(v2+'#requirements/SR-050');await page.waitForSelector('#requirement-filter');
      const initialCounts=await page.$$eval('.evaluation-child-count',n=>n.map(x=>x.textContent));
      const selectedBefore=await page.$eval('.requirement-label[aria-current]',n=>n.closest('.requirement-node').dataset.key);
      await page.select('#requirement-filter','no-ar');
      await page.$eval('#requirement-search',n=>{n.value='SR-050';n.dispatchEvent(new Event('input',{bubbles:true}));});
      assert.deepEqual(await page.$$eval('.requirement-match',n=>n.map(x=>x.closest('.requirement-node').dataset.entity)),['SR-050']);
      assert.match(await page.$eval('.results-count',n=>n.textContent),/^1 matching occurrences$/);
      assert.deepEqual(await page.$$eval('.evaluation-child-count',n=>n.map(x=>x.textContent)),initialCounts);
      await page.select('#requirement-filter','design-gap');
      assert.equal(await page.$$eval('.requirement-match',n=>n.length),0);
      await page.$eval('#requirement-search',n=>{n.value='';n.dispatchEvent(new Event('input',{bubbles:true}));});
      assert.deepEqual(await page.$$eval('.requirement-match',n=>n.map(x=>x.closest('.requirement-node').dataset.entity)),['SR-009']);
      await page.select('#requirement-filter','not-assessed');
      const matches=await page.$$eval('.requirement-match',n=>n.map(x=>x.closest('.requirement-node').dataset.entity));
      assert(matches.includes('SR-050'));assert(!matches.includes('AR-046'));assert(!matches.includes('IR-002'));assert(!matches.includes('SR-085'));
      await page.goBack();await page.waitForFunction(()=>document.querySelector('#requirement-filter')?.value==='design-gap');
      await page.goForward();await page.waitForFunction(()=>document.querySelector('#requirement-filter')?.value==='not-assessed');
      await page.$$eval('.requirement-actions button',nodes=>nodes.find(n=>n.textContent==='Clear filters').click());
      assert.equal(await page.$eval('#requirement-filter',n=>n.value),'');assert.equal(await page.$eval('#requirement-search',n=>n.value),'');
      assert.equal(await page.$eval('.requirement-label[aria-current]',n=>n.closest('.requirement-node').dataset.key),selectedBefore);
      // Filter history has already canonicalized this occurrence's URL. Normal
      // reactivation must reopen details even though no hashchange will fire.
      const sameOccurrence=await page.$eval('.requirement-label[aria-current]',n=>n.hash);
      assert.equal(await page.evaluate(()=>location.hash),sameOccurrence);
      const historyLength=await page.evaluate(()=>history.length);
      for(const activation of ['keyboard','pointer']) {
        await page.$$eval('.requirement-detail-actions button',nodes=>nodes.find(n=>n.textContent==='Close details').click());
        assert.equal(await page.$('.requirement-detail'),null);
        await page.focus('.requirement-label[aria-current]');
        if(activation==='keyboard')await page.keyboard.press('Enter');
        else await page.click('.requirement-label[aria-current]');
        await page.waitForSelector('.requirement-detail');
        assert.equal(await page.evaluate(()=>location.hash),sameOccurrence);
        assert.equal(await page.evaluate(()=>history.length),historyLength);
        assert.match(await page.$eval('.requirement-detail',n=>n.innerText),/SR-050/);
      }
      await page.select('#requirement-filter','design-gap');
      await page.$$eval('.requirement-detail-actions button',nodes=>nodes.find(n=>n.textContent.includes('Reveal')).click());
      assert.equal(await page.$eval('#requirement-filter',n=>n.value),'');
      assert.equal(await page.$eval('.requirement-label[aria-current]',n=>n.closest('.requirement-node').dataset.entity),'SR-050');
    }
    assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
    console.log('Assessment reader: 4 states, 2 routes, desktop/mobile, absent neighbor; actual Design projection fixtures, three child summaries; zero errors/network.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
