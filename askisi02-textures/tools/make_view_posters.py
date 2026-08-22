"""Θέα από τα παράθυρα και αφίσες τοίχου."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

from _common import OUT, font

rng = np.random.default_rng(31)


def save(im, name, q=84):
    im.save(os.path.join(OUT, name), quality=q, optimize=True)
    print(f"{name:20} {im.size[0]}x{im.size[1]:5} {os.path.getsize(os.path.join(OUT,name))//1024:4} KB")


# ==================================================== θέα από τα παράθυρα
W, H = 1600, 900
im = Image.new("RGB", (W, H))
px = np.zeros((H, W, 3))

# ουρανός με διαβάθμιση
t = np.linspace(0, 1, H)[:, None]
px[:, :, 0] = 236 - 96 * (1 - t)
px[:, :, 1] = 244 - 62 * (1 - t)
px[:, :, 2] = 250 - 16 * (1 - t)

# σύννεφα
cl = rng.normal(0, 1, (24, 40))
cl = np.asarray(Image.fromarray(((cl - cl.min()) / (np.ptp(cl) + 1e-9) * 255)
                                .astype(np.uint8)).resize((W, H), Image.BICUBIC), float) / 255
mask = np.clip((cl - 0.58) * 2.4, 0, 1) * np.clip(1.5 - 2.4 * t, 0, 1)
px = px * (1 - mask[:, :, None]) + 253 * mask[:, :, None]

im = Image.fromarray(np.clip(px, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)

HZ = int(H * 0.62)                       # γραμμή ορίζοντα

# μακρινή λοφοσειρά
hill = [(0, HZ + 30)]
for x in range(0, W + 40, 40):
    hill.append((x, HZ - 20 + int(38 * np.sin(x / 260) + 16 * np.sin(x / 71))))
hill += [(W, HZ + 30)]
d.polygon(hill, fill=(150, 166, 148))

# έδαφος
d.rectangle([0, HZ, W, H], fill=(126, 142, 96))
for _ in range(2600):                    # υφή χόρτου
    x, y = rng.integers(0, W), rng.integers(HZ, H)
    g = int(96 + 70 * rng.random() + 40 * (y - HZ) / (H - HZ))
    d.line([x, y, x + rng.integers(-2, 3), y - rng.integers(2, 7)],
           fill=(g - 26, g, g - 46), width=1)

# δέντρα: κορμός και συστάδες φυλλώματος
def tree(cx, base, scale, dark):
    tw = max(2, int(9 * scale))
    d.rectangle([cx - tw // 2, base - int(120 * scale), cx + tw // 2, base],
                fill=(74 - dark, 58 - dark, 44 - dark))
    for _ in range(int(26 * scale) + 8):
        r = int(rng.integers(14, 42) * scale)
        ox = int(rng.normal(0, 46 * scale))
        oy = int(rng.normal(0, 34 * scale))
        cy = base - int(190 * scale) + oy
        g = int(rng.integers(58, 112)) - dark
        d.ellipse([cx + ox - r, cy - r, cx + ox + r, cy + r],
                  fill=(g - 22, g + 26, g - 34))

for cx, sc, dk in [(210, 1.35, 6), (520, 1.05, 0), (900, 1.5, 10),
                   (1290, 1.15, 4), (1520, 0.9, 0)]:
    tree(cx, HZ + int(70 * sc), sc, dk)

# χαμηλοί θάμνοι στο πρώτο επίπεδο
for _ in range(30):
    cx = int(rng.integers(0, W)); cy = int(rng.integers(HZ + 90, H))
    r = int(rng.integers(20, 60))
    g = int(rng.integers(70, 115))
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(g - 26, g + 18, g - 40))

im = im.filter(ImageFilter.GaussianBlur(0.6))
save(im, "view_outside.jpg", 80)


# ==================================================== αφίσες τοίχου
def poster_a():
    w, h = 620, 880
    im = Image.new("RGB", (w, h), (243, 241, 234))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(206, 202, 192), width=3)
    # συγκεντρικοί δακτύλιοι, μερικώς αποκομμένοι
    cx, cy = w // 2, int(h * 0.42)
    for i, r in enumerate(range(320, 40, -34)):
        col = (24, 26, 30) if i % 2 == 0 else (243, 241, 234)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.rectangle([0, cy, w, h], fill=(243, 241, 234))
    for i, r in enumerate(range(320, 40, -34)):
        col = (24, 26, 30) if i % 2 == 0 else (243, 241, 234)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col)
    d.rectangle([0, cy - 3, w, cy + 3], fill=(190, 44, 38))
    d.text((44, h - 210), "ΗΧΟΣ", font=font(74, bold=True), fill=(24, 26, 30))
    d.text((44, h - 130), "ΚΑΙ ΕΙΚΟΝΑ", font=font(46, bold=True), fill=(24, 26, 30))
    d.text((46, h - 62), "εργαστηριο εικονικης πραγματικοτητας",
           font=font(20), fill=(120, 122, 126))
    return im


def poster_b():
    w, h = 620, 880
    im = Image.new("RGB", (w, h), (18, 20, 26))
    d = ImageDraw.Draw(im)
    # κατακόρυφες ράβδοι μεταβλητού πλάτους, τύπου κυματομορφής
    x = 40
    rng2 = np.random.default_rng(5)
    while x < w - 40:
        bw = int(rng2.integers(6, 26))
        amp = float(rng2.random())
        top = int(h * 0.20 + (1 - amp) * h * 0.28)
        bot = int(h * 0.72 - (1 - amp) * h * 0.24)
        g = int(120 + 120 * amp)
        d.rectangle([x, top, x + bw, bot], fill=(g, g - 10, max(0, g - 60)))
        x += bw + int(rng2.integers(5, 16))
    d.rectangle([40, int(h * 0.455), w - 40, int(h * 0.462)], fill=(228, 228, 224))
    d.text((44, h - 190), "AVA846", font=font(62, bold=True), fill=(238, 238, 234))
    d.text((46, h - 116), "WEBVR", font=font(30), fill=(150, 152, 158))
    d.text((46, h - 70), "τμημα τεχνων ηχου και εικονας",
           font=font(19), fill=(110, 112, 118))
    return im


save(poster_a(), "poster_a.jpg")
save(poster_b(), "poster_b.jpg")
