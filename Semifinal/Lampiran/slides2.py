# -*- coding: utf-8 -*-
import math
from collections import defaultdict
from slides1 import *


def cellbox(s, x, y, w, h, label, kind, size=11):
    fills = {"ya": (NAVY, WHITE), "sebagian": (TINT2, INK), "tidak": (WHITE, MUTED), "nr": (TINT3, MUTED), "simak": (TEAL, WHITE)}
    f, c = fills[kind]
    box(s, x, y, w, h, [label], fill=f, line=LINE, lw=0.5, size=size, color=c, bold=(kind in ("ya", "simak")), align="c", anchor="m",
        margins=(0.04, 0.02, 0.04, 0.02))


# =============================================================== F.5 Matriks pembanding
def f5():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.5", "Analisis Kompetitor: Matriks Pembanding Fitur",
          "Sel diisi hanya dengan yang dilaporkan sumber (Tabel IV naskah) atau diamati langsung penulis; n/r = tidak dilaporkan",
          note="SIMAK: kolom rancangan, kinerja belum terbukti. Sumber: PAVE 2.0, iTagPDF, OpenDataLoader, Adobe/AbilityNet, SEA-Vision; uji awal penulis.")
    cols = ["Remediasi manual (ULD, lembaga)", "Adobe Auto-Tag", "OpenData-Loader", "iTagPDF", "PAVE 2.0", "VLM langsung (tanpa gerbang)", "SIMAK"]
    x0, w0, wc = 0.5, 3.0, 1.33
    y0, hh, rh = 1.5, 0.78, 0.58
    box(s, x0, y0, w0, hh, ["Kriteria"], fill=NAVY_D, size=12.5, color=WHITE, bold=True, align="c", anchor="m")
    for j, c in enumerate(cols):
        box(s, x0 + w0 + j * wc, y0, wc, hh, [c], fill=(TEAL if j == 6 else NAVY), size=11, color=WHITE, bold=True, align="c", anchor="m",
            margins=(0.03, 0.02, 0.03, 0.02))
    rows = [
        ("Menerima PDF tanpa berkas sumber", [("Ya", "ya"), ("Ya", "ya"), ("Ya", "ya"), ("Tidak: perlu sumber LaTeX", "tidak"), ("Ya (PDF ilmiah)", "ya"), ("Ya", "ya"), ("Ya", "simak")]),
        ("Perakitan tag dan urutan baca otomatis", [("Tidak: manual", "tidak"), ("Ya; perlu koreksi", "sebagian"), ("Ya (gratis)", "ya"), ("Ya", "ya"), ("Sebagian: dipandu", "sebagian"), ("Tidak", "tidak"), ("Ya", "simak")]),
        ("Deskripsi gambar atau grafik oleh AI", [("Tidak", "tidak"), ("n/r", "nr"), ("Ya (mode hybrid)", "ya"), ("Ya (agen LLM)", "ya"), ("n/r", "nr"), ("Ya", "ya"), ("Ya", "simak")]),
        ("Deskripsi diperiksa terhadap data grafik", [("Tidak", "tidak"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("Tidak", "tidak"), ("Ya: tingkat klaim", "simak")]),
        ("Rumus dibacakan (MathML ke ucapan)", [("Bergantung staf", "sebagian"), ("n/r", "nr"), ("Sebagian: ke LaTeX", "sebagian"), ("n/r", "nr"), ("n/r", "nr"), ("Tidak", "tidak"), ("Ya: MathCAT", "simak")]),
        ("Peninjau ULD dan status per elemen", [("Ya: oleh manusia", "ya"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("Tidak", "tidak"), ("Ya", "simak")]),
        ("Diuji pada materi berbahasa Indonesia", [("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("n/r", "nr"), ("Akurasi menurun (SEA-Vision)", "sebagian"), ("Direncanakan (G6)", "simak")]),
    ]
    for i, (lab, vals) in enumerate(rows):
        y = y0 + hh + i * rh
        box(s, x0, y, w0, rh, [lab], fill=TINT1, line=LINE, lw=0.5, size=11.5, color=NAVY, bold=True, anchor="m", margins=(0.1, 0.02, 0.05, 0.02))
        for j, (t, k) in enumerate(vals):
            cellbox(s, x0 + w0 + j * wc, y, wc, rh, t, k, size=10.5)
    yb = y0 + hh + 7 * rh + 0.12
    box(s, 0.5, yb, 12.33, 0.55, [[("Nilai unik: ", {"bold": True, "color": TEAL}),
        "kombinasi masukan PDF tanpa sumber, deskripsi yang diperiksa terhadap data, dan peninjau ULD belum dilaporkan oleh sumber mana pun yang ditinjau. SIMAK tidak mengklaim akurasi lebih tinggi daripada alat-alat di atas."]],
        fill=TEAL_L, size=12, anchor="m")
    return s


# =============================================================== F.6 STP
def f6():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.6", "Segmentasi, Target, dan Posisi (STP)", None,
          note="Posisi pada peta adalah penilaian kualitatif penulis dari Tabel IV naskah, bukan hasil pengukuran.")
    hdr(s, 0.5, 1.2, 6.0, "SEGMENTASI", NAVY)
    seg = [("Institusi", "Universitas, fakultas, dan unit yang melayani mahasiswa disabilitas (282 perguruan tinggi mencatat mahasiswa disabilitas)."),
           ("Wilayah", "Indonesia; fokus awal pada materi kuliah berbahasa Indonesia."),
           ("Perilaku", "Berorientasi inklusivitas, digitalisasi, dan accessibility-by-design; ingin mengurangi remediasi manual; terbuka pada alur kerja berbantuan AI."),
           ("Kebutuhan", "Banyak materi PDF dan memiliki ULD; butuh teks alternatif, urutan baca, tabel, grafik, rumus, dan metadata bahasa.")]
    for i, (t, d) in enumerate(seg):
        y = 1.65 + i * 0.66
        box(s, 0.5, y, 1.25, 0.6, [t], fill=TINT2, size=12, color=NAVY, bold=True, anchor="m", align="c")
        box(s, 1.75, y, 4.75, 0.6, [d], fill=WHITE, line=LINE, lw=0.75, size=10.5, anchor="m")
    hdr(s, 6.83, 1.2, 6.0, "TARGET", ROYAL)
    tg = [("Prioritas 1", "Tinggi", "Perguruan tinggi dengan ULD dan mahasiswa pengguna pembaca layar."),
          ("Prioritas 2", "Tinggi", "Institusi dengan banyak materi kuliah berbasis PDF."),
          ("Prioritas 3", "Menengah", "Institusi yang terbuka terhadap alur kerja berbantuan AI."),
          ("Sekunder", "Hipotesis", "Mahasiswa pendengar (42,6% pendengar podcast mingguan); manfaat belum diuji.")]
    for i, (t, lv, d) in enumerate(tg):
        y = 1.65 + i * 0.66
        box(s, 6.83, y, 1.25, 0.6, [t], fill=[ROYAL, ROYAL, AZURE, TEAL][i], size=11.5, color=WHITE, bold=True, anchor="m", align="c")
        box(s, 8.08, y, 4.75, 0.6, [[(lv + ". ", {"bold": True, "color": NAVY}), d]], fill=WHITE, line=LINE, lw=0.75, size=10.5, anchor="m")
    # peta posisi
    hdr(s, 0.5, 4.4, 6.0, "PETA POSISI: OTOMASI DAN VERIFIKASI", TEAL)
    mx, my, mw, mh = 1.2, 4.88, 5.1, 1.62
    box(s, mx, my, mw, mh, None, fill=TINT3, line=LINE)
    box(s, mx + mw / 2, my, mw / 2, mh / 2, None, fill=TEAL_L)
    line(s, mx + mw / 2, my, mx + mw / 2, my + mh, color=MUTED, lw=1, dash=True)
    line(s, mx, my + mh / 2, mx + mw, my + mh / 2, color=MUTED, lw=1, dash=True)
    text(s, mx, my + mh + 0.01, mw, 0.22, [[("Otomasi: rendah  →  tinggi", {"size": 10, "italic": True, "color": MUTED})]], align="c", margins=(0, 0, 0, 0))
    text(s, 0.5, my, 0.7, mh, [[("Verifikasi tinggi", {"size": 10, "italic": True, "color": MUTED})]], align="c", anchor="t", margins=(0, 0, 0, 0))
    text(s, 0.5, my + mh - 0.4, 0.7, 0.4, [[("rendah", {"size": 10, "italic": True, "color": MUTED})]], align="c", anchor="b", margins=(0, 0, 0, 0))
    pts = [("Manual", 0.10, 0.20, "r"), ("PAVE 2.0", 0.30, 0.62, "r"), ("Adobe", 0.60, 0.86, "r"),
           ("OpenDataLoader", 0.58, 0.68, "r"), ("iTagPDF", 0.80, 0.66, "r"), ("VLM langsung", 0.92, 0.90, "l")]
    for lab, px, py, side in pts:
        cx, cy = mx + px * mw, my + py * mh
        circle(s, cx, cy, 0.16, fill=BRIGHT)
        if side == "r":
            text(s, cx + 0.1, cy - 0.12, 1.3, 0.24, [[(lab, {"size": 9.5, "color": INK})]], margins=(0, 0, 0, 0))
        else:
            text(s, cx - 1.4, cy - 0.12, 1.3, 0.24, [[(lab, {"size": 9.5, "color": INK})]], margins=(0, 0, 0, 0), align="r")
    cx, cy = mx + 0.86 * mw, my + 0.16 * mh
    circle(s, cx, cy, 0.34, fill=TEAL)
    text(s, cx - 1.25, cy - 0.12, 0.85, 0.24, [[("SIMAK", {"size": 11, "bold": True, "color": TEAL})]], align="r", margins=(0, 0, 0, 0))
    # pernyataan posisi
    hdr(s, 6.83, 4.4, 6.0, "PERNYATAAN POSISI", NAVY)
    box(s, 6.83, 4.83, 6.0, 1.85, [[("Bagi ULD perguruan tinggi ", {"bold": True, "color": NAVY}), "yang harus menyediakan materi aksesibel bagi mahasiswa tunanetra, ",
          ("SIMAK ", {"bold": True, "color": TEAL}), "adalah sistem remediasi PDF berbahasa Indonesia yang menerima PDF apa adanya dan menahan setiap keluaran yang tidak dapat diverifikasi untuk ditinjau ULD."],
         {"runs": [("Berbeda dari auto-tag dan VLM langsung, ", {"bold": True, "color": NAVY}), "SIMAK hanya menerbitkan otomatis deskripsi yang lolos pemeriksaan terhadap data sumbernya."], "space_before": 4}],
        fill=WHITE, line=NAVY, lw=1.5, radius=0.04, size=12, anchor="m", margins=(0.18, 0.08, 0.18, 0.08))
    return s


# =============================================================== F.7 BMC ringkas
def f7():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.7", "Model Bisnis dan Keberlanjutan (Business Model Canvas Ringkas)",
          "Tahap penelitian: sumber pendapatan dan saluran bersifat hipotesis yang belum diuji",
          note="Tidak ada angka biaya atau pendapatan yang diklaim; biaya VLM per gambar diukur pada uji penentu 1–3 Oktober 2026.")
    W, gx = 2.4, 0.08
    xs = [0.5 + i * (W + gx) for i in range(5)]

    def blk(x, y, w, h, title, items, fill=TINT1, tc=NAVY):
        box(s, x, y, w, h, None, fill=fill, line=LINE, lw=0.75)
        text(s, x + 0.06, y + 0.04, w - 0.1, 0.3, [[(title, {"bold": True, "size": 13.5, "color": tc})]], margins=(0, 0, 0, 0))
        text(s, x + 0.04, y + 0.4, w - 0.08, h - 0.44, [{"runs": [t], "bullet": "•", "indent": 0.13, "space_after": 2} for t in items], size=12.5, margins=(0.04, 0, 0.02, 0))
    top, hgt = 1.5, 3.95
    blk(xs[0], top, W, hgt, "Mitra utama", ["ULD perguruan tinggi mitra", "Yayasan Mitra Netra dan komunitas pengguna pembaca layar", "Penyedia VLM atau komunitas model terbuka", "Komunitas kode terbuka (OpenDataLoader, veraPDF, MathCAT)"])
    blk(xs[1], top, W, hgt / 2 - 0.04, "Aktivitas utama", ["Mengembangkan pipeline dan gerbang", "Mengevaluasi tujuh gerbang", "Menyempurnakan aturan bahasa Indonesia"])
    blk(xs[1], top + hgt / 2 + 0.04, W, hgt / 2 - 0.04, "Sumber daya utama", ["Kode, data audit, dan protokol evaluasi", "Akses VLM (API atau lokal)", "Tim peneliti dan ULD mitra"])
    blk(xs[2], top, W, hgt, "Proposisi nilai", ["PDF apa adanya menjadi materi aksesibel dengan status tiap elemen", "Deskripsi grafik berbasis data dan terverifikasi, atau ditandai", "ULD memegang kendali", "Berbahasa Indonesia; berjalan di CPU biasa"], fill=TEAL_L, tc=TEAL)
    blk(xs[3], top, W, hgt / 2 - 0.04, "Hubungan pelanggan", ["Pendampingan awal (onboarding) ULD", "Umpan balik dari antrean tinjauan"])
    blk(xs[3], top + hgt / 2 + 0.04, W, hgt / 2 - 0.04, "Saluran", ["Aplikasi web untuk ULD", "Kemitraan langsung dengan ULD (rencana)"])
    blk(xs[4], top, W, hgt, "Segmen pelanggan", ["ULD perguruan tinggi (operator dan peninjau)", "Mahasiswa tunanetra (penerima manfaat)", "Dosen pembuat materi (pengunggah)", "Sekunder: mahasiswa pendengar (hipotesis)"])
    yb = top + hgt + 0.1
    half = 2.5 * W + 2 * gx - 0.04
    blk(xs[0], yb, half, 1.12, "Struktur biaya", ["Biaya API VLM per gambar dan komputasi CPU", "Pengembangan, pemeliharaan, dan waktu peninjauan staf ULD"])
    blk(xs[0] + half + 0.08, yb, half, 1.12, "Sumber pendapatan (hipotesis)", ["Hibah atau program inklusivitas perguruan tinggi", "Layanan berlangganan institusi (belum diuji)"])
    return s


# =============================================================== F.8 SWOT
def f8():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.8", "Analisis SWOT", None,
          note="Kelemahan dinyatakan apa adanya: penelitian berada pada tahap kelayakan dan rancangan evaluasi.")
    Q = [("Kekuatan (Strengths)", NAVY, TINT1, 0.5, 1.2,
          ["Gerbang verifikasi tertutup: keluaran yang tidak dapat diverifikasi ditahan.", "ULD tetap memegang kendali: meninjau, memperbaiki, menyetujui, atau menolak.",
           "Deskripsi grafik berbasis data: tabel data dan statistik yang dihitung kode.", "Pembacaan rumus terstruktur: MathML dan MathCAT.",
           "Tidak bergantung pada berkas sumber: bekerja dari PDF.", "Setiap elemen terdokumentasi: halaman, posisi, jenis, klaim, hasil pemeriksaan, status."]),
         ("Kelemahan (Weaknesses)", AZURE, TINT3, 6.75, 1.2,
          ["Cakupan masukan terbatas: PDF berlapis teks berbahasa Indonesia.", "Kinerja akhir belum terbukti: tahap kelayakan dan rancangan evaluasi.",
           "Elemen tertentu masih butuh manusia: foto dan diagram nondata.", "Bergantung pada kualitas AI: kesalahan interpretasi tetap mungkin.",
           "Dampak belajar belum terukur.", "Belum ada uji pengguna: mahasiswa tunanetra belum terlibat langsung."]),
         ("Peluang (Opportunities)", TEAL, TEAL_L, 0.5, 4.0,
          ["Kebutuhan materi aksesibel di perguruan tinggi (1.727 mahasiswa tunanetra tercatat).", "Kesenjangan aksesibilitas digital: teks alternatif, struktur, tabel, grafik, rumus.",
           "Perkembangan AI mempercepat remediasi yang semula manual.", "Penguatan peran ULD dengan dukungan teknologi.",
           "Integrasi dengan LMS, repositori, dan sistem pembelajaran.", "Fokus materi berbahasa Indonesia yang belum dilayani alat yang ada."]),
         ("Ancaman (Threats)", INDIGO, TINT2, 6.75, 4.0,
          ["Alat remediasi PDF otomatis sudah tersedia (Adobe, OpenDataLoader, iTagPDF).", "Kesalahan interpretasi AI pada grafik, tabel, atau rumus.",
           "Keamanan data: materi kuliah dapat memuat informasi internal.", "Beban kerja ULD bila terlalu banyak keluaran ditinjau.",
           "Ketergantungan pada penyedia AI: perubahan model, API, atau biaya.", "Lulus pemeriksaan teknis belum menjamin nyaman bagi pembaca layar."])]
    for t, c, bg, x, y, items in Q:
        box(s, x, y, 6.08, 2.7, None, fill=bg, line=LINE)
        box(s, x, y, 6.08, 0.38, [t], fill=c, size=14, color=WHITE, bold=True, anchor="m", margins=(0.15, 0.02, 0.1, 0.02))
        text(s, x + 0.08, y + 0.42, 5.92, 2.25, [{"runs": [it], "bullet": "•", "space_after": 5} for it in items], size=13, margins=(0.05, 0.02, 0.05, 0))
    return s


# =============================================================== F.9 TOWS
def f9():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.9", "Strategi TOWS: dari Analisis ke Tindakan", None,
          note="Strategi turunan SWOT (Lampiran F.8); dijadwalkan pada peta jalan Lampiran F.13.")
    box(s, 2.1, 1.2, 5.3, 0.45, ["Peluang (O)"], fill=TEAL, size=14, color=WHITE, bold=True, align="c", anchor="m")
    box(s, 7.5, 1.2, 5.33, 0.45, ["Ancaman (T)"], fill=INDIGO, size=14, color=WHITE, bold=True, align="c", anchor="m")
    box(s, 0.5, 1.75, 1.5, 2.45, ["Kekuatan (S)"], fill=NAVY, size=14, color=WHITE, bold=True, align="c", anchor="m")
    box(s, 0.5, 4.3, 1.5, 2.4, ["Kelemahan (W)"], fill=AZURE, size=14, color=WHITE, bold=True, align="c", anchor="m")
    cells = [(2.1, 1.75, 5.3, 2.45, "SO: memanfaatkan kekuatan untuk peluang", TEAL_L,
              ["Kemitraan pilot dengan ULD: gerbang fail-closed dan kendali ULD menjawab kebutuhan materi aksesibel.", "Jadikan PDF tanpa berkas sumber dan bahasa Indonesia sebagai pembeda pada institusi dengan banyak materi PDF.", "Terbitkan data audit dan protokol sebagai bukti kondisi awal."]),
             (7.5, 1.75, 5.33, 2.45, "ST: kekuatan untuk menghadapi ancaman", TINT2,
              ["Diferensiasi lewat verifikasi dan konteks akademik Indonesia, bukan lewat akurasi mentah.", "Adaptor VLM tak terikat penyedia dengan cadangan model terbuka lokal.", "Proses per sesi tanpa penyimpanan; dokumen tidak dipakai melatih model."]),
             (2.1, 4.3, 5.3, 2.4, "WO: menutup kelemahan dengan peluang", TINT1,
              ["Perluas cakupan bertahap (PowerPoint dan Word langsung, PDF pindai) mengikuti kemajuan AI.", "Uji pengguna G7 bersama ULD mitra untuk mengukur dampak dan kenyamanan pembaca layar.", "Libatkan staf ULD sebagai penilai luar pada G6."]),
             (7.5, 4.3, 5.33, 2.4, "WT: meminimalkan kelemahan dan ancaman", TINT3,
              ["Batasi klaim: tidak mengklaim akurasi di atas alat yang ada; laporkan kegagalan gerbang apa adanya.", "Tekan beban ULD lewat ambang gerbang yang dikunci dan pelaporan rasio tinjauan R.", "Pemeriksaan singkat dengan NVDA melengkapi veraPDF."])]
    for x, y, w, h, t, bg, items in cells:
        box(s, x, y, w, h, None, fill=bg, line=LINE)
        text(s, x + 0.1, y + 0.06, w - 0.2, 0.32, [[(t, {"bold": True, "size": 13, "color": NAVY})]], margins=(0, 0, 0, 0))
        text(s, x + 0.08, y + 0.42, w - 0.16, h - 0.45, [{"runs": [it], "bullet": "•", "space_after": 6} for it in items], size=13.5, margins=(0.04, 0.02, 0.04, 0))
    return s


# =============================================================== F.10 Porter
def f10():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.10", "Lima Kekuatan Porter", "Skor 1–5: makin tinggi makin besar tekanan kompetitif (penilaian awal tim)",
          note="Skor merupakan penilaian awal tim berdasarkan Tabel IV naskah dan bukan hasil survei pasar.")
    cx, cy, R = 3.1, 4.2, 1.6
    names = ["Ancaman pendatang baru", "Daya tawar pemasok", "Daya tawar pembeli", "Persaingan antarpemain", "Ancaman substitusi"]
    vals = [3, 3, 4, 4, 3]
    ang = [-90 + 72 * i for i in range(5)]

    def pt(i, r):
        return cx + r * math.cos(math.radians(ang[i])), cy + r * math.sin(math.radians(ang[i]))
    for lv in range(5, 0, -1):
        poly(s, [pt(i, R * lv / 5) for i in range(5)], fill=(TINT3 if lv % 2 else WHITE), line_c=LINE, lw=0.75)
    for i in range(5):
        x2, y2 = pt(i, R)
        line(s, cx, cy, x2, y2, color=LINE, lw=0.75)
    poly(s, [pt(i, R * vals[i] / 5) for i in range(5)], fill=TEAL, line_c=TEAL, lw=2.25, alpha=35)
    lab_pos = [(cx - 1.1, cy - R - 0.32, 2.2, "c"), (cx + R * 0.95 + 0.08, cy - R * 0.31 - 0.22, 1.3, "l"), (cx + R * 0.59 + 0.08, cy + R * 0.81 - 0.05, 1.3, "l"),
               (cx - R * 0.59 - 1.38, cy + R * 0.81 - 0.05, 1.3, "r"), (cx - R * 0.95 - 1.38, cy - R * 0.31 - 0.22, 1.3, "r")]
    for (x, y, w, al), n in zip(lab_pos, names):
        text(s, x, y, w, 0.5, [[(n, {"bold": True, "size": 11.5, "color": NAVY})]], align=al, margins=(0, 0, 0, 0))
    rows = [("Ancaman pendatang baru", 3, "AI mudah diakses, tetapi verifikasi, akurasi, dan integrasi alur ULD meningkatkan hambatan masuk."),
            ("Daya tawar pemasok", 3, "Ketergantungan pada model AI, perangkat lunak PDF, dan teknologi pembacaan rumus memengaruhi biaya dan kapabilitas."),
            ("Daya tawar pembeli", 4, "Institusi dan ULD punya alternatif remediasi manual maupun otomatis, sehingga menuntut akurasi, keamanan, dan kemudahan tinggi."),
            ("Persaingan antarpemain", 4, "Tersedia remediasi manual, auto-tag, dan pembaca layar, tetapi belum tentu memadukan seluruh fungsi SIMAK."),
            ("Ancaman substitusi", 3, "Solusi aksesibilitas PDF, AI, dan teknologi bantu lain dapat menggantikan sebagian fungsi.")]
    for i, (n, v, d) in enumerate(rows):
        y = 1.55 + i * 0.86
        box(s, 6.0, y, 2.3, 0.78, [n], fill=NAVY, size=12, color=WHITE, bold=True, anchor="m", align="c")
        box(s, 8.35, y, 0.75, 0.78, [f"{v}/5"], fill=(NAVY_D if v >= 4 else TINT2), size=17, color=(WHITE if v >= 4 else NAVY), bold=True, anchor="m", align="c")
        box(s, 9.15, y, 3.68, 0.78, [d], fill=TINT3, line=LINE, lw=0.5, size=10.5, anchor="m")
    box(s, 6.0, 5.95, 6.83, 0.7, [[("Implikasi: ", {"bold": True, "color": TEAL}), "diferensiasi dibangun melalui verifikasi dan konteks akademik Indonesia; SIMAK tidak bersaing pada akurasi mentah model."]],
        fill=TEAL_L, size=12, anchor="m")
    return s


