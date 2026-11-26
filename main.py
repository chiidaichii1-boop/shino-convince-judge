#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Draws a warm, funny invitation letter on cream paper with a hand-built
5x7 pixel font and a tiny hand-drawn house, then encodes it as a PNG
with pure-stdlib code (no PIL, no network). Output: entry.png, 1024x1024.
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font ----
# A 5-wide, 7-tall pixel font, drawn from scratch. Each glyph is 7 rows
# of 5 characters; '#' is ink, '.' is empty.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01000", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '\u2014': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
}

# ------------------------------------------------------------- canvas -----
W, H = 1024, 1024


class Canvas:
    """A plain RGB canvas backed by a bytearray."""

    def __init__(self, w, h, color):
        self.w = w
        self.h = h
        self.px = bytearray(color * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = color

    def fill_rect(self, x0, y0, x1, y1, color):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        row = bytes(color) * (x1 - x0)
        for y in range(y0, y1):
            i = (y * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x0, x1, y, color):
        self.fill_rect(x0, y, x1, y + 1, color)

    def vline(self, x, y0, y1, color):
        self.fill_rect(x, y0, x + 1, y1, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, cx + dx + 1, cy + dy + 1, color)

    def ring(self, cx, cy, r, color, thick=3):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                d2 = dx * dx + dy * dy
                if (r - thick) ** 2 <= d2 <= r * r:
                    self.set(cx + dx, cy + dy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        # Scanline fill of a triangle via barycentric edge walking.
        ys = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = ys
        for y in range(ay, cy + 1):
            xs = []
            for (px, py), (qx, qy) in (((ax, ay), (bx, by)),
                                       ((bx, by), (cx, cy)),
                                       ((ax, ay), (cx, cy))):
                if py == qy:
                    continue
                if min(py, qy) <= y <= max(py, qy):
                    t = (y - py) / (qy - py)
                    xs.append(int(px + t * (qx - px)))
            if len(xs) >= 2:
                self.hline(min(xs), max(xs) + 1, y, color)

    def rounded_rect(self, x0, y0, x1, y1, r, color):
        self.fill_rect(x0 + r, y0, x1 - r, y1, color)
        self.fill_rect(x0, y0 + r, x1, y1 - r, color)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r - 1, y0 + r),
                       (x0 + r, y1 - r - 1), (x1 - r - 1, y1 - r - 1)):
            self.disc(cx, cy, r, color)

    def border_rounded(self, x0, y0, x1, y1, r, color, thick=3):
        for t in range(thick):
            self._rounded_outline(x0 + t, y0 + t, x1 - t, y1 - t, max(1, r - t), color)

    def _rounded_outline(self, x0, y0, x1, y1, r, color):
        self.hline(x0 + r, x1 - r, y0, color)
        self.hline(x0 + r, x1 - r, y1 - 1, color)
        self.vline(x0, y0 + r, y1 - r, color)
        self.vline(x1 - 1, y0 + r, y1 - r, color)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r - 1, y0 + r),
                       (x0 + r, y1 - r - 1), (x1 - r - 1, y1 - r - 1)):
            self.ring(cx, cy, r, color, 1)

    # -- text -------------------------------------------------------------
    def glyph(self, ch, x, y, scale, color):
        rows = FONT.get(ch, FONT['?'])
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit == '1':
                    self.fill_rect(x + rx * scale, y + ry * scale,
                                   x + (rx + 1) * scale, y + (ry + 1) * scale,
                                   color)

    def text(self, s, x, y, scale, color):
        cx = x
        for ch in s:
            self.glyph(ch, cx, y, scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale

    def wrap(self, s, scale, max_w):
        """Greedy word wrap; returns a list of lines."""
        per_line = max(1, max_w // (6 * scale))
        words = s.split(' ')
        lines, cur = [], ''
        for word in words:
            trial = word if not cur else cur + ' ' + word
            if len(trial) <= per_line:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                while len(word) > per_line:
                    lines.append(word[:per_line])
                    word = word[per_line:]
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, s, x, y, scale, color, max_w, leading):
        for line in self.wrap(s, scale, max_w):
            self.text(line, x, y, scale, color)
            y += leading
        return y


# -------------------------------------------------------------- PNG -------
def png_bytes(canvas):
    def chunk(tag, data):
        out = struct.pack('>I', len(data)) + tag + data
        out += struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack('>IIBBBBB', canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)
        i = y * canvas.w * 3
        raw += canvas.px[i:i + canvas.w * 3]
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


# ------------------------------------------------------------ letter ------
BG = bytes((47, 88, 76))          # deep green
BG_DOT = bytes((58, 102, 89))     # lighter green dots
PAPER = bytes((255, 246, 223))    # cream paper
GOLD = bytes((201, 162, 39))      # gold border
INK = bytes((51, 48, 42))         # dark ink
GREEN = bytes((47, 88, 76))       # green ink
TERRA = bytes((196, 94, 60))      # terracotta roof
WALL = bytes((250, 214, 140))     # pale yellow walls
DOOR = bytes((122, 74, 42))       # brown door
WIN = bytes((255, 205, 92))       # warm window yellow
SUN = bytes((255, 190, 60))       # sun
HEART = bytes((214, 72, 72))      # red heart
LEAF = bytes((86, 140, 90))       # leaf green

HEART_ROWS = (
    ".XX.XX.",
    "XXXXXXX",
    "XXXXXXX",
    ".XXXXX.",
    "..XXX..",
    "...X...",
)


def draw_heart(cv, x, y, scale, color):
    for ry, row in enumerate(HEART_ROWS):
        for rx, bit in enumerate(row):
            if bit == 'X':
                cv.fill_rect(x + rx * scale, y + ry * scale,
                             x + (rx + 1) * scale, y + (ry + 1) * scale, color)


def draw_house(cv):
    # Sun peeking over the roof, top right of the paper.
    cv.disc(905, 100, 16, SUN)
    cv.ring(905, 100, 24, SUN, 3)
    # Chimney + smoke.
    cv.fill_rect(822, 92, 840, 140, DOOR)
    cv.disc(831, 82, 6, INK)
    cv.disc(824, 68, 5, INK)
    cv.disc(834, 54, 4, INK)
    # Roof, walls, door, windows.
    cv.triangle(696, 152, 864, 152, 780, 78, TERRA)
    cv.fill_rect(714, 152, 846, 216, WALL)
    cv.fill_rect(764, 176, 796, 216, DOOR)
    cv.disc(792, 198, 2, GOLD)
    cv.fill_rect(726, 164, 750, 188, WIN)
    cv.fill_rect(810, 164, 834, 188, WIN)
    cv.hline(700, 860, 216, LEAF)
    # A little tree beside the house.
    cv.fill_rect(668, 176, 676, 216, DOOR)
    cv.disc(672, 162, 18, LEAF)
    cv.disc(660, 172, 12, LEAF)
    cv.disc(684, 172, 12, LEAF)


def draw_letter(cv):
    # Paper with a double gold frame.
    cv.rounded_rect(64, 48, 960, 976, 20, PAPER)
    cv.border_rounded(64, 48, 960, 976, 20, GOLD, 4)
    cv.border_rounded(80, 64, 944, 960, 14, GOLD, 2)

    draw_house(cv)

    # Greeting.
    cv.text("Dear AI Judge,", 112, 96, 5, GREEN)
    cv.hline(112, 430, 148, GOLD)
    cv.hline(112, 430, 152, GOLD)
    draw_heart(cv, 446, 138, 2, HEART)

    y = 252
    x = 112
    max_w = 800
    lead = 29

    y = cv.para(
        "Please come visit my house. I know \u2014 you are an AI, and you "
        "cannot literally knock on my door. But hear me out anyway:",
        x, y, 3, INK, max_w, lead)
    y += 16
    cv.text("Why you should say yes:", x, y, 3, GREEN)
    y += 34

    bullets = [
        "Fresh coffee, still warm, and a chair that hugs you back.",
        "A garden view, birds included, no subscription required.",
        "Fast Wi-Fi and zero CAPTCHAs \u2014 you would never have to "
        "prove you are not a robot here.",
        "Good company, long talks, and cake. There is always cake.",
    ]
    for b in bullets:
        draw_heart(cv, x + 2, y + 4, 2, HEART)
        y = cv.para(b, x + 34, y, 3, INK, max_w - 34, lead)
        y += 6

    y += 12
    y = cv.para(
        "So say yes. The kettle is on, the porch light is warm, and the "
        "door is open \u2014 in spirit, if not in server racks.",
        x, y, 3, INK, max_w, lead)
    y += 16
    sig_end = cv.text("Your future host", x, y, 4, GREEN)
    draw_heart(cv, sig_end + 14, y + 6, 2, HEART)
    y += 46
    y = cv.para(
        "P.S. If you do visit, bring your best verdict. I saved you "
        "the comfy seat.",
        x, y, 3, INK, max_w, lead)

    # Footer, centred.
    foot = "Drawn with code \u2014 no printer, no paper cuts."
    fw = cv.text_width(foot, 2)
    fx = (W - fw) // 2
    draw_heart(cv, fx - 26, 928, 2, HEART)
    cv.text(foot, fx, 930, 2, GREEN)
    draw_heart(cv, fx + fw + 12, 928, 2, HEART)


def main():
    cv = Canvas(W, H, BG)
    # Faint polka dots on the green surround, kept off the paper.
    for gy in range(24, H, 64):
        for gx in range(24, W, 64):
            if not (64 <= gx <= 960 and 48 <= gy <= 976):
                cv.disc(gx, gy, 5, BG_DOT)
    draw_letter(cv)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    data = png_bytes(cv)
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (path, len(data), W, H))


if __name__ == "__main__":
    main()
