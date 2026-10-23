---
name: SIMAK
description: Every document element is a numbered library catalog card; every gate check and ULD decision is a dated stamp on its slip.
colors:
  rail: "#1F4D3A"
  rail-deep: "#173B2C"
  rail-ink: "#EEF4F0"
  rail-muted: "#BBD0C3"
  ground: "#F3F6F4"
  card: "#FFFFFF"
  slip-paper: "#FBFCFB"
  ink: "#1B1F1D"
  ink-2: "#47524C"
  line: "#C9D4CE"
  line-soft: "#E1E8E4"
  ruling: "#DCE6F3"
  ruling-ink: "#2F5BA8"
  catalog-red: "#B3261E"
  red-ink: "#8C1D17"
  red-bg: "#FBE4E2"
  red-line: "#E3B4B0"
  stamp: "#5B3FA0"
  stamp-ink: "#4A2C8C"
  stamp-bg: "#EEE8FA"
  stamp-bg-2: "#E0D5F5"
  ok: "#1F6B45"
  ok-bg: "#E2F1E7"
  highlight: "#FFF0A6"
  focus: "#2F5BA8"
  dark-ground: "#141816"
  dark-card: "#1C211E"
  dark-ink: "#E8EFEA"
  dark-ink-2: "#A9B6AE"
  dark-line: "#33403A"
  dark-ruling: "#2A3540"
  dark-ok: "#7FD3A3"
  dark-ok-bg: "#17321F"
  dark-stamp-ink: "#CDBAF7"
  dark-stamp-bg: "#2A2140"
  dark-stamp-bg-2: "#33284F"
  dark-focus: "#9DBBF2"
  dark-highlight: "#4B4312"
typography:
  display:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(3rem, 4.4vw, 4.5rem)"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontFeature: "tnum"
  headline:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 800
    lineHeight: 1.2
  title-card:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 800
    lineHeight: 1.2
  verdict:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 800
    lineHeight: 1.3
  body:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "tnum"
  body-ruled:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: "2rem"
  label:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
    lineHeight: 1.2
  label-small:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.3
  stamp:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 800
    lineHeight: 1.2
    letterSpacing: "0.02em"
  call-number:
    fontFamily: "Atkinson Hyperlegible Mono, ui-monospace, Consolas, monospace"
    fontSize: "0.875rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0.02em"
  numeric:
    fontFamily: "Atkinson Hyperlegible Mono, ui-monospace, Consolas, monospace"
    fontWeight: 400
    fontFeature: "tnum"
  table-head:
    fontFamily: "Atkinson Hyperlegible Next, Segoe UI, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    letterSpacing: "0.04em"
rounded:
  card: "4px"
  stamp: "3px"
  image: "2px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "32px"
  s7: "48px"
  rail-width: "272px"
  hit-min: "44px"
