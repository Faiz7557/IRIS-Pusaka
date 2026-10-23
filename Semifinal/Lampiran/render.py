# -*- coding: utf-8 -*-
"""Render PPTX -> PNG per slide (dan PDF) memakai PowerPoint COM."""
import sys, os, win32com.client
src = os.path.abspath(sys.argv[1]); outdir = os.path.abspath(sys.argv[2])
os.makedirs(outdir, exist_ok=True)
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
app = win32com.client.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(src, WithWindow=False, ReadOnly=True)
n = pres.Slides.Count
h = int(w * 7.5 / 13.333)
for i in range(1, n + 1):
    pres.Slides(i).Export(os.path.join(outdir, f"s{i:02d}.png"), "PNG", w, h)
if len(sys.argv) > 4:
    pres.SaveAs(os.path.abspath(sys.argv[4]), 32)  # ppSaveAsPDF
pres.Close()
try:
    app.Quit()
except Exception:
    pass
print("slides:", n)
