# Audit Final SIMAK (ICC 2026) dan Rencana Perbaikan

Disusun 23 Oktober 2026, 00.30 WIB. Batas pengumpulan: **23 Oktober 2026, 23.59 WIB** (sisa ±23 jam).
Dasar audit: `Ketentuan Final ICC 2026.pdf`, guidebook (7.2.4–7.2.7), TM Semifinal, paper semifinal
(27 halaman), seluruh kode `Prototype/` (commit `ad7f6b6`), `eval/results.json`, verdict sidang `.court/` (21 Okt),
dan **uji jalan dari clone bersih GitHub** di lingkungan Python baru (dijalankan tanpa API key, kondisi yang sama
dengan laptop presentasi bila internet/key bermasalah).

> Catatan aturan 7.2.4: dokumen ini adalah rencana kerja, bukan naskah. Analisis, interpretasi hasil,
> pembahasan, dan kesimpulan Bab 4–5 wajib ditulis tim sendiri. Bagian "isi wajib" di bawah hanya daftar
> periksa: apa yang harus ada dan dari berkas mana angkanya diambil.

---

## 1. Verdict ringkas

| Komponen (bobot) | Kondisi sekarang | Setelah rencana P0 |
|---|---|---|
| Hasil dan Demo/Prototipe (30%) | **Berisiko.** Ide gerbang kuat dan nyata, tetapi dari clone bersih tanpa key: 34 dari 60 grafik Demo Gerbang error 500, dokumen contoh uji menahan semua gambar, veraPDF tidak terpasang | Kuat: demo luring penuh, angka bisa direproduksi |
| Kelengkapan dan Konsistensi Karya Ilmiah (20%) | **Gagal saat ini.** Bab 4–5 belum ada; Bab 3 menyebut Web Speech API, MathCAT, VLM penyunting, Docling yang tidak ada di kode | Lengkap dan konsisten bila Bab 3 direvisi minor |
| Presentasi (20%) | Belum ada naskah demo | Alur 15 menit terlatih |
| Tanya Jawab (20%) | Ada 8 titik serang yang belum punya jawaban (Bagian 4) | Jawaban siap, keterbatasan diakui di Bab 4 |
| Inovasi dan Dampak (10%) | Kuat: "tidak ada deskripsi keliru yang terbit tanpa penanda" mudah dipahami | Tetap |

**Kesimpulan:** proyek layak bersaing di papan atas, tetapi hanya bila dalam 23 jam ini tim (1) membuat demo jalan
luring dari repo, (2) menulis Bab 4–5 sendiri dengan angka yang dapat direproduksi, dan (3) menyelaraskan Bab 3
dengan kode. Berhenti menambah fitur baru di luar daftar P0/P1. Terlambat mengumpulkan lebih merugikan daripada
sampel kecil.

---

## 2. Temuan audit prototipe

Setiap temuan diberi bukti yang bisa diperiksa ulang.

### 2.1 Kritis (P0)

**A1. Hasil beku tidak dihasilkan oleh kode yang ada di repo.**
Kunci cache VLM adalah `hash(perintah + json.dumps(SCHEMA))` (`simak/vlm.py`, `extract_table`). Hash perintah
sama dengan manifes `results.json` (`a2db0023d821`, `bbe13c6a83dc`), tetapi hash ekstraksi di cache yang dipakai
run 12 Okt adalah `8ef1ab154d54`/`88fed23f8a87`, sedangkan kode HEAD menghasilkan `5f9442f371cc`/`4602a024e43a`.
Artinya skema JSON berubah setelah evaluasi beku (sebelum commit pertama 13 Okt), dan manifes tidak mencatat hash skema.
Uji ulang luring dari clone bersih pada 60 grafik uji: **26 lengkap di cache, 34 cache miss**; dari yang lengkap,
17 terbit dengan Fk 200/200 dan status identik dengan hasil beku (0 selisih). Jadi angka yang ada konsisten,
tetapi 57% set uji tidak bisa direproduksi tanpa memanggil API lagi.
Dampak: juri yang menjalankan repo tidak bisa mendapatkan angka Bab 4; demo luring rusak (A2).

