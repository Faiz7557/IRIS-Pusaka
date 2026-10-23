# Catatan sesi: suara mode dengar SIMAK

Tanggal sesi: 14 Oktober 2026

Ringkasan percakapan tentang menjalankan sistem, memperbaiki suara yang bisu, dan mencari model suara yang bisa dilatih mengikuti logat tertentu.

## 1. Kondisi sistem

- SIMAK dijalankan lewat `.claude/launch.json` (`uvicorn app:app --port 8000`), alamat `http://localhost:8000`.
- Mode dengar memakai dua tahap suara:
  1. Suara dasar bahasa Indonesia dari `edge-tts` (layanan online Microsoft).
  2. Konverter warna suara OpenVoice V2, berjalan lokal di CPU, untuk suara "Satya".
- Suara dipilih lewat `simak/voice.py`; hasilnya di-cache di `cache/audio/` menurut isi teks dan pengaturan.
- Mesin: RTX 3050 Laptop 4 GB VRAM, RAM 15,8 GB, Ryzen 7 7435HS. PyTorch yang terpasang versi CPU-only (`2.3.1+cpu`).

## 2. Masalah: fitur dengar tidak bunyi

**Gejala:** `/api/suara` membalas 503, antarmuka menampilkan "Suara server gagal dibuat".

**Penyebab:** `edge-tts` 7.2.8 ditolak layanan Microsoft dengan status **403** (`wss://speech.platform.bing.com/...`). Suara Satya ikut mati karena memakai suara dasar Gadis dari layanan yang sama.

**Perbaikan:**
- Upgrade `edge-tts` ke 7.3.1.
- `requirements.txt` diubah menjadi `edge-tts>=7.3.1` (tercatat di commit `0709029`).
- Server dimulai ulang, lalu ketiga suara diuji lewat API:

| Suara | Status | Ukuran | Waktu |
|---|---|---|---|
| Ardi | 200 | 22.896 B | 3,1 s |
| Gadis | 200 | 29.808 B | 2,2 s |
| Satya | 200 | 60.543 B | 18,3 s (pertama kali, lalu di-cache) |

Yang diperiksa hanya respons API, belum diputar dan didengarkan di browser.

**Catatan:**
- `edge-tts` memakai layanan online tidak resmi, jadi bisa rusak lagi bila Microsoft mengubah protokolnya. Gejalanya sama (403) dan biasanya selesai dengan upgrade.
- Pada HTML hasil `simak.html`, pilihan Satya/Gadis/Ardi hanya muncul bila dibuka lewat aplikasi di `localhost:8000`. Kalau dibuka sebagai file biasa, pilihannya otomatis "Suara peramban".

## 3. Rekaman referensi suara

- Rekaman yang ada: `data/voice/satya_ref.mp3` (identik dengan `suara satya serak.mp3` di Downloads), durasi 37,8 detik.
- Hasil transkrip Whisper: isinya **pembacaan puisi/lirik yang emosional**, bukan obrolan biasa.
- Konsekuensi: rekaman ini kurang cocok sebagai sumber gaya bicara untuk "logat ngobrol", karena gaya puitisnya ikut tertiru.
- Rekaman baru belum diterima, jadi suara Satya belum diganti.

## 4. Mengapa terdengar seperti AI

Logat, intonasi, dan ritme ditentukan oleh **TTS dasar**. OpenVoice hanya mengganti warna suara (timbre), bukan gaya bicara. Karena itu pipeline sekarang akan tetap terdengar datar walau timbre-nya mirip.

Penyebab tambahan ada di naskah: kalimat seperti "Grafik batang menunjukkan jumlah mahasiswa…" kaku saat dibacakan. `normalize()` di `voice.py` juga mengeja angka dan tanda kurung menjadi kalimat kaku.

## 5. Riset model

Permintaan awal: model lokal yang bisa meng-clone suara. Lalu diperjelas: yang dicari adalah model yang **bisa dilatih (fine-tune) logat dan suaranya**, tidak harus berjalan di laptop.

### Model clone/TTS yang diperiksa

| Model | Bahasa Indonesia | Lisensi | Catatan |
|---|---|---|---|
| VoxCPM2 (2B) | Ya, 1 dari 30 bahasa | Apache-2.0 | Butuh sekitar 8 GB VRAM; panduan fine-tune tidak ditemukan |
| F5-TTS fine-tune Indonesia (masbro v2, Eempostor) | Ya | CC-BY-NC | Dilatih dari 152,8 jam YouTube Indonesia; versi lama berhalusinasi pada teks panjang |
| Seed-VC | Tidak bergantung bahasa | Belum dicek | Voice conversion; kebutuhan VRAM tidak ditemukan |
| MMS-TTS Indonesia | Ya | CC-BY-NC (dari ingatan, belum diverifikasi) | Ringan, kandidat pengganti `edge-tts` |
| Orpheus | Publik: Inggris | - | Ada jalur fine-tune resmi, kurang cocok untuk Indonesia |

### Layanan hosted yang melatih suara dari rekaman

