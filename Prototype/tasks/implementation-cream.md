# Hasil implementasi SIMAK — cream

23 Oktober 2026. Ruang lingkup: aplikasi lokal, empat halaman web, reader HTML, voice, ketahanan proses, dokumentasi dan verifikasi. Dokumen paper dan angka evaluasi ilmiah tidak diubah.

## Perubahan

- Latar utama dan header cream `#f6efdf`, permukaan baca `#fffaf0`. Panel oranye, violet, sage dan taupe tetap menjadi identitas. Footer dan popup perintah suara memiliki warna teks yang sesuai latar terang.
- Pemutar bersama `web/speech.js` dipakai aplikasi dan ditanam ke HTML hasil. ElevenLabs menjadi pilihan awal saat server dikonfigurasi; pilihan peramban yang sengaja disimpan pengguna dihormati. HTML dari disk memakai suara peramban.
- Teks panjang dipotong maksimal 2.400 karakter per bagian, dengan batas kalimat bila tersedia. Pembatalan menghentikan sisa bagian dan respons lama tidak boleh memulai audio baru. Error media dan penolakan play membebaskan object URL.
- Key/voice dimuat dari `.env.local` di server, tanpa menaruhnya pada frontend. File rahasia, environment dan audio cache diabaikan Git; `.env.example` tersedia.
- Cache MP3 diterbitkan setelah unduhan berhasil melalui penggantian atomik. Pesan kegagalan layanan memberi tindakan yang bisa dilakukan tanpa meneruskan respons mentah penyedia.
- Kode OpenVoice/edge-tts yang tidak dipanggil aplikasi dihapus dari modul voice aktif. Berkas requirements suara lama tetap arsip terpisah.
- Error respons VLM/jaringan yang lolos setelah retry menahan gambar, sehingga elemen lain tetap dapat diproses. Retry dibatasi secara default empat percobaan; maksimum enam melalui `SIMAK_VLM_ATTEMPTS`.
- Ringkasan Evaluasi menjadi satu kolom pada layar sangat sempit agar angka tidak menyebabkan overflow. Fokus file picker diberi outline terlihat.
- Startup tersedia melalui `run.ps1`; notice template dan font tersedia lokal.

## Bukti

| Pemeriksaan | Hasil |
|---|---|
| Tes Python | 18 lulus: reader, review/transaksi, upload, voice dan hold saat respons VLM rusak |
| Regresi frontend | Lulus: stale polling, start ganda, offline recovery, kontrol player tetap dan empty state |
| Regresi pemutar bersama | Lulus: default ElevenLabs, preferensi eksplisit, teks panjang, fallback file, cancel, respons terlambat, penolakan play |
| ElevenLabs live | Teks pendek menghasilkan HTTP 200 audio/mpeg, 71.514 byte; audio tersimpan lokal pada cache |
| Coba suara di browser | Request berhasil HTTP 200; UI kembali ke status siap sesudah pemutaran |
| Empat halaman | HTTP 200 |
| Demo dari cache | 60/60 dijalankan HTTP 200, tanpa VLM live |
| Empat injeksi syn043 | Semua menjadi antrean; tukar label juga diperiksa lewat UI |
| materi_01 lewat UI | Selesai: 3 terbit, 2 antrean, 2 dekoratif; satu keputusan ubah disimpan dan terlihat di Dengar |
| materi_03 smoke | Selesai: 2 terbit, 3 antrean, 2 dekoratif sebelum review; B0/B1/D = 6/5/0 aturan gagal; D compliant=true |
| Review smoke | State diubah, versi baru diterbitkan; teks baru ditemukan pada HTML dan alt PDF |
| Tampilan | Empat halaman dan reader diperiksa pada enam target lebar; ukuran CSS aktual dicatat pada JSON |
| Bug 320 px | Evaluasi semula overflow 356 px; setelah fix scrollWidth = clientWidth = 320 |

Artefak: [smoke.json](evidence/cream/smoke.json), [final-viewport-checks.json](evidence/cream/final-viewport-checks.json), screenshot di `evidence/cream/`, tes di `tests/`, dan [panduan demo](demo-runbook.md).

## Batas pengujian

- Matriks akhir berisi 30 pemeriksaan pada lima permukaan, dengan target 1440/1366/1024/768/390/320 px. Beberapa ukuran CSS aktual berbeda 1 px dari target; 320 dan 390 px terukur tepat. Seluruh konfirmasi akhir tidak memiliki overflow halaman. Ukuran aktual dicatat pada final-viewport-checks.json.
- NVDA, perangkat sentuh fisik, proyektor target, zoom 200/400%, dan pergantian tema OS reader belum diuji. Pemeriksaan ini bukan sertifikasi WCAG atau pengujian dengan mahasiswa tunanetra.
- Tidak menjalankan ulang kalibrasi atau eksperimen penelitian penuh. Cache/demo smoke berbeda dari bukti independensi VLM dan generalisasi dokumen nyata.
- Penguncian review dan pembatasan proses tetap untuk satu worker. Retensi tetap manual melalui Hapus sesi.
- Rumus/vektor yang belum terverifikasi tetap ditahan. Batas PDF pada halaman campuran tetap berlaku.
- Snapshot proyek ini tidak memiliki metadata Git; tidak ada commit/tag/PR baru. Sesi pengguna lama tidak dirakit ulang massal atau dihapus.

## Kondisi operasi

Jalankan `./run.ps1` dari folder Prototype, lalu buka `http://127.0.0.1:8017`. Environment `.venv` sudah disiapkan pada mesin ini. Gunakan satu proses server; jangan menyalakan server kedua pada port yang sama.

Environment yang disiapkan memakai paket sistem sebagai dasar. Tes proyek lulus; ini tidak menjadi klaim instalasi bersih tanpa paket sistem.

Port instance hasil akhir: **8017**, untuk menghindari benturan dengan aplikasi lain pada port 8000. Server berjalan tersembunyi; log dan PID ada di `work/cream-server.*`. `run.ps1` memakai 8017 secara default atau menerima `-Port`.

Pengecekan warna akhir: tinta/cream 17,26:1; teks sekunder/cream 7,39:1. Pasangan lama teks metadata/sage dan tombol hapus/taupe diganti dengan tinta gelap dan latar blush. Detail ada di `contrast.json`. Verifikasi akhir dan ukuran aset ada di `final-review.json` dan `verification.json`.
