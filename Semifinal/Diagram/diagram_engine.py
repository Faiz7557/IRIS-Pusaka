# -*- coding: utf-8 -*-
"""Satu spesifikasi -> (1) file .drawio (XML mxGraph, dapat diedit di diagrams.net) dan (2) PNG dengan tata letak identik."""
import xml.sax.saxutils as su
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Ellipse
from matplotlib import font_manager as fm

COL = {  # fill, stroke
    "blue": ("#dae8fc", "#6c8ebf"), "pink": ("#f8cecc", "#b85450"), "orange": ("#ffcc99", "#d79b00"),
    "yellow": ("#fff2cc", "#d6b656"), "green": ("#d5e8d4", "#82b366"), "purple": ("#e1d5e7", "#9673a6"),
    "gray": ("#f5f5f5", "#666666"), "white": ("#ffffff", "#666666"), "red": ("#f8cecc", "#b85450"),
    "peach": ("#ffe6cc", "#d79b00"), "cream": ("#fffbe6", "#d6b656"),
    "clear": ("#ffffff", "none"),
}


class Node:
    def __init__(self, id, text, x, y, w, h, color="white", kind="box", bold=False, fs=12,
                 dashed=False, parent=None, thick=False, fillnone=False):
        self.id, self.text, self.x, self.y, self.w, self.h = id, text, x, y, w, h
        self.color, self.kind, self.bold, self.fs = color, kind, bold, fs
        self.dashed, self.parent, self.thick, self.fillnone = dashed, parent, thick, fillnone


class Edge:
    def __init__(self, src, dst, p0, p1, via=(), dashed=False, color="#333333"):
        self.src, self.dst, self.p0, self.p1 = src, dst, p0, p1
        self.via, self.dashed, self.color = list(via), dashed, color


