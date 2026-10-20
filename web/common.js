// Komponen bersama antarmuka SIMAK (dunia: kartu katalog perpustakaan).
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const cap = s => s ? s[0].toUpperCase() + s.slice(1) : '';
const fmtId = v => typeof v === 'string' ? v : Number(v).toLocaleString('id-ID', {maximumFractionDigits: 2});
const norm = s => String(s).toLowerCase().normalize('NFKC').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
const $ = s => document.querySelector(s);

// Ikon garis 24px, satu ketebalan; dekoratif (aria-hidden) kecuali diberi label di elemen induk.
const ICON_PATHS = {
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  cross: '<path d="M6 6l12 12M18 6L6 18"/>',
  hold: '<rect x="5" y="4" width="14" height="16" rx="1.5"/><path d="M9 9h6M9 13h6M9 17h3"/>',
  alert: '<path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17.5v.01"/>',
  play: '<path d="M8 5.5v13l11-6.5z"/>',
  pause: '<path d="M8 5v14M16 5v14"/>',
  prev: '<path d="M18 6l-8 6 8 6zM6 6v12"/>',
  next: '<path d="M6 6l8 6-8 6zM18 6v12"/>',
  upload: '<path d="M12 16V4M7 9l5-5 5 5M5 20h14"/>',
  doc: '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/>',
  open: '<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>',
  trash: '<path d="M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13"/>',
  inject: '<path d="M14 4l6 6M17 7l-9 9-3 1 1-3 9-9M4 20l2-2"/>',
  undo: '<path d="M9 14L4 9l5-5"/><path d="M4 9h11a5 5 0 010 10h-3"/>',
  gauge: '<path d="M4 18a8 8 0 1116 0"/><path d="M12 18l4-6"/>',
  layers: '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
  chart: '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
  ear: '<path d="M7 9a5 5 0 0110 0c0 3-3 4-3 7a3 3 0 01-5.5 1.6"/><path d="M10 9a2 2 0 014 0"/>',
  skip: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  heading: '<path d="M6 4v16M18 4v16M6 12h12"/>',
  table: '<rect x="4" y="5" width="16" height="14" rx="1"/><path d="M4 10h16M10 10v9"/>',
};
const icon = (name, label) => `<svg class="icon" viewBox="0 0 24 24" ${label ? `role="img" aria-label="${esc(label)}"` : 'aria-hidden="true"'}>${ICON_PATHS[name] || ''}</svg>`;

// Rail: wordmark, navigasi, dan satu angka bukti dari evaluasi beku.
function renderRail(current) {
  const items = [['demo.html', 'Demo Gerbang', 'layers'], ['dengar.html', 'Dengar', 'ear'], ['index.html', 'Remediasi', 'doc'], ['evaluasi.html', 'Evaluasi', 'chart']];
  const rail = document.querySelector('.rail');
  rail.innerHTML = `
    <a class="wordmark" href="demo.html"><b>SIMAK</b><span>Sistem Ilustrasi Materi Aksesibel untuk Kuliah</span></a>
    <nav class="nav" aria-label="Navigasi utama">${items.map(([h, l, i]) =>
      `<a href="${h}" ${h === current ? 'aria-current="page"' : ''}>${icon(i)}${l}</a>`).join('')}</nav>
    <div class="rail-proof" id="rail-proof" hidden></div>`;
  fetch('/api/evaluasi').then(r => r.json()).then(r => {
    if (!r || r.ada === false || !r.G3) return;
    const f = r.G3.D_fk_terbit;
    const el = document.getElementById('rail-proof');
    el.innerHTML = `<div class="fig">${f.k}/${f.n}</div><p>angka yang terbit otomatis setia pada tabel acuan, set uji tertahan</p>`;
    el.hidden = false;
  }).catch(() => {});
}

const STATUS = {
  terbit_otomatis: ['pass', 'Terbit otomatis', 'check'],
  antrean: ['hold', 'Ditahan · menunggu ULD', 'hold'],
  disetujui: ['pass', 'Disetujui ULD', 'check'],
  diubah: ['pass', 'Diubah ULD', 'check'],
  ditolak: ['fail', 'Ditolak ULD', 'cross'],
  dekoratif: ['pending', 'Dekoratif', 'doc'],
};
const statusStamp = s => {
  const [k, t, i] = STATUS[s] || ['pending', s, 'doc'];
  return `<span class="stamp ${k === 'pass' ? '' : k}">${icon(i)}${t}</span>`;
};

