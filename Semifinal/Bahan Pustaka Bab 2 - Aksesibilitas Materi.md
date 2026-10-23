# Bahan Pustaka Bab 2: Aksesibilitas Materi Kuliah bagi Mahasiswa Tunanetra

Catatan penelusuran awal pustaka, dibantu AI (Claude). Isinya ringkasan faktual dari sumber, bukan narasi paper.
Wajib dilakukan tim sebelum dipakai: buka dan baca sendiri tiap sumber, cek ulang angka yang dikutip, lengkapi data bibliografi yang bertanda [LENGKAPI].
Format sitasi mengikuti template (IEEE, angka dalam kurung siku). Nomor di sini hanya nomor kerja, bukan urutan final.

Status verifikasi:
- ✅ judul, venue, dan angka yang dikutip sudah dicocokkan dengan halaman sumber atau abstrak. **Daftar penulis TIDAK dijamin**: pada beberapa entri ditandai [LENGKAPI penulis]; ambil dari halaman resmi/DOI, jangan dari catatan ini
- ⚠️ sumber sekunder atau grey literature; cari sumber primer atau pakai dengan hati-hati

---

## A. Konteks dan regulasi (bahan Bab 1 dan awal Bab 2)

**[K1] Jumlah mahasiswa disabilitas (PDDikti, Juni 2025)** ⚠️ berita, sumber primer adalah PDDikti
- Ada 3.128 mahasiswa disabilitas di 282 PT. Tunanetra kelompok terbesar dengan 1.727 orang; sekitar 1.078 dengan gangguan emosi/perilaku, 327 dengan kesulitan belajar spesifik, dan 172 disabilitas intelektual.
- Sumber: detik.com, "Jumlah Mahasiswa Disabilitas RI Capai 3.128 Orang, Tersebar di 282 Kampus", https://www.detik.com/edu/perguruan-tinggi/d-8536719 ; juga Tribunnews dan Global Review. Cek portal https://ptinklusif.kemdiktisaintek.go.id

**[K2] Penyandang disabilitas yang tamat perguruan tinggi: 4,24% (2024)** ⚠️ sumber sekunder
- Dikutip dataindonesia.id dari BPS. Cari tabel aslinya, kemungkinan di "Potret Penyandang Disabilitas di Indonesia: Hasil Long Form SP2020" (BPS, Des 2024) atau Statistik Pendidikan 2024.
- Jangan pakai angka pembanding 35,21% untuk nondisabilitas; konteksnya ambigu di sumber sekunder.

**[K3] UU No. 8 Tahun 2016 tentang Penyandang Disabilitas** (dasar kewajiban akomodasi dan ULD) [LENGKAPI pasal yang relevan]

**[K4] Permendikbudristek No. 48 Tahun 2023 tentang Akomodasi yang Layak untuk Peserta Didik Penyandang Disabilitas** (berlaku sampai pendidikan tinggi) ✅
- Pasal 3: pemenuhan akomodasi yang layak adalah tanggung jawab pemerintah daerah dan satuan pendidikan.
- JDIH: https://jdih.kemdikbud.go.id/detail_peraturan?main=3314

**[K5] W3C, "Web Content Accessibility Guidelines (WCAG) 2.2", W3C Recommendation, 5 Okt 2023** ✅
- SC 1.1.1 Non-text Content: semua konten non-teks wajib punya alternatif teks dengan fungsi setara.
- Diadopsi sebagai ISO/IEC 40500:2025. https://www.w3.org/TR/WCAG22/

**[K6] ISO 14289-2:2024, PDF/UA-2** (terbit 15 Mar 2024), standar PDF aksesibel untuk PDF 2.0 ✅
- https://www.iso.org/standard/82278.html
- PDF/UA-1 adalah ISO 14289-1.

---

## B. Skala masalah: dokumen akademik tidak aksesibel

