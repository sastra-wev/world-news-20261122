#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Round two of "The World in One Page": the same verified reporting as
the first edition, recomposed around a drawn summit scene. The hero
art now shows the Antalya negotiating hall itself -- delegates still
seated at the long table, the wall clock past midnight, and the draft
text with FOSSIL FUELS struck through in red -- instead of an abstract
globe. Type is larger throughout, the two side panels carry clearer
pictures, and the briefs and the day-in-numbers strip are tightened.

Pillow is a build-time tool only; the shipped program (main.py) needs
nothing beyond the standard library. Run:  python3 render.py
"""

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
PAPER = (247, 241, 227)
CARD = (253, 250, 242)
INK = (17, 19, 25)
SOFT = (74, 72, 64)
RED = (166, 30, 20)
NAVY = (23, 44, 76)
GOLD = (196, 138, 30)
RULE = (17, 19, 25)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_RG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(path, text, limit, start):
    """Largest font at or below `start` points whose text fits `limit`."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size = start
    while size > 10:
        font = load(path, size)
        if probe.textlength(text, font=font) <= limit:
            return font
        size -= 2
    return load(path, 10)


def wrap_pixels(draw, text, font, limit):
    """Greedy word wrap measured in pixels, not characters."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def tracked(draw, xy, text, font, fill, tracking=3):
    """Draw text with extra letter spacing; returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - tracking


def tracked_width(draw, text, font, tracking=3):
    total = sum(draw.textlength(c, font=font) for c in text)
    return total + tracking * (len(text) - 1)


def v_gradient(width, height, top, bottom):
    """A small vertical gradient, stretched to the requested size."""
    column = Image.new("RGB", (1, height))
    px = column.load()
    for row in range(height):
        t = row / max(height - 1, 1)
        px[0, row] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return column.resize((width, height))


page = Image.new("RGB", (SIDE, SIDE), PAPER)
pen = ImageDraw.Draw(page)

# ---------------------------------------------------------------- frame
pen.rectangle([13, 13, SIDE - 13, SIDE - 13], outline=RULE, width=3)
pen.rectangle([20, 20, SIDE - 20, SIDE - 20], outline=RULE, width=1)

# ------------------------------------------------------------- masthead
title_font = shrink_to_fit(SERIF, "THE WORLD IN ONE PAGE", 940, 84)
title = "THE WORLD IN ONE PAGE"
tw = pen.textlength(title, font=title_font)
pen.text(((SIDE - tw) / 2, 30), title, font=title_font, fill=INK)
pen.line([44, 122, SIDE - 44, 122], fill=RULE, width=3)
pen.line([44, 128, SIDE - 44, 128], fill=RULE, width=1)

# ------------------------------------------------------------ dateline
pen.rectangle([44, 140, SIDE - 44, 176], fill=INK)
date_font = load(SANS_BD, 21)
pen.text((58, 147), "SUNDAY 22 NOVEMBER 2026", font=date_font, fill=PAPER)
tag = "THE DAY'S WORLD NEWS · IN A SINGLE IMAGE"
tag_font = load(SANS_BD, 15)
tag_w = tracked_width(pen, tag, tag_font, 2)
tracked(pen, (SIDE - 58 - tag_w, 150), tag, tag_font, PAPER, 2)

# ------------------------------------------------------------ hero text
LEFT = 44
TEXT_W = 568
kick = "CLIMATE SUMMIT — ANTALYA, TURKEY"
kick_font = load(SANS_BD, 22)
kw = tracked_width(pen, kick, kick_font, 2)
tracked(pen, (LEFT, 190), kick, kick_font, RED, 2)
pen.line([LEFT, 222, LEFT + kw, 222], fill=RED, width=2)

head_font = shrink_to_fit(SERIF, "RUN INTO OVERTIME", TEXT_W, 66)
pen.text((LEFT, 232), "CLIMATE TALKS", font=head_font, fill=INK)
pen.text((LEFT, 300), "RUN INTO OVERTIME", font=head_font, fill=INK)

