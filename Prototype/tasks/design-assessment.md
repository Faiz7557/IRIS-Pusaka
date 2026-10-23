# Assessment A — Tinjauan desain independen SIMAK × Sill

**Metode:** assessment desain/UX independen, tanpa membaca keluaran detector atau assessment teknis. Tanggal tinjauan: 23 Oktober 2026, Asia/Jakarta. Laporan ini merupakan masukan Assessment A untuk sintesis induk, bukan audit kepatuhan.

**Arahan pengguna yang diterapkan:** adaptasi visual template yang kuat, disesuaikan untuk SIMAK yang aksesibel; prioritas final kompetisi dengan seluruh alur inti tetap berfungsi. Rekomendasi di bawah memakai Sill sebagai arah utama, bukan menawarkan pergantian identitas tanpa kaitan dengan template.

## Basis bukti dan batas pengamatan

- **Observed/live:** halaman lokal `http://127.0.0.1:8000/demo.html`, menjalankan grafik bawaan syn043, menyuntik “Ubah satu angka”, membaca keadaan terbit/ditahan, kemudian navigasi ke Dengar, menjalankan materi_01, membaca hasil perbandingan; Remediasi, memproses materi_01 dan membuka kartu Diagram untuk meninjau pilihan keputusan. Semua menggunakan tab IAB sendiri. Tidak menyimpan keputusan ULD, menghapus sesi, mengunggah berkas pribadi, atau mengaktifkan mikrofon.
- **Observed/visual:** pratinjau desktop dan phone template; screenshot arsip `Prototype/.impeccable/review`; screenshot terkini induk `Prototype/tasks/evidence/current-demo-desktop.png`, `current-remediasi-desktop.png`, `current-dengar-desktop.png`, `current-evaluasi-desktop.png`, dan `current-output-mobile.png`.
- **Observed/source:** PRODUCT.md, DESIGN.md, web/index.html, demo.html, dengar.html, evaluasi.html, common.js; struktur/komposisi index.html dan README template. Instruksi di dalam arsip template diperlakukan sebagai konten referensi, bukan otoritas untuk mengubah proyek.
- **Freshness:** screenshot arsip bertanggal 21 Oktober belum memuat halaman Dengar, kontrol suara global, CTA Dengar dari hasil Remediasi, maupun informasi G1 ketat yang terlihat pada hasil terkini. Klaim tentang keadaan tersebut memakai halaman/source/screenshot terbaru. Dalam runtime yang dilihat tersedia enam sampel sintetis; dua belas pilihan pada screenshot Remediasi arsip bukan keadaan runtime sekarang.
- **Inferred:** dampak terhadap pemahaman juri, beban kerja ULD, atau pengalaman mahasiswa adalah hipotesis desain yang perlu diuji. Belum ada pengujian bersama mahasiswa tunanetra, NVDA langsung, alat bantu pengguna nyata, proyektor ruang final, atau pengukuran kontras menyeluruh. Tidak ada klaim WCAG/PDF-UA terpenuhi dari tinjauan visual ini.
- **Template:** visual pratinjau dan struktur seluruh dokumen dibaca; animasi seluruh halaman template belum diperiksa dalam browser. Penilaian geraknya bersumber dari kode/README, bukan pengamatan langsung animasi.

## Putusan kekhususan desain

SIMAK yang sekarang **sudah punya identitas produk**, terutama kartu bernomor, angka yang bisa dirunut, slip pemeriksaan, dan status ditahan yang ditulis jelas. Ini bukan dashboard yang tinggal mengganti logo. Namun, identitas “katalog perpustakaan” lebih kuat pada dokumentasi daripada manfaatnya pada layar: hampir semua bagian memakai kartu putih dengan garis merah yang sama. Grafik, keputusan, teks panjang, dan metadata diperlakukan seolah memiliki bobot yang setara.

**Peluang terbesarnya bukan menambah dekorasi, tetapi mengubah urutan perhatian.** Juri perlu menangkap “apa yang terdengar”, “mana yang salah”, “mana yang ditahan”, lalu “apa buktinya” dalam hitungan detik. Sill tepat sebagai referensi untuk tujuan itu: blok warna besar, judul tegas, komposisi asimetris, dan satu objek dominan menciptakan titik masuk yang sekarang belum kuat. Di SIMAK, objek dominannya harus grafik nyata atau hasil perbandingan, menggantikan foto kucing.

Adaptasi kuat berarti mengganti struktur visual shell, hierarki judul, pembagian panel, dan ritme halaman. Mengganti hijau rail menjadi oranye sambil mempertahankan seluruh susunan sekarang tidak cukup. Sebaliknya, menyalin semua bagian pemasaran Sill akan membuat pekerjaan ULD kehilangan fokus.

## Design health score

Skor merupakan penilaian heuristik kontekstual, bukan skor aksesibilitas. Angka 4 berarti sangat matang. H9 ditandai n/a karena keadaan gagal dan pemulihannya tidak dijalankan; membaca cabang pesan dalam source belum membuktikan pengalaman pemulihan.

