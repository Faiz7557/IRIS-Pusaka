# Implementasi redesign SIMAK × Sill

Status: **belum dimulai; untuk diskusi rencana**. Dasar: [plan.md](plan.md). Arahan yang sudah dikonfirmasi: adaptasi visual template kuat, demo final lebih dahulu, seluruh alur inti tetap berfungsi. Checkbox di sini adalah pekerjaan implementasi mendatang, bukan pekerjaan audit yang sudah selesai.

Tidak ada frontend build command pada stack saat ini. Startup tetap `python -m uvicorn app:app --host 127.0.0.1 --port 8000` dari `Prototype`; gunakan interpreter/environment proyek yang memiliki requirements. Jangan menjalankan server kedua di port yang sama. Pengujian Python baru memakai stdlib unittest bila tidak ada runner proyek lain yang ditetapkan.

## Gelombang 0 — Baseline dan bukti visual pertama (8–13 jam indikatif)

### T01 — Baseline sintetis yang dapat diulang

- [ ] Rekam file/version, route, screenshot, API shape, dan enam status dari versi sebelum perubahan.
- [ ] Siapkan fixture sintetis kecil untuk hasil campuran, vektor tanpa draf, empty, partial, dan error; tidak menyertakan PDF nyata/key/voice berizin.
- [ ] Definisikan smoke alur inti dan target viewport pada satu manifest agar hasil sebelum/sesudah dapat dibandingkan.

Verifikasi: buka empat route dan reader dengan fixture yang tercatat; manifest merujuk file yang benar-benar ada. Tidak menganggap job ID sesi audit sebagai fixture permanen.

Dependensi: keputusan rencana. Berkas: `tests/fixtures/ui_states.json` (baru, usulan), `tasks/evidence/baseline.json`, `tasks/smoke.md` (baru). Ukuran: M. Hasil: baseline yang dapat direproduksi tanpa VLM berbayar.

### T02 — Token, font, dan surface baru

- [ ] Tambahkan token peran visual Sill dan status semantik terpisah; warna normal-text mengikuti pasangan kontras yang sudah dihitung.
- [ ] Tambahkan Gabarito lokal dengan notice resmi; pertahankan Atkinson lokal untuk body/reader.
- [ ] Definisikan panel/grid/control baru tanpa mengimpor CSS global template atau mematahkan halaman yang belum dipindahkan.

Verifikasi: font fallback dan local font diuji; cek kontras normal/hover/focus/disabled yang relevan; tidak ada CDN wajib. Token/ukuran root 18px tetap konsisten.

Dependensi: T01. Berkas: `web/style.css`, `web/fonts.css`, satu aset font lokal beserta notice, `THIRD_PARTY_NOTICES.md` (baru jika belum ada). Ukuran: M.

### T03 — Navigasi shared dengan kompatibilitas caller

- [ ] Siapkan output header hitam pada fungsi shell yang sudah dipakai; pertahankan hook lama sampai caller dipindahkan.
- [ ] Nav empat halaman, wordmark ke `/`, halaman aktif, perintah suara, dan bukti tersimpan tetap berfungsi serta berlabel.
- [ ] Tidak menambah overlay/drawer atau mode presentasi baru yang memerlukan state tambahan.

Verifikasi: panggilan render dari keempat halaman tidak menghasilkan null selector/console error; akses keyboard dan voice resolver cocok dengan label baru.

Dependensi: T02. Berkas: `web/common.js`, `web/style.css`. Ukuran: S. Jika kompatibilitas sementara menambah kompleksitas lebih besar dari satu perubahan atomik, gabungkan T03/T04 dalam satu commit terkoordinasi dan uji keempat caller sebelum menyatakan selesai.

### T04 — Pindahkan shell ke empat halaman

- [ ] Terapkan markup header/main yang benar pada empat halaman dan hilangkan asumsi rail desktop 272px.
- [ ] Navigasi mobile ringkas; heading, skip link, dan fokus tidak tertutup header.
- [ ] Aturan inline per halaman yang bergantung shell lama diubah hanya jika diperlukan.

Verifikasi: empat route pada 1440×900 dan 390×844; screenshot dibaca untuk wrapping dan prioritas tindakan; keyboard skip link masih mencapai main.

