# CLAUDE.md — context for future sessions

## What this project is

A one-shot anniversary card for John Stewart (JDS, `jds@amplify.com`,
SVP Research & Measurement, Amplify hire date 2001-05-01 — 25 years on
2026-05-01). Deliverable is a ZX Spectrum `.tap` because JDS owns a real
Spectrum (per Slack: "the beautiful spectrum I have", linked
retrogames.biz). The medium is part of the joke.

## Tone — non-negotiable

JDS is **erudite, curmudgeonly, anti-pomp**. He explicitly said today
("I seek not attention", "wtf is this 25 year icon", "from the mesozoic!").
The card leans in: the gag is that we made it anyway, and packed it with
in-jokes only he and a few colleagues will get.

If iterating on copy: stay dry, never effusive. No "thank you for your
service" energy. Self-deprecating-on-his-behalf is fine; reverent is wrong.

## Personality color used in the card (sourced from Slack)

- **Common Lisp loyalist**: "it's been so good to be back in Lisp" / "things
  working right on the first try with strangely high frequency" — the
  marquee quotes this verbatim.
- **JVM hater**: "somehow I just can't get myself back onto the JVM. Maybe
  cuz Ellison owns it now?" — hence "TONGUES: LISP, FORTH, NOT JVM".
- **Forth evangelist**: he told his kid Ansel to learn Forth, "a lesson in
  encapsulation and composition he'll never forget".
- **Erudite flexes**: drops Kafka's *Metamorphosis* unprompted; published a
  Lexile R²>0.94 formula in #fun-ai for fun.
- **"From the mesozoic" / "I seek not attention"** are direct quotes from
  the 25-year-icon Slack thread (2026-04-28).

User suggested trophies (kept verbatim in card):
- longest-lived schema (objet)
- inventor of marvelous oddities
- deepest thinker

## Build pipeline

```
jds_avatar.png ──► build_screen.py ──► card.scr (6912 bytes)
                                          │
                          INCBIN inside ──┘
                                          │
                       card.bas ──► zxbc -B -a -f tap ──► card.tap
```

- `build_screen.py` is the only place the layout lives — title position,
  avatar crop bias, attribute color zones, hearts row, banner copy.
- `card.bas` is the runtime: `LDIR` SCREEN$ to $4000, print stats, beep
  tune, marquee loop with `INKEY$` exit.
- `verify_tap.py` is a sanity check (checksum + block-type table). Not
  needed for the build; useful when changing zxbc flags.

## ZX Spectrum constraints worth remembering

- 256×192 mono pixel bitmap + 32×24 attribute grid. Each attribute byte:
  `FLASH | BRIGHT | PAPER<<3 | INK`. **Color clash** means two colors max
  per 8×8 cell — don't try to paint a multicolored portrait.
- Pixel-row layout is the famous interleaved scheme; see
  `build_screen.py` `for y in range(H)` for the address calc.
- 32-column PRINT width. Lines longer than 32 chars wrap and break the
  layout. `card.bas` lines were measured against this.
- Default zxbc ORG is $8000. SCREEN$ at $4000 (16384), 6912 bytes. The
  `LDIR` in `card.bas` copies our embedded blob into screen RAM on entry.

## Files: deliverable vs. scaffolding

- **Deliverable**: `card.tap`. That's it.
- **Source-of-truth**: `card.bas`, `build_screen.py`. Edit these to change
  anything. Never hand-edit `.scr` or `.tap`.
- **Reference**: `card.html` (original web mockup; lives in `card.html`'s
  own design — do not let it drift in sync with the Spectrum version).
- **Generated** (gitignored): `card_preview.png`, `jds_avatar.png`,
  `*.bin`/`*.lst`, etc. Regenerate via `build_screen.py`.

## Avatar source

`jds_avatar.png` is JDS's Slack profile photo
(`https://avatars.slack-edge.com/2016-03-03/24200414038_c76e63284efa1511767f_original.png`).
It's a co-worker's photo so it's gitignored. Re-fetch with `curl` if
missing; `build_screen.py` expects a roughly square 1:1 photo at that path.

LinkedIn (`linkedin.com/in/johndanielstewart/`) returns 404 for
WebFetch — don't waste a turn re-trying it.

## Branches

- `main` — the original 25-year anniversary card.
- `birthday` — birthday variant (HAPPY BIRTHDAY splash, 57 hearts = his
  age uncounted-out-loud, youthfulness/candle-overflow selfcheck,
  `(incf age)` finale signed "- AARON").

## Publishing (web)

- **Public repo**: `github.com/aaronharnly/jds-card` (renamed from
  `jds25`). Gets **deliverables only**: `card.tap`, `index.html`,
  `jsspeccy/`. NEVER push this source repo there — CLAUDE.md/README
  contain Slack-mined personal notes.
- Live page: `https://aaronharnly.github.io/jds-card/` (GitHub Pages,
  main branch, root). Old `…/jds25/` Pages URL is dead (Pages doesn't
  redirect renames); old raw.githubusercontent `jds25` URLs still work.
- Publish loop: build → `cp card.tap index.html /tmp/jds25-publish/` →
  commit/push there (HTTPS + gh credential helper). If the clone is
  missing: `git clone https://github.com/aaronharnly/jds-card.git`.
  Pages deploys in ~1-2 min; verify with an md5 poll, not eyeballs.
- `gh` CLI is authed (aaronharnly); SSH key also works.
- qaop fallback link:
  `https://torinak.com/qaop/#l=https://raw.githubusercontent.com/aaronharnly/jds-card/main/card.tap`

## Web page (index.html) hard-won facts

- The `JSSpeccy()` factory returns ONLY `{openUrl, setZoom, onReady,
  exit, fullscreen…}` — no start/pause, no internal Emulator access.
  Working audio requires starting inside a user gesture, so the page
  uses JSSpeccy's own start button stretched invisibly over the screen
  ("CLICK TO SWITCH ON"). Don't reintroduce `autoStart`.
- The menu bar nests inside the canvas's parent — find the start button
  with `:scope > button`, not `querySelector('button')`.
- Don't schedule one-shot UI fixup with requestAnimationFrame (stalls in
  hidden tabs); tidy() runs synchronously post-factory.
- Cache-freshness: `fetch('card.tap', {cache:'reload'})` primes the HTTP
  cache before the emulator's own fetch of the same URL.
- zxbc may not be on PATH: `/opt/miniconda3/bin/zxbc`.
- zxbasic strings are 0-indexed — see typeSrc/typeLine in card.bas.
- Local preview: `.claude/launch.json` serves the dir on :8765.

## Don't

- Don't add a sentimental message. JDS will hate it.
- Don't widen scope beyond the card (no "while we're here, let me also…").
- Don't commit `jds_avatar.png` (it's a coworker's photo).
- Don't push to a remote without asking.
