# Brief dan Rencana Penulisan Paper Final SIMAK (ICC 2026)

Versi 23 Oktober 2026, ±01.40 WIB. Batas unggah: **23 Oktober 2026, 23.59 WIB**; target unggah **21.00 WIB**.
Pelengkap dokumen `AUDIT_DAN_RENCANA_FINAL.md` (temuan audit A1–A18, B1–B7 dirujuk dengan kode yang sama).
Disusun dengan skill `academic-paper` mode *outline-only* (struktur, alokasi panjang, peta bukti), tanpa draf.

---

## 0. Aturan main dokumen ini (baca dulu)

1. **Dokumen ini bukan naskah.** Guidebook 7.2.4 melarang AI generatif menghasilkan rumusan masalah, analisis,
   argumen, metodologi, interpretasi hasil, kesimpulan, atau narasi substansial. Karena itu setiap subbab di bawah
   berisi: tujuan, angka/bukti yang wajib dipakai dan lokasinya, pertanyaan pemandu, serta kriteria selesai.
   **Kalimat paper ditulis tim sendiri.**
2. **Jangan menyalin kalimat dari dokumen ini ke paper.** Selain melanggar 7.2.4, teks di sini ikut terbaca Turnitin.
3. **Angka hanya diambil dari berkas sumber** (`Prototype/eval/results.json` dan berkas lain yang disebut di §5),
   tidak dari ingatan, tidak dari dokumen ini. Dokumen ini mencantumkan angka run 1 sebagai patokan; setelah run 2
   selesai, angka run 2 menggantikannya (§5).
4. **Lampiran A (pernyataan AI) harus menggambarkan penggunaan AI yang sebenarnya pada versi final.** Lihat §8.4.

---

## 1. Brief satu halaman

| Butir | Isi |
|---|---|
| Judul (tetap) | SIMAK: Remediasi Materi Kuliah Berbahasa Indonesia agar Dapat Disimak oleh Mahasiswa Tunanetra dan Pendengar dengan Gerbang Verifikasi |
| Tim / penulis | IRIS kata HQ ini lomba terakhir; 4 penulis, Universitas Airlangga |
| Topik dan 3 rumusan masalah | **Tidak boleh berubah** (7.2.4 butir 7). RM1 struktur dan urutan baca; RM2 deskripsi grafik dan pembacaan rumus yang setia; RM3 alur kerja yang menahan keluaran tak terverifikasi ke peninjau ULD |
| Yang baru di final | Bab IV Hasil dan Pembahasan; Bab V Penutup; revisi minor Bab I–III agar sesuai MVP; abstrak berisi hasil; Lampiran A, B (Turnitin) final; Lampiran H (reproduksi) |
| Pembaca | Dewan juri ICC: menilai kelengkapan dan konsistensi (20%), dan memakai paper untuk memeriksa apakah demo (30%) membuktikan isinya. Juri juga menyiapkan pertanyaan tanya jawab (20%) dari paper |
| Pesan inti yang harus terbukti | Sesuai klaim semifinal: setiap deskripsi grafik yang terbit terverifikasi terhadap data atau diberi penanda "ditahan", dengan biaya tinjauan (R) yang diukur. Rumusan kalimatnya ditulis tim |
| Bukti utama | G1, G3, G4 pada set uji tertahan sintetis (run 1 dan run 2), pembanding B0/B1/B2, G6 ringan pada 6 PDF nyata, audit B2 manual, tangkapan layar MVP |
| Batasan yang wajib diakui | Set uji sintetis buatan tim; G6 berisi dokumen administratif; rumus selalu ditahan; T1/T2/QA satu model; G1 menghitung penanda tahan; G2, G5, G7 belum dijalankan (detail §4, IV.D) |
| Format | Template panitia: Times New Roman 10 pt, satu spasi, rata kiri-kanan, judul bab angka Romawi rata tengah, subbab huruf miring rata kiri, keterangan gambar di bawah dan tabel di atas (9 pt), referensi 8 pt gaya bernomor, rujukan persamaan "(1)" |
| Berkas keluaran | `IRIS kata HQ ini lomba terakhir_ICC2026_Final.pdf` + link GitHub `github.com/Faiz7557/IRIS-Pusaka` |
| Kepatuhan | Similarity Turnitin < 15% (di luar kutipan dan pustaka) dan dilampirkan; pernyataan AI di lampiran; Bahasa Indonesia baku |

---

## 2. Keputusan yang harus diambil sebelum menulis (paling lambat 08.00)

