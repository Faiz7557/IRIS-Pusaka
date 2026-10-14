# SIMAK: prototipe

Prototipe *Sistem Ilustrasi Materi Aksesibel untuk Kuliah* (proposal ICC 2026, tim IRIS).
Masukannya PDF materi kuliah apa adanya. Keluarannya PDF bertag (PDF/UA-1) dan HTML aksesibel dengan
mode dengar. Setiap deskripsi grafik **terverifikasi terhadap tabel data atau ditahan** di antrean tinjauan ULD.

## Menjalankan

```bash
pip install -r requirements.txt
python data/make_synth.py 90          # set sintetis: 90 grafik + 6 dokumen PDF
python -m uvicorn app:app --port 8000 # buka http://localhost:8000
```

Key API disimpan di environment variable `GEMINI_API_KEY`, ditambah `GEMINI_API_KEY_2`, `_3`, … untuk
rotasi kuota. Jangan menaruh key di berkas mana pun di repo ini.

### Persiapan alat (folder `tools/`, tidak ikut di repo)

1. **Java 21** (Temurin), lalu **veraPDF 1.30** dipasang headless ke `tools/verapdf/`:
   unduh `https://software.verapdf.org/releases/verapdf-installer.zip`, ekstrak, ganti `TOOLS_DIR` di
   `setup/verapdf-auto-install.xml` dengan path folder `tools` kamu, lalu
   `java -jar verapdf-izpack-installer-*.jar setup/verapdf-auto-install.xml`.
2. **Suara (opsional):** `git clone https://github.com/myshell-ai/OpenVoice tools/OpenVoice`, lalu unduh
   `converter/config.json` dan `converter/checkpoint.pth` dari `https://huggingface.co/myshell-ai/OpenVoiceV2`
   ke `tools/ov_ckpt/converter/`.
3. **Rekaman suara referensi** tidak disertakan karena milik pribadi dan dipakai atas izin. Taruh rekaman
   (1–2 menit, dengan izin pemilik suara) di `data/voice/satya_ref.mp3`. Tanpa rekaman ini, pilih suara
   "Gadis", "Ardi", atau "Suara peramban".

4. **Suara manusia via ElevenLabs (opsional, berbayar per karakter):** buat suara dari rekaman (dengan izin
   pemilik suara) di akun ElevenLabs, lalu atur environment variable `ELEVENLABS_API_KEY` dan
   `ELEVENLABS_VOICE_ID` (opsional `ELEVENLABS_MODEL`, bawaan `eleven_multilingual_v2`). Pilihan "Suara manusia"
   baru muncul bila keduanya terisi. Teks yang dibacakan dikirim ke ElevenLabs, dan audio hanya dibuat saat
   diputar (tanpa pra-pembuatan massal) agar kredit tidak terpakai sia-sia.

Data yang sengaja tidak ikut di repo: PDF materi kuliah nyata (`data/cc/*.pdf`, hanya metadata `cc.json`
yang disertakan; jalankan `python data/fetch_cc.py` untuk mengambil ulang dari Common Crawl), rekaman dan
audio suara Satya, serta folder sesi `work/`.

Evaluasi dengan kriteria terkunci:

```bash
python -m eval.evaluate kalibrasi   # set pengembangan saja → simak/thresholds.json (locked)
python -m eval.evaluate uji         # set uji tertahan, sekali → eval/results.json
```

## Halaman

| Halaman | Isi |
|---|---|
| **Remediasi & Tinjauan** (`/`) | Unggah PDF atau pilih contoh. Menampilkan veraPDF B0/B1/D, G1, beban tinjauan R, antrean ULD (setujui/ubah/tolak/dekoratif) dengan T1 vs T2 dan klaim yang bisa diklik ke sumbernya |
| **Demo Gerbang** (`/demo.html`) | B2 (VLM langsung) vs SIMAK pada grafik yang sama. Tombol *suntik kesalahan* (ubah angka, tukar label, angka turunan, tren) menunjukkan B2 tetap terbit sementara SIMAK menahan |
| **Evaluasi** (`/evaluasi.html`) | G1, G3, G4 dengan selang Wilson 95%, injeksi per jenis, dan manifes run |
| **Keluaran HTML** | HTML semantik `lang="id"`, penanda status per gambar, tabel data grafik, mode dengar Web Speech id-ID |

## Pemetaan ke proposal

| Proposal | Berkas |
|---|---|
| STR-01 struktur dan urutan baca | `simak/pdfa11y.py` (`autotag`), `simak/pipeline.py` (`_blocks`, tabel cadangan PyMuPDF) |
| OUT-01 perakitan dan validasi | `simak/pdfa11y.py` (`patch`, `verapdf`, `g1_audit`) |
| CLS-01 jenis gambar | `pipeline._classify_decorative` (ukuran, hash, pengulangan) + kolom `jenis` dari VLM |
| CHT-01 ekstraksi ganda, pers. (2), cA | `simak/vlm.py`, `chart.delta`, `chart.axis_check` |
| CHT-02 statistik kode, pers. (3)–(4), templat level 1–3 | `chart.derived`, `chart.build_description` |
| GAT-01 gerbang, pers. (5) dan (7) | `simak/gate.py` (`fk`, `evaluate`) |
| REV-01 tinjauan ULD | `pipeline.review`, `web/index.html` |
| OUT-02 mode dengar | `simak/output.py` |
| Evaluasi, pers. (8), G1/G3/G4 | `eval/evaluate.py` |
| Adaptor VLM tidak terikat penyedia | `simak/vlm.py` (T1 dan T2 memakai model berbeda) |

