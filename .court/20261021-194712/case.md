# Perkara

Tim IRIS ("IRIS kata HQ ini lomba terakhir", Universitas Airlangga) ingin mengembangkan karya semifinal SIMAK menjadi karya final Innovation Case Competition (ICC) 2026, dengan paper semifinal Bab 1-3 dan prototipe yang sudah ada. Pertanyaan sidang: apakah progres saat ini (paper semifinal + prototipe) layak dan siap untuk memenangkan / bersaing kuat di Babak Final ICC 2026 sesuai ketentuan final?

Hari ini: 21 Oktober 2026. Batas pengumpulan: 23 Oktober 2026 pukul 23.59 WIB (sisa sekitar 2 hari).

---

## 1. Ketentuan Babak Final ICC 2026 (dari dokumen resmi panitia)

- Penyelenggara: Pusat Satu Data dan Kecerdasan Digital, Universitas Airlangga (Campus Data Week 2026). Tema umum: "Improving Student's Learning Experience in Indonesia Through AI Innovation".
- 6 tim finalis (dari 20 semifinalis). Nilai semifinal tidak dihitung; semua dinilai ulang dari awal.
- WAJIB: (a) Karya ilmiah lengkap Bab 1-5: Bab 1-3 dari draf semifinal, boleh direvisi minor; Bab 4 Hasil dan Pembahasan dan Bab 5 Penutup ditulis baru. (b) Demo prototipe MVP: sudah bisa dijalankan, sesuai metodologi Bab 3, boleh aplikasi atau hardware. PPT opsional, tidak memengaruhi nilai.
- Topik dan rumusan masalah harus tetap sama dengan draf semifinal; hanya isi yang boleh direvisi.
- Isi Bab 4: (01) Hasil implementasi, dengan tangkapan layar/output; (02) Pengujian: hasil uji MVP memakai metrik yang ditulis di Bab 3; (03) Pembahasan: apakah hasil menjawab rumusan masalah Bab 1; (04) Keterbatasan: bagian yang belum berjalan atau belum sempat diuji.
- Isi Bab 5: (01) Kesimpulan: jawaban singkat atas rumusan masalah; (02) Rencana pengembangan; (03) Dampak bagi target pengguna. Nama/urutan subbab mengikuti template panitia. Format mengikuti template resmi.
- MVP BOLEH: aplikasi/website/sistem yang bisa dijalankan; fitur utama sesuai Bab 3 dan Bab 4. TIDAK BOLEH: hanya desain/mockup; demo yang direkayasa seolah-olah berjalan; demo yang berbeda dari isi karya ilmiah. "Juri melihat apakah MVP sesuai dan bisa membuktikan isi karya ilmiah. Produk yang sederhana tidak masalah."
- Presentasi 15 menit (demo termasuk di dalamnya, tidak ada sesi demo terpisah) + 15 menit tanya jawab dengan juri. Disarankan: latih demo dari awal sampai akhir dan catat waktunya; bawa data contoh dan perangkat cadangan kalau internet atau laptop bermasalah; setiap anggota siap menjelaskan metode dan hasil.
- Bobot penilaian final: 30% Hasil dan Demo/Prototipe (MVP berjalan dan sesuai isi karya ilmiah); 20% Kelengkapan dan Konsistensi Karya Ilmiah (Bab 1-5 lengkap dan sejalan dengan draf semifinal); 20% Presentasi (kejelasan selama 15 menit termasuk demo); 20% Tanya Jawab; 10% Inovasi dan Dampak (kebaruan ide dan manfaatnya untuk mahasiswa).
- Pengumpulan: PDF bernama [NamaTim]_ICC2026_Final dan link GitHub source code MVP, lewat platform peserta. Terlambat dikenai pengurangan poin.
- Aturan semifinal tetap berlaku: similarity Turnitin di bawah 15% (tidak termasuk kutipan dan daftar pustaka) dan dilampirkan; wajib ada pernyataan penggunaan AI di lampiran; topik tidak boleh diganti; demo harus asli (demo palsu = pelanggaran berat). Diskualifikasi untuk: plagiarisme, joki, kerja sama antartim, pemakaian AI di luar batas, demo palsu.
- Batas penggunaan AI menurut guidebook (7.2.4): AI generatif dalam penyusunan karya ilmiah dibatasi hanya untuk pemeriksaan tata bahasa, penyuntingan bahasa, dan bantuan penelusuran awal tinjauan pustaka. AI generatif dilarang dipakai untuk menghasilkan rumusan masalah, analisis, argumen, metodologi, interpretasi hasil, kesimpulan, atau narasi substansial lainnya. Pernyataan penggunaan AI wajib memuat nama tools, tujuan spesifik, pernyataan isi telah ditinjau dan disunting penulis, dan tanggung jawab penuh penulis.
- Final luring di Universitas Airlangga, 27-28 Oktober 2026; minimal 2 anggota hadir; tidak hadir tanpa alasan jelas = gugur.

