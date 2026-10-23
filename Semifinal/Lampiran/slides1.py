# -*- coding: utf-8 -*-
"""Deck Lampiran F SIMAK (palet logo). Jalankan: python build_deck.py -> Lampiran_F_SIMAK.pptx"""
import sys
sys.path.insert(0, ".")
from pptlib import *

prs = new_prs()
B = {"bold": True}


def hdr(s, x, y, w, label, fill=NAVY, h=0.38, size=14):
    return box(s, x, y, w, h, [label], fill=fill, size=size, color=WHITE, bold=True, align="c", anchor="m")


# =============================================================== F.1 Profil nilai jual
def f1():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.1", "Profil dan Nilai Jual SIMAK",
          "Dari masalah yang terukur, ke solusi yang terverifikasi, ke jaminan bagi ULD dan mahasiswa tunanetra",
          note="Sumber angka: PDDikti via detikEdu (Juni 2025); audit awal penulis (28 PDF, 18 kampus; bukan sampel acak); uji kelayakan awal penulis (3 dokumen contoh).")
    # kolom 1: masalah
    hdr(s, 0.5, 1.5, 3.85, "MASALAH YANG TERBUKTI", NAVY)
    stats = [("1.727", "mahasiswa tunanetra tercatat, kelompok terbesar dari 3.128 mahasiswa disabilitas di 282 perguruan tinggi"),
             ("0 dari 28", "PDF materi kuliah berbahasa Indonesia yang lulus PDF/UA-1 (audit awal)"),
             ("2,6%", "elemen gambar bertag yang memiliki teks alternatif (29 dari 1.111)")]
    for i, (n, d) in enumerate(stats):
        y = 2.0 + i * 1.32
        box(s, 0.5, y, 3.85, 1.2, None, fill=TINT1, line=LINE)
        box(s, 0.5, y, 0.09, 1.2, None, fill=ROYAL)
        text(s, 0.72, y + 0.08, 3.55, 0.55, [[(n, {"bold": True, "size": 27, "color": ROYAL})]], margins=(0, 0, 0, 0))
        text(s, 0.72, y + 0.6, 3.55, 0.6, [[(d, {"size": 12.5})]], margins=(0, 0, 0, 0))
    # kolom 2: solusi
    hdr(s, 4.6, 1.5, 4.15, "SOLUSI: SIMAK", ROYAL)
    steps = [("1", "Perbaiki struktur", "PDF apa adanya menjadi HTML aksesibel dan PDF bertag (PDF/UA-1) tanpa berkas sumber."),
             ("2", "Sampaikan isi", "Deskripsi grafik dari tabel data dengan statistik yang dihitung kode; rumus dibacakan MathCAT; mode dengar."),
             ("3", "Jaga kepercayaan", "Gerbang fail-closed: keluaran yang tidak dapat diverifikasi ditahan untuk ditinjau ULD.")]
    for i, (n, t, d) in enumerate(steps):
        y = 2.0 + i * 1.32
        box(s, 4.6, y, 4.15, 1.2, None, fill=WHITE, line=ROYAL, lw=1.25)
        circle(s, 4.95, y + 0.6, 0.5, fill=[ROYAL, AZURE, TEAL][i], label=n, size=16)
        text(s, 5.3, y + 0.05, 3.4, 0.35, [[(t, {"bold": True, "size": 14, "color": NAVY})]], margins=(0, 0, 0, 0))
        text(s, 5.3, y + 0.38, 3.4, 0.8, [[(d, {"size": 11.5})]], margins=(0, 0, 0, 0))
    # kolom 3: nilai jual
    hdr(s, 9.0, 1.5, 3.83, "NILAI JUAL UNIK", TEAL)
    uv = [("Tanpa berkas sumber", "Dosen tidak perlu mengubah alur kerja."),
          ("Terverifikasi atau ditandai", "Tidak ada deskripsi keliru terbit tanpa penanda."),
          ("ULD tetap memegang kendali", "Terima, ubah, atau tolak per elemen."),
          ("Berjalan di CPU biasa", "21 halaman dalam 4,6 detik (uji awal).")]
    for i, (t, d) in enumerate(uv):
        y = 2.0 + i * 0.99
        box(s, 9.0, y, 3.83, 0.9, None, fill=TEAL_L)
        text(s, 9.12, y + 0.05, 3.6, 0.85, [[(t, {"bold": True, "size": 13, "color": NAVY})], [(d, {"size": 12})]], margins=(0, 0, 0, 0))
    # status bukti
    y = 6.05
    text(s, 0.5, y - 0.02, 2.0, 0.3, [[("Status bukti hari ini", {"bold": True, "size": 12, "color": NAVY})]], margins=(0, 0, 0, 0))
    seg = [("Terukur", "kondisi awal (audit 28 PDF)", NAVY, WHITE, 3.0), ("Teruji awal", "perakitan tag lulus veraPDF pada 2 dari 3 dokumen", ROYAL, WHITE, 5.0),
           ("Belum terukur", "akurasi grafik dan rumus, dampak belajar", TINT2, INK, 4.33)]
    x = 0.5
    for t, d, f, c, w in seg:
        box(s, x, y + 0.27, w - 0.05, 0.42, [[(t + ": ", {"bold": True}), d]], fill=f, size=11, color=c, anchor="m")
        x += w
    # tagline
    return s