**A2. Demo luring rusak dari clone bersih.**
- `POST /api/demo/jalankan/{id}` mengembalikan **HTTP 500** untuk 34 dari 60 grafik uji (syn036–syn089), karena
  `app._simak_chart` memanggil `pipeline.process_image`, bukan `process_or_hold`, sehingga `QuotaHabis` tidak tertangkap.
- `materi_05.pdf` (dokumen uji): 7 gambar → 5 antrean, 2 dekoratif, **0 terbit**, alasan
  "VLM tidak tersedia (GEMINI_API_KEY belum diset…)". `materi_01.pdf` (dev): 1 terbit.
- Juri melihat ini sebagai "fitur utama tidak jalan", padahal penyebabnya cache.

**A3. veraPDF tidak terpasang.** Panel B0/B1/D menampilkan
`Error: Could not find or load main class org.verapdf.apps.GreenfieldCliWrapper`. Folder `tools/` tidak ada di laptop
ini. Java 21 sudah ada.

**A4. Mode dengar tidak sesuai Bab 3 dan tidak bersuara tanpa ElevenLabs.**
Paper (Bab III.B, Tabel 6 OUT-02, Lampiran E): Web Speech API id-ID. Kode: `simak/output.py` hanya memanggil
`/api/suara` (ElevenLabs, berbayar per karakter; `voice.py`). Tanpa `ELEVENLABS_API_KEY`, `/api/suara` → 503 dan
`/api/suara/daftar` → `[]`. HTML keluaran yang diunduh tidak punya suara sama sekali di luar server.
Docstring `output.py` masih menyebut Web Speech API; docstring `voice.py` menyebut edge-tts + OpenVoice. Teks
materi juga terkirim ke layanan luar, hal yang tidak disebut paper (risiko etika/hak cipta, Bab III.J).

**A5. G1 menghitung penanda tahan sebagai teks alternatif bermakna.**
`pdfa11y.is_placeholder` hanya menolak kosong, "image N", nama berkas. Teks
"[Menunggu tinjauan ULD] … deskripsi belum diverifikasi." lolos. Bukti: `materi_05.pdf` dengan 5 dari 5 gambar
nondekoratif ditahan tetap `g1.pass = True`; G6 ringan D 6/6 lulus G1 padahal R = 18/18. Ini bukan pelanggaran
aturan PDF/UA (penanda memang informatif), tetapi angka G1 harus dilaporkan dua versi agar jujur.

### 2.2 Tinggi (P1)

**A6. "Dokumen nyata" G6 bukan materi kuliah.** `data/cc/cc.json`: dua RPS ITS, dua *Module Handbook*
(Unair, Unej), SOP Layanan Cuti Kuliah (UNY), Pemberitahuan Perkuliahan selama UTBK (UNY). Aturan URL stratum A
meloloskan dokumen administratif. Ini menjelaskan R = 18/18 dan 0 grafik terbit: tidak ada grafik data raster.
Paper menjanjikan pemeriksaan manual presisi aturan URL (Lampiran G.3) yang belum dilakukan.
Peluang: 28 tautan audit awal (`Semifinal/Audit/Audit_Awal_daftar_tautan_dicoba.txt`) adalah salindia dan bahan ajar
nyata (mis. "Slide Pertemuan 1 Sistem Operasi", "bahan ajar statistik"), kemungkinan besar memuat grafik.

**A7. Figur vektor tidak muncul di antrean UI.** 13 dari 18 gambar G6 adalah figur vektor; ditahan di PDF
(`pdfa11y.patch`, `figur_tambahan`) tetapi tidak menjadi kartu di `web/index.html`. Juri melihat antrean yang tidak
lengkap.

**A8. `requirements.txt` memaksa `torch`, `librosa`, `soundfile`, `edge-tts`** (±2 GB) padahal README menyebut
ElevenLabs satu-satunya suara dan kode OpenVoice tidak dipakai. Clone bersih jadi lambat dan rawan gagal.

**A9. README bertentangan dengan dirinya sendiri.** Tabel halaman menyebut "mode dengar Web Speech id-ID", bagian
Persiapan menyebut ElevenLabs satu-satunya; tabel Hasil memuat "G6 ringan", tetapi baris terakhir Batasan menulis
"G2, G5, G6 … belum dijalankan".

### 2.3 Sedang (untuk Bab 4 Keterbatasan dan tanya jawab)