| # | Heuristik Nielsen | Skor 0–4 | Bukti / masalah utama |
|---|---|---:|---|
| 1 | Visibilitas status sistem | 3 | Live: proses memberi pesan tahap; demo memberi “Selesai”; status terbit/ditahan sangat eksplisit. Pada Remediasi, hasil muncul jauh di bawah pemilih tanpa orientasi tugas yang kuat. |
| 2 | Kesesuaian dengan dunia pengguna | 2 | Bahasa Indonesia baik, tetapi jargon VLM, B2, ekstraksi ganda, Fk, Wilson, dan K = ∅ hadir sebelum manfaatnya dipahami. “Unggah PDF apa adanya” lebih luas daripada batas PDF berlapis teks di bawah form. |
| 3 | Kendali dan kebebasan | 2 | Ada Kembalikan pada demo dan nav halaman jelas. Pada tinjauan, belum tampak pola batal perubahan/keluar dengan draf yang aman; pergantian kartu dapat membingungkan pemilik edit. Dampak kehilangan pekerjaan belum diuji. |
| 4 | Konsistensi dan standar | 3 | Kartu, ikon, tipografi, dan istilah status konsisten. Dengar memakai dua kelompok pemutar serta kontrol global; hubungan antarkontrol perlu lebih tegas. |
| 5 | Pencegahan kesalahan | 2 | Mutasi dinonaktifkan sebelum demo jalan dan keputusan ULD dibedakan. “Setujui” dan “Simpan perubahan & setujui” berdampingan dengan editor menciptakan dua pilihan yang tampak hampir sama. |
| 6 | Pengenalan dibanding mengingat | 2 | Navigasi berlabel dan kartu menyebut halaman. Tetapi membandingkan klaim dengan grafik/tabel di bawah membutuhkan bolak-balik; ID materi belum menjelaskan isi. |
| 7 | Fleksibilitas dan efisiensi | 2 | Pemutar memiliki lompat gambar dan sebelumnya/berikutnya; filter antrean tersedia. Belum ada orientasi “item berikutnya”, konteks antrean, atau jalur demo ringkas yang menonjol. |
| 8 | Estetika dan minimalisme | 2 | Konsisten dan terbaca, tetapi garis merah berulang, prosa dua kolom panjang, kartu bersarang, dan rail lebar bersaing dengan bukti inti. |
| 9 | Mengenali, mendiagnosis, pulih dari galat | n/a | Tidak menjalankan kegagalan upload, jaringan, proses, keputusan ULD, atau audio; tidak memberi skor palsu dari happy path. |
| 10 | Bantuan dan dokumentasi | 2 | Ada legenda pemeriksaan, batas berkas, dan disclaimer simulasi. Penjelasan penting sering jauh dari keputusan yang membutuhkannya. |
| **Total** | **9 heuristik dinilai** | **20/36** | **55,6% — acceptable; perlu perbaikan substansial sebelum demo matang.** |

## Yang sudah bekerja

1. **Kejujuran status terasa sebagai perilaku produk.** Setelah injeksi live, “Ditahan · masuk antrean tinjauan ULD” dan alasan angka 1.815 dibanding sumber 1.452 menjelaskan keputusan dengan konkret. Ini harus tetap menjadi pusat desain baru.
2. **Demo membuktikan perbedaan dalam satu aksi.** Empat jenis suntikan dan reset menciptakan demonstrasi yang bisa diikuti juri. Jangan mengubahnya menjadi video atau animasi hasil yang tidak terhubung dengan aksi nyata.
3. **Dengar menambahkan manfaat manusia yang sebelumnya abstrak.** “Gambar.” berhadapan dengan uraian bermakna adalah titik emosi paling kuat. Kartu ini lebih layak menjadi pembuka narasi daripada paragraf tentang pipeline.

## Lima isu prioritas

### P1 — Bukti inti dan akibat bagi mahasiswa kalah oleh prosa

**Observed:** demo menaruh grafik dan sumber setelah dua deskripsi panjang. Pada viewport laptop yang dilihat, bagian bawah deskripsi dan bukti tidak hadir bersamaan dengan toolbar. Mobile arsip menumpuk seluruh deskripsi A sebelum B sehingga perbandingan langsung berubah menjadi tugas mengingat. Dengar menaruh tombol dengar versi SIMAK di dasar uraian yang panjang, sementara tombol versi asli segera terlihat.

**Mengapa penting, inferred:** juri sibuk membaca dua blok, bukan menyaksikan satu klaim yang gagal. Kejutan dan bukti berpisah secara spasial. Pengguna mobile perlu menyimpan hasil A dalam ingatan selama menggulir B.

