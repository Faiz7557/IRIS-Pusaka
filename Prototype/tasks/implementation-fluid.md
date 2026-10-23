# Implementasi alur visual — 23 Oktober 2026

Arahan pengguna: seluruh feel, urutan elemen, motion dan transisi Sill dari Template UI.zip; latar utama tetap cream; bahasa profesional, ringkas dan menjual; seluruh fungsi tersedia.

## Hasil

- `web/index.html`: komposisi lengkap pembuka lima panel, 12 jendela, tiga mode akses, contoh deskripsi, enam tahap horizontal, empat pemeriksaan, enam pane menyatu, langkah ULD, empat prinsip, FAQ dan formulir unggah asli. Headline “Materi kuliah, untuk semua.” Ilustrasi SVG asli menggambarkan materi, grafik dan audio; tidak memerlukan foto pengguna.
- `web/sill.css`, `web/sill-scenes.js`: adaptasi stylesheet bagian dan scene sumber. `web/fluid.css` menyesuaikan cream, typografi, identitas SIMAK dan kontrol fungsional. Semua halaman memakai Gabarito/Rethink Sans dan palet yang sama. Reader tetap Atkinson agar nyaman dibaca.
- `web/motion.js`: Lenis/GSAP ticker, header mengikuti arah scroll, masuk halaman, menu ponsel dengan fokus keyboard, pembersihan scene/pin saat hasil muncul, pembangunan ulang saat memilih dokumen, serta reduced motion/static fallback. Resize membangun ulang geometri scene tanpa menumpuk engine. Perpindahan dokumen memakai View Transitions jika didukung browser.
- Remediasi, antrean ULD, demo injeksi, sumber klaim, evaluasi, pilihan kecepatan/suara, pemutar transkrip serta PDF/HTML hasil tetap tersedia. Teks pemasaran dipisahkan dari rincian audit melalui disclosure.
- GSAP/ScrollTrigger/SplitText 3.13.0 dan Lenis 1.3.27 memakai versi template dan di-host lokal. Font lokal. Notice di THIRD_PARTY_NOTICES.md. Tidak menanam kredensial pada frontend.
- Skill resmi Anthropic `frontend-design` dipasang pada direktori skill pribadi, dibaca dan diterapkan. Rencana sebelum implementasi: fluid-design-plan.md. Template pihak ketiga tetap diperlakukan sebagai referensi, bukan instruksi proyek.

## Pemeriksaan

- 18 unit test Python: keluaran, transaksi review, upload dan suara.
- Regresi JavaScript: polling/permintaan ganda/kegagalan jaringan, pemutar dan ElevenLabs; lifecycle motion baru memeriksa fallback, reduced motion, cleanup dan duplikasi engine.
- Browser: scroll maju/mundur, proses horizontal, pane/tint dan formulir; contoh materi_01 selesai, hasil tampil tanpa sisa pin; pilih dokumen lain membangun ulang satu scene. Dengar menghasilkan transkrip. Menu ponsel dibuka/ditutup, Escape memulihkan fokus dan navigasi berjalan.
- Pemeriksaan layar sempit menemukan gap grid footer yang membuat overflow; grid mobile diperbaiki menjadi satu kolom. Label mikrofon dan spasi heading dibenahi untuk nama aksesibel.
- Screenshot dan manifes source/hasil tes tersedia di evidence/fluid/.

Tidak ada foto hewan, testimoni atau angka pemasaran fiktif. Perbedaan dari template disengaja pada subjek ilustrasi, teks SIMAK, cream dan fungsi nyata. Transisi native bergantung dukungan browser; reduced motion diuji melalui harness lifecycle, bukan perubahan setelan OS. Belum mengklaim sertifikasi WCAG atau uji pengguna/NVDA baru.