# =============================================================== F.11 PESTEL
def f11():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.11", "Analisis PESTEL: Lingkungan Eksternal SIMAK", None,
          note="Sumber: UU 8/2016; Permendikbudristek 48/2023; PDDikti via detikEdu; Tempo.co; CharXiv; SEA-Vision; Databoks/We Are Social; uji awal penulis.")
    hdr(s, 0.5, 1.15, 1.9, "Faktor", NAVY, h=0.34, size=12.5)
    hdr(s, 2.45, 1.15, 6.1, "Kondisi", ROYAL, h=0.34, size=12.5)
    hdr(s, 8.6, 1.15, 4.23, "Implikasi bagi SIMAK", TEAL, h=0.34, size=12.5)
    P = [("P", "Politik", "UU 8/2016 dan Permendikbudristek 48/2023 mewajibkan akomodasi yang layak dan pembentukan ULD di perguruan tinggi.", "Permintaan berbasis kewajiban, bukan sekadar pilihan; ULD menjadi operator yang alami."),
         ("E", "Ekonomi", "Produksi materi aksesibel, misalnya buku braille, terkendala biaya dan bertumpu pada tenaga manusia.", "Otomasi terverifikasi menekan beban; biaya utama adalah API VLM (diukur 1–3 Okt), infrastruktur cukup CPU."),
         ("S", "Sosial", "3.128 mahasiswa disabilitas di 282 perguruan tinggi; tunanetra 1.727 (terbesar). Podcast didengar 42,6% pengguna internet tiap pekan.", "Kebutuhan nyata bagi pengguna utama; kebiasaan mendengar memberi hipotesis manfaat bagi mahasiswa pendengar."),
         ("T", "Teknologi", "VLM berkembang tetapi tidak andal (GPT-4o 47,1% pada grafik ilmiah; 43,61% pada tanya-jawab visual berbahasa Indonesia). Komponen kode terbuka tersedia.", "Verifikasi menjadi pembeda; perakitan memanfaatkan OpenDataLoader, veraPDF, dan MathCAT."),
         ("E", "Lingkungan", "Distribusi materi digital yang aksesibel berpotensi mengurangi kebutuhan cetak dan produksi braille (belum diukur).", "Sistem berjalan tanpa GPU (uji awal: 21 halaman, 4,6 detik); dampak lingkungan tidak diklaim."),
         ("L", "Hukum", "Hak cipta dan kerahasiaan materi dosen; WCAG 2.2 dan PDF/UA sebagai acuan teknis aksesibilitas.", "Dokumen diproses per sesi tanpa disimpan, tidak dipakai melatih model; kepatuhan diukur dengan veraPDF.")]
    for i, (l, n, c, im) in enumerate(P):
        y = 1.55 + i * 0.86
        circle(s, 0.78, y + 0.4, 0.5, fill=[NAVY, ROYAL, AZURE, TEAL, INDIGO, BRIGHT][i], label=l, size=17)
        box(s, 1.1, y, 1.3, 0.8, [n], fill=TINT2, size=12.5, color=NAVY, bold=True, anchor="m", align="c", margins=(0.2, 0.02, 0.04, 0.02))
        box(s, 2.45, y, 6.1, 0.8, [c], fill=WHITE, line=LINE, lw=0.75, size=11.5, anchor="m")
        box(s, 8.6, y, 4.23, 0.8, [im], fill=TEAL_L, size=11.5, anchor="m")
    return s