## Model

Bawaan: **Gemma 4 26B-A4B** (open-weight) lewat Gemini API untuk T1, T2, B2, dan penjawab G4.
T1 dan T2 memakai dua perintah berbeda, sesuai Bab III.F. Untuk akun berbayar, `SIMAK_MODEL_T2` bisa diisi
model lain (mis. `gemma-4-31b-it`, sudah diuji dan berjalan tetapi ±40–70 dtk/panggilan) supaya kedua pengenal
benar-benar independen. Model lain bisa diganti lewat env `SIMAK_MODEL`, `SIMAK_MODEL_T2`, `SIMAK_MODEL_QA`.
Respons di-cache di `cache/` menurut hash (citra, perintah, model) supaya demo stabil.

## Hasil (versi beku, 12 Okt 2026, `eval/results.json`)

Set uji tertahan sintetis: 60 grafik, 4 dokumen. Ambang dikunci pada 30 grafik dev (θe = 0,01, ε = 0,02, ρ = 0,10).

| Gerbang | Hasil | Kriteria | Status |
|---|---|---|---|
| G1 | D 4/4 dokumen lulus (B0 0/4, B1 0/4); veraPDF: B0 6 → B1 5 → D 0 aturan gagal | ≥ 90%, lebih baik dari B1 | lulus |
| G3 | Fk terbit **440/440 = 1,00** [0,991; 1,00]; injeksi tertahan **137/138 = 0,993** | Fk ≥ 0,98; ≥ 0,90 | lulus |
| G3 (pembanding) | B2 terbit 60/60, 17 angka tidak setia pada 7/60 grafik; D 0 angka keliru terbit | — | — |
| G3 (biaya) | D terbit 40/60; beban tinjauan R = 20/60 (semua grafik tanpa label nilai) | dilaporkan | — |
| G4 | Q(D) = **1,00** (80/80); Q(B2) = 0,99 | Q ≥ 0,80 | lulus |
| G6 ringan | 6 PDF nyata (Common Crawl ac.id, 4 kampus): G1 D 6/6 (B0, B1 0/6); veraPDF penuh D 2/6; R = 18/18 | dilaporkan | — |

Catatan penting:
- Satu injeksi tukar label tidak tertahan karena kedua nilai berselisih 5 < ε·s = 6,74. Kesalahan di bawah ε memang tidak terdeteksi secara definisi.
- Audit pemeriksa B2 ada di `eval/audit_b2.md`. Kesalahan B2 yang bukan pembulatan semuanya berupa **rerata yang dihitung model** (mis. 1.107 vs 1.206,8). Inilah alasan SIMAK menghitung statistik dengan kode.
- Kalibrasi dua kali diperbaiki pada set dev sebelum set uji dibuka (riwayat di `simak/thresholds.json` dan `eval/kalibrasi_v1_sebelum_perbaikan.json`). v1 menunjukkan Fk 0,937 bahkan pada δ = 0: dua ekstraksi bisa *sepakat pada angka yang salah* untuk grafik tanpa label. Dari temuan ini lahir pemeriksaan **cL**.
- Pemetaan alt per halaman (fail-closed untuk figur vektor) ditambahkan setelah G6 menemukan Figure vektor yang tidak memiliki citra raster. Perubahan ini dipicu dokumen nyata, dan seluruh evaluasi dijalankan ulang sesudahnya.
- Temuan G6: di materi nyata, 13 dari 18 gambar adalah figur vektor dari Word/PowerPoint. Ekstraksi data langsung dari jalur vektor PDF (cadangan di Bab III.H) adalah langkah berikut yang paling berdampak untuk menurunkan R.

## Batasan (dilaporkan apa adanya)

- Kuota free tier Gemini Flash hanya 20 permintaan/hari/model. Karena itu evaluasi memakai Gemma, dan T1/T2 memakai model yang sama dengan dua perintah berbeda.
- Figur vektor (bukan citra raster) belum dideskripsikan; semuanya ditahan dengan penanda di PDF dan dihitung dalam R, tetapi belum muncul sebagai kartu di antrean UI.
- Evaluasi baru satu kali run (VLM suhu 0 + cache); dua run dengan selisih dilaporkan seperti di Bab III.C belum dilakukan.
- Rumus belum memakai pengenal kedua dan MathCAT, jadi seluruh rumus ditahan (fail-closed) dengan draf LaTeX + ucapan untuk ULD.
- Gambar dekoratif diberi `/Alt` "Hiasan (dekoratif)" di PDF; penandaan sebagai *Artifact* (menyunting aliran konten) belum dibuat. Di HTML sudah `alt=""`.
- Tabel yang tidak dikenali auto-tag tetap benar di HTML (deteksi PyMuPDF), tetapi di PDF bertag belum menjadi `Table/TH`.
- Pemeriksa angka B2 adalah pemeriksa pola pada teks bebas, sehingga Fk B2 berupa perkiraan.
- Evaluasi baru pada set sintetis. G2, G5, G6 (dokumen nyata Common Crawl), dan G7 belum dijalankan.