dek = (
    "The UN climate summit in Antalya ran into a second day of overtime "
    "on Sunday, deadlocked over the fossil-fuel wording of its final "
    "text, as a new draft deal circulated to avert a collapse."
)
dek_font = load(SANS, 21)
dy = 382
for line in wrap_pixels(pen, dek, dek_font, TEXT_W):
    pen.text((LEFT, dy), line, font=dek_font, fill=(30, 30, 30))
    dy += 28

# ------------------------------------------------------------- hero art
# The Antalya hall at night: a COP31 sign, the wall clock past
# midnight, the draft deal with its fossil-fuel line struck out, and
# five delegates still seated at the long table.
import math
import os

AX, AY, AX2, AY2 = 636, 190, 980, 486
sky = v_gradient(AX2 - AX - 8, 250, (13, 19, 44), (150, 66, 33))
page.paste(sky, (AX + 4, AY + 4))
pen = ImageDraw.Draw(page)

for i in range(26):  # stars over the hall's glass roof
    sx = AX + 18 + (i * 67) % 300
    sy = AY + 12 + (i * 37) % 56
    pen.ellipse([sx, sy, sx + 2, sy + 2], fill=(214, 216, 200))

pen.rectangle([AX + 20, AY + 18, AX + 152, AY + 52], fill=RED)
sign_font = load(SERIF, 25)
sw = pen.textlength("COP31", font=sign_font)
pen.text((AX + 86 - sw / 2, AY + 22), "COP31", font=sign_font, fill=(252, 246, 230))

# wall clock, reading about 1:55 -- long past the scheduled close
cx, cy, cr = AX + 268, AY + 58, 38
pen.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(245, 241, 229), outline=INK, width=3)
for k in range(12):
    a = math.radians(k * 30)
    r1, r2 = cr - 7, cr - 3
    pen.line([cx + r1 * math.sin(a), cy - r1 * math.cos(a),
              cx + r2 * math.sin(a), cy - r2 * math.cos(a)], fill=INK, width=2)


def hand(angle_deg, length, width, colour):
    a = math.radians(angle_deg)
    pen.line([cx, cy, cx + length * math.sin(a), cy - length * math.cos(a)],
             fill=colour, width=width)


hand(57.5, 20, 5, INK)    # hour hand, nearing two
hand(330, 30, 3, INK)     # minute hand, five to the hour
hand(140, 32, 1, RED)     # second hand
pen.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)

# the draft deal, drawn on its own sheet so it can sit at an angle
sheet = Image.new("RGBA", (146, 106), (0, 0, 0, 0))
sp = ImageDraw.Draw(sheet)
sp.rectangle([2, 2, 143, 103], fill=(252, 250, 244), outline=(110, 106, 96), width=2)
sp.text((10, 7), "DRAFT — FINAL TEXT", font=load(SANS_BD, 10), fill=(90, 86, 78))
for j, wline in enumerate((118, 124, 104, 122)):
    sp.line([10, 26 + j * 10, 10 + wline, 26 + j * 10], fill=(138, 134, 122), width=3)
sp.text((10, 68), "FOSSIL FUELS", font=load(SANS_BD, 17), fill=(24, 24, 30))
sp.line([8, 77, 136, 77], fill=RED, width=4)
sheet = sheet.rotate(8, expand=True, resample=Image.BICUBIC)
page.paste(sheet, (AX + 20, AY + 60), sheet)
pen = ImageDraw.Draw(page)

# the long table and the delegates who have not gone home
pen.polygon([(AX + 12, AY + 208), (AX + 332, AY + 208),
             (AX + 314, AY + 244), (AX + 30, AY + 244)], fill=(56, 39, 29))
