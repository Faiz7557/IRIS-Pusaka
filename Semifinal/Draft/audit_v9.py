# -*- coding: utf-8 -*-
"""Audit kepenulisan dan format: v8 -> v9 (langsung pada .docx, tanpa content.py).
Cakupan: ejaan/tanda baca, italik istilah asing dan variabel, subskrip, rujukan persamaan sesuai template,
spasi tanpa putus, huruf tabel 9 pt (template), italik pada daftar referensi, dan penyeragaman bahasa korektur.
Pemakaian: python audit_v9.py SUMBER.docx TUJUAN.docx
"""
import copy, re, sys
import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC, DST = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
body = d.element.body
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
NBSP = " "

def ptext(p):
    return "".join(t.text or "" for t in p.iter(qn("w:t")))

def all_pars():
    return list(body.iter(qn("w:p")))

pars = all_pars()
i_ref = next(i for i, p in enumerate(pars) if ptext(p).strip() == "REFERENSI")
i_lamp = next(i for i, p in enumerate(pars) if ptext(p).startswith("Lampiran A."))
i_lampF = next(i for i, p in enumerate(pars) if ptext(p).startswith("Lampiran F."))
REF_IDS = {id(p) for p in pars[i_ref + 1:i_lamp]}
APP_IDS = {id(p) for p in pars[i_lamp:]}          # semua paragraf lampiran
LAMPF_IDS = {id(p) for p in pars[i_lampF:]}

def pstyle(p):
    ppr = p.find(qn("w:pPr"))
    s = ppr.find(qn("w:pStyle")) if ppr is not None else None
    return s.get(qn("w:val")) if s is not None else ""

# ------------------------------------------------------------------ utilitas run
RANK = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike", "outline", "shadow", "emboss",
        "imprint", "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz", "szCs",
        "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath"]

def rpr_set(rpr, name, val=None):
    """Tambah/ubah elemen rPr pada urutan skema yang benar."""
    ex = rpr.find(qn("w:" + name))
    if ex is None:
        ex = OxmlElement("w:" + name)
        rk = RANK.index(name)
        pos = len(rpr)
        for k, c in enumerate(rpr):
            tag = c.tag.split("}")[1]
            if tag in RANK and RANK.index(tag) > rk:
                pos = k
                break
        rpr.insert(pos, ex)
    if val is not None:
        ex.set(qn("w:val"), val)
    return ex

def rpr_del(rpr, name):
    for e in rpr.findall(qn("w:" + name)):
        rpr.remove(e)

def is_on(rpr, name):
    e = rpr.find(qn("w:" + name)) if rpr is not None else None
    return e is not None and e.get(qn("w:val")) not in ("0", "false")

def simple_run(r):
    kids = [k for k in r if k.tag != qn("w:rPr")]
    return len(kids) == 1 and kids[0].tag == qn("w:t")

def mk_piece(base, text, italic=None, sub=None):
    n = copy.deepcopy(base)
    rpr = n.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr"); n.insert(0, rpr)
    if italic is True:
        rpr_set(rpr, "i"); rpr_set(rpr, "iCs")
    elif italic is False:
        rpr_del(rpr, "i"); rpr_del(rpr, "iCs")
    if sub:
        rpr_set(rpr, "vertAlign", "subscript")
    t = n.find(qn("w:t")); t.text = text; t.set(XML_SPACE, "preserve")
    return n

def restyle(p, regex, pieces_fn, only_nonitalic=False):
    """Pecah run sederhana yang memuat regex; pieces_fn(match) -> [(teks, italic, sub)] menggantikan bagian yang cocok."""
    n_hit = 0
    for r in [c for c in p if c.tag == qn("w:r")]:
        if not simple_run(r):
            continue
        rpr = r.find(qn("w:rPr"))
        if only_nonitalic and is_on(rpr, "i"):
            continue
        t = r.find(qn("w:t")); txt = t.text or ""
        ms = list(regex.finditer(txt))
        if not ms:
            continue
        out, pos = [], 0
        for m in ms:
            if m.start() > pos:
                out.append(mk_piece(r, txt[pos:m.start()]))
            for (tx, it, sb) in pieces_fn(m):
                out.append(mk_piece(r, tx, it, sb))
            pos = m.end()
        if pos < len(txt):
            out.append(mk_piece(r, txt[pos:]))
        parent = r.getparent(); idx = parent.index(r)
        parent.remove(r)
        for k, o in enumerate(out):
            parent.insert(idx + k, o)
        n_hit += len(ms)
    return n_hit

