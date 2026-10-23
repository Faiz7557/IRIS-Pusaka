# -*- coding: utf-8 -*-
# Blok keselarasan naskah dengan rencana data (di-exec oleh edit_paper_v6.py; memakai body, ptext, find_par, qn, dll.)
import re


def ptch(p, old, new):
    """Ganti `old` (boleh melintasi batas run) dengan `new` pada paragraf p; NBSP dianggap spasi."""
    ts = [t for t in p.iter(qn("w:t")) if t.text is not None]
    full = "".join(t.text for t in ts)
    norm = full.replace("\xa0", " ")
    i = norm.find(old)
    if i < 0:
        raise AssertionError(f"ptch gagal: {old[:60]!r} pada {norm[:50]!r}")
    j = i + len(old)
    pos = 0
    first = True
    for t in ts:
        a, b = pos, pos + len(t.text)
        pos = b
        if b <= i or a >= j:
            continue
        s, e = max(i, a) - a, min(j, b) - a
        if first:
            t.text = t.text[:s] + new + t.text[e:]
            first = False
        else:
            t.text = t.text[:s] + t.text[e:]
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")


def find_contains(sub, nth=0):
    hits = [p for p in all_pars() if sub in ptext(p).replace("\xa0", " ")]
    assert len(hits) > nth, f"paragraf tidak ditemukan: {sub!r}"
    return hits[nth]


def row_of(prefix):
    for tr in body.iter(qn("w:tr")):
        if ptext(tr).replace("\xa0", " ").startswith(prefix):
            return tr
    raise AssertionError("baris tidak ditemukan: " + prefix)


def cell_par_of(prefix, col):
    tr = row_of(prefix)
    return tr.findall(qn("w:tc"))[col].findall(qn("w:p"))[0]


# ---------------- Abstrak
ptch(find_par("Abstrak"), "Evaluasi dirancang melalui tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian, sedangkan uji pada mahasiswa tunanetra ditunda.",
     "Evaluasi dirancang melalui tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian, memakai sampel acak berstrata dari bingkai publik "
     "228.383 PDF domain kampus, dokumen sintetis, dan benchmark publik yang dibagi menjadi set pengembangan dan uji tertahan; uji pada mahasiswa tunanetra ditunda.")

# ---------------- Bab I: Tujuan, kontribusi
p = find_par("Berdasarkan rumusan masalah tersebut")
ptch(p, "(iv) protokol evaluasi tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian dan dapat dijalankan tanpa pengguna, serta (v) data audit awal atas materi kuliah berbahasa Indonesia.",
     "(iv) protokol evaluasi tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian, dapat dijalankan tanpa pengguna, dan bertumpu pada set pengembangan serta uji tertahan yang terpisah, "
     "serta (v) rancangan data publik yang dapat direplikasi, yaitu bingkai dan sampel acak berstrata untuk audit materi kuliah berbahasa Indonesia beserta hasil audit awalnya.")
# Tabel III
ptch(find_contains("Kegagalan aturan teks alternatif bermakna"), "kondisi awal 0 dari 28 lulus", "kondisi awal 0 dari 28 lulus, diperluas pada audit skala besar")

# ---------------- Bab I: Batasan
NEWBAT = ("Penelitian ini memiliki tujuh batasan. Pertama, belum ada uji pada mahasiswa tunanetra; klaim dampak belajar tidak dibuat dan uji "
          "tersebut dirancang sebagai gerbang G7. Kedua, sasaran utama adalah pembaca layar; manfaat bagi pendengar adalah hipotesis, dan "
          "kebutuhan pengguna *low vision* dan tuli belum tercakup. Ketiga, masukan berupa PDF berlapis teks berbahasa Indonesia; PDF hasil "
          "pindai ditangani manual dan berkas PowerPoint diekspor ke PDF lebih dahulu. Keempat, deskripsi grafik dibatasi pada level 1–3 "
          "model Lundgard dan Satyanarayan [@r21]; foto dan diagram nondata selalu ditinjau manusia. Kelima, audit awal (28 PDF) berasal dari "
          "pencarian repositori publik dan bukan sampel acak, dan uji kelayakan awal hanya mencakup tiga dokumen contoh sehingga angkanya tidak "
          "mewakili seluruh kampus; audit skala besar dengan sampel acak berstrata dirancang untuk babak final dan hanya mencakup materi yang "
          "terbuka untuk publik (Lampiran G). Keenam, kelulusan veraPDF menjamin terpenuhinya aturan yang dapat diperiksa mesin, bukan "
          "kenyamanan pemakaian dengan pembaca layar. Ketujuh, SIMAK adalah alat bantu ULD dan bukan pengganti tenaga ahli.")
