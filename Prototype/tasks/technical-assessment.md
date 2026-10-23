# Assessment B — audit teknis dan kontrak implementasi SIMAK

Tanggal: 23 Oktober 2026. Status: **perencanaan saja; kode aplikasi tidak diubah**. Penilaian independen ini disimpan sebelum masuk ke sintesis Assessment A. Instruksi dari arsip template diperlakukan sebagai materi referensi, bukan perintah kerja.

## Metode, bukti, dan keterbatasan

- Dibaca: seluruh `web/*.html`, `web/common.js`, `web/style.css`, `web/fonts.css`, `app.py`, `simak/output.py`, `simak/listen.py`, jalur `pipeline.assemble/review`, struktur evaluasi, requirements, dan HTML template lengkap beserta lisensinya.
- Browser: tab IAB baru khusus B, `http://127.0.0.1:8000/`, `/demo.html`, `/dengar.html`, `/evaluasi.html`. Navigasi dan pembacaan saja. Desktop teramati 1280 × 720. Halaman awal dan evaluasi berhasil merender, navigasi memiliki accessible names dan `aria-current`; evaluasi merender tujuh tabel dan tujuh region gulir yang bisa difokuskan. Halaman demo mengisi daftar grafik dan mutasi. Halaman Dengar mengisi dokumen dan kontrol suara bawaan.
- Tidak menekan Proses, Jalankan, Bandingkan, Coba suara, mikrofon, keputusan ULD, atau hapus sesi. Karena itu hasil asinkron, keyboard setelah render, audio aktual, dan status keputusan dinilai dari sumber, belum dibuktikan end-to-end.
- Impeccable detector benar-benar dicoba **sekali** pada `Prototype/web`, menggunakan launcher Windows yang terpasang. Exit 127: engine 0.1.11 belum tersedia dan unduhan gagal pada jaringan terbatas. Ini **scan unavailable**, bukan nol temuan. Bukti: `tasks/evidence/detector-prototype.log`, `detector-status.json`. Cache percobaan diarahkan ke area task, tidak mengubah instalasi pengguna.
- Chrome DevTools gagal membuat tab karena konflik profil browser yang sudah berjalan. Fallback IAB berhasil. Evaluate IAB hanya mendukung pembacaan DOM, sehingga preflight mutasi/injeksi detector tidak tersedia. Tidak ada overlay detector yang andal; tidak memulai live server detector.
- Shell HTTP localhost ditolak izin socket; bukti gagal tercatat `http-readonly.json`. Keberhasilan browser tidak berarti shell HTTP berhasil.
- Inventaris parser HTML lokal ada di `source-contract-inventory.json`; perhitungan kontras sRGB ada di `contrast-srgb.json`. Inventaris HTML hanya merekam markup statis, tidak menggantikan DOM yang dihasilkan JavaScript.
- Belum ada pengukuran Lighthouse, Core Web Vitals, NVDA, TalkBack, VoiceOver, perangkat fisik, zoom 200/400%, synthesized touch, atau viewport mobile dalam B. Jangan menyebut hasil ini sertifikasi WCAG atau audit performa produksi.

## Kesimpulan teknis

Perombakan paling kecil yang lengkap tetap menggunakan **FastAPI + halaman HTML + CSS + JavaScript vanilla**. Template merupakan satu dokumen HTML 96.333 byte, 1.388 baris, tanpa build step; SIMAK juga tidak mempunyai frontend package.json atau bundler. Memindahkan ke React/Next/Tailwind tidak diperlukan untuk memenuhi permintaan UI dan menambah risiko pada input PDF, status, audio, dan keluaran HTML mandiri.

Adopsi template sebagai **sumber bahasa visual**, lalu implementasikan ulang komposisi yang relevan di sistem SIMAK. Hindari menempel seluruh HTML, GSAP/Lenis, booking form, foto kucing, atau dua belas bagian marketing ke workspace operasional. Lisensi template MIT menyatakan notice copyright/permission harus ikut pada salinan substansial; simpan notice pada direktori third-party jika memakai potongan kode. Foto mempunyai lisensi terpisah dan tidak dibutuhkan dalam produk ini.