def patch_all(old, new, expect=1, scope=None):
    """Ganti teks pada satu w:t (harus berada dalam satu run); NBSP diperlakukan sebagai spasi dan dipulihkan pada langkah 6."""
    n = 0
    for p in all_pars():
        if scope is not None and id(p) not in scope:
            continue
        for t in p.iter(qn("w:t")):
            if t.text:
                norm = t.text.replace(NBSP, " ")
                if old in norm:
                    n += norm.count(old)
                    t.text = norm.replace(old, new)
                    t.set(XML_SPACE, "preserve")
    assert n == expect, f"patch {old[:50]!r}: ditemukan {n}, diharapkan {expect}"

def find_par(prefix, nth=0):
    hits = [p for p in all_pars() if ptext(p).replace(NBSP, " ").startswith(prefix)]
    assert len(hits) > nth, f"paragraf tidak ditemukan: {prefix!r}"
    return hits[nth]

# ================================================================== 1) PERBAIKAN KEPENULISAN (teks)
# Abstrak: kalimat data dipecah agar tidak ambigu (jumlah kata dijaga <= 250)
patch_all("Evaluasi dirancang melalui tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian, memakai sampel acak "
          "berstrata dari bingkai publik 228.383 PDF domain kampus, dokumen sintetis, dan benchmark publik yang dibagi menjadi "
          "set pengembangan dan uji tertahan; uji pada mahasiswa tunanetra ditunda.",
          "Evaluasi dirancang melalui tujuh gerbang dengan kriteria lulus yang dikunci sebelum pengujian. Datanya berupa sampel "
          "acak berstrata dari 228.383 PDF domain kampus, dokumen sintetis, dan benchmark publik yang dipisah menjadi set "
          "pengembangan dan set uji tertahan; uji pada mahasiswa tunanetra ditunda.")
patch_all("Makalah ini belum melaporkan kinerja sistem; hasil implementasi dan evaluasi disajikan pada tahap final.",
          "Makalah ini belum melaporkan kinerja sistem; hasilnya disajikan pada tahap final.")
patch_all("statistiknya dihitung oleh kode,", "statistiknya dihitung kode,")
# Kata kunci diakhiri titik (template)
kw = find_par("Kata Kunci")
last_t = [t for t in kw.iter(qn("w:t"))][-1]
if not last_t.text.rstrip().endswith("."):
    last_t.text = last_t.text.rstrip() + "."

# Bab I
patch_all("Staf unit layanan disabilitas melaporkan bahwa AI generatif meningkatkan kecepatan dan kepercayaan diri dalam menulis deskripsi gambar",
          "Studi pada staf unit layanan disabilitas menunjukkan bahwa AI generatif meningkatkan kecepatan dan kepercayaan diri mereka dalam menulis deskripsi gambar")
patch_all("seperti MSCOCO dan Flickr", "seperti MS COCO dan Flickr")
patch_all("Sistem menerima PDF apa adanya", "Sistem ini menerima PDF apa adanya")
patch_all("mendukung SDG 4 (pendidikan berkualitas) serta SDG 10 (berkurangnya kesenjangan)",
          "mendukung SDG (Sustainable Development Goals) 4 (pendidikan berkualitas) serta 10 (berkurangnya kesenjangan)")
patch_all("3.128 di 282 PT;", "3.128 di 282 perguruan tinggi;")
patch_all("<3,2% dari 20.000 PDF", "kurang dari 3,2% dari 20.000 PDF")
patch_all("Setiap gambar, grafik, dan rumus beralternatif teks atau berstatus “ditahan”",
          "Setiap gambar, grafik, dan rumus memiliki teks alternatif atau berstatus “ditahan”")
