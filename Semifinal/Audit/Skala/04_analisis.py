# -*- coding: utf-8 -*-
"""Langkah 4: analisis. Proporsi + selang Wilson (independen) dan selang bootstrap klaster (per domain/kampus).
Jalankan: python 04_analisis.py hasil_audit.csv manifest_sampel.csv
"""
import sys, math, random, csv, statistics, collections
import pandas as pd

aud = pd.read_csv(sys.argv[1], encoding="utf-8-sig")
man = pd.read_csv(sys.argv[2], encoding="utf-8-sig")
man["file"] = man["berkas"]
df = aud.merge(man[["file", "dom", "sumber", "url"]], on="file", how="left")
ok = df[df["status"] == "ok"].copy()
print("sampel diunduh:", len(man), "| berhasil dibuka:", len(ok), "| domain:", ok["dom"].nunique())
print("bahasa isi (heuristik):", ok["bahasa_isi"].value_counts().to_dict())
n_all = len(ok)
ok = ok[ok["bahasa_isi"] == "id"].copy()
print("dipertahankan (bahasa Indonesia):", len(ok), "| dikeluarkan:", n_all - len(ok), "| domain:", ok["dom"].nunique())


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def boot_cluster(sub, flag, B=2000, seed=1):
    rng = random.Random(seed)
    groups = {d: g[flag].tolist() for d, g in sub.groupby("dom")}
    keys = list(groups)
    ests = []
    for _ in range(B):
        ks = [rng.choice(keys) for _ in keys]
        num = sum(sum(groups[k]) for k in ks); den = sum(len(groups[k]) for k in ks)
        ests.append(num / den)
    ests.sort()
    return ests[int(0.025 * B)], ests[int(0.975 * B)]


def rep(name, sub, flag):
    k = int(sub[flag].sum()); n = len(sub)
    lo, hi = wilson(k, n)
    blo, bhi = boot_cluster(sub, flag)
    print(f"{name}: {k}/{n} = {100*k/n:.1f}% | Wilson {100*lo:.1f}-{100*hi:.1f} | klaster {100*blo:.1f}-{100*bhi:.1f}")


ok["lulus"] = (ok["ua1"] == "lulus").astype(int)
ok["bertag"] = ok["ditandai"].fillna(0).astype(int)
ok["ada_lang"] = ok["lang"].fillna("").astype(str).str.len().gt(0).astype(int)
ok["lang_id"] = ok["lang"].fillna("").astype(str).str.lower().str.startswith("id").astype(int)
ok["ada_judul"] = ok["judul_metadata"].fillna(0).astype(int)
ok["punya_teks"] = (ok["char_per_hal"].fillna(0) >= 100).astype(int)
ok["tanpa_teks"] = 1 - ok["punya_teks"]
print("\n== Seluruh sampel yang berhasil dibuka ==")
for n_, f_ in [("Lulus PDF/UA-1 (veraPDF)", "lulus"), ("Bertag (StructTreeRoot + Marked)", "bertag"), ("Mendeklarasikan bahasa (Lang)", "ada_lang"),
               ("Judul pada metadata", "ada_judul"), ("Tanpa lapisan teks (pindai)", "tanpa_teks")]:
    rep(n_, ok, f_)

t = ok[ok["bertag"] == 1].copy()
print("\n== Dokumen bertag ==", len(t))
print("Total Figure:", int(t["figure"].sum()), "| dengan alt:", int(t["fig_alt"].sum()), "| alt bermakna:", int(t["fig_alt_bermakna"].sum()))
if t["figure"].sum():
    for lab, col in (("alt ada", "fig_alt"), ("alt bermakna", "fig_alt_bermakna")):
        k, n = int(t[col].sum()), int(t["figure"].sum()); lo, hi = wilson(k, n)
        print(f"  Figure {lab}: {k}/{n} = {100*k/n:.1f}% (Wilson {100*lo:.1f}-{100*hi:.1f}; catatan: elemen bersarang dalam dokumen)")
tf = t[t["figure"] > 0].copy()
tf["semua_alt"] = (tf["fig_alt_bermakna"] == tf["figure"]).astype(int)
print("Dokumen bertag dengan >=1 Figure:", len(tf))
if len(tf):
    rep("  dokumen di mana SEMUA Figure beralt bermakna", tf, "semua_alt")
tt = t[t["table"] > 0].copy(); tt["ada_th"] = (tt["table_th"] > 0).astype(int)
print("Dokumen bertag dengan tabel:", len(tt))
if len(tt):
    rep("  dokumen bertabel yang memiliki sel judul (TH)", tt, "ada_th")

print("\n== Bahasa isi (heuristik) ==")
print(ok["bahasa_isi"].value_counts().to_dict())
idn = ok[ok["bahasa_isi"] == "id"].copy()
print("Dokumen berisi bahasa Indonesia:", len(idn))
if len(idn):
    rep("  mendeklarasikan Lang=id", idn, "lang_id")
    print("  Lang lain:", idn["lang"].fillna("(kosong)").replace("", "(kosong)").value_counts().head(6).to_dict())

print("\n== Ukuran dan beban ==")
print("Halaman: median", ok["halaman"].median(), "| total", int(ok["halaman"].sum()))
print("Aturan PDF/UA-1 gagal per dokumen: median", ok["aturan_gagal"].median(), "| IQR", ok["aturan_gagal"].quantile([.25, .75]).tolist())
print("Gambar besar (>=100px, <=60 hlm) per dokumen: median", ok["gambar_besar_60hal"].median(), "| rerata", round(ok["gambar_besar_60hal"].mean(), 1),
      "| dokumen dengan >=1:", int((ok["gambar_besar_60hal"] > 0).sum()))

print("\n== Asal aplikasi (pengelompokan dari Producer/Creator) ==")
def app(s):
    s = str(s).lower()
    if "powerpoint" in s: return "PowerPoint"
    if "word" in s: return "Word"
    if "latex" in s or "pdftex" in s or "xetex" in s or "luatex" in s: return "LaTeX"
    if "libreoffice" in s or "openoffice" in s: return "LibreOffice"
    if "acrobat" in s or "distiller" in s: return "Adobe Acrobat/Distiller"
    if "canva" in s or "google" in s: return "Canva/Google"
    return "lainnya/tak diketahui"
ok["app"] = ok["pembuat"].map(app)
print(ok["app"].value_counts().to_dict())
print(ok.groupby("app")[["lulus", "bertag"]].mean().round(2).to_dict())

print("\n== Aturan PDF/UA-1 yang paling sering gagal ==")
cnt = collections.Counter()
for s in ok["daftar_aturan"].dropna():
    for r in str(s).split(";"):
        if r: cnt[r] += 1
for r, c in cnt.most_common(8):
    print(f"  {r}: {c} dokumen ({100*c/len(ok):.0f}%)")
ok.to_csv("hasil_gabungan.csv", index=False, encoding="utf-8-sig")
