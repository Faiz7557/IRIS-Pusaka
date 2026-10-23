# Angka kanon paper final SIMAK (diisi otomatis)

Dibuat oleh `buat_angka_tabel.py` dari `Prototype/eval/results.json` (run 2, 2026-10-23 01:39:38) dan
`Prototype/eval/results_run1_2026-10-12.json` (run 1, 2026-10-12 13:20:22). Jalankan ulang skrip bila `results.json` berubah.
Format: k/n [batas bawah; batas atas] selang Wilson 95%, koma desimal.

## Pemeriksaan otomatis

- Selang Wilson: 24 proporsi di run 2 dihitung ulang dengan pers. (8); semuanya cocok (4 desimal).
- Ambang run 1 = run 2: **ya** (θe = 0,01; ε = 0,02; ρ = 0,10; dikunci 2026-10-12 12:38:31, 30 grafik dev).
- Status grafik berbeda run 1 vs run 2: **0/60** .
- Manifes run 2: T1 `gemma-4-26b-a4b-it`, T2 `gemma-4-26b-a4b-it`, B2 `gemma-4-26b-a4b-it`, QA `gemma-4-26b-a4b-it`, suhu 0,
  hash perintah T1 `a2db0023d821`, T2 `bbe13c6a83dc`, B2 `ad760959b04a`, skema `2881acdadcfe` (run 1: skema tidak tercatat).
- G6 ringan tidak diulang di run 2 (isi identik dengan run 1).

## Tabel §5

| Kunci (`results.json`) | Makna | Run 1 (12 Okt) | Run 2 (23 Okt) | Run 1 vs 2 | Dipakai di |
|---|---|---|---|---|---|
| `G1.D` | Dokumen uji D lulus G1 | 4/4 [0,510; 1,000] | 4/4 [0,510; 1,000] | sama | IV.B, Tabel 10–11 |
| `G1.B0` | B0 lulus G1 | 0/4 [0,000; 0,490] | 0/4 [0,000; 0,490] | sama | Tabel 11 |
| `G1.B1` | B1 lulus G1 | 0/4 [0,000; 0,490] | 0/4 [0,000; 0,490] | sama | Tabel 11 |
| `G1.D_ketat` | G1-ketat (penanda tahan dihitung belum bermakna) | — | 0/4 [0,000; 0,490] | baru di run 2 | Tabel 10 |
| `G1.veraPDF_lulus_D` | veraPDF penuh lulus (D) | 4/4 [0,510; 1,000] | 4/4 [0,510; 1,000] | sama | Tabel 11 |
| `G3.D_fk_terbit` | Fk klaim terbit vs Tacuan | 440/440 [0,991; 1,000] | 440/440 [0,991; 1,000] | sama | Abstrak, IV.B, IV.C |
| `G3.D_terbit` | Grafik terbit otomatis (D) | 40/60 [0,541; 0,773] | 40/60 [0,541; 0,773] | sama | Tabel 11 |
| `G3.D_R_beban_tinjauan` | R set uji | 20/60 [0,227; 0,459] | 20/60 [0,227; 0,459] | sama | IV.C RM3 |
| `G3.injeksi_tertahan` | Injeksi tertahan | 137/138 [0,960; 0,999] | 137/138 [0,960; 0,999] | sama | IV.B, IV.C |
| `G3.injeksi_per_jenis.ubah_angka` | Injeksi: ubah angka | 40/40 [0,912; 1,000] | 40/40 [0,912; 1,000] | sama | IV.B |
| `G3.injeksi_per_jenis.tukar_label` | Injeksi: tukar label | 39/40 [0,871; 0,996] | 39/40 [0,871; 0,996] | sama | IV.B |
| `G3.injeksi_per_jenis.turunan_salah` | Injeksi: turunan salah | 40/40 [0,912; 1,000] | 40/40 [0,912; 1,000] | sama | IV.B |
| `G3.injeksi_per_jenis.tren_salah` | Injeksi: tren salah | 18/18 [0,824; 1,000] | 18/18 [0,824; 1,000] | sama | IV.B |
| `G3.B2_terbit` | B2 terbit | 60/60 [0,940; 1,000] | 60/60 [0,940; 1,000] | sama | Tabel 11 |
| `G3.B2_angka_keliru_terbit` | Angka keliru B2 terbit (jumlah angka) | 17 | 17 | sama | Abstrak, IV.C |
| `G3.B2_grafik_dengan_angka_keliru` | Grafik B2 dengan angka keliru | 7/60 [0,058; 0,222] | 7/60 [0,058; 0,222] | sama | Abstrak, IV.C |
| `G3.D_angka_keliru_terbit` | Angka keliru D terbit | 0 | 0 | sama | Tabel 11 |
| `G3.B2_fk_perkiraan` | Fk B2 (pemeriksa pola, perkiraan) | 566/583 [0,954; 0,982] | 566/583 [0,954; 0,982] | sama | Tabel 11 |
| `G4.D` | G4 jawaban benar dari deskripsi D | 80/80 [0,954; 1,000] | 80/80 [0,954; 1,000] | sama | IV.B |
| `G4.B2` | G4 jawaban benar dari deskripsi B2 | 79/80 [0,932; 0,998] | 79/80 [0,932; 0,998] | sama | IV.B |
| `G4.tabel` | G4 jawaban benar dari tabel (penyebut Q) | 80/80 [0,954; 1,000] | 80/80 [0,954; 1,000] | sama | IV.B |
| `G4.Q_D` | Rasio Q(D) | 1 | 1 | sama | IV.B |
| `G4.Q_B2` | Rasio Q(B2) | 0,9875 | 0,9875 | sama | IV.B |
| `G6_ringan.G1_D` | G1 dokumen nyata (D) | 6/6 [0,610; 1,000] | 6/6 [0,610; 1,000] | sama | IV.B, IV.D |
| `G6_ringan.G1_B0` | G1 dokumen nyata (B0) | 0/6 [0,000; 0,390] | 0/6 [0,000; 0,390] | sama | IV.B |
| `G6_ringan.G1_B1` | G1 dokumen nyata (B1) | 0/6 [0,000; 0,390] | 0/6 [0,000; 0,390] | sama | IV.B |
| `G6_ringan.veraPDF_lulus_D` | veraPDF penuh nyata (D) | 2/6 [0,097; 0,700] | 2/6 [0,097; 0,700] | sama | IV.B |
| `G6_ringan.R_beban_tinjauan` | R dokumen nyata | 18/18 [0,824; 1,000] | 18/18 [0,824; 1,000] | sama | IV.C, IV.D |
| `ambang` | θe, ε, ρ | 0,01; 0,02; 0,10 | 0,01; 0,02; 0,10 | sama | III.G, Lampiran H |
| `eval/audit_b2.md` | Audit pemeriksa B2 | 13 pembulatan, 3 rerata keliru, 1 salah tandai | — | — | IV.B |
| `Semifinal/Audit/` | Audit awal | 0/28 PDF/UA-1; 29/1.111 Figure beralt | — | — | Abstrak, Bab I |

