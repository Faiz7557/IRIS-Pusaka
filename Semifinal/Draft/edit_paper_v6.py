# -*- coding: utf-8 -*-
"""Sunting naskah v6 langsung pada .docx milik pengguna (bukan content.py):
 - tulis ulang Latar Belakang (sitasi benar, referensi baru terintegrasi)
 - tambah rujukan referensi baru di Bab II/III + tautan ke Lampiran F
 - hapus referensi duplikat, nomori ulang sitasi menurut urutan kemunculan (IEEE)
 - bangun ulang Daftar Referensi
Markup teks: [@kunci,@kunci] sitasi | *miring*
"""
import copy, re, sys
from lxml import etree
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = sys.argv[1]
DST = sys.argv[2]
d = docx.Document(SRC)
body = d.element.body

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def ptext(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t")))


def all_pars():
    return list(body.iter(qn("w:p")))


def find_par(prefix, nth=0):
    hits = [p for p in all_pars() if ptext(p).replace(" ", " ").startswith(prefix)]
    assert len(hits) > nth, f"paragraf tidak ditemukan: {prefix!r}"
    return hits[nth]


def merge_runs(p):
    """Gabungkan run bersebelahan yang hanya berisi satu w:t dengan rPr identik."""
    runs = [c for c in p if c.tag == qn("w:r")]
    prev = None
    for r in runs:
        kids = [k for k in r if k.tag != qn("w:rPr")]
        simple = len(kids) == 1 and kids[0].tag == qn("w:t")
        if not simple:
            prev = None
            continue
        rpr = r.find(qn("w:rPr"))
        key = etree.tostring(rpr) if rpr is not None else ""
        if prev is not None and prev[0] == key and r.getprevious() is prev[1]:
            t0 = prev[1].find(qn("w:t"))
            t0.text = (t0.text or "") + (kids[0].text or "")
            t0.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            p.remove(r)
        else:
            prev = (key, r)


def mk_run(text, italic=False, sz=None, lang="en-ID"):
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    if italic:
        rpr.append(OxmlElement("w:i"))
        rpr.append(OxmlElement("w:iCs"))
    if sz:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(sz)); rpr.append(s)
        s = OxmlElement("w:szCs"); s.set(qn("w:val"), str(sz)); rpr.append(s)
    lg = OxmlElement("w:lang"); lg.set(qn("w:val"), lang); rpr.append(lg)
    r.append(rpr)
    t = OxmlElement("w:t"); t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    return r


def set_text(p, markup, sz=None, lang="en-ID"):
    for c in list(p):
        if c.tag != qn("w:pPr"):
            p.remove(c)
    for i, seg in enumerate(re.split(r"\*", markup)):
        if seg:
            p.append(mk_run(seg, italic=(i % 2 == 1), sz=sz, lang=lang))


def patch(p, old, new, count=1):
    n = 0
    for t in p.iter(qn("w:t")):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new, count)
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            n += 1
            break
    assert n == 1, f"patch gagal: {old!r} pada {ptext(p)[:50]!r}"


# ------------------------------------------------------------------ daftar referensi lama
pars = all_pars()
i_ref = next(i for i, p in enumerate(pars) if ptext(p).strip() == "REFERENSI")
i_lamp = next(i for i, p in enumerate(pars) if ptext(p).startswith("Lampiran A."))
ref_pars = pars[i_ref + 1:i_lamp]
old_refs = {}
for p in ref_pars:
    txt = ""
    for r in p.iter(qn("w:r")):
        if r.find(qn("w:br")) is not None:
            break
        for t in r.iter(qn("w:t")):
            txt += t.text or ""
    m = re.match(r"\[(\d+)\]\s*(.*)$", txt.strip(), flags=re.S)
    if m and int(m.group(1)) <= 47:
        old_refs[int(m.group(1))] = m.group(2).strip()
assert sorted(old_refs) == list(range(1, 48)), sorted(old_refs)
template_ref_par = copy.deepcopy(ref_pars[0])  # pPr: ind left=284 hanging=295