Skor teknis sementara berbasis sumber dan baseline desktop: aksesibilitas 2/4; performa 3/4; responsivitas 2/4; theming 2/4; integritas implementasi 3/4 = **12/20, significant improvements needed**. Skor responsivitas belum divalidasi perangkat/mobile; score 4 tidak dapat diberikan tanpa pengujian tersebut. Detector unavailable tidak diperlakukan sebagai lulus.

## Temuan prioritas terverifikasi

### [P1] Recovery operasi asinkron belum lengkap

Lokasi: `web/index.html:126–160`, `245–259`; `web/demo.html:115–131`, `172–185`; `web/dengar.html:185–209`; `web/evaluasi.html:56–102`.

Kode memeriksa `r.ok` pada beberapa POST tetapi tidak membungkus penolakan jaringan/JSON dengan catch/finally. Akibat inferensi yang kuat dari kontrol alur: jaringan putus saat review dapat meninggalkan empat tombol disabled; demo/Dengar dapat tetap busy; daftar contoh atau evaluasi bisa kosong tanpa jalur coba lagi. `index.html` juga memakai JID global dan membiarkan pemicu proses dipakai kembali saat polling; respons/poll lama berpotensi bersaing dengan sesi baru.

Rencana: sediakan state loading/success/empty/error yang jelas; tangkap kegagalan transport dan JSON; selalu kembalikan enable state; satu operasi pemrosesan aktif per halaman; identifikasi request/job lokal saat polling agar respons lama tidak mengganti hasil baru; retry eksplisit yang mempertahankan pilihan/teks. Jangan mengarang persen kemajuan bila API hanya menyediakan `tahap/pesan`.

### [P1] Fokus keyboard rentan hilang saat render ulang

Lokasi: `web/dengar.html:133–158` (`Player.render` mengganti `bar.innerHTML` pada play dan tiap segmen); `web/index.html:205–209` (klik mengganti list yang memuat tombol pemicu); `web/index.html:225–259` (review mengganti detail dan hasil). Ini temuan sumber, belum diuji interaksi live.

Dampak: tombol yang sedang difokuskan bisa terlepas dari DOM sehingga pengguna keyboard/screen reader kehilangan tempat kerja. `aria-live` bukan pengganti manajemen fokus; live region seluruh detail juga berpotensi terlalu banyak mengumumkan.

Rencana: update label/state kontrol pemutar pada node tetap; pada selection arahkan fokus secara sengaja ke heading detail `tabindex=-1` atau pertahankan fokus list menurut pola yang dipilih; setelah keputusan arahkan ke status/elemen berikut yang eksplisit; simpan textarea saat error; pakai live region status ringkas. Pertahankan semantic `<button>` dan `aria-pressed/current`, bukan menggantinya menjadi kartu div klik.

### [P1] Kontrak keselamatan konten harus ikut bahasa visual baru

Lokasi: `web/common.js:58–75`; `web/index.html:163–259`; `simak/pipeline.py:193–207`, `262–307`; `simak/output.py:106–165`; `simak/listen.py:47–114`.

Enam status mempunyai arti produk berbeda. Dekoratif mengosongkan alt; antrean dan ditolak tidak boleh dibacakan sebagai deskripsi terverifikasi; setujui/ubah menghasilkan `alt_final`; PDF serta HTML dirakit ulang setelah review. `assemble` masih dapat menahan figur karena pasangan halaman tidak cocok. Warna baru harus mengomunikasikan status secara konsisten, tetapi nama, ikatan data, teks penanda, dan mekanisme fail-closed tidak boleh hilang.

Rencana: pisahkan warna **brand/dekorasi** dari **success/held/error**. Misalnya orange boleh menjadi CTA, tetapi kartu orange tidak boleh otomatis berarti ditahan. Semua status tetap memakai teks + ikon/border, bukan warna tunggal. Pertahankan identitas elemen `e.id`, halaman, alasan, tabel T1/T2, dan hubungan klaim-ke-baris.

### [P1] Copy retensi dan hapus sesi perlu selaras perilaku nyata

Lokasi: `web/index.html:66`, `190–191`; `app.py:27–36`, `157–162`.

