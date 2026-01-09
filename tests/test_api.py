import json
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

from dataguardian.api import create_server
from dataguardian.config import Settings


class ApiTestCase(unittest.TestCase):
    def _start_server(self, settings):
        server = create_server(settings=settings, host="127.0.0.1", port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        return server, host, port

    def test_api_audit_endpoint(self):
        with TemporaryDirectory() as tmp:
            settings = Settings(
                data_dir=Path(tmp),
                sqlite_path=Path(tmp) / "audit.db",
                audit_timeout_seconds=5,
                user_agent="DataGuardian-Test",
                log_level="INFO",
            )
            server, host, port = self._start_server(settings)

            html = Path("tests/fixtures/sample_page.html").read_text(encoding="utf-8")
            payload = json.dumps({"html": html, "source_label": "https://api-test.local"}).encode("utf-8")
            request = Request(
                f"http://{host}:{port}/audit",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request) as response:
                data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(data["message"], "Audit completed")
            self.assertGreaterEqual(data["result"]["trackers"], 3)

            server.shutdown()
            server.server_close()

    def test_api_healthcheck(self):
        with TemporaryDirectory() as tmp:
            settings = Settings(
                data_dir=Path(tmp),
                sqlite_path=Path(tmp) / "audit.db",
                audit_timeout_seconds=5,
                user_agent="DataGuardian-Test",
                log_level="INFO",
            )
            server, host, port = self._start_server(settings)

            with urlopen(f"http://{host}:{port}/healthz") as response:
                data = json.loads(response.read().decode("utf-8"))

            self.assertEqual(data["status"], "ok")
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
