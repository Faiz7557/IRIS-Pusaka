# Telaah proyek SIMAK

> Ini telaah sebelum implementasi. Perubahan cream, voice dan hasil verifikasi terbaru tercatat di `Prototype/tasks/implementation-cream.md`.

Tanggal: 23 Oktober 2026. Tahap: memahami sistem sebelum perbaikan.

## Dasar pemeriksaan

Pada pemeriksaan awal, folder `Prototype` belum tersedia sehingga kode diperoleh dari repositori yang dirujuk dokumen proyek: `https://github.com/Faiz7557/IRIS-Pusaka`, commit `7f86623` (HEAD dan tag `v1.0-final` saat pemeriksaan). Setelah percakapan dilanjutkan, folder lokal telah tersedia beserta tools dan sesi lama, tetapi tanpa metadata `.git`. Kode utama yang diperiksa ulang menunjukkan implementasi yang sama; kesamaan seluruh berkas belum diverifikasi lewat hash. Hasil uji salinan awal dan kondisi folder terkini dibedakan di bawah.

Pemeriksaan mencakup kode backend dan frontend utama, konfigurasi, modul voice, pipeline PDF, gerbang verifikasi, keluaran HTML, data evaluasi tersimpan, tes yang tersedia, dokumentasi arsitektur/desain, bahan paper, serta isi dan preview template UI. Ini bukan audit baris demi baris seluruh cache dan bukan pengujian kepatuhan aksesibilitas menyeluruh.

Kode aplikasi tidak diubah. Kredensial ElevenLabs dari percakapan belum disimpan, belum dipasang, dan belum dipakai untuk memanggil API. Penggantian voice dicatat sebagai pekerjaan implementasi berikutnya sesuai permintaan untuk menelaah dahulu.

## Tujuan dan pengguna

SIMAK adalah Sistem Ilustrasi Materi Aksesibel untuk Kuliah. Petugas Unit Layanan Disabilitas (ULD) memasukkan PDF materi, memeriksa elemen yang belum dapat diverifikasi, lalu menyediakan PDF bertag dan HTML aksesibel untuk mahasiswa. HTML memiliki mode dengar.

Nilai utama sistem terletak pada mekanisme penerbitannya: deskripsi grafik yang memenuhi pemeriksaan dapat terbit otomatis, sedangkan elemen yang tidak memenuhi pemeriksaan diberi penanda dan ditahan untuk tinjauan manusia. Mekanisme ini tidak membuktikan bahwa setiap PDF atau setiap hasil AI selalu benar.

## Alur aplikasi

1. **Masukan.** Pengguna mengunggah PDF atau memilih satu dari enam PDF sintetis. Endpoint unggah memeriksa signature, keterbacaan, kata sandi, ukuran maksimal 20 MiB, dan jumlah 1–200 halaman. Pemrosesan dibatasi satu dokumen aktif pada satu proses server.
2. **Sesi.** Server membuat `work/job_<id>/`, menyalin PDF asli, memulai thread pemrosesan, dan memberi ID job kepada frontend. Frontend menanyakan progres sekitar setiap 1,2 detik.
3. **Struktur.** OpenDataLoader menganalisis tata letak dan melakukan auto-tag bila diperlukan. PyMuPDF melengkapi deteksi tabel. Heading, paragraf, tabel, dan gambar menjadi rekaman elemen dalam urutan baca.
4. **Gambar.** Gambar dirender untuk analisis. Heuristik ukuran/pengulangan membantu menyaring dekorasi; VLM mengklasifikasikan jenis gambar dan mengekstraksi data.
5. **Grafik.** VLM membaca tabel dua kali menggunakan dua prompt berbeda, menghasilkan T1 dan T2. Bawaan keduanya memakai model yang sama; ini bukan dua model independen. Statistik dan kalimat deskripsi dibangun melalui kode dan templat.
6. **Gerbang.** Empat pemeriksaan menentukan apakah grafik boleh terbit: cF (klaim sesuai tabel), cδ (dua ekstraksi konsisten), cA (nilai masuk rentang sumbu), dan cL (label nilai tercetak). Ambang terkunci dibaca dari `simak/thresholds.json`.
7. **Tinjauan.** Rumus, foto, diagram nondata, figur vektor, grafik yang gagal pemeriksaan, atau gambar tanpa respons VLM yang tersedia ditahan sesuai jalur implementasinya. ULD dapat menyetujui, mengubah dan menyetujui, menolak, atau menandai dekoratif. Draf AI yang belum disetujui tidak diterbitkan sebagai deskripsi final.
8. **Keluaran.** Sistem menambal metadata/tag PDF dan teks alternatif, membangun HTML semantik dengan gambar/font tertanam, lalu menjalankan audit G1 dan validator veraPDF jika alatnya tersedia. Tinjauan menerbitkan versi keluaran baru melalui pointer state atomik, dengan lock per job pada satu proses.
9. **Dengar.** Transkrip hasil SIMAK dibentuk dari state elemen yang sama. Versi PDF asli pada halaman Dengar merupakan simulasi urutan baca, bukan rekaman NVDA atau hasil pengujian pengguna.

