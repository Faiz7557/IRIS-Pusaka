# -*- coding: utf-8 -*-
"""Isi naskah semifinal ICC 2026 (Bab I-III), versi 6 (sunting bahasa dan tata letak).
Markup: [@k1,@k2] sitasi | *miring* | _{subskrip} | {T:kunci} {G:kunci} {E:kunci} rujukan silang bernomor otomatis.
Istilah asing dimiringkan otomatis oleh build_docx.py (daftar FOREIGN)."""

NS = "SIMAK"
TITLE = NS + ": Remediasi Materi Kuliah Berbahasa Indonesia agar Dapat Disimak oleh Mahasiswa Tunanetra dan Pendengar dengan Gerbang Verifikasi"
TEAM = "IRIS kata HQ ini lomba terakhir"
AUTHORS = [("Faiz Iqbal I’tishom", "1"), ("Shidqy Baihaqy El Muhammady", "2"),
           ("M. Devian Rhefanza Rafi Zackary", "3"), ("Christofanny Nathaniela Naibaho", "4")]
AFFILS = [("1,2,3,4", "Universitas Airlangga, Indonesia")]

ABSTRACT = (
    "Mahasiswa tunanetra mengakses materi kuliah melalui pembaca layar, tetapi materi berformat PDF jarang dapat dibaca "
    "secara utuh; hal yang sama dialami mahasiswa yang memilih mendengarkan materi lewat alat bacaan suara. Audit awal "
    "terhadap 28 PDF materi kuliah dari 18 kampus menunjukkan bahwa tidak satu pun memenuhi standar PDF/UA-1 dan hanya 29 "
    "dari 1.111 elemen gambar pada dokumen bertag (2,6%) memiliki teks alternatif. Unit Layanan Disabilitas (ULD) "
    "bertanggung jawab atas akomodasi ini, tetapi belum memiliki perangkat yang menangani grafik, tabel, dan rumus dalam "
    "materi berbahasa Indonesia. Makalah ini mengusulkan " + NS + " (Sistem Ilustrasi Materi Aksesibel untuk Kuliah), "
    "sebuah pipeline remediasi yang menempatkan ULD sebagai peninjau. Sistem ini melengkapi struktur dan tag dokumen, "
    "menyusun deskripsi grafik dari tabel data yang statistiknya dihitung oleh kode, membacakan rumus melalui MathML dan "
    "MathCAT berbahasa Indonesia, menyediakan mode dengar, dan menahan setiap keluaran yang tidak dapat diverifikasi pada "
    "antrean tinjauan (gerbang fail-closed). Uji kelayakan awal menunjukkan bahwa perakitan tag hingga lulus validator "
    "veraPDF dapat dicapai pada dua dari tiga dokumen, dengan waktu proses 4,6 detik untuk 21 halaman pada perangkat tanpa "
    "GPU. Uji rancangan gerbang menunjukkan bahwa kemiripan citra tidak dapat memverifikasi rumus dan bahwa pemeriksaan "
    "angka harus dilakukan pada tingkat klaim. Evaluasi dirancang melalui tujuh gerbang dengan kriteria lulus yang "
    "dikunci sebelum pengujian, sedangkan uji pada mahasiswa tunanetra ditunda. Makalah ini belum melaporkan kinerja "
    "sistem; hasil implementasi dan evaluasi disajikan pada tahap final."
)
KEYWORDS = "aksesibilitas dokumen, tunanetra, deskripsi grafik, model vision-language, PDF/UA"

REFS = {
 "podcast": "Databoks Katadata, “Indonesia: Leading podcast listener nation by early 2025,” 2025 (data: We Are Social, Feb. 2025). Diakses: 30 Sep. 2026. [Online]. Available: https://databoks.katadata.co.id/en/technology-telecommunications/statistics/67bd8f7c19196/indonesia-leading-podcast-listener-nation-by-early-2025",
 "pashler": "H. Pashler, M. McDaniel, D. Rohrer, and R. Bjork, “Learning styles: Concepts and evidence,” Psychol. Sci. Public Interest, vol. 9, no. 3, pp. 105–119, Dec. 2008.",
 "cast": "CAST, “Universal Design for Learning Guidelines version 3.0,” 2024. Diakses: 30 Sep. 2026. [Online]. Available: https://udlguidelines.cast.org/",
 "blackwell": "A. G. Blackwell, “The curb-cut effect,” Stanford Social Innovation Review, Winter 2017. [Online]. Available: https://ssir.org/pdf/Winter_17_The_Curb_Cut_Effect.pdf",
 "wood": "S. G. Wood, J. H. Moxley, E. L. Tighe, and R. K. Wagner, “Does use of text-to-speech and related read-aloud tools improve reading comprehension for students with reading disabilities? A meta-analysis,” J. Learn. Disabil., vol. 51, no. 1, pp. 73–84, 2018, doi: 10.1177/0022219416688170.",

 "detik": "detikEdu, “Jumlah mahasiswa disabilitas RI capai 3.128 orang, tersebar di 282 kampus,” detik.com, 2025. [Online]. Available: https://www.detik.com/edu/perguruan-tinggi/d-8536719/",
 "pddikti": "Kemdiktisaintek, “Dashboard Mahasiswa,” Portal Data Pendidikan Tinggi, Sains, dan Teknologi, data tahun 2025. Diakses: 29 Sep. 2026. [Online]. Available: https://data.kemdiktisaintek.go.id/dashboard/mahasiswa",
 "uu8": "Undang-Undang Republik Indonesia Nomor 8 Tahun 2016 tentang Penyandang Disabilitas, 2016.",
 "permen48": "Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi Nomor 48 Tahun 2023 tentang Akomodasi yang Layak untuk Peserta Didik Penyandang Disabilitas pada Satuan Pendidikan Anak Usia Dini Formal, Pendidikan Dasar, Pendidikan Menengah, dan Pendidikan Tinggi, 2023. [Online]. Available: https://jdih.kemdikbud.go.id/detail_peraturan?main=3314",
 "wcag": "W3C, “Web Content Accessibility Guidelines (WCAG) 2.2,” W3C Recommendation, Okt. 2023. [Online]. Available: https://www.w3.org/TR/WCAG22/",
 "wang21": "L. L. Wang et al., “Improving the accessibility of scientific documents: Current state, user needs, and a system solution to enhance scientific PDF accessibility for blind and low vision users,” arXiv:2105.00076, 2021.",
 "kumar24": "A. Kumar and L. L. Wang, “Uncovering the new accessibility crisis in scholarly PDFs: Publishing model and platform changes contribute to declining scholarly document accessibility in the last decade,” in Proc. 26th Int. ACM SIGACCESS Conf. Comput. Accessibility (ASSETS), 2024, doi: 10.1145/3663548.3675634.",
 "arxivhtml": "arXiv, “HTML as an accessible format for papers.” Diakses: 29 Sep. 2026. [Online]. Available: https://info.arxiv.org/about/accessible_HTML.html",
 "mahalli": "Mahalli, “Mayoritas website pemerintah dan universitas di Indonesia tidak ramah difabel,” The Conversation Indonesia, 8 Des. 2021. [Online]. Available: https://theconversation.com/mayoritas-website-pemerintah-dan-universitas-di-indonesia-tidak-ramah-difabel-173159",
 "charxiv": "Z. Wang et al., “CharXiv: Charting gaps in realistic chart understanding in multimodal LLMs,” in Proc. NeurIPS Datasets and Benchmarks Track, 2024.",
 "blind": "P. Rahmanzadehgervi, L. Bolton, M. R. Taesiri, and A. T. Nguyen, “Vision language models are blind: Failing to translate detailed visual features into words,” arXiv:2407.06581, 2024.",
 "sea": "P. Yue et al., “SEA-Vision: A multilingual benchmark for comprehensive document and scene text understanding in Southeast Asia,” arXiv:2603.15409, 2026.",
 "adnin": "R. Adnin and M. Das, “‘I look at it as the king of knowledge’: How blind people use and understand generative AI tools,” in Proc. 26th Int. ACM SIGACCESS Conf. Comput. Accessibility (ASSETS), 2024, doi: 10.1145/3663548.3675631.",
 "mitranetra": "Yayasan Mitra Netra, “Perpustakaan.” Diakses: 29 Sep. 2026. [Online]. Available: https://mitranetra.or.id/program-layanan/perpustakaan/",
 "tempo": "Tempo.co, “Produksi buku braille terkendala biaya yang mahal.” Diakses: 29 Sep. 2026. [Online]. Available: https://www.tempo.co/politik/produksi-buku-braille-terkendala-biaya-yang-mahal-2104555",
 "raees": "M. Raees, Y. Iwamoto, K. Papangelis, J. Heard, and G. W. Tigwell, “How university disability services professionals write image descriptions for HCI figures using generative AI,” arXiv:2602.08937, 2026.",
 "verapdf": "veraPDF Consortium, “veraPDF validation.” Diakses: 29 Sep. 2026. [Online]. Available: https://docs.verapdf.org/validation/",
 "kumarbench": "A. Kumar, T. Padath, and L. L. Wang, “Benchmarking PDF accessibility evaluation: A dataset and framework for assessing automated and LLM-based approaches for accessibility testing,” arXiv:2509.18965, 2025.",
 "lundgard": "A. Lundgard and A. Satyanarayan, “Accessible visualization via natural language descriptions: A four-level model of semantic content,” IEEE Trans. Vis. Comput. Graphics, vol. 28, no. 1, pp. 1073–1083, Jan. 2022.",
 "jung": "C. Jung, S. Mehta, A. Kulkarni, Y. Zhao, and Y.-S. Kim, “Communicating visualizations without visuals: Investigation of visualization alternative text for people with visual impairments,” IEEE Trans. Vis. Comput. Graphics, vol. 28, no. 1, pp. 1095–1105, Jan. 2022.",
 "chinta": "S. Chintalapati, J. Bragg, and L. L. Wang, “A dataset of alt texts from HCI publications: Analyses and uses towards producing more descriptive alt texts of data visualizations in scientific papers,” in Proc. 24th Int. ACM SIGACCESS Conf. Comput. Accessibility (ASSETS), 2022, doi: 10.1145/3517428.3544796.",
 "vistext": "B. J. Tang, A. Boggust, and A. Satyanarayan, “VisText: A benchmark for semantically rich chart captioning,” in Proc. 61st Annu. Meeting Assoc. Comput. Linguistics (ACL), 2023.",
 "indotab": "S. Gautam, A. Dravichi, and G. Harit, “IndoTabVQA: A benchmark for cross-lingual table understanding in Bahasa Indonesia documents,” arXiv:2604.11970, 2026.",
 "pave": "F. M. Schmitt-Koopmann, E. M. Huang, H.-P. Hutter, and A. Darvishy, “Towards more accessible scientific PDFs for people with visual impairments: Step-by-step PDF remediation to improve tag accuracy,” in Proc. CHI Conf. Human Factors Comput. Syst. (CHI), 2025, doi: 10.1145/3706598.3713084.",
 "itag": "P. Mowar, A. Steinfeld, and J. Bigham, “iTagPDF: Towards finally automating PDF accessibility,” in Proc. CHI Conf. Human Factors Comput. Syst. (CHI), 2026, doi: 10.1145/3772318.3790289.",
 "odl": "OpenDataLoader Project, “OpenDataLoader PDF.” GitHub. Diakses: 29 Sep. 2026. [Online]. Available: https://github.com/opendataloader-project/opendataloader-pdf",
 "adobe": "Adobe, “PDF Accessibility Auto-Tag API.” Diakses: 29 Sep. 2026. [Online]. Available: https://developer.adobe.com/document-services/apis/pdf-accessibility-auto-tag/",
 "abilitynet": "AbilityNet, “Evaluating Adobe’s new cloud-based auto-tagging feature for PDF accessibility.” Diakses: 29 Sep. 2026. [Online]. Available: https://abilitynet.org.uk/news-blogs/evaluating-adobes-new-cloud-based-auto-tagging-feature-pdf-accessibility",
 "mathcat": "N. Soiffer et al., “MathCAT user guide,” DAISY Consortium. Diakses: 29 Sep. 2026. [Online]. Available: https://daisy.github.io/MathCAT/users.html",
 "mathcatrepo": "N. Soiffer et al., “MathCAT: Math Capable Assistive Technology.” GitHub, DAISY Consortium. Diakses: 29 Sep. 2026. [Online]. Available: https://github.com/daisy/MathCAT",
 "mathcatdemo": "DAISY Consortium, “MathCATDemo: A web-based demo of MathCAT.” GitHub. Diakses: 29 Sep. 2026. [Online]. Available: https://github.com/daisy/MathCATDemo",
 "docling": "C. Auer et al., “Docling technical report,” arXiv:2408.09869, 2024.",
 "unimer": "B. Wang et al., “UniMERNet: A universal network for real-world mathematical expression recognition,” arXiv:2404.15254, 2024.",
 "doclaynet": "B. Pfitzmann et al., “DocLayNet: A large human-annotated dataset for document-layout analysis,” in Proc. 28th ACM SIGKDD Conf. Knowl. Discovery Data Mining (KDD), 2022.",
 "tableformer": "A. Nassar, N. Livathinos, M. Lysak, and P. Staar, “TableFormer: Table structure understanding with transformers,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2022.",
 "deplot": "F. Liu et al., “DePlot: One-shot visual language reasoning by plot-to-table translation,” in Findings Assoc. Comput. Linguistics: ACL 2023, pp. 10381–10399.",
 "qwen25vl": "S. Bai et al., “Qwen2.5-VL technical report,” arXiv:2502.13923, 2025.",
 "ssim": "Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: From error visibility to structural similarity,” IEEE Trans. Image Process., vol. 13, no. 4, pp. 600–612, Apr. 2004.",
 "kendall": "M. G. Kendall, “A new measure of rank correlation,” Biometrika, vol. 30, no. 1–2, pp. 81–93, Jun. 1938.",
 "cohen": "J. Cohen, “A coefficient of agreement for nominal scales,” Educ. Psychol. Meas., vol. 20, no. 1, pp. 37–46, Apr. 1960.",
 "wilson": "E. B. Wilson, “Probable inference, the law of succession, and statistical inference,” J. Amer. Statist. Assoc., vol. 22, no. 158, pp. 209–212, Jun. 1927.",
 "levenshtein": "V. I. Levenshtein, “Binary codes capable of correcting deletions, insertions and reversals,” Sov. Phys. Dokl., vol. 10, no. 8, pp. 707–710, Feb. 1966.",
}

