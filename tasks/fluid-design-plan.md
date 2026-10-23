# SIMAK — alur visual Sill

Arahan 23 Oktober 2026: adaptasi menyeluruh komposisi, urutan cerita dan motion template Sill; latar cream tetap berlaku. Seluruh fungsi aplikasi dipertahankan.

## Konsep

Materi kuliah bergerak dari halaman menjadi pemahaman: dokumen, data, keputusan, suara. Pembuka merupakan komposisi lima panel Sill dengan ilustrasi materi besar; perjalanan berikutnya memperkenalkan bentuk keluaran, proses, verifikasi dan ruang kerja. Area kerja tetap tenang agar keputusan dapat diperiksa.

Palet inti: cream `#f6efdf`, tinta `#0b0a0a`, oranye `#cf6224`, violet `#5a3cd4`, sage `#80a89b`, taupe `#bca59d`. Mustard, maroon dan mauve dari template hanya sebagai panel pendukung; warna status tetap semantik. Rethink Sans untuk teks/antarmuka, Gabarito untuk headline, Atkinson untuk reader dan nilai bukti.

Tata letak rata kiri dan headline besar seperti template. Tidak mengubah semua area menjadi kartu seragam. Caption dan kontrol tetap ringkas; rincian teknis masuk disclosure yang tetap bisa diakses keyboard.

```text
Header: SIMAK / Jelajahi / Dengar / Demo / Bukti / Mulai

[ Headline oranye                   ][ Ilustrasi materi ]
[ Manfaat violet ][ Mulai taupe ][ Audio maroon        ]
                ~ peralihan bukit cream ~
[ Pengantar ][ dua belas jendela materi                 ]

Panel fitur mengembang → contoh keluaran → proses horizontal
Empat gerbang → enam potongan visual menyatu → langkah ULD
Empat prinsip → FAQ → form remediasi → wordmark besar
```

## Pemetaan motion

| Sill | Adaptasi SIMAK |
|---|---|
| Lenis + GSAP ticker | Scroll lembut; area editor/list dikecualikan agar gulirnya tetap lokal |
| Nav hilang/muncul menurut arah scroll | Header cream; menu mobile panel warna dan fokus terkelola |
| Opening: lima panel, hill, curl, 12 windows | Lima panel manfaat/aksi/ilustrasi dan 12 jendela materi; CTA tetap langsung menuju form |
| Rooms: panel clip-path, judul berputar | Tiga bentuk akses: baca, dengar, telusuri |
| Letters: peek + curl + heading line mask | Contoh isi dan keputusan; tidak membuat testimoni fiktif |
| Day: pinned horizontal rail, sky/disc | Enam tahap dari PDF sampai keluaran |
| Sitters: empat podium | Empat pemeriksaan grafik |
| Courtyard: enam panes dan tint | Potongan dokumen menyatu menjadi satu keluaran |
| Visit: empat langkah bertingkat | Pilih, proses, tinjau, bagikan |
| Quiet: panel miring, menyatu dan berubah warna | Prinsip publikasi yang bisa dipercaya |
| Contact: panel mengapit form dari empat sisi | Form unggah SIMAK yang sesungguhnya, bukan form demo |
| Footer besar | Wordmark SIMAK dan navigasi fungsi |

Perpindahan halaman menggunakan transisi dokumen browser bila didukung, dengan masuk halaman yang terorkestrasi sebagai fallback. Form, editor dan state hasil tidak dipindahkan lewat router baru. Motion berjalan setelah font/DOM siap; perubahan hasil memperbarui layout dan membersihkan scene tersembunyi. Reduced motion menampilkan isi lengkap tanpa pin/smooth scroll.

## Tinjauan sebelum implementasi

Arah ini memakai perilaku template yang memang diminta, bukan sekadar recolor atau fade-up berulang. Ilustrasi dibuat dari bentuk dokumen/grafik/audio yang relevan dengan SIMAK; tidak perlu foto stok atau foto pengguna. Statistik dan batas kemampuan tetap faktual. Implementasi tidak menambah klaim aksesibilitas universal maupun testimoni pengguna.

## Verifikasi

Tes regresi domain yang ada, semua kontrol inti, scroll maju/mundur pada scene utama, tab desktop/menu mobile, viewport 320–1440, reduced motion, browser tanpa library, HTML reader mandiri, dan tidak ada key pada aset publik. Screenshot pembuka dan beberapa posisi scroll menjadi bukti komposisi dan motion.
