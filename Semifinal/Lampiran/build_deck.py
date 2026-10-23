# -*- coding: utf-8 -*-
"""Deck Lampiran F SIMAK. Jalankan: python build_deck.py [keluaran.pptx]"""
import sys
sys.path.insert(0, ".")
from slides1 import prs, f1, f2, f3, f4
from slides2 import f5, f6, f7, f8, f9, f10, f11, f12, f13

for fn in (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13):
    fn()

out = sys.argv[1] if len(sys.argv) > 1 else "Lampiran_F_SIMAK.pptx"
prs.save(out)
print("saved", out)
