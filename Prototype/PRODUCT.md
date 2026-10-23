# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary viewers of this prototype are competition judges at the ICC 2026 (Campus Data Week) final, watching a 15-minute live demo on a projector. The product being demonstrated is a work tool for staff of the Unit Layanan Disabilitas (ULD) at Indonesian universities, who upload lecture PDFs and review held elements; its end beneficiaries are blind students who read the output with a screen reader (NVDA) and students who listen via the listen mode. The UI must convince judges while remaining credible as a ULD work tool.

## Product Purpose

SIMAK (Sistem Ilustrasi Materi Aksesibel untuk Kuliah) remediates Indonesian-language lecture PDFs: it completes tags and structure (PDF/UA-1), builds chart descriptions from extracted data tables with statistics computed by code, and holds every output it cannot verify in a ULD review queue (fail-closed gate). Success: no wrong description is ever published without a marker.

## Positioning

The value is not a smarter AI but a guarantee: every description is either verified against data claim-by-claim (equations 5 and 7 of the proposal) or visibly held for human review. A direct VLM (baseline B2) publishes whatever it writes; SIMAK does not.

## Operating Context

Pages: Remediasi & Tinjauan (upload, veraPDF B0/B1/D, review queue), Demo Gerbang (B2 vs SIMAK side by side with error injection), Evaluasi (G1/G3/G4/G6 with Wilson intervals), and the generated accessible HTML output with listen mode (Web Speech, id-ID). Runs locally (FastAPI) during the demo; VLM responses for demo charts are cached.

## Capabilities and Constraints

- Static HTML/CSS/JS served by FastAPI; no frontend framework.
- Language: Indonesian throughout.
- Terminology from the proposal must stay: B0/B1/B2/D, G1–G7, cF/cδ/cA/cL, Fk, δ, θe, ε, R, klaim (e, m, v), terbit otomatis, antrean tinjauan, fail-closed.
- Formulas are always held; vector figures are held; decorative images get alt="".

## Brand Commitments

Product name SIMAK; team IRIS (Universitas Airlangga). No binding colors or logo: the visual identity is free to define.

## Evidence on Hand

Real evaluation results in eval/results.json (frozen 12 Oct 2026), audit in eval/audit_b2.md, synthetic charts in data/synth, six real lecture PDFs from Common Crawl in data/cc (not to be redistributed). No user testing with blind students yet (G7 deferred); do not imply it happened.

## Product Principles

1. Verified or visibly held: status is never ambiguous.
2. Show the evidence: every number traces to its source cell.
3. Honest reporting: failures and limits are shown, not hidden.
4. The tool itself must be accessible to the people it serves.

## Accessibility & Inclusion

WCAG 2.2 AA for every UI page and the generated HTML: keyboard operable, screen-reader labelled, contrast AA in light and dark, reduced motion respected.