REFS = {f"r{n}": t for n, t in old_refs.items()}
REFS.update({
    "almalky": "H. A. Almalky and K. A. Qaysi, “Assistive technology for university students with disabilities: Availability, utilization, and impact on academic performance,” Res. Dev. Disabil., vol. 164, Art. no. 105078, Sep. 2025, doi: 10.1016/j.ridd.2025.105078.",
    "day": "J. R. Day and K. R. Fleischmann, “Academic libraries and accessibility: How academic librarians assist students with visual impairments in accessing academic reading materials,” J. Acad. Librariansh., vol. 52, no. 3, Art. no. 103238, May 2026, doi: 10.1016/j.acalib.2026.103238.",
    "khlaif": "Z. N. Khlaif, R. Alshakhshir, B. T. Hamamra, and A. I. Joma, “Assistive generative AI for visually impaired learners: Personalization and inclusion in higher education,” Int. J. Artif. Intell. Educ., vol. 36, no. 1–2, Art. no. 100008, Mar. 2026, doi: 10.1016/j.ijaied.2026.100008.",
    "gidisu": "P. Gidisu, W. K. Abroampa, and M. K. G. Nyatsikor, “Ensuring technological inclusivity for students with visual impairments in higher education: A systematic literature review,” Soc. Sci. Humanit. Open, vol. 13, Art. no. 102780, Jun. 2026, doi: 10.1016/j.ssaho.2026.102780.",
    "nganji": "J. T. Nganji, “The Portable Document Format (PDF) accessibility practice of four journal publishers,” Libr. Inf. Sci. Res., vol. 37, no. 3, pp. 254–262, Jul. 2015, doi: 10.1016/j.lisr.2015.02.002.",
    "chartqa": "A. Masry, X. L. Do, J. Q. Tan, S. Joty, and E. Hoque, “ChartQA: A benchmark for question answering about charts with visual and logical reasoning,” in Findings Assoc. Comput. Linguistics: ACL 2022, pp. 2263–2279.",
    "cc": "S. Nagel, “Index to WARC files and URLs in columnar format,” Common Crawl Foundation, Mar. 2018. Diakses: 30 Sep. 2026. [Daring]. Tersedia: https://commoncrawl.org/blog/index-to-warc-files-and-urls-in-columnar-format",
    "safedocs": "Digital Corpora, “SAFEDOCS (CC-MAIN-2021-31-PDF-UNTRUNCATED).” Diakses: 30 Sep. 2026. [Daring]. Tersedia: https://digitalcorpora.org/corpora/file-corpora/cc-main-2021-31-pdf-untruncated/",
    "hicap": "W. Li, X. Li, Z. Li, J. Yu, and P. Chen, “HI-Captioner: End-to-end image captioning based on hierarchical multi-scale encoding and cross-modal interactive decoding,” Neurocomputing, vol. 647, Art. no. 130622, Sep. 2025, doi: 10.1016/j.neucom.2025.130622.",
})
for _k in list(REFS):
    REFS[_k] = REFS[_k].replace("Tersedia: https://", "Tersedia: ").replace(" [Daring].", "")
# dokumen 'Pashler' lama tanpa DOI: tambahkan DOI terverifikasi pengguna
REFS["r14"] = REFS["r14"].rstrip(".") + ", doi: 10.1111/j.1539-6053.2009.01038.x."

# ------------------------------------------------------------------ teks Latar Belakang baru
P1 = ("Transformasi digital memindahkan materi kuliah dari kertas ke berkas PDF, tetapi akses digital tidak otomatis "
      "berarti aksesibilitas. Pangkalan Data Pendidikan Tinggi (PDDikti) per Juni 2025 mencatat 3.128 mahasiswa "
      "disabilitas di 282 perguruan tinggi, dan tunanetra merupakan kelompok terbesar dengan 1.727 orang [@r3]; perguruan "
      "tinggi berkewajiban menyediakan akomodasi yang layak dan membentuk Unit Layanan Disabilitas (ULD) [@r1,@r2]. "
      "Namun, tinjauan sistematis atas 60 studi menemukan bahwa konten digital yang tidak aksesibel, keterbatasan "
      "infrastruktur, dan kurangnya pelatihan tetap menjadi hambatan utama mahasiswa tunanetra, padahal pembaca layar "
      "(*screen reader*) dan layar braille telah tersedia [@gidisu]. Ketersediaan teknologi bantu pun tidak cukup; "
      "implementasinya dipengaruhi kebijakan institusi, pendanaan, dan kebutuhan individu [@almalky].")
