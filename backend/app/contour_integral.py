"""Contour integral ∮ 1/z^n dz along z(t) = R e^{it}."""

from __future__ import annotations

import math
from dataclasses import dataclass

from app.complex_math import ComplexPoint

RADIUS = 88.0
TAU = 2 * math.pi
INTEGRAND_SCALE = 42.0
# Visual scaling for accumulated integral path (Euler sum in the UI plane).
PATH_GAIN = 1.85 * 55 * 0.028
DEFAULT_STEPS = 240


def z_on_circle(R: float, t: float) -> ComplexPoint:
    """Parametrize the circle |z| = R."""
    return ComplexPoint(real=R * math.cos(t), imag=R * math.sin(t))


def integrand(n: int, R: float, t: float) -> ComplexPoint:
    """
    Differential 1/z^n dz along z(t) = R e^{it}.

    With z = R e^{it}, dz = i R e^{it} dt and 1/z^n = R^{-n} e^{-int},
    so the integrand is i R^{1-n} e^{-i(n-1)t}.
    """
    mag = R ** (1 - n)
    angle = -(n - 1) * t
    return ComplexPoint(real=-mag * math.sin(angle), imag=mag * math.cos(angle))


def residue_note(n: int) -> str:
    if n == 1:
        return "For n = 1 the path encloses a simple pole: ∮ 1/z dz = 2πi (nonzero)."
    return f"For n > 1 the pole at 0 has order {n}: the contour integral closes at 0."


def trace_contour(
    n: int,
    R: float = RADIUS,
    steps: int = DEFAULT_STEPS,
) -> dict:
    """Sample the contour and accumulate ∫ f(z) dz from t = 0 to t = 2π."""
    steps = max(8, min(steps, 480))
    dt = TAU / steps

    path: list[ComplexPoint] = [ComplexPoint(0.0, 0.0)]
    z_points: list[ComplexPoint] = []
    integrand_points: list[ComplexPoint] = []

    for i in range(steps + 1):
        t = min(i * dt, TAU)
        z_points.append(z_on_circle(R, t))
        ing = integrand(n, R, t)
        integrand_points.append(ing)
        if i > 0:
            last = path[-1]
            path.append(
                ComplexPoint(
                    real=last.real + PATH_GAIN * ing.real * dt,
                    imag=last.imag + PATH_GAIN * ing.imag * dt,
                )
            )

    return {
        "n": n,
        "R": R,
        "tau": TAU,
        "dt": dt,
        "steps": steps,
        "integrand_scale": INTEGRAND_SCALE,
        "note": residue_note(n),
        "z_points": [p.as_dict() for p in z_points],
        "integrand_points": [p.as_dict() for p in integrand_points],
        "path": [p.as_dict() for p in path],
    }
