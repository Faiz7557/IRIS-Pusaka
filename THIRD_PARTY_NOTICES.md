# Aset dan dependensi antarmuka

Komposisi, stylesheet bagian dan scene motion diadaptasi dari template Sill (8B), yang disertakan pengguna sebagai `Template UI.zip`. Notice MIT asli tersedia di [third_party/sill/LICENSE](third_party/sill/LICENSE). Foto, teks bisnis, dan formulir booking tidak digunakan. Ilustrasi dokumen, data dan audio adalah SVG yang dibuat untuk SIMAK.

Library di-host lokal pada `web/vendor/`, dengan versi yang sama seperti template:

- GSAP, ScrollTrigger, SplitText **3.13.0**: Copyright 2025 GreenSock; header lisensi asli dipertahankan. [Standard no-charge license](https://gsap.com/standard-license/), juga dicatat pada `third_party/gsap/NOTICE.md`.
- Lenis **1.3.27**: Copyright darkroom.engineering, [MIT](third_party/lenis/LICENSE).

Font di-host lokal pada `web/fonts/`:

- Gabarito: `Gabarito-OFL.txt`.
- Rethink Sans: `RethinkSans-OFL.txt`.
- Atkinson Hyperlegible Next: `AtkinsonHyperlegibleNext-OFL.txt`.
- Atkinson Hyperlegible Mono: `AtkinsonHyperlegibleMono-OFL.txt`.

Ikon antarmuka adalah SVG inline dari source aplikasi. HTML hasil menanam font Next dan gambar dokumen secara langsung. Voice ElevenLabs adalah layanan eksternal yang diakses server hanya saat pengguna meminta pemutaran; file audio cache dan konfigurasi rahasia tidak dimasukkan source control.
