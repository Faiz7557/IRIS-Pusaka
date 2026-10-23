"""Daftar semua angka B2 yang ditandai keliru, untuk audit manual presisi pemeriksa."""
import json
from simak import chart, config, gate, vlm

th = config.thresholds()
for c in json.load(open("data/synth/charts.json", encoding="utf-8")):
    if c["set"] != "uji":
        continue
    txt = vlm.describe_direct(open(f"data/synth/charts/{c['id']}.png", "rb").read())
    t = [{"kategori": k, "nilai": v} for k, v in zip(c["kategori"], c["nilai"])]
    D = chart.derived(t, chart.is_ordered({"jenis_grafik": c["jenis_grafik"]}, t), th["rho"])
    dd = {f["m"]: round(f["v"], 2) if not isinstance(f["v"], str) else f["v"] for f in D}
    for m in gate.check_free_text(txt, t, D, th["epsilon"]):
        if m["verdict"] != "setia":
            ctx = txt[max(0, m["start"] - 80):m["end"] + 20].replace("\n", " ")
            print(f"{c['id']} | {'label' if c['label_nilai'] else 'NOLABEL'} | {m['verdict']} | ...{ctx}...")
            print(f"     acuan {dict(zip(c['kategori'], c['nilai']))} rerata={dd['rerata']} selisih={dd['selisih']}")
