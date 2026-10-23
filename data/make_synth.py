"""Set sintetis penulis (Tabel 5 / G.1 no. 4): grafik berbahasa Indonesia dengan
tabel acuan pasti, dan dokumen materi kuliah PDF tanpa tag yang memuat grafik,
tabel, rumus, gambar dekoratif, dan diagram.

Pembagian pengembangan : uji = 1 : 2 dengan seed tetap 20260930 (Lampiran G.2).
"""
import json
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "synth"
SEED = 20260930

TOPIK = [
    ("Mahasiswa baru per fakultas", "Fakultas", "Jumlah mahasiswa", "orang",
     ["Kedokteran", "Hukum", "Ekonomi", "Teknik", "Psikologi", "Farmasi", "Sains", "Vokasi"], (80, 900), 0),
    ("Persentase penduduk miskin per provinsi", "Provinsi", "Persentase", "%",
     ["Aceh", "Sumut", "Jabar", "Jateng", "Jatim", "Bali", "NTT", "Papua", "Maluku"], (3, 30), 1),
    ("Rata-rata IPK lulusan per program studi", "Program studi", "IPK", "",
     ["Akuntansi", "Manajemen", "Statistika", "Biologi", "Kimia", "Fisika"], (2.8, 3.9), 2),
    ("Kunjungan perpustakaan per bulan", "Bulan", "Kunjungan", "kali",
     ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"], (300, 2500), 0),
    ("Mahasiswa disabilitas terdaftar per tahun", "Tahun", "Jumlah", "orang",
     ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"], (40, 400), 0),
    ("Anggaran riset per unit", "Unit", "Anggaran", "juta rupiah",
     ["LPPM", "FK", "FT", "FEB", "FST", "FISIP", "FIB"], (120, 1800), 0),
    ("Tingkat kelulusan tepat waktu per angkatan", "Angkatan", "Persentase", "%",
     ["2015", "2016", "2017", "2018", "2019", "2020", "2021"], (35, 92), 1),
    ("Curah hujan bulanan Surabaya", "Bulan", "Curah hujan", "mm",
     ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep"], (10, 380), 0),
    ("Skor rata-rata ujian per kelas", "Kelas", "Skor", "",
     ["Kelas A", "Kelas B", "Kelas C", "Kelas D", "Kelas E"], (55, 95), 1),
    ("Ekspor komoditas Jawa Timur", "Komoditas", "Nilai ekspor", "juta USD",
     ["Perhiasan", "Tembaga", "Kayu olahan", "Udang", "Kertas", "Rokok"], (90, 1400), 0),
]
TYPES = ["batang", "batang_horizontal", "garis", "area", "titik"]
ORDERED_TOPIC = {3, 4, 6, 7}


def make_series(rng, lo, hi, n, dec, ordered):
    if ordered:
        start = rng.uniform(lo, lo + (hi - lo) * 0.4)
        slope = rng.choice([1, -1, 0.15]) * (hi - lo) / n * rng.uniform(0.4, 0.9)
        base = start + slope * np.arange(n) if slope > 0 else hi - (start - lo) + slope * np.arange(n)
        v = base + rng.normal(0, (hi - lo) * 0.06, n)
    else:
        v = np.array([rng.uniform(lo, hi) for _ in range(n)])
    v = np.clip(v, lo * 0.9, hi)
    return [round(float(x), dec) for x in v]


def fmt_id(v, dec):
    s = f"{v:,.{dec}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def draw(spec, path, dpi=110):
    cats, vals, kind = spec["kategori"], spec["nilai"], spec["jenis_grafik"]
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=dpi)
    color = spec["warna"]
    x = np.arange(len(cats))
    if kind == "batang":
        bars = ax.bar(x, vals, color=color)
    elif kind == "batang_horizontal":
        bars = ax.barh(x, vals, color=color)
    elif kind == "garis":
        ax.plot(x, vals, marker="o", color=color, lw=2)
    elif kind == "area":
        ax.fill_between(x, vals, alpha=0.45, color=color)
        ax.plot(x, vals, color=color, lw=2)
    else:  # titik (dot plot)
        ax.scatter(x, vals, s=70, color=color, zorder=3)
        ax.vlines(x, 0, vals, color=color, lw=1, alpha=0.5)
    if kind == "batang_horizontal":
        ax.set_yticks(x, cats); ax.set_xlabel(spec["label_y_full"]); ax.set_ylabel(spec["label_x"])
        ax.invert_yaxis()
    else:
        ax.set_xticks(x, cats, rotation=30 if len(cats) > 7 else 0, ha="right" if len(cats) > 7 else "center")
        ax.set_xlabel(spec["label_x"]); ax.set_ylabel(spec["label_y_full"])
    if spec["label_nilai"]:
        for i, v in enumerate(vals):
            t = fmt_id(v, spec["desimal"])
            if kind == "batang_horizontal":
                ax.text(v, i, " " + t, va="center", fontsize=8)
            else:
                ax.text(i, v, t, ha="center", va="bottom", fontsize=8)
    if kind in ("area", "titik", "batang", "batang_horizontal"):
        (ax.set_xlim if kind == "batang_horizontal" else ax.set_ylim)(0, max(vals) * 1.15)
    ax.set_title(spec["judul"], fontsize=11)
    ax.grid(axis="x" if kind == "batang_horizontal" else "y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def gen_charts(n_total=90):
    rng = np.random.default_rng(SEED)
    prng = random.Random(SEED)
    charts = []
    palette = ["#2b6cb0", "#2f855a", "#c05621", "#6b46c1", "#b7791f", "#2c7a7b"]
    for i in range(n_total):
        ti = i % len(TOPIK)
        judul, lx, ly, sat, cats_all, (lo, hi), dec = TOPIK[ti]
        ordered = ti in ORDERED_TOPIC
        kinds = ["garis", "area", "batang"] if ordered else ["batang", "batang_horizontal", "titik"]
        kind = kinds[(i // len(TOPIK)) % len(kinds)]
        n = prng.randint(4, len(cats_all)) if not ordered else prng.randint(5, len(cats_all))
        cats = cats_all[:n] if ordered else prng.sample(cats_all, n)
        vals = make_series(rng, lo, hi, n, dec, ordered)
        if len(set(vals)) < len(vals):
            vals = [round(v + k * 10 ** -dec, dec) for k, v in enumerate(vals)]
        spec = {
            "id": f"syn{i:03d}", "judul": f"{judul} ({2020 + i % 6})", "label_x": lx,
            "label_y": ly, "satuan": sat, "label_y_full": f"{ly} ({sat})" if sat else ly,
            "kategori": cats, "nilai": vals, "desimal": dec, "jenis_grafik": kind,
            "label_nilai": bool(i % 3 != 2),  # sepertiga tanpa label nilai: lebih sulit
            "warna": palette[i % len(palette)],
        }
        charts.append(spec)
    idx = list(range(n_total)); prng.shuffle(idx)
    n_dev = n_total // 3
    for k, j in enumerate(idx):
        charts[j]["set"] = "dev" if k < n_dev else "uji"
    (OUT / "charts").mkdir(parents=True, exist_ok=True)
    for c in charts:
        draw(c, OUT / "charts" / f"{c['id']}.png")
    (OUT / "charts.json").write_text(json.dumps(charts, ensure_ascii=False, indent=1), encoding="utf-8")
    return charts


# ------------------------------------------------------------------ dokumen PDF
PARAGRAF = [
    "Statistika deskriptif membantu kita meringkas data sebelum melakukan inferensi. Pada pertemuan ini kita membahas ukuran pemusatan, ukuran penyebaran, dan cara membaca grafik dengan benar.",
    "Grafik batang cocok untuk membandingkan kategori, sedangkan grafik garis cocok untuk memperlihatkan perubahan menurut waktu. Perhatikan selalu satuan dan skala pada sumbu nilai.",
    "Data berikut berasal dari contoh ilustratif dan tidak mewakili statistik resmi. Mahasiswa diminta mengidentifikasi nilai tertinggi, nilai terendah, serta pola umum pada setiap grafik.",
    "Regresi linear sederhana memodelkan hubungan antara variabel bebas x dan variabel terikat y. Koefisien kemiringan menunjukkan besarnya perubahan y untuk setiap kenaikan satu satuan x.",
    "Tabel berikut merangkum hasil kuis mingguan. Gunakan tabel ini untuk berlatih menghitung rerata dan simpangan baku secara manual sebelum memakai perangkat lunak.",
]
RUMUS = [r"$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$",
         r"$s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2$",
         r"$\hat{\beta} = \frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^2}$"]


def render_formula(tex, path):
    fig = plt.figure(figsize=(4, 0.8), dpi=150)
    fig.text(0.5, 0.5, tex, fontsize=18, ha="center", va="center")
    fig.savefig(path, transparent=False, facecolor="white"); plt.close(fig)


def render_logo(path):
    fig, ax = plt.subplots(figsize=(1, 1), dpi=80)
    ax.add_patch(plt.Circle((0.5, 0.5), 0.45, color="#1a365d")); ax.text(0.5, 0.5, "U", color="white",
                                                                         ha="center", va="center", fontsize=28)
    ax.set_axis_off(); ax.set_aspect("equal"); fig.savefig(path, transparent=True); plt.close(fig)


def render_diagram(path):
    fig, ax = plt.subplots(figsize=(5, 2), dpi=110)
    for i, t in enumerate(["Populasi", "Sampel", "Statistik", "Inferensi"]):
        ax.add_patch(plt.Rectangle((i * 1.3, 0.3), 1, 0.6, fc="#edf2f7", ec="#2d3748"))
        ax.text(i * 1.3 + 0.5, 0.6, t, ha="center", va="center", fontsize=10)
        if i < 3:
            ax.annotate("", (i * 1.3 + 1.28, 0.6), (i * 1.3 + 1.02, 0.6), arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(-0.1, 5.1); ax.set_ylim(0, 1.2); ax.set_axis_off()
    fig.savefig(path); plt.close(fig)


def gen_docs(charts, n_docs=6):
    import fitz
    prng = random.Random(SEED + 1)
    d = OUT / "docs"; a = d / "assets"; a.mkdir(parents=True, exist_ok=True)
    render_logo(a / "logo.png"); render_diagram(a / "diagram.png")
    for k, tex in enumerate(RUMUS):
        render_formula(tex, a / f"rumus{k}.png")
    meta = []
    for j in range(n_docs):
        split = "dev" if j < n_docs // 3 else "uji"
        pool = [c for c in charts if c["set"] == split]
        picks = prng.sample(pool, 3)
        rows = [(f"Mahasiswa {chr(65 + r)}", prng.randint(55, 98), prng.randint(50, 99)) for r in range(5)]
        tbl = "".join(f"<tr><td>{n}</td><td>{x}</td><td>{y}</td></tr>" for n, x, y in rows)
        html = f"""
<h1>Pertemuan {j + 3}: Statistika Deskriptif dan Visualisasi Data</h1>
<p><img src="logo.png" width="28"/> Mata kuliah Statistika Dasar, semester gasal</p>
<h2>1. Pendahuluan</h2><p>{PARAGRAF[0]}</p>
<p>{PARAGRAF[4]}</p>
<table border="1" cellspacing="0" cellpadding="4"><tr><td>Nama</td><td>Kuis 1</td><td>Kuis 2</td></tr>{tbl}</table>
<p>{PARAGRAF[1]}</p>
<p><img src="{picks[0]['id']}.png" width="380"/></p>
<p>Gambar 1. {picks[0]['judul']}</p>
<h2>2. Membaca grafik</h2><p>{PARAGRAF[2]}</p>
<p><img src="{picks[1]['id']}.png" width="380"/></p><p>Gambar 2. {picks[1]['judul']}</p>
<p><img src="diagram.png" width="380"/></p><p>Gambar 3. Alur dari populasi ke inferensi</p>
<h2>3. Ukuran pemusatan</h2><p>Rerata sampel didefinisikan sebagai berikut.</p>
<p><img src="rumus{j % 3}.png" width="240"/></p>
<p>{PARAGRAF[3]}</p>
<h2>4. Latihan</h2><p>Perhatikan grafik berikut dan tentukan kategori dengan nilai tertinggi.</p>
<p><img src="{picks[2]['id']}.png" width="380"/></p><p>Gambar 4. {picks[2]['judul']}</p>
<p><img src="logo.png" width="28"/> Akhir materi</p>
"""
        for c in picks:
            (a / f"{c['id']}.png").write_bytes((OUT / "charts" / f"{c['id']}.png").read_bytes())
        css = "body{font-family:sans-serif;font-size:11pt} h1{font-size:17pt} h2{font-size:13pt} table{border-collapse:collapse} td{padding:3px 8px;border:1px solid #333}"
        story = fitz.Story(html=html, user_css=css, archive=fitz.Archive(str(a)))
        path = d / f"materi_{j + 1:02d}.pdf"
        wr = fitz.DocumentWriter(str(path))
        more = True
        while more:
            dev = wr.begin_page(fitz.paper_rect("a4"))
            more, _ = story.place(fitz.paper_rect("a4") + (56, 56, -56, -56))
            story.draw(dev); wr.end_page()
        wr.close()
        meta.append({"file": path.name, "set": split, "charts": [c["id"] for c in picks],
                     "rumus": RUMUS[j % 3]})
    (OUT / "docs.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    ch = gen_charts(n)
    gen_docs(ch)
    print(f"{len(ch)} grafik ({sum(c['set'] == 'dev' for c in ch)} dev), dokumen di {OUT / 'docs'}")
