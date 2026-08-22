"""Διαδικαστική παραγωγή υφών για τη 2η εργαστηριακή άσκηση (AVA846 WebVR).

Οι υφές παράγονται τοπικά ώστε ο κατάλογος της άσκησης να είναι αυτόνομος
και να μην εξαρτάται από εξωτερικούς συνδέσμους.
"""
import numpy as np
from PIL import Image, ImageFilter
import os

from _common import OUT

rng = np.random.default_rng(7)
N = 256


def save(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(
        os.path.join(OUT, name), optimize=True
    )
    print(name, os.path.getsize(os.path.join(OUT, name)) // 1024, "KB")


def tileable_noise(n, scale, octaves=4):
    """Θόρυβος που επαναλαμβάνεται χωρίς ραφή (μέσω FFT σε χαμηλές συχνότητες)."""
    out = np.zeros((n, n))
    amp = 1.0
    for o in range(octaves):
        f = scale * (2 ** o)
        g = rng.normal(0, 1, (f, f))
        img = Image.fromarray(((g - g.min()) / (np.ptp(g) + 1e-9) * 255).astype(np.uint8))
        img = img.resize((n, n), Image.BICUBIC)
        out += np.asarray(img, dtype=float) * amp
        amp *= 0.5
    out -= out.min()
    return out / (out.max() + 1e-9)


# ---------------------------------------------------------------- δάπεδο
base = np.array([221, 214, 198], dtype=float)
spec = rng.random((N, N))
lino = np.zeros((N, N, 3))
for c in range(3):
    lino[:, :, c] = base[c]
flecks = (spec > 0.986)
lino[flecks] = np.array([150, 142, 124])
flecks2 = (spec < 0.012)
lino[flecks2] = np.array([243, 238, 226])
lino *= (0.94 + 0.12 * tileable_noise(N, 8, 3))[:, :, None]
lino = np.asarray(
    Image.fromarray(np.clip(lino, 0, 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.4)
    ),
    dtype=float,
)
save(lino, "floor_lino.png")

# ---------------------------------------------------------------- τοίχος
plaster = 243 + 9 * (tileable_noise(N, 6, 4) - 0.5)
wall = np.stack([plaster, plaster - 1.5, plaster - 5], axis=-1)
save(wall, "wall_plaster.png")

# normal map του σοβά, για ελαφρύ ανάγλυφο
h = tileable_noise(N, 6, 4)
gy, gx = np.gradient(h * 4.0)
nz = np.ones_like(gx)
ln = np.sqrt(gx ** 2 + gy ** 2 + nz ** 2)
normal = np.stack([(-gx / ln * 0.5 + 0.5), (-gy / ln * 0.5 + 0.5), (nz / ln * 0.5 + 0.5)], -1) * 255
save(normal, "wall_normal.png")

# ---------------------------------------------------------------- οροφή
tile = np.full((N, N, 3), 250.0)
tile *= (0.97 + 0.06 * tileable_noise(N, 16, 2))[:, :, None]
tile[:3, :] *= 0.88
tile[:, :3] *= 0.88
save(tile, "ceiling_tile.png")

# ---------------------------------------------------------------- πάγκος (λαμινέιτ)
x = np.linspace(0, 1, N)
grain = np.zeros((N, N))
for _ in range(90):
    y0 = rng.random()
    w = rng.uniform(0.002, 0.012)
    wob = 0.01 * np.sin(x * rng.uniform(4, 14) * np.pi + rng.random() * 6)
    d = np.abs(((np.linspace(0, 1, N)[:, None] - y0 - wob[None, :] + 0.5) % 1) - 0.5)
    grain += np.exp(-(d / w) ** 2) * rng.uniform(0.2, 0.6)
grain = grain / (grain.max() + 1e-9)
lam = np.stack(
    [235 - 26 * grain, 227 - 30 * grain, 210 - 34 * grain], axis=-1
) * (0.97 + 0.06 * tileable_noise(N, 8, 2))[:, :, None]
save(lam, "desk_laminate.png")

# ---------------------------------------------------------------- ξύλο τραπεζιού
wood = np.stack(
    [206 - 58 * grain, 172 - 62 * grain, 124 - 54 * grain], axis=-1
) * (0.95 + 0.1 * tileable_noise(N, 6, 3))[:, :, None]
save(wood, "wood_table.png")

# ---------------------------------------------------------------- πόρτα
door = np.full((N, N, 3), 250.0)
door *= (0.97 + 0.05 * tileable_noise(N, 10, 3))[:, :, None]
yy, xx = np.mgrid[0:N, 0:N]
panel = ((xx > 34) & (xx < N - 34) & (((yy > 26) & (yy < 116)) | ((yy > 140) & (yy < N - 26))))
edge = np.zeros((N, N), bool)
for d in range(3):
    edge |= (np.abs(xx - 34) == d) | (np.abs(xx - (N - 34)) == d)
    for b in (26, 116, 140, N - 26):
        edge |= (np.abs(yy - b) == d) & (xx > 30) & (xx < N - 30)
door[panel] *= 0.965
door[edge] *= 0.87
save(door, "door_wood.png")

# ---------------------------------------------------------------- ύφασμα κουρτίνας
weave = np.zeros((N, N))
for i in range(0, N, 3):
    weave[i:i + 2, :] += 0.35
for j in range(0, N, 5):
    weave[:, j:j + 2] += 0.5
weave += 0.4 * tileable_noise(N, 12, 3)
weave = weave / (weave.max() + 1e-9)
fab = np.stack([200 + 46 * weave, 178 + 44 * weave, 130 + 40 * weave], axis=-1)
save(fab, "curtain_fabric.png")

# ---------------------------------------------------------------- μέταλλο
brush = np.tile(rng.normal(0, 1, (1, N)), (N, 1))
brush = np.asarray(
    Image.fromarray(((brush - brush.min()) / (np.ptp(brush) + 1e-9) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.8)
    ),
    dtype=float,
)
met = np.stack([brush * 0.22 + 128, brush * 0.22 + 134, brush * 0.22 + 142], axis=-1)
save(met, "metal_brushed.png")

# ---------------------------------------------------------------- οθόνη Η/Υ
scr = np.zeros((N, N, 3))
scr[:, :] = np.array([22, 38, 62])
for i in range(N):
    scr[i, :] *= 1.0 + 0.28 * (1 - i / N)
scr[N - 26:, :] = np.array([16, 22, 34])           # γραμμή εργασιών
for k in range(6):
    x0 = 8 + k * 26
    scr[N - 20:N - 8, x0:x0 + 18] = np.array([70, 104, 150])
win = (slice(30, 150), slice(34, 200))              # παράθυρο εφαρμογής
scr[win] = np.array([238, 240, 244])
scr[30:44, 34:200] = np.array([196, 202, 212])
for r in range(6):
    y0 = 56 + r * 15
    scr[y0:y0 + 4, 46:46 + int(120 * (0.4 + 0.6 * rng.random()))] = np.array([120, 128, 140])
save(scr, "screen_desktop.png")

# ---------------------------------------------------------------- γρασίδι
gr = tileable_noise(N, 10, 4)
grass = np.stack([96 + 44 * gr, 126 + 46 * gr, 74 + 38 * gr], axis=-1)
grass += rng.normal(0, 7, (N, N, 1))
save(grass, "grass.png")

# ---------------------------------------------------------------- ουρανός (equirectangular)
W, H = 1024, 512
t = np.linspace(0, 1, H)[:, None]
sky = np.zeros((H, W, 3))
sky[:, :, 0] = 118 + 130 * t
sky[:, :, 1] = 168 + 84 * t
sky[:, :, 2] = 214 + 32 * t
cl = tileable_noise(256, 6, 4)
cl = np.asarray(Image.fromarray((cl * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float) / 255
mask = np.clip((cl - 0.55) * 2.6, 0, 1) * np.clip(1.35 - 1.7 * t, 0, 1)
sky = sky * (1 - mask[:, :, None]) + 252 * mask[:, :, None]
save(sky, "sky_clouds.png")

print("\nΣύνολο:", sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024, "KB")