components:
  rail:
    backgroundColor: "{colors.rail}"
    textColor: "{colors.rail-ink}"
    padding: "32px 24px"
    width: "{spacing.rail-width}"
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.rail-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  nav-item-hover:
    backgroundColor: "{colors.rail-deep}"
  nav-item-active:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.rail}"
  button:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "10px 16px"
    height: "{spacing.hit-min}"
  button-primary:
    backgroundColor: "{colors.rail}"
    textColor: "{colors.rail-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "10px 16px"
    height: "{spacing.hit-min}"
  button-primary-hover:
    backgroundColor: "{colors.rail-deep}"
  button-inject:
    backgroundColor: "{colors.card}"
    textColor: "{colors.red-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "10px 16px"
  button-inject-hover:
    backgroundColor: "{colors.red-bg}"
  button-danger:
    backgroundColor: "{colors.card}"
    textColor: "{colors.red-ink}"
    rounded: "{rounded.card}"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.card}"
  button-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.card}"
  input-select:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.card}"
    padding: "9px 12px"
    height: "{spacing.hit-min}"
  textarea:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "{spacing.s3}"
  toolbar:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  catalog-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
  card-head:
    typography: "{typography.title-card}"
    padding: "16px 24px 12px"
  ruled-description:
    typography: "{typography.body-ruled}"
    padding: "0 24px 12px"
  call-number:
    textColor: "{colors.ink-2}"
    typography: "{typography.call-number}"
  slip:
    backgroundColor: "{colors.slip-paper}"
    padding: "16px 24px"
  stamp-pass:
    backgroundColor: "transparent"
    textColor: "{colors.stamp-ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.stamp}"
    padding: "5px 10px"
  stamp-fail:
    backgroundColor: "transparent"
    textColor: "{colors.red-ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.stamp}"
    padding: "5px 10px"
  stamp-held:
    backgroundColor: "{colors.stamp-bg}"
    textColor: "{colors.stamp-ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.stamp}"
    padding: "5px 10px"
  stamp-pending:
    backgroundColor: "transparent"
    textColor: "{colors.ink-2}"
    typography: "{typography.stamp}"
    rounded: "{rounded.stamp}"
    padding: "5px 10px"
  verdict-published:
    backgroundColor: "{colors.ok-bg}"
    textColor: "{colors.ok}"
    typography: "{typography.verdict}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  verdict-failed:
    backgroundColor: "{colors.red-bg}"
    textColor: "{colors.red-ink}"
    typography: "{typography.verdict}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  verdict-held:
    backgroundColor: "{colors.stamp-bg}"
    textColor: "{colors.stamp-ink}"
    typography: "{typography.verdict}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  verdict-idle:
    backgroundColor: "{colors.line-soft}"
    textColor: "{colors.ink-2}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "12px 16px"
  claim-number-faithful:
    textColor: "{colors.ink}"
    typography: "{typography.numeric}"
    padding: "0 2px"
  claim-number-wrong:
    backgroundColor: "{colors.red-bg}"
    textColor: "{colors.red-ink}"
    typography: "{typography.numeric}"
    padding: "0 2px"
  claim-number-focused:
    backgroundColor: "{colors.highlight}"
  poster-figure:
    textColor: "{colors.rail}"
    typography: "{typography.display}"
  queue-card:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.card}"
    padding: "{spacing.s3}"
    height: "72px"
  listen-bar:
    backgroundColor: "{colors.rail}"
    textColor: "{colors.rail-ink}"
    padding: "10px 16px"
  listen-bar-play:
    backgroundColor: "{colors.rail-ink}"
    textColor: "{colors.rail}"
    rounded: "{rounded.card}"
    height: "{spacing.hit-min}"
---

# Design System: SIMAK

## Overview

**Creative North Star: "Kartu Katalog Perpustakaan"**

SIMAK looks like the card catalog of a university library. Every document element (a chart, a diagram, a formula) is a numbered catalog card in white card stock, topped by a thin catalog-red rule and carrying a monospaced call number. Each description sits on blue-ruled lines like a typed card. Below it is a dashed-off slip where the gate checks (cF, cδ, cA, cL) and the ULD's decisions are pressed as slightly rotated, dated rubber stamps. A buckram-green rail binds the pages like a library ledger spine. Its foot carries one poster-scale proof figure from the frozen evaluation.

Density suits a projector: the root size is 18px, controls are at least 44px tall, and verdicts are set at headline weight so the room can read "Terbit · 1 angka keliru sampai ke mahasiswa" from the back row. Status is never carried by colour alone. Every verdict band and stamp pairs an icon with Indonesian words, and the held state also gets a violet diagonal hatch. The surfaces are flat colour on paper. The only patterns are the ruling and the hatch, and the only lift is one soft card shadow.

The world rejects the generic grey SaaS dashboard with coloured pills. It also avoids a glossy AI-startup sheen and the rigid look of a government form. Evidence (numbers, source cells, stamps) always outranks decoration.

**Key Characteristics:**
- White catalog cards on cool card-stock ground, each topped by a 5px catalog-red rule.
- Monospaced call numbers (`SIMAK·e014·hlm 2`, `B2·syn043`) identify every element across pages.
- Descriptions are typed on faint blue ruling, 2rem line pitch.
- Gate checks and ULD decisions are rotated rubber stamps on a slip and are pressed in sequence when a run completes.
- Held equals violet hatch plus words; failure equals catalog red plus words; published equals green band plus words.
- Poster-scale tabular numerals carry the proof (`440/440`, `6 → 5 → 0`).
- One typeface family, Atkinson Hyperlegible Next for text and Mono for evidence, chosen for low-vision legibility.

## Colors