UI menjanjikan dihapus setelah enam jam, tetapi `_cleanup()` terlihat hanya dipanggil saat modul aplikasi dimuat; tidak ada scheduler pembersih berkala pada kode yang diperiksa. Hapus sesi langsung DELETE dan reload tanpa recovery/error handling. Jangan memperbesar janji privasi melalui redesign.

Rencana: sebelum implementasi, pilih mengoreksi copy agar sesuai cleanup yang tersedia atau memperbaiki retensi sebagai pekerjaan terpisah yang teruji. Untuk hapus sesi, tampilkan dampak konkret dan aksi batal/lanjut pada UI; jangan memanggil DELETE ketika sekadar menutup panel atau kembali. Jangan menjanjikan undo jika backend tidak memiliki trash/restore. B tidak melakukan penghapusan apa pun.

### [P2] Dukungan motion dan tema belum seragam antarsurface

Lokasi: `web/style.css:5–46`, `161–167`, `232–233`; `simak/output.py:14–18`, `50`, `64`; `web/dengar.html:145`.

UI memiliki tokens dan fokus jelas, serta mematikan stamp animation/transition ketika reduced motion. Spinner `.status.busy::before` didefinisikan kemudian dan animasi spin tidak dimatikan oleh aturan yang hanya menonaktifkan transition. Reader keluaran mendukung prefers-color-scheme dark, workspace tidak. Ini bukan kewajiban menambahkan tombol tema; yang penting keputusan konsisten.

Rencana: reduced-motion menggunakan indikator status statis dengan teks progress; hindari scroll halus paksa. Tentukan light-first workspace dan reader tetap menghormati preferensi sistem, atau satu strategi tema yang sengaja diuji. Jangan menambahkan dark switch baru tanpa kebutuhan.

### [P2] Kontras palette template harus berdasarkan pasangan peran

Lokasi template: `index.html:75–90`, `128–163`. Perhitungan sRGB, bukan pembuktian composite screenshot:

| Pasangan | Rasio | Teks normal AA |
|---|---:|---|
| Orange #cf6224 / ink #0b0a0a | 5,109:1 | Lulus |
| Orange #cf6224 / paper #f4f1ee | 3,440:1 | Gagal |
| Purple #5a3cd4 / paper #f4f1ee | 6,156:1 | Lulus |
| Green SIMAK #1F4D3A / #EEF4F0 | 8,636:1 | Lulus |
| Muted SIMAK #47524C / #F3F6F4 | 7,483:1 | Lulus |

Orange template bukan warna teks kecil yang aman di atas paper, dan paper text kecil di atas orange juga gagal. Pakai orange dengan ink gelap atau sebagai dekorasi noninformasi; buat token orange-ink lebih gelap untuk link di paper jika dibutuhkan. Rasio dihitung dengan fungsi sRGB yang memeriksa pasangan hitam/putih = 21:1; seluruh pasangan ada di evidence JSON. Tidak mengklaim template memakai pasangan gagal pada semua tempat; ini constraint adaptasi.

### [P2] Pemutar dan baris transkrip perlu semantik/states yang lebih kuat

Lokasi: `web/dengar.html:133–174`, `web/common.js:131–205`, `simak/output.py:54–81`.

Baris transkrip `li tabindex=0` menerima Enter/Space namun tidak memiliki peran kontrol interaktif. Player menampilkan i+1/length sehingga saat selesai i==length hasil bisa melebihi total; daftar kosong juga menghasilkan 1/0. Audio mempunyai error text, tetapi kondisi tidak ada voice id-ID dan unavailable speech perlu terlihat sebelum aksi utama. Kegagalan voice jangan menghilangkan transkrip.

Rencana: gunakan button di dalam li atau role/state lengkap bila struktur lama dipertahankan; nyatakan bagian aktif; disable prev/next di batas; finished/empty state benar; label Pause/Resume sesuai perilaku yang sebenarnya (saat ini pemutaran ulang segmen, bukan melanjutkan posisi audio); no-voice fallback menuju transkrip. Pertahankan pengaturan lokal dan batas kirim paid TTS.

## Hal yang sudah kuat dan harus dipertahankan

