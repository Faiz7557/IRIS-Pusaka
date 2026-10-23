"""Selisih dua run evaluasi (Bab III.C: versi akhir dijalankan dua kali dan selisihnya dilaporkan).

  python -m eval.banding_run eval/results_run1_2026-10-12.json eval/results.json
"""
import json
import sys


def fmt(x):
    return f"{x['k']}/{x['n']}" if isinstance(x, dict) and "k" in x else str(x)


def main(a_path, b_path):
    a, b = (json.load(open(p, encoding="utf-8")) for p in (a_path, b_path))
    print(f"run A {a['waktu']}  vs  run B {b['waktu']}")
    for k in ("model_t1", "model_t2", "prompt_t1", "prompt_t2", "skema"):
        if a["manifest"].get(k) != b["manifest"].get(k):
            print(f"  manifes {k}: {a['manifest'].get(k)} -> {b['manifest'].get(k)}")
    if a["ambang"] != b["ambang"]:
        print("  PERINGATAN: ambang berbeda antar-run")
    for g in ("G1", "G3", "G4"):
        for m, va in a[g].items():
            if isinstance(va, dict) and "k" not in va:
                continue
            vb = b[g].get(m)
            print(f"{g}.{m}: {fmt(va)} | {fmt(vb)}{'' if va == vb else '  <- beda'}")
    pa = {p["id"]: p for p in a["per_grafik"]}
    beda = [(i, pa[i]["status"], p["status"]) for i, p in ((p["id"], p) for p in b["per_grafik"])
            if i in pa and pa[i]["status"] != p["status"]]
    print(f"status grafik berbeda: {len(beda)}/{len(b['per_grafik'])}")
    for i, sa, sb in beda:
        print(f"  {i}: {sa} -> {sb}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
