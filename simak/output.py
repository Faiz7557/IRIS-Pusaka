"""OUT-01/OUT-02: HTML aksesibel dengan penanda status dan mode dengar (Web Speech API, id-ID)."""
import base64
import html
from pathlib import Path

from .chart import fmt

_FONT = Path(__file__).resolve().parent.parent / "web" / "fonts" / "AtkinsonHyperlegibleNext-normal-latin.woff2"
_FONT_FACE = ("@font-face{font-family:'Atkinson Hyperlegible Next';font-weight:200 800;font-display:swap;"
              "src:url(data:font/woff2;base64," + base64.b64encode(_FONT.read_bytes()).decode() + ") format('woff2')}"
              ) if _FONT.exists() else ""

# Dunia kartu katalog yang sama dengan antarmuka ULD; mengikuti preferensi terang/gelap pembaca.
CSS = """
:root{--rail:#1F4D3A;--rail-ink:#EEF4F0;--bg:#F3F6F4;--card:#fff;--fg:#1B1F1D;--muted:#47524C;--line:#C9D4CE;
--ruling:#DCE6F3;--red:#B3261E;--ok:#1F6B45;--okbg:#E2F1E7;--hold:#4A2C8C;--h1:#EEE8FA;--h2:#E0D5F5;--acc:#2F5BA8;--hl:#FFF0A6}
@media (prefers-color-scheme:dark){:root{--bg:#141816;--card:#1C211E;--fg:#E8EFEA;--muted:#A9B6AE;--line:#33403A;
--ruling:#2A3540;--ok:#7FD3A3;--okbg:#17321F;--hold:#CDBAF7;--h1:#2A2140;--h2:#33284F;--acc:#9DBBF2;--hl:#4B4312}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:400 18px/1.7 "Atkinson Hyperlegible Next","Segoe UI",system-ui,sans-serif}
::selection{background:var(--h2)}:focus-visible{outline:3px solid var(--acc);outline-offset:2px;border-radius:3px}
.skip{position:absolute;left:-999px}.skip:focus{left:16px;top:8px;background:var(--card);padding:8px 12px;z-index:9;font-weight:700}
main{max-width:46rem;margin:0 auto;padding:1.5rem 16px 6rem}
h1{font-size:2rem;line-height:1.2;font-weight:800}h2{font-size:1.45rem;line-height:1.25}h1,h2,h3{text-wrap:balance}
.bar{position:sticky;top:0;z-index:5;background:var(--rail);color:var(--rail-ink);padding:.6rem 16px;
display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}
.bar b{font-weight:800;letter-spacing:.02em;margin-right:.5rem}
.bar button,.bar select{font-family:inherit;font-weight:700;font-size:15px;line-height:1.2;min-height:44px;padding:.45rem .85rem;border:1.5px solid rgba(238,244,240,.4);
border-radius:4px;background:transparent;color:var(--rail-ink);cursor:pointer;display:inline-flex;align-items:center;gap:.4rem}
.bar button:hover{background:rgba(0,0,0,.18)}.bar button#play{background:var(--rail-ink);color:var(--rail)}
.bar select option{color:#1B1F1D}.bar label{font-size:15px;display:inline-flex;gap:.4rem;align-items:center}
.bar :focus-visible{outline-color:var(--rail-ink)}
.bar .st{font-size:14px;opacity:.9}
.icon{width:1.1em;height:1.1em;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.notice{background:var(--card);border:1.5px solid var(--line);border-radius:4px;padding:.9rem 1.1rem;font-size:16px;margin:1rem 0 1.5rem}
figure{margin:1.75rem 0;background:var(--card);border:1.5px solid var(--line);border-radius:4px;overflow:hidden}
figure::before{content:"";display:block;height:5px;background:var(--red)}
figure>img{max-width:100%;height:auto;display:block;margin:1rem auto;background:#fff}
figcaption{padding:0 1.1rem 1rem;font-size:17px}
.stamp{display:inline-block;margin:1rem 1.1rem 0;border:2.5px solid currentColor;border-radius:3px;padding:.2rem .6rem;
font-size:15px;font-weight:800;letter-spacing:.02em;transform:rotate(-1.5deg)}
.s-ok{color:var(--ok)}.s-hold{color:var(--hold);border-style:dashed;
background:repeating-linear-gradient(135deg,var(--h1) 0 8px,var(--h2) 8px 16px)}
table{border-collapse:collapse;margin:.6rem 0;font-size:16px;font-variant-numeric:tabular-nums}
caption{text-align:left;font-weight:700;color:var(--muted);padding-bottom:.3rem}
th,td{border-bottom:1.5px solid var(--ruling);padding:.35rem .7rem;text-align:left}thead th{border-bottom:2px solid var(--fg)}
details summary{cursor:pointer;color:var(--acc);font-weight:700;padding:.3rem 0}
.speaking{background:var(--hl);outline:3px solid var(--hl);border-radius:3px}
img.deco{height:1.6em;width:auto}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""

JS = """
const blocks=[...document.querySelectorAll('[data-say]')];let i=0,playing=false,audio=null,ctl=null;
const st=document.getElementById('st'),selV=document.getElementById('voice'),selR=document.getElementById('rate');
const synth=window.speechSynthesis;
function bVoice(){const v=synth?synth.getVoices():[];return v.find(x=>/natural|online/i.test(x.name)&&x.lang.toLowerCase().startsWith('id'))||v.find(x=>x.lang.toLowerCase().startsWith('id'))||null}
try{const p=JSON.parse(localStorage.getItem('simak-suara')||'{}');if(p.suara)selV.value=p.suara;if(p.kecepatan!==undefined)selR.value=p.kecepatan}catch(e){}
// Suara server (Satya, Ardi) hanya tersedia bila halaman dibuka dari aplikasi SIMAK.
fetch('/api/suara/daftar').then(r=>{if(!r.ok)throw 0;return r.json()}).then(l=>{if(l.some(s=>s.id==='eleven'))return;const o=selV.querySelector('option[value=eleven]');if(o)o.remove();if(selV.value==='eleven')selV.value='satya'}).catch(()=>{[...selV.options].forEach(o=>{if(o.value!=='peramban')o.remove()});selV.value='peramban'});
function save(){try{localStorage.setItem('simak-suara',JSON.stringify({suara:selV.value,kecepatan:+selR.value,nada:0}))}catch(e){}}
function stopAll(){if(ctl)ctl.abort();ctl=null;if(audio){audio.pause();audio=null}if(synth)synth.cancel()}
function mark(){blocks.forEach(b=>b.classList.remove('speaking'));const b=blocks[i];if(b){b.classList.add('speaking');b.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}}
function next(){if(playing){i++;speak()}}
async function speak(){stopAll();if(i>=blocks.length){playing=false;st.textContent='Selesai dibacakan';return}
mark();const text=blocks[i].dataset.say,rate=+selR.value;st.textContent='Membacakan bagian '+(i+1)+' dari '+blocks.length;
if(selV.value==='peramban'){const u=new SpeechSynthesisUtterance(text);u.lang='id-ID';const v=bVoice();if(v)u.voice=v;u.rate=1+rate/100;u.onend=next;synth.speak(u);return}
const c=new AbortController();ctl=c;
try{const r=await fetch('/api/suara',{method:'POST',headers:{'Content-Type':'application/json'},signal:c.signal,body:JSON.stringify({teks:text,suara:selV.value,kecepatan:rate,nada:0})});
if(!r.ok)throw new Error(r.status);const url=URL.createObjectURL(await r.blob());if(ctl!==c)return;
const a=new Audio(url);audio=a;a.onended=()=>{URL.revokeObjectURL(url);if(audio===a){audio=null;next()}};await a.play()}
catch(e){if(e.name!=='AbortError'){playing=false;st.textContent='Suara gagal dibuat; pilih "Suara peramban".'}}}
function prefetch(){if(selV.value==='peramban')return;fetch('/api/suara/siapkan',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({teks:blocks.map(b=>b.dataset.say),suara:selV.value,kecepatan:+selR.value,nada:0})}).catch(()=>{})}
selV.onchange=selR.onchange=()=>{save();stopAll();if(playing)speak();prefetch()};
document.getElementById('play').onclick=()=>{playing=true;speak()};
document.getElementById('pause').onclick=()=>{playing=false;stopAll();st.textContent='Dijeda pada bagian '+(i+1)};
document.getElementById('prev').onclick=()=>{i=Math.max(0,i-1);if(playing)speak();else mark()};
document.getElementById('next').onclick=()=>{i=Math.min(blocks.length-1,i+1);if(playing)speak();else mark()};
blocks.forEach((b,k)=>b.addEventListener('dblclick',()=>{i=k;playing=true;speak()}));
setTimeout(prefetch,800);
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
    return (f"<details><summary>Tabel data grafik</summary><table><caption>Data yang mendasari grafik"
            f"{' (' + esc(sat) + ')' if sat else ''}</caption><thead><tr><th scope='col'>{esc(el['ext'].get('label_x') or 'Kategori')}</th>"
            f"<th scope='col'>{esc(el['ext'].get('label_y') or 'Nilai')}</th></tr></thead><tbody>{rows}</tbody></table></details>")


