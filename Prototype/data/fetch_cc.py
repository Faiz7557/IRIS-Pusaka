"""Sampel kecil dokumen nyata dari bingkai Common Crawl (PDF pada domain ac.id).

Aturan URL stratum A (materi kuliah) dan pengecualiannya mengikuti Lampiran G.3.
Berkas diambil dari arsip WARC publik (range request), bukan dari server kampus.
Hanya metadata dan hitungan agregat yang dilaporkan; berkas tidak disebarluaskan.
"""
import gzip
import io
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

CRAWL = "CC-MAIN-2026-39"
OUT = Path(__file__).resolve().parent / "cc"
SEED = 20260930
DOMAINS = ["unair.ac.id", "ui.ac.id", "ugm.ac.id", "its.ac.id", "ub.ac.id", "undip.ac.id", "unpad.ac.id",
           "uny.ac.id", "unesa.ac.id", "uns.ac.id", "unhas.ac.id", "usu.ac.id", "unej.ac.id", "um.ac.id",
           "unila.ac.id", "unsri.ac.id", "untan.ac.id", "unud.ac.id", "umy.ac.id", "uii.ac.id"]
INCL = re.compile(r"slide|materi|bahan[-_ ]?ajar|modul|pertemuan|handout|diktat|kuliah|presentasi|ppt|rps|sap", re.I)
EXCL = re.compile(r"skripsi|tesis|thesis|jurnal|journal|prosiding|surat|laporan|pedoman|panduan|akreditasi|"
                  r"repository|eprints|digilib|sk[-_]|pengumuman|brosur|kalender", re.I)


def get(url, timeout=90, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "SIMAK-research/0.1 (ICC2026 audit)", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def query(domain):
    q = urllib.parse.urlencode({"url": domain, "matchType": "domain", "filter": "mime-detected:application/pdf",
                                "output": "json", "limit": "3000"})
    try:
        raw = get(f"https://index.commoncrawl.org/{CRAWL}-index?{q}").decode()
    except Exception as e:
        print(domain, "gagal:", e)
        return []
    rows = [json.loads(l) for l in raw.splitlines() if l.startswith("{")]
    return rows


def fetch(row) -> bytes | None:
    off, length = int(row["offset"]), int(row["length"])
    data = get(f"https://data.commoncrawl.org/{row['filename']}",
               headers={"Range": f"bytes={off}-{off + length - 1}"})
    rec = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
    parts = rec.split(b"\r\n\r\n", 2)  # header WARC, header HTTP, isi
    body = parts[2] if len(parts) == 3 else b""
    return body if body.startswith(b"%PDF") else None


def main(n_target=12):
    OUT.mkdir(parents=True, exist_ok=True)
    frame = []
    for d in DOMAINS:
        rows = query(d)
        a = [r for r in rows if INCL.search(r["url"]) and not EXCL.search(r["url"]) and r.get("status") == "200"]
        print(f"{d}: {len(rows)} PDF, {len(a)} lolos aturan materi kuliah", flush=True)
        frame += [{**r, "domain": d} for r in a if not r.get("truncated")]
        time.sleep(1)
    rnd = random.Random(SEED)
    rnd.shuffle(frame)
    picked, per_dom = [], {}
    for r in frame:
        if len(picked) >= n_target:
            break
        if per_dom.get(r["domain"], 0) >= 2:
            continue
        try:
            pdf = fetch(r)
        except Exception as e:
            print("unduh gagal:", e)
            continue
        if not pdf:
            continue
        name = f"cc_{len(picked) + 1:02d}_{r['domain'].split('.')[0]}.pdf"
        (OUT / name).write_bytes(pdf)
        picked.append({"file": name, "url": r["url"], "domain": r["domain"], "bytes": len(pdf)})
        per_dom[r["domain"]] = per_dom.get(r["domain"], 0) + 1
        print("ambil", name, len(pdf), flush=True)
    meta = {"crawl": CRAWL, "seed": SEED, "domain_dicoba": len(DOMAINS), "bingkai_stratum_A": len(frame),
            "sampel": picked}
    (OUT / "cc.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"bingkai {len(frame)}, sampel {len(picked)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12)