# =============================================================== F.2 Pohon masalah
def f2():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.2", "Pohon Masalah: dari Tujuan ke Akar Masalah dan Buktinya",
          None, note="Bukti: audit awal penulis; uji kelayakan awal (Tabel VIII naskah); CharXiv (Wang dkk., 2024); Jung dkk. (2022).")
    hdr(s, 0.5, 1.2, 2.15, "Tujuan", NAVY)
    hdr(s, 2.85, 1.2, 4.6, "Masalah", ROYAL)
    hdr(s, 7.7, 1.2, 3.2, "Akar Masalah", AZURE)
    hdr(s, 11.05, 1.2, 1.78, "Bukti", TEAL)
    box(s, 0.5, 1.68, 2.15, 4.95, [[("Bagaimana SIMAK mengubah PDF materi kuliah yang tidak aksesibel menjadi materi yang dapat diakses sekaligus mengurangi beban remediasi ULD?", {"bold": True})]],
        fill=WHITE, line=NAVY, lw=1.75, radius=0.06, size=15, color=NAVY, align="c", anchor="m", margins=(0.15, 0.1, 0.15, 0.1))
    groups = [("1", "Materi Pembelajaran Tidak Aksesibel",
               [("1a", "Teks alternatif tidak tersedia", "Grafik, gambar, dan elemen visual tidak memiliki deskripsi yang dapat dibaca pembaca layar.", "2,6% Figure beralt"),
                ("1b", "Struktur dokumen tidak tepat", "Urutan baca, judul, bahasa dokumen, dan struktur tabel belum konsisten.", "0 dari 28 lulus PDF/UA‑1")]),
              ("2", "Informasi Semantik Sulit Diakses",
               [("2a", "Grafik sulit dipahami pembaca layar", "Informasi grafik tidak cukup direpresentasikan hanya melalui gambar; pengguna butuh rujukan ke data.", "22 wawancara (Jung dkk.)"),
                ("2b", "Rumus dan tabel tidak ramah teknologi bantu", "Rumus memerlukan pembacaan khusus; tabel memerlukan struktur judul kolom yang benar.", "1 dari 13 dokumen bertabel punya sel judul")]),
              ("3", "Risiko Kesalahan Keluaran AI",
               [("3a", "AI salah menginterpretasikan konten", "AI dapat menghasilkan deskripsi, angka, atau pembacaan rumus yang tidak sesuai sumber.", "GPT-4o: 47,1% pada grafik ilmiah"),
                ("3b", "Lulus validasi teknis belum menjamin kebenaran isi", "Validator memeriksa struktur, bukan apakah teks alternatif benar secara makna.", "Teks “image N” lolos veraPDF")])]
    y0 = 1.68; rh = 0.72; gap = 0.08
    for gi, (gn, gt, subs) in enumerate(groups):
        gy = y0 + gi * (2 * (rh + gap) + 0.1)
        gh = 2 * rh + gap
        box(s, 2.85, gy, 1.72, gh, [gt], fill=TINT2, size=12.5, color=NAVY, bold=True, align="c", anchor="m")
        circle(s, 2.85, gy + 0.05, 0.4, fill=NAVY, label=gn, size=13)
        for si, (sn, st, rc, ev) in enumerate(subs):
            yy = gy + si * (rh + gap)
            line(s, 4.57, gy + gh / 2, 4.75, yy + rh / 2, color=ROYAL, lw=1.25)
            box(s, 4.75, yy, 2.7, rh, [st], fill=TINT1, size=12, color=INK, bold=True, anchor="m", align="c", margins=(0.32, 0.04, 0.08, 0.04))
            circle(s, 4.75, yy + 0.02, 0.34, fill=ROYAL, label=sn, size=11)
            line(s, 7.45, yy + rh / 2, 7.7, yy + rh / 2, color=ROYAL, lw=1.25)
            box(s, 7.7, yy, 3.2, rh, [rc], fill=WHITE, line=AZURE, lw=1.25, size=11.5, anchor="m", align="c")
            box(s, 11.05, yy, 1.78, rh, [ev], fill=TEAL_L, size=11.5, color=NAVY, bold=True, anchor="m", align="c", margins=(0.06, 0.03, 0.06, 0.03))
        line(s, 0.5 + 2.15, 1.68 + 2.47, 2.85, gy + gh / 2, color=NAVY, lw=1.25)
    return s


