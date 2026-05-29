from dataclasses import dataclass
import base64
import io
import math


@dataclass(frozen=True)
class ComplexPoint:
    real: float
    imag: float

    def as_dict(self) -> dict[str, float]:
        return {"real": self.real, "imag": self.imag}


def add_complex(a: ComplexPoint, b: ComplexPoint) -> ComplexPoint:
    return ComplexPoint(real=a.real + b.real, imag=a.imag + b.imag)


def plot_argand_base64(a: ComplexPoint, b: ComplexPoint, total: ComplexPoint) -> str:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    max_abs = max(
        abs(a.real), abs(a.imag),
        abs(b.real), abs(b.imag),
        abs(total.real), abs(total.imag),
        1.0,
    )
    extent = max(2, math.ceil(max_abs * 1.2))

    fig, ax = plt.subplots(figsize=(3, 3), dpi=100)

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect('equal')
    ax.grid(True, color='#ebebeb', linewidth=0.5)
    ax.axhline(y=0, color='#bbb', linewidth=0.8)
    ax.axvline(x=0, color='#bbb', linewidth=0.8)

    ax.quiver(0, 0, a.real, a.imag, angles='xy', scale_units='xy', scale=1,
              color='#e76f51', width=0.012, label='a')
    ax.quiver(0, 0, b.real, b.imag, angles='xy', scale_units='xy', scale=1,
              color='#2a9d8f', width=0.012, label='b')
    ax.quiver(0, 0, total.real, total.imag, angles='xy', scale_units='xy', scale=1,
              color='#5c5ce0', width=0.015, label='z = a+b')

    ax.plot([a.real, total.real], [a.imag, total.imag], '--',
            color='#2a9d8f', linewidth=1, alpha=0.65)
    ax.plot([b.real, total.real], [b.imag, total.imag], '--',
            color='#e76f51', linewidth=1, alpha=0.65)

    ax.set_xticks(range(-extent, extent + 1))
    ax.set_yticks(range(-extent, extent + 1))
    ax.tick_params(labelsize=6)

    ax.legend(loc='lower right', fontsize=7, framealpha=0.9)
    ax.set_xlabel('Re', fontsize=8)
    ax.set_ylabel('Im', fontsize=8)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
