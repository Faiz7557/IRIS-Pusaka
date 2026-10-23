"""Gambar 5–7 untuk badan Bab IV (statis, cetak 300 dpi, Times New Roman).

  python gambar/buat_gambar_bab4.py   (dari folder Final/Paper; butuh lampiran/lampiran_data.json)

Gambar 5: alur gerbang pada satu grafik uji nyata (syn043) — SIMAK, B2, dan injeksi tukar label.
Gambar 6: status 60 grafik uji, D vs B2.
Gambar 7: proporsi dan selang Wilson per gerbang terhadap kriteria terkunci.
Semua angka dibaca dari results.json / lampiran_data.json / cache (lewat hitung_lampiran.py), bukan diketik.
Warna: palet tervalidasi skill dataviz (D #2a78d6, B2 #eb6834, B1 #1baf7a, B0 abu); status terbit #0ca30c,
ditahan #fab219, keliru #d03b3b — status selalu disertai label teks.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PROTO = PAPER.parent / "Prototype"
R = json.load(open(PROTO / "eval/results.json", encoding="utf-8"))
L = json.load(open(PAPER / "lampiran/lampiran_data.json", encoding="utf-8"))

C = {"D": "#2a78d6", "B2": "#eb6834", "B1": "#1baf7a", "B0": "#8a8986", "ok": "#0ca30c", "hold": "#fab219",
     "bad": "#d03b3b", "ink": "#0b0b0b", "ink2": "#52514e", "grid": "#e4e3df", "pale": "#f4f3f0"}
plt.rcParams.update({
    "font.family": "Times New Roman", "font.size": 8.5, "axes.edgecolor": C["ink2"], "xtick.color": C["ink2"],
    "ytick.color": C["ink2"], "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "savefig.dpi": 300, "savefig.bbox": "tight", "figure.facecolor": "white",
})


def idn(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def kotak(ax, x, y, w, h, judul, isi, warna, tebal=1.4, isi_warna=None, nomor=None):
    """Kotak langkah; nomor digambar dalam lingkaran (Times New Roman tidak punya glyph ①–④)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.012",
                                fc=isi_warna or "white", ec=warna, lw=tebal))
    tx = x + 0.008
    if nomor:
        ax.add_patch(Ellipse((x + 0.02, y + h - 0.045), 0.026, 0.026 * 7.0 / 3.75, color=warna))
        ax.text(x + 0.02, y + h - 0.045, str(nomor), fontsize=7.2, fontweight="bold", color="white",
                ha="center", va="center")
        tx = x + 0.04
    ax.text(tx, y + h - 0.03, judul, fontsize=8, fontweight="bold", color=C["ink"], va="top")
    ax.text(x + 0.008, y + h - 0.095, isi, fontsize=7.4, color=C["ink"], va="top", linespacing=1.32)


def panah(ax, a, b, warna=None, gaya="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=gaya, mutation_scale=9, lw=1.1, color=warna or C["ink2"],
                                 shrinkA=1, shrinkB=1))


