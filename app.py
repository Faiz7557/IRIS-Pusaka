"""SIMAK — aplikasi web tiga lapis (Lampiran E).

Jalankan:  python -m uvicorn app:app --port 8000
Titik akhir mengikuti rancangan: POST /api/unggah, GET /api/pekerjaan/{id},
POST /api/tinjau/{id}/{el}, GET /keluaran/{id}/simak.html|simak.pdf.
Dokumen diproses per sesi di work/ dan dihapus saat sesi dihapus atau kedaluwarsa.
"""
import json
import shutil
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from simak import chart, gate, listen, pipeline, vlm
from simak.config import DATA, ROOT, WORK, thresholds

app = FastAPI(title="SIMAK")
WEB = ROOT / "web"
JOBS: dict[str, dict] = {}
SYN = DATA / "synth"
SESSION_TTL = 6 * 3600


def _cleanup():
    for d in WORK.glob("job_*"):
        if time.time() - d.stat().st_mtime > SESSION_TTL:
            shutil.rmtree(d, ignore_errors=True)


_cleanup()


def _job_dir(jid: str) -> Path:
    if not jid.isalnum():
        raise HTTPException(400)
    return WORK / f"job_{jid}"


def _start(pdf: Path, name: str) -> str:
    jid = uuid.uuid4().hex[:10]
    job = _job_dir(jid)
    job.mkdir(parents=True)
    shutil.copy(pdf, job / "asli.pdf")
    JOBS[jid] = {"tahap": "antre", "pesan": "Menunggu", "nama": name, "mulai": time.time()}

    def work():
        try:
            pipeline.run(job / "asli.pdf", job, lambda t, m: JOBS[jid].update(tahap=t, pesan=m))
        except Exception as e:  # dilaporkan ke antarmuka, tidak disembunyikan
            JOBS[jid].update(tahap="gagal", pesan=f"{type(e).__name__}: {e}")
    threading.Thread(target=work, daemon=True).start()
    return jid


# ------------------------------------------------------------------ dokumen
@app.get("/api/sampel")
def sampel():
    meta = json.loads((SYN / "docs.json").read_text(encoding="utf-8"))
    out = [{"file": m["file"], "set": m["set"]} for m in meta]
    cc = DATA / "cc" / "cc.json"
    if cc.exists():
        out += [{"file": m["file"], "set": "nyata"} for m in json.loads(cc.read_text(encoding="utf-8"))["sampel"]]
    return out


@app.post("/api/sampel/{name}")
def proses_sampel(name: str):
    f = SYN / "docs" / Path(name).name
    if not f.exists():
        f = DATA / "cc" / Path(name).name
    if not f.exists():
        raise HTTPException(404)
    return {"id": _start(f, f.name)}


@app.post("/api/unggah")
async def unggah(file: UploadFile = File(...)):
    data = await file.read()
    if not data.startswith(b"%PDF"):
        raise HTTPException(400, "Berkas bukan PDF")
    tmp = WORK / f"up_{uuid.uuid4().hex}.pdf"
    tmp.write_bytes(data)
    try:
        return {"id": _start(tmp, Path(file.filename or "dokumen.pdf").name)}
    finally:
        tmp.unlink(missing_ok=True)


@app.get("/api/pekerjaan/{jid}")
def pekerjaan(jid: str):
    job = _job_dir(jid)
    info = JOBS.get(jid, {})
    if (job / "state.json").exists() and info.get("tahap") in (None, "selesai"):
        st = pipeline.load(job)
        st.pop("_job", None)
        return {"tahap": "selesai", "nama": info.get("nama", st.get("file")), "state": st}
    if not job.exists():
        raise HTTPException(404)
    return {"tahap": info.get("tahap"), "pesan": info.get("pesan"), "nama": info.get("nama")}


@app.get("/api/pekerjaan/{jid}/dengar")
def dengar(jid: str):
    """Dua transkrip untuk halaman Dengar: simulasi PDF asli dan urutan baca hasil SIMAK."""
    job = _job_dir(jid)
    if not (job / "state.json").exists():
        raise HTTPException(404, "Dokumen belum selesai diproses")
    st = pipeline.load(job)
    asli, simak = listen.original(job / "asli.pdf"), listen.remediated(st)
    listen.pair(asli, st)
    return {"judul": st["title"], "berkas": st.get("file"), "asli": asli, "simak": simak,
            "ringkasan": listen.summary(asli, simak)}


@app.get("/api/pekerjaan/{jid}/img/{el}")
def gambar(jid: str, el: str):
    f = _job_dir(jid) / "img" / f"{Path(el).name}.png"
    if not f.exists():
        raise HTTPException(404)
    return FileResponse(f)