# penyeragaman label rujukan daring dengan bahasa naskah (Indonesia)
for _k in REFS:
    REFS[_k] = REFS[_k].replace("[Online]. Available:", "[Daring]. Tersedia:")

# ---------------------------------------------------------------- BLOCKS
B = []
def h1(t): B.append(dict(kind="h1", text=t))
def h2(t): B.append(dict(kind="h2", text=t))
def p(t): B.append(dict(kind="p", text=t))
def pc(t): B.append(dict(kind="p", text=t, cont=True))     # lanjutan kalimat setelah persamaan (tanpa indentasi)
def eq(key, latex, desc, end=""): B.append(dict(kind="eq", key=key, latex=latex, desc=desc, end=end))
def table(key, cap, hdr, rows, widths, full=True, note=None, newpage=False):
    B.append(dict(kind="table", key=key, cap=cap, hdr=hdr, rows=rows, widths=widths, full=full, note=note, newpage=newpage))
def fig(key, file, cap, alt): B.append(dict(kind="fig", key=key, file=file, cap=cap, alt=alt))

# ================================================================= I. PENDAHULUAN
h1("PENDAHULUAN")
h2("Latar Belakang")
p("Perguruan tinggi di Indonesia berkewajiban menyediakan akomodasi yang layak bagi peserta didik penyandang disabilitas "
  "dan membentuk Unit Layanan Disabilitas (ULD) [@uu8,@permen48]. Pangkalan Data Pendidikan Tinggi (PDDikti) per Juni "
  "2025 mencatat 3.128 mahasiswa disabilitas di 282 perguruan tinggi, dan tunanetra merupakan kelompok terbesar dengan "
  "1.727 orang [@detik]. Seluruh mahasiswa disabilitas itu setara dengan sekitar 0,03% dari 10,75 juta mahasiswa "
  "terdaftar [@pddikti]. Meskipun kecil secara proporsi, bagi mahasiswa yang bersangkutan materi yang tidak terbaca "
  "berarti kesempatan belajar yang tidak setara. Kewajiban itu sudah jelas; yang belum tersedia adalah perangkat yang "
  "membuat materi kuliah dapat dibaca oleh pembaca layar.")
p("Skenario berikut bersifat ilustratif dan disusun dari temuan audit awal. Seorang mahasiswa tunanetra menerima berkas "
  "presentasi kuliah statistika berformat PDF. Pembaca layar membacakan judul salindia, tetapi diam pada grafik regresi dan "
  "rumus koefisien korelasi karena keduanya tidak memiliki teks alternatif, kondisi yang ditemukan pada 97,4% elemen "
  "gambar bertag dalam audit awal. Tabel dibacakan sel demi sel tanpa judul kolom, seperti pada 12 dari 13 dokumen "
  "bertabel yang diaudit. Mahasiswa itu lalu meminta rekannya menjelaskan, atau menunggu staf ULD menyalin ulang materi "
  "secara manual.")
p("Pembaca layar hanya membacakan teks dan teks alternatif yang tersedia. Gambar, grafik, dan rumus tanpa teks alternatif "
  "tidak menyampaikan informasi apa pun kepada penggunanya, sehingga Web Content Accessibility Guidelines (WCAG) 2.2 "
  "mensyaratkan setiap konten nonteks memiliki alternatif teks yang setara fungsinya [@wcag]. Tabel {T:bukti} merangkum "
  "bukti besaran masalah dari statistik resmi, penelitian terdahulu, audit awal penulis, dan tolok ukur (*benchmark*) "
  "model *vision-language* (VLM). Terdapat dua temuan utama. Pertama, dokumen aksesibel sangat jarang: 2,4% dan kurang "
  "dari 3,2% pada dua studi dokumen ilmiah [@wang21,@kumar24], serta 0 dari 28 pada audit awal penulis terhadap materi "
  "kuliah berbahasa Indonesia. Kedua, teks alternatif yang ada jarang informatif: hanya 31% memuat tren atau "
  "perbandingan utama [@chinta], dan pada audit penulis hanya 2,6% elemen gambar bertag yang memiliki teks alternatif. "
  "Dari 24 dokumen yang isinya berbahasa Indonesia, hanya 6 yang mendeklarasikan bahasa Indonesia, sedangkan 9 "
  "mendeklarasikan bahasa Inggris sehingga pembaca layar berisiko memakai aturan pelafalan yang keliru.")
table("bukti", "Tabel {T:bukti}. Bukti besaran masalah, sumber, dan kelas buktinya",
      ["Angka", "Nilai", "Sumber", "Kelas bukti"],
      [["Mahasiswa disabilitas tercatat (Juni 2025)", "3.128 di 282 PT; tunanetra 1.727 (terbesar); sekitar 0,03% dari 10.754.154 mahasiswa terdaftar (2025)", "PDDikti via detikEdu [@detik]; Portal Data Kemdiktisaintek [@pddikti]", "Statistik resmi (via media)"],
       ["PDF ilmiah yang memenuhi kriteria aksesibilitas", "2,4% dari 11.397 PDF (2010–2019); <3,2% dari 20.000 PDF (2014–2023), dengan 74,9% tidak memenuhi satu pun kriteria", "[@wang21,@kumar24]", "Penelitian"],
       ["Audit awal penulis: kepatuhan dan asal dokumen", "0 dari 28 PDF lulus PDF/UA-1 (median 7,5 aturan gagal; 3.229 halaman, 18 kampus); 17 dari 28 (61%) bertag, 16 dari 17 di antaranya berasal dari Word/PowerPoint; 1 dari 28 bermetadata LaTeX", "Audit awal penulis (Lampiran C)", "Audit awal (sampel tidak acak)"],
       ["Audit awal penulis: elemen *Figure*, bahasa, dan tabel", "29 dari 1.111 elemen *Figure* memiliki teks alternatif (2,6%); 6 dari 24 dokumen berbahasa Indonesia mendeklarasikan bahasa Indonesia (9 Inggris, 9 tanpa deklarasi); 1 dari 13 dokumen bertabel memiliki sel judul (318 tabel)", "Audit awal penulis", "Audit awal (sampel tidak acak)"],
       ["Akurasi VLM pada grafik ilmiah dan pada tanya-jawab visual berbahasa Indonesia", "Grafik ilmiah: GPT-4o 47,1%, model terbuka terbaik 29,2%, manusia 80,5%; tanya-jawab visual: 43,61%", "CharXiv [@charxiv]; SEA-Vision [@sea]", "*Benchmark*"]],
      [4.2, 6.6, 4.4, 3.0])
