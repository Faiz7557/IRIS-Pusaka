# Brief Sisa Penulisan Naskah Final SIMAK

> **Pembaruan ±14.30 WIB.** Aturan "teks ditulis tim" dianulir; batas badan utama 20 halaman. Butir 1–9 dan 11
> (kecuali ekspor akhir) sudah dikerjakan oleh `isi_naskah.py` (sumber `…_Final_rakitan.docx`): Bab IV A–D, Bab V A–C,
> abstrak (192 kata), revisi 17 komentar Bab I–III dan Lampiran A, D, E, rujukan [55] (dikoreksi ke halaman Digital
> Corpora) dan [56] (cocok W3C REC 5 Des 2019), komentar dan sorotan dihapus. `cek_naskah.py`: angka bersih; badan
> utama **17 halaman** (`PRATINJAU_naskah_final.pdf`, render WPS). Sisa untuk tim: baca dan setujui teks (Lampiran A
> menyatakan isi ditinjau penulis), Turnitin → Lampiran B (satu-satunya penanda ISIAN tersisa), ekspor PDF final dari
> Word, unggah. Skrip menolak menimpa docx bila sudah disunting tangan (`.isian.sha256`).

Disusun 23 Oktober 2026, ±13.15 WIB. Target unggah **21.00 WIB** (batas 23.59).
Berkas induk: `Paper/IRIS kata HQ ini lomba terakhir_ICC2026_Final.docx` (dirakit, belum disunting tangan).
Pelengkap: `RENCANA_PENULISAN_PAPER_FINAL.md` (rencana), `ANGKA_KANON.md` (angka), `BAHAN_PENDUKUNG.md` (data teknis).

> **Aturan pakai brief ini.** Brief berisi fakta, angka, letak bukti, pertanyaan pemandu, dan jebakan. Tidak ada
> kalimat siap salin, karena Guidebook 7.2.4 butir 2 mewajibkan analisis, interpretasi, pembahasan, dan kesimpulan
> ditulis tim. Tulis di docx induk, langsung di tempat penanda **[ISIAN TIM …]** yang disorot kuning.
> **Jangan jalankan `susun_final.py` lagi setelah mulai menyunting** (menimpa suntingan; skrip juga menolak).

---

## 0. Yang sudah selesai (tidak perlu dikerjakan ulang)

| Butir | Letak di docx |
|---|---|
| Judul Bab IV "Hasil dan Pembahasan" (A–D) dan Bab V "Penutup" (A–C) | setelah Bab III, sebelum Referensi |
| Gambar 4 (montase 4 halaman MVP), Gambar 5 (alur gerbang syn043), Tabel 9 (realisasi fitur) | IV.A, selebar halaman |
| Gambar 6 (status 60 grafik D vs B2), Gambar 7 (gerbang vs kriteria), Tabel 10, Tabel 11 | IV.B, selebar halaman |
| Tabel 6 kolom Status diperbarui (disorot) | III.E |
| Rujukan [55], [56] masuk daftar (disorot, wajib verifikasi) | Referensi |
| 17 komentar Word di titik revisi Bab I–III dan Lampiran A, D, E | lihat §3 |
| Lampiran H–P (data, tabel, grafik) | setelah Lampiran G |
| Angka run 2 = run 1 (0/60 status beda), selang Wilson tervalidasi | `ANGKA_KANON.md` |

Kondisi halaman sekarang: **badan utama 14 halaman** (Lampiran A mulai hlm. 15). Batas 20, sisa **±6 halaman**.

---

## 1. Peta pekerjaan tersisa

| # | Pekerjaan | Pemilik usulan | Kata | Prioritas | Selesai paling lambat |
|---|---|---|---|---|---|
| 1 | IV.B Pengujian | W1 | 600–750 | wajib | 15.30 |
| 2 | IV.A Hasil Implementasi | W1 | 400–500 | wajib | 15.30 |
| 3 | IV.C Pembahasan (RM1, RM2, RM3, pustaka) | W1 + W2 | 800–950 | wajib | 17.00 |
| 4 | IV.D Keterbatasan | W2 | 350–450 | wajib | 16.30 |
| 5 | V.A Kesimpulan, V.B Rencana, V.C Dampak | W2 | 600–750 | wajib | 17.30 |
| 6 | Abstrak baru (≤ 250 kata) | W2 | 200–250 | wajib | 18.00 |
| 7 | Revisi Bab I–III sesuai 17 komentar | E | ±300 diubah | wajib | 16.00 |
| 8 | Lampiran A pernyataan AI (jujur, lengkap) | Ketua | 120–200 | wajib | 18.00 |
| 9 | Verifikasi rujukan [55], [56] | E | — | wajib | 15.00 |
| 10 | Turnitin < 15% → Lampiran B | E | — | wajib | 19.30 |
| 11 | Bersih-bersih, format, ekspor PDF | Penyunting tunggal | — | wajib | 20.30 |
| 12 | Unggah PDF + link GitHub | Ketua | — | wajib | 21.00 |