set_text(find_par("Penelitian ini memiliki tujuh batasan."), NEWBAT)
ptch(cell_par_of("Mahasiswa tunanetra (pengguna utama)", 1), "Teks alternatif informatif, urutan baca benar, tabel berjudul kolom, rumus dapat diucapkan, dan bahasa dokumen benar bagi pembaca layar",
     "Teks alternatif informatif, urutan baca benar, judul kolom tabel, rumus terucapkan, dan bahasa dokumen benar")

# ---------------- Bab II
ptch(find_par("WCAG 2.2 mensyaratkan"), "bukan materi kuliah.", "bukan materi kuliah. Audit awal penulis (Tabel I) merupakan ukuran pertama pada materi kuliah, dan babak final memperluasnya dengan sampel acak (Bab III.D).")
ptch(find_par("Lundgard dan Satyanarayan"), "dicocokkan dengan sumbernya.", "dicocokkan dengan sumbernya; ChartQA menambah grafik beragam gaya beserta tabel data dan pertanyaan [@chartqa].")
ptch(find_par("Struktur dokumen dan urutan baca."), "tidak terbaca pada dokumen nyata.", "tidak terbaca pada set pengembangan (citra tabel IndoTabVQA dan dokumen kuliah).")
ptch(find_par("Pengenalan rumus dan ucapan."), "menjadi LaTeX [@r35].", "menjadi LaTeX [@r35]; UniMER-Test memuat 23.789 sampel dalam empat kategori (cetak, kompleks, tangkapan layar, tulisan tangan).")
p = find_par("Ringkasnya, alat remediasi")
ptch(p, "melaporkan evaluasi pada materi kuliah berbahasa Indonesia.", "melaporkan evaluasi pada materi kuliah berbahasa Indonesia, sehingga evaluasi SIMAK memakai sampel materi kuliah Indonesia (Tabel V).")
ptch(p, "tidak menjangkau sumber materi terbesar di kampus.", "tidak menjangkau sumber materi terbesar di kampus; audit skala besar menguji dugaan ini melalui metadata pembuat dokumen.")

# ---------------- Bab III
ptch(find_par("Gambar 2 memperlihatkan alur penelitian."), "Data dikumpulkan dari empat sumber, lalu",
     "Data dikumpulkan dari empat sumber (bingkai publik, dokumen sintetis, benchmark publik, dan dokumen nyata pada G6), lalu")
ptch(find_par("Sistem D dibandingkan dengan tiga pembanding"), "Ambang ditetapkan sebelum eksperimen pertama pada set uji tertahan",
     "Ambang, termasuk θe dan θr, disetel pada set pengembangan lalu ditetapkan sebelum eksperimen pertama pada set uji tertahan")
# Tabel VII
ptch(cell_par_of("G1 Struktur dan metadata", 2), "veraPDF pada keluaran D, B0, B1", "veraPDF pada keluaran D, B0, B1 untuk 200 PDF uji")
ptch(cell_par_of("G2 Urutan baca dan tabel", 2), "Dokumen sintetis dengan sumber diketahui", "Dokumen sintetis dengan sumber diketahui; citra tabel IndoTabVQA")
ptch(cell_par_of("G3 Kesetiaan angka", 2), "Tabel data VisText dan grafik buatan penulis", "Tabel data VisText, ChartQA, dan grafik buatan penulis")
ptch(cell_par_of("G5 Rumus", 2), "200 ekspresi bersumber LaTeX diketahui", "100 rumus UniMER-Test dan 150 sintetis")
# Tabel VI
ptch(cell_par_of("CLS-01", 4), "Rencana", "Rencana; 200 gambar berlabel")
# Metrik
ptch(find_contains("dan z kuantil normal baku."), "dan z kuantil normal baku.",
     "dan z kuantil normal baku. Pada audit skala besar, estimasi gabungan dibobot menurut ukuran stratum dan selang juga dihitung dengan bootstrap per kampus.")
# Kelayakan, risiko
ptch(find_par("Analisis tata letak berjalan pada CPU biasa"), "data berlabel berbahasa Indonesia yang memadai belum ditemukan", "data grafik berlabel berbahasa Indonesia yang memadai belum ditemukan")
p = find_par("Risiko utama")
ptch(p, "Ancaman validitas ada tiga.", "Ancaman validitas ada empat.")
ptch(p, "sebagai penilai luar pada G6.", "sebagai penilai luar pada G6. Keempat, bingkai publik hanya mencakup materi yang terbuka dan dirayapi Common Crawl, dan benchmark publik mungkin pernah dilihat VLM; keduanya ditangani dengan stratum pembanding dan dokumen sintetis.")