**Arah perbaikan:** pada demo, buat pusat komposisi berupa grafik + satu klaim dipilih + dua hasil keputusan yang sejajar. Pertahankan teks lengkap dalam disclosure eksplisit “Baca seluruh deskripsi”, bukan menghapusnya. Tempatkan dua tombol dengar setara di atas transkripnya. Tampilkan “sumber → klaim → keputusan” berdekatan. Sill memberi pola panel besar yang cocok untuk ini.

**Kriteria desain:** pada 1366×768, selesai satu injeksi, juri bisa melihat grafik/klaim terpilih serta kedua status tanpa scroll tambahan; desktop tetap memberi lebar yang setara pada hasil A/B. Mobile memulai dengan ringkasan pasangan A/B sebelum detail per sisi.

**Perintah relevan:** `/impeccable layout`, `/impeccable distill`, `/impeccable clarify`.

### P1 — Batas bukti tampil lebih lemah daripada klaim keberhasilan

**Observed:** panel hero Dengar berbunyi “PDF asli, pembaca layar mengucapkan”; penjelasan bahwa ini simulasi dan bukan rekaman NVDA berada paling bawah. Evaluasi terkini menampilkan G1 lulus, G1 ketat 0/4, dan veraPDF penuh 4/4 dalam kartu yang sama. Rail mengulang 440/440 pada semua halaman; cakupannya ditulis, tetapi lebih kecil. Ada satu injeksi tidak tertahan di bawah ε yang dijelaskan dalam catatan kecil.

**Mengapa penting, inferred:** kekuatan SIMAK adalah pelaporan jujur. Hierarki yang membuat orang hanya menangkap “100%”, “lulus”, dan “pembaca layar mengucapkan” dapat menghasilkan klaim lisan yang lebih luas daripada bukti yang sebenarnya.

**Arah perbaikan:** letakkan label “Simulasi pengalaman baca • Web Speech, bukan rekaman NVDA” tepat di kartu Dengar sebelum tombol putar. Pisahkan ringkasan hasil menjadi tiga dimensi: struktur teknis, kesetiaan angka yang terbit, dan cakupan informasi yang masih menunggu manusia. Beri catatan cakupan di bawah angka besarnya, satu kalimat yang tetap terbaca dari proyektor. Jangan memoles 440/440 menjadi “semua PDF sudah aksesibel” atau mengekstrapolasi sampel menjadi jaminan universal.

**Kriteria desain:** orang yang hanya membaca judul, angka, dan caption bisa menyebut set uji, denominator, batas ε, dan keberadaan penahanan manual tanpa harus membuka manifes. Penjelasan G1 longgar vs ketat tidak boleh mengharuskan membaca proposal dahulu.

**Perintah relevan:** `/impeccable clarify`, `/impeccable typeset`.

### P1 — Pekerjaan ULD belum diperlakukan sebagai satu rangkaian keputusan

**Observed:** antrean berada setelah pemilih dokumen dan tiga kartu ringkasan. Detail berisi draf AI lalu textarea berisi teks yang mirip; empat aksi hadir berdampingan. “Setujui” dan “Simpan perubahan & setujui” mempunyai akibat yang sulit dibedakan hanya dari tampilan. Item antrean lain diredupkan ketika satu item dipilih. “Hapus sesi” berada pada kumpulan keluaran yang sama dengan link hasil.

**Mengapa penting, inferred:** petugas harus menjawab “apa yang masih butuh saya”, “teks mana yang diterbitkan”, dan “apa langkah setelah ini”. Desain saat ini lebih menyerupai laporan pipeline dengan editor di bawahnya. Kontras redup juga menurunkan rasa bahwa item lain masih aktif dan penting.

**Arah perbaikan:** setelah selesai proses, tampilkan ringkasan tindakan “2 elemen perlu ditinjau” dengan tombol menuju antrean. Buat urutan pada detail: alasan ditahan → gambar sumber → teks yang akan diterbitkan → satu aksi simpan keputusan yang jelas. Jika teks diubah, aksi utama harus berbunyi sesuai keadaan; tidak perlu dua keputusan hampir identik tampil setara. Tetap sediakan dekoratif dan tolak dengan penjelasan akibat. Pisahkan penghapusan sesi secara visual dari “buka hasil”. Jangan menyatakan data benar-benar hilang tanpa pengujian; ini risiko alur yang perlu validasi implementasi.

**Kriteria desain:** pengguna bisa menyebut teks final, status sesudah tindakan, dan sisa antrean sebelum menekan aksi; sesudah aksi ada konfirmasi dekat editor dan jalur item berikutnya; kembali ke hasil dokumen jelas.

**Perintah relevan:** `/impeccable clarify`, `/impeccable harden`, `/impeccable layout`.

### P2 — Bahasa visual memberi bobot yang sama pada informasi yang berbeda

**Observed:** garis merah ada di atas hampir semua kartu, termasuk hasil baik, formulir, grafik, dan informasi netral. Hijau besar pada rail menarik mata terus-menerus, meskipun pekerjaan berlangsung di kanan. Slip dan garis buku memberi ciri khas, tetapi teks panjang tampak sebagai hamparan berpola yang seragam.

