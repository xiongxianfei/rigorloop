/* Real offline browser boundary: invoked by the composed Python generation case. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const puppeteer = require(process.env.REM_PUPPETEER);
(async () => {
  const browser = await puppeteer.launch({executablePath:process.env.REM_CHROMIUM,headless:true,args:['--no-sandbox']});
  try {
    const page=await browser.newPage();await page.setViewport({width:1440,height:1000});await page.setOfflineMode(true);
    const errors=[],network=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
    const base=pathToFileURL(path.resolve(process.argv[2])).href,shots=process.argv[3];
    const go=async hash=>{await page.goto(base+'#'+hash);await page.waitForFunction(()=>document.querySelector('main h1'));};
    const text=()=>page.$eval('main',e=>e.innerText);
    const capture=async name=>{if(shots){fs.mkdirSync(shots,{recursive:true});await page.screenshot({path:path.join(shots,name+'.png'),fullPage:true})}};
    const overflow=async()=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'viewport overflow');
    const skillsCase = async prefix => {
      await go('skills');
      assert.match(await text(),/Design catalogue/);
      const names=await page.$$eval('.catalog-entry strong',n=>n.map(x=>x.textContent));
      for (const name of ['requirement-analysis','requirement-review','system-design','architecture-design']) assert(names.includes(name));
      for (const name of ['proposal','proposal-review','design']) assert(!names.includes(name));
      assert.equal(await page.$('.observed-skill-sources'),null);
      await overflow();await capture(prefix+'-designed-skills');
      await page.type('#catalog-filter','requirement-analysis');
      assert.equal(await page.$$eval('.catalog-entry',n=>n.length),1);
      await page.click('.catalog-entry');await page.waitForFunction(()=>document.querySelector('main h1')?.textContent === 'requirement-analysis');
      assert.equal(await page.$eval('main .qualification',n=>n.textContent),'Design');
      assert.match(await text(),/Read design contract/);
      assert.equal(await page.$('a[href$="skills/requirement-analysis/SKILL.md"]'),null);
      await overflow();await capture(prefix+'-designed-skill-detail');
      await go('commands');
      const commands=await page.$$eval('.catalog-entry strong',n=>n.map(x=>x.textContent));
      assert.deepEqual([...commands].sort(), [
        'store backup','store restore','store migrate','init','change create','change context','change update','change complete',
        'review prepare','review show','review record','verification show','verification record',
        'browser generate','browser check','browser recover',
        '--help','version','capabilities','logs'
      ].sort());
      await page.type('#catalog-filter','browser');
      await overflow();await capture(prefix+'-designed-commands');
      await go('development/MOD-012');
      assert(await page.$$eval('details > summary',n=>n.some(x=>x.textContent==='Observed public sources')));
    };
    const inlineCase = async (route, titles, shot) => {
      await go(route);await page.reload();
      await page.waitForFunction(()=>document.querySelector('main h1'));
      assert.equal(await page.$$eval('.inline-view-diagrams .diagram-panel',n=>n.length),titles.length);
      assert.equal(await page.$$eval('.diagram-section-navigation',n=>n.length),titles.length>1?1:0);
      assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),route.split('/')[1]);
      assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),route.startsWith('process')?'Process':'Development');
      if (!titles.length) {
        assert.match(await text(),/No development realization detail recorded/);
        assert.equal(await page.$('.diagram-panel'),null);
      } else {
        await page.waitForFunction(()=>[...document.querySelectorAll('.inline-view-diagrams img')].every(i=>i.naturalWidth>0 && parseFloat(i.style.width)>0));
        assert.deepEqual(await page.$$eval('.inline-view-diagrams .diagram-toolbar h3',n=>n.map(x=>x.textContent)),titles);
        assert.equal(await page.$$eval('.inline-view-diagrams .diagram-expanded-link',n=>n.length),titles.length);
        assert.equal(await page.$$eval('.inline-view-diagrams .qualification',n=>n.length),titles.length);
        const widths=await page.$$eval('.inline-view-diagrams img',n=>n.map(i=>parseFloat(i.style.width)));
        await page.click('.inline-view-diagrams [aria-label="Zoom in"]');
        const zoomed=await page.$$eval('.inline-view-diagrams img',n=>n.map(i=>parseFloat(i.style.width)));
        assert(zoomed[0]>widths[0]);assert.deepEqual(zoomed.slice(1),widths.slice(1));
        await page.click('.inline-view-diagrams [aria-label="Fit diagram"]');
        assert(await page.$eval('.inline-view-diagrams .authored-viewport',e=>e.querySelector('img').getBoundingClientRect().width<=e.clientWidth));
        if (titles.length>1) {
          assert.deepEqual(await page.$$eval('.section-jump',n=>n.map(b=>b.textContent)),titles);
          const buttons=await page.$$('.section-jump');await buttons.at(-1).focus();await page.keyboard.press('Enter');
          assert.equal(await page.evaluate(()=>document.activeElement.id),await buttons.at(-1).evaluate(n=>n.getAttribute('aria-controls')));
          assert.equal(await page.evaluate(()=>location.hash),'#'+route);
          assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),route.split('/')[1]);
        }
      }
      if (route === 'development/MOD-004') {
        assert.equal(await page.$eval('.development-build-resources',n=>n.checkVisibility()),true);
        assert.equal(await page.$$eval('.development-build-resources tbody tr',n=>n.length),6);
        assert.match(await page.$eval('.development-build-resources .qualification',n=>n.textContent),/^Design/);
        assert.match(await page.$eval('.development-build-resources',n=>n.innerText),/Customer snapshot generation is runtime product behavior/);
        assert.match(await page.$eval('.development-build-resources tbody a',n=>n.getAttribute('href')),/MOD-013-product-package-production\/README.md#browser-candidate-contract$/);
        assert(await page.evaluate(()=>Boolean(document.querySelector('.inline-view-diagrams').compareDocumentPosition(document.querySelector('.development-build-resources')) & Node.DOCUMENT_POSITION_FOLLOWING)));
        assert(await page.evaluate(()=>Boolean(document.querySelector('.development-build-resources').compareDocumentPosition(document.querySelector('.facet-panel')) & Node.DOCUMENT_POSITION_FOLLOWING)));
        if (page.viewport().width < 700) {
          await page.focus('.development-build-resources .development-table-scroll');await page.keyboard.press('ArrowRight');
          await page.waitForFunction(()=>document.querySelector('.development-build-resources .development-table-scroll').scrollLeft>0);
        }
        assert.equal(await page.$eval('.implementation-references',n=>n.open),false);
        assert.equal(await page.$eval('.implementation-references > summary',n=>n.textContent),'Implementation references');
        assert.equal(await page.$eval('.development-implementation',n=>n.checkVisibility()),false);
        assert(await page.evaluate(()=>Boolean(document.querySelector('.facet-panel').compareDocumentPosition(document.querySelector('.implementation-references')) & Node.DOCUMENT_POSITION_FOLLOWING)));
        await page.focus('.implementation-references > summary');await page.keyboard.press('Enter');
        assert.equal(await page.$eval('.implementation-references',n=>n.open),true);
        assert.equal(await page.$$eval('.development-implementation tbody tr',n=>n.length),5);
        assert.deepEqual(await page.$$eval('.development-implementation th',n=>n.map(x=>x.textContent)),['Software responsibility','Current source','Scope and limitation']);
        assert.match(await page.$eval('.development-implementation',n=>n.innerText),/do not implement the target atomic snapshot publication/);
        assert.match(await page.$eval('.development-implementation .qualification',n=>n.textContent),/Observed/);
        assert.equal(await page.$eval('.development-implementation tbody a',n=>n.getAttribute('href')),'../../../../scripts/lib/rem_architecture_model.py');
        assert(await page.evaluate(()=>Boolean(document.querySelector('.inline-view-diagrams').compareDocumentPosition(document.querySelector('.development-implementation')) & Node.DOCUMENT_POSITION_FOLLOWING)));
        if (page.viewport().width < 700) {
          assert(await page.$eval('.development-implementation .development-table-scroll',n=>n.scrollWidth>n.clientWidth));
          await page.focus('.development-implementation .development-table-scroll');
          assert.equal(await page.evaluate(()=>document.activeElement.getAttribute('aria-label')),'Current implementation table');
          await page.keyboard.press('ArrowRight');
          await page.waitForFunction(()=>document.querySelector('.development-implementation .development-table-scroll').scrollLeft>0);
        }
        if(shot)await capture(shot+'-references');
        await page.focus('.implementation-references > summary');await page.keyboard.press('Enter');
        assert.equal(await page.$eval('.implementation-references',n=>n.open),false);
      } else {
        assert.equal(await page.$('.development-implementation'),null);
        assert.equal(await page.$('.development-build-resources'),null);
      }
      await overflow();if(shot)await capture(shot);
    };

    await skillsCase('desktop');

    // Scope tree and perspective navigation must agree after actual clicks.
    const clickRoute=async(selector,hash)=>{await page.click(selector);await page.waitForFunction(expected=>location.hash===expected && document.querySelector('#navigation [aria-current]')?.getAttribute('href')===expected,{},hash);};
    await go('home');
    assert.deepEqual(await page.$$eval('#navigation .nav-label',nodes=>nodes.map(n=>n.textContent)),['Architecture','Public capabilities']);
    assert.equal(await page.$$eval('.architecture-view-navigation a',nodes=>nodes.length),6);
    assert.equal(await page.$eval('#navigation .system-nav',n=>n.textContent),'RigorLoop');
    await clickRoute('.architecture-view-navigation a[href="#process"]','#process');
    await clickRoute('#navigation a[data-scope="MOD-016"]','#process/MOD-016');
    await clickRoute('#navigation a[data-scope="MOD-004"]','#process/MOD-004');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Process');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-004');
    await clickRoute('.architecture-view-navigation a[href="#physical/MOD-004"]','#physical/MOD-004');
    await clickRoute('#navigation .system-nav','#physical');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Physical');
    await page.goBack();await page.waitForFunction(()=>location.hash==='#physical/MOD-004');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-004');
    await go('process/MOD-009');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Process');
    assert.match(await text(),/No process realization detail recorded/);
    await go('commands');assert.equal(await page.$('.architecture-view-navigation'),null);
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.textContent),'Commands');
    await go('home');assert.match(await text(),/Top-level Modules/);await capture('home');await overflow();
    await go('module/MOD-004');assert.equal(await page.$$eval('.architecture-view-navigation a',n=>n.length),6);assert.match(await text(),/Direct Interfaces/);await capture('module');
    await go('logical/MOD-004');assert.equal(await page.$$eval('.diagram-canvas > svg',n=>n.length),1);
    assert.equal(await page.$$eval('.inline-view-diagrams .diagram-panel',n=>n.length),2);
    assert.deepEqual(await page.$$eval('.section-jump',n=>n.map(x=>x.textContent)),['Collaboration context','Browser technical structure']);
    await page.waitForFunction(()=>document.querySelector('.inline-view-diagrams img')?.naturalWidth>0);
    const technicalJump=(await page.$$('.section-jump')).at(-1);await technicalJump.focus();await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(()=>document.activeElement.id),await technicalJump.evaluate(n=>n.getAttribute('aria-controls')));
    assert.equal(await page.evaluate(()=>location.hash),'#logical/MOD-004');
    await overflow();await capture('logical-technical');
    await page.click('main a[href="#logical/MOD-004/proposed/topology/browser-technical-structure"]');
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent==='Browser technical structure');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Logical');
    await page.click('.topic-return');await page.waitForFunction(()=>location.hash==='#logical/MOD-004' && !document.querySelector('.topic-return'));
    await inlineCase('development/MOD-009',[],'zero-graphs');
    await inlineCase('process/MOD-006',['Resume and coordinate work'],'one-graph');
    await inlineCase('development/MOD-004',['Browser software organization','Browser file and package organization','Browser build and artifacts'],'development-graphs');
    await inlineCase('process/MOD-004',['Generation topology','Generation sequence','Publication and recovery'],'several-graphs');
    assert.deepEqual(await page.$$eval('.process-details h2',nodes=>nodes.map(n=>n.textContent)),['Runtime topology','Interactions','State and coordination']);
    assert.doesNotMatch(await text(),/Source-owned design topics/);
    await go('process/MOD-011');
    await page.click('.process-details a[href="#process/MOD-011/interaction/publication"]');
    await page.waitForFunction(()=>document.querySelector('.topic-return')?.getAttribute('href')==='#process/MOD-011');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-011');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Process');
    await page.click('.topic-return');await page.waitForFunction(()=>location.hash==='#process/MOD-011' && !document.querySelector('.topic-return'));
    const route='process/MOD-004/proposed/sequence/generation-sequence';await go(route);
    await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);await capture('sequence');
    const width=await page.$eval('.authored-viewport img',e=>parseFloat(e.style.width));await page.click('[aria-label="Zoom in"]');assert((await page.$eval('.authored-viewport img',e=>parseFloat(e.style.width)))>width);
    await page.click('[aria-label="Fit diagram"]');assert(await page.$eval('.authored-viewport',e=>e.querySelector('img').getBoundingClientRect().width<=e.clientWidth));
    await go('process/MOD-004/proposed/state/publication-recovery');await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);await capture('recovery');
    await page.click('main a[href="#entity/AR-048"]');await page.waitForFunction(()=>document.querySelector('h1')?.textContent.includes('Preserve source'));await page.goBack();assert(page.url().endsWith('publication-recovery'));
    // Both published presentations resolve to the single current sequence.
    for (const [owner,topic] of [['MOD-006','resume-and-progress'],['MOD-017','whole-change-review-and-correction']]) {
      for (const presentation of ['sequence','flowchart']) {
        await go(`process/${owner}/proposed/${presentation}/${topic}`);
        await page.reload();
        await page.waitForFunction(expected=>document.querySelector('main > .qualification')?.textContent === 'Design · Sequence' && document.querySelector('#navigation [aria-current]')?.dataset.scope === expected,{},owner);
        await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);
        assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),owner);
      }
    }
    await go('process/MOD-017/proposed/sequence/correct-and-reassess');
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent === 'Correct and reassess');
    await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);
    await capture('corrections');
    await go('capability/architecture-browser');
    assert.equal(await page.$('.architecture-view-navigation'),null);
    await page.click('main a[href="#logical/MOD-004"]');
    await page.waitForFunction(()=>location.hash==='#logical/MOD-004' && document.querySelector('.architecture-view-navigation [aria-current]')?.textContent==='Logical');
    assert.match(await text(),/Browser technical structure/);
    await go('capability/architecture-browser');
    await page.click('main a[href="#development/MOD-004"]');
    await page.waitForFunction(()=>location.hash === '#development/MOD-004' && document.querySelector('.architecture-view-navigation [aria-current]')?.textContent === 'Development');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-004');
    assert.match(await text(),/Design decisions/);
    assert.match(await text(),/Browser software organization/);
    assert.match(await text(),/browser-data contract/);
    await page.click('main a[href="#development/MOD-004/proposed/topology/browser-software-organization"]');
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent === 'Browser software organization');
    await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);
    assert.equal(await page.$eval('main > .qualification',n=>n.textContent),'Design · Topology');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-004');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Development');
    assert.match(await text(),/reusable browser template/);
    await capture('browser-development');
    await page.click('.topic-return');
    await page.waitForFunction(()=>location.hash === '#development/MOD-004' && !document.querySelector('.topic-return'));
    assert.equal(await page.$$eval('.inline-view-diagrams .authored-diagram',n=>n.length),3);
    await page.click('main a[href="#development/MOD-004/proposed/topology/browser-file-organization"]');
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent === 'Browser file and package organization');
    await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);
    assert.match(await text(),/packages\/rigorloop\/browser\//);
    assert.match(await text(),/not claims that the files already exist/);
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Development');
    await capture('file-organization');
    await page.click('.topic-return');
    await page.waitForFunction(()=>location.hash === '#development/MOD-004' && !document.querySelector('.topic-return'));
    await page.click('main a[href="#development/MOD-004/proposed/topology/browser-build-packaging"]');
    await page.waitForFunction(()=>document.querySelector('h1')?.textContent === 'Browser build and artifacts');
    await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Development');
    assert.equal(await page.$eval('#navigation [aria-current]',n=>n.dataset.scope),'MOD-004');
    assert.match(await text(),/package assembly owned by MOD-013/);
    await capture('build-packaging');
    await page.click('.topic-return');
    await page.waitForFunction(()=>location.hash === '#development/MOD-004' && !document.querySelector('.topic-return'));
    assert.equal(await page.$$eval('.inline-view-diagrams .authored-diagram',n=>n.length),3);
    await go('process/MOD-006');await page.reload();
    assert.equal(await page.$$eval('.inline-view-diagrams .authored-diagram',n=>n.length),1);
    assert.equal(await page.$$eval('.parent-process-topics .authored-diagram',n=>n.length),0);
    assert.equal(await page.$$eval('.parent-process-topics a.module-card',n=>n.length),2);
    await go('physical/MOD-004');assert.match(await text(),/Design decisions/);
    await go('scenarios/MOD-004');assert.match(await text(),/No participation walkthrough recorded/);
    await go('process/MOD-009');assert.match(await text(),/No process realization detail recorded/);
    await go('process/MOD-009/interaction/publication');assert.match(await text(),/Process diagram not found/);
    await go('process/MOD-004/observed/sequence/generation-sequence');assert.match(await text(),/not found/);
    for(const hash of ['overview','process','development','physical','scenarios','cooperation','contributions','commands','skills','process/interaction/publication','development/testing','physical/storage']){await go(hash);assert.doesNotMatch(await page.$eval('h1',e=>e.textContent),/not found/)}
    await page.setViewport({width:390,height:844});
    await skillsCase('mobile');
    await inlineCase('development/MOD-009',[],'mobile-zero-graphs');
    await inlineCase('process/MOD-006',['Resume and coordinate work'],'mobile-one-graph');
    await inlineCase('development/MOD-004',['Browser software organization','Browser file and package organization','Browser build and artifacts'],'mobile-development-graphs');
    await go('logical/MOD-004');await page.waitForFunction(()=>document.querySelector('.inline-view-diagrams img')?.naturalWidth>0);
    assert.equal(await page.$$eval('.inline-view-diagrams .diagram-panel',n=>n.length),2);
    await overflow();await capture('mobile-logical-technical');
    await inlineCase('process/MOD-004',['Generation topology','Generation sequence','Publication and recovery'],'mobile-several-graphs');
    await go('module/MOD-004');await overflow();
    await page.click('#navigation-toggle');assert.equal(await page.$eval('#navigation-toggle',e=>e.getAttribute('aria-expanded')),'true');
    await page.keyboard.press('Escape');assert.equal(await page.$eval('#navigation-toggle',e=>e.getAttribute('aria-expanded')),'false');
    await go('process/MOD-004');await page.click('#navigation-toggle');
    await clickRoute('#navigation .system-nav','#process');
    assert.equal(await page.$eval('#navigation-toggle',e=>e.getAttribute('aria-expanded')),'false');
    assert.equal(await page.$eval('.architecture-view-navigation [aria-current]',n=>n.textContent),'Process');
    await overflow();
    await go(route);await page.waitForFunction(()=>document.querySelector('.authored-viewport img')?.naturalWidth>0);await overflow();await capture('mobile-process');
    await page.keyboard.press('Tab');assert(await page.evaluate(()=>document.activeElement!==document.body));
    assert.deepEqual(errors,[]);assert.deepEqual(network,[]);assert.equal(await page.evaluate(()=>globalThis.untrustedTextExecuted),undefined);
    console.log(JSON.stringify({browser:await browser.version(),offline:true,network,errors,result:'passed'}));
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
