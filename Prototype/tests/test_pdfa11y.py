import tempfile
import unittest
from pathlib import Path

import fitz
import pikepdf
from pikepdf import Array, Dictionary, Name

from simak import pdfa11y, pipeline

HELD = pipeline.HELD_FIGURE_ALT
PAGE_H = 842


def make_tagged(path: Path, boxes, skip_mcid=()):
    """PDF bertag satu halaman: satu Figure per bbox (ruang PDF) ditambah satu P, seperti keluaran auto-tag."""
    p = pikepdf.new()
    p.add_blank_page(page_size=(595, PAGE_H))
    page = p.pages[0]
    img = pikepdf.Stream(p, b"\x80", Type=Name.XObject, Subtype=Name.Image, Width=1, Height=1,
                         ColorSpace=Name.DeviceGray, BitsPerComponent=8)
    page.Resources = Dictionary(XObject=Dictionary(Im0=img))
    ops = []
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        draw = f"q {x1 - x0} 0 0 {y1 - y0} {x0} {y0} cm /Im0 Do Q"
        ops.append(draw if i in skip_mcid else f"/Figure <</MCID {i}>> BDC {draw} EMC")
    ops.append(f"/P <</MCID {len(boxes)}>> BDC EMC")
    page.Contents = p.make_stream("\n".join(ops).encode())
    root = p.make_indirect(Dictionary(Type=Name.StructTreeRoot))
    doc = p.make_indirect(Dictionary(Type=Name.StructElem, S=Name.Document, P=root))
    kids = [p.make_indirect(Dictionary(Type=Name.StructElem, S=Name.Figure, P=doc, Pg=page.obj, K=Array([i]),
                                       A=Dictionary(O=Name.Layout, BBox=Array(list(bb)))))
            for i, bb in enumerate(boxes)]
    kids.append(p.make_indirect(Dictionary(Type=Name.StructElem, S=Name.P, P=doc, Pg=page.obj,
                                           K=Array([len(boxes)]))))
    doc.K = Array(kids)
    root.K = doc
    root.ParentTree = Dictionary(Nums=Array([0, Array(kids)]))
    root.ParentTreeNextKey = 1
    page.obj.StructParents = 0
    p.Root.StructTreeRoot = root
    p.Root.MarkInfo = Dictionary(Marked=True)
    p.save(path)


def marked(pdf: Path):
    with pikepdf.open(pdf) as p:
        return [(str(i.operator), str(i.operands[0]), i.operands[1].get("/MCID") if len(i.operands) > 1 else None)
                for i in pikepdf.parse_content_stream(p.pages[0]) if str(i.operator) in ("BDC", "BMC")]


BOXES = [(50, 600, 300, 800), (50, 350, 300, 550), (50, 100, 300, 300)]


class PatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / "work")
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.src, self.dst = self.dir / "src.pdf", self.dir / "dst.pdf"

    def run_patch(self, entries):
        return pdfa11y.patch(self.src, self.dst, "Uji", {1: entries}, HELD)

    def test_decorative_figure_becomes_artifact(self):
        make_tagged(self.src, BOXES[:2])
        st = self.run_patch([{"id": "a", "alt": None, "bbox": None}, {"id": "b", "alt": "Grafik penjualan", "bbox": None}])
        self.assertEqual(pdfa11y.figure_alts(self.dst), ["Grafik penjualan"])
        self.assertEqual(marked(self.dst), [("BMC", "/Artifact", None), ("BDC", "/Figure", 1), ("BDC", "/P", 2)])
        with pikepdf.open(self.dst) as p:
            arr = p.Root.StructTreeRoot.ParentTree.Nums[1]
            self.assertIsNone(arr[0])
            self.assertEqual(arr[1].get("/Alt"), "Grafik penjualan")
            self.assertEqual([str(k.S) for k in p.Root.StructTreeRoot.K.K], ["/Figure", "/P"])
        self.assertEqual((st["artefak"], st["artefak_gagal"], sorted(st["tertanam"])), (1, 0, ["a", "b"]))
        g1 = pdfa11y.g1_audit(self.dst)
        self.assertEqual((g1["figures"], g1["alt_bermakna"]), (1, 1))

    def test_unmappable_decorative_keeps_figure_with_alt(self):
        make_tagged(self.src, BOXES[:1], skip_mcid={0})  # MCID tidak ada di content stream
        st = self.run_patch([{"id": "a", "alt": None, "bbox": None}])
        self.assertEqual(pdfa11y.figure_alts(self.dst), [pdfa11y.DECORATIVE_ALT])
        self.assertEqual((st["artefak"], st["artefak_gagal"]), (0, 1))
        self.assertEqual(marked(self.dst), [("BDC", "/P", 1)])

    def test_mismatched_page_pairs_by_bbox_and_holds_the_rest(self):
        make_tagged(self.src, BOXES)
        near = lambda b: [b[0] + 3, b[1] - 2, b[2] + 1, b[3] + 2]
        st = self.run_patch([{"id": "c", "alt": "Alt C", "bbox": near(BOXES[2])},
                             {"id": "a", "alt": "Alt A", "bbox": near(BOXES[0])}])
        self.assertEqual(pdfa11y.figure_alts(self.dst), ["Alt A", HELD, "Alt C"])
        self.assertEqual(st["halaman_tidak_cocok"], [1])
        self.assertEqual((st["figur_ditahan"], st["figur_tambahan"]), (1, 1))
        self.assertEqual(sorted(st["tertanam"]), ["a", "c"])

    def test_mismatched_page_without_reliable_bbox_holds_every_figure(self):
        make_tagged(self.src, BOXES)
        half = [50, 450, 300, 650]  # IoU dengan figur pertama dan kedua 0,33: tidak cukup untuk dipasangkan
        st = self.run_patch([{"id": "a", "alt": "Alt A", "bbox": None}, {"id": "b", "alt": "Alt B", "bbox": half}])
        self.assertEqual(pdfa11y.figure_alts(self.dst), [HELD] * 3)
        self.assertEqual(st["tertanam"], [])

    def test_mismatched_page_decorative_match_becomes_artifact(self):
        make_tagged(self.src, BOXES)
        st = self.run_patch([{"id": "b", "alt": None, "bbox": list(BOXES[1])}])
        self.assertEqual(pdfa11y.figure_alts(self.dst), [HELD, HELD])
        self.assertEqual(marked(self.dst)[1], ("BMC", "/Artifact", None))
        self.assertEqual((st["artefak"], st["tertanam"]), (1, ["b"]))


class AssembleTests(unittest.TestCase):
    """Keputusan ULD sampai ke PDF bertag lewat assemble, termasuk konversi bbox fitz → ruang PDF."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / "work")
        self.addCleanup(self.tmp.cleanup)
        self.job = Path(self.tmp.name)
        make_tagged(self.job / "asli.pdf", BOXES)

    def fitz_box(self, b):
        return [b[0], PAGE_H - b[3], b[2], PAGE_H - b[1]]

    def image(self, el_id, box, status, **kw):
        return {"id": el_id, "kind": "image", "page": 1, "bbox": self.fitz_box(box), "status": status,
                "jenis": "grafik", "reasons": [], **kw}

    def test_decision_on_mismatched_page_reaches_pdf(self):
        # tiga Figure bertag, dua citra terproses: halaman tidak cocok
        state = {"title": "Uji", "elements": [
            self.image("e0", BOXES[0], "disetujui", alt_final="Disetujui untuk figur atas"),
            self.image("e2", BOXES[2], "dekoratif")]}
        pipeline.assemble(self.job, state)
        self.assertEqual(pdfa11y.figure_alts(self.job / "simak.pdf"),
                         ["[Disetujui ULD] Disetujui untuk figur atas", HELD])
        self.assertEqual(marked(self.job / "simak.pdf")[2], ("BMC", "/Artifact", None))
        els = {e["id"]: e for e in state["elements"]}
        self.assertFalse(els["e0"]["pdf_ditahan"])
        self.assertNotIn(pipeline.PDF_HELD_REASON, els["e0"]["reasons"])

    def test_unmatched_element_is_flagged_and_auto_publish_held(self):
        state = {"title": "Uji", "elements": [
            self.image("e0", (400, 600, 500, 700), "terbit_otomatis", alt_auto="Deskripsi otomatis"),
            self.image("e1", (400, 100, 500, 200), "disetujui", alt_final="Keputusan ULD")]}
        pipeline.assemble(self.job, state)
        els = {e["id"]: e for e in state["elements"]}
        self.assertEqual(els["e0"]["status"], "antrean")
        self.assertEqual(els["e1"]["status"], "disetujui")
        for e in els.values():
            self.assertTrue(e["pdf_ditahan"])
            self.assertEqual(e["reasons"].count(pipeline.PDF_HELD_REASON), 1)
        self.assertEqual(pdfa11y.figure_alts(self.job / "simak.pdf"), [HELD] * 3)
        pipeline.assemble(self.job, state)  # perakitan ulang tidak menggandakan alasan
        self.assertEqual(els["e1"]["reasons"].count(pipeline.PDF_HELD_REASON), 1)


if __name__ == "__main__":
    unittest.main()
