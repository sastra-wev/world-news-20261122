#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

Build-time only: draws "The World in One Page" -- a 1024x1024 newspaper
front page summing up the day's world news -- and saves it as entry.png
next to this script. Requires Pillow. The shipped entry program
(main.py) is stdlib-only and simply copies entry.png to /output.

The day's reporting (22 November 2026) behind the page:
- Hero: the COP31 climate summit in Antalya, Turkey ran into a second
  day of overtime, deadlocked over the fossil-fuel wording of its final
  text; a new draft deal was circulated to avert a collapse.
- Panels: Iran struck an industrial site in Bahrain, sparking fires,
  as the blocked Strait of Hormuz kept oil near $90; Mexican special
  forces captured cartel boss Fausto Isidro Meza Flores, "El Chapo
  Isidro", and 11 people died in the violence that followed.
- Briefs and the numbers strip draw on the same day's reporting.
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (247, 243, 233)
PANEL_BG = (238, 231, 214)
INK = (26, 23, 19)
FAINT = (96, 88, 74)
RED = (164, 32, 28)
NAVY = (18, 28, 54)
DARK = (18, 18, 22)
GOLD = (240, 200, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, s, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, s, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, x0=MARGIN, x1=RIGHT, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- art

def draw_hero_art(img, box):
    """A warming globe over a deadlocked negotiating table.

    Dusk-orange sky, a big Earth disc ringed by the sun's heat, a
    thermometer with the mercury near the top, and below, the dark
    silhouettes of delegates seated at a long conference table that
    has run past the clock.
    """
    x0, y0, x1, y1 = box
    art = Image.new("RGB", (x1 - x0, y1 - y0), NAVY)
    d = ImageDraw.Draw(art)
    aw, ah = art.size

    top, bot = (24, 30, 62), (196, 92, 40)
    for i in range(ah):
        t = i / max(ah - 1, 1)
        d.line([(0, i), (aw, i)], fill=tuple(
            int(top[c] + (bot[c] - top[c]) * t) for c in range(3)))

    rng = random.Random(20261122)
    for _ in range(46):  # faint stars in the upper sky
        sx, sy = rng.randrange(aw), rng.randrange(int(ah * 0.34))
        d.point((sx, sy), fill=(205, 210, 230))

    # sun disc behind the globe, with short heat rays
    gx, gy, gr = int(aw * 0.40), int(ah * 0.46), int(ah * 0.335)
    for ang in range(0, 360, 15):
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(gx + (gr + 14) * ca, gy + (gr + 14) * sa),
                (gx + (gr + 30) * ca, gy + (gr + 30) * sa)],
               fill=(255, 166, 66), width=4)
    d.ellipse([gx - gr - 8, gy - gr - 8, gx + gr + 8, gy + gr + 8],
              fill=(255, 150, 54))

    # the globe: ocean disc and simple continent masses
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(38, 84, 138))
    # subtle latitude/longitude grid, clipped to the globe disc and
    # drawn before the continents so the land sits on top of it
    grid_col = (64, 110, 164)  # slightly lighter blue than the ocean
    grid_layer = Image.new("RGB", art.size, (38, 84, 138))
    gd = ImageDraw.Draw(grid_layer)
    for dy_frac, ry_frac in [(-0.45, 0.16), (0.0, 0.22), (0.45, 0.16)]:
        dy = int(gr * dy_frac)  # horizontal (latitude) ellipse arcs
        half = int(math.sqrt(max(gr * gr - dy * dy, 0)))
        ry = int(gr * ry_frac)
        gd.ellipse([gx - half, gy + dy - ry, gx + half, gy + dy + ry],
                   outline=grid_col, width=1)
    for dx_frac, rx_frac in [(-0.45, 0.16), (0.0, 0.22), (0.45, 0.16)]:
        dx = int(gr * dx_frac)  # vertical (longitude) ellipse arcs
        half = int(math.sqrt(max(gr * gr - dx * dx, 0)))
        rx = int(gr * rx_frac)
        gd.ellipse([gx + dx - rx, gy - half, gx + dx + rx, gy + half],
                   outline=grid_col, width=1)
    globe_mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(globe_mask).ellipse(
        [gx - gr, gy - gr, gx + gr, gy + gr], fill=255)
    art.paste(grid_layer, (0, 0), globe_mask)
    d = ImageDraw.Draw(art)
    land = (74, 138, 84)
    d.polygon([(gx - 62, gy - 58), (gx - 18, gy - 74), (gx - 8, gy - 38),
               (gx - 30, gy - 6), (gx - 58, gy - 18)], fill=land)   # Americas N
    d.polygon([(gx - 34, gy + 2), (gx - 10, gy + 4), (gx - 16, gy + 40),
               (gx - 32, gy + 58), (gx - 42, gy + 26)], fill=land)  # Americas S
    d.polygon([(gx + 4, gy - 68), (gx + 58, gy - 64), (gx + 78, gy - 34),
               (gx + 72, gy - 18), (gx + 36, gy - 20),
               (gx + 6, gy - 36)], fill=land)                      # Eurasia (wider right)
    d.polygon([(gx + 16, gy - 14), (gx + 42, gy - 12), (gx + 48, gy + 16),
               (gx + 36, gy + 38), (gx + 22, gy + 42),
               (gx + 12, gy + 12)], fill=land)                     # Africa (more distinct)
    d.polygon([(gx + 50, gy + 4), (gx + 58, gy + 6), (gx + 56, gy + 12),
               (gx + 49, gy + 10)], fill=land)                     # SE Asia 1
    d.polygon([(gx + 61, gy + 12), (gx + 68, gy + 14), (gx + 66, gy + 19),
               (gx + 60, gy + 17)], fill=land)                     # SE Asia 2
    d.polygon([(gx + 44, gy + 15), (gx + 50, gy + 16), (gx + 49, gy + 21),
               (gx + 43, gy + 20)], fill=land)                     # SE Asia 3
    d.polygon([(gx + 54, gy + 20), (gx + 60, gy + 21), (gx + 58, gy + 25),
               (gx + 53, gy + 24)], fill=land)                     # SE Asia 4
    d.polygon([(gx + 48, gy + 28), (gx + 68, gy + 32), (gx + 62, gy + 52),
               (gx + 46, gy + 46)], fill=land)                     # Australia
    # heat tint creeping up from the bottom of the globe
    for i in range(int(gr * 0.9)):
        t = i / max(int(gr * 0.9) - 1, 1)
        y = gy + gr - i
        half = int(math.sqrt(max(gr * gr - (y - gy) ** 2, 0)))
        d.line([(gx - half, y), (gx + half, y)],
               fill=(int(38 + 160 * t * t), int(84 - 30 * t), int(138 - 96 * t)))

    # thermometer, right side, mercury near the top
    tx = aw - 52
    d.rounded_rectangle([tx - 9, 26, tx + 9, ah - 96], radius=9,
                        fill=(238, 234, 220))
    d.rounded_rectangle([tx - 9, 66, tx + 9, ah - 96], radius=9,
                        fill=(206, 48, 36))
    d.ellipse([tx - 17, ah - 122, tx + 17, ah - 88], fill=(206, 48, 36))
    for k in range(5):
        ty = 44 + k * 32
        d.line([(tx - 16, ty), (tx - 9, ty)], fill=(238, 234, 220), width=2)
    d.text((tx - 13, 4), "+2°", font=font(SANS_B, 15), fill=(255, 214, 150))

    # the negotiating table: dark band, seated delegate silhouettes
    table_y = ah - 62
    d.rectangle([0, table_y, aw, ah], fill=(12, 12, 18))
    d.rectangle([0, table_y, aw, table_y + 5], fill=(30, 30, 40))
    rng2 = random.Random(7)
    for k in range(7):
        cx = 26 + k * (aw - 52) // 6 + rng2.randrange(-4, 5)
        d.ellipse([cx - 8, table_y + 12, cx + 8, table_y + 28],
                  fill=(52, 52, 66))                       # head
        d.pieslice([cx - 14, table_y + 24, cx + 14, table_y + 56],
                   180, 360, fill=(52, 52, 66))            # shoulders
        d.rectangle([cx - 11, table_y + 40, cx + 11, table_y + 46],
                    fill=(214, 208, 188))                  # name plate

    img.paste(art, (x0, y0))
    d2 = ImageDraw.Draw(img)
    d2.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cap = "ANTALYA — THE SUMMIT THAT WOULD NOT END"
    cap_size = 13
    cf = font(SANS_B, cap_size)
    while text_w(d2, cap, cf) > (x1 - x0) - 12 and cap_size > 8:
        cap_size -= 1
        cf = font(SANS_B, cap_size)
    cw = text_w(d2, cap, cf)
    d2.rectangle([x0, y1 - 26, x1, y1], fill=(10, 10, 16))
    d2.text((x0 + (x1 - x0 - cw) / 2, y1 - 20), cap, font=cf,
            fill=(238, 234, 220))