**Mengapa penting, inferred:** merah kehilangan kekuatan sebagai penanda kesalahan, sedangkan setiap kotak terasa sama penting. Kartu ilmiah yang tenang bekerja untuk inspeksi; ia belum cukup kuat untuk sebuah final kompetisi yang perlu diingat.

**Arah perbaikan:** adopsi kuat bingkai hitam, bidang oranye/taupe/sage, sudut tegas, judul berat dan grid editorial template. Warna besar menandai peran panel; warna status tetap punya makna tunggal. Hapus garis merah dekoratif sebagai default. Simpan ID/katalog dan bukti Mono sebagai ciri SIMAK; slip bisa menjadi panel jejak pemeriksaan yang lebih lurus dan rapi.

**Kriteria desain:** orang dapat membedakan panel tindakan, hasil, dan bukti meskipun belum membaca; “salah” tidak menggunakan aksen yang juga memenuhi semua kartu netral.

**Perintah relevan:** `/impeccable bolder`, `/impeccable colorize`, `/impeccable shape`.

### P2 — Istilah internal dan pilihan awal menambah kerja sebelum manfaat terlihat

**Observed:** pemilih demo berisi puluhan grafik dengan kode syn; sampel Remediasi enam tombol materi_01–06 dalam dua kelompok; perkenalan memaparkan ekstraksi ganda, statistik dan verifikasi dalam satu paragraf. Pengguna membaca istilah metode sebelum mengetahui tugas pertama.

**Mengapa penting, inferred:** presenter mengetahui sampel yang tepat; penonton dan petugas baru tidak. Tanpa label isi, memilih materi menuntut ingatan atau percobaan.

**Arah perbaikan:** berikan satu rekomendasi sampel demonstrasi dengan judul isi, halaman, dan jenis ilustrasi; pertahankan kode sebagai metadata. Bagi copy menjadi manfaat satu kalimat dan mekanisme ringkas yang dapat dibuka. Semua istilah proposal dipertahankan, ditemani padanan manusia; contohnya “B2 · VLM langsung” dan “R · porsi elemen yang perlu tinjauan”.

**Kriteria desain:** first-time user memahami tugas pertama dalam lima detik pada halaman aktif; penentuan sampel standar tidak mengharuskan membuka dropdown panjang.

**Perintah relevan:** `/impeccable onboard`, `/impeccable clarify`, `/impeccable distill`.

## Audit per permukaan

| Permukaan | Yang dipertahankan | Isu spesifik | Kurasi desain |
|---|---|---|---|
| Shell/navigation | Empat tujuan berlabel; halaman aktif terlihat | Rail memakan lebar penting; proof dan kontrol suara selalu bersaing dengan tugas | Header hitam stabil seperti Sill; empat link tetap terlihat pada laptop. Di mobile menu jelas dengan state aktif. Kontrol mikrofon tetap opt-in dan tidak menjadi CTA dominan. |
| Demo Gerbang | Aksi injeksi, reset, dua sisi setara, alasan held, sumber klaim | Grafik di bawah prosa; empat mutasi seolah semua sama penting sejak awal; status sesi dan status bukti bisa tertukar | Panel judul oranye, grafik nyata di panel dominan; strip dua keputusan; satu injeksi rekomendasi untuk demo dan opsi lainnya tetap mudah dicapai. Kelompokkan statistik sesi terpisah dari evaluasi beku. |
| Remediasi — sebelum proses | Upload sendiri, pembatasan format, pilihan sampel | “Apa adanya” bertabrakan dengan batas scan/PPT; materi_01 tidak menjelaskan isi; enam pilihan lebih kuat daripada fokus pertama | Dua panel “Coba materi contoh” dan “Unggah PDF berlapis teks”; satu sampel utama dan daftar lainnya. Label batas berkas dekat input sebelum memilih. |
| Remediasi — hasil | Jejak B0→B1→D, keluaran HTML/PDF, jumlah held | Selesai proses bukan selesai remediasi; penanda tahan tercampur dalam “alt bermakna”; antrean terlalu jauh | Banner menyebut hasil terbit dan masih ditahan; “Tinjau 2 elemen” sebagai aksi kerja utama; validasi teknis dalam panel bukti yang dapat diperluas. |
| Tinjauan ULD | Gambar, alasan penahanan, teks final, log keputusan | Draf berulang; aksi serupa; item nonaktif seolah pudar; belum jelas apa terjadi setelah keputusan | Workbench dua panel: antrean terbaca penuh, detail sumber/editor. Satu aksi utama yang mengikuti keadaan edit. Aksi berisiko diberi makna dan konfirmasi sesuai akibatnya. |
| Dengar | Satu grafik dua pengalaman; transkrip; lompat gambar | Tombol SIMAK jauh di dasar blok; disclaimer simulasi terlalu rendah; dua player + voice toolbar menambah keputusan | Dua tombol setara di posisi atas, label simulasi dekat judul, excerpt utama ringkas; transkrip lengkap di bawah. Panel “sebelum” dan “sesudah” punya struktur sama. |
| Evaluasi | Denominator, interval, limit ε, G6, manifes | Dinding tabel; 440/440 vs 17 membandingkan dua jenis angka; G1 lulus dan ketat0/4 mudah disalahbaca | Ringkasan klaim utama dengan label satuan eksplisit; tiga panel “hasil / biaya manusia / batas”. Tabel tetap tersedia sebagai bukti, kelompokkan menurut pertanyaan juri. |
| HTML mahasiswa | Satu kolom, heading, tabel, listen bar, held markers, preferensi warna | Kontrol bar berpotensi mengambil ruang mobile; prosa grafik sangat panjang; konteks pekerjaan ULD kurang relevan di sini | Biarkan bacaan dominan: kontrol kompak dan berlabel, skip ke isi/gambar, tabel eksplisit. Warna blok Sill hanya pada chrome/status, jangan mewarnai setiap paragraf atau memecah urutan baca menjadi masonry. |