| # | Keputusan | Pilihan | Dampak |
|---|---|---|---|
| K1 | Batas halaman final | Tanyakan panitia sekarang. Tanpa jawaban sampai 10.00, **pakai skenario A (10 halaman tanpa lampiran)** karena itu aturan tertulis terakhir | Menentukan anggaran §3 |
| K2 | Basis berkas | **Salin `Semifinal/Draft/Fix/IRIS kata HQ ini lomba terakhir_ICC2026_Semifinal.docx`**, sunting di Word. Jangan membangun ulang dari `content.py`: isinya tertinggal (47 referensi vs 54+ di PDF semifinal) | Menghindari kehilangan suntingan manual |
| K3 | Pembagian penulis | W1: Bab IV; W2: Abstrak, Bab I–III, Bab V, Lampiran; E: angka, tabel, gambar, Turnitin; P: tangkapan layar dan kecocokan demo | Paralel, tanpa saling menimpa bab |
| K4 | Satu penyunting akhir | Satu orang memegang berkas induk setelah 16.00; yang lain mengirim perubahan sebagai komentar | Mencegah konflik versi |

Folder kerja usulan: `Final/Paper/` berisi `…_Final.docx` (induk), `gambar/`, berkas angka kanon (§5), dan `turnitin/`.

---

## 3. Arsitektur dan anggaran panjang

Struktur: pola IMRaD sesuai template dan ketentuan final (Bab I–V). Kapasitas semifinal sebagai patokan:
10 halaman memuat ±7.900 kata termasuk tabel dan referensi (Abstrak ±250, Bab I 1.802, Bab II 1.671,
Bab III 2.571, Referensi 1.616), 8 tabel, 3 gambar, 10 persamaan.

| Bagian | Skenario A: tetap 10 hlm (tanpa lampiran) | Skenario B: tanpa batas ketat | Catatan |
|---|---|---|---|
| Abstrak + kata kunci | ≤ 250 kata | ≤ 250 kata | Template: 100–250 kata, tebal, 9 pt |
| I. Pendahuluan | ±1.150 (−650) | ±1.700 | Padatkan Tabel 1–3 |
| II. Tinjauan Pustaka | ±1.100 (−570) | ±1.650 | Pertahankan pers. (1)–(10) |
| III. Metodologi | ±1.700 (−870) | ±2.400 | Tabel 8 dan Gambar 3 ke lampiran |
| IV. Hasil dan Pembahasan | ±1.800 | ±2.400 | 3 tabel + 1–2 gambar |
| V. Penutup | ±450 | ±650 | Tanpa tabel |
| Referensi | ±1.400 | ±1.650 | Hapus rujukan yang tak lagi dikutip |
| **Total** | **±7.850** | **±10.500** | Skenario A: deviasi ≤ ±5% dari 7.900 |

Pemindahan ke lampiran pada skenario A (urut dari yang paling aman): Tabel 8 (uji kelayakan awal) → Lampiran D;
Gambar 3 (kerangka tujuh langkah) → Lampiran F; Tabel 2 (profil pengguna) dipadatkan; Tabel 5 diringkas dengan
rujukan ke Lampiran G. Tabel 4 (solusi yang ada) dan Tabel 7 (gerbang terkunci) **tetap di badan**, karena
dibutuhkan juri untuk memeriksa posisi dan kriteria.

---

## 4. Outline rinci per bab

Format tiap subbab: **Tujuan** · **Bukti wajib (lokasi)** · **Pertanyaan pemandu** (dijawab tim dengan kalimat
sendiri) · **Selesai bila**. Kode A#/B# merujuk temuan audit.

### Abstrak (W2, ditulis setelah Bab IV selesai)
- **Tujuan:** ringkasan masalah, pendekatan, hasil utama, dan batasan terpenting dalam ≤ 250 kata.
- **Bukti wajib:** satu angka besaran masalah (audit awal 0/28 lulus PDF/UA-1; 29/1.111 Figure beralt), angka
  utama G3 dan B2, R, satu batasan (set uji sintetis atau G6 kecil).
- **Ganti:** pernyataan semifinal bahwa makalah belum melaporkan kinerja harus hilang.
- **Pertanyaan pemandu:** angka mana yang paling langsung membuktikan janji di Bab I? Batasan mana yang paling
  mungkin ditanyakan juri dan harus disebut sejak abstrak?
- **Selesai bila:** semua angka di abstrak muncul identik di Bab IV; tidak ada klaim yang tidak ada di badan.

