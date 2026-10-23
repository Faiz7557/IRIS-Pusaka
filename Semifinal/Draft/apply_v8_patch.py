# -*- coding: utf-8 -*-
p = "edit_paper_v6.py"
s = open(p, encoding="utf8").read()


def rep(old, new):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, 1)


# P3: jembatan dari audit awal ke rencana data final
rep('memiliki teks alternatif (Tabel I; sampel tidak acak).")',
    'memiliki teks alternatif (Tabel I). Karena sampelnya kecil dan tidak acak, audit ini hanya membuktikan bahwa masalahnya ada, "\n      "bukan seberapa luas; babak final memperluasnya dengan sampel acak dari bingkai publik (Bab III.D).")')
# P4: penutup
rep('Karena itu, diperlukan alur yang membuktikan bahwa "\n      "deskripsi setia pada datanya dan menahan yang tidak terbukti.")',
    'Belum ada ukuran kesetiaan deskripsi grafik pada materi "\n      "kuliah berbahasa Indonesia, sehingga diperlukan alur yang membuktikan bahwa deskripsi setia pada datanya dan menahan yang "\n      "tidak terbukti, serta data evaluasi yang mencakup materi tersebut (Bab III.D).")')
# P5 lebih ringkas
a = s.index('P5 = (')
b = s.index('P6 = (')
P5 = '''P5 = ("Masalah yang sama dialami mahasiswa yang memilih mendengarkan. Indonesia memiliki proporsi pendengar podcast mingguan "
      "tertinggi di antara negara yang diukur, yaitu 42,6% pengguna internet berusia 16 tahun ke atas pada awal 2025 [@r13], "
      "sedangkan alat bacaan suara (*text-to-speech*, TTS) melewatkan grafik, rumus, dan tabel tanpa teks alternatif. Kebiasaan ini "
      "hanya indikator preferensi, bukan bukti bahwa mendengarkan meningkatkan hasil belajar; teori gaya belajar tidak didukung "
      "bukti memadai [@r14]. Dasarnya adalah akses dan pilihan: Universal Design for Learning menganjurkan beragam cara penyajian "
      "[@r15], fitur bagi kelompok rentan sering bermanfaat bagi banyak orang (*curb-cut effect*) [@r16], dan TTS meningkatkan "
      "pemahaman bacaan siswa dengan kesulitan membaca (meta-analisis 22 studi; ukuran efek 0,35) [@r17]. Karena itu, mahasiswa "
      "tunanetra menjadi pengguna utama, sedangkan manfaat bagi pendengar diperlakukan sebagai hipotesis.")
'''
s = s[:a] + P5 + s[b:]
# P6: kalimat lampiran lebih ringkas
rep('Profil nilai jual, pohon masalah, *value proposition canvas*, skenario sebelum dan sesudah, serta analisis strategis "\n      "(SWOT, TOWS, Porter, PESTEL, risiko, dan peta jalan) dimuat pada Lampiran F.")',
    'Profil nilai jual dan analisis strategisnya dimuat pada Lampiran F.")')
# II.E: hapus kalimat nilai jual per pihak (sudah di Lampiran F.1 dan F.3)
rep('Nilai jualnya berbeda bagi tiap pihak: bagi ULD, keluaran yang dapat "\n      "ditinjau per elemen; bagi mahasiswa, materi yang dapat disimak dengan status yang jelas; bagi institusi, "\n      "kepatuhan yang dapat diukur dengan veraPDF tanpa mengubah alur kerja dosen. Matriks pembanding',
    'Matriks pembanding')
# P_DATA lebih ringkas
a = s.index('P_DATA = (')
b = s.index('set_text(find_par("Tabel V merinci seluruh data."), P_DATA)')
PD = '''P_DATA = ("Tabel V merinci data yang dipakai; Lampiran G memuat inventaris, metadata, dan pemetaannya ke fitur prototipe. "
          "Setiap sumber dibagi menjadi set pengembangan, untuk merancang aturan tambal, skema ekstraksi, dan ambang gerbang, dan set "
          "uji tertahan yang tidak disentuh sampai versi dibekukan. Audit awal (28 PDF) hanya memberi selang sekitar ±17 poin "
          "persentase dan bukan sampel acak; babak final memakai bingkai publik (indeks Common Crawl, PDF pada domain ac.id [@cc]) "
          "dengan sampel acak berstrata 600 PDF berbahasa Indonesia (400 materi kuliah menurut aturan URL, 200 dokumen akademik lain; "
          "maksimum 12 dokumen per domain) berselang sekitar ±5 poin pada stratum materi kuliah, dengan bootstrap per kampus dan "
          "tangkapan terpotong dilengkapi korpus SafeDocs [@safedocs]. Ukuran 60 dokumen G6 dipilih agar hasil teramati 90% berbatas "
          "bawah selang Wilson sekitar 80%.")
'''
s = s[:a] + PD + s[b:]
# RENCANA
rep('validasi veraPDF pada lima materi nyata, "\n           "bersama', 'validasi veraPDF pada lima materi nyata dari set pengembangan, "\n           "bersama')
# exec blok koherensi sebelum penomoran ulang
marker = "# ------------------------------------------------------------------ 3) nomori ulang menurut urutan kemunculan"
rep(marker, "exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'koherensi_v8.py'), encoding='utf8').read())\n\n" + marker)
open(p, "w", encoding="utf8").write(s)
print("ok")
