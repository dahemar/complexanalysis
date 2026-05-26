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
    Integrand f(z) dz/dt for f(z) = 1/z^n and z(t) = R e^{it}.

    With z = R e^{it}: dz = i R e^{it} dt and 1/z^n = R^{-n} e^{-int},
    so dz/dt · 1/z^n = i R^{1-n} e^{-i(n-1)t}.
    """
    mag = R ** (1 - n)
    angle = -(n - 1) * t
    return ComplexPoint(real=-mag * math.sin(angle), imag=mag * math.cos(angle))


def closed_contour_integral(n: int) -> ComplexPoint:
    """Exact value of ∮_{|z|=R} 1/z^n dz (R > 0, origin inside)."""
    if n == 1:
        return ComplexPoint(0.0, TAU)  # 2πi
    return ComplexPoint(0.0, 0.0)


def integral_up_to_t(n: int, R: float, t: float, euler: ComplexPoint) -> ComplexPoint:
    """∫_0^t f(z) dz; exact for n = 1 where the integrand is constant i."""
    if n == 1:
        return ComplexPoint(0.0, t)
    return euler


def residue_note(n: int) -> str:
    if n == 1:
        return "∮_C 1/z dz = 2πi (simple pole at the origin)."
    return f"∮_C 1/z^{n} dz = 0 (pole at 0 has order {n})."


def trace_contour(
    n: int,
    R: float = RADIUS,
    steps: int = DEFAULT_STEPS,
) -> dict:
    """Sample the contour and accumulate ∫ f(z) dz from 0 to t."""
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
            euler = ComplexPoint(
                real=last.real + ing.real * dt,
                imag=last.imag + ing.imag * dt,
            )
            path.append(integral_up_to_t(n, R, t, euler))

    closed = closed_contour_integral(n)

    return {
        "n": n,
        "R": R,
        "tau": TAU,
        "dt": dt,
        "steps": steps,
        "integrand_scale": INTEGRAND_SCALE,
        "note": residue_note(n),
        "closed_integral": closed.as_dict(),
        "closed_label": "2πi" if n == 1 else "0",
        "z_points": [p.as_dict() for p in z_points],
        "integrand_points": [p.as_dict() for p in integrand_points],
        "path": [p.as_dict() for p in path],
    }
