/* Motion orchestration for the Sill adaptation. Native content stays visible without JS. */
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const root = document.documentElement;
  let lenis = null, tick = null, homeContexts = [], homeMedia = [], entry = null;
  let initialized = false, lastWidth = innerWidth, resizeTimer, refreshTimer;
  const home = () => document.getElementById('input-stage');
  const homeVisible = () => home() && !home().classList.contains('hide');

  function refresh() {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => { lenis?.resize(); window.ScrollTrigger?.sort(); window.ScrollTrigger?.refresh(); }, 80);
  }
  function clearHome() {
    homeMedia.splice(0).reverse().forEach(media => media.revert());
    homeContexts.splice(0).reverse().forEach(context => context.revert());
    home()?.removeAttribute('data-scenes');
  }
  function buildHome() {
    clearHome();
    if (!homeVisible() || reduced.matches || !window.gsap || !window.buildSillScenes) return;
    window.createSillMedia = () => { const media = gsap.matchMedia(); homeMedia.push(media); return media; };
    window.queueMotion = setup => {
      const context = gsap.context(() => {}, home());
      try { context.add(setup); homeContexts.push(context); }
      catch (error) { context.revert(); console.error('SIMAK scene:', error); }
    };
    window.buildSillScenes();
    home().setAttribute('data-scenes', 'ready');
    refresh();
  }
  function startSmooth() {
    if (lenis || reduced.matches || !window.Lenis || !window.gsap || !window.ScrollTrigger) return;
    lenis = window.lenis = new Lenis({lerp:.09,wheelMultiplier:.95,anchors:true,
      prevent: node => !!node.closest('[data-lenis-prevent],textarea,select,.tr,.qlist,.twrap,.nav-menu')});
    lenis.on('scroll', ScrollTrigger.update);
    tick = time => lenis?.raf(time * 1000);
    gsap.ticker.add(tick);gsap.ticker.lagSmoothing(0);
  }
  function stopSmooth() {
    if (tick) window.gsap?.ticker.remove(tick);
    tick = null;lenis?.destroy();lenis = window.lenis = null;
  }
  function enterPage() {
    entry?.revert();entry = null;
    if (reduced.matches || !window.gsap) return;
    const main = document.querySelector('main');
    if (homeVisible()) return;
    entry = gsap.context(() => {
      const heading = main?.querySelector('h1');
      if (heading && window.SplitText) {
        const split = SplitText.create(heading,{type:'lines',mask:'lines'});
        gsap.from(split.lines,{yPercent:105,duration:.8,stagger:.075,ease:'power3.out',onComplete:()=>split.revert()});
      }
      const panels = main?.querySelectorAll('.page-head,.source-panel,.listen-intro,.toolbar');
      if (panels?.length) gsap.from(panels,{y:i=>i%2?22:-16,duration:.65,stagger:.06,ease:'power2.out',clearProps:'transform'});
    },main);
  }
  function configure() {
    clearHome();stopSmooth();entry?.revert();entry = null;
    if (reduced.matches) { root.dataset.motion = 'reduced';return; }
    if (!window.gsap || !window.ScrollTrigger) { root.dataset.motion = 'static';return; }
    gsap.registerPlugin(ScrollTrigger);
    if (window.SplitText) gsap.registerPlugin(SplitText);
    startSmooth();buildHome();enterPage();root.dataset.motion = 'ready';
  }
  function initNavigation() {
    const header = document.querySelector('.rail'), menu = document.getElementById('site-menu');
    const toggle = document.getElementById('nav-toggle'), close = document.getElementById('nav-close');
    if (!header || !menu || !toggle || !close) return;
    let last = scrollY, run = 0, lastFocus;
    function shut(refocus=true) {
      menu.hidden = true;toggle.setAttribute('aria-expanded','false');
      header.removeAttribute('data-hidden');lenis?.start();document.body.style.overflow='';
      if (refocus) (lastFocus || toggle).focus();
    }
    toggle.addEventListener('click',()=>{
      lastFocus = document.activeElement;menu.hidden=false;toggle.setAttribute('aria-expanded','true');
      header.removeAttribute('data-hidden');lenis?.stop();document.body.style.overflow='hidden';
      if (!reduced.matches && window.gsap) gsap.fromTo(menu.querySelectorAll('li'),{y:35},{y:0,duration:.55,stagger:.045,ease:'power3.out',clearProps:'transform'});
      close.focus();
    });
    close.addEventListener('click',()=>shut());
    menu.addEventListener('click',event=>{if(event.target.closest('a'))shut(false);});
    menu.addEventListener('keydown',event=>{
      if(event.key==='Escape'){event.preventDefault();shut();return;}
      if(event.key!=='Tab')return;
      const controls=[...menu.querySelectorAll('button,a[href]')];
      const first=controls[0],last=controls[controls.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    });
    header.addEventListener('focusin',()=>header.removeAttribute('data-hidden'));
    addEventListener('scroll',()=>{
      const y=scrollY,d=y-last;last=y;
      if(y<90||!menu.hidden){header.removeAttribute('data-hidden');run=0;return;}
      if(!d)return;if(Math.sign(d)!==Math.sign(run))run=0;run+=d;
      if(run>30&&!header.contains(document.activeElement))header.setAttribute('data-hidden','');
      else if(run< -30)header.removeAttribute('data-hidden');
    },{passive:true});
    addEventListener('resize',()=>{if(innerWidth>1100&&!menu.hidden)shut(false);});
  }
  function bindHomeState() {
    const stage=home();if(!stage)return;
    let visible=homeVisible();
    new MutationObserver(()=>{
      const next=homeVisible();if(next===visible)return;visible=next;
      if(!next){clearHome();refresh();requestAnimationFrame(()=>{lenis?.scrollTo(0,{immediate:true});if(!lenis)scrollTo(0,0);});}
      else{buildHome();setTimeout(()=>{const target=document.getElementById('contact');if(target){lenis?lenis.scrollTo(target,{immediate:true}):target.scrollIntoView();}},150);}
    }).observe(stage,{attributes:true,attributeFilter:['class']});
    const screen=stage.querySelector('.op-s1');
    if(screen&&'IntersectionObserver' in window)new IntersectionObserver(([entry])=>screen.toggleAttribute('data-paused',!entry.isIntersecting)).observe(screen);
  }
  function boot() {
    if(initialized)return;initialized=true;
    initNavigation();bindHomeState();
    const fonts=document.fonts?.ready||Promise.resolve();
    fonts.then(()=>{
      configure();
      if(location.hash&&homeVisible())setTimeout(()=>{
        let target;try{target=document.querySelector(location.hash);}catch(_){}
        if(target){lenis?lenis.scrollTo(target,{immediate:true}):target.scrollIntoView();}
      },180);
    });
    reduced.addEventListener?.('change',configure);
    addEventListener('resize',()=>{
      clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{
        if(Math.abs(innerWidth-lastWidth)>30){lastWidth=innerWidth;buildHome();}refresh();
      },180);
    },{passive:true});
    document.querySelectorAll('img').forEach(img=>{if(!img.complete)img.addEventListener('load',refresh,{once:true});});
    addEventListener('pageshow',refresh);
  }
  window.refreshScroll=refresh;
  window.SimakMotion={refresh,configure};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
