"""HTTP API server for DataGuardian (stdlib-only)."""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple

from dataguardian.audit import AuditEngine
from dataguardian.config import Settings, ensure_data_dir
from dataguardian.storage import SQLiteAuditStore

LOGGER = logging.getLogger(__name__)


class AuditServer(HTTPServer):
    def __init__(self, server_address: Tuple[str, int], settings: Settings):
        self.settings = settings
        ensure_data_dir(settings)
        self.engine = AuditEngine(
            timeout_seconds=settings.audit_timeout_seconds,
            user_agent=settings.user_agent,
        )
        self.store = SQLiteAuditStore(settings.sqlite_path)
        self.store.initialize()
        super().__init__(server_address, AuditHandler)


class AuditHandler(BaseHTTPRequestHandler):
    server: AuditServer

    def _send_json(self, payload: dict, status_code: int = 200) -> None:
        response = json.dumps(payload, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._send_json({"status": "ok"})
            return
        self._send_json({"detail": "Not found"}, status_code=404)

    def do_POST(self) -> None:
        if self.path != "/audit":
            self._send_json({"detail": "Not found"}, status_code=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"detail": "Invalid JSON"}, status_code=400)
            return

        url = payload.get("url")
        html = payload.get("html")
        source_label = payload.get("source_label")
        try:
            result = self.server.engine.audit(url=url, html=html, source_label=source_label)
        except ValueError as exc:
            self._send_json({"detail": str(exc)}, status_code=400)
            return
        except Exception:
            LOGGER.exception("Audit failed")
            self._send_json({"detail": "Audit failed"}, status_code=500)
            return

        self.server.store.save(result)
        self._send_json({"message": "Audit completed", "result": result.to_dict()})

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        LOGGER.info("%s - %s", self.client_address[0], format % args)


def create_server(settings: Settings | None = None, host: str = "127.0.0.1", port: int = 8000) -> AuditServer:
    settings = settings or Settings.load()
    return AuditServer((host, port), settings)


def serve(host: str = "0.0.0.0", port: int = 8000, settings: Settings | None = None) -> None:
    settings = settings or Settings.load()
    logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))
    server = create_server(settings=settings, host=host, port=port)
    LOGGER.info("Starting DataGuardian API on %s:%s", host, port)
    server.serve_forever()


if __name__ == "__main__":
    serve()