- Font Atkinson Hyperlegible Next/Mono sudah self-hosted, `font-display:swap`, dengan fallback system dan unicode-range (`web/fonts.css:1–54`). Tidak memerlukan font pihak ketiga saat presentasi offline.
- Keempat halaman memakai `lang=id`, viewport, skip link, main, label kontrol, live region status. Fokus 3px dan minimum tinggi tombol/select 44px tersedia (`style.css:57`, `198`, `214`). Desktop DOM yang diperiksa sesuai.
- Kontras foreground teks utama/sekunder/status yang dihitung baik; jangan menghapus legibilitas untuk meniru template.
- Navigasi bersama mempunyai `aria-current=page`, kata label, dan ikon dekoratif; claim interaction mendukung click, focus, Enter, Space dan CSS.escape (`common.js:107–117`).
- Evaluasi menjaga caption, scope header, Wilson CI, data run, dan disclosure manifesto; region horizontal scroll diberi label/tabindex (`evaluasi.html:100–102`).
- HTML keluaran menyematkan font, gambar base64, CSS, JS; body dokumen tetap terbaca tanpa API server. Mode dengar lokal default dan ElevenLabs hanya ditawarkan saat server siap (`output.py:8–11`, `54–81`).
- `listen.original` menyatakan **simulasi pembacaan PDF**, bukan rekaman NVDA; UI Dengar mempunyai disclaimer eksplisit (`dengar.html:94`). Kejujuran ini tidak boleh dihapus demi narasi before/after.

## Template: dependensi, fallback, dan bagian yang tidak boleh dicopy mentah

| Area template | Bukti sumber | Keputusan teknis yang disarankan |
|---|---|---|
| Tokens/CSS layers/typography | 75–177; tokens/base/atoms/layout/sections/scenes | Ambil struktur token dan komposisi; gunakan nama peran SIMAK, jangan impor seluruh namespace generik `m-*`/`color-1..10`. |
| External fonts | 21–67 | Gabarito, Rethink Sans, Playwrite berasal fonts.gstatic.com. Body reader/transkrip tetap Atkinson. Display font bersifat opsional dan harus self-hosted dengan license bila dipilih. |
| 30 img, 29 lazy | HTML parser inventory | Bukan 30 request unik: enam pane courtyard memakai URL sama dan browser dapat cache. Sebagian besar foto tidak relevan. Gunakan grafik/SIMAK preview yang sudah tersedia, bukan remote Unsplash untuk workspace. |
| Hero | 241–256; 609–674 | Komposisi berwarna dan tipografi besar bisa diterapkan pada pengantar; looping pan/sway dekoratif dan twelve-window cat facade tidak diperlukan. |
| Navigation overlay | 587–605; 1048–1082 | Label, expanded state, Escape, fokus link pertama/return ke toggle sudah ada. Overlay belum terlihat mempunyai focus trap atau background inert; jika pola modal dipakai, lengkapi dan uji. Navigasi operasional sebaiknya tetap mudah ditemukan. |
| Contact form | 987–998; 1094–1104 | Placeholder action=#; JS hanya checkValidity, tampilkan sukses, lalu reset. Tidak mengirim booking sungguhan. Jangan gunakan form ini untuk unggah/proses atau notifikasi sukses SIMAK. |
| GSAP/ScrollTrigger/SplitText/Lenis | 1106–1109 | Empat script CDN pinned, tanpa build step. Tidak perlu ditambah untuk merombak UI; CSS state/focus/layout native cukup. |
| Motion guards | 1171; 1202–1227; 1242–1372 | Banyak scene dibatasi `prefers-reduced-motion:no-preference`, sebuah kekuatan. Hover transitions masih ada. Jangan menyimpulkan reduced motion tidak didukung sama sekali. |
| Horizontal pinned day scene | 375–385; 1292–1316 | Ketika motion aktif, stage pinned + track horizontal berdasarkan scroll. Cocok untuk storytelling pilihan; tidak cocok untuk review PDF, tabel bukti, atau navigasi yang harus cepat/keyboard-friendly. |
| Motion queue fallback | 1110–1163 | Queue memeriksa gsap dan dapat mengembalikan attribute mutation saat setup gagal. Tetapi page-init memanggil `gsap.registerPlugin` tanpa guard; jika CDN gagal akan ada error. Markup dasar/semantik sebagian besar tetap ada; jangan klaim blank total tanpa uji runtime. |
| Placeholder/fake product | metadata 18; contact 942–1013 | Replace branding, alamat, harga, booking, foto, OG preview, favicon hanya pada implementasi desain yang benar-benar dipilih; jangan memasukkan fitur booking palsu. |

