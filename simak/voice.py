"""Suara server opsional untuk mode dengar. Suara bawaan adalah Web Speech API di peramban (id-ID).

Yang dipakai server: ElevenLabs (`synthesize`, suara klon dengan izin pemilik), hanya bila
ELEVENLABS_API_KEY dan ELEVENLABS_VOICE_ID diatur; teks yang dibacakan dikirim ke ElevenLabs.
Jalur lama edge-tts + konverter OpenVoice V2 masih ada di modul ini tetapi tidak dipanggil aplikasi
(dependensinya di requirements-suara.txt).
"""
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import types
import urllib.error
import urllib.request
from pathlib import Path

from .config import CACHE, ROOT

VOICE_DIR = ROOT / "data" / "voice"
OV_DIR = ROOT / "tools" / "OpenVoice"
OV_CKPT = ROOT / "tools" / "ov_ckpt" / "converter"
AUDIO = CACHE / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)
# Suara dasar per penutur: pilih yang jenis suaranya sama dengan rekaman referensi,
# karena konverter hanya mengganti warna suara, bukan resonansi dan gaya bicara.
BASE_VOICES = {"ardi": "id-ID-ArdiNeural", "gadis": "id-ID-GadisNeural"}
SPEAKER_BASE = {"satya": "gadis", "ardi": "ardi", "gadis": "gadis"}

