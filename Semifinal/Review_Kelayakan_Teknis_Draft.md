# Review Kelayakan Teknis: Draft Semifinal ICC 2026 (Bab 1–3)

Tanggal: 29 Sep 2026. Objek: `Draft/Draft_Semifinal_ICC2026_Bab1-3.docx`.
Skrip uji: `Audit/Spike_Kelayakan/`. Semua angka "uji tim" di bawah berasal dari satu kali jalan di laptop tim (CPU saja, tanpa GPU, RAM 15 GB, disk kosong 22 GB, Python 3.13, Java 21).

> **Status 29 Sep 2026 (malam):** perbaikan butir bagian 7 sudah diterapkan ke `Draft/content.py` (naskah v3). Lihat catatan perubahan di percakapan; versi sebelum pemangkasan tersimpan sebagai `Draft/content_v3_full.py.bak`.

## 1. Putusan

**Idenya layak dibuat sebagai MVP, tetapi tidak dengan lingkup dan rancangan gerbang seperti tertulis sekarang.** Bagian yang paling menakutkan ternyata paling mudah (menulis tag PDF/UA). Bagian yang tampak mudah ternyata paling berisiko (verifikasi rumus dan verifikasi angka). Ada empat cacat rancangan yang perlu diperbaiki di naskah, dua di antaranya terbukti gagal saat saya jalankan.

| Komponen | Putusan | Dasar |
|---|---|---|
| Struktur dan tag PDF (STR-01, OUT-01) | **Hijau, terbukti** | Uji tim, bagian 2 |
| Antarmuka tinjauan ULD (REV-01) | Hijau | Web biasa; tidak ada risiko riset |
| Statistik grafik oleh kode (CHT-02) | Hijau | Deterministik |
| Ekstraksi tabel data dari grafik oleh VLM (CHT-01) | **Merah/belum diketahui**, risiko nomor 1 | Tidak bisa diuji di sini (tidak ada VLM/API) |
| Gerbang angka (Pers. 2 dan 5) | **Kuning, cacat rancangan** | Uji tim, bagian 3 |
| Pengenalan rumus dan gerbang SSIM (FRM-01, Pers. 6) | **Merah, gerbang tidak valid** | Uji tim, bagian 3 |
| Ucapan rumus MathCAT (FRM-02) | Kuning | Aturan Indonesia ada, tetapi tidak ada paket `pip` |
| Klasifikasi/penyaringan gambar dekoratif (CLS-01) | Kuning | Ada pertanyaan teknis terbuka (bagian 4, butir 7) |

## 2. Yang terbukti (uji langsung)

Semua PDF uji adalah contoh paper lomba di folder ini, bukan materi kuliah asli. Validasi memakai veraPDF 1.30.2, profil PDF/UA-1.

**a. PDF yang sudah bertag (IFEST Teen Tensors, 18 hlm, 113 Figure, 0 alt, sudah berbahasa `id-ID`).**
veraPDF awal: 1 aturan gagal (7.3-1, Figure tanpa alt, ×113). Setelah patch teks alternatif dan metadata dengan `pikepdf`: **lulus penuh (0 aturan gagal)**. Waktu patch 0,38 detik.

**b. PDF tak bertag (paper 21 hlm).**

| Tahap | Aturan gagal | Pemeriksaan gagal |
|---|---|---|
| PDF asli | 11 | 4.020 |
| Setelah auto-tag OpenDataLoader (4,6 detik) | 8 | 2.120 |
| Setelah patch ±30 baris (Lang, MarkInfo, DisplayDocTitle, Title/XMP, Tabs, penanda PDF/UA, Alt) | **0** | **0** |

**c. Deck 43 slide.** Auto-tag 10,5 detik. Setelah patch metadata, **belum lulus**: tersisa 3 aturan (22 pemeriksaan): level judul melompat (7.4.2-1 ×6), tipe struktur non-standar belum dipetakan ke tipe standar (7.1-5 ×14), sel tabel saling bertumpuk (7.2-15 ×2). Ketiganya bisa diperbaiki (RoleMap, normalisasi level judul), tetapi tumpukan sel tabel mungkin butuh jalur cadangan (HTML saja). Ini belum terbukti.

**d. Temuan tentang OpenDataLoader (baseline B1), berlaku untuk 2 dokumen tak bertag:**
- Auto-tag gratis (Apache 2.0) menghasilkan `TD` tetapi **tidak satu pun `TH`** (0 dari 13 dan 0 dari 85 sel), tidak ada tag `Formula`, dan tidak mengisi `Lang` maupun `MarkInfo`.
- Ia mengisi `/Alt` dengan **placeholder `"image 1"`, `"image 2"`, ...** dan **veraPDF meloloskannya** (tidak ada kegagalan 7.3-1). Jadi validator menyatakan "punya teks alternatif" untuk isi yang tidak bermakna. Ini mendukung tesis naskah, tetapi juga berarti metrik G1 harus didefinisikan ulang (lihat butir P4).

