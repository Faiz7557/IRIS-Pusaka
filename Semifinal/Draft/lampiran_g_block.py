# -*- coding: utf-8 -*-
# Blok Lampiran G; di-exec oleh add_lampiran_f.py (memakai `par`, `content`, OxmlElement, qn).
import json, os
FS = {}
_fs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Audit", "Skala", "frame_stats.json")
if os.path.exists(_fs):
    FS = json.load(open(_fs))
_f = lambda x: f"{x:,}".replace(",", ".")
frame_size = (f"{_f(FS['n'])} PDF unik dari {FS['paneN']} panen; {_f(FS['d'])} domain; {_f(FS['n_materi'])} PDF ({_f(FS['d_materi'])} domain) lolos aturan URL materi kuliah; {_f(FS['utuh'])} tidak terpotong (terukur 30 Sep. 2026)" if FS else "Diukur pada 1–3 Okt. 2026")


def cell_par(text, bold=False, color=None, size=16, jc=None):
    p = OxmlElement("w:p"); ppr = OxmlElement("w:pPr")
    sp = OxmlElement("w:spacing"); sp.set(qn("w:before"), "20"); sp.set(qn("w:after"), "20"); sp.set(qn("w:line"), "228"); sp.set(qn("w:lineRule"), "auto"); ppr.append(sp)
    if jc:
        j = OxmlElement("w:jc"); j.set(qn("w:val"), jc); ppr.append(j)
    p.append(ppr)
    r = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
    if bold:
        rpr.append(OxmlElement("w:b")); rpr.append(OxmlElement("w:bCs"))
    if color:
        c = OxmlElement("w:color"); c.set(qn("w:val"), color); rpr.append(c)
    for tag in ("w:sz", "w:szCs"):
        e = OxmlElement(tag); e.set(qn("w:val"), str(size)); rpr.append(e)
    lg = OxmlElement("w:lang"); lg.set(qn("w:val"), "id-ID"); rpr.append(lg)
    r.append(rpr)
    t = OxmlElement("w:t"); t.text = text; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r.append(t); p.append(r)
    return p


def mk_table(headers, rows, widths_cm, size=16, first_bold=False):
    tbl = OxmlElement("w:tbl"); pr = OxmlElement("w:tblPr")
    tw = OxmlElement("w:tblW"); tw.set(qn("w:w"), str(int(sum(widths_cm) * 567))); tw.set(qn("w:type"), "dxa"); pr.append(tw)
    jc = OxmlElement("w:jc"); jc.set(qn("w:val"), "center"); pr.append(jc)
    bd = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement("w:" + side); b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:color"), "B9CCEC"); bd.append(b)
    pr.append(bd)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); pr.append(lay)
    cm = OxmlElement("w:tblCellMar")
    for side, v in (("top", 30), ("left", 70), ("bottom", 30), ("right", 70)):
        e = OxmlElement("w:" + side); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); cm.append(e)
    pr.append(cm); tbl.append(pr)
    grid = OxmlElement("w:tblGrid")
    for w in widths_cm:
        g = OxmlElement("w:gridCol"); g.set(qn("w:w"), str(int(w * 567))); grid.append(g)
    tbl.append(grid)

    def row(vals, header=False, zebra=False):
        tr = OxmlElement("w:tr"); trpr = OxmlElement("w:trPr")
        trpr.append(OxmlElement("w:cantSplit"))
        if header:
            trpr.append(OxmlElement("w:tblHeader"))
        tr.append(trpr)
        for k, (v, w) in enumerate(zip(vals, widths_cm)):
            tc = OxmlElement("w:tc"); tcp = OxmlElement("w:tcPr")
            tcw = OxmlElement("w:tcW"); tcw.set(qn("w:w"), str(int(w * 567))); tcw.set(qn("w:type"), "dxa"); tcp.append(tcw)
            fill = "0B2E63" if header else ("EAF1FC" if zebra else None)
            if fill:
                sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill); tcp.append(sh)
            tc.append(tcp)
            tc.append(cell_par(v, bold=(header or (first_bold and k == 0)), color=("FFFFFF" if header else None), size=size))
            tr.append(tc)
        return tr
    tbl.append(row(headers, header=True))
    for i, r_ in enumerate(rows):
        tbl.append(row(r_, zebra=(i % 2 == 1)))
    return tbl


def sub(text):
    return par([(text, True)], before=160, after=60, size=20, keep_next=True)


