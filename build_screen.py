"""
Build a ZX Spectrum SCREEN$ (.scr) for JDS's 25th anniversary card.

Output: card.scr (6912 bytes) - 256x192 mono bitmap + 32x24 attribute grid.

Layout:
  Rows 0-15 (top half, 128 px): avatar on left, chunky title on right.
  Rows 16-23 (bottom 64 px): blank — BASIC PRINTs stats here at runtime.

Spectrum screen memory layout:
  - 6144 bytes pixel data, organized in three 2048-byte thirds.
  - Inside each third, rows are interleaved: line offset = (y_in_third & 7) << 8 | (y_in_third >> 3) << 5
  - 768 bytes attribute data (one byte per 8x8 cell): bits 0-2 INK, 3-5 PAPER, 6 BRIGHT, 7 FLASH.
"""

from PIL import Image, ImageOps, ImageDraw, ImageFilter

W, H = 256, 192
AVATAR_PATH = "jds_avatar.png"
OUT_PATH = "card.scr"

# Paper/ink colors (use 1=blue paper / 7=white ink for upper half, with bright)
# Spectrum colors: 0=black 1=blue 2=red 3=magenta 4=green 5=cyan 6=yellow 7=white
ATTR_TITLE = (7 << 3) | 0 | (1 << 6)   # paper=7(white) ink=0(black) bright — for the title strip
ATTR_AVATAR = (0 << 3) | 7             # paper=0(black) ink=7(white) — avatar dither cells
ATTR_TITLE_AREA = (0 << 3) | 6 | (1 << 6)  # paper=black ink=yellow bright — title text panel
ATTR_BANNER = (2 << 3) | 7 | (1 << 6)  # paper=red ink=white bright — top banner
ATTR_DEFAULT = (0 << 3) | 7            # paper=black ink=white — bottom area (BASIC text)
ATTR_HEARTS = (0 << 3) | 2 | (1 << 6)  # paper=black ink=red bright — heart row
ATTR_LABEL = (0 << 3) | 5 | (1 << 6)   # paper=black ink=cyan bright — labels
ATTR_VALUE = (0 << 3) | 7 | (1 << 6)   # paper=black ink=white bright — values

# 5x7 chunky pixel font for the big title text.
# Each glyph is 5 wide x 7 tall. We'll scale x3 -> 15x21 px for "JDS" headline,
# and x2 -> 10x14 for "LEVEL 25" / "2001-2026".
FONT_5x7 = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01110"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","10101","01010"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","10001","01010","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00010","00100","01000","11111"],
    '3': ["11110","00001","00001","01110","00001","00001","11110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","10000","11110","00001","00001","11110"],
    '6': ["01110","10000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00001","01110"],
    '-': ["00000","00000","00000","11111","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","00000","00100"],
    ':': ["00000","00100","00000","00000","00000","00100","00000"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '/': ["00000","00001","00010","00100","01000","10000","00000"],
}


def draw_text(canvas: Image.Image, text: str, x: int, y: int, scale: int, color: int = 0):
    """Draw text using the 5x7 bitmap font, scaled. color = 0 (black) or 255 (white)."""
    px = canvas.load()
    cur_x = x
    for ch in text:
        glyph = FONT_5x7.get(ch.upper(), FONT_5x7[' '])
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            xx = cur_x + col * scale + dx
                            yy = y + row * scale + dy
                            if 0 <= xx < W and 0 <= yy < H:
                                px[xx, yy] = color
        cur_x += (5 + 1) * scale  # 1px gap between chars


def text_width(text: str, scale: int) -> int:
    return len(text) * (5 + 1) * scale - scale


def make_avatar_block(av_path: str, size_px: int) -> Image.Image:
    """Load avatar, crop to face area, dither to 1-bit at size_px x size_px."""
    src = Image.open(av_path).convert("L")
    # Boost contrast and slight sharpen so dither preserves face features
    src = ImageOps.autocontrast(src, cutoff=3)
    # The Slack avatar shows head & shoulders centered; crop tighter to the head
    w, h = src.size
    crop_size = int(min(w, h) * 0.92)
    cx, cy = w // 2, int(h * 0.46)  # bias slightly upward to keep face
    half = crop_size // 2
    left = max(0, cx - half)
    top = max(0, cy - half)
    right = min(w, left + crop_size)
    bottom = min(h, top + crop_size)
    src = src.crop((left, top, right, bottom))
    src = src.resize((size_px, size_px), Image.LANCZOS)
    src = src.filter(ImageFilter.UnsharpMask(radius=1.0, percent=120, threshold=2))
    src = ImageOps.autocontrast(src, cutoff=2)
    # Floyd-Steinberg dither to 1-bit
    bw = src.convert("1", dither=Image.FLOYDSTEINBERG)
    return bw


