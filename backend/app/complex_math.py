from dataclasses import dataclass


@dataclass(frozen=True)
class ComplexPoint:
    real: float
    imag: float

    def as_dict(self) -> dict[str, float]:
        return {"real": self.real, "imag": self.imag}


def add_complex(a: ComplexPoint, b: ComplexPoint) -> ComplexPoint:
    return ComplexPoint(real=a.real + b.real, imag=a.imag + b.imag)