def build_html(state: dict, alt_for) -> str:
    parts, n_ok, n_wait, fig_no, tab_no = [], 0, 0, 0, 0
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
            parts.append(f"<table data-say='{esc(say)}'><caption>Tabel {tab_no}</caption><thead><tr>{head}</tr></thead>"
                         f"<tbody>{body}</tbody></table>")
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
                badge = "<span class='stamp s-ok'>Disetujui ULD</span>"
                body = f"<p>{esc(el['alt_final'])}</p>" + (_data_table(el) if el.get("table") else "")
                say = f"Gambar {fig_no}. {el['alt_final']}"
            else:
                n_wait += 1
                badge = "<span class='stamp s-hold'>Menunggu tinjauan ULD</span>"
                body = "<p>Deskripsi gambar ini belum dapat diverifikasi otomatis dan sedang ditinjau Unit Layanan Disabilitas.</p>"
                say = f"Gambar {fig_no}. {el.get('jenis', 'gambar')}, menunggu tinjauan Unit Layanan Disabilitas."
            parts.append(f"<figure data-say='{esc(say)}'>{badge}<img src='{src}' alt='{esc(alt)}'>"
                         f"<figcaption><strong>Gambar {fig_no}.</strong> {body}</figcaption></figure>")
    notice = (f"<div class='notice' role='note'>Dokumen ini diremediasi oleh SIMAK. {n_ok} gambar memiliki deskripsi "
              f"terverifikasi atau disetujui ULD; {n_wait} gambar menunggu tinjauan. Deskripsi berlabel "
              f"<em>dihasilkan otomatis</em> dibangun dari tabel data dengan statistik yang dihitung kode.</div>")
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(state['title'])}</title>
<style>{_FONT_FACE}{CSS}</style></head><body><a class="skip" href="#isi">Lompat ke isi</a>
<div class="bar" role="region" aria-label="Mode dengar"><b>SIMAK</b>
<button id="play">{_ic('play')}Putar</button><button id="pause">{_ic('pause')}Jeda</button>
<button id="prev" aria-label="Bagian sebelumnya">{_ic('prev')}</button><button id="next" aria-label="Bagian berikutnya">{_ic('next')}</button>
<label>Suara <select id="voice"><option value="satya" selected>Satya (sintetis, dengan izin)</option><option value="gadis">Gadis (neural, perempuan)</option><option value="ardi">Ardi (neural, laki-laki)</option><option value="eleven">Suara manusia (ElevenLabs, berbayar)</option><option value="peramban">Suara peramban</option></select></label>
<label>Kecepatan <select id="rate"><option value="-20">−20%</option><option value="-10">−10%</option><option value="0" selected>normal</option><option value="10">+10%</option><option value="20">+20%</option><option value="35">+35%</option></select></label>
<span class="st" id="st" aria-live="polite"></span></div>
<main id="isi">{notice}{''.join(parts)}</main><script>{JS}</script></body></html>"""
