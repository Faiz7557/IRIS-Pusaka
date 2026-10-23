# Audit manual pemeriksa angka B2 (set uji, 60 grafik)

Pemeriksa pola (`gate.check_free_text`) menandai 17 angka pada deskripsi B2 sebagai tidak setia
(ε = 0,02 × rentang). Setiap tanda dibaca manual terhadap tabel acuan (`python eval/audit_b2.py`).

| Kategori | Jumlah | Keterangan |
|---|---|---|
| Salah tandai pemeriksa | 1 | syn079: "di atas 500 juta USD" adalah ambang, bukan klaim data |
| Pembulatan/perkiraan di luar ε | 13 | syn011, syn032, syn062 (6), syn068 (5): semua grafik tanpa label nilai, nilai dibulatkan B2 |
| Statistik turunan salah | 3 | syn043 rerata 1.107 (acuan 1.206,8); syn083 rerata 448 (acuan 487,9); syn068 rerata 75,6 (acuan 76,0) |

Presisi pemeriksa: 16/17 tanda benar tidak setia terhadap acuan pada toleransi ε.
Kesalahan B2 yang bukan pembulatan seluruhnya berupa rerata yang dihitung model.

Riwayat pemeriksa: versi pertama (pencocokan per kalimat) menghasilkan 141 tanda yang sebagian besar
salah tandai (nama bulan panjang, tahun di judul, rentang sumbu). Ekstraksi klaim dengan LLM dicoba
dan ditolak karena keluarannya tidak andal. Versi akhir memeriksa per klausa dan diaudit di atas.
Perubahan pemeriksa hanya memengaruhi pengukuran B2 (membuat B2 tampak lebih baik), bukan keluaran SIMAK.