p("VLM tampak menjanjikan untuk membangkitkan teks alternatif, tetapi keandalannya terbatas: pada tugas geometri "
  "sederhana, VLM mutakhir hanya mencapai akurasi rata-rata 58,07% [@blind], dan pengguna tunanetra sendiri melaporkan "
  "ketidakakuratan serta halusinasi pada alat deskripsi berbasis AI [@adnin]. Oleh karena itu, yang dibutuhkan bukan "
  "sekadar model yang menghasilkan deskripsi, melainkan alur yang membuktikan bahwa suatu deskripsi setia pada "
  "datanya dan menahan deskripsi yang tidak dapat dibuktikan.")
p("Masalah yang sama dialami mahasiswa lain yang memilih mendengarkan. Indonesia memiliki proporsi pendengar podcast "
  "mingguan tertinggi di antara negara yang diukur, yaitu 42,6% pengguna internet berusia 16 tahun ke atas pada awal 2025 "
  "[@podcast]. Alat bacaan suara (*text-to-speech*, TTS) pun hanya membacakan teks yang tersedia dalam berkas, sehingga "
  "grafik, rumus, dan tabel tanpa teks alternatif terlewat. Kebiasaan mendengarkan ini merupakan indikator preferensi, "
  "bukan bukti bahwa mendengarkan meningkatkan hasil belajar: teori gaya belajar (auditori, visual, kinestetik) tidak "
  "didukung bukti yang memadai [@pashler]. Dasar yang lebih kuat adalah akses dan pilihan. Kerangka Universal Design for "
  "Learning menganjurkan beragam cara penyajian informasi [@cast], efek *curb-cut* menunjukkan bahwa fitur yang "
  "dirancang bagi kelompok rentan sering bermanfaat bagi banyak orang [@blackwell], dan meta-analisis 22 studi "
  "menemukan bahwa alat bacaan suara meningkatkan pemahaman bacaan siswa dengan kesulitan membaca (ukuran efek 0,35) "
  "[@wood]. Karena itu, penelitian ini menempatkan mahasiswa tunanetra sebagai pengguna utama, sedangkan manfaat bagi "
  "mahasiswa yang mendengarkan diperlakukan sebagai hipotesis.")
p("Kesenjangan ini terletak pada perangkat, bukan pada saluran: ULD telah ada, tetapi kemampuan teknisnya belum. Produksi "
  "materi aksesibel, baik oleh staf ULD maupun lembaga seperti Yayasan Mitra Netra, masih bertumpu pada tenaga manusia "
  "dan berbiaya tinggi [@mitranetra,@tempo]. Studi pada staf unit layanan disabilitas menunjukkan bahwa AI generatif "
  "meningkatkan kecepatan dan kepercayaan diri mereka dalam menulis deskripsi gambar, tetapi alur kerja bersama AI masih "
  "menjadi kendala [@raees]. " + NS + " (Sistem Ilustrasi Materi Aksesibel untuk Kuliah) dirancang untuk kondisi tersebut: "
  "mesin mengerjakan bagian yang dapat diverifikasi, sedangkan manusia memutuskan bagian yang tidak. Nama sistem ini "
  "diambil dari kata “simak”, yang berarti mendengarkan atau memperhatikan dengan saksama, sesuai dengan gagasannya: "
  "materi kuliah yang dapat disimak tanpa ada yang terlewat. Sistem ini menjawab subfokus aksesibilitas materi pada "
  "tema Innovation Case Competition (ICC).")
h2("Profil Pengguna")
p("Tabel {T:profil} memetakan empat profil yang terlibat. Pengguna utama dan operator menjadi dasar perancangan dan "
  "evaluasi; profil sekunder dicatat sebagai hipotesis yang belum diuji.")
table("profil", "Tabel {T:profil}. Profil pengguna, kebutuhannya, peran " + NS + ", dan status buktinya",
      ["Profil", "Kebutuhan pada materi PDF", "Peran " + NS, "Dasar dan status bukti"],
      [["Mahasiswa tunanetra (pengguna utama)", "Teks alternatif informatif, urutan baca benar, tabel berjudul kolom, rumus dapat diucapkan, dan bahasa dokumen benar bagi pembaca layar", "Menerima HTML aksesibel dan PDF bertag dengan penanda “dihasilkan otomatis” atau “disetujui ULD”", "1.727 mahasiswa [@detik]; kebutuhan terukur pada audit awal; uji pengguna (G7) ditunda"],
       ["Staf ULD (operator dan peninjau)", "Menghasilkan materi aksesibel dengan cepat dan mengendalikan keluaran AI [@raees]", "Mengunggah materi, meninjau antrean elemen yang ditahan, lalu menyetujui atau memperbaikinya", "Peran hukum [@uu8,@permen48]; beban tinjauan *R* dilaporkan (G6)"],
       ["Dosen atau pembuat materi", "Tetap membuat materi di Word atau PowerPoint", "Materi diunggah apa adanya, tanpa berkas sumber", "16 dari 17 dokumen bertag berasal dari Word/PowerPoint (audit awal)"],
       ["Mahasiswa pendengar (pengguna sekunder)", "Materi yang dibacakan tidak kehilangan grafik, rumus, dan tabel", "Mode dengar pada keluaran HTML dengan suara bahasa Indonesia (OUT-02)", "Kebiasaan podcast 42,6% [@podcast]; TTS membantu pembaca dengan kesulitan membaca [@wood]; hipotesis, belum diuji"]],
      [3.4, 5.2, 5.2, 4.4])

h2("Rumusan Masalah")
B.append(dict(kind="list", items=[
  "Bagaimana mengubah materi kuliah PDF berbahasa Indonesia yang memuat teks, tabel, grafik, dan rumus menjadi dokumen "
  "berstruktur dengan urutan baca yang benar bagi pembaca layar?",
  "Bagaimana menghasilkan deskripsi grafik dan pembacaan rumus berbahasa Indonesia yang setia pada data sumbernya?",
  "Bagaimana merancang alur kerja yang menahan keluaran yang tidak dapat diverifikasi dan menyerahkannya kepada peninjau "
  "ULD sehingga tidak ada deskripsi keliru yang terbit tanpa penanda?"]))

h2("Tujuan, Kontribusi, dan Manfaat")
p("Berdasarkan rumusan masalah tersebut, penelitian ini bertujuan merancang dan mengevaluasi " + NS + ". Setiap rumusan "
  "masalah dijawab oleh satu kontribusi utama: (i) perakitan keluaran aksesibel (PDF bertag dan HTML dengan mode dengar) "
  "yang melengkapi hasil analisis tata letak dan penandaan otomatis (*auto-tag*) hingga memenuhi PDF/UA-1, dengan sasaran "
  "celah terbesar hasil audit, yaitu teks alternatif, bahasa dokumen, dan sel judul tabel; (ii) modul deskripsi grafik "
  "yang berpijak pada tabel data dengan statistik yang dihitung oleh kode, serta pembacaan rumus melalui MathCAT; dan "
  "(iii) gerbang verifikasi *fail-closed* beserta antarmuka tinjauan bagi ULD. Dua kontribusi pendukung adalah (iv) "
  "protokol evaluasi tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian dan dapat dijalankan tanpa "
  "pengguna, serta (v) data audit awal atas materi kuliah berbahasa Indonesia. Kebaruan yang diklaim terbatas pada "
  "cakupan (materi berbahasa Indonesia dari PDF tanpa berkas sumber) dan sifat keluaran (setiap deskripsi terverifikasi "
  "atau ditandai), bukan pada penandaan otomatis itu sendiri. Tabel {T:manfaat} menyatakan manfaat yang dijanjikan "
  "beserta ukuran pembuktinya dan status buktinya hari ini; manfaat yang belum diukur dinyatakan sebagai belum diukur.")
table("manfaat", "Tabel {T:manfaat}. Manfaat yang dijanjikan, ukuran pembuktinya, dan status buktinya hari ini",
      ["Janji kepada pengguna", "Ukuran pembukti", "Status"],
      [["Setiap gambar, grafik, dan rumus beralternatif teks atau berstatus “ditahan”", "Proporsi elemen tanpa status (G1, G6)", "Rancangan; belum diukur"],
       ["Angka pada deskripsi grafik tidak dikarang", "*F*_{k} terhadap tabel acuan dan proporsi deskripsi berangka diubah yang tertahan (G3)", "Belum diukur; rancangan awal diperbaiki (Tabel {T:kelayakan})"],
       ["Grafik, rumus, dan tabel dapat disimak tanpa melihat", "Rasio *Q* akurasi tanya-jawab dari teks alternatif (G4); aturan ucapan MathCAT dan kecocokan rumus (G5)", "Belum diukur; bagi pendengar nontunanetra berupa hipotesis"],
       ["Bahasa, judul, dan struktur dokumen benar bagi pembaca layar", "Kegagalan aturan teks alternatif bermakna, bahasa, dan judul pada veraPDF (G1); kondisi awal 0 dari 28 lulus", "Kondisi awal terukur; perakitan teruji awal (Tabel {T:kelayakan}); hasil sistem belum diukur"],
       ["Keputusan tetap di tangan ULD; dokumen tidak disimpan; mahasiswa lebih mandiri", "Status “dihasilkan otomatis” atau “antrean tinjauan”; beban tinjauan *R* (G6); waktu tugas mahasiswa (G7)", "Rancangan; G7 ditunda"]],
      [5.6, 8.0, 4.6])