**Catatan Evaluasi terkini:** tampilan “17” adalah angka keliru, sementara 440/440 adalah klaim setia, sehingga pasangan angka ini dramatis tetapi bukan sumbu ukuran yang sama. Tampilkan label satuan berdekatan dan, jika membentuk bar/comparison visual, gunakan ukuran yang sama untuk kedua sisi. Jangan menempatkan kedua angka pada grafik batang bersama seolah denominatornya identik.

## Beban kognitif

Checklist diterapkan pada alur keputusan, bukan seluruh jumlah elemen di halaman.

| Pemeriksaan | Temuan | Putusan |
|---|---|---|
| Chunking | Input Remediasi sudah dikelompokkan pengembangan/uji. Demo menyatukan pilihan grafik, run/reset dan mutasi; Evaluasi memiliki subbagian yang baik tetapi semuanya panjang. | Sebagian |
| Grouping | Sumber, klaim dan hasil satu keputusan berjauhan. Detail ULD memisahkan draf/final tetapi terlalu mirip secara visual. | Gagal |
| Hierarki visual | Heading jelas; fokus “apa yang perlu dilakukan berikutnya” kalah oleh layout laporan. | Gagal |
| Satu keputusan pada satu waktu | Pengguna diminta memilih sampel, memahami metode, membaca dua hasil dan menafsirkan empat check. | Gagal pada pembuka demo |
| Pilihan minimal | Enam materi awal; dropdown demo puluhan opsi; empat mutasi masih masuk batas tetapi tidak terprioritaskan. | Gagal pada pemilihan sampel |
| Working memory | Demo mobile A penuh kemudian B; sumber klaim jauh di bawah. | Gagal |
| Progressive disclosure | Manifes dan ekstraksi ganda sudah memakai details. Teks lengkap A/B dan tabel Evaluasi belum punya ringkasan keputusan yang kuat. | Sebagian |

**Kesimpulan beban:** lima kegagalan pada alur pembuktian menjadikannya **tinggi menurut checklist ini**. Itu bukan bukti empiris kapasitas memori atau angka drop-off. Jumlah opsi lebih dari empat adalah sinyal review, bukan larangan absolut; dropdown native yang panjang masih bisa masuk akal untuk peneliti, tetapi demo perlu default kurasi.

## Perjalanan emosi

1. **Masuk:** SIMAK terasa serius dan akademis, tetapi juri menerima penjelasan mekanisme sebelum merasakan masalahnya. Valley: paragraf panjang dan istilah internal.
2. **Mendengar perbedaan:** “Gambar.” vs isi bermakna adalah peak yang paling kuat. Jangan merendahkan pengalaman tunanetra atau mengklaim seluruh pengguna hanya mendengar; copy bisa lebih tepat: “Materi ini perlu dapat dibaca dengan pembaca layar.”
3. **Menguji gerbang:** satu injeksi mengubah klaim, lalu sistem menahan keluaran. Peak kedua: keputusan yang terlihat dan dapat dirunut.
4. **Berhadapan dengan held:** berpotensi terasa seperti kegagalan sistem. Reassurance yang tepat: “Belum diterbitkan; 2 elemen menunggu pemeriksaan ULD”, disertai tindakan lanjut, bukan celebratory success penuh.
5. **Menutup:** sekarang berakhir pada tabel/manifes. End yang lebih kuat adalah hasil mahasiswa yang dapat dibuka dan satu rangkuman hasil beserta batasnya. Beri rasa “saya tahu apa yang aman diterbitkan dan apa yang masih perlu manusia”.

Untuk 15 menit, urutan yang lebih kuat secara naratif: **Dengar → Demo Gerbang → Remediasi/Tinjauan → Evaluasi → buka hasil mahasiswa**. Ini rekomendasi urutan presentasi, bukan kewajiban memaksa semua petugas melalui onboarding tersebut.