const CHECKS = {cF: 'klaim setia pada tabel', 'cδ': 'dua ekstraksi konsisten', cA: 'nilai dalam rentang sumbu', cL: 'nilai tercetak pada grafik'};
const nowStamp = () => new Date().toLocaleTimeString('id-ID', {hour: '2-digit', minute: '2-digit'});
const checkStamps = (checks, when) => Object.entries(checks || {}).map(([k, v], i) =>
  `<span class="stamp ${v ? '' : 'fail'}" style="--i:${i}" title="${esc(CHECKS[k] || k)}">${icon(v ? 'check' : 'cross')}${esc(k)} ${v ? 'lulus' : 'gagal'}${when ? ` <span class="when">${esc(when)}</span>` : ''}<span class="sr"> · ${esc(CHECKS[k] || k)}</span></span>`).join('');
const checkLegend = () => Object.entries(CHECKS).map(([k, v]) => `<b class="num">${k}</b> ${v}`).join(' · ');

function pressSlip(slip) {
  if (!slip) return;
  slip.classList.remove('pressing');
  void slip.offsetWidth;
  slip.classList.add('pressing');
}

const MEASURE = {nilai: 'nilai', maksimum: 'maksimum', minimum: 'minimum', selisih: 'selisih', rerata: 'rerata',
  total: 'total', perubahan_terfit: 'perubahan terfit', perubahan: 'perubahan', tren: 'tren'};

function segHtml(seg, detail) {
  return seg.map(s => {
    if (s.claim === undefined || s.claim === null) return esc(s.text);
    const d = detail && detail[s.claim];
    const bad = d && !d.ok;
    const title = d ? `Klaim (${d.e}, ${MEASURE[d.m] || d.m}, ${fmtId(d.v)}): ${d.ok ? 'cocok dengan tabel data' : 'tidak cocok, tabel memuat ' + (d.ref === null ? 'tidak ada' : fmtId(d.ref))}` : '';
    return `<span class="cl${bad ? ' bad' : ''}${s.injected ? ' inj' : ''}" tabindex="0" role="button" data-claim="${s.claim}" data-e="${esc(d ? d.e : '')}" title="${esc(title)}" aria-label="${esc(s.text + '. ' + title)}">${esc(s.text)}</span>`;
  }).join('');
}

function t1t2(e) {
  const m2 = Object.fromEntries((e.T2 || []).map(r => [norm(r.kategori), r.nilai]));
  return `<table><caption>Ekstraksi ganda, δ = ${Number(e.delta).toFixed(3)}</caption><thead><tr><th scope="col">Kategori</th><th scope="col" class="n">T1</th><th scope="col" class="n">T2</th><th scope="col" class="n">|T1 − T2|</th></tr></thead><tbody>` +
    e.T1.map(r => {
      const v2 = m2[norm(r.kategori)];
      const dd = v2 === undefined ? null : Math.abs(r.nilai - v2);
      return `<tr data-row="${esc(norm(r.kategori))}"><th scope="row">${esc(r.kategori)}</th><td class="n">${fmtId(r.nilai)}</td><td class="n">${v2 === undefined ? '–' : fmtId(v2)}</td><td class="n ${dd ? 'd' : ''}">${dd === null ? '–' : fmtId(dd)}</td></tr>`;
    }).join('') + '</tbody></table>';
}

function bindClaims(root) {
  root.querySelectorAll('.cl').forEach(el => {
    const on = () => {
      root.querySelectorAll('.on').forEach(x => x.classList.remove('on'));
      el.classList.add('on');
      el.dataset.e.split('|').forEach(k => root.querySelectorAll(`tr[data-row="${CSS.escape(norm(k))}"]`).forEach(tr => tr.classList.add('on')));
    };
    el.addEventListener('click', on);
    el.addEventListener('focus', on);
    el.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); on(); } });
  });
}

