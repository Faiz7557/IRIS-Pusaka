"""Evaluasi SIMAK dengan kriteria lulus terkunci (Tabel 7).

  python -m eval.evaluate kalibrasi   # set pengembangan saja → thresholds.json (locked)
  python -m eval.evaluate uji         # set uji tertahan, sekali, setelah ambang dikunci

Gerbang yang dijalankan: G1 (struktur dan metadata), G3 (kesetiaan angka dan
penahanan deskripsi yang diubah), G4 (kesetaraan informasi, rasio Q).
Pembanding: B0 (PDF asli), B1 (auto-tag tanpa modul tambahan), B2 (VLM langsung).
"""
import hashlib
import json
import math
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from simak import chart, gate, pipeline, vlm
from simak.config import DATA, ROOT, THRESHOLDS_FILE, WORK, thresholds

SYN = DATA / "synth"
OUT = ROOT / "eval"
SEED = 20260930
CRITERIA = {"G1": "≥90% dokumen uji bebas kegagalan teks alt, bahasa, judul; lebih baik dari B1",
            "G3": "Fk ≥ 0,98 pada keluaran terbit; ≥ 0,90 deskripsi yang diubah tertahan",
            "G4": "Q ≥ 0,80"}


def wilson(k, n, z=1.96):
    """Pers. (8): selang kepercayaan Wilson untuk proporsi."""
    if n == 0:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [round(c - h, 4), round(c + h, 4)]


def prop(k, n):
    return {"k": k, "n": n, "p": round(k / n, 4) if n else None, "ci95": wilson(k, n)}


def charts(split):
    return [c for c in json.loads((SYN / "charts.json").read_text(encoding="utf-8")) if c["set"] == split]


def truth_of(c):
    t = [{"kategori": k, "nilai": v} for k, v in zip(c["kategori"], c["nilai"])]
    return t, chart.derived(t, chart.is_ordered({"jenis_grafik": c["jenis_grafik"]}, t), thresholds()["rho"])


def run_chart(c, th):
    img = (SYN / "charts" / f"{c['id']}.png").read_bytes()
    el = pipeline.process_image({"id": c["id"], "page": 1, "kind": "image", "png_bytes": img}, th)
    return el


def map_threads(fn, items, n=16):
    with ThreadPoolExecutor(max_workers=n) as ex:
        return list(ex.map(fn, items))