def main():
    # Canvas in palette: 0 = ink (black), 255 = paper (white) — we'll invert per-attribute later.
    canvas = Image.new("L", (W, H), 255)  # start with paper=white
    draw = ImageDraw.Draw(canvas)

    # ---- TOP BANNER (rows 0..1, y 0..15) ----
    # Solid black strip with white text "AMPLIFY ENT. SYSTEM"
    draw.rectangle([0, 0, W - 1, 15], fill=0)
    banner = "AMPLIFY ENT. SYSTEM"
    bw = text_width(banner, 1) * 2
    draw_text(canvas, banner, (W - bw) // 2, 4, scale=2, color=255)

    # ---- AVATAR (rows 2..13, y 16..111: 96x96 px in cells (1..12, 2..13)) ----
    AV_SIZE = 96
    avatar = make_avatar_block(AVATAR_PATH, AV_SIZE)
    # Paste at x=8 (col 1), y=16 (row 2). Avatar is 1-bit; black=1=ink, white=0=paper.
    # When pasted into our "L" canvas: black=0, white=255 — same convention.
    avatar_l = avatar.convert("L")
    canvas.paste(avatar_l, (8, 16))

    # Optional 1-pixel frame around avatar
    draw.rectangle([7, 15, 8 + AV_SIZE, 16 + AV_SIZE], outline=0)

    # ---- TITLE PANEL (right of avatar, cols 14..30 = x 112..247) ----
    title_x = 116
    # "JDS" big — scale 4 -> 5*4=20 wide per char, 7*4=28 tall
    draw_text(canvas, "JDS", title_x, 22, scale=4, color=0)
    # "LEVEL 25" — scale 2
    draw_text(canvas, "LEVEL 25", title_x, 60, scale=2, color=0)
    # Underline
    draw.rectangle([title_x, 76, title_x + text_width("LEVEL 25", 2), 78], fill=0)
    # "2001-2026" — scale 2
    draw_text(canvas, "2001-2026", title_x, 84, scale=2, color=0)

    # Decorative pixel "stars" / sparkles around title
    for sx, sy in [(110, 28), (240, 32), (108, 96), (242, 96), (170, 100)]:
        draw.rectangle([sx, sy, sx + 1, sy + 1], fill=0)
        draw.rectangle([sx - 2, sy + 1, sx - 2, sy + 1], fill=0)
        draw.rectangle([sx + 3, sy + 1, sx + 3, sy + 1], fill=0)
        draw.rectangle([sx + 1, sy + 2, sx + 1, sy + 2], fill=0)
        draw.rectangle([sx + 1, sy - 1, sx + 1, sy - 1], fill=0)

    # ---- ROW OF HEARTS (row 14, y 112..119): 25 of them ----
    # Tiny 4x4 heart sprite, 5px stride, repeated 25 times.
    heart = [
        "01010",
        "11111",
        "11111",
        "01110",
        "00100",
    ]
    # 25 hearts * (4 + 1) = 125 px wide; centre across 256
    stride = 5
    n_hearts = 25
    total_w = n_hearts * stride - 1
    hx0 = (W - total_w) // 2
    hy0 = 114
    for i in range(n_hearts):
        for r, row in enumerate(heart):
            for c, b in enumerate(row):
                if b == '1':
                    canvas.putpixel((hx0 + i * stride + c, hy0 + r), 0)

    # ---- DIVIDER LINE (row 15, y 120..127) ----
    draw.line([(0, 124), (W - 1, 124)], fill=0, width=1)

    # Below row 15 left blank for BASIC PRINT.

    # ---- Build SCREEN$ binary ----
    # Pixel data: 6144 bytes
    pixels = bytearray(6144)
    px = canvas.load()
    for y in range(H):
        third = y // 64
        y_in_third = y % 64
        line_in_block = y_in_third & 7
        block_in_third = y_in_third >> 3
        row_addr_offset = (third * 2048) + (line_in_block * 256) + (block_in_third * 32)
        for col_byte in range(32):
            byte_val = 0
            for bit in range(8):
                x = col_byte * 8 + bit
                if px[x, y] == 0:  # black -> ink bit set
                    byte_val |= (1 << (7 - bit))
            pixels[row_addr_offset + col_byte] = byte_val

    # Attributes: 768 bytes
    attrs = bytearray(768)
    for cell_y in range(24):
        for cell_x in range(32):
            idx = cell_y * 32 + cell_x
            if cell_y == 0:
                attrs[idx] = ATTR_BANNER
            elif cell_y == 14:
                attrs[idx] = ATTR_HEARTS
            elif 1 <= cell_y <= 13:
                # Avatar cells (cols 1..12) get paper-black ink-white
                if 1 <= cell_x <= 12:
                    attrs[idx] = ATTR_AVATAR
                else:
                    attrs[idx] = ATTR_TITLE_AREA
            elif cell_y == 15:
                attrs[idx] = ATTR_LABEL  # divider
            else:
                # Bottom rows used by PRINT — colour by row
                # 16..23 — labels in cyan, values in white. We'll keep simple: all black/white bright.
                attrs[idx] = ATTR_VALUE
    # Splash a couple of color accents in the bottom (rows 17, 19 etc) using LABEL color for first 9 cols
    for cell_y in (16, 17, 18, 19, 20):
        for cell_x in range(0, 11):
            attrs[cell_y * 32 + cell_x] = ATTR_LABEL

    with open(OUT_PATH, "wb") as f:
        f.write(pixels + attrs)

    # Also save a PNG preview for debugging
    canvas.save("card_preview.png")
    print(f"wrote {OUT_PATH} ({len(pixels) + len(attrs)} bytes)")
    print(f"wrote card_preview.png ({W}x{H})")


if __name__ == "__main__":
    main()