P2 = ("Beban itu jatuh pada staf layanan. Wawancara dengan 28 pustakawan akademik di 25 perguruan tinggi Amerika Serikat "
      "menunjukkan bahwa hambatan akses bahan bacaan bagi mahasiswa tunanetra saling bertautan, mulai dari proses "
      "organisasi, registrasi layanan disabilitas, hingga jenis konten, dan menuntut tambahan tenaga kerja [@day]. Di "
      "Indonesia, produksi materi aksesibel oleh staf ULD maupun lembaga seperti Yayasan Mitra Netra juga masih bertumpu "
      "pada tenaga manusia dan berbiaya tinggi [@r18,@r19]. Staf unit layanan disabilitas melaporkan bahwa AI generatif "
      "meningkatkan kecepatan dan kepercayaan diri dalam menulis deskripsi gambar, tetapi alur kerja bersama AI masih "
      "menjadi kendala [@r20].")
P3 = ("Masalah ini paling terasa pada PDF, format dominan materi kuliah, karena struktur visual tidak otomatis menjadi "
      "struktur semantik yang dipahami pembaca layar. Pada 200 artikel PDF dari empat penerbit jurnal (2009–2013), 97% tidak "
      "menyediakan teks alternatif untuk gambar, hanya 4,5% bertag, 67% tidak menetapkan bahasa dokumen, dan 99,5% tidak "
      "memiliki urutan baca logis [@nganji]. Studi yang lebih baru pada 20.000 PDF ilmiah (2014–2023) menemukan bahwa kurang "
      "dari 3,2% memenuhi kriteria aksesibilitas [@r7]. Audit awal penulis terhadap 28 PDF materi kuliah berbahasa "
      "Indonesia dari 18 perguruan tinggi menunjukkan pola serupa: tidak satu pun memenuhi PDF/UA-1, dan hanya 29 dari "
      "1.111 elemen *Figure* pada dokumen bertag (2,6%) memiliki teks alternatif (Tabel I). Karena sampelnya kecil dan tidak acak, audit ini hanya membuktikan bahwa masalahnya ada, "
      "bukan seberapa luas; babak final memperluasnya dengan sampel acak dari bingkai publik (Bab III.D).")
P4 = ("Kegagalan terberat terjadi pada grafik. Teks alternatif seperti “image 1” atau “grafik” tidak menyampaikan "
      "variabel, nilai, ekstrem, maupun pola. Wawancara dengan 22 pengguna berhambatan penglihatan menunjukkan bahwa mereka "
      "membangun gambaran mental grafik dan ingin mengambil nilai tertentu seperti pengguna awas, sehingga teks alternatif "
      "perlu merujuk pada data yang mendasari grafik, bukan pada tampilan visualnya [@r25]. AI generatif tampak menjawab "
      "kebutuhan ini: 21 mahasiswa tunanetra di Palestina melaporkan manfaat personalisasi dan akses inklusif [@khlaif]. Namun, kemajuan pembuatan deskripsi gambar (*image captioning*) dievaluasi pada foto alami "
      "seperti MSCOCO dan Flickr [@hicap], bukan pada grafik; model *vision-language* (VLM) GPT-4o hanya mencapai akurasi "
      "47,1% pada grafik ilmiah [@r9] dan rata-rata 58,07% pada tugas geometri sederhana [@r11]; dan pengguna tunanetra "
      "sendiri melaporkan ketidakakuratan dan halusinasi [@r12]. Belum ada ukuran kesetiaan deskripsi grafik pada materi "
      "kuliah berbahasa Indonesia, sehingga diperlukan alur yang membuktikan bahwa deskripsi setia pada datanya dan menahan yang "
      "tidak terbukti, serta data evaluasi yang mencakup materi tersebut (Bab III.D).")
