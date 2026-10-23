# Bahan pendukung paper final (data, bukan naskah)

Disiapkan 23 Okt 2026 dini hari untuk peran E/P di `RENCANA_PENULISAN_PAPER_FINAL.md`. Berkas ini hanya data
dan daftar periksa. Kalimat paper tetap ditulis tim (Guidebook 7.2.4 butir 2). Jangan salin teks berkas ini ke paper.

## 1. Isi folder `Final/Paper/`

| Berkas | Isi | Cara membuat ulang |
|---|---|---|
| `IRIS kata HQ ini lomba terakhir_ICC2026_Final.docx` | Salinan utuh docx semifinal (K2), belum disunting | — |
| `ANGKA_KANON.md` | Tabel §5 terisi run 1 dan run 2, rincian per dokumen, G6 | `python buat_angka_tabel.py` |
| `Tabel_9_10_11.docx` | Tabel 9–11, TNR 9 pt, border sama dengan tabel semifinal | `python buat_angka_tabel.py` |
| `gambar/Gambar4_montase.png` | Montase 2×2, 5832×4200 px (±340 dpi pada lebar 17 cm) | `python gambar/tangkap_mvp.py` |
| `gambar/g4_*.png` | Empat panel terpisah (2880×2000 px) | idem |
| `turnitin/` | Kosong; tempat laporan Turnitin final | — |

Panel Gambar 4 (diambil luring, tanpa `GEMINI_API_KEY`, dokumen `materi_03.pdf`):
(a) Remediasi & Tinjauan: katalog gambar, veraPDF 6 → 5 → 0, antrean ULD dengan alasan cL;
(b) Demo Gerbang `syn043` setelah suntik "Tukar label-nilai": B2 "Terbit · 3 angka keliru", SIMAK "Ditahan";
(c) Evaluasi G3; (d) HTML keluaran dengan bilah Putar/Jeda/Suara "Peramban (id-ID)" dan catatan status.
Catatan: panel (a) menampilkan waktu proses 7,56 dtk karena hasil VLM dari cache; waktu run evaluasi ada di `ANGKA_KANON.md`.

### 1a. Naskah final terakit (pembaruan 02.35 WIB, K1: 20 halaman utama, lampiran tanpa batas)

`IRIS kata HQ ini lomba terakhir_ICC2026_Final.docx` kini dirakit oleh `susun_final.py` dari docx semifinal:

| Bagian | Isi yang dirakit | Status |
|---|---|---|
| Bab IV | Judul bab dan subbab A–D, Gambar 4, Tabel 9–11 (bagian selebar halaman) | Kalimat: **ISIAN TIM** (kuning) |
| Bab V | Judul bab dan subbab A–C | Kalimat: **ISIAN TIM** |
| Tabel 6 | Kolom Status diganti status MVP (disorot) | Kolom Model/metode: revisi tim |
| Referensi | [55] SafeDocs, [56] WebAssembly (disorot) | Wajib diverifikasi tim |
| Bab I–III, Lampiran A, D, E | 17 komentar Word di titik yang wajib direvisi (rencana §4) | Revisi kalimat oleh tim |
| Lampiran B | Penanda ganti gambar Turnitin semifinal dengan laporan final | Tim |
| Lampiran H–P (baru, potret) | Reproduksi; seluruh selang Wilson; hasil per grafik (60); injeksi per kasus (138); audit B2 (17); kalibrasi; G6 per dokumen; rencana vs realisasi data; galeri antarmuka + titik akhir | Data saja, keterangan netral |

Hasil render (`PRATINJAU_kerangka_final.pdf`, 45 hlm): badan utama hlm. 1–13 (Lampiran A mulai hlm. 13), jadi ruang
±7 halaman tersisa untuk teks Bab IV–V tim sebelum batas 20. Skenario B: Bab I–III tidak perlu dipadatkan.
Validasi XSD docx: lulus. Rujukan: 56 entri, tidak ada yang yatim.

