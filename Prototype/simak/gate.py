"""GAT-01: gerbang verifikasi fail-closed.

pub(e) = 1[K(e) ≠ ∅] · Π_k c_k(e)   (pers. 7)

Untuk grafik K = {cF, cδ, cA, cL}; cL ditambahkan dari analisis kesalahan set
pengembangan: bila nilai tidak tercetak, angka hanya perkiraan skala yang dapat
keliru serupa pada kedua ekstraksi (δ = 0), sehingga tidak dapat diverifikasi. Untuk rumus, foto, dan diagram nondata K = ∅
sehingga selalu ditahan untuk ULD.
"""
import random
import re

from .chart import fmt, norm


def _value_range(table) -> float:
    vals = [r["nilai"] for r in table]
    return (max(vals) - min(vals)) if vals else 0.0


def facts_of(table, D) -> list[dict]:
    return [{"e": r["kategori"], "m": "nilai", "v": r["nilai"]} for r in table] + list(D)


def claim_ok(cl, facts, tol) -> tuple[bool, dict | None]:
    """Klaim setia bila ada fakta dengan entitas dan ukuran sama dan |v−v′| ≤ ε·s."""
    for f in facts:
        if f["m"] != cl["m"] or norm(f["e"]) != norm(cl["e"]):
            continue
        if isinstance(cl["v"], str) or isinstance(f["v"], str):
            return (str(cl["v"]) == str(f["v"])), f
        return (abs(cl["v"] - f["v"]) <= tol), f
    return False, None


def fk(claims, table, D, eps) -> tuple[float, list[dict]]:
    """Pers. (5): proporsi klaim setia beserta rincian per klaim."""
    s = _value_range(table)
    tol = eps * s if s > 0 else 1e-9
    facts = facts_of(table, D)
    detail = []
    for cl in claims:
        ok, f = claim_ok(cl, facts, tol)
        detail.append({**cl, "ok": ok, "ref": None if f is None else f["v"]})
    return (sum(d["ok"] for d in detail) / len(detail) if detail else 0.0), detail


def evaluate(el: dict, th: dict) -> dict:
    """Menjalankan K(e) dan memutuskan terbit atau tahan, dengan alasan yang dapat dibaca."""
    checks, reasons = {}, []
    if el["jenis"] == "grafik" and el.get("table"):
        f, detail = fk(el["claims"], el["table"], el["D"], th["epsilon"])
        el["claim_detail"] = detail
        checks["cF"] = f == 1.0
        if not checks["cF"]:
            for d in detail:
                if not d["ok"]:
                    want = "tidak ada pada T" if d["ref"] is None else fmt(d["ref"])
                    reasons.append(f"Klaim ({d['e']}, {d['m']}, {fmt(d['v'])}) tidak setia: T memuat {want}")
        checks["cδ"] = el["delta"] <= th["theta_e"]
        if not checks["cδ"]:
            reasons.append(f"Dua ekstraksi tidak konsisten: δ = {el['delta']:.3f} > θe = {th['theta_e']}")
        checks["cL"] = bool(el.get("label_tertulis"))
        if not checks["cL"]:
            reasons.append("Nilai tidak tercetak pada grafik: angka hasil perkiraan skala, tidak dapat diverifikasi")
        checks["cA"] = el["axis_ok"]
        if not el["axis_ok"]:
            reasons.append(f"Pemeriksaan sumbu gagal: {el['axis_msg']}")
    else:
        reasons.append({
            "rumus": "Rumus: pengenal kedua belum tersedia, ditahan (fail-closed)",
            "foto": "Foto tidak memiliki pemeriksaan otomatis (K = ∅)",
            "diagram": "Diagram nondata tidak memiliki pemeriksaan otomatis (K = ∅)",
            "tabel": "Tabel-citra: struktur belum diverifikasi, perlu tinjauan",
        }.get(el["jenis"], "Grafik tanpa tabel data yang dapat diekstraksi"))
    pub = bool(checks) and all(checks.values())
    el["checks"], el["reasons"] = checks, reasons
    el["status"] = "terbit_otomatis" if pub else "antrean"
    return el


# ---------------------------------------------------------------- demo adversarial
MUTATIONS = {
    "ubah_angka": "Mengubah satu angka nilai (mis. 38 → 45)",
    "tukar_label": "Menukar pasangan label–nilai dua kategori",
    "turunan_salah": "Mengubah angka turunan (selisih) yang dihitung",
    "tren_salah": "Membalik label tren",
}


