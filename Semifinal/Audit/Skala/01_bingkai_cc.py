# -*- coding: utf-8 -*-
"""Langkah 1: bingkai sampel (sampling frame) dari indeks kolumnar Common Crawl (publik).
Bingkai = seluruh tangkapan PDF (HTTP 200) pada host *.ac.id pada satu panen (crawl).
Catatan (uji 30 Sep 2026): kolom content_languages KOSONG untuk PDF, sehingga bahasa ditentukan setelah unduh (03_audit_pdf.py). Keluaran: bingkai.parquet + ringkasan.
Jalankan: python 01_bingkai_cc.py CC-MAIN-2026-39
"""
import duckdb, gzip, sys, time, urllib.request, os

crawl = sys.argv[1] if len(sys.argv) > 1 else "CC-MAIN-2026-39"
out = f"bingkai_{crawl}.parquet"
paths_url = f"https://data.commoncrawl.org/crawl-data/{crawl}/cc-index-table.paths.gz"
paths = gzip.decompress(urllib.request.urlopen(paths_url, timeout=60).read()).decode().split()
warc = ["https://data.commoncrawl.org/" + p for p in paths if "subset=warc" in p]
print("berkas parquet subset=warc:", len(warc))

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; SET threads=16;")
t0 = time.time()
con.execute(f"""
COPY (
  SELECT url, url_host_name AS host, url_host_registered_domain AS dom, content_languages AS bahasa,
         content_mime_detected AS mime, content_truncated AS terpotong, fetch_time,
         warc_filename, warc_record_offset AS off, warc_record_length AS len
  FROM read_parquet({warc})
  WHERE url_surtkey >= 'id,ac,' AND url_surtkey < 'id,ac-'
    AND content_mime_detected = 'application/pdf' AND fetch_status = 200
) TO '{out}' (FORMAT PARQUET)
""")
print("selesai dalam", round(time.time() - t0), "detik")
print(con.execute(f"SELECT count(*), count(DISTINCT dom), sum(CASE WHEN terpotong IS NULL THEN 1 ELSE 0 END) FROM '{out}'").fetchall())

# ringkasan bingkai dan stratum materi kuliah: jalankan 01b_ringkasan_bingkai.py