h2("Batasan")
p("Penelitian ini memiliki tujuh batasan. Pertama, belum ada uji pada mahasiswa tunanetra; klaim dampak belajar tidak "
  "dibuat dan uji tersebut dirancang sebagai gerbang G7. Kedua, sasaran utama adalah pembaca layar; manfaat bagi "
  "mahasiswa yang mendengarkan merupakan hipotesis yang belum diuji, dan kebutuhan pengguna *low vision* dan tuli belum "
  "tercakup. Ketiga, masukan berupa PDF berlapis teks dan berbahasa Indonesia; PDF hasil pindai ditolak untuk ditangani "
  "secara manual, dan berkas PowerPoint diekspor ke PDF lebih dahulu. Keempat, deskripsi grafik dibatasi pada level 1–3 "
  "model Lundgard dan Satyanarayan [@lundgard]; foto dan diagram nondata tanpa acuan pemeriksaan selalu ditinjau oleh "
  "manusia. Kelima, audit awal berasal dari pencarian repositori publik dan bukan sampel acak, sedangkan uji kelayakan "
  "awal hanya mencakup tiga dokumen contoh; angkanya tidak mewakili seluruh kampus. Keenam, kelulusan veraPDF menjamin "
  "terpenuhinya aturan yang dapat diperiksa mesin, tetapi bukan bukti bahwa dokumen nyaman dipakai dengan pembaca layar. "
  "Ketujuh, " + NS + " adalah alat bantu ULD dan bukan pengganti tenaga ahli.")
# ================================================================= II. TINJAUAN PUSTAKA
h1("TINJAUAN PUSTAKA")
h2("Standar dan Kondisi Aksesibilitas Dokumen")
p("WCAG 2.2 mensyaratkan alternatif teks yang setara fungsinya bagi konten nonteks (SC 1.1.1) [@wcag], sedangkan PDF/UA "
  "(ISO 14289) menetapkan persyaratan PDF bertag yang dapat dibaca teknologi bantu. veraPDF adalah validator sumber "
  "terbuka yang menerapkan aturan tersebut, tetapi hanya memeriksa kondisi yang dapat diperiksa mesin [@verapdf]: "
  "keberadaan teks alternatif terdeteksi, sedangkan kebenarannya tidak. Kondisi dokumen di lapangan telah diukur pada "
  "makalah ilmiah [@wang21,@kumar24]; di Indonesia, yang terukur baru situs web perguruan tinggi (sekitar 95% "
  "bermasalah aksesibilitas menurut ulasan atas studi di *Indonesian Journal of Disability Studies*) [@mahalli], bukan "
  "materi kuliah. Kumar dkk. membangun tolok ukur PDF beranotasi pakar dan menemukan bahwa *large language model* (LLM) "
  "terbaik mencapai akurasi 0,85 pada penilaian aksesibilitas, tetapi lemah pada kualitas teks alternatif; mereka "
  "menyarankan pendekatan hibrida yang memadukan pemeriksa berbasis aturan, LLM, dan penilaian manusia [@kumarbench]. "
  "Rancangan evaluasi penelitian ini mengikuti saran tersebut. Uji awal penulis (Tabel {T:kelayakan}) menunjukkan "
  "konsekuensi praktisnya: *auto-tag* sumber terbuka mengisi teks alternatif dengan teks pengisi (*placeholder*) seperti "
  "“image 1”, dan teks itu tetap dinyatakan lulus oleh veraPDF.")
h2("Deskripsi Visual dan Batas Model Vision-Language")
p("Lundgard dan Satyanarayan [@lundgard] menyusun model empat level isi semantik deskripsi visualisasi dari analisis "
  "2.147 kalimat: level 1 (sifat elemental, misalnya jenis grafik dan sumbu), level 2 (konsep statistik, misalnya nilai "
  "ekstrem dan rerata), level 3 (fenomena perseptual, misalnya tren dan pola), dan level 4 (wawasan kontekstual); "
  "pembaca tunanetra maupun awas dilaporkan paling terbantu oleh level 3. Jung dkk. [@jung] mendapati dari wawancara "
  "dengan 22 orang berhambatan penglihatan bahwa praktik penulisan teks alternatif hanya sebagian sesuai pedoman, dan "
  "Chintalapati dkk. [@chinta] menemukan cakupan level 2 dan 3 yang rendah pada teks alternatif publikasi (Tabel "
  "{T:bukti}). VisText menyediakan 12.441 grafik beserta tabel data dan keterangan (*caption*) berlevel [@vistext]; "
  "keberadaan tabel data memungkinkan angka pada deskripsi dicocokkan dengan sumbernya.")
p("Di sisi model, kemampuan VLM memahami grafik masih jauh di bawah manusia, dan perubahan kecil pada grafik atau soal dapat "
  "menurunkan performa hingga 34,5% [@charxiv]. Untuk bahasa Indonesia, SEA-Vision melaporkan penurunan akurasi "
  "tanya-jawab visual [@sea] dan IndoTabVQA menunjukkan celah pada pemahaman tabel [@indotab]. Pengguna tunanetra "
  "menghadapi halusinasi dan membentuk model mental yang sering keliru tentang cara kerja alat tersebut [@adnin]. Bukti "
  "ini mendasari dua keputusan rancangan: deskripsi harus berpijak pada data yang dapat diperiksa, dan keluaran yang "
  "tidak dapat diperiksa tidak boleh terbit tanpa penanda.")
h2("Landasan Model Usulan dan Persamaan Kunci")
p("*Struktur dokumen dan urutan baca.* OpenDataLoader PDF [@odl] adalah pustaka sumber terbuka berlisensi Apache 2.0 yang "
  "menganalisis tata letak secara deterministik, menghasilkan JSON dengan kotak pembatas setiap elemen, dan mengeluarkan "
  "PDF bertag dari PDF tidak bertag tanpa GPU. Docling menyediakan alternatif berbasis model (DocLayNet [@doclaynet] dan "
  "TableFormer [@tableformer]) yang dilaporkan berjalan pada perangkat biasa [@docling]. Penelitian ini memakai "
  "OpenDataLoader sebagai tulang punggung karena telah menghasilkan PDF bertag, dan Docling hanya bila tabel tanpa garis "
  "tidak terbaca pada dokumen nyata. Kesesuaian urutan baca hasil sistem terhadap acuan pada *n* blok diukur dengan "
  "korelasi peringkat Kendall [@kendall],")
eq("tau", r"\tau=\frac{C-D}{n(n-1)/2}", "Korelasi peringkat Kendall untuk urutan baca (G2)", end=",")
pc("dengan *C* dan *D* masing-masing adalah jumlah pasangan blok yang urutannya sepakat dan bertentangan dengan acuan.")
p("*Ekstraksi tabel data dan statistik grafik.* DePlot menguraikan penalaran visual menjadi penerjemahan grafik ke tabel "
  "lalu penalaran atas tabel [@deplot]; kandidat VLM untuk langkah ini adalah model terbuka seperti Qwen2.5-VL [@qwen25vl] "
  "dan model komersial yang dievaluasi pada CharXiv [@charxiv]. Karena ekstraksi dapat keliru, tabel data diekstraksi "
  "dua kali menjadi *T*_{1} dan *T*_{2}. Dengan *t*_{1} dan *t*_{2} nilai kedua ekstraksi itu untuk titik data *t*, |*T*| "
  "banyaknya titik data, dan *s* rentang nilai (selisih nilai maksimum dan minimum gabungan *T*_{1} dan *T*_{2}), selisih "
  "relatif kedua ekstraksi dinyatakan sebagai")
eq("delta", r"\delta(T_1,T_2)=\frac{1}{|T|}\sum_{t\in T}\frac{|t_1-t_2|}{s}", "Selisih relatif antar-ekstraksi tabel data terhadap rentang nilai s", end=".")
pc("Bila *s* = 0, *δ* bernilai 0 jika kedua ekstraksi identik dan 1 jika tidak; nilai *δ* harus kecil agar tabel diterima. "
   "Statistik yang dilaporkan dihitung oleh kode, bukan oleh model. Untuk *n* titik (*x*_{*i*}, *y*_{*i*}) dengan rerata "
   "*x̄* dan *ȳ*, kemiringan kuadrat terkecil dan perubahan terfit dihitung sebagai")
eq("slope", r"\hat{\beta}=\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sum_{i=1}^{n}(x_i-\bar{x})^2}", "Kemiringan regresi linear kuadrat terkecil", end=",")
eq("Delta", r"\hat{\Delta}=\hat{\beta}\,(x_n-x_1)", "Perubahan terfit sepanjang sumbu", end=".")
pc("Tren dilabeli naik bila *Δ̂* ≥ *ρ*(maks *y* − min *y*), turun bila *Δ̂* ≤ −*ρ*(maks *y* − min *y*), dan tidak jelas di luar "
   "itu, dengan *ρ* ambang relatif. Deskripsi akhir *d* dibangun dari templat yang diisi fakta terstruktur. Tiap fakta "
   "berbentuk klaim (*e*, *m*, *v*), yaitu entitas *e* (misalnya kategori pada sumbu-*x*), ukuran *m* (misalnya nilai, "
   "maksimum, atau selisih), dan nilai *v*. Himpunan klaim *Λ*(*d*) dibaca langsung dari isian templat, bukan dari "
   "pemindaian angka pada kalimat. Sebuah klaim setia bila tabel data *T* atau himpunan fakta turunan *D*(*T*) yang "
   "dihitung kode memuat entitas dan ukuran yang sama dengan nilai *v*′ yang selisihnya dari *v* tidak melebihi *ε* kali "
   "rentang nilai *s* = maks *T* − min *T*. Proporsi klaim setia dinyatakan sebagai")
