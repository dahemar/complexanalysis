from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.complex_math import ComplexPoint, add_complex, plot_argand_base64
from app.contour_integral import RADIUS, plot_contour_base64, trace_contour

app = FastAPI(title="Complex Analysis API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ComplexInput(BaseModel):
    real: float = Field(description="Real part")
    imag: float = Field(description="Imaginary part")


class AddRequest(BaseModel):
    a: ComplexInput
    b: ComplexInput


class AddResponse(BaseModel):
    a: dict[str, float]
    b: dict[str, float]
    sum: dict[str, float]
    plot_base64: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/complex/add", response_model=AddResponse)
def complex_add(body: AddRequest) -> AddResponse:
    a = ComplexPoint(real=body.a.real, imag=body.a.imag)
    b = ComplexPoint(real=body.b.real, imag=body.b.imag)
    total = add_complex(a, b)
    return AddResponse(
        a=a.as_dict(),
        b=b.as_dict(),
        sum=total.as_dict(),
        plot_base64=plot_argand_base64(a, b, total),
    )


class ContourTraceRequest(BaseModel):
    n: int = Field(ge=1, le=12, description="Exponent in 1/z^n")
    R: float = Field(default=RADIUS, gt=0, description="Contour radius")
    steps: int = Field(default=240, ge=8, le=480, description="Sample count")


@app.post("/api/contour/trace")
def contour_trace(body: ContourTraceRequest) -> dict:
    data = trace_contour(n=body.n, R=body.R, steps=body.steps)
    data["plot_base64"] = plot_contour_base64(data)
    return data