## 2. Paper semifinal (yang sudah dikumpulkan; lolos ke Top 6)

Judul: "SIMAK: Remediasi Materi Kuliah Berbahasa Indonesia agar Dapat Disimak oleh Mahasiswa Tunanetra dan Pendengar dengan Gerbang Verifikasi". 4 penulis. 10 halaman isi + lampiran A-G (total 27 halaman).

Masalah: PDF materi kuliah tidak aksesibel bagi pembaca layar. Data: PDDikti Juni 2025 mencatat 3.128 mahasiswa disabilitas di 282 PT, tunanetra 1.727 (terbesar). Audit awal tim (28 PDF materi kuliah, 18 kampus, sampel tidak acak): 0 dari 28 lulus PDF/UA-1; hanya 29 dari 1.111 elemen Figure bertag (2,6%) memiliki teks alternatif; 6 dari 24 dokumen berbahasa Indonesia mendeklarasikan bahasa Indonesia. Literatur: GPT-4o 47,1% di CharXiv (grafik ilmiah), VLM berhalusinasi. Pengguna sekunder: mahasiswa pendengar (diperlakukan sebagai hipotesis).

Solusi: pipeline remediasi dengan Unit Layanan Disabilitas (ULD) sebagai peninjau. Melengkapi tag/struktur (OpenDataLoader auto-tag + tambalan pikepdf), deskripsi grafik dari tabel data yang diekstraksi VLM dua kali (T1, T2) dengan statistik dihitung kode, templat level 1-3 (Lundgard & Satyanarayan), pembacaan rumus via MathML + MathCAT bahasa Indonesia, mode dengar, dan gerbang fail-closed: elemen yang tidak lolos pemeriksaan ditahan di antrean tinjauan ULD. "Nilai jualnya bukan AI yang lebih cerdas, melainkan jaminan bahwa tidak ada deskripsi keliru yang terbit tanpa penanda."

Rumusan masalah:
1) Bagaimana mengubah materi kuliah PDF berbahasa Indonesia (teks, tabel, grafik, rumus) menjadi dokumen berstruktur dengan urutan baca benar bagi pembaca layar?
2) Bagaimana menghasilkan deskripsi grafik dan pembacaan rumus berbahasa Indonesia yang setia pada data sumbernya?
3) Bagaimana merancang alur kerja yang menahan keluaran yang tidak dapat diverifikasi dan menyerahkannya ke peninjau ULD sehingga tidak ada deskripsi keliru yang terbit tanpa penanda?

Persamaan kunci di Bab II/III: Kendall τ untuk urutan baca (1); selisih relatif dua ekstraksi δ (2); regresi dan perubahan terfit untuk tren (3)-(4); proporsi klaim setia Fk dengan klaim (e, m, v) dan toleransi ε×rentang (5); kecocokan Levenshtein untuk rumus A (6); gerbang pub(e) = 1[K(e)≠∅]·Π c_k(e) (7); selang Wilson (8); kappa Cohen (9); rasio kesetaraan informasi Q = Acc_alt/Acc_tab dan beban tinjauan R = |E_tinjau|/|E| (10).

