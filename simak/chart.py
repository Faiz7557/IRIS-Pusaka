"""CHT-01/CHT-02: konsistensi ekstraksi ganda, statistik yang dihitung kode,
klaim (e, m, v), dan deskripsi level 1–3 dari templat.

Deskripsi disimpan sebagai segmen; segmen berangka menunjuk ke klaim sehingga
himpunan klaim Λ(d) dibaca langsung dari isian templat, bukan dari pemindaian kalimat.
"""
import re
import unicodedata

import numpy as np


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", str(s)).lower().strip()
    return re.sub(r"[^\w]+", " ", s).strip()


def to_table(ext: dict) -> list[dict]:
    return [{"kategori": str(r["kategori"]).strip(), "nilai": float(r["nilai"])}
            for r in ext.get("data", []) if r.get("kategori") is not None]


def align(t1: list[dict], t2: list[dict]):
    """Pasangkan baris T1 dan T2 menurut nama kategori; jatuh ke urutan bila nama berbeda tipis."""
    m2 = {norm(r["kategori"]): r["nilai"] for r in t2}
    pairs = [(r["kategori"], r["nilai"], m2.get(norm(r["kategori"]))) for r in t1]
    if all(p[2] is not None for p in pairs) and len(t1) == len(t2):
        return pairs
    if len(t1) == len(t2):
        return [(a["kategori"], a["nilai"], b["nilai"]) for a, b in zip(t1, t2)]
    return None


def delta(t1, t2) -> float:
    """Pers. (2): rerata selisih mutlak dinormalisasi terhadap rentang gabungan s."""
    pairs = align(t1, t2)
    if not pairs:
        return 1.0
    vals = [p[1] for p in pairs] + [p[2] for p in pairs]
    s = max(vals) - min(vals)
    if s == 0:
        return 0.0 if all(p[1] == p[2] for p in pairs) else 1.0
    return float(np.mean([abs(p[1] - p[2]) / s for p in pairs]))


def axis_check(table, tik_min, tik_max) -> tuple[bool, str]:
    """cA: nilai T harus berada dalam rentang label tik sumbu yang dibaca terpisah."""
    if tik_max is None or tik_min is None or tik_max <= tik_min:
        return False, "label tik sumbu tidak terbaca"
    span = tik_max - tik_min
    # Sumbu boleh melampaui label tik terluar sekitar satu langkah tik; pemeriksaan ini
    # ditujukan untuk salah baca skala (mis. 10×), bukan selisih kecil.
    lo, hi = tik_min - 0.2 * span, tik_max + 0.2 * span
    out = [r["kategori"] for r in table if not lo <= r["nilai"] <= hi]
    if out:
        return False, f"nilai di luar rentang sumbu [{fmt(tik_min)}, {fmt(tik_max)}]: {', '.join(out)}"
    return True, "nilai berada dalam rentang sumbu"


ORDERED_TYPES = {"garis", "area"}
_MONTHS = "jan|feb|mar|apr|mei|jun|jul|agu|agt|sep|okt|nov|des|januari|februari|maret|april|juni|juli|agustus|september|oktober|november|desember"
_TIME = re.compile(rf"^((19|20)\d{{2}}|q[1-4]|kuartal \d|semester \d|({_MONTHS})( \d{{2,4}})?|(minggu|pekan|bulan|tahun|pertemuan) \d+)$", re.I)


def is_ordered(ext, table) -> bool:
    if ext.get("jenis_grafik") in ORDERED_TYPES:
        return True
    return len(table) >= 3 and all(_TIME.match(r["kategori"].strip()) for r in table)


def decimals(table) -> int:
    d = 0
    for r in table:
        v = r["nilai"]
        for k in range(0, 3):
            if abs(round(v, k) - v) < 1e-9:
                d = max(d, k)
                break
        else:
            d = 2
    return d