**e. Kinerja komputasi.** Docling melaporkan 0,60–0,94 halaman/detik pada Xeon E5-2690 (4 thread, OCR mati) dengan RAM 2,4–6,2 GB (laporan teknis Docling, arXiv:2408.09869, Tabel 1). Klaim "berjalan pada perangkat biasa [28]" di naskah **didukung**, dengan catatan OCR mati. Uji tim atas OpenDataLoader di atas juga cukup cepat. Karena VLM lewat API, tidak perlu GPU.

## 3. Yang terbukti cacat (uji langsung)

**P1. Gerbang rumus berbasis SSIM (Pers. 6, G5) tidak valid.** Saya membandingkan render "dokumen asli" dengan render ulang LaTeX memakai dua font berbeda (proksi: mathtext DejaVu vs Computer Modern), pada 5 rumus dengan satu simbol diubah (mis. `+`→`−`, pangkat 2→3).

| | SSIM |
|---|---|
| Rumus benar, font berbeda | 0,65–0,87 |
| Rumus **salah**, font sama | 0,97–0,99 |
| Rumus salah, font berbeda | 0,64–0,87 |

Skor didominasi font dan tata letak, bukan isi matematika. Rumus benar yang beda font justru skornya lebih rendah daripada rumus salah yang tampil sama (5 dari 5 kasus). Tidak ada ambang yang memisahkan keduanya. Batas uji: proksi font, bukan TeX sungguhan, 5 rumus; kesimpulan arahnya kuat, angkanya bukan estimasi akhir.
**Perbaikan:** jangan jadikan SSIM gerbang kebenaran. Pilihan (urut saran): (i) rumus **selalu** masuk antrean tinjauan dengan gambar berdampingan dan ucapan MathCAT (konsisten dengan prinsip fail-closed); (ii) konsensus dua pengenal berbeda (mis. UniMERNet dan VLM) dengan LaTeX ternormalisasi, dan hanya yang sepakat yang lolos; (iii) SSIM hanya sebagai penyaring kasar untuk sampah (misalnya ambang rendah), dinyatakan begitu.

**P2. Kesetiaan angka (Pers. 5) tidak mendeteksi kesalahan yang paling berbahaya.** Diuji dengan T = [40, 55, 62, 48] untuk Jan–Apr:
- "tertinggi pada **Maret** sebesar 62" (benar) dan "tertinggi pada **Januari** sebesar 62" (salah): keduanya Fnum = 1,0. Pemeriksaan bersifat "angka ini ada di tabel mana saja", tidak memeriksa pasangan label–nilai.
- "turun 14 poin" (benar, 62−48) mendapat Fnum = 0,0 karena 14 tidak ada di T. Jadi gerbang menolak angka turunan yang benar, padahal desain (level 2) justru mengandalkan angka turunan.
- Label berangka ("Q3", "2023", "Semester 2") ikut dihitung sebagai angka yang tidak cocok.
**Perbaikan:** verifikasi pada tingkat klaim terstruktur `(entitas, ukuran, nilai)`, bukan pemindaian angka di kalimat akhir. Karena kalimat dibangun dari templat yang diisi kode, cukup kunci token angka dan label saat VLM menyunting (diff terhadap templat); tolak bila berubah. Untuk MVP, boleh tanpa VLM penyunting sama sekali.
Selain itu, di naskah Pers. 5 dipakai baik sebagai gerbang (terhadap T hasil ekstraksi) maupun sebagai metrik G3 (terhadap tabel acuan). Itu dua besaran berbeda; jika tidak dipisah, Fnum pada keluaran terbit bernilai 1,0 **menurut definisi** (tautologi). Pisahkan: `Fnum-gerbang` vs `Fnum-acuan`.

**P3. Selisih antar-ekstraksi (Pers. 2) bergantung satuan, dan tidak menangkap kesalahan sistematik.**
- Data sama, dua ekstraksi yang sangat berbeda: δ = 0,073 bila dinyatakan sebagai proporsi (0–1), tetapi 0,274 bila dinyatakan dalam persen. Lantai `max(…,1)` melemahkan pemeriksaan pada data berskala kecil. Normalisasikan dengan rentang sumbu atau rentang nilai.
- Salah baca skala sumbu (×10) yang sama pada kedua ekstraksi memberi δ = 0 dan lolos. Ekstraksi ganda hanya menangkap kesalahan acak. Akui ini di Batasan/Ancaman Validitas dan tambahkan pemeriksaan skala (mis. cocokkan label tik sumbu yang dibaca dengan nilai maksimum).