## Peta perubahan, caller, selector, dan contract

### Shared shell dan komponen

`common.js` dimuat oleh index, demo, dengar, evaluasi. Call sites `renderRail` masing-masing ada pada index:120, demo:85, dengar:100, evaluasi:43. `renderRail` mengasumsikan `.rail` ada dan mengganti innerHTML; mengubah shell menjadi header tanpa memperbarui fungsi akan mematahkan semua halaman.

Shared selectors yang terikat perilaku: `.rail`, `.cl`, `.on`, `tr[data-row]`, `.speaking`, `#vc`, `#vc-btn`, `#vc-st`, `#rail-proof`, `#sr-live`, `#v-suara`, `#v-cepat`, `#v-coba`. Hook lain: `[data-claim]`, `[data-e]`, `[role=button]`, `button`, `a[href]`; voice commands membaca accessible name/text dari kontrol yang **terlihat** (`common.js:211–267`). Perubahan label tombol mengubah vocabulary perintah suara; dua tombol berlabel sama bisa menjadi ambigu.

Shared visual classes: `.shell`, `.rail`, `.wordmark`, `.nav`, `.card`, `.card-head`, `.card-body`, `.slip`, `.stamp` + `.fail/.hold/.pending`, `.verdict` + `.v-pub/.v-bad/.v-hold/.v-idle`, `.status/.busy`, `.ruled`, `.hide`, `.sr`, `.btn-primary/.btn-danger/.btn-quiet`, `.twrap`, `.halves`. Semua HTML memiliki inline CSS spesifik halaman; mengganti style.css saja tidak mencakup keseluruhan desain.

| Fungsi shared | Caller nyata | Yang dipertahankan |
|---|---|---|
| `renderRail`, `icon` | Seluruh 4 halaman | href, aria-current, icon decorative, microphone support detection. |
| `statusStamp` | index list | Mapping enam status; readable name. |
| `checkStamps`, `pressSlip` | index detail/action, demo show | cF/cδ/cA/cL, data source, reduced-motion feedback. |
| `segHtml`, `t1t2`, `bindClaims` | index detail, demo show | data-claim/data-e, normalized table row keys, keyboard source highlighting. |
| `announce` | index review/error, demo run/inject | polite live region ringkas, bukan visual-only toast. |
| `Voice` | Dengar controls, Player, sayOnce; VoiceCmd feedback guard | stop/cancel, id-ID preference, onend/onerror/onstart, optional paid path. |
| `VoiceCmd` | renderRail pada semua halaman | labels/visibility/disabled filtering; no auto permission acceptance dalam pengujian. |

### Per halaman