pen.line([AX + 12, AY + 208, AX + 332, AY + 208], fill=(120, 88, 58), width=2)
for i, dx in enumerate((58, 118, 178, 238, 296)):
    shade = (24 + 6 * i, 26 + 4 * i, 36 + 3 * i)
    pen.ellipse([AX + dx - 11, AY + 168, AX + dx + 11, AY + 190], fill=shade)
    pen.rounded_rectangle([AX + dx - 23, AY + 188, AX + dx + 23, AY + 210],
                          radius=8, fill=shade)
    pen.rectangle([AX + dx - 9, AY + 216, AX + dx + 9, AY + 223], fill=(238, 232, 214))

pen.rectangle([AX + 4, AY + 254, AX2 - 4, AY2 - 4], fill=INK)
cap = "ANTALYA — THE SUMMIT THAT WOULD NOT END"
cap_font = shrink_to_fit(SANS_BD, cap, AX2 - AX - 30, 16)
cw = pen.textlength(cap, font=cap_font)
pen.text((AX + (AX2 - AX - cw) / 2, AY + 262), cap, font=cap_font, fill=(250, 246, 232))
pen.rectangle([AX, AY, AX2, AY2], outline=INK, width=2)
pen.line([44, 499, SIDE - 44, 499], fill=RULE, width=1)

# --------------------------------------------------------- side panels
def panel(box, header, body, art):
    x0, y0, x1, y1 = box
    pen.rectangle(box, fill=CARD, outline=INK, width=1)
    hf = load(SANS_BD, 19)
    tracked(pen, (x0 + 16, y0 + 13), header, hf, RED, 1)
    art(x0 + 16, y0 + 46)
    bf = load(SANS, 17)
    ty = y0 + 46
    for line in wrap_pixels(pen, body, bf, x1 - (x0 + 162) - 14):
        pen.text((x0 + 162, ty), line, font=bf, fill=(28, 28, 28))
        ty += 21


def bahrain_art(x, y):
    pen.rectangle([x, y, x + 132, y + 104], fill=(22, 28, 46))
    pen.rectangle([x, y + 90, x + 132, y + 104], fill=(10, 11, 15))
    for bx, bw, bh in ((8, 26, 46), (42, 26, 38), (96, 28, 52)):
        pen.rectangle([x + bx, y + 104 - bh - 12, x + bx + bw, y + 92], fill=(7, 9, 13))
    pen.rectangle([x + 76, y + 34, x + 86, y + 92], fill=(7, 9, 13))
    flame = [(x + 81, y + 6), (x + 90, y + 22), (x + 86, y + 34),
             (x + 76, y + 34), (x + 72, y + 22)]
    pen.polygon(flame, fill=(233, 108, 28))
    pen.polygon([(x + 81, y + 16), (x + 86, y + 26), (x + 81, y + 33),
                 (x + 76, y + 26)], fill=(247, 183, 62))
    for gx, gy, gr in ((98, 10, 7), (110, 6, 9), (122, 10, 6)):
        pen.ellipse([x + gx - gr, y + gy - gr, x + gx + gr, y + gy + gr], fill=(96, 96, 102))
    pen.rectangle([x + 4, y + 4, x + 66, y + 21], fill=INK)
    pen.text((x + 8, y + 6), "BAHRAIN", font=load(SANS_BD, 11), fill=(250, 246, 232))