### I. Pendahuluan (W2) — revisi minor
| Subbab | Perubahan wajib | Bukti / lokasi |
|---|---|---|
| A. Latar Belakang | Padatkan (skenario A); data masalah tidak diubah | Tabel 1 tetap; baris boleh digabung |
| B. Profil Pengguna | Tabel 2 dipadatkan; status bukti diperbarui (OUT-02 kini ada) | §5, mode dengar |
| C. Rumusan Masalah | **Tidak diubah satu kata pun** | Salin dari semifinal |
| D. Tujuan, Kontribusi, Manfaat | Tabel 3 kolom "Status" diperbarui dari "belum diukur" ke hasil nyata atau "tidak dijalankan" | §5; janji yang tak terbukti tetap ditulis tak terbukti |
| E. Batasan | Sesuaikan dengan kenyataan (mis. data uji sintetis); detailnya di IV.D | A6, A14 |
- **Selesai bila:** RM identik dengan semifinal; Tabel 3 tidak lagi memuat status per 30 September.

### II. Tinjauan Pustaka (W2) — revisi minor
| Subbab | Perubahan wajib | Bukti / lokasi |
|---|---|---|
| A–B | Padatkan; isi tetap | — |
| C. Landasan dan Persamaan Kunci | Pers. (7): himpunan pemeriksaan grafik menjadi {cF, cδ, cA, cL}; tambahkan definisi cL dan asal-usulnya dari kalibrasi set pengembangan. Pertahankan kalimat bahwa Fk terhadap T bernilai 1 menurut definisi (A10) | `simak/gate.py` docstring; `simak/thresholds.json` "riwayat" |
| C | Sebut cadangan tabel yang benar-benar dipakai (PyMuPDF `find_tables`), bukan Docling | `simak/pipeline.py` `_blocks` |
| D. Solusi yang Ada | Tetap | — |
| E. Kesenjangan dan Posisi | Tetap | — |
| Referensi | Tambahkan [55] SafeDocs dan [56] MathCAT/WebAssembly yang dikutip tetapi hilang dari daftar | PDF semifinal hlm. 7–8 |
- **Selesai bila:** setiap simbol di pers. (7) sama dengan kode; tidak ada rujukan yatim.

### III. Metodologi (W2) — revisi minor, hanya agar sesuai MVP
| Subbab | Perubahan wajib | Bukti / lokasi |
|---|---|---|
| A. Gambaran Solusi | Tetap | Gambar 1 |
| B. Arsitektur | Sebut model: Gemma 4 26B-A4B lewat Gemini API, suhu 0, cache per hash; T1 dan T2 memakai model yang sama dengan dua perintah berbeda (alasan: kuota). Mode dengar: Web Speech API id-ID (Microsoft Andika) bawaan, ElevenLabs opsional | `README.md` bagian Model; `simak/vlm.py`; commit `5d01a55` |
| C. Alur Penelitian | Janji "dijalankan dua kali" kini dipenuhi run 1 (12 Okt) dan run 2 (23 Okt); hasilnya di IV.B | `eval/banding_run.py` |
| D. Dataset | Tabel 5 tetap sebagai rancangan; tambahkan rujukan ke tabel realisasi di IV.A | B5 |
| E. Kerangka Fitur, Tabel 6 | Kolom Status: jalan / sebagian / belum. CHT-02 menjadi templat murni (tanpa VLM penyunting); FRM-01/02 belum, semua rumus ditahan; OUT-02 jalan (Web Speech); REV-01 jalan | A16, A18; README "Pemetaan ke proposal" |
| F. Komponen Pipeline | Modul grafik: hapus peran VLM penyunting kalimat. Modul rumus: nyatakan status fail-closed | A18, A16 |
| G. Rancangan Evaluasi, Tabel 7 | **Kriteria terkunci tidak diubah.** G1-ketat disebut sebagai pelaporan tambahan, bukan kriteria baru | A5 |
| H. Uji Kelayakan Awal | Skenario A: Tabel 8 ke Lampiran D, sisakan 2–3 kalimat | — |
| I. Rencana Kerja | Jadwal 1–23 Okt dihapus atau diganti satu kalimat realisasi | — |
| J. Risiko dan Ancaman Validitas | Tetap; tambahan dibahas di IV.D | — |
- **Selesai bila:** tidak ada fitur di Bab III yang tidak ada di demo tanpa diberi status "belum diimplementasikan".

### IV. Hasil dan Pembahasan (W1) — baru, ±1.800 kata (skenario A)

#### IV.A Hasil Implementasi (±400 kata, Gambar 4, Tabel 9)
- **Tujuan:** menunjukkan apa yang benar-benar dibangun, dengan bukti visual.
- **Bukti wajib:**
  - **Gambar 4** (montase 2×2, satu gambar): (a) Remediasi & Tinjauan dengan antrean ULD dan panel veraPDF
    B0→B1→D; (b) Demo Gerbang setelah "suntik kesalahan" (B2 terbit, SIMAK ditahan); (c) halaman Evaluasi;
    (d) HTML keluaran dengan cap status dan bilah mode dengar. Diambil P dari server lokal setelah P0 selesai.
  - **Tabel 9: Realisasi fitur** — kolom: ID (Tabel 6), status (jalan / sebagian / belum), berkas kode,
    dapat didemokan (ya/tidak). Sumber: README "Pemetaan ke proposal" dan audit A16–A18.
  - Satu contoh keluaran utuh di teks atau Gambar 5 (opsional): grafik, T1/T2, δ, klaim, kalimat level 1–3,
    status. Sumber: halaman Demo Gerbang, grafik `syn043`.
  - Waktu proses per dokumen dari `state.json` `timing` dan G6 `detik` (6–43 dtk per dokumen).