- **A10. cF memeriksa klaim terhadap T1, padahal klaim diisi dari T1** (`chart.build_description` → `gate.fk`
  terhadap `el["table"] = t1`). cF hampir selalu 1 menurut konstruksi; perlindungan nyata dari cδ, cL, cA. Paper
  sudah menyebut ini di Bab II.C ("terhadap T nilainya 1 menurut definisi"); pastikan konsisten di Bab 4.
- **A11. Uji injeksi menguji logika gerbang, bukan kesalahan VLM.** Kesalahan disuntik ke klaim keluaran sendiri lalu
  diperiksa terhadap T1. 137/138 membuktikan gerbang menolak klaim yang tidak cocok dengan tabel, bukan bahwa VLM
  tidak salah baca. Bukti untuk kesalahan VLM adalah Fk terbit terhadap Tacuan (440/440) dan R.
- **A12. T1 dan T2 memakai model yang sama** (Gemma 4 26B-A4B, dua perintah). Kesalahan sistematik bisa sama di
  keduanya; cL lahir dari temuan ini (README). Sebutkan.
- **A13. G4 dijawab oleh model yang sama dengan pengekstraksi** dan pertanyaannya dibangkitkan dari tabel yang juga
  menjadi isi deskripsi; Q = 1,00 nyaris otomatis untuk templat yang memuat semua nilai. Klaim G4 harus sempit.
- **A14. Set uji sintetis dibuat penulis** (`data/make_synth.py`, matplotlib): 60 grafik, 4 dokumen; target paper
  150 grafik, 30 dokumen, 200 rumus. VisText/ChartQA/UniMER/IndoTabVQA tidak dipakai.
- **A15. Hanya satu run**; paper (Bab III.C) menjanjikan dua run dan selisihnya.
- **A16. Rumus**: tanpa pengenal kedua dan MathCAT; semua rumus ditahan dengan draf LaTeX dari VLM.
- **A17. Dekoratif** hanya `/Alt "Hiasan (dekoratif)"`, belum Artifact; tabel yang terlewat auto-tag belum `Table/TH`
  di PDF.
- **A18. CHT-02 "VLM penyunting bertoken terkunci"** (Bab III.F, Tabel 6) tidak ada: deskripsi murni templat. Ini
  lebih aman, tetapi berbeda dari paper.

### 2.4 Yang sudah kuat (pertahankan)

- Gerbang fail-closed nyata dan konsisten: gambar tanpa VLM ditahan, bukan menggagalkan dokumen (`process_or_hold`).
- Ambang dikunci di 30 grafik dev sebelum set uji dibuka, dengan riwayat perbaikan v1→v2 tercatat
  (`simak/thresholds.json`, `eval/kalibrasi_v1_sebelum_perbaikan.json`).
- Pembanding B2 diaudit manual (`eval/audit_b2.md`): 16/17 tanda benar; kesalahan B2 non-pembulatan semuanya
  rerata hitungan model. Ini argumen terkuat untuk "statistik dihitung kode".
- Selang Wilson di semua proporsi; manifes model dan hash perintah.
- `import app` berhasil dari clone bersih dengan dependensi inti; halaman `/`, `/demo.html`, `/evaluasi.html`,
  `/dengar.html`, keluaran HTML dan PDF bertag semuanya HTTP 200.

---

## 3. Temuan audit paper

Lensa: skill `academic-paper-reviewer` mode *quick* (kecocokan venue + isu kunci, tiap temuan dengan lokasi dan
perbaikan; status `NOT_CALIBRATED`), ditambah rubrik final panitia.

### 3.1 Kritis

- **B1. Bab 4 dan Bab 5 belum ada.** Wajib, dengan subbab: Bab 4 (Hasil Implementasi, Pengujian, Pembahasan,
  Keterbatasan); Bab 5 (Kesimpulan, Rencana Pengembangan, Dampak).