Dependensi: T03. Berkas: `web/index.html`, `web/demo.html`, `web/dengar.html`, `web/evaluasi.html`. Ukuran: M.

### T05 — Selesaikan satu irisan Demo Gerbang

- [ ] Grafik asli, kontrol run/injeksi, dan dua status tersedia dalam komposisi panel khas template; hasil B2/D setara lebarnya di desktop.
- [ ] Run, empat injeksi, reset, skor sesi, klaim-ke-sumber, dan deep link `?grafik` tetap benar; picker/baseline tidak dapat bertukar konteks saat busy.
- [ ] Galat jaringan memulihkan kontrol; respons stale tidak mengganti grafik aktif; teks panjang tetap dapat diakses lewat disclosure bila diringkas.

Verifikasi: syn043 cached → baseline → empat injeksi yang berlaku → reset; uji request gagal dan ganti pilihan cepat dengan fixture. Cek grafik, klaim dipilih, dan kedua verdict pada 1366×768. `?grafik` sudah ada pada source audit `demo.html:97–105`; jangan salah menganggapnya fitur baru.

Dependensi: T04. Berkas: `web/demo.html`, `web/style.css`, `web/common.js` bila komponen shared perlu, fixture baseline terkait. Ukuran: M.

### Checkpoint 1 — Arah visual

- [ ] T01–T05 lolos smoke dan komposisi terasa sebagai adaptasi kuat Sill, bukan sekadar palet baru.
- [ ] Source→klaim→keputusan lebih dekat, dua status tidak bergantung warna, URL/caller lain tetap berjalan.
- [ ] Bandingkan screenshot desktop/mobile dengan template dan baseline; diskusikan koreksi komposisi sebelum menyebarkan ke seluruh workspace.

## Gelombang 1 — Dengar dan kontinuitas (4–7 jam)

### T06 — Dengar yang jujur, setara, dan operabel

- [ ] Label simulasi dekat judul/aksi; tombol versi asli dan SIMAK mudah dijangkau sebelum uraian panjang.
- [ ] Struktur transkrip memakai kontrol native/semantik yang sesuai dan fokus tetap saat player memperbarui segmen.
- [ ] Satu audio aktif; suara hilang/gagal/dokumen berubah memiliki recovery dan teks tetap tersedia.

Verifikasi: keyboard pilih bagian/play/jeda/prev/next/lompat gambar, berganti dua versi, kecepatan, stop saat keluar; fixture empty dan voice unsupported. Audio nyata diuji pada perangkat demo dan hasilnya dicatat, tidak diasumsikan dari ketersediaan API.

Dependensi: T05. Berkas: `web/dengar.html`, `web/common.js`, `web/style.css`, fixture transkrip. Ukuran: M.

### T07 — Bawa konteks dokumen lintas halaman

- [ ] Link Dengar↔Remediasi membawa job; root benar-benar membaca query job baru dan memuat state yang tepat.
- [ ] Refresh memakai ID server yang masih valid; penyimpanan lokal hanya ID/konteks minimum, bukan PDF/alt sensitif permanen.
- [ ] Job hilang atau dihapus memberi recovery dan membersihkan konteks usang.

Verifikasi: job selesai → Dengar → Remediasi → refresh; job 404; tanpa job; hapus sesi; dua tab dengan konteks berbeda. Jangan mengubah dukungan `?doc` Dengar atau `?grafik` Demo tanpa alasan.

Dependensi: T06. Berkas: `web/index.html`, `web/dengar.html`, `web/common.js`, fixture 404. Ukuran: M.

### Checkpoint 2 — Narasi pembuka

- [ ] Dengar→Demo bekerja dengan konten nyata yang sama, label simulasi tidak tersembunyi, suara tidak bertumpuk.
- [ ] Tanpa audio pun teks dan bukti tetap lengkap; fokus/keyboard tidak hilang ketika transkrip diperbarui.

## Gelombang 2 — Pekerjaan ULD lengkap (10–17 jam)

### T08 — Unggah dan progres yang fokus

- [ ] Form upload mendahului daftar contoh di mobile; nama/deskripsi contoh berasal metadata nyata atau tetap nama file yang jujur.
- [ ] Busy state dikunci sebelum request dimulai; poll memiliki job/token pemilik, timer bersih, dan catch/finally yang benar.
- [ ] Status proses sesuai server; reconnect membaca job yang sama dan tidak memulai job ganda.

