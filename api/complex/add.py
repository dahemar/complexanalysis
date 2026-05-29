from http.server import BaseHTTPRequestHandler
import json
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(_ROOT, "backend"))

from app.complex_math import ComplexPoint, add_complex, plot_argand_base64  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self._respond(204, b"")

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw)
            a = ComplexPoint(real=float(body["a"]["real"]), imag=float(body["a"]["imag"]))
            b = ComplexPoint(real=float(body["b"]["real"]), imag=float(body["b"]["imag"]))
            total = add_complex(a, b)
            payload = {"a": a.as_dict(), "b": b.as_dict(), "sum": total.as_dict(), "plot_base64": plot_argand_base64(a, b, total)}
            self._respond(200, json.dumps(payload).encode("utf-8"))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._respond(400, json.dumps({"error": str(exc)}).encode("utf-8"))

    def _respond(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        if body:
            self.wfile.write(body)