# =============================================================== F.3 Value proposition canvas
def f3():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.3", "Value Proposition Canvas: Kesesuaian Solusi dengan Pengguna",
          "Segmen utama: staf ULD (operator dan peninjau). Penerima manfaat langsung: mahasiswa tunanetra.",
          note="Isi disusun dari temuan Bab I–II naskah: Day & Fleischmann (2026), Mitra Netra, Tempo.co, Raees dkk. (2026), audit awal penulis.")
    # panel kiri: peta nilai
    text(s, 0.5, 1.45, 5.9, 0.35, [[("PETA NILAI SIMAK", {"bold": True, "size": 15, "color": ROYAL})]], margins=(0, 0, 0, 0))
    text(s, 6.93, 1.45, 5.9, 0.35, [[("PROFIL PELANGGAN (ULD dan mahasiswa tunanetra)", {"bold": True, "size": 15, "color": TEAL})]], margins=(0, 0, 0, 0))
    L = [("Produk dan layanan", ROYAL, ["Remediasi PDF menjadi HTML aksesibel dan PDF bertag (PDF/UA-1)", "Deskripsi grafik berbasis tabel data; pembacaan rumus MathCAT; mode dengar", "Gerbang verifikasi fail-closed dan antarmuka tinjauan ULD"]),
         ("Pereda masalah", INDIGO, ["Menerima PDF apa adanya, tanpa berkas sumber", "Statistik dihitung kode, klaim diperiksa terhadap data", "Elemen yang tidak terverifikasi ditahan, bukan diterbitkan"]),
         ("Pencipta manfaat", AZURE, ["Penanda per elemen: “dihasilkan otomatis” atau “disetujui ULD”", "Laporan veraPDF dan rekaman lengkap tiap elemen", "Berjalan di CPU biasa; model VLM dapat diganti"])]
    R = [("Tugas pelanggan", TEAL, ["ULD: menyediakan materi aksesibel tepat waktu dan mengendalikan keluaran AI", "Mahasiswa: membaca materi mandiri dengan pembaca layar"]),
         ("Masalah (pain)", NAVY, ["Produksi manual bertumpu tenaga manusia dan berbiaya tinggi", "Grafik, rumus, tabel “diam” atau tak terbaca; risiko AI berhalusinasi", "Beban kerja tambahan dan hambatan yang saling bertautan"]),
         ("Manfaat yang diharapkan (gain)", TEALB, ["Materi tersedia lebih cepat dengan beban tinjauan terukur", "Keputusan akhir tetap di tangan ULD", "Mahasiswa dapat menyimak seluruh materi dan tahu status tiap elemen"])]
    for i in range(3):
        y = 1.85 + i * 1.62
        for (x, data) in ((0.5, L[i]), (6.93, R[i])):
            t, c, items = data
            box(s, x, y, 5.9, 1.5, None, fill=WHITE, line=c, lw=1.5, radius=0.05)
            box(s, x, y, 5.9, 0.34, [t], fill=c, size=12.5, color=WHITE, bold=True, anchor="m", margins=(0.12, 0.02, 0.1, 0.02))
            text(s, x + 0.08, y + 0.36, 5.75, 1.12, [{"runs": [it], "bullet": "•", "space_after": 2} for it in items], size=13, margins=(0.05, 0.02, 0.05, 0.02))
        line(s, 6.4, y + 0.75, 6.93, y + 0.75, color=NAVY, lw=2, arrow=True)
    return s