patch_all("PDF hasil pindai ditangani manual dan berkas PowerPoint", "PDF hasil pindai ditangani secara manual dan berkas PowerPoint")
# Bab II: sitasi mengikuti nama penulis (gaya IEEE)
patch_all("Kumar dkk. membangun tolok ukur", "Kumar dkk. [30] membangun tolok ukur")
patch_all("penilaian manusia [30]. Rancangan evaluasi", "penilaian manusia. Rancangan evaluasi")
# Bab III.D
patch_all("Setiap sumber dibagi menjadi set pengembangan, untuk merancang aturan tambal, skema ekstraksi, dan ambang gerbang, dan set "
          "uji tertahan yang tidak disentuh sampai versi dibekukan. Audit awal (28 PDF) hanya memberi selang sekitar ±17 poin "
          "persentase dan bukan sampel acak; babak final memakai bingkai publik (indeks Common Crawl, PDF pada domain ac.id [54]) "
          "dengan sampel acak berstrata 600 PDF berbahasa Indonesia (400 materi kuliah menurut aturan URL, 200 dokumen akademik lain; "
          "maksimum 12 dokumen per domain) berselang sekitar ±5 poin pada stratum materi kuliah, dengan bootstrap per kampus dan "
          "tangkapan terpotong dilengkapi korpus SafeDocs [55]. Ukuran 60 dokumen G6 dipilih agar hasil teramati 90% berbatas "
          "bawah selang Wilson sekitar 80%.",
          "Setiap sumber dibagi menjadi set pengembangan, yang dipakai untuk merancang aturan tambal, skema ekstraksi, dan ambang "
          "gerbang, serta set uji tertahan, yang tidak disentuh sampai versi dibekukan. Audit awal (28 PDF) hanya memberi selang "
          "sekitar ±17 poin persentase dan bukan sampel acak. Babak final memakai bingkai publik (indeks Common Crawl, PDF pada "
          "domain ac.id [54]) dengan sampel acak berstrata 600 PDF berbahasa Indonesia (400 materi kuliah menurut aturan URL dan "
          "200 dokumen akademik lain; maksimum 12 dokumen per domain) yang berselang sekitar ±5 poin pada stratum materi kuliah. "
          "Selang dihitung dengan bootstrap per kampus, dan tangkapan yang terpotong dilengkapi dengan korpus SafeDocs [55]. Ukuran "
          "60 dokumen G6 dipilih agar hasil teramati 90% menghasilkan batas bawah selang Wilson sekitar 80%.")
patch_all("bingkai 228.383 PDF dari 1.833 domain", "Bingkai 228.383 PDF dari 1.833 domain")

# Tabel VI: rujukan persamaan diberi kata pengantar agar tetap terbaca tanpa "Pers."
patch_all("dua kali [40, 41]; Pers. (2); ", "dua kali [40, 41]; selisih relatif Pers. (2); ")
patch_all("dan pengenal kedua; Pers. (6)", "dan pengenal kedua; kecocokan Pers. (6)")
patch_all("Aturan Pers. (7); klaim Pers. (5); ambang ", "Aturan Pers. (7); klaim Pers. (5); ambang ")
# kalimat tidak dimulai dengan nama yang berhuruf kecil
patch_all("veraPDF adalah validator sumber terbuka yang menerapkan aturan tersebut, tetapi hanya memeriksa",
          "Validator sumber terbuka veraPDF menerapkan aturan tersebut, tetapi hanya memeriksa")

# pemadatan tanpa mengubah substansi: kalimat tautologis dihapus
patch_all(" beserta ukuran pembuktinya dan status buktinya hari ini; manfaat yang belum diukur dinyatakan sebagai belum diukur.",
          " beserta ukuran pembuktinya dan status buktinya hari ini.")

# ================================================================== 2) RUJUKAN PERSAMAAN (template: "(1)", bukan "Pers. (1)")
n_pers = 0
for p in all_pars():
    for t in p.iter(qn("w:t")):
        if t.text and "Pers." in t.text:
            x = t.text.replace(NBSP, " ")
            x = re.sub(r",\s+Pers\.\s+\((\d+)\)", lambda m: " (" + m.group(1) + ")", x)
            x, k = re.subn(r"Pers\.\s+\(?(\d+)\)?", lambda m: "(" + m.group(1) + ")", x)
            t.text = x; t.set(XML_SPACE, "preserve"); n_pers += k
print("rujukan persamaan diseragamkan:", n_pers)
# kalimat yang dimulai dengan rujukan persamaan tidak ada (sudah "Persamaan (5)")

