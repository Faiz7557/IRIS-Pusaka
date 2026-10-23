"""Pemeriksa naskah final sebelum ekspor PDF (hanya membaca, tidak mengubah docx).

  python cek_naskah.py [naskah.docx] [--pdf naskah.pdf]

Memeriksa: penanda ISIAN/sorotan/komentar yang tersisa; jumlah kata abstrak (100–250); setiap pecahan k/n dan
desimal di Abstrak, Bab IV, dan Bab V harus cocok dengan eval/results.json atau lampiran_data.json; setiap
"Gambar n"/"Tabel n" punya keterangan dan dirujuk di teks sebelum objeknya; nomor rujukan [n] ada di daftar;
bila --pdf diberikan, jumlah halaman badan utama (sebelum Lampiran A) ≤ 20.
"""
import json
import re
import sys
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent
PDF = sys.argv[sys.argv.index("--pdf") + 1] if "--pdf" in sys.argv else None
args = [a for a in sys.argv[1:] if not a.startswith("--") and a != PDF]
DOCX = Path(args[0]) if args else ROOT / "IRIS kata HQ ini lomba terakhir_ICC2026_Final.docx"
R = json.load(open(ROOT.parent / "Prototype/eval/results.json", encoding="utf-8"))
L = json.load(open(ROOT / "lampiran/lampiran_data.json", encoding="utf-8"))


def angka_sah():
    """Pecahan dan desimal yang boleh muncul: semua k/n, p, dan batas selang di results.json + rincian lampiran."""
    frac, dec = set(), set()

    def walk(o):
        if isinstance(o, dict):
            if {"k", "n"} <= o.keys():
                frac.add(f"{o['k']}/{o['n']}")
                for v in [o.get("p")] + list(o.get("ci95") or []):
                    if v is not None:
                        for d in (2, 3, 4):
                            dec.add(f"{v:.{d}f}".replace(".", ","))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, float):
            for d in ((1, 2, 3, 4) if o >= 1 else (2, 3, 4)):  # 1 desimal hanya untuk detik dan nilai ≥ 1
                dec.add(f"{o:.{d}f}".replace(".", ","))
    walk(R)
    walk(L["grafik"])
    for g in L["grafik"]:
        frac.add(f"{g.get('klaim_setia', 0)}/{g['n_klaim']}")
    H = [g for g in L["grafik"] if g["status"] != "terbit_otomatis"]
    frac |= {f"{sum(g.get('klaim_setia', 0) for g in H)}/{sum(g['n_klaim'] for g in H)}",
             f"{sum(g.get('klaim_setia', 0) < g['n_klaim'] for g in H)}/{len(H)}", "15/18", "13/14", "0/28", "29/1.111",
             "28/43", "13/17", "16/17", "0/60", "60/60", "20/30"}
    dec |= {"0,01", "0,02", "0,10", "0,90", "0,98", "0,80", "0,60", "0,937", "0,923", "6,74", "1.206,8",
            "7,6", "0,75", "0,875"}  # 7,6: waktu materi_03 dengan cache (Gambar 4a, 7,56 dtk); 0,75–0,875: kalibrasi v1
    for f in list(frac):  # selang Wilson untuk pecahan turunan (mis. 205/222) dihitung dengan pers. (8)
        k, n = (int(x.replace(".", "")) for x in f.split("/"))
        if n:
            z, p = 1.959963984540054, k / n
            c, h = p + z * z / (2 * n), z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
            dec |= {f"{(c + s * h) / (1 + z * z / n):.3f}".replace(".", ",") for s in (-1, 1)}
    return frac, dec


def badan(doc):
    """(bagian, teks, jenis) per paragraf/tabel dalam urutan dokumen; bagian = judul Heading 1 terakhir."""
    bag, out = "Abstrak", []
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:p"):
            p = Paragraph(el, doc)
            if p.style.name == "Heading 1":
                bag = p.text.strip().replace("\xa0", " ")
            out.append((bag, p.text.replace("\xa0", " "), "p"))
        elif el.tag == qn("w:tbl"):
            out.append((bag, " ".join(c.text for r in Table(el, doc).rows for c in r.cells).replace("\xa0", " "), "t"))
    return out