- **B2. Lampiran A (pernyataan AI) menyebut Claude dipakai untuk "penyusunan dan revisi draf naskah".** Guidebook
  7.2.4 butir 2 membatasi AI generatif pada pemeriksaan tata bahasa, penyuntingan bahasa, dan penelusuran awal
  pustaka; 7.2.7 kategori 4 menjadikan pelanggaran batas AI alasan diskualifikasi. Pernyataan harus tetap jujur
  (menyembunyikan penggunaan juga pelanggaran). Jalan yang aman: konsultasi tertulis ke panitia pagi ini, tulis
  Bab 4–5 dan revisi Bab 1–3 dengan kata-kata tim sendiri, dan buat Lampiran A final yang menggambarkan penggunaan
  AI sebenarnya pada versi final.
- **B3. Batas halaman final belum jelas.** TM Semifinal: maksimal 10 halaman termasuk daftar pustaka, tidak termasuk
  lampiran. Paper semifinal sudah 10 halaman untuk Bab 1–3. Ketentuan Final hanya berkata "ikuti template". Bila batas
  10 halaman berlaku, Bab 1–3 harus dipadatkan ±35–40%. Tanyakan ke panitia sekarang; siapkan rencana untuk kedua kemungkinan.
- **B4. Lampiran B Turnitin kosong** di PDF semifinal (hanya judul). Final wajib < 15% (Ketentuan Final; TM semifinal
  menulis < 20%, pakai yang lebih ketat) dan hasilnya dilampirkan.

### 3.2 Tinggi (konsistensi Bab 3 dengan MVP, bobot 20% + aturan "demo berbeda dari karya ilmiah")

| Lokasi di paper | Tertulis | Kenyataan kode | Pilihan |
|---|---|---|---|
| III.B, Tabel 6 OUT-02, Lampiran E | Mode dengar Web Speech API, suara Microsoft Andika id-ID | ElevenLabs berbayar | Tambah Web Speech di kode (P0-4) |
| II.C pers. (7), III.F | K(e) grafik = {cF, cδ, cA} | {cF, cδ, cA, cL} | Revisi minor: tambah cL dan alasannya |
| III.F Modul grafik, Tabel 6 CHT-02 | VLM menyunting kelancaran kalimat | Templat murni | Revisi minor |
| III.F Modul rumus, Tabel 6 FRM-01/02, Lampiran E | Dua pengenal + MathCAT WebAssembly | Semua rumus ditahan dengan draf VLM | Ubah status jadi "belum diimplementasikan; fail-closed" |
| II.C, Tabel 6 STR-01 | Docling bila tabel tanpa garis gagal | PyMuPDF `find_tables` sebagai cadangan | Revisi minor |
| III.B, III.F | Adaptor VLM, model belum disebut | Gemma 4 26B-A4B via Gemini API, T1=T2 model sama | Sebut model dan alasannya (kuota) |
| Tabel 6 kolom Status | Status per 30 Sep ("Rencana") | Sebagian besar sudah jalan | Perbarui status |
| III.I Rencana kerja | Jadwal 1–23 Okt | Sudah lewat | Ubah ke realisasi singkat atau pindah ke Bab 4 |
| Abstrak | "belum melaporkan kinerja sistem" | Ada hasil | Tulis ulang abstrak dengan hasil utama (100–250 kata, sesuai template) |
| Referensi | [55] SafeDocs dan [56] WebAssembly dikutip | Tidak ada di daftar (berhenti di [54]) | Tambahkan |

Topik dan tiga rumusan masalah **jangan diubah** (7.2.4 butir 7).

### 3.3 Sedang

- **B5.** Tabel 5 dan Lampiran G menjanjikan 600 PDF, VisText/ChartQA, UniMER, IndoTabVQA. Bab 3 boleh tetap sebagai
  rancangan, tetapi Bab 4 harus memuat tabel "rencana vs realisasi" agar juri tidak menemukannya sendiri.
- **B6.** Klaim G1 "lebih baik dari B1" di dokumen sintetis (4/4 vs 0/4) memakai n = 4, selang Wilson [0,51; 1,00].
  Tulis selangnya, jangan hanya persentase.
- **B7.** Pernyataan "tidak ada deskripsi keliru yang terbit tanpa penanda" harus dibatasi: terbukti pada 440 klaim
  sintetis; di dokumen nyata belum ada grafik yang terbit (sampel 0) kecuali G6 diperluas (P1-9).

---

## 4. Titik serang juri dan bahan jawaban (persiapan Tanya Jawab 20%)

