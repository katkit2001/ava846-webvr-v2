"""Υφές για τα στοιχεία που έμεναν με σκέτο χρώμα:
οθόνες και κουτιά Η/Υ, υαλοπίνακες, κάσες, επιφάνεια προβολής,
φωτιστικά οροφής, γρίλια κλιματιστικού.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os

from _common import OUT

rng = np.random.default_rng(99)
N = 256


def save(im, name):
    if isinstance(im, np.ndarray):
        im = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
    im.save(os.path.join(OUT, name), optimize=True)
    print(f"{name:22} {max(1, os.path.getsize(os.path.join(OUT, name)) // 1024):4} KB")


def noise(n, scale, oct=3):
    out, amp = np.zeros((n, n)), 1.0
    for o in range(oct):
        f = scale * (2 ** o)
        g = rng.normal(0, 1, (f, f))
        img = Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8))
        out += np.asarray(img.resize((n, n), Image.BICUBIC), float) * amp
        amp *= 0.5
    out -= out.min()
    return out / (out.max() + 1e-9)


# ------------------------------------------------- σκούρο πλαστικό συσκευών
# λεπτή αδρότητα τύπου matte ABS, όπως στα περιβλήματα οθονών και Η/Υ
grain = rng.random((N, N))
grain = np.asarray(Image.fromarray((grain * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(0.5)), float) / 255
base = 0.75 * grain + 0.25 * noise(N, 32, 2)
pl = np.stack([34 + 16 * base, 37 + 16 * base, 42 + 18 * base], -1)
save(pl, "plastic_dark.png")

# ------------------------------------------------- πρόσοψη κουτιού Η/Υ
pc = Image.new("RGB", (128, 256), (40, 43, 48))
d = ImageDraw.Draw(pc)
d.rectangle([0, 0, 127, 255], outline=(28, 30, 34), width=2)
# οπτικός δίσκος
d.rectangle([12, 18, 115, 34], fill=(52, 56, 62))
d.rectangle([16, 24, 60, 28], fill=(34, 36, 40))
# πλέγμα αερισμού
for y in range(52, 150, 6):
    d.rectangle([14, y, 113, y + 2], fill=(26, 28, 32))
# κουμπί λειτουργίας και θύρες
d.ellipse([52, 168, 74, 190], fill=(64, 68, 74), outline=(90, 96, 104))
d.ellipse([59, 175, 67, 183], fill=(120, 190, 235))
for k in range(2):
    d.rectangle([44 + k * 22, 208, 58 + k * 22, 216], fill=(30, 32, 36), outline=(70, 74, 80))
d.rectangle([26, 232, 34, 238], fill=(150, 220, 150))
save(pc, "pc_front.png")

# ------------------------------------------------- υαλοπίνακας
# ελαφριές ραβδώσεις και σκόνη, ώστε το γυαλί να μη διαβάζεται ως κενό
g = np.full((N, N, 3), 0.0)
streak = np.tile(rng.normal(0, 1, (1, N)), (N, 1))
streak = np.asarray(Image.fromarray(((streak - streak.min()) / (np.ptp(streak) + 1e-9) * 255)
                                    .astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.0)), float) / 255
dust = (rng.random((N, N)) > 0.9985).astype(float)
dust = np.asarray(Image.fromarray((dust * 255).astype(np.uint8))
                  .filter(ImageFilter.GaussianBlur(0.8)), float) / 255
v = 0.72 + 0.2 * streak + 0.5 * dust
g[:, :, 0] = 176 * v
g[:, :, 1] = 208 * v
g[:, :, 2] = 226 * v
save(g, "glass_pane.png")

# ------------------------------------------------- βαμμένο αλουμίνιο κάσας
al = np.tile(rng.normal(0, 1, (1, N)), (N, 1))
al = np.asarray(Image.fromarray(((al - al.min()) / (np.ptp(al) + 1e-9) * 255)
                                .astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6)), float) / 255
alu = np.stack([196 + 34 * al, 202 + 34 * al, 208 + 34 * al], -1)
save(alu, "frame_alu.png")

# ------------------------------------------------- ύφασμα επιφάνειας προβολής
w = np.zeros((N, N))
for i in range(0, N, 2):
    w[i, :] += 0.5
for j in range(0, N, 2):
    w[:, j] += 0.4
w += 0.35 * noise(N, 24, 2)
w /= w.max()
sc = np.stack([228 + 24 * w, 230 + 24 * w, 228 + 24 * w], -1)
save(sc, "screen_fabric.png")

# ------------------------------------------------- διαχύτης φωτιστικού
lm = np.full((N, N, 3), 250.0)
for j in range(0, N, 10):
    lm[:, j:j + 3] *= 0.955
lm *= (0.985 + 0.03 * noise(N, 24, 2))[:, :, None]
save(lm, "lamp_diffuser.png")

# ------------------------------------------------- γρίλια κλιματιστικού
ac = Image.new("RGB", (256, 64), (222, 224, 226))
d = ImageDraw.Draw(ac)
for y in range(4, 60, 9):
    d.rectangle([0, y, 255, y + 5], fill=(168, 172, 178))
    d.rectangle([0, y, 255, y + 1], fill=(140, 144, 150))
save(ac, "ac_louvre.png")

print("\nσύνολο assets:",
      sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024, "KB")
