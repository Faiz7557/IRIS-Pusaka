# Rebuttal: Defense

**1. AI statement: partly survives.** The wording "penyusunan dan revisi draf naskah" is a real risk. But the same appendix was on file when the paper reached Top 6, and the record has no sign the committee flagged it. That makes it something to fix, not proof of disqualification: the team can write Bab 4-5 itself and make the statement precise.

**2. Written work missing: survives as a schedule risk, not a failure.** The content of Bab 4 already exists in eval/results.json, and the README's limitations map straight onto 4.04. "Judul saja" only describes what text extraction found. It does not show that the Turnitin appendix is missing.

**3. Demo differs from the paper: partly survives.** The voice mismatch is real. It can be fixed with a minor Bab 3 revision, which the rules allow. The paper already says cached results are used for the demo, so the cache is not staging. The record calls the `import app` failure "belum dikonfirmasi".

**4. RM2 on real material: partly survives.** The test set was held out, and the thresholds were locked before it was opened. "0 grafik terbit otomatis" with R = 18/18 is the fail-closed gate working, and that answers RM3. Counting the placeholder alt text in G1 is a real flaw and has to be disclosed.

**5. Gates short: weak.** The paper itself marked G2 and G5 "bila waktu memungkinkan" and G7 "ditunda". Reporting them under 4.04 matches Bab 3. Only the full G6 is a genuine gap.

**Decisive point:** Point 4. The rules say "Produk yang sederhana tidak masalah" and require a limitations section. The jury should decide whether honestly reported partial results, held-out but synthetic, plus a working gate on real documents, can count as answering the problem statements.