- **Pertanyaan pemandu:** fitur mana yang melayani RM1, RM2, RM3 secara langsung? Apa yang diperlihatkan setiap
  panel Gambar 4 kepada mahasiswa tunanetra dan kepada staf ULD?
- **Selesai bila:** setiap baris "jalan" di Tabel 9 bisa ditunjukkan saat demo; setiap "belum" muncul lagi di IV.D.

#### IV.B Pengujian (±600 kata, Tabel 10, Tabel 11)
- **Tujuan:** melaporkan metrik Bab III dengan kriteria terkunci, apa adanya.
- **Tabel 10: Hasil gerbang terhadap kriteria terkunci** — kolom: gerbang, kriteria (salin dari Tabel 7),
  hasil k/n, selang Wilson 95% (pers. 8), status (lulus / tidak lulus / tidak dijalankan), data.
  Baris: G1, G1-ketat (tambahan), G2, G3 (Fk terbit), G3 (injeksi tertahan), G4 (Q), G5, G6 ringan, G7.
- **Tabel 11: SIMAK (D) vs pembanding** — kolom: B0, B1, B2, D. Baris: lulus G1; aturan veraPDF gagal;
  grafik terbit; angka keliru terbit; Fk; R.
- Teks juga memuat: rincian injeksi per jenis (4 jenis), audit manual B2 (13 pembulatan, 3 rerata hitungan model,
  1 salah tandai pemeriksa), dan selisih run 1 vs run 2 (keluaran `eval/banding_run.py`).
- **Pertanyaan pemandu:** kriteria mana yang lulus, mana yang tidak dijalankan, dan apakah ada yang tidak lulus?
  Seberapa lebar selangnya, dan apa artinya untuk n = 4 dokumen? Apakah run 2 mengubah status grafik mana pun?
- **Selesai bila:** setiap angka di Tabel 10–11 cocok dengan §5; setiap proporsi punya selang; gerbang yang tidak
  dijalankan tetap muncul di tabel.

#### IV.C Pembahasan (±500 kata)
Satu paragraf per rumusan masalah, ditambah satu paragraf perbandingan dengan pustaka.

| Paragraf | Bukti yang harus dirujuk | Pertanyaan pemandu |
|---|---|---|
| RM1 (struktur, urutan baca) | G1 dan G1-ketat; veraPDF B0 → B1 → D di set uji dan G6; Lang, Title, TH | Apakah RM1 terjawab penuh atau sebagian? Apa bedanya lolos G1 dengan lolos G1-ketat bagi pembaca layar? G2 (urutan baca τ) tidak dijalankan: apa konsekuensinya bagi klaim RM1? |
| RM2 (deskripsi setia; rumus) | Fk terbit vs Tacuan; B2: 17 angka keliru pada 7/60 grafik; 3 kesalahan rerata hitungan model; G4 Q(D), Q(B2); rumus selalu ditahan | Apa yang ditunjukkan audit B2 tentang statistik yang dihitung kode? Bagian RM2 mana (rumus) yang belum terjawab? |
| RM3 (menahan dan menyerahkan ke ULD) | R pada set uji (20/60) dan G6 (18/18); cL menahan semua grafik tanpa label nilai; injeksi 137/138; alur setujui/ubah/tolak/dekoratif | Apa harga fail-closed bagi ULD? Apakah 137/138 membuktikan VLM tidak salah, atau hanya logika gerbang (A11)? |
| Perbandingan dengan pustaka | CharXiv (akurasi VLM pada grafik), Kumar dkk. (LLM lemah pada mutu teks alternatif), B1 OpenDataLoader (teks pengisi "image N" lolos veraPDF) | Bagaimana hasil tim memperkuat atau membatasi temuan pustaka Bab II? |

- **Selesai bila:** ketiga RM dijawab dengan status "terjawab / terjawab sebagian / belum terjawab" beserta bukti;
  tidak ada angka baru yang tidak ada di IV.B.