Status elemen dibedakan menjadi `terbit_otomatis`, `antrean`, `disetujui`, `diubah`, `ditolak`, dan `dekoratif`. Keputusan ULD dicatat terpisah dari verifikasi otomatis.

## Peta halaman

| Halaman | Fungsi |
|---|---|
| `/` — Remediasi | Unggah/pilih contoh, progres, ringkasan hasil, antrean ULD, unduh keluaran |
| `/dengar.html` | Perbandingan simulasi PDF asli dan hasil SIMAK; player dan transkrip |
| `/demo.html` | Pembanding B2 versus SIMAK, grafik sumber, tabel acuan, injeksi kesalahan dan skor sesi |
| `/evaluasi.html` | Menampilkan hasil evaluasi tersimpan beserta cakupan dan manifes; tidak menjalankan eksperimen baru |
| `/keluaran/<id>/simak.html` | Dokumen hasil untuk membaca dan mendengarkan |

Alur kerja operasional dimulai dari Remediasi. Untuk presentasi, alur Dengar → Demo Gerbang → Remediasi/Tinjauan → Evaluasi dapat memperkenalkan manfaat sebelum rincian teknis.

## Peta kode

| Berkas/folder | Tanggung jawab |
|---|---|
| `Prototype/app.py` | FastAPI, unggah, status job, tinjauan, demo, suara, keluaran |
| `Prototype/simak/pipeline.py` | Orkestrasi, klasifikasi, state elemen, tinjauan dan versi keluaran |
| `Prototype/simak/vlm.py` | Prompt/skema ekstraksi, Gemini API, cache, rotasi key |
| `Prototype/simak/chart.py` | Penyelarasan tabel, statistik, klaim dan templat deskripsi |
| `Prototype/simak/gate.py` | Pemeriksaan cF/cδ/cA/cL dan injeksi kesalahan |
| `Prototype/simak/pdfa11y.py` | Auto-tag, penambalan PDF, G1, pemanggilan veraPDF |
| `Prototype/simak/output.py` | HTML hasil mandiri dan player suara tersendiri |
| `Prototype/simak/listen.py` | Transkrip asli/hasil dan ringkasan perbandingan |
| `Prototype/simak/voice.py` | Normalisasi ucapan, ElevenLabs dan cache MP3; masih memuat kode suara lama |
| `Prototype/web/common.js` | Navigasi, konteks job, klaim, player bersama dan perintah suara |
| `Prototype/web/style.css` | Token, komposisi, komponen dan responsivitas UI |
| `Prototype/eval/` | Evaluasi dan hasil tersimpan |
| `Prototype/tests/` | Tes transaksi tinjauan, batas unggah, HTML hasil dan regresi frontend |

Stack saat ini adalah FastAPI + HTML/CSS/JavaScript statis. Perbaikan desain tidak memerlukan migrasi framework.

## Template UI dan kondisi desain saat ini