**[P1] L. L. Wang et al., "Improving the Accessibility of Scientific Documents: Current State, User Needs, and a System Solution to Enhance Scientific PDF Accessibility for Blind and Low Vision Users," arXiv:2105.00076, 2021.** ✅
- Menilai 11.397 PDF ilmiah (2010–2019): hanya 2,4% memenuhi semua kriteria aksesibilitas.
- Memperkenalkan SciA11y, yang mengubah PDF ilmiah menjadi HTML aksesibel (heading bertag, daftar isi, tautan sitasi dua arah). Respons pengguna BLV positif.
- Batas: dirancang untuk paper ilmiah berbahasa Inggris, bukan slide atau materi kuliah.

**[P2] A. Kumar dan L. L. Wang, "Uncovering the New Accessibility Crisis in Scholarly PDFs," Proc. ACM ASSETS '24, 2024, doi:10.1145/3663548.3675634.** ✅ (judul, venue, angka); penulis terverifikasi (arXiv)
- 20.000 PDF (2014–2023): kurang dari 3,2% memenuhi keenam kriteria (Default Language, Appropriate Nesting, Tagged PDF, Table Headers, Tab Order, Alt-Text); 74,9% tidak memenuhi satu pun.
- Aksesibilitas menurun sejak 2019, terutama pada open access. Platform pembuat dokumen berpengaruh.

**[P3] S. Brinn et al., "HTML papers on arXiv – why it is important, and how we made it happen," arXiv:2402.08954, 2024.** ✅ [LENGKAPI daftar penulis]
- Survei arXiv 2022: hanya 30% pengguna teknologi bantu bisa mengakses semua riset yang dibutuhkan tanpa bantuan; PDF adalah hambatan terbesar.
- Solusi: HTML via LaTeXML sejak Des 2023.
- Batas (fakta): hanya berlaku untuk naskah yang dikirim dalam LaTeX ke arXiv, bukan slide atau PDF materi kuliah.

**[P4] Konteks Indonesia: NVDA dan mahasiswa tunanetra** ⚠️ grey literature, cari yang terbit di jurnal
- Repositori Universitas Brawijaya, "Implementasi Pembaca Layar NVDA Sebagai Alat Bantu Menulis Karya Ilmiah Bagi Mahasiswa Tunanetra di Universitas Brawijaya," https://repository.ub.ac.id/id/eprint/203894/
- Pengaruh NVDA terhadap hasil belajar mahasiswa tunanetra Universitas PGRI Argopuro Jember (ResearchGate 364589424).
- TEPTUN, Jurnal Pendidikan dan Konseling (JPDK), https://journal.universitaspahlawan.ac.id/index.php/jpdk/article/view/7224
- Temuan umum: NVDA membaca teks PDF, tetapi tidak bisa menangani gambar, tabel, grafik, dan slide yang padat visual.

> **Celah data yang ditemukan:** belum ditemukan studi kuantitatif tentang tingkat aksesibilitas materi kuliah di PT Indonesia (setara P1/P2). Tim bisa mengisinya sendiri sebagai data awal, misalnya menjalankan veraPDF pada sejumlah PDF materi kuliah terbuka dari PT Indonesia. Analisis dan interpretasinya dikerjakan tim.

---

## C. Isi deskripsi visual: apa yang dibutuhkan pengguna tunanetra

**[V1] A. Lundgard dan A. Satyanarayan, "Accessible Visualization via Natural Language Descriptions: A Four-Level Model of Semantic Content," IEEE TVCG, vol. 28, no. 1, pp. 1073–1083, 2022.** ✅
- Model 4 level isi semantik deskripsi visualisasi: L1 konstruksi (jenis grafik, sumbu), L2 statistik, L3 tren/pola perseptual, L4 konteks/domain.
- Disusun dari analisis grounded theory atas 2.147 kalimat. Pembaca tunanetra maupun awas paling terbantu oleh isi L3.

