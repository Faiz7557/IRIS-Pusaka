# -*- coding: utf-8 -*-
"""Langkah 5 (untuk prototipe CLS-01): ekspor gambar sampel dari PDF pengembangan/uji untuk dilabeli dua penilai.
Kelas: grafik | tabel_citra | rumus | foto_diagram | dekoratif.
Jalankan: python 05_ekspor_gambar_label.py manifest_sampel.csv 200 100
Keluaran: label_gambar/{dev,uji}/*.png dan label_gambar.csv (kolom penilai_1, penilai_2 dikosongkan).
Gambar dipakai hanya untuk pelabelan internal dan tidak disebarluaskan.
"""
import sys, os, csv, random, hashlib
import fitz
import pandas as pd

man = pd.read_csv(sys.argv[1], encoding="utf-8-sig")
n_dev, n_uji = int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(20260930)
rows = []
for st, n in (("dev", n_dev), ("uji", n_uji)):
    os.makedirs(f"label_gambar/{st}", exist_ok=True)
    cand = []
    for _, r in man[(man["status"] == "ok") & (man["set"] == st)].iterrows():
        try:
            d = fitz.open(os.path.join("unduhan", r["berkas"]))
        except Exception:
            continue
        for pno in range(min(len(d), 60)):
            for im in d[pno].get_images(full=True):
                if im[2] >= 60 and im[3] >= 60:
                    cand.append((r["berkas"], pno, im[0], im[2], im[3]))
    rng.shuffle(cand)
    seen = set(); k = 0
    for berkas, pno, xref, w, h in cand:
        if k >= n:
            break
        d = fitz.open(os.path.join("unduhan", berkas))
        try:
            pix = fitz.Pixmap(d, xref)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            hsh = hashlib.md5(pix.samples).hexdigest()[:10]
            if hsh in seen:
                continue
            seen.add(hsh)
            name = f"{st}_{k:04d}.png"
            pix.save(f"label_gambar/{st}/{name}")
        except Exception:
            continue
        rows.append(dict(id=name, set=st, dokumen=berkas, halaman=pno + 1, lebar=w, tinggi=h, hash=hsh, penilai_1="", penilai_2=""))
        k += 1
    print(st, "gambar diekspor:", k)
pd.DataFrame(rows).to_csv("label_gambar.csv", index=False, encoding="utf-8-sig")
