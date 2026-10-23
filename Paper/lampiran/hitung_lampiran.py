"""Data lampiran baru (rincian per grafik, injeksi per kasus, audit B2), dihitung luring dari cache.

  python lampiran/hitung_lampiran.py   (dari folder Final/Paper)

Tidak memanggil API: GEMINI key dikosongkan; cache miss menghentikan skrip.
Keluaran: lampiran/lampiran_data.json. Status setiap grafik dicocokkan dengan eval/results.json.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROTO = HERE.parents[1] / "Prototype"
os.chdir(PROTO)
sys.path.insert(0, str(PROTO))

from simak import chart, gate, vlm  # noqa: E402
from simak.config import thresholds  # noqa: E402
from eval.evaluate import SEED, charts, run_chart, truth_of  # noqa: E402

vlm.KEYS[:] = []
th = thresholds()
res = json.load(open("eval/results.json", encoding="utf-8"))
beku = {p["id"]: p for p in res["per_grafik"]}

grafik, injeksi, audit = [], [], []
for c in charts("uji"):
    el = run_chart(c, th)
    t, D = truth_of(c)
    s = max(c["nilai"]) - min(c["nilai"])
    row = {
        "id": c["id"], "judul": c["judul"], "jenis": c["jenis_grafik"], "label_nilai": c["label_nilai"],
        "n_kategori": len(c["kategori"]), "status": el["status"], "delta": el.get("delta"),
        "checks": el.get("checks", {}), "alasan": el.get("reasons", []),
        "n_klaim": len(el.get("claims") or []),
    }
    if el.get("claims"):
        f, det = gate.fk(el["claims"], t, D, th["epsilon"])
        row["klaim_setia"] = sum(d["ok"] for d in det)
    b = beku[c["id"]]
    assert b["status"] == el["status"], (c["id"], b["status"], el["status"])
    row["b2_angka"], row["b2_keliru"] = b["b2_angka"], b["b2_keliru"]
    grafik.append(row)

    if el["status"] == "terbit_otomatis":
        for k in gate.MUTATIONS:
            seg, cl, touched = gate.inject(el["seg"], el["claims"], k, seed=SEED)
            if not touched:
                continue
            m = {**el, "seg": seg, "claims": cl}
            gate.evaluate(m, th)
            injeksi.append({"id": c["id"], "jenis": k, "tertahan": m["status"] != "terbit_otomatis",
                            "alasan": m.get("reasons", []), "eps_s": round(th["epsilon"] * s, 3)})

    txt = vlm.describe_direct(open(f"data/synth/charts/{c['id']}.png", "rb").read())
    for m in gate.check_free_text(txt, t, D, th["epsilon"]):
        if m["verdict"] != "setia":
            audit.append({"id": c["id"], "label_nilai": c["label_nilai"], "verdict": m["verdict"],
                          "kutipan": txt[max(0, m["start"] - 60):m["end"] + 15].replace("\n", " ").strip()})

kal = {"v1": json.load(open("eval/kalibrasi_v1_sebelum_perbaikan.json", encoding="utf-8")),
       "v2": json.load(open("eval/kalibrasi.json", encoding="utf-8"))}
out = {"grafik": grafik, "injeksi": injeksi, "audit_b2": audit, "kalibrasi": kal,
       "charts_json": json.load(open("data/synth/charts.json", encoding="utf-8"))}

# self-check terhadap angka kanon run 2
g3 = res["G3"]
assert sum(r["status"] == "terbit_otomatis" for r in grafik) == g3["D_terbit"]["k"]
assert sum(r.get("klaim_setia", 0) for r in grafik if r["status"] == "terbit_otomatis") == g3["D_fk_terbit"]["k"]
assert (sum(i["tertahan"] for i in injeksi), len(injeksi)) == (g3["injeksi_tertahan"]["k"], g3["injeksi_tertahan"]["n"])
assert len(audit) == g3["B2_angka_keliru_terbit"], len(audit)
(HERE / "lampiran_data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(grafik), "grafik,", len(injeksi), "injeksi,", len(audit), "tanda B2")
