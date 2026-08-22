"""Πρόσθετες διαδικαστικές υφές για τη 2η εργαστηριακή άσκηση (AVA846 WebVR)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

from _common import OUT, font

rng = np.random.default_rng(21)
N = 256


def save(im, name):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
    im.save(os.path.join(OUT, name), optimize=True)
    print(name, max(1, os.path.getsize(os.path.join(OUT, name)) // 1024), "KB")


def noise(n, scale, octaves=3):
    out, amp = np.zeros((n, n)), 1.0
    for o in range(octaves):
        f = scale * (2 ** o)
        g = rng.normal(0, 1, (f, f))
        img = Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8))
        out += np.asarray(img.resize((n, n), Image.BICUBIC), float) * amp
        amp *= 0.5
    out -= out.min()
    return out / (out.max() + 1e-9)


# --------------------------------------------------------------- πληκτρολόγιο
kb = Image.new("RGB", (N, N), (38, 41, 46))
d = ImageDraw.Draw(kb)
cols, rows = 15, 5
for r in range(rows):
    for c in range(cols):
        x0 = 6 + c * ((N - 12) / cols)
        y0 = 40 + r * ((N - 56) / rows)
        w = (N - 12) / cols - 3
        h = (N - 56) / rows - 3
        if r == rows - 1 and 4 <= c <= 9:
            if c != 4:
                continue
            w = w * 6 + 15
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=3, fill=(62, 66, 73))
        d.line([x0, y0 + h, x0 + w, y0 + h], fill=(28, 30, 34), width=1)
save(kb, "keyboard.png")

# --------------------------------------------------------------- ύφασμα καθίσματος
w1 = np.zeros((N, N))
for i in range(0, N, 4):
    w1[i:i + 2, :] += 0.5
for j in range(0, N, 4):
    w1[:, j:j + 2] += 0.35
w1 += 0.5 * noise(N, 16, 2)
w1 /= w1.max()
fab = np.stack([26 + 26 * w1, 29 + 27 * w1, 35 + 30 * w1], -1)
save(fab, "chair_fabric.png")

# --------------------------------------------------------------- θερμαντικό σώμα
rad = np.full((N, N, 3), 246.0)
for j in range(0, N, 16):
    rad[:, j:j + 3] *= 0.86
    rad[:, j + 3:j + 5] *= 0.96
rad[:14, :] *= 0.93
rad[N - 14:, :] *= 0.93
save(rad, "radiator_fins.png")

# --------------------------------------------------------------- οθόνη: επεξεργαστής κώδικα
ed = Image.new("RGB", (N, N), (24, 28, 38))
d = ImageDraw.Draw(ed)
d.rectangle([0, 0, N, 18], fill=(34, 40, 52))
d.rectangle([0, 18, 40, N], fill=(20, 24, 32))
palette = [(122, 176, 220), (196, 152, 214), (156, 200, 140), (216, 178, 120), (150, 160, 176)]
y = 26
while y < N - 10:
    ind = rng.integers(0, 4) * 9
    x = 46 + ind
    for _ in range(rng.integers(1, 4)):
        w = int(rng.integers(14, 60))
        if x + w > N - 8:
            break
        d.rectangle([x, y, x + w, y + 4], fill=palette[rng.integers(0, len(palette))])
        x += w + 6
    y += 11
save(ed, "screen_code.png")

# --------------------------------------------------------------- οθόνη: πρόγραμμα εικόνας
ph = Image.new("RGB", (N, N), (46, 48, 54))
d = ImageDraw.Draw(ph)
d.rectangle([0, 0, N, 20], fill=(64, 68, 76))
for r in range(3):
    for c in range(4):
        x0, y0 = 12 + c * 60, 34 + r * 68
        base = np.zeros((56, 52, 3))
        hue = rng.random()
        for i in range(56):
            base[i, :] = np.array([
                120 + 110 * np.sin(6.28 * hue + i / 40),
                110 + 100 * np.sin(6.28 * hue + 2 + i / 34),
                120 + 100 * np.sin(6.28 * hue + 4 + i / 46)])
        ph.paste(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)), (x0, y0))
        d.rectangle([x0, y0, x0 + 51, y0 + 55], outline=(90, 94, 102))
save(ph, "screen_photo.png")

# --------------------------------------------------------------- πινακίδα θύρας
sign = Image.new("RGB", (256, 128), (247, 247, 245))
d = ImageDraw.Draw(sign)
d.rectangle([0, 0, 255, 127], outline=(178, 182, 188), width=3)
d.rectangle([0, 0, 255, 30], fill=(46, 72, 108))
d.text((12, 7), "ΚΤΙΡΙΟ Γ΄", font=font(17), fill=(255, 255, 255))
d.text((16, 44), "ΥΚ 1", font=font(46, bold=True), fill=(38, 42, 50))
d.text((132, 62), "Υπολογιστικό\nΚέντρο 01", font=font(14), fill=(96, 102, 112))
save(sign, "door_sign.png")

# --------------------------------------------------------------- ανακοίνωση τοίχου
po = Image.new("RGB", (200, 280), (252, 252, 250))
d = ImageDraw.Draw(po)
d.rectangle([0, 0, 199, 279], outline=(208, 210, 214), width=2)
d.rectangle([14, 16, 185, 60], fill=(178, 62, 54))
d.text((24, 26), "ΩΡΑΡΙΟ", font=font(24, bold=True), fill=(255, 255, 255))
y = 78
for _ in range(11):
    d.rectangle([20, y, 20 + int(rng.integers(60, 160)), y + 6], fill=(126, 132, 142))
    y += 16
d.rectangle([20, 244, 96, 262], fill=(46, 72, 108))
save(po, "poster_notice.png")

# --------------------------------------------------------------- φλοιός δέντρου
bk = noise(N, 4, 4)
streak = np.tile(rng.normal(0, 1, (N, 1)), (1, N))
streak = np.asarray(Image.fromarray(((streak - streak.min()) / (np.ptp(streak) + 1e-9) * 255)
                                    .astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), float) / 255
b = 0.55 * bk + 0.45 * streak
bark = np.stack([76 + 62 * b, 60 + 50 * b, 44 + 36 * b], -1)
save(bark, "bark.png")

# --------------------------------------------------------------- πλακάκια διαδρόμου
tl = np.full((N, N, 3), 198.0)
tl *= (0.94 + 0.11 * noise(N, 8, 3))[:, :, None]
for k in (0, 128):
    tl[k:k + 4, :] = 168
    tl[:, k:k + 4] = 168
save(tl, "corridor_tile.png")

print("\nΣύνολο assets:",
      sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024, "KB")