def lencana(ax, x, y, teks, warna, w=0.1, fg="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, 0.075, boxstyle="round,pad=0.003,rounding_size=0.02", fc=warna, ec=warna))
    ax.text(x + w / 2, y + 0.0375, teks, fontsize=7.8, fontweight="bold", color=fg, ha="center", va="center")


# ---------------------------------------------------------------- Gambar 5
def gambar5():
    c = next(x for x in L["charts_json"] if x["id"] == "syn043")
    g = next(x for x in L["grafik"] if x["id"] == "syn043")
    inj = next(i for i in L["injeksi"] if i["id"] == "syn043" and i["jenis"] == "tukar_label")
    a = next(x for x in L["audit_b2"] if x["id"] == "syn043")
    nil = dict(zip(c["kategori"], c["nilai"]))
    mx, mn = max(nil, key=nil.get), min(nil, key=nil.get)
    rerata = sum(c["nilai"]) / len(c["nilai"])
    th = R["ambang"]

    fig = plt.figure(figsize=(7.0, 3.75))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # grafik masukan
    img = plt.imread(PROTO / "data/synth/charts/syn043.png")
    fh = 0.165 * 7.0 * img.shape[0] / img.shape[1] / 3.75   # tinggi sumbu (fraksi) mengikuti rasio citra
    y0 = 0.55 - fh / 2
    ia = fig.add_axes([0.005, y0, 0.165, fh]); ia.imshow(img); ia.axis("off")
    ax.text(0.088, y0 + fh + 0.025, "Masukan: grafik syn043", ha="center", fontsize=8, fontweight="bold")
    judul = c["judul"].replace(" per ", "\nper ", 1)  # dua baris agar tidak menabrak lajur injeksi
    ax.text(0.088, y0 - 0.015, f"{judul}\n{len(c['kategori'])} kategori, berlabel nilai", ha="center",
            fontsize=6.8, color=C["ink2"], va="top")

    # lajur SIMAK
    ax.text(0.185, 0.965, "SIMAK (D): verifikasi sebelum terbit", fontsize=8.5, fontweight="bold", color=C["D"])
    y, h = 0.60, 0.33
    kotak(ax, 0.185, y, 0.165, h, "Ekstraksi ganda",
          "T1 dan T2: dua perintah,\nGemma 4 26B-A4B\n"
          f"δ = {idn(g['delta'], 3)} ≤ θe = {idn(th['theta_e'], 2)}\nrentang sumbu sesuai\nnilai tercetak di grafik", C["D"],
          nomor=1)
    kotak(ax, 0.365, y, 0.165, h, "Statistik oleh kode",
          f"maks: {mx} {idn(nil[mx])}\nmin: {mn} {idn(nil[mn])}\nselisih: {idn(nil[mx] - nil[mn])}\n"
          f"rerata: {idn(rerata, 1)}\ntren: naik", C["D"], nomor=2)
    kotak(ax, 0.545, y, 0.165, h, "Deskripsi templat",
          f"level 1–3 dari tabel T\n{g['n_klaim']} klaim terstruktur\n(nilai, maks, min, selisih,\nrerata, tren)", C["D"],
          nomor=3)
    kotak(ax, 0.725, y, 0.145, h, "Gerbang K(e)",
          f"cF: {g['klaim_setia']}/{g['n_klaim']} klaim\ncocok dengan T\ncδ, cA, cL: lulus\n→ semua lulus", C["D"], nomor=4)
    for x0, x1 in ((0.35, 0.365), (0.53, 0.545), (0.71, 0.725)):
        panah(ax, (x0, y + h / 2), (x1, y + h / 2), C["D"])
    panah(ax, (0.87, y + h / 2), (0.885, y + h / 2), C["D"])
    lencana(ax, 0.885, y + h / 2 - 0.0375, "TERBIT", C["ok"])
    ax.text(0.935, y + h / 2 - 0.06, f"klaim setia\nvs acuan {g['klaim_setia']}/{g['n_klaim']}", fontsize=6.8,
            ha="center", va="top", color=C["ink2"])

    # lajur injeksi
    yi, hi = 0.335, 0.2
    ax.text(0.185, yi + hi + 0.02, "Uji injeksi: kesalahan disuntik ke deskripsi SIMAK", fontsize=8.5,
            fontweight="bold", color=C["ink2"])
    kotak(ax, 0.185, yi, 0.525, hi, "Tukar label–nilai (Apr ↔ Okt), dicek ulang oleh gerbang",
          "\n".join(f"× {r}" for r in inj["alasan"][:2]), C["hold"], isi_warna="#fffaf0")
    panah(ax, (0.6275, y), (0.6275, yi + hi), C["ink2"])
    panah(ax, (0.71, yi + hi / 2), (0.885, yi + hi / 2), C["hold"])
    lencana(ax, 0.885, yi + hi / 2 - 0.0375, "DITAHAN", C["hold"], fg=C["ink"])
    ax.text(0.935, yi + hi / 2 - 0.06, "antrean tinjauan\nULD", fontsize=6.8, ha="center", va="top", color=C["ink2"])

    # lajur B2
    yb, hb = 0.04, 0.215
    ax.text(0.185, yb + hb + 0.025, "B2: VLM langsung menulis deskripsi, tanpa gerbang", fontsize=8.5,
            fontweight="bold", color=C["B2"])
    kotak(ax, 0.185, yb, 0.525, hb, "Teks bebas dari model yang sama",
          f"{g['b2_angka']} angka diperiksa terhadap acuan; {g['b2_angka'] - g['b2_keliru']} setia, "
          f"{g['b2_keliru']} tidak setia:\n“…Rata-rata kunjungan bulanan adalah sekitar 1.107 kali…”\n"
          f"acuan: rerata {idn(rerata, 1)} (selisih {idn(rerata - 1107, 1)}; rerata dihitung model)", C["B2"],
          isi_warna="#fff6f1")
    panah(ax, (0.71, yb + hb / 2), (0.885, yb + hb / 2), C["B2"])
    lencana(ax, 0.885, yb + hb / 2 - 0.0375, "TERBIT", C["bad"])
    ax.text(0.935, yb + hb / 2 - 0.06, "1 angka keliru\nsampai ke pembaca", fontsize=6.8, ha="center", va="top",
            color=C["bad"])
    assert a["verdict"] == "dikarang" and "1.107" in a["kutipan"]
    fig.savefig(HERE / "Gambar5_alur_gerbang_syn043.png")
    plt.close(fig)
    print("ok Gambar5")


# ---------------------------------------------------------------- Gambar 6
def gambar6():
    G, g3 = L["grafik"], R["G3"]
    b2_bad = sum(1 for x in G if x["b2_keliru"] > 0)
    d_ok = sum(1 for x in G if x["status"] == "terbit_otomatis")
    assert b2_bad == g3["B2_grafik_dengan_angka_keliru"]["k"] and d_ok == g3["D_terbit"]["k"]
    rows = [
        ("B2  VLM langsung", [(60 - b2_bad, C["B2"], "terbit tanpa pemeriksaan,\ntidak ada angka ditandai", "white"),
                               (b2_bad, C["bad"], f"terbit dengan angka keliru\n({g3['B2_angka_keliru_terbit']} angka)", "white")]),
        ("D  SIMAK", [(d_ok, C["ok"], f"terbit terverifikasi\n({g3['D_fk_terbit']['k']}/{g3['D_fk_terbit']['n']} klaim setia)", "white"),
                      (60 - d_ok, C["hold"], "ditahan ke antrean ULD\n(tanpa label nilai, cL)", C["ink"])]),
    ]
    fig, ax = plt.subplots(figsize=(7.0, 2.3))
    for yy, (lab, segs) in enumerate(rows):
        left = 0
        for v, col, teks, fg in segs:
            ax.barh(yy, v, left=left, color=col, height=0.62, edgecolor="white", linewidth=2)
            ax.text(left + v / 2, yy, f"{v}", ha="center", va="center", color=fg, fontsize=10, fontweight="bold")
            sempit = v < 12  # label segmen sempit rata kanan agar tidak keluar sumbu
            ax.text(left + v if sempit else left + v / 2, yy + 0.36, teks, ha="right" if sempit else "center",
                    va="top", color=C["ink"], fontsize=7.2, linespacing=1.15)
            left += v
    ax.text(61, 0, f"angka keliru terbit: {g3['B2_angka_keliru_terbit']}\nbeban tinjauan: 0/60",
            va="center", fontsize=7.6, color=C["ink"])
    ax.text(61, 1, f"angka keliru terbit: {g3['D_angka_keliru_terbit']}\nbeban tinjauan R: "
                   f"{g3['D_R_beban_tinjauan']['k']}/60", va="center", fontsize=7.6, color=C["ink"])
    ax.set_yticks([0, 1], [r[0] for r in rows], fontsize=8.5, fontweight="bold")
    ax.set_xlim(0, 60); ax.set_ylim(1.75, -0.45)
    ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
    ax.set_xlabel("Jumlah grafik pada set uji tertahan (n = 60)")
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=C["grid"], lw=0.6); ax.set_axisbelow(True)
    fig.savefig(HERE / "Gambar6_status_D_vs_B2.png")
    plt.close(fig)
    print("ok Gambar6")


