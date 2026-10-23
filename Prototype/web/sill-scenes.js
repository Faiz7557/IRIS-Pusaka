/* Adapted from Sill by 8B. MIT. See third_party/sill/LICENSE. */
function buildSillScenes(){
// Sill: motion

const effects = {
  peek(frame, vars = {}) {
    return gsap.fromTo(frame.firstElementChild, { yPercent: 42 }, { yPercent: 0, ease: 'none', ...vars });
  },
  rise(heading, vars = {}) {
    const split = SplitText.create(heading, { type: 'lines', mask: 'lines' });
    const timeline = gsap.timeline({ ...vars, onComplete() { split.revert(); } });
    timeline.from(split.lines, { yPercent: 108, duration: .9, stagger: .09, ease: 'power3.out' });
    timeline.split = split;
    return timeline;
  },
  curl(svg, vars = {}) {
    return gsap.fromTo(svg.querySelector('path'), { strokeDashoffset: 1 }, { strokeDashoffset: 0, ease: 'none', ...vars });
  }
};
document.querySelectorAll('[data-8b-section]').forEach(section => {
  const first = section.getBoundingClientRect().top < window.innerHeight;
  const peeks = section.querySelectorAll('[data-8b-motion~="peek"]');
  if (peeks.length) {
    const id = `effect:peek:${section.id}`;
    queueMotion(() => createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
      peeks.forEach((frame, i) => ScrollTrigger.create({
        id: `${id}:${i}`, trigger: frame, start: 'top bottom', end: 'top 40%', scrub: .5,
        animation: effects.peek(frame)
      }));
    }), { first, id });
  }
  const rises = section.querySelectorAll('[data-8b-motion~="rise"]');
  if (rises.length) {
    const id = `effect:rise:${section.id}`;
    queueMotion(() => createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
      const timelines = [...rises].map((heading, i) => {
        const timeline = effects.rise(heading, { paused: true });
        ScrollTrigger.create({ id: `${id}:${i}`, trigger: heading, start: 'top 88%', once: true, animation: timeline, toggleActions: 'play play none none' });
        return timeline;
      });
      return () => timelines.forEach(timeline => timeline.split.revert());
    }), { first, id });
  }
  const curls = section.querySelectorAll('[data-8b-motion~="curl"]');
  if (curls.length) {
    const id = `effect:curl:${section.id}`;
    queueMotion(() => createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
      curls.forEach((svg, i) => ScrollTrigger.create({
        id: `${id}:${i}`, trigger: svg, start: 'top 95%', end: 'bottom 45%', scrub: .6,
        animation: effects.curl(svg)
      }));
    }), { first, id });
  }
});

// Sill: scene:opening

queueMotion(() => {
  const section = document.getElementById('opening');
  const first = section.querySelector('.op-s1');
  const second = section.querySelector('.op-s2');
  const ink = section.querySelector('.op-ink');
  const inkCurl = ink.querySelector('.op-ink__curl path');
  const cells = ['.op-a', '.op-e', '.op-c', '.op-d', '.op-b'].map(selector => section.querySelector(selector));
  const windows = gsap.utils.toArray('.op-win', section);
  createSillMedia().add({
    wide: '(min-width: 768px) and (prefers-reduced-motion: no-preference)',
    narrow: '(max-width: 767.98px) and (prefers-reduced-motion: no-preference)'
  }, context => {
    const { wide } = context.conditions;
    section.setAttribute('data-ink', '');
    const shear = wide
      ? [[-.03, -.16], [.05, -.3], [-.06, .02], [.01, -.1], [.06, -.2]]
      : [[-.04, -.12], [.06, -.22], [-.05, .02], [.02, -.08], [-.06, -.18]];
    const house = section.querySelector('.op-house');
    const jitter = [.03, 0, .05, .02, .06, .01];
    const timeline = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { id: 'opening', trigger: second, start: 'top bottom', end: 'top top', scrub: .5, invalidateOnRefresh: true }
    });
    timeline.fromTo(ink, { y: 0 }, { y: () => -1.02 * first.offsetHeight, duration: 1 }, 0);
    timeline.fromTo(inkCurl, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: .42 }, .06);
    cells.forEach((cell, i) => timeline.fromTo(cell, { x: 0, y: 0 }, {
      x: () => shear[i][0] * window.innerWidth, y: () => shear[i][1] * window.innerHeight, duration: .85, ease: 'power1.in'
    }, 0));
    windows.forEach((win, i) => {
      const at = Math.min(.84, (house.offsetTop + win.offsetTop) / first.offsetHeight + .05 + jitter[i % jitter.length]);
      timeline.fromTo(win, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: .14, ease: 'power1.out' }, at);
      const photo = win.querySelector('img');
      if (photo) timeline.fromTo(photo, { yPercent: 45 }, { yPercent: 0, duration: .2, ease: 'power2.out' }, at + .04);
    });
    return () => section.removeAttribute('data-ink');
  });
}, { first: true });