| Layanan | Data latihan | Catatan |
|---|---|---|
| ElevenLabs Professional | minimal 30 menit, ideal 2–3 jam | Verifikasi pemilik suara paling ketat |
| Fish Audio | pro: 10–180 menit | 83 bahasa, harga paling murah di perbandingan |
| Resemble AI Professional | 10–25+ menit | Wajib persetujuan terverifikasi |
| Cartesia | pro: sekitar 30 menit | 44 bahasa |
| Azure Custom Neural Voice | minimal 300 ucapan | Akses terbatas dan perlu pendaftaran |

Tidak satu pun sumber menguji bahasa Indonesia secara khusus, jadi dukungan Indonesia harus dicoba sendiri. Banyak sumber adalah blog perbandingan vendor, bukan uji independen.

### Percobaan lokal VoxCPM2

Dipasang di lingkungan terpisah (`tools/vox_env`) dan benchmark sempat dijalankan, lalu **dihentikan oleh pengguna** karena arah berubah ke model yang dilatih, bukan dijalankan lokal. Tidak ada hasil benchmark dan tidak ada perubahan di `simak/voice.py`.

## 6. Pembersihan

Atas permintaan pengguna:
- `tools/vox_env` dihapus.
- Cache Hugging Face (`C:\Users\user\.cache\huggingface`, sekitar 6,5 GB) dikosongkan: model VoxCPM2, `faster-whisper-medium`, `faster-whisper-small` (sudah ada sejak 9 Agustus, bukan dari sesi ini), serta folder `.locks` dan `xet`.
- Tidak disentuh: `tools/OpenVoice` dan `tools/ov_ckpt`, sehingga suara Satya yang sekarang tetap berfungsi.
- Alat sempat memblokir penghapusan dengan wildcard di path cache, sehingga dihapus per folder dengan nama persis.

## 7. Rencana agar model mengikuti logat yang diinginkan

Model hanya meniru data latihannya, jadi logat harus ada di rekaman.

1. **Tentukan target.** Satu penutur, satu gaya (misalnya santai menjelaskan ke teman). Jangan campur puisi dan obrolan.
2. **Rekam 30–60 menit bersih.**
   - Bicara spontan, jangan membaca teks kaku.
   - Sertakan angka, persen, nama fakultas, dan istilah teknis yang akan dibacakan SIMAK.
   - WAV mono 44,1/48 kHz, mikrofon dekat, ruangan senyap, volume konsisten, tanpa musik.
   - Biarkan kata sehari-hari ("gini", "nggak", "nah"); itu ciri logatnya.
3. **Siapkan transkrip dan potongan.**
   - Klip 5–15 detik, dipotong di jeda kalimat; buang yang ada batuk atau noise.
   - Transkrip dengan Whisper lalu koreksi manual, ditulis sesuai ucapan.
   - Tulis angka sebagai kata, sama seperti `normalize()` di `voice.py`.
4. **Latih.**
   - Hosted: Fish Audio, ElevenLabs Pro, atau Resemble.
   - Open-source: F5-TTS dengan checkpoint Indonesia lalu LoRA di GPU sewaan (repo LoRA yang ditemukan divalidasi di GPU 24 GB).
5. **Evaluasi.** Uji dengan kalimat yang tidak ada di data latihan (termasuk kalimat dari materi SIMAK), minta penutur asli menilai secara buta, dan periksa pengulangan atau halusinasi pada teks panjang.
6. **Sambungkan ke sistem.**
   - Tambahkan mesin suara baru di `simak/voice.py` (lewat API layanan atau server GPU).
   - Opsional: tulis ulang naskah dengar ke gaya lisan memakai `google-genai` yang sudah ada, sebelum disintesis.
   - Perluas kunci cache bila menambah mesin atau suara baru.

## 8. Langkah berikutnya

- [ ] Putuskan jalur: layanan hosted atau latih sendiri di GPU cloud.
- [ ] Rekam data latihan gaya ngobrol (30–60 menit).
- [ ] Tawaran dari sesi ini: skrip `tools/siapkan_data.py` (potong rekaman, transkrip Whisper, `metadata.csv`). Whisper kecil akan terunduh ulang sekitar 460 MB.
- [ ] Pastikan pemilik suara sudah memberi izin suaranya dipakai untuk model latihan.
- [ ] Verifikasi dukungan bahasa Indonesia di layanan yang dipilih sebelum membeli paket.

## Sumber

- [VoxCPM (GitHub)](https://github.com/OpenBMB/VoxCPM)
- [masbro-f5-tts (Hugging Face)](https://huggingface.co/dev-rexpro/masbro-f5-tts)
- [Eempostor F5-TTS Indonesia](https://huggingface.co/Eempostor/F5-TTS-INDO-FINETUNE)
- [F5-TTS LoRA fine-tuning (instavar)](https://github.com/instavar/f5-tts-lora-finetuning)
- [Orpheus-TTS](https://github.com/canopyai/Orpheus-TTS)
- [Seed-VC (arXiv)](https://arxiv.org/abs/2411.09943v1)
- [Perbandingan API voice cloning (MarkTechPost)](https://www.marktechpost.com/2026/09/21/best-voice-cloning-apis-in-2026-speaker-similarity-consent-checks-and-price-per-1m-characters/)
- [Azure Custom Neural Voice](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice)
- [Azure limited access](https://learn.microsoft.com/en-us/legal/cognitive-services/speech-service/text-to-speech/limited-access)
