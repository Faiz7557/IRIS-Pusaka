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


def patch(src: Path, dst: Path, title: str, alts_by_page: dict, held_alt: str, lang: str = "id-ID") -> dict:
    """Menambal PDF bertag. Teks alternatif dipetakan per halaman menurut urutan; bila jumlah Figure
    pada suatu halaman tidak sama dengan jumlah citra yang diproses (mis. figur vektor), seluruh Figure
    pada halaman itu diberi penanda ditahan (fail-closed) agar deskripsi tidak terpasang pada gambar lain."""
    stats = {"figures": 0, "alt_filled": 0, "figur_ditahan": 0, "figur_tambahan": 0, "halaman_tidak_cocok": [],
             "th_cells": 0}
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
        found = {"fig": [], "table": []}
        if "/StructTreeRoot" in p.Root:
            _struct_walk(p.Root.StructTreeRoot.get("/K"), found)
        page_no = {pg.obj.objgen: i + 1 for i, pg in enumerate(p.pages)}
        by_page: dict[int, list] = {}
        for fig, pg in zip(found["fig"], found.get("fig_pg", [])):
            n = page_no.get(pg.objgen) if pg is not None else None
            by_page.setdefault(n, []).append(fig)
        stats["figures"] = len(found["fig"])
        for n, figs in by_page.items():
            alts = alts_by_page.get(n, [])
            if len(alts) != len(figs):
                stats["halaman_tidak_cocok"].append(n)
                alts = [held_alt] * len(figs)
                stats["figur_ditahan"] += len(figs)
                stats["figur_tambahan"] += max(0, len(figs) - len(alts_by_page.get(n, [])))
            for fig, alt in zip(figs, alts):
                fig.Alt = pikepdf.String(alt)
                stats["alt_filled"] += 1
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