Urutan membuat ulang (dari `Final/Paper`): `buat_angka_tabel.py` → `lampiran/hitung_lampiran.py` →
`lampiran/buat_grafik.py` → `gambar/tangkap_mvp.py` → `susun_final.py`. Perakit menolak menimpa docx final bila
berkas itu sudah disunting tangan (sidik `.rakitan.sha256`). **Setelah tim mulai menyunting di Word, jangan jalankan
`susun_final.py` lagi.**

Sebelum ekspor PDF final: terima/hapus semua komentar, hapus sorotan kuning dan penanda ISIAN, ekspor tanpa markup,
beri nama `IRIS kata HQ ini lomba terakhir_ICC2026_Final.pdf`. `PRATINJAU_kerangka_final.pdf` hanya pratinjau (dirender
WPS, memuat markup komentar), jangan diunggah.

## 2. Temuan pemeriksaan

- **Run 2 sudah selesai dan identik dengan run 1**: 0/60 status grafik berbeda, ambang sama, semua proporsi sama.
  Satu-satunya perbedaan manifes: hash skema kini tercatat (`2881acdadcfe`). G1-ketat baru ada di run 2: D 0/4.
- **Selang Wilson**: 24 proporsi di `results.json` dihitung ulang dengan pers. (8); semuanya cocok.
- **Rujukan**: docx memuat 54 entri; teks mengutip [55] dan [56] (Tabel 5 dan Tabel 6/Lampiran G). Tidak ada entri
  yang tidak dikutip.
- **Repo**: commit `016d19d` (run 2 + 93 berkas cache) ada di lokal. **Tiga commit belum di-push** ke
  `origin/main` (`5d01a55`, `d73b409`, `016d19d`); tag `v1.0-final` belum ada. Juri yang membuka GitHub sekarang
  melihat `ad7f6b6` (tanpa Web Speech, tanpa G1-ketat, tanpa run 2).
- **README masih bertentangan dengan kode/hasil** (§9.3):
  - baris 82: "T1 dan T2 memakai model berbeda" (manifes: model sama);
  - baris 92: judul "Hasil (versi beku, 12 Okt 2026…)" (kini ada run 2);
  - baris 117: "Evaluasi baru satu kali run…" (run 2 sudah ada).
- **Lingkungan laptop ini**: Python 3.13 sistem belum punya `google-genai`, `python-multipart`, dll. sehingga server
  gagal menyala. Sudah dipasang dari `requirements.txt` (`pip install --user`). Periksa juga laptop presentasi.

## 3. Hitungan kata docx semifinal vs anggaran §3

| Bagian | Semifinal | Skenario A | Selisih |
|---|---|---|---|
| Abstrak + judul | 298 | ≤ 250 (abstrak) | — |
| I. Pendahuluan | 1.808 | ±1.150 | −658 |
| II. Tinjauan Pustaka | 1.625 | ±1.100 | −525 |
| III. Metodologi | 2.563 | ±1.700 | −863 |
| Referensi | 1.358 | ±1.400 | +42 |

Rincian subbab terpanjang: I.A Latar Belakang 978; II.C Landasan dan Persamaan 771; III.G Rancangan Evaluasi 424;
III.D Dataset 342; III.E Kerangka Fitur 340; III.H Uji Kelayakan 337. (Persamaan OMML tidak terhitung.)

## 4. Data Lampiran H (reproduksi)

