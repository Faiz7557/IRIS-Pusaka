"""Tangkapan layar MVP untuk Gambar 4 (montase 2×2), dijalankan luring dari cache.

  python gambar/tangkap_mvp.py [materi_03.pdf]   (dari folder Final/Paper)

Menyalakan server SIMAK sendiri tanpa GEMINI_API_KEY (kondisi demo luring), lalu memotret:
(a) Remediasi & Tinjauan, (b) Demo Gerbang setelah suntik "tukar label", (c) Evaluasi, (d) HTML keluaran.
"""
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
PROTO = OUT.parents[1] / "Prototype"
PORT = 8017
URL = f"http://127.0.0.1:{PORT}"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DOC = sys.argv[1] if len(sys.argv) > 1 else "materi_03.pdf"


def tunggu_server():
    for _ in range(60):
        try:
            urllib.request.urlopen(URL + "/api/sampel", timeout=2)
            return
        except Exception:
            time.sleep(1)
    raise SystemExit("server SIMAK tidak menyala")


def potret(page, nama):
    p = OUT / f"g4_{nama}.png"
    page.screenshot(path=str(p))
    print("ok", p.name)
    return p


def montase(paths):
    ims = [Image.open(p) for p in paths]
    w, h = ims[0].size
    pad, lab = 24, 64
    M = Image.new("RGB", (2 * w + 3 * pad, 2 * (h + lab) + 3 * pad), "white")
    d = ImageDraw.Draw(M)
    try:
        f = ImageFont.truetype("times.ttf", 52)
    except OSError:
        f = ImageFont.load_default()
    for i, (im, tag) in enumerate(zip(ims, "abcd")):
        x, y = pad + (i % 2) * (w + pad), pad + (i // 2) * (h + lab + pad)
        d.text((x + w // 2, y + lab // 2), f"({tag})", fill="black", font=f, anchor="mm")
        M.paste(im, (x, y + lab))
        d.rectangle([x, y + lab, x + w - 1, y + lab + h - 1], outline="#888888", width=2)
    p = OUT / "Gambar4_montase.png"
    M.save(p, dpi=(300, 300))
    print("ok", p.name, M.size)


def main():
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GEMINI_API_KEY", "ELEVENLABS"))}
    srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "app:app", "--port", str(PORT)],
                           cwd=PROTO, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        tunggu_server()
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=CHROME)
            page = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2, locale="id-ID")

            # (a) Remediasi & Tinjauan: proses satu dokumen contoh, buka elemen pertama di antrean
            page.goto(URL + "/")
            page.click(f"#sampel button[data-s='{DOC}']")
            page.wait_for_selector("#hasil:not(.hide)", timeout=180_000)
            page.wait_for_timeout(1500)
            jid = page.evaluate("JID")
            first = page.locator(".qlist button, .qlist [role=button], .qlist li").first
            if first.count():
                first.click()
                page.wait_for_timeout(800)
            page.evaluate("scrollTo(0, document.querySelector('#hasil').getBoundingClientRect().top + scrollY - 12)")
            pa = potret(page, "a_remediasi")

            # (b) Demo Gerbang: grafik syn043, suntik tukar label (B2 terbit, SIMAK ditahan)
            page.goto(URL + "/demo.html?grafik=syn043")
            page.wait_for_function("typeof BASE !== 'undefined' && BASE", timeout=120_000)
            page.click("#mut button[data-k='tukar_label']")
            page.wait_for_function("!document.querySelector('#run').disabled", timeout=60_000)
            page.wait_for_timeout(800)
            pb = potret(page, "b_demo_gerbang")

            # (c) Evaluasi
            page.goto(URL + "/evaluasi.html")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            pc = potret(page, "c_evaluasi")

            # (d) HTML keluaran dengan cap status dan bilah mode dengar
            page.goto(f"{URL}/keluaran/{jid}/simak.html")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(800)
            pd = potret(page, "d_html_keluaran")
            b.close()
        montase([pa, pb, pc, pd])
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()