P5 = ("Masalah yang sama dialami mahasiswa yang memilih mendengarkan. Indonesia memiliki proporsi pendengar podcast mingguan "
      "tertinggi di antara negara yang diukur, yaitu 42,6% pengguna internet berusia 16 tahun ke atas pada awal 2025 [@r13], "
      "sedangkan alat bacaan suara (*text-to-speech*, TTS) melewatkan grafik, rumus, dan tabel tanpa teks alternatif. Kebiasaan ini "
      "hanya indikator preferensi, bukan bukti bahwa mendengarkan meningkatkan hasil belajar; teori gaya belajar tidak didukung "
      "bukti memadai [@r14]. Dasarnya adalah akses dan pilihan: Universal Design for Learning menganjurkan beragam cara penyajian "
      "[@r15], fitur bagi kelompok rentan sering bermanfaat bagi banyak orang (*curb-cut effect*) [@r16], dan TTS meningkatkan "
      "pemahaman bacaan siswa dengan kesulitan membaca (meta-analisis 22 studi; ukuran efek 0,35) [@r17]. Karena itu, mahasiswa "
      "tunanetra menjadi pengguna utama, sedangkan manfaat bagi pendengar diperlakukan sebagai hipotesis.")
P6 = ("Kesenjangannya terletak pada perangkat, bukan pada saluran: ULD sudah ada, tetapi kemampuan teknisnya belum. "
      "SIMAK (Sistem Ilustrasi Materi Aksesibel untuk Kuliah) dirancang untuk kondisi tersebut: mesin mengerjakan bagian "
      "yang dapat diverifikasi, sedangkan manusia memutuskan bagian yang tidak. Sistem menerima PDF apa adanya, memperbaiki "
      "struktur dan urutan baca, menyusun deskripsi grafik dari tabel data dengan statistik yang dihitung kode, "
      "membacakan rumus, dan menahan setiap keluaran yang tidak dapat diverifikasi untuk ditinjau ULD (*fail-closed*). "
      "Nilai jualnya bukan AI yang lebih cerdas, melainkan jaminan bahwa tidak ada deskripsi keliru yang terbit tanpa "
      "penanda. Sistem ini menjawab subfokus "
      "aksesibilitas materi pada tema Innovation Case Competition (ICC) dan mendukung SDG 4 (pendidikan berkualitas) "
      "serta SDG 10 (berkurangnya kesenjangan). Profil nilai jual dan analisis strategisnya dimuat pada Lampiran F.")

# ------------------------------------------------------------------ 1) tulis ulang Latar Belakang
first = find_par("Transformasi digital dalam pendidikan tinggi")
seq = [first]
cur = first
for pre in ["Masalah tersebut menjadi lebih kritis", "Konteks pendidikan tinggi memperkuat", "Pada konteks Indonesia yang menjadi sasaran"]:
    seq.append(find_par(pre))
old_extra = [find_par(x) for x in ["Permasalahan menjadi semakin kompleks", "Penggunaan Generative AI/Vision-Language",
                                     "Kebutuhan terhadap mekanisme verifikasi", "Berdasarkan kondisi tersebut, penelitian ini mengembangkan"]]
for p, txt in zip(seq, [P1, P2, P3, P4]):
    set_text(p, txt)
for p in old_extra:
    p.getparent().remove(p)
p_vlm = find_par("VLM tampak menjanjikan")
p_vlm.getparent().remove(p_vlm)
set_text(find_par("Masalah yang sama dialami mahasiswa lain"), P5)
set_text(find_par("Kesenjangan ini terletak pada perangkat"), P6)

# ------------------------------------------------------------------ 2) tautan rujukan baru di Bab II/III
# konversi sitasi lama "[n]" / "[n, m]" menjadi token kunci pada paragraf lain (di luar daftar referensi)
new_par_ids = {id(p) for p in seq} | {id(find_par("Masalah yang sama dialami mahasiswa yang memilih")), id(find_par("Kesenjangannya terletak pada"))}
ref_ids = {id(p) for p in ref_pars}
cite_old = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
for p in all_pars():
    if id(p) in ref_ids or id(p) in new_par_ids:
        continue
    if not cite_old.search(ptext(p)):
        continue
    merge_runs(p)
    n_para = len(cite_old.findall(ptext(p)))
    n_run = 0
    for t in p.iter(qn("w:t")):
        if t.text and cite_old.search(t.text):
            def rep(m):
                keys = [f"@r{int(x)}" for x in re.split(r"\s*,\s*", m.group(1))]
                return "[" + ",".join(keys) + "]"
            n_run += len(cite_old.findall(t.text))
            t.text = cite_old.sub(rep, t.text)
    assert n_run == n_para, ("sitasi terbelah antar-run", ptext(p)[:80], n_para, n_run)