# =============================================================== F.12 Risiko
def f12():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.12", "Analisis Risiko dan Mitigasi", None,
          note="Penilaian dampak dan probabilitas adalah penilaian awal tim. Rujukan gerbang G1–G7 pada Tabel VII naskah; R = rasio beban tinjauan (Pers. 10).")
    mx, my, cw, ch = 1.15, 1.75, 1.3, 1.5
    lv = ["Rendah", "Sedang", "Tinggi"]
    shade = {2: TINT2, 3: "B5CDF3", 4: SKY, 5: INDIGO, 6: NAVY_D}
    for r in range(3):
        for c in range(3):
            imp = 3 - r; prob = c + 1
            box(s, mx + c * cw, my + r * ch, cw, ch, None, fill=shade[imp + prob], line=WHITE, lw=1.5)
    for c in range(3):
        text(s, mx + c * cw, my + 3 * ch + 0.03, cw, 0.28, [[(lv[c], {"size": 11, "color": MUTED})]], align="c", margins=(0, 0, 0, 0))
    for r in range(3):
        text(s, 0.5, my + r * ch, 0.65, ch, [[(lv[2 - r], {"size": 11, "color": MUTED})]], align="c", anchor="m", margins=(0, 0, 0, 0))
    text(s, mx, my + 3 * ch + 0.3, 3 * cw, 0.3, [[("Probabilitas →", {"bold": True, "size": 12, "color": NAVY})]], align="c", margins=(0, 0, 0, 0))
    text(s, 0.5, 1.42, 3, 0.3, [[("↑ Dampak", {"bold": True, "size": 12, "color": NAVY})]], margins=(0, 0, 0, 0))
    R = [(1, 3, 3), (2, 3, 2), (3, 2, 3), (4, 2, 3), (5, 2, 2), (6, 3, 1), (7, 2, 2)]
    cell = defaultdict(list)
    for n, imp, prob in R:
        cell[(imp, prob)].append(n)
    for (imp, prob), ns in cell.items():
        r = 3 - imp; c = prob - 1
        for k, n in enumerate(ns):
            ox = (k - (len(ns) - 1) / 2) * 0.5
            circle(s, mx + c * cw + cw / 2 + ox, my + r * ch + ch / 2, 0.42, fill=WHITE, label=str(n), size=13, color=NAVY_D, line_c=NAVY_D)
    hdr(s, 5.35, 1.2, 0.5, "No", NAVY, h=0.34, size=12)
    hdr(s, 5.9, 1.2, 3.1, "Risiko (dampak / probabilitas)", ROYAL, h=0.34, size=12)
    hdr(s, 9.05, 1.2, 3.78, "Mitigasi", TEAL, h=0.34, size=12.5)
    T = [("Kesalahan interpretasi AI", "Deskripsi grafik atau rumus tidak sesuai sumber.", "Tinggi / Tinggi", "Gerbang fail-closed; klaim diperiksa terhadap tabel data (Pers. 5); penanda “dihasilkan otomatis”."),
         ("Lolos validator, salah makna", "Struktur benar, isi keliru.", "Tinggi / Sedang", "G1 mengecualikan teks pengisi; G4 rasio informasi; pemeriksaan NVDA pada G6."),
         ("Beban tinjauan ULD berlebih", "Terlalu banyak elemen ditahan.", "Sedang / Tinggi", "Laporkan R (G6); ambang gerbang dikunci; antrean berurutan menurut jenis elemen."),
         ("Dokumen nyata lebih berantakan", "Materi asli tidak serapi data sintetis.", "Sedang / Tinggi", "G6 pada 60 dokumen nyata dari sampel acak bingkai publik; jalur cadangan HTML aksesibel."),
         ("Ketergantungan penyedia VLM", "Perubahan API, biaya, layanan.", "Sedang / Sedang", "Adaptor tak terikat penyedia; model terbuka lokal; hasil demo disimpan (cache)."),
         ("Hak cipta dan kerahasiaan materi", "Materi dosen dapat memuat informasi internal.", "Tinggi / Rendah", "Proses per sesi tanpa penyimpanan; tidak dipakai melatih model; opsi model lokal."),
         ("Adopsi rendah", "ULD atau dosen enggan mengubah alur.", "Sedang / Sedang", "Dosen tidak perlu mengubah alur (PDF apa adanya); pilot dan onboarding ULD.")]
    for i, (t, d, lvl, m) in enumerate(T):
        y = 1.6 + i * 0.73
        circle(s, 5.6, y + 0.34, 0.4, fill=NAVY_D, label=str(i + 1), size=12)
        box(s, 5.9, y, 3.1, 0.68, [[(t, {"bold": True, "color": NAVY}), (f"  ({lvl})", {"color": MUTED, "size": 9.5})], [(d, {"size": 10.5})]], fill=TINT1, size=11.5, anchor="m", margins=(0.08, 0.02, 0.06, 0.02))
        box(s, 9.05, y, 3.78, 0.68, [m], fill=WHITE, line=LINE, lw=0.5, size=10.5, anchor="m", margins=(0.08, 0.02, 0.06, 0.02))
    return s