Arsitektur di Bab III.B: aplikasi web tiga lapis, FastAPI, OpenDataLoader (Java), pikepdf, PyMuPDF, veraPDF; adaptor VLM tidak terikat penyedia; "Keluaran HTML memuat mode dengar berbasis Web Speech API; suara bahasa Indonesia (Microsoft Andika, id-ID)". Lampiran E: MathCAT di peramban via WebAssembly; mode dengar Web Speech API id-ID.

Data yang dijanjikan untuk final (Bab III.D, Tabel 5, Lampiran G): sampel acak berstrata 600 PDF berbahasa Indonesia dari bingkai Common Crawl domain ac.id (bingkai 228.383 PDF, 1.833 domain, 1.911 berciri materi kuliah), dibagi dev/uji 2:1 per kampus; set sintetis penulis (target 30 dokumen, 150 grafik, 200 rumus); VisText/ChartQA subset 300 grafik; UniMER-Test 200 rumus; IndoTabVQA 300 citra tabel; 60 dokumen nyata untuk G6 (dipilih agar 90% teramati berbatas bawah Wilson ~80%).

Rancangan evaluasi (Tabel 7), pembanding B0 (PDF asli), B1 (auto-tag OpenDataLoader saja), B2 (VLM langsung tanpa gerbang). Tujuh gerbang dengan ambang dikunci sebelum uji: G1 struktur & metadata (inti): ≥90% dokumen uji bebas kegagalan teks alt bermakna, bahasa, judul, lebih baik dari B1, pada 200 PDF uji; G2 urutan baca τ ≥0,90; G3 kesetiaan angka (inti): Fk ≥0,98 pada keluaran terbit terhadap tabel acuan, ≥0,90 deskripsi yang sengaja diubah tertahan; G4 kesetaraan informasi (inti): Q ≥0,80; G5 rumus A ≥0,90; G6 dokumen nyata (inti): 60 dokumen, G1 ≥80%, κ ≥0,60, R dilaporkan, cek singkat NVDA; G7 uji pengguna tunanetra: ditunda. G2 dan G5 "bila waktu memungkinkan". Versi akhir dijalankan dua kali dan selisihnya dilaporkan. Penilai manusia dua orang, kappa dilaporkan.

Rencana kerja di paper: 1-3 Okt uji penentu; 4-9 Okt perakitan + G1; 10-15 Okt modul grafik, gerbang, G3, G4; 16-19 Okt antarmuka tinjauan, G6, rumus; 20-22 Okt pembekuan, evaluasi set uji, tulis Bab IV-V; 23 Okt pengumpulan. Lingkup minimum demo: unggah PDF, keluaran HTML aksesibel dan PDF bertag, deskripsi grafik dengan gerbang, antrean tinjauan; hasil dokumen contoh di-cache karena demo 15 menit dan bergantung layanan VLM.

Lampiran A (pernyataan AI) di paper semifinal, bunyinya: "Tim menggunakan Claude (Anthropic) untuk penelusuran awal pustaka, pemeriksaan angka terhadap sumber, pembuatan skrip audit dokumen dan skrip uji kelayakan awal, penyusunan dan revisi draf naskah, serta pemeriksaan bahasa. Seluruh isi telah ditinjau dan disunting oleh penulis, dan penulis bertanggung jawab penuh atas akurasi dan orisinalitas karya. Seluruh referensi telah diperiksa keasliannya oleh penulis."
Lampiran B (hasil Turnitin) pada PDF semifinal berisi judul saja, tanpa isi yang terbaca pada ekstraksi teks.
Lampiran F: 13 gambar analisis strategis (profil nilai jual, pohon masalah, Value Proposition Canvas, kompetitor, STP, BMC, SWOT, TOWS, Porter, PESTEL, risiko, peta jalan).

## 3. Prototipe saat ini (folder Prototype, repo GitHub github.com/Faiz7557/IRIS-Pusaka, branch main, 5 commit, commit terakhir 20 Okt 2026, working tree bersih)