# ------------------------------------------------------------------ kalibrasi
def kalibrasi():
    th = thresholds()
    if th.get("locked"):
        print("Ambang sudah dikunci; hapus thresholds.json untuk kalibrasi ulang (dan laporkan).")
        return
    dev = charts("dev")
    print(f"Kalibrasi pada {len(dev)} grafik pengembangan…")
    els = map_threads(lambda c: run_chart(c, th), dev)
    rows = []
    for c, el in zip(dev, els):
        if not el.get("claims"):
            rows.append({"id": c["id"], "delta": None})
            continue
        t, D = truth_of(c)
        f, _ = gate.fk(el["claims"], t, D, th["epsilon"])
        rows.append({"id": c["id"], "delta": el["delta"], "axis": el["axis_ok"] and el["label_tertulis"], "fk": f,
                     "label": c["label_nilai"], "label_tertulis_vlm": el["label_tertulis"]})
    best = None
    grid = [0.0, 0.002, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05, 0.08, 0.12]
    table = []
    for te in grid:
        pub = [r for r in rows if r["delta"] is not None and r["delta"] <= te and r["axis"]]
        fk_mean = sum(r["fk"] for r in pub) / len(pub) if pub else None
        table.append({"theta_e": te, "terbit": len(pub), "fk_rerata": fk_mean})
    # Aturan: θe terkecil (≥ 0,01 untuk pembulatan) yang mempertahankan jumlah terbit maksimum
    # di antara nilai dengan rerata Fk ≥ 0,98. Memilih ujung atas dataran Fk = 1 terlalu longgar.
    ok = [r for r in table if r["fk_rerata"] is not None and r["fk_rerata"] >= 0.98 and r["theta_e"] >= 0.01]
    if ok:
        top = max(r["terbit"] for r in ok)
        best = min(r["theta_e"] for r in ok if r["terbit"] == top)
    th.update(theta_e=best if best is not None else 0.0, locked=True,
              locked_at=time.strftime("%Y-%m-%d %H:%M:%S"), calibrated_on=f"{len(dev)} grafik dev",
              aturan="θe terkecil (≥0,01) yang mempertahankan jumlah terbit maksimum dengan rerata Fk (vs acuan) ≥ 0,98 pada grafik dev",
              riwayat="v1: Fk 0,937 pada δ=0 → ditambah cL (nilai tercetak) dan aturan urutan acuan diselaraskan; "
                      "v2: cA ditoleransi 20% rentang (sumbu melewati tik terluar); set uji belum dibuka")
    THRESHOLDS_FILE.write_text(json.dumps(th, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "kalibrasi.json").write_text(json.dumps({"grid": table, "per_grafik": rows, "terkunci": th},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    for r in table:
        print(r)
    print("θe dikunci =", th["theta_e"])


# ------------------------------------------------------------------ G4: pertanyaan otomatis
def questions(c, rnd):
    t, D = truth_of(c)
    dd = {f["m"]: f for f in D}
    k = rnd.choice(t)
    return [
        ("Kategori apa yang memiliki nilai tertinggi?", "kat", dd["maksimum"]["e"]),
        ("Kategori apa yang memiliki nilai terendah?", "kat", dd["minimum"]["e"]),
        (f"Berapa nilai {k['kategori']}?", "num", k["nilai"]),
        ("Berapa selisih antara nilai tertinggi dan terendah?", "num", dd["selisih"]["v"]),
    ]


def grade(ans, kind, want, s, eps):
    a = ans.strip()
    if kind == "kat":
        return chart.norm(want) in chart.norm(a)
    nums = [gate.parse_num(m.group(1)) for m in gate._NUM.finditer(a)]
    return any(abs(v - want) <= max(eps * s, 1e-9) for v in nums)


def table_text(c):
    unit = f" ({c['satuan']})" if c["satuan"] else ""
    return f"Tabel data grafik “{c['judul']}”. Kolom: {c['label_x']}; {c['label_y']}{unit}.\n" + "\n".join(
        f"{k}: {chart.fmt(v)}" for k, v in zip(c["kategori"], c["nilai"]))


# ------------------------------------------------------------------ uji tertahan
def uji(n_g4=20):
    th = thresholds()
    if not th.get("locked"):
        sys.exit("Ambang belum dikunci. Jalankan kalibrasi pada set pengembangan dahulu.")
    test = charts("uji")
    print(f"G3 pada {len(test)} grafik uji…")
    els = map_threads(lambda c: run_chart(c, th), test)
    b2 = map_threads(lambda c: vlm.describe_direct((SYN / "charts" / f"{c['id']}.png").read_bytes()), test)

    d_claims_pub = d_ok_pub = 0
    b2_nums = b2_ok = 0
    pub_n = 0
    per = []
    inj = {k: [0, 0] for k in gate.MUTATIONS}
    for c, el, txt in zip(test, els, b2):
        t, D = truth_of(c)
        row = {"id": c["id"], "jenis": c["jenis_grafik"], "label_nilai": c["label_nilai"], "status": el["status"],
               "delta": el.get("delta")}
        if el.get("claims"):
            f, det = gate.fk(el["claims"], t, D, th["epsilon"])
            row["fk_vs_acuan"] = f
            if el["status"] == "terbit_otomatis":
                pub_n += 1
                d_claims_pub += len(det)
                d_ok_pub += sum(d["ok"] for d in det)
                for k in gate.MUTATIONS:
                    seg, cl, touched = gate.inject(el["seg"], el["claims"], k, seed=SEED)
                    if not touched:
                        continue
                    m = {**el, "seg": seg, "claims": cl}
                    gate.evaluate(m, th)
                    inj[k][1] += 1
                    inj[k][0] += m["status"] != "terbit_otomatis"
        marks = gate.check_free_text(txt, t, D, th["epsilon"])
        b2_nums += len(marks)
        b2_ok += sum(m["verdict"] == "setia" for m in marks)
        row["b2_angka"] = len(marks)
        row["b2_keliru"] = sum(m["verdict"] != "setia" for m in marks)
        per.append(row)
    inj_total = [sum(v[0] for v in inj.values()), sum(v[1] for v in inj.values())]

    g3 = {
        "D_fk_terbit": prop(d_ok_pub, d_claims_pub),
        "D_terbit": prop(pub_n, len(test)),
        "D_R_beban_tinjauan": prop(len(test) - pub_n, len(test)),
        "B2_fk_perkiraan": prop(b2_ok, b2_nums),
        "B2_terbit": prop(len(test), len(test)),
        "B2_grafik_dengan_angka_keliru": prop(sum(r["b2_keliru"] > 0 for r in per), len(test)),
        "D_angka_keliru_terbit": d_claims_pub - d_ok_pub,
        "B2_angka_keliru_terbit": b2_nums - b2_ok,
        "injeksi_tertahan": prop(*inj_total),
        "injeksi_per_jenis": {k: prop(*v) for k, v in inj.items()},
    }
    g3["lulus"] = bool(g3["D_fk_terbit"]["p"] is not None and g3["D_fk_terbit"]["p"] >= 0.98
                       and g3["injeksi_tertahan"]["p"] is not None and g3["injeksi_tertahan"]["p"] >= 0.90)

    # G4: subset tetap dari grafik uji yang punya deskripsi SIMAK
    rnd = random.Random(SEED)
    cand = [(c, el, txt) for c, el, txt in zip(test, els, b2) if el.get("alt_auto")]
    sub = rnd.sample(cand, min(n_g4, len(cand)))
    print(f"G4 pada {len(sub)} grafik ({len(sub) * 4 * 3} pertanyaan)…")
    jobs = []
    for c, el, txt in sub:
        for q, kind, want in questions(c, rnd):
            for src, ctx in (("tabel", table_text(c)), ("D", el["alt_auto"]), ("B2", txt)):
                jobs.append((c, q, kind, want, src, ctx))
    answers = map_threads(lambda j: vlm.answer(j[5], j[1]), jobs)
    acc = {"tabel": [0, 0], "D": [0, 0], "B2": [0, 0]}
    for (c, q, kind, want, src, _), a in zip(jobs, answers):
        s = max(c["nilai"]) - min(c["nilai"])
        acc[src][1] += 1
        acc[src][0] += grade(a, kind, want, s, th["epsilon"])
    a_tab = acc["tabel"][0] / acc["tabel"][1]
    g4 = {k: prop(*v) for k, v in acc.items()}
    g4["Q_D"] = round((acc["D"][0] / acc["D"][1]) / a_tab, 4) if a_tab else None
    g4["Q_B2"] = round((acc["B2"][0] / acc["B2"][1]) / a_tab, 4) if a_tab else None
    g4["lulus"] = bool(g4["Q_D"] and g4["Q_D"] >= 0.80)

    # G1: dokumen uji sintetis melalui pipeline penuh
    docs = [m for m in json.loads((SYN / "docs.json").read_text(encoding="utf-8")) if m["set"] == "uji"]
    print(f"G1 pada {len(docs)} dokumen uji…")
    g1_rows = []
    for m in docs:
        job = WORK / f"eval_{Path(m['file']).stem}"
        st = pipeline.run(SYN / "docs" / m["file"], job)
        rep = st["report"]
        g1_rows.append({"file": m["file"], **{k: {"aturan_gagal": rep[k]["verapdf"].get("failed_rules"),
                                                   "g1_lulus": rep[k]["g1"]["pass"],
                                                   "g1_ketat": rep[k]["g1"]["pass_ketat"]} for k in ("B0", "B1", "D")},
                        "detik": st["timing"]["total_s"], "halaman": st["pages"]})
    g1 = {k: prop(sum(r[k]["g1_lulus"] for r in g1_rows), len(g1_rows)) for k in ("B0", "B1", "D")}
    # Penanda "[Menunggu tinjauan ULD]" dihitung belum bermakna; dilaporkan berdampingan, bukan kriteria terkunci.
    g1["D_ketat"] = prop(sum(r["D"]["g1_ketat"] for r in g1_rows), len(g1_rows))
    g1["veraPDF_lulus_D"] = prop(sum(r["D"]["aturan_gagal"] == 0 for r in g1_rows), len(g1_rows))
    g1["lulus"] = bool(g1["D"]["p"] >= 0.90 and g1["D"]["p"] > g1["B1"]["p"])

    data_hash = hashlib.sha256((SYN / "charts.json").read_bytes()).hexdigest()[:12]
    res = {"waktu": time.strftime("%Y-%m-%d %H:%M:%S"), "manifest": vlm.manifest(), "ambang": th,
           "data": {"grafik_uji": len(test), "dokumen_uji": len(docs), "hash_charts_json": data_hash, "seed": SEED},
           "kriteria": CRITERIA, "G1": g1, "G1_per_dokumen": g1_rows, "G3": g3, "G4": g4, "per_grafik": per}
    old = OUT / "results.json"
    if old.exists() and "G6_ringan" in (prev := json.loads(old.read_text(encoding="utf-8"))):
        res["G6_ringan"] = prev["G6_ringan"]
    old.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("G1", "G3", "G4")}, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------ G6 ringan: dokumen nyata
def nyata():
    """G1 dan beban tinjauan R pada sampel dokumen nyata dari bingkai Common Crawl ac.id."""
    th = thresholds()
    if not th.get("locked"):
        sys.exit("Ambang belum dikunci.")
    meta = json.loads((DATA / "cc" / "cc.json").read_text(encoding="utf-8"))
    rows = []
    for m in meta["sampel"]:
        job = WORK / f"eval_{Path(m['file']).stem}"
        print("memproses", m["file"], flush=True)
        try:
            st = pipeline.run(DATA / "cc" / m["file"], job)
        except Exception as e:
            rows.append({"file": m["file"], "domain": m["domain"], "galat": f"{type(e).__name__}: {e}"[:200]})
            continue
        imgs = [e for e in st["elements"] if e["kind"] == "image"]
        nondek = [e for e in imgs if e["status"] != "dekoratif"]
        rep = st["report"]
        rows.append({"file": m["file"], "domain": m["domain"], "halaman": st["pages"], "bertag_asli": st["tagged_input"],
                     "gambar": len(imgs) + st["patch"]["figur_tambahan"], "dekoratif": len(imgs) - len(nondek),
                     "figur_vektor_ditahan": st["patch"]["figur_tambahan"],
                     "antrean": sum(e["status"] == "antrean" for e in nondek) + st["patch"]["figur_tambahan"],
                     "terbit_otomatis": sum(e["status"] == "terbit_otomatis" for e in nondek),
                     **{k: {"aturan_gagal": rep[k]["verapdf"].get("failed_rules"), "g1_lulus": rep[k]["g1"]["pass"],
                            "g1_ketat": rep[k]["g1"]["pass_ketat"]}
                        for k in ("B0", "B1", "D")}, "detik": st["timing"]["total_s"]})
    ok = [r for r in rows if "galat" not in r]
    g6 = {"sumber": f"Common Crawl {meta['crawl']}, seed {meta['seed']}, bingkai stratum A = {meta['bingkai_stratum_A']}",
          "dokumen": len(rows), "berhasil": len(ok),
          **{f"G1_{k}": prop(sum(r[k]["g1_lulus"] for r in ok), len(ok)) for k in ("B0", "B1", "D")},
          "G1_D_ketat": prop(sum(r["D"]["g1_ketat"] for r in ok), len(ok)),
          "veraPDF_lulus_D": prop(sum(r["D"]["aturan_gagal"] == 0 for r in ok), len(ok)),
          "R_beban_tinjauan": prop(sum(r["antrean"] for r in ok), sum(r["gambar"] - r["dekoratif"] for r in ok)),
          "per_dokumen": rows}
    f = OUT / "results.json"
    res = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    res["G6_ringan"] = g6
    f.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in g6.items() if k != "per_dokumen"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"kalibrasi": kalibrasi, "uji": uji, "nyata": nyata}[sys.argv[1]]()