# ================================================================== 3) LAMPIRAN F/G: keterangan gambar tidak dimiringkan seluruhnya
n_deital = 0
for p in all_pars():
    if id(p) not in LAMPF_IDS:
        continue
    runs = [r for r in p if r.tag == qn("w:r") and simple_run(r)]
    txt = ptext(p)
    if runs and len(txt) > 40 and all(is_on(r.find(qn("w:rPr")), "i") for r in runs) and not txt.startswith("Gambar"):
        for r in runs:
            rpr = r.find(qn("w:rPr")); rpr_del(rpr, "i"); rpr_del(rpr, "iCs")
        n_deital += 1
print("keterangan lampiran ditegakkan:", n_deital)

# butir bertitik pada Lampiran G: gunakan indentasi gantung
n_bul = 0
for p in all_pars():
    txt = ptext(p)
    if id(p) in APP_IDS and txt.startswith("• "):
        first = next(t for t in p.iter(qn("w:t")))
        first.text = first.text[2:]
        ppr = p.find(qn("w:pPr"))
        ind = ppr.find(qn("w:ind"))
        if ind is None:
            ind = OxmlElement("w:ind")
            # w:ind harus sebelum w:jc
            jc = ppr.find(qn("w:jc"))
            (jc.addprevious(ind) if jc is not None else ppr.append(ind))
        ind.set(qn("w:left"), "227"); ind.set(qn("w:hanging"), "227")
        # sisipkan run "• <tab>"
        r0 = next(r for r in p if r.tag == qn("w:r"))
        bl = copy.deepcopy(r0)
        for k in list(bl):
            if k.tag != qn("w:rPr"): bl.remove(k)
        bt = OxmlElement("w:t"); bt.text = "•"; bl.append(bt)
        bl.append(OxmlElement("w:tab"))
        r0.addprevious(bl)
        n_bul += 1
print("butir diberi indentasi gantung:", n_bul)

# ================================================================== 4) VARIABEL: italik + subskrip
def V(text, it=True, sub=False): return (text, it, sub)
# θe, θr
for p in all_pars():
    if id(p) in REF_IDS: continue
    restyle(p, re.compile(r"θ([er])(?![A-Za-z])"), lambda m: [V("θ"), V(m.group(1), False, True)], only_nonitalic=True)
# n = 60, n = 30
for p in all_pars():
    if id(p) in REF_IDS: continue
    restyle(p, re.compile(r"\bn(?= = \d)"), lambda m: [V("n")], only_nonitalic=True)
# "dan z kuantil", "laju penahanan R", "rasio Q pada G4"
p = find_par("dengan p̂ proporsi teramati"); restyle(p, re.compile(r"(?<=dan )z(?= kuantil)"), lambda m: [V("z")], only_nonitalic=True)
for p in all_pars():
    if id(p) in REF_IDS: continue
    restyle(p, re.compile(r"(?<=penahanan )R\b"), lambda m: [V("R")], only_nonitalic=True)
    restyle(p, re.compile(r"(?<=rasio )Q(?= pada)"), lambda m: [V("Q")], only_nonitalic=True)
# Lampiran E: T1 dan T2; cF, cδ, cA, cR
pE = find_par("Rekaman elemen memuat")
restyle(pE, re.compile(r"\bT([12])\b"), lambda m: [V("T"), V(m.group(1), False, True)], only_nonitalic=True)
restyle(pE, re.compile(r"\bc([FδAR])\b"), lambda m: [V("c"), V(m.group(1), False, True)], only_nonitalic=True)
# judul kolom "n" pada tabel G.3: miring
for tbl in body.iter(qn("w:tbl")):
    rows = tbl.findall(qn("w:tr"))
    if rows and ptext(rows[0]).startswith("nSetengah lebar"):
        r = next(rows[0].iter(qn("w:r"))); rpr = r.find(qn("w:rPr")); rpr_set(rpr, "i"); rpr_set(rpr, "iCs")

