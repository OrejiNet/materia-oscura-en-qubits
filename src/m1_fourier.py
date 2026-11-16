"""M1: solver clásico split-step Fourier para Schrödinger–Poisson en 1D.

Algoritmo 1 de Mocz & Szasz (2021), con a(t) = 1:
    i dpsi/dt = -1/2 d2psi/dx2 + V psi,    d2V/dx2 = |psi|^2 - 1
Caso de prueba (sección 5): x en [0, 8) periódico, psi0 = sqrt(1 + 0.6 sin(pi x / 4)), t en [0, 3].
"""
import numpy as np


def solve(N=256, L=8.0, t_end=3.0, dt=1e-3, n_snap=301):
    x = np.arange(N) * L / N
    k = 2 * np.pi * np.fft.fftfreq(N, d=L / N)
    k2 = k ** 2
    k2_safe = np.where(k2 == 0, 1.0, k2)

    psi = np.sqrt(1 + 0.6 * np.sin(np.pi * x / 4)).astype(complex)

    def potential(psi):
        Vh = -np.fft.fft(np.abs(psi) ** 2 - 1) / k2_safe
        Vh[0] = 0.0
        return np.real(np.fft.ifft(Vh))

    n_steps = int(round(t_end / dt))
    snap_every = n_steps // (n_snap - 1)
    times, rhos = [0.0], [np.abs(psi) ** 2]
    kin = np.exp(-1j * k2 / 2 * dt)

    # esquema "kick-drift-kick" (Strang, 2.º orden)
    V = potential(psi)
    for i in range(1, n_steps + 1):
        psi *= np.exp(-1j * V * dt / 2)
        psi = np.fft.ifft(kin * np.fft.fft(psi))
        V = potential(psi)
        psi *= np.exp(-1j * V * dt / 2)
        if i % snap_every == 0:
            times.append(i * dt)
            rhos.append(np.abs(psi) ** 2)
    return x, np.array(times), np.array(rhos)


if __name__ == "__main__":
    x, t, rho = solve()
    print("masa inicial / final:", rho[0].mean(), rho[-1].mean())
    print("densidad máxima:", rho.max(), "en t =", t[rho.max(axis=1).argmax()])