def mexico_art(x, y):
    pen.rectangle([x, y, x + 100, y + 104], fill=(250, 246, 235), outline=INK, width=2)
    wf = load(SERIF, 15)
    ww = pen.textlength("WANTED", font=wf)
    pen.text((x + 50 - ww / 2, y + 6), "WANTED", font=wf, fill=INK)
    pen.ellipse([x + 38, y + 28, x + 62, y + 52], fill=INK)
    pen.pieslice([x + 24, y + 48, x + 76, y + 84], 180, 360, fill=INK)
    stamp = Image.new("RGBA", (88, 24), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([1, 1, 86, 22], outline=RED, width=2)
    sf = load(SANS_BD, 13)
    swd = sd.textlength("CAPTURED", font=sf)
    sd.text(((88 - swd) / 2, 4), "CAPTURED", font=sf, fill=RED)
    stamp = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
    page.paste(stamp, (x + 4, y + 66), stamp)


panel((44, 508, 500, 672), "THE GULF — IRAN STRIKES",
      "Iran strikes an industrial site in Bahrain, sparking fires. "
      "Manama says civilian property was hit; Houthi strikes follow "
      "in Saudi Arabia.", bahrain_art)
pen = ImageDraw.Draw(page)
panel((524, 508, 980, 672), "MEXICO — CARTEL BOSS TAKEN",
      "Special forces arrest Fausto Isidro Meza Flores — \u201cEl Chapo "
      "Isidro\u201d, on the FBI's Ten Most Wanted — in Sinaloa. Eleven "
      "die in the violence that follows.", mexico_art)
pen = ImageDraw.Draw(page)

# --------------------------------------------------------------- briefs
pen.text((44, 684), "THE REST OF THE DAY — IN BRIEF",
         font=load(SANS_BD, 21), fill=INK)
pen.line([44, 712, SIDE - 44, 712], fill=RULE, width=2)
pen.line([44, 712, 330, 712], fill=RED, width=2)

BRIEFS = [
    ("KRYVYI RIH", "Russian missile strike on Zelensky's hometown kills 2 and wounds about 60."),
    ("GULF OF FINLAND", "Ukrainian drones hit a Russian cargo ship; the vessel catches fire."),
    ("BRUSSELS", "The EU and Indonesia sign a trade deal after ten years of talks."),
    ("WASHINGTON", "The FBI's criminal database is breached; Trump confirms the hack."),
    ("NIGERIA", "A boat carrying mourners to a funeral capsizes; 24 people die."),
    ("COPENHAGEN", "Denmark expels a Russian attaché over an alleged assassination plot."),
    ("BRASILIA", "Bolsonaro is in intensive care with a bowel obstruction."),
    ("GAZA", "Israeli strikes continue across the strip; an aid vehicle is hit."),
    ("SCIENCE", "An Anthropic researcher says AI helped prove the Riemann hypothesis."),
    ("LONDON", "Leeds stun Chelsea 4–1 at Stamford Bridge, a first win there since 1999."),
]

num_font = load(SANS_BD, 18)
lead_font = load(SANS_BD, 18)
body_font = load(SANS, 18)


def brief(x, y, idx, lead, rest, width):
    pen.text((x, y), f"{idx}.", font=num_font, fill=RED)
    head = lead + " — "
    pen.text((x + 30, y), head, font=lead_font, fill=INK)
    first_room = width - 30 - pen.textlength(head, font=lead_font)
    words, line, lines = rest.split(), "", []
    room = first_room
    for word in words:
        trial = word if not line else line + " " + word
        if pen.textlength(trial, font=body_font) <= room:
            line = trial
        else:
            lines.append(line)
            line, room = word, width - 30
    if line:
        lines.append(line)
    for j, text in enumerate(lines):
        lx = x + 30 + pen.textlength(head, font=lead_font) if j == 0 else x + 30
        pen.text((lx, y + j * 20), text, font=body_font, fill=(28, 28, 28))
    return y + max(len(lines), 1) * 20 + 5


by = 722
for i in range(5):
    by = brief(44, by, i + 1, *BRIEFS[i], 448)
by = 722
for i in range(5, 10):
    by = brief(524, by, i + 1, *BRIEFS[i], 456)

# -------------------------------------------------------- numbers strip
pen.rectangle([44, 946, SIDE - 44, 996], fill=INK)
STATS = [
    ("DAY 2", "of overtime at COP31"),
    ("11", "killed in Sinaloa violence"),
    ("24", "dead in Nigeria boat sinking"),
    ("$89.95", "Brent crude, Hormuz blocked"),
    ("10 YRS", "of EU–Indonesia trade talks"),
]
stat_font = load(SERIF, 21)
lab_font = load(SANS, 11)
for i, (big, small) in enumerate(STATS):
    sx = 60 + i * 187
    pen.text((sx, 951), big, font=stat_font, fill=GOLD)
    pen.text((sx, 977), small, font=lab_font, fill=(238, 234, 220))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
page.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
