"""Figura del caso de prueba con el método clásico M1 (split-step Fourier)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from m1_fourier import solve

OUT = os.path.join(os.path.dirname(__file__), "..", "figures", "m1_colapso_materia_oscura.png")

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#888888", "xtick.color": "#555555", "ytick.color": "#555555",
})

x, t, rho = solve()
i_peak = rho.max(axis=1).argmax()

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1, 1.05]})

# (a) mapa espacio-tiempo: magnitud -> secuencial de un solo tono
im = a1.imshow(rho, origin="lower", aspect="auto", cmap="Blues",
               extent=[x[0], x[-1] + x[1], t[0], t[-1]], vmin=0)
cb = fig.colorbar(im, ax=a1, pad=0.02)
cb.set_label(r"densidad $|\psi|^2$")
cb.outline.set_visible(False)
a1.set_xlabel(r"posición $x$")
a1.set_ylabel(r"tiempo $t$")
a1.set_title("(a) Evolución de la densidad", loc="left", fontsize=11)
a1.axhline(t[i_peak], color="#333333", lw=0.8, ls=":")
a1.text(4.2, t[i_peak] + 0.05, f"máximo colapso, t ≈ {t[i_peak]:.1f}", fontsize=9, color="#333333")

# (b) perfiles en instantes elegidos: tiempo ordenado -> tonos del mismo azul, claro a oscuro
sel = [0.0, 1.0, t[i_peak], 3.0]
shades = ["#9ecae1", "#4292c6", "#08519c", "#08306b"]
for ts, c in zip(sel, shades):
    j = np.abs(t - ts).argmin()
    a2.plot(x, rho[j], color=c, lw=2, label=f"t = {t[j]:.1f}")
a2.set_xlabel(r"posición $x$")
a2.set_ylabel(r"densidad $|\psi|^2$")
a2.set_title("(b) Perfiles en distintos instantes", loc="left", fontsize=11)
a2.grid(axis="y", color="#e5e5e5", lw=0.6)
a2.set_xlim(0, 8)
a2.set_ylim(0, None)
a2.legend(frameon=False, fontsize=9.5)

fig.suptitle("Colapso gravitacional de materia oscura ondulatoria (método clásico M1, N = 256)",
             fontsize=12, x=0.01, ha="left")
fig.tight_layout()
fig.savefig(OUT, dpi=200, facecolor="white")
print("guardado:", os.path.abspath(OUT))
