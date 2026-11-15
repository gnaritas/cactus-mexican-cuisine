#!/usr/bin/env python3
"""og.png 1200x630 — Cactus Mexican Cuisine Bar & Grill (2x supersample, measured clearances).
Desert-dusk deep green, marigold sun rings, cream Georgia wordmark, saguaro art, papel picado base.
Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

DEEP = (18, 44, 22); GREEN2 = (35, 79, 43); CREAM = (247, 239, 221); GOLD = (224, 161, 50)
TERRA = (191, 68, 41); SAG = (60, 122, 77); SAGL = (127, 174, 116); SAND = (232, 220, 198)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Georgia Bold.ttf", "GeorgiaB.ttf", "Georgia.ttf"], s*S)
cond  = lambda s: font(["Avenir Next Condensed Bold.ttf", "AvenirNextCondensed-Bold.ttf", "Futura.ttc", "HelveticaNeue-Bold.ttf"], s*S)
sans  = lambda s: font(["Avenir Next Medium.ttf", "AvenirNext-Medium.ttf", "HelveticaNeue.ttc", "Arial.ttf"], s*S)

L = 80                      # left text margin
cx0 = 812                   # cactus art box left edge — all text must end left of this
img = Image.new("RGB", (W*S, H*S), DEEP)
d = ImageDraw.Draw(img, "RGBA")

# vertical dusk gradient
for y in range(H*S):
    t = y / (H*S)
    d.line([(0, y), (W*S, y)], fill=(int(DEEP[0]+(GREEN2[0]-DEEP[0])*t*.8),
                                      int(DEEP[1]+(GREEN2[1]-DEEP[1])*t*.8),
                                      int(DEEP[2]+(GREEN2[2]-DEEP[2])*t*.8)))

def P(x, y): return (x*S, y*S)
# marigold sun rings behind the cactus
for i, r in enumerate([96, 128, 162]):
    a = max(28, 70 - i*16)
    d.ellipse([P(cx0+128-r, 300-r), P(cx0+128+r, 300+r)], outline=GOLD+(a,), width=3*S)

# speckle grain
rng = random.Random(2411)
for _ in range(1500):
    x = rng.randint(0, W*S-1); y = rng.randint(0, H*S-1)
    d.point((x, y), fill=(255, 250, 235, rng.randint(3, 12)))

# ---- saguaro (right side), trunk center cxT ----
cxT = cx0 + 128
def capsule(x1, y1, x2, y2, w, color):
    d.line([P(x1, y1), P(x2, y2)], fill=color, width=w*S)
    r = w/2.0
    d.ellipse([P(x1-r, y1-r), P(x1+r, y1+r)], fill=color)
    d.ellipse([P(x2-r, y2-r), P(x2+r, y2+r)], fill=color)
capsule(cxT, 500, cxT, 148, 30, SAG)
# arms: out then up
d.line([P(cxT, 355), P(cxT-34, 355)], fill=SAG, width=24*S)
capsule(cxT-34, 355, cxT-34, 258, 24, SAG)
d.line([P(cxT, 322), P(cxT+34, 322)], fill=SAG, width=24*S)
capsule(cxT+34, 322, cxT+34, 226, 24, SAG)
# ribs
for dx in (-8, 0, 8):
    d.line([P(cxT+dx, 480), P(cxT+dx, 170)], fill=(44, 101, 57), width=3*S)
d.line([P(cxT-38, 330), P(cxT-38, 272)], fill=(44, 101, 57), width=5)
d.line([P(cxT-30, 330), P(cxT-30, 272)], fill=(44, 101, 57), width=5)
d.line([P(cxT+30, 300), P(cxT+30, 242)], fill=(44, 101, 57), width=5)
d.line([P(cxT+38, 300), P(cxT+38, 242)], fill=(44, 101, 57), width=5)
# blossoms
for (bx, by, r) in [(cxT, 138, 8), (cxT-34, 248, 6.6), (cxT+34, 216, 6.6)]:
    d.ellipse([P(bx-r, by-r), P(bx+r, by+r)], fill=GOLD)
    d.ellipse([P(bx-int(r*.4), by-int(r*.4)), P(bx+int(r*.4), by+int(r*.4))], fill=TERRA)
# ground shadow
d.ellipse([P(cxT-92, 506), P(cxT+92, 528)], fill=(10, 26, 14, 140))

# ---- text column ----
y = 132
k = cond(21)
kicker = "WINSTON-SALEM, NC · OPENING NOV 24, 2026"
d.text((L*S, y*S), kicker, font=k, fill=GOLD)
y += 52

t1 = serif(88)
d.text((L*S, y*S), "Cactus", font=t1, fill=CREAM)
y += 104
t2 = serif(46)
d.text((L*S, y*S), "Mexican Cuisine", font=t2, fill=CREAM)
y += 64
d.text((L*S, y*S), "Bar & Grill", font=t2, fill=(224, 161, 50))
y += 92

# gold rule
d.line([P(L, y), P(L+120, y)], fill=GOLD, width=4*S)
y += 26

s1 = sans(23)
d.text((L*S, y*S), "Authentic Mexican · Tex-Mex Favorites", font=s1, fill=SAND)
y += 34
d.text((L*S, y*S), "Handcrafted Drinks · Bar & Grill", font=s1, fill=SAND)

# ---- measured clearance proof ----
def tw(f, s): return f.getlength(s)/S
right = max(tw(k, kicker), tw(t1, "Cactus"), tw(t2, "Mexican Cuisine"),
            tw(t2, "Bar & Grill"), tw(s1, "Authentic Mexican · Tex-Mex Favorites"),
            tw(s1, "Handcrafted Drinks · Bar & Grill")) + L
print("text right edge:", round(right), "| art left edge:", cx0, "| clearance:", cx0 - round(right))
assert right < cx0 - 30, "text collides with cactus art"

# ---- papel picado base ----
bar_y = H - 24
d.line([P(0, bar_y), P(W, bar_y)], fill=GOLD, width=5*S)
cols = [TERRA, GOLD, (44, 101, 57), TERRA]
for i in range(13):
    x0 = 5 + i*96 + 12
    d.polygon([P(x0, bar_y), P(x0+34, bar_y), P(x0+17, H)], fill=cols[i % 4])

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
sz = os.path.getsize(OUT)
print("saved", OUT, f"{W}x{H}", f"{sz/1024:.1f} KB")
assert sz < 500*1024