| Surface | IDs/hooks wajib dicakup saat markup berubah | State/contract |
|---|---|---|
| Remediasi `index.html` | isi, h-pilih, sampel, up, file, file-lbl, up-btn, prog, hasil, h-hasil, nama, pages, tally, vtrail, vera tbody, out, timing, els, detail/h-detail, alt, del, d-slip; `[data-s]`, `[data-f]`, `[data-id]`, `[data-a]` | JID/STATE/FILTER/SEL; sampel groups dev/uji/nyata; file FormData key=`file`; polling tahap; output links; image identity; four review actions. |
| Demo `demo.html` | isi, pick, run, reset, st, inj-lbl, mut, a-call/a-verdict/a-text/a-slip, b-call/b-verdict/b-reasons/b-text/b-slip/b-fk, legend, img-call/img-slot, score, truth, t12/t12-body; `[data-k]`, claim rows | CID/BASE/SCORE; B2 marks offsets/start/end; SIMAK seg/checks/reasons; seed and mutation kinds; baseline restore; source highlighting. |
| Dengar `dengar.html` | isi, doc, go, st, voice-ctl, stage, h-moment, m-call/m-img/m-before/m-after/m-play-a/m-play-s, tally, p-a/p-s, tr-a/tr-s; `.moment`, `.tr li`, `[data-a]`, `[data-on]` | DATA/JID/active; query `?job=`/`?doc=`; transcript kinds; serialized audio one active player; preferences localStorage. |
| Evaluasi `evaluasi.html` | isi, empty, res; dynamic h-G3/h-G1/h-G4/h-G6/h-man; `.twrap`, `.ci-in/.ci-col`, `.kn`, `.manifest` | immutable results json; G6 optional; D_ketat optional; absent data; table captions, percent vs ratio formatting, CI; jangan tulis angka marketing yang terpisah dari hasil. |
| HTML keluaran `output.py` | isi, play/pause/prev/next, voice/rate/st, `[data-say]`, `.speaking`, `.bar`, `.notice`, `.stamp`, `.s-ok/.s-hold` | `build_html(state, alt_for)` dipanggil `pipeline.assemble`; semua asset embedded; localhost voice optional; standalone path tetap bisa dibaca. Jangan import common.js yang mengharuskan rail. |

### API dan data yang sebaiknya tetap tanpa migrasi

| Endpoint | Consumer dan payload |
|---|---|
| GET `/api/sampel` | index loadSamples + Dengar loadDocs: array `{file,set}`. |
| POST `/api/sampel/{name}` | index sample + Dengar go: response `{id}`. Dapat memproses/VLM; belum dipanggil B. |
| POST `/api/unggah` | index submit: multipart `file`, response `{id}`. |
| GET `/api/pekerjaan/{jid}` | index/Dengar poll: `{tahap,pesan,nama,state}`; selesai/gagal vs intermediate. |
| GET `/api/pekerjaan/{jid}/dengar` | Dengar show: `{judul,berkas,asli,simak,ringkasan}`. |
| GET `/api/pekerjaan/{jid}/img/{el}` | list/detail/moment: PNG preview id stabil. |
| POST `/api/tinjau/{jid}/{el}` | index act: JSON `{aksi,alt}`; `aksi=setujui/ubah/tolak/dekoratif`; server validates empty description; rebuilds PDF/HTML. |
| DELETE `/api/pekerjaan/{jid}` | Hapus sesi, irreversible on current implementation. |
| GET `/keluaran/{jid}/simak.html`, `simak.pdf`, `asli.pdf` | output actions; retain target/rel and filenames. |
| GET `/api/demo/grafik`, `/api/demo/mutasi` | demo initial selectors; availability cached/labels. |
| POST `/api/demo/jalankan/{cid}`, `/api/demo/suntik/{cid}` | demo; mutation JSON `{jenis,seed}`. |
| GET `/api/grafik/{cid}.png` | demo image. |
| GET `/api/evaluasi` | evaluasi + shared rail proof; `{ada:false}` when missing. |
| GET `/api/suara/daftar` | shared controls + standalone reader; paid speaker only if configured. |
| POST `/api/suara` | optional audio JSON `{teks,suara,kecepatan,nada}`; max text 4000 chars on server; audio/mpeg. |
| POST `/api/suara/siapkan` | optional prefetch; server skips paid speakers, max 300 text blocks. |
| POST `/api/perintah` | unmatched speech label guess; JSON `{ucapan,tombol}`, response `{pilihan}`; do not expose server key in new UI. |

Sumber endpoint: `app.py:62–162`, `169–257`, `308–375`. Mount `StaticFiles(directory=WEB,html=True)` pada root ada di `app.py:378`; menambah landing pada `/` berarti menyelesaikan konflik index.html dan memperbarui link rail/README, bukan sekadar menambah halaman baru. Pilihan minimum ialah pertahankan existing routes pada gelombang UI pertama; bila landing baru disetujui, tentukan URL halaman Remediasi sebelum implementasi.

### Status/elemen yang tidak boleh kehilangan makna