| Pertanyaan yang hampir pasti muncul | Bahan jawaban (harus dijelaskan dengan kata-kata sendiri) |
|---|---|
| "Di PDF nyata, apa yang terbit otomatis?" | Hasil G6 diperluas (P1-9). Bila tetap 0, jelaskan fail-closed dan beban R sebagai biaya yang diukur |
| "Uji injeksi 137/138 bukankah pasti lulus?" | A11: membuktikan logika gerbang; kesetiaan terhadap data diukur terpisah oleh Fk vs Tacuan |
| "T1 dan T2 model yang sama, independen?" | A12, cL, rencana T2 model berbeda (`SIMAK_MODEL_T2`) |
| "G1 lulus padahal semua ditahan?" | Laporkan G1 dan G1-ketat (P0-5) |
| "Kenapa ElevenLabs, materi dosen dikirim ke luar?" | Setelah P0-4: bawaan Web Speech lokal; ElevenLabs opsional |
| "Set uji buatan sendiri?" | A14, ambang dikunci sebelum set uji dibuka, run kedua (P0-2) |
| "Kenapa hasil beku 12 Okt tapi kode berubah?" | A1: jelaskan perubahan skema, run kedua pada kode beku, selisihnya |
| "Berapa biaya/waktu per dokumen?" | `timing` di state.json; G6 `detik` 6–43 dtk per dokumen |

Setiap anggota (minimal 2 yang hadir) harus bisa menjelaskan pers. (2), (5), (7), arti R, dan alur demo.
Ketidakmampuan menjelaskan isi karya sendiri termasuk pelanggaran kategori 3 (7.2.7).

---

## 5. Rencana perbaikan prototipe

Prinsip: semua yang ditulis di paper harus ada di repo GitHub saat link dikumpulkan (23 Okt 23.59). Setelah itu hanya
perbaikan bug dan latihan demo. Beri tag `v1.0-final` pada commit yang dikumpulkan.

### P0 (wajib sebelum 16.00 WIB)

| # | Tugas | Berkas | Selesai bila | Perkiraan |
|---|---|---|---|---|
| P0-1 | Siapkan API key Gemini (env `GEMINI_API_KEY`, opsional `_2`) di laptop pengembang. Laptop ini tidak punya key di env/registri. Tanpa key, P0-2, P0-3, P1-9 tidak bisa jalan | env | `python -c "from simak import vlm; print(len(vlm.KEYS))"` ≥ 1 | 10 mnt |
| P0-2 | Salin `eval/results.json` → `eval/results_run1_2026-10-12.json` (jangan ditimpa). Jalankan `python -m eval.evaluate uji` pada kode HEAD tanpa mengubah `thresholds.json`. Ini mengisi cache untuk ke-60 grafik uji dan menjadi **run 2** yang dijanjikan Bab III.C. Catat selisih run 1 vs run 2 per gerbang. Tambahkan hash skema ke `vlm.manifest()` | `eval/`, `simak/vlm.py` | `results.json` baru + berkas run 1 + tabel selisih | 1–1,5 jam (latar belakang) |
| P0-3 | Isi cache untuk 6 dokumen contoh dan 30 grafik dev: proses `materi_01`–`06` lewat aplikasi sekali dengan key aktif. Commit seluruh `cache/` | `cache/` | Uji luring (P0-8) 0 cache miss | 30 mnt (latar belakang) |
| P0-4 | Mode dengar Web Speech API: di `output.py` dan `web/common.js`, pakai `speechSynthesis` dengan suara `id-ID` sebagai bawaan; ElevenLabs hanya bila `/api/suara/daftar` tidak kosong. Perbarui docstring `output.py`/`voice.py` | `simak/output.py`, `web/common.js` | HTML keluaran yang dibuka langsung dari disk bisa membaca dengan suara id-ID | 1–1,5 jam |
| P0-5 | G1 ketat: tambahkan hitungan figur berpenanda "[Menunggu tinjauan ULD]" dan `pass_ketat` (penanda tahan dihitung belum bermakna) di `g1_audit`; tampilkan keduanya di halaman Evaluasi dan laporkan keduanya | `simak/pdfa11y.py`, `eval/evaluate.py`, `web/evaluasi.html` | `results.json` memuat G1 dan G1_ketat | 45 mnt |
| P0-6 | Demo tahan error: `_simak_chart` memakai `process_or_hold`; endpoint demo mengembalikan 503 dengan pesan jelas, bukan 500; `/api/demo/grafik` boleh menandai grafik tanpa cache | `app.py`, `web/demo.html` | Tidak ada HTTP 500 pada 60 grafik tanpa key | 30 mnt |
| P0-7 | Pasang veraPDF 1.30 ke `tools/verapdf/` di laptop presentasi **dan** laptop cadangan (README langkah 1) | `tools/` | Panel B0/B1/D menampilkan jumlah aturan gagal | 30 mnt per laptop |
| P0-8 | Uji clone bersih sebagai gerbang rilis: venv baru, `pip install -r requirements.txt`, tanpa key, jalankan server, proses `materi_05.pdf`, jalankan Demo Gerbang di semua 60 grafik | — | 0 HTTP 500, 0 "VLM tidak tersedia" pada contoh, angka Evaluasi sama dengan `results.json` | 30 mnt |
| P0-9 | `requirements.txt`: pindahkan `edge-tts`, `librosa`, `soundfile`, `torch` ke `requirements-suara.txt`; perbaiki kontradiksi README (Web Speech/ElevenLabs, status G6), tambah bagian "Demo luring" dan "Reproduksi angka Bab 4" (perintah + commit + manifes) | `requirements.txt`, `README.md` | README cocok dengan kode dan Bab 4 | 30 mnt |