#### IV.D Keterbatasan (±300 kata, daftar bernomor boleh)
Wajib memuat, dengan bukti masing-masing:
1. Set uji G1/G3/G4 sintetis buatan tim (60 grafik, 4 dokumen); target rancangan (150 grafik, 30 dokumen,
   200 rumus, benchmark publik) tidak tercapai (A14, B5).
2. G6 ringan: 6 PDF yang lolos aturan URL ternyata RPS, *module handbook*, SOP, dan pengumuman; tidak ada grafik
   raster; 0 grafik terbit pada dokumen nyata; presisi aturan URL belum diperiksa (A6). Bila P1-9 jalan, laporkan.
3. Figur vektor (13 dari 18 gambar G6) belum dideskripsikan (A7).
4. T1, T2, dan penjawab G4 memakai model yang sama; kesalahan sistematik bisa sama di kedua ekstraksi (A12, A13).
5. cF terhadap T1 bernilai 1 menurut konstruksi; perlindungan nyata berasal dari cδ, cL, cA (A10); uji injeksi
   menguji logika gerbang (A11).
6. G1 menghitung penanda tahan sebagai teks alternatif bermakna; karena itu G1-ketat dilaporkan (A5).
7. Rumus tanpa pengenal kedua dan MathCAT; dekoratif belum sebagai Artifact; tabel cadangan belum Table/TH di PDF
   (A16, A17).
8. G2, G5, G7 tidak dijalankan; G6 penuh (60 dokumen, kappa, NVDA) belum.
9. Perubahan skema setelah run 1 (A1) dan cara run 2 menanganinya.
- **Selesai bila:** setiap butir "belum" di Tabel 9 dan setiap "tidak dijalankan" di Tabel 10 muncul di sini.

### V. Penutup (W2) — baru, ±450 kata
| Subbab | Isi wajib | Pertanyaan pemandu |
|---|---|---|
| A. Kesimpulan | Satu jawaban singkat per RM, konsisten dengan IV.C; tanpa angka baru | Jika juri hanya membaca bagian ini, apa yang harus mereka percayai dan apa yang belum? |
| B. Rencana Pengembangan | Daftar langkah lanjutan dari IV.D: ekstraksi data dari jalur vektor PDF; T2 model berbeda (`SIMAK_MODEL_T2`); pengenal rumus kedua + MathCAT; Artifact dan Table/TH; G6 penuh dan audit 600 PDF; G7 bersama ULD. Urutannya diputuskan tim | Langkah mana yang paling menurunkan beban ULD menurut data G6? |
| C. Dampak | Bagi mahasiswa tunanetra, staf ULD, dosen; dampak belajar belum diuji (G7) | Dampak mana yang sudah terukur (R, penanda status) dan mana yang masih hipotesis (pendengar)? |
- **Selesai bila:** tidak ada janji di V.B yang bertentangan dengan IV.D; V.C tidak mengklaim hasil belajar.

### Referensi
- Hapus rujukan yang tidak lagi dikutip setelah pemadatan; nomori ulang berurutan kemunculan.
- Tambahkan [55] dan [56] yang hilang.
- Kandidat rujukan baru (setiap entri **wajib diverifikasi tim** dari sumber aslinya sebelum dipakai):
  kartu model Gemma 4 dari Google (model yang dipakai), spesifikasi Web Speech API (W3C), dokumentasi veraPDF 1.30.3.
- Pemeriksaan: setiap [n] di teks ada di daftar dan sebaliknya.

### Lampiran
| Lampiran | Status | Tindakan |
|---|---|---|
| A. Pernyataan AI | Wajib diperbarui | §8.4 |
| B. Hasil Turnitin | Wajib, sebelumnya kosong | Halaman ringkasan laporan Turnitin final (< 15%) |
| C. Protokol audit awal | Tetap | — |
| D. Protokol uji kelayakan | Tetap; terima Tabel 8 bila dipindah; versi veraPDF yang dipakai MVP kini 1.30.3 | Perbarui versi |
| E. Rincian arsitektur | Perbarui: model, mode dengar Web Speech, titik akhir nyata (`app.py`) | A4 |
| F. Analisis strategis | Tetap; terima Gambar 3 bila dipindah | — |
| G. Rencana data | Tetap sebagai rancangan; satu baris catatan realisasi | B5 |
| **H. Reproduksi (baru)** | Commit/tag `v1.0-final`, perintah evaluasi, manifes (model, hash perintah, hash skema), ringkasan run 1 vs run 2, cara demo luring | README "Demo luring", `eval/banding_run.py` |

---

## 5. Angka kanon (satu-satunya sumber angka paper)

Run 2 selesai 23 Okt 01.39 WIB (commit `016d19d`, `eval/results.json`; run 1 di
`eval/results_run1_2026-10-12.json`). Paper memakai angka run 2; run 1 dilaporkan sebagai pembanding.
Jangan mengetik angka di paper tanpa baris di tabel ini.