eq("fklaim", r"F_{\mathrm{k}}(d,T)=\frac{\left|\left\{(e,m,v)\in\Lambda(d):\ \exists\,(e,m,v')\in T\cup D(T),\ |v-v'|\le\epsilon\,s\right\}\right|}{|\Lambda(d)|}", "Kesetiaan klaim deskripsi terhadap tabel data (gerbang dan G3)", end=".")
p("Persamaan {E:fklaim} dipakai dengan dua tabel berbeda: *T* hasil ekstraksi sebagai pemeriksa gerbang, dan tabel acuan "
  "*T*_{acuan} sebagai metrik G3. Nilai yang dilaporkan pada G3 selalu terhadap *T*_{acuan}, sebab terhadap *T* nilainya 1 "
  "menurut definisi pada keluaran yang terbit. Ekstraksi ganda hanya menangkap kesalahan acak. Kesalahan sistematik, "
  "misalnya salah membaca skala sumbu pada kedua ekstraksi, ditangani pemeriksaan tambahan *c*_{A}, yaitu nilai *T* harus "
  "berada dalam rentang label tik sumbu yang dibaca secara terpisah; sisanya ditangani antrean tinjauan.")
p("*Pengenalan rumus dan ucapan.* UniMERNet mengubah citra ekspresi matematika pada kondisi dunia nyata menjadi LaTeX "
  "[@unimer]. MathCAT mengubah *Mathematical Markup Language* (MathML) menjadi ucapan (gaya ClearSpeak dan SimpleSpeak) "
  "dan braille serta menyediakan aturan bahasa Indonesia [@mathcat,@mathcatrepo]. Hasil pengenalan tidak diverifikasi "
  "dengan membandingkan citra hasil render ulang terhadap citra asli. Uji awal pada lima rumus menunjukkan bahwa indeks "
  "kemiripan struktural (SSIM) [@ssim] didominasi perbedaan font: skor rumus benar berfont berbeda (0,65–0,87) lebih "
  "rendah daripada skor rumus salah berfont sama (0,97–0,99), seperti terlihat pada Tabel {T:kelayakan}. Rumus karena itu "
  "diverifikasi melalui kesepakatan dua pengenal independen, yang diukur dengan kecocokan berbasis jarak sunting "
  "Levenshtein (*ED*) [@levenshtein] antara dua *string* LaTeX *L̂* dan *L* (kedua pengenal, atau pengenal dan acuan pada "
  "evaluasi), yaitu")
eq("ed", r"A(\hat{L},L)=1-\frac{\mathrm{ED}(\hat{L},L)}{\max(|\hat{L}|,|L|)}", "Kecocokan LaTeX berbasis jarak sunting (kesepakatan pengenal dan G5)", end=".")
p("*Gerbang verifikasi.* Setiap elemen *e* memiliki himpunan pemeriksaan *K*(*e*) menurut jenisnya: untuk grafik, *c*_{F} "
  "(*F*_{k} = 1), *c*_{δ} (*δ* ≤ *θ*_{e}), dan *c*_{A} (rentang sumbu); untuk rumus, *c*_{R} (*A* ≥ *θ*_{r}) antara dua pengenal; "
  "foto dan diagram nondata tidak memiliki pemeriksaan sehingga *K*(*e*) = ∅. Elemen terbit otomatis hanya jika")
eq("gate", r"\mathrm{pub}(e)=\mathbf{1}\left[K(e)\neq\emptyset\right]\prod_{k\in K(e)}c_k(e)=1", "Aturan penerbitan gerbang fail-closed", end=",")
pc("dengan 1[·] fungsi indikator dan *c*_{*k*}(*e*) bernilai 1 bila pemeriksaan *k* lulus. Kesepakatan dua pengenal tidak menjamin "
   "kebenaran karena keduanya dapat keliru bersama; kebenaran diukur terhadap LaTeX acuan pada G5.")
p("*Metrik evaluasi.* Proporsi dilaporkan dengan selang kepercayaan Wilson [@wilson],")
eq("wilson", r"\frac{\hat{p}+z^2/(2n)\pm z\sqrt{\hat{p}(1-\hat{p})/n+z^2/(4n^2)}}{1+z^2/n}", "Selang kepercayaan Wilson untuk proporsi", end=",")
pc("dengan *p̂* proporsi teramati, *n* ukuran sampel, dan *z* kuantil normal baku. Kesepakatan dua penilai diukur dengan "
   "kappa Cohen [@cohen],")
eq("kappa", r"\kappa=\frac{p_o-p_e}{1-p_e}", "Kappa Cohen antar-penilai (G6)", end=",")
pc("dengan *p*_{o} kesepakatan teramati dan *p*_{e} kesepakatan kebetulan. Kesetaraan informasi (G4) dan beban tinjauan (G6) "
   "didefinisikan sebagai")
eq("ratio", r"Q=\frac{\mathrm{Acc}_{\mathrm{alt}}}{\mathrm{Acc}_{\mathrm{tab}}},\qquad R=\frac{|E_{\mathrm{tinjau}}|}{|E|}", "Rasio kesetaraan informasi Q dan beban tinjauan R", end=",")
pc("dengan Acc_{alt} dan Acc_{tab} akurasi menjawab pertanyaan hanya dari teks alternatif dan dari tabel data, serta "
   "*E*_{tinjau} himpunan elemen yang masuk antrean tinjauan dari seluruh elemen *E*.")

h2("Solusi yang Sudah Ada dan Titik Berhentinya")
p("Tabel {T:solusi} merangkum solusi terdekat; sel diisi hanya dengan apa yang dilaporkan sumbernya atau diamati langsung "
  "oleh penulis.")
table("solusi", "Tabel {T:solusi}. Solusi yang ada dan titik berhentinya",
      ["Solusi", "Masukan", "Yang dikerjakan", "Titik berhenti"],
      [["PAVE 2.0 [@pave]", "PDF ilmiah", "Remediasi langkah demi langkah; skor tag naik dari 42,0% ke 80,1% (ahli) dan 39,2% ke 75,2% (pemula) dibanding Acrobat Pro", "Bergantung pada kerja manual pengguna"],
       ["SciA11y; HTML arXiv [@wang21,@arxivhtml]", "PDF ilmiah; sumber LaTeX", "Konversi ke HTML aksesibel dengan navigasi", "Naskah ilmiah; HTML arXiv bergantung pada sumber LaTeX"],
       ["iTagPDF [@itag]", "PDF + sumber LaTeX", "Tag dan urutan baca akurat; agen LLM mendeskripsikan gambar bila penulis belum", "Memerlukan sumber LaTeX; bahasa Indonesia tidak dilaporkan"],
       ["OpenDataLoader PDF [@odl]", "PDF", "*Auto-tag* gratis; JSON berkotak pembatas; deskripsi AI untuk gambar/grafik dan ekstraksi rumus ke LaTeX (mode *hybrid*)", "Ekspor PDF/UA berbayar; pada uji awal penulis (2 dokumen) teks alternatif berisi teks pengisi “image N” yang lolos veraPDF, tanpa sel judul (TH), tag rumus, dan bahasa dokumen; verifikasi terhadap data grafik tidak dilaporkan"],
       ["Adobe Auto-Tag [@adobe,@abilitynet]", "PDF", "Penandaan otomatis berbasis *cloud*", "Produk komersial; tabel kompleks, urutan baca, dan level judul perlu koreksi manual"],
       ["MathCAT [@mathcat]", "MathML", "Ucapan (ClearSpeak/SimpleSpeak) dan braille; mendukung bahasa Indonesia", "Membutuhkan MathML; tidak mengenali rumus dari PDF atau gambar; tidak ditemukan sebagai paket pip"],
       ["veraPDF [@verapdf]", "PDF", "Validasi PDF/UA", "Hanya kondisi yang dapat diperiksa mesin; tidak menilai kebenaran teks alternatif"]],
      [3.4, 2.4, 6.0, 6.4])

h2("Kesenjangan dan Posisi Solusi")
fig("impl", "Gambar_Alur_Implementasi.png",
    "Gambar {G:impl}. Alur implementasi model: alur ringkas (atas) dan rincian pipeline remediasi (bawah).",
    "Diagram alur implementasi. Materi kuliah PDF diunggah, diproses sistem remediasi, lalu gerbang verifikasi memutuskan apakah "
    "elemen terbit otomatis atau masuk antrean tinjauan staf ULD. Rincian: analisis tata letak dan auto-tag, perutean elemen ke jalur teks, "
    "grafik, dan rumus, verifikasi klaim atau kesepakatan dua pengenal, gerbang verifikasi, perakitan, validasi veraPDF, dan keluaran HTML serta PDF bertag.")

p("Ringkasnya, alat remediasi yang ada bergantung pada kerja manual [@pave] atau pada sumber LaTeX [@itag,@arxivhtml]; "
  "sistem otomatis yang ditinjau (dokumentasi OpenDataLoader dan abstrak iTagPDF) tidak melaporkan verifikasi deskripsi "
  "terhadap data grafik; dan tidak satu pun sumber yang ditinjau melaporkan evaluasi pada materi kuliah berbahasa "
  "Indonesia. Pada sampel audit, hanya 1 dari 28 dokumen yang metadatanya menunjukkan LaTeX, sedangkan 16 dari 17 dokumen "
  "bertag berasal dari Word atau PowerPoint. Hal ini mengindikasikan, tetapi belum membuktikan, bahwa metode yang "
  "bergantung pada sumber LaTeX tidak menjangkau sumber materi terbesar di kampus. " + NS + " mengambil tiga posisi: "
  "(1) masukan berupa PDF apa adanya tanpa berkas sumber, (2) deskripsi grafik yang berpijak pada tabel data dengan "
  "statistik yang dihitung kode dan diperiksa gerbang pada tingkat klaim, dan (3) ULD sebagai peninjau untuk elemen yang "
  "tidak dapat diverifikasi. Sistem ini dibangun di atas *auto-tag* sumber terbuka dan tidak mengklaim akurasi lebih "
  "tinggi daripada sistem-sistem tersebut; klaimnya terbatas pada cakupan dan sifat keluaran (setiap deskripsi "
  "terverifikasi atau ditandai).")
