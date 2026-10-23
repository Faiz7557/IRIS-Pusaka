Reevaluasi progres prototipe SIMAK dan paper final ICC 2026 sejauh ini, menjelang pengumpulan 23 Oktober 2026 pukul 23.59 WIB dan presentasi final 28 Oktober 2026: apakah keduanya sudah siap dan cukup kuat untuk babak final?

## Konteks lomba (dari "Ketentuan Final ICC 2026.pdf")

- Innovation Case Competition 2026, Campus Data Week, Universitas Airlangga. 6 tim finalis; nilai semifinal tidak dihitung.
- Wajib: karya ilmiah Bab 1–5 (Bab 1–3 dari semifinal, boleh revisi minor; Bab 4 Hasil dan Pembahasan: hasil implementasi, pengujian dengan metrik Bab 3, pembahasan apakah rumusan masalah terjawab, keterbatasan; Bab 5 Penutup: kesimpulan, rencana pengembangan, dampak) dan demo MVP yang bisa dijalankan dan sesuai Bab 3. Topik dan rumusan masalah tidak boleh berubah.
- Demo palsu/direkayasa = pelanggaran berat. Similarity Turnitin < 15% (di luar kutipan dan pustaka), dilampirkan. Pernyataan penggunaan AI wajib di lampiran.
- Presentasi 15 menit termasuk demo + 15 menit tanya jawab, luring di Unair 28 Okt.
- Bobot penilaian: Hasil dan Demo/Prototipe 30%; Kelengkapan dan Konsistensi Karya Ilmiah 20%; Presentasi 20%; Tanya Jawab 20%; Inovasi dan Dampak 10% ("kebaruan ide dan manfaatnya untuk mahasiswa").
- Pengumpulan: PDF `[NamaTim]_ICC2026_Final` + link GitHub kode MVP.
- Koreksi dari pengguna: aturan pembatasan penulisan oleh AI dianulir untuk proyek ini; batas badan utama paper 20 halaman.

## Ide dan rumusan masalah (tetap dari semifinal)

Judul: "SIMAK: Remediasi Materi Kuliah Berbahasa Indonesia agar Dapat Disimak oleh Mahasiswa Tunanetra dan Pendengar dengan Gerbang Verifikasi". Tim "IRIS kata HQ ini lomba terakhir", 4 mahasiswa Universitas Airlangga.
- RM1: mengubah PDF materi kuliah berbahasa Indonesia menjadi dokumen berstruktur dengan urutan baca benar bagi pembaca layar.
- RM2: deskripsi grafik dan pembacaan rumus berbahasa Indonesia yang setia pada data sumber.
- RM3: alur kerja yang menahan keluaran tak terverifikasi dan menyerahkannya ke peninjau Unit Layanan Disabilitas (ULD) sehingga tidak ada deskripsi keliru terbit tanpa penanda.
Masalah: audit awal 28 PDF materi kuliah dari 18 kampus: 0/28 lulus PDF/UA-1; 29/1.111 elemen Figure pada dokumen bertag memiliki teks alternatif.

## Prototipe (folder `Final/Prototype`, repo publik github.com/Faiz7557/IRIS-Pusaka, tag v1.0-final = commit f73bfb1, sudah di-push)

- Aplikasi web lokal FastAPI. Halaman: Remediasi & Tinjauan (unggah PDF, katalog gambar, veraPDF B0/B1/D, antrean ULD setujui/ubah/tolak/dekoratif), Demo Gerbang (B2 vs SIMAK pada satu grafik, suntik 4 jenis kesalahan), Evaluasi, Dengar, keluaran HTML dengan penanda status dan mode dengar Web Speech API id-ID (ElevenLabs opsional).
- Pipeline: OpenDataLoader auto-tag + tambalan pikepdf/PyMuPDF (Lang, Title, TH, penanda PDF/UA), veraPDF 1.30.3; VLM Gemma 4 26B-A4B lewat Gemini API suhu 0; ekstraksi tabel data dua kali (T1, T2 = model sama, dua perintah, karena kuota free tier); statistik (maks, min, selisih, rerata, tren) dihitung kode; deskripsi murni templat; gerbang fail-closed K = {cF, cδ, cA, cL}; respons VLM di-cache sehingga demo bisa luring.
- Realisasi fitur (Tabel 9 paper): jalan CLS-01, CHT-01, GAT-01, OUT-01, OUT-02, REV-01; sebagian STR-01 (cadangan tabel PyMuPDF bukan Docling; tabel cadangan belum Table/TH di PDF), CHT-02 (tanpa VLM penyunting); belum FRM-01 dan FRM-02 (semua rumus ditahan, MathCAT belum ada).
- Figur vektor belum dideskripsikan dan belum tampil sebagai kartu di antrean UI. Dekoratif belum ditandai Artifact.

