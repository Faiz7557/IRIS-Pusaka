# Status pekerjaan SIMAK — cream

23 Oktober 2026. Implementasi inti selesai dan diuji lokal. Bukti terperinci: [implementation-cream.md](implementation-cream.md). Rencana lama di plan.md adalah arsip arah awal, bukan status pekerjaan saat ini.

| ID | Implementasi/status | Bukti atau batas |
|---|---|---|
| T01 | Fixture sintetis dan smoke tersedia | tests/fixtures; smoke_cream.py. Baseline sebelum cream tidak direkam ulang. |
| T02 | Token cream, panel dan font lokal selesai | style.css, fonts.css, DESIGN.md |
| T03–T04 | Header dan empat halaman selesai | Navigasi/job context diperiksa di browser |
| T05 | Demo lengkap tetap berfungsi | 60/60 grafik cache; empat injeksi; screenshot |
| T06 | Dengar dan pemutar bersama selesai | Voice live HTTP 200; player regresi dan browser |
| T07 | Konteks dokumen selesai | Remediasi → Dengar membawa keputusan hasil uji |
| T08 | Unggah/progres dan recovery tersedia | Tes boundary/stale poll/start ganda/offline |
| T09 | Review konsisten pada satu proses | Tes konkurensi, assembly gagal, pointer gagal dan versi lama |
| T10 | Editor/antrean selesai | Ubah dan simpan lewat UI; PDF/HTML diperiksa pada smoke |
| T11 | Batas file dan copy sesuai kemampuan | 20 MiB, 200 halaman, retensi manual; VLM error menjadi tahan |
| T12 | Hapus sesi memiliki konfirmasi/recovery | Source dan tes active-job; tidak menghapus sesi pengguna |
| T13 | Evaluasi bertingkat selesai | Tujuh tabel, denominator/CI, G1 ketat, G6 dan batas |
| T14 | Reader mandiri dan identitas selesai | Semantik/provenance diuji; embed speech; fallback file diuji melalui regresi |
| T15 | Token/metadata/favikon lokal tersedia | Empat halaman dan reader memakai identitas sama |
| T16 | Notice/aset lokal selesai | THIRD_PARTY_NOTICES.md dan third_party/sill/LICENSE |
| T17 | Regresi lokal lulus; uji manual tertentu tersisa | 18 Python, dua suite Node, browser desktop/mobile; NVDA/zoom/tema OS belum diuji |
| T18 | Dokumentasi final diperbarui | DESIGN/README/PRODUCT, sidecar dan catatan implementasi |
| T19 | Runbook dan rehearsal lokal tersedia | Proyektor/laptop target perlu rehearsal tim; metadata Git tidak tersedia sehingga tidak membuat commit/tag |

## Tambahan yang sudah diselesaikan

- ElevenLabs memakai key/voice pengguna melalui .env.local yang diabaikan Git.
- Pilihan voice sama pada aplikasi dan HTML hasil; preference eksplisit peramban dihormati.
- Chunk teks panjang, cancel, stale audio, play error, cache audio atomik dan pesan pemulihan.
- Popup voice dan footer memiliki kontras sesuai cream; file picker mendapat fokus terlihat.
- Overflow Evaluasi pada 320px diperbaiki dan dikonfirmasi ulang.

## Verifikasi manual pada perangkat presentasi

- [ ] NVDA dan pengalaman pengguna pembaca layar.
- [ ] Proyektor, volume/speaker, perangkat sentuh fisik.
- [ ] Zoom 200/400% dan perubahan tema OS reader.

Keterbatasan penelitian (MathCAT, ekstraksi figur vektor, evaluasi G2/G5/G6 penuh/G7) tetap dicatat; bukan fitur yang diklaim selesai oleh pekerjaan UI ini.