class Tinjau(BaseModel):
    aksi: str
    alt: str = ""


@app.post("/api/tinjau/{jid}/{el}")
def tinjau(jid: str, el: str, body: Tinjau):
    if body.aksi not in ("setujui", "ubah", "tolak", "dekoratif"):
        raise HTTPException(400)
    if body.aksi == "ubah" and not body.alt.strip():
        raise HTTPException(400, "Teks alternatif tidak boleh kosong")
    return pipeline.review(_job_dir(jid), el, body.aksi, body.alt.strip())


@app.get("/keluaran/{jid}/{name}")
def keluaran(jid: str, name: str):
    if name not in ("simak.html", "simak.pdf", "asli.pdf"):
        raise HTTPException(404)
    f = _job_dir(jid) / name
    if not f.exists():
        raise HTTPException(404)
    return FileResponse(f, filename=None if name.endswith("html") else f"{name}")


@app.delete("/api/pekerjaan/{jid}")
def hapus(jid: str):
    shutil.rmtree(_job_dir(jid), ignore_errors=True)
    JOBS.pop(jid, None)
    return {"dihapus": True}


# ------------------------------------------------------------------ demo adversarial
def _charts():
    return {c["id"]: c for c in json.loads((SYN / "charts.json").read_text(encoding="utf-8"))}


@app.get("/api/demo/grafik")
def demo_grafik():
    return [{"id": c["id"], "judul": c["judul"], "jenis": c["jenis_grafik"], "label_nilai": c["label_nilai"]}
            for c in _charts().values() if c["set"] == "uji"]


DEMO: dict[str, dict] = {}


def _simak_chart(img: bytes) -> dict:
    th = thresholds()
    el = {"id": "demo", "page": 1, "png_bytes": img, "kind": "image"}
    return pipeline.process_image(el, th)


@app.post("/api/demo/jalankan/{cid}")
def demo_jalankan(cid: str):
    charts = _charts()
    if cid not in charts:
        raise HTTPException(404)
    spec = charts[cid]
    img = (SYN / "charts" / f"{cid}.png").read_bytes()
    el = _simak_chart(img)
    b2 = vlm.describe_direct(img)
    th = thresholds()
    truth = [{"kategori": k, "nilai": v} for k, v in zip(spec["kategori"], spec["nilai"])]
    ordered = chart.is_ordered({"jenis_grafik": spec["jenis_grafik"]}, [{"kategori": k} for k in spec["kategori"]])
    D_true = chart.derived(truth, ordered, th["rho"])
    b2_marks = gate.check_free_text(b2, truth, D_true, th["epsilon"])
    simak_vs_truth = None
    if el.get("claims"):
        f, det = gate.fk(el["claims"], truth, D_true, th["epsilon"])
        simak_vs_truth = {"fk": f, "detail": det}
    DEMO[cid] = {"el": el, "b2": b2, "truth": truth, "D_true": D_true}
    return {"spec": {k: spec[k] for k in ("id", "judul", "jenis_grafik", "label_nilai", "satuan")},
            "truth": truth, "simak": el, "simak_vs_truth": simak_vs_truth,
            "b2": {"text": b2, "marks": b2_marks, "status": "terbit (tanpa gerbang)"}, "thresholds": th}


class Suntik(BaseModel):
    jenis: str
    seed: int = 0


@app.post("/api/demo/suntik/{cid}")
def demo_suntik(cid: str, body: Suntik):
    if cid not in DEMO or body.jenis not in gate.MUTATIONS:
        raise HTTPException(400)
    d = DEMO[cid]
    el = json.loads(json.dumps(d["el"]))
    if not el.get("seg"):
        raise HTTPException(400, "Elemen ini tidak memiliki deskripsi grafik")
    vals = [r["nilai"] for r in el["table"]]
    gap = 2 * thresholds()["epsilon"] * (max(vals) - min(vals))
    seg, claims, touched = gate.inject(el["seg"], el["claims"], body.jenis, body.seed, min_gap=gap)
    if not touched:
        raise HTTPException(400, "Mutasi tidak berlaku untuk grafik ini (mis. tidak ada tren)")
    el["seg"], el["claims"] = seg, claims
    gate.evaluate(el, thresholds())
    # Kesalahan yang sama pada B2: angka yang sama di teks bebas diganti; tanpa gerbang, tetap terbit.
    th = thresholds()
    b2_text = d["b2"]
    marks = gate.check_free_text(b2_text, d["truth"], d["D_true"], th["epsilon"])
    edits, used = [], set()
    for i in touched:
        old_v, new_v = d["el"]["claims"][i]["v"], claims[i]["v"]
        if isinstance(old_v, str):
            if old_v in b2_text:
                b2_text = b2_text.replace(old_v, new_v, 1)
            continue
        m = next((m for m in marks if abs(m["v"] - old_v) < 1e-6 and m["start"] not in used), None)
        if m:
            used.add(m["start"])
            edits.append((m["start"], m["end"], chart.fmt(new_v)))
    for s, e, t in sorted(edits, reverse=True):
        b2_text = b2_text[:s] + t + b2_text[e:]
    return {"mutasi": gate.MUTATIONS[body.jenis], "simak": el,
            "b2": {"text": b2_text, "marks": gate.check_free_text(b2_text, d["truth"], d["D_true"], th["epsilon"]),
                   "status": "terbit (tanpa gerbang)"}}