## Rincian per dokumen uji (run 2): aturan veraPDF gagal

| Dokumen | Halaman | B0 | B1 | D | Waktu proses (dtk) |
|---|---|---|---|---|---|
| materi_03.pdf | 3 | 6 | 5 | 0 | 39,9 |
| materi_04.pdf | 3 | 6 | 5 | 0 | 34,0 |
| materi_05.pdf | 3 | 6 | 5 | 0 | 43,9 |
| materi_06.pdf | 3 | 6 | 5 | 0 | 29,9 |

## Rincian G6 ringan (6 PDF nyata)

| Dokumen | Domain | Hlm | Gambar | Dekoratif | Figur vektor ditahan | Antrean | Terbit | veraPDF B0 | B1 | D | Dtk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cc_01_its.pdf | its.ac.id | 10 | 1 | 0 | 1 | 1 | 0 | 5 | 6 | 2 | 12,0 |
| cc_02_its.pdf | its.ac.id | 6 | 1 | 0 | 1 | 1 | 0 | 5 | 5 | 1 | 11,2 |
| cc_03_unair.pdf | unair.ac.id | 192 | 14 | 1 | 13 | 13 | 0 | 10 | 10 | 6 | 37,8 |
| cc_04_uny.pdf | uny.ac.id | 2 | 2 | 0 | 0 | 2 | 0 | 6 | 5 | 0 | 17,4 |
| cc_05_unej.pdf | unej.ac.id | 158 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 5 | 43,0 |
| cc_06_uny.pdf | uny.ac.id | 1 | 1 | 0 | 0 | 1 | 0 | 3 | 3 | 0 | 6,5 |