| Butir | Nilai |
|---|---|
| Repositori | `github.com/Faiz7557/IRIS-Pusaka` |
| Commit final | tag `v1.0-final` → `f73bfb1` (sudah di-push); run 2 + cache masuk di `016d19d` |
| Model | `gemma-4-26b-a4b-it` untuk T1, T2, B2, penjawab G4; suhu 0 |
| Hash perintah | T1 `a2db0023d821`; T2 `bbe13c6a83dc`; B2 `ad760959b04a` |
| Hash skema | `2881acdadcfe` (run 2; run 1 tidak mencatat) |
| Data | 60 grafik uji, 4 dokumen uji; `hash_charts_json` `94ae1b4caa6f`; seed `20260930` |
| Ambang | θe 0,01; ε 0,02; ρ 0,10; dikunci 2026-10-12 12:38:31 pada 30 grafik dev |
| Run 1 | `eval/results_run1_2026-10-12.json`, 2026-10-12 13:20:22 |
| Run 2 | `eval/results.json`, 2026-10-23 01:39:38 |
| Selisih | `python -m eval.banding_run eval/results_run1_2026-10-12.json eval/results.json` → 0/60 status berbeda |
| Perintah evaluasi | `python -m eval.evaluate kalibrasi` (dev); `python -m eval.evaluate uji` (uji tertahan) |
| Validator | veraPDF 1.30.3 (`tools/verapdf/bin/cli-1.30.3.jar`), Java 21 |
| Demo luring | README bagian "Demo luring"; cache lengkap di `cache/` |

Lampiran D semifinal menyebut veraPDF 1.30.2; MVP kini 1.30.3 (rencana §4 Lampiran D).

## 5. Kandidat rujukan (WAJIB diverifikasi tim dari sumber asli sebelum dipakai, 7.2.4 butir 2)

| No. | Sumber | Tautan untuk diverifikasi | Catatan |
|---|---|---|---|
| [55] | T. Allison, M. Milano, R. Stonebraker, P. Wyatt; korpus SafeDocs `CC-MAIN-2021-31-PDF-UNTRUNCATED`, Digital Corpora (NASA JPL, program DARPA SafeDocs) | digitalcorpora.org/corpora/file-corpora/ ; pdfa.org/new-large-scale-pdf-corpus-now-publicly-available/ | ±8 juta PDF dari panen Common Crawl 2021; tanggal panen berbeda antarsumber (Jul/Agu vs Agu/Sep) |
| [56] | W3C WebAssembly Working Group, "WebAssembly Core Specification" | w3.org/TR/wasm-core/ | Versi 1.0 berstatus Recommendation; versi 2.0 masih Candidate Recommendation Draft. Pilih yang dimaksud teks |
| baru | Google, kartu model / dokumentasi Gemma 4 (26B A4B) | ai.google.dev/gemma/docs/core ; kartu model di Hugging Face | Sumber resmi kartu model belum ditemukan langsung; jangan kutip angka benchmark dari situs pihak ketiga |
| baru | W3C Speech API Community Group, "Web Speech API" (laporan CG 2012, draf editor 2014) | w3.org/community/speech-api ; wicg.github.io/speech-api | Bukan standar W3C; sebut sebagai laporan Community Group |
| ada | veraPDF sudah dikutip sebagai [28] | docs.verapdf.org | Tidak perlu entri baru; cukup versi di Lampiran D/H |

## 6. Status daftar periksa §9 yang bisa dicek mesin

| Butir | Status |
|---|---|
| 9.1-9 Tabel 10 memuat G1–G7 termasuk yang tidak dijalankan | ada di `Tabel_9_10_11.docx` |
| 9.1-10 Semua proporsi k/n + Wilson | ada di `ANGKA_KANON.md` dan Tabel 10 |
| 9.1-11 Run 1 vs run 2 | data ada (identik); narasi oleh tim |
| 9.1-18 Lampiran H: commit, perintah, manifes | data di §4 berkas ini; menunggu tag `v1.0-final` |
| 9.1-19 Rujukan yatim; [55] [56] | [55] [56] belum ada di daftar; kandidat di §5 |
| 9.3 Angka cocok dengan `results.json` commit yang dikumpulkan | cocok dengan `016d19d`; perlu push |
| 9.3 README cocok dengan kode | belum: 3 baris di §2 |
| Lainnya (narasi Bab I–V, Abstrak, Lampiran A, format, Turnitin) | dikerjakan tim |
