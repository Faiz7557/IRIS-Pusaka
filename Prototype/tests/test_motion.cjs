// Exercise the real motion lifecycle; no network, timers or paid API requests.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const script = fs.readFileSync(path.join(__dirname, '../web/motion.js'), 'utf8');
async function harness({reduce = false, libraries = true} = {}) {
  const media = {matches:reduce,addEventListener(){}};
  const stage = {hidden:false,attrs:{},classList:{contains:()=>stage.hidden},
    querySelector:()=>null,setAttribute:(k,v)=>stage.attrs[k]=v,removeAttribute:k=>delete stage.attrs[k]};
  let observer, active = 0, smooth = 0, scenes = 0;
  const root = {dataset:{}};
  const context = {
    console,innerWidth:1200,scrollY:0,location:{hash:''},matchMedia:()=>media,
    setTimeout:()=>0,clearTimeout(){},requestAnimationFrame:f=>f(),scrollTo(){},addEventListener(){},
    document:{readyState:'complete',documentElement:root,fonts:{ready:Promise.resolve()},
      getElementById:id=>id==='input-stage'?stage:null,querySelector:()=>null,querySelectorAll:()=>[]},
    MutationObserver:class {constructor(callback){observer=callback;}observe(){}},
  };
  context.window=context;
  if(libraries) {
    context.ScrollTrigger={update(){},sort(){},refresh(){}};
    context.gsap={registerPlugin(){},ticker:{add(){},remove(){},lagSmoothing(){}},
      context(){let used=false;return {add(f){used=true;active++;f();},revert(){if(used){active--;used=false;}}};},
      matchMedia(){return {revert(){}};}};
    context.Lenis=class {constructor(){smooth++;}on(){}resize(){}raf(){}destroy(){smooth--;}scrollTo(){}};
    context.buildSillScenes=()=>{scenes++;context.queueMotion(()=>context.createSillMedia());};
  }
  vm.runInNewContext(script,context);
  await new Promise(setImmediate);
  return {context,root,stage,media,stats:()=>({active,smooth,scenes}),changed:()=>observer()};
}
(async()=>{
  const staticPage=await harness({libraries:false});
  assert.equal(staticPage.root.dataset.motion,'static');
  assert.equal(staticPage.stage.attrs['data-scenes'],undefined);
  const h=await harness({reduce:true});
  assert.equal(h.root.dataset.motion,'reduced');
  assert.deepEqual(h.stats(),{active:0,smooth:0,scenes:0});
  h.media.matches=false;h.context.SimakMotion.configure();
  assert.deepEqual(h.stats(),{active:1,smooth:1,scenes:1});
  h.stage.hidden=true;h.changed();
  assert.equal(h.stats().active,0,'hidden introduction must release its pin/scene contexts');
  assert.equal(h.stage.attrs['data-scenes'],undefined);
  h.stage.hidden=false;h.changed();
  assert.equal(h.stats().active,1,'returning to upload builds one set of scenes');
  h.context.SimakMotion.configure();
  assert.equal(h.stats().active,1,'reconfiguration must not stack scene contexts');
  assert.equal(h.stats().smooth,1,'reconfiguration must not stack smooth scroll engines');
  h.media.matches=true;h.context.SimakMotion.configure();
  assert.equal(h.root.dataset.motion,'reduced');
  assert.equal(h.stats().active,0);assert.equal(h.stats().smooth,0);
  console.log('PASS: missing-library fallback, reduced motion, result cleanup, upload restoration, no stacked engines');
})().catch(e=>{console.error(e);process.exitCode=1;});
