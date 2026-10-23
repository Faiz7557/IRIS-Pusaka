"""Grafik lampiran (statis, cetak) dari lampiran_data.json dan eval/results.json.

  python lampiran/buat_grafik.py   (dari folder Final/Paper; jalankan hitung_lampiran.py dahulu)

Palet tervalidasi (skill dataviz, validate_palette.js --pairs all): D #2a78d6, B2 #eb6834, B1 #1baf7a;
B0 abu netral (konteks, bukan seri). Status: terbit #0ca30c, ditahan #fab219, selalu berlabel teks.
"""
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "gambar"
OUT.mkdir(exist_ok=True)
D = json.load(open(HERE / "lampiran_data.json", encoding="utf-8"))
R = json.load(open(HERE.parents[1] / "Prototype" / "eval" / "results.json", encoding="utf-8"))

C = {"D": "#2a78d6", "B2": "#eb6834", "B1": "#1baf7a", "B0": "#8a8986",
     "terbit": "#0ca30c", "ditahan": "#fab219", "ink": "#0b0b0b", "ink2": "#52514e", "grid": "#e4e3df"}
plt.rcParams.update({
    "font.family": "Times New Roman", "font.size": 9, "axes.titlesize": 9.5, "axes.titleweight": "bold",
    "axes.edgecolor": C["ink2"], "axes.labelcolor": C["ink"], "xtick.color": C["ink2"], "ytick.color": C["ink2"],
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": C["grid"],
    "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False, "savefig.dpi": 300,
    "savefig.bbox": "tight", "figure.facecolor": "white",
})
W = 7.0  # inci, lebar teks lampiran satu kolom


def idn(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def simpan(fig, nama):
    fig.savefig(OUT / nama)
    plt.close(fig)
    print("ok", nama)


JENIS = {"batang": "Batang", "batang_horizontal": "Batang horizontal", "garis": "Garis", "area": "Area", "titik": "Titik"}


def status_per_jenis():
    G = D["grafik"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.3), gridspec_kw={"width_ratios": [3, 2]})
    for ax, keys, label, judul in (
        (a, list(JENIS), lambda k: JENIS[k], "(a) Menurut jenis grafik"),
        (b, [True, False], lambda k: "Berlabel nilai" if k else "Tanpa label nilai", "(b) Menurut keberadaan label nilai"),
    ):
        field = "jenis" if ax is a else "label_nilai"
        cnt = Counter((g[field], g["status"]) for g in G)
        ys = range(len(keys))
        t = [cnt[(k, "terbit_otomatis")] for k in keys]
        h = [cnt[(k, "antrean")] for k in keys]
        ax.barh(ys, t, color=C["terbit"], height=0.6, edgecolor="white", linewidth=1.5, label="Terbit otomatis")
        ax.barh(ys, h, left=t, color=C["ditahan"], height=0.6, edgecolor="white", linewidth=1.5, label="Ditahan (antrean ULD)")
        for y, ti, hi in zip(ys, t, h):
            if ti:
                ax.text(ti / 2, y, str(ti), ha="center", va="center", color="white", fontweight="bold")
            if hi:
                ax.text(ti + hi / 2, y, str(hi), ha="center", va="center", color=C["ink"], fontweight="bold")
        ax.set_yticks(list(ys), [label(k) for k in keys])
        ax.invert_yaxis()
        ax.set_xlabel("Jumlah grafik uji")
        ax.set_title(judul, loc="left")
        ax.grid(axis="y", visible=False)
    a.legend(loc="upper center", bbox_to_anchor=(0.85, -0.32), ncol=2)
    fig.tight_layout()
    simpan(fig, "L_status_grafik.png")


def injeksi():
    J = R["G3"]["injeksi_per_jenis"]
    nama = {"ubah_angka": "Ubah angka", "tukar_label": "Tukar label–nilai", "turunan_salah": "Turunan salah",
            "tren_salah": "Tren salah"}
    rows = [(nama[k], v) for k, v in J.items()] + [("Seluruh injeksi", R["G3"]["injeksi_tertahan"])]
    fig, ax = plt.subplots(figsize=(W, 2.2))
    for y, (lab, v) in enumerate(rows):
        lo, hi = v["ci95"]
        ax.plot([lo, hi], [y, y], color=C["D"], linewidth=2, solid_capstyle="round")
        ax.plot(v["p"], y, "o", color=C["D"], markersize=7, markeredgecolor="white", markeredgewidth=1.5)
        ax.text(1.012, y, f"{v['k']}/{v['n']}  [{idn(lo, 3)}; {idn(hi, 3)}]", va="center", fontsize=8.5, color=C["ink"],
                transform=ax.get_yaxis_transform())
    ax.axvline(0.90, color=C["ink2"], linestyle=(0, (4, 3)), linewidth=1)
    ax.text(0.895, -0.55, "kriteria ≥ 0,90", ha="right", fontsize=8, color=C["ink2"])
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(0.80, 1.006)
    ax.set_xticks([0.80, 0.85, 0.90, 0.95, 1.00])
    ax.set_xlabel("Proporsi deskripsi terinjeksi yang tertahan (titik) dengan selang Wilson 95% (garis)")
    ax.xaxis.set_major_formatter(lambda x, _: idn(x))
    ax.grid(axis="y", visible=False)
    simpan(fig, "L_injeksi.png")


