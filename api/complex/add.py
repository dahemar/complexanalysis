from http.server import BaseHTTPRequestHandler
import json


def _add(a: dict, b: dict) -> dict[str, float]:
    return {
        "real": float(a["real"]) + float(b["real"]),
        "imag": float(a["imag"]) + float(b["imag"]),
    }


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self._respond(204, b"")

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw)
            a = body["a"]
            b = body["b"]
            payload = {
                "a": {"real": float(a["real"]), "imag": float(a["imag"])},
                "b": {"real": float(b["real"]), "imag": float(b["imag"])},
                "sum": _add(a, b),
            }
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
