# JDS — 25 Years at Amplify

A retro 8-bit anniversary card for John Stewart's 25th anniversary at Amplify
(2001 → 2026), delivered as a real ZX Spectrum tape image (`.tap`) that runs
in any Spectrum emulator. JDS owns an actual Spectrum, so the medium is the
message.

Designed in the spirit of the recipient: **erudite, curmudgeonly, allergic
to pomp**. No fanfare. Just a chunky title, a dithered portrait, a stat line
or two, and a marquee on row 23.

## What's in the box

| File | Role |
|------|------|
| `card.tap` | **The deliverable.** Drag into Fuse, type `LOAD ""`. |
| `card.scr` | 6912-byte ZX Spectrum SCREEN$ binary (avatar + title art). |
| `card.bas` | zxb (Boriel's ZX BASIC) source. Loads SCREEN$, prints stats, plays a 5-note tune, scrolls a marquee. |
| `card.html` | Original web mockup, kept as design reference. |
| `card_preview.png` | PNG render of the SCREEN$ for sanity-checking the bitmap. |
| `build_screen.py` | Python tool: `jds_avatar.png` → dithered/composited 256×192 → `card.scr`. |
| `verify_tap.py` | Parses a `.tap`, prints block table and validates checksums. |

## Build

Prereqs (one-time):

```bash
pip install zxbasic Pillow
```

Then:

```bash
# 1) Fetch the avatar (any 1:1-ish photo at jds_avatar.png works)
# 2) Composite & dither into card.scr
python3 build_screen.py

# 3) Compile the BASIC source + INCBIN'd SCREEN$ data into a .tap
zxbc -B -a -f tap card.bas -o card.tap

# 4) Verify
python3 verify_tap.py card.tap
```

## Run

Install [Fuse](https://fuse-emulator.sourceforge.net/) (macOS):

```bash
brew install --cask fuse-emulator
```

Launch Fuse, then:

1. **File → Open** → `card.tap`
2. Type `J` (LOAD), then `Shift+P Shift+P` for `""`, then **Enter**
3. (Or just press F5 / Tape Browser → start, depending on Fuse build)

Should also load in **ZEsarUX**, **Spectaculator**, **Speccy**, or any
RetroArch ZX core.

## Design notes

- 256 × 192, 8 colors with the famous 8 × 8 attribute grid.
- Avatar is Floyd-Steinberg dithered to 1-bit (the Spectrum doesn't care
  what the photo originally looked like).
- Bottom 8 rows are deliberately left as plain text via `PRINT AT` — the
  Spectrum's ROM font is crisper than anything we'd render into the bitmap.
- The marquee uses the `mm = m + m; mm(i TO i+31)` trick — no wrap logic.
- Default zxbc `ORG` is $8000 (32768); SCREEN$ is INCBIN'd inside the code
  block and `LDIR`-copied into screen RAM at $4000 on entry.
