// Microsoft Playwright browser regression. Install @playwright/test as a dev tool; set SIMAK_PLAYWRIGHT if external.
const {chromium,expect}=require(process.env.SIMAK_PLAYWRIGHT || '@playwright/test');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'..'), out=path.join(root,'tasks/evidence/workbench');
const base=process.env.SIMAK_TEST_URL || 'http://127.0.0.1:8019';
(async()=>{
  const browser=await chromium.launch({channel:'chrome',headless:true});
  try {
    const context=await browser.newContext({viewport:{width:1440,height:1000}});
    const page=await context.newPage(),errors=[],report={checks:[],viewports:[]};
    page.on('pageerror',error=>errors.push(error.message));
    const ready=async()=>{await page.locator('html[data-motion]').waitFor();await page.waitForTimeout(800);};
    const shot=name=>page.screenshot({path:path.join(out,name+'.png')});
    await page.goto(base+'/evaluasi.html');await page.locator('#res .twrap').first().waitFor();await ready();
    const table=page.locator('#res .twrap').first();await table.scrollIntoViewIfNeeded();await page.waitForTimeout(350);
    const box=await table.boundingBox();await page.mouse.move(box.x+box.width/2,box.y+12);
    const y=await page.evaluate(()=>scrollY);await page.mouse.wheel(0,350);await page.waitForTimeout(700);
    const after=await page.evaluate(()=>scrollY);assert(after>y+150,'wheel over a table with no vertical overflow must scroll the page');
    report.checks.push({test:'table/padding wheel scroll',before:y,after});
    await page.goto(base+'/demo.html');await expect(page.locator('#run')).toBeEnabled();await ready();
    await page.locator('#run').click();await expect(page.locator('#b-verdict')).not.toHaveClass(/v-idle/,{timeout:45000});
    await expect(page.locator('#truth tbody tr')).not.toHaveCount(0);
    await page.locator('#mut [data-k="ubah_angka"]').click();await expect(page.locator('#b-verdict')).toHaveClass(/v-hold/,{timeout:15000});
    await page.locator('#reset').click();await expect(page.locator('#st')).toContainText('dikembalikan');
    const claim=page.locator('#b-focus .cl').first();
    if(await claim.count()){await claim.click();await expect(page.locator('#truth tr.on')).not.toHaveCount(0);}
    await page.evaluate(()=>window.lenis?window.lenis.scrollTo(0,{immediate:true}):scrollTo(0,0));await page.waitForTimeout(400);await shot('after-demo-desktop');
    report.checks.push({test:'demo run, mutation, reset and source claim',passed:true});
    await page.goto(base+'/dengar.html');await expect(page.locator('#go')).toBeEnabled();await ready();
    await page.locator('#go').click();await expect(page.locator('#stage')).toBeVisible({timeout:120000});
    await expect(page.locator('#tr-s li')).not.toHaveCount(0);
    await expect(page.locator('#p-s [data-a="play"]')).toBeEnabled();
    const job=new URL(page.url()).searchParams.get('job');report.job=job;
    const list=page.locator('#tr-s');await list.scrollIntoViewIfNeeded();await page.waitForTimeout(400);
    const b=await list.boundingBox();await page.mouse.move(b.x+b.width/2,b.y+60);
    const start=await list.evaluate(e=>e.scrollTop);await page.mouse.wheel(0,250);await page.waitForTimeout(600);
    assert(await list.evaluate(e=>e.scrollTop)>start,'a transcript with overflow must retain internal scrolling');
    await list.evaluate(e=>e.scrollTop=e.scrollHeight);await page.waitForTimeout(300);
    const edge=await page.evaluate(()=>scrollY);await page.mouse.wheel(0,300);await page.waitForTimeout(700);
    assert(await page.evaluate(()=>scrollY)>edge+100,'transcript bottom must hand scrolling back to page');
    await page.evaluate(()=>window.lenis?window.lenis.scrollTo(0,{immediate:true}):scrollTo(0,0));await page.waitForTimeout(350);await shot('after-dengar-desktop');
    report.checks.push({test:'listen transcript, controls, nested scroll and edge handoff',passed:true});
    await page.goto(base+'/index.html?job='+job);await expect(page.locator('#hasil')).toBeVisible({timeout:15000});await ready();
    await expect(page.locator('#out a[href$="simak.html"]')).toBeVisible();
    await expect(page.locator('#out a[href$="simak.pdf"]')).toBeVisible();
    await page.locator('#els button').first().click();await expect(page.locator('#alt')).toBeVisible();
    await expect(page.locator('#approve')).toBeEnabled();
    const editor=page.locator('#alt');await editor.scrollIntoViewIfNeeded();await page.waitForTimeout(350);
    const editorBox=await editor.boundingBox();await page.mouse.move(editorBox.x+6,editorBox.y+10);
    const editorY=await page.evaluate(()=>scrollY);await page.mouse.wheel(0,300);await page.waitForTimeout(650);
    assert(await page.evaluate(()=>scrollY)>editorY+100,'a short textarea must not trap page scrolling');
    await page.evaluate(()=>window.lenis?window.lenis.scrollTo(0,{immediate:true}):scrollTo(0,0));await page.waitForTimeout(300);await shot('after-remediasi-desktop');
    report.checks.push({test:'results, exports, queue selection and review controls',passed:true});
    for(const width of [320,390,768,1440]){
      await page.setViewportSize({width,height:1000});
      for(const route of ['demo.html','dengar.html?job='+job,'evaluasi.html','index.html?job='+job]){
        await page.goto(base+'/'+route);await ready();
        if(route.startsWith('evaluasi'))await page.locator('#res .eval-stat').first().waitFor();
        if(route.startsWith('index'))await page.locator('#hasil:not(.hide)').waitFor();
        const size=await page.evaluate(()=>({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
        assert(size.scroll<=size.client+1,`${route} overflows at ${width}: ${JSON.stringify(size)}`);
        report.viewports.push({width,route,...size});
        if(width===390||width===1440)await shot('after-'+route.split('.')[0]+'-'+width);
      }
    }
    await page.setViewportSize({width:390,height:900});await page.goto(base+'/demo.html');await ready();
    await page.locator('#nav-toggle').click();await expect(page.locator('#site-menu')).toBeVisible();
    await page.keyboard.press('Escape');await expect(page.locator('#site-menu')).toBeHidden();await expect(page.locator('#nav-toggle')).toBeFocused();
    await page.goto(base+'/?jelajah=1#opening');await ready();
    assert.equal(await page.locator('.gate-art').count(),0);
    await page.locator('#sitters').scrollIntoViewIfNeeded();await page.waitForTimeout(900);await shot('after-illustrations-mobile');
    await page.setViewportSize({width:1440,height:1000});await page.locator('#sitters').scrollIntoViewIfNeeded();await page.waitForTimeout(900);await shot('after-illustrations-desktop');
    await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await ready();
    await expect(page.locator('html')).toHaveAttribute('data-motion','reduced');assert.equal(await page.locator('.pin-spacer').count(),0);
    report.checks.push({test:'mobile menu/focus, illustration overlays, reduced motion',passed:true});
    const baseline=JSON.parse(fs.readFileSync(path.join(out,'unchanged-source.json'),'utf8'));
    for(const [file,hash] of Object.entries(baseline))assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex'),hash,file+' must remain unchanged');
    for(const name of ['index','demo','dengar']){
      const before=fs.readFileSync(path.join(out,'before-script-'+name+'.txt'),'utf8');
      const html=fs.readFileSync(path.join(root,'web',name+'.html'),'utf8');
      const current=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n');
      assert.equal(current.replace(/\r\n/g,'\n'),before.replace(/\r\n/g,'\n'),name+' business script changed');
    }
    assert.deepEqual(errors,[]);report.errors=errors;
    fs.writeFileSync(path.join(out,'after-browser.json'),JSON.stringify(report,null,2));
    console.log('PASS: '+report.checks.length+' browser flow checks, '+report.viewports.length+' responsive layouts; backend/shared controls and route logic unchanged.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
