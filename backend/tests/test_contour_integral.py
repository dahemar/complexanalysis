import math

from app.contour_integral import TAU, closed_contour_integral, trace_contour


def test_n1_closed_is_2pi_i():
    z = closed_contour_integral(1)
    assert abs(z.real) < 1e-12
    assert abs(z.imag - TAU) < 1e-12


def test_n_gt_1_closed_is_zero():
    for n in range(2, 7):
        z = closed_contour_integral(n)
        assert abs(z.real) < 1e-10
        assert abs(z.imag) < 1e-10


def test_trace_endpoint_matches_closed():
    for n in range(1, 7):
        data = trace_contour(n, steps=360)
        end = data["path"][-1]
        closed = data["closed_integral"]
        assert abs(end["real"] - closed["real"]) < 1e-9
        assert abs(end["imag"] - closed["imag"]) < 1e-9


def test_n_gt_1_trace_stays_at_zero():
    for n in range(2, 7):
        data = trace_contour(n, steps=180)
        for p in data["path"]:
            assert abs(p["real"]) < 1e-12
            assert abs(p["imag"]) < 1e-12