# =============================================================== F.13 Peta jalan
def f13():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.13", "Peta Jalan: dari Bukti Awal ke Pilot dan Perluasan", None,
          note="Jadwal hingga Oktober 2026 mengikuti rencana kerja naskah; tahap setelahnya adalah rencana lanjutan yang belum berkomitmen.")
    ph = [("Sep 2026", "Semifinal", NAVY), ("Okt 2026", "Final dan MVP", ROYAL), ("Nov 2026 – Q1 2027", "Pilot bersama ULD", AZURE), ("2027", "Perluasan (rencana)", TEAL)]
    lx, lw, x0, cw = 0.5, 1.5, 2.06, 2.66
    for j, (a, b, c) in enumerate(ph):
        box(s, x0 + j * (cw + 0.03), 1.2, cw, 0.62, [[(a, {"bold": True, "size": 13.5})], [(b, {"size": 11.5})]], fill=c, color=WHITE, align="c", anchor="m")
    lanes = [("Pembuktian", NAVY_D, TINT2,
              [["Audit awal 28 PDF", "Uji kelayakan 3 dokumen", "Kueri bingkai publik diuji"], ["1–3 Okt: audit skala besar (600 PDF acak)", "20–22 Okt: evaluasi G1, G3, G4, G6 pada set uji tertahan"], ["Uji pengguna G7 bersama ULD dan mahasiswa tunanetra"], ["Publikasi hasil; audit dokumen lebih luas"]]),
             ("Pipeline dan modul AI", INDIGO, TINT1,
              [["Arsitektur dan adaptor VLM"], ["1–3 Okt: uji penentu VLM dan veraPDF", "4–9 Okt: perakitan dan aturan tambal", "10–15 Okt: modul grafik dan kalibrasi gerbang"], ["Modul rumus (UniMERNet, MathCAT)", "Mode dengar"], ["PowerPoint dan Word langsung", "PDF pindai (OCR); braille"]]),
             ("Pengguna dan ULD", ROYAL, TINT3,
              [["Profil pengguna dan peran ULD"], ["16–19 Okt: antarmuka tinjauan ULD dan audit dokumen nyata"], ["Onboarding ULD mitra", "Ukur beban tinjauan R"], ["Pelatihan staf ULD"]]),
             ("Kemitraan dan keberlanjutan", TEAL, TEAL_L,
              [["Identifikasi mitra ULD"], ["23 Okt naskah lengkap; 28 Okt demo dan presentasi"], ["Kemitraan ULD dan Mitra Netra", "Model VLM lokal sebagai cadangan"], ["Integrasi LMS dan repositori", "Model layanan institusi (hipotesis)"]])]
    lh = 1.1
    for i, (name, c, bg, cells) in enumerate(lanes):
        y = 1.92 + i * (lh + 0.05)
        box(s, lx, y, lw, lh, [name], fill=c, size=12.5, color=WHITE, bold=True, anchor="m", align="c")
        for j, items in enumerate(cells):
            box(s, x0 + j * (cw + 0.03), y, cw, lh, None, fill=bg, line=LINE, lw=0.5)
            text(s, x0 + j * (cw + 0.03) + 0.04, y + 0.04, cw - 0.08, lh - 0.06, [{"runs": [it], "bullet": "•", "indent": 0.13, "space_after": 2} for it in items], size=11.5, margins=(0.04, 0.02, 0.03, 0))
    return s