// Sill: scene:rooms

queueMotion(() => {
  const section = document.getElementById('rooms');
  const rooms = gsap.utils.toArray('.rm-room', section);
  const towerName = section.querySelector('.rm-tower .rm-name');
  createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
    const side = () => Math.min(...rooms.map(room => Math.min(room.offsetWidth, room.offsetHeight))) * (window.innerWidth < 768 ? .62 : .9);
    rooms.forEach((room, i) => {
      const timeline = gsap.timeline({
        defaults: { ease: 'none' },
        scrollTrigger: { id: `rooms:${i}`, trigger: room, start: 'top 88%', end: 'bottom 78%', scrub: .5, invalidateOnRefresh: true }
      });
      timeline.fromTo(room, {
        clipPath: () => { const s = side(); return `inset(${room.offsetHeight - s}px ${room.offsetWidth - s}px 0px 0px)`; }
      }, { clipPath: 'inset(0px 0px 0px 0px)', duration: 1, ease: 'power1.inOut' }, 0);
      if (room.contains(towerName)) timeline.fromTo(towerName, { rotation: 0 }, { rotation: -90, duration: .7, ease: 'power2.inOut' }, .3);
    });
  });
});

// Sill: scene:day

queueMotion(() => {
  const section = document.getElementById('day');
  const stage = section.querySelector('.dy-stage');
  const rail = section.querySelector('.dy-rail');
  const track = section.querySelector('.dy-track');
  const sky = section.querySelector('.dy-sky');
  const disc = section.querySelector('.dy-disc');
  const tokens = getComputedStyle(document.documentElement);
  const colors = ['--color-3', '--color-10', '--color-9', '--color-6', '--color-7', '--color-5'].map(token => tokens.getPropertyValue(token).trim());
  createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
    section.setAttribute('data-track', '');
    const travel = () => Math.max(0, track.scrollWidth - rail.clientWidth);
    const timeline = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { id: 'day', trigger: section, start: 'top top', end: () => `+=${Math.max(window.innerHeight, travel() * 1.15)}`, pin: stage, scrub: .6, invalidateOnRefresh: true }
    });
    timeline.fromTo(track, { x: 0 }, { x: () => -travel(), duration: 1 }, 0);
    colors.slice(1).forEach((color, i) => timeline.to(sky, { backgroundColor: color, duration: 1 / (colors.length - 1) }, i / (colors.length - 1)));
    timeline.fromTo(disc, { x: () => sky.clientWidth * .06 }, { x: () => sky.clientWidth - disc.offsetWidth - sky.clientWidth * .06, duration: 1 }, 0);
    timeline.fromTo(disc, { y: () => sky.clientHeight + 4 }, { y: () => sky.clientHeight * .12, duration: .42, ease: 'sine.out' }, .02);
    timeline.to(disc, { y: () => sky.clientHeight + 4, duration: .4, ease: 'sine.in' }, .58);
    return () => section.removeAttribute('data-track');
  });
});

// Sill: scene:courtyard