def draw_tanks(draw, box):
    """Oil tanks with a fire plume, for the Gulf panel."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(30, 26, 30))
    base = y1 - 8
    for tx, tw, th in [(8, 52, 26), (66, 52, 32), (124, 52, 26)]:
        draw.rectangle([x0 + tx, base - th, x0 + tx + tw, base],
                       fill=(120, 124, 132))
        draw.line([(x0 + tx, base - th), (x0 + tx + tw, base - th)],
                  fill=(170, 174, 182), width=2)
    fx = x0 + 92  # flame over the middle tank
    for wdt, hgt, col in [(24, 30, (214, 84, 30)), (16, 23, (240, 130, 40)),
                          (9, 15, (252, 196, 92))]:
        draw.polygon([(fx - wdt // 2, base - 30), (fx + wdt // 2, base - 30),
                      (fx + 2, base - 30 - hgt), (fx - 4, base - 30 - hgt + 6)],
                     fill=col)
    for sx, sy, sr in [(fx + 13, base - 66, 5), (fx + 22, base - 74, 7)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 64, 70))
    draw.text((x0 + 8, y0 + 5), "BAHRAIN", font=font(SANS_B, 14),
              fill=(255, 205, 170))


def draw_wanted(draw, box):
    """A wanted-poster miniature stamped CAPTURED, for the Mexico panel."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=(226, 214, 182))
    draw.rectangle([x0 + 3, y0 + 3, x1 - 3, y1 - 3], outline=INK, width=2)
    t = "WANTED"
    tf = font(SERIF_B, 17)
    draw.text((x0 + (x1 - x0 - text_w(draw, t, tf)) / 2, y0 + 6), t,
              font=tf, fill=INK)
    cx, cy = (x0 + x1) // 2, y0 + 52
    draw.ellipse([cx - 11, cy - 16, cx + 11, cy + 6], fill=(70, 62, 52))
    draw.pieslice([cx - 19, cy + 2, cx + 19, cy + 38], 180, 360,
                  fill=(70, 62, 52))
    draw.rectangle([cx - 23, cy - 18, cx + 23, cy - 13], fill=(70, 62, 52))
    stamp = "CAPTURED"
    sf = font(SANS_B, 11)
    sw = text_w(draw, stamp, sf) + 10
    sx, sy = cx - sw // 2, y1 - 26
    draw.rectangle([sx, sy, sx + sw, sy + 17], outline=RED, width=2)
    draw.text((sx + 5, sy + 3), stamp, font=sf, fill=RED)