# ================================================================= III. METODOLOGI
h1("METODOLOGI")
h2("Gambaran Solusi dan Alur Implementasi")
p("Gambar {G:impl} memperlihatkan alur implementasi. Staf ULD atau dosen mengunggah materi kuliah PDF. Sistem "
  "menghasilkan keluaran aksesibel berupa HTML dan PDF bertag, kemudian memutuskan per elemen apakah keluaran tersebut "
  "lolos gerbang verifikasi. Elemen yang lolos diterbitkan dengan penanda “dihasilkan otomatis”; elemen yang tidak "
  "lolos ditahan dalam antrean tinjauan ULD dan baru diterbitkan setelah disetujui atau diperbaiki. Pemilihan ULD "
  "sebagai operator mengikuti peran hukumnya [@uu8,@permen48] dan temuan bahwa staf unit layanan disabilitas "
  "membutuhkan kendali atas keluaran AI [@raees].")
h2("Arsitektur dan Implementasi Teknis")
p(NS + " dibangun sebagai aplikasi web tiga lapis; Lampiran E merinci antarmuka dan sumber dayanya. Lapisan antarmuka "
  "berupa halaman web statis untuk unggah, tinjauan, dan pemutaran keluaran. Lapisan layanan berupa aplikasi Python "
  "(FastAPI) dengan antrean kerja yang memanggil pemroses dokumen, yaitu OpenDataLoader [@odl] (Java 11 atau lebih baru), "
  "pikepdf dan PyMuPDF untuk menambal pohon struktur PDF, serta veraPDF [@verapdf] untuk validasi. Lapisan model berupa "
  "adaptor VLM yang tidak terikat penyedia sehingga model komersial dapat diganti model terbuka lokal. Setiap elemen "
  "dokumen direpresentasikan sebagai satu rekaman JSON berisi halaman, kotak pembatas, jenis, tabel data, klaim, hasil "
  "pemeriksaan, dan status, sehingga gerbang, antarmuka tinjauan, dan perakit keluaran memakai satu model data. Uji "
  "kelayakan awal pada perangkat tanpa GPU (RAM 15 GB) memproses 21 halaman dalam 4,6 detik (Tabel {T:kelayakan}), "
  "sehingga penerapan pada satu server CPU biasa atau laptop dinilai layak. Keluaran HTML memuat mode dengar berbasis Web "
  "Speech API; suara bahasa Indonesia (Microsoft Andika, id-ID) terpasang pada sistem uji, sedangkan ketersediaannya pada "
  "peramban pengguna diuji pada tahap implementasi.")

h2("Alur Penelitian")
fig("pen", "Gambar_Alur_Penelitian.png",
    "Gambar {G:pen}. Alur penelitian: pengumpulan data, pemisahan set, pengembangan pipeline, dan evaluasi dengan kriteria lulus terkunci.",
    "Diagram alur penelitian. Empat sumber data dipisah menjadi set pengembangan dan set uji tertahan. Pipeline dikembangkan pada set "
    "pengembangan, dievaluasi pada gerbang G1 sampai G6 terhadap tiga pembanding pada set uji tertahan, dianalisis kesalahannya "
    "secara iteratif, lalu dibekukan. Uji pengguna G7 ditunda.")

p("Gambar {G:pen} memperlihatkan alur penelitian. Data dikumpulkan dari empat sumber, lalu dipisah menjadi set "
  "pengembangan dan set uji tertahan (*held-out*) sebelum pengembangan dimulai; set uji tertahan tidak dipakai untuk "
  "menyetel komponen, ambang, atau perintah model. " + NS + " (selanjutnya sistem D) dan tiga pembanding dievaluasi pada "
  "gerbang evaluasi; kesalahan dianalisis dan diperbaiki pada set pengembangan, sedangkan versi yang dibekukan baru "
  "dievaluasi pada set uji tertahan. Karena keluaran VLM tidak deterministik, versi akhir dijalankan dua kali dan "
  "selisihnya dilaporkan, dengan versi model, *hash* perintah, dan ambang tercatat dalam manifes.")
h2("Dataset dan Sumber Acuan")
p("Tabel {T:data} merinci seluruh data. Tiga sumber acuan dipakai: dokumen sintetis buatan penulis dari sumber "
  "berstruktur sehingga urutan baca, tabel, letak gambar, dan angka grafiknya diketahui; VisText [@vistext], yang "
  "berbahasa Inggris sehingga hanya menguji komponen; dan audit dokumen nyata untuk menjawab risiko bahwa dokumen "
  "sintetis lebih rapi daripada materi kuliah sebenarnya. Audit awal hanya memakai metadata dan struktur berkas publik "
  "dan dilaporkan secara agregat.")
table("data", "Tabel {T:data}. Dataset yang dipakai, akses, ukuran, dan perannya",
      ["Dataset", "Akses/lisensi", "Ukuran", "Peran dalam penelitian"],
      [["Audit awal materi kuliah", "Tautan publik; berkas tidak disebarluaskan", "28 PDF; 3.229 halaman; 18 kampus (terukur)", "Bukti urgensi; contoh awal set nyata"],
       ["Materi kuliah nyata (G6)", "Berlisensi terbuka dan materi milik penulis", "20–30 dokumen PDF/PPT (target)", "Set uji dokumen nyata: G1, G3, G6"],
       ["Set sintetis buatan penulis (Word/LaTeX ke PDF; grafik berbahasa Indonesia; ekspresi rumus)", "Dibuat penulis", "30 dokumen, 150 grafik lima jenis, 200 ekspresi rumus (target)", "Acuan urutan baca dan tabel (G2), angka dan pertanyaan (G3, G4), pengenalan rumus (G5)"],
       ["VisText [@vistext]", "Repositori publik (GPL-3.0)", "12.441 grafik dengan tabel data dan *caption*", "Uji komponen grafik (bahasa Inggris): G3"]],
      [4.4, 4.2, 4.8, 4.8])
h2("Kerangka Pemodelan dan Fitur")
fig("kerangka", "Gambar_Kerangka_Tujuh_Langkah.png",
    "Gambar {G:kerangka}. Kerangka tujuh langkah untuk setiap fitur, terisi untuk fitur deskripsi grafik.",
    "Diagram tujuh langkah berurutan: masalah, masukan, praproses, model atau metode, inferensi, keluaran, status dan bukti, "
    "dengan contoh pengisian untuk fitur deskripsi grafik.")
p("Setiap fitur AI dikembangkan dengan kerangka tujuh langkah yang sama: masalah, masukan, praproses, model atau "
  "metode, inferensi, keluaran, dan status beserta buktinya. Gambar {G:kerangka} mengisinya untuk fitur inti, yaitu "
  "deskripsi grafik, dan Tabel {T:fitur} merangkum sepuluh fitur beserta status buktinya; fitur yang belum dibangun "
  "dinyatakan sebagai rencana.")
table("fitur", "Tabel {T:fitur}. Fitur AI dan non-AI: model, keluaran, dan status buktinya",
      ["ID", "Fitur", "Model/metode", "Keluaran", "Status"],
      [["STR-01", "Struktur dan urutan baca", "OpenDataLoader [@odl]; Docling [@docling] bila tabel tanpa garis tidak terbaca", "Blok berurut; baris judul tabel (TH)", "*Auto-tag* teruji awal; integrasi 4–9 Okt."],
       ["CLS-01", "Klasifikasi jenis gambar", "Heuristik ukuran, *hash*, posisi; VLM *zero-shot*", "Grafik, tabel-citra, rumus, foto/diagram, dekoratif", "Rencana"],
       ["CHT-01", "Ekstraksi tabel data grafik", "VLM keluaran terstruktur, dua kali [@deplot,@qwen25vl]; Pers. {E:delta}; *c*_{A}", "Tabel *T*_{1}, *T*_{2}; status konsistensi", "Uji penentu 1–3 Okt.; pengembangan 10–15 Okt."],
       ["CHT-02", "Statistik dan kalimat", "Kode: maks, min, selisih, regresi Pers. {E:slope}, {E:Delta}; templat; VLM penyunting bertoken terkunci", "Deskripsi level 1–3", "Rencana"],
       ["FRM-01", "Pengenalan rumus", "UniMERNet [@unimer] dan pengenal kedua; Pers. {E:ed}", "LaTeX dan status kesepakatan", "Opsional (16–19 Okt.); tanpanya rumus ditinjau"],
       ["FRM-02", "Ucapan rumus", "MathCAT aturan Indonesia [@mathcat]; WebAssembly [@mathcatdemo]", "Teks ucapan", "Integrasi rencana"],
       ["GAT-01", "Gerbang verifikasi", "Aturan Pers. {E:gate}; klaim Pers. {E:fklaim}; ambang *θ*_{e}, *θ*_{r}", "Terbit atau tahan", "Rencana (10–15 Okt.)"],
       ["OUT-01", "Perakitan dan validasi", "Tag, teks alternatif, bahasa, judul, penanda PDF/UA; veraPDF [@verapdf]", "HTML aksesibel; PDF bertag; laporan PDF/UA-1", "Teruji awal pada 3 dokumen"],
       ["OUT-02", "Mode dengar", "Web Speech API dengan suara id-ID; teks alternatif, tabel berjudul, dan ucapan rumus dibacakan berurutan", "HTML yang dapat diputar dan dijeda per elemen", "Opsional (16–19 Okt.); suara id-ID tersedia pada sistem uji"],
       ["REV-01", "Antarmuka tinjauan ULD", "Aplikasi web minimal", "Keputusan terima, ubah, tolak", "Rencana (16–19 Okt.)"]],
      [1.3, 2.7, 6.2, 3.8, 4.2])
h2("Komponen Pipeline")
p("*Analisis tata letak dan perakitan keluaran.* Setiap blok diarahkan menurut jenisnya dan diurutkan; kesesuaian urutan "
  "diukur dengan Pers. {E:tau}. Untuk PDF yang sudah bertag (61% pada audit awal), pipeline memakai tag yang ada dan menambal "
  "teks alternatif, bahasa dokumen, dan judul. Untuk PDF tidak bertag, struktur dibangun oleh *auto-tag* OpenDataLoader "
  "[@odl], lalu dilengkapi dengan bahasa dokumen, judul, penanda PDF/UA, dan pemetaan baris judul tabel menjadi sel TH "
  "karena keluaran *auto-tag* tidak memuatnya (Tabel {T:kelayakan}). Hasil divalidasi dengan veraPDF; bila masih ada aturan "
  "struktural yang gagal, keluaran dibatasi pada HTML aksesibel dan kegagalannya dilaporkan.")