Fakta run 2 untuk IV.B dan IV.D (bukan interpretasi):
- `python -m eval.banding_run …`: semua metrik G1/G3/G4 sama; 0 dari 60 status grafik berubah.
- Ambang, model, dan hash perintah sama dengan run 1; manifes kini mencatat hash skema `2881acdadcfe`.
- Run 2 tidak seluruhnya panggilan baru: 26 grafik uji sudah memiliki respons di cache dengan skema saat ini,
  34 grafik dipanggil ulang ke VLM. Suhu 0 dipakai pada kedua run.

| Kunci (`results.json`) | Makna | Run 1 (12 Okt) | Run 2 (23 Okt) | Dipakai di |
|---|---|---|---|---|
| `G1.D` | Dokumen uji D lulus G1 | 4/4 [0,51; 1,00] | 4/4 [0,51; 1,00] | IV.B, Tabel 10–11 |
| `G1.B0`, `G1.B1` | Pembanding | 0/4, 0/4 | 0/4, 0/4 | Tabel 11 |
| `G1.D_ketat` | G1-ketat | belum dihitung | **0/4** [0,00; 0,49] | Tabel 10, IV.D |
| `G1.veraPDF_lulus_D` | veraPDF penuh lulus | 4/4 | 4/4 | Tabel 11 |
| `G1_per_dokumen` | Aturan veraPDF gagal B0 → B1 → D | 6 → 5 → 0 | 6 → 5 → 0 (keempat dokumen) | Tabel 11 |
| `G3.D_fk_terbit` | Fk klaim terbit vs Tacuan | 440/440 [0,991; 1,00] | 440/440 [0,991; 1,00] | Abstrak, IV.B, IV.C |
| `G3.D_terbit` | Grafik terbit otomatis | 40/60 | 40/60 | Tabel 11 |
| `G3.D_R_beban_tinjauan` | R set uji | 20/60 | 20/60 | IV.C RM3 |
| `G3.injeksi_tertahan` | Injeksi tertahan | 137/138 [0,960; 0,999] | 137/138 [0,960; 0,999] | IV.B, IV.C |
| `G3.injeksi_per_jenis` | ubah angka, tukar label, turunan, tren | 40/40, 39/40, 40/40, 18/18 | sama | IV.B |
| `G3.B2_terbit` | B2 terbit | 60/60 | 60/60 | Tabel 11 |
| `G3.B2_angka_keliru_terbit` | Angka keliru B2 | 17 pada 7/60 grafik | 17 pada 7/60 grafik | Abstrak, IV.C |
| `G3.B2_fk_perkiraan` | Fk B2 (pemeriksa pola) | 566/583 | 566/583 | Tabel 11 |
| `G4.Q_D`, `G4.Q_B2` | Rasio Q | 1,00 (80/80); 0,99 (79/80) | sama | IV.B |
| `G6_ringan.G1_D` | G1 dokumen nyata | 6/6 | (tidak diulang) | IV.B, IV.D |
| `G6_ringan.veraPDF_lulus_D` | veraPDF penuh nyata | 2/6 | (tidak diulang) | IV.B |
| `G6_ringan.R_beban_tinjauan` | R nyata | 18/18 | (tidak diulang) | IV.C, IV.D |
| `ambang` | θe, ε, ρ | 0,01; 0,02; 0,10 (dikunci 12 Okt, 30 grafik dev) | sama | III.G, Lampiran H |
| `eval/audit_b2.md` | Audit pemeriksa B2 | 13 pembulatan, 3 rerata keliru, 1 salah tandai | — | IV.B |
| `Semifinal/Audit/` | Audit awal | 0/28 PDF/UA-1; 29/1.111 Figure beralt | — | Abstrak, Bab I |

Format angka Indonesia: koma desimal, titik ribuan, selang ditulis [0,991; 1,00].

---

## 6. Peta bukti per rumusan masalah

| RM | Klaim yang diuji | Bukti mendukung | Bukti membatasi | Status yang dilaporkan |
|---|---|---|---|---|
| RM1 | Dokumen berstruktur, urutan baca benar | G1 D vs B0/B1; veraPDF B0→B1→D; Lang/Title/TH | n = 4 sintetis; G1 menghitung penanda tahan; G2 tidak dijalankan; veraPDF penuh hanya 2/6 dokumen nyata | diputuskan tim |
| RM2 | Deskripsi grafik setia; rumus terucapkan | Fk terbit; B2 17 angka keliru; audit rerata; Q | sintetis; T1=T2 model sama; rumus selalu ditahan; Q nyaris otomatis (A13) | diputuskan tim |
| RM3 | Keluaran tak terverifikasi ditahan dan diserahkan ke ULD | R 20/60 dan 18/18; cL; injeksi 137/138; UI tinjauan; demo | Injeksi menguji logika gerbang; 0 grafik nyata terbit | diputuskan tim |