content.append(par([("Lampiran G. Rencana Data Babak Final: Inventaris, Pemetaan ke Prototipe, dan Justifikasi Sampel", True)], style="Heading1", page_break=True, keep_next=True))
content.append(par([("Lampiran ini merinci data yang diusulkan untuk babak final. Setiap sumber dipakai dua kali: pada set pengembangan untuk membangun dan mengalibrasi prototipe, dan pada set uji tertahan untuk evaluasi tujuh gerbang. Status “terverifikasi” berarti ukuran dan isi sumber telah dicocokkan dengan makalah atau repositorinya pada 30 September 2026; butir lain dikonfirmasi saat pengunduhan.", False)],
                    jc="both", after=80, size=20))
content.append(sub("G.1 Inventaris data"))
G1 = [
    ["1", "Bingkai Common Crawl: PDF pada domain ac.id", "Indeks kolumnar Common Crawl (panen CC-MAIN-2026-39); terbuka. Berkas diambil dari arsip WARC publik.", "URL, host, domain terdaftar, jenis berkas terdeteksi, status HTTP, penanda terpotong, lokasi arsip (nama berkas, posisi, panjang). Kolom bahasa indeks kosong untuk PDF (uji 30 Sep.), sehingga bahasa ditentukan setelah unduh", frame_size, "Bingkai sampel audit skala besar; sumber dokumen pengembangan dan uji (STR-01, OUT-01, CLS-01) dan 60 dokumen G6", "Kueri diuji; bingkai diekstraksi"],
    ["2", "Korpus SafeDocs (CC-MAIN-2021-31-PDF-UNTRUNCATED)", "Digital Corpora; terbuka", "PDF utuh tanpa pemotongan ukuran; URL sumber", "Hampir 8 juta PDF (seluruh web, panen 2021)", "Pelengkap untuk berkas besar (mis. salindia) yang terpotong pada bingkai 1; mengurangi bias ukuran berkas", "Kandidat; penyaringan ac.id belum dijalankan"],
    ["3", "Audit awal materi kuliah", "Tautan publik; berkas tidak disebarluaskan", "Metadata dan struktur (bertag, teks alternatif, bahasa, tabel), hasil veraPDF", "28 PDF; 3.229 halaman; 18 kampus", "Uji coba protokol dan skrip; bukti awal urgensi", "Terukur"],
    ["4", "Set sintetis penulis", "Dibuat penulis (Word dan LaTeX ke PDF; grafik berbahasa Indonesia)", "Acuan pasti: urutan baca, tabel data, angka grafik, LaTeX rumus", "30 dokumen; 150 grafik lima jenis; 200 ekspresi rumus (target)", "Acuan G2 sampai G5; pengembangan (sepertiga) dan uji (dua pertiga)", "Rencana"],
    ["5", "VisText", "GitHub mitvis/vistext; GPL-3.0", "Citra grafik, tabel data, graf adegan, keterangan berlevel", "12.441 pasang grafik dan keterangan", "Merancang skema ekstraksi tabel data dan templat kalimat (CHT-01, CHT-02); uji komponen G3", "Terverifikasi (makalah)"],
    ["6", "ChartQA", "Masry dkk., Findings ACL 2022; publik", "Citra grafik, tabel data pendukung, pertanyaan dan jawaban", "9,6 ribu pertanyaan manusia; 23,1 ribu pertanyaan dibangkitkan", "Grafik dengan beragam gaya untuk menguji ketahanan ekstraksi dan rasio Q pada G4", "Terverifikasi (makalah); tabel data dicek saat unduh"],
    ["7", "UniMER-Test", "GitHub opendatalab/UniMERNet; publik", "Citra rumus dan LaTeX; kategori SPE, CPE, SCE, HWE", "23.789 sampel", "Memilih pengenal rumus dan menyetel θr (FRM-01); uji G5", "Terverifikasi (makalah dan repositori)"],
    ["8", "IndoTabVQA", "ACL Findings 2026, arXiv:2604.11970; publik", "Citra dokumen bertabel (berbingkai, tanpa garis, berwarna); tanya-jawab dalam empat bahasa", "1.593 citra dokumen", "Tabel berbahasa Indonesia; keputusan OpenDataLoader atau Docling untuk tabel tanpa garis (STR-01); uji G2", "Terverifikasi (abstrak)"],
    ["9", "SEA-Vision", "arXiv:2603.15409; publik", "Penguraian dokumen dan tanya-jawab teks; 11 bahasa termasuk Indonesia", "15.234 sampel penguraian; 7.496 pasangan tanya-jawab (seluruh bahasa)", "Pembanding kemampuan VLM pada dokumen Indonesia; subset Indonesia dipilih setelah unduh", "Terverifikasi (abstrak); subset dan lisensi dicek"],
    ["10", "Tolok ukur aksesibilitas PDF (Kumar dkk., ASSETS 2025)", "arXiv:2509.18965; ketersediaan berkas dikonfirmasi", "Anotasi ahli pada tujuh kriteria (kualitas teks alternatif, urutan baca, tag, tabel, dan lain-lain)", "Jumlah PDF dikonfirmasi saat unduh", "Validasi silang pemeriksa otomatis (G1, G4) bila berkas tersedia", "Kandidat; ketersediaan belum terkonfirmasi"],
]
content.append(mk_table(["No", "Data", "Sumber dan akses", "Metadata atau label yang dipakai", "Ukuran", "Peran pada prototipe dan evaluasi", "Status verifikasi"],
                        G1, [0.8, 3.5, 4.2, 5.0, 3.6, 4.7, 2.8], size=15))