p("*Modul grafik.* Ekstraksi tabel data memakai keluaran terstruktur (skema JSON dengan kolom kategori dan nilai) dan suhu "
  "pengambilan sampel nol, dilakukan dua kali dengan perintah berbeda, dan harus konsisten menurut Pers. {E:delta}. Level 1 "
  "dibangun dari jenis grafik, judul, dan label sumbu; level 2 dari nilai maksimum, minimum, dan selisih yang dihitung "
  "kode; level 3 dari label tren menurut Pers. {E:slope} dan {E:Delta}. Kalimat dibangun dari templat bahasa Indonesia yang "
  "diisi fakta tersebut, dengan VLM hanya berwenang memilih urutan dan menyunting kelancaran bahasa tanpa mengubah "
  "token angka dan label, sehingga ruang model untuk mengarang angka dipersempit sejak awal. Setiap klaim pada "
  "deskripsi diperiksa oleh Pers. {E:fklaim}.")
p("*Modul rumus.* Citra rumus diubah menjadi LaTeX oleh dua pengenal independen, kemudian menjadi MathML dan diucapkan "
  "oleh MathCAT dengan aturan bahasa Indonesia. MathCAT dapat dijalankan di peramban melalui WebAssembly [@mathcatdemo] "
  "atau dibangun dari kode sumber [@mathcatrepo]; *binding* Python-nya tidak ditemukan sebagai paket pip. Karena MathCAT "
  "sudah mendukung bahasa Indonesia [@mathcat], kontribusi penelitian ini berada pada jalur dari PDF menuju MathML "
  "yang benar, bukan pada aturan ucapannya; kebenaran jalur itu diperiksa oleh kesepakatan kedua pengenal menurut "
  "Pers. {E:ed}. Selama pengenal kedua belum tersedia, seluruh rumus masuk antrean tinjauan.")
p("*Gerbang verifikasi, perakitan, dan tinjauan.* Elemen terbit otomatis hanya bila Pers. {E:gate} terpenuhi; kegagalan "
  "pemeriksaan mana pun menahan elemen, dan foto serta diagram nondata selalu masuk antrean tinjauan. Arah kegagalan "
  "ini dipilih dengan sengaja: penahanan terlihat oleh peninjau, sedangkan deskripsi keliru tidak. Antarmuka tinjauan "
  "menampilkan gambar halaman, tabel data hasil ekstraksi, dan draf deskripsi secara berdampingan dengan aksi terima, "
  "ubah, atau tolak.")
h2("Rancangan Evaluasi dan Kriteria Lulus Terkunci")
p("Sistem D dibandingkan dengan tiga pembanding: B0 (PDF asli tanpa remediasi), B1 (*auto-tag* sumber terbuka "
  "OpenDataLoader [@odl] tanpa modul tambahan, sehingga D terhadap B1 berfungsi sebagai ablasi kontribusi penelitian ini), "
  "dan B2 (VLM langsung tanpa gerbang). Tabel {T:gerbang} memuat tujuh gerbang; G1, G3, G4, dan G6 menjadi inti evaluasi "
  "final, G2 dan G5 dijalankan bila waktu memungkinkan, dan G7 ditunda. Pada G1, teks alternatif dianggap ada bila tidak "
  "kosong dan bukan teks pengisi (pola “image N”, nama berkas, atau kata tunggal seperti “gambar”). Ambang ditetapkan "
  "sebelum eksperimen pertama pada set uji tertahan dan tidak diubah setelah hasil terlihat; kegagalan pada satu gerbang "
  "dilaporkan apa adanya dan menghentikan klaim yang bersangkutan. Proporsi dilaporkan dengan selang pada Pers. {E:wilson}. "
  "LLM sebagai penilai hanya dipakai bila kesepakatannya dengan penilai manusia pada sampel, menurut Pers. {E:kappa}, telah "
  "diperiksa lebih dahulu [@kumarbench].")
table("gerbang", "Tabel {T:gerbang}. Tujuh gerbang evaluasi dan kriteria lulus yang dikunci sebelumnya",
      ["Gerbang", "Yang diuji", "Sumber acuan", "Ambang lulus*"],
      [["G1 Struktur dan metadata (inti)", "Aturan PDF/UA-1 yang gagal per dokumen; khusus teks alternatif bermakna (bukan teks pengisi), bahasa, judul", "veraPDF pada keluaran D, B0, B1", "≥ 90% dokumen uji bebas kegagalan teks alternatif, bahasa, dan judul; lebih baik dari B1"],
       ["G2 Urutan baca dan tabel", "Kesesuaian urutan baca *τ*, Pers. {E:tau}; struktur baris dan kolom judul tabel", "Dokumen sintetis dengan sumber diketahui", "*τ* ≥ 0,90"],
       ["G3 Kesetiaan angka (inti)", "*F*_{k}, Pers. {E:fklaim}, terhadap *T*_{acuan}; deskripsi dengan angka yang sengaja diubah yang tertahan", "Tabel data VisText dan grafik buatan penulis", "*F*_{k} ≥ 0,98 pada keluaran terbit; ≥ 0,90 deskripsi yang diubah tertahan"],
       ["G4 Kesetaraan informasi (inti)", "Rasio *Q*, Pers. {E:ratio}", "Pertanyaan otomatis dari tabel data", "*Q* ≥ 0,80"],
       ["G5 Rumus", "Kecocokan *A*, Pers. {E:ed}, terhadap LaTeX acuan; kesepakatan dua pengenal", "200 ekspresi bersumber LaTeX diketahui", "*A* ≥ 0,90"],
       ["G6 Dokumen nyata (inti)", "G1 dan G3 pada materi nyata; beban tinjauan *R*, Pers. {E:ratio}; kappa *κ*, Pers. {E:kappa}; pemeriksaan singkat dengan pembaca layar NVDA pada sampel keluaran", "Audit 20–30 dokumen dengan rubrik penulis", "G1 ≥ 80%; *κ* ≥ 0,60; *R* dilaporkan"],
       ["G7 Pengguna", "Ketepatan dan waktu tugas mahasiswa tunanetra; waktu kerja staf ULD", "Uji pengguna bersama ULD mitra", "Ditunda; kriteria disepakati bersama ULD sebelum uji"]],
      [2.8, 5.8, 4.2, 5.4],
      note="*Ambang awal yang dikunci sebelum eksperimen pertama pada set uji tertahan.")

h2("Uji Kelayakan Awal")
p("Sebelum rancangan dikunci, komponen berisiko diuji pada tiga dokumen contoh karya kompetisi (dua laporan dan satu berkas "
  "presentasi) dengan perangkat berspesifikasi umum (CPU tanpa GPU, RAM 15 GB). Tabel {T:kelayakan} merangkum hasilnya dan "
  "Lampiran D memuat protokolnya. Sampel yang kecil dan bukan materi kuliah membuat hasil ini menunjukkan kelayakan, bukan "
  "kinerja.")
p("Dua hal belum teruji: akurasi ekstraksi tabel data dari grafik oleh VLM dan kualitas keluaran pada materi kuliah asli. "
  "Keduanya menjadi uji penentu pada 1–3 Oktober. Bila ekstraksi tidak konsisten pada sebagian besar grafik uji, modul "
  "grafik beralih ke pembacaan data dari jalur vektor PDF atau seluruh grafik dimasukkan ke antrean tinjauan.")

table("kelayakan", "Tabel {T:kelayakan}. Hasil uji kelayakan awal dan konsekuensinya bagi rancangan",
      ["Uji", "Hasil", "Konsekuensi rancangan"],
      [["*Auto-tag* dan penambalan metadata: PDF tidak bertag (21 halaman) dan PDF bertag (113 elemen *Figure* tanpa teks alternatif)", "Aturan PDF/UA-1 yang gagal menurut veraPDF pada PDF tidak bertag: 11 (asli), 8 (setelah *auto-tag*, 4,6 detik), 0 (setelah penambalan). PDF bertag: 1 aturan (113 pemeriksaan) menjadi 0 dalam 0,38 detik", "Perakitan PDF bertag layak untuk dokumen sederhana"],
       ["*Auto-tag* pada berkas presentasi (43 salindia)", "10,5 detik; setelah penambalan tersisa 3 aturan struktural: level judul melompat, tipe struktur nonstandar, sel tabel bertumpuk", "Jalur cadangan HTML dipertahankan; level judul dan pemetaan peran diperbaiki"],
       ["Isi keluaran *auto-tag* (2 dokumen tidak bertag)", "Teks alternatif berupa teks pengisi “image N” yang lolos veraPDF; 0 sel TH dari 98 sel; tanpa tag rumus, bahasa, dan *MarkInfo*", "G1 mengecualikan teks pengisi; sel TH dan bahasa ditambahkan sendiri"],
       ["SSIM sebagai pemeriksa rumus (5 rumus, proksi font)", "Benar, font berbeda: 0,65–0,87; salah, font sama: 0,97–0,99; salah, font berbeda: 0,64–0,87", "SSIM tidak menjadi gerbang; rumus dinilai dari kesepakatan dua pengenal atau ditinjau manusia"],
       ["Suara bahasa Indonesia untuk mode dengar", "Suara Microsoft Andika (id-ID) terpasang pada Windows 11 uji; belum diuji pada peramban", "Mode dengar layak tanpa layanan berbayar; uji peramban pada tahap implementasi"],
       ["Pemeriksaan angka pada data buatan (versi awal)", "Pasangan label–nilai tertukar lolos; angka turunan yang benar ditolak; selisih ekstraksi bergantung satuan (0,073 vs 0,274 pada data yang sama)", "Verifikasi tingkat klaim, Pers. {E:fklaim}; selisih dinormalisasi terhadap rentang, Pers. {E:delta}"]],
      [4.4, 8.4, 5.4])