Total teks baru Bab IV–V ≈ **2.800–3.400 kata**. Halaman dua kolom 10 pt memuat ±850–950 kata teks, jadi
3.400 kata ≈ 4 halaman → badan akhir ±18–19 halaman. **Di atas 3.800 kata, batas 20 halaman terancam.**
Cek dengan `python cek_naskah.py --pdf <pdf>` setiap kali selesai satu subbab.

---

## 2. Brief per subbab

Format: **Tujuan** (dari Ketentuan Final hlm. 5) · **Objek yang dirujuk** · **Fakta wajib** (semua dari
`results.json` run 2 / `lampiran_data.json`; format Indonesia) · **Pertanyaan pemandu** · **Jebakan** ·
**Selesai bila**.

### IV.A Hasil Implementasi (400–500 kata)

- **Tujuan:** apa yang sudah dibuat, lengkap dengan tangkapan layar atau keluaran.
- **Objek:** Gambar 4 (sebut panel a–d satu per satu), Gambar 5, Tabel 9. Rujuk masing-masing **sebelum** objeknya.
- **Fakta wajib:**
  - Empat halaman MVP: Remediasi & Tinjauan (`/`), Demo Gerbang (`/demo.html`), Evaluasi (`/evaluasi.html`),
    keluaran HTML dengan mode dengar; ditambah halaman Dengar (`/dengar.html`). Titik akhir: Lampiran P.
  - Model: Gemma 4 26B-A4B lewat Gemini API, suhu 0; T1 dan T2 satu model dengan dua perintah (hash
    `a2db0023d821`, `bbe13c6a83dc`); respons di-cache per hash citra, perintah, skema (`2881acdadcfe`), model.
  - Mode dengar: Web Speech API id-ID bawaan (lokal, tanpa key); ElevenLabs opsional.
  - Validator: veraPDF 1.30.3, profil PDF/UA-1. Pembanding B0 PDF asli, B1 OpenDataLoader 2.5.11.
  - Realisasi fitur (Tabel 9): **jalan** CLS-01, CHT-01, GAT-01, OUT-01, OUT-02, REV-01; **sebagian** STR-01
    (cadangan tabel PyMuPDF, bukan Docling; belum Table/TH di PDF), CHT-02 (templat, tanpa VLM penyunting);
    **belum** FRM-01 (semua rumus ditahan), FRM-02 (MathCAT).
  - Contoh utuh syn043 (Gambar 5): 10 kategori; δ = 0,000 ≤ θe = 0,01; statistik kode maks Jul 1.452, min Feb 854,
    selisih 598, rerata 1.206,8, tren naik; 16 klaim; 16/16 cocok; terbit. Injeksi tukar Apr↔Okt → ditahan dengan
    alasan tercatat. B2 pada grafik sama: 14 angka, 1 tidak setia ("sekitar 1.107", acuan 1.206,8).
  - Waktu proses dokumen uji 3 halaman: 29,9–43,9 dtk; PDF nyata 6,5–43,0 dtk (1–192 halaman). Dengan cache: ±7,6 dtk.
  - Contoh dokumen materi_03 (Gambar 4a): veraPDF 6 → 5 → 0 aturan gagal; 2 terbit, 3 ditahan, 2 dekoratif.
- **Pertanyaan pemandu:** fitur mana melayani RM1, RM2, RM3 langsung? Apa yang dilihat mahasiswa tunanetra di
  panel (d) dan apa yang dikerjakan staf ULD di panel (a)? Apa yang ditunjukkan Gambar 5 yang tidak ditunjukkan B2?
- **Jebakan:** jangan menyebut MathCAT, Docling, VLM penyunting, atau Artifact sebagai fitur jalan. Jangan menyebut
  T1/T2 "independen". Jangan menyebut "real-time".
