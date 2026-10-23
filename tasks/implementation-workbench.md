# Revisi visual halaman kerja

23 Oktober 2026. Sumber yang diedit: `Revisi Last/Prototype`, mengikuti pembaruan pengguna. Folder Prototype lama tidak ditimpa.

## Perubahan terbatas

- `web/workspace.css`: hierarki judul 32–52px dengan bobot lebih tenang, jarak kontrol yang jelas, perbandingan sejajar, transkrip yang nyaman dibaca dan tampilan hasil/review. Semua memakai font, palet dan komponen Sill yang sudah ada. Selector dibatasi ke halaman kerja atau `#hasil`.
- Empat HTML: tambahkan stylesheet halaman kerja, ringkas judul/petunjuk, tambahkan tiga langkah di demo. ID kontrol, urutan proses, keluaran, formulir dan handler tetap sama. Detail evaluasi, nilai dan batas pengujian tetap tersedia.
- `web/motion.js`: aktifkan `allowNestedScroll` Lenis, hapus pencegahan wheel berdasarkan kelas tabel/list/textarea. Region yang secara eksplisit memakai `data-lenis-prevent` tetap terisolasi. CSS nested scroll memakai `overscroll-behavior:auto` agar ujung daftar mengembalikan scroll ke halaman.
- Pengecualian kecil di landing sesuai laporan: hapus empat span `gate-art` yang menutup ilustrasi dan kembalikan opasitas gambar. Komposisi, tulisan, font, scene dan alur landing lainnya dipertahankan.
- Konfigurasi `.env.local` yang sudah tersedia dipakai lagi di folder terbaru, tanpa mencetak key atau menanamnya ke frontend. File ini tetap diabaikan Git.

## Alat dan pemeriksaan

Ponytail 5.3.2 dipasang dari marketplace repository resmi DietrichGebert/ponytail; skill-nya dibaca dan dipakai untuk membatasi perubahan. Frontend Design dipakai untuk hierarki visual. Microsoft `@playwright/test` dipasang sebagai alat pengembangan eksternal, tanpa dependensi runtime baru untuk aplikasi. Tidak mengaktifkan hook lifecycle tambahan pada sesi ini.

Reproduksi Playwright sebelum perbaikan: wheel 350px di atas tabel Evaluasi menghasilkan scrollY 297 → 297. Uji setelah perbaikan memeriksa perpindahan halaman di atas tabel/textarea, scroll internal transkrip dan handoff di ujung daftar, demo/injeksi/reset/angka sumber, proses materi sintetis, keluaran PDF/HTML, pemilihan review, menu/fokus, reduced motion serta empat halaman pada lebar 320/390/768/1440. Bukti di `tasks/evidence/workbench/after-browser.json` dan PNG terkait.

26 unit test Python dan tiga suite JavaScript lama lulus. Manifes hash memastikan seluruh backend, shared controls, speech dan scene landing tetap sama; script bisnis index/demo/dengar dibandingkan dengan versi awal dengan normalisasi newline Windows. Evaluasi hanya mengubah string tampilan.

Jalankan server dari folder ini dengan interpreter environment yang tersedia, misalnya port 8019 untuk berdampingan dengan instance lama. Jalankan browser regression:

```powershell
$env:SIMAK_PLAYWRIGHT='C:/Users/haqyb/.codex/tmp/simak-ui-check/node_modules/@playwright/test'
node tests/test_workspace.cjs
```

`SIMAK_TEST_URL` dapat mengganti alamat uji. Tes memakai materi sintetis lokal, membuat sesi contoh, dan tidak memutar audio berbayar. Tidak ada perubahan pada hasil evaluasi atau ambang gerbang. Belum melakukan pengujian NVDA/perangkat sentuh fisik baru.