- `state.elements[].kind`: heading, paragraph, table, image; heading.level, rows, page, id.
- Status image: `terbit_otomatis`, `antrean`, `disetujui`, `diubah`, `ditolak`, `dekoratif`.
- Review display: `alt_final`, `alt_auto`, `draft`, `reasons`, `checks`, `log`, `table`, `T1/T2`, `delta`, `seg`, `claim_detail`, `jenis`, `vektor`, `campuran`.
- Statistik hasil: pages, report.B0/B1/D verapdf/g1, timing.struktur_s/total_s, manifest.model_t1.
- Transcript: kind/page/text/say/note/el/status. `say=''` dekoratif skip. Pair image only ketika jumlah per halaman cocok (`listen.py:82–97`); jangan memaksa pasangan untuk animasi before/after.
- localStorage: `simak-suara` object `{suara,kecepatan,nada}`; `simak-perintah` string '1'/'0'. Jangan rename/hapus tanpa migration atau default fallback.

## Rencana pengerjaan yang dapat direview

### Tahap 0 — Bekukan baseline dan pilihan desain

1. Setujui tingkat adopsi template, halaman entry, dan prioritas mode presentasi vs operasional. Rekomendasi teknis: komposisi expressive pada introduction, workspace tugas tenang, reader low-stimulation; satu keluarga token.
2. Simpan screenshot desktop/mobile dan data fixture dari hasil yang sudah ada; sertakan satu output HTML mandiri dan baseline caption/status. Hindari mererun evaluasi model atau threshold calibration demi screenshot.
3. Tetapkan route map, vocabulary CTA, token roles, state inventory. Buat daftar selisih label karena perintah suara mengikuti label.

Acceptance: ada artefak before, kontrak API/DOM, papan state, dan daftar file perubahan; belum mengubah pipeline/model/data eval.

### Tahap 1 — Fondasi visual bersama

Ubah `style.css` tokens dan shared primitives; `common.js` shell/brand/nav/icon/status; empat HTML pada wrapper/heading. Fonts.css hanya berubah jika display font benar-benar dipilih. Hilangkan CSS inline yang digantikan token bersama secara selektif, tanpa refactor besar.

Acceptance: seluruh 4 route memuat; active nav/skip link/fokus/voice support bekerja; target min 44 × 44; tidak overflow body di 320/375/390/768/1024/1280/1440; zoom/reflow teruji; kontras semua pairing baru memenuhi target; no network font/CDN dependency wajib.

### Tahap 2 — Remediasi dan review

Susun input, progress, hasil, output, antrean/detail dengan hierarchy baru. Pertahankan hook atau perbarui semua selector/caller bersamaan. Lengkapi loading/error/retry, stale-response protection, focus after selection/review, dan edit state. Perlakukan approval/reject/delete sebagai aksi berbeda dengan konsekuensi jelas.

Acceptance: upload invalid dan empty dikabarkan; progress menyebut tahap; error tidak membuang file/teks; satu operasi aktif; queue filter dan selected identity konsisten; semua enam status benar; keputusan hanya tersimpan melalui endpoint lama; output links sesudah review terbaru; tidak ada keputusan ULD otomatis karena redesign.

### Tahap 3 — Demo dan Dengar

Demo: controls → verdict → traceable evidence; pertahankan baseline/reset/inject dan tabel acuan. Dengar: primary comparison, player tetap di DOM, transcript accessible button, state ready/preparing/playing/paused/finished/error/no-voice, one active playback. Copy menyatakan simulasi dan perbedaan lokal/opsional provider.

Acceptance: tidak ada angka hard-coded pengganti data; claim activation dengan Enter/Space menuju baris benar; Escape/back tidak memutus fokus; pemutar tidak tumpang tindih; prev/next batas; reduced-motion static feedback; error voice meninggalkan teks; paid audio hanya ketika pengguna memilih/memutar.

### Tahap 4 — Evaluasi dan keluaran mandiri

Evaluasi: progressive disclosure untuk detail tanpa menghapus denominator, interval, sample provenance, failure dan caveat. HTML reader: adopsi tokens seperlunya dalam CSS embedded, struktur dokumen tetap reading-first dan dark preference tetap diuji.

