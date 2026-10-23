# SIMAK — alur visual Sill pada cream

Implementasi 23 Oktober 2026. Acuan visual: template Sill milik 8B. Arahan pengguna: latar utama cream.

## Warna dan hierarki

| Peran | Nilai |
|---|---|
| Latar halaman/header | #f6efdf |
| Kertas/kartu | #fffaf0 |
| Tinta utama | #0b0a0a |
| Teks sekunder | #514c49 |
| Panel utama | #cf6224 |
| Panel pembanding/contoh | #5a3cd4 |
| Panel langkah/hasil SIMAK | #80a89b |
| Toolbar/keluaran | #bca59d |
| Terbit | #185c3a pada #e4f2e9 |
| Ditahan | #624000 pada #fff0c2 |
| Gagal/ditolak | #a51d2d pada #fce6e8 |
| Fokus | #1457c5 |

Panel oranye menggunakan teks gelap. Violet menggunakan teks kertas terang. Warna status terpisah dari warna panel dan selalu disertai kata/ikon. Latar halaman, sela panel, dan header mengikuti cream; tombol utama menggunakan tinta gelap.

## Tipografi dan komposisi

Gabarito untuk judul dan angka besar; Rethink Sans untuk teks/antarmuka seperti template; Atkinson Hyperlegible Next untuk reader dan Atkinson Hyperlegible Mono untuk nilai yang diperiksa. Seluruh font lokal dengan OFL. Root 18px, kontrol minimal 44px, panel datar dan tajam.

Header mengikuti arah scroll dan membawa empat halaman; layar kecil memakai menu panel warna dengan focus trap, Escape dan pemulihan fokus. Lebar area kerja maksimum 1600px. Pengantar memakai komposisi penuh Sill: lima panel, 12 jendela, fitur, contoh, proses, gerbang, enam potongan dokumen, langkah ULD, prinsip, FAQ dan unggah. Pembuka diringkas menjadi “Materi kuliah, untuk semua.” Layout menyesuaikan layar kecil; tabel menggulir dalam regionnya sendiri.

Remediasi memprioritaskan unggah, lalu hasil dan sisa antrean. Demo menempatkan grafik sumber dekat kontrol dan keputusan. Dengar menyebut simulasi dekat judul dan menyediakan teks lengkap. Evaluasi menampilkan dataset, beban tinjauan, G1 ketat, serta batas hasil.

## Interaksi

- Status: otomatis, antrean, disetujui, diubah, ditolak, dekoratif. Provenance manusia dan otomatis tetap berbeda.
- Angka klaim dapat difokuskan/dipilih untuk menyorot baris sumber.
- Review mempertahankan draf dan menangani status simpan ambigu; publikasi memakai versi PDF/HTML/state.
- Job dibawa antarhalaman melalui query/sessionStorage; dokumen tidak disimpan pada localStorage.
- Satu modul speech menangani default ElevenLabs, preferensi suara, chunk teks, pembatalan dan error untuk aplikasi serta reader.
- Reader menanam gambar, font dan script; mode file menggunakan suara peramban. Reader light memakai cream; preferensi dark OS tetap didukung.
- GSAP/ScrollTrigger/SplitText 3.13.0 dan Lenis 1.3.27 lokal, sama dengan template. Semua scene sumber diadaptasi, dengan hill cream menggantikan hitam dan SVG materi menggantikan foto hewan.
- Fokus keyboard terlihat dan skip link tersedia. Reduced motion mematikan smooth scroll, pin dan reveal; konten tetap terlihat bila library gagal. Scroll lokal editor/list tidak diambil alih Lenis.
- Perpindahan halaman memakai native cross-document View Transitions bila browser mendukung; browser lain memakai masuk heading/panel. Sesi/form tetap mengikuti navigasi biasa. Scene dilepas ketika hasil muncul dan dibangun ulang saat kembali ke unggah.

## Bukti dan batas

Lihat tasks/implementation-fluid.md dan tasks/evidence/fluid/, serta bukti sebelumnya di tasks/evidence/cream/. Ini bukan sertifikasi WCAG. NVDA, proyektor, perangkat sentuh fisik, zoom 200/400% dan perubahan tema OS reader belum diverifikasi.
