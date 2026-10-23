"""STR-01 dan OUT-01: auto-tag (OpenDataLoader), penambalan struktur dengan
pikepdf, dan validasi veraPDF (profil PDF/UA-1).

Penambalan mengikuti Lampiran D: Lang, MarkInfo/Marked, DisplayDocTitle, Title
(Info dan XMP), kunci Tabs per halaman, pdfuaid:part = 1, /Alt pada Figure, dan
baris pertama tabel menjadi sel TH karena keluaran auto-tag tidak memuatnya.
"""
import json
import os
import re
import subprocess
from pathlib import Path

import pikepdf

from .config import TOOLS, java_bin

_JAVA_DIR = str(Path(java_bin()).parent)
if _JAVA_DIR not in os.environ.get("PATH", ""):
    os.environ["PATH"] = _JAVA_DIR + os.pathsep + os.environ.get("PATH", "")

PLACEHOLDER = re.compile(r"^\s*(image|img|gambar|grafik|figure|picture|foto|chart)?\s*[-_ ]?\d*\s*$"
                         r"|\.(png|jpe?g|gif|bmp|tiff?)\s*$", re.I)


HELD_PREFIXES = ("[Menunggu tinjauan ULD]", "[Ditolak ULD]")  # teks alt penanda dari pipeline.alt_for


def is_placeholder(alt) -> bool:
    """G1: teks alternatif dianggap tidak ada bila kosong atau teks pengisi."""
    return alt is None or not str(alt).strip() or bool(PLACEHOLDER.search(str(alt).strip()))


def is_tagged(pdf: Path) -> bool:
    with pikepdf.open(pdf) as p:
        mi = p.Root.get("/MarkInfo")
        return "/StructTreeRoot" in p.Root and bool(mi and mi.get("/Marked"))


def autotag(pdf: Path, outdir: Path, use_struct_tree: bool = False) -> tuple[Path, Path | None]:
    import opendataloader_pdf
    outdir.mkdir(parents=True, exist_ok=True)
    fmt = "json" if use_struct_tree else "json,tagged-pdf"
    opendataloader_pdf.convert(str(pdf), output_dir=str(outdir), format=fmt, quiet=True,
                               use_struct_tree=use_struct_tree, table_method="cluster")
    stem = pdf.stem
    tagged = outdir / f"{stem}_tagged.pdf"
    return outdir / f"{stem}.json", (tagged if tagged.exists() else None)