- **Selesai bila:** setiap baris "jalan" di Tabel 9 bisa ditunjukkan saat demo; setiap "belum/sebagian" muncul lagi di IV.D.

### IV.B Pengujian (600–750 kata)

- **Tujuan:** hasil uji MVP memakai metrik yang ditulis di Bab III, dengan kriteria terkunci.
- **Objek:** Tabel 10 (gerbang vs kriteria), Tabel 11 (D vs B0/B1/B2), Gambar 6, Gambar 7. Rujuk Lampiran H–N
  untuk rincian.
- **Fakta wajib (selang Wilson 95% wajib menyertai setiap proporsi):**

| Ukuran | Nilai |
|---|---|
| Set uji tertahan | 60 grafik sintetis, 4 dokumen (3 halaman), seed 20260930; ambang dikunci 12 Okt 12:38 pada 30 grafik dev |
| Dua run | run 1 (12 Okt) dan run 2 (23 Okt): 0/60 status berbeda; semua ukuran identik; hash skema baru tercatat di run 2 |
| G1 D | 4/4 [0,510; 1,000]; B0 0/4, B1 0/4 [0,000; 0,490]; veraPDF B0 6 → B1 5 → D 0 aturan gagal per dokumen → **lulus** |
| G1-ketat D (tambahan) | 0/4 [0,000; 0,490] — penanda "[Menunggu tinjauan ULD]" dihitung belum bermakna |
| G3 Fk klaim terbit | 440/440 [0,991; 1,000] → **lulus** (kriteria ≥ 0,98) |
| G3 injeksi tertahan | 137/138 [0,960; 0,999] → **lulus** (≥ 0,90); per jenis: ubah angka 40/40, tukar label 39/40, turunan salah 40/40, tren salah 18/18 |
| Injeksi yang lolos | syn073, tukar label: selisih dua nilai 5 < ε·s = 6,74 (di bawah toleransi menurut definisi) |
| G3 terbit / R | D terbit 40/60 [0,541; 0,773]; R = 20/60 [0,227; 0,459]; B2 terbit 60/60 |
| Angka keliru terbit | D 0; B2 17 angka pada 7/60 grafik [0,058; 0,222] |
| Fk B2 (perkiraan) | 566/583 = 0,971 [0,954; 0,982]; pemeriksa pola diaudit: 16/17 tanda benar |
| Audit B2 (17 tanda) | 13 pembulatan/perkiraan di luar ε (semua grafik tanpa label nilai), 3 rerata dihitung model keliru (syn043, syn083, syn068), 1 salah tandai (syn079) |
| G4 | Q(D) = 80/80 ÷ 80/80 = 1,00; Q(B2) = 79/80 ÷ 80/80 = 0,99 → **lulus** (Q ≥ 0,80); 20 grafik × 4 pertanyaan |
| G6 ringan (6 PDF nyata) | G1 D 6/6 [0,610; 1,000], B0 0/6, B1 0/6; veraPDF penuh D 2/6 [0,097; 0,700]; R 18/18 [0,824; 1,000]; 0 grafik terbit |
| G2, G5, G7 | **tidak dijalankan**; G6 penuh (60 dokumen, κ, NVDA) belum |

- **Fakta tambahan dari rincian per grafik (Lampiran J), belum ada di Bab III:**
  - Semua 40 grafik terbit berlabel nilai; semua 20 grafik ditahan tanpa label nilai.
  - Alasan penahanan: 19 hanya cL; 1 cL + cδ (syn014, δ = 0,0128 > θe).
  - 5 grafik dengan δ > 0 (syn014, syn020, syn059, syn062, syn083) semuanya ditahan.
  - Klaim D pada 20 grafik yang ditahan, bila dibandingkan dengan acuan: 205/222 setia [0,881; 0,952];
    6/20 grafik memuat klaim tidak setia (syn011 9/12, syn032 7/8, syn050 9/11, syn068 1/9, syn077 12/13, syn089 10/12).
  - Klaim per grafik terbit: 8–16.
  - Grafik B2 dengan angka keliru: 5 tanpa label nilai, 2 berlabel (syn043 rerata; syn079 salah tandai).
- **Pertanyaan pemandu:** kriteria mana lulus, mana tidak dijalankan, adakah yang tidak lulus? Apa arti selang
  [0,510; 1,000] untuk n = 4? Mengapa G1 dan G1-ketat berbeda? Apakah run 2 mengubah status grafik mana pun?
