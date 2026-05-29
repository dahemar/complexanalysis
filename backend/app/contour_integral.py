"""Contour integral ∮ 1/z^n dz along z(t) = R e^{it}."""

from __future__ import annotations

import base64
import io
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
    t = max(0.0, min(t, TAU))
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


def plot_contour_base64(trace_data: dict) -> str:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    n = trace_data["n"]
    R = trace_data["R"]
    z_points = [ComplexPoint(**p) for p in trace_data["z_points"]]
    integrand_points = [ComplexPoint(**p) for p in trace_data["integrand_points"]]
    path = [ComplexPoint(**p) for p in trace_data["path"]]
    integrand_scale = trace_data["integrand_scale"]
    display_extent = trace_data["display_extent"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3), dpi=100)

    margin = R * 1.3
    ax1.set_xlim(-margin, margin)
    ax1.set_ylim(-margin, margin)
    ax1.set_aspect('equal')
    ax1.grid(True, color='#ebebeb', linewidth=0.5)
    ax1.axhline(y=0, color='#bbb', linewidth=0.8)
    ax1.axvline(x=0, color='#bbb', linewidth=0.8)

    theta = np.linspace(0, 2 * math.pi, 200)
    ax1.plot(R * np.cos(theta), R * np.sin(theta), color='#e0e0e0', linewidth=1.5)

    zx = [p.real for p in z_points]
    zy = [p.imag for p in z_points]
    ax1.plot(zx, zy, color='#e76f51', linewidth=2)

    last_z = z_points[-1]
    ax1.plot(last_z.real, last_z.imag, 'o', color='#e76f51', markersize=6)

    step = max(1, len(z_points) // 20)
    for i in range(0, len(z_points), step):
        zi = z_points[i]
        wi = integrand_points[i]
        if abs(wi.real) < 1e-12 and abs(wi.imag) < 1e-12:
            continue
        dx = integrand_scale * wi.real
        dy = integrand_scale * wi.imag
        ax1.arrow(zi.real, zi.imag, dx, dy, head_width=3, head_length=5,
                  fc='#2a6f9d', ec='#2a6f9d', linewidth=0.6, alpha=0.5)

    ax1.plot(0, 0, 'o', color='#1a1a1a', markersize=3)
    ax1.set_xlabel('Re', fontsize=8)
    ax1.set_ylabel('Im', fontsize=8)
    ax1.set_title(f'Contour z(t) = R e^(iθ), n={n}', fontsize=9)

    pad = max(display_extent, 0.1) * 1.25
    ax2.set_xlim(-pad, pad)
    ax2.set_ylim(-pad, pad)
    ax2.set_aspect('equal')
    ax2.grid(True, color='#ebebeb', linewidth=0.5)
    ax2.axhline(y=0, color='#bbb', linewidth=0.8)
    ax2.axvline(x=0, color='#bbb', linewidth=0.8)

    if len(path) > 1:
        px = [p.real for p in path]
        py = [p.imag for p in path]
        ax2.plot(px, py, color='#5c5ce0', linewidth=2)

    last_p = path[-1]
    ax2.plot(last_p.real, last_p.imag, 'o', color='#5c5ce0', markersize=5)
    ax2.plot(0, 0, 'o', color='#1a1a1a', markersize=3)

    ax2.set_xlabel('Re', fontsize=8)
    ax2.set_ylabel('Im', fontsize=8)
    ax2.set_title(f'∮ 1/z^{n} dz', fontsize=9)

    fig.tight_layout(pad=1.5)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