function announce(msg) {
  let r = document.getElementById('sr-live');
  if (!r) { r = document.createElement('div'); r.id = 'sr-live'; r.setAttribute('aria-live', 'polite'); r.className = 'sr'; document.body.appendChild(r); }
  r.textContent = '';
  setTimeout(() => { r.textContent = msg; }, 30);
}

// ---------------------------------------------------------------- suara (mode dengar)
// Satu sumber: suara manusia dari ElevenLabs, dibuat oleh server (perlu ELEVENLABS_API_KEY dan ELEVENLABS_VOICE_ID).
const Voice = {
  pref: {suara: 'eleven', kecepatan: 0, nada: 0},
  audio: null, utter: null, ctl: null,
  load() { try { Object.assign(this.pref, JSON.parse(localStorage.getItem('simak-suara') || '{}'), {suara: 'eleven'}); } catch (e) {} },
  save() { try { localStorage.setItem('simak-suara', JSON.stringify(this.pref)); } catch (e) {} },
  stop() {
    if (this.ctl) this.ctl.abort();
    this.ctl = null;
    if (this.audio) { this.audio.pause(); this.audio = null; }
  },
  // Mengucapkan teks; onend dipanggil saat selesai, onerror bila suara server gagal.
  async speak(text, onend, onerror, onstart) {
    this.stop();
    const p = this.pref;
    const ctl = new AbortController(); this.ctl = ctl;
    try {
      const r = await fetch('/api/suara', {method: 'POST', headers: {'Content-Type': 'application/json'}, signal: ctl.signal,
        body: JSON.stringify({teks: text, suara: p.suara, kecepatan: p.kecepatan, nada: p.nada})});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const url = URL.createObjectURL(await r.blob());
      if (this.ctl !== ctl) return;
      const a = new Audio(url); this.audio = a;
      a.onended = () => { URL.revokeObjectURL(url); if (this.audio === a) { this.audio = null; onend && onend(); } };
      await a.play();
      onstart && onstart();
    } catch (e) {
      if (e.name === 'AbortError') return;
      onerror ? onerror(e) : onend && onend();
    }
  },
  prefetch(texts) {
    fetch('/api/suara/siapkan', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({teks: texts.filter(Boolean), suara: this.pref.suara, kecepatan: this.pref.kecepatan, nada: this.pref.nada})}).catch(() => {});
  },
  // Kontrol pilihan suara, kecepatan, dan nada; onchange dipanggil setelah pengguna mengubahnya.
  controls(el, onchange) {
    const opt = (v, l, cur) => `<option value="${v}" ${String(cur) === String(v) ? 'selected' : ''}>${l}</option>`;
    el.innerHTML = `
      <span class="lbl" style="min-width:0">Suara: manusia (ElevenLabs)</span>
      <label class="lbl" for="v-cepat" style="min-width:0">Kecepatan</label>
      <select id="v-cepat">${[-20, -10, 0, 10, 20, 35].map(v => opt(v, (v > 0 ? '+' : '') + v + '%', this.pref.kecepatan)).join('')}</select>
      <button type="button" id="v-coba">${icon('play')}Coba suara</button>`;
    const upd = () => {
      this.pref = {suara: 'eleven', kecepatan: +el.querySelector('#v-cepat').value, nada: 0};
      this.save(); this.stop(); onchange && onchange();
    };
    // Bila server belum dikonfigurasi (ELEVENLABS_API_KEY dan ELEVENLABS_VOICE_ID), beri tahu pengguna.
    fetch('/api/suara/daftar').then(r => r.json()).then(list => {
      if (list.some(s => s.id === 'eleven')) return;
      el.querySelector('#v-coba').insertAdjacentHTML('afterend', '<span class="lbl" role="alert">Suara ElevenLabs belum diatur di server.</span>');
    }).catch(() => {});
    el.querySelectorAll('select').forEach(s => s.onchange = upd);
    el.querySelector('#v-coba').onclick = () => this.speak('Halo, saya membacakan materi kuliah untuk Anda. Nilai tertinggi pada Juli, yaitu 1.452 kunjungan.');
  },
};
Voice.load();