def kalibrasi():
    k1, k2 = D["kalibrasi"]["v1"]["grid"], D["kalibrasi"]["v2"]["grid"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.4))
    for g, lab, col in ((k1, "Versi 1 (sebelum perbaikan)", "#6250d6"), (k2, "Versi 2 (terkunci)", C["D"])):
        x = [r["theta_e"] for r in g]
        a.plot(x, [r["terbit"] for r in g], "-o", color=col, linewidth=2, markersize=4, label=lab)
        b.plot(x, [r["fk_rerata"] for r in g], "-o", color=col, linewidth=2, markersize=4, label=lab)
    a.set_title("(a) Grafik dev yang terbit (dari 30)", loc="left")
    b.set_title("(b) Rerata Fk terhadap acuan pada grafik terbit", loc="left")
    b.axhline(0.98, color=C["ink2"], linestyle=(0, (4, 3)), linewidth=1)
    b.text(0.12, 0.982, "batas 0,98", ha="right", va="bottom", fontsize=8, color=C["ink2"])
    for ax in (a, b):
        ax.axvline(0.01, color=C["ink2"], linewidth=0.8)
        ax.set_xlabel("Ambang selisih ekstraksi θe")
        ax.xaxis.set_major_formatter(lambda x, _: idn(x, 2))
    a.text(0.0115, 21.2, "θe terkunci = 0,01", fontsize=8, color=C["ink2"])
    a.set_ylim(18, 28)
    a.set_yticks([18, 20, 22, 24, 26, 28])
    b.set_ylim(0.92, 1.005)
    b.set_yticks([0.92, 0.94, 0.96, 0.98, 1.00])
    for ax in (a, b):
        ax.set_xticks([0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12])
    b.yaxis.set_major_formatter(lambda x, _: idn(x, 2))
    a.legend(loc="upper center", bbox_to_anchor=(1.1, -0.28), ncol=2)
    fig.tight_layout()
    simpan(fig, "L_kalibrasi.png")


def forest():
    g1, g3, g4, g6 = R["G1"], R["G3"], R["G4"], R["G6_ringan"]
    rows = [  # (label, [(sistem, prop)], kriteria)
        ("G1 lulus, dokumen uji (n = 4)", [("D", g1["D"]), ("B1", g1["B1"]), ("B0", g1["B0"])], 0.90),
        ("G1-ketat, dokumen uji (n = 4)", [("D", g1["D_ketat"])], None),
        ("veraPDF penuh lulus, dokumen uji", [("D", g1["veraPDF_lulus_D"])], None),
        ("G3 klaim terbit setia, Fk", [("D", g3["D_fk_terbit"]), ("B2", g3["B2_fk_perkiraan"])], 0.98),
        ("G3 injeksi tertahan", [("D", g3["injeksi_tertahan"])], 0.90),
        ("G4 jawaban benar dari deskripsi", [("D", g4["D"]), ("B2", g4["B2"])], None),
        ("G3 grafik terbit otomatis", [("D", g3["D_terbit"]), ("B2", g3["B2_terbit"])], None),
        ("G3 beban tinjauan R, set uji", [("D", g3["D_R_beban_tinjauan"])], None),
        ("G6 G1 lulus, PDF nyata (n = 6)", [("D", g6["G1_D"]), ("B1", g6["G1_B1"]), ("B0", g6["G1_B0"])], 0.80),
        ("G6 veraPDF penuh lulus, PDF nyata", [("D", g6["veraPDF_lulus_D"])], None),
        ("G6 beban tinjauan R, PDF nyata", [("D", g6["R_beban_tinjauan"])], None),
    ]
    off = {"D": 0, "B2": 0.26, "B1": 0.26, "B0": 0.52}
    fig, ax = plt.subplots(figsize=(W, 5.4))
    seen = set()
    for y, (lab, items, krit) in enumerate(rows):
        for s, v in items:
            yy = y * 1.25 + off[s]
            ax.plot(v["ci95"], [yy, yy], color=C[s], linewidth=2, solid_capstyle="round")
            ax.plot(v["p"], yy, "o", color=C[s], markersize=6.5, markeredgecolor="white", markeredgewidth=1.3,
                    label=None if s in seen else {"D": "SIMAK (D)", "B2": "B2 VLM langsung", "B1": "B1 auto-tag",
                                                  "B0": "B0 PDF asli"}[s])
            seen.add(s)
        ax.text(1.02, y * 1.25, "  ·  ".join(f"{s} {v['k']}/{v['n']}" for s, v in items), va="center",
                fontsize=7.5, color=C["ink"], transform=ax.get_yaxis_transform())
        if krit:
            ax.plot([krit, krit], [y * 1.25 - 0.3, y * 1.25 + 0.75], color=C["ink"], linewidth=1.2,
                    linestyle=(0, (2, 1.5)))
    ax.set_yticks([y * 1.25 + 0.13 for y in range(len(rows))], [r[0] for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(-0.02, 1.02)
    ax.xaxis.set_major_formatter(lambda x, _: idn(x, 1))
    ax.set_xlabel("Proporsi (titik) dan selang Wilson 95% (garis); garis putus vertikal = kriteria lulus terkunci")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.13), ncol=4)
    simpan(fig, "L_selang_wilson.png")