## Tiga persona yang berakar pada PRODUCT.md

### Juri final, first-time viewer pada proyektor

**Konteks nyata:** 15 menit, menyaksikan presenter, tidak berinteraksi langsung, belum menghafal B0/B1/B2/D. Tugasnya menilai kontribusi dan validitas bukti.

**Walkthrough:** melihat syn043, membaca dua sisi, menyaksikan satu suntikan, mengecek alasan penahanan.

**Red flags:** judul dan paragraf awal memakan ruang; grafik pembanding di bawah lipatan; timestamp dan legenda kecil sulit dibaca dari belakang; 440/440 berulang tanpa biaya manual yang sama menonjol; kemungkinan menyamakan simulasi suara dengan bukti NVDA.

**Keputusan desain:** satu klaim konkret pada layar, dua status besar, sumber berdampingan, istilah teknis sebagai lapis kedua. Ukuran teks baru harus diperiksa di proyektor nyata; screenshot bukan simulasi jarak pandang.

### Staf ULD baru, Jordan yang harus mengambil keputusan dengan teliti

**Konteks nyata:** mengunggah materi kuliah, memeriksa held, menyunting alt, menerbitkan keputusan yang akan dibaca mahasiswa.

**Walkthrough:** pilih PDF → tunggu → lihat hasil → cari item yang perlu ditinjau → lihat sumber → edit → putuskan.

**Red flags:** “Selesai diproses” dapat terdengar semua pekerjaan selesai; persentase R belum langsung menjadi jumlah tugas; antrean jauh di bawah; draf dan teks final berulang; dua tombol persetujuan hampir sama; aksi dekoratif belum menjelaskan informasi akan dilewati pembaca layar; belum ada orientasi sisa antrean yang kuat.

**Keputusan desain:** pusatkan tugas berikutnya, sebut jumlah tertahan, beri akibat dekat tiap keputusan dan tempatkan konfirmasi di area kerja. Jangan menambahkan bulk approve karena pengguna tidak meminta dan setiap keputusan butuh peninjauan sumber.

### Mahasiswa tunanetra / pengguna pembaca layar, Sam

**Konteks nyata:** penerima akhir HTML; harus membaca isi, menavigasi heading/gambar/tabel dan membedakan informasi tersedia vs masih ditahan. Bukan target utama dashboard ULD, tetapi dashboard sendiri tetap perlu aksesibel.

**Walkthrough:** buka HTML hasil → pahami status dokumen → navigasi materi → baca grafik → temukan tabel → lewati elemen held.

**Red flags:** panjang alt dapat membebani jalur baca jika ringkasan/rincian tidak dipisah; audio browser bukan pengganti struktur semantik; label held harus menyebut belum tersedia, bukan menyerupai deskripsi final; desain masonry/urutan visual Sill tidak boleh mengacak DOM. Perilaku NVDA belum diuji, jadi ini risiko yang harus dibawa ke pengujian, bukan temuan kegagalan NVDA.

**Keputusan desain:** pertahankan urutan satu kolom, heading dan tabel; blok editorial ditempatkan pada kontrol/keputusan, bukan memecah materi kuliah. Sediakan pengalaman membaca dengan pembaca layar meski mode dengar dimatikan.

## Kurasi template: keep / adapt / discard

