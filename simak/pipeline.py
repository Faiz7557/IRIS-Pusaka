"""Pipeline remediasi SIMAK: PDF apa adanya → elemen berstatus → PDF bertag + HTML.

Setiap elemen adalah satu rekaman JSON (Lampiran E) sehingga gerbang, antarmuka
tinjauan, dan perakit keluaran memakai satu model data.
"""
import hashlib
import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fitz

from . import chart, gate, pdfa11y, vlm
from .config import thresholds

DRAFT_PROMPT = (
    "Tuliskan draf teks alternatif berbahasa Indonesia (maksimal 3 kalimat) untuk gambar ini "
    "dari materi kuliah. Jika gambar berupa rumus matematika, tulis LaTeX-nya di baris pertama "
    "diawali 'LaTeX:' lalu cara membacanya dalam bahasa Indonesia diawali 'Ucapan:'. Tanpa markdown."
)


def _flatten(kids, out):
    for k in kids:
        t = k.get("type")
        if t in ("heading", "paragraph", "caption", "image", "list item", "table"):
            out.append(k)
        for key in ("kids", "list items"):
            if isinstance(k.get(key), list):
                _flatten(k[key], out)


def _rect(page, bbox):
    h = page.rect.height
    x0, y0, x1, y1 = bbox
    return fitz.Rect(x0, h - y1, x1, h - y0)