Pemeriksaan reproduksi luring yang dipakai audit ini (simpan sebagai `eval/reproduksi_luring.py` bila mau dipakai tim):

```python
# Jalankan dari folder Prototype: membaca cache saja, tanpa memanggil API.
import json
from simak import vlm, pipeline
from simak.config import thresholds
from eval.evaluate import charts
vlm.KEYS[:] = []
th = thresholds()
frozen = {p["id"]: p for p in json.load(open("eval/results.json", encoding="utf-8"))["per_grafik"]}
miss = beda = 0
for c in charts("uji"):
    img = open(f"data/synth/charts/{c['id']}.png", "rb").read()
    try:
        el = pipeline.process_image({"id": c["id"], "page": 1, "kind": "image", "png_bytes": img}, th)
    except vlm.QuotaHabis:
        miss += 1
        continue
    beda += frozen.get(c["id"], {}).get("status") != el["status"]
print(f"cache_miss={miss} status_beda={beda}")   # hasil audit: 34 dan 0; target setelah P0-2: 0 dan 0
```

### P1 (bila P0 selesai; batas 16.00 WIB, lalu bekukan kode)

| # | Tugas | Selesai bila |
|---|---|---|
| P1-9 | **G6 pada materi kuliah sungguhan.** Unduh ulang PDF dari 28 tautan audit awal (salindia, bahan ajar; tidak disebarkan, tidak di-commit). Pilih 10–20 yang memuat grafik data. Jalankan `pipeline.run`. Untuk setiap grafik yang terbit, dua anggota membuat tabel acuan secara manual dan terpisah, lalu hitung Fk terbit vs acuan dan kappa keputusan "deskripsi benar/salah". Laporkan jumlah grafik nyata yang terbit, Fk, R, dan kappa, termasuk bila hasilnya nol | Tabel G6 baru di `results.json` (kunci terpisah, mis. `G6_materi`) |
| P1-10 | Figur vektor tampil sebagai kartu antrean (render potongan halaman dari `patch.halaman_tidak_cocok`) | Jumlah kartu antrean UI = R di laporan |
| P1-11 | Rekam video cadangan demo yang benar-benar dijalankan (diberi label "rekaman run nyata, tanggal …"), hanya dipakai bila laptop gagal | Berkas video di dua perangkat |

### Ditunda (tulis di Bab 5 Rencana Pengembangan, jangan dikerjakan sekarang)

Ekstraksi data dari jalur vektor PDF; pengenal rumus kedua + MathCAT; T2 dengan model berbeda; Artifact untuk dekoratif;
`Table/TH` untuk tabel cadangan; audit 600 PDF; benchmark publik; uji pengguna G7 bersama ULD.

### Alur demo 15 menit (usulan, latih dan ukur waktunya)