ZIP berisi template Sill untuk pet boarding, satu HTML dengan CSS/JS inline, preview, lisensi dan credits. Ciri utamanya adalah latar hitam, sela hitam, panel warna datar, oranye/violet/taupe/sage, judul Gabarito besar, serta komposisi grid asimetris. Template asal memakai animasi GSAP/Lenis dan aset eksternal.

**Temuan penting: versi kode terbaru sudah mengadaptasi desain Sill.** `web/style.css` memuat token Sill, header navigasi hitam, panel oranye dan tipografi Gabarito lokal. Reader hasil juga sudah memakai warna terkait. Jadi pekerjaan berikutnya perlu menilai dan menyempurnakan adaptasi yang sudah ada, bukan menganggap UI masih sepenuhnya versi katalog hijau.

Yang perlu dipertahankan dari SIMAK: keterbacaan tabel, status dengan teks, bukti klaim ke sumber, tombol keyboard, fokus, dan reduced motion. Konten pet boarding, foto kucing, formulir pemesanan dan koreografi scroll template tidak memiliki fungsi langsung pada alat ULD.

Penilaian komposisi aplikasi secara visual pada browser desktop/mobile belum dilakukan dalam pemeriksaan ini; preview template sudah dilihat dan implementasi CSS/markup sudah dibaca.

## Voice ElevenLabs

Jalur backend ElevenLabs sudah tersedia:

- `/api/suara/daftar` menawarkan suara ElevenLabs ketika key dan voice ID tersedia dalam environment.
- `/api/suara` membuat audio melalui `voice.synthesize()`.
- Model bawaan di kode adalah `eleven_multilingual_v2`; hasil MP3 di-cache berdasarkan teks, voice ID, model dan kecepatan.
- Pembuatan massal di latar dilewati untuk ElevenLabs; audio dibuat saat diminta.

Saat ini suara peramban tetap menjadi bawaan. Menyetel key dan voice ID saja belum mengganti bawaan tersebut. Ada **dua jalur frontend yang harus diselaraskan**: `web/common.js` untuk aplikasi dan JavaScript tertanam di `simak/output.py` untuk HTML hasil. Reader hasil saat ini memulihkan kecepatan, tetapi belum memulihkan pilihan voice yang tersimpan.

Untuk implementasi berikutnya: pasang kredensial pada environment server, gunakan voice ID yang diberikan, tentukan pemilihan ElevenLabs saat tersedia secara konsisten pada dua player, pertahankan suara peramban untuk HTML yang dibuka tanpa server, dan uji audio pendek secara nyata. Key tidak perlu masuk frontend atau source control.

Endpoint membatasi teks 4.000 karakter per permintaan, sedangkan player mengirim satu blok teks sekaligus. Blok panjang perlu dipotong agar tidak gagal saat memakai ElevenLabs. Kualitas suara, izin akses voice, dan keberhasilan kredensial belum diuji pada tahap telaah ini.

## Bukti pengujian lokal

Pengujian Python dan smoke berikut dilakukan pada salinan awal dengan environment audit yang memakai paket sistem sebagai dasar. Ini bukan pembuktian instalasi bersih penuh dari `requirements.txt`. Environment dan artefak audit tersebut tidak lagi tersedia pada snapshot folder terkini setelah percakapan dilanjutkan; hasil berikut berasal dari output eksekusi yang tercatat pada percakapan.

| Pemeriksaan | Hasil |
|---|---|
| Tes Python yang tersedia | 14/14 lulus |
| Tes regresi frontend Node | Lulus: polling stale, start ganda, pemulihan offline, kontrol player dan empty state |
| Empat halaman utama melalui TestClient | Semua HTTP 200 |
| Cache grafik demo | 60/60 tersedia |
| Demo `syn043` tanpa key VLM | HTTP 200; terbit otomatis |
| Empat injeksi pada `syn043` | Semuanya HTTP 200 dan berubah menjadi antrean |
| Pemrosesan `materi_01.pdf` tanpa panggilan VLM live | Selesai, 3 halaman; 3 gambar terbit otomatis, 2 antrean, 2 dekoratif |
| Keluaran PDF dan HTML contoh | Keduanya HTTP 200 |
| Endpoint transkrip Dengar | HTTP 200 |
| G1 internal contoh hasil | Biasa lulus; ketat tidak lulus karena 2 gambar masih ditahan |
| veraPDF pada salinan awal | Tidak tersedia, sehingga validasi penuh pada smoke awal belum dapat dikonfirmasi |
| veraPDF pada folder terkini | `--version` berhasil: versi 1.30.3; validasi dokumen belum diulang |
| Tes frontend pada folder terkini | Dijalankan ulang dan tetap lulus |
| Interpreter Python aktif pada folder terkini | Belum memiliki `google-genai`, `pikepdf`, dan `opendataloader-pdf` |