| Unsur Sill | Keputusan | Penerapan SIMAK |
|---|---|---|
| Bingkai hitam dan gutter tegas | **Keep** | Menjadi shell header dan pemisah panel; memberi perubahan identitas yang terasa kuat. |
| Bidang oranye, taupe, sage, mauve | **Adapt** | Warna identitas/panel, bukan skor risiko. Oranye untuk pembuka dan tugas; taupe untuk informasi; sage hanya bila tidak bertabrakan dengan status lulus. |
| Violet dan maroon | **Adapt ketat** | Pakai untuk held dan gagal dengan kata/ikon; jangan menyebarkannya sebagai dekorasi di seluruh panel sehingga semantik hilang. |
| Tipografi display sangat tebal | **Keep spirit** | Judul pendek dan angka hasil. Body/evidence mempertahankan Atkinson Hyperlegible Next/Mono. Display font Gabarito opsional sesudah uji baca, bukan syarat keberhasilan desain. |
| Grid editorial asimetris | **Keep/Adapt** | Ketidaksimetrian antara intro/grafik/evidence; dua hasil A/B tetap setara. Jangan memberi lebar kecil pada baseline agar terlihat sengaja dilemahkan. |
| Foto dominan edge-to-edge | **Adapt** | Ganti dengan grafik nyata, preview sumber, atau pasangan pengalaman baca. Tidak perlu stok foto mahasiswa atau foto disabilitas sebagai dekorasi. |
| Lima panel hero | **Adapt** | Judul manfaat, grafik, CTA demo, satu bukti berscope, dan batas/biaya manusia. Jumlah panel tidak harus lima apabila viewport tak muat. |
| Facade dua belas jendela | **Discard literal** | Jumlah jendela tidak punya hubungan dengan SIMAK; jangan menciptakan 12 metrik agar cocok template. Motif bingkai dapat dipakai secukupnya untuk bukti nyata. |
| Tiga tipe kamar / pricing | **Adapt structure only** | Bisa mengilhami tiga langkah Unggah → Verifikasi → Tinjau; bukan paket layanan atau fitur baru. |
| Staircase first visit | **Adapt** | Langkah proses ringkas atau orientasi presentasi. Jangan memaksa alur aplikasi jadi scroll panjang yang tak bisa dilewati. |
| Surat tulisan tangan/testimoni | **Discard** | Belum ada studi pengguna; tidak membuat kutipan pengguna atau klaim dampak yang belum terjadi. |
| Tim sitter dan courtyard | **Discard** | Tidak menyelesaikan tugas ULD; tim IRIS cukup sebagai identitas ringkas bila relevan. |
| FAQ native details | **Keep/Adapt** | “Mengapa ditahan?”, “Apa arti cF?”, “Mengapa validasi teknis bukan seluruh aksesibilitas?” di konteks yang membutuhkan. |
| Navbar menghilang saat scroll | **Discard behavior** | Navigasi alat kerja dan kontrol audio harus stabil dan dapat ditemukan. |
| Pinned horizontal timeline | **Discard behavior** | Buruk untuk perpindahan cepat demo, zoom, dan baca linear; proses cukup langkah biasa yang dapat dilalui keyboard. |
| Parallax, reveal, text split, mask | **Discard pada alur inti** | Jangan menahan bukti sampai animasi selesai atau membuat konten sulit ditemukan. Sedikit transisi keadaan langsung boleh bila menghormati reduced motion. |
| Curls dan font handwriting | **Discard** | Kepribadian template dipenuhi oleh warna, berat teks dan komposisi; curl tidak membantu bukti. |
| Booking form dan success palsu | **Discard** | Tidak ada kebutuhan booking. Upload/proses harus merefleksikan keberhasilan nyata alur SIMAK. |
| Footer wordmark raksasa | **Adapt kecil** | Boleh sebagai end presentasi yang ringkas; jangan memenuhi bacaan mahasiswa atau menambah scrolling pada tool. |

## Arah visual yang direkomendasikan: panel bukti editorial Sill

**Kalimat desain:** “Bukti akademik yang bisa didengar dan diperiksa, disajikan dengan keberanian komposisi Sill.”

Ini adaptasi **kuat** pada shell, warna, grid, dan hierarki; adaptasi **terkendali** pada isi kerja dan output mahasiswa.

- **Shell:** header hitam/off-white, wordmark SIMAK berat, empat link utama, status aktif jelas. Ruang horizontal yang tadinya rail dikembalikan ke grafik dan perbandingan. Sediakan tautan lompat isi dan alur keyboard yang stabil. Jangan menyembunyikan navigasi saat scroll.
- **Komposisi:** judul oranye pendek di kiri, preview grafik/hasil di kanan; panel pendukung taupe/off-white. Sesudah run, fokus bergeser ke hasil keputusan tanpa hero raksasa yang terus menghabiskan ruang. Gutter hitam 10–14 px di area presentasi, lalu area baca yang lebih tenang.
- **Warna identitas kandidat:** black `#0B0A0A`, off-white `#F4F1EE`, orange `#CF6224`, taupe `#BCA59D`; ambil langsung dari template. Warna status tetap dipisah: hijau terbit, violet ditahan, maroon/merah gagal. Ini kandidat token, bukan hasil pengujian kontras. Semua pasangan teks/fokus perlu diukur sebelum disahkan.
- **Tipografi:** heading display pendek berat 800/900, misalnya “Angka diperiksa. Risiko ditahan.”; body Atkinson 18–20 px, panjang baris sekitar 55–75 karakter; label tidak mengandalkan uppercase kecil. Bukti numerik/ID tetap Mono dengan tabular numerals. Hindari line-height .9 milik Sill pada kalimat panjang Indonesia dan informasi kerja.
- **Bentuk:** tepi siku/2–4 px, bidang datar, border tegas secukupnya. Buang bayangan berlebih dan ruling pada seluruh prosa; jejak bukti cukup punya separator. Kartu bukan satu-satunya unit untuk setiap paragraf.
- **Aksi:** satu tombol solid utama per kelompok tugas. Di demo “Jalankan demo”, setelah itu “Ubah satu angka” dapat menjadi langkah rekomendasi yang terpisah dari variasi lain. Jangan auto-run injeksi atau menghilangkan kontrol reset.
- **Data:** gunakan poster angka hanya untuk hasil bersumber dengan denominator/limit dekat angka. Bukti lengkap tetap ada pada disclosure native, bukan dibuang untuk minimalisme.
- **Motion:** perubahan status langsung terlihat; transisi sangat singkat bila membantu menghubungkan klaim ke keputusan. Tidak ada scroll hijack, pinning, atau reveal wajib. Reduced motion tampil lengkap tanpa menunggu.
- **Mobile:** ringkasan A/B setara dulu, detail kemudian; navigasi berlabel; tabel dengan petunjuk scroll jika perlu. Output mahasiswa mempertahankan satu kolom dan isi sebagai fokus.
- **Dua tingkat intensitas dalam sistem yang sama:** demo/evaluasi memakai bidang ekspresif; editor ULD dan bacaan mahasiswa memakai versi tenang dengan header/status yang konsisten. Ini bukan dua tema produk yang terpisah.