Verifikasi: upload valid, tanpa file, sampel, double click, response A terlambat setelah B, koneksi putus, polling 404/gagal. Pada 390×844 aksi input utama tidak didorong melewati seluruh daftar contoh.

Dependensi: T07. Berkas: `web/index.html`, `web/style.css`, fixture progres. Ukuran: M.

### T09 — Review/save yang konsisten dan galat domain

- [ ] Elemen/job tidak ditemukan menjadi respons domain tepat; validasi alt tetap di server.
- [ ] Review/delete disinkronkan per job pada proses tunggal; tidak ada lost update antar dua keputusan.
- [ ] Pilih dan uji strategi publikasi konsisten PDF/HTML/state; kegagalan assemble tidak ditandai sebagai sukses. Rename atomik per file saja tidak disebut transaksi penuh.

Verifikasi: stdlib unittest terfokus `python -m unittest discover -s tests -p "test_review*.py"` setelah test dibuat; mock validator/assembler untuk concurrent save dan injected write failure. Semua artefak di direktori temporer, tanpa VLM atau dokumen pengguna.

Dependensi: T01; selesai sebelum T10 dinyatakan aman. Berkas: `simak/pipeline.py`, `app.py`, `tests/test_review.py` (baru), bila perlu satu helper penyimpanan yang memang digunakan. Ukuran: M. Batas: satu worker; tidak menambah storage service terdistribusi.

### T10 — Antrean dan editor ULD

- [ ] Ringkasan operasional pendek, antrean mudah dicapai, sumber/draf/alt jelas; enam status dan provenance manusia/otomatis tetap berbeda.
- [ ] Satu aksi persetujuan utama mengikuti dirty state dengan payload setujui/ubah; tolak/dekoratif terpisah dan akibatnya jelas.
- [ ] Draf/fokus terjaga pada error/navigation; save ambigu memeriksa state terbaru sebelum retry mutasi.

Verifikasi: enam status, raster/vector/formula, alt kosong/panjang, berpindah item dirty, simpan sukses/gagal, antrean habis, semua gambar, keyboard setelah render. Tinjauan valid diuji hanya dengan fixture sintetis disposable.

Dependensi: T08–T09. Berkas: `web/index.html`, `web/style.css`, `web/common.js` bila perlu, fixture review. Ukuran: M.

### T11 — Dukungan file dan copy sesuai kemampuan

- [ ] Hapus janji retensi berkala yang belum dijalankan; batas scan/PPT/PDF berlapis teks berada dekat input.
- [ ] Jika dipilih batas byte/halaman, nilai ditetapkan dari mesin demo dan benar-benar ditegakkan/diuji server; jangan hanya label frontend.
- [ ] Galat internal tidak disajikan sebagai traceback/jargon ke pengguna; detail diagnostik tetap di log lokal yang sesuai.

Verifikasi: non-PDF, PDF gagal parse, file di batas dan melewati batas bila diberlakukan; copy tidak menjanjikan kapasitas/retensi yang belum ada. `python -m unittest discover -s tests -p "test_upload*.py"` untuk validasi server baru bila ditambahkan.

Dependensi: T08. Berkas: `web/index.html`, `app.py`, `tests/test_upload.py` (baru hanya jika validasi ditambah), `README.md` untuk batas operasional. Ukuran: M. TTL lifecycle sungguhan adalah tambahan terpisah jika disepakati, bukan terselip pada task copy.

### T12 — Hapus sesi dengan hasil yang jelas

- [ ] Ada konfirmasi dengan nama sesi dan akibat yang tepat sebelum menghapus dokumen/keputusan; pengguna bisa batal.
- [ ] Kegagalan DELETE tidak diikuti reload seolah sukses; konteks lokal dibersihkan hanya setelah sukses.
- [ ] Aksi tidak bersaing sebagai CTA utama dengan unduh/dengar; delete dan review tidak balapan.

Verifikasi: batal, sukses di fixture disposable, 404, error jaringan, pending review; jangan menghapus job pengguna/audit untuk menguji UI. Pemeriksaan sumber/mock dapat membuktikan sebagian jalur tanpa mutasi nyata.