# ---------------------------------------------------------------- the page

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([MARGIN, 30, RIGHT, H - 30], outline=INK, width=2)
    f_mast = font(SERIF_B, 55)
    title = "THE WORLD IN ONE PAGE"
    d.text(((W - text_w(d, title, f_mast)) / 2, 44), title,
           font=f_mast, fill=INK)
    rule(d, 118, width=3)
    rule(d, 124, width=1)
    f_date = font(SANS_B, 17)
    d.text((MARGIN + 6, 134), "SUNDAY 22 NOVEMBER 2026", font=f_date,
           fill=INK)
    tag = "THE DAY'S WORLD NEWS IN A SINGLE IMAGE"
    d.text((RIGHT - 6 - text_w(d, tag, f_date), 134), tag, font=f_date,
           fill=FAINT)
    rule(d, 162, width=2)

    # ---- hero (text left, art right)
    hero_x1 = 606
    d.text((MARGIN + 6, 174), "CLIMATE — ANTALYA, TURKEY",
           font=font(SANS_B, 19), fill=RED)
    f_head = font(SERIF_B, 57)
    while (max(text_w(d, "CLIMATE TALKS", f_head),
               text_w(d, "RUN INTO OVERTIME", f_head))
           > hero_x1 - MARGIN - 10 and f_head.size > 30):
        f_head = font(SERIF_B, f_head.size - 1)
    d.text((MARGIN + 4, 200), "CLIMATE TALKS", font=f_head, fill=INK)
    d.text((MARGIN + 4, 200 + f_head.size + 8), "RUN INTO OVERTIME",
           font=f_head, fill=INK)
    deck = ("The UN climate summit in Antalya ran into a second day of "
            "overtime on Sunday, deadlocked over the fossil-fuel wording "
            "of its final text. A new draft deal was circulated to avert "
            "a collapse of the talks.")
    draw_wrapped(d, (MARGIN + 6, 336), deck, font(SANS, 20), INK,
                 hero_x1 - MARGIN - 12, 27)
    draw_hero_art(img, (622, 174, RIGHT - 6, 472))
    rule(d, 486, width=2)

    # ---- two panels
    py, ph = 498, 148
    mid = (MARGIN + RIGHT) // 2
    for x0, x1 in [(MARGIN + 4, mid - 8), (mid + 8, RIGHT - 4)]:
        d.rectangle([x0, py, x1, py + ph], fill=PANEL_BG)
        d.rectangle([x0, py, x1, py + ph], outline=INK, width=1)

    d.text((MARGIN + 18, py + 10), "THE GULF — IRAN STRIKES",
           font=font(SANS_B, 17), fill=RED)
    draw_tanks(d, (MARGIN + 18, py + 38, MARGIN + 198, py + 132))
    gulf = ("Iran hits an industrial site in Bahrain, sparking fires; "
            "Manama says civilian property was struck. Houthi strikes "
            "follow in Saudi Arabia, and oil holds near $90.")
    draw_wrapped(d, (MARGIN + 212, py + 37), gulf, font(SANS, 14), INK,
                 mid - 8 - (MARGIN + 212) - 8, 19)

    d.text((mid + 26, py + 10), "MEXICO — CARTEL BOSS TAKEN",
           font=font(SANS_B, 17), fill=NAVY)
    draw_wanted(d, (mid + 26, py + 38, mid + 122, py + 132))
    mexico = ("Special forces arrest Fausto Isidro Meza Flores — "
              "\"El Chapo Isidro\", on the FBI's Ten Most Wanted — in "
              "Sinaloa. Eleven die in the violence that follows.")
    draw_wrapped(d, (mid + 138, py + 37), mexico, font(SANS, 14), INK,
                 RIGHT - 4 - (mid + 138) - 10, 19)
    rule(d, py + ph + 14, width=2)

    # ---- briefs
    by = py + ph + 28
    d.text((MARGIN + 6, by), "THE REST OF THE DAY — IN BRIEF",
           font=font(SANS_B, 18), fill=INK)
    by += 32
    briefs = [
        ("KRYVYI RIH", "Russian missile strike on Zelensky's hometown "
         "kills 2 and wounds about 60."),
        ("GULF OF FINLAND", "Ukrainian drones hit a Russian cargo "
         "ship; the vessel catches fire."),
        ("BRUSSELS", "The EU and Indonesia sign a trade deal after "
         "ten years of talks."),
        ("WASHINGTON", "The FBI's criminal database is breached; "
         "Trump confirms the hack."),
        ("NIGERIA", "A boat carrying mourners to a funeral capsizes; "
         "24 people die."),
        ("COPENHAGEN", "Denmark expels a Russian attaché over an "
         "alleged assassination plot."),
        ("BRASILIA", "Bolsonaro is in intensive care with a bowel "
         "obstruction."),
        ("GAZA", "Israeli strikes continue across the strip; an aid "
         "vehicle is hit."),
        ("SCIENCE", "An Anthropic researcher says AI helped prove "
         "the Riemann hypothesis."),
        ("LONDON", "Leeds stun Chelsea 4–1 at Stamford Bridge, a "
         "first win there since 1999."),
    ]
    col_w = (CONTENT_W - 28) // 2
    f_br = font(SANS, 16)
    f_brb = font(SANS_B, 16)
    for i, (place, body) in enumerate(briefs):
        col, row = i % 2, i // 2
        x = MARGIN + 6 + col * (col_w + 16)
        y = by + row * 39
        num_s = f"{i + 1}."
        d.text((x, y), num_s, font=f_brb, fill=RED)
        off0 = max(30, int(text_w(d, num_s, f_brb)) + 8)
        tag_s = place + " — "
        d.text((x + off0, y), tag_s, font=f_brb, fill=INK)
        avail = col_w - off0 - text_w(d, tag_s, f_brb)
        words, line1 = body.split(), ""
        while words:
            trial = words[0] if not line1 else line1 + " " + words[0]
            if text_w(d, trial, f_br) <= avail:
                line1 = trial
                words.pop(0)
            else:
                break
        d.text((x + off0 + text_w(d, tag_s, f_brb), y), line1, font=f_br,
               fill=INK)
        if words:
            line2 = " ".join(words)
            while text_w(d, line2, f_br) > col_w - off0 and " " in line2:
                line2 = line2.rsplit(" ", 1)[0]
            d.text((x + off0, y + 20), line2, font=f_br, fill=INK)

    # ---- numbers strip
    ny = 912
    d.rectangle([MARGIN + 4, ny, RIGHT - 4, ny + 50], fill=DARK)
    stats = [("DAY 2", "of overtime at COP31"),
             ("11", "killed in Sinaloa violence"),
             ("24", "dead in Nigeria boat sinking"),
             ("$89.95", "Brent crude, Hormuz blocked"),
             ("10 YRS", "of EU–Indonesia trade talks")]
    sw = (CONTENT_W - 8) // len(stats)
    for i, (num, lab) in enumerate(stats):
        x = MARGIN + 12 + i * sw
        d.text((x, ny + 5), num, font=font(SANS_B, 21), fill=GOLD)
        d.text((x, ny + 31), lab, font=font(SANS, 12),
               fill=(232, 228, 216))

    foot = "Compiled from the day's reporting · One image, one day"
    d.text(((W - text_w(d, foot, font(SANS, 13))) / 2, 972), foot,
           font=font(SANS, 13), fill=FAINT)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