**P4. Metrik G1 dan baseline B1 harus mengecualikan alt placeholder.** Lihat 2d. Definisikan "teks alternatif ada" sebagai tidak kosong **dan** bukan pola placeholder (`image N`, nama berkas, "gambar"). Tanpa ini, B1 tampak lulus G1 dan perbandingan tidak adil.

## 4. Risiko dan celah lain

5. **Ekstraksi grafik oleh VLM (CHT-01) belum teruji.** Seluruh nilai sistem (gerbang, deskripsi level 2–3, G3, G4) bergantung pada seberapa akurat tabel data yang diekstraksi dari grafik Indonesia nyata, terutama grafik tanpa label nilai (nilai harus diperkirakan dari piksel). Ini spike hari pertama (bagian 6). Cadangan yang layak dipertimbangkan: untuk PDF yang grafiknya vektor, data dapat dibaca dari jalur vektor dan teks label secara deterministik.
6. **Dua alat tata letak (Docling dan OpenDataLoader) dalam satu rancangan.** Tabel 5 memakai Docling untuk STR-01, sedangkan baseline B1 dan seluruh bukti di atas memakai OpenDataLoader. Putuskan satu tulang punggung. Saran: OpenDataLoader sebagai tulang punggung (sudah menghasilkan PDF bertag dan JSON dengan kotak pembatas serta `alt_source`), Docling hanya bila uji pada 5 dokumen nyata menunjukkan tabel tanpa garis tidak terbaca. Catatan: OpenDataLoader mode bawaan mendeteksi tabel berbasis garis; belum saya uji pada tabel tanpa garis.
7. **Gambar dekoratif dan PDF/UA.** IFEST punya 113 Figure di 18 halaman; banyak yang kemungkinan dekoratif. Menandai dekoratif berarti mengubah menjadi Artifact di aliran konten (bukan sekadar mengubah tag); menghapus elemen struktur saja akan memicu kegagalan 7.1-3 ("konten harus di-Artifact atau bertag"). Pekerjaan `pikepdf` di aliran konten mungkin tetapi rumit; belum saya uji. Ini juga alasan penyaring CLS-01 tidak bisa dianggap sepele.
8. **MathCAT tidak tersedia lewat `pip`.** Aturan Indonesia (`Rules/Languages/id`, ClearSpeak dan SimpleSpeak) terverifikasi ada, tetapi pustakanya Rust; binding Python memakai pyo3 dan tidak terbit sebagai paket PyPI. Jalur: (a) pakai versi WASM di peramban (demo resmi MathCAT begitu), cocok karena antarmuka tinjauan memang web; (b) pasang Rust dan bangun sendiri (di mesin ini belum ada Rust). Kelengkapan aturan Indonesia untuk kalkulus/matriks belum saya nilai; yang terlihat lengkap adalah pecahan, akar, dan pangkat.
9. **PDF hasil pindai.** Materi kuliah sering berupa pindaian tanpa lapisan teks. Naskah tidak menyebutnya di Batasan. Sistem harus menolak atau memasukkan seluruh dokumen ke antrean, dan itu harus dinyatakan.
10. **"Lulus veraPDF" bukan "dapat dipakai pembaca layar".** Kepatuhan mesin tidak menjamin urutan baca yang benar atau pengalaman NVDA. Belum ada uji dengan pembaca layar. Tambahkan uji tim sederhana dengan NVDA pada beberapa keluaran, dan jangan menulis "aksesibel" hanya berdasarkan veraPDF.
11. **Demo harus muat di 15 menit dan bergantung jaringan.** TM: "wajib working prototype minimal MVP, bukan mockup, dan sesuai metodologi". Demo di dalam slot presentasi 15 menit, tanpa slot terpisah, di venue luring. Panggilan VLM lewat API rawan lambat/putus. Siapkan hasil ter-cache untuk dokumen demo dan jalur langsung sebagai tambahan, bukan satu-satunya.
12. **Jadwal.** Pengumuman finalis 10 Okt; karya lengkap 23 Okt. Rencana "1–7 Okt" berarti membangun sebelum tahu lolos, dan setelah pengumuman hanya tersisa 13 hari. Sembilan fitur, tujuh gerbang, tiga baseline, dan Bab 4–5 dalam ±3 minggu terlalu padat.

## 5. Lingkup MVP yang disarankan

**Wajib (memenuhi "sesuai metodologi" dan menyentuh nilai inti):** unggah PDF → auto-tag (OpenDataLoader) → patch Lang/MarkInfo/judul/Tabs/penanda PDF/UA → **TH pada baris judul tabel** → deskripsi grafik dari tabel data (ekstraksi ganda, statistik oleh kode, templat) → gerbang terklaim-terstruktur → antrean tinjauan ULD → keluaran PDF bertag + HTML → laporan veraPDF sebelum/sesudah.
**Opsional:** rumus (semua ke antrean tinjauan, dengan ucapan MathCAT bila WASM berhasil dalam sehari), G4.
**Tunda:** SSIM sebagai gerbang, G7, braille, PowerPoint/Word langsung.
Evaluasi cukup: G1 (tanpa alt placeholder), G3 (tabel acuan, klaim terstruktur), G6 versi ringan, dan G4 bila waktu ada. Tujuh gerbang terlalu banyak untuk satu tim dalam jadwal ini.

