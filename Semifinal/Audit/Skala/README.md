# Audit skala besar dan data pengembangan prototipe SIMAK

Semua langkah memakai data publik. Berkas PDF tidak disebarluaskan; yang dilaporkan hanya metadata, struktur, dan hitungan agregat.

| Langkah | Skrip | Keluaran | Dipakai untuk prototipe |
|---|---|---|---|
| 1 | `01_bingkai_cc.py CC-MAIN-2026-39` | `bingkai_*.parquet` (bingkai sampel dari indeks Common Crawl: PDF pada domain ac.id; kolom bahasa indeks kosong untuk PDF, bahasa ditentukan setelah unduh) dan `frame_stats.json` | ukuran bingkai; dasar sampel acak |
| 2 | `02_sampel_unduh.py bingkai_*.parquet 800` | `unduhan/`, `manifest_sampel.csv` (kolom `set` = dev atau uji, per domain 2:1) | dokumen pengembangan dan uji tertahan |
| 3 | `03_audit_pdf.py unduhan hasil_audit.csv` | metadata, bertag, teks alternatif, TH, bahasa, veraPDF PDF/UA-1 | daftar aturan gagal terbanyak = prioritas aturan tambal (OUT-01, STR-01) |
| 4 | `04_analisis.py hasil_audit.csv manifest_sampel.csv` | proporsi, selang Wilson, bootstrap klaster per domain | angka Tabel I naskah; estimasi efek desain |
| 5 | `05_ekspor_gambar_label.py manifest_sampel.csv 200 100` | `label_gambar/`, `label_gambar.csv` | data berlabel untuk CLS-01 (ambang heuristik dan perintah zero-shot) |

Aturan pemakaian: menyetel komponen hanya dengan set `dev`; set `uji` dibuka sekali setelah versi dibekukan (jadwal 20–22 Oktober). Seed 20260930; maksimum 12 dokumen per domain. Tangkapan yang terpotong tidak diunduh ulang dari server kampus (dilengkapi dari korpus SafeDocs).
