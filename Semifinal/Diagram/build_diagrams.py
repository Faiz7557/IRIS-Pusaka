# -*- coding: utf-8 -*-
from diagram_engine import Diagram

# =====================================================================
# GAMBAR A: ALUR PENELITIAN  (pola: Pembuatan Dataset -> Pemisahan -> Pemodelan & Evaluasi)
# =====================================================================
A = Diagram(910, 420, "Alur Penelitian")
A.node("cL", "Pengumpulan dan Penyiapan Data", 10, 10, 236, 400, "blue", "container", bold=True)
ys = [46, 138, 230, 322]
txt = ["Bingkai publik ac.id\n(indeks Common Crawl):\nsampel berstrata 600 PDF",
       "Dokumen sintetis dari sumber\nberstruktur (Word/LaTeX\n→ PDF), urutan baca diketahui",
       "Grafik, rumus, tabel acuan\npublik (VisText, ChartQA,\nUniMER-Test, IndoTabVQA)",
       "Dokumen nyata untuk G6:\n60 dokumen dari set uji\nsampel bingkai publik"]
for i in range(4):
    A.node("d%d" % (i + 1), txt[i], 22, ys[i], 212, 80, "white", parent="cL")

A.node("split", "Pemisahan\nSet Data", 272, 190, 110, 56, "orange", bold=True, thick=True)
A.node("dev", "Set pengembangan\n(penyetelan)", 268, 84, 118, 54, "yellow")
A.node("tst", "Set uji tertahan\n(held-out)", 268, 300, 118, 54, "yellow")

A.node("cR", "Pengembangan Sistem dan Evaluasi", 422, 10, 478, 400, "pink", "container", bold=True)
A.node("cP", "Pengembangan Pipeline", 444, 44, 414, 112, "blue", "container", bold=True, parent="cR")
for i, t in enumerate(["Analisis tata\nletak &\nurutan baca", "Modul grafik\n(tabel data →\ndeskripsi)", "Modul rumus\n(→ MathML\n→ ucapan)", "Gerbang\nverifikasi\n(fail-closed)"]):
    A.node("p%d" % (i + 1), t, 451 + i * 102, 76, 94, 68, "white" if i < 3 else "pink", parent="cP")
A.node("ev", "Evaluasi gerbang G1–G6 pada set uji tertahan\nSistem D vs B0 (PDF mentah), B1 (auto-tag\nopen-source), B2 (VLM tanpa gerbang)", 444, 182, 414, 64, "yellow", parent="cR")
A.node("frz", "Sistem dibekukan\n(versi final)", 444, 274, 196, 52, "purple", parent="cR")
A.node("err", "Analisis kesalahan &\nperbaikan iteratif", 662, 274, 196, 52, "peach", parent="cR")
A.node("res", "Hasil dan pembahasan\n(Bab IV, tahap final)", 444, 350, 196, 48, "green", bold=True, parent="cR")
A.node("g7", "G7: uji pengguna tunanetra\ndan ULD (ditunda)", 662, 350, 196, 48, "white", dashed=True, parent="cR")

A.edge("cL", "split", (246, 218), (272, 218))
A.edge("split", "dev", (327, 190), (327, 138))
A.edge("split", "tst", (327, 246), (327, 300))
A.edge("dev", "cP", (386, 111), (444, 111))
A.edge("tst", "ev", (386, 327), (444, 214), via=[(404, 327), (404, 214)])
A.edge("cP", "ev", (651, 156), (651, 182))
A.edge("ev", "frz", (541, 246), (541, 274))
A.edge("ev", "err", (760, 246), (760, 274))
A.edge("frz", "res", (541, 326), (541, 350))
A.edge("res", "g7", (640, 374), (662, 374), dashed=True)
A.edge("err", "cP", (858, 300), (858, 100), via=[(881, 300), (881, 100)], dashed=True)
A.label("lulus gerbang", 541 - 6, 260, fs=10, w=80)
A.label("belum lulus", 760 + 4, 260, fs=10, w=70)
A.label("iterasi", 881, 200, fs=10, italic=True, w=40)

# =====================================================================
# GAMBAR B: ALUR IMPLEMENTASI  (pola: alur ringkas -> keputusan; lalu 'zoom' ke pipeline rinci)
# =====================================================================
B = Diagram(920, 500, "Alur Implementasi")
B.node("a1", "Materi kuliah (PDF)\ndiunggah staf ULD / dosen", 10, 40, 160, 64, "orange", bold=True)
B.node("a2", "Sistem remediasi\n(rincian di bawah)", 210, 30, 170, 84, "blue", thick=True, bold=True)
B.node("a3", "Semua elemen\nlolos gerbang\nverifikasi?", 420, 16, 170, 112, "blue", "diamond")
B.node("ok", "Terbit: HTML aksesibel + PDF bertag;\ndeskripsi ditandai 'dihasilkan otomatis'", 640, 10, 270, 56, "green")
B.node("no", "Ditahan: antrean tinjauan staf ULD\n(diperbaiki, lalu diterbitkan)", 640, 80, 270, 56, "red")
B.edge("a1", "a2", (170, 72), (210, 72))
B.edge("a2", "a3", (380, 72), (420, 72))
B.edge("a3", "ok", (590, 72), (640, 38), via=[(615, 72), (615, 38)])
B.edge("a3", "no", (590, 72), (640, 108), via=[(615, 72), (615, 108)])
B.label("YA", 602, 52, fs=10, bold=True, w=30)
B.label("TIDAK", 613, 128, fs=10, bold=True, w=44)
B.freeline([(210, 114), (10, 160)])
B.freeline([(380, 114), (910, 160)])

