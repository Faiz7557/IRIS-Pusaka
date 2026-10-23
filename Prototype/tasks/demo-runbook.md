# Panduan demo SIMAK — 15 menit

## Sebelum presentasi

1. Buka PowerShell di `Prototype`, jalankan `./run.ps1`. Bila port sudah dipakai oleh SIMAK, gunakan instance itu.
   Pembuka visual: `http://localhost:8017/?jelajah=1#opening`; CTA **Mulai dari PDF** langsung menuju formulir. Preferensi reduced motion sistem menampilkan halaman tanpa pin/scroll lembut.
2. Buka halaman Remediasi, Dengar, Demo Gerbang, dan Evaluasi. Key tidak perlu ditampilkan di terminal/layar.
3. Pastikan `/api/suara/daftar` menawarkan ElevenLabs. Gunakan Coba suara satu kali, atur volume perangkat, lalu hentikan audio sebelum berpindah halaman.
4. Pilih `materi_01.pdf` untuk cerita sebelum/sesudah dan `syn043` untuk demo gerbang. Respons VLM contoh tersedia dari cache. Pastikan veraPDF 1.30.3 dapat dijalankan.
5. Siapkan satu hasil PDF/HTML sintetis yang sudah selesai. Jangan memakai job ID lama sebagai dependensi permanen.

## Urutan

| Menit | Tindakan dan pokok penjelasan |
|---|---|
| 0–3 | Dengar: pilih materi_01, bandingkan “Gambar.” dengan deskripsi lengkap. Jelaskan bahwa versi asli adalah simulasi transkrip, bukan rekaman NVDA. |
| 3–7 | Demo Gerbang: pilih syn043, jalankan, tunjukkan sumber grafik dan dua keputusan. Suntik tukar label; B2 tetap terbit, SIMAK ditahan. Klik angka klaim untuk menyorot tabel sumber. |
| 7–11 | Remediasi: tampilkan hasil PDF, sisa antrean dan G1 ketat. Pilih diagram sintetis, sunting deskripsi, simpan, lalu tunjukkan perubahan pada reader. Jangan menyebut keputusan manusia sebagai verifikasi otomatis. |
| 11–14 | Evaluasi: jelaskan 440/440 pada set sintetis, 20/60 grafik butuh tinjauan, 137/138 injeksi ditahan, serta batas G6. Bedakan validasi teknis PDF dari kelengkapan deskripsi. |
| 14–15 | Tutup dengan keluaran PDF/HTML dan batas implementasi yang masih memerlukan tinjauan manusia. |

## Cadangan

- Tanpa ElevenLabs/jaringan: pilih Peramban (id-ID); teks tetap tersedia. Kualitas/ketersediaan suara mengikuti perangkat.
- Tanpa key VLM: contoh cache tetap berjalan; cache miss ditahan dengan alasan.
- Proses belum selesai: buka hasil sintetis yang telah disiapkan. Tampilkan status nyata, bukan mengklaim hasil yang belum selesai.
- Gangguan review: draf tetap ada dalam tab; Periksa status penyimpanan sebelum mengirim ulang keputusan ketika statusnya ambigu.
- File HTML yang dibuka dari disk memakai suara peramban; ElevenLabs memerlukan server SIMAK.

Rehearsal pada mesin lokal sudah mencakup proses, demo, review dan Dengar. Rehearsal dengan proyektor/NVDA pada perangkat presentasi masih perlu dilakukan tim.