Kode: Python ~2.000 baris (app.py FastAPI 368 baris; modul simak/: pipeline, vlm, chart, gate, pdfa11y, output, voice, listen, config) + web statis (index, demo, evaluasi, dengar; HTML/CSS/JS tanpa framework; font Atkinson Hyperlegible). Folder cache/ berisi 698 respons VLM yang di-commit agar demo stabil.

Halaman:
- Remediasi & Tinjauan (/): unggah PDF atau pilih contoh; tampilkan veraPDF B0/B1/D, G1, beban tinjauan R, antrean ULD (setujui/ubah/tolak/dekoratif) dengan T1 vs T2 dan klaim yang bisa diklik ke sumbernya.
- Demo Gerbang (/demo.html): B2 (VLM langsung) vs SIMAK pada grafik yang sama; tombol "suntik kesalahan" (ubah angka, tukar label, angka turunan, tren) memperlihatkan B2 tetap terbit sementara SIMAK menahan.
- Evaluasi (/evaluasi.html): G1, G3, G4 dengan selang Wilson, injeksi per jenis, manifes.
- Dengar: transkrip "apa yang terdengar" PDF asli vs SIMAK; plus perintah suara (SpeechRecognition peramban, pemetaan ucapan ke tombol via LLM).
- Keluaran HTML: lang="id", penanda status per gambar, tabel data grafik, mode dengar.

Implementasi gerbang: untuk grafik K = {cF, cδ, cA, cL}. cF: Fk = 1 (klaim dari templat yang diisi T1, dicek terhadap T1 dan fakta turunan). cδ: δ(T1,T2) ≤ θe. cA: nilai dalam rentang label tik sumbu ±20%. cL (ditambahkan dari analisis set dev): label nilai harus tercetak pada grafik (menurut kedua ekstraksi); grafik tanpa label nilai selalu ditahan. Rumus, foto, diagram nondata, tabel-citra: selalu ditahan dengan draf dari VLM. Figur vektor (bukan raster) ditahan dengan teks alt "[Menunggu tinjauan ULD] ...". Gambar dekoratif disaring heuristik ukuran/hash.
VLM bawaan: Gemma 4 26B-A4B lewat Gemini API, untuk T1, T2, B2, dan penjawab G4. T1 dan T2 memakai model yang sama dengan dua perintah berbeda (satu bahasa Indonesia, satu bahasa Inggris), karena kuota free tier; model T2 berbeda bisa diatur lewat env (gemma-4-31b-it diuji jalan tetapi 40-70 detik/panggilan). Suhu 0, respons di-cache per hash(citra, perintah, model).

