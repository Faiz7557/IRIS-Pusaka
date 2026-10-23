# -*- coding: utf-8 -*-
"""Langkah 2: sampel acak BERSTRATA dari bingkai (gabungan beberapa panen Common Crawl), lalu unduh dari arsip WARC publik.
Stratum A = 'materi kuliah' menurut aturan URL (ditetapkan sebelum melihat hasil); Stratum B = PDF ac.id lain yang tidak
memuat kata pengecualian (jurnal, skripsi, surat, dll.) sebagai pembanding generalisasi.
Bobot: N_stratum / n_stratum (dipakai pada estimasi gabungan). Maksimum 12 dokumen per domain per stratum.
Tangkapan terpotong TIDAK diunduh ulang dari server kampus; dicatat 'terpotong_lewati'.
Setiap dokumen diberi set 'dev' atau 'uji' menurut domain (2:1, hash ber-seed) agar kedua set tidak berbagi kampus.
Jalankan: python 02_sampel_unduh.py "bingkai_*.parquet" 480 240   (diunduh lebih banyak dari target karena ada yang bukan bahasa Indonesia)
"""
import sys, os, re, io, csv, random, hashlib, urllib.request, urllib.parse, time
from concurrent.futures import ThreadPoolExecutor
import duckdb
from warcio.archiveiterator import ArchiveIterator

SEED = 20260930
PER_DOMAIN_CAP = 12
frame_glob = sys.argv[1]
N_A = int(sys.argv[2]) if len(sys.argv) > 2 else 480
N_B = int(sys.argv[3]) if len(sys.argv) > 3 else 240
OUT = "unduhan"
os.makedirs(OUT, exist_ok=True)

KEY = re.compile(r"(slide|materi|bahan[-_ ]?ajar|modul|module|pertemuan|handout|diktat|lecture|kuliah|presentasi|presentation|"
                 r"\bppt|mata[-_ ]?kuliah|perkuliahan|minggu[-_ ]?\d|week[-_ ]?\d|pert[-_ ]?\d|\bsap\b|\brps\b)", re.I)
NEG = re.compile(r"(skripsi|tesis|thesis|disertasi|jurnal|journal|prosiding|proceeding|surat|laporan|lpj|pedoman|panduan|"
                 r"akreditasi|abstrak|abstract|artikel|article|publikasi|sk[-_]|keputusan|pengumuman|brosur|katalog|cover|sertifikat)", re.I)


def path_of(url):
    return urllib.parse.unquote(urllib.parse.urlparse(url).path).lower()


con = duckdb.connect()
rows = con.execute(f"SELECT url, host, dom, terpotong, warc_filename, off, len FROM read_parquet('{frame_glob}')").fetchall()
print("baris bingkai:", len(rows))
seen = set(); uniq = []
for r in rows:
    if r[0] in seen:
        continue
    seen.add(r[0]); uniq.append(r)
A = [r for r in uniq if KEY.search(path_of(r[0])) and not NEG.search(path_of(r[0]))]
B = [r for r in uniq if not KEY.search(path_of(r[0])) and not NEG.search(path_of(r[0]))]
print("URL unik:", len(uniq), "| domain:", len({r[2] for r in uniq}), "| A materi kuliah:", len(A), "| B lainnya:", len(B))

rng = random.Random(SEED)


def draw(pool_all, n, label):
    by = {}
    for r in pool_all:
        by.setdefault(r[2], []).append(r)
    pool = []
    for d, lst in by.items():
        rng.shuffle(lst)
        pool.extend(lst[:PER_DOMAIN_CAP])
    rng.shuffle(pool)
    pick = pool[:n]
    print(f"stratum {label}: N={len(pool_all)} domain={len(by)} kolam(cap)={len(pool)} sampel={len(pick)}")
    return [(r, label, len(pool_all) / max(len(pick), 1)) for r in pick]


sample = draw(A, N_A, "A") + draw(B, N_B, "B")
rng.shuffle(sample)


def set_of(dom):
    return "uji" if int(hashlib.sha256(f"{SEED}:{dom}".encode()).hexdigest(), 16) % 3 == 0 else "dev"


def fetch_warc(r):
    url, host, dom, trunc, fn, off, ln = r
    req = urllib.request.Request("https://data.commoncrawl.org/" + fn, headers={"Range": f"bytes={off}-{off + ln - 1}"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    for rec in ArchiveIterator(io.BytesIO(raw)):
        if rec.rec_type == "response":
            return rec.content_stream().read()
    return b""


def work(item):
    i, (r, stratum, w) = item
    base = dict(idx=i, url=r[0], dom=r[2], stratum=stratum, bobot=round(w, 3), set=set_of(r[2]))
    if r[3] is not None:
        return dict(base, status="terpotong_lewati", ukuran=0)
    err = ""; data = b""
    try:
        data = fetch_warc(r)
    except Exception as e:
        err = type(e).__name__
    if b"%PDF-" not in data[:1024]:
        return dict(base, status="bukan_pdf_atau_gagal:" + err, ukuran=len(data))
    fn = f"{i:04d}.pdf"
    open(os.path.join(OUT, fn), "wb").write(data)
    return dict(base, status="ok", ukuran=len(data), berkas=fn)


t0 = time.time()
res = []
with ThreadPoolExecutor(max_workers=16) as ex:
    for k, d in enumerate(ex.map(work, list(enumerate(sample)))):
        res.append(d)
        if (k + 1) % 100 == 0:
            print("unduh", k + 1, round(time.time() - t0), "dtk", flush=True)
with open("manifest_sampel.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["idx", "url", "dom", "stratum", "bobot", "set", "status", "ukuran", "berkas"])
    w.writeheader(); w.writerows(res)
ok = [d for d in res if d["status"] == "ok"]
print("berhasil:", len(ok), "dari", len(res), "| terpotong dilewati:", sum(1 for d in res if d["status"] == "terpotong_lewati"),
      "| A:", sum(1 for d in ok if d["stratum"] == "A"), "| B:", sum(1 for d in ok if d["stratum"] == "B"),
      "| dev:", sum(1 for d in ok if d["set"] == "dev"), "| uji:", sum(1 for d in ok if d["set"] == "uji"))
