"""Render one Thinkless Instagram Story (1080x1920 JPEG).

usage: python3 tools/make_story.py spec.json out.jpg

spec.json fields:
  layout: "quote" | "statement" | "contrast" | "question" | "tip"
  lines:  list of text lines (quote/statement/question/tip)
  gold:   phrase (case-insensitive) whose line is drawn in gold
  label:  small kicker text above the main text (optional)
  a_label, a_lines, b_label, b_lines: for layout "contrast"
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = lambda n: os.path.join(ROOT, "assets", "fonts", n)
FB, FS, FM = FONT("Inter-Bold.otf"), FONT("Inter-SemiBold.otf"), FONT("Inter-Medium.otf")
CHAR = os.path.join(ROOT, "assets", "character.png")
W, H = 1080, 1920
GOLD, WHITE, GREY, DIM = (255, 182, 32), (242, 242, 242), (150, 150, 150), (110, 110, 110)
SAFE_TOP, SAFE_BOTTOM = 300, 1620   # keep clear of Story header and reply bar


def tw(t, f, tr): return sum(f.getlength(c) for c in t) + tr * max(0, len(t) - 1)


class Canvas:
    def __init__(self, glow_y):
        bg = Image.new("RGB", (W, H), (9, 9, 10))
        gl = Image.new("L", (W, H), 0)
        ImageDraw.Draw(gl).ellipse((W / 2 - 650, glow_y - 650, W / 2 + 650, glow_y + 650), fill=70)
        gl = gl.filter(ImageFilter.GaussianBlur(220))
        self.im = Image.composite(Image.new("RGB", (W, H), (70, 48, 12)), bg, gl)
        self.glow = Image.new("RGB", (W, H), (0, 0, 0))

    def character(self, size, cy):
        ic = Image.open(CHAR).convert("RGB").resize((size, size), Image.LANCZOS)
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).ellipse((10, 10, size - 10, size - 10), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(30))
        tile = Image.new("RGB", (W, H), (0, 0, 0)); tile.paste(ic, ((W - size) // 2, cy - size // 2), m)
        self.im = ImageChops.screen(self.im, tile)

    def text(self, y, t, f, col, tr=2, glow=False, x=None):
        d = ImageDraw.Draw(self.im); g = ImageDraw.Draw(self.glow)
        x = (W - tw(t, f, tr)) / 2 if x is None else x
        for ch in t:
            d.text((x, y), ch, font=f, fill=col)
            if glow: g.text((x, y), ch, font=f, fill=(255, 150, 20))
            x += f.getlength(ch) + tr

    def block(self, lines, top, size, gold=None, maxw=900, font=FB):
        f = ImageFont.truetype(font, size)
        while max(tw(l, f, 2) for l in lines) > maxw and size > 40:
            size -= 4; f = ImageFont.truetype(font, size)
        lh = int(size * 1.22)
        for i, l in enumerate(lines):
            isg = bool(gold) and gold.lower() in l.lower()
            self.text(top + i * lh, l, f, GOLD if isg else WHITE, glow=isg)
        return top + len(lines) * lh

    def rule(self, y):
        ImageDraw.Draw(self.im).line((W / 2 - 40, y, W / 2 + 40, y), fill=GOLD, width=3)

    def kicker(self, y, t):
        self.text(y, t.upper(), ImageFont.truetype(FS, 34), GOLD, tr=6)

    def save(self, out):
        self.im = ImageChops.screen(self.im, self.glow.filter(ImageFilter.GaussianBlur(20)).point(lambda v: int(v * 0.7)))
        h = "@thinkless.mind"; fsm = ImageFont.truetype(FM, 34)
        self.text(1660, h, fsm, GREY)
        self.im.save(out, quality=92)


def block_height(n, size): return n * int(size * 1.22)


def render(spec, out):
    L = spec["layout"]
    if L == "quote":          # text top, character bottom
        c = Canvas(1350); c.character(600, 1300)
        y = 600 - block_height(len(spec["lines"]), 78) // 2
        if spec.get("label"): c.kicker(y - 90, spec["label"])
        e = c.block(spec["lines"], y, 78, spec.get("gold")); c.rule(e + 40)
    elif L == "statement":    # big centered text only
        c = Canvas(900)
        y = 900 - block_height(len(spec["lines"]), 88) // 2
        if spec.get("label"): c.kicker(y - 100, spec["label"])
        e = c.block(spec["lines"], y, 88, spec.get("gold")); c.rule(e + 44)
    elif L == "question":     # question to the viewer, small character
        c = Canvas(1000); c.character(440, 1330)
        c.kicker(470, spec.get("label") or "Be honest")
        e = c.block(spec["lines"], 560, 76, spec.get("gold")); c.rule(e + 40)
    elif L == "tip":          # "try this today" micro-action
        c = Canvas(1100)
        c.kicker(640, spec.get("label") or "Try this today")
        e = c.block(spec["lines"], 730, 72, spec.get("gold"), font=FB)
        c.rule(e + 40)
        if spec.get("sub"):
            c.block(spec["sub"], e + 100, 44, None, font=FM)
    elif L == "contrast":     # overthinking says vs reality says
        c = Canvas(960)
        c.kicker(600, spec.get("a_label", "Overthinking says"))
        e = c.block(spec["a_lines"], 670, 64, None, font=FS)
        ImageDraw.Draw(c.im).line((W / 2 - 300, e + 60, W / 2 + 300, e + 60), fill=(60, 60, 60), width=2)
        c.kicker(e + 130, spec.get("b_label", "Reality says"))
        e2 = c.block(spec["b_lines"], e + 200, 64, spec.get("gold") or spec["b_lines"][-1])
        c.rule(e2 + 40)
    else:
        raise SystemExit(f"unknown layout {L}")
    c.save(out)


if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
