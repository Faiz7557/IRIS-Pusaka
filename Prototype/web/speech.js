/* Pemutar bersama aplikasi dan reader mandiri. Tidak memuat kredensial. */
(() => {
  function splitSpeechText(text, limit = 2400) {
    const chunks = [];
    let rest = String(text).trim();
    while (rest.length > limit) {
      const head = rest.slice(0, limit);
      const sentence = [...head.matchAll(/[.!?;]\s+/g)].pop();
      let cut = sentence && sentence.index > limit / 2 ? sentence.index + 1 : head.lastIndexOf(' ');
      if (cut < limit / 2) cut = limit;
      if (/[\uD800-\uDBFF]/.test(rest[cut - 1])) cut--;
      chunks.push(rest.slice(0, cut).trim());
      rest = rest.slice(cut).trim();
    }
    if (rest) chunks.push(rest);
    return chunks;
  }

  class SimakSpeech {
    constructor() {
      this.pref = {suara: 'peramban', kecepatan: 0, nada: 0};
      this.savedVoice = null;
      try {
        const p = JSON.parse(localStorage.getItem('simak-suara') || '{}');
        if (['eleven', 'peramban'].includes(p.suara)) this.savedVoice = p.suara;
        this.pref.kecepatan = Math.max(-20, Math.min(20, Number(p.kecepatan) || 0));
      } catch (_) {}
      this.generation = 0;
      this.audio = this.utter = this.controller = this.cancelPlayback = null;
      this.available = false;
      this.ready = this.discover();
    }
    async discover() {
      try {
        if (globalThis.location?.protocol === 'file:') return;
        const r = await fetch('/api/suara/daftar');
        if (!r.ok) return;
        const list = await r.json();
        this.available = Array.isArray(list) && list.some(s => s.id === 'eleven');
      } catch (_) {} finally {
        this.pref.suara = this.available ? (this.savedVoice || 'eleven') : 'peramban';
      }
    }
    save() {
      this.savedVoice = this.pref.suara;
      try { localStorage.setItem('simak-suara', JSON.stringify(this.pref)); } catch (_) {}
    }
    speaking() { return !!(this.audio || this.utter || this.controller); }
    stop() {
      this.generation++;
      this.controller?.abort(); this.controller = null;
      const cancel = this.cancelPlayback; this.cancelPlayback = null;
      cancel?.();
      if (this.utter) { this.utter = null; globalThis.speechSynthesis?.cancel(); }
    }
    async speak(text, onend, onerror, onstart) {
      this.stop();
      const generation = this.generation;
      await this.ready;
      if (generation !== this.generation) return;
      const settings = {...this.pref};
      const ctl = new AbortController(); this.controller = ctl;
      let started = false;
      try {
        for (const chunk of splitSpeechText(text)) {
          if (generation !== this.generation) return;
          await this.playChunk(chunk, settings, ctl, () => {
            if (!started && generation === this.generation) { started = true; onstart?.(); }
          });
        }
        if (generation === this.generation) { this.controller = null; onend?.(); }
      } catch (e) {
        if (generation === this.generation && e.name !== 'AbortError') {
          this.controller = null;
          onerror?.(e);
        }
      }
    }
    async playChunk(text, settings, ctl, onstart) {
      if (settings.suara !== 'eleven') {
        if (!globalThis.speechSynthesis) throw new Error('Suara peramban tidak tersedia.');
        return new Promise((resolve, reject) => {
          const u = new SpeechSynthesisUtterance(text);
          u.lang = 'id-ID'; u.rate = 1 + settings.kecepatan / 100;
          const voice = speechSynthesis.getVoices().find(v => /^id[-_]/i.test(v.lang));
          if (voice) u.voice = voice;
          const clean = () => { if (this.utter === u) this.utter = null; this.cancelPlayback = null; };
          u.onend = () => { clean(); resolve(); };
          u.onerror = e => { clean(); reject(new Error(e.error || 'Suara peramban gagal.')); };
          u.onstart = onstart;
          this.utter = u;
          this.cancelPlayback = () => { u.onend = u.onerror = u.onstart = null; clean(); speechSynthesis.cancel(); resolve(); };
          speechSynthesis.speak(u);
        });
      }
      const r = await fetch('/api/suara', {method: 'POST', headers: {'Content-Type': 'application/json'},
        signal: ctl.signal, body: JSON.stringify({teks: text, suara: 'eleven', kecepatan: settings.kecepatan, nada: 0})});
      if (!r.ok) {
        const body = await r.json().catch(() => ({}));
        throw new Error(body.detail || 'ElevenLabs belum dapat memutar suara. Pilih suara peramban atau coba lagi.');
      }
      const blob = await r.blob();
      if (ctl.signal.aborted) return;
      const url = URL.createObjectURL(blob);
      return new Promise((resolve, reject) => {
        const audio = new Audio(url); this.audio = audio;
        let settled = false;
        const finish = error => {
          if (settled) return; settled = true;
          audio.onended = audio.onerror = audio.onplaying = null;
          audio.pause(); URL.revokeObjectURL(url);
          if (this.audio === audio) this.audio = null;
          this.cancelPlayback = null;
          error ? reject(error) : resolve();
        };
        this.cancelPlayback = () => finish();
        audio.onended = () => finish();
        audio.onerror = () => finish(new Error('Audio gagal dibaca. Pilih suara peramban atau coba lagi.'));
        audio.onplaying = onstart;
        Promise.resolve(audio.play()).catch(finish);
      });
    }
  }
  globalThis.SimakSpeech = SimakSpeech;
  globalThis.splitSpeechText = splitSpeechText;
})();