- **Jebakan:** jangan tulis persentase tanpa k/n dan selang; jangan menyebut G1 "100% dokumen nyata" tanpa n = 6 dan
  catatan G1-ketat; Fk B2 adalah perkiraan; G6 bukan materi kuliah (lihat IV.D).
- **Selesai bila:** setiap angka lolos `cek_naskah.py`; setiap gerbang di Tabel 10 disebut, termasuk yang tidak dijalankan.

### IV.C Pembahasan (800–950 kata; satu paragraf per RM + satu paragraf pustaka)

- **Tujuan:** apakah hasil sudah menjawab rumusan masalah Bab I.
- **Format status yang wajib dipilih tim untuk tiap RM:** terjawab / terjawab sebagian / belum terjawab, dengan bukti.

| RM | Bukti mendukung | Bukti membatasi | Pertanyaan pemandu |
|---|---|---|---|
| RM1 struktur dan urutan baca | G1 D 4/4 vs B1 0/4; veraPDF 6 → 5 → 0; Lang, Title, TH ditambahkan; G6 G1 D 6/6 | n = 4 sintetis; G1-ketat 0/4; veraPDF penuh nyata hanya 2/6; G2 (τ urutan baca) tidak dijalankan; tabel cadangan belum TH di PDF | Apakah "lolos G1" sama dengan "terbaca utuh oleh pembaca layar"? Apa akibat G2 tidak diukur bagi klaim urutan baca? |
| RM2 deskripsi setia, rumus terucap | Fk terbit 440/440; B2 17 angka keliru pada 7/60; 3 rerata keliru B2 vs statistik kode; G4 Q(D) 1,00; klaim D yang ditahan 205/222 (17 klaim tak setia tidak sampai ke pembaca) | set uji sintetis; T1 = T2 model sama (cF terhadap T1 bernilai 1 menurut konstruksi); Q nyaris otomatis (penanya = model sama, pertanyaan dari tabel); rumus selalu ditahan | Apa yang dibuktikan audit B2 tentang statistik yang dihitung kode vs model? Bagian RM2 mana yang belum terjawab (rumus)? |
| RM3 menahan keluaran tak terverifikasi ke ULD | R 20/60 (uji) dan 18/18 (nyata); cL menahan semua grafik tanpa label nilai; injeksi 137/138; antrean setujui/ubah/tolak/dekoratif; 6/20 grafik ditahan memang memuat klaim keliru | injeksi menguji logika gerbang, bukan kesalahan baca VLM; 0 grafik nyata terbit; figur vektor belum tampil di antrean UI | Berapa "harga" fail-closed bagi ULD? Apakah 137/138 membuktikan VLM benar, atau hanya gerbang bekerja? |
| Pustaka Bab II | CharXiv (akurasi VLM pada grafik), Kumar dkk. (LLM lemah pada mutu teks alternatif), B1 OpenDataLoader menghasilkan "image N" yang lolos veraPDF (Tabel 8) | — | Temuan mana yang menguatkan atau membatasi pustaka? |

- **Jebakan:** jangan menulis "tidak ada deskripsi keliru yang terbit" tanpa batas "pada 440 klaim sintetis";
  jangan mengklaim dampak belajar; jangan memasukkan angka yang tidak ada di IV.B.

### IV.D Keterbatasan (350–450 kata; daftar bernomor boleh)

Wajib memuat 10 butir berikut, masing-masing dengan bukti:

| # | Keterbatasan | Bukti/angka | Kode audit |
|---|---|---|---|
| 1 | Set uji G1/G3/G4 sintetis buatan tim | 60 grafik, 4 dokumen vs rancangan 150 grafik, 30 dokumen, 200 rumus; benchmark publik tidak dipakai (Lampiran O) | A14, B5 |
| 2 | G6 ringan bukan materi kuliah | 6 PDF: 2 RPS ITS, 2 module handbook (Unair, Unej), SOP cuti dan pengumuman UNY; 0 grafik raster; presisi aturan URL belum diperiksa | A6 |
| 3 | Figur vektor belum dideskripsikan | 15 figur vektor ditahan dari 18 elemen antrean G6 (bukan "13 dari 18" seperti di README/rencana; 13 berasal dari satu dokumen, cc_03) | A7 |
| 4 | T1, T2, penjawab G4 satu model | Gemma 4 26B-A4B; kesalahan sistematik bisa sama; opsi `SIMAK_MODEL_T2` | A12, A13 |
| 5 | cF terhadap T1 bernilai 1 menurut konstruksi; injeksi menguji logika gerbang | perlindungan nyata dari cδ, cL, cA; kesetiaan diukur terpisah vs Tacuan | A10, A11 |
| 6 | G1 menghitung penanda tahan sebagai teks alt bermakna | G1 4/4 vs G1-ketat 0/4 | A5 |
| 7 | Rumus, dekoratif, tabel cadangan | semua rumus ditahan; dekoratif `/Alt` belum Artifact; tabel cadangan belum Table/TH | A16, A17 |
| 8 | Gerbang tidak dijalankan | G2, G5, G7; G6 penuh (60 dokumen, κ, NVDA) | — |
| 9 | Perubahan skema setelah run 1 | hash skema tidak tercatat di run 1; run 2 pada kode HEAD mengisi ulang cache; hasil identik | A1 |
| 10 | Toleransi ε | kesalahan di bawah ε·s tidak terdeteksi menurut definisi (syn073: 5 < 6,74) | — |

- **Selesai bila:** setiap "belum/sebagian" di Tabel 9 dan setiap "tidak dijalankan" di Tabel 10 muncul di sini.

### V.A Kesimpulan (200–250 kata)

- Satu jawaban singkat per RM, status sama persis dengan IV.C, **tanpa angka baru** (boleh mengulang angka kunci IV.B).
- Pertanyaan pemandu: jika juri hanya membaca V.A, apa yang harus dipercaya dan apa yang belum?

### V.B Rencana Pengembangan (200–250 kata)

Bahan (urutan diputuskan tim; dasar: dampaknya pada R menurut G6):
1. Ekstraksi data dari jalur vektor PDF (15 figur vektor = penyumbang terbesar R nyata).
2. T2 dengan model berbeda (`SIMAK_MODEL_T2`, mis. `gemma-4-31b-it`, ±40–70 dtk per panggilan).
3. Pengenal rumus kedua + MathCAT aturan Indonesia (FRM-01/02).
4. Artifact untuk dekoratif; Table/TH untuk tabel cadangan.
5. G6 penuh: 60 dokumen materi kuliah nyata (28 tautan audit awal sebagai kandidat), κ dua penilai, NVDA.
6. G2 (τ urutan baca), G5 (rumus), G7 bersama ULD mitra.
7. Audit 600 PDF bingkai Common Crawl; benchmark publik (VisText, ChartQA, UniMER, IndoTabVQA).
- Jebakan: tidak boleh bertentangan dengan IV.D.

### V.C Dampak (200–250 kata)

| Pihak | Yang sudah terukur | Yang masih hipotesis |
|---|---|---|
| Mahasiswa tunanetra | penanda status per gambar; 0 angka keliru terbit pada set uji; mode dengar id-ID lokal | ketepatan dan waktu tugas (G7) |
| Staf ULD | beban tinjauan R terukur (20/60 uji; 18/18 nyata); antrean dengan alasan per elemen | penghematan waktu kerja |
| Dosen | unggah PDF apa adanya; tidak perlu menulis teks alt | adopsi |
| Mahasiswa pendengar | mode dengar | manfaat belajar |
- Jebakan: jangan mengklaim hasil belajar atau penghematan waktu ULD (belum diukur).

### Abstrak (≤ 250 kata; tulis terakhir)

- Wajib: satu angka besaran masalah (audit awal 0/28 PDF lulus PDF/UA-1; 29/1.111 elemen Figure beralt);
  pendekatan (ekstraksi ganda + statistik kode + gerbang fail-closed); hasil utama (Fk 440/440; B2 17 angka keliru
  pada 7/60; injeksi 137/138; R 20/60); satu batasan (set uji sintetis / G6 kecil).
- Hapus pernyataan semifinal bahwa makalah belum melaporkan kinerja (ada komentar).
- Abstrak lama memuat desimal 1,2; 2,6; 4,6 yang tidak ada di data final — pastikan hilang.
- Selesai bila: semua angka abstrak identik dengan Bab IV; `cek_naskah.py` hijau untuk abstrak.

---

## 3. Revisi Bab I–III (17 komentar Word, kolom kanan docx)

