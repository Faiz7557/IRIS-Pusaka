# -*- coding: utf-8 -*-
"""v10 -> v11: hanya tabel pada Lampiran G yang disamakan gayanya dengan tabel bab utama
(garis kisi hitam, header tanpa arsiran dan tebal-tengah, isi 9 pt, keterangan "Tabel G.n. Judul" di atas tabel).
Pemakaian: python tabel_g_v11.py SUMBER.docx TUJUAN.docx"""
import copy, re, sys
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC, DST = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
body = d.element.body

def ptext(e):
    return "".join(t.text or "" for t in e.iter(qn("w:t")))

# tabel Lampiran G = tabel biasa (bukan gambar mengambang, bukan tabel bernomor "Tabel n.")
g_tables = [t for t in body.findall(qn("w:tbl"))
            if t.find(".//" + qn("w:tblpPr")) is None and not ptext(t).startswith("Tabel")]
assert len(g_tables) == 3, len(g_tables)

CAPTIONS = [
    "Tabel G.1. Inventaris data babak final: sumber, metadata, ukuran, dan perannya",
    "Tabel G.2. Pemetaan data ke fitur prototipe dan pembagian set pengembangan dan uji tertahan",
    "Tabel G.3. Setengah lebar selang Wilson 95% menurut ukuran sampel",
]
RANK = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "noProof", "color", "spacing", "w", "kern",
        "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd", "vertAlign", "lang"]

def rpr_set(rpr, name, val=None):
    ex = rpr.find(qn("w:" + name))
    if ex is None:
        ex = OxmlElement("w:" + name)
        rk = RANK.index(name); pos = len(rpr)
        for k, c in enumerate(rpr):
            tag = c.tag.split("}")[1]
            if tag in RANK and RANK.index(tag) > rk:
                pos = k; break
        rpr.insert(pos, ex)
    if val is not None:
        ex.set(qn("w:val"), val)
    return ex

def rpr_del(rpr, name):
    for e in rpr.findall(qn("w:" + name)):
        rpr.remove(e)

for tbl, cap in zip(g_tables, CAPTIONS):
    tp = tbl.find(qn("w:tblPr"))
    # 1) garis kisi hitam seperti tabel utama
    old = tp.find(qn("w:tblBorders")); nb = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        for k, v in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", "000000")):
            e.set(qn("w:" + k), v)
        nb.append(e)
    old.addprevious(nb); tp.remove(old)
    # 2) bantalan sel seperti tabel utama
    mar = tp.find(qn("w:tblCellMar"))
    for side in ("top", "bottom"):
        mar.find(qn("w:" + side)).set(qn("w:w"), "4")
    rows = tbl.findall(qn("w:tr"))
    ncol = len(rows[0].findall(qn("w:tc")))
    width = sum(int(g.get(qn("w:w"))) for g in tbl.find(qn("w:tblGrid")).findall(qn("w:gridCol")))
    for k, tr in enumerate(rows):
        head = (k == 0)
        for tc in tr.findall(qn("w:tc")):
            tcp = tc.find(qn("w:tcPr"))
            shd = tcp.find(qn("w:shd"))
            if shd is not None: tcp.remove(shd)
            for p in tc.findall(qn("w:p")):
                ppr = p.find(qn("w:pPr"))
                sp = ppr.find(qn("w:spacing"))
                sp.set(qn("w:before"), "0"); sp.set(qn("w:after"), "0")
                if head:
                    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "center"); ppr.append(jc)
                for r in p.iter(qn("w:r")):
                    rpr = r.find(qn("w:rPr"))
                    if rpr is None:
                        rpr = OxmlElement("w:rPr"); r.insert(0, rpr)
                    rpr_del(rpr, "color")
                    rpr_set(rpr, "sz", "18"); rpr_set(rpr, "szCs", "18")
                    if head:
                        rpr_set(rpr, "b"); rpr_set(rpr, "bCs")
                    else:
                        rpr_del(rpr, "b"); rpr_del(rpr, "bCs")
    # 3) baris keterangan di atas tabel (tanpa garis, berulang di halaman lanjutan, seperti tabel utama)
    tr = OxmlElement("w:tr")
    trpr = OxmlElement("w:trPr")
    trpr.append(OxmlElement("w:cantSplit")); trpr.append(OxmlElement("w:tblHeader"))
    j = OxmlElement("w:jc"); j.set(qn("w:val"), "center"); trpr.append(j); tr.append(trpr)
    tc = OxmlElement("w:tc"); tcp = OxmlElement("w:tcPr")
    w = OxmlElement("w:tcW"); w.set(qn("w:w"), str(width)); w.set(qn("w:type"), "dxa"); tcp.append(w)
    gs = OxmlElement("w:gridSpan"); gs.set(qn("w:val"), str(ncol)); tcp.append(gs)
    bd = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + side); e.set(qn("w:val"), "nil"); bd.append(e)
    tcp.append(bd); tc.append(tcp)
    p = OxmlElement("w:p"); ppr = OxmlElement("w:pPr")
    ppr.append(OxmlElement("w:keepNext"))
    sp = OxmlElement("w:spacing"); sp.set(qn("w:before"), "100"); sp.set(qn("w:after"), "60"); ppr.append(sp)
    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "center"); ppr.append(jc)
    p.append(ppr)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    rpr_set(rpr, "sz", "18"); rpr_set(rpr, "szCs", "18")
    lg = OxmlElement("w:lang"); lg.set(qn("w:val"), "id-ID"); rpr.append(lg); r.append(rpr)
    t = OxmlElement("w:t"); t.text = cap.replace("Tabel G.", "Tabel G.", 1)
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r.append(t)
    p.append(r); tc.append(p); tr.append(tc)
    rows[0].addprevious(tr)


# tanda kurung ganda tak seimbang pada dua sel G.2 (akibat penyeragaman "Pers. n" -> "(n)") diperbaiki
for tbl in g_tables:
    for t in tbl.iter(qn("w:t")):
        if t.text and "((" in t.text:
            t.text = t.text.replace("((", "(")

d.save(DST)
print("tabel Lampiran G disesuaikan:", len(g_tables), "->", DST)