def _blocks(odl_json: Path, pdf: fitz.Document) -> list[dict]:
    """Blok berurutan dari OpenDataLoader; tabel yang terlewat auto-tag dilengkapi PyMuPDF."""
    j = json.loads(odl_json.read_text(encoding="utf-8"))
    flat = []
    _flatten(j.get("kids", []), flat)
    tables = {}
    for pno, page in enumerate(pdf, start=1):
        for t in page.find_tables().tables:
            rows = [[(c or "").strip() for c in r] for r in t.extract()]
            if len(rows) >= 2 and len(rows[0]) >= 2:
                tables.setdefault(pno, []).append({"rect": fitz.Rect(t.bbox), "rows": rows, "used": False})
    blocks = []
    for k in flat:
        pno = int(k.get("page number", 1))
        page = pdf[pno - 1]
        r = _rect(page, k.get("bounding box", [0, 0, 0, 0]))
        hit = next((t for t in tables.get(pno, []) if t["rect"].contains(fitz.Point((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))), None)
        if hit and k["type"] != "image":
            if not hit["used"]:
                hit["used"] = True
                blocks.append({"kind": "table", "page": pno, "rows": hit["rows"], "source": "pymupdf"})
            continue
        if k["type"] == "table":
            rows = []
            for row in k.get("rows", []):
                rows.append([" ".join(p.get("content", "") for p in c.get("kids", [])) for c in row.get("cells", [])])
            blocks.append({"kind": "table", "page": pno, "rows": rows, "source": "odl"})
        elif k["type"] == "image":
            blocks.append({"kind": "image", "page": pno, "bbox": list(r), "odl_id": k.get("id")})
        elif k["type"] == "heading":
            lvl = int(k.get("heading level") or 2)
            blocks.append({"kind": "heading", "level": min(max(lvl, 1), 6), "page": pno, "text": k.get("content", "")})
        else:
            txt = k.get("content", "")
            if txt.strip():
                blocks.append({"kind": "paragraph", "page": pno, "text": txt})
    return blocks


def _classify_decorative(blocks, pdf):
    hashes = {}
    for b in blocks:
        if b["kind"] != "image":
            continue
        page = pdf[b["page"] - 1]
        rect = fitz.Rect(b["bbox"])
        pix = page.get_pixmap(clip=rect, dpi=150)
        b["png"] = pix.tobytes("png")
        b["hash"] = hashlib.md5(page.get_pixmap(clip=rect, dpi=24).samples).hexdigest()
        b["area"] = rect.get_area() / page.rect.get_area()
        hashes[b["hash"]] = hashes.get(b["hash"], 0) + 1
    for b in blocks:
        if b["kind"] == "image":
            b["decorative"] = b["area"] < 0.01 or (hashes[b["hash"]] >= 2 and b["area"] < 0.05)


def process_image(el: dict, th: dict) -> dict:
    """CLS-01 → CHT-01/02 → GAT-01 untuk satu gambar."""
    img = el.pop("png_bytes")
    if el.get("decorative"):
        el.update(jenis="dekoratif", status="dekoratif", checks={}, reasons=["Disaring heuristik ukuran/pengulangan"])
        return el
    e1 = vlm.extract_table(img, 1)
    el["jenis"] = e1.get("jenis", "foto")
    if el["jenis"] == "dekoratif":
        el.update(status="dekoratif", checks={}, reasons=["VLM: gambar dekoratif"])
        return el
    if el["jenis"] == "grafik" and e1.get("data"):
        e2 = vlm.extract_table(img, 2)
        t1, t2 = chart.to_table(e1), chart.to_table(e2)
        el["ext"] = {k: e1.get(k) for k in ("jenis_grafik", "judul", "label_x", "label_y", "satuan", "banyak_seri")}
        el["T1"], el["T2"], el["table"] = t1, t2, t1
        el["delta"] = chart.delta(t1, t2)
        el["axis_ok"], el["axis_msg"] = chart.axis_check(t1, e2.get("tik_min"), e2.get("tik_max"))
        el["label_tertulis"] = bool(e1.get("label_nilai_tertulis")) and bool(e2.get("label_nilai_tertulis"))
        if (e1.get("banyak_seri") or 1) > 1:
            el["axis_ok"], el["axis_msg"] = False, "grafik multi-seri di luar lingkup level 1–3"
        el["seg"], el["claims"], el["D"] = chart.build_description(e1, t1, th["rho"])
        el["alt_auto"] = chart.render(el["seg"])
        gate.evaluate(el, th)
    else:
        el["draft"] = vlm.describe_draft(img, DRAFT_PROMPT)
        gate.evaluate(el, th)
    return el


def process_or_hold(el: dict, th: dict) -> dict:
    """Tanpa VLM (key kosong atau kuota habis), gambar ditahan untuk ULD; dokumen tetap selesai (fail-closed)."""
    try:
        return process_image(el, th)
    except vlm.QuotaHabis as e:
        el.update(jenis=el.get("jenis", "gambar"), status="antrean", checks={},
                  reasons=[f"VLM tidak tersedia ({e}); ditahan untuk tinjauan ULD"])
        return el


HELD_FIGURE_ALT = ("[Menunggu tinjauan ULD] Gambar yang belum dapat diproses otomatis "
                   "(mis. figur vektor); deskripsi belum diverifikasi.")


def _struct_src(job: Path) -> Path:
    """PDF yang pohon strukturnya ditambal: keluaran auto-tag, atau PDF asli bila sudah bertag."""
    src = job / "odl" / "asli_tagged.pdf"
    return src if src.exists() else job / "asli.pdf"


def _vector_figures(job: Path, doc, els: list) -> list:
    """Figure bertag tanpa citra raster (figur vektor dari Word/PowerPoint) menjadi elemen antrean ULD.

    K = ∅ (data jalur vektor belum dibaca), jadi selalu ditahan. Pada halaman tanpa citra raster, urutan
    Figure pada pohon struktur = urutan kartu, sehingga keputusan ULD dapat ditanam ke PDF. Pada halaman
    campuran urutannya tidak dapat dipastikan: PDF tetap berpenanda tahan, keputusan ULD hanya masuk HTML.
    """
    raster = {}
    for e in els:
        if e["kind"] == "image":
            raster[e["page"]] = raster.get(e["page"], 0) + 1
    out = []
    for n, boxes in sorted(pdfa11y.figure_boxes(_struct_src(job)).items()):
        extra = len(boxes) - raster.get(n, 0)
        if extra <= 0 or n > doc.page_count:
            continue
        page = doc[n - 1]
        campuran = raster.get(n, 0) > 0
        # ponytail: pada halaman campuran Figure mana yang vektor tidak diketahui; pratinjau seluruh halaman.
        cand = [None] * extra if campuran else boxes
        for k, bb in enumerate(cand):
            el_id = f"v{n:03d}{k:02d}"
            clip = None
            if bb:
                r = fitz.Rect(bb) * page.transformation_matrix & page.rect  # ruang PDF → ruang halaman
                clip = r if r.get_area() >= 0.005 * page.rect.get_area() else None
            pix = page.get_pixmap(clip=clip, dpi=150 if clip else 90)
            (job / "img").mkdir(exist_ok=True)
            (job / "img" / f"{el_id}.png").write_bytes(pix.tobytes("png"))
            vektor_murni = not page.get_images()
            reasons = ["Figur vektor tanpa citra raster: data jalur vektor belum dibaca (K = ∅), ditahan untuk ULD"
                       if vektor_murni else
                       "Figure bertag tanpa citra yang terdeteksi tata letak, tidak dapat diverifikasi (K = ∅); "
                       "ditahan untuk ULD"]
            if campuran:
                reasons.append("Halaman ini juga memuat citra raster sehingga urutan Figure tidak dapat dipastikan; "
                               "di PDF bertag figur tetap berpenanda tahan, keputusan ULD diterapkan pada HTML")
            if not clip:
                reasons.append(f"Pratinjau menampilkan seluruh halaman karena letak figur tidak tercatat "
                               f"(figur ke-{k + 1} dari {len(cand)} pada halaman ini)")
            out.append({"id": el_id, "kind": "image", "page": n, "vektor": True, "campuran": campuran,
                        "jenis": "figur vektor" if vektor_murni else "figur", "status": "antrean", "checks": {},
                        "reasons": reasons})
    return out


def alt_for(el: dict) -> str:
    """Teks alternatif yang ditanam ke keluaran, selalu dengan penanda statusnya."""
    st = el.get("status")
    if st == "dekoratif":
        return "Hiasan (dekoratif)"
    if st == "terbit_otomatis":
        return "[Dihasilkan otomatis, angka terverifikasi terhadap data] " + el["alt_auto"]
    if st in ("disetujui", "diubah"):
        return f"[Disetujui ULD] {el['alt_final']}"
    if st == "ditolak":
        return "[Ditolak ULD] Gambar ini belum memiliki deskripsi yang dapat dipercaya."
    jenis = el.get("jenis", "gambar")
    return f"[Menunggu tinjauan ULD] {jenis.capitalize()} pada halaman {el['page']}; deskripsi belum diverifikasi."


def run(pdf_path: Path, job: Path, progress=lambda *a: None) -> dict:
    t0 = time.time()
    th = thresholds()
    job.mkdir(parents=True, exist_ok=True)
    orig = job / "asli.pdf"
    if pdf_path.resolve() != orig.resolve():
        shutil.copy(pdf_path, orig)
    progress("struktur", "Menganalisis tata letak dan auto-tag (OpenDataLoader)")
    tagged_in = pdfa11y.is_tagged(orig)
    odl_json, tagged = pdfa11y.autotag(orig, job / "odl", use_struct_tree=tagged_in)
    b1 = tagged if tagged else orig  # PDF bertag: pakai tag yang ada
    t_struct = time.time() - t0

    doc = fitz.open(orig)
    blocks = _blocks(odl_json, doc)
    _classify_decorative(blocks, doc)
    title = next((b["text"] for b in blocks if b["kind"] == "heading"), None) or doc.metadata.get("title") or orig.stem
    els = []
    for i, b in enumerate(blocks):
        b["id"] = f"e{i:03d}"
        if b["kind"] == "image":
            b["png_bytes"] = b.pop("png")
            (job / "img").mkdir(exist_ok=True)
            (job / "img" / f"{b['id']}.png").write_bytes(b["png_bytes"])
        els.append(b)
    imgs = [e for e in els if e["kind"] == "image"]
    progress("gambar", f"Mengklasifikasi dan mendeskripsikan {len(imgs)} gambar")
    done = 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for _ in ex.map(lambda e: process_or_hold(e, th), imgs):
            done += 1
            progress("gambar", f"Gambar {done}/{len(imgs)} selesai")
    for e in els:
        e.pop("png_bytes", None)
    for v in _vector_figures(job, doc, els):  # sisipkan setelah blok terakhir di halamannya (urutan baca)
        i = max((j for j, e in enumerate(els) if e["page"] <= v["page"]), default=-1)
        els.insert(i + 1, v)

    state = {"title": title, "file": pdf_path.name, "tagged_input": tagged_in, "elements": els,
             "thresholds": th, "manifest": vlm.manifest(), "pages": doc.page_count,
             "timing": {"struktur_s": round(t_struct, 2)}}
    doc.close()
    progress("rakit", "Merakit PDF bertag dan HTML, lalu validasi veraPDF")
    assemble(job, state)
    rep = {}
    for name, f in (("B0", orig), ("B1", b1), ("D", job / "simak.pdf")):
        rep[name] = {"verapdf": pdfa11y.verapdf(f), "g1": pdfa11y.g1_audit(f)}
    state["report"] = rep
    state["timing"]["total_s"] = round(time.time() - t0, 2)
    save(job, state)
    progress("selesai", "Selesai")
    return state


def assemble(job: Path, state: dict):
    from .output import build_html
    state["_job"] = str(job)
    alts_by_page: dict[int, list] = {}
    for e in state["elements"]:
        if e["kind"] == "image" and not e.get("campuran"):
            alts_by_page.setdefault(e["page"], []).append(alt_for(e))
    state["patch"] = pdfa11y.patch(_struct_src(job), job / "simak.pdf", state["title"], alts_by_page, HELD_FIGURE_ALT)
    for e in state["elements"]:  # status mengikuti isi PDF: halaman tidak cocok berarti ditahan
        if e["kind"] == "image" and e["page"] in state["patch"]["halaman_tidak_cocok"] and e["status"] == "terbit_otomatis":
            e["status"] = "antrean"
            e.setdefault("reasons", []).append("Halaman memuat figur yang tidak dapat dipasangkan dengan citra; "
                                               "ditahan agar deskripsi tidak terpasang pada gambar lain")
    (job / "simak.html").write_text(build_html(state, alt_for), encoding="utf-8")


def save(job: Path, state: dict):
    (job / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def load(job: Path) -> dict:
    return json.loads((job / "state.json").read_text(encoding="utf-8"))


def review(job: Path, el_id: str, aksi: str, alt: str = "") -> dict:
    """REV-01: keputusan ULD — setujui, ubah, tolak, atau tandai dekoratif."""
    state = load(job)
    el = next(e for e in state["elements"] if e["id"] == el_id)
    if aksi == "setujui":
        el["alt_final"] = alt or el.get("alt_auto") or el.get("draft", "")
        if not el["alt_final"].strip():  # figur vektor tidak punya draf: ULD wajib menulis deskripsinya
            raise ValueError("Teks alternatif tidak boleh kosong")
        el["status"] = "disetujui"
    elif aksi == "ubah":
        el["alt_final"], el["status"] = alt, "diubah"
    elif aksi == "tolak":
        el["status"] = "ditolak"
    elif aksi == "dekoratif":
        el["status"] = "dekoratif"
    el.setdefault("log", []).append({"aksi": aksi, "waktu": time.strftime("%Y-%m-%d %H:%M:%S")})
    assemble(job, state)
    rep = state.setdefault("report", {})
    rep["D"] = {"verapdf": pdfa11y.verapdf(job / "simak.pdf"), "g1": pdfa11y.g1_audit(job / "simak.pdf")}
    save(job, state)
    return el