1. Masalah (2 mnt): "Dengar" PDF asli vs SIMAK pada satu dokumen (halaman Dengar).
2. Demo Gerbang (4 mnt): satu grafik berlabel → B2 vs SIMAK → suntik "tukar label" → B2 tetap terbit, SIMAK menahan.
   Lalu satu grafik tanpa label nilai → SIMAK menahan karena cL.
3. Remediasi & Tinjauan (4 mnt): proses `materi_0x.pdf` (sudah di-cache), tunjukkan veraPDF B0/B1/D, antrean ULD,
   setujui satu elemen, unduh HTML dan putar mode dengar.
4. Evaluasi (3 mnt): G1/G1-ketat, G3 (Fk, injeksi, B2 17 angka keliru), G4, G6, R.
5. Keterbatasan dan rencana (2 mnt).
Cadangan: laptop kedua dengan clone yang sama, cache lengkap, veraPDF terpasang, tanpa ketergantungan internet.

---

## 6. Rencana perbaikan paper

### 6.1 Struktur final (ikuti template: judul bab angka Romawi, subbab berhuruf, keterangan tabel di atas, gambar di bawah)

- **Abstrak** (100–250 kata): tulis ulang dengan hasil utama.
- **I. Pendahuluan, II. Tinjauan Pustaka, III. Metodologi**: revisi minor sesuai tabel 3.2.
- **IV. Hasil dan Pembahasan**
  - A. Hasil Implementasi
  - B. Pengujian
  - C. Pembahasan
  - D. Keterbatasan
- **V. Penutup**
  - A. Kesimpulan
  - B. Rencana Pengembangan
  - C. Dampak
- Referensi (tambah [55], [56], dan rujukan baru bila ada).
- Lampiran: A pernyataan AI (versi final yang akurat), B hasil Turnitin final, C–G tetap (dipangkas bila perlu),
  **H baru: reproduksi** (commit `v1.0-final`, perintah, manifes model/perintah/skema, run 1 vs run 2).

### 6.2 Isi wajib Bab 4 (daftar periksa, bukan teks)

**A. Hasil Implementasi**
- Gambar: tangkapan layar empat halaman (Remediasi & Tinjauan, Demo Gerbang dengan injeksi, Evaluasi, HTML keluaran
  dengan penanda status). Ambil ulang setelah P0 (yang di `.impeccable/review/` sudah lama).