# Bab II.A
p = find_par("WCAG 2.2 mensyaratkan")
patch(p, "diukur pada makalah ilmiah [@r6,@r7]", "diukur pada makalah ilmiah sejak lebih dari satu dekade lalu [@nganji,@r6,@r7]")
# Bab II.B
p = find_par("Di sisi model, kemampuan VLM")
patch(p, "cara kerja alat tersebut [@r12].",
      "cara kerja alat tersebut [@r12]. Studi AI generatif bagi mahasiswa tunanetra melaporkan persepsi manfaat dari wawancara [@khlaif], dan "
      "HI-Captioner dievaluasi pada foto alami [@hicap]; keduanya belum mengukur kesetiaan deskripsi grafik terhadap datanya.")
# Bab II.E
p = find_par("Ringkasnya, alat remediasi")
patch(p, "(setiap deskripsi terverifikasi atau ditandai).",
      "(setiap deskripsi terverifikasi atau ditandai). Matriks pembanding dan peta posisi "
      "dimuat pada Lampiran F.5 dan F.6.")
# Bab III.G, F
p = find_par("Risiko utama adalah halusinasi")
patch(p, "Risiko utama adalah halusinasi", "Risiko utama (Lampiran F.12) adalah halusinasi")
p = find_par("Rencana kerja memuat titik keputusan")
patch(p, "Rencana kerja memuat titik keputusan lebih awal.", "Rencana kerja (Lampiran F.13) memuat titik keputusan lebih awal.")



# ------------------------------------------------------------------ 2a) rencana data babak final (Bab III.D, Tabel V, G6, Batasan, jadwal)
import json, os
FS = {}
_fs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Audit", "Skala", "frame_stats.json")
if os.path.exists(_fs):
    FS = json.load(open(_fs))
_f = lambda x: f"{x:,}".replace(",", ".")
frame_txt = (f"bingkai {_f(FS['n'])} PDF dari {_f(FS['d'])} domain ({FS['paneN']} panen), {_f(FS['n_materi'])} berciri materi kuliah; " if FS else "ukuran bingkai diukur pada 1–3 Okt.; ")

P_DATA = ("Tabel V merinci data yang dipakai; Lampiran G memuat inventaris, metadata, dan pemetaannya ke fitur prototipe. "
          "Setiap sumber dibagi menjadi set pengembangan, untuk merancang aturan tambal, skema ekstraksi, dan ambang gerbang, dan set "
          "uji tertahan yang tidak disentuh sampai versi dibekukan. Audit awal (28 PDF) hanya memberi selang sekitar ±17 poin "
          "persentase dan bukan sampel acak; babak final memakai bingkai publik (indeks Common Crawl, PDF pada domain ac.id [@cc]) "
          "dengan sampel acak berstrata 600 PDF berbahasa Indonesia (400 materi kuliah menurut aturan URL, 200 dokumen akademik lain; "
          "maksimum 12 dokumen per domain) berselang sekitar ±5 poin pada stratum materi kuliah, dengan bootstrap per kampus dan "
          "tangkapan terpotong dilengkapi korpus SafeDocs [@safedocs]. Ukuran 60 dokumen G6 dipilih agar hasil teramati 90% berbatas "
          "bawah selang Wilson sekitar 80%.")
set_text(find_par("Tabel V merinci seluruh data."), P_DATA)

# Tabel V
tblV = next(t for t in body.iter(qn("w:tbl")) if ptext(t).startswith("TABEL V."))
rowsV = tblV.findall(qn("w:tr"))
tmpl = copy.deepcopy(rowsV[2])
for r in rowsV[2:]:
    tblV.remove(r)
