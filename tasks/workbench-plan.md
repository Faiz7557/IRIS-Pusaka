# Revisi halaman kerja — 23 Oktober 2026

Sumber aktif hanya Revisi Last/Prototype. Pertahankan landing, backend, API, sesi, ID kontrol, fungsi review, pemutar, injeksi dan angka evaluasi. Pengecualian landing: hapus empat span gate-art yang dilaporkan menutup gambar; tidak mengubah scene/komposisinya.

Palet tetap: cream #f6efdf, kertas #fffaf0, tinta #0b0a0a, oranye #cf6224, violet #5a3cd4, sage #80a89b. Gabarito untuk judul 36–48px, Rethink Sans untuk teks; kurangi bobot/kerapatan dan metafora pada halaman kerja. Font serta aset yang sudah ada dipakai kembali.

Demo: [judul + tiga langkah] [grafik sumber], kontrol terkelompok, dua keputusan sejajar, lalu tabel/skor. Dengar: judul tugas, pilihan dokumen/suara, perbandingan dan transkrip dengan header pemutar yang jelas. Evaluasi: judul langsung, ringkasan ukuran dengan label konkret, detail uji dan keterbatasan. Hasil remediasi: keluaran/status di atas, daftar tinjauan dan editor di bawah. Semua rata kiri, tanpa penambahan metrik atau alur baru.

Perbaikan scroll harus pada penyebab bersama di motion.js: gunakan nested scroll bawaan Lenis, jangan menahan wheel pada seluruh leluhur tabel/list yang tidak mempunyai overflow. Uji bagian tengah/padding tabel, tepi list, ujung list serta textarea. Menu yang terbuka tetap sengaja menahan halaman di belakangnya.

Tinjauan: halaman kerja membutuhkan petunjuk tindakan, bukan hero promosi tambahan. Pertahankan panel warna dan bentuk template; jangan mengganti semua tampilan menjadi kartu baru. Ponytail digunakan untuk membatasi perubahan; Playwright resmi untuk reproduksi dan verifikasi browser. Tes lama dan pemeriksaan bahwa script bisnis/backend tidak berubah melengkapi screenshot desktop/mobile.