| Lokasi | Yang harus diubah tim | Sumber |
|---|---|---|
| Abstrak | tulis ulang dengan hasil (lihat §2) | rencana §4 |
| Tabel 3 (I.D) | kolom Status per 30 Sep → hasil nyata / "tidak dijalankan" | Tabel 10 |
| II.C paragraf OpenDataLoader | Docling → PyMuPDF `find_tables` sebagai cadangan | `simak/pipeline.py` |
| II.C pers. (7) | K(e) grafik = {cF, cδ, cA, cL}; definisi cL + asal dari kalibrasi v1 (Fk 0,937 pada δ = 0; grafik tanpa label Fk 0,75–0,875) | Lampiran M |
| III.B Arsitektur | sebut Gemma 4 26B-A4B, suhu 0, cache; T1 = T2 dua perintah; Web Speech id-ID, ElevenLabs opsional | Lampiran H |
| III.C Alur penelitian | dua run sudah terpenuhi (0/60 beda) | Lampiran H |
| Tabel 5 (III.D) | tetap rancangan; rujuk Lampiran O | Lampiran O |
| Tabel 6 (III.E) | kolom Status sudah diubah; tinjau kolom Model/metode CHT-02 (VLM penyunting) dan STR-01 (Docling) | Tabel 9 |
| III.F Modul grafik | hapus peran VLM penyunting; deskripsi murni templat | `chart.build_description` |
| III.F Modul rumus | belum ada pengenal kedua/MathCAT; semua rumus ditahan | `gate.py` |
| III.G Tabel 7 | kriteria tidak diubah; G1-ketat = pelaporan tambahan | — |
| III.I Rencana kerja | jadwal 1–23 Okt → satu kalimat realisasi atau hapus | — |
| Lampiran A | lihat §4 | — |
| Lampiran D | uji awal veraPDF 1.30.2; MVP 1.30.3 | Lampiran H |
| Lampiran E | model, Web Speech, titik akhir (Lampiran P); MathCAT belum | Lampiran P |
| Referensi [55], [56] | verifikasi sumber asli, hapus sorotan | `BAHAN_PENDUKUNG.md` §5 |

**Jangan ubah:** judul, topik, dan RM1–RM3 (7.2.4 butir 7). Bab I–III tidak perlu dipadatkan (batas 20 halaman).

---

## 4. Lampiran A — isi wajib (7.2.4 butir 3)

Tulis ulang oleh tim; harus **jujur dan sesuai penggunaan sebenarnya**. Karya tanpa pernyataan dianggap disusun
tanpa AI, dan pernyataan yang tidak sesuai kenyataan adalah pelanggaran. Elemen wajib:
1. Nama alat: Claude (Anthropic), lewat Claude Code; alat lain yang dipakai tim (mis. Grammarly, Gemini/Gemma
   sebagai komponen sistem, bukan penulis).
2. Tujuan spesifik setiap penggunaan. Penggunaan pada sesi persiapan final ini (fakta untuk dicantumkan):
   - skrip pengolah angka dan selang Wilson (`buat_angka_tabel.py`), Tabel 9–11 berisi data;
   - tangkapan layar otomatis Gambar 4; grafik Gambar 5–7 dan grafik lampiran;
   - perakitan struktur docx, Lampiran H–P berisi data dan keterangan netral;
   - komentar penanda titik revisi; alat pemeriksa angka (`cek_naskah.py`);
   - penelusuran awal rujukan [55], [56] (diverifikasi tim);
   - perbaikan README dan skrip pada prototipe; penyusunan rencana dan audit kerja.
   - Penggunaan pada babak sebelumnya sesuai Lampiran A semifinal.
3. Pernyataan bahwa seluruh isi telah ditinjau dan disunting penulis.
4. Pernyataan bahwa penulis bertanggung jawab penuh atas akurasi dan orisinalitas.
- Bila panitia menjawab pertanyaan tentang batas AI, ikuti jawabannya dan simpan bukti tertulisnya.

---

## 5. Lampiran B, rujukan, format, ekspor

1. **Turnitin:** unggah naskah final (setelah semua teks tim masuk). Target < 15% di luar kutipan dan pustaka.
   Ganti gambar laporan semifinal di Lampiran B dengan halaman ringkasan laporan final; simpan PDF laporan di
   `Paper/turnitin/`. Bila ≥ 15%: tulis ulang bagian yang ditandai dengan kata sendiri; jangan pakai parafrase AI.
