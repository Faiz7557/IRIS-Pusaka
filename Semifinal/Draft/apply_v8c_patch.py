# -*- coding: utf-8 -*-
s = open("edit_paper_v6.py", encoding="utf8").read()
k = open("koherensi_v8.py", encoding="utf8").read()


def rep(txt, old, new):
    assert old in txt, old[:80]
    return txt.replace(old, new, 1)


s = rep(s, 'Nama “simak” berarti mendengarkan dengan saksama: materi kuliah yang dapat disimak tanpa ada yang terlewat. ', '')
s = rep(s, "k = 13.0 / 15.0", "k = 12.6 / 15.0")
k = rep(k, "keduanya ditangani dengan stratum pembanding, dokumen sintetis, dan pelaporan batas generalisasi.", "keduanya ditangani dengan stratum pembanding dan dokumen sintetis.")
k = rep(k, "menjadi LaTeX [@r35]; set uji UniMER-Test memuat 23.789 sampel dalam empat kategori (cetak sederhana, cetak kompleks, tangkapan layar, tulisan tangan).",
        "menjadi LaTeX [@r35]; UniMER-Test memuat 23.789 sampel dalam empat kategori (cetak, kompleks, tangkapan layar, tulisan tangan).")
k = rep(k, "100 rumus UniMER-Test dan 150 rumus sintetis (LaTeX acuan diketahui)", "100 rumus UniMER-Test dan 150 sintetis")
open("edit_paper_v6.py", "w", encoding="utf8").write(s)
open("koherensi_v8.py", "w", encoding="utf8").write(k)
print("ok")