**[V2] C. Jung, S. Mehta, A. Kulkarni, Y. Zhao, dan Y.-S. Kim, "Communicating Visualizations without Visuals: Investigation of Visualization Alternative Text for People with Visual Impairments," IEEE TVCG, vol. 28, no. 1, pp. 1095–1105, 2022.** ✅
- Wawancara 22 orang dengan hambatan penglihatan.
- Dari 7.493 gambar di 2.278 publikasi (VIS/TVCG, ASSETS, CHI), 40% punya alt text (VIS/TVCG 0%, ASSETS 65%, CHI 51%). Praktik penulisan hanya sebagian sesuai pedoman.

**[V3] S. Chintalapati, J. Bragg, dan L. L. Wang, "A Dataset of Alt Texts from HCI Publications: Analyses and Uses Towards Producing More Descriptive Alt Texts of Data Visualizations in Scientific Papers," Proc. ACM ASSETS '22, 2022, doi:10.1145/3517428.3544796.** ✅
- Hanya 50% alt text yang memuat nilai ekstrem/outlier, dan hanya 31% yang memuat tren/perbandingan utama.
- Dataset beranotasi level semantik: https://github.com/allenai/hci-alt-texts

**[V4] B. J. Tang, A. Boggust, dan A. Satyanarayan, "VisText: A Benchmark for Semantically Rich Chart Captioning," Proc. ACL 2023 (Long Papers), 2023.** ✅
- 12.441 pasangan grafik dan caption. Setiap grafik tersedia sebagai citra, tabel data, dan scene graph.
- Caption L1 dibangkitkan otomatis, caption L2/L3 dari crowdsourcing. https://github.com/mitvis/vistext
- Kegunaan untuk evaluasi: tabel data memungkinkan cek otomatis angka yang dikarang pada deskripsi.

---

## D. Kemampuan dan keterbatasan model vision-language

**[M1] Z. Wang, M. Xia, L. He, H. Chen, Y. Liu, R. Zhu, K. Liang, X. Wu, H. Liu, S. Malladi, A. Chevalier, S. Arora, dan D. Chen, "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs," NeurIPS 2024 Datasets & Benchmarks Track.** ✅ [LENGKAPI penulis]
- 2.323 grafik dari paper ilmiah. Soal penalaran: GPT-4o 47,1%, model open-source terbaik 29,2%, manusia 80,5%.
- Uji dengan grafik atau pertanyaan yang sedikit berbeda menurunkan performa hingga 34,5%; benchmark lama terlalu optimistis.

**[M2] P. Rahmanzadehgervi, L. Bolton, M. R. Taesiri, dan A. T. Nguyen, "Vision language models are blind: Failing to translate detailed visual features into words," Proc. ACCV 2024.** ✅
- VLM mutakhir rata-rata hanya 58,07% akurat pada tugas geometri sederhana; terbaik Claude 3.5 Sonnet 77,84% (halaman arXiv, versi Juli 2024). Cek angka pada versi ACCV.

**[M3] M. Raees, Y. Iwamoto, K. Papangelis, J. Heard, dan G. W. Tigwell, "How University Disability Services Professionals Write Image Descriptions for HCI Figures Using Generative AI," arXiv:2602.08937, 2026.** ✅ (penulis dan judul dari halaman arXiv). Catatan: ada makalah terkait berjudul "Exploring Generative AI to Support Disability Service Professionals in Writing Image Descriptions for HCI Science Figures," ASSETS '25, doi:10.1145/3663547.3759763; itu BUKAN judul yang sama, jangan dicampur.
- 12 staf unit layanan disabilitas PT menulis alt text dengan dan tanpa bantuan AI generatif.
- Dengan AI lebih cepat dan lebih percaya diri, tetapi staf mengeluhkan kurangnya kendali atas keluaran dan relevansinya.
- Relevan langsung dengan peran ULD di Indonesia.

---

## E. Remediasi PDF dan ekstraksi struktur dokumen (solusi yang sudah ada)

