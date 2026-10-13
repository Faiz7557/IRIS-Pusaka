"""Suara sintetis 'Satya' untuk mode dengar (dengan izin pemilik suara).

Alur: teks → normalisasi angka ke kata → suara dasar Indonesia neural (edge-tts, Ardi)
→ warna suara diubah ke suara referensi dengan konverter OpenVoice V2 (berjalan lokal di CPU).
Rekaman referensi tidak dikirim ke layanan luar; hanya teks yang dikirim ke layanan TTS dasar.
"""
import asyncio
import hashlib
import re
import subprocess
import sys
import types
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


def synthesize(text: str, speaker: str = "satya", rate: str = "+0%", pitch: str = "+0Hz", tau: float = 0.3) -> Path:
    """Teks → berkas MP3 dengan suara speaker; hasil di-cache menurut isi dan pengaturan."""
    spoken = normalize(text)
    base = SPEAKER_BASE.get(speaker, "ardi")
    key = hashlib.sha256(f"{speaker}|{base}|{rate}|{pitch}|{tau}|{spoken}".encode()).hexdigest()[:20]
    out = AUDIO / f"{key}.mp3"
    if out.exists():
        return out
    tmp = AUDIO / f"{key}_base"
    asyncio.run(_edge(spoken, tmp.with_suffix(".mp3"), rate, pitch, base))
    if speaker in BASE_VOICES:
        tmp.with_suffix(".mp3").rename(out)
        return out
    _wav(tmp.with_suffix(".mp3"), tmp.with_suffix(".wav"))
    conv_wav = AUDIO / f"{key}_conv.wav"
    _converter().convert(audio_src_path=str(tmp.with_suffix(".wav")), src_se=_base_se(base),
                         tgt_se=speaker_embedding(speaker), output_path=str(conv_wav), tau=tau)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(conv_wav), "-b:a", "96k", str(out)], check=True)
    for p in (tmp.with_suffix(".mp3"), tmp.with_suffix(".wav"), conv_wav):
        p.unlink(missing_ok=True)
    return out