This is a library palette: buckram green, card-stock white, typewriter-ribbon violet and catalog red, with blue ruling kept faint enough to read as printed paper.

### Primary
- **Buckram Green** (rail): the ledger spine. It fills the rail, the listen-mode bar of the generated HTML and the primary button ("Jalankan", "Proses PDF", "Setujui"), and it colours poster figures and the final value of the veraPDF trail. **Deep Buckram** (rail-deep) is its hover and pressed shade.
- **Rail Ink** and **Faded Rail Ink** (rail-ink, rail-muted) are text on the rail: nav labels and wordmark, then the subtitle and proof caption.

### Secondary
- **Stamp Violet** (stamp) and **Ribbon Violet** (stamp-ink): stamp borders and stamp text for passed checks and ULD decisions, plus the held verdict text. The spinner ring and text caret also use stamp violet. **Violet Wash** and **Violet Hatch** (stamp-bg, stamp-bg-2) alternate in the 135° hatch that marks held items. Violet Hatch also serves as the selection colour.

### Tertiary
- **Catalog Red** (catalog-red): the 5px rule on top of every card and figure, the top edge of queue cards, failed stamp borders and wrong-number underlines. **Oxblood Ink** (red-ink) is the text colour for every failure: failed stamps, reasons lists, "tidak", wrong numbers and the inject and danger buttons. **Blush** (red-bg) fills the failed verdict band and wrong-number marks. **Blush Line** (red-line) is the resting border of the inject and danger buttons.
- **Ledger Green** (ok) on **Mint Wash** (ok-bg): used only for the published verdict band ("Terbit · lolos semua pemeriksaan"), the underline under a number that matches the table, and "ya".

### Neutral
- **Card-Stock Ground** (ground): the page behind all cards and the active nav pill.
- **Card White** (card): card, toolbar, button and input fill. **Slip Paper** (slip-paper) is the barely-off-white strip under the dashed slip edge.
- **Catalog Ink** (ink): body text, and the 2px rule under table heads. **Pencil Grey** (ink-2): secondary text, metadata, call numbers and captions.
- **Card Edge** (line): 1.5px card, button and input borders, the dashed slip edge and pending stamps. **Soft Edge** (line-soft): the idle verdict, toolbar row divider, image frames.
- **Blue Ruling** (ruling): the printed lines of description text, the card-head underline and table row rules. **Ruling Ink** (ruling-ink): links and `details` summaries. **Focus Blue** (focus) shares that hue for the 3px focus ring.
- **Highlighter** (highlight): marks the focused claim number and its source row in the table, and the block being read aloud in listen mode.

### Dark scheme (generated student HTML only)
The generated accessible HTML follows `prefers-color-scheme`. Its dark values, the `dark-*` tokens, keep the same roles: a near-black green ground and card, pale ink, lifted green and violet for stamps, a dimmed hatch, a pale focus blue and a dark ochre highlighter. The rail green and the catalog-red top rule do not change between schemes. The ULD web tool is light-only.

### Named Rules
**The Stamp Violet Rule.** Violet belongs to the gate and the ULD. It marks checks that passed, ULD decisions and held items, and nothing else. It is never a link, a button or a decorative accent.

**The Red Means Wrong Rule.** Outside the card-top rule, catalog red appears only where something is wrong or destructive: a failed check, a wrong number reaching students, an injected error, a delete or reject action.

**The Words-With-Colour Rule.** No status is colour-only. Each verdict band and stamp carries an icon and an Indonesian phrase ("Ditahan · menunggu ULD", "cF gagal"). Held additionally carries the hatch.

## Typography

**Display Font:** Atkinson Hyperlegible Next (with Segoe UI, system-ui)
**Body Font:** Atkinson Hyperlegible Next (with Segoe UI, system-ui)
**Label/Mono Font:** Atkinson Hyperlegible Mono (with ui-monospace, Consolas)

**Character:** This is a single humanist family designed by the Braille Institute for low-vision readers. It is heavy at the top (800 for headings, verdicts, stamps and figures) and plain in running text. The Mono cut works like the catalog typewriter: call numbers, claim numbers, table values and stamp times.

Both fonts are self-hosted variable woff2 files (weights 200–800, latin and latin-ext; Next also has italic). The generated HTML inlines only Next normal-latin as a data URI. The root size is 18px, so 1rem equals 18px throughout the web tool. Tabular numerals are on globally.