## Hasil evaluasi (eval/results.json run 2, 23 Okt; run 1 12 Okt identik, 0/60 status berbeda)

Set uji tertahan sintetis buatan tim: 60 grafik, 4 dokumen 3 halaman, seed 20260930; ambang dikunci 12 Okt pada 30 grafik dev sebelum set uji dibuka (θe 0,01; ε 0,02; ρ 0,10).
- G1: D 4/4 [0,510; 1,000]; B0, B1 0/4. veraPDF aturan gagal B0 6 → B1 5 → D 0. G1-ketat (penanda tahan dihitung belum bermakna) D 0/4.
- G3: D terbit 40/60; Fk klaim terbit 440/440 [0,991; 1,000]; injeksi tertahan 137/138 [0,960; 0,999] (lolos 1: tukar label di bawah toleransi ε·s). Semua 40 grafik terbit berlabel nilai; semua 20 ditahan tanpa label nilai (cL). Klaim D pada grafik yang ditahan: 205/222 setia; 6/20 grafik ditahan memuat klaim keliru.
- B2 (VLM langsung tanpa gerbang, model sama): terbit 60/60; 17 angka ditandai keliru pada 7/60 grafik; audit manual: 13 pembulatan di luar ε (grafik tanpa label), 3 rerata dihitung model keliru, 1 salah tandai.
- G4: Q(D) 1,00 (80/80); Q(B2) 0,99; penanya/penjawab model sama, pertanyaan dari tabel.
- G6 ringan: 6 PDF nyata ac.id dari Common Crawl (ternyata RPS, module handbook, SOP, pengumuman, bukan materi kuliah; tanpa grafik raster): G1 D 6/6, veraPDF penuh D 2/6, beban tinjauan R 18/18 (0 grafik terbit; 15/18 figur vektor).
- G2 (urutan baca), G5 (rumus), G7 (uji pengguna tunanetra/ULD) tidak dijalankan; G6 penuh (60 dokumen, kappa, NVDA) belum.
- Waktu proses: dokumen uji 29,9–43,9 dtk; PDF nyata 6,5–43,0 dtk; dengan cache ±7,6 dtk.

## Paper (Final/Paper)

- Berkas: `IRIS kata HQ ini lomba terakhir_ICC2026_Final.docx`; pratinjau render `PRATINJAU_naskah_final.pdf` (50 halaman total; badan utama 17 halaman, Lampiran A di hlm. 18; Lampiran H–P berisi data reproduksi, selang Wilson, hasil per grafik, injeksi, audit B2, kalibrasi, G6, rencana vs realisasi data, galeri UI).
- Bab IV dan V, abstrak baru, revisi Bab I–III sesuai komentar, dan Lampiran A ditulis hari ini (23 Okt) dengan bantuan Claude dari angka evaluasi; Lampiran A menyatakan penggunaan itu. Tim belum membaca ulang teks tersebut.
- Status per RM yang ditulis di paper: RM1 terjawab sebagian; RM2 terjawab untuk grafik pada data sintetis, rumus belum; RM3 terjawab untuk grafik pada set uji.
- Pemeriksa otomatis `cek_naskah.py`: semua pecahan/desimal di Abstrak dan Bab IV–V cocok dengan data; rujukan 56 entri tanpa yatim.
- Belum selesai saat ini (±14.30 WIB, 23 Okt): laporan Turnitin final untuk Lampiran B (belum dicek), pembacaan ulang oleh tim, ekspor PDF final dari Word, unggah (target 21.00).
- Rencana penulisan awal menargetkan set data 150 grafik, 30 dokumen, 200 rumus, sampel 600 PDF bingkai Common Crawl, dan benchmark publik; realisasinya lebih kecil (Lampiran O).

Semua berkas di atas dapat dibuka langsung dari folder kerja `C:\Uner\Lomba\Campus Data Week\Final` (subfolder `Prototype` dan `Paper`) bila perlu memeriksa bukti.