AUDIT_KAT = {"syn079": "Salah tandai pemeriksa"}
RERATA = {"syn043", "syn083"}  # rerata keliru; syn068 punya satu rerata keliru di antara pembulatan


def audit_b2():
    A = D["audit_b2"]
    ids = sorted({a["id"] for a in A})
    kat = Counter()
    for a in A:
        if a["id"] in AUDIT_KAT:
            kat[(a["id"], "Salah tandai pemeriksa")] += 1
        elif a["id"] in RERATA or (a["id"] == "syn068" and "rata" in a["kutipan"]):
            kat[(a["id"], "Rerata dihitung model keliru")] += 1
        else:
            kat[(a["id"], "Pembulatan/perkiraan di luar ε")] += 1
    assert sum(v for (i, k), v in kat.items() if k == "Pembulatan/perkiraan di luar ε") == 13
    assert sum(v for (i, k), v in kat.items() if k == "Rerata dihitung model keliru") == 3
    # kategori kesalahan, bukan sistem: tidak memakai warna entitas D/B0/B1/B2
    cats = [("Pembulatan/perkiraan di luar ε", "#8a8986"), ("Rerata dihitung model keliru", "#6250d6"),
            ("Salah tandai pemeriksa", "#c3c2b7")]
    fig, ax = plt.subplots(figsize=(W, 2.5))
    left = [0] * len(ids)
    for nm, col in cats:
        vals = [kat[(i, nm)] for i in ids]
        ax.barh(range(len(ids)), vals, left=left, color=col, height=0.6, edgecolor="white", linewidth=1.5, label=nm)
        for y, (l, v) in enumerate(zip(left, vals)):
            if v:
                ax.text(l + v / 2, y, str(v), ha="center", va="center", fontsize=8,
                        color="white" if col == "#6250d6" else C["ink"], fontweight="bold")
        left = [l + v for l, v in zip(left, vals)]
    lab = {g["id"]: g for g in D["grafik"]}
    ax.set_yticks(range(len(ids)), [f"{i} ({'berlabel' if lab[i]['label_nilai'] else 'tanpa label'})" for i in ids])
    ax.invert_yaxis()
    ax.set_xlabel("Jumlah angka B2 yang ditandai tidak setia (total 17)")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.25), ncol=3)
    simpan(fig, "L_audit_b2.png")


def g6_verapdf():
    P = R["G6_ringan"]["per_dokumen"]
    fig, ax = plt.subplots(figsize=(W, 2.4))
    w = 0.26
    for j, s in enumerate(("B0", "B1", "D")):
        xs = [i + (j - 1) * w for i in range(len(P))]
        vals = [p[s]["aturan_gagal"] for p in P]
        ax.bar(xs, vals, width=w - 0.03, color=C[s], label={"B0": "B0 PDF asli", "B1": "B1 auto-tag", "D": "SIMAK (D)"}[s])
        for x, v in zip(xs, vals):
            ax.text(x, v + 0.15, str(v), ha="center", va="bottom", fontsize=7.5, color=C["ink"])
    ax.set_xticks(range(len(P)), [f"{p['file'].replace('.pdf', '')}\n{p['halaman']} hlm" for p in P])
    ax.set_ylabel("Aturan PDF/UA-1 gagal")
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    simpan(fig, "L_g6_verapdf.png")


if __name__ == "__main__":
    status_per_jenis()
    injeksi()
    kalibrasi()
    forest()
    audit_b2()
    g6_verapdf()
