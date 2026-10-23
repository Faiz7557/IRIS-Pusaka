const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../web/speech.js'), 'utf8');
const tick = () => new Promise(setImmediate);

function harness({saved, file = false, autoEnd = true, rejectPlay = false} = {}) {
  const requests = [], revoked = [], audios = [];
  const context = vm.createContext({
    AbortController, console, location: {protocol: file ? 'file:' : 'http:'},
    localStorage: {getItem: () => JSON.stringify(saved || {}), setItem() {}},
    URL: {createObjectURL: () => 'blob:' + audios.length, revokeObjectURL: url => revoked.push(url)},
    Audio: class {
      constructor(src) { this.src = src; audios.push(this); }
      pause() { this.paused = true; }
      play() {
        if (rejectPlay) return Promise.reject(new Error('play denied'));
        queueMicrotask(() => { this.onplaying?.(); if (autoEnd) this.onended?.(); });
        return Promise.resolve();
      }
    },
    fetch: async (url, opts) => {
      if (url.endsWith('/daftar')) return {ok: true, json: async () => [{id: 'eleven'}]};
      requests.push(JSON.parse(opts.body));
      return {ok: true, blob: async () => ({})};
    },
  });
  vm.runInContext(source, context);
  return {context, requests, revoked, audios, create: () => vm.runInContext('new SimakSpeech()', context)};
}

(async () => {
  {
    const h = harness(), player = h.create(); await player.ready;
    assert.equal(player.pref.suara, 'eleven', 'configured server defaults to ElevenLabs');
    const text = ('Kalimat materi dengan angka dan data. ').repeat(300);
    let ended = 0, started = 0;
    await player.speak(text, () => ended++, assert.fail, () => started++);
    assert(h.requests.length > 1);
    assert(h.requests.every(r => r.teks.length <= 2400));
    assert.equal(h.requests.map(r => r.teks).join(' '), text.trim());
    assert.equal(ended, 1); assert.equal(started, 1);
    assert.equal(h.revoked.length, h.audios.length);
  }
  {
    const h = harness({saved: {suara: 'peramban', kecepatan: 20}}), player = h.create();
    await player.ready;
    assert.equal(player.pref.suara, 'peramban', 'explicit browser choice survives discovery');
    assert.equal(player.pref.kecepatan, 20);
  }
  {
    const h = harness({file: true}), player = h.create(); await player.ready;
    assert.equal(player.pref.suara, 'peramban'); assert.equal(h.requests.length, 0);
  }
  {
    const h = harness({autoEnd: false}), player = h.create(); await player.ready;
    let ended = 0;
    const task = player.speak('Teks panjang. '.repeat(500), () => ended++, assert.fail);
    await tick(); assert.equal(h.audios.length, 1);
    player.stop(); await task;
    assert.equal(ended, 0); assert.equal(h.requests.length, 1);
    assert(h.audios[0].paused); assert.equal(h.revoked.length, 1);
  }
  {
    const h = harness({rejectPlay: true}), player = h.create(); await player.ready;
    let error = '';
    await player.speak('Uji', assert.fail, e => error = e.message);
    assert.equal(error, 'play denied'); assert.equal(h.revoked.length, 1);
    assert.equal(player.speaking(), false);
  }
  {
    const h = harness(), player = h.create(); await player.ready;
    let release, ended = 0;
    h.context.fetch = () => new Promise(r => release = r);
    const task = player.speak('Uji respons terlambat', () => ended++, assert.fail);
    await tick(); player.stop();
    release({ok: true, blob: async () => ({})}); await task;
    assert.equal(h.audios.length, 0); assert.equal(ended, 0);
  }
  console.log('PASS: ElevenLabs default, preferences, long blocks, standalone fallback, cancellation, playback errors, stale audio');
})().catch(e => { console.error(e); process.exitCode = 1; });