# ---------------------------------------------------------------- Gambar 7
def gambar7():
    g1, g3, g4, g6 = R["G1"], R["G3"], R["G4"], R["G6_ringan"]
    rows = [
        ("G1 struktur dan metadata\n4 dokumen uji", [("D", g1["D"]), ("B1", g1["B1"]), ("B0", g1["B0"])], 0.90, "≥ 0,90"),
        ("G1-ketat (tambahan)\npenanda tahan belum bermakna", [("D", g1["D_ketat"])], None, "— (tambahan)"),
        ("G3 kesetiaan klaim terbit (Fk)\nterhadap tabel acuan", [("D", g3["D_fk_terbit"]), ("B2", g3["B2_fk_perkiraan"])], 0.98, "≥ 0,98"),
        ("G3 deskripsi terinjeksi\nyang tertahan", [("D", g3["injeksi_tertahan"])], 0.90, "≥ 0,90"),
        ("G4 jawaban benar dari\ndeskripsi (80 pertanyaan)", [("D", g4["D"]), ("B2", g4["B2"])], None, "Q ≥ 0,80"),
        ("G6 ringan: G1 pada\n6 PDF nyata", [("D", g6["G1_D"]), ("B1", g6["G1_B1"]), ("B0", g6["G1_B0"])], 0.80, "≥ 0,80"),
    ]
    off = {"D": 0.0, "B2": 0.24, "B1": 0.24, "B0": 0.48}
    nama = {"D": "SIMAK (D)", "B2": "B2 VLM langsung", "B1": "B1 auto-tag", "B0": "B0 PDF asli"}
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    seen = set()
    for i, (lab, items, krit, kt) in enumerate(rows):
        y0 = i * 1.15
        ax.axhspan(y0 - 0.32, y0 + 0.8, color=C["pale"] if i % 2 == 0 else "white", zorder=0, lw=0)
        for s, v in items:
            yy = y0 + off[s]
            ax.plot(v["ci95"], [yy, yy], color=C[s], lw=2.2, solid_capstyle="round", zorder=2)
            ax.plot(v["p"], yy, "o", color=C[s], ms=6.5, mec="white", mew=1.3, zorder=3,
                    label=None if s in seen else nama[s])
            seen.add(s)
        if krit:
            ax.plot([krit, krit], [y0 - 0.28, y0 + 0.76], color=C["ink"], lw=1.1, ls=(0, (2, 1.5)), zorder=1)
        ax.text(1.03, y0 + 0.2, "  ·  ".join(f"{s} {v['k']}/{v['n']}" for s, v in items), fontsize=7.2,
                va="center", transform=ax.get_yaxis_transform(), color=C["ink"])
        ax.text(1.03, y0 + 0.55, f"kriteria {kt}", fontsize=6.8, va="center", color=C["ink2"],
                transform=ax.get_yaxis_transform())
    ax.set_yticks([i * 1.15 + 0.2 for i in range(len(rows))], [r[0] for r in rows], fontsize=7.6)
    ax.invert_yaxis()
    ax.set_xlim(-0.02, 1.02)
    ax.xaxis.set_major_formatter(lambda x, _: idn(x, 1))
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Proporsi (titik) dan selang Wilson 95% (garis); garis putus = kriteria lulus terkunci")
    ax.legend(loc="upper center", bbox_to_anchor=(0.42, -0.17), ncol=4, fontsize=7.6)
    fig.savefig(HERE / "Gambar7_gerbang_vs_kriteria.png")
    plt.close(fig)
    print("ok Gambar7")


if __name__ == "__main__":
    gambar5()
    gambar6()
    gambar7()