Dependensi: T07, T09–T10. Berkas: `web/index.html`, `web/common.js` hanya bila konteks bersama memerlukannya, fixture delete. Ukuran: M.

### Checkpoint 3 — Alur kerja tidak kehilangan data

- [ ] Unggah→progres→hasil→tinjau→dengar/unduh selesai pada data sintetis.
- [ ] Tidak ada stale poll, lost update, draf hilang, atau sukses palsu pada failure yang diuji.
- [ ] Perbedaan status struktur PDF dan kelengkapan deskripsi terlihat; vector/mixed-page limits tetap dijelaskan.

## Gelombang 3 — Evaluasi dan keluaran (6–10 jam)

### T13 — Evaluasi bertingkat dan faktual

- [ ] Panel ringkas memakai angka dari JSON aktual; unit/dataset/run dekat angka, bukan copy hard-coded.
- [ ] G1 ketat, R, kegagalan injeksi, G6 ringan, dan gerbang belum diuji tetap tampak/terjangkau.
- [ ] Mobile mempertahankan k/n dan CI; empty/partial/error tidak berubah jadi angka nol palsu.

Verifikasi: cocokkan ringkasan/tabel dengan fixture hasil run, JSON hilang/partial, label panjang, 320 px. Jangan membuat perbandingan grafik 440 klaim vs 17 angka keliru seolah unit analisisnya sama.

Dependensi: T04; dapat dikerjakan setelah checkpoint visual bila file tidak bentrok. Berkas: `web/evaluasi.html`, `web/style.css`, fixture evaluasi. Ukuran: M.

### T14 — Reader HTML mandiri mengikuti identitas baru

- [ ] Perbarui subset token/komponen reader dengan area baca tenang, status akurat, dan light/dark yang sudah didukung.
- [ ] Pertahankan semantik, embedded font/images, data-say, voice browser, dan fallback tanpa server/jaringan.
- [ ] Perbarui kontrol secara minimal agar fokus/viewport mobile tidak tertutup; jangan merakit ulang massal job lama.

Verifikasi: `python -m unittest discover -s tests -p "test_output*.py"` setelah fixture/assert baru dibuat; hasil sementara dibuka via server dan disk, keyboard, dark, mobile, font tidak ada, status campuran. Tidak menganggap screenshot reader lama sebagai hasil generator baru.

Dependensi: T02, T06, T10. Berkas: `simak/output.py`, `tests/test_output.py` (baru), fixture state yang sudah ada. Ukuran: M.

### T15 — Token shared terakhir tanpa runtime dependency baru

- [ ] Satukan aturan visual yang benar-benar berulang, bersihkan rule katalog/inline yang sudah tidak digunakan setelah migrasi.
- [ ] Tambahkan favikon lokal, judul halaman konsisten, alt aset, ukuran gambar untuk stabilitas; status dan kontrol tidak berubah makna.
- [ ] Tidak menyisakan placeholder booking, foto kucing, alamat/harga/testimoni fiktif, atau library motion template yang tidak digunakan.

Verifikasi: `rg` untuk pola/konten template yang tidak relevan dan selector tak terpakai; network offline baseline; console tidak berisi error tugas. Jangan melakukan refactor domain demi kebersihan kosmetik.

Dependensi: T05–T14. Berkas: `web/style.css`, `web/common.js`, satu favikon, file HTML yang memerlukan metadata (bila >5 berkas, pecah metadata menjadi patch terpisah). Ukuran: M.

### T16 — Lisensi dan aset final

- [ ] Notice MIT template dan OFL font yang benar-benar digunakan tersimpan sesuai distribusi.
- [ ] Aset demo inti lokal; data nyata/voice/key tidak masuk paket screenshot atau source.
- [ ] Rekam ukuran resource awal dan request eksternal; angka budget dilaporkan sebagai terukur atau belum terukur.

Verifikasi: inspeksi notices dan paket aset; buka tanpa jaringan pada data cache siap; pastikan suara eksternal opsional. Tidak menambahkan GSAP/Lenis hanya karena tersedia dalam template.

Dependensi: T02, T14–T15. Berkas: `THIRD_PARTY_NOTICES.md`, notice font, `tasks/evidence/resources.json`, dokumentasi paket bila perlu. Ukuran: M.

