"""Konfigurasi SIMAK: path, model, dan ambang gerbang.

Ambang (θe, ε, ρ) disetel pada set pengembangan oleh eval/calibrate.py lalu
dikunci ke thresholds.json; set uji tertahan tidak boleh dipakai untuk menyetel.
"""
import hashlib
import json
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env.local", override=False)
DATA = ROOT / "data"
WORK = ROOT / "work"          # sesi sementara (dihapus per sesi)
CACHE = ROOT / "cache"        # cache respons VLM untuk dokumen demo
TOOLS = ROOT / "tools"
for p in (WORK, CACHE):
    p.mkdir(exist_ok=True)

MODEL = os.environ.get("SIMAK_MODEL", "gemma-4-26b-a4b-it")

THRESHOLDS_FILE = ROOT / "simak" / "thresholds.json"
DEFAULT_THRESHOLDS = {
    "theta_e": 0.03,   # δ maksimum antara dua ekstraksi (pers. 2)
    "epsilon": 0.02,   # toleransi klaim relatif terhadap rentang (pers. 5)
    "rho": 0.10,       # ambang relatif label tren (pers. 3–4)
    "locked": False,
}


def thresholds() -> dict:
    if THRESHOLDS_FILE.exists():
        return {**DEFAULT_THRESHOLDS, **json.loads(THRESHOLDS_FILE.read_text())}
    return dict(DEFAULT_THRESHOLDS)


def java_bin() -> str:
    for base in (Path(r"C:\Program Files\Eclipse Adoptium"), Path(r"C:\Program Files\Java")):
        if base.exists():
            for jdk in sorted(base.iterdir(), reverse=True):
                exe = jdk / "bin" / "java.exe"
                if exe.exists():
                    return str(exe)
    return "java"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]
