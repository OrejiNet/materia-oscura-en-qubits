# Materia oscura en qubits

**Resolución de la ecuación de Schrödinger–Poisson mediante métodos clásicos y cuánticos híbridos**

Proyecto final del Postítulo en Tecnologías Cuánticas, Universidad Adolfo Ibáñez (2026).

- **Autor:** Cristopher Angulo Ahumada
- **Profesor guía:** Dr. Felipe Asenjo Zapata

## Idea

La *materia oscura ondulatoria* (ψDM o *fuzzy dark matter*) propone que la materia oscura está formada por partículas ultralivianas que se comportan como una onda. Su evolución obedece el sistema de Schrödinger–Poisson (en unidades adimensionales):

```
i ∂ψ/∂t = −½ ∇²ψ + a(t) V ψ        (1)  la onda se mueve
∇²V     = |ψ|² − 1                   (2)  la onda genera su propia gravedad
```

Este proyecto resuelve el sistema en 1D con cuatro métodos y compara los resultados:

| Método | Tipo | Descripción |
|---|---|---|
| M1 · Fourier (FFT) | Clásico | Solución de referencia (split-step espectral) |
| M2 · Crank–Nicolson | Clásico | Segunda solución independiente |
| M3 · Fourier cuántica (QFT) | Cuántico híbrido | Evolución con compuertas en Qiskit; gravedad calculada clásicamente |
| M4 · Variacional (VQC) | Cuántico híbrido | Circuito parametrizado optimizado clásicamente |

**Caso de prueba** (Mocz & Szasz 2021, §5): dominio periódico [0, 8], ψ(x, 0) = √(1 + 0.6 sin(πx/4)), evolución hasta t = 3, con 2 a 6 qubits.

**Contribución:** reproducir el caso de prueba como validación y extenderlo con
(i) implementación en Qiskit,
(ii) ruido de medición y modelos de ruido de hardware IBM, y
(iii) comparación sistemática con métodos clásicos.

## Estructura

```
├── docs/         Pauta y prepropuesta del proyecto
├── papers/       Literatura de referencia
├── notebooks/    Notebooks de experimentos
├── src/          Código reutilizable (solvers, circuitos)
└── figures/      Figuras y animaciones generadas
```

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## Plazos

| Fecha | Entrega |
|---|---|
| 17 nov 2026 | Prepropuesta (1 página) |
| 10 ene 2027 | Paper final (máx. 20 páginas) |
| 20 y 27 ene 2027 | Presentación (7 min) |

## Referencias

1. P. Mocz & A. Szasz, *Towards Cosmological Simulations of Dark Matter on Quantum Computers*, [arXiv:2101.05821](https://arxiv.org/abs/2101.05821) (2021).
2. H.-Y. Schive, T. Chiueh & T. Broadhurst, *Cosmic structure as the quantum interference of a coherent dark wave*, Nat. Phys. **10**, 496 (2014). [doi:10.1038/nphys2996](https://doi.org/10.1038/nphys2996)
3. M. Lubasch et al., *Variational quantum algorithms for nonlinear problems*, Phys. Rev. A **101**, 010301 (2020).
4. L. Hui, J. P. Ostriker, S. Tremaine & E. Witten, *Ultralight scalars as cosmological dark matter*, Phys. Rev. D **95**, 043541 (2017).
5. C. W. Bauer, Z. Davoudi, N. Klco & M. J. Savage, *Quantum Simulating Nature's Fundamental Fields* (2024).
