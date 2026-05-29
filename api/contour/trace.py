from http.server import BaseHTTPRequestHandler
import json
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(_ROOT, "backend"))

from app.contour_integral import RADIUS, plot_contour_base64, trace_contour  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self._respond(204, b"")

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw)
            n = int(body["n"])
            R = float(body.get("R", RADIUS))
            steps = int(body.get("steps", 240))
            if n < 1 or n > 12:
                raise ValueError("n must be between 1 and 12")
            payload = trace_contour(n=n, R=R, steps=steps)
            payload["plot_base64"] = plot_contour_base64(payload)
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