@app.get("/api/demo/mutasi")
def demo_mutasi():
    return gate.MUTATIONS


# ------------------------------------------------------------------ evaluasi
# ------------------------------------------------------------------ suara
SUARA = {"eleven": "Suara manusia (ElevenLabs)"}  # satu-satunya sumber suara
_voice_lock = threading.Lock()
_prep_q: list[tuple] = []
_prep_cv = threading.Condition()


class Suara(BaseModel):
    teks: str
    suara: str = "eleven"
    kecepatan: int = 0   # persen, mis. -10 atau 15
    nada: int = 0        # Hz, mis. -20 atau 10


_interactive = [0]  # permintaan pengguna yang sedang menunggu; pra-pembuatan mengalah padanya


def _synth(teks: str, suara: str, kecepatan: int, nada: int, prioritas: bool = True):
    from simak import voice
    if prioritas:
        _interactive[0] += 1
    try:
        with _voice_lock:  # konverter OpenVoice tidak aman dipakai bersamaan
            return voice.synthesize(teks, speaker=suara, rate=f"{kecepatan:+d}%", pitch=f"{nada:+d}Hz")
    finally:
        if prioritas:
            _interactive[0] -= 1


def _prep_worker():
    while True:
        with _prep_cv:
            while not _prep_q:
                _prep_cv.wait()
            job = _prep_q.pop(0)
        while _interactive[0] > 0:  # beri jalan untuk suara yang sedang ditunggu pengguna
            time.sleep(0.1)
        try:
            _synth(*job, prioritas=False)
        except Exception as e:  # pembuatan awal hanya mempercepat; kegagalan tidak menghentikan server
            print("siapkan suara gagal:", e)


threading.Thread(target=_prep_worker, daemon=True).start()


@app.get("/api/suara/daftar")
def suara_daftar():
    from simak import voice
    return [{"id": k, "nama": v} for k, v in SUARA.items() if k not in voice.PAID_SPEAKERS or voice.eleven_ready()]


@app.post("/api/suara")
def suara(body: Suara):
    if body.suara not in SUARA or not body.teks.strip() or len(body.teks) > 4000:
        raise HTTPException(400, "Teks atau suara tidak valid")
    try:
        f = _synth(body.teks, body.suara, max(-50, min(50, body.kecepatan)), max(-50, min(50, body.nada)))
    except Exception as e:
        raise HTTPException(503, f"Suara tidak dapat dibuat: {type(e).__name__}")
    return FileResponse(f, media_type="audio/mpeg")


class Siapkan(BaseModel):
    teks: list[str]
    suara: str = "eleven"
    kecepatan: int = 0
    nada: int = 0


@app.post("/api/suara/siapkan")
def suara_siapkan(body: Siapkan):
    """Membuat audio lebih dulu di latar belakang agar pemutaran tidak menunggu."""
    from simak import voice
    if body.suara not in SUARA:
        raise HTTPException(400)
    if body.suara in voice.PAID_SPEAKERS:  # berbayar per karakter: hanya dibuat saat benar-benar diputar
        return {"diantrekan": 0}
    with _prep_cv:
        for t in body.teks[:300]:
            if t.strip():
                _prep_q.append((t, body.suara, body.kecepatan, body.nada))
        _prep_cv.notify()
    return {"diantrekan": len(body.teks[:300])}


@app.get("/api/evaluasi")
def evaluasi():
    f = ROOT / "eval" / "results.json"
    if not f.exists():
        return JSONResponse({"ada": False})
    return json.loads(f.read_text(encoding="utf-8"))


@app.get("/api/grafik/{cid}.png")
def grafik_png(cid: str):
    f = SYN / "charts" / f"{Path(cid).name}.png"
    if not f.exists():
        raise HTTPException(404)
    return FileResponse(f)


app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