NEW_V = [
    ["Bingkai publik materi kuliah (indeks Common Crawl; PDF pada domain ac.id)",
     "Metadata indeks terbuka [@cc]; berkas dari arsip publik dan SafeDocs [@safedocs]",
     frame_txt + "sampel berstrata 600 PDF (400 materi kuliah, 200 lain); 2:1 pengembangan dan uji per kampus",
     "Audit skala besar; aturan tambal dan penyaring gambar dekoratif (STR-01, OUT-01, CLS-01); sumber 60 dokumen G6"],
    ["Audit awal materi kuliah", "Tautan publik; berkas tidak disebarluaskan", "28 PDF; 3.229 halaman; 18 kampus (terukur)",
     "Uji coba protokol; bukti awal urgensi"],
    ["Set sintetis penulis (dokumen, grafik berbahasa Indonesia, rumus)", "Dibuat penulis",
     "30 dokumen, 150 grafik, 200 rumus (target)", "Acuan pasti G2–G5; dibagi pengembangan dan uji"],
    ["Grafik publik: VisText [@r26], ChartQA [@chartqa]", "Publik (VisText GPL-3.0); bahasa Inggris",
     "12.441 grafik (VisText); subset 300 (150 pengembangan, 150 uji)",
     "Skema ekstraksi tabel data dan ambang θe (CHT-01, CHT-02); uji komponen G3"],
    ["Rumus dan tabel publik: UniMER-Test [@r35], IndoTabVQA [@r27]", "Publik",
     "23.789 rumus; 1.593 citra tabel Indonesia; subset 200 rumus, 300 citra tabel",
     "Memilih pengenal rumus (G5) dan tulang punggung tabel: OpenDataLoader atau Docling (G2)"],
]
for vals in NEW_V:
    row = copy.deepcopy(tmpl)
    for tc, v in zip(row.findall(qn("w:tc")), vals):
        ps = tc.findall(qn("w:p"))
        for extra in ps[1:]:
            tc.remove(extra)
        set_text(ps[0], v, sz=17, lang="id-ID")
    tblV.append(row)

# ambang G6, batasan, jadwal
def patch_opt(p, old, new):
    try:
        patch(p, old, new); return True
    except AssertionError as e:
        print("PERINGATAN:", e); return False
patch_opt(find_par("Audit 20–30 dokumen dengan rubrik penulis"), "Audit 20–30 dokumen dengan rubrik penulis", "60 dokumen dari set uji sampel acak bingkai publik; rubrik penulis")
patch_opt(find_par("Penelitian ini memiliki tujuh batasan."), "angkanya tidak mewakili seluruh kampus.", "angkanya tidak mewakili seluruh kampus; audit skala besar dengan sampel acak dirancang untuk babak final (Lampiran G).")
RENCANA = ("Rencana kerja (Lampiran F.13) memuat titik keputusan lebih awal. Pada 1–3 Oktober dijalankan dua uji penentu, yaitu "
           "ekstraksi tabel data dari grafik sintetis berbahasa Indonesia oleh VLM dan validasi veraPDF pada lima materi nyata dari set pengembangan, "
           "bersama pengambilan sampel dan audit skala besar (Lampiran G) yang berjalan otomatis. Selanjutnya, 4–9 Oktober untuk "
           "perakitan keluaran (STR-01, OUT-01) dan G1; 10–15 Oktober untuk modul grafik, gerbang, G3, dan G4; 16–19 Oktober untuk "
           "antarmuka tinjauan, G6, dan modul rumus bila waktu tersedia; 20–22 Oktober untuk pembekuan versi, evaluasi pada set uji "
           "tertahan, dan penulisan Bab IV–V; serta 23 Oktober untuk pengumpulan. Lingkup minimum demo adalah unggah PDF, keluaran "
           "HTML aksesibel dan PDF bertag, deskripsi grafik dengan gerbang, dan antrean tinjauan; hasil dokumen contoh disimpan "
           "sebelumnya (*cache*) karena demo dibatasi 15 menit dan bergantung pada layanan VLM. Ditunda: PowerPoint dan Word "
           "langsung, braille, dan G7; rumus yang belum dapat diproses ditahan ke antrean tinjauan (*fail-closed*).")
set_text(find_par("Rencana kerja (Lampiran F.13)"), RENCANA)