Acceptance: missing results punya recovery; G6/D_ketat absent aman; 7 tabel yang ada tetap semantic/scrollable; original result json tidak berubah; file HTML dibuka offline menampilkan semua teks/gambar/status; voice server failure tidak memblokir reading. Tidak mengubah tag PDF/algoritme bila hanya visual reader berubah.

### Tahap 5 — Verifikasi dan handoff

Uji keyboard penuh + NVDA di Windows/Chrome atau Edge; mobile touch sungguhan/emulasi yang dilabeli jelas; 200/400% zoom; reduced-motion; offline/slow/error fixtures; speech synthesis yang tersedia/tidak tersedia. Ambil screenshots sesudah pada ukuran sama dan catat bug konkret, bukan score-only.

Acceptance: data safety/status semantics, route compatibility, accessible flow, dan offline reader lulus. Detector dapat dicoba ulang bila engine tersedia; hasil ini tidak mengklaim scan sebelumnya clean.

## Testing sekarang dan tambahan minimum yang bermakna

Tidak ditemukan frontend test runner, package.json, Playwright config, pytest config, atau unit test suite pada Prototype melalui inventaris nama dan pencarian test/assert. Ada `eval/evaluate.py`, `audit_b2.py`, `banding_run.py`, results, serta dokumentasi pengujian pipeline dari clean clone. Itu evaluasi penelitian/pipeline, **bukan** regression suite UI. Menjalankan `eval.evaluate kalibrasi` dapat mengubah thresholds; `uji` dapat memanggil model/mengganti results, sehingga tidak dipakai sebagai tes UI rutin.

Tambahkan sekecil mungkin saat implementasi, bukan sekarang:

1. Fixture respons jaringan untuk semua status dan failure, termasuk G6 absent, transkrip kosong, teks panjang, grafik held/non-table/vector. Uji UI dengan mocked API agar tidak membayar model atau memodifikasi dokumen nyata.
2. Satu smoke flow browser empat route + upload invalid + sample mocked/poll success/error + queue/filter + keyboard selection + preserve textarea saat gagal + fokus setelah action. Pastikan tidak memanggil production review/delete.
3. Satu regression output `build_html` berbasis state fixture: heading/table/image status/escaping; standalone fonts/images embedded; data-say dan voice IDs ada. Jangan menulis ulang tes algoritme gerbang untuk perubahan CSS.
4. Self-check numerik palette dengan formula luminance dan expected black/white 21:1; rasio hasil dibandingkan threshold. Kegunaan nyata: mencegah orange/paper salah pairing.
5. Manual assistive-technology smoke yang direkam hasilnya, karena screenshot atau axe tidak membuktikan listening/focus nyaman.

## Risiko dan keputusan yang perlu dibahas

- Risiko terbesar implementasi: styling global merusak semua halaman; markup mengganti hooks; fokus hilang; status held terlihat sukses; voice command berubah makna karena label; reader mandiri tergantung asset/server; bukti penelitian tertutup dekorasi atau denominator hilang.
- Pilihan bernilai tinggi: route entry (`/` Remediasi sekarang), tingkat adopsi template, apakah reader ikut rebrand penuh, dan apakah koreksi hardening P1 masuk paket redesign. Hindari mengikat fitur landing baru sebelum disepakati.
- Estimasi sebaiknya per tahap dan berdasarkan exit criteria; tidak memberi janji jam/hari tanpa keputusan desain dan baseline uji.
- Pengamanan publik seperti autentikasi, batas upload (saat ini `await file.read()` tanpa size cap pada `app.py:85`), dan authorization bukan hasil redesign CSS. Prototype tidak otomatis aman untuk internet hanya karena UI lebih rapi; deployment publik merupakan ruang kerja terpisah bila diminta.

Yang belum diperiksa: runtime mobile/zoom/AT/audio, post-processing/review/delete, template live/failure injection, Lighthouse, dan detector aktual (engine tidak tersedia).
Risiko yang harus diketahui: skor adalah sementara; rencana menjaga kontrak tidak membuktikan implementasi sudah benar, dan copy retensi enam jam saat ini lebih kuat daripada scheduler yang terlihat.
