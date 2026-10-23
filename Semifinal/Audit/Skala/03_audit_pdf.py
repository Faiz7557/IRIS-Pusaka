# -*- coding: utf-8 -*-
"""Langkah 3: audit struktur/metadata setiap PDF sampel (pikepdf + PyMuPDF) dan validasi PDF/UA-1 (veraPDF).
Jalankan: python 03_audit_pdf.py unduhan/ hasil_audit.csv
Tidak ada isi dokumen yang disimpan ke keluaran; hanya metadata dan hitungan agregat per dokumen.
"""
import sys, os, re, csv, subprocess, time, collections
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import pikepdf

VP = r"C:\vpaudit\verapdf\verapdf.bat"
PLACEHOLDER = re.compile(r"^\s*(image|img|gambar|picture|pic|figure|fig|foto|photo|slide|shape|graphic)[\s_\-]*\d*\s*$|\.(png|jpe?g|gif|bmp|emf|wmf)\b", re.I)
ID_W = set("yang dan dengan untuk dari pada adalah dalam ini itu atau akan oleh dapat sebagai tidak karena juga ke di serta bahwa dalam antara suatu".split())
EN_W = set("the and of to in is that for with as on by are this from be or an it at which can not".split())
STD = {"Figure", "Table", "TH", "TD", "TR", "Formula", "P", "L", "LI", "H", "H1", "H2", "H3", "H4", "H5", "H6", "Document", "Sect", "Span", "Link", "Caption"}


def walk_struct(root, maxnodes=400000):
    st = root.get("/StructTreeRoot")
    res = dict(node=0, figure=0, fig_alt=0, fig_alt_bermakna=0, table=0, table_th=0, th=0, formula=0, heading=0, truncated=0)
    if st is None:
        return res
    rolemap = {}
    rm = st.get("/RoleMap")
    if rm is not None:
        for k in rm.keys():
            rolemap[str(k)[1:]] = str(rm[k])[1:]

    def std(name):
        seen = 0
        while name not in STD and name in rolemap and seen < 10:
            name = rolemap[name]; seen += 1
        return name

    seen = set()
    stack = [(st.get("/K"), None)]
    tables = {}
    while stack:
        n, tbl = stack.pop()
        if n is None:
            continue
        if isinstance(n, pikepdf.Array):
            for k in n:
                stack.append((k, tbl))
            continue
        if not isinstance(n, pikepdf.Dictionary):
            continue
        try:
            og = n.objgen
            if og != (0, 0):
                if og in seen:
                    continue
                seen.add(og)
        except Exception:
            pass
        res["node"] += 1
        if res["node"] > maxnodes:
            res["truncated"] = 1
            break
        s = n.get("/S")
        cur = tbl
        if s is not None:
            t = std(str(s)[1:])
            if t == "Figure":
                res["figure"] += 1
                alt = n.get("/Alt")
                txt = str(alt).strip() if alt is not None else ""
                if txt:
                    res["fig_alt"] += 1
                    if not PLACEHOLDER.search(txt) and len(txt) >= 3:
                        res["fig_alt_bermakna"] += 1
            elif t == "Table":
                res["table"] += 1
                cur = id(n)
                tables[cur] = False
            elif t == "TH":
                res["th"] += 1
                if tbl is not None:
                    tables[tbl] = True
            elif t == "Formula":
                res["formula"] += 1
            elif t in ("H", "H1", "H2", "H3", "H4", "H5", "H6"):
                res["heading"] += 1
        k = n.get("/K")
        if k is not None:
            stack.append((k, cur))
    res["table_th"] = sum(1 for v in tables.values() if v)
    return res