B.node("c", "Sistem Remediasi (rincian)", 10, 160, 900, 330, "gray", "container", bold=True)
B.node("pdf", "PDF materi\nkuliah", 22, 280, 76, 60, "orange", "cyl", parent="c")
B.node("lay", "Analisis tata\nletak, urutan\nbaca, auto-tag", 116, 268, 104, 84, "blue", parent="c")
B.node("rt", "Perutean\nelemen (teks,\ntabel, grafik,\nrumus)", 238, 268, 104, 84, "blue", parent="c")
B.node("lt", "Teks, judul, daftar, tabel\n→ tag struktur (TH, heading)", 372, 196, 266, 56, "green", parent="c")
B.node("g1", "Ekstraksi tabel data\ngrafik → deskripsi\nID level 1–3 (VLM)", 372, 278, 126, 64, "green", parent="c")
B.node("g2", "Verifikasi klaim\n(label, nilai)\nterhadap tabel data", 512, 278, 126, 64, "green", parent="c")
B.node("r1", "Rumus → LaTeX /\nMathML → ucapan\n(MathCAT, id)", 372, 356, 126, 64, "green", parent="c")
B.node("r2", "Uji kesepakatan\ndua pengenal\n(jarak sunting)", 512, 356, 126, 64, "green", parent="c")
B.node("gate", "Gerbang\nverifikasi\n(fail-closed)", 664, 250, 112, 120, "pink", bold=True, parent="c")
B.node("asm", "Perakitan: tag,\nalt text, bahasa", 800, 196, 100, 56, "blue", parent="c")
B.node("val", "Validasi veraPDF\n(PDF/UA-1)", 800, 272, 100, 56, "blue", parent="c")
B.node("out", "Keluaran:\nHTML + PDF\nbertag", 800, 348, 100, 56, "green", bold=True, parent="c")
B.node("uld", "Antrean tinjauan\nstaf ULD (editor\ndeskripsi)", 650, 416, 140, 64, "red", parent="c")

B.edge("pdf", "lay", (98, 310), (116, 310))
B.edge("lay", "rt", (220, 310), (238, 310))
B.edge("rt", "lt", (342, 310), (372, 224), via=[(356, 310), (356, 224)])
B.edge("rt", "g1", (342, 310), (372, 310))
B.edge("rt", "r1", (342, 310), (372, 388), via=[(356, 310), (356, 388)])
B.edge("g1", "g2", (498, 310), (512, 310))
B.edge("r1", "r2", (498, 388), (512, 388))
B.edge("lt", "gate", (638, 224), (664, 285), via=[(650, 224), (650, 285)])
B.edge("g2", "gate", (638, 310), (664, 310))
B.edge("r2", "gate", (638, 388), (664, 335), via=[(650, 388), (650, 335)])
B.edge("gate", "asm", (776, 300), (800, 224), via=[(788, 300), (788, 224)])
B.edge("asm", "val", (850, 252), (850, 272))
B.edge("val", "out", (850, 328), (850, 348))
B.edge("gate", "uld", (720, 370), (720, 416))
B.edge("uld", "asm", (790, 448), (900, 224), via=[(906, 448), (906, 224)], dashed=True)
B.label("lolos", 794, 262, fs=10, w=40)
B.label("tidak lolos", 720, 393, fs=10, w=70)
B.label("setelah disetujui", 850, 462, fs=10, italic=True, w=110)

# =====================================================================
# GAMBAR C: KERANGKA TUJUH LANGKAH (pola: Masalah -> Input -> ... -> Status & Bukti), contoh pengisian fitur deskripsi grafik
# =====================================================================
Cc = Diagram(920, 185, "Kerangka Tujuh Langkah")
steps = ["Masalah", "Input", "Praproses", "Model /\nMetode", "Inferensi", "Output", "Status &\nBukti"]
caps = ["grafik pada materi\nkuliah tak terbaca\npembaca layar",
        "citra grafik dari\nPDF (gambar\nnon-dekoratif)",
        "klasifikasi jenis\ngambar; normalisasi\nresolusi",
        "VLM mengekstraksi\ntabel data dua kali;\nstatistik oleh kode",
        "keluaran JSON\nterstruktur, suhu 0;\nkalimat dari templat",
        "tabel T1, T2;\ndeskripsi level 1–3;\nstatus terbit/tahan",
        "rancangan; diuji\npada G3 dan G4"]
for i in range(7):
    x = 3 + i * 134
    Cc.node("s%d" % i, steps[i], x, 12, 110, 52, "purple" if i in (3, 4) else "white", bold=True, fs=13)
    Cc.node("c%d" % i, caps[i], x, 92, 110, 50, "clear", fs=11, fillnone=True)
    Cc.edge("s%d" % i, "c%d" % i, (x + 55, 64), (x + 55, 92), dashed=True, color="#888888")
    if i < 6:
        Cc.edge("s%d" % i, "s%d" % (i + 1), (x + 110, 38), (x + 134, 38))
Cc.label("Contoh pengisian untuk fitur CHT (deskripsi grafik)", 460, 165, fs=12, italic=True, w=420)

if __name__ == "__main__":
    A.to_drawio("Gambar_Alur_Penelitian.drawio"); A.to_png("Gambar_Alur_Penelitian.png")
    B.to_drawio("Gambar_Alur_Implementasi.drawio"); B.to_png("Gambar_Alur_Implementasi.png")
    Cc.to_drawio("Gambar_Kerangka_Tujuh_Langkah.drawio"); Cc.to_png("Gambar_Kerangka_Tujuh_Langkah.png")
    print("done")