class Diagram:
    def __init__(self, W, H, name):
        self.W, self.H, self.name = W, H, name
        self.nodes, self.edges, self.labels, self.lines = [], [], [], []

    def node(self, *a, **k):
        n = Node(*a, **k); self.nodes.append(n); return n

    def edge(self, *a, **k):
        e = Edge(*a, **k); self.edges.append(e); return e

    def label(self, text, x, y, fs=11, color="#333333", bold=False, italic=False, w=90, h=16):
        self.labels.append((text, x, y, fs, color, bold, italic, w, h))

    def freeline(self, pts, dashed=True, color="#888888"):
        self.lines.append((pts, dashed, color))

    def byid(self, i):
        return [n for n in self.nodes if n.id == i][0]

    # ---------------- drawio ----------------
    def to_drawio(self, path):
        cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

        def esc(t):
            return su.escape(t, {'"': "&quot;"}).replace("\n", "&lt;br&gt;")

        for n in self.nodes:
            fill, stroke = COL[n.color]
            par, ox, oy = "1", 0, 0
            if n.parent:
                par = n.parent; p = self.byid(n.parent); ox, oy = p.x, p.y
            st = ["html=1", "whiteSpace=nowrap", "fontFamily=Arial", "fontSize=%d" % n.fs, "fontColor=#000000",
                  "strokeColor=%s" % stroke, "strokeWidth=%d" % (2 if n.thick else 1)]
            if n.kind == "diamond":
                st.insert(0, "rhombus")
            elif n.kind == "cyl":
                st.insert(0, "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=8")
            else:
                st.insert(0, "rounded=1;arcSize=%d" % (6 if n.kind == "container" else 12))
            st.append("fillColor=%s" % ("none" if n.fillnone else fill))
            if n.dashed: st.append("dashed=1")
            if n.bold: st.append("fontStyle=1")
            st.append("verticalAlign=top;spacingTop=4" if n.kind == "container" else "verticalAlign=middle")
            cells.append('<mxCell id="%s" value="%s" style="%s;" vertex="1" parent="%s"><mxGeometry x="%g" y="%g" width="%g" height="%g" as="geometry"/></mxCell>'
                         % (n.id, esc(n.text), ";".join(st), par, n.x - ox, n.y - oy, n.w, n.h))
        for i, e in enumerate(self.edges):
            a, b = self.byid(e.src), self.byid(e.dst)
            st = ["edgeStyle=none", "html=1", "rounded=0", "endArrow=block", "endFill=1", "strokeColor=%s" % e.color, "strokeWidth=1.5",
                  "exitX=%.4f" % ((e.p0[0] - a.x) / a.w), "exitY=%.4f" % ((e.p0[1] - a.y) / a.h),
                  "entryX=%.4f" % ((e.p1[0] - b.x) / b.w), "entryY=%.4f" % ((e.p1[1] - b.y) / b.h),
                  "exitPerimeter=0", "entryPerimeter=0"]
            if e.dashed: st.append("dashed=1")
            pts = "".join('<mxPoint x="%g" y="%g"/>' % p for p in e.via)
            geo = '<mxGeometry relative="1" as="geometry">%s</mxGeometry>' % (('<Array as="points">%s</Array>' % pts) if pts else "")
            cells.append('<mxCell id="e%d" style="%s;" edge="1" parent="1" source="%s" target="%s">%s</mxCell>' % (i, ";".join(st), e.src, e.dst, geo))
        for j, (pts, dash, col) in enumerate(self.lines):
            st = "edgeStyle=none;html=1;endArrow=none;strokeColor=%s;strokeWidth=1;%s" % (col, "dashed=1;" if dash else "")
            mid = "".join('<mxPoint x="%g" y="%g"/>' % p for p in pts[1:-1])
            cells.append('<mxCell id="l%d" style="%s" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="%g" y="%g" as="sourcePoint"/><mxPoint x="%g" y="%g" as="targetPoint"/>%s</mxGeometry></mxCell>'
                         % (j, st, pts[0][0], pts[0][1], pts[-1][0], pts[-1][1], ('<Array as="points">%s</Array>' % mid) if mid else ""))
        for k, (t, x, y, fs, col, b, it, w, h) in enumerate(self.labels):
            fst = (1 if b else 0) | (2 if it else 0)
            st = "text;html=1;align=center;verticalAlign=middle;fontFamily=Arial;fontSize=%d;fontColor=%s;%swhiteSpace=nowrap;" % (fs, col, ("fontStyle=%d;" % fst) if fst else "")
            cells.append('<mxCell id="t%d" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="%g" y="%g" width="%g" height="%g" as="geometry"/></mxCell>'
                         % (k, esc(t), st, x - w / 2, y - h / 2, w, h))
        xml = ('<mxfile host="app.diagrams.net"><diagram id="%s" name="%s"><mxGraphModel dx="%d" dy="%d" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="%d" pageHeight="%d" math="0" shadow="0"><root>%s</root></mxGraphModel></diagram></mxfile>'
               % (self.name, self.name, self.W, self.H, self.W, self.H, "".join(cells)))
        open(path, "w", encoding="utf-8").write(xml)

    # ---------------- PNG ----------------
    def to_png(self, path, dpi=220):
        fam = "Arial" if any(f.name == "Arial" for f in fm.fontManager.ttflist) else "DejaVu Sans"
        fig = plt.figure(figsize=(self.W / 100, self.H / 100))
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, self.W); ax.set_ylim(self.H, 0); ax.axis("off")
        k = 0.72
        for n in self.nodes:
            fill, stroke = COL[n.color]; lw = 2.2 if n.thick else 1.0
            ls = "--" if n.dashed else "-"
            fc = "none" if n.fillnone else fill
            if n.kind == "diamond":
                ax.add_patch(Polygon([(n.x + n.w / 2, n.y), (n.x + n.w, n.y + n.h / 2), (n.x + n.w / 2, n.y + n.h), (n.x, n.y + n.h / 2)],
                                     closed=True, fc=fc, ec=stroke, lw=lw, ls=ls, zorder=2))
            elif n.kind == "cyl":
                ax.add_patch(FancyBboxPatch((n.x, n.y + 6), n.w, n.h - 6, boxstyle="round,pad=0,rounding_size=4", fc=fc, ec=stroke, lw=lw, zorder=2))
                ax.add_patch(Ellipse((n.x + n.w / 2, n.y + 8), n.w, 14, fc=fc, ec=stroke, lw=lw, zorder=3))
            else:
                r = 6 if n.kind == "container" else 8
                ax.add_patch(FancyBboxPatch((n.x, n.y), n.w, n.h, boxstyle="round,pad=0,rounding_size=%d" % r, fc=fc, ec=stroke, lw=lw, ls=ls,
                                            zorder=1 if n.kind == "container" else 2))
            fw = "bold" if n.bold else "normal"
            if n.kind == "container":
                ax.text(n.x + n.w / 2, n.y + 6, n.text, ha="center", va="top", fontsize=n.fs * k, fontweight=fw, family=fam, zorder=4, linespacing=1.15)
            else:
                cy = n.y + n.h / 2 + (4 if n.kind == "cyl" else 0)
                ax.text(n.x + n.w / 2, cy, n.text, ha="center", va="center", fontsize=n.fs * k, fontweight=fw, family=fam, zorder=4, linespacing=1.15)
        for e in self.edges:
            pts = [e.p0] + list(e.via) + [e.p1]
            ls = "--" if e.dashed else "-"
            for i in range(len(pts) - 2):
                ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]], color=e.color, lw=1.1, ls=ls, zorder=5, solid_capstyle="butt")
            a, b = pts[-2], pts[-1]
            ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>,head_length=0.55,head_width=0.25", color=e.color, lw=1.1, ls=ls,
                                                            shrinkA=0, shrinkB=0), zorder=6)
        for pts, dash, col in self.lines:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, lw=0.9, ls="--" if dash else "-", zorder=0)
        for (t, x, y, fs, col, b, it, w, h) in self.labels:
            ax.text(x, y, t, ha="center", va="center", fontsize=fs * k, color=col, fontweight="bold" if b else "normal",
                    fontstyle="italic" if it else "normal", family=fam, zorder=7, bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.85))
        fig.savefig(path, dpi=dpi, facecolor="white"); plt.close(fig)