# ================================================================== 5) ISTILAH ASING: miring (tidak pada judul, referensi, dan teks yang sudah miring)
FOREIGN = re.compile(
    r"(?<![A-Za-z-])(pipeline|fail-closed|vision-language|low vision|auto-tag|Auto-tag|zero-shot|benchmark|Benchmark|caption|"
    r"hash|cache|held-out|placeholder|string|binding|hybrid|cloud|screen reader|image captioning|text-to-speech|"
    r"curb-cut effect|large language model|seed|bootstrap|Figure|Artifact|MarkInfo|StructTreeRoot|Sustainable Development Goals)"
    r"(?![A-Za-z-])")
n_it = 0
for p in all_pars():
    if id(p) in REF_IDS or pstyle(p).startswith("Heading") or pstyle(p) == "Title":
        continue
    n_it += restyle(p, FOREIGN, lambda m: [V(m.group(1))], only_nonitalic=True)
print("istilah asing dimiringkan:", n_it)

# ================================================================== 6) SPASI TANPA PUTUS
NB1 = re.compile(r"\b(Tabel|Gambar|Lampiran|Persamaan|Bab|Gerbang|Level|level|SDG) (?=[\dIVXA-G(])")
NB2 = re.compile(r"(\d) (GB|detik|halaman|dokumen|PDF|persen)\b")
n_nb = 0
for p in all_pars():
    if id(p) in REF_IDS: continue
    for t in p.iter(qn("w:t")):
        if not t.text: continue
        new = NB2.sub(lambda m: m.group(1) + NBSP + m.group(2), NB1.sub(lambda m: m.group(1) + NBSP, t.text))
        if new != t.text:
            t.text = new; t.set(XML_SPACE, "preserve"); n_nb += 1
print("spasi tanpa putus:", n_nb)

# ================================================================== 7) CATATAN KAKI TABEL 9 pt (template); isi tabel tetap 8,5 pt demi batas 10 halaman
note = find_par("*Ambang awal yang dikunci")
for r in note.iter(qn("w:r")):
    rpr = r.find(qn("w:rPr"))
    for tag in ("sz", "szCs"):
        e = rpr.find(qn("w:" + tag))
        if e is not None: e.set(qn("w:val"), "18")

# ================================================================== 7b) bantalan atas-bawah sel tabel bernomor dikurangi (pemadatan)
n_mar = 0
for tbl in body.iter(qn("w:tbl")):
    if not ptext(tbl).startswith("TABEL"): continue
    mar = tbl.find(qn("w:tblPr") + "/" + qn("w:tblCellMar"))
    if mar is None: continue
    for side in ("top", "bottom"):
        e = mar.find(qn("w:" + side))
        if e is not None: e.set(qn("w:w"), "10"); n_mar += 1
print("bantalan sel atas-bawah 10 twips:", n_mar)

# ================================================================== 8) DAFTAR REFERENSI: italik judul sumber (gaya IEEE)
JOURNAL = re.compile(r"(?<=,” )([^,]+?)(?=, (?:vol\.|Art\. no\.|pp\.|no\.))")
PROC = re.compile(r"(?<=in )((?:Proc\.|Findings) .+?)(?=, (?:\d{4}|doi|pp\.))")
EXTRA = re.compile(r"(?<=,” )(detik\.com|The Conversation Indonesia|Stanford Social Innovation Review)(?=,)|(?<= )(Stanford Social Innovation Review)(?=, Winter)")
n_ri = 0
for p in pars[i_ref + 1:i_lamp]:
    for rx in (JOURNAL, PROC, EXTRA):
        n_ri += restyle(p, rx, lambda m: [V(m.group(0))], only_nonitalic=True)
print("referensi dengan judul sumber miring:", n_ri)

# ================================================================== 9) BAHASA KOREKTUR: id-ID
lang_root = d.styles.element
for lg in lang_root.iter(qn("w:lang")):
    if (lg.get(qn("w:val")) or "").startswith("en"):
        lg.set(qn("w:val"), "id-ID")
for lg in body.iter(qn("w:lang")):
    if (lg.get(qn("w:val")) or "").startswith("en"):
        lg.set(qn("w:val"), "id-ID")

# ================================================================== pemeriksaan akhir
abs_p = find_par("Abstrak")
words = len(ptext(abs_p).replace("Abstrak—", "").split())
print("kata abstrak:", words)
assert words <= 248, words
d.save(DST)
print("tersimpan:", DST)
