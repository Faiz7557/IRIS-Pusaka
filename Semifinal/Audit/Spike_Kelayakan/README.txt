Skrip uji kelayakan teknis (29 Sep 2026). Semua dijalankan sekali di laptop tim (CPU saja, 15 GB RAM).
finish_pdfua.py   : melengkapi metadata PDF/UA-1 (Lang, MarkInfo, Tabs, XMP, DisplayDocTitle) + mengisi Alt pada Figure (pikepdf)
verapdf_check.py  : menjalankan veraPDF (profil ua1) dan meringkas aturan yang gagal; path veraPDF di dalamnya perlu disesuaikan
inspect_tagged.py : menghitung tag hasil auto-tag OpenDataLoader (Figure, Alt, TH, TD, Formula)
spike_ssim.py     : uji apakah SSIM membedakan rumus salah dari rumus benar berbeda font (proksi: mathtext DejaVu vs CM)
spike_gate.py     : uji kelemahan Pers. (2) dan (5)
spike_alt.py      : patch Alt pada PDF yang sudah bertag
Perlu: pip install pikepdf pymupdf opendataloader-pdf torch torchmetrics matplotlib; Java 11+; veraPDF 1.30.