---

## 7. Tabel dan gambar baru

| Nomor | Isi | Pembuat | Sumber | Ukuran |
|---|---|---|---|---|
| Gambar 4 | Montase 2×2 antarmuka MVP | P | Server lokal setelah P0; ≥ 150 dpi; teks UI terbaca saat dicetak | Lebar halaman |
| Gambar 5 (opsional) | Satu contoh keluaran grafik → status | P | Demo Gerbang `syn043` | Satu kolom |
| Tabel 9 | Realisasi fitur | E | README, audit | Satu kolom |
| Tabel 10 | Gerbang vs kriteria terkunci | E | §5 | Lebar halaman |
| Tabel 11 | D vs B0/B1/B2 | E | §5 | Satu kolom |
| Grafik selang (opsional) | Proporsi per gerbang dengan selang Wilson | E | §5 | Hanya skenario B |

Aturan: keterangan gambar di bawah dan rata tengah, keterangan tabel di atas, 9 pt; rujuk "Gambar n" dan
"Tabel n" di teks sebelum objeknya muncul; isi tabel 9 pt.

---

## 8. Alur kerja end-to-end dan jadwal (23 Okt, WIB)

### 8.1 Tahapan
| Tahap | Jam | Pemilik | Masukan | Keluaran | Gerbang lolos |
|---|---|---|---|---|---|
| T0 Persiapan | 07.00–08.00 | W2 | `Fix/…Semifinal.docx` | `Final/Paper/…_Final.docx`, folder kerja | K1–K4 diputuskan |
| T1 Revisi Bab I–III | 08.00–12.00 | W2 | §4 Bab I–III, audit §3.2 | Bab I–III terevisi | §9.1 butir 1–6 |
| T2 Angka kanon | setelah run 2 selesai | E | `results.json` run 2, `banding_run.py` | §5 terisi | Ambang run 2 = run 1 |
| T3 Tabel 9–11, Gambar 4 | 09.00–12.00 | E, P | §5, server lokal | Tabel dan gambar | §7 |
| T4 Bab IV | 10.00–15.00 | W1 | T2, T3, §4 Bab IV | IV.A–D | §9.1 butir 7–12 |
| T5 Bab V + Abstrak | 14.00–16.00 | W2 | Bab IV final | V.A–C, abstrak | §9.1 butir 13–15 |
| T6 Lampiran + referensi | 15.00–16.30 | W2, E | §4 Lampiran | A–H, daftar pustaka | §9.1 butir 16–19 |
| T7 Integrasi + format | 16.30–18.00 | Penyunting tunggal | Semua bab | Naskah utuh sesuai template | §9.2 |
| T8 Turnitin | 18.00–19.00 | E | Naskah utuh | Laporan < 15% | Tulis ulang bagian yang ditandai bila ≥ 15% |
| T9 Baca silang | 19.00–20.30 | Semua (bab yang tidak ditulis sendiri) | PDF | Koreksi akhir | §9.3 |
| T10 Ekspor + unggah | 20.30–21.00 | Ketua | PDF final, link repo | Unggahan terkonfirmasi | §9.4 |

### 8.2 Titik keputusan
- **10.00** belum ada jawaban panitia soal halaman: kunci skenario A.
- **12.00** run 2 belum selesai: tulis Bab IV dengan angka run 1, biarkan sel run 2 kosong, perbarui saat tersedia;
  bila sampai 17.00 belum ada, laporkan run 1 saja dan sebut di IV.D.
- **15.00** Bab IV belum lengkap: pangkas IV.C menjadi satu paragraf per RM tanpa paragraf perbandingan pustaka.
- **19.00** Turnitin ≥ 15%: tulis ulang bagian yang ditandai dengan kata-kata sendiri; jangan memakai alat parafrase AI
  (melanggar 7.2.4).

### 8.3 Cara menulis yang aman terhadap 7.2.4
- Tulis langsung di Word dari tabel §5 dan pertanyaan pemandu §4. AI hanya boleh untuk cek tata bahasa,
  penyuntingan bahasa, dan penelusuran awal pustaka.
- Simpan riwayat versi (Word "Version History" atau salinan bertanggal) sebagai bukti penulisan tim bila panitia
  meminta klarifikasi (7.2.9).
- Setiap penulis harus bisa menjelaskan isi babnya saat tanya jawab (7.2.7 kategori 3).

