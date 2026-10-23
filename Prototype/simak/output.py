"""OUT-01/OUT-02: HTML mandiri dengan status dan pemutar ElevenLabs/peramban bersama."""
import base64
import html
from pathlib import Path

from .chart import fmt

_FONT = Path(__file__).resolve().parent.parent / "web" / "fonts" / "AtkinsonHyperlegibleNext-normal-latin.woff2"
_FONT_FACE = ("@font-face{font-family:'Atkinson Hyperlegible Next';font-weight:200 800;font-display:swap;"
              "src:url(data:font/woff2;base64," + base64.b64encode(_FONT.read_bytes()).decode() + ") format('woff2')}"
              ) if _FONT.exists() else ""

# Permukaan baca cream; mengikuti preferensi terang/gelap pembaca.
CSS = """
:root{--rail:#f6efdf;--rail-ink:#0b0a0a;--bar-hover:#e6dcc8;--bg:#f6efdf;--card:#fffaf0;--fg:#0b0a0a;--muted:#514c49;--line:#b5aaa3;
--ruling:#d8d1cc;--brand:#cf6224;--red:#a51d2d;--redbg:#fce6e8;--ok:#185c3a;--okbg:#e4f2e9;--hold:#624000;--h1:#fff0c2;--h2:#f4dfa2;--acc:#1457c5;--hl:#fff0a6}
@media(prefers-color-scheme:dark){:root{--rail:#181615;--rail-ink:#f4f1ee;--bar-hover:#38302b;--bg:#181615;--card:#24201d;--fg:#f4f1ee;--muted:#cbbdb3;--line:#78685c;--ruling:#55483e;--red:#ffafb7;--redbg:#4d2027;--ok:#9bdfb7;--okbg:#173a29;--hold:#f3cf79;--h1:#3e2e12;--h2:#544016;--acc:#a9c9ff;--hl:#504115}}
*{box-sizing:border-box}html{scroll-padding-top:140px}body{margin:0;background:var(--bg);color:var(--fg);font:400 18px/1.7 'Atkinson Hyperlegible Next','Segoe UI',system-ui,sans-serif}
::selection{background:var(--hl);color:var(--fg)}:focus-visible{outline:3px solid var(--acc);outline-offset:3px;box-shadow:0 0 0 5px var(--bg)}*{scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:8px;background:var(--card);padding:8px 12px;z-index:9;font-weight:700}
main{max-width:48rem;margin:0 auto;padding:1.5rem 20px 6rem}h1{font-size:2rem;line-height:1.2;font-weight:800;letter-spacing:-.025em}h2{font-size:1.45rem;line-height:1.25}h1,h2,h3{text-wrap:balance;scroll-margin-top:140px}
.bar{position:sticky;top:0;z-index:5;background:var(--rail);color:var(--rail-ink);padding:10px 16px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bar b{font-weight:800;letter-spacing:-.02em;margin-right:6px}.bar button,.bar select,.bar summary{font-family:inherit;font-size:15px;font-weight:700;line-height:1.2;min-height:44px;min-width:44px;padding:10px 12px;border:1px solid #bca59d;border-radius:2px;background:transparent;color:var(--rail-ink);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:6px}
.bar button:hover{background:var(--bar-hover)}.bar button#play{background:var(--fg);color:var(--card);border-color:var(--fg)}.bar select option{color:#0b0a0a;background:#f4f1ee}.bar label{font-size:15px;display:inline-flex;gap:8px;align-items:center;flex-wrap:wrap}.bar :focus-visible{outline-color:var(--acc);box-shadow:none}.bar .st{font-size:14px;flex:1 1 100%}.bar .st:empty{display:none}.settings[open]{flex:1 1 100%}.settings>div{display:flex;flex-wrap:wrap;gap:12px;padding-top:10px}.settings summary{list-style:none}.settings p{font-size:14px;margin:0;max-width:65ch}
.icon{width:1.1em;height:1.1em;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.notice{border:1px solid var(--line);border-top:5px solid var(--brand);padding:18px 20px;background:var(--card);font-size:16px;margin:1rem 0 1.5rem}
figure{margin:1.75rem 0;background:var(--card);border:1px solid var(--line);border-radius:2px;overflow:hidden}figure>img{max-width:100%;height:auto;display:block;margin:1rem auto;background:#fff}figcaption{padding:0 20px 18px;font-size:18px}.stamp{display:inline-block;margin:16px 20px 0;border:1px solid currentColor;border-radius:2px;padding:5px 10px;font-size:15px;font-weight:700}.s-ok{color:var(--ok);background:var(--okbg)}.s-hold{color:var(--hold);background:var(--h1)}.s-reject{color:var(--red);background:var(--redbg)}
table{border-collapse:collapse;width:100%;font-size:16px;font-variant-numeric:tabular-nums}caption{text-align:left;font-weight:700;color:var(--muted);padding-bottom:8px}th,td{border-bottom:1px solid var(--ruling);padding:8px 10px;text-align:left}thead th{border-bottom:2px solid var(--fg)}.twrap{overflow:auto;margin:1rem 0;max-width:100%}details summary{cursor:pointer;color:var(--acc);font-weight:700;padding:10px 0;min-height:44px}.speaking{background:var(--hl);outline:2px solid var(--acc);outline-offset:3px}img.deco{height:1.6em;width:auto}
@media(max-width:500px){.bar{padding:8px 10px;gap:6px}.bar b{font-size:16px}.bar button{padding:10px;font-size:14px}.bar summary{font-size:14px}.bar .settings{flex:1 1 100%}main{padding:1rem 16px 4rem}h1{font-size:1.7rem}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""

# Sumber pemutar yang sama ditanam agar HTML tetap mandiri tanpa server.
SPEECH_JS = (Path(__file__).resolve().parent.parent / "web" / "speech.js").read_text(encoding="utf-8")
JS = SPEECH_JS + """
const blocks=[...document.querySelectorAll('[data-say]')];let i=0,playing=false;
const st=document.getElementById('st'),selR=document.getElementById('rate'),selV=document.getElementById('voice');
const reader=new SimakSpeech();selV.disabled=true;
reader.ready.then(()=>{if(reader.available)selV.add(new Option('ElevenLabs · suara pilihan','eleven'));selV.value=reader.pref.suara;selR.value=reader.pref.kecepatan;selV.disabled=false;});
function stopAll(){reader.stop()}
function mark(){blocks.forEach(b=>b.classList.remove('speaking'));const b=blocks[i];if(b){b.classList.add('speaking');b.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}}
function fail(e){playing=false;st.textContent=e.message+' Teks tetap tersedia.';document.getElementById('play').setAttribute('aria-pressed','false');}
function speak(){stopAll();if(!blocks.length){playing=false;st.textContent='Dokumen tidak memiliki bagian yang dapat dibacakan.';return}if(i>=blocks.length){i=Math.max(0,blocks.length-1);playing=false;st.textContent='Selesai dibacakan';document.getElementById('play').setAttribute('aria-pressed','false');return}
mark();st.textContent='Menyiapkan bagian '+(i+1)+' dari '+blocks.length;
reader.speak(blocks[i].dataset.say,()=>{if(playing){i++;speak()}},fail,()=>{st.textContent='Membacakan bagian '+(i+1)+' dari '+blocks.length;});}
selR.onchange=selV.onchange=()=>{stopAll();reader.pref.suara=selV.value;reader.pref.kecepatan=+selR.value;reader.save();if(playing)speak()};
document.getElementById('play').onclick=()=>{if(i>=blocks.length-1&&st.textContent==='Selesai dibacakan')i=0;playing=true;document.getElementById('play').setAttribute('aria-pressed','true');speak()};
document.getElementById('pause').onclick=()=>{playing=false;stopAll();document.getElementById('play').setAttribute('aria-pressed','false');st.textContent=blocks.length?'Dijeda pada bagian '+(i+1):'Dokumen kosong';};
document.getElementById('prev').onclick=()=>{i=Math.max(0,i-1);if(playing)speak();else mark()};
document.getElementById('next').onclick=()=>{i=Math.min(blocks.length-1,i+1);if(playing)speak();else mark()};
blocks.forEach((b,k)=>b.addEventListener('dblclick',()=>{i=k;playing=true;speak()}));
window.addEventListener('pagehide',()=>{playing=false;stopAll()});
"""


_ICONS = {"play": '<path d="M8 5.5v13l11-6.5z"/>', "pause": '<path d="M8 5v14M16 5v14"/>',
          "prev": '<path d="M18 6l-8 6 8 6zM6 6v12"/>', "next": '<path d="M6 6l8 6-8 6zM18 6v12"/>'}


def _ic(name: str) -> str:
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{_ICONS[name]}</svg>'


def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)


def _data_table(el) -> str:
    sat = el["ext"].get("satuan") or ""
    rows = "".join(f"<tr><th scope='row'>{esc(r['kategori'])}</th><td>{fmt(r['nilai'])}</td></tr>" for r in el["table"])
    return (f"<details><summary>Tabel data grafik</summary><div class='twrap' tabindex='0' role='region' aria-label='Tabel data grafik'><table><caption>Data yang mendasari grafik"
            f"{' (' + esc(sat) + ')' if sat else ''}</caption><thead><tr><th scope='col'>{esc(el['ext'].get('label_x') or 'Kategori')}</th>"
            f"<th scope='col'>{esc(el['ext'].get('label_y') or 'Nilai')}</th></tr></thead><tbody>{rows}</tbody></table></details>")


def build_html(state: dict, alt_for) -> str:
    parts, n_ok, n_wait, n_reject, fig_no, tab_no = [], 0, 0, 0, 0, 0
    for el in state["elements"]:
        k = el["kind"]
        if k == "heading":
            lv = el["level"]
            parts.append(f"<h{lv} data-say='{esc('Judul. ' + el['text'])}'>{esc(el['text'])}</h{lv}>")
        elif k == "paragraph":
            parts.append(f"<p data-say='{esc(el['text'])}'>{esc(el['text'])}</p>")
        elif k == "table":
            tab_no += 1
            rows = el["rows"]
            head = "".join(f"<th scope='col'>{esc(c)}</th>" for c in rows[0])
            body = "".join("<tr>" + "".join((f"<th scope='row'>{esc(c)}</th>" if j == 0 else f"<td>{esc(c)}</td>")
                                            for j, c in enumerate(r)) + "</tr>" for r in rows[1:])
            say = f"Tabel {tab_no}, {len(rows) - 1} baris. Kolom: {', '.join(rows[0])}. " + " ".join(
                f"Baris {i + 1}: " + "; ".join(f"{h} {c}" for h, c in zip(rows[0], r)) + "." for i, r in enumerate(rows[1:]))
            parts.append(f"<div class='twrap' tabindex='0' role='region' aria-label='Tabel {tab_no}'><table data-say='{esc(say)}'><caption>Tabel {tab_no}</caption><thead><tr>{head}</tr></thead>"
                         f"<tbody>{body}</tbody></table></div>")
        elif k == "image":
            img_path = Path(state.get("_job", "")) / "img" / f"{el['id']}.png"
            src = ""
            if img_path.exists():
                src = "data:image/png;base64," + base64.b64encode(img_path.read_bytes()).decode()
            st = el.get("status")
            if st == "dekoratif":
                parts.append(f"<img class='deco' src='{src}' alt=''>")
                continue
            fig_no += 1
            alt = alt_for(el)
            if st == "terbit_otomatis":
                n_ok += 1
                badge = "<span class='stamp s-ok'>Dihasilkan otomatis · angka terverifikasi</span>"
                body = f"<p>{esc(el['alt_auto'])}</p>" + _data_table(el)
                say = f"Gambar {fig_no}. {el['alt_auto']}"
            elif st in ("disetujui", "diubah"):
                n_ok += 1
                badge = "<span class='stamp s-ok'>" + ("Diubah dan disetujui ULD" if st == "diubah" else "Disetujui ULD") + "</span>"
                body = f"<p>{esc(el['alt_final'])}</p>" + (_data_table(el) if el.get("table") else "")
                say = f"Gambar {fig_no}. {el['alt_final']}"
            elif st == "ditolak":
                n_reject += 1
                badge = "<span class='stamp s-reject'>Ditolak ULD · deskripsi belum tersedia</span>"
                body = "<p>Deskripsi ditolak ULD. Gambar ini belum memiliki uraian yang dapat dipercaya.</p>"
                say = f"Gambar {fig_no}. Deskripsi ditolak Unit Layanan Disabilitas; uraian belum tersedia."
            else:
                n_wait += 1
                badge = "<span class='stamp s-hold'>Menunggu tinjauan ULD</span>"
                body = "<p>Deskripsi gambar ini belum dapat diverifikasi otomatis dan sedang ditinjau Unit Layanan Disabilitas.</p>"
                say = f"Gambar {fig_no}. {el.get('jenis', 'gambar')}, menunggu tinjauan Unit Layanan Disabilitas."
            parts.append(f"<figure data-say='{esc(say)}'>{badge}<img src='{src}' alt='{esc(alt)}'>"
                         f"<figcaption><strong>Gambar {fig_no}.</strong> {body}</figcaption></figure>")
    notice = (f"<div class='notice' role='note'>Dokumen ini diremediasi oleh SIMAK. {n_ok} gambar memiliki deskripsi "
              f"terverifikasi atau disetujui ULD; {n_wait} gambar menunggu tinjauan; {n_reject} deskripsi ditolak. Deskripsi berlabel "
              f"<em>dihasilkan otomatis</em> dibangun dari tabel data dengan statistik yang dihitung kode.</div>")
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(state['title'])}</title>
<style>{_FONT_FACE}{CSS}</style></head><body><a class="skip" href="#isi">Lompat ke isi</a>
<div class="bar" role="region" aria-label="Mode dengar"><b>SIMAK.</b>
<button id="play" aria-pressed="false">{_ic('play')}Putar</button><button id="pause">{_ic('pause')}Jeda</button>
<button id="prev" aria-label="Bagian sebelumnya">{_ic('prev')}</button><button id="next" aria-label="Bagian berikutnya">{_ic('next')}</button>
<details class="settings"><summary>Pengaturan suara</summary><div><label>Suara <select id="voice"><option value="peramban" selected>Peramban (id-ID)</option></select></label>
<label>Kecepatan <select id="rate"><option value="-20">−20%</option><option value="-10">−10%</option><option value="0" selected>normal</option><option value="10">+10%</option><option value="20">+20%</option></select></label><p>ElevenLabs dipilih otomatis saat server siap. Teks yang diputar dikirim ke layanan suara. Pilih Peramban untuk suara perangkat atau saat membaca tanpa server.</p></div></details>
<span class="st" id="st" aria-live="polite"></span></div>
<main id="isi">{notice}{''.join(parts)}</main><script>{JS}</script></body></html>"""
