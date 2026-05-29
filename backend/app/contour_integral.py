"""Contour integral ∮ 1/z^n dz along z(t) = R e^{it}."""

from __future__ import annotations

import math

from app.complex_math import ComplexPoint

RADIUS = 88.0
TAU = 2 * math.pi
INTEGRAND_SCALE = 42.0
DEFAULT_STEPS = 240


def z_on_circle(R: float, t: float) -> ComplexPoint:
    """Parametrize the circle |z| = R."""
    return ComplexPoint(real=R * math.cos(t), imag=R * math.sin(t))


def integrand(n: int, R: float, t: float) -> ComplexPoint:
    """
    (dz/dt) · 1/z^n for z(t) = R e^{it}, i.e. i R^{1-n} e^{-i(n-1)t}.
    """
    mag = R ** (1 - n)
    angle = -(n - 1) * t
    return ComplexPoint(real=-mag * math.sin(angle), imag=mag * math.cos(angle))


def integral_up_to_t(n: int, R: float, t: float) -> ComplexPoint:
    """
    Exact ∫_0^t (dz/dt) / z^n dt'.

    Visualization convention for this demo:
    - n = 1: show the exact partial integral ∫_0^t i dt' = i t'.
    - n > 1: show the closed-contour result (0) at all times.
    """
    if n == 1:
        return ComplexPoint(0.0, t)
    return ComplexPoint(0.0, 0.0)


def closed_contour_integral(n: int) -> ComplexPoint:
    """∮_{|z|=R} 1/z^n dz with the origin inside the contour."""
    return integral_up_to_t(n, RADIUS, TAU)


def residue_note(n: int) -> str:
    if n == 1:
        return "∮_C 1/z dz = 2πi (simple pole at the origin)."
    return f"∮_C 1/z^{n} dz = 0 (pole at 0 has order {n})."


def _display_extent(path: list[ComplexPoint], n: int) -> float:
    """Fixed vertical scale for the integral panel (avoids jumping while scrubbing θ)."""
    if n == 1:
        return TAU
    return 0.2


def trace_contour(
    n: int,
    R: float = RADIUS,
    steps: int = DEFAULT_STEPS,
) -> dict:
    steps = max(8, min(steps, 480))
    dt = TAU / steps

    path: list[ComplexPoint] = []
    z_points: list[ComplexPoint] = []
    integrand_points: list[ComplexPoint] = []

    for i in range(steps + 1):
        t = min(i * dt, TAU)
        z_points.append(z_on_circle(R, t))
        integrand_points.append(integrand(n, R, t))
        path.append(integral_up_to_t(n, R, t))

    closed = integral_up_to_t(n, R, TAU)
    extent = _display_extent(path, n)

    return {
        "n": n,
        "R": R,
        "tau": TAU,
        "dt": dt,
        "steps": steps,
        "integrand_scale": INTEGRAND_SCALE,
        "display_extent": extent,
        "note": residue_note(n),
        "closed_integral": closed.as_dict(),
        "closed_label": "2πi" if n == 1 else "0",
        "z_points": [p.as_dict() for p in z_points],
        "integrand_points": [p.as_dict() for p in integrand_points],
        "path": [p.as_dict() for p in path],
    }