def fmt(v, d: int = None) -> str:
    """Format angka Indonesia: koma desimal, titik ribuan."""
    if isinstance(v, str):
        return v
    if d is None:
        d = 0 if abs(v - round(v)) < 1e-9 else (1 if abs(v * 10 - round(v * 10)) < 1e-9 else 2)
    s = f"{v:,.{d}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def derived(table, ordered: bool, rho: float) -> list[dict]:
    """D(T): fakta turunan yang dihitung kode, termasuk pers. (3)–(4)."""
    vals = np.array([r["nilai"] for r in table])
    cats = [r["kategori"] for r in table]
    imax, imin = int(vals.argmax()), int(vals.argmin())
    facts = [
        {"e": cats[imax], "m": "maksimum", "v": float(vals[imax])},
        {"e": cats[imin], "m": "minimum", "v": float(vals[imin])},
        {"e": f"{cats[imax]}|{cats[imin]}", "m": "selisih", "v": float(vals[imax] - vals[imin])},
        {"e": "*", "m": "rerata", "v": float(vals.mean())},
        {"e": "*", "m": "total", "v": float(vals.sum())},
    ]
    if ordered and len(vals) >= 3:
        x = np.arange(len(vals), dtype=float)
        beta = float(((x - x.mean()) * (vals - vals.mean())).sum() / ((x - x.mean()) ** 2).sum())
        dhat = beta * (x[-1] - x[0])
        rng = vals.max() - vals.min()
        label = "naik" if dhat >= rho * rng else "turun" if dhat <= -rho * rng else "tidak jelas"
        facts += [
            {"e": f"{cats[0]}|{cats[-1]}", "m": "perubahan_terfit", "v": float(dhat)},
            {"e": f"{cats[0]}|{cats[-1]}", "m": "perubahan", "v": float(vals[-1] - vals[0])},
            {"e": "*", "m": "tren", "v": label},
        ]
    return facts


JENIS_TEKS = {"batang": "batang", "batang_horizontal": "batang horizontal", "garis": "garis",
              "area": "area", "pai": "lingkaran", "lainnya": ""}


def build_description(ext: dict, table: list[dict], rho: float):
    """Mengisi templat level 1–3; mengembalikan (segmen, klaim)."""
    ordered = is_ordered(ext, table)
    D = derived(table, ordered, rho)
    dd = {f["m"]: f for f in D}
    d = decimals(table)
    sat = (" " + ext["satuan"].strip()) if ext.get("satuan", "").strip() else ""
    claims, seg = [], []

    def t(text):
        seg.append({"text": text})

    def c(e, m, v, show=None):
        claims.append({"e": e, "m": m, "v": v})
        seg.append({"text": show if show is not None else fmt(v, d if m != "rerata" else max(d, 1)),
                    "claim": len(claims) - 1})

    # Level 1: sifat elemental
    jenis = JENIS_TEKS.get(ext.get("jenis_grafik"), "")
    t(f"Grafik {jenis} " if jenis else "Grafik ")
    if ext.get("judul"):
        t(f"berjudul “{ext['judul'].strip()}”, ")
    lx, ly = ext.get("label_x"), ext.get("label_y")
    if ext.get("jenis_grafik") == "batang_horizontal":  # sumbu mendatar adalah sumbu nilai
        lx, ly = ly, lx
    if sat and ly and ly.strip().endswith(f"({sat.strip()})"):  # hindari satuan tertulis dua kali
        ly = ly.strip()[: -len(sat.strip()) - 2].strip()
    t(f"dengan sumbu kategori {lx or 'tanpa label'} dan sumbu nilai "
      f"{ly or 'tanpa label'}{f' ({sat.strip()})' if sat else ''}. ")
    t(f"Grafik memuat {len(table)} kategori, dari {table[0]['kategori']} sampai {table[-1]['kategori']}. ")
    # Level 2: konsep statistik
    t(f"Nilai tertinggi pada {dd['maksimum']['e']}, yaitu ")
    c(dd["maksimum"]["e"], "maksimum", dd["maksimum"]["v"]); t(f"{sat}; terendah pada {dd['minimum']['e']}, yaitu ")
    c(dd["minimum"]["e"], "minimum", dd["minimum"]["v"]); t(f"{sat}. Selisih keduanya ")
    c(dd["selisih"]["e"], "selisih", dd["selisih"]["v"]); t(f"{sat}, dan rerata seluruh kategori ")
    c("*", "rerata", dd["rerata"]["v"]); t(f"{sat}. ")
    # Level 3: fenomena perseptual
    if ordered and "tren" in dd:
        t("Secara keseluruhan tren ")
        c("*", "tren", dd["tren"]["v"], show=dd["tren"]["v"])
        t(f": garis regresi berubah sekitar ")
        c(dd["perubahan_terfit"]["e"], "perubahan_terfit", dd["perubahan_terfit"]["v"])
        t(f"{sat} dari {table[0]['kategori']} ke {table[-1]['kategori']}. ")
    else:
        urut = sorted(table, key=lambda r: -r["nilai"])
        t("Urutan dari tertinggi: " + ", ".join(r["kategori"] for r in urut) + ". ")
    # Rincian nilai (level 2) agar nilai tertentu dapat diambil, sesuai kebutuhan pengguna [12]
    t("Rincian nilai: ")
    for i, r in enumerate(table):
        t(f"{r['kategori']} ")
        c(r["kategori"], "nilai", r["nilai"])
        t(sat + ("; " if i < len(table) - 1 else "."))
    return seg, claims, D


def render(seg) -> str:
    return "".join(s["text"] for s in seg).replace("  ", " ").strip()