Hasil evaluasi beku (12 Okt 2026, eval/results.json). Ambang dikunci pada 30 grafik dev: θe = 0,01, ε = 0,02, ρ = 0,10. Kalibrasi diperbaiki dua kali di set dev sebelum set uji dibuka (v1: Fk 0,937 bahkan pada δ=0, karena dua ekstraksi bisa sepakat pada angka salah untuk grafik tanpa label; dari situ lahir cL; v2: toleransi cA 20%).
Set uji tertahan: SINTETIS buatan tim (data/make_synth.py, grafik matplotlib + dokumen PDF): 60 grafik, 4 dokumen.
- G1: D 4/4 dokumen lulus (Wilson [0,51; 1,00]); B0 0/4, B1 0/4; veraPDF aturan gagal B0 6 → B1 5 → D 0.
- G3: Fk terbit 440/440 klaim = 1,00 [0,991; 1,00] terhadap tabel acuan; D terbit 40/60 grafik; R = 20/60 (semua grafik tanpa label nilai ditahan); injeksi kesalahan tertahan 137/138 = 0,993 (satu tukar label lolos karena selisih 5 < ε·s = 6,74). B2: terbit 60/60, Fk perkiraan 566/583 = 0,971, 17 angka tidak setia pada 7/60 grafik (audit manual: 13 pembulatan pada grafik tanpa label, 3 rerata yang dihitung model salah, 1 salah tandai pemeriksa).
- G4 (20 grafik, 80 pertanyaan otomatis dari tabel, dijawab model yang sama): akurasi tabel 80/80, D 80/80, B2 79/80; Q(D) = 1,00, Q(B2) = 0,99.
- G6 "ringan": 6 PDF nyata dari Common Crawl CC-MAIN-2026-39 (4 kampus, stratum A bingkai = 57 dokumen pada panen itu): G1 D 6/6 (B0 0/6, B1 0/6); veraPDF penuh lulus D 2/6; R = 18/18 (seluruh gambar non-dekoratif ditahan; 13 dari 18 adalah figur vektor dari Word/PowerPoint); 0 grafik terbit otomatis pada dokumen nyata. Teks alt penanda "[Menunggu tinjauan ULD] ..." dihitung sebagai teks alternatif bermakna oleh aturan G1 (aturan pengisi hanya menolak kosong, "image N", nama berkas, kata tunggal).
- Belum dijalankan: G2, G5, G7; G6 penuh (60 dokumen, kappa dua penilai, cek NVDA); audit skala besar 600 PDF (hanya bingkai yang dibangun; unduhan, audit, analisis belum ada di folder); VisText/ChartQA/UniMER/IndoTabVQA belum dipakai; dua kali run dengan selisih belum dilakukan.
- README menulis batasan apa adanya: figur vektor belum dideskripsikan dan belum muncul sebagai kartu di antrean UI; rumus belum memakai pengenal kedua dan MathCAT (semua rumus ditahan dengan draf LaTeX + ucapan dari VLM); dekoratif diberi /Alt "Hiasan (dekoratif)" di PDF, belum sebagai Artifact; tabel yang tidak dikenali auto-tag benar di HTML tetapi belum menjadi Table/TH di PDF bertag; pemeriksa angka B2 adalah pemeriksa pola.

Suara / mode dengar: paper menyebut Web Speech API id-ID. Kode saat ini tidak memakai speechSynthesis peramban; mode dengar memanggil endpoint server /api/suara. README menulis ElevenLabs sebagai satu-satunya sumber suara (berbayar per karakter, butuh ELEVENLABS_API_KEY dan VOICE_ID; tanpa itu mode dengar tidak bersuara; teks dikirim ke ElevenLabs). Docstring voice.py masih menyebut edge-tts + OpenVoice V2 (suara klon "Satya", dengan izin pemilik). requirements.txt mencantumkan edge-tts, librosa, soundfile, torch. Catatan sesi 14 Okt: edge-tts pernah ditolak Microsoft (403) lalu diperbaiki dengan upgrade.

Kondisi menjalankan: README memerlukan Java 21 + veraPDF dipasang manual ke tools/ (tidak di repo), GEMINI_API_KEY, opsional ElevenLabs. Pada checkout di laptop ini, folder tools/ tidak ada dan `import app` gagal karena paket google-genai tidak terpasang pada Python yang aktif (kemungkinan dijalankan di lingkungan lain; belum dikonfirmasi). Ada .claude/launch.json untuk menjalankan uvicorn port 8000.

Dokumen desain: PRODUCT.md (penonton utama prototipe adalah juri; produk = alat kerja ULD; prinsip "verified or visibly held", "show the evidence", "honest reporting", aksesibel WCAG 2.2 AA), DESIGN.md, tangkapan layar review desktop/mobile.

## 4. Status karya ilmiah final

Bab 4 dan Bab 5 belum ditulis (belum ada draf di folder). Bab 1-3 belum direvisi untuk final. Lampiran Turnitin final belum ada. Kerangka penulisan paper semifinal dibangun dengan skrip Python (build_docx.py, content.py) yang menghasilkan .docx/.pdf.

## 5. Yang diminta pengguna

Analisis menyeluruh ketentuan final, paper semifinal, dan prototipe, lalu penjurian atas keseluruhan progres: apakah progres ini siap dan kuat untuk Babak Final, dan apa yang harus dilakukan dalam sisa waktu.