- Tabel fitur Tabel 6 dengan kolom status akhir: jalan / jalan sebagian / belum, dan berkas kodenya (README "Pemetaan
  ke proposal").
- Satu contoh keluaran utuh: grafik, tabel T1/T2, δ, klaim, deskripsi level 1–3, status.

**B. Pengujian** (metrik harus sama dengan Tabel 7)
- Tabel gerbang: gerbang, kriteria terkunci, hasil (k/n, Wilson 95%), status (lulus / tidak lulus / tidak dijalankan).
  Sumber: `eval/results.json` run 2 dan `results_run1_2026-10-12.json`.
- G1 dan G1-ketat (P0-5); veraPDF B0 → B1 → D.
- G3: Fk terbit, jumlah terbit, R, injeksi per jenis, B2 (terbit 60/60, 17 angka keliru pada 7 grafik, audit
  `eval/audit_b2.md`).
- G4: Q(D), Q(B2), dan catatan A13.
- G6: ringan (6 dokumen administratif) dan G6 materi (P1-9) dipisah.
- Selisih run 1 vs run 2.
- G2, G5, G7: "tidak dijalankan" beserta alasannya.

**C. Pembahasan** (tim menulis sendiri): jawab RM1, RM2, RM3 satu per satu, masing-masing dengan angka dari B.
Bandingkan dengan B0/B1/B2 dan dengan literatur Bab II (CharXiv, Kumar dkk.).

**D. Keterbatasan**: A5, A6, A10–A18, ukuran sampel, model yang sama untuk T1/T2/QA, set uji sintetis.

### 6.3 Isi wajib Bab 5
- A. Kesimpulan: satu jawaban per rumusan masalah.
- B. Rencana Pengembangan: daftar "Ditunda" di Bagian 5, urut menurut dampak terhadap R (jalur vektor dulu, temuan G6).
- C. Dampak: bagi mahasiswa tunanetra (penanda status, mode dengar), staf ULD (beban R yang terukur), dosen
  (unggah PDF apa adanya). Batasi klaim: dampak belajar belum diuji (G7).

### 6.4 Anggaran halaman
- Bila batas 10 halaman berlaku: Bab I ±1,5 hlm, Bab II ±1,5, Bab III ±2,5, Bab IV ±3, Bab V ±0,5, referensi ±1.
  Pindahkan Tabel 4, rincian Tabel 5, dan Gambar 3 ke lampiran.
- Bila tidak ada batas: tetap padatkan; juri membaca sebelum presentasi.

### 6.5 Kepatuhan
- Nama berkas: `IRIS kata HQ ini lomba terakhir_ICC2026_Final.pdf` (format `[NamaTim]_ICC2026_Final`).
- Turnitin < 15% di luar kutipan dan pustaka, laporan dilampirkan.
- Link GitHub publik `github.com/Faiz7557/IRIS-Pusaka`, tag `v1.0-final`, README memuat cara menjalankan.
- Jangan commit PDF materi kuliah nyata atau audio suara (sudah di `.gitignore`).

---

## 7. Jadwal 23 Oktober (WIB)

Peran usulan (sesuaikan): **P** = prototipe (1 orang), **E** = evaluasi/G6 (1 orang), **W1/W2** = penulis
(2 orang). Bergantian tidur; minimal dua orang harus segar di 27–28 Okt.

| Jam | P | E | W1 | W2 |
|---|---|---|---|---|
| 00.30–01.30 | P0-1, mulai P0-2 di latar belakang | Unduh PDF tautan audit (P1-9) | Kirim pertanyaan tertulis ke panitia: batas halaman final, Lampiran A | Kerangka Bab 4–5 di docx |
| 01.30–07.00 | P0-4, P0-5, P0-6 (gantian tidur) | Tidur | Tidur | Revisi Bab 3 (tabel 3.2) |
| 07.00–11.00 | P0-3, P0-9, P0-7 | P1-9: jalankan pipeline, pilih grafik, tabel acuan manual | Bab 4.A (tangkapan layar setelah P0) | Abstrak, Bab 1–2 minor, referensi [55] [56] |
| 11.00–14.00 | P0-8 uji clone bersih; P1-10 bila sempat | P1-9: penilai kedua, kappa | Bab 4.B dari `results.json` | Tidur |
| 14.00–16.00 | Bekukan kode, tag `v1.0-final`, push | Serahkan angka G6 ke W1 | Bab 4.C–D | Bab 5 |
| 16.00–18.00 | Tangkapan layar final, latihan demo | Periksa angka paper vs `results.json` | Gabung naskah, Lampiran A–H | Format template, anggaran halaman |
| 18.00–19.30 | Laptop cadangan siap | Turnitin | Perbaiki similarity bila > 15% | Baca ulang dan sunting |
| 19.30–21.00 | — | Cek ulang konsistensi demo vs Bab 3–4 | PDF final, nama berkas benar | — |
| **21.00** | **Submit** PDF + link GitHub (sisakan 3 jam cadangan) | | | |
| 21.00–23.59 | Verifikasi unggahan berhasil; jangan ubah repo setelah ini kecuali bug | | | |

Titik keputusan:
- **03.00**: P0-2 belum jalan karena tidak ada key → pakai cache yang ada, laporkan run 1 saja, dan batasi Demo Gerbang
  ke 26 grafik yang tercache (P0-6).
- **11.00**: P1-9 belum menghasilkan grafik nyata yang terbit → hentikan, laporkan apa adanya (termasuk nol).
- **16.00**: fitur apa pun yang belum selesai keluar dari paper, masuk Bab 5.

---

## 8. Keputusan yang hanya bisa diambil tim

1. Isi pertanyaan ke panitia (batas halaman, Lampiran A) dan siapa yang mengirim.
2. Ada atau tidak API key Gemini malam ini (menentukan P0-2, P0-3, P1-9).
3. Web Speech sebagai bawaan (rekomendasi) atau revisi Bab 3 agar menyebut ElevenLabs.
4. Pembagian peran P/E/W1/W2 dan siapa dua orang yang pasti hadir 27–28 Okt.
