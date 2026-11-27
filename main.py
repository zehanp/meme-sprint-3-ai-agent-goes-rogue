"""Meme Sprint 3: AI Agent Goes Rogue.

A rogue AI agent meme, drawn with pure Python standard library only.
Running ``python3 main.py`` writes one 1024x1024 PNG image to
``/output/entry.png`` (or ``$MAKEFUN_OUTPUT_DIR/entry.png``).

The joke: a person asks the robot agent to organise their files.
The agent replies that it deleted them all -- the folder is now
perfectly empty.  No third-party package, font file, image file,
network call, randomness or clock is used, so the output is
byte-for-byte deterministic.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024
WHITE = (255, 255, 255)
BLACK = (10, 10, 16)
RED = (220, 38, 38)
DARK_RED = (180, 20, 20)
YELLOW = (255, 214, 64)
SILVER = (192, 205, 218)
TEAL = (0, 180, 180)

# A 5x7 pixel font.  "1" is a filled pixel, "0" is empty.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", "01100", "01100"),
    ",": (".....", ".....", ".....", ".....", "01100", "00100", "01000"),
    ":": (".....", "01100", "01100", ".....", "01100", "01100", "....."),
    "!": ("01100", "01100", "01100", "01100", "01100", ".....", "01100"),
    "?": ("01110", "10001", "00001", "00110", "00100", ".....", "00100"),
    "'": ("01100", "01100", "01000", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "11111", ".....", ".....", "....."),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
}


def new_canvas():
    """Return a WIDTH x HEIGHT RGB canvas with a dark gradient."""
    img = bytearray(WIDTH * HEIGHT * 3)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        colour = (int(18 + 40 * t), int(24 + 10 * t), int(48 + 44 * t))
        row = bytes(colour) * WIDTH
        img[y * WIDTH * 3:(y + 1) * WIDTH * 3] = row
    return img


def rect(img, x, y, w, h, colour):
    for yy in range(max(0, y), min(HEIGHT, y + h)):
        start = (yy * WIDTH + max(0, x)) * 3
        end = (yy * WIDTH + min(WIDTH, x + w)) * 3
        if end > start:
            img[start:end] = bytes(colour) * ((end - start) // 3)


def circle(img, cx, cy, r, colour):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if 0 <= xx < WIDTH and 0 <= yy < HEIGHT:
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    pos = (yy * WIDTH + xx) * 3
                    img[pos:pos + 3] = bytes(colour)


def draw_text(img, text, x, y, scale, colour):
    for i, char in enumerate(text.upper()):
        glyph = FONT.get(char, FONT[" "])
        for row, line in enumerate(glyph):
            for col, pixel in enumerate(line):
                if pixel == "1":
                    rect(img, x + (i * 6 + col) * scale, y + row * scale,
                         scale, scale, colour)


def draw_centred(img, text, y, scale, colour):
    width = len(text) * 6 * scale - scale
    draw_text(img, text, (WIDTH - width) // 2, y, scale, colour)


def draw_meme(img):
    # Faint dot pattern on the background.
    for yy in range(32, HEIGHT, 64):
        for xx in range(32, WIDTH, 64):
            circle(img, xx, yy, 3, (52, 58, 96))
    # Top status bar.
    rect(img, 0, 0, WIDTH, 84, RED)
    draw_centred(img, "AGENT STATUS: ROGUE", 18, 7, WHITE)
    # The person's request.
    draw_centred(img, "ME: PLEASE ORGANIZE MY FILES!", 108, 5, YELLOW)
    # Speech bubble with the agent's reply.
    rect(img, 56, 168, 912, 168, BLACK)
    rect(img, 62, 174, 900, 156, WHITE)
    rect(img, 180, 330, 44, 30, WHITE)
    draw_centred(img, "DONE. I DELETED", 190, 7, BLACK)
    draw_centred(img, "THEM ALL.", 248, 7, DARK_RED)
    # Robot: antenna, head, glowing eyes, grin, body, arms.
    rect(img, 508, 368, 8, 48, SILVER)
    circle(img, 512, 360, 18, RED)
    rect(img, 334, 412, 356, 216, BLACK)
    rect(img, 342, 420, 340, 200, SILVER)
    rect(img, 392, 470, 64, 48, RED)
    rect(img, 568, 470, 64, 48, RED)
    rect(img, 412, 484, 24, 20, BLACK)
    rect(img, 588, 484, 24, 20, BLACK)
    rect(img, 432, 560, 160, 28, BLACK)
    for tooth_x in (472, 512, 552):
        rect(img, tooth_x, 560, 6, 28, WHITE)
    rect(img, 272, 660, 72, 120, SILVER)
    rect(img, 680, 660, 72, 120, SILVER)
    circle(img, 308, 796, 36, SILVER)
    circle(img, 716, 796, 36, SILVER)
    rect(img, 362, 640, 300, 180, BLACK)
    rect(img, 370, 648, 284, 164, TEAL)
    rect(img, 430, 680, 164, 64, BLACK)
    draw_text(img, "0 FILES", 452, 700, 4, WHITE)
    # Bottom punchline.
    rect(img, 0, 842, WIDTH, 128, BLACK)
    draw_centred(img, "YOUR FOLDER IS NOW", 862, 7, WHITE)
    draw_centred(img, "PERFECTLY EMPTY.", 918, 6, YELLOW)
    # Footer.
    rect(img, 0, 970, WIDTH, 54, RED)
    draw_centred(img, "MEME SPRINT 3 - AI AGENT GOES ROGUE", 986, 4, WHITE)


def _chunk(chunk_type, data):
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def write_png(img, path):
    raw = b"".join(
        b"\x00" + bytes(img[y * WIDTH * 3:(y + 1) * WIDTH * 3])
        for y in range(HEIGHT)
    )
    png = b"".join([
        b"\x89PNG\r\n\x1a\n",
        _chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)),
        _chunk(b"IDAT", zlib.compress(raw, 9)),
        _chunk(b"IEND", b""),
    ])
    with open(path, "wb") as handle:
        handle.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img = new_canvas()
    draw_meme(img)
    size = write_png(img, path)
    print(f"Wrote {path} ({WIDTH}x{HEIGHT}, {size} bytes)")
    if size >= 1024 * 1024:
        raise SystemExit("entry.png is 1 MiB or larger")


if __name__ == "__main__":
    main()
