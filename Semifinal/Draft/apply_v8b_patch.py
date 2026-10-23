# -*- coding: utf-8 -*-
s = open("edit_paper_v6.py", encoding="utf8").read()
k = open("koherensi_v8.py", encoding="utf8").read()


def rep(txt, old, new):
    assert old in txt, old[:80]
    return txt.replace(old, new, 1)


# P1 lebih ringkas
a = s.index("P1 = (")
b = s.index("P2 = (")
P1 = '''P1 = ("Transformasi digital memindahkan materi kuliah dari kertas ke berkas PDF, tetapi akses digital tidak otomatis "
      "berarti aksesibilitas. Pangkalan Data Pendidikan Tinggi (PDDikti) per Juni 2025 mencatat 3.128 mahasiswa "
      "disabilitas di 282 perguruan tinggi, dan tunanetra merupakan kelompok terbesar dengan 1.727 orang [@r3]; perguruan "
      "tinggi berkewajiban menyediakan akomodasi yang layak dan membentuk Unit Layanan Disabilitas (ULD) [@r1,@r2]. "
      "Namun, tinjauan sistematis atas 60 studi menemukan bahwa konten digital yang tidak aksesibel, keterbatasan "
      "infrastruktur, dan kurangnya pelatihan tetap menjadi hambatan utama mahasiswa tunanetra, padahal pembaca layar "
      "(*screen reader*) dan layar braille telah tersedia [@gidisu]. Ketersediaan teknologi bantu pun tidak cukup; "
      "implementasinya dipengaruhi kebijakan institusi, pendanaan, dan kebutuhan individu [@almalky].")
'''
s = s[:a] + P1 + s[b:]
# P4: kalimat Khlaif lebih ringkas (rinciannya ada di Bab II.B)
s = rep(s, "AI generatif tampak menjawab \"\n      \"kebutuhan ini: 21 mahasiswa tunanetra di Palestina melaporkan manfaat personalisasi, akses inklusif, dan \"\n      \"multimodalitas [@khlaif]. ",
        "AI generatif tampak menjawab \"\n      \"kebutuhan ini: 21 mahasiswa tunanetra di Palestina melaporkan manfaat personalisasi dan akses inklusif [@khlaif]. ")
# II.B: kalimat lebih ringkas
a = s.index('ptch_dummy') if 'ptch_dummy' in s else -1
old = ('Studi terbaru tentang AI generatif bagi mahasiswa tunanetra melaporkan persepsi manfaat "\n      "berdasarkan wawancara [@khlaif], sedangkan penelitian pembuatan deskripsi gambar terbaru, misalnya HI-Captioner, dievaluasi "\n      "pada foto alami MSCOCO dan Flickr [@hicap]; keduanya belum mengukur kesetiaan deskripsi grafik terhadap data sumbernya.")')
assert old in s
s = s.replace(old, 'Studi AI generatif bagi mahasiswa tunanetra melaporkan persepsi manfaat dari wawancara [@khlaif], dan "\n      "HI-Captioner dievaluasi pada foto alami [@hicap]; keduanya belum mengukur kesetiaan deskripsi grafik terhadap datanya.")', 1)
# RENCANA: buang kalimat penutup
s = rep(s, ' Seluruh "\n           "komponen utama berupa kode terbuka (Tabel IV).")', '")')
# Batasan: tulis ulang ringkas
a = k.index("# ---------------- Bab I: Batasan")
b = k.index("# ---------------- Bab II")
BAT = '''# ---------------- Bab I: Batasan
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

'''
k = k[:a] + BAT + k[b:]
open("edit_paper_v6.py", "w", encoding="utf8").write(s)
open("koherensi_v8.py", "w", encoding="utf8").write(k)
print("ok")