### 8.4 Lampiran A final
- Ditulis ulang oleh tim; memuat nama alat, tujuan spesifik setiap penggunaan, pernyataan bahwa isi ditinjau dan
  disunting penulis, dan tanggung jawab penuh penulis (7.2.4 butir 3).
- Isinya harus sesuai penggunaan yang sebenarnya, termasuk penggunaan pada prototipe, audit, dan perencanaan ini.
  Jangan menghapus penggunaan yang memang terjadi.
- Bila panitia sudah menjawab pertanyaan tentang Lampiran A semifinal, ikuti arahannya dan simpan bukti tertulisnya.

---

## 9. Daftar periksa

### 9.1 Isi
1. [ ] Judul, topik, dan RM1–RM3 identik dengan semifinal.
2. [ ] Pers. (7) memuat cL; definisi cL ada.
3. [ ] Bab III menyebut model nyata, T1/T2 satu model, mode dengar Web Speech.
4. [ ] Tabel 6 kolom status sesuai kode; CHT-02, FRM-01/02 jujur.
5. [ ] Kriteria Tabel 7 tidak berubah; G1-ketat disebut sebagai tambahan.
6. [ ] Rencana kerja bertanggal sudah dihapus atau diganti realisasi.
7. [ ] Gambar 4 memperlihatkan keempat halaman MVP.
8. [ ] Setiap baris "jalan" di Tabel 9 dapat didemokan.
9. [ ] Tabel 10 memuat semua gerbang G1–G7 termasuk yang tidak dijalankan.
10. [ ] Semua proporsi memakai k/n dan selang Wilson.
11. [ ] Run 1 vs run 2 dilaporkan.
12. [ ] IV.D memuat 9 butir keterbatasan wajib.
13. [ ] V.A menjawab ketiga RM dan konsisten dengan IV.C.
14. [ ] V.C tidak mengklaim dampak belajar.
15. [ ] Abstrak ≤ 250 kata, tanpa angka yang tidak ada di badan.
16. [ ] Lampiran A final sesuai penggunaan nyata.
17. [ ] Lampiran B berisi laporan Turnitin < 15%.
18. [ ] Lampiran H berisi commit, perintah, manifes.
19. [ ] Tidak ada rujukan yatim; [55] dan [56] ada.

### 9.2 Format (template panitia)
- [ ] Times New Roman 10 pt, satu spasi, rata kiri-kanan, tanpa baris kosong antarparagraf, indentasi paragraf.
- [ ] Judul bab angka Romawi rata tengah; subbab huruf miring rata kiri; sub-subbab bernomor.
- [ ] Keterangan gambar di bawah (rata tengah), tabel di atas, 9 pt; isi tabel 9 pt.
- [ ] Persamaan bernomor di kanan, dirujuk "(n)".
- [ ] Referensi 8 pt, bernomor dalam kurung siku.
- [ ] Istilah asing dicetak miring; Bahasa Indonesia baku (EYD).
- [ ] Jumlah halaman sesuai keputusan K1.

### 9.3 Konsistensi paper ↔ MVP ↔ repo
- [ ] Setiap angka cocok dengan §5 dan `results.json` di commit yang dikumpulkan.
- [ ] Setiap fitur di Bab III–IV dapat ditunjukkan di demo atau diberi status "belum".
- [ ] Nama halaman, tombol, dan status di teks sama dengan antarmuka (mis. "Demo Gerbang", "Menunggu tinjauan ULD").
- [ ] Commit yang disebut di Lampiran H sama dengan link yang diunggah.

### 9.4 Pengumpulan
- [ ] PDF bernama `IRIS kata HQ ini lomba terakhir_ICC2026_Final.pdf`.
- [ ] Link GitHub publik dan dapat dibuka tanpa login; README memuat cara menjalankan.
- [ ] Unggah sebelum 21.00; tangkapan layar bukti unggah disimpan.

---

## 10. Peta bobot penilaian final ke bagian paper

Panitia hanya memberi bobot komponen, bukan rubrik rinci; tabel ini memetakan bobot itu saja.

| Komponen (bobot) | Bagian paper yang paling menentukan | Risiko utama |
|---|---|---|
| Kelengkapan dan Konsistensi (20%) | Bab I–V lengkap; Bab III cocok dengan MVP; §9.1 | Bab III menjanjikan fitur yang tidak ada |
| Hasil dan Demo (30%) | IV.A, Tabel 9, Gambar 4 | Klaim di paper tak terlihat di demo |
| Presentasi (20%) | Tabel 10–11 dan Gambar 4 dipakai ulang di salindia | Angka di salindia beda dengan paper |
| Tanya Jawab (20%) | IV.D dan Lampiran H | Penulis tidak bisa menjelaskan babnya |
| Inovasi dan Dampak (10%) | Bab I.D, V.C | Klaim dampak berlebihan |
