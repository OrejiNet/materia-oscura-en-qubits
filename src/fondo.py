"""Fondo conceptual 16:9 del proyecto 'Materia oscura en qubits'.

Elementos (todos inspirados en la física del proyecto):
  - red cósmica de filamentos (campo gaussiano aleatorio),
  - halo de materia oscura ondulatoria con granulación de interferencia (|psi|^2 de muchas ondas),
  - núcleo solitónico con el perfil de Schive et al. (2014): rho ~ [1 + 0.091 (r/rc)^2]^-8,
  - un circuito cuántico tenue (cables de qubits y compuertas).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, Circle

W, H = 1920, 1080
rng = np.random.default_rng(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "fondo_proyecto.png")

y, x = np.mgrid[0:H, 0:W].astype(float)
kx = np.fft.fftfreq(W)[None, :]
ky = np.fft.fftfreq(H)[:, None]
kk = np.sqrt(kx ** 2 + ky ** 2)
kk[0, 0] = 1e-9


def gauss_field(slope, k_cut):
    noise = np.fft.fft2(rng.normal(size=(H, W)))
    f = np.real(np.fft.ifft2(noise * kk ** (slope / 2) * np.exp(-(kk / k_cut) ** 2)))
    return (f - f.mean()) / f.std()


# 1) red cósmica: crestas donde el campo cruza cero -> red de filamentos
g1 = gauss_field(-3.2, 0.02)
g2 = gauss_field(-3.0, 0.012)
web = np.exp(-(g1 / 0.09) ** 2) * (0.55 + 0.45 * np.tanh(g2 + 0.6))
web += 0.5 * np.exp(-(gauss_field(-3.2, 0.03) / 0.06) ** 2) * (g2 > 0.3)

# 2) halo de materia oscura ondulatoria (centro a la derecha, deja espacio para el texto)
cx, cy = 0.70 * W, 0.50 * H
r = np.hypot(x - cx, y - cy)
Rs = 300.0
envelope = 1.0 / ((r / 90 + 0.35) * (1 + r / Rs) ** 2)
speck_spec = np.exp(-((kk - 0.035) / 0.012) ** 2)
psi = np.fft.ifft2(np.fft.fft2(rng.normal(size=(H, W)) + 1j * rng.normal(size=(H, W))) * speck_spec)
granules = np.abs(psi) ** 2
granules /= granules.mean()
halo = envelope * granules

# 3) núcleo solitónico (Schive et al. 2014)
rc = 38.0
soliton = 1.0 / (1 + 0.091 * (r / rc) ** 2) ** 8

dens = 0.45 * web + 1.3 * halo + 4.0 * soliton
img = np.log1p(6 * dens)
img = np.clip(img / np.percentile(img, 99.7), 0, 1) ** 1.15

# brillo suave (glow) del núcleo
glow = np.exp(-(r / 160) ** 2) * 0.22 + np.exp(-(r / 420) ** 2) * 0.12
img = np.clip(img + glow, 0, 1.1)

cmap = LinearSegmentedColormap.from_list("cosmos", [
    (0.00, "#03040b"), (0.18, "#0a1230"), (0.38, "#1b2f6e"), (0.55, "#3d4fb5"),
    (0.72, "#7a62d6"), (0.86, "#c9a6ff"), (1.00, "#ffffff")])

fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img, cmap=cmap, vmin=0, vmax=1.05, interpolation="bilinear")

# estrellas tenues
n = 900
sx, sy = rng.uniform(0, W, n), rng.uniform(0, H, n)
ax.scatter(sx, sy, s=rng.exponential(0.6, n), c="white", alpha=0.55, linewidths=0)

# 4) circuito cuántico tenue (abajo a la izquierda, se desvanece hacia el halo)
wires_y = [H * f for f in (0.70, 0.76, 0.82, 0.88)]
x0, x1 = 60, 0.60 * W
col = "#8fd3ff"
for wy in wires_y:
    xs = np.linspace(x0, x1, 400)
    for a, b in zip(xs[:-1], xs[1:]):
        ax.plot([a, b], [wy, wy], color=col, lw=1.1, alpha=0.32 * (1 - (a - x0) / (x1 - x0)) ** 0.8)
gates = [(170, 0, "H"), (170, 1, "H"), (170, 2, "H"), (170, 3, "H"),
         (330, 0, "QFT"), (520, 1, "Rz"), (520, 3, "Ry"), (700, 2, "Rz")]
for gx, wi, lab in gates:
    fade = 0.75 * (1 - (gx - x0) / (x1 - x0))
    if lab == "QFT":
        top, bot = wires_y[0] - 18, wires_y[3] + 18
        box = FancyBboxPatch((gx - 30, top), 60, bot - top, boxstyle="round,pad=2,rounding_size=6",
                             fc="#0a1230", ec=col, lw=1.2, alpha=fade)
        ax.add_patch(box)
        ax.text(gx, (top + bot) / 2, lab, color=col, alpha=fade, ha="center", va="center",
                fontsize=13, family="monospace")
    else:
        wy = wires_y[wi]
        box = FancyBboxPatch((gx - 18, wy - 16), 36, 32, boxstyle="round,pad=1,rounding_size=5",
                             fc="#0a1230", ec=col, lw=1.2, alpha=fade)
        ax.add_patch(box)
        ax.text(gx, wy, lab, color=col, alpha=fade, ha="center", va="center", fontsize=12, family="monospace")
# CNOT
for cxg, (c, t) in [(420, (0, 2)), (610, (1, 3))]:
    fade = 0.7 * (1 - (cxg - x0) / (x1 - x0))
    ax.plot([cxg, cxg], [wires_y[c], wires_y[t]], color=col, lw=1.2, alpha=fade)
    ax.add_patch(Circle((cxg, wires_y[c]), 5, color=col, alpha=fade))
    ax.add_patch(Circle((cxg, wires_y[t]), 11, fc="none", ec=col, lw=1.2, alpha=fade))
    ax.plot([cxg - 11, cxg + 11], [wires_y[t]] * 2, color=col, lw=1.2, alpha=fade)
for i, wy in enumerate(wires_y):
    ax.text(x0 - 10, wy, f"q{i}", color=col, alpha=0.45, ha="right", va="center", fontsize=11, family="monospace")

# viñeta para oscurecer bordes y que el texto resalte
vig = np.clip(1 - 0.55 * ((x / W - 0.62) ** 2 / 0.35 + (y / H - 0.5) ** 2 / 0.45), 0.25, 1)
ax.imshow(np.dstack([np.zeros_like(vig)] * 3 + [1 - vig]), interpolation="bilinear")

ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")
fig.savefig(OUT, dpi=100, facecolor="#03040b")
print("guardado:", os.path.abspath(OUT))