# ganti Gambar 2 (alur penelitian) dengan versi yang memuat rencana data baru
_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Diagram", "Gambar_Alur_Penelitian.png")
_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_done = False
for ip in body.iter(qn("wp:inline")):
    dp = ip.find(qn("wp:docPr"))
    if dp is not None and dp.get("descr", "").startswith("Diagram alur penelitian"):
        rid = ip.find(".//" + _A + "blip").get(_R + "embed")
        d.part.related_parts[rid]._blob = open(_png, "rb").read()
        dp.set("descr", "Diagram alur penelitian. Data dari empat sumber (bingkai publik Common Crawl, dokumen sintetis, benchmark publik, dokumen nyata G6) dipisah menjadi set pengembangan dan set uji tertahan; sistem dikembangkan pada set pengembangan lalu dievaluasi pada gerbang G1 sampai G6 pada set uji tertahan, dan G7 ditunda.")
        _done = True
assert _done, "gambar alur penelitian tidak ditemukan"

# ------------------------------------------------------------------ 2b) pemadatan agar muat 10 halaman
# hapus baris tabel VIII tentang suara id-ID (informasi sama tetap ada di Bab III.B dan Tabel VI)
for tr in list(body.iter(qn("w:tr"))):
    if ptext(tr).startswith("Suara bahasa Indonesia untuk mode dengar"):
        tr.getparent().remove(tr)
        break
else:
    raise AssertionError("baris suara tidak ditemukan")
# skala gambar 15 cm -> 13,8 cm
for ip in body.iter(qn("wp:inline")):
    ext = ip.find(qn("wp:extent"))
    if int(ext.get("cx")) >= 5400000:
        k = 12.6 / 15.0
        ext.set("cx", str(int(int(ext.get("cx")) * k))); ext.set("cy", str(int(int(ext.get("cy")) * k)))
        for a in ip.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}ext"):
            a.set("cx", str(int(int(a.get("cx")) * k))); a.set("cy", str(int(int(a.get("cy")) * k)))

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'koherensi_v8.py'), encoding='utf8').read())

# ------------------------------------------------------------------ 3) nomori ulang menurut urutan kemunculan
tok = re.compile(r"\[(@[A-Za-z0-9_]+(?:,@[A-Za-z0-9_]+)*)\]")
order = []
for p in all_pars():
    if id(p) in ref_ids:
        continue
    for t in p.iter(qn("w:t")):
        if t.text:
            for m in tok.finditer(t.text):
                for k in m.group(1).split(","):
                    k = k[1:]
                    if k not in order:
                        order.append(k)
missing = [k for k in order if k not in REFS]
assert not missing, missing
unused = [k for k in REFS if k not in order]
print("referensi dipakai:", len(order), "| tidak dikutip:", unused)
num = {k: i + 1 for i, k in enumerate(order)}
for p in all_pars():
    if id(p) in ref_ids:
        continue
    for t in p.iter(qn("w:t")):
        if t.text and tok.search(t.text):
            def rep(m):
                ns = sorted(num[k[1:]] for k in m.group(1).split(","))
                return "[" + ", ".join(str(n) for n in ns) + "]"
            t.text = tok.sub(rep, t.text)

# ------------------------------------------------------------------ 4) bangun ulang daftar referensi
anchor = ref_pars[0]
parent = anchor.getparent()
idx = list(parent).index(anchor)
for p in ref_pars:
    parent.remove(p)
for k in order:
    np_ = copy.deepcopy(template_ref_par)
    for c in list(np_):
        if c.tag != qn("w:pPr"):
            np_.remove(c)
    np_.append(mk_run(f"[{num[k]}]", sz=16, lang="id-ID"))
    r = OxmlElement("w:r"); rp = OxmlElement("w:rPr")
    s = OxmlElement("w:sz"); s.set(qn("w:val"), "16"); rp.append(s)
    s = OxmlElement("w:szCs"); s.set(qn("w:val"), "16"); rp.append(s)
    r.append(rp); r.append(OxmlElement("w:tab")); np_.append(r)
    np_.append(mk_run(REFS[k], sz=16, lang="id-ID"))
    parent.insert(idx, np_); idx += 1

d.save(DST)
print("tersimpan:", DST)
import json
json.dump({"order": order}, open(DST + ".order.json", "w"))