Arsitektur ringkas: Python (FastAPI sudah terpasang) + OpenDataLoader (Java 11+) + `pikepdf`/PyMuPDF + veraPDF CLI + VLM lewat API yang tidak terikat penyedia + halaman web statis untuk tinjauan. Disk tersisa 22 GB (96% terisi): cukup, tetapi jangan mengunduh banyak model lokal.

## 6. Spike yang harus dijalankan dulu (berurutan, masing-masing ±setengah hari)

1. **VLM grafik→tabel:** 20–30 grafik sintetis berbahasa Indonesia dengan data diketahui (batang, garis, pai, dengan dan tanpa label nilai). Ukur galat nilai, konsistensi dua kali jalan, biaya dan latensi per grafik. Putusan go/no-go untuk modul grafik.
2. **veraPDF pada 5 materi kuliah nyata** (sertakan file PPT milik tim): berapa yang lulus setelah alur di bagian 2; catat penyebab kegagalan tersisa.
3. **Artifact dekoratif** lewat aliran konten (butir 7).
4. **MathCAT WASM** menghasilkan ucapan Indonesia untuk 10 rumus; kalau gagal dalam sehari, rumus hanya ke antrean tinjauan.
5. **Rumus:** bila waktu ada, UniMERNet di CPU pada 30 rumus vs VLM sebagai pengenal; lisensi UniMERNet Apache-2.0, model 441 MB–1,3 GB, tidak ada angka kecepatan CPU di repositori.

## 7. Kurasi naskah

**Sebelum tenggat (30 Sep 23.59), perubahan kecil yang aman:**
- Hapus SSIM sebagai *syarat lulus* pada Pers. 8 dan G5 (Tabel 6), atau turunkan menjadi penyaring kasar. Bila tidak sempat menata ulang persamaan, cukup ubah kalimat dan baris tabelnya; jangan biarkan naskah menjanjikan gerbang yang terbukti tidak bekerja.
- Pisahkan definisi Fnum untuk gerbang dan untuk metrik G3; ganti "angka cocok" menjadi pemeriksaan klaim `(label, nilai)`; sebutkan angka turunan dihitung kode sehingga tercakup.
- Tetapkan satu tulang punggung tata letak (Tabel 5: STR-01) dan samakan dengan B1.
- Tambahkan di Batasan: PDF pindai; kesalahan sistematik pada ekstraksi ganda; kepatuhan veraPDF bukan uji pembaca layar.
- Definisikan "teks alternatif ada" tanpa placeholder pada G1.
- Perbarui baris OpenDataLoader di Tabel 3 dengan pengamatan tim (alt placeholder, tanpa TH/Formula/Lang) dan tandai jelas "uji tim, n = 2 dokumen".
- Ganti klaim lingkup MVP "PDF bertag hanya untuk dokumen yang sudah bertag" bila Anda yakin jalur auto-tag akan dibangun; jika ragu, biarkan sebagai lingkup minimum.
- Rencana kerja: tandai fitur wajib vs opsional agar Bab 3 tidak menjanjikan lebih dari yang akan didemokan.

**Pertahankan:** posisi klaim yang sempit, kejujuran status bukti di Tabel 2, batasan yang eksplisit, prinsip fail-closed, dan audit awal (kini ditambah bukti bahwa validator meloloskan placeholder).

**Yang belum saya periksa:** kebenaran seluruh 43 referensi (saya tidak mengulang verifikasi sitasi di sesi ini), hasil Turnitin, dan uji dengan pembaca layar sungguhan. Penilaian ini juga tidak menguji kualitas urutan baca pada materi kuliah asli.

## 8. Catatan jujur tentang batas bukti

- Tiga dokumen uji, semuanya contoh paper lomba, bukan sampel materi kuliah. Hasil PDF/UA "0 aturan gagal" berlaku untuk dokumen tertentu itu.
- Angka SSIM memakai proksi font, bukan TeX; arah temuannya kuat, tetapi ambang sebenarnya perlu diukur pada render asli.
- Uji gerbang angka memakai data buatan; menunjukkan cacat logika, bukan laju kesalahan di dunia nyata.
- Pernyataan Lampiran A perlu diperbarui: skrip uji kelayakan ini dibuat dengan bantuan AI, dan penulis perlu menyesuaikan pernyataannya dengan penggunaan sebenarnya.
