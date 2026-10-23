# Pembukaan Pembela

**1. MVP sudah nyata dan sejalan dengan Bab 3 (bobot 30%).** Prototipe memuat pipeline, `gate`, `pdfa11y`, antrean ULD "setujui/ubah/tolak/dekoratif", serta Demo Gerbang dengan tombol "suntik kesalahan" yang memperlihatkan "B2 tetap terbit sementara SIMAK menahan". Panitia sendiri menulis "Produk yang sederhana tidak masalah." Keberatan bahwa `import app` gagal di laptop ini menyangkut paket yang tidak terpasang (google-genai, veraPDF). Arsitektur aplikasinya tidak rusak, dan masalah itu bisa dibereskan dalam hitungan jam. 698 respons VLM yang di-cache sesuai dengan rencana paper ("hasil dokumen contoh di-cache"). Itu respons asli, jadi bukan demo palsu.

**2. Klaim inti terbukti dengan angka.** RM3 menjanjikan "tidak ada deskripsi keliru yang terbit tanpa penanda". Hasil beku: Fk terbit 440/440 [0,991; 1,00], injeksi tertahan 137/138, sedangkan B2 menerbitkan 60/60 grafik dengan "17 angka tidak setia pada 7/60 grafik". Pada dokumen nyata, "0 grafik terbit otomatis". Hasil ini sesuai dengan janji fail-closed, bukan kegagalan.

**3. Bahan Bab 4 sudah ada, tinggal ditulis.** Bab 4 meminta hasil uji "memakai metrik yang ditulis di Bab 3" dan subbab Keterbatasan. G1, G3, G4, dan G6 ringan sudah berselang Wilson. G2 dan G5 sejak semifinal ditulis "bila waktu memungkinkan", dan G7 "ditunda", jadi ketiganya sah masuk subbab (04) dan tidak melanggar konsistensi dengan draf.

**4. Disiplin metode menguatkan sesi tanya jawab (20%).** Ambang dikunci pada set dev sebelum set uji dibuka. Kegagalan v1 (Fk 0,937) dicatat terbuka dan melahirkan aturan cL. README menulis batasannya "apa adanya". Juri yang menanyakan kelemahan akan mendapati tim sudah menjawabnya lebih dulu.

**5. Inovasi dan dampak (10%) berpijak pada data.** Ada 1.727 mahasiswa tunanetra, dan audit tim menemukan 0/28 PDF lulus PDF/UA-1 serta teks alternatif hanya 2,6%. Nilai jualnya adalah jaminan, bukan "AI yang lebih cerdas". Ini posisi yang khas dan bisa dipertahankan.

**Konsesi:**
- Lampiran A menyebut AI dipakai untuk "penyusunan dan revisi draf naskah". Ini bertentangan dengan 7.2.4 dan tidak bisa dibela. Praktiknya harus diperbaiki dan pernyataannya ditulis ulang dengan jujur.
- Mode dengar memakai ElevenLabs, padahal paper menyebut Web Speech API. Selisih ini harus diselaraskan atau diungkapkan.
- Sampel uji kecil (4 dokumen sintetis, 6 dokumen nyata). Selain itu, R = 18/18 pada dokumen nyata berarti semua gambar ditahan, dan ini harus dilaporkan terus terang.
- Bab 4-5 dan Turnitin final belum ada, sedangkan waktu tersisa sekitar 2 hari.

Kekurangan di atas menyangkut kelengkapan yang masih bisa dikejar, dan landasan proyeknya tetap utuh. Karena itu proyek ini layak lanjut sebagaimana dijelaskan.