# ------------------------------------------------------------------ angka → kata (bahasa Indonesia)
_SATUAN = ["nol", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan", "sepuluh", "sebelas"]


def terbilang(n: int) -> str:
    if n < 0:
        return "minus " + terbilang(-n)
    if n < 12:
        return _SATUAN[n]
    if n < 20:
        return _SATUAN[n - 10] + " belas"
    if n < 100:
        return _SATUAN[n // 10] + " puluh" + ("" if n % 10 == 0 else " " + _SATUAN[n % 10])
    if n < 200:
        return "seratus" + ("" if n == 100 else " " + terbilang(n - 100))
    if n < 1000:
        return _SATUAN[n // 100] + " ratus" + ("" if n % 100 == 0 else " " + terbilang(n % 100))
    if n < 2000:
        return "seribu" + ("" if n == 1000 else " " + terbilang(n - 1000))
    for unit, name in ((10 ** 12, "triliun"), (10 ** 9, "miliar"), (10 ** 6, "juta"), (1000, "ribu")):
        if n >= unit:
            head, rest = divmod(n, unit)
            return terbilang(head) + " " + name + ("" if rest == 0 else " " + terbilang(rest))
    return str(n)


_NUM = re.compile(r"(?<![\w])(-?\d{1,3}(?:\.\d{3})+(?:,\d+)?|-?\d+(?:,\d+)?)(?![\w])")


def _say_number(tok: str) -> str:
    neg = tok.startswith("-")
    tok = tok.lstrip("-")
    whole, _, frac = tok.replace(".", "").partition(",")
    out = terbilang(int(whole))
    if frac:
        out += " koma " + " ".join(_SATUAN[int(d)] for d in frac)
    return ("minus " if neg else "") + out


def normalize(text: str) -> str:
    """Siapkan teks untuk diucapkan: angka menjadi kata, satuan umum dieja."""
    text = text.replace("%", " persen").replace("“", "").replace("”", "").replace("·", ",")
    text = re.sub(r"\s*\(([^)]*)\)", r", \1", text)
    text = _NUM.sub(lambda m: _say_number(m.group(1)), text)
    text = re.sub(r"\s*,\s*(,\s*)+", ", ", text)
    return re.sub(r"\s+([,.;])", r"\1", text)


# ------------------------------------------------------------------ OpenVoice (konverter saja)
_conv = None
_se = {}


def _converter():
    global _conv
    if _conv is None:
        if str(OV_DIR) not in sys.path:
            sys.path.insert(0, str(OV_DIR))
        # Bagian teks OpenVoice (fonemisasi Inggris/Mandarin) tidak dipakai; cegah impor dependensinya.
        stub = types.ModuleType("openvoice.text")
        stub.text_to_sequence = lambda *a, **k: []
        sys.modules.setdefault("openvoice.text", stub)
        # Watermark wavmark tidak dipakai (pustakanya tidak terpasang); sebagai gantinya audio diberi
        # label "suara sintetis" secara terbuka di antarmuka.
        wm = types.ModuleType("wavmark")
        wm.load_model = lambda: types.SimpleNamespace(to=lambda device: None)
        sys.modules.setdefault("wavmark", wm)
        from openvoice.api import ToneColorConverter
        _conv = ToneColorConverter(str(OV_CKPT / "config.json"), device="cpu")
        _conv.load_ckpt(str(OV_CKPT / "checkpoint.pth"))
    return _conv


def _wav(src: Path, dst: Path, sr: int = 22050):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(sr), str(dst)], check=True)


def _chunks(wav: Path, prefix: str, seconds: int = 8) -> list[str]:
    """Potong rekaman menjadi beberapa bagian agar warna suara dirata-rata dari banyak potongan."""
    import soundfile as sf
    data, sr = sf.read(str(wav))
    n = seconds * sr
    paths = []
    for i in range(0, max(len(data) - sr * 3, 1), n):
        p = wav.parent / f"{prefix}_{i // n:02d}.wav"
        sf.write(str(p), data[i:i + n], sr)
        paths.append(str(p))
    return paths


def speaker_embedding(name: str, ref_audio: Path | None = None):
    """Ciri warna suara (tone color) dari rekaman referensi; disimpan agar tidak dihitung ulang."""
    import torch
    if name in _se:
        return _se[name]
    se_path = VOICE_DIR / f"{name}_se.pth"
    if se_path.exists():
        _se[name] = torch.load(se_path, map_location="cpu")
        return _se[name]
    work = VOICE_DIR / f"{name}_work"
    work.mkdir(parents=True, exist_ok=True)
    wav = work / "ref.wav"
    _wav(ref_audio, wav)
    _se[name] = _converter().extract_se(_chunks(wav, "ref"), se_save_path=str(se_path))
    return _se[name]


BASE_SAMPLE = ("Selamat datang di SIMAK. Materi kuliah ini dibacakan untuk mahasiswa. Grafik batang menunjukkan "
               "jumlah mahasiswa baru per fakultas. Nilai tertinggi pada Kedokteran, yaitu delapan ratus tiga orang, "
               "dan terendah pada Psikologi. Secara keseluruhan tren naik dari tahun ke tahun. Tabel berikut "
               "merangkum hasil kuis mingguan. Gunakan tabel ini untuk berlatih menghitung rerata.")


async def _edge(text: str, out: Path, rate: str = "+0%", pitch: str = "+0Hz", base: str = "ardi"):
    import edge_tts
    await edge_tts.Communicate(text, BASE_VOICES[base], rate=rate, pitch=pitch).save(str(out))


def _base_se(base: str = "ardi"):
    if "_base_" + base in _se:
        return _se["_base_" + base]
    se_path = VOICE_DIR / f"base_{base}_se.pth"
    if not se_path.exists():
        work = VOICE_DIR / f"base_{base}_work"
        work.mkdir(parents=True, exist_ok=True)
        mp3 = work / "base.mp3"
        asyncio.run(_edge(BASE_SAMPLE, mp3, base=base))
        wav = work / "base.wav"
        _wav(mp3, wav)
        _converter().extract_se(_chunks(wav, "base"), se_save_path=str(se_path))
    import torch
    _se["_base_" + base] = torch.load(se_path, map_location="cpu")
    return _se["_base_" + base]


# ------------------------------------------------------------------ suara manusia (ElevenLabs, berbayar)
# Suara hasil kloning/pelatihan dari rekaman manusia (dengan izin pemiliknya) di akun ElevenLabs sendiri.
# Key dan voice id dibaca dari environment variable; teks yang dibacakan dikirim ke layanan ElevenLabs.
ELEVEN_SPEAKER = "eleven"
PAID_SPEAKERS = {ELEVEN_SPEAKER}  # dipakai server agar tidak membuat audio massal di latar belakang
ELEVEN_MODEL = os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")


def eleven_ready() -> bool:
    return bool(os.environ.get("ELEVENLABS_API_KEY") and os.environ.get("ELEVENLABS_VOICE_ID"))


def _eleven(text: str, out: Path, rate: str):
    if not eleven_ready():
        raise RuntimeError("ELEVENLABS_API_KEY dan ELEVENLABS_VOICE_ID belum diatur")
    speed = max(0.7, min(1.2, 1 + int(rate.rstrip("%")) / 100))
    body = json.dumps({"text": text, "model_id": ELEVEN_MODEL,
                       "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": speed}})
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{os.environ['ELEVENLABS_VOICE_ID']}?output_format=mp3_44100_128",
        data=body.encode(), method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
    except urllib.error.HTTPError as e:  # ke log server saja, tanpa key
        print("ElevenLabs gagal:", e.code, e.read()[:300].decode("utf-8", "replace"))
        raise


def synthesize(text: str, speaker: str = ELEVEN_SPEAKER, rate: str = "+0%", pitch: str = "+0Hz", tau: float = 0.3) -> Path:
    """Teks → berkas MP3 dengan suara ElevenLabs; hasil di-cache menurut isi dan pengaturan."""
    spoken = normalize(text)
    if speaker == ELEVEN_SPEAKER:
        key = hashlib.sha256(f"{speaker}|{ELEVEN_MODEL}|{os.environ.get('ELEVENLABS_VOICE_ID')}|{rate}|{spoken}".encode()).hexdigest()[:20]
        out = AUDIO / f"{key}.mp3"
        if not out.exists():
            _eleven(spoken, out, rate)
        return out
    raise ValueError(f"Sumber suara tidak didukung: {speaker}")