queueMotion(() => {
  const section = document.getElementById('courtyard');
  const view = section.querySelector('.cy-window');
  const panes = gsap.utils.toArray('.cy-pane', view);
  const tints = gsap.utils.toArray('.cy-tint', view);
  createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
    const offsets = [[-5, -20], [4, 16], [-3, -11], [6, 22], [-6, 12], [3, -18]];
    const timeline = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { id: 'courtyard', trigger: view, start: 'top 92%', end: 'center 52%', scrub: .6 }
    });
    panes.forEach((pane, i) => timeline.fromTo(pane, { xPercent: offsets[i][0], yPercent: offsets[i][1] }, { xPercent: 0, yPercent: 0, duration: 1, ease: 'power2.out' }, 0));
    tints.forEach((tint, i) => timeline.fromTo(tint, { opacity: .94 }, { opacity: 0, duration: .55 }, .3 + i * .03));
  });
});

// Sill: scene:quiet

queueMotion(() => {
  const section = document.getElementById('quiet');
  const list = section.querySelector('.qt-rules');
  const rules = gsap.utils.toArray('.qt-rule', list);
  const words = rules.map(rule => rule.querySelector('.qt-word'));
  const loud = getComputedStyle(document.documentElement).getPropertyValue('--color-3').trim();
  createSillMedia().add('(prefers-reduced-motion: no-preference)', () => {
    const rest = rules.map(rule => getComputedStyle(rule).backgroundColor);
    const weight = getComputedStyle(words[0]).fontWeight;
    const scale = window.innerWidth < 768 ? .45 : 1;
    const tilt = [[-7, -50, 34], [6, 40, -26], [-5, -26, 30], [8, 56, -36]];
    const timeline = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { id: 'quiet', trigger: list, start: 'top 95%', end: 'center 56%', scrub: .6 }
    });
    rules.forEach((rule, i) => {
      timeline.fromTo(rule, { rotation: tilt[i][0] * scale, y: tilt[i][1] * scale, x: tilt[i][2] * scale }, { rotation: 0, y: 0, x: 0, duration: 1, ease: 'power2.out' }, 0);
      timeline.fromTo(rule, { backgroundColor: loud }, { backgroundColor: rest[i], duration: .6 }, .35);
      timeline.fromTo(words[i], { fontWeight: 900 }, { fontWeight: weight, duration: .7 }, .25);
    });
  });
});

// Sill: scene:contact

queueMotion(() => {
  const section = document.getElementById('contact');
  const grid = section.querySelector('.ct-grid');
  const call = section.querySelector('.ct-call');
  const write = section.querySelector('.ct-write');
  const visit = section.querySelector('.ct-visit');
  const hours = section.querySelector('.ct-hours');
  createSillMedia().add({
    wide: '(min-width: 900.02px) and (prefers-reduced-motion: no-preference)',
    narrow: '(max-width: 900px) and (prefers-reduced-motion: no-preference)'
  }, context => {
    const { wide } = context.conditions;
    const timeline = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: { id: 'contact', trigger: grid, start: 'top 92%', end: () => wide ? 'top 22%' : 'top 40%', scrub: .6, invalidateOnRefresh: true }
    });
    timeline.fromTo(call, { xPercent: wide ? -80 : -40 }, { xPercent: 0, duration: 1, ease: 'power2.out' }, 0)
      .fromTo(write, { xPercent: wide ? 80 : 40 }, { xPercent: 0, duration: 1, ease: 'power2.out' }, 0)
      .fromTo(visit, { yPercent: -60 }, { yPercent: 0, duration: 1, ease: 'power2.out' }, 0)
      .fromTo(hours, { yPercent: 60 }, { yPercent: 0, duration: 1, ease: 'power2.out' }, 0);
    if (wide) {
      timeline.fromTo(call.querySelector('.ct-label'), { rotation: 0 }, { rotation: -90, duration: .6, ease: 'power2.inOut' }, .35)
        .fromTo(write.querySelector('.ct-label'), { rotation: 0 }, { rotation: 90, duration: .6, ease: 'power2.inOut' }, .35);
    }
  });
});

}