Uji cache dan demo ini tidak menjalankan ulang seluruh eksperimen penelitian. Hasil evaluasi tersimpan melaporkan 440/440 klaim terbit setia pada acuan, 40/60 grafik terbit, dan 137/138 injeksi tertahan pada set sintetis; angka tersebut harus tetap disertai cakupan datasetnya.

Artefak `.review/`, environment audit, serta job smoke awal tidak tersedia pada snapshot folder terkini. Jangan mengandalkan path tersebut untuk reproduksi. Folder terkini memiliki sesi hasil lama pada `Prototype/work/`; sesi tersebut bukan hasil uji baru dalam telaah ini. Kode aplikasi tidak diedit dalam penelaahan.

## Temuan dan urutan perbaikan

1. **Kesiapan demo lokal:** siapkan environment Python dari requirements dan jalankan ulang alur lengkap menggunakan folder terkini. veraPDF 1.30.3 sudah tersedia dan executable; hasil validasi PDF/UA penuh perlu dikonfirmasi setelah dependensi Python siap.
2. **Voice:** integrasi backend sudah ada; selaraskan konfigurasi, bawaan pemilihan, penanganan blok panjang dan pemulihan galat pada kedua player, lalu uji suara yang diminta.
3. **Dokumentasi tertinggal:** `tasks/plan.md` dan `tasks/todo.md` menyebut implementasi belum dimulai; kode sudah memuat redesign dan sejumlah perbaikan teknis. `DESIGN.md` juga masih menjelaskan dunia visual katalog hijau. Audit lama perlu diberi label historis.
4. **Ketahanan VLM:** `process_or_hold()` hanya menangkap `QuotaHabis`; error jaringan/JSON/skema lain dapat lolos dan menggagalkan job. Ini temuan pembacaan kode, belum direproduksi dengan gangguan jaringan. Penanganan perlu menjaga status tahan beserta alasan yang jelas.
5. **Tinjauan figur campuran:** pada halaman yang memuat raster dan figur tambahan tanpa pemetaan pasti, keputusan ULD untuk figur campuran hanya diterapkan pada HTML; PDF mempertahankan penanda tahan. Batas ini perlu tetap jelas di UI dan demo.
6. **Batas kemampuan:** rumus belum memakai pengenal kedua/MathCAT, figur vektor belum diekstraksi datanya, PDF pindai/PPT belum didukung langsung, dan sebagian tabel HTML belum memiliki struktur setara di PDF. Ini ruang pengembangan yang sudah diakui kode/dokumentasi.
7. **Klaim hasil:** lulus G1 biasa atau validator teknis tidak berarti seluruh gambar sudah dideskripsikan. G1 ketat, sisa antrean dan cakupan evaluasi perlu tetap mudah ditemukan.
8. **Penyempurnaan visual:** lakukan pemeriksaan browser terhadap komposisi yang sudah diimplementasikan, terutama prioritas aksi, grafik-klaim-keputusan, antrean ULD, kontras dan mobile, sebelum memutuskan perubahan layout berikutnya.

Masalah audit lama berupa cache demo tidak lengkap, review target tidak dikenal menjadi 500, review tanpa transaksi, unggahan tanpa pembatas, dan janji cleanup enam jam tidak boleh langsung dianggap masih berlaku: versi terbaru sudah memuat perbaikan terkait, dan bagian yang dicakup tes telah lulus. Penguncian transaksi tetap terbatas satu proses, belum jaminan operasi multi-worker.