def inject(seg, claims, kind: str, seed: int = 0, min_gap: float = 0.0):
    """Menyuntik satu kesalahan ke deskripsi; mengembalikan segmen dan klaim baru.

    min_gap membatasi tukar label pada pasangan yang selisihnya cukup besar untuk bermakna
    (dipakai demo); evaluasi memakai 0 sehingga pasangan di bawah ε ikut terhitung.
    """
    rnd = random.Random(seed)
    seg = [dict(s) for s in seg]
    claims = [dict(c) for c in claims]
    idx_nilai = [i for i, c in enumerate(claims) if c["m"] == "nilai"]
    touched = []
    if kind == "ubah_angka" and idx_nilai:
        i = rnd.choice(idx_nilai)
        v = claims[i]["v"]
        claims[i]["v"] = round(v * rnd.choice([1.18, 1.25, 0.8]) + (1 if v == 0 else 0), 1 if v != int(v) else 0)
        touched = [i]
    elif kind == "tukar_label" and len(idx_nilai) >= 2:
        pairs = [(a, b) for a in idx_nilai for b in idx_nilai if a < b and claims[a]["v"] != claims[b]["v"]]
        pairs = [p for p in pairs if abs(claims[p[0]]["v"] - claims[p[1]]["v"]) > min_gap] or pairs
        a, b = rnd.choice(pairs)
        claims[a]["v"], claims[b]["v"] = claims[b]["v"], claims[a]["v"]
        touched = [a, b]
    elif kind == "turunan_salah":
        i = next((i for i, c in enumerate(claims) if c["m"] == "selisih"), None)
        if i is not None:
            claims[i]["v"] = round(claims[i]["v"] * 1.3 + 2, 1)
            touched = [i]
    elif kind == "tren_salah":
        i = next((i for i, c in enumerate(claims) if c["m"] == "tren"), None)
        if i is not None:
            claims[i]["v"] = "turun" if claims[i]["v"] != "turun" else "naik"
            touched = [i]
    for s in seg:
        if s.get("claim") in touched:
            v = claims[s["claim"]]["v"]
            s["text"] = v if isinstance(v, str) else fmt(v)
            s["injected"] = True
    return seg, claims, touched


# ---------------------------------------------------------------- pemeriksa teks bebas (B2)
_NUM = re.compile(r"(?<![\w,.])(-?\d{1,3}(?:\.\d{3})+(?:,\d+)?|-?\d+(?:,\d+)?)(?![\w]|[.,]\d)")
_MONTH = {"jan": "januari", "feb": "februari", "mar": "maret", "apr": "april", "mei": "mei", "jun": "juni",
          "jul": "juli", "agu": "agustus", "sep": "september", "okt": "oktober", "nov": "november", "des": "desember"}
_DERIVED_KW = re.compile(r"selisih|beda|perbedaan|rerata|rata-rata|rata rata|total|jumlah keseluruhan|kenaikan|"
                         r"penurunan|naik|turun|meningkat|menurun|bertambah|berkurang", re.I)
_AXIS_STRONG = re.compile(r"sumbu|skala|rentang|label tik|garis bantu", re.I)
_AXIS_KW = re.compile(r"hingga|sampai", re.I)


def parse_num(tok: str) -> float:
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", tok):
        tok = tok.replace(".", "")
    return float(tok.replace(",", "."))


def _aliases(cat: str) -> list[str]:
    n = norm(cat)
    out = [n]
    if n in _MONTH:
        out.append(_MONTH[n])
    return out


def check_free_text(text: str, table, D, eps) -> list[dict]:
    """Memeriksa angka pada deskripsi bebas (B2) terhadap tabel acuan, per klausa.

    Angka yang bukan klaim data diabaikan: tahun, rentang/label sumbu, jumlah kategori.
    Angka setia bila cocok dengan nilai kategori yang disebut di klausa yang sama, atau dengan
    fakta turunan bila klausa memuat kata selisih/rerata/total/kenaikan; cocok dengan kategori
    lain berarti label tertukar. Ini pemeriksa pola, sehingga presisinya diaudit manual.
    """
    s = _value_range(table)
    tol = max(eps * s, 1e-9)
    facts = facts_of(table, D)
    derived_vals = [abs(f["v"]) for f in facts if f["m"] != "nilai" and not isinstance(f["v"], str)]
    out = []
    for cm in re.finditer(r"[^,;.:]+(?:[.,]\d[^,;.:]*)*", text):
        clause = cm.group(0)
        low = " " + norm(clause) + " "
        mentioned = [r for r in table if any(f" {a} " in low for a in _aliases(r["kategori"]))]
        for m in _NUM.finditer(clause):
            tok = m.group(1)
            v = parse_num(tok)
            if re.fullmatch(r"(19|20)\d{2}", tok):
                continue  # tahun: label kategori atau judul, bukan klaim nilai
            if v == len(table) and re.search(r"kategori|batang|titik|bulan|provinsi|kelas|unit|fakultas", clause, re.I)                     and not any(abs(r["nilai"] - v) <= tol for r in table):
                continue  # jumlah kategori
            if _AXIS_STRONG.search(clause) or (_AXIS_KW.search(clause) and not mentioned
                                                and not _DERIVED_KW.search(clause)):
                continue  # rentang atau label sumbu
            hit_cat = [r for r in mentioned if abs(r["nilai"] - v) <= tol]
            hit_der = _DERIVED_KW.search(clause) and any(abs(dv - abs(v)) <= tol for dv in derived_vals)
            any_val = [r["kategori"] for r in table if abs(r["nilai"] - v) <= tol]
            if hit_cat or hit_der:
                verdict = "setia"
            elif not mentioned and (any_val or any(abs(dv - abs(v)) <= tol for dv in derived_vals)):
                verdict = "setia"
            elif any_val:
                verdict = "label_tertukar"
            else:
                verdict = "dikarang"
            st = cm.start() + m.start(1)
            out.append({"start": st, "end": st + len(tok), "v": v, "verdict": verdict,
                        "note": "" if verdict == "setia" else (f"angka ini milik {', '.join(any_val)}" if any_val
                                                              else "tidak ada pada tabel data")})
    return out