def verapdf(pdf: Path) -> dict:
    cp = str(TOOLS / "verapdf" / "bin" / "*")
    r = subprocess.run([java_bin(), "-cp", cp, "-Dfile.encoding=UTF8", "org.verapdf.apps.GreenfieldCliWrapper",
                        "--flavour", "ua1", "--format", "json", str(pdf)],
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    try:
        j = json.loads(r.stdout)
        res = j["report"]["jobs"][0]["validationResult"]
        res = res[0] if isinstance(res, list) else res
    except Exception:
        return {"error": (r.stderr or r.stdout)[-400:]}
    d = res["details"]
    rules = [{"clause": x["clause"], "test": x["testNumber"], "checks": x["failedChecks"],
              "desc": x["description"]} for x in d.get("ruleSummaries", [])]
    return {"compliant": res["compliant"], "failed_rules": d["failedRules"],
            "failed_checks": d["failedChecks"], "rules": rules}


def _struct_walk(node, out, depth=0, pg=None):
    """DFS pada pohon struktur; mengumpulkan Figure (beserta halamannya) dan Table sesuai urutan dokumen."""
    if depth > 60:
        return
    if isinstance(node, pikepdf.Array):
        for k in node:
            _struct_walk(k, out, depth + 1, pg)
        return
    if not isinstance(node, pikepdf.Dictionary):
        return
    pg = node.get("/Pg", pg)
    s = node.get("/S")
    if s == "/Figure":
        out["fig"].append(node)
        out.setdefault("fig_pg", []).append(pg)
    elif s == "/Table":
        out["table"].append(node)
    k = node.get("/K")
    if k is not None:
        _struct_walk(k, out, depth + 1, pg)


def _first_row_to_th(table) -> int:
    """Memetakan baris pertama tabel menjadi sel judul kolom (TH, Scope Column)."""
    def children(n):
        k = n.get("/K")
        if k is None:
            return []
        return list(k) if isinstance(k, pikepdf.Array) else [k]
    rows = []
    for c in children(table):
        if isinstance(c, pikepdf.Dictionary):
            if c.get("/S") == "/TR":
                rows.append(c)
            elif c.get("/S") in ("/THead", "/TBody"):
                rows += [r for r in children(c) if isinstance(r, pikepdf.Dictionary) and r.get("/S") == "/TR"]
    if not rows:
        return 0
    n = 0
    for cell in children(rows[0]):
        if isinstance(cell, pikepdf.Dictionary) and cell.get("/S") == "/TD":
            cell.S = pikepdf.Name.TH
            cell.A = pikepdf.Dictionary(O=pikepdf.Name.Table, Scope=pikepdf.Name.Column)
            n += 1
    return n


def _figs_by_page(p) -> tuple[dict, dict]:
    """Figure pada pohon struktur, dikelompokkan per nomor halaman (1-based) menurut urutan dokumen."""
    found = {"fig": [], "table": []}
    if "/StructTreeRoot" in p.Root:
        _struct_walk(p.Root.StructTreeRoot.get("/K"), found)
    page_no = {pg.obj.objgen: i + 1 for i, pg in enumerate(p.pages)}
    by_page: dict[int, list] = {}
    for fig, pg in zip(found["fig"], found.get("fig_pg", [])):
        by_page.setdefault(page_no.get(pg.objgen) if pg is not None else None, []).append(fig)
    return found, by_page


def _bbox(fig):
    """Atribut Layout /BBox sebuah Figure (koordinat PDF), bila ada."""
    attrs = fig.get("/A")
    for a in (attrs if isinstance(attrs, pikepdf.Array) else [attrs]):
        if isinstance(a, pikepdf.Dictionary) and isinstance(a.get("/BBox"), pikepdf.Array) and len(a.BBox) == 4:
            return [float(v) for v in a.BBox]
    return None


def figure_boxes(pdf: Path) -> dict:
    """{halaman: [bbox | None, …]} untuk setiap Figure bertag, dalam urutan pohon struktur."""
    with pikepdf.open(pdf) as p:
        return {n: [_bbox(f) for f in figs] for n, figs in _figs_by_page(p)[1].items() if n}


DECORATIVE_ALT = "Hiasan (dekoratif)"  # hanya bila Figure tidak dapat dijadikan Artifact
MATCH_IOU = 0.8


def _iou(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def _match_by_bbox(figs, entries) -> dict:
    """{indeks Figure: entri} untuk pasangan satu-satu dengan IoU ≥ MATCH_IOU; sisanya tidak dipasangkan."""
    boxes = [_bbox(f) for f in figs]
    cand = sorted(((_iou(fb, e["bbox"]), i, j) for i, fb in enumerate(boxes) if fb
                   for j, e in enumerate(entries) if e.get("bbox")), reverse=True)
    used_f, used_e, out = set(), set(), {}
    for iou, i, j in cand:
        if iou < MATCH_IOU:
            break
        if i not in used_f and j not in used_e:
            used_f.add(i), used_e.add(j)
            out[i] = entries[j]
    return out


def _mcids(fig, page) -> list | None:
    """MCID langsung milik Figure pada halamannya; None bila bentuk /K tidak sederhana (objek, stream lain)."""
    k = fig.get("/K")
    out = []
    for c in (list(k) if isinstance(k, pikepdf.Array) else [k]):
        if isinstance(c, int):
            out.append(int(c))
        elif (isinstance(c, pikepdf.Dictionary) and c.get("/Type") == "/MCR" and "/Stm" not in c
              and c.get("/Pg", page.obj).objgen == page.obj.objgen):
            out.append(int(c.MCID))
        else:
            return None
    return out or None


def _parent_tree_array(p, idx):
    def find(node):
        nums = node.get("/Nums")
        if nums is not None:
            for i in range(0, len(nums) - 1, 2):
                if int(nums[i]) == idx:
                    return nums[i + 1]
        for kid in node.get("/Kids") or []:
            lim = kid.get("/Limits")
            if lim is None or int(lim[0]) <= idx <= int(lim[1]):
                hit = find(kid)
                if hit is not None:
                    return hit
        return None
    pt = p.Root.StructTreeRoot.get("/ParentTree")
    return find(pt) if pt is not None else None


def _to_artifact(p, page, figs) -> set:
    """Menjadikan Figure dekoratif sebagai Artifact (PDF/UA 7.1): konten bertanda BMC /Artifact, Figure
    dilepas dari pohon struktur, entri ParentTree dikosongkan. Mengembalikan objgen Figure yang berhasil."""
    plan = {f.objgen: m for f in figs if (m := _mcids(f, page))}
    wanted = {m for ms in plan.values() for m in ms}
    if not wanted:
        return set()
    ops, seen = [], set()
    for ins in pikepdf.parse_content_stream(page):
        if (isinstance(ins, pikepdf.ContentStreamInstruction) and str(ins.operator) == "BDC"
                and len(ins.operands) == 2 and isinstance(ins.operands[1], pikepdf.Dictionary)
                and ins.operands[1].get("/MCID") in wanted):
            seen.add(int(ins.operands[1].MCID))
            ins = pikepdf.ContentStreamInstruction([pikepdf.Name.Artifact], pikepdf.Operator("BMC"))
        ops.append(ins)
    done = {g for g, ms in plan.items() if set(ms) <= seen}
    if not done:
        return set()
    if seen - {m for g in done for m in plan[g]}:
        return set()  # MCID Figure lain ikut terkena: batalkan seluruhnya agar konten tidak yatim
    page.contents_coalesce()
    page.Contents.write(pikepdf.unparse_content_stream(ops))
    arr = _parent_tree_array(p, int(page.obj.get("/StructParents", -1)))
    for f in figs:
        if f.objgen not in done:
            continue
        if arr is not None:
            for m in plan[f.objgen]:
                if m < len(arr):
                    arr[m] = None
        parent = f.get("/P")
        pk = parent.get("/K") if parent is not None else None
        if isinstance(pk, pikepdf.Array):
            parent.K = pikepdf.Array([c for c in pk if not (isinstance(c, pikepdf.Dictionary) and c.objgen == f.objgen)])
        elif isinstance(pk, pikepdf.Dictionary) and pk.objgen == f.objgen:
            del parent["/K"]
    return done


def patch(src: Path, dst: Path, title: str, alts_by_page: dict, held_alt: str, lang: str = "id-ID") -> dict:
    """Menambal PDF bertag. alts_by_page = {halaman: [{"id", "alt", "bbox"}]}, alt None berarti dekoratif
    (dijadikan Artifact), bbox dalam ruang PDF. Bila jumlah Figure pada halaman sama dengan jumlah entri,
    pemetaan mengikuti urutan; bila tidak, entri dipasangkan menurut bbox (IoU ≥ MATCH_IOU) dan Figure yang
    tidak berpasangan diberi penanda ditahan (fail-closed) agar deskripsi tidak terpasang pada gambar lain.
    "tertanam" mencatat id entri yang keputusannya benar-benar masuk PDF."""
    stats = {"figures": 0, "alt_filled": 0, "figur_ditahan": 0, "figur_tambahan": 0, "halaman_tidak_cocok": [],
             "th_cells": 0, "tertanam": [], "artefak": 0, "artefak_gagal": 0}
    with pikepdf.open(src) as p:
        p.Root.Lang = pikepdf.String(lang)
        p.Root.MarkInfo = pikepdf.Dictionary(Marked=True)
        vp = p.Root.get("/ViewerPreferences") or pikepdf.Dictionary()
        vp.DisplayDocTitle = True
        p.Root.ViewerPreferences = vp
        p.docinfo["/Title"] = title
        for page in p.pages:
            page.obj.Tabs = pikepdf.Name.S
        with p.open_metadata(set_pikepdf_as_editor=False) as m:
            m["dc:title"] = title
            m["dc:language"] = [lang]
            m.register_xml_namespace("http://www.aiim.org/pdfua/ns/id/", "pdfuaid")
            m["pdfuaid:part"] = "1"
        found, by_page = _figs_by_page(p)
        stats["figures"] = len(found["fig"])
        for n, figs in by_page.items():
            entries = alts_by_page.get(n, [])
            if len(entries) == len(figs):
                pairs = dict(enumerate(entries))
            else:
                stats["halaman_tidak_cocok"].append(n)
                stats["figur_tambahan"] += max(0, len(figs) - len(entries))
                pairs = _match_by_bbox(figs, entries)
            deco = []
            for i, fig in enumerate(figs):
                e = pairs.get(i)
                if e is None:
                    fig.Alt = pikepdf.String(held_alt)
                    stats["figur_ditahan"] += 1
                elif e["alt"] is None:
                    deco.append(fig)
                    continue
                else:
                    fig.Alt = pikepdf.String(e["alt"])
                stats["alt_filled"] += 1
            if deco:
                done = _to_artifact(p, p.pages[n - 1], deco) if n else set()
                for fig in deco:
                    if fig.objgen not in done:
                        fig.Alt = pikepdf.String(DECORATIVE_ALT)
                        stats["alt_filled"] += 1
                stats["artefak"] += len(done)
                stats["artefak_gagal"] += len(deco) - len(done)
            stats["tertanam"] += [e["id"] for e in pairs.values()]
        for t in found["table"]:
            stats["th_cells"] += _first_row_to_th(t)
        p.save(dst)
    return stats


def figure_alts(pdf: Path) -> list:
    """Membaca /Alt semua Figure (untuk audit G1 pada B0/B1/D)."""
    with pikepdf.open(pdf) as p:
        if "/StructTreeRoot" not in p.Root:
            return []
        found = {"fig": [], "table": []}
        _struct_walk(p.Root.StructTreeRoot.get("/K"), found)
        return [str(f.get("/Alt")) if f.get("/Alt") is not None else None for f in found["fig"]]


def g1_audit(pdf: Path) -> dict:
    """G1: kegagalan teks alternatif bermakna, bahasa, dan judul pada satu dokumen."""
    with pikepdf.open(pdf) as p:
        lang = str(p.Root.get("/Lang", "")).strip()
        title = str(p.docinfo.get("/Title", "")).strip()
        vp = p.Root.get("/ViewerPreferences")
        display_title = bool(vp and vp.get("/DisplayDocTitle"))
    alts = figure_alts(pdf)
    tagged = is_tagged(pdf)
    bad_alt = sum(is_placeholder(a) for a in alts)
    # G1 ketat: penanda tahan SIMAK informatif bagi pembaca layar, tetapi belum mendeskripsikan gambarnya.
    held = sum(bool(a) and str(a).lstrip().startswith(HELD_PREFIXES) for a in alts)
    ok = tagged and bad_alt == 0 and bool(lang) and bool(title) and display_title
    return {"tagged": tagged, "figures": len(alts), "alt_bermakna": len(alts) - bad_alt,
            "alt_ok": tagged and bad_alt == 0, "lang_ok": bool(lang), "title_ok": bool(title) and display_title,
            "pass": ok, "alt_ditahan": held, "pass_ketat": ok and held == 0}