# =============================================================== F.4 Sebelum - sesudah
def f4():
    s = add_slide(prs)
    frame(s, "LAMPIRAN F.4", "Skenario Ilustratif: Sebelum dan Sesudah SIMAK",
          "Mahasiswa tunanetra menerima salindia kuliah statistika berformat PDF",
          note="Skenario ilustratif yang disusun dari temuan audit awal; contoh deskripsi bukan keluaran sistem yang telah diuji.")
    # kolom sebelum
    hdr(s, 0.5, 1.5, 5.95, "SEBELUM: PDF APA ADANYA", NAVY)
    box(s, 0.5, 1.95, 5.95, 3.2, None, fill=TINT3, line=LINE)
    items = [("Grafik regresi", "Pembaca layar diam; teks alternatif tidak ada (97,4% elemen gambar bertag tanpa teks alternatif)."),
             ("Rumus koefisien korelasi", "Tidak terbaca; tak ada MathML atau teks alternatif."),
             ("Tabel hasil", "Dibacakan sel demi sel tanpa judul kolom (hanya 1 dari 13 dokumen bertabel memiliki sel judul)."),
             ("Akibatnya", "Mahasiswa meminta rekan menjelaskan atau menunggu ULD menyalin ulang secara manual.")]
    for i, (t, d) in enumerate(items):
        y = 2.05 + i * 0.78
        circle(s, 0.82, y + 0.3, 0.32, fill=NAVY, label="✕", size=11)
        text(s, 1.1, y, 5.25, 0.75, [[(t + ". ", {"bold": True, "color": NAVY, "size": 12.5}), (d, {"size": 12})]], margins=(0, 0, 0, 0))
    # panah
    chevron(s, 6.55, 3.05, 0.6, 1.0, fill=TEAL, kind=MSO_SHAPE.RIGHT_ARROW)
    # kolom sesudah
    hdr(s, 7.25, 1.5, 5.58, "SESUDAH: KELUARAN SIMAK", TEAL)
    box(s, 7.25, 1.95, 5.58, 3.2, None, fill=TEAL_L, line=TEAL)
    items2 = [("Grafik", "Deskripsi level 1–3 dari tabel data; statistik dihitung kode; klaim diperiksa gerbang."),
              ("Rumus", "MathML diucapkan MathCAT; bila belum pasti, ditahan untuk ULD."),
              ("Tabel", "Baris judul menjadi sel TH; dibaca dengan judul kolom."),
              ("Status", "Tiap elemen berpenanda “dihasilkan otomatis” atau “menunggu ULD”.")]
    for i, (t, d) in enumerate(items2):
        y = 2.05 + i * 0.78
        circle(s, 7.57, y + 0.3, 0.32, fill=TEAL, label="✓", size=11)
        text(s, 7.85, y, 4.9, 0.75, [[(t + ". ", {"bold": True, "color": NAVY, "size": 12.5}), (d, {"size": 12})]], margins=(0, 0, 0, 0))
    # alur
    y = 5.35
    labels = [("Unggah PDF", ROYAL), ("Analisis dan perakitan", INDIGO), ("Gerbang verifikasi", NAVY)]
    for i, (t, c) in enumerate(labels):
        chevron(s, 0.5 + i * 2.6, y, 2.75, 0.75, fill=c, paras=[t], size=12.5)
    box(s, 8.4, y - 0.02, 2.2, 0.36, ["Lolos: terbit otomatis"], fill=TEAL, size=11.5, color=WHITE, bold=True, align="c", anchor="m")
    box(s, 8.4, y + 0.4, 2.2, 0.36, ["Ditahan: antrean ULD"], fill=NAVY_D, size=11.5, color=WHITE, bold=True, align="c", anchor="m")
    line(s, 8.25, y + 0.37, 8.4, y + 0.16, color=NAVY, lw=1.5, arrow=True)
    line(s, 8.25, y + 0.37, 8.4, y + 0.58, color=NAVY, lw=1.5, arrow=True)
    box(s, 10.75, y - 0.02, 2.08, 0.78, [[("Uji awal: ", {"bold": True}), "2 dari 3 dokumen contoh lulus veraPDF"]], fill=TINT2, size=11, anchor="m")
    text(s, 0.5, 6.2, 12.3, 0.5, [[("Ilustrasi deskripsi grafik: ", {"bold": True, "color": NAVY}),
         ("“Diagram pencar jam belajar terhadap nilai ujian. Nilai tertinggi 92 pada 8 jam; kemiringan garis regresi positif; tren naik.” ", {"italic": True}),
         ("(angka ilustratif)", {"color": MUTED, "size": 11})]], size=12, margins=(0, 0, 0, 0))
    return s


