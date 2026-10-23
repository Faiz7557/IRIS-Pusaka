// Run with Microsoft's Playwright installed as an external development tool.
const {chromium}=require(process.env.SIMAK_PLAYWRIGHT || '@playwright/test');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
  const out=path.resolve(__dirname,'evidence/workbench');fs.mkdirSync(out,{recursive:true});
  const browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const report={};
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  for(const route of ['demo.html','dengar.html','evaluasi.html']){
    await page.goto('http://127.0.0.1:8019/'+route);
    await page.locator('html[data-motion]').waitFor();await page.waitForTimeout(1000);
    await page.screenshot({path:path.join(out,'before-'+route.replace('.html','.png'))});
    report[route]={title:await page.title(),width:await page.evaluate(()=>({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}))};
  }
  await page.goto('http://127.0.0.1:8019/evaluasi.html');
  const table=page.locator('.twrap').first();await table.waitFor();await table.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);const box=await table.boundingBox();
  await page.mouse.move(box.x+box.width/2,box.y+12);
  const before=await page.evaluate(()=>scrollY);await page.mouse.wheel(0,350);await page.waitForTimeout(650);
  report.tableWheel={before,after:await page.evaluate(()=>scrollY)};report.errors=errors;
  fs.writeFileSync(path.join(out,'before-browser.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));await browser.close();
})().catch(error=>{console.error(error);process.exitCode=1;});