**[R1] F. M. Schmitt-Koopmann, E. M. Huang, H.-P. Hutter, dan A. Darvishy, "Towards More Accessible Scientific PDFs for People with Visual Impairments: Step-by-Step PDF Remediation to Improve Tag Accuracy," Proc. CHI '25, 2025, doi:10.1145/3706598.3713084.** ✅ [LENGKAPI penulis]
- PAVE 2.0 dibandingkan dengan Adobe Acrobat Pro (19 partisipan). Skor tagging pengguna berpengalaman naik dari 42,0% ke 80,1%, pemula dari 39,2% ke 75,2%.
- Memuat pendekatan membuat alt text rumus tanpa keahlian khusus.
- Batas (fakta): alat bantu remediasi manual langkah demi langkah, berbahasa Inggris.

**[R2] Adobe PDF Accessibility Auto-Tag (Acrobat / API)** ⚠️ dokumentasi vendor dan evaluasi pihak ketiga
- https://developer.adobe.com/document-services/apis/pdf-accessibility-auto-tag/
- Evaluasi AbilityNet: membantu sebagai titik awal, tetapi tabel kompleks, urutan baca, dan level heading pada tata letak rumit masih perlu koreksi manual.
- Berbayar. Tidak membuat deskripsi isi grafik.

**[R3] A. Kumar, T. Padath, dan L. L. Wang, "Benchmarking PDF Accessibility Evaluation: A Dataset and Framework for Assessing Automated and LLM-Based Approaches for Accessibility Testing," arXiv:2509.18965, 2025 (juga di ACM ASSETS '25, doi:10.1145/3663547.3746380).** ✅
- Benchmark PDF beranotasi pakar pada 7 kriteria: kualitas alt text, urutan baca, tagging semantik, struktur tabel, hyperlink, kontras warna, keterbacaan font.
- GPT-4-Turbo akurasi 0,85, tetapi lemah pada label "Not Present/Cannot Tell", terutama kualitas alt text.
- Rule-based checker unggul untuk verifikasi teknis, LLM untuk kesesuaian semantik. Menyarankan pendekatan hibrida (checker + LLM + manusia).

**[R4] veraPDF, validator PDF/A dan PDF/UA open-source (Open Preservation Foundation dan PDF Association).** ✅
- https://docs.verapdf.org/validation/
- Hanya memeriksa kondisi gagal Matterhorn Protocol yang bisa dicek mesin. Keberadaan alt text terdeteksi, kebenaran isinya tidak.

**[R5] C. Auer et al. (19 penulis; pertama Christoph Auer, terakhir Peter W. J. Staar), "Docling Technical Report," arXiv:2408.09869, 2024.** ✅
- Toolkit open-source (MIT) untuk konversi PDF: analisis tata letak (dilatih pada DocLayNet) dan struktur tabel (TableFormer); berjalan di perangkat biasa.

**[R6] L. Blecher, G. Cucurull, T. Scialom, dan R. Stojnic, "Nougat: Neural Optical Understanding for Academic Documents," ICLR 2024 (arXiv:2308.13418).** ✅
- Transformer visual yang mengubah halaman dokumen akademik menjadi markup, termasuk rumus.

**[R7] B. Wang, Z. Gu, G. Liang, C. Xu, B. Zhang, B. Shi, dan C. He, "UniMERNet: A Universal Network for Real-World Mathematical Expression Recognition," arXiv:2404.15254, 2024.** ✅ [LENGKAPI penulis]
- Mengubah citra ekspresi matematika menjadi LaTeX pada kondisi dunia nyata. Kode terbuka.

**[R8] [LENGKAPI penulis], "LayoutReader: Pre-training of Text and Layout for Reading Order Detection," Proc. EMNLP 2021.** ✅
- ReadingBank: 500 ribu dokumen dengan label urutan baca, dibangun otomatis dari metadata XML dokumen Word.
- Contoh acuan yang lahir dari cara data dibuat.

---

## F. Aksesibilitas matematika

**[F1] MathCAT (N. Soiffer, proyek DAISY): mesin pengubah MathML menjadi ucapan (ClearSpeak/SimpleSpeak) dan braille (Nemeth/UEB).** ✅
- https://daisy.github.io/MathCAT/users.html
- **Penting untuk klaim kebaruan: MathCAT sudah mendukung Bahasa Indonesia (id).** Jadi "membacakan rumus dalam Bahasa Indonesia" bukan hal baru. Yang belum tersedia adalah jalur dari materi kuliah (PDF/slide/gambar rumus) menjadi MathML yang benar.

**[F2] Frankel dkk. [LENGKAPI penulis], "Development and Initial Evaluation of the ClearSpeak Style for Automated Speaking of Algebra," ETS Research Report Series, 2016.** ✅ [cek penulis dan nomor]
- ClearSpeak: gaya ucapan matematika yang lebih alami untuk pemula; MathSpeak lebih presisi struktural.

**[F3] Konteks Indonesia: hambatan belajar matematika tunanetra** ⚠️ mayoritas tingkat sekolah
- "Hambatan Belajar Matematika Siswa Tunanetra di Kelas Inklusi: Perspektif Siswa Tunanetra dan Guru," Gammath: Jurnal Ilmiah Prodi Pendidikan Matematika, Univ. Muhammadiyah Jember. https://ejurnal.unmuhjember.ac.id/index.php/JPM/article/view/1362
- Studi tingkat perguruan tinggi belum ditemukan.

---

## G. Solusi dan layanan yang sudah ada di Indonesia

**[L1] Yayasan Mitra Netra** ⚠️ situs lembaga dan berita
- Perintis produksi buku aksesibel (braille, audio, digital untuk screen reader); perpustakaan daring/luring; ada produk "Mitranetra Braille Converter" berbasis AI.
- Produksi manual butuh SDM, sarana, dan biaya tinggi.
- https://mitranetra.or.id/program-layanan/perpustakaan/ ; https://mitranetra.or.id/produk/mitranetra-braille-converter/ ; Tempo, "Produksi Buku Braille Terkendala Biaya yang Mahal"
- Batas (fakta): fokus pada buku, bukan materi kuliah mingguan dari dosen. Cek sendiri apakah melayani konversi materi kuliah atas permintaan.

**[L2] Unit Layanan Disabilitas (ULD) di PT** (diwajibkan UU 8/2016 dan Permen 48/2023)
- Kemdiktisaintek mengalokasikan bantuan hingga Rp40 juta untuk penguatan layanan inklusif melalui ULD (berita K1). [cek sumber primer]
- Laman Kemdiktisaintek tentang ULD: https://kemdiktisaintek.go.id/news/article/unit-layanan-disabilitas-sebagai-pilar-kesetaraan-di-perguruan-tinggi-langkah-nyata-menuju-kampus-inklusif

---

## H. Pembanding terdekat (prior art) yang ditemukan pada pencarian lanjutan

> **Perhatian untuk positioning (25%):** dua sistem di bawah ini melakukan sebagian dari yang mungkin ingin tim klaim. Keduanya harus muncul di tabel pembanding Bab 2, dan klaim kebaruan tim harus dirumuskan dengan memperhitungkannya.

**[X1] P. Mowar, A. Steinfeld, dan J. Bigham, "iTagPDF: Towards Finally Automating PDF Accessibility," Proc. CHI '26, 13 Apr 2026, doi:10.1145/3772318.3790289.** ⚠️ hanya dari abstrak; halaman ACM memblokir akses otomatis (HTTP 403), jadi tim wajib membaca teks lengkapnya
- Memakai gabungan dua representasi yang lahir saat penulisan, yaitu dokumen sumber LaTeX dan render PDF, untuk menghasilkan tag yang akurat dengan urutan baca yang benar. Untuk gambar, cek dulu apakah penulis sudah menyediakan alt text; jika belum, agen LLM mendeskripsikan gambar.
- Mengklaim melampaui kualitas tagging manual oleh penulis pada dataset yang mereka kumpulkan.
- Fakta yang relevan untuk positioning: metode ini bergantung pada **sumber LaTeX**. Apakah materi kuliah di PT Indonesia (Word/PowerPoint/PDF hasil ekspor) juga tersedia dalam LaTeX perlu dicek tim; catatan ini tidak menyimpulkannya.
- Pekerjaan terkait dari sisi LaTeX: "MathML and other XML Technologies for Accessible PDF from LaTeX," ACM DocEng 2025, doi:10.1145/3704268.3748669; "Automatically producing accessible and reusable PDFs with LaTeX," DocEng 2024, doi:10.1145/3685650.3685670.

**[X2] OpenDataLoader PDF (proyek open-source, opendataloader-project).** ✅ dari README repositori; tidak ada tanggal versi di dokumentasi
- https://github.com/opendataloader-project/opendataloader-pdf
- Auto-tag PDF tak bertag menjadi Tagged PDF (Apache 2.0, gratis), divalidasi dengan veraPDF. Ekspor ke PDF/UA-1/UA-2 adalah add-on enterprise (berbayar).
- Mode hybrid: deskripsi AI untuk grafik/gambar (`--enrich-picture-description`, ditandai "ai-generated/original/missing") dan ekstraksi rumus LaTeX (`--enrich-formula`).
- Bahasa OCR yang disebut eksplisit: Inggris, Korea, Jepang, Tionghoa, Jerman, Prancis, Arab, "dan lainnya"; Indonesia tidak disebut eksplisit di dokumentasi yang dibaca. Tim perlu mengujinya sendiri sebelum menulis klaim.
- Tidak memproses berkas Word/Excel/PowerPoint.

**[X3] Adobe PDF Accessibility Auto-Tag** (lihat R2), dan **PAVE 2.0** (lihat R1).

Implikasi untuk tabel pembanding (isi kolom hanya dengan yang tim verifikasi sendiri): sumber input yang dibutuhkan (LaTeX / PDF / Word), deskripsi isi grafik, rumus, urutan baca, Bahasa Indonesia, biaya/lisensi, cara evaluasinya.

---

## I. Pengguna tunanetra dan AI generatif

**[U1] R. Adnin dan M. Das, "\"I look at it as the king of knowledge\": How Blind People Use and Understand Generative AI Tools," Proc. ACM ASSETS '24, 27–30 Okt 2024, doi:10.1145/3663548.3675631.** ✅ (dibaca dari PDF)
- Wawancara semi-terstruktur dengan 19 orang tunanetra pengguna ChatGPT, Copilot, Gemini, Claude, dan Be My AI (dipilih dari 27 responden; wawancara Jan–Mar 2024; mayoritas peserta di AS).
- Temuan: pengguna menghadapi ketidakakuratan, halusinasi, dan keanehan keluaran GenAI, serta membentuk model mental yang sering keliru; penulis menekankan verifikasi informasi sebagai isu utama.
- Contoh dari makalah: deskripsi Be My AI menukar barang yang dipegang di tangan kanan dan kiri.
- Catatan: partisipan hampir seluruhnya di AS; jangan digeneralisasi ke Indonesia tanpa dasar.

**[U2] "Surfacing Variations to Calibrate Perceived Reliability of MLLM-generated Image Descriptions," arXiv:2507.15692, 2025.** ⚠️ hanya dari hasil pencarian; baca dan lengkapi
- Topik: menampilkan variasi antar deskripsi agar pengguna dapat menakar keandalan deskripsi buatan MLLM. Berkaitan dengan kebutuhan transparansi ketidakpastian.

---

## J. Kinerja model pada konten berbahasa Indonesia

**[N1] P. Yue dkk., "SEA-Vision: A Multilingual Benchmark for Comprehensive Document and Scene Text Understanding in Southeast Asia," arXiv:2603.15409, 16 Mar 2026.** ✅ (dari halaman arXiv)
- 15.234 halaman untuk document parsing dan 7.496 pasangan tanya-jawab (TEC-VQA) dalam 11 bahasa Asia Tenggara, termasuk Indonesia; menguji 13 baseline parsing dan 12 VLM (termasuk GPT-4o dan Gemini 2.5 Pro).
- Kutipan hasil: akurasi turun menjadi 43,61% pada Indonesia. Untuk pembanding tim perlu membaca angka bahasa Inggris pada makalah yang sama.

**[N2] S. Gautam, A. Dravichi, dan G. Harit, "INDOTABVQA: A Benchmark for Cross-Lingual Table Understanding in Bahasa Indonesia Documents," arXiv:2604.11970, April 2026.** ✅ (dari halaman arXiv)
- Benchmark tanya-jawab visual atas tabel pada dokumen berbahasa Indonesia, dengan anotasi dalam Indonesia, Inggris, Hindi, dan Arab; dataset di Hugging Face (NusaBharat/INDOTABVQA), lisensi CC BY 4.0.
- Menunjukkan celah performa pada pemahaman tabel non-Inggris. Angka spesifik belum saya ekstrak; baca makalahnya.

Catatan: kedua benchmark ini belum menguji keluaran untuk pembaca layar. Yang mereka ukur adalah pemahaman dokumen, bukan kelayakan deskripsi bagi pengguna tunanetra.

---

## K. Kondisi aksesibilitas digital di kampus Indonesia

**[I1] Mahalli, "Mayoritas website pemerintah dan universitas di Indonesia tidak ramah difabel," The Conversation Indonesia, 8 Des 2021.** ⚠️ artikel populer
- Menyebut sekitar 95% situs web perguruan tinggi di Indonesia bermasalah aksesibilitas, dengan merujuk pada studi di Indonesian Journal of Disability Studies (IJDS). Cari artikel IJDS aslinya dan kutip yang primer.
- Juga merujuk survei AIDRAN (Australia-Indonesia Research and Advocacy Network) tentang aksesibilitas pembelajaran daring saat COVID-19.
- Batas: yang diukur adalah situs web, bukan materi kuliah.

**[I2] AIDRAN, "Perguruan Tinggi dan Praktik Akomodasi Layak bagi Mahasiswa Penyandang Disabilitas di Indonesia di Masa Pandemi COVID-19," 2021.** ⚠️ belum dibaca isinya
- https://aidran.org/wp-content/uploads/2021/08/perguruan-tinggi-dan-praktik-akomodasi-layak-bagi-mahasiswa-penyandang-disabilitas-di-indonesia-di-masa-pandemi-covid-19.pdf
- Kandidat sumber primer untuk hambatan materi pembelajaran daring bagi mahasiswa disabilitas di Indonesia. Tim perlu membacanya dan mengambil temuan spesifik.

**[I3] Kemdikbud, "Panduan Layanan Mahasiswa Disabilitas di Perguruan Tinggi."** ⚠️ hanya judul dari hasil pencarian
- https://dikti.kemdikbud.go.id/library/book/panduan-layanan-mahasiswa-disabilitas-di-perguruan-tinggi
- Cek apakah memuat ketentuan tentang bahan ajar aksesibel.

---

## Yang belum ditemukan (celah pencarian)
- Studi kuantitatif tingkat aksesibilitas materi kuliah (bukan situs web) di PT Indonesia.
- Angka Bahasa Inggris pembanding pada SEA-Vision dan INDOTABVQA, dan hasil uji model pada Bahasa Indonesia untuk deskripsi grafik (bukan VQA).
- Studi pengguna tunanetra di Indonesia terhadap deskripsi gambar buatan AI.
- Teks lengkap iTagPDF (perlu akses ACM dari jaringan kampus).
- Sumber primer untuk angka 4,24% dan jumlah mahasiswa disabilitas (portal PDDikti dan publikasi BPS).