def text_stats(path, maxp=12):
    import fitz
    d = fitz.open(path)
    n = len(d)
    chars = 0; idc = 0; enc = 0
    land = 0
    for i in range(min(n, maxp)):
        p = d[i]
        t = p.get_text()
        chars += len(t)
        ws = re.findall(r"[a-zA-Z]+", t.lower())
        idc += sum(1 for w in ws if w in ID_W); enc += sum(1 for w in ws if w in EN_W)
        if p.rect.width > p.rect.height:
            land += 1
    m = min(n, maxp)
    imgs = 0
    for i in range(min(n, 60)):
        try:
            for im in d[i].get_images(full=True):
                if im[2] >= 100 and im[3] >= 100:
                    imgs += 1
        except Exception:
            pass
    lang = "tak_terdeteksi"
    if idc + enc >= 15:
        lang = "id" if idc > 1.5 * enc else ("en" if enc > 1.5 * idc else "campuran")
    return dict(char_per_hal=round(chars / max(m, 1)), bahasa_isi=lang, hal_lanskap_pct=round(100 * land / max(m, 1)), gambar_besar_60hal=imgs)


def audit_one(path):
    rec = dict(file=os.path.basename(path), ukuran_kb=round(os.path.getsize(path) / 1024))
    try:
        pdf = pikepdf.open(path)
    except Exception as e:
        rec["status"] = "gagal_buka:" + type(e).__name__
        return rec
    rec["status"] = "ok"
    try:
        root = pdf.Root
        rec["halaman"] = len(pdf.pages)
        info = pdf.docinfo
        rec["pembuat"] = (str(info.get("/Producer", "")) + " | " + str(info.get("/Creator", "")))[:120]
        title = str(info.get("/Title", "")).strip()
        rec["judul_metadata"] = int(bool(title))
        lang = root.get("/Lang")
        rec["lang"] = str(lang) if lang is not None else ""
        mi = root.get("/MarkInfo")
        marked = bool(mi.get("/Marked")) if mi is not None and "/Marked" in mi else False
        rec["ditandai"] = int(("/StructTreeRoot" in root) and marked)
        rec["terenkripsi"] = int(pdf.is_encrypted)
        rec.update(walk_struct(root))
    except Exception as e:
        rec["status"] = "gagal_struktur:" + type(e).__name__
    try:
        rec.update(text_stats(path))
    except Exception as e:
        rec["status_teks"] = type(e).__name__
    return rec


RULE = re.compile(r'<rule specification="[^"]*" clause="([^"]+)" testNumber="(\d+)" status="failed"[^>]*?failedChecks="(\d+)"')


def verapdf(path):
    try:
        r = subprocess.run([VP, "--flavour", "ua1", "--format", "xml", "--maxfailuresdisplayed", "1", path],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
    except subprocess.TimeoutExpired:
        return os.path.basename(path), dict(ua1="timeout")
    x = r.stdout
    if "<validationReport" not in x:
        return os.path.basename(path), dict(ua1="galat")
    m = re.search(r'isCompliant="(\w+)"', x)
    rules = RULE.findall(x)
    return os.path.basename(path), dict(ua1=("lulus" if m and m.group(1) == "true" else "gagal"), aturan_gagal=len(rules),
                                       pemeriksaan_gagal=sum(int(n) for _, _, n in rules),
                                       daftar_aturan=";".join(f"{c}-{t}" for c, t, _ in rules))


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    files = sorted(os.path.join(src, f) for f in os.listdir(src) if f.lower().endswith(".pdf"))
    print("dokumen:", len(files))
    t0 = time.time()
    rows = {}
    with ProcessPoolExecutor(max_workers=12) as ex:
        for i, r in enumerate(ex.map(audit_one, files, chunksize=4)):
            rows[r["file"]] = r
            if (i + 1) % 50 == 0:
                print("struktur", i + 1, round(time.time() - t0), "dtk", flush=True)
    print("struktur selesai", round(time.time() - t0), "dtk")
    ok = [f for f in files if rows[os.path.basename(f)].get("status") == "ok"]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(verapdf, f) for f in ok]
        for i, fu in enumerate(as_completed(futs)):
            name, d = fu.result()
            rows[name].update(d)
            if (i + 1) % 50 == 0:
                print("veraPDF", i + 1, round(time.time() - t0), "dtk", flush=True)
    keys = []
    for r in rows.values():
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows.values():
            w.writerow(r)
    print("selesai", round(time.time() - t0), "dtk ->", out)