content.append(sub("G.2 Pemetaan data ke fitur prototipe dan pembagian set"))
content.append(par([("Pembagian dilakukan sebelum pengembangan dan menurut domain kampus (untuk dokumen) atau menurut grafik (untuk benchmark) dengan seed tetap, sehingga set pengembangan dan set uji tidak berbagi kampus. Perubahan komponen hanya boleh didasarkan pada set pengembangan; set uji dibuka sekali setelah versi dibekukan.", False)], jc="both", after=60, size=18))
G2 = [
    ["STR-01 Struktur, urutan baca, tabel", "400 PDF pengembangan (bingkai); 100 citra IndoTabVQA (per gaya visual)", "200 PDF uji; 200 citra IndoTabVQA", "Memilih OpenDataLoader atau Docling (uji tabel tanpa garis); aturan pemetaan baris judul menjadi sel TH; syarat jatuh ke HTML aksesibel", "G1, G2"],
    ["OUT-01 Perakitan dan validasi", "400 PDF pengembangan", "200 PDF uji; 60 dokumen G6", "Aturan PDF/UA-1 yang paling sering gagal pada sampel menentukan prioritas aturan tambal (bahasa, judul, teks alternatif, TH, urutan baca)", "G1"],
    ["CLS-01 Jenis gambar", "200 gambar dari PDF pengembangan, dilabeli dua penilai (grafik, tabel-citra, rumus, foto atau diagram, dekoratif)", "100 gambar dari PDF uji", "Ambang heuristik ukuran, hash, dan posisi; perintah zero-shot; laju grafik yang terlewat", "G3"],
    ["CHT-01, CHT-02 Tabel data dan statistik", "150 grafik VisText dan ChartQA; 50 grafik sintetis", "150 grafik VisText dan ChartQA; 100 sintetis; grafik nyata pada G6", "Skema JSON, perintah ekstraksi ganda, ambang θe (Pers. 2), ambang tren ρ, templat kalimat", "G3, G4"],
    ["FRM-01, FRM-02 Rumus", "100 rumus UniMER-Test (25 per kategori); 50 sintetis", "100 rumus UniMER-Test; 150 sintetis", "Memilih pengenal pertama dan kedua; ambang θr (Pers. 6); uji aturan ucapan MathCAT", "G5"],
    ["GAT-01 Gerbang verifikasi", "Seluruh set pengembangan", "Seluruh set uji", "Kalibrasi θe dan θr pada set pengembangan lalu dikunci; estimasi laju penahanan R", "G3, G6"],
    ["REV-01, OUT-02 Tinjauan ULD dan mode dengar", "20 dokumen pengembangan yang memuat elemen ditahan", "60 dokumen G6; staf ULD mitra bila tersedia", "Urutan antrean, tampilan berdampingan; uji pembacaan dengan NVDA dan suara id-ID", "G6, G7"],
]
content.append(mk_table(["Fitur", "Data pengembangan", "Data uji tertahan", "Yang dibangun atau dikalibrasi dari data pengembangan", "Gerbang"],
                        G2, [3.6, 5.6, 4.6, 8.8, 2.0], size=15, first_bold=True))
