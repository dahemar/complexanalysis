from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.complex_math import ComplexPoint, add_complex

app = FastAPI(title="Complex Analysis API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/complex/add", response_model=AddResponse)
def complex_add(body: AddRequest) -> AddResponse:
    a = ComplexPoint(real=body.a.real, imag=body.a.imag)
    b = ComplexPoint(real=body.b.real, imag=body.b.imag)
    total = add_complex(a, b)
    return AddResponse(a=a.as_dict(), b=b.as_dict(), sum=total.as_dict())