### Hierarchy
- **Display** (800, clamp(3rem, 4.4vw, 4.5rem), 1, -0.02em, tabular): poster proof figures in Evaluasi (`fig-big`) in buckram green, or oxblood for the B2 count. The rail proof figure is a smaller sibling (800, clamp(2rem, 2.7vw, 2.75rem)). Tally and score figures are a mid tier at 800, 2–2.5rem, line-height 1.
- **Headline** (800, 2.25rem, 1.2, -0.01em): the page h1, one per page. It drops to 1.75rem at ≤1200px.
- **Title** (800, 1.5rem, 1.2): section h2 ("Antrean tinjauan ULD", gate cards). **Card title** (800, 1.25rem) sits in every card head.
- **Verdict** (800, 1.25rem, 1.3): verdict band text. It is set big on purpose because it is the sentence judges must read.
- **Body** (400, 1.0625rem, 1.55): running text. Page intros cap at 68ch. Ruled descriptions use the same size on a 2rem line pitch, capped at 75ch.
- **Label** (700, 0.9375rem, 1.2): buttons, selects, toolbar labels, field labels and group headings.
- **Small label** (600, 0.875rem, 1.3): card-head metadata ("sesi ini", "kriteria terkunci"), slip label and legends. Table heads use this size at 700, uppercase, with 0.04em tracking.
- **Stamp** (800, 0.875rem, 0.02em): stamp text. The stamp time is Mono 600 at 0.75rem, the smallest text in the system.
- **Call number / numeric** (Mono 600, 0.875rem, 0.02em): call numbers. Claim numbers, numeric table cells, file names and the run manifest are also in Mono.

### Named Rules
**The Typewriter Evidence Rule.** Anything a reader might check against a source goes in Atkinson Hyperlegible Mono: call numbers, claim numbers, numeric cells, timestamps, file names. Prose never goes in Mono.

**The Back-Row Rule.** The root stays at 18px. Body text never goes below 0.875rem. Only stamp timestamps (0.75rem) and the compact stamps on queue cards (0.72rem) go smaller.

## Layout

The layout is a two-column shell. A fixed 272px buckram rail on the left is sticky at full viewport height and holds the wordmark, three nav items and the proof figure pinned to its foot. To its right is a fluid main column with padding of 32px top and clamp(16px, 3vw, 44px) at the sides. At ≤1200px the rail collapses into a wrapping top bar. The wordmark shrinks to 1.5rem, the subtitle and proof figure are hidden, and nav items become compact pills.

Spacing follows a 4px-based scale (s1–s7: 4, 8, 12, 16, 24, 32, 48px). The 24px step is the standard gutter between cards. Card internals use 16px vertical and 24px horizontal padding, which tightens to 16px horizontal at ≤1200px.

Recurring grids:
- **Equal halves** (1fr 1fr, 24px gap): Sisi A and Sisi B always get the same width, because neither side is privileged. They stack at ≤760px.
- **Evidence below**: a 1.7fr / 1fr split under the halves for the chart and scoreboard against the reference table, stacking at ≤760px.
- **Queue split**: a 280–380px list of queue cards next to a fluid element-card detail, stacking at ≤1000px.
- **Summary row**: three cards (0.9 / 1.45 / 0.85fr) that become two at ≤1200px and one at ≤760px.
- **Tables** scroll inside their own wrapper (`twrap`). On narrow screens the k/n and CI columns fold into the value cell.

The generated student HTML is a single column (max 46rem, centred) under a sticky buckram listen-mode bar.

Breakpoints are 1200px (rail collapses), 1000px, 760px (halves stack) and 600px (secondary table columns fold).

## Elevation & Depth