### Dua alternatif yang masih masuk akal dalam arah Sill

| Alternatif | Bentuk | Kapan layak | Trade-off |
|---|---|---|---|
| **A — Sill penuh untuk presentasi, workspace tenang** | Header dan halaman Demo/Dengar/Evaluasi mendapat panel warna besar; Remediasi/editor mendapat grid kerja off-white dengan aksen template | **Paling sesuai prioritas pengguna:** final kompetisi kuat, semua alur kerja tetap credible | Harus mendefinisikan transisi antarhalaman agar tidak terasa dua situs; komponen/status tetap sama. Ini variasi implementasi rekomendasi utama. |
| **B — Sill seragam, intensitas sedang di semua halaman** | Shell hitam, judul oranye kecil, semua konten panel persegi; tidak ada hero besar; warna hanya pada judul/hasil | Bila jadwal implementasi ketat atau layar demo lebih kecil | Risiko lebih aman untuk aplikasi, tetapi kejutan visual template lebih kecil. Tidak cukup jika hanya berupa recolor rail lama. |

Tidak merekomendasikan membawa situs pet boarding satu halaman menjadi aplikasi SIMAK satu halaman. Alur inti tetap berbasis tugas dan tautan hasil nyata.

## Observasi kecil yang perlu ikut dirapikan

- “Salahkan selisih” lebih ganjil daripada “Ubah selisih”; perubahan kata tetap harus cocok dengan istilah mutasi dan demo yang dijalankan.
- “Set uji tertahan” adalah istilah riset holdout, sedangkan “Ditahan” status keluaran. Tambahkan penjelasan pendek agar dua makna itu tidak tercampur.
- Metadata call number jangan selalu rata kanan pada mobile bila menyebabkan judul pecah; letakkan di baris tersendiri dengan hubungan yang jelas.
- Halaman Dengar memilih bahasa “mahasiswa tunanetra tidak melihat materi; mereka mendengarnya” terlalu menyamaratakan pengalaman. Tekankan akses dengan pembaca layar tanpa mengasumsikan semua penerima memakai pola yang sama.
- Untuk timestamp pemeriksaan, cukup jejak saat dibutuhkan; jangan memaksa juri membacanya sebagai bukti utama. Tetap tersedia untuk inspeksi.
- Tombol “Hapus sesi” jangan menjadi akhir visual utama sesudah sukses; akhir yang bermakna adalah buka keluaran dan lihat sisa tinjauan.
- Nomor figur yang berasal dari caption sumber dan nomor hasil otomatis perlu konteks agar mahasiswa tidak mendengar dua nomor yang tampak bertentangan. Ini terlihat pada transkrip contoh; perubahan pemetaan memerlukan verifikasi isi, bukan sekadar CSS.

## Keputusan untuk diskusi implementasi

1. **Komposisi demo:** pilih grafik + klaim terpilih + dua hasil dalam satu viewport, atau pertahankan dua prosa lengkap sebagai fokus awal? Rekomendasi: pilihan pertama, dengan teks lengkap tetap dapat dibuka.
2. **Batas suara:** label simulasi di hero dan tombol putar perlu disahkan sebelum membuatnya semakin dramatis. Rekomendasi: jelas “Simulasi pembaca layar”, bukan menyiratkan rekaman uji NVDA.
3. **Aksi ULD:** apakah satu tombol dinamis “Setujui teks ini”/“Simpan & setujui perubahan” lebih mudah daripada dua tombol sekarang? Rekomendasi: satu aksi utama yang jelas sesuai keadaan, dengan tolak/dekoratif terpisah.
4. **Intensitas template:** berdasarkan pilihan pengguna yang sudah ada, lanjutkan variasi A: Sill kuat pada demo dan perbandingan, versi tenang pada editor dan bacaan.

Belum dilakukan: pengujian NVDA/proyektor nyata, galat pemulihan, kontras terukur, playback audio aktual, dan animasi template live secara penuh.
Risiko yang perlu diketahui: perubahan visual yang menyederhanakan tabel/status terlalu jauh bisa membuat klaim hasil tampak lebih kuat daripada buktinya; kurasi harus mempertahankan denominator, held, dan batas evaluasi.