2. **Rujukan:** buka sumber [55] dan [56]; cocokkan penulis, judul, tanggal, URL; hapus sorotan.
3. **Format (template):** TNR 10 pt, satu spasi, rata kiri-kanan; judul bab Romawi rata tengah; subbab miring rata
   kiri; keterangan tabel di atas dan gambar di bawah (9 pt); referensi 8 pt; istilah asing miring
   (*fail-closed*, *cache*, *template* bila dipakai); EYD.
4. **Bersih-bersih:** hapus semua penanda [ISIAN TIM]; hapus sorotan kuning (Beranda → Sorot → Tanpa Warna, pilih
   seluruh dokumen); Tinjau → Hapus Semua Komentar.
5. **Periksa:** `python cek_naskah.py --pdf <pdf>` harus 0 butir "CEK" (abaikan Gambar 1–3: positif palsu karena gambar
   semifinal memakai tabel melayang).
6. **Ekspor:** Word → Simpan Sebagai PDF, tanpa markup; nama `IRIS kata HQ ini lomba terakhir_ICC2026_Final.pdf`.
   Jangan unggah `PRATINJAU_kerangka_final.pdf`.
7. **Unggah:** campusdataweek.satudata.unair.ac.id → Team Login (akun ketua) → PDF + link
   `github.com/Faiz7557/IRIS-Pusaka` (tag `v1.0-final`, sudah publik). Simpan tangkapan layar bukti unggah.

---

## 6. Jadwal sisa hari ini (WIB)

| Jam | W1 | W2 | E | Ketua/penyunting |
|---|---|---|---|---|
| 13.15–15.30 | IV.A, IV.B | IV.D | revisi Bab I–III (komentar), verifikasi [55]/[56] | Lampiran A draf, latihan demo |
| 15.30–17.00 | IV.C (RM1–RM3) | V.A–V.C | cek angka `cek_naskah.py` per subbab | baca IV.A–B |
| 17.00–18.00 | IV.C pustaka, rapikan | Abstrak | format template | integrasi ke berkas induk (satu orang) |
| 18.00–19.30 | baca silang bab W2 | baca silang bab W1 | Turnitin → Lampiran B | Lampiran A final |
| 19.30–20.30 | — | — | `cek_naskah.py` 0 CEK | bersih-bersih, ekspor PDF |
| 20.30–21.00 | | | | **unggah**, bukti unggah |

Titik keputusan: **16.00** IV.A–B belum jadi → pangkas IV.C jadi satu paragraf per RM tanpa paragraf pustaka.
**19.00** Turnitin ≥ 15% → tulis ulang bagian bertanda. **20.30** apa pun kondisinya, ekspor dan unggah.

---

## 7. Persiapan tanya jawab (bahan, bukan jawaban)

| Pertanyaan yang hampir pasti muncul | Letak bukti |
|---|---|
| Di PDF nyata, apa yang terbit otomatis? | G6: 0 terbit, R 18/18; 15 figur vektor (Lampiran N) |
| Injeksi 137/138 bukankah pasti lulus? | A11; kesetiaan diukur terpisah: Fk 440/440 vs Tacuan; 205/222 klaim pada grafik ditahan (Lampiran J) |
| T1 dan T2 model sama, independen? | A12; cL lahir dari kalibrasi v1 (Lampiran M); `SIMAK_MODEL_T2` |
| G1 lulus padahal gambar ditahan? | G1 4/4 vs G1-ketat 0/4 (Tabel 10) |
| Set uji buatan sendiri? | ambang dikunci sebelum set uji dibuka; dua run identik (Lampiran H, M) |
| Kenapa hasil beku 12 Okt tapi kode berubah? | hash skema; run 2 23 Okt identik (Lampiran H) |
| Biaya/waktu per dokumen? | 29,9–43,9 dtk uji; 6,5–43,0 dtk nyata; ±7,6 dtk dengan cache |
| Kenapa B2 bisa salah padahal model sama? | audit B2: rerata dihitung model (Lampiran L); Gambar 5 |
| Kenapa 20 grafik ditahan? | semua tanpa label nilai → cL; 6/20 memang memuat klaim keliru (Lampiran J) |

Setiap anggota yang hadir harus bisa menjelaskan pers. (2), (5), (7), (8), arti R, cL, dan alur demo.
