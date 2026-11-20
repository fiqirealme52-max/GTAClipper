#!/usr/bin/env python3
"""Generate the 1080x1920 end-card PNG for the GTA 6 clipper Short.

Pitch (kit wording): "Make clips like this with AI and earn money on make.fun"
+ the bounty page link. Dark Vice City gradient, gold $500 badge, pink brand line.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
TOP = (22, 10, 46)        # deep purple
BOT = (74, 10, 58)        # deep plum/magenta
GOLD = (255, 209, 102)
PINK = (255, 45, 120)
WHITE = (255, 255, 255)
GREY = (180, 170, 190)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

img = Image.new("RGB", (W, H))
px = img.load()
# vertical gradient
for y in range(H):
    t = y / (H - 1)
    r = int(TOP[0] + (BOT[0] - TOP[0]) * t)
    g = int(TOP[1] + (BOT[1] - TOP[1]) * t)
    b = int(TOP[2] + (BOT[2] - TOP[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)
# soft magenta glow in the middle
glow = Image.new("RGB", (W, H), (0, 0, 0))
gp = glow.load()
cx, cy, rad = W // 2, 950, 620
for y in range(max(0, cy - rad), min(H, cy + rad)):
    for x in range(max(0, cx - rad), min(W, cx + rad)):
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / rad
        if d < 1:
            a = (1 - d) * 0.35
            gp[x, y] = (int(120 * a), int(20 * a), int(80 * a))
img = Image.blend(img, Image.blend(img, glow, 0.5), 0.5)

d = ImageDraw.Draw(img)

def center_text(y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return w

# --- gold $500 BOUNTY badge ---
badge_font = ImageFont.truetype(BOLD, 46)
badge_text = "$500 BOUNTY"
bw = d.textlength(badge_text, font=badge_font)
bx0, by0 = (W - bw) / 2 - 34, 400
bx1, by1 = (W + bw) / 2 + 34, 400 + 92
d.rounded_rectangle([bx0, by0, bx1, by1], radius=46, fill=GOLD)
d.text(((W - bw) / 2, by0 + 20), badge_text, font=badge_font, fill=(30, 10, 40))

# --- pitch lines ---
f1 = ImageFont.truetype(BOLD, 74)
f2 = ImageFont.truetype(BOLD, 100)
f3 = ImageFont.truetype(MONO, 40)
y = 780
center_text(y, "Make clips like this", f1, WHITE)
y += 108
center_text(y, "with AI and earn money", f1, WHITE)
y += 108
center_text(y, "on make.fun", f2, PINK)
y += 170
# gold divider
d.line([(W / 2 - 130, y), (W / 2 + 130, y)], fill=GOLD, width=4)
y += 44
center_text(y, "make.fun/bounty/gta6-clipper-01", f3, GOLD)

# --- footer credit ---
ff = ImageFont.truetype(BOLD, 28)
center_text(H - 90, "Footage: GTA VI Trailer 2  |  Rockstar Games", ff, GREY)

img.save("/home/hatch/workspace/makefun/GTAClipper/endcard.png")
print("saved endcard.png", img.size)