def main():
    doc = docx.Document(DOCX)
    B = badan(doc)
    masalah = 0

    def lapor(ok, pesan):
        nonlocal masalah
        masalah += not ok
        print(("  ok   " if ok else "  CEK  ") + pesan)

    print(f"Naskah: {DOCX.name}")
    isian = sum("[ISIAN TIM" in t for _, t, _ in B)
    lapor(isian == 0, f"penanda [ISIAN TIM] tersisa: {isian}")
    hl = sum(1 for _ in doc.element.body.iter(qn("w:highlight")))
    lapor(hl == 0, f"run bersorot tersisa: {hl}")
    km = len(list(doc.comments))
    lapor(km == 0, f"komentar Word tersisa: {km}")

    abs_p = next((t for b, t, k in B if t.strip().startswith("Abstrak")), "")
    n_abs = len(re.sub(r"^Abstrak\W*", "", abs_p.strip()).split())
    lapor(100 <= n_abs <= 250, f"kata abstrak: {n_abs} (template 100–250)")

    frac, dec = angka_sah()
    i0 = next(i for i, (b, t, k) in enumerate(B) if t.strip().startswith("Abstrak"))  # lewati judul dan afiliasi
    target = [(b, t) for b, t, k in B[i0:] if k == "p" and (b == "Abstrak" or b.startswith(("HASIL", "PENUTUP")))]
    asing_f, asing_d = set(), set()
    for _, t in target:
        if "[ISIAN TIM" in t:
            continue
        asing_f |= {m for m in re.findall(r"\b\d{1,3}(?:\.\d{3})*/\d{1,3}(?:\.\d{3})*\b", t) if m not in frac}
        asing_d |= {m for m in re.findall(r"\b\d{1,3}(?:\.\d{3})*,\d+\b", t) if m not in dec}
    lapor(not asing_f, f"pecahan di Abstrak/Bab IV–V yang tidak ada di data: {sorted(asing_f) or '—'}")
    lapor(not asing_d, f"desimal di Abstrak/Bab IV–V yang tidak ada di data (periksa manual): {sorted(asing_d) or '—'}")

    cap_pos, sebut = {}, {}
    for i, (b, t, k) in enumerate(B):
        if b.upper().startswith("LAMPIRAN"):
            break
        if k == "t":
            m = re.match(r"\s*((?:Tabel|Gambar) \d+)\.", t)
            if m:
                cap_pos.setdefault(m.group(1), i)
        else:
            for m in re.findall(r"(?:Tabel|Gambar) \d+", t):
                sebut.setdefault(m, i)
    for obj, i in sorted(cap_pos.items(), key=lambda x: x[1]):
        lapor(obj in sebut and sebut[obj] < i, f"{obj}: dirujuk di teks sebelum objek muncul")
    for obj in sebut:
        lapor(obj in cap_pos, f"{obj}: dirujuk dan ada keterangannya")

    refs = [t for b, t, k in B if b == "REFERENSI" and re.match(r"\[\d+\]", t)]
    cit = {int(x) for b, t, k in B if b != "REFERENSI" for g in re.findall(r"\[([\d,\s–-]+)\]", t)
           for x in re.findall(r"\d+", g)}
    lapor(max(cit or {0}) <= len(refs), f"rujukan: {len(refs)} entri, nomor tertinggi dikutip [{max(cit or {0})}]")

    if PDF:
        import pymupdf
        d = pymupdf.open(PDF)
        hal = next(i for i, p in enumerate(d) if "LAMPIRAN A." in p.get_text().replace("\xa0", " ").upper())
        lapor(hal <= 20, f"halaman badan utama (sebelum Lampiran A): {hal} dari maks 20")
    print(f"\n{masalah} butir perlu dicek.")


if __name__ == "__main__":
    main()