h2("Kelayakan, Alternatif, dan Rencana Kerja")
p("Analisis tata letak berjalan pada CPU biasa: Docling melaporkan 0,60–0,94 halaman per detik pada CPU Xeon 16 inti dengan "
  "OCR nonaktif [@docling], dan *auto-tag* OpenDataLoader memproses 21 halaman dalam 4,6 detik pada uji penulis. VLM hanya "
  "dipanggil per gambar nondekoratif. Pada audit awal, dokumen bertag memuat median 20 elemen *Figure* per dokumen "
  "(rentang 0–419), dan sebagian besar pada salindia kemungkinan dekoratif; gambar dekoratif karena itu disaring lebih "
  "dahulu berdasarkan ukuran, kemunculan berulang (*hash* citra), dan posisi. Penandaan dekoratif sebagai *Artifact* "
  "menuntut penyuntingan aliran konten PDF dan diuji pada pekan pertama. "
  "Enam alternatif ditolak: (1) melatih VLM sendiri, karena data berlabel berbahasa Indonesia yang memadai belum "
  "ditemukan; (2) menghasilkan HTML saja, karena PDF asli tetap beredar; (3) penerbitan otomatis penuh, karena "
  "halusinasi [@charxiv,@blind,@adnin]; (4) bergantung pada sumber LaTeX seperti [@itag], karena hanya 1 dari 28 "
  "dokumen bermetadata LaTeX; (5) menilai mutu hanya dengan validator [@verapdf]; dan (6) memverifikasi rumus dengan "
  "kemiripan citra [@ssim] (Tabel {T:kelayakan}).")
p("Rencana kerja memuat titik keputusan lebih awal. Pada 1–3 Oktober dijalankan dua uji penentu: ekstraksi tabel data dari "
  "grafik sintetis berbahasa Indonesia oleh VLM dan validasi veraPDF pada lima materi kuliah nyata. Selanjutnya, 4–9 "
  "Oktober untuk perakitan keluaran (STR-01, OUT-01) dan G1; 10–15 Oktober untuk modul grafik, gerbang, G3, dan G4; 16–19 "
  "Oktober untuk antarmuka tinjauan, audit dokumen nyata (G6), dan modul rumus bila waktu tersedia; 20–22 Oktober untuk "
  "pembekuan versi, evaluasi pada set uji tertahan, dan penulisan Bab IV–V; serta 23 Oktober untuk pengumpulan karya "
  "lengkap. Lingkup minimum demo adalah unggah PDF, keluaran HTML aksesibel dan PDF bertag, deskripsi grafik dengan "
  "gerbang, dan antrean tinjauan. Karena demo berlangsung dalam slot presentasi 15 menit dan bergantung pada layanan VLM, "
  "hasil dokumen contoh disimpan sebelumnya (*cache*) dan jalur langsung menjadi tambahan. Ditunda: PowerPoint dan Word "
  "langsung, braille, dan G7. Rumus yang belum dapat diproses ditahan ke antrean tinjauan sesuai prinsip *fail-closed* "
  "sehingga demo tidak bergantung padanya. Seluruh komponen utama berupa kode terbuka (Tabel {T:solusi}); pekerjaan "
  "penulis berada pada perangkaian, gerbang, antarmuka, dan evaluasi.")
h2("Risiko, Etika, dan Ancaman Validitas")
p("Risiko utama adalah halusinasi (dimitigasi gerbang dan penanda “dihasilkan otomatis”), deskripsi yang benar tetapi tidak "
  "berguna (diukur pada G4 dan G7), beban tinjauan yang membuat ULD kewalahan (dilaporkan pada G6), dan hak cipta materi "
  "dosen (dokumen diproses per sesi tanpa disimpan dan tidak dipakai melatih model). Ancaman validitas ada tiga. Pertama, "
  "dokumen sintetis lebih rapi daripada materi nyata, yang ditangkal oleh G6. Kedua, ekstraksi ganda tidak menangkap "
  "kesalahan sistematik; pemeriksaan rentang sumbu dan antrean tinjauan mengurangi tetapi tidak menghapus risiko ini. "
  "Ketiga, penilai berasal dari tim penulis sehingga berisiko bias; set uji dikunci dengan *hash*, dua penilai bekerja "
  "terpisah dengan kappa dilaporkan, dan bila memungkinkan staf ULD dilibatkan sebagai penilai luar pada G6.")
# ================================================================= LAMPIRAN
APPENDIX = [
 ("h", "Lampiran A. Pernyataan Penggunaan AI Generatif"),
 ("p", "[Sesuaikan dengan penggunaan sebenarnya.] Tim menggunakan Claude (Anthropic) untuk penelusuran awal pustaka, "
       "pemeriksaan angka terhadap sumber, pembuatan skrip audit dokumen dan skrip uji kelayakan awal, penyusunan dan "
       "revisi draf naskah, serta pemeriksaan bahasa. Seluruh isi telah ditinjau dan disunting oleh penulis, dan "
       "penulis bertanggung jawab penuh atas akurasi dan orisinalitas karya. Seluruh referensi telah diperiksa "
       "keasliannya oleh penulis."),
 ("h", "Lampiran B. Hasil Pengecekan Similarity (Turnitin)"),
 ("p", "[Tempelkan laporan Turnitin di sini. Ambang: di bawah 15% di luar kutipan dan daftar referensi.]"),
 ("h", "Lampiran C. Protokol Audit Awal"),
 ("p", "Sumber: 28 PDF materi kuliah berbahasa Indonesia dari 18 kampus, dikumpulkan dari hasil pencarian repositori publik "
       "(bukan sampel acak); 43 tautan dicoba dan 28 berkas berhasil diunduh, sisanya diblokir server atau tidak "
       "tersedia. Alat: veraPDF 1.30.2 (profil PDF/UA-1) dan PyMuPDF. Dokumen dianggap bertag bila memiliki StructTreeRoot "
       "dan MarkInfo/Marked bernilai true. Elemen Figure dihitung dari pohon struktur, dan dianggap memiliki teks "
       "alternatif bila atribut /Alt ada dan tidak kosong. Aplikasi pembuat dikelompokkan dari metadata Producer/Creator. "
       "Bahasa isi diperkirakan dari rasio kata fungsi bahasa Indonesia dan Inggris pada 12 halaman pertama; ini heuristik "
       "dan bukan pengukuran kebahasaan. Daftar sumber dan tabel per dokumen tersedia pada berkas terpisah milik tim."),
 ("h", "Lampiran D. Protokol Uji Kelayakan Awal"),
 ("p", "Perangkat: laptop tanpa GPU (RAM 15 GB, Python 3.13, Java 21). Perangkat lunak: OpenDataLoader PDF 2.5.11, "
       "pikepdf 10.15.0, PyMuPDF 1.28.2, dan veraPDF 1.30.2 (profil PDF/UA-1). Dokumen uji: tiga PDF contoh karya "
       "kompetisi, yaitu laporan bertag berbahasa Indonesia (18 halaman, 113 elemen Figure), laporan tidak bertag (21 "
       "halaman), dan berkas presentasi tidak bertag (43 salindia). Penambalan menambahkan Lang, MarkInfo/Marked, "
       "ViewerPreferences/DisplayDocTitle, Title (Info dan XMP), kunci Tabs pada setiap halaman, penanda pdfuaid:part = 1, "
       "dan mengisi /Alt pada elemen Figure. Uji SSIM: lima rumus, masing-masing dirender dalam bentuk benar dan bentuk "
       "dengan satu simbol diubah (misalnya tanda tambah menjadi kurang, atau pangkat 2 menjadi 3) memakai dua rangkaian "
       "font (mathtext DejaVu Sans dan Computer Modern); citra dipangkas dan dinormalisasi ke tinggi 64 piksel sebelum "
       "SSIM dihitung. Pasangan font tersebut hanya aproksimasi perbedaan font dokumen sebenarnya. Uji pemeriksaan angka "
       "memakai data buatan dan mengimplementasikan versi awal pemeriksa angka dan selisih ekstraksi. Skrip tersedia pada "
       "berkas terpisah milik tim."),
 ("h", "Lampiran E. Rincian Arsitektur Teknis (Rancangan)"),
 ("p", "Antarmuka: HTML, CSS, dan JavaScript tanpa kerangka kerja berat, dengan tiga halaman (unggah, tinjauan, keluaran). "
       "Layanan: Python 3.13 dengan FastAPI dan antrean kerja dalam proses; sesi disimpan pada memori atau direktori "
       "sementara dan dihapus setelah sesi berakhir. Pemroses dokumen: OpenDataLoader PDF 2.5.11 (Java 21), PyMuPDF 1.28, "
       "dan pikepdf 10.15; validasi memakai veraPDF 1.30.2. Model: adaptor VLM dengan satu fungsi yang menerima citra dan "
       "skema JSON serta mengembalikan tabel data, sehingga model komersial atau terbuka (misalnya Qwen2.5-VL) dapat "
       "dipasang. Rumus: MathCAT di peramban melalui WebAssembly. Mode dengar: Web Speech API dengan suara id-ID."),
 ("p", "Rekaman elemen memuat id, halaman, kotak pembatas, jenis (teks, judul, tabel, grafik, rumus, foto, dekoratif), "
       "tabel data T1 dan T2, klaim, hasil pemeriksaan (cF, cδ, cA, cR), teks alternatif, dan status (terbit otomatis, "
       "antrean, disetujui, diubah, ditolak). Titik akhir yang direncanakan: POST /unggah, GET /pekerjaan/{id}, "
       "GET /elemen/{id}, POST /tinjau/{id}, dan GET /keluaran/{id}.html atau .pdf."),
 ("p", "Sumber daya yang terukur pada uji awal: CPU tanpa GPU, RAM 15 GB; auto-tag 21 halaman dalam 4,6 detik dan penambalan "
       "113 elemen Figure dalam 0,38 detik. Waktu dan biaya VLM per gambar diukur pada uji penentu 1–3 Oktober."),
]
