# -*- coding: utf-8 -*-
"""Langkah 1b: ringkasan bingkai dan stratum 'materi kuliah' (aturan URL). Menulis frame_stats.json.
Jalankan setelah 01_bingkai_cc.py selesai: python 01b_ringkasan_bingkai.py "bingkai_*.parquet"
"""
import sys, re, json, urllib.parse
import duckdb

KEY = re.compile(r"(slide|materi|bahan[-_ ]?ajar|modul|module|pertemuan|handout|diktat|lecture|kuliah|presentasi|presentation|"
                 r"\bppt|mata[-_ ]?kuliah|perkuliahan|minggu[-_ ]?\d|week[-_ ]?\d|pert[-_ ]?\d|\bsap\b|\brps\b)", re.I)
NEG = re.compile(r"(skripsi|tesis|thesis|disertasi|jurnal|journal|prosiding|proceeding|surat|laporan|lpj|pedoman|panduan|"
                 r"akreditasi|abstrak|abstract|artikel|article|publikasi|sk[-_]|keputusan|pengumuman|brosur|katalog|cover|sertifikat)", re.I)


def is_m(u):
    p = urllib.parse.unquote(urllib.parse.urlparse(u).path).lower()
    return bool(KEY.search(p)) and not NEG.search(p)


f = sys.argv[1]
con = duckdb.connect()
rows = con.execute(f"SELECT url, dom, terpotong FROM read_parquet('{f}')").fetchall()
uniq = {}
for u, dm, tr in rows:
    uniq.setdefault(u, (dm, tr))
M = {u: v for u, v in uniq.items() if is_m(u)}
n_neg = sum(1 for u in uniq if NEG.search(urllib.parse.unquote(urllib.parse.urlparse(u).path).lower()))
stats = dict(paneN=len(__import__("glob").glob("bingkai_*.parquet")), n=len(uniq), d=len({v[0] for v in uniq.values()}), utuh=sum(1 for v in uniq.values() if v[1] is None),
             n_materi=len(M), d_materi=len({v[0] for v in M.values()}), utuh_materi=sum(1 for v in M.values() if v[1] is None), n_pengecualian=n_neg, n_lain=len(uniq)-len(M)-n_neg)
json.dump(stats, open("frame_stats.json", "w"))
print(stats)
top = {}
for u, (dm, tr) in M.items():
    top[dm] = top.get(dm, 0) + 1
print("domain terbanyak (stratum materi):", sorted(top.items(), key=lambda x: -x[1])[:5])
print("domain dengan >=12 dokumen (batas per domain berlaku):", sum(1 for v in top.values() if v >= 12))
