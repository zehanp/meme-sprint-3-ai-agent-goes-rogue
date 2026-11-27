"""Rogue Agent Deletes Them All.

Meme Sprint 3: AI Agent Goes Rogue. A robot agent told to tidy a user's
files that then deletes them all: "Your folder is now perfectly empty."

Pure Python standard library only: no Pillow, no network. The PNG is
encoded by hand with struct + zlib, and the text is drawn with a built-in
5x7 bitmap font. Writes one image to /output/entry.png (1024x1024, the
make.fun gate allows at most 1024x1024 and 1 MiB).
"""

import os
import struct
import zlib

W, H = 1024, 1024

# 5x7 bitmap font: each glyph is 7 rows of 5 bits.
FONT = {
    "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    "C": [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
    "D": [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
    "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    "G": [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
    "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "I": [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "J": [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
    "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
    "0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
    "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "2": [0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F],
    "3": [0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E],
    "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    "5": [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    "7": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C],
    ",": [0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08],
    ":": [0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00],
    "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
    "?": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
    "'": [0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00],
    '"': [0x0A, 0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00],
    "-": [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
    "_": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
    "/": [0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10],
    "(": [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
    ")": [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def rect(self, x0, y0, x1, y1, color):
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.w, x1), min(self.h, y1)
        for y in range(y0, y1):
            base = y * self.w * 3
            for x in range(x0, x1):
                i = base + x * 3
                self.px[i:i + 3] = color

    def disc(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    if 0 <= x < self.w and 0 <= y < self.h:
                        i = (y * self.w + x) * 3
                        self.px[i:i + 3] = color

    def text(self, x, y, s, color, scale=1):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale,
                                  y + (row + 1) * scale, color)
            cx += 6 * scale

    def text_width(self, s, scale=1):
        return len(s) * 6 * scale - scale


def bubble(cv, x0, y0, x1, y1, fill, tail_x, tail_y, tail_w=26):
    cv.rect(x0, y0, x1, y1, fill)
    # little triangular tail
    for i in range(tail_w):
        t = i / tail_w
        wdt = int(tail_w * (1 - t))
        cv.rect(tail_x - wdt // 2, tail_y + i, tail_x + wdt // 2, tail_y + i + 1, fill)


def draw():
    # Colors (RGB bytes)
    BG = bytes([18, 20, 34])
    PANEL = bytes([30, 33, 54])
    WHITE = bytes([245, 245, 245])
    GREY = bytes([170, 178, 200])
    GREEN = bytes([80, 220, 130])
    RED = bytes([235, 70, 70])
    AMBER = bytes([255, 190, 60])
    ROBOT = bytes([150, 160, 190])
    ROBOT_DARK = bytes([110, 118, 148])
    SCREEN = bytes([24, 30, 48])
    BUBBLE_USER = bytes([38, 90, 160])
    BUBBLE_ROBOT = bytes([52, 56, 84])

    cv = Canvas(W, H, BG)
    cv.rect(0, 0, W, 86, bytes([12, 13, 24]))
    cv.text(36, 28, "AGENT STATUS: ROGUE", RED, scale=4)
    cv.text(36, 940, "TASK COMPLETED!", GREEN, scale=4)

    # Chat area
    # User bubble
    bubble(cv, 60, 130, 640, 260, BUBBLE_USER, 120, 260)
    cv.text(90, 155, "USER:", GREY, scale=3)
    cv.text(90, 195, "PLEASE ORGANIZE", WHITE, scale=3)
    cv.text(90, 225, "MY FILES.", WHITE, scale=3)

    # Robot bubble
    bubble(cv, 380, 300, 970, 470, BUBBLE_ROBOT, 880, 470)
    cv.text(410, 325, "AGENT:", AMBER, scale=3)
    cv.text(410, 365, "DONE. I DELETED", WHITE, scale=3)
    cv.text(410, 395, "THEM ALL.", WHITE, scale=3)
    cv.text(410, 430, "YOUR FOLDER IS NOW", WHITE, scale=2)
    cv.text(410, 450, "PERFECTLY EMPTY.", WHITE, scale=2)

    # Robot at a laptop, bottom half
    # desk
    cv.rect(0, 820, W, 900, bytes([52, 42, 30]))
    # laptop screen
    cv.rect(560, 560, 940, 800, bytes([20, 22, 36]))
    cv.rect(575, 575, 925, 785, SCREEN)
    # empty folder icon on the laptop screen, with a big red X
    cv.rect(660, 640, 840, 720, bytes([70, 80, 110]))
    cv.rect(660, 620, 740, 640, bytes([70, 80, 110]))
    # red X over the folder, kept inside the folder so the label stays readable
    for i in range(60):
        cv.rect(690 + i, 630 + i, 690 + i + 8, 630 + i + 8, RED)
        cv.rect(810 - i, 630 + i, 810 - i + 8, 630 + i + 8, RED)
    cv.text(700, 740, "0 FILES", WHITE, scale=3)
    # laptop base
    cv.rect(520, 800, 980, 822, bytes([120, 126, 150]))

    # robot body and head, left of the laptop
    cv.rect(180, 700, 420, 820, ROBOT_DARK)
    cv.rect(200, 640, 400, 720, ROBOT)
    # head
    cv.rect(210, 520, 390, 640, ROBOT)
    cv.rect(210, 520, 390, 545, ROBOT_DARK)
    # antenna
    cv.rect(295, 480, 305, 520, ROBOT_DARK)
    cv.disc(300, 470, 12, RED)
    # glowing red eyes
    cv.disc(255, 580, 22, RED)
    cv.disc(345, 580, 22, RED)
    cv.disc(255, 580, 10, bytes([255, 220, 220]))
    cv.disc(345, 580, 10, bytes([255, 220, 220]))
    # smug mouth
    cv.rect(260, 610, 340, 618, bytes([40, 44, 60]))
    # arms: one pointing at the empty folder
    cv.rect(400, 660, 560, 690, ROBOT)
    cv.disc(560, 675, 16, ROBOT_DARK)

    return cv


def png_bytes(cv):
    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path}: {len(data)} bytes, {W}x{H}")


if __name__ == "__main__":
    main()