### Checkpoint 4 — Semua permukaan satu sistem

- [ ] Empat halaman aplikasi + reader punya identitas baru yang selaras; editor/reader tetap mudah dibaca.
- [ ] Denominator, provenance, hasil ditahan, dan seluruh batas evaluasi tidak hilang dalam penyederhanaan.
- [ ] Asset/CDN fallback dan file mandiri diverifikasi pada hasil aktual.

## Gelombang 4 — Finalisasi dan rehearsal (7–11 jam)

### T17 — Regression responsif, aksesibilitas, dan recovery

- [ ] Jalankan matriks viewport 1440,1366,1024,768,390,320 dan zoom 200/400% pada alur yang relevan.
- [ ] Uji keyboard/fokus/reduced-motion/status/live region/kontras seluruh warna dan kondisi; lakukan NVDA di mesin target jika tersedia, catat bila belum.
- [ ] Uji happy path dan failure yang tercantum pada plan; simpan screenshot dan temuan terpisah dari klaim lulus.

Verifikasi: semua unittest terfokus yang ditambahkan lulus via `python -m unittest discover -s tests -p "test_*.py"`; smoke browser nyata; satu ronde review desktop/mobile, batch fix, satu konfirmasi bagian terdampak. Jangan memperluas menjadi kalibrasi VLM atau evaluasi ilmiah penuh tanpa pemicu.

Dependensi: T05–T16. Berkas: test yang sudah ditambahkan, `tasks/evidence/final-review.json`, artefak screenshot dan daftar gap. Ukuran: M untuk pencatatan; setiap fix yang luas dipisah menjadi task kecil sesuai file terdampak.

### T18 — Dokumentasi desain dan operasi final

- [ ] Perbarui DESIGN.md + token sidecar/surface brief sesuai implementasi akhir, bukan gambar konsep.
- [ ] README menjelaskan startup satu worker, font/aset luring, query context, retensi yang nyata, dan fallback demo.
- [ ] Klarifikasi sumber run 12/23 Oktober pada PRODUCT/README tanpa mengubah angka evaluasi; batas penelitian tetap lengkap.

Verifikasi: dokumentasi cocok dengan source dan screenshot terakhir; tidak ada klaim implementasi/audio/NVDA/produksi yang belum dibuktikan. Jangan memperbaiki drift lain yang tidak relevan secara diam-diam.

Dependensi: T17. Berkas: `DESIGN.md`, `.impeccable/design.json`, surface brief terkait, `README.md`, `PRODUCT.md`. Ukuran: M.

### T19 — Rehearsal demo dan titik rollback

- [ ] Jalankan alur 15 menit dari plan pada laptop/proyektor target; pilih sampel/cache yang tersedia di model/schema aktif.
- [ ] Catat fallback audio/jaringan dan langkah membuka hasil siap; seluruh tindakan tetap nyata, bukan tombol dummy.
- [ ] Simpan baseline perubahan sesuai workflow Git proyek, tag/commit lokal hanya bila diotorisasi; rollback UI tidak menghapus state/keputusan pengguna.

Verifikasi: dua hasil demo/status terbaca pada proyektor; satu keputusan ULD sintetis mengubah hasil; dokumen unduhan bisa dibuka; tidak ada key/PDF nyata/suara berizin tak relevan di layar. Jika belum diuji pada perangkat target, status tetap "siap untuk rehearsal", bukan "demo tervalidasi".

Dependensi: T17–T18. Berkas: `tasks/demo-runbook.md`, `tasks/evidence/rehearsal.json`, daftar versi/cache. Ukuran: S.

### Checkpoint akhir

- [ ] Semua alur inti berfungsi dengan identitas baru dan evidence yang dibaca/review.
- [ ] Gap yang belum diuji ditulis jelas; tidak ada P1 terbuka pada penyimpanan keputusan atau alur demo utama.
- [ ] Hasil siap ditinjau pengguna; deployment/publikasi tetap pekerjaan terpisah bila diminta.

Belum dikerjakan: seluruh implementasi T01–T19. Risiko utama: perkiraan 35–58 jam dapat bertambah pada transaksi review, NVDA/audio, atau kendala mesin demo; animasi/dekorasi adalah bagian pertama yang dapat dikurangi.