content.append(sub("G.3 Desain sampel dan justifikasi ukuran"))
G3 = [
    ["28", "±17,4", "±24,6", "Audit awal (uji coba)"],
    ["60", "±12,3", "±17,3", "Dokumen nyata G6"],
    ["150", "±7,9", "±11,2", "Grafik sintetis; grafik publik per set uji"],
    ["400", "±4,9", "±6,9", "Stratum materi kuliah pada audit skala besar"],
    ["600", "±4,0", "±5,6", "Sampel gabungan dua stratum (berbobot)"],
]
content.append(par([("Setengah lebar selang Wilson 95% pada proporsi 50% (kasus terburuk); efek desain 2 diasumsikan untuk sampel berklaster per kampus dan akan diestimasi dari data.", False)], jc="both", after=40, size=18, italic=True))
content.append(mk_table(["n", "Setengah lebar selang (poin persentase)", "Dengan efek desain 2", "Pemakaian"], G3, [2.0, 7.0, 5.0, 10.6], size=16))
pts = [
    "Populasi dan bingkai: PDF pada domain ac.id yang dirayapi Common Crawl. Karena indeks tidak memuat bahasa PDF, sampel diunduh lebih banyak (target 800) dan dokumen berbahasa Indonesia (heuristik kata fungsi dan deklarasi Lang) dipertahankan hingga 600; jumlah yang dikeluarkan dilaporkan. Generalisasi terbatas pada materi yang terbuka untuk publik; materi di balik kata sandi (mis. LMS) tidak terwakili.",
    "Stratifikasi: stratum A (materi kuliah) dan stratum B (dokumen akademik lain yang tidak memuat kata pengecualian) diambil terpisah dan dibobot N/n pada estimasi gabungan; stratum B menguji apakah kesimpulan berlaku di luar materi kuliah. Stratum A menurut kata kunci pada jalur URL (slide, materi, bahan ajar, modul, pertemuan, handout, diktat, kuliah, presentasi, ppt, RPS, SAP) dengan pengecualian (skripsi, tesis, jurnal, prosiding, surat, laporan, pedoman, panduan, akreditasi, dan sejenisnya), ditetapkan sebelum melihat hasil; presisi aturan diperiksa manual pada 100 dokumen dan dilaporkan.",
    "Pengambilan: acak dengan seed 20260930, maksimum 12 dokumen per domain per stratum agar satu kampus tidak mendominasi; unduh 480 (A) dan 240 (B) agar setelah dokumen non-Indonesia dikeluarkan tersisa target 400 dan 200; pembagian pengembangan dan uji 2:1 menurut domain.",
    "Analisis yang ditetapkan sebelumnya: proporsi dengan selang Wilson dan bootstrap klaster per domain (2.000 replikasi); tingkat keberhasilan unduh dan alasan kegagalan dilaporkan; sensitivitas menurut aplikasi pembuat dan kelengkapan berkas (tangkapan utuh atau dilengkapi SafeDocs).",
    "Makna keputusan: 0 dari 28 hanya menjamin batas atas 12,1% dan 0 dari 600 menjamin batas atas 0,64%, sehingga klaim “hampir tidak ada yang lulus” baru dapat dibuat dari sampel besar. Pada G6, hasil teramati 90% berbatas bawah 79,9% bila n = 60 tetapi 74,4% bila n = 30, sehingga ambang 80% tidak dapat dibuktikan dengan 30 dokumen.",
    "Kebocoran data dan etika: benchmark publik mungkin pernah dilihat VLM, sehingga kesimpulan G3 juga bertumpu pada dokumen sintetis dan dokumen nyata. Hanya metadata, struktur, dan hitungan agregat yang dilaporkan; berkas tidak disebarluaskan, dan tangkapan terpotong tidak diunduh ulang dari server kampus (dilengkapi dari SafeDocs).",
]
if FS:
    pts.insert(1, f"Alasan stratifikasi (terukur 30 Sep. 2026): pada bingkai gabungan {FS['paneN']} panen terdapat {_f(FS['n'])} PDF unik dari {_f(FS['d'])} domain, tetapi hanya {_f(FS['n_materi'])} "
                  f"({format(100*FS['n_materi']/FS['n'], '.1f').replace('.', ',')}%) berciri materi kuliah menurut URL; sisanya didominasi artikel jurnal dan bagian skripsi. Sampel acak sederhana atas bingkai akan memuat sangat sedikit materi kuliah.".replace("%)", "%)"))
for t_ in pts:
    content.append(par([("• " + t_, False)], jc="both", after=30, size=18))