Depth is mostly material, not light. Cards are white on a slightly cooler ground with a 1.5px card-edge border, and the slip below a dashed edge sits on near-white slip paper. One soft, green-tinted ambient shadow lifts catalog cards and the selected queue card. Nothing else casts a shadow, and there are no glows. Pattern carries meaning instead of depth: the blue ruling is printed lines, and the violet hatch means held.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 1px 2px rgba(23, 59, 44, .06), 0 6px 18px -8px rgba(23, 59, 44, .18)`): every catalog card at rest, and the queue card currently under review.

### Named Rules
**The One Shadow Rule.** Only one shadow value exists. Cards rest on it, and the reviewed queue card gains it. Stamps, buttons, bands and inputs stay flat.

**The Pattern-Is-Meaning Rule.** The only gradients allowed are hard-stop pattern gradients: the ruling (horizontal lines every 2rem) and the hatch (135° stripes, 7/14px on stamps and 9/18px on bands). A smooth decorative gradient has no place here.

## Shapes

Cards, buttons, inputs, bands and nav pills share one gently squared corner (4px). Stamps are slightly tighter (3px) and sit at a slight tilt: -1.5° by default, +1.2° on every third stamp and -0.6° on every fourth, so a slip reads as hand-pressed. Borders are 1.5px throughout, with two exceptions. Stamps get a heavy 2.5px border so they read as inked impressions. Table heads end on a 2px ink rule. Dashed strokes always mean "not settled yet": the slip's perforated edge, held and pending stamps, the file picker and injected-number outlines. Every card is clipped (`overflow: hidden`) so its 5px catalog-red top rule runs edge to edge.

## Components

### Buttons
Tactile and plain, like the brass buttons on a card drawer.
- **Shape:** 4px corners, 1.5px border, min-height 44px, 10px × 16px padding, label type (700, 0.9375rem) with an optional 24px line icon before the text.
- **Default:** white with a card-edge border. On hover the border darkens to pencil grey. On press it shifts down 1px.
- **Primary:** buckram green with rail ink text ("Jalankan", "Proses PDF", "Setujui", "HTML aksesibel + mode dengar"). Hover goes to deep buckram.
- **Inject:** white with a blush-line border and oxblood text and the pen icon ("Ubah satu angka", "Tukar label–nilai"). Hover fills with blush and turns the border catalog red.
- **Danger:** the same blush-line and oxblood treatment for "Tolak" and "Hapus sesi".
- **Quiet:** borderless, transparent and pencil grey ("Kembalikan").
- **Toggle (aria-pressed):** filled with ink and white text ("Antrean" / "Semua gambar").
- **Disabled:** 50% opacity, not-allowed cursor and no press shift.

### Inputs / Fields
- **Style:** white, 1.5px card-edge border, 4px corners, 44px minimum height, 9px × 12px padding, 600 weight. Textareas use body type at 1.6 line-height and are at least 140px tall with vertical resize. The file picker is a dashed-border button-label 64px tall with the document icon.
- **Focus:** the global 3px Focus Blue outline at 2px offset. The caret is stamp violet.

### Navigation
- **Rail nav:** a vertical stack of 4px-corner items at 600 weight and body size, each with a line icon (layers, doc, chart) and a 12px gap. Hover fills with deep buckram. The current page (aria-current) is a card-stock pill with buckram 800 text, an inverted swatch of the page ground. The focus ring turns rail ink on the rail.
- **Collapsed (≤1200px):** a wrapping row of compact pills (8px × 12px, 0.9375rem) beside the wordmark.

### Catalog Card (signature)
The unit of the whole system.
- **Corner Style:** 4px, clipped.
- **Background:** card white, 1.5px card-edge border, card-lift shadow, and a 5px catalog-red rule across the top.
- **Head:** the title (800, 1.25rem) sits on the left and a Mono call number or a small metadata label sits on the right, aligned to the baseline. The head ends on a 1.5px blue-ruling underline.
- **Ruled description:** body text on a 2rem ruled line pitch, capped at 75ch. Claim numbers inside it are Mono. A faithful number has a 3px ledger-green underline, and a wrong one is blush-filled with oxblood text and a catalog-red underline. An injected number gets a dashed red outline. Clicking or focusing a number highlights it and its source table row with the highlighter.
- **Internal padding:** 16px × 24px.

### Stamps and Slip (signature)
- **Slip:** a strip below a 1.5px dashed card-edge, on slip paper, holding a small "Slip pemeriksaan" label followed by wrapped stamps (8px × 12px gap).
- **Stamp:** an inline 2.5px-bordered impression with 3px corners, 800 weight at 0.875rem, an icon and a Mono timestamp, tilted per the Shapes rule. **Pass:** violet border and ribbon-violet text ("cF lulus 14.05", "ULD setujui"). **Fail:** catalog-red border with oxblood text ("cA gagal", "Tidak diperiksa · tetap terbit"). **Held:** dashed violet border on the violet hatch ("ULD · menunggu"). **Pending:** dashed card-edge border in pencil grey ("cF", "K = ∅ · tanpa pemeriksaan otomatis").
- **Motion:** when a run completes or a ULD decision is saved, the stamps are pressed in sequence. Each one scales from 1.35 with an extra -6° tilt and a 1.5px blur down to rest over 0.5s on `cubic-bezier(.16, 1, .3, 1)`, with a 110ms stagger. With reduced motion there is no animation and all transitions are off.

### Verdict Bands
A full-width band inside the card under the head, with 4px corners, 12px × 16px padding, verdict type and a 1.4em icon. **Published:** ledger green on mint. **Failed (B2 published wrong):** oxblood on blush with the alert icon. **Held:** ribbon violet on the 9/18px hatch with the hold icon. **Idle:** pencil grey on soft edge at body size ("Belum dijalankan"). Under a held band, a reasons list gives each cause in oxblood with a cross icon.

### Toolbar
A white bordered bar (4px, 12px × 16px padding) that groups the demo controls into rows: picker, Jalankan, Kembalikan and status on one row, and the four inject buttons on the next. Rows are divided by a soft-edge rule. A busy status shows a small violet spinner ring.

### Queue Card
A list button 72px tall: a 4px catalog-red top edge, a 64 × 48 thumbnail, a Mono call number, an element type in bold and a flat (untilted, 0.72rem) status stamp. While one card is under review, the others dim to 50% opacity and come back on hover or focus. The selected card gets an ink border and the card-lift shadow.

### Poster Figures and Tallies
Proof numbers are set big, in Next 800 with tabular figures. Examples: `440/440` on the rail, `6 → 5 → 0` failed rules (the final value in buckram), the G3 versus block (buckram for SIMAK, oxblood for B2), and the tally and score definition lists with a right-aligned number beside a pencil-grey caption.

### Data Tables
Full width at 0.9375rem. The caption is left-aligned, bold and pencil grey. The head is uppercase small label on a 2px ink rule. Rows are separated by 1.5px blue ruling, numeric columns are right-aligned Mono, and differences (|T1 − T2|) are in oxblood.

### Listen-Mode Bar (generated HTML)
A sticky buckram bar holding the "SIMAK" wordmark, Putar (inverted: rail-ink fill, buckram text), Jeda, previous and next icon buttons, the Kecepatan select and a live voice status. Bar buttons are transparent with a 40% rail-ink border and are 44px tall. The block being read is highlighted. Figures in the generated HTML reuse the catalog card: 5px red rule, a stamp ("Dihasilkan otomatis · angka terverifikasi", "Menunggu tinjauan ULD" on the hatch) and a collapsible data table.

## Do's and Don'ts

### Do:
- **Do** give every element its own catalog card with a 5px catalog-red top rule and a Mono call number in the form `SIMAK·<id>·hlm <n>`.
- **Do** record every gate check and ULD decision as a stamp on the card's slip, with an icon, words and a Mono time where one exists.
- **Do** mark held items with the violet hatch and words ("Ditahan · menunggu ULD") together, never with one alone.
- **Do** set checkable values (claim numbers, numeric cells, call numbers, times) in Atkinson Hyperlegible Mono with tabular figures.
- **Do** keep Sisi A and Sisi B as equal halves (1fr 1fr) with identical card anatomy.
- **Do** keep controls at least 44px tall and text at 0.875rem or above (stamp times and queue stamps excepted) on the 18px root.
- **Do** honour `prefers-reduced-motion`: stamps appear without the press and transitions stop.

### Don't:
- **Don't** use stamp violet for links, primary buttons or decoration. It belongs to the gate and the ULD.
- **Don't** use catalog red except for the card-top rule or something wrong or destructive.
- **Don't** add smooth gradients, glows or extra shadow levels. Only the ruling, the hatch and the single card-lift shadow exist.
- **Don't** render status as a coloured pill or badge without words. That is the grey-SaaS-dashboard look this world refuses.
- **Don't** let decoration outrank evidence. Poster figures must be real, frozen results, and nothing is implied that has not happened.
